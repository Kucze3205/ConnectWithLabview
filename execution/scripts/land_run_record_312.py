"""Land the #312 run-record template and checker from tag iter/0050/312.

Idempotent and hash-gated. Copies two new files only; benchmark/baseline/README.md
and both preparation JSON files stay unchanged (pins come after independent review).
Delete this script after the landing merges.
"""
import hashlib
import pathlib
import subprocess
import sys

TAG = "iter/0050/312"
FILES = {
    "benchmark/baseline/run-record.template.json":
        "aa92803180d88a8336243c6db08dc4b65529f0db6c87d553f23c083b9b44e35d",
    "benchmark/scripts/run_record.py":
        "bf57224fb2e29fb476b4d343770adc20126a2997f622efcd8c5ce353cd9c3300",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root = pathlib.Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True).strip())
    for rel, want in FILES.items():
        target = root / rel
        if target.exists() and sha(target.read_bytes()) == want:
            print(f"unchanged {rel} {want}")
            continue
        data = subprocess.check_output(["git", "show", f"{TAG}:{rel}"], cwd=root)
        got = sha(data)
        if got != want:
            sys.exit(f"hash mismatch for {rel} at {TAG}: {got} != {want}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        print(f"wrote {rel} {want}")
    for pyc in root.joinpath("benchmark").rglob("__pycache__"):
        sys.exit(f"remove bytecode directory before commit: {pyc}")
    check = subprocess.run(
        [sys.executable, "-I", "-B", "benchmark/scripts/run_record.py", "--check"],
        cwd=root)
    sys.exit(check.returncode)


if __name__ == "__main__":
    main()
