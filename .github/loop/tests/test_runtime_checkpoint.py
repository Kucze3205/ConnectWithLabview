import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

import fakes
from runtime_checkpoint import Checkpoint
from tool_broker import Broker


class ArchiveStore(Checkpoint):
    def __init__(self, broker, directory):
        super().__init__(broker, 'owner/repo', 11)
        self.storage = Path(directory)

    def command(self, command, **kwargs):
        if command[0] != 'gh':
            return super().command(command, **kwargs)
        if command[2] == 'upload':
            source = Path(command[4])
            shutil.copy(source, self.storage / source.name)
        if command[2] == 'download':
            name, target = command[command.index('--pattern') + 1], command[command.index('--dir') + 1]
            shutil.copy(self.storage / name, Path(target, name))
        return subprocess.CompletedProcess(command, 0, '', '')


class CheckpointTest(unittest.TestCase):
    def setUp(self):
        self.world = fakes.worker_world()
        self.addCleanup(self.world.close)
        self.work = Path(self.world.tmp, 'checkpoint-work')
        fakes.sh(self.world.tmp, 'git', 'clone', '-q', '-c', 'core.autocrlf=false', self.world.origin, str(self.work))
        (self.work / '.git/info/exclude').write_text('.session/\n')
        (self.work / 'src').mkdir(exist_ok=True)
        self.broker = Broker(self.work, {'tools': ['Read', 'Write'], 'write': ['src/**']},
                             {'protected': ['engine.yml', '.github/'], 'evaluator_paths': ['policy/evaluator/']})
        self.checkpoint = ArchiveStore(self.broker, self.world.tmp)

    def test_parent_commits_and_pushes_without_running_task_git_hooks(self):
        hooks = self.work / '.git/hooks'
        hook = hooks / 'pre-commit'
        hook.write_text('#!/bin/sh\nexit 42\n')
        hook.chmod(0o755)
        (self.work / 'src/result').write_text('accepted turn')
        result = self.checkpoint({})
        remote = fakes.sh(self.world.tmp, 'git', '--git-dir=' + self.world.origin, 'show', 'task/11:src/result')
        self.assertEqual(remote, 'accepted turn')
        self.assertEqual(len(result['head']), 40)

    def test_checkpoint_refuses_out_of_scope_mutations_before_push(self):
        (self.work / 'engine.yml').write_text('forbidden')
        with self.assertRaises(PermissionError):
            self.checkpoint({})

    def test_outputs_and_artifact_survive_new_runner_without_replacing_staged_inputs(self):
        (self.work / '.session/artifacts').mkdir(parents=True)
        (self.work / '.session/report.md').write_text('accepted report')
        (self.work / '.session/artifacts/data.bin').write_bytes(b'\x00\xff\x01')
        (self.work / '.session/issue.md').write_text('trusted input')
        state = self.checkpoint.snapshot({})
        (self.work / '.session/report.md').unlink()
        (self.work / '.session/artifacts/data.bin').unlink()
        self.checkpoint.restore(state)
        self.assertEqual((self.work / '.session/report.md').read_text(), 'accepted report')
        self.assertEqual((self.work / '.session/artifacts/data.bin').read_bytes(), b'\x00\xff\x01')
        self.assertEqual((self.work / '.session/issue.md').read_text(), 'trusted input')

    def test_archive_traversal_cannot_write_outside_declared_outputs(self):
        asset = 'session-11-' + 'a' * 64 + '.zip'
        with zipfile.ZipFile(Path(self.world.tmp, asset), 'w') as archive:
            archive.writestr('.session/artifacts/../../../outside', 'forbidden')
        with self.assertRaises(PermissionError):
            self.checkpoint.restore({'outputs_asset': asset, 'outputs_digest': 'a' * 64})
        self.assertFalse(Path(self.world.tmp, 'outside').exists())
