"""One-off landing of the #195 challenge fixtures (tag iter/0022/195) onto current main.

Iteration 0023 (#201) lost repeated merge resolutions across runner interruptions.
This script avoids merge state: it copies the five challenge files byte-for-byte
from the tag, marks challenges prepared-not-reviewed, appends #195's limitation
sentence and re-pins every reference in benchmark/preparation.json. Lineage and
split files are not touched. Delete this script once the landing has merged.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

FILES = ["benchmark/scripts/challenges.py",
         "benchmark/challenges/README.md",
         "benchmark/challenges/library-icon-tests.json",
         "benchmark/challenges/library-specialty.json",
         "benchmark/challenges/vi-actor-core-native-gap.json"]
STATUS = "benchmark/preparation-status.json"
MANIFEST = "benchmark/preparation.json"
SENTENCE = ("Challenge fixtures are public development fixtures, unexecuted, "
            "with no scorer; independent review is pending.")


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", default="iter/0022/195")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root)

    for name in FILES:
        content = subprocess.run(["git", "show", args.ref + ":" + name],
                                 check=True, capture_output=True).stdout
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_bytes(content)

    status = json.loads((root / STATUS).read_text(encoding="utf-8"))
    status["milestones"]["challenges"] = "prepared-not-reviewed"
    if SENTENCE not in status["limitations"]:
        status["limitations"] += " " + SENTENCE
    dump(root / STATUS, status)

    def sha(name):
        return hashlib.sha256((root / name).read_bytes()).hexdigest()

    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    manifest["milestones"]["challenges"] = [{"path": n, "sha256": ""} for n in FILES + [STATUS]]
    for refs in manifest["milestones"].values():
        for ref in refs:
            ref["sha256"] = sha(ref["path"])
    dump(root / MANIFEST, manifest)
    print("landed %d challenge files from %s; re-pinned %s" % (len(FILES), args.ref, MANIFEST))


if __name__ == "__main__":
    main()
