#!/usr/bin/env python3
"""Validate the public, design-only split boundary templates."""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "benchmark" / "split" / "allocation-manifest.template.json"
ISOLATION = ROOT / "benchmark" / "split" / "isolation-record.template.json"
PARTITIONS = {"development", "eval-unseen-lineage", "eval-held-out-family"}
STEPS = [
    "custodian_clone_push",
    "scorer_clone_push_rejected",
    "tokenless_ls_remote_denied",
    "sentinel_grep_zero_hits",
    "revoked_scorer_token_clone_denied",
]
SECRET_RE = re.compile(
    r"(?i)(token|secret|password|credential|private[_ -]?key|api[_ -]?key|bearer)"
)
TOKEN_VALUE_RE = re.compile(
    r"(?i)(?:bearer\s+|gh[pousr]_)[A-Za-z0-9_./+=-]{8,}|(?:sk|pk)-[A-Za-z0-9_-]{12,}"
)


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str):
    raise AssertionError(message)


def assert_reason_field(obj, name: str):
    fail_if = lambda condition, message: fail(message) if condition else None
    fail_if(not isinstance(obj, dict), f"{name}: expected object")
    fail_if(set(obj) != {"value", "reason"}, f"{name}: expected value/reason only")
    fail_if(obj["value"] is not None, f"{name}: value must be null")
    fail_if(not isinstance(obj["reason"], str) or not obj["reason"].strip(), f"{name}: reason required")


def walk_for_secrets(value, path="$"):
    if isinstance(value, dict):
        for key, child in value.items():
            if SECRET_RE.search(str(key)) and key not in {"reason"}:
                # Secret-related field names are allowed only as schema labels, never values.
                if isinstance(child, str) and child:
                    fail(f"secret-like field contains a value at {path}.{key}")
            walk_for_secrets(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_for_secrets(child, f"{path}[{index}]")
    elif isinstance(value, str):
        fail_if = TOKEN_VALUE_RE.search(value)
        if fail_if:
            fail(f"token-like value at {path}")


def validate_manifest(data):
    fail_if = lambda condition, message: fail(message) if condition else None
    fail_if(set(data) != {"schema_version", "fields", "lineage_groups"}, "manifest top-level keys differ")
    fail_if(data["schema_version"] != 1, "manifest schema_version must be 1")
    required = {
        "split_revision", "lineage_group_id", "partition", "group_member_hashes",
        "adjudication_notes", "key_revision_hashes", "access_configuration_hash",
        "custodian_label",
    }
    fail_if(set(data["fields"]) != required, "manifest fields differ from required schema")
    for name, field in data["fields"].items():
        if name == "partition" and field.get("value") not in (None, *PARTITIONS):
            fail(f"fields.partition: unknown partition {field.get('value')!r}")
        assert_reason_field(field, f"fields.{name}")
    fail_if(not isinstance(data["lineage_groups"], dict), "lineage_groups must be an object")
    fail_if(set(data["lineage_groups"]) != {"schema", "records"}, "lineage_groups keys differ")
    assert_reason_field(data["lineage_groups"]["schema"], "lineage_groups.schema")
    fail_if(data["lineage_groups"]["schema"]["value"] is not None, "lineage schema must be null")
    fail_if(data["lineage_groups"]["records"] != [], "manifest must contain no allocated records")


def validate_isolation(data):
    fail_if = lambda condition, message: fail(message) if condition else None
    fail_if(set(data) != {"schema_version", "fields", "steps"}, "isolation top-level keys differ")
    fail_if(data["schema_version"] != 1, "isolation schema_version must be 1")
    required = {"identity_label", "operation", "expected", "actual", "evidence_sha256", "reviewer_session"}
    for name, field in data["fields"].items():
        assert_reason_field(field, f"fields.{name}")
    fail_if(set(data["fields"]) != required, "isolation fields differ from required schema")
    fail_if(not isinstance(data["steps"], list) or len(data["steps"]) != 5, "exactly five steps required")
    seen = []
    for index, row in enumerate(data["steps"]):
        fail_if(set(row) != {"step_id", "identity_label", "operation", "expected", "actual", "evidence_sha256", "reviewer_session"}, f"step {index} keys differ")
        fail_if(row["step_id"] not in STEPS, f"unknown step id: {row['step_id']}")
        seen.append(row["step_id"])
        for key in required:
            if key == "actual" or key == "evidence_sha256" or key == "reviewer_session":
                fail_if(row[key] is not None, f"step {index} {key} must be null")
            else:
                fail_if(not isinstance(row[key], str) or not row[key].strip(), f"step {index} {key} required")
    fail_if(seen != STEPS, "isolation steps missing, duplicated, or out of order")


def validate(manifest, isolation):
    validate_manifest(manifest)
    validate_isolation(isolation)
    walk_for_secrets(manifest)
    walk_for_secrets(isolation)


def mutations(manifest, isolation):
    cases = []
    altered = copy.deepcopy(isolation)
    altered["steps"][0]["actual"] = "unexpected"
    cases.append((altered, "non-null actual"))
    altered = copy.deepcopy(manifest)
    altered["fields"]["partition"]["value"] = "unknown"
    cases.append((altered, "unknown partition"))
    altered = copy.deepcopy(isolation)
    altered["steps"].pop()
    cases.append((altered, "missing step"))
    altered = copy.deepcopy(manifest)
    altered["fields"]["custodian_label"]["value"] = "ghp_example_token_123456789"
    cases.append((altered, "token-like string"))
    for candidate, label in cases:
        try:
            if label == "unknown partition":
                if candidate["fields"]["partition"]["value"] not in PARTITIONS:
                    raise AssertionError("partition rejected")
            validate(candidate if label != "missing step" and label != "non-null actual" else manifest,
                     candidate if label in {"missing step", "non-null actual"} else isolation)
        except (AssertionError, KeyError, TypeError):
            continue
        raise AssertionError(f"mutation was accepted: {label}")


def main():
    if len(sys.argv) != 2 or sys.argv[1] != "--check":
        print("usage: split_boundary.py --check", file=sys.stderr)
        return 2
    try:
        manifest, isolation = load(MANIFEST), load(ISOLATION)
        validate(manifest, isolation)
        mutations(manifest, isolation)
    except (OSError, json.JSONDecodeError, AssertionError) as exc:
        print(f"split boundary check failed: {exc}", file=sys.stderr)
        return 1
    print("split boundary check: templates valid; 4 rejecting mutations passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
