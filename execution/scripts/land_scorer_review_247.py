"""Pin the reviewed development scorer (#244, review #247 accept) under the challenges milestone.

Idempotent and git-free. Run from the repository root:
    python3 -I execution/scripts/land_scorer_review_247.py
Delete this script after its result merges.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
# Bytes accepted by review #247 at main 8a8455f.
REVIEWED = {"benchmark/scripts/score.py": "810a5457c3c32ff8c856ae3d960ea06a495860b1efa5c78a8a895610eb649aac",
            "benchmark/results/challenges.json": "a5b9798495cc18006b7128bfaf5e80e4c371cb6f1ac6fd41851fe303da79e484"}
PREPARATION = "benchmark/preparation.json"
STATUS = "benchmark/preparation-status.json"
OLD = "Challenge fixtures are public development fixtures, unexecuted, with no scorer; independent review is pending."
NEW = ("Challenge fixtures are public development fixtures (review #212 revise; its one disclosure finding was fixed "
       "by the landed diagram-difference gap row, which was not re-reviewed). The development scorer "
       "benchmark/scripts/score.py and benchmark/results/challenges.json (33 synthetic controls, 33 matches) were "
       "accepted by review #247 after revise rounds #232 and #241; authors and reviewers were the same model family "
       "(codex gpt-6.1-sol), so the results keep independently_reviewed false. No agent or reader run is executed.")


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
    for rel, want in REVIEWED.items():
        if digest(rel) != want:
            raise SystemExit(rel + ": not the reviewed bytes " + digest(rel))

    status = load(STATUS)
    if NEW not in status["limitations"]:
        if status["limitations"].count(OLD) != 1:
            raise SystemExit(STATUS + ": challenge limitation sentence not found once")
        status["limitations"] = status["limitations"].replace(OLD, NEW)
    status["milestones"]["challenges"] = "scorer-reviewed"
    (ROOT / STATUS).write_text(dump(status), encoding="utf-8")

    preparation = load(PREPARATION)
    refs = preparation["milestones"]["challenges"]
    present = {ref["path"] for ref in refs}
    refs.extend({"path": rel, "sha256": ""} for rel in REVIEWED if rel not in present)
    changed = set(REVIEWED) | {STATUS}
    for entries in preparation["milestones"].values():
        for ref in entries:
            if ref["path"] in changed:
                ref["sha256"] = digest(ref["path"])
            elif ref["sha256"] != digest(ref["path"]):
                raise SystemExit(ref["path"] + ": pinned hash mismatch")
    (ROOT / PREPARATION).write_text(dump(preparation), encoding="utf-8")
    print(json.dumps({"challenges": [ref["path"] for ref in refs], "status": digest(STATUS)}))


if __name__ == "__main__":
    main()
