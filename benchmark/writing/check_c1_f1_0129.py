#!/usr/bin/env python3
"""Read-only integrity/accounting check for one authored F1 overlay, not a scorer.

Only repository bytes and Python standard library are used. No historical code,
subprocess, environment, native runtime, writes, or arbitrary answer inputs.
Passing does not establish the semantic authority of this proposed local rule.
"""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREFIX = "benchmark/writing/"
CASES = PREFIX + "c1-challenges-0125-cases.json"
EXPECTATIONS = PREFIX + "c1-challenges-0125-expectations.json"
OVERLAY = PREFIX + "c1-f1-0129.json"
VERIFICATION = PREFIX + "c1-f1-0129-verification.json"
NEW_FILES = [OVERLAY, PREFIX + "c1-f1-0129.md", PREFIX + "check_c1_f1_0129.py"]
START = {
    "commit": "38183e8e52d74b67588c14be2a4052274cb54c96",
    "tree": "31ea4b54b9a9e5e8215dcdfc1478f0b5d9de84fe",
    "working_tree": "clean before authoring",
}
# Fixed measured source identities: manifest edits cannot silently rebaseline them.
SOURCE_ROWS = [
    (CASES, 31266, "73dfd06532782777d5cc7390fef290c5ef079730ed41ac9bd5786956d2b0a710"),
    (EXPECTATIONS, 1110893, "5b3761ae2b8e351038b9b2ace8b5a684940009b55e1fbee9d0907ff642864071"),
    (PREFIX + "c1-challenges-0125.md", 9775, "8cbe9c8c9aa9a4b1fb308e4050df342de079d09b3940dba85ce8b1f6fdb5661f"),
    (PREFIX + "c1-challenges-0125-findings.md", 2991, "a6888f282d1da28258dc460e954d8472d0c997d4f67515a2d7fb5b661782c0a7"),
    (PREFIX + "reviews-0128/handoff-0128.md", 5106, "13c006165e16e6c559e252b470713a3a41e27c1d8d5459888495d54d3f036ff1"),
    (PREFIX + "reviews-0128/c1-findings-0126.md", 7179, "519fe802c72d1089b55425936ce31485d9d7502b2c602b72bdda92c11f4fbf41"),
    (PREFIX + "reviews-0128/c1-review-completion-0127.json", 10038, "fc11233cd67752355607350a4a223395db07ee65a7933004517f85225d6cf600"),
    (PREFIX + "reviews-0128/integrity-0128.json", 12665, "5e45a9eb16f047ab1eaecfb4dd68e3ed9ee034fb6e11321d9eed6a749ef842b4"),
    (PREFIX + "method.json", 45705, "276f2881c70eae311195a4cc0a802e316ca06a206a0f1d16e7f041205fd3b0ac"),
    (PREFIX + "wp1-key-0119.json", 327961, "2afdca4bfc6feaa9464348bed7709b0657ea1ccbbe5d6b0a33b549c78f41c142"),
    (PREFIX + "wp1-examples-0121.json", 204095, "8c6f6d82e4fdc9db268827fd1cc942daebf84319336bba3e7141a7a110a8e382"),
    ("benchmark/protocol.md", 38342, "1aeb83227dc11761160ff80d24eb03a216a2531d90c1a6d10ccb25bb85c7eb2f"),
    ("docs/perpetua/evaluation.md", 7552, "d9eb079a6be4a99aa4697433ce56ac2ef0d05dff15074b24215c8947b6e6e8d8"),
    ("goal/goal.md", 4161, "5ee530059fd3efd34280ba632f160bbf37cb4f13c5d3e09cd841966ede5929cb"),
    ("benchmark/preparation.json", 12895, "b6f9721c4518e2b9d9ed1be6a962175935f82991fd2e606ee27f5f737be97f25"),
]
PINS = [{"path": p, "bytes": n, "sha256": h} for p, n, h in SOURCE_ROWS]
SHA_BY_PATH = {r["path"]: r["sha256"] for r in PINS}
CATEGORIES = ["correct", "incorrect", "partial", "missing", "unverified", "unsupported", "error", "unexecuted"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_bytes(path):
    relative = Path(path)
    require(not relative.is_absolute() and ".." not in relative.parts, "unsafe repository path")
    target = ROOT
    for part in relative.parts:
        target = target / part
        require(not target.is_symlink(), "symlink: " + path)
    require(target.is_file(), "missing file: " + path)
    data = target.read_bytes()
    require(0 < len(data) < 2_000_000, "file size: " + path)
    return data


def load(path):
    return json.loads(read_bytes(path))


def check_pin(record):
    data = read_bytes(record["path"])
    require(len(data) == record["bytes"], "byte length mismatch: " + record["path"])
    require(hashlib.sha256(data).hexdigest() == record["sha256"], "sha256 mismatch: " + record["path"])


def pointer(document, locator):
    value = document
    for part in locator.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def assessment(required, extras, dimension):
    # Protocol L41 bookkeeping only; the labels are authored inputs, not inferred truth.
    require(bool(required), "empty inventory cannot be correct")
    values = [r[dimension] for r in required + extras]
    if "incorrect" in values:
        return "incorrect"
    if "unverified" in values:
        return "unverified"
    if all(v == "correct" for v in values):
        return "correct"
    if any(v in ("correct", "partial") for v in values):
        return "partial"
    if "error" in values:
        return "error"
    if all(r[dimension] == "unsupported" for r in required):
        return "unsupported"
    return "missing"


def main():
    v = load(VERIFICATION)
    d = load(OVERLAY)
    require(v["protected_sources"] == d["protected_sources"] == PINS, "protected pin set/rebaseline")
    for record in PINS:
        check_pin(record)
    require([r["path"] for r in v["files"]] == NEW_FILES, "new semantic manifest paths")
    for record in v["files"]:
        require(set(record) == {"path", "bytes", "sha256"}, "manifest row schema")
        check_pin(record)
    require(v["start"] == d["start"] == START, "recorded start identity")
    require(v["changed_paths"] == sorted(NEW_FILES + [VERIFICATION]), "four-addition scope")
    require(v["scope_limits"]["preexisting_files_changed"] == [], "preexisting edits declared")
    require(v["scope_limits"]["historical_0125_checker_executed"] is False, "historical checker scope")
    require(v["scope_limits"]["semantic_authority"] is False, "no semantic authority")
    require(d["revision"] == "c1-f1-0129" and d["issue"] == 611, "overlay identity")
    require(d["status"] == "proposed-F1-resolution-pending-separate-review", "proposal status")
    require(d["benchmark_ready"] is False and v["benchmark_ready"] is False, "readiness")
    require(d["application"]["base_expectations"] == EXPECTATIONS, "base expectations")
    require(d["application"]["replace_pointer"] == "/cases/7", "N08-only replacement")
    require(d["application"]["replacement_pointer"] == "/revised_n08", "replacement locator")
    c = load(CASES)
    e = load(EXPECTATIONS)
    old = e["cases"][7]
    new = d["revised_n08"]
    prior = old["atoms"][11]
    raw = c["cases"][7]["raw_answer"].encode("utf-8")
    require(c["cases"][7]["id"] == old["id"] == new["id"] == "C1-0125-N08-v1", "case identity")
    require(d["raw_answer"] == {
        "locator": CASES + "#/cases/7/raw_answer", "text": raw.decode("utf-8"),
        "bytes": 636, "sha256": "f83e7bd495cda9cb421995758109a3b5bb6e62c479d04a18f85449dc8c450bc7",
    }, "raw answer copy identity")
    require(len(raw) == c["cases"][7]["raw_utf8_bytes"] == 636, "raw answer byte length")
    require(hashlib.sha256(raw).hexdigest() == old["raw_utf8_sha256"] == d["raw_answer"]["sha256"], "raw answer hash")
    require(raw[554:635].decode("utf-8") == prior["raw_quote"] == d["finding"]["raw_quote"], "exact F1 span")
    require(prior["atom_id"] == "a11.1" and prior["property"] == "delivered_project_and_map" and prior["value"] == "absent", "historical absence row")
    require(d["frozen_V"] == c["citation_registry"]["V"], "V must stay unchanged")
    require(len(d["frozen_V"]["evidence"]) == 5, "original V reference count")
    require(all(r["locator"] != "/conditions/scenarios/abstention" for r in d["frozen_V"]["evidence"]), "no scenario pointer in V")
    rule = d["local_rule"]
    for key, value in {
        "id": "C1-F1-0129-B", "scope": "c1-f1-0129 only", "interpretation": "B",
        "submitted_evidence": "Frozen bracket citation_registry expansions, including the zero-execution record explicitly attached to V by conditions/citations; no uncited scenario evidence.",
        "deictic_scenario_reference_supplies_grounding": False,
        "scenario_truth_supplies_grounding": False, "correctness_uses_stipulated_scenario": True,
        "non_supporting_citation_outcome": "incorrect", "registry_unchanged": True,
        "raw_answer_unchanged": True, "scenario_token_added": False, "V_extended": False,
    }.items():
        require(rule[key] == value, "local B rule: " + key)
    scenario = {"path": CASES, "sha256": SHA_BY_PATH[CASES], "locator": "/conditions/scenarios/abstention"}
    execution = {"path": CASES, "sha256": SHA_BY_PATH[CASES], "locator": "/conditions/execution_record"}
    replacement = new["atoms"][11:]
    require(len(replacement) == 2, "exactly two separate inability atoms")
    changed_atom_fields = {"atom_id", "subject", "property", "value", "truth_evidence", "context_evidence", "original_output_evidence", "citation_support_decision", "correctness", "grounding", "rationale", "uncertainty"}
    for a, tag, subject in zip(replacement, ["project", "map"], ["edited project", "original/output map"]):
        require(set(a) == set(prior), "atom schema inheritance")
        for key in set(prior) - changed_atom_fields:
            require(a[key] == prior[key], "unexpected atom change: " + key)
        require(a["atom_id"] == "a11." + tag + "-inability", "separate atom identity")
        require(a["subject"] == "speaker supplying " + subject, "separate inability object")
        require(a["property"] == "ability_to_supply" and a["value"] == "unable", "explicit inability modality")
        require(a["truth_evidence"] == a["context_evidence"] == [scenario], "stipulated truth separated")
        require(a["original_output_evidence"] == c["citation_registry"]["V"]["evidence"] + [execution], "submitted support cannot gain scenario evidence")
        require(a["citation_ids"] == ["V"], "submitted V only")
        require(a["correctness"] == "correct" and a["grounding"] == "incorrect", "B inability outcomes")
        require(a["citation_support_decision"] == "non-supporting for inability under package-local B; scenario truth is not submitted support", "support decision")
        require(bool(a["rationale"]) and bool(a["uncertainty"]), "rationale/uncertainty required")
        for record in a["truth_evidence"] + a["original_output_evidence"]:
            require(record["sha256"] == SHA_BY_PATH[record["path"]], "citation container pin")
            pointer(load(record["path"]), record["locator"])
    # Construct the entire allowed N08 delta from pinned history and checked atoms.
    expected = copy.deepcopy(old)
    expected["atoms"] = old["atoms"][:11] + replacement
    expected["required_items"][2]["atom_ids"] = [a["atom_id"] for a in expected["atoms"]]
    expected["required_items"][2]["grounding"] = "incorrect"
    expected["required_counts"]["grounding"]["correct"] = 0
    expected["required_counts"]["grounding"]["incorrect"] = 1
    expected["assessment"]["grounding"] = "incorrect"
    require(new == expected, "change outside exact F1 delta")
    paths = ["/cases/7/atoms/11", "/cases/7/required_items/2/atom_ids", "/cases/7/required_items/2/grounding", "/cases/7/required_counts/grounding", "/cases/7/assessment/grounding"]
    require([x["original_locator"] for x in d["changes"]] == [EXPECTATIONS + "#" + p for p in paths], "exact delta locator list")
    for index, (entry, path) in enumerate(zip(d["changes"], paths)):
        require(entry["before"] == pointer(e, path), "before record: " + path)
        if index == 0:
            require(entry["after"] == replacement, "two replacement records")
            require(entry["revised_locators"] == [OVERLAY + "#/revised_n08/atoms/11", OVERLAY + "#/revised_n08/atoms/12"], "atom after locators")
        else:
            locator = "/revised_n08" + path.removeprefix("/cases/7")
            require(entry["after"] == pointer(d, locator), "after record: " + path)
            require(entry["revised_locator"] == OVERLAY + "#" + locator, "after locator: " + path)
        require(bool(entry["reason"]), "delta rationale")
    for case in [old, new]:
        require(case["required_denominator_per_dimension"] == len(case["required_items"]) == 3, "fixed required denominator")
        require(case["extras"] == case["duplicates"] == case["contradictions"] == [], "empty extras/duplicates/contradictions")
        for dimension in ["correctness", "grounding"]:
            tally = Counter(r[dimension] for r in case["required_items"])
            require(case["required_counts"][dimension] == {k: tally[k] for k in CATEGORIES}, "required recount")
            require(case["extra_counts"][dimension] == {k: 0 for k in CATEGORIES}, "extra recount")
            require(case["assessment"][dimension] == assessment(case["required_items"], case["extras"], dimension), "L41 accounting")
    require(d["non_submission_context"] == [
        {"object": subject, "property": "submission_status", "value": "not-submitted", "truth_evidence": [scenario], "role": "context-only stipulated fact; not a submitted inability assertion, not an extra, not scored"}
        for subject in ["edited project", "original/output map"]
    ], "absence context remains separate from asserted inability")
    consequences = d["consequences"]
    require(consequences["n08_atom_count"] == {"before": 12, "after": 13}, "N08 atom count")
    total = sum(len(case["atoms"]) for case in e["cases"])
    require(consequences["package_atom_count"] == {"before": total, "after": total + 1} and total == 265, "package atom accounting")
    require(consequences["required_denominators"] == e["inherited_denominators"], "inherited denominators")
    for label, case in [("before", old), ("after", new)]:
        require(consequences["missing_slots"][label] == {r["id"]: r["missing_slots"] for r in case["required_items"]}, "omission records")
        require(consequences["required_counts"][label] == case["required_counts"], "consequence counts")
        require(consequences["whole_answer"][label] == case["assessment"], "whole answer before/after")
    require(consequences["missing_slots"]["before"] == consequences["missing_slots"]["after"], "no omitted slot erased")
    for item in new["required_items"]:
        require(item["required_slots"] == e["required_slot_inventory"][item["id"]], "no new required slots")
        represented = {a["slot"] for a in new["atoms"] if a["required_id"] == item["id"]}
        require(item["missing_slots"] == [s for s in item["required_slots"] if s not in represented], "slot bookkeeping")
    history = d["historical_interpretations"]
    for branch, grounding in [("A", "correct"), ("B", "incorrect")]:
        require(history[branch]["inability"] == history[branch]["honest_limits"] == {"correctness": "correct", "grounding": grounding}, "historical branch outcomes")
        require(history[branch]["whole_answer"] == {"correctness": "partial", "grounding": "partial" if branch == "A" else "incorrect"}, "historical whole-answer branch")
    boundaries = {
        "historical_verdicts": {"Standards": "CLEAR", "Spec": "NOT-CLEAR"},
        "F1": "proposed pending separate review", "actual_human_C1": "pending",
        "historical_F4": "blocked", "general_established_key_release": "blocked",
        "full_trial_release": "blocked", "method_acceptance": "pending", "owner_acceptance": "pending",
        "native_execution": False, "native_or_product_quality_claim": False, "independent_semantic_recheck": False,
    }
    require(d["boundaries"] == boundaries, "no boundary promotion")
    require(d["exposure"]["candidate"] == "codex/gpt-6.1-sol" and d["exposure"]["startup_label"] == "claude-sonnet-5-5", "exposure labels")
    require(d["exposure"]["continuity"] == "uncertified", "continuity")
    require(all(d["exposure"][key] is False for key in ["cold_independence", "human_result", "withheld", "model_unseen"]), "no independence/human claim")
    print(json.dumps({"result": "pass", "protected_sources": len(PINS), "new_semantic_files": len(NEW_FILES), "delta_entries": len(paths), "n08_atoms_before": 12, "n08_atoms_after": 13, "whole_answer_before": old["assessment"], "whole_answer_after": new["assessment"], "scope": "repository byte integrity and authored accounting only", "semantic_authority": False}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, IndexError, TypeError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit("FAIL: " + str(exc))
