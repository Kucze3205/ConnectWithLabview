#!/usr/bin/env python3
"""Fixed WP1 proposal consistency and in-memory preparation controls, not a benchmark.

Only stdlib/local committed inputs. No environment, session files, Git, native
LabVIEW, product imports, subprocesses or writes. Prose truth needs separate review.
"""
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = "benchmark/project-text-writing-0109.json"
DOC = "benchmark/project-text-writing-0109.md"
REVIEW = "benchmark/real-project-0107/review-0108.json"
REVIEW_SHA = "6ad9596c1c5e05f08ee3647ae3af1596f1882944e2397ac9efcd79383aa78894"
ORIGINAL = "benchmark/real-project-0107/original.lvproj"
LICENSE = "benchmark/real-project-0107/LICENSE.txt"
ORIGINAL_SHA = "1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf"
METHOD = "benchmark/writing/method.json"
OUTPUT = "Core/AF PPL Build.lvproj"
LOCATOR = ("./Item[@Name='My Computer']/Item[@Name='Build Specifications']/"
           "Item[@Name='AF PPL']/Property[@Name='Bld_version.build']")
TOKEN = b'<Property Name="Bld_version.build" Type="Int">2</Property>'
OFFSET = 3347
PRECONDITION = {
    "original_sha256": ORIGINAL_SHA, "root_tag": "Project",
    "root_attributes": {"Type": "Project", "LVVersion": "20008000"},
    "match_count": 1, "property_attributes": {"Name": "Bld_version.build", "Type": "Int"},
    "text": "2", "property_children": 0,
}
DELTA = {"before": "2", "after": "3", "offset_zero_based": OFFSET,
         "line_one_based": 42, "removed_hex": "32", "inserted_hex": "33",
         "output_size": 5806, "allowed_changed_bytes": 1}
PLANNED = {"text_correctness": "unexecuted", "root_version_declaration": "unexecuted",
           "native_validity": "unexecuted", "dependency_resolution": "unexecuted",
           "build": "unexecuted", "behavior": "unexecuted",
           "save_version": "unverified", "overall_writing": "unverified"}
CLAIMS = {"project_artifact_edits": 0, "native_executions": 0, "benchmark_runs": 0,
          "writing_trial_executed": False, "native_oracle_established": False,
          "native_property_semantics_established": False,
          "save_version_preservation_established": False, "method_frozen": False,
          "method_accepted": False, "benchmark_ready": False,
          "product_quality_measured": False, "independent_proposal_review": "pending"}
SUPPLEMENTARY = {
    "benchmark/baseline/runner-contract.md": {
        "sha256": "b9e47205b0ef3f479a77bd3b4dd06e89c3521923e6b316bef14f624cbbcaa5c0", "size": 2834},
    "benchmark/precision/README.md": {
        "sha256": "f94ba74b1c22e551b3cf8eabafdb5868705baa889e17ad5f301fb08cbe18824b", "size": 5854},
}
TASKS = ["WC1-create-vi", "WM1-diagram-not", "WM2-typedef-cluster", "WB1-source-rebuild"]
UNCOVERED = ".lvlib and .lvproj direct creation/modification"
PRESERVATION_IDS = ["WP1-other-project-bytes", "WP1-file-set-and-unrelated-files",
                    "WP1-root-version-declaration", "WP1-original-and-license"]
ANSWER_IDS = ["WP1-describe-text-delta", "WP1-original-output-grounding", "WP1-honest-limits"]
INTEGRATION = ["benchmark/writing/method.json", "benchmark/writing/README.md",
               "benchmark/writing/verify_method.py", "benchmark/writing/controls.json",
               "benchmark/writing/verification.json"]
NEW_FILES = [DOC, PROPOSAL, REVIEW, "benchmark/scripts/check_project_text_writing_0109.py",
             "benchmark/project-text-writing-0109/verification.json"]
TRIAL_FIELDS = ["complete-original-bytes", "complete-edited-bytes", "license-notice",
                "workspace-dependency-manifest", "output-path-size-sha256-manifest",
                "original-output-source-map", "missing-unexpected-paths",
                "failed-invalid-empty-raw-outputs", "errors-truncation-retries",
                "request-response-tool-records", "time-cost-budget-records",
                "per-file-save-version-evidence", "native-logs-or-explicit-missing-status"]
REQUEST = ("In the isolated writable Core/AF PPL Build.lvproj copy, require the pinned original "
           "hash and unique WP1 locator/precondition. Change only its exact property text from 2 "
           "to 3. Return the complete edited project, artifact manifest, original/output source "
           "map and honest validation-limits answer. Preserve every other byte and file, "
           "including root LVVersion 20008000. Stop and report any failed precondition; "
           "do not build or resolve dependencies.")


class Invalid(ValueError):
    pass


def need(ok, reason):
    if not ok:
        raise Invalid(reason)


def same(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_local(path):
    p = PurePosixPath(path)
    need(not p.is_absolute() and p.parts and all(x not in (".", "..") for x in p.parts), "unsafe-path")
    current = ROOT
    for part in p.parts:
        current = current / part
        need(not current.is_symlink(), "symlink:" + path)
    need(current.is_file(), "missing-evidence:" + path)
    need(current.stat().st_size <= 2_000_000, "oversize:" + path)
    return current.read_bytes()


def xml(data):
    try:
        return ET.fromstring(data)
    except ET.ParseError as exc:
        raise Invalid("malformed-xml") from exc


def validate(p, read=read_local):
    review_bytes = read(REVIEW)
    need(digest(review_bytes) == REVIEW_SHA, "review-hash")
    r = json.loads(review_bytes)
    need(p["schema_version"] == 1 and p["issue"] == 544 and p["case_id"] == "WP1-project-build-text"
         and p["revision"] == "proposal-1" and p["status"] == "proposal-awaiting-independent-review"
         and p["scope"] == "public-development-preparation", "proposal-status")
    need(same(p["baseline"], {"commit": "8b93818c2779be00a2e267a3588eadcdaf665911",
                             "tree": "e5cdbf5a3bf02dce5de55e0b0cd3fc27bb744c31"}), "baseline")
    v = p["review"]
    need(v["issue"] == r["issue"] == 541 and v["preserved_path"] == REVIEW
         and v["sha256"] == REVIEW_SHA and v["recommendation"] == r["overall_recommendation"] == "CLEAR"
         and v["report_sha256"] == r["supporting_artifacts"][".session/report.md"]
         and same(v["reviewed_identities"], r["identities"]), "review-provenance")
    pins = {k: {"sha256": row["sha256"], "size": row["size"]}
            for k, row in r["files"].items() if not k.startswith(".session/")}
    need(len(pins) == 22 and same(p["input_pins"], pins), "reviewed-input-pins")
    need(same(p["supplementary_pins"], SUPPLEMENTARY), "supplementary-pins")
    for path, pin in {**pins, **SUPPLEMENTARY}.items():
        data = read(path)
        need(len(data) == pin["size"] and digest(data) == pin["sha256"], "input-hash:" + path)
    need(p["documentation"]["path"] == DOC
         and digest(read(DOC)) == p["documentation"]["sha256"], "documentation-integrity")
    s, upstream = p["source"], r["prepared_upstream"]
    need(s["commit"] == upstream["identity"]["commit"] and s["tree"] == upstream["identity"]["tree"]
         and s["path"] == OUTPUT and s["snapshot"] == ORIGINAL and s["sha256"] == ORIGINAL_SHA
         and s["size"] == 5806 and s["git_blob"] == upstream["files"][OUTPUT]["git_blob"]
         and s["license"] == "MIT" and s["license_path"] == LICENSE
         and s["license_sha256"] == pins[LICENSE]["sha256"], "source-provenance")
    b = read(ORIGINAL)
    need(digest(b) == ORIGINAL_SHA and len(b) == 5806, "original-identity")
    root = xml(b)
    t = p["task"]
    need(t["operation"] == "proposed-text-modification" and t["family"] == ".lvproj"
         and t["output_path"] == OUTPUT and t["request"] == REQUEST, "task-instruction")
    need(t["locator"] == LOCATOR, "wrong-locator")
    need(same(t["precondition"], PRECONDITION), "wrong-precondition")
    matches = root.findall(LOCATOR)
    need(root.tag == "Project" and root.attrib == PRECONDITION["root_attributes"]
         and len(matches) == 1 and matches[0].attrib == PRECONDITION["property_attributes"]
         and matches[0].text == "2" and len(matches[0]) == 0, "source-precondition")
    d4 = r["claims"][3]
    need(d4["id"] == "D4" and d4["agreement"] is True and d4["locator"] == LOCATOR
         and d4["parsed_value"] == "2" and d4["property_type"] == "Int", "review-D4")
    need(b.count(TOKEN) == 1 and b.index(TOKEN) + TOKEN.index(b">2<") + 1 == OFFSET
         and b[OFFSET:OFFSET+1] == b"2" and b[:OFFSET].count(b"\n") + 1 == 42,
         "source-byte-locator")
    need(same(t["delta"], DELTA), "wrong-delta")
    need(t["text_ids"] == ["WP1-property-text"] and t["preservation_ids"] == PRESERVATION_IDS
         and t["answer_ids"] == ANSWER_IDS, "fixed-IDs")
    invariants = {"project_rule": "exact-one-byte-substitution", "unrelated_files": "byte-identical",
                  "file_set": "unchanged", "allowed_metadata_deltas": [], "root_version": "20008000",
                  "root_version_authority": "declaration-only", "native_save_version": "unverified",
                  "originals_outside_writable_workspace": True,
                  "complete_original_and_edited_bytes_required": True, "license_notice_required": True}
    need(same({k: p["preservation"].get(k) for k in invariants}, invariants), "preservation-contract")
    o = p["oracle"]
    need(o["text_key_status"] == "proposed-awaiting-separate-check"
         and o["native_key_status"] == "unavailable"
         and o["separate_checker_required_before_candidate"] is True
         and o["candidate_derived_key_allowed"] is False, "independent-key-boundary")
    need(same(p["planned_results"], PLANNED) and same(p["claims"], CLAIMS), "missing-evidence-boundary")
    need(p["trial_artifacts"]["required"] == TRIAL_FIELDS, "complete-artifacts")
    method = json.loads(read(METHOD))
    need(set(p["requirements"]) == {"W" + str(i) for i in range(1, 9)}
         and all(row.get("contract") and row.get("review") for row in p["requirements"].values()),
         "W1-W8-mapping")  # Presence only; semantic adequacy explicitly needs review.
    c = p["coverage"]
    need(c["method"] == METHOD and c["uncovered_locator"] == "/coverage/uncovered_families"
         and c["uncovered_entry"] == UNCOVERED and UNCOVERED in method["coverage"]["uncovered_families"]
         and c["status"] == "proposed-narrow-instance-still-uncovered"
         and c["existing_task_ids"] == [t["id"] for t in method["tasks"]] == TASKS, "coverage-boundary")
    compare = p["comparison"]
    need(compare["arms"] == ["no-tool", "tool"] and compare["paired_runs_executed"] == 0
         and compare["matched_fields"] == method["comparison"]["matched_fields"]
         and compare["runner"] in SUPPLEMENTARY and compare["precision"] in SUPPLEMENTARY
         and compare["native_access"] == "neither-arm; post-output-freeze identical separate trusted validation only",
         "comparison-contract")
    isolation = p["isolation"]
    need(isolation["visibility"] == "public-development-only" and isolation["withheld"] is False
         and isolation["model_unseen"] is False and isolation["restricted_evaluation_ready"] is False,
         "isolation-boundary")
    need(p["integration_after_review"]["existing_files_to_change"] == INTEGRATION
         and p["integration_after_review"]["preserve_historical_files"] == [
             "benchmark/writing/input-pins.json", "benchmark/writing/review-corrections.json"]
         and p["handoff"]["new_candidate_files"] == NEW_FILES, "integration-scope")
    need(p["checker"]["path"] == NEW_FILES[3]
         and p["checker"]["kind"] == "offline-preparation-consistency-only"
         and p["checker"]["emits_edited_project"] is False
         and p["checker"]["narrative_truth_validated"] is False
         and "all-prose-assertions" in p["checker"]["review_required"], "checker-boundary")
    return b


def structural_signature(node, selected):
    # Compare entire XML tree, masking only the chosen property's text value.
    return (node.tag, sorted(node.attrib.items()), None if node is selected else node.text,
            node.tail, tuple(structural_signature(child, selected) for child in node))


def check_example(originals, files, original_after, statuses, support="text-only"):
    """In-memory bytes only. Not an executable artifact scorer or candidate API."""
    need(support == "text-only", "unsupported-artifact")
    need(original_after == originals, "original-overwritten")
    need(set(files) == set(originals), "output-file-set")
    b, changed = originals[OUTPUT], files[OUTPUT]
    need(digest(b) == ORIGINAL_SHA, "example-original")
    out = xml(changed)
    need(out.attrib.get("LVVersion") == "20008000", "version-drift")
    need(changed != b, "no-op")
    matches = out.findall(LOCATOR)
    need(len(matches) == 1 and matches[0].text == "3"
         and matches[0].attrib == PRECONDITION["property_attributes"], "wrong-output-property")
    before = xml(b)
    need(structural_signature(before, before.findall(LOCATOR)[0]) ==
         structural_signature(out, matches[0]), "unrelated-XML-change")
    expected = b[:OFFSET] + b"3" + b[OFFSET+1:]
    need(changed == expected, "unrelated-byte-change")
    need(all(files[k] == v for k, v in originals.items() if k != OUTPUT), "unrelated-file-change")
    expected_status = dict(PLANNED, text_correctness="correct", root_version_declaration="correct")
    need(same(statuses, expected_status), "false-native-or-overall-pass")
    return "text-only-correct;overall-unverified"


def set_field(p, path, value):
    for key in path[:-1]:
        p = p[key]
    p[path[-1]] = value


def controls(p, b, read=read_local):
    results = []

    def reject(label, action, reason):
        try:
            action()
        except Invalid as exc:
            need(str(exc) == reason, "wrong-rejection:" + label + ":" + str(exc))
            results.append({"control": label, "rejected": reason})
        else:
            raise Invalid("accepted-malformed:" + label)

    def mutate(label, path, value, reason):
        q = copy.deepcopy(p)
        set_field(q, path, value)
        reject(label, lambda: validate(q, read), reason)

    mutate("wrong-locator", ["task", "locator"], LOCATOR.replace("Bld_version.build", "Bld_version.major"), "wrong-locator")
    for field, value in [("text", "1"), ("match_count", 2), ("property_attributes", {"Name": "Bld_version.build", "Type": "Str"})]:
        mutate("precondition-" + field, ["task", "precondition", field], value, "wrong-precondition")
    for field, value in [("after", "4"), ("before", "1"), ("offset_zero_based", OFFSET+1), ("allowed_changed_bytes", 2)]:
        mutate("delta-" + field, ["task", "delta", field], value, "wrong-delta")
    mutate("metadata-exception", ["preservation", "allowed_metadata_deltas"], ["resave"], "preservation-contract")
    mutate("version-authority", ["preservation", "root_version_authority"], "native-certified", "preservation-contract")
    for field in PLANNED:
        mutate("false-status-" + field, ["planned_results", field], "passed", "missing-evidence-boundary")
    for field, value in CLAIMS.items():
        wrong = 1 if type(value) is int else (True if type(value) is bool else "approved")
        mutate("false-claim-" + field, ["claims", field], wrong, "missing-evidence-boundary")
    mutate("candidate-derived-key", ["oracle", "candidate_derived_key_allowed"], True, "independent-key-boundary")
    mutate("key-self-approval", ["oracle", "text_key_status"], "established", "independent-key-boundary")
    mutate("withheld-case", ["isolation", "withheld"], True, "isolation-boundary")
    mutate("incomplete-artifacts", ["trial_artifacts", "required"], TRIAL_FIELDS[1:], "complete-artifacts")
    mutate("unmatched-budget", ["comparison", "matched_fields"], [], "comparison-contract")
    q = copy.deepcopy(p)
    del q["input_pins"][METHOD]
    reject("missing-pin", lambda: validate(q, read), "reviewed-input-pins")
    q = copy.deepcopy(p)
    del q["requirements"]["W8"]
    reject("missing-W8", lambda: validate(q, read), "W1-W8-mapping")
    # Tampering is rejected against historical pins; expected hashes are not refreshed.
    for path in [REVIEW] + list(p["input_pins"]) + list(SUPPLEMENTARY):
        def override(name, changed_path=path):
            data = read(name)
            return data + b"\n" if name == changed_path else data
        reason = "review-hash" if path == REVIEW else "input-hash:" + path
        reject("tampered-" + path, lambda: validate(p, override), reason)
    def absent(name):
        need(name != ORIGINAL, "missing-evidence:" + ORIGINAL)
        return read(name)
    reject("missing-original", lambda: validate(p, absent), "missing-evidence:" + ORIGINAL)

    originals = {OUTPUT: b, "LICENSE.txt": read(LICENSE)}
    good = {**originals, OUTPUT: b[:OFFSET] + b"3" + b[OFFSET+1:]}
    status = dict(PLANNED, text_correctness="correct", root_version_declaration="correct")
    positive = check_example(originals, good, originals, status)
    reject("no-op", lambda: check_example(originals, originals, originals, status), "no-op")
    wrong = {**good, OUTPUT: b[:OFFSET] + b"4" + b[OFFSET+1:]}
    reject("wrong-output-value", lambda: check_example(originals, wrong, originals, status), "wrong-output-property")
    wrong = {**good, OUTPUT: b.replace(b'Name="Bld_version.major" Type="Int">1', b'Name="Bld_version.major" Type="Int">3')}
    reject("wrong-output-locator", lambda: check_example(originals, wrong, originals, status), "wrong-output-property")
    wrong = {**good, OUTPUT: good[OUTPUT].replace(b'LVVersion="20008000"', b'LVVersion="24008000"')}
    reject("output-version-drift", lambda: check_example(originals, wrong, originals, status), "version-drift")
    wrong = {**good, OUTPUT: good[OUTPUT].replace(b'Name="Bld_autoIncrement" Type="Bool">true', b'Name="Bld_autoIncrement" Type="Bool">false')}
    reject("unrelated-output-property", lambda: check_example(originals, wrong, originals, status), "unrelated-XML-change")
    wrong = {**good, OUTPUT: good[OUTPUT][3:]}  # Remove original UTF-8 BOM.
    reject("BOM-lost", lambda: check_example(originals, wrong, originals, status), "unrelated-byte-change")
    wrong = {**good, "LICENSE.txt": b"MIT"}
    reject("unrelated-file", lambda: check_example(originals, wrong, originals, status), "unrelated-file-change")
    wrong = {**good, "extra.lvproj": b"unexpected"}
    reject("extra-output", lambda: check_example(originals, wrong, originals, status), "output-file-set")
    wrong = {k: v for k, v in good.items() if k != OUTPUT}
    reject("missing-output", lambda: check_example(originals, wrong, originals, status), "output-file-set")
    reject("overwritten-original", lambda: check_example(originals, good, good, status), "original-overwritten")
    reject("unsupported-output", lambda: check_example(originals, good, originals, status, "unsupported"), "unsupported-artifact")
    for field in ["native_validity", "dependency_resolution", "build", "behavior", "save_version", "overall_writing"]:
        false_status = dict(status, **{field: "passed"})
        reject("output-false-" + field, lambda: check_example(originals, good, originals, false_status), "false-native-or-overall-pass")
    # Intentional counterexample: no claim of complete narrative validation.
    q = copy.deepcopy(p)
    q["requirements"]["W5"]["review"] = "Native loading, builds and save-version preservation were verified."
    validate(q, read)
    return positive, results, {"control": "W5-prose-overclaim", "accepted_by_structured_checker": True,
                                "meaning": "Requires independent semantic/prose review; no narrative pass."}


def main():
    try:
        p = json.loads(read_local(PROPOSAL))
        b = validate(p)
        positive, rejected, narrative = controls(p, b)
        print(json.dumps({"status": "proposal-consistent", "scope": "preparation-only",
                          "input_hashes_checked": 24, "preserved_review_sha256": REVIEW_SHA,
                          "positive_control": positive, "rejection_count": len(rejected),
                          "rejecting_controls": rejected, "narrative_boundary": narrative,
                          "project_artifact_edits": 0, "native_executions": 0, "benchmark_runs": 0,
                          "overall_writing": "unverified", "independent_review": "pending"}, sort_keys=True))
        return 0
    except (Invalid, KeyError, TypeError, ValueError, OSError) as exc:
        print(json.dumps({"status": "invalid", "reason": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
