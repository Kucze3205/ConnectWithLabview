"""Pin the #312 run-record contract (review #318 accept) under the baseline milestone.

Idempotent and hash-gated. Changes only benchmark/baseline/README.md,
benchmark/preparation.json and benchmark/preparation-status.json.
Run from the repository root: python3 -I -B execution/scripts/pin_run_record_318.py
"""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TAG = "iter/0050/312"
NEW_FILES = {
    "benchmark/baseline/run-record.template.json": "aa92803180d88a8336243c6db08dc4b65529f0db6c87d553f23c083b9b44e35d",
    "benchmark/scripts/run_record.py": "bf57224fb2e29fb476b4d343770adc20126a2997f622efcd8c5ce353cd9c3300",
}
README = "benchmark/baseline/README.md"
README_MAIN = "0adac3b9be04e076e59fbb9be676bd7c5ad65f362074caeffff9ad7d8688d5e2"
README_TAG = "02020a5d1e5580f50aed9d48890ad253f65ccbce31d09873299882837a057023"
STATUS = "benchmark/preparation-status.json"
PREP = "benchmark/preparation.json"
OLD_TAIL = "Request independent review before pinning this evidence or implementing executable runner/scoring integration; preparation indexes remain unchanged.\n"
NEW_TAIL = "Review #318 accepted this design with no blocking findings; it is pinned under the baseline milestone. Manifest-content binding stays unresolved (#318 finding 4): actual binding and a negative test are required before runner integration.\n"
SENTENCE = (
    "The synthetic raw run-record contract benchmark/baseline/run-record.template.json with "
    "benchmark/scripts/run_record.py (author #312) was accepted by review #318 as a design only: "
    "no runs, no readiness, tool quality unmeasured; eight fields stay undecided and manifest-content "
    "binding is unresolved (#318 finding 4); author and reviewer are the same model family (codex gpt-6.1-sol)."
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(rel):
    return (ROOT / rel).read_bytes()


def dump(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()


def fail(msg):
    print("ERROR:", msg)
    sys.exit(1)


def main():
    for rel, want in NEW_FILES.items():
        if sha(read(rel)) != want:
            fail(f"{rel} sha256 differs from reviewed bytes")

    readme = read(README)
    if sha(readme) == README_MAIN:
        tag_bytes = subprocess.run(["git", "show", f"{TAG}:{README}"], cwd=ROOT,
                                   capture_output=True, check=True).stdout
        if sha(tag_bytes) != README_TAG or not tag_bytes.startswith(readme):
            fail("tag README differs from the #312 bytes")
        text = tag_bytes.decode()
        if not text.endswith(OLD_TAIL):
            fail("tag README tail not found")
        readme = (text[: -len(OLD_TAIL)] + NEW_TAIL).encode()
        (ROOT / README).write_bytes(readme)
        print("README: section added")
    elif readme.decode().endswith(NEW_TAIL):
        print("README: unchanged")
    else:
        fail("README is neither the main nor the pinned bytes")

    status = json.loads(read(STATUS))
    if SENTENCE not in status["limitations"]:
        status["limitations"] = status["limitations"].rstrip() + " " + SENTENCE
    (ROOT / STATUS).write_bytes(dump(status))

    prep = json.loads(read(PREP))
    baseline = prep["milestones"]["baseline"]
    paths = [r["path"] for r in baseline]
    for rel in NEW_FILES:
        if rel not in paths:
            at = paths.index(STATUS) if STATUS in paths else len(paths)
            baseline.insert(at, {"path": rel, "sha256": NEW_FILES[rel]})
            paths.insert(at, rel)
    current = {README: sha(read(README)), STATUS: sha(read(STATUS))}
    count = 0
    for refs in prep["milestones"].values():
        for ref in refs:
            count += 1
            if ref["path"] in current:
                ref["sha256"] = current[ref["path"]]
    (ROOT / PREP).write_bytes(dump(prep))
    print(f"references: {count}")
    print(f"README {current[README]}")
    print(f"status {current[STATUS]}")
    print(f"preparation {sha(read(PREP))}")


if __name__ == "__main__":
    main()
