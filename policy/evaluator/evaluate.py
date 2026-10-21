#!/usr/bin/env python3
"""Bootstrap evidence inventory. Never a measurement of LabVIEW tool quality."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath

MANIFEST = "benchmark/preparation.json"
MILESTONES = ("sources", "tasks", "oracle", "split", "coverage", "baseline", "challenges")
MAX_BYTES = 2_000_000


def read_file(root, relative):
    path = PurePosixPath(relative)
    if not relative or "\\" in relative or ":" in relative or path.is_absolute() or ".." in path.parts:
        raise ValueError("evidence path must be relative and inside the tree")
    root = Path(root).resolve()
    target = root.joinpath(*path.parts)
    # Reject symlinks even when their current destination is inside the tree.
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("symlink evidence is not allowed")
    if not target.resolve().is_relative_to(root) or not target.is_file():
        raise ValueError("evidence is not a regular file inside the tree")
    with target.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("evidence exceeds 2 MB; use a small pinned evidence record")
    return data


def inventory(root):
    result = {"manifest": "missing", "evidence_references": 0,
              "missing": list(MILESTONES), "errors": [], "tool_quality": None,
              "benchmark_executed": False, "benchmark_ready": False}
    manifest = Path(root) / MANIFEST
    if not manifest.exists() and not manifest.is_symlink():
        return result
    result["manifest"] = "invalid"
    try:
        doc = json.loads(read_file(root, MANIFEST).decode("utf-8"))
        if not isinstance(doc, dict) or set(doc) != {"schema_version", "milestones"} or type(doc["schema_version"]) is not int or doc["schema_version"] != 1:
            raise ValueError("expected schema_version: 1 and milestones only")
        sections = doc["milestones"]
        if not isinstance(sections, dict) or set(sections) != set(MILESTONES):
            raise ValueError("milestones must name all seven preparation areas")
        for name in MILESTONES:
            refs = sections[name]
            if not isinstance(refs, list) or len(refs) > 100:
                raise ValueError("each milestone must contain at most 100 evidence references")
            if not refs:
                continue
            for ref in refs:
                if not isinstance(ref, dict) or set(ref) != {"path", "sha256"} or not all(isinstance(v, str) for v in ref.values()):
                    raise ValueError("evidence reference requires path and sha256 strings")
                content = read_file(root, ref["path"])
                if not content.strip() or hashlib.sha256(content).hexdigest() != ref["sha256"]:
                    raise ValueError("empty evidence or hash mismatch: " + ref["path"])
                result["evidence_references"] += 1
            result["missing"].remove(name)
        result["manifest"] = "indexed"
    except (OSError, ValueError, TypeError, RecursionError) as exc:
        result["errors"].append(str(exc))
    return result


def compare(candidate, baseline):
    before, after = inventory(baseline), inventory(candidate)
    return {"verdict": "rejected" if after["errors"] else "inconclusive",
            "improved": False, "phase": "benchmark-preparation",
            "detail": "Evidence integrity only; owner must judge substance. Tool effectiveness is unmeasured.",
            "baseline": before, "candidate": after}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check evidence integrity in the current tree")
    parser.add_argument("--candidate", default=os.environ.get("CANDIDATE_DIR", "."))
    parser.add_argument("--baseline", default=os.environ.get("BASELINE_DIR", "."))
    args = parser.parse_args()
    if args.check:
        result = inventory(args.candidate)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 1 if result["errors"] else 0
    print(json.dumps(compare(args.candidate, args.baseline), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
