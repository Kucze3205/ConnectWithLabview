#!/usr/bin/env python3
"""Validate public change-case designs; never execute or edit LabVIEW sources."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
COMMIT = "371c631c16155d88f02be11a953e4964d7452fd8"
PREFIX = "actor-framework/Core/ActorFramework/Message Dequeuer/"
PINS = {
    "typedef-impact": ("Dequeue Priority.ctl", "4a291d5d18c372ab0221bfc84a16b56fb7e97f736329a393c047a4c84bfc4ea9", 4417),
    "diagram-difference": ("Equals Not A Refnum.vi", "19b5dcd98b3b2e83e2b533d9227bd07d16837f350243377292b7c0b8a935338c", 6847),
}
CLAIMS = {name: [f"{prefix}-{i:02d}" for i in range(1, 5)]
          for name, prefix in [("typedef-impact", "TI"), ("diagram-difference", "DD")]}
OBSERVATIONS = {
    "typedef-impact": ["TI-O1-original-properties", "TI-O2-consumer-bindings", "TI-O3-native-differences", "TI-O4-controlled-io"],
    "diagram-difference": ["DD-O1-original-dataflow", "DD-O2-behavior-variant", "DD-O3-presentation-variant", "DD-O4-uncertainty"],
}
CANDIDATES = [
    ("Dequeue.vi", "656c0cff6cfadbe3a918728d03a5634423a26b0e55605cc29de50481c8072fbc", "potentially-affected"),
    ("Equals Not A Refnum.vi", "19b5dcd98b3b2e83e2b533d9227bd07d16837f350243377292b7c0b8a935338c", "potentially-unaffected-negative-control"),
]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def mapping(value, reason):
    require(isinstance(value, dict), reason)
    return value


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, minimum=1):
    return isinstance(value, list) and len(value) >= minimum and all(nonempty(x) for x in value)


def validate(spec, case):
    mapping(spec, "spec object required")
    require(spec.get("schema_version") == 1 and type(spec.get("schema_version")) is int, "schema version")
    require(spec.get("case_id") == case and spec.get("revision") == "design-1", "case identity/revision")
    require(spec.get("status") == "design-only", "design status")
    source = mapping(spec.get("source"), "source required")
    filename, digest, size = PINS[case]
    require(source.get("repository") == "NI Actor Framework" and source.get("commit") == COMMIT, "source provenance")
    require((source.get("path"), source.get("sha256"), source.get("size_bytes")) == (PREFIX + filename, digest, size), "source pin")
    require(nonempty(source.get("save_version")) and nonempty(source.get("preservation")), "source preservation/version")
    scope = mapping(spec.get("scope"), "scope required")
    require(scope.get("partition") == "public-development" and scope.get("lineage_group") == "public-ni-actor-framework-all-projects-copies-variants", "public lineage")
    require(type(scope.get("native_executions")) is int and scope["native_executions"] == 0 and type(scope.get("edits_performed")) is int and scope["edits_performed"] == 0 and scope.get("key_established") is False, "zero execution/no key")
    require(nonempty(scope.get("limitations")), "limitations required")
    auth = mapping(spec.get("authorization"), "authorization required")
    require(all(auth.get(k) is True for k in ["explicit_owner_grant_required_for_edits", "explicit_owner_grant_required_for_builds", "derived_copies_only"]) and auth.get("grant_obtained") is False, "owner grant flags")
    require(auth.get("authority") == "benchmark/protocol.md:120" and nonempty(auth.get("execution_gate")), "grant authority/gate")
    docs = mapping(spec.get("documentation"), "documentation required")
    require(docs.get("pin_required") is True and docs.get("pin_fields") == ["version", "section_or_location", "sha256_or_preserved_permitted_excerpt"], "documentation pin requirements")
    require(docs.get("authority") == "benchmark/protocol.md:59" and docs.get("status") == "gap" and strings(docs.get("unpinned")) and nonempty(docs.get("rule")), "documentation gap")
    require(spec.get("inventory_frozen") is True and spec.get("required_claim_ids") == CLAIMS[case], "frozen claim ids")
    require(spec.get("required_observation_ids") == OBSERVATIONS[case], "frozen observation ids")
    questions = spec.get("questions")
    require(isinstance(questions, list) and len(questions) == 4 and all(isinstance(q, dict) for q in questions), "questions required")
    require([q.get("claim_id") for q in questions] == CLAIMS[case] and all(nonempty(q.get("question")) for q in questions), "question claim alignment")
    answers = spec.get("native_answers")
    require(isinstance(answers, list) and len(answers) == 4 and all(isinstance(a, dict) for a in answers), "native answers required")
    require([a.get("claim_id") for a in answers] == CLAIMS[case], "native answer claim alignment")
    require(all(a.get("status") == "unavailable" and "answer" in a and a["answer"] is None and a.get("citations") == [] and nonempty(a.get("reason")) and "#169" in a["reason"] for a in answers), "native answers unavailable #169")
    require(strings(spec.get("observation_procedure"), 4), "observation procedure required")
    require(strings(spec.get("checker_steps"), 4), "checker steps required")
    recipes = spec.get("edit_recipes")
    expected = [("TI-E1", "type-changing")] if case == "typedef-impact" else [("DD-E1", "behavior-changing"), ("DD-E2", "presentation-only")]
    require(isinstance(recipes, list) and len(recipes) == len(expected) and all(isinstance(r, dict) for r in recipes), "edit recipes required")
    require([(r.get("recipe_id"), r.get("category")) for r in recipes] == expected, "recipe categories")
    for recipe in recipes:
        require(recipe.get("status") == "not-executed" and recipe.get("derived_copies_only") is True, "derived unexecuted recipes")
        require(nonempty(recipe.get("preconditions")) and strings(recipe.get("steps"), 3), "recipe preconditions/steps")
    if case == "typedef-impact":
        candidates = spec.get("consumer_candidates")
        require(isinstance(candidates, list) and len(candidates) == 2 and all(isinstance(c, dict) for c in candidates), "consumer candidates required")
        for candidate, (name, sha, role) in zip(candidates, CANDIDATES):
            require((candidate.get("path"), candidate.get("sha256"), candidate.get("role")) == (PREFIX + name, sha, role), "consumer candidate pins")
            require(candidate.get("status") == "unconfirmed" and nonempty(candidate.get("static_evidence")), "unconfirmed static candidates")
    else:
        require("No paired public revisions" in scope["limitations"] and "returned 1" in scope["limitations"], "single commit revision gap")
        uncertain = mapping(spec.get("uncertain_effect_category"), "uncertain category required")
        require(uncertain.get("category") == "uncertain-effect" and strings(uncertain.get("criteria"), 4) and nonempty(uncertain.get("handling")), "uncertain effect handling")


def rejecting_mutations(specs):
    tests = [
        ("typedef-impact", lambda s: s["required_claim_ids"].pop(), "frozen claim ids"),
        ("typedef-impact", lambda s: s["native_answers"][0].update(status="available", answer=True), "native answers unavailable #169"),
        ("diagram-difference", lambda s: s["authorization"].update(explicit_owner_grant_required_for_edits=False), "owner grant flags"),
        ("diagram-difference", lambda s: s["authorization"].update(explicit_owner_grant_required_for_builds=False), "owner grant flags"),
        ("typedef-impact", lambda s: s["consumer_candidates"][0].update(status="confirmed"), "unconfirmed static candidates"),
        ("diagram-difference", lambda s: s["edit_recipes"][1].update(derived_copies_only=False), "derived unexecuted recipes"),
        ("diagram-difference", lambda s: s["documentation"].update(pin_fields=["version"]), "documentation pin requirements"),
        ("typedef-impact", lambda s: s["source"].update(sha256="0" * 64), "source pin"),
        ("diagram-difference", lambda s: s.pop("uncertain_effect_category"), "uncertain category required"),
        ("typedef-impact", lambda s: s["native_answers"][1].update(reason="pending"), "native answers unavailable #169"),
    ]
    def expect_reject(case, changed, reason):
        try:
            validate(changed, case)
        except ValueError as exc:
            assert str(exc) == reason, (reason, str(exc))
        else:
            raise AssertionError(f"mutation accepted: {reason}")

    for case, mutate, reason in tests:
        changed = copy.deepcopy(specs[case])
        mutate(changed)
        expect_reject(case, changed, reason)

    case, mutate, actual_reason = tests[0]
    changed = copy.deepcopy(specs[case])
    mutate(changed)
    wrong_reason = actual_reason + " [deliberately wrong suffix]"
    try:
        expect_reject(case, changed, wrong_reason)
    except AssertionError as exc:
        require(exc.args == ((wrong_reason, actual_reason),),
                f"reason comparison self-test: wrong mismatch error: {exc}")
    else:
        raise ValueError("reason comparison self-test: mismatch accepted")
    print("PASS: reason comparison self-test rejects a deliberately wrong expected reason")
    return (len(tests), 1)


def check_sources(specs):
    environment = os.environ.get("LABVIEW_ENVIRONMENT")
    if not environment:
        print("SKIPPED: source sha256 verification; LABVIEW_ENVIRONMENT is not set")
        return
    root = Path(environment).resolve(strict=True)
    pins = {}
    for spec in specs.values():
        records = [spec["source"]] + spec.get("consumer_candidates", [])
        for record in records:
            pins[record["path"]] = record["sha256"]
    for relative, expected in pins.items():
        path = (root / relative).resolve(strict=True)
        require(path.is_relative_to(root) and path.is_file(), f"source containment: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected, f"source sha256 mismatch: {relative}")
    print(f"PASS: {len(pins)} prepared source sha256 pins (read only)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True, help="validate without writing files")
    parser.parse_args()
    specs = {}
    for case in PINS:
        path = ROOT / "benchmark" / "change-cases" / f"{case}.spec.json"
        spec = json.loads(path.read_text(encoding="utf-8"))
        validate(spec, case)
        specs[case] = spec
    print("PASS: two design specifications; frozen claims, unavailable native answers and grant flags")
    completed = rejecting_mutations(specs)
    require(completed == (10, 1), "rejecting controls did not complete: expected (10, 1)")
    print(f"PASS: {completed[0]} in-memory rejecting mutations with asserted reasons")
    check_sources(specs)
    print("Design validation only: zero native executions; no semantic key established.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, AssertionError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
