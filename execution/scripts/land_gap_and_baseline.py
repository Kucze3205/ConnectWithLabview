"""Land the diagram-difference gap row (review #212) and pin the reviewed baseline design (#216, review #221).

Idempotent and git-free. Run from the repository root:
    python3 -I execution/scripts/land_gap_and_baseline.py
Delete this script after its result merges.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
ANCHOR = "no key is inferred from synthetic responses. |\n"
ROW = ("| Diagram difference (paired revisions) | none: explicit gap | No diagram-difference (paired-revision) "
       "control exists. Missing evidence: before/after revisions of the same VI, native diagram evidence for both, "
       "and an independently established difference key. This remains a visible gap and the case stays in scope. |\n")
# Hashes produced by session #215 (tag iter/0025/215) for the same one-row edit.
EXPECTED = {"benchmark/scripts/challenges.py": "8195c1d95a84593ec5fbf094aa6268ac7f62c8df957b7f075e50c76bb32aed11",
            "benchmark/challenges/README.md": "e42027c705c184f994b959780ff19cbe2fbf8d4c8f3e85d06694e2dd5d5df100"}
BASELINE = ["benchmark/baseline/README.md", "benchmark/baseline/run-manifest.template.json",
            "benchmark/scripts/baseline.py"]
PREPARATION = "benchmark/preparation.json"
STATUS = "benchmark/preparation-status.json"
NOTE = ("Baseline is a reviewed design template only (review #221 accept; reviewer and author #216 were the same "
        "model family): no manifest is populated, no paired run or pilot is executed, quota and isolation are "
        "unverified.")


def digest(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def dump(doc):
    return json.dumps(doc, indent=2, sort_keys=True) + "\n"


def load(rel):
    text = (ROOT / rel).read_text(encoding="utf-8")
    doc = json.loads(text)
    if text != dump(doc):
        raise SystemExit(rel + ": unexpected formatting")
    return doc


def main():
    for rel, want in EXPECTED.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if ROW not in text:
            if text.count(ANCHOR) != 1:
                raise SystemExit(rel + ": anchor not unique")
            path.write_text(text.replace(ANCHOR, ANCHOR + ROW), encoding="utf-8")
        if digest(rel) != want:
            raise SystemExit(rel + ": unexpected sha256 " + digest(rel))

    status = load(STATUS)
    status["milestones"]["baseline"] = "design-reviewed"
    if NOTE not in status["limitations"]:
        status["limitations"] += " " + NOTE
    (ROOT / STATUS).write_text(dump(status), encoding="utf-8")

    preparation = load(PREPARATION)
    preparation["milestones"]["baseline"] = [{"path": rel, "sha256": ""} for rel in BASELINE + [STATUS]]
    changed = set(EXPECTED) | set(BASELINE) | {STATUS}
    for refs in preparation["milestones"].values():
        for ref in refs:
            if ref["path"] in changed:
                ref["sha256"] = digest(ref["path"])
            elif ref["sha256"] != digest(ref["path"]):
                raise SystemExit(ref["path"] + ": pinned hash mismatch")
    (ROOT / PREPARATION).write_text(dump(preparation), encoding="utf-8")
    print(json.dumps({"challenges": EXPECTED, "baseline": [digest(rel) for rel in BASELINE + [STATUS]]}))


if __name__ == "__main__":
    main()
