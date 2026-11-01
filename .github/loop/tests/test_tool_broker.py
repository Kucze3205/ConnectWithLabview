import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import fakes
from tool_broker import Broker, FIELDS


def action(tool, **kwargs):
    return dict({key: "" for key in FIELDS}, tool=tool, **kwargs)


class BrokerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "work"
        self.root.mkdir()
        (self.root / ".session").mkdir()
        (self.root / ".git").mkdir()
        (self.root / "src").mkdir()
        (self.root / "engine.yml").write_text("trusted")
        (self.root / ".session/issue.md").write_text("original task")
        self.profile = {"tools": ["Read", "Write", "Edit", "Glob", "Grep", "Bash(python3:*)"], "write": ["src/**"]}
        self.config = {"protected": ["engine.yml", ".github/", "goal/"], "evaluator_paths": ["policy/evaluator/"]}
        self.broker = Broker(self.root, self.profile, self.config)

    def test_role_writes_and_exact_edit_are_visible_to_later_provider(self):
        self.broker.execute(action("Write", path="src/result.txt", text="first provider"))
        other = Broker(self.root, self.profile, self.config)
        self.assertEqual(other.execute(action("Read", path="src/result.txt"))["text"], "first provider")
        other.execute(action("Edit", path="src/result.txt", old="first", new="second"))
        self.assertEqual((self.root / "src/result.txt").read_text(), "second provider")

    def test_inputs_and_trusted_or_out_of_scope_paths_cannot_be_replaced(self):
        for path in ("engine.yml", ".session/issue.md", "goal/goal.md", "other/file", "../outside", ".git/config", "C:/secrets"):
            with self.subTest(path=path), self.assertRaises(PermissionError):
                self.broker.execute(action("Write", path=path, text="overwritten"))
        self.assertEqual((self.root / "engine.yml").read_text(), "trusted")
        self.assertEqual((self.root / ".session/issue.md").read_text(), "original task")
        self.broker.execute(action("Write", path=".session/report.md", text="progress"))

    def test_profile_cannot_use_an_unlisted_tool_or_escape_command_prefix(self):
        self.broker.tools.remove("Write")
        with self.assertRaises(PermissionError):
            self.broker.execute(action("Write", path="src/no", text="x"))
        for command in ("bash -c echo", "/usr/bin/python3 -c pass", "curl example.com"):
            with self.subTest(command=command), self.assertRaises(PermissionError):
                self.broker.execute(action("Bash", command=command))

    def test_prepared_sources_remain_readable_without_exposing_other_runner_files(self):
        prepared = Path(self.temp.name, 'prepared')
        prepared.mkdir()
        (prepared / 'fixture.txt').write_text('public fixture')
        broker = Broker(self.root, self.profile, self.config, {'environment': prepared.resolve()})
        self.assertEqual(broker.execute(action('Read', path='@environment/fixture.txt'))['text'], 'public fixture')
        self.assertIn('@environment/fixture.txt', broker.execute(action('Glob', pattern='@environment/*'))['paths'])
        for path in ('@environment/fixture.txt', '@environment/../outside', '@unlisted/secret'):
            with self.assertRaises(PermissionError):
                broker.execute(action('Write', path=path, text='overwritten'))

    def test_finish_cannot_replace_a_missing_or_unfinished_report(self):
        with self.assertRaisesRegex(ValueError, 'Use Write to create'):
            self.broker.execute(action('Finish', status='done'))
        report = self.root / '.session/report.md'
        report.write_text('<!-- session-report -->\n```yaml\nstatus: wip\n```\n')
        with self.assertRaises(ValueError):
            self.broker.execute(action('Finish', status='done'))
        report.write_text('<!-- session-report -->\n```yaml\nstatus: done\n```\n')
        self.assertEqual(self.broker.execute(action('Finish', status='done'))['status'], 'done')

    @unittest.skipIf(os.name == "nt", "Linux symlinks")
    def test_symlink_and_hardlink_cannot_redirect_trusted_parent_operations(self):
        outside = Path(self.temp.name) / "secret"
        outside.write_text("synthetic secret")
        (self.root / "src/link").symlink_to(outside)
        os.link(outside, self.root / "src/hard")
        for path in ("src/link", "src/hard"):
            with self.subTest(path=path), self.assertRaises(PermissionError):
                self.broker.execute(action("Read", path=path))
        self.assertEqual(outside.read_text(), "synthetic secret")

    @unittest.skipUnless(shutil.which("python3"), "needs python3 on PATH")
    def test_command_gets_no_parent_secret_and_sees_the_prepared_resource(self):
        # No sandbox (ADR-0006): the command runs in the workspace; admission enforces the write paths later.
        resource = Path(self.temp.name, 'prepared')
        resource.mkdir()
        (resource / 'example').write_text('public input')
        self.broker = Broker(self.root, self.profile, self.config, {'environment': resource.resolve()})
        code = """import os, pathlib
assert 'GH_TOKEN' not in os.environ and 'SYNTHETIC_SECRET' not in os.environ
assert (pathlib.Path(os.environ['LABVIEW_ENVIRONMENT']) / 'example').read_text() == 'public input'
pathlib.Path('src/allowed.txt').write_text('ok')
"""
        import shlex
        from unittest import mock
        with mock.patch.dict(os.environ, {"GH_TOKEN": "x", "SYNTHETIC_SECRET": "y"}):
            result = self.broker.execute(action("Bash", command="python3 -c " + shlex.quote(code)))
        self.assertEqual(result["exit"], 0, result["text"])
        self.assertEqual((self.root / "src/allowed.txt").read_text(), "ok")

if __name__ == "__main__":
    unittest.main()
