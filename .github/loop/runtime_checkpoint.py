"""Trusted git/file checkpoint. Restores only declared role outputs, never code.

Task code lives on task/N. Session outputs and large artifacts live in immutable
release assets, referenced by a CAS-protected session continuation. No extracted
archive path is trusted and no hook/config in the task checkout is executed.
"""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile

import common as c
from tool_broker import OUTPUTS


class Checkpoint:
    def __init__(self, broker, repository, issue):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) or not str(issue).isdigit():
            raise ValueError("invalid checkpoint identity")
        self.broker, self.repo, self.issue = broker, repository, str(issue)
        self.release = "loop-checkpoints"

    def command(self, command, *, cwd=None, remote=False, check=True):
        env = {k: os.environ[k] for k in ("PATH", "HOME", "SYSTEMROOT", "SSL_CERT_FILE", "SSL_CERT_DIR") if k in os.environ}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
                   GH_PROMPT_DISABLED="1")
        author = self.broker.config.get('author') or {}
        env.update(GIT_AUTHOR_NAME=author.get('name') or c.BOT,
                   GIT_AUTHOR_EMAIL=author.get('email') or '41898282+github-actions[bot]@users.noreply.github.com',
                   GIT_COMMITTER_NAME=c.BOT, GIT_COMMITTER_EMAIL='41898282+github-actions[bot]@users.noreply.github.com')
        if remote:
            env["GH_TOKEN"] = os.environ.get("GH_TOKEN", "")
        if command[0] == "git":
            command = ["git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
                       "-c", "maintenance.auto=false", "-c", "gc.auto=0"] + (c.auth_args() if remote else []) + command[1:]
        try:
            result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=180)
        except subprocess.SubprocessError:
            # TimeoutExpired includes argv, which may contain git's encoded
            # authorization header. Never propagate that exception to a log.
            raise RuntimeError('durable checkpoint process failed') from None
        if check and result.returncode:
            raise RuntimeError("durable checkpoint operation failed")
        return result

    def git(self, *args, **kwargs):
        return self.command(["git"] + list(args), cwd=self.broker.root, **kwargs)

    def files(self):
        session = self.broker.root / ".session"
        if not session.exists():
            return []
        result = []
        for path in session.rglob("*"):
            relative = path.relative_to(self.broker.root).as_posix()
            tail = relative[len(".session/"):]
            if tail not in OUTPUTS and not tail.startswith("artifacts/"):
                continue
            checked = self.broker.path(relative)
            if checked.is_file():
                result.append((relative, checked))
        return sorted(result)

    def snapshot(self, previous):
        entries, checksum = self.files(), hashlib.sha256()
        for name, path in entries:
            checksum.update(name.encode() + b'\0')
            checksum.update(path.stat().st_size.to_bytes(8, 'big'))
            with path.open('rb') as source:
                for chunk in iter(lambda: source.read(1024 * 1024), b''):
                    checksum.update(chunk)
        digest = checksum.hexdigest()
        if previous.get('outputs_digest') == digest:
            return {k: previous[k] for k in ('outputs_digest', 'outputs_asset') if k in previous}
        if not entries:
            return {'outputs_digest': digest, 'outputs_asset': None}
        asset = 'session-' + self.issue + '-' + digest + '.zip'
        with tempfile.TemporaryDirectory(prefix='trusted-checkpoint-') as directory:
            archive = Path(directory, asset)
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
                for name, path in entries:
                    output.write(path, name)
            release = self.command(['gh', 'release', 'view', self.release, '--repo', self.repo], remote=True, check=False)
            if release.returncode:
                # Concurrent sessions can race on creation; verify after create.
                self.command(['gh', 'release', 'create', self.release, '--repo', self.repo,
                              '--target', os.environ.get('DEFAULT_BRANCH', 'main'), '--prerelease',
                              '--title', 'Engine session checkpoints', '--notes', 'Durable role outputs; managed by the engine.'],
                             remote=True, check=False)
                self.command(['gh', 'release', 'view', self.release, '--repo', self.repo], remote=True)
            self.command(['gh', 'release', 'upload', self.release, str(archive), '--repo', self.repo, '--clobber'], remote=True)
        return {'outputs_digest': digest, 'outputs_asset': asset}

    def restore(self, state):
        asset = state.get('outputs_asset')
        if not asset:
            return
        if not re.fullmatch('session-' + self.issue + r'-[a-f0-9]{64}\.zip', asset):
            raise ValueError('invalid session checkpoint asset')
        with tempfile.TemporaryDirectory(prefix='restore-checkpoint-') as directory:
            self.command(['gh', 'release', 'download', self.release, '--repo', self.repo,
                          '--pattern', asset, '--dir', directory], remote=True)
            with zipfile.ZipFile(Path(directory, asset)) as archive:
                if sum(item.file_size for item in archive.infolist()) > 2_000_000_000:
                    raise ValueError('session checkpoint exceeds artifact bound')
                for item in archive.infolist():
                    name = item.filename
                    if not name.startswith('.session/') or not self.broker.writable(name):
                        raise PermissionError('checkpoint contains an undeclared output')
                    path = self.broker.check_write(name)
                    if item.is_dir() or (item.external_attr >> 16) & 0o170000 == 0o120000:
                        raise PermissionError('checkpoint contains a redirected output')
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(item) as source, path.open('wb') as target:
                        shutil.copyfileobj(source, target)
        # Verify content identity after canonical-safe extraction.
        entries, checksum = self.files(), hashlib.sha256()
        for name, path in entries:
            checksum.update(name.encode() + b'\0')
            checksum.update(path.stat().st_size.to_bytes(8, 'big'))
            with path.open('rb') as source:
                for chunk in iter(lambda: source.read(1024 * 1024), b''):
                    checksum.update(chunk)
        if checksum.hexdigest() != state.get('outputs_digest'):
            raise ValueError('session checkpoint content mismatch')

    def __call__(self, previous):
        changed = set()
        for args in (('diff', '--name-only', '-z', 'HEAD'), ('ls-files', '--others', '--exclude-standard', '-z')):
            changed.update(p for p in self.git(*args).stdout.split('\0') if p)
        for name in changed:
            self.broker.check_write(name)
        if changed:
            # Explicit paths avoid staging unrelated/unreviewed files. The .git
            # directory is immutable in every model/tool subprocess.
            self.git('add', '-A', '--', *sorted(changed))
            self.git('commit', '-m', 'Role checkpoint for task ' + self.issue)
        head = self.git('rev-parse', 'HEAD').stdout.strip()
        # A work repository prepared by the executor boundary is a fresh snapshot without `origin`: its
        # source reaches `task/N` only when the epilogue admits the files as data. Outputs still go to
        # the release asset below.
        if self.git('remote', 'get-url', 'origin', check=False).returncode == 0:
            self.git('push', 'origin', 'HEAD:refs/heads/task/' + self.issue, remote=True)
        return dict(self.snapshot(previous), head=head)
