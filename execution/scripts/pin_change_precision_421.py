"""Pin the reviewed change-case specs (tasks) and precision plan (baseline) (reviews #408, #409, #415, #421).

Hash-gated and idempotent. Usage: python3 -I -B execution/scripts/pin_change_precision_421.py [repo-root]
"""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
FILES = {
    "tasks": {
        "benchmark/change-cases/README.md": "e3ab5773d419c5356684548e64f2f72c605af6f4fd66215454cb2dea85ecb7ad",
        "benchmark/change-cases/typedef-impact.spec.json": "091a4f81e9cbbc0c4dfc157e268873a37401589be95f84829e1e5d12c4e77299",
        "benchmark/change-cases/diagram-difference.spec.json": "edab2e8000808ea49d53a7b72f25ac8316da38bff7a3adbeaf74a8c98782e607",
        "benchmark/scripts/change_cases.py": "657f7fec440790b2f73b9ada4a52dd7cff58da11b5559b3235aedf8dc03668d6",
    },
    "baseline": {
        "benchmark/precision/README.md": "f94ba74b1c22e551b3cf8eabafdb5868705baa889e17ad5f301fb08cbe18824b",
        "benchmark/precision/plan.json": "bbf834a810706f291dde095183a96b04b0f6de05a39687ce3373e1ad1381e7f3",
        "benchmark/scripts/precision_plan.py": "0bcc765aba2fbbbb76203fb07a749fe8a72fe71f3c6ef179f3f9df97201e8ec3",
    },
}
STATUS = "benchmark/preparation-status.json"
PREP = "benchmark/preparation.json"
MARK = "review #421"
SENTENCE = (
    "The public change-case specifications (benchmark/change-cases/README.md, typedef-impact.spec.json, "
    "diagram-difference.spec.json, benchmark/scripts/change_cases.py; author #404 codex gpt-6.1-sol; tasks milestone) "
    "and the repetition/precision plan (benchmark/precision/README.md, plan.json, benchmark/scripts/precision_plan.py; "
    "author #405 codex gpt-6.1-sol; baseline milestone) passed specification reviews #408/#409 (same model family as "
    "the authors); their reason-control fixes #412 (codex gpt-6.1-sol) and #418 (Policymaker script, Claude family) "
    "were accepted by review #421 (codex gpt-6.1-sol, cross-family to the #418 fix author only): design only, no "
    "change case executed, native answers unavailable (#169), model quota and repetition resources remain an owner "
    "decision, change-case source pins verify only with LABVIEW_ENVIRONMENT, a coordinated removal of the "
    "rejecting-control count check is not detected (#421 finding 4), tool quality unmeasured."
)


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def dump(path, data):
    (ROOT / path).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


for group in FILES.values():
    for path, want in group.items():
        got = sha(path)
        if got != want:
            sys.exit(f"hash gate failed: {path} {got}")

status = json.loads((ROOT / STATUS).read_text())
if MARK not in status["limitations"]:
    status["limitations"] = status["limitations"].rstrip() + " " + SENTENCE
dump(STATUS, status)
status_sha = sha(STATUS)

prep = json.loads((ROOT / PREP).read_text())
for milestone, group in FILES.items():
    entries = prep["milestones"][milestone]
    pinned = {entry["path"] for entry in entries}
    at = next(i for i, entry in enumerate(entries) if entry["path"] == STATUS)
    for path, want in group.items():
        if path not in pinned:
            entries.insert(at, {"path": path, "sha256": want})
            at += 1
for entries in prep["milestones"].values():
    for entry in entries:
        if entry["path"] == STATUS:
            entry["sha256"] = status_sha
dump(PREP, prep)

print("status", status_sha)
print("preparation", sha(PREP))
failed = 0
for cmd in (["benchmark/scripts/change_cases.py", "--check"],
            ["benchmark/scripts/precision_plan.py", "--check"],
            ["benchmark/scripts/runner_contract.py", "--check"],
            ["benchmark/scripts/baseline.py", "--check"],
            ["policy/evaluator/evaluate.py", "--check"]):
    r = subprocess.run([sys.executable, "-I", "-B", *cmd], cwd=ROOT, capture_output=True, text=True)
    print(cmd[0], r.returncode, (r.stdout + r.stderr).strip()[-300:])
    failed |= r.returncode != 0
sys.exit(1 if failed else 0)
