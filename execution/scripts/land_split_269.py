#!/usr/bin/env python3
"""Land the #269 split boundary design from tag iter/0039/269 (hash-gated, idempotent).

Copies four design-only files; edits no preparation index. Delete after the landing merges.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG = "iter/0039/269"
FILES = {
    "benchmark/scripts/split_boundary.py": "1365e531e7dfa4b2edb31a25248ee8e11871893f6e2dafc027389f10d01d4558",
    "benchmark/split/README.md": "c2ecb9a7bf9af8cd38ac34a06c63bec723f8e2f7a8acacc4341f0fd0b49cbd36",
    "benchmark/split/allocation-manifest.template.json": "5ebe26be811569303d8fc48286d19fe2b0513da77f89ddcc7ec4064f817a3926",
    "benchmark/split/isolation-record.template.json": "6d540b661063a79a47cbaae39f58f7b22abf552f0d7fb69196216ca2d3406ba4",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    for rel, want in FILES.items():
        dst = ROOT / rel
        if dst.exists() and sha(dst.read_bytes()) == want:
            print(f"unchanged {rel}")
            continue
        data = subprocess.run(["git", "show", f"{TAG}:{rel}"], cwd=ROOT,
                              capture_output=True, check=True).stdout
        if sha(data) != want:
            print(f"hash mismatch for {rel} on {TAG}", file=sys.stderr)
            return 1
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        print(f"wrote {rel}")
    check = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "benchmark/scripts/split_boundary.py"), "--check"],
                           cwd=ROOT)
    return check.returncode


if __name__ == "__main__":
    raise SystemExit(main())
