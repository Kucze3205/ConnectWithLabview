"""The real routed chain for a role behind the executor boundary, with a stand-in provider CLI.

stage → executor_boundary.prepare → runtime_entry.py (real broker, real git checkpoint, real runtime state
machine, real provider_adapter.request) → epilogue. Replaced: the `claude` executable (answers from a script),
GitHub's contents API and release assets (plain files) and the bubblewrap wrapper around the CLI (the namespace
is covered by test_model_boundary.py). A stand-in is no provider evidence; it proves the engine's own chain, the
one that stopped iteration 0 twice (a checkpoint that needed `origin`, a prompt that did not fit in argv).
test_agent_chain.py covers the native-CLI path.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import yaml

import fakes
from fakes import common as c, loop
import session_inputs
import test_session as sessions
from tool_broker import FIELDS

BIG = 200 * 1024                      # over the 128 KiB limit of one argv string on Linux
# Runs in the role's place of the real entry point: patches the transport and GitHub, then runs the staged file.
HARNESS = r'''
import json, os, runpy, subprocess, sys
from pathlib import Path

trusted, state = sys.argv[1], Path(sys.argv[2])
sys.path.insert(0, trusted)
import provider_adapter, runtime_checkpoint, runtime_store


class FileBackend:
    def __init__(self, *args, **kwargs):
        pass

    def initialize(self):
        state.mkdir(exist_ok=True)

    def read(self, key):
        path = state / key.replace("/", "__")
        return (json.loads(path.read_text()), path.stat().st_mtime_ns) if path.exists() else ({}, None)

    def write(self, key, value, expected):
        if expected != self.read(key)[1]:
            return False
        (state / key.replace("/", "__")).write_text(json.dumps(value))
        return True


command = runtime_checkpoint.Checkpoint.command


def offline_gh(self, argv, **kwargs):
    if argv[0] == "gh":
        return subprocess.CompletedProcess(argv, 0, "", "")
    return command(self, argv, **kwargs)


runtime_store.GitHubBackend = FileBackend
runtime_checkpoint.Checkpoint.command = offline_gh
provider_adapter.sandbox = lambda command, root: command
runpy.run_path(os.path.join(trusted, "runtime_entry.py"), run_name="__main__")
'''


CLI = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
state = Path(STATE)   # the transport passes the CLI a scrubbed environment: paths are baked in
prompt = sys.stdin.buffer.read()
log = state / "calls.json"
calls = json.loads(log.read_text()) if log.exists() else []
calls.append({"prompt_bytes": len(prompt), "prompt_tail": prompt.decode()[-4000:], "longest_arg": max(map(len, sys.argv)),
              "token": os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")})
log.write_text(json.dumps(calls))
action = json.loads(Path(SCRIPT).read_text())[len(calls) - 1]
print(json.dumps({"is_error": False, "structured_output": action, "usage": {"input_tokens": 1, "output_tokens": 1}}))
'''


def action(tool, **kwargs):
    return dict({key: "" for key in FIELDS}, tool=tool, **kwargs)


@unittest.skipIf(os.name == "nt", "requires a POSIX shell: the stand-in CLI is an executable script")
class RoutedChainTest(sessions.SessionCase):
    work = sessions.StageTest.work

    def setUp(self):
        super().setUp()
        cfg = c.load_yaml('engine.yml')             # a routed pool: the staged entry point is runtime_entry.py
        cfg['provider_pool'] = {'providers': {'claude': {'models': ['approved-model']}},
                                'backoff': {'initial_seconds': 60, 'max_seconds': 300}}
        params = c.load_yaml('policy/params.yml')
        params['routing'] = {'tasks': {'default': [{'provider': 'claude', 'model': 'approved-model'}]}}
        filler = "\n".join("filler line %06d" % i for i in range(BIG // 18)) + "\nEND-OF-PROMPT\n"
        self.w.push_main({"execution/prompts/role.md": filler, "engine.yml": yaml.safe_dump(cfg),
                          "policy/params.yml": yaml.safe_dump(params)}, "routing setup and big prompt")
        self.w.write(self.w.loop, "engine.yml", yaml.safe_dump(cfg))
        self.w.write(self.w.loop, "policy/params.yml", yaml.safe_dump(params))
        c.sync_main()

    def test_restricted_role_does_work_through_the_routed_runtime_and_it_is_admitted(self):
        n = self.issue("worker")
        self.assertTrue(session_inputs.restricted("worker"))
        work, output = self.work(), os.path.join(self.w.tmp, "run")
        trusted, state = os.path.join(output, "trusted"), os.path.join(self.w.tmp, "state")
        os.environ["RUNNER_TEMP"] = output
        loop.stage(n, work, trusted)
        self.assertTrue(Path(trusted, "executor-mode").exists())        # prepared: a fresh repository, no remote
        self.assertEqual(subprocess.run(["git", "remote"], cwd=work, capture_output=True, text=True).stdout.strip(), "")
        report = c.MARK + "\n```yaml\nstatus: done\n```\nDid the work.\n"
        script = [action("Read", path=".session/issue.md"),
                  action("Write", path="src/product.txt", text="agent product"),
                  action("Write", path=".session/report.md", text=report),
                  action("Finish", status="done")]
        harness, steps, fakebin = Path(self.w.tmp, "harness.py"), Path(self.w.tmp, "script.json"), Path(self.w.tmp, "bin")
        fakebin.mkdir()
        fakebin.joinpath("claude").write_text(CLI.replace("STATE", repr(state)).replace("SCRIPT", repr(str(steps))))
        fakebin.joinpath("claude").chmod(0o755)
        os.makedirs(state)
        harness.write_text(HARNESS)
        steps.write_text(json.dumps(script))
        env = dict(os.environ, WORK=work, ISSUE=str(n), EFFORT="high", MAX_TURNS="10", AGENT_TIMEOUT="1",
                   DEFAULT_BRANCH="main", GITHUB_REPOSITORY="o/r", CLAUDE_CODE_OAUTH_TOKEN="synthetic-token",
                   PATH=str(fakebin) + os.pathsep + os.environ["PATH"])
        result = subprocess.run([sys.executable, str(harness), trusted, state], env=env,
                                capture_output=True, text=True, cwd=output)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(Path(output, "provider-execution-output.json").read_text())
        self.assertEqual((summary["status"], summary.get("turns")), ("done", len(script)), summary)
        self.assertEqual(Path(output, "agent-exit").read_text().strip(), "0")
        calls = json.loads(Path(state, "calls.json").read_text())
        self.assertEqual(len(calls), len(script))
        self.assertGreater(calls[0]["prompt_bytes"], 128 * 1024)         # the whole prompt reaches the CLI, by stdin
        self.assertLess(max(call["longest_arg"] for call in calls), 4096)
        self.assertEqual({call["token"] for call in calls}, {"synthetic-token"})
        self.assertIn("Goal", calls[1]["prompt_tail"])      # the Read came back to the model
        session = json.loads(Path(state, "sessions__%s.json" % n).read_text())
        self.assertGreaterEqual(session["turns"], 1)
        self.assertEqual(session["result"]["status"], "done")
        self.assertEqual(subprocess.run(["git", "show", "task/%s:src/product.txt" % n], cwd=work, capture_output=True,
                                        text=True).stdout, "agent product")
        original = loop.merge_branch
        with patch.object(loop, "merge_branch", wraps=original) as merge:
            merge.side_effect = lambda *a, **kw: original(*a, **dict(kw, override={"verdict": "accepted"}))
            loop.finalize(n, work)
        frozen = self.hub.report(n)
        self.assertEqual((frozen["status"], frozen["turns"], frozen["merged"]), ("done", str(len(script)), "true"))
        self.assertEqual(fakes.sh(self.w.origin, "git", "show", "main:src/product.txt"), "agent product")


if __name__ == "__main__":
    unittest.main()
