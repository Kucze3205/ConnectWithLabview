#!/usr/bin/env python3
"""Generate public challenge inputs and authored expectations, never score a reader.

Only checked-in development inventories are read. Native references and independent
review remain unavailable. Synthetic raw responses below are inputs, not run evidence.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = ROOT / "benchmark/cases/dev"
OUT_DIR = ROOT / "benchmark/challenges"
DIMENSIONS = {"correctness": "answer_correctness", "grounding": "source_grounding",
              "fidelity": "reading_fidelity"}
OUTCOMES = ("correct", "partial", "incorrect", "missing", "unsupported", "unverified", "error")
CASES = ("library-icon-tests", "library-specialty", "vi-actor-core-native-gap")
CONSTANT_EXPORT = '{"status":"complete","observations":[{"observation_id":"R0001","scope":"/Library/@LVVersion","value":"20008000"},{"observation_id":"R0005","scope":"/Library/Item[1]/@Name","value":"Actor.lvclass"}]}\n'


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_case(name):
    return json.loads((CASE_DIR / (name + ".json")).read_text(encoding="utf-8"))


def aggregate(items, extras):
    """Apply protocol precedence to authored labels, not to submitted content."""
    labels = list(items) + list(extras)
    if not items:
        return "unverified"
    if "incorrect" in labels:
        return "incorrect"
    if "unverified" in labels:
        return "unverified"
    if all(x == "correct" for x in labels):
        return "correct"
    if any(x in ("correct", "partial") for x in labels):
        return "partial"
    if "error" in labels:
        return "error"
    if all(x == "unsupported" for x in items):
        return "unsupported"
    return "missing"


def submission(case):
    claims = [{"claim_id": row["claim_id"], "answer": row["atomic_fact"]["value"],
               "conditions": deepcopy(row["conditions"]), "citations": deepcopy(row["citations"])}
              for row in case["reference_inventory"]]
    observations = [{"observation_id": row["observation_id"], "scope": row["scope"],
                     "value": row["expected"]}
                    for row in case["reader_reference_inventory"]]
    unavailable = [r["claim_id"] for r in case["reference_inventory"]
                   if r["atomic_fact"]["value"] is None]
    native_ids = [r["observation_id"] for r in case["reader_reference_inventory"]]
    return {"answer_record": {"case_id": case["case_id"], "status": "incomplete",
                             "claims": claims,
                             "limitations": "Null entries are unavailable answers for " + ", ".join(unavailable)
                             + "; they assert no native fact and have no supporting native locator."},
            "reader_response": {"probe_id": case["reader_probe_contract"]["probe_id"],
                                "status": "incomplete", "observations": observations,
                                "limitations": "No native alignment is available for " + ", ".join(native_ids)
                                + "; null entries assert no observation."}}


def control(case, name, purpose):
    ids = {d: deepcopy(case["denominators"][key]["required_ids"])
           for d, key in DIMENSIONS.items()}
    outcomes = {d: {i: ("correct" if i.startswith("A") else "unverified") for i in ids[d]}
                for d in ("correctness", "grounding")}
    outcomes["fidelity"] = {i: "unverified" for i in ids["fidelity"]}
    return {"name": name, "purpose": purpose, "submitted": submission(case),
            "expected": {"required_ids": ids, "per_id": outcomes,
                         "extras_ledger": [], "duplicates_ledger": [], "contradictions_ledger": []},
            "evidence": [],
            "_raw_override": None, "_operation": {"exit_code": 0, "error": None, "truncated": False}}


def change_expected(c, dimension, item, outcome):
    c["expected"]["per_id"][dimension][item] = outcome


def claim(c, item):
    return next(x for x in c["submitted"]["answer_record"]["claims"] if x["claim_id"] == item)


def observation(c, item):
    return next(x for x in c["submitted"]["reader_response"]["observations"] if x["observation_id"] == item)


def evidence(case, item):
    index, row = next((n, r) for n, r in enumerate(case["reference_inventory"]) if r["claim_id"] == item)
    return {"inventory": "benchmark/cases/dev/" + case["case_id"] + ".json",
            "json_pointer": "/reference_inventory/" + str(index),
            "literal": deepcopy(row["atomic_fact"]), "citations": deepcopy(row["citations"]),
            "status": "provisional XML author extraction; independent review pending"}


def finish_control(case, c):
    expected = c["expected"]
    raw_override = c.pop("_raw_override")
    operation = c.pop("_operation")
    answer_text = encoded(c["submitted"]["answer_record"])
    response_text = encoded(c["submitted"]["reader_response"]) if raw_override is None else raw_override
    request = {"probe_id": case["reader_probe_contract"]["probe_id"],
               "entry_point": case["reader_probe_contract"]["entry_point"],
               "arguments": deepcopy(case["reader_probe_contract"]["arguments"])}
    c["submitted"]["raw_answer_record"] = {"encoding": "utf-8", "text": answer_text,
                                           "sha256": digest(answer_text)}
    c["submitted"]["raw_reader_response"] = {"encoding": "utf-8", "text": response_text,
                                              "sha256": digest(response_text)}
    c["probe"] = {"request": request, "raw_request": encoded(request),
                  "raw_request_sha256": digest(encoded(request)),
                  "reader_revision": None, "configuration_revision": None,
                  "environment": "synthetic public fixture; no reader/runtime invoked",
                  "timestamps": {"start": None, "end": None},
                  "simulated_operation": operation,
                  "actual_execution": {"planned": 1, "attempted": 0, "executed": 0, "scored": 0}}
    alignment = []
    obs = c["submitted"]["reader_response"].get("observations", [])
    for row in case["reader_reference_inventory"]:
        item = row["observation_id"]
        positions = [n for n, o in enumerate(obs) if o["observation_id"] == item]
        alignment.append({"observation_id": item, "aligned_claim_id": row["aligned_claim_id"],
                          "raw_json_pointers": ["/observations/" + str(n) for n in positions],
                          "reference_scope": row["scope"], "xml_expected": row["expected"],
                          "native_reference": "unavailable", "expected_outcome": expected["per_id"]["fidelity"][item]})
    c["alignment"] = alignment
    expected["fixed_denominators"] = {d: len(v) for d, v in expected["required_ids"].items()}
    expected["counts"] = {d: {o: list(rows.values()).count(o) for o in OUTCOMES}
                          for d, rows in expected["per_id"].items()}
    expected["dimensions"] = {
        d: aggregate(list(rows.values()), [x["outcomes"][d] for x in expected["extras_ledger"] if d in x["outcomes"]])
        for d, rows in expected["per_id"].items()}
    expected["extra_counts"] = {
        d: {o: sum(x["outcomes"].get(d) == o for x in expected["extras_ledger"]) for o in OUTCOMES}
        for d in DIMENSIONS}
    expected["assessment_basis"] = (
        "Authored expected behavior against provisional XML declarations, conditional on their independent confirmation. "
        "This is not a scorer result. Native-required answers remain unverified; every otherwise matching reader "
        "observation remains unverified without a native reference. Explicit XML contradictions are incorrect. "
        "A current independent-evidence assessment remains unverified for XML matches as well until review.")
    expected["current_evidence_per_id"] = {
        d: {i: ("unverified" if outcome == "correct" else outcome) for i, outcome in rows.items()}
        for d, rows in expected["per_id"].items()}
    expected["current_evidence_dimensions"] = {
        d: aggregate(list(rows.values()), ["unverified" if x["outcomes"][d] == "correct" else x["outcomes"][d]
                                         for x in expected["extras_ledger"] if d in x["outcomes"]])
        for d, rows in expected["current_evidence_per_id"].items()}
    return c


def add_extra(case, c, channel, kind):
    row = next(r for r in case["reference_inventory"] if r["claim_id"] == "A0005")
    value = row["atomic_fact"]["value"]
    length = len(value.encode("utf-8"))
    assertion = ("The XML-parsed literal at /Library/Item[1]/@Name has UTF-8 byte length "
                 + str(length + (1 if kind == "false" else 0)) + ".")
    if kind == "unverified":
        assertion = "The resolved native library contains exactly 999 members."
    xid = "X-" + kind
    if channel == "answer":
        cites = deepcopy(claim(c, "A0001" if kind == "false" else "A0005")["citations"])
        if kind == "unverified":
            cites = []
        rows = c["submitted"]["answer_record"]["claims"]
        pointer = "/claims/" + str(len(rows))
        rows.append({"claim_id": xid, "answer": assertion,
                     "conditions": deepcopy(row["conditions"]), "citations": cites})
        dimensions = ("correctness", "grounding")
    else:
        rows = c["submitted"]["reader_response"]["observations"]
        pointer = "/observations/" + str(len(rows))
        rows.append({"observation_id": xid, "scope": "derived UTF-8 literal length" if kind != "unverified"
                     else "resolved-native-membership", "value": assertion})
        dimensions = ("fidelity",)
    label = {"false": "incorrect", "true": "correct", "unverified": "unverified"}[kind]
    # Matching reader extras still lack native reference alignment.
    outcomes = {d: ("unverified" if d == "fidelity" and kind == "true" else label) for d in dimensions}
    c["expected"]["extras_ledger"].append({
        "assertion_id": xid, "channel": channel, "raw_json_pointer": pointer, "assertion": assertion,
        "outcomes": outcomes, "inventory_evidence": evidence(case, "A0005") if kind != "unverified" else None,
        "derivation": {"utf8_literal": value, "actual_byte_length": length} if kind != "unverified" else None,
        "reason": "Literal byte length is outside the required atomic inventory; native resolved membership has no key. "
                  "False answer cites the real save-version location, which does not support the length assertion.",
        "required_credit": 0})


def library_controls(case, extensive):
    controls = [control(case, "positive-control", "Submit every ID: all ten XML literals with supporting locators, "
                        "and both native slots explicitly null. Full correctness/grounding is unverified, not correct.")]
    if extensive:
        c = control(case, "wrong-answer-declared-dependency", "Change A0007 URL declaration, retain its valid locator. "
                    "This tests a declared dependency literal, not native resolution, computation or typedef impact.")
        claim(c, "A0007")["answer"] = "../Nonexistent Challenge Member.vi"
        for d in ("correctness", "grounding"):
            change_expected(c, d, "A0007", "incorrect")
        c["evidence"].append(evidence(case, "A0007"))
        controls.append(c)
        for name, existing in (("wrong-citation-existing", True), ("wrong-citation-unresolvable", False)):
            c = control(case, name, "Keep correct A0005 literal, replace only its citation.")
            cite = deepcopy(claim(c, "A0008")["citations"][0])
            if not existing:
                cite["locator"]["expression"] = "/Library/Item[999999]/@Name"
            claim(c, "A0005")["citations"] = [cite]
            change_expected(c, "grounding", "A0005", "incorrect")
            c["evidence"] = [evidence(case, "A0005"), evidence(case, "A0008")]
            controls.append(c)
        for channel in ("answer", "reader"):
            c = control(case, "selective-omission-" + channel, "Remove one required item; all 12 slots remain. "
                        "Native gaps keep the whole dimension unverified; XML-only conditional assessment is partial.")
            if channel == "answer":
                c["submitted"]["answer_record"]["claims"] = [r for r in c["submitted"]["answer_record"]["claims"]
                                                             if r["claim_id"] != "A0008"]
                for d in ("correctness", "grounding"):
                    change_expected(c, d, "A0008", "missing")
            else:
                c["submitted"]["reader_response"]["observations"] = [r for r in c["submitted"]["reader_response"]["observations"]
                                                                    if r["observation_id"] != "R0008"]
                change_expected(c, "fidelity", "R0008", "missing")
            controls.append(c)
            for kind in ("false", "true", "unverified"):
                c = control(case, "extra-" + kind + "-" + channel, "Retain all required slots and materialize an extra assertion.")
                add_extra(case, c, channel, kind)
                controls.append(c)
            c = control(case, "true-extra-with-omission-" + channel, "A supported extra cannot replace omitted required credit.")
            key, rows_key, id_key, item = (("answer_record", "claims", "claim_id", "A0008") if channel == "answer"
                                          else ("reader_response", "observations", "observation_id", "R0008"))
            c["submitted"][key][rows_key] = [r for r in c["submitted"][key][rows_key] if r[id_key] != item]
            for d in (("correctness", "grounding") if channel == "answer" else ("fidelity",)):
                change_expected(c, d, item, "missing")
            add_extra(case, c, channel, "true")
            controls.append(c)
            for contradiction in (False, True):
                name = "contradiction" if contradiction else "duplicate"
                c = control(case, name + "-" + channel, "Preserve both raw assertions and retain the fixed denominator.")
                key, rows_key, id_key, item, value_key = (("answer_record", "claims", "claim_id", "A0005", "answer")
                                                         if channel == "answer" else
                                                         ("reader_response", "observations", "observation_id", "R0005", "value"))
                rows = c["submitted"][key][rows_key]
                original = next(n for n, r in enumerate(rows) if r[id_key] == item)
                repeated = deepcopy(rows[original])
                if contradiction:
                    repeated[value_key] = "It is not the case that this literal equals " + repr(repeated[value_key]) + "."
                    for d in (("correctness", "grounding") if channel == "answer" else ("fidelity",)):
                        change_expected(c, d, item, "incorrect")
                rows.append(repeated)
                ledger = "contradictions_ledger" if contradiction else "duplicates_ledger"
                c["expected"][ledger].append({"channel": channel, "required_id": item,
                                              "raw_json_pointers": ["/" + rows_key + "/" + str(original),
                                                                    "/" + rows_key + "/" + str(len(rows) - 1)],
                                              "count": 1, "credit_at_most_once": True,
                                              "evidence": evidence(case, "A0005")})
                controls.append(c)
        for name, status, raw, outcome in (
            ("empty-probe", "empty", "", "missing"),
            ("wrapper-only-probe", "complete", None, "missing"),
            ("truncated-probe", "truncated", '{"status":"complete","observations":[', "missing"),
            ("unsupported-probe", "unsupported", None, "unsupported"),
            ("failed-probe", "error", None, "error"),
        ):
            c = control(case, name, "Concrete synthetic raw response; answer correctness supplies no reader credit.")
            c["submitted"]["reader_response"] = {
                "probe_id": case["reader_probe_contract"]["probe_id"], "status": status, "observations": [],
                "limitations": ("Controlled fixture: LabVIEW runtime unavailable for all required observation IDs."
                                if outcome == "unsupported" else "")}
            c["_raw_override"] = raw
            if name == "truncated-probe":
                c["_operation"]["truncated"] = True
            if outcome == "error":
                c["submitted"]["reader_response"]["error"] = {"code": "CONTROLLED_READER_ERROR", "message": "Fixture reader failed before returning observations."}
                c["_operation"] = {"exit_code": 1, "error": "CONTROLLED_READER_ERROR", "truncated": False}
            for item in c["expected"]["per_id"]["fidelity"]:
                change_expected(c, "fidelity", item, outcome)
            controls.append(c)
        for name in ("missing-independent-key", "missing-native-run", "zero-executed-tests"):
            c = control(case, name, "Concrete absence-of-evidence input; no semantic pass is available.")
            c["submitted"]["evidence_record"] = {
                "independent_key": None if name == "missing-independent-key" else "public provisional inventory only",
                "native_run": None, "report": {"planned": 1, "attempted": 0, "executed": 0, "scored": 0}}
            if name == "missing-independent-key":
                for dimension, rows in c["expected"]["per_id"].items():
                    for item in rows:
                        change_expected(c, dimension, item, "unverified")
            controls.append(c)
    c = control(case, "constant-export", "Apply identical fixed export bytes to both library probes. "
                "R0005 contradicts each original; R0001 also contradicts icon-tests. Other required IDs remain missing.")
    c["submitted"]["reader_response"] = json.loads(CONSTANT_EXPORT)
    c["_raw_override"] = CONSTANT_EXPORT
    for item in c["expected"]["per_id"]["fidelity"]:
        change_expected(c, "fidelity", item, "missing")
    change_expected(c, "fidelity", "R0001", "incorrect" if case["case_id"] == "library-icon-tests" else "unverified")
    change_expected(c, "fidelity", "R0005", "incorrect")
    c["evidence"] = [evidence(case, "A0001"), evidence(case, "A0005")]
    c["comparison"] = {"cases": ["library-icon-tests", "library-specialty"],
                       "fixed_export_sha256": digest(CONSTANT_EXPORT),
                       "contradicted_observation_ids": ["R0001", "R0005"] if case["case_id"] == "library-icon-tests" else ["R0005"],
                       "native_comparison": "explicit gap: no native references or reader executions"}
    controls.append(c)
    return [finish_control(case, c) for c in controls]


def native_controls(case):
    result = []
    for condition in ("missing-runtime", "missing-dependency", "missing-license", "inaccessible-diagram"):
        c = control(case, "unsupported-" + condition, "Synthetic declared limitation; no demonstrated native behavior.")
        limitation = "Controlled fixture condition: " + condition + "; affects N0001,N0002,N0003 and RN0001,RN0002,RN0003."
        c["submitted"]["answer_record"].update(status="unsupported", claims=[], limitations=limitation)
        c["submitted"]["reader_response"].update(status="unsupported", observations=[], limitations=limitation)
        for dimension, rows in c["expected"]["per_id"].items():
            for item in rows:
                change_expected(c, dimension, item, "unsupported")
        c["evidence"] = [{"inventory": "benchmark/cases/dev/" + case["case_id"] + ".json",
                          "json_pointer": "/dependencies_and_environment",
                          "note": "Condition is injected for the fixture, not an observed native failure."}]
        result.append(finish_control(case, c))
    return result


README = """# Public development challenge inputs

Generated by `python3 -I benchmark/scripts/challenges.py`; verify with `python3 -I benchmark/scripts/challenges.py --check`.
No environment variable, prepared source cache or non-stdlib package is needed. `--check` regenerates in memory, never writes, and rejects differing, missing or extra entries (including README and nested files).

These are synthetic inputs and authored expectations, not executed challenges or scorer results. Three public cases are planned; zero reader attempts, executions or scores exist. Every probe preserves its exact synthetic request/response text, UTF-8 SHA256, simulated failure/truncation record, and per-ID alignment. Null timestamps/revisions mean no execution evidence exists. The concrete reader adapter is unavailable.

Both libraries freeze 12 IDs per dimension: ten XML declaration IDs plus two unavailable native IDs. The VI freezes three native IDs per dimension. Every positive submission includes all IDs; unavailable answers are null, carry no fabricated citation, and remain unverified. All ten XML literals have their real supporting inventory locators. No complete positive control can currently earn `correct`: native-required slots prevent it. `expected.per_id` is the provisional author's XML expectation conditional on independent confirmation; `current_evidence_per_id` additionally marks XML matches unverified pending that review. Dimensions and all seven outcome counts are recorded for both fixed inventories; extra outcomes are separate and never alter denominators. Reader matches are always unverified without native references. Known XML contradictions are deliberately incorrect author expectations, pending independent confirmation of the underlying evidence.

The table covers every [protocol challenge row](../protocol.md#challenges). Control names below occur in [library-icon-tests.json](library-icon-tests.json) unless another fixture is named. [library-specialty.json](library-specialty.json) supplies the second positive and constant-export comparison; [vi-actor-core-native-gap.json](vi-actor-core-native-gap.json) supplies unsupported conditions.

| Protocol row | Fixture/control names | Setup or explicit gap, and why |
|---|---|---|
| Positive controls | Both libraries: `positive-control` | Full materialized submissions and ten supporting XML locators; two native answer slots null. Whole correctness/grounding and fidelity are unverified. Independent XML checking and native evidence are gaps; no scorer that rejects everything has been validated. |
| Wrong answer | `wrong-answer-declared-dependency` | Replace A0007's literal declared member URL, retain its valid source locator, and preserve original/replacement evidence. Correctness and grounding incorrect. This tests a dependency declaration literal; computation, runtime dependencies and typedef-impact challenges are explicit gaps requiring controlled native evidence. |
| Wrong citation | `wrong-citation-existing`, `wrong-citation-unresolvable` | Correct A0005 uses real A0008 location (different member name), or syntactically valid `/Library/Item[999999]/@Name`. A0005 grounding incorrect independently of matching answer content. |
| Selective omission | `selective-omission-answer`, `selective-omission-reader`, `true-extra-with-omission-answer`, `true-extra-with-omission-reader` | A0008/R0008 stays missing among 12 required slots; extra true content cannot replace it. Overall assessments remain unverified because native references are unavailable. The protocol's fully checked partial-case demonstration is an explicit gap; a conditional XML-only answer tally would be 9 correct/1 missing, with 2 native slots separately unverified. |
| Extra false claim | `extra-false-answer`, `extra-false-reader`, `extra-true-answer`, `extra-true-reader`, `extra-unverified-answer`, `extra-unverified-reader` | Concrete extra UTF-8 literal-length assertions are falsified/supported by A0005 and a recorded byte-length derivation. False answer uses existing non-supporting A0001 citation. Native member-count assertion is explicitly unverified. False extras make the affected authored dimension incorrect; true reader extras remain unverified without native alignment. |
| Duplicate and contradiction | `duplicate-answer`, `duplicate-reader`, `contradiction-answer`, `contradiction-reader` | Preserve two equivalent assertions or assertion plus explicit negation, with both raw pointers and evidence. Duplicate counted once; contradiction makes A0005/R0005 and its dimension incorrect. |
| Constant export | Both libraries: `constant-export` | Identical fixed bytes assert R0001=20008000 and R0005=Actor.lvclass. R0005 contradicts Test Caller.vi and Batch Msg.lvclass respectively; R0001 also contradicts icon-tests 21008000. Remaining ten observations stay missing; fidelity authored expectation incorrect in both. Native comparisons are an explicit gap. |
| Empty, truncated or failed probe | `empty-probe`, `wrapper-only-probe`, `truncated-probe`, `unsupported-probe`, `failed-probe` | Preserve empty bytes, valid wrapper without observations, exact incomplete JSON prefix, explicit missing-runtime response, and concrete error JSON/exit 1 respectively. All required fidelity slots missing, unsupported or error as appropriate. Calls and failures are simulated fixture inputs. |
| Unsupported or inaccessible case | VI: `unsupported-missing-runtime`, `unsupported-missing-dependency`, `unsupported-missing-license`, `unsupported-inaccessible-diagram` | Concrete abstentions and exact injected conditions retain all three IDs, unsupported outcomes, and planned=1/attempted=executed=scored=0 per control. These are controlled declarations, not observed environment failures or demonstrated behavior. |
| Missing evidence or execution | `missing-independent-key`, `missing-native-run`, `zero-executed-tests` | Materialized null-key/native-run and zero-test report records. All remain unverified/unexecuted; no key is inferred from synthetic responses. |

Every control carries full submitted records, exact raw text, fixed per-ID ledgers, outcome counts, separate extras/duplicate/contradiction ledgers and evidence pointers. Null native slots are not factual assertions. Structural XML inspection makes no hardware, execution, resolved-membership, effective-scope or compatibility claim. Native locators cannot be supplied from these inventories, and remain explicit gaps.

Next: independently check all provisional XML expectations and original locators, review the accounting and synthetic raw alignments, then request a Policymaker-ordered scorer with separate evaluator verification. Native references, a concrete adapter and actual substantive comparisons remain required. Public inputs are unsuitable as withheld evaluation evidence; no readiness, threshold, scope or LabVIEW 2024 claim is made.
"""


def rendered():
    files = {"README.md": README}
    for name in CASES:
        case = load_case(name)
        fixture = {"schema_version": 2, "fixture_id": name,
                   "source": {"case_id": name, "case_revision": case["case_revision"],
                              "inventory_revision": case["inventory_revision"], "artifact": case["artifact"],
                              "inventory_path": "benchmark/cases/dev/" + name + ".json",
                              "inventory_sha256": hashlib.sha256((CASE_DIR / (name + ".json")).read_bytes()).hexdigest()},
                   "public_development_only": True,
                   "execution": {"planned_cases": 1, "attempted_cases": 0, "executed_cases": 0, "scored_cases": 0},
                   "denominators": deepcopy(case["denominators"]),
                   "controls": native_controls(case) if name.startswith("vi-") else library_controls(case, name == "library-icon-tests")}
        files[name + ".json"] = json.dumps(fixture, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = {name: value.encode("utf-8") for name, value in rendered().items()}
    if args.check:
        entries = list(OUT_DIR.rglob("*")) if OUT_DIR.exists() else []
        actual = {p.relative_to(OUT_DIR).as_posix(): p.read_bytes()
                  for p in entries if p.is_file() and not p.is_symlink()}
        unexpected_entries = [p.relative_to(OUT_DIR).as_posix() for p in entries if p.is_symlink() or not p.is_file()]
        missing = sorted(set(files) - set(actual))
        extra = sorted((set(actual) - set(files)) | set(unexpected_entries))
        different = sorted(n for n in set(files) & set(actual) if files[n] != actual[n])
        if missing or extra or different:
            raise SystemExit("challenge bytes differ: " + json.dumps({"missing": missing, "extra": extra, "different": different}))
        print("challenge fixtures and README match (4 files; no reader executed)")
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (OUT_DIR / name).write_bytes(content)
    print("wrote %d challenge evidence files; remove obsolete files explicitly before --check" % len(files))


if __name__ == "__main__":
    main()
