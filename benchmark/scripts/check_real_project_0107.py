#!/usr/bin/env python3
"""Validate the fixed 0107 public declaration evidence, never LabVIEW results.

Standard library only. No source cache, session files, Git, network, subprocesses,
product reader, source imports or writes. Fixed claims prevent a supporting XML
locator from being used to smuggle in an unsupported semantic assertion.
"""
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
RECORD = "benchmark/real-project-0107.json"
SNAPSHOT = "benchmark/real-project-0107/original.lvproj"
LICENSE = "benchmark/real-project-0107/LICENSE.txt"
METHOD = "benchmark/writing/method.json"
CHECKER = "benchmark/writing/verify_method.py"
COMMIT = "371c631c16155d88f02be11a953e4964d7452fd8"
ORIGINAL = "Core/AF PPL Build.lvproj"
SHA256 = "1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf"
INPUT_PINS = {
    "goal/goal.md": "5ee530059fd3efd34280ba632f160bbf37cb4f13c5d3e09cd841966ede5929cb",
    "docs/perpetua/evaluation.md": "d9eb079a6be4a99aa4697433ce56ac2ef0d05dff15074b24215c8947b6e6e8d8",
    "docs/perpetua/roles.md": "d55ebb50e4ca83b74c2261549856493233b3c072294066281259fce33cbdb40a",
    "benchmark/protocol.md": "1aeb83227dc11761160ff80d24eb03a216a2531d90c1a6d10ccb25bb85c7eb2f",
    "benchmark/sources.md": "43eafe9c348eba4516871f508121b29147e7c07677e6a6ca9b0d63bfc23babb2",
    "benchmark/sources.json": "e3c53d98c2affe60b399ba7c7c444c91a4607c6fd9120b77a6e7291ac93da92a",
    "benchmark/writing/README.md": "b842f83b5521dece0970cb0876a372830806fc03cdef87eeca009721f9f2a5e8",
    METHOD: "8c3b165c33c8fb4944f10a0eaa3c384fcc90d62c3278c0c910a5f2ae8b9d4da1",
    CHECKER: "b24ca4515ab8f7bd3980cd273647114c4f01abffc942a2464390a4d206e40a5f",
    "benchmark/writing/controls.json": "96d48292fcf2b461b7c8f4af98dc0e894cef8e10eeb6c45edd04bdacad896824",
    "benchmark/writing/input-pins.json": "d6a9914bb86fa593654da3468396b171ec7769a7bec607157b71cb9442b9af44",
    "benchmark/writing/verification.json": "01e4ad1d72cb8f782e0dcfe3ce5e9b27756520da8a403df41707a1d37f1e1022",
    "benchmark/writing/review-corrections.json": "3c92d3e102bb3976ee267ea74393855e520461e2e5f4869fa9d5a864ff17430e",
    ".github/loop/data/session-reports/485/fc8f1c7702fb7c2057e92b968fae62524d85d654060da71d2d3069e9a4bfb25d.json": "fc8f1c7702fb7c2057e92b968fae62524d85d654060da71d2d3069e9a4bfb25d",
    ".github/loop/data/session-reports/493/4ff9c7cc83b7533020b632b0d20b3e8ad99b230e99a756d876c5aab979b6e17e.json": "4ff9c7cc83b7533020b632b0d20b3e8ad99b230e99a756d876c5aab979b6e17e",
}
BUILD = "./Item[@Name='My Computer']/Item[@Name='Build Specifications']/Item[@Name='AF PPL']"
# id, statement, unique ElementTree path, attribute (None means exact text),
# parsed raw value, lexical value, forbidden inferences. No type coercion/trim.
CLAIMS = [
    ("D1", "The original Project declares LVVersion 20008000.", ".", "LVVersion",
     "20008000", "20008000", ["native-save-version-preserved", "runtime-compatibility"]),
    ("D2", "The named Dependencies VI item declares the quoted URL.",
     "./Item[@Name='My Computer']/Item[@Name='Dependencies']/Item[@Name='vi.lib']/Item[@Name='Error Cluster From Error Code.vi']",
     "URL", "/<vilib>/Utility/error.llb/Error Cluster From Error Code.vi",
     "/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi",
     ["dependency-resolved", "dependency-version-known", "vi-diagram-semantics"]),
    ("D3", "The AF PPL build item declares Type Packed Library.", BUILD, "Type",
     "Packed Library", "Packed Library", ["build-succeeded", "matching-source-build-chain-established"]),
    ("D4", "The AF PPL Bld_version.build property has original text 2.",
     BUILD + "/Property[@Name='Bld_version.build']", None, "2", "2",
     ["built-output-version", "native-property-effect"]),
]
TASKS = ["WC1-create-vi", "WM1-diagram-not", "WM2-typedef-cluster", "WB1-source-rebuild"]
UNCOVERED = ".lvlib and .lvproj direct creation/modification"
NATIVE = ["project-load", "dependency-resolution", "build", "controlled-behavior", "save-version-preservation"]
RAW_CONVENTION = ("Exact parsed XML attribute/text value without trimming or type conversion; "
                  "lexical_value retains original entity spelling. Element paths are ElementTree "
                  "paths relative to Project and must resolve uniquely.")
LIMITATIONS = {k: False for k in [
    "native_checks_available", "dependency_resolution_established", "native_load_established",
    "build_success_established", "native_behavior_established", "save_version_preservation_established",
    "vi_diagram_semantics_inferred", "withheld_case", "model_unseen", "native_oracle",
    "completed_write_trial", "product_quality_result", "method_accepted",
]}
LIMITATIONS.update(declaration_evidence_only=True, independent_review_pending=True,
                   artifact_edits=0, native_executions=0, benchmark_runs=0,
                   raw_value_convention=RAW_CONVENTION)


class Invalid(ValueError):
    pass


def need(condition, reason):
    if not condition:
        raise Invalid(reason)


def same(a, b):
    # Preserve bool/int distinction and reject additions as well as omissions.
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_local(path):
    p = PurePosixPath(path)
    need(not p.is_absolute() and all(x not in (".", "..") for x in p.parts), "unsafe-path")
    current = ROOT
    for part in p.parts:
        current = current / part
        need(not current.is_symlink(), "symlink:" + path)
    need(current.is_file(), "missing-evidence:" + path)
    need(0 < current.stat().st_size < 2_000_000, "evidence-size:" + path)
    return current.read_bytes()


def load_json(data):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            need(k not in result, "duplicate-json-key:" + k)
            result[k] = v
        return result
    return json.loads(data, object_pairs_hook=unique)


def validate(record, read=read_local):
    need(type(record) is dict and set(record) == {
        "schema_version", "verdict", "scope", "review_status", "input_hashes",
        "source_provenance", "selection", "claims", "writing_case_mapping",
        "inherited_review", "unresolved", "limitations",
    }, "record-schema")
    need(type(record["schema_version"]) is int and record["schema_version"] == 1, "schema-version")
    need(record["verdict"] in ("candidate-supported", "blocked"), "verdict")
    need(record["scope"] == "public-development-preparation" and
         record["review_status"] == "independent-review-pending", "scope-review")
    need(same(record["input_hashes"], INPUT_PINS), "input-pin-inventory")
    for path, expected in INPUT_PINS.items():
        need(digest(read(path)) == expected, "input-hash:" + path)
    inventory = load_json(read("benchmark/sources.json"))
    repo = next(r for r in inventory["repositories"] if r["name"] == "actor-framework")
    projects = [a for a in repo["artifacts"] if a["path"].lower().endswith(".lvproj")]
    chosen = min(projects, key=lambda a: (a["size"], a["path"]))
    need(repo["commit"] == COMMIT and chosen["path"] == ORIGINAL and
         chosen["sha256"] == SHA256 and chosen["size"] == 5806, "inventory-source")
    provenance = record["source_provenance"]
    expected_provenance = dict(
        repository="actor-framework", upstream_url=repo["upstream_url"], commit=COMMIT,
        original_path=ORIGINAL, original_sha256=SHA256, original_size=5806,
        snapshot_path=SNAPSHOT, snapshot_kind="complete-byte-identical-original",
        license="MIT", license_original_path=repo["license_file"]["path"],
        license_snapshot_path=LICENSE, license_sha256=repo["license_file"]["sha256"],
        readiness_sha256=inventory["preparation_readiness_sha256"],
    )
    need(type(provenance) is dict and set(provenance) == set(expected_provenance) | {"checks_performed_now"}, "provenance-schema")
    need(same({k: provenance[k] for k in expected_provenance}, expected_provenance), "provenance")
    need(type(provenance["checks_performed_now"]) is list and len(provenance["checks_performed_now"]) == 5
         and all(type(s) is str and s for s in provenance["checks_performed_now"]), "observations")
    data = read(SNAPSHOT)
    need(digest(data) == chosen["sha256"] and len(data) == chosen["size"], "snapshot-identity")
    license_data = read(LICENSE)
    need(digest(license_data) == repo["license_file"]["sha256"] and
         len(license_data) == repo["license_file"]["size"], "license-identity")
    selection = record["selection"]
    need(type(selection) is dict and set(selection) == {
        "rule", "candidate_count", "selected_path", "declaration_relevance", "alternatives_inspected"
    }, "selection-schema")
    need(selection["rule"] == "Among actor-framework inventory artifacts ending in .lvproj, choose minimum (size, path), then verify pins before inspection; stop at this one project."
         and type(selection["candidate_count"]) is int and selection["candidate_count"] == len(projects)
         and selection["selected_path"] == chosen["path"] and type(selection["alternatives_inspected"]) is int
         and selection["alternatives_inspected"] == 0 and bool(selection["declaration_relevance"]), "selection")
    # No DTD/entities or other source processing: parse original XML directly.
    need(b"<!DOCTYPE" not in data and b"<!ENTITY" not in data, "unsupported-xml")
    xml = ET.fromstring(data)
    need(xml.tag == "Project" and xml.get("Type") == "Project", "xml-root")
    need(type(record["claims"]) is list and len(record["claims"]) == len(CLAIMS), "claim-inventory")
    for actual, frozen in zip(record["claims"], CLAIMS):
        ident, statement, element, attribute, raw, lexical, prohibited = frozen
        expected = dict(id=ident, statement=statement, element=element, attribute=attribute,
                        raw_value=raw, lexical_value=lexical, prohibited_inferences=prohibited,
                        level="original-text-declaration-only", review_status="independent-review-pending")
        need(same(actual, expected), "unsupported-claim:" + ident)
        nodes = [xml] if element == "." else xml.findall(element)
        need(len(nodes) == 1, "claim-locator:" + ident)
        value = nodes[0].text if attribute is None else nodes[0].get(attribute)
        need(value == raw, "claim-value:" + ident)
        # The unique parsed locator establishes the value; separately confirm its
        # lexical spelling in the hash-pinned original bytes.
        if attribute:
            need((attribute + '=\"' + lexical + '\"').encode() in data, "claim-lexical:" + ident)
        else:
            need(('Name=\"Bld_version.build\" Type=\"Int\">' + lexical + '</Property>').encode() in data,
                 "claim-lexical:" + ident)
    need(xml.get("LVVersion") == chosen["save_version"]["raw_hex"], "original-version")
    method = load_json(read(METHOD))
    need([t["id"] for t in method["tasks"]] == TASKS and
         UNCOVERED in method["coverage"]["uncovered_families"], "writing-case-absence")
    mapping = record["writing_case_mapping"]
    need(type(mapping) is dict and set(mapping) == {
        "status", "existing_case_id", "existing_task_ids", "blocker_code", "blocker", "evidence",
        "uncovered_entry", "checker_contract", "permitted_xml_change", "expected_before_after",
        "unchanged_scope", "original_version_check", "requirements", "required_native_checks_unavailable",
    }, "mapping-schema")
    # This pinned measurement found no corresponding case. Do not silently promote it.
    need(record["verdict"] == mapping["status"] == "blocked" and
         mapping["existing_case_id"] is None and mapping["existing_task_ids"] == TASKS and
         mapping["blocker_code"] == "no-existing-project-xml-writing-case" and
         mapping["evidence"] == METHOD + "#/coverage/uncovered_families" and
         mapping["uncovered_entry"] == UNCOVERED and
         mapping["permitted_xml_change"] is None and mapping["expected_before_after"] is None,
         "mapping-blocker")
    need(type(mapping["blocker"]) is str and "WB1" in mapping["blocker"] and
         "does not specify a project XML edit" in mapping["blocker"] and
         type(mapping["unchanged_scope"]) is str and mapping["unchanged_scope"], "precise-blocker")
    contract = mapping["checker_contract"]
    need(type(contract) is dict and set(contract) == {"path", "locator", "applicability"} and
         contract["path"] == CHECKER and "task-inventory" in contract["locator"] and
         "no project XML writing checker" in contract["applicability"], "checker-applicability")
    need(same(mapping["original_version_check"], dict(claim_id="D1", locator="/Project/@LVVersion",
         expected_raw="20008000", native_preservation="unverified")), "mapping-version")
    requirements = mapping["requirements"]
    need(type(requirements) is dict and set(requirements) == {"W" + str(i) for i in range(1, 9)}
         and all(type(s) is str and s for s in requirements.values()), "requirements-mapping")
    need(mapping["required_native_checks_unavailable"] == NATIVE, "native-gaps")
    need(same(record["limitations"], LIMITATIONS), "non-native-limitations")
    review = record["inherited_review"]
    need(type(review) is dict and set(review) == {"481", "485", "489", "493", "current_scope"}
         and all(type(s) is str and s for s in review.values()) and
         "Inherited review" in review["493"] and "not repeated independent review" in review["493"] and
         "has not independently replayed" in review["current_scope"], "inherited-review")
    unresolved = record["unresolved"]
    need(type(unresolved) is list and len(unresolved) == 4 and
         all(type(s) is str and s for s in unresolved), "unresolved")
    report = read("benchmark/real-project-0107.md").decode("utf-8")
    need(len(report.splitlines()) <= 100 and "blocked" in report and "reviewer" in report, "report")
    return {"verdict": "blocked", "declaration_claims_checked": len(CLAIMS),
            "native_executions": 0, "independent_review": "pending"}


def self_test(record):
    tests = []
    def mutation(label, change, reason):
        altered = copy.deepcopy(record)
        change(altered)
        tests.append((label, altered, {}, reason))
    mutation("wrong-raw", lambda d: d["claims"][0].update(raw_value="24008000"), "unsupported-claim:D1")
    mutation("wrong-locator", lambda d: d["claims"][1].update(element="."), "unsupported-claim:D2")
    mutation("native-claim-at-valid-locator", lambda d: d["claims"][2].update(statement="The build succeeded."), "unsupported-claim:D3")
    mutation("missing-claim", lambda d: d["claims"].pop(), "claim-inventory")
    mutation("extra-claim", lambda d: d["claims"].append(copy.deepcopy(d["claims"][0])), "claim-inventory")
    mutation("drop-prohibition", lambda d: d["claims"][0].update(prohibited_inferences=[]), "unsupported-claim:D1")
    mutation("invent-write-case", lambda d: d["writing_case_mapping"].update(existing_case_id="WB1-source-rebuild"), "mapping-blocker")
    mutation("invent-edit", lambda d: d["writing_case_mapping"].update(permitted_xml_change={"after": "3"}), "mapping-blocker")
    mutation("promote-verdict", lambda d: d.update(verdict="candidate-supported"), "mapping-blocker")
    mutation("native-success", lambda d: d["limitations"].update(native_load_established=True), "non-native-limitations")
    mutation("missing-version-gap", lambda d: d["writing_case_mapping"]["required_native_checks_unavailable"].pop(), "native-gaps")
    mutation("missing-input-pin", lambda d: d["input_hashes"].pop(METHOD), "input-pin-inventory")
    tests.extend([
        ("missing-original", record, {SNAPSHOT: None}, "missing-evidence:" + SNAPSHOT),
        ("altered-original", record, {SNAPSHOT: read_local(SNAPSHOT) + b" "}, "snapshot-identity"),
        ("altered-license", record, {LICENSE: b"MIT"}, "license-identity"),
        ("altered-input", record, {METHOD: b"{}"}, "input-hash:" + METHOD),
    ])
    passed = []
    for label, altered, overrides, expected in tests:
        def read(path):
            if path in overrides:
                need(overrides[path] is not None, "missing-evidence:" + path)
                return overrides[path]
            return read_local(path)
        try:
            validate(altered, read)
        except Invalid as exc:
            need(str(exc) == expected, "wrong-rejection:" + label + ":" + str(exc))
            passed.append({"control": label, "rejected": expected})
        else:
            raise Invalid("false-acceptance:" + label)
    return passed


def main():
    need(len(sys.argv) == 1, "no-arguments-supported")
    record = load_json(read_local(RECORD))
    result = validate(record)
    result.update(status="evidence-consistent", rejecting_controls=self_test(record),
                  limitation="No native certification, independent approval or method acceptance.")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Invalid, OSError, ValueError, KeyError, TypeError, StopIteration, ET.ParseError) as exc:
        print("real-project-0107: FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
