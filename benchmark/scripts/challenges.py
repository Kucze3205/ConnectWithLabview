#!/usr/bin/env python3
"""Generate deterministic public development challenge fixtures.

The fixtures are preparation evidence, not a scorer. Every positive control is a
materialized answer and reader submission in the case contracts, with fixed
per-ID outcomes and separate accounting ledgers. Mutations contain changed
records rather than prose descriptions. --check never writes.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = ROOT / "benchmark" / "cases" / "dev"
OUT_DIR = ROOT / "benchmark" / "challenges"
CASES = ("library-icon-tests", "library-specialty", "vi-actor-core-native-gap")


def load(case_id):
    return json.loads((CASE_DIR / (case_id + ".json")).read_text(encoding="utf-8"))


def answer_claims(case):
    rows = []
    for row in case["reference_inventory"]:
        item = {"claim_id": row["claim_id"], "answer": row["atomic_fact"].get("value"),
                "conditions": list(row.get("conditions", [])), "citations": []}
        if row.get("citations"):
            item["citations"] = [dict(row["citations"][0])]
        rows.append(item)
    return rows


def reader_observations(case):
    by_id = {row["observation_id"]: row for row in case["reader_reference_inventory"]}
    return [{"observation_id": oid, "value": by_id[oid].get("expected"),
             "scope": by_id[oid]["scope"]}
            for oid in case["required_reader_observation_ids"]]


def outcomes(case, answer="unverified", grounding="unverified", fidelity="unverified"):
    return {"answer_correctness": {"required_ids": case["denominators"]["answer_correctness"]["required_ids"],
                                    "outcome_by_id": {x: answer for x in case["denominators"]["answer_correctness"]["required_ids"]}},
            "source_grounding": {"required_ids": case["denominators"]["source_grounding"]["required_ids"],
                                  "outcome_by_id": {x: grounding for x in case["denominators"]["source_grounding"]["required_ids"]}},
            "reading_fidelity": {"required_ids": case["denominators"]["reading_fidelity"]["required_ids"],
                                  "outcome_by_id": {x: fidelity for x in case["denominators"]["reading_fidelity"]["required_ids"]}}}


def base(case, fixture_id, label):
    return {"schema_version": 2, "fixture_id": fixture_id, "label": label,
            "public_development_only": True,
            "source": {"case_id": case["case_id"], "case_revision": case["case_revision"],
                       "family": case["family"], "save_version": case["save_version"],
                       "artifact": case["artifact"]},
            "denominators": {k: case["denominators"][k]["count"] for k in
                             ("answer_correctness", "source_grounding", "reading_fidelity")},
            "submitted": {"answer_record": {"case_id": case["case_id"], "status": "complete",
                                               "claims": answer_claims(case), "limitations": ""},
                          "reader_response": {"probe_id": case["reader_probe_contract"]["probe_id"],
                                              "status": "complete", "observations": reader_observations(case),
                                              "limitations": ""}},
            "expected": {"outcomes": outcomes(case), "extras_ledger": [], "duplicates": [],
                         "contradictions": [], "fixed_denominators": True},
            "evidence_status": "public XML literals are independently reproduced; native references remain unavailable and provisional claims remain unverified",
            "execution": {"attempted": False, "executed": False, "scored": False}}


def make():
    cases = {x: load(x) for x in CASES}
    out = {}
    c = cases["library-icon-tests"]
    f = base(c, "library-icon-tests-positive", "complete materialized positive control")
    f["expected"]["outcomes"] = outcomes(c, "correct", "correct", "unverified")
    out[f["fixture_id"] + ".json"] = f

    c = cases["library-specialty"]
    positive = base(c, "library-specialty-positive", "complete materialized positive control")
    positive["expected"]["outcomes"] = outcomes(c, "correct", "correct", "unverified")
    out["library-specialty-positive.json"] = positive
    answer_ids = c["denominators"]["answer_correctness"]["required_ids"]
    reader_ids = c["denominators"]["reading_fidelity"]["required_ids"]

    def mutation(name, record, expected, ledgers=None):
        x = base(c, "library-specialty-" + name, "materialized challenge control: " + name)
        x["submitted"] = record
        x["expected"] = {"outcomes": expected, "extras_ledger": [], "duplicates": [],
                         "contradictions": [], "fixed_denominators": True}
        if ledgers:
            x["expected"].update(ledgers)
        return x

    omitted = json.loads(json.dumps(positive["submitted"]))
    omitted["answer_record"]["claims"] = omitted["answer_record"]["claims"][1:]
    out["library-specialty-omission.json"] = mutation("omission", omitted,
        outcomes(c, "partial", "partial", "unverified"))
    extra = json.loads(json.dumps(positive["submitted"]))
    extra["answer_record"]["claims"].append({"claim_id": "X_FALSE", "answer": "false assertion",
        "conditions": [], "citations": [dict(extra["answer_record"]["claims"][0]["citations"][0])]})
    extra["reader_response"]["observations"].append({"observation_id": "X_FALSE", "value": "false assertion", "scope": "extra"})
    out["library-specialty-extra-false.json"] = mutation("extra-false", extra,
        outcomes(c, "incorrect", "incorrect", "incorrect"), {"extras_ledger": [{"id": "X_FALSE", "answer_outcome": "false", "reader_outcome": "false"}]})
    duplicate = json.loads(json.dumps(positive["submitted"]))
    duplicate["answer_record"]["claims"].append(dict(duplicate["answer_record"]["claims"][0]))
    duplicate["reader_response"]["observations"].append(dict(duplicate["reader_response"]["observations"][0]))
    out["library-specialty-duplicate.json"] = mutation("duplicate", duplicate,
        outcomes(c, "correct", "correct", "unverified"), {"duplicates": [{"answer_id": answer_ids[0], "reader_id": reader_ids[0]}]})
    contradiction = json.loads(json.dumps(positive["submitted"]))
    contradiction["answer_record"]["claims"].append({"claim_id": answer_ids[0] + "-contradiction", "answer": "CONTRADICTORY-LITERAL", "conditions": [], "citations": []})
    contradiction["reader_response"]["observations"].append({"observation_id": reader_ids[0] + "-contradiction", "value": "CONTRADICTORY-LITERAL", "scope": "same-required-observation"})
    out["library-specialty-contradiction.json"] = mutation("contradiction", contradiction,
        outcomes(c, "incorrect", "incorrect", "incorrect"), {"contradictions": [{"answer_id": answer_ids[0], "reader_id": reader_ids[0]}]})
    empty = json.loads(json.dumps(positive["submitted"]))
    empty["reader_response"] = {"probe_id": c["reader_probe_contract"]["probe_id"], "status": "empty", "observations": [], "limitations": "empty response"}
    out["library-specialty-empty.json"] = mutation("empty", empty, outcomes(c, "unverified", "unverified", "missing"))
    failed = json.loads(json.dumps(positive["submitted"]))
    failed["reader_response"] = {"probe_id": c["reader_probe_contract"]["probe_id"], "status": "error", "observations": [], "limitations": "controlled reader error", "error": "controlled reader error"}
    out["library-specialty-error.json"] = mutation("error", failed, outcomes(c, "unverified", "unverified", "error"))

    c = cases["vi-actor-core-native-gap"]
    gap = base(c, "vi-actor-core-native-gap", "explicit native gap and unsupported control")
    gap["submitted"]["answer_record"]["status"] = "unsupported"
    gap["submitted"]["answer_record"]["limitations"] = "Native connector, diagram and controlled behavior evidence unavailable."
    gap["submitted"]["reader_response"]["status"] = "unsupported"
    gap["submitted"]["reader_response"]["limitations"] = "Concrete reader adapter and native reference unavailable."
    gap["expected"]["outcomes"] = outcomes(c, "unsupported", "unsupported", "unsupported")
    gap["gaps"] = [{"required_id": x, "status": "explicit-gap", "reason": "native evidence unavailable"} for x in c["required_answer_claim_ids"]]
    out["vi-actor-core-native-gap.json"] = gap
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    rendered = {name: json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n" for name, value in make().items()}
    actual = {p.name: p.read_text(encoding="utf-8") for p in OUT_DIR.glob("*.json")}
    if args.check:
        if actual != rendered:
            raise SystemExit("challenge bytes differ")
        print("challenge fixtures match")
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in rendered.items():
        (OUT_DIR / name).write_text(text, encoding="utf-8")
    for name in set(actual) - set(rendered):
        (OUT_DIR / name).unlink()
    print("wrote %d challenge fixtures" % len(rendered))

if __name__ == "__main__":
    main()
