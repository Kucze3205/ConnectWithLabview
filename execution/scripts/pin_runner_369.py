"""Pin the reviewed synthetic runner contract under the baseline milestone (reviews #358, #369).

Hash-gated and idempotent. Usage: python3 -I -B execution/scripts/pin_runner_369.py [repo-root]
"""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
FILES = {
    "benchmark/baseline/run-manifest.synthetic.json": "4d4c2b0f02fdde8d17d6c4632b5809680a0ba1b84b9d647cecef53875bcf3e9a",
    "benchmark/baseline/runner-contract.md": "b9e47205b0ef3f479a77bd3b4dd06e89c3521923e6b316bef14f624cbbcaa5c0",
    "benchmark/scripts/runner_contract.py": "866e9c44bad30f654dd516e15cf2d47618838a551e408c86efd5e7b998f3429a",
}
STATUS = "benchmark/preparation-status.json"
PREP = "benchmark/preparation.json"
MARK = "review #369"
SENTENCE = (
    "The synthetic populated-manifest and runner contract (benchmark/baseline/run-manifest.synthetic.json, "
    "benchmark/baseline/runner-contract.md, benchmark/scripts/runner_contract.py; author #352 claude-sonnet-5-5, "
    "reason-control fix #364 codex gpt-6.1-sol) was reviewed by #358 (manifest comparison passed, one reason-control "
    "finding) and its fix was accepted by review #369 (claude-sonnet-5-5, cross-family to #364): design only, "
    "12 planned runs, zero runs executed, no real runner, no restricted-boundary preservation, tool quality "
    "unmeasured; the pending-review sentence in runner-contract.md is dated at its reviewed bytes."
)


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def dump(path, data):
    (ROOT / path).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


for path, want in FILES.items():
    got = sha(path)
    if got != want:
        sys.exit(f"hash gate failed: {path} {got}")

status = json.loads((ROOT / STATUS).read_text())
if MARK not in status["limitations"]:
    status["limitations"] = status["limitations"].rstrip() + " " + SENTENCE
dump(STATUS, status)
status_sha = sha(STATUS)

prep = json.loads((ROOT / PREP).read_text())
baseline = prep["milestones"]["baseline"]
pinned = {entry["path"] for entry in baseline}
at = next(i for i, entry in enumerate(baseline) if entry["path"] == STATUS)
for path, want in FILES.items():
    if path not in pinned:
        baseline.insert(at, {"path": path, "sha256": want})
        at += 1
for entries in prep["milestones"].values():
    for entry in entries:
        if entry["path"] == STATUS:
            entry["sha256"] = status_sha
dump(PREP, prep)

print("status", status_sha)
print("preparation", sha(PREP))
failed = 0
for cmd in (["benchmark/scripts/runner_contract.py", "--check"],
            ["benchmark/scripts/run_record.py", "--check"],
            ["benchmark/scripts/baseline.py", "--check"],
            ["policy/evaluator/evaluate.py", "--check"]):
    r = subprocess.run([sys.executable, "-I", "-B", *cmd], cwd=ROOT, capture_output=True, text=True)
    print(cmd[0], r.returncode, (r.stdout + r.stderr).strip()[-300:])
    failed |= r.returncode != 0
sys.exit(1 if failed else 0)
