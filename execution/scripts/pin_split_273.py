"""Pin the reviewed split boundary design (review #273 accept) under the split milestone.

Idempotent and hash-gated: checks the four landed design files, sets the split
milestone label to design-reviewed, replaces the stale "Split remains not-started"
limitation sentence, adds the four files to the split milestone of
benchmark/preparation.json and re-pins every reference to preparation-status.json.
Run from the repository root:
    python3 -I -B execution/scripts/pin_split_273.py
Delete this script after the change merges.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

FILES = {
    "benchmark/split/README.md": "c2ecb9a7bf9af8cd38ac34a06c63bec723f8e2f7a8acacc4341f0fd0b49cbd36",
    "benchmark/split/allocation-manifest.template.json": "5ebe26be811569303d8fc48286d19fe2b0513da77f89ddcc7ec4064f817a3926",
    "benchmark/split/isolation-record.template.json": "6d540b661063a79a47cbaae39f58f7b22abf552f0d7fb69196216ca2d3406ba4",
    "benchmark/scripts/split_boundary.py": "1365e531e7dfa4b2edb31a25248ee8e11871893f6e2dafc027389f10d01d4558",
}
STATUS = "benchmark/preparation-status.json"
MANIFEST = "benchmark/preparation.json"
OLD = "Split remains not-started: restricted allocation and isolation evidence do not exist."
NEW = (
    "Split is a reviewed design only (benchmark/split/ with benchmark/scripts/split_boundary.py,"
    " review #273 accept, two non-blocking checker findings open: two self-mutations are rejected"
    " before reaching the rule they target): no allocation exists, no isolation step is executed,"
    " the restricted store (capability #268) is not ready, and no secrecy is claimed; author"
    " (copilot gpt-5.6-luna) and reviewer (codex gpt-6.1-sol) are both GPT-family models."
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(doc):
    return (json.dumps(doc, indent=2, sort_keys=True) + "\n").encode("utf-8")


def load(path):
    raw = path.read_bytes()
    doc = json.loads(raw)
    if dump(doc) != raw:
        sys.exit(f"unexpected formatting in {path}")
    return doc


def main():
    root = pathlib.Path.cwd()
    for rel, want in FILES.items():
        if sha((root / rel).read_bytes()) != want:
            sys.exit(f"hash mismatch on disk for {rel}")
    status_path = root / STATUS
    status = load(status_path)
    if "review #273" not in status["limitations"]:
        if OLD not in status["limitations"]:
            sys.exit("stale split sentence not found")
        status["limitations"] = status["limitations"].replace(OLD, NEW)
    status["milestones"]["split"] = "design-reviewed"
    status_bytes = dump(status)
    status_path.write_bytes(status_bytes)
    status_sha = sha(status_bytes)
    manifest_path = root / MANIFEST
    manifest = load(manifest_path)
    for refs in manifest["milestones"].values():
        for ref in refs:
            if ref["path"] == STATUS:
                ref["sha256"] = status_sha
    split = manifest["milestones"]["split"]
    present = {ref["path"] for ref in split}
    for rel, want in FILES.items():
        if rel not in present:
            split.append({"path": rel, "sha256": want})
    manifest_path.write_bytes(dump(manifest))
    r = subprocess.run([sys.executable, "-I", "-B", "benchmark/scripts/split_boundary.py", "--check"])
    if r.returncode:
        sys.exit("split_boundary.py --check failed")
    r = subprocess.run([sys.executable, "-I", "-B", "policy/evaluator/evaluate.py", "--check"],
                       capture_output=True, text=True)
    result = json.loads(r.stdout)
    if r.returncode or result["errors"] or result["missing"]:
        sys.exit("evaluator --check failed: " + r.stdout)
    print("pinned; status sha", status_sha, "; evidence references", result["evidence_references"])


if __name__ == "__main__":
    main()
