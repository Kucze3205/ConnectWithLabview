"""Provider-independent role tools. Credentials never enter this boundary.

Model CLIs propose JSON actions; only this trusted broker touches the workspace.
Direct operations check canonical paths and write permissions. Commands run with
a minimal filesystem, immutable git metadata and kernel-enforced offline mode.
"""
import fnmatch
import os
from pathlib import Path, PurePosixPath
import shlex
import shutil
import subprocess
import tempfile

import common as c
from probe_isolation import sandbox

FIELDS = ("tool", "path", "text", "pattern", "command", "old", "new", "status")
TOOLS = ["Read", "Glob", "Grep", "Write", "Edit", "Delete", "Bash", "Finish"]
ACTION_SCHEMA = {"type": "object", "additionalProperties": False, "required": list(FIELDS),
                 "properties": {k: {"type": "string"} for k in FIELDS}}
ACTION_SCHEMA["properties"]["tool"]["enum"] = TOOLS
OUTPUTS = {"report.md", "tasks.json", "orders.json", "requests.json", "suggestions.json", "suggestion-decisions.json"}
MAX_TEXT = 200_000


def validate(action):
    if not isinstance(action, dict) or set(action) != set(FIELDS):
        raise ValueError("action requires exactly the declared fields")
    if any(not isinstance(value, str) or len(value) > 5_000_000 for value in action.values()):
        raise ValueError("action fields must be bounded strings")
    if action["tool"] not in TOOLS:
        raise ValueError("unknown broker tool")
    return action


class Broker:
    def __init__(self, work, profile, config, resources=None):
        self.root = Path(work).resolve()
        self.profile, self.config = profile, config
        self.tools = {t.split("(", 1)[0] for t in profile.get("tools", [])}
        self.resources = {}
        for name, directory in (resources or {}).items():
            if name != 'environment':
                raise ValueError('unknown prepared resource')
            path = Path(directory)
            if not path.is_absolute() or not path.is_dir() or path.is_symlink() or path.resolve() != path:
                raise ValueError('prepared resource must be a canonical directory')
            self.resources[name] = path

    def path(self, relative):
        if not relative or "\\" in relative or "\0" in relative:
            raise PermissionError("invalid workspace path")
        parts = PurePosixPath(relative)
        if parts.is_absolute() or any(p in {"..", ".git"} or ":" in p for p in parts.parts):
            raise PermissionError("path is outside the role workspace")
        segments = parts.parts
        base = self.root
        if segments and segments[0].startswith('@'):
            base = self.resources.get(segments[0][1:])
            if base is None:
                raise PermissionError('unknown prepared resource')
            segments = segments[1:]
        result = base
        for part in segments:
            result /= part
            if result.is_symlink():
                raise PermissionError("redirected paths are not role tools")
            if result.exists() and result.is_file() and result.stat().st_nlink != 1:
                raise PermissionError("hardlinked workspace file")
        if not result.resolve().is_relative_to(base):
            raise PermissionError("workspace path escaped")
        return result

    def writable(self, relative):
        if relative.startswith('@'):
            return False
        if relative.startswith(".session/"):
            tail = relative[len(".session/"):]
            return tail in OUTPUTS or tail.startswith("artifacts/")
        if c.path_match(relative, self.config["protected"]):
            return False
        if c.path_match(relative, self.config["evaluator_paths"]) and not self.profile.get("owns_evaluator"):
            return False
        return c.path_match(relative, self.profile.get("write") or [])

    def check_write(self, relative):
        path = self.path(relative)
        if not self.writable(relative):
            raise PermissionError("write is outside the role's accepted paths")
        return path

    def files(self):
        for prefix, base in [('', self.root)] + [('@' + key + '/', value) for key, value in self.resources.items()]:
            for root, dirs, names in os.walk(base, followlinks=False):
                dirs[:] = [d for d in dirs if d != ".git" and not Path(root, d).is_symlink()]
                for name in names:
                    file = Path(root, name)
                    if file.is_symlink():
                        continue
                    yield prefix + file.relative_to(base).as_posix()

    def execute(self, action, timeout=60):
        validate(action)
        tool, relative = action["tool"], action["path"]
        needed = "Write" if tool == "Delete" else tool
        if tool != "Finish" and needed not in self.tools:
            raise PermissionError("tool is not in this role's profile")
        if tool == "Finish":
            if action["status"] not in {"done", "partial", "blocked", "rejected"}:
                raise ValueError("Finish requires an agent terminal status")
            report = self.path('.session/report.md').read_text(encoding='utf-8')
            if not report.startswith(c.MARK) or c.fields(report).get('status') != action['status']:
                raise ValueError('Finish requires a matching marked terminal report')
            return {"status": action["status"], "text": action["text"]}
        if tool == "Read":
            path = self.path(relative)
            with path.open(encoding="utf-8") as fh:
                text = fh.read(MAX_TEXT + 1)
            return {"text": text[:MAX_TEXT], "truncated": len(text) > MAX_TEXT}
        if tool == "Glob":
            matches = [p for p in self.files() if fnmatch.fnmatchcase(p, action["pattern"])]
            return {"paths": sorted(matches)[:2000], "truncated": len(matches) > 2000}
        if tool == "Grep":
            # Literal search is deliberate: an untrusted regex must not hang the
            # trusted parent. No shell or provider-native search bypass.
            found, remaining = [], 5_000_000
            for rel in self.files():
                if action["path"] and not rel.startswith(action["path"]):
                    continue
                try:
                    with self.path(rel).open("rb") as fh:
                        text = fh.read(min(MAX_TEXT, remaining)).decode("utf-8")
                except (OSError, UnicodeError, PermissionError):
                    continue
                remaining -= len(text)
                for number, line in enumerate(text.splitlines(), 1):
                    if action["pattern"] in line:
                        found.append({"path": rel, "line": number, "text": line[:1000]})
                    if len(found) >= 500:
                        return {"matches": found, "truncated": True}
                if remaining <= 0:
                    return {"matches": found, "truncated": True}
            return {"matches": found, "truncated": False}
        if tool in {"Write", "Edit", "Delete"}:
            path = self.check_write(relative)
            if tool == "Delete":
                path.unlink()
            else:
                text = action["text"]
                if tool == "Edit":
                    text = path.read_text(encoding="utf-8")
                    if not action["old"] or text.count(action["old"]) != 1:
                        raise ValueError("Edit requires one exact occurrence")
                    text = text.replace(action["old"], action["new"], 1)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8", newline="\n")
            return {"written": relative}
        return self.command(action["command"], timeout)

    def command(self, command, timeout):
        argv = shlex.split(command)
        if not argv:
            raise ValueError("empty command")
        rules = self.profile.get("tools", [])
        allowed = "Bash" in rules or any(rule == "Bash(%s:*)" % argv[0] for rule in rules)
        if not allowed or "/" in argv[0] or "\\" in argv[0]:
            raise PermissionError("command is outside the role's Bash rules")
        with tempfile.TemporaryDirectory(prefix="role-command-") as scratch:
            prefix = sandbox([], scratch)[:-1]
            prefix += ["--ro-bind", str(self.root), "/workspace"]
            for name, path in self.resources.items():
                prefix += ['--ro-bind', str(path), '/resources/' + name]
            # A read-only root prevents creation of new protected root paths.
            # Direct Write can create new allowed roots, which later commands see.
            for child in self.root.iterdir():
                rel = child.name
                if rel in {".git", ".session"} or child.is_symlink():
                    continue
                if not self.writable(rel + "/x" if child.is_dir() else rel):
                    continue
                if child.is_dir() and not any(p in {"**", rel + "/**", rel + "/"} for p in self.profile.get("write", [])):
                    continue  # granular globs use direct tools, never a broader mount
                protected = self.config["protected"] + ([] if self.profile.get("owns_evaluator") else self.config["evaluator_paths"])
                if any(any(char in p for char in "*?[") for p in protected):
                    continue
                if any(p.rstrip("/").startswith(rel + "/") for p in protected):
                    continue  # fail closed for a nested protected subtree
                prefix += ["--bind", str(child), "/workspace/" + rel]
            # Session inputs/contracts remain immutable; only declared outputs
            # are writable. Commands cannot replace the whole .session folder.
            session = self.root / ".session"
            session.mkdir(exist_ok=True)
            for name in OUTPUTS:
                path = self.path(".session/" + name)
                path.touch(exist_ok=True)
                prefix += ["--bind", str(path), "/workspace/.session/" + name]
            artifacts = self.path(".session/artifacts")
            artifacts.mkdir(exist_ok=True)
            prefix += ["--bind", str(artifacts), "/workspace/.session/artifacts", "--chdir", "/workspace"]
            if not self.profile.get("internet", False):
                helper = Path(scratch, "offline_exec.py")
                shutil.copy(Path(__file__).with_name("offline_exec.py"), helper)
                prefix += ["--unshare-net"]
                argv = ["python3", str(helper)] + argv
            env = {"PATH": os.environ["PATH"], "HOME": scratch, "LANG": "C.UTF-8", "CI": "true",
                   "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_TERMINAL_PROMPT": "0"}
            if 'environment' in self.resources:
                env['LABVIEW_ENVIRONMENT'] = '/resources/environment'
            with tempfile.TemporaryFile() as output:
                try:
                    result = subprocess.run(prefix + ["--"] + argv, env=env, stdin=subprocess.DEVNULL,
                                            stdout=output, stderr=subprocess.STDOUT, timeout=timeout, check=False)
                except subprocess.TimeoutExpired:
                    return {"exit": 124, "text": "tool deadline exceeded"}
                size = output.tell()
                output.seek(max(0, size - MAX_TEXT))
                return {"exit": result.returncode, "text": output.read().decode("utf-8", errors="replace"),
                        "truncated": size > MAX_TEXT}
