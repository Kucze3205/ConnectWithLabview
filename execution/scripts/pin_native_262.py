"""Pin the reviewed native job design (review #262 accept) under the oracle milestone.

Idempotent and hash-gated: checks the four landed design files, appends one
limitation sentence to benchmark/preparation-status.json, adds the four files to
the oracle milestone of benchmark/preparation.json and re-pins every reference
to preparation-status.json. The oracle milestone label is left unchanged.
Run from the repository root:
    python3 -I execution/scripts/pin_native_262.py
Delete this script after the change merges.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

FILES = {
    "benchmark/scripts/native_jobs.py": "081040ce35f2916ef851cea9f96750a5b43f6486408d29f8cca34a6de402655a",
    "benchmark/native/README.md": "78a54100473259a7feaf7dc4684cda1a96836f93b1fd94d200d21b93415376d2",
    "benchmark/native/recipes.json": "f292d56ebfe8428f4f37b589666feebc321136b4cbc26ea51cc27e389d6179e8",
    "benchmark/native/output-record.template.json": "86ba84aaef63a327bc53868622e0b085b49352ed1b220e7481f73f7aac9ec9c7",
}
STATUS = "benchmark/preparation-status.json"
MANIFEST = "benchmark/preparation.json"
SENTENCE = (
    " The native job design benchmark/native/ with benchmark/scripts/native_jobs.py"
    " (23/23 native-required development slots mapped to 12 recipes) was accepted by review #262"
    " as a design-only contract: zero native executions, capability #169 not ready, the readiness VI"
    " lacks independently known behaviour, builds stay gaps; author (codex gpt-6.1-sol) and reviewer"
    " (copilot gpt-5.6-luna) are both GPT-family models."
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
    if "review #262" not in status["limitations"]:
        status["limitations"] += SENTENCE
    status_bytes = dump(status)
    status_path.write_bytes(status_bytes)
    status_sha = sha(status_bytes)
    manifest_path = root / MANIFEST
    manifest = load(manifest_path)
    for refs in manifest["milestones"].values():
        for ref in refs:
            if ref["path"] == STATUS:
                ref["sha256"] = status_sha
    oracle = manifest["milestones"]["oracle"]
    present = {ref["path"] for ref in oracle}
    for rel, want in FILES.items():
        if rel not in present:
            oracle.append({"path": rel, "sha256": want})
    manifest_path.write_bytes(dump(manifest))
    r = subprocess.run([sys.executable, "-I", "benchmark/scripts/native_jobs.py", "--check"])
    if r.returncode:
        sys.exit("native_jobs.py --check failed")
    r = subprocess.run([sys.executable, "policy/evaluator/evaluate.py", "--check"], capture_output=True, text=True)
    result = json.loads(r.stdout)
    if r.returncode or result["errors"] or result["missing"]:
        sys.exit("evaluator --check failed: " + r.stdout)
    print("pinned; status sha", status_sha, "; evidence references", result["evidence_references"])


if __name__ == "__main__":
    main()
