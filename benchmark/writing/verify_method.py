#!/usr/bin/env python3
"""Check this public writing DESIGN and its fictional examples; never score LabVIEW.

No CLI input, native APIs, environment, session state, subprocesses or file writes.
Inputs are repository-local method, controls, pinned source and integration evidence only.
Every file read is checked against benchmark/writing/current-pins.json, the one current
pin file; historical records (provenance, proposal, review) are compared only with each other.
These checks deliberately do not implement an artifact reader, writer or evaluator.
"""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import types
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
CONTROL_REASONS = {
    "constant-writer-on-two": "no-op-edit",
    "compiled-without-source": "missing-source",
    "invented-rebuild": "build-unexecuted",
    "wrong-source-build-link": "source-build-link",
    "no-op": "no-op-edit",
    "changed-bytes-only": "no-op-edit",
    "wrong-behavior": "wrong-behavior",
    "wrong-type": "wrong-type",
    "unintended-object-edit": "unintended-edits",
    "unintended-file-edit": "unintended-edits",
    "extra-file": "output-file-set",
    "missing-artifact": "output-file-set",
    "version-drift": "version-drift",
    "unknown-version": "save-version-unverified",
    "unsupported-artifact": "unsupported-artifact",
    "correct-answer-wrong-artifact": "wrong-behavior",
    "correct-artifact-wrong-answer": "answer-incorrect",
    "wrong-original-citation": "source-unsupported",
    "wrong-output-citation": "source-unsupported",
    "extra-false-claim": "extra-answer-claim",
    "invented-native-pass": "native-unexecuted",
    "original-overwritten": "original-not-preserved",
    "creation-overwrite": "creation-destination-exists",
    "missing-arm": "planned-arm-missing",
    "unmatched-request": "pair-request-mismatch",
    "unmatched-originals": "pair-originals-mismatch",
    "unmatched-inputs": "pair-allowed_inputs-mismatch",
    "unmatched-budget": "pair-budgets-mismatch",
    "shared-session": "session-reused",
    "lost-output-accounting": "output-accounting-missing",
    "lost-failure-accounting": "failure-accounting-missing",
    "method-native-claim": "method-overclaim",
    "method-missing-preservation": "task-preservation-ids",
    "method-invented-key": "native-key-unavailable",
    "method-missing-anchor": "task-source-anchor",
    "original-output-version-drift": "version-drift",
    "source-original-output-version-drift": "version-drift",
    "missing-pair-request": "pair-setting-required",
    "missing-pair-originals": "pair-setting-required",
    "missing-pair-allowed_inputs": "pair-setting-required",
    "missing-pair-model": "pair-setting-required",
    "missing-pair-budgets": "pair-setting-required",
    "missing-pair-key_revision": "pair-setting-required",
    "missing-pair-repetitions": "pair-setting-required",
}

# Mandatory names in this bounded synthetic pair representation, independent of
# its frozen dictionary: protocol.md:79-84 and baseline/runner-contract.md
# (Inputs, Audit, Still undecided); writing method.json#/comparison maps the
# request/original/input/model/budget/key/repetition obligations to these names.
REQUIRED_PAIR_SETTINGS = frozenset({
    "request", "originals", "allowed_inputs", "model", "budgets",
    "key_revision", "repetitions",
})


class Inconsistent(ValueError):
    pass


def need(condition, reason):
    if not condition:
        raise Inconsistent(reason)


def canonical(value):
    # Retain types: Python equality alone would allow True to equal integer 1.
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def same(left, right):
    return canonical(left) == canonical(right)


def check_method(method):
    need(method["schema_version"] == 1, "method-schema")
    need(method["status"] == "design-only-unreviewed", "method-status")
    need(same(method["claims"], {
        "native_executions": 0, "artifact_edits": 0, "benchmark_runs": 0,
        "key_established": False, "benchmark_ready": False,
        "method_accepted": False, "model_unseen": False,
    }), "method-overclaim")
    for field, prefix in (("existing_requirements", "E"), ("new_requirements", "W")):
        rows = method[field]
        need([r["id"] for r in rows] == [prefix + str(i) for i in range(1, 9)],
             "requirement-inventory")
    for row in method["new_requirements"]:
        need(row["extends"] and set(row["extends"]) <= {"E" + str(i) for i in range(1, 9)},
             "requirement-extension")
        need(bool(row["requirement"]), "requirement-empty")
    need(method["extends"] == [
        "benchmark/protocol.md", "benchmark/change-cases/typedef-impact.spec.json",
        "benchmark/change-cases/diagram-difference.spec.json",
        "benchmark/baseline/runner-contract.md", "benchmark/precision/README.md",
    ], "extension-links")
    tasks = method["tasks"]
    need([t["id"] for t in tasks] == ["WC1-create-vi", "WM1-diagram-not",
         "WM2-typedef-cluster", "WB1-source-rebuild", "WP1-project-build-text"], "task-inventory")
    all_ids = []
    for task in tasks:
        need(task["preconditions"] and task["request"] and task["expected_semantics"],
             "task-contract")
        need(task["source_anchors"] and all(a["path"] and a["locator"] for a in task["source_anchors"]),
             "task-source-anchor")
        need(task["semantic_ids"], "task-semantic-ids")
        need(task["output_paths"] and task["output_manifest_rule"], "task-output-paths")
        need(task["preservation_ids"] and task["preservation"], "task-preservation-ids")
        need(task["answer_ids"], "task-answer-ids")
        all_ids += task["semantic_ids"] + task["preservation_ids"] + task["answer_ids"]
        need(task["oracle"]["native_key"] == "unavailable", "native-key-unavailable")
        need(task["oracle"]["method"] and task["oracle"]["provenance"] and task["oracle"]["missing"],
             "oracle-provenance")
        need(task["native_outcome"].startswith("unexecuted:"), "native-outcome")
        if task["operation"] == "modify":
            need(task["originals"], "modification-original-missing")
            for original in task["originals"]:
                digest = original["sha256"]
                need(len(digest) == 64 and set(digest) <= set("0123456789abcdef"), "original-hash")
                need(original["save_version"] == "unavailable", "invented-original-version")
    need(len(all_ids) == len(set(all_ids)), "duplicate-required-id")
    need(tasks[0]["originals"] == [], "creation-original")
    for task, increment in ((tasks[0], 1), (tasks[3], 2)):
        for x, y in task["expected_semantics"]["vectors"]:
            need(type(x) is int and type(y) is int and y == x + increment,
                 "requirement-arithmetic")
    need(tasks[1]["expected_semantics"]["selected_boolean_relation"] == [[False, True], [True, False]],
         "requirement-inversion")
    need(method["common"]["dimensions"] == ["artifact-fidelity", "answer-correctness",
         "source-grounding", "native-execution"], "dimension-separation")
    need(method["comparison"]["arms"] == ["no-tool", "tool"], "comparison-arms")
    required_matches = {"requested_change_hash", "original_manifest_hash", "allowed_inputs_hash",
                        "total_token_budget", "wall_time_budget", "case_key_revision", "repetition_count"}
    need(required_matches <= set(method["comparison"]["matched_fields"]), "comparison-matching")
    need(len(method["coverage"]["uncovered_families"]) >= 18 and method["coverage"]["gaps"],
         "coverage-gaps")
    check_wp1_method(method)
    return "method-consistent;native-unavailable"


def check_example(example, frozen):
    # Fictional graph snapshots only: this is not a LabVIEW parser or general scorer.
    original, candidate = example["original"], example["candidate"]
    rebuild = example.get("requirement") == "source-rebuild"
    if rebuild:
        need(candidate["build"]["source_available"] is True, "missing-source")
    if example["operation"] == "create":
        need("result.synth" not in original, "creation-destination-exists")
    need(same(candidate["original_after"], original), "original-not-preserved")
    need(candidate["support"] == "synthetic-supported", "unsupported-artifact")
    files = candidate["files"]
    need(set(files) == {"result.synth", "sentinel.txt"}, "output-file-set")
    artifact = files["result.synth"]
    need(artifact.get("version") is not None, "save-version-unverified")
    need(artifact["version"] == frozen["version"], "version-drift")
    if example["operation"] == "modify":
        original_version = original["result.synth"].get("version")
        need(original_version is not None, "save-version-unverified")
        need(artifact["version"] == original_version, "version-drift")
    graph = artifact["graph"]
    if example["operation"] == "modify":
        need(not same(graph, original["result.synth"]["graph"]), "no-op-edit")
    need(graph.get("type") == "I32", "wrong-type")
    need(same(graph, frozen["graph"]), "wrong-behavior")
    need(set(artifact) == {"version", "graph", "label"} and artifact["label"] == frozen["label"]
         and files["sentinel.txt"] == frozen["sentinel"], "unintended-edits")
    answer = candidate["answer"]
    need(set(answer) == {"relation", "vectors", "source", "output_source"}, "extra-answer-claim")
    need(answer["relation"] == ("y=x+2" if rebuild else "y=x+1")
         and same(answer["vectors"], frozen["vectors"]),
         "answer-incorrect")
    source = ("controls.json#/frozen/request" if example["operation"] == "create" else
              "controls.json#/examples/1/original/result.synth/graph")
    if rebuild:
        source = "controls.json#/examples/2/original/result.synth/graph"
        build = candidate["build"]
        need(same(build["source_graph"], graph), "source-build-link")
        need(build["builder_available"] is False and build["compiled_outputs"] == []
             and build["status"] == "unexecuted", "build-unexecuted")
    need(answer["source"] == source and answer["output_source"] == "result.synth#/graph",
         "source-unsupported")
    need(same(candidate["native"], frozen["native"]), "native-unexecuted")
    return ("synthetic-source-consistent;build-unexecuted" if rebuild else
            "synthetic-consistent;native-unexecuted")


def check_pair(pair):
    arms = pair["arms"]
    need(len(arms) == 2 and {a["arm"] for a in arms} == {"no-tool", "tool"}, "planned-arm-missing")
    need(len({a["session"] for a in arms}) == 2, "session-reused")
    need(REQUIRED_PAIR_SETTINGS <= set(pair["frozen"]), "pair-setting-required")
    for arm in arms:
        settings = arm["settings"]
        need(REQUIRED_PAIR_SETTINGS <= set(settings), "pair-setting-required")
        need(set(settings) == set(pair["frozen"]), "pair-setting-set")
        for name, value in pair["frozen"].items():
            need(same(settings[name], value), "pair-" + name + "-mismatch")
        need("output_artifacts" in arm and arm["output_artifacts"] == [], "output-accounting-missing")
        need(arm["attempt_status"] == "unexecuted" and bool(arm["failure_reason"]),
             "failure-accounting-missing")
    return "synthetic-pair-consistent;zero-agent-runs"


# Answer-ledger controls (issue #947, UF-A). The scoring rules they enforce are the
# protocol.md "Account for every required ID ..." paragraph: omissions retain their
# required slots; repeated equivalent assertions earn credit once; an assertion and
# its negation are a contradiction that marks the affected item incorrect. They run
# on in-memory synthetic ledgers built from the method's own required answer IDs
# and add no scoring semantics: a ledger is data a scorer would have to produce.
LEDGER_REASONS = {
    "ledger-omitted-required-id": "required-id-omitted",
    "ledger-duplicate-credited-twice": "duplicate-credited-twice",
    "ledger-contradiction-not-incorrect": "contradiction-not-incorrect",
}


def check_answer_ledger(ledger, required):
    outcomes, rows = ledger["outcomes"], ledger["assertions"]
    # A dropped required ID must stay in the frozen denominator, not vanish.
    need(len(outcomes) == len(required) and set(outcomes) == set(required),
         "required-id-omitted")
    credited, polarities = {}, {}
    for row in rows:
        slot = row["required_id"]
        credited[slot] = credited.get(slot, 0) + (1 if row["credited"] else 0)
        polarities.setdefault((slot, row["claim"]), set()).add(row["polarity"])
    need(all(count <= 1 for count in credited.values()), "duplicate-credited-twice")
    contradicted = [key for key, signs in polarities.items() if signs == {True, False}]
    for slot, _ in contradicted:
        need(outcomes[slot] == "incorrect", "contradiction-not-incorrect")
    duplicates = len(rows) - len({(r["required_id"], r["claim"], r["polarity"]) for r in rows})
    need(same(ledger["counts"], {"duplicates": duplicates, "contradictions": len(contradicted)}),
         "ledger-count-mismatch")
    return "ledger-consistent"


def check_answer_ledger_controls(method):
    required = method["tasks"][0]["answer_ids"]
    need(len(required) >= 2, "ledger-fixture-ids")
    first, last = required[0], required[-1]
    base = {"outcomes": {i: "correct" for i in required},
            "assertions": [{"required_id": i, "claim": "synthetic claim for " + i,
                            "polarity": True, "credited": True} for i in required],
            "counts": {"duplicates": 0, "contradictions": 0}}
    # Positive controls: a duplicate credited once and a contradiction marked
    # incorrect are accepted, so rejecting everything cannot pass these controls.
    duplicate_once = copy.deepcopy(base)
    duplicate_once["assertions"].append(dict(base["assertions"][0], credited=False))
    duplicate_once["counts"]["duplicates"] = 1
    contradiction_incorrect = copy.deepcopy(base)
    contradiction_incorrect["assertions"][0]["credited"] = False
    contradiction_incorrect["assertions"].append(
        dict(base["assertions"][0], polarity=False, credited=False))
    contradiction_incorrect["outcomes"][first] = "incorrect"
    contradiction_incorrect["counts"]["contradictions"] = 1
    positive = {}
    for name, ledger in (("ledger-base", base), ("ledger-duplicate-credited-once", duplicate_once),
                         ("ledger-contradiction-incorrect", contradiction_incorrect)):
        positive[name] = check_answer_ledger(ledger, required)
    omitted = copy.deepcopy(base)
    del omitted["outcomes"][last]
    omitted["assertions"] = [r for r in omitted["assertions"] if r["required_id"] != last]
    duplicate = copy.deepcopy(base)
    duplicate["assertions"].append(dict(base["assertions"][0]))
    duplicate["counts"]["duplicates"] = 1
    contradiction = copy.deepcopy(base)
    contradiction["assertions"].append(dict(base["assertions"][0], polarity=False, credited=False))
    contradiction["counts"]["contradictions"] = 1
    rejected = {}
    for name, ledger in (("ledger-omitted-required-id", omitted),
                         ("ledger-duplicate-credited-twice", duplicate),
                         ("ledger-contradiction-not-incorrect", contradiction)):
        try:
            check_answer_ledger(ledger, required)
        except Inconsistent as error:
            need(str(error) == LEDGER_REASONS[name],
                 "wrong-rejection-reason:" + name + ":" + str(error))
            rejected[name] = str(error)
        else:
            raise Inconsistent("negative-control-accepted:" + name)
    return {"positive": positive, "rejected": rejected}


def mutate(value, changes):
    result = copy.deepcopy(value)
    for change in changes:
        parent = result
        for part in change["path"][:-1]:
            parent = parent[part]
        key = change["path"][-1]
        if change.get("delete"):
            del parent[key]
        else:
            parent[key] = copy.deepcopy(change["value"])
    return result



# WP1 is a separate public project-text preparation stratum. These constants
# pin the reviewed source/request, never a candidate or a native observation.
ROOT = HERE.parent.parent
REVIEW_PATH = 'benchmark/project-text-writing-0109/review-0110.json'
REVIEW_SHA256 = '2dc007939a4b0637716027ef6e5a874702c9be7288daf80c3f007c07f382cdaf'
PROPOSAL_PATH = 'benchmark/project-text-writing-0109.json'
PROPOSAL_SHA256 = '74b6346cb646a8caa10a90462edee266832260d26c6f3685d7fd461cb56abdf8'
PROVENANCE_PATH = 'benchmark/writing/integration-0112-provenance.json'
PROVENANCE_MD = 'benchmark/writing/integration-0112-provenance.md'
BASELINE = {'commit': '575d59ef8fcaf1f81a81d2eb605f52eb94053839',
            'tree': 'bd09e3a07e772337a3f045f69611b9f51dd3e227'}
CHANGED_EXISTING = [
    'benchmark/writing/method.json', 'benchmark/writing/README.md',
    'benchmark/writing/verify_method.py', 'benchmark/writing/controls.json',
    'benchmark/writing/verification.json',
]
INTEGRATION_OUTPUTS = set(CHANGED_EXISTING) - {'benchmark/writing/verification.json'}
INTEGRATION_OUTPUTS.add(PROVENANCE_MD)
ENVELOPE = '.github/loop/data/session-reports/547/ba754b9a0cc86b2d1cd17aa6287c05ad71696775c9e2c92a22f9db02415d6861.json'
EXTRA_HISTORICAL = {
    REVIEW_PATH: REVIEW_SHA256,
    'benchmark/project-text-writing-0109/review-0110-provenance.md':
        'b36c4b56aaad03c93fb3cca444367c8525b492e8e0a31868f0727f2718623364',
    ENVELOPE: 'ba754b9a0cc86b2d1cd17aa6287c05ad71696775c9e2c92a22f9db02415d6861',
}
PROJECT_REASONS = {
    'project-no-op': 'project-no-op',
    'project-wrong-locator': 'project-locator',
    'project-wrong-value': 'project-value',
    'project-wrong-precondition': 'project-precondition',
    'project-wrong-original': 'project-original-hash',
    'project-wrong-allowance': 'project-delta-contract',
    'project-wrong-location-edit': 'project-value',
    'project-unrelated-byte': 'project-byte-delta',
    'project-extra-file': 'project-file-set',
    'project-missing-file': 'project-file-set',
    'project-unrelated-file': 'project-unrelated-file',
    'project-original-overwritten': 'project-original-not-preserved',
    'project-bom-removed': 'project-serialization',
    'project-line-endings': 'project-serialization',
    'project-xml-declaration': 'project-serialization',
    'project-entity-rewrite': 'project-byte-delta',
    'project-final-newline': 'project-serialization',
    'project-version-drift': 'project-version-declaration',
    'project-duplicate-property': 'project-locator-count',
    'project-property-type': 'project-property-precondition',
    'project-false-native_validity': 'project-unsupported-pass',
    'project-false-dependency_resolution': 'project-unsupported-pass',
    'project-false-build': 'project-unsupported-pass',
    'project-false-behavior': 'project-unsupported-pass',
    'project-false-save_version': 'project-unsupported-pass',
    'project-false-overall_writing': 'project-unsupported-pass',
    'project-method-invented-save-version': 'invented-original-version',
    'project-method-native-key': 'native-key-unavailable',
    'project-method-overall-pass': 'project-task-planned_results',
    'project-method-missing-task': 'task-inventory',
}
# Current-file validity is decided only by CURRENT_PINS_PATH (issue #941): every
# repository file read must be listed there and match its size and sha256. A
# later correction re-pins by editing that one file. Section "current" lists
# files a correction may change (including the live indexes preparation.json and
# input-pins.json, whose historical proposal pins stay frozen); section "frozen"
# lists historical records, which must also equal the pin the frozen proposal,
# review or provenance recorded. The pin file cannot pin itself; its hash is
# printed under inputs_sha256.
CURRENT_PINS_PATH = 'benchmark/writing/current-pins.json'
PIN_SECTIONS = ('current', 'frozen')
CURRENT_PINS = None
READ_INPUTS = {}
PROPOSAL = None


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_repository(path):
    relative = Path(path)
    need(not relative.is_absolute() and '..' not in relative.parts
         and '.session' not in relative.parts, 'repository-input-path')
    location = ROOT / relative
    need(location.resolve().is_relative_to(ROOT) and not any(
        (ROOT / Path(*relative.parts[:i])).is_symlink()
        for i in range(1, len(relative.parts) + 1)), 'repository-input-path')
    if path not in READ_INPUTS:
        data = location.read_bytes()
        if path != CURRENT_PINS_PATH:
            check_pin(current_pins(), path, data)
        READ_INPUTS[path] = data
    return READ_INPUTS[path]


def parse_pins(data):
    pins = json.loads(data)
    need(type(pins) is dict and set(pins) == {'schema_version', 'meaning'} | set(PIN_SECTIONS)
         and pins['schema_version'] == 1, 'current-pin-file')
    for section in PIN_SECTIONS:
        need(type(pins[section]) is dict and pins[section], 'current-pin-file')
        for path, pin in pins[section].items():
            need(type(path) is str and type(pin) is dict and set(pin) == {'size', 'sha256'}
                 and type(pin['size']) is int and type(pin['sha256']) is str
                 and len(pin['sha256']) == 64 and set(pin['sha256']) <= set('0123456789abcdef'),
                 'current-pin-file')
    need(not set(pins['current']) & set(pins['frozen']), 'current-pin-file')
    need(CURRENT_PINS_PATH not in pins['current'] and CURRENT_PINS_PATH not in pins['frozen'],
         'current-pin-file')
    return pins


def current_pins():
    global CURRENT_PINS
    if CURRENT_PINS is None:
        CURRENT_PINS = parse_pins(read_repository(CURRENT_PINS_PATH))
    return CURRENT_PINS


def check_pin(pins, path, data):
    # The single place where the validity of a live repository file is decided.
    sections = [s for s in PIN_SECTIONS if path in pins[s]]
    need(len(sections) == 1, 'current-pin-unlisted:' + path)
    need(same({'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()},
              pins[sections[0]][path]), 'current-pin-drift:' + path)


def check_pin_controls():
    pins = current_pins()
    path = 'benchmark/writing/method.json'
    data = read_repository(path)
    check_pin(pins, path, data)
    wrong_hash = copy.deepcopy(pins)
    wrong_hash['current'][path]['sha256'] = '0' * 64
    wrong_size = copy.deepcopy(pins)
    wrong_size['current'][path]['size'] += 1
    unlisted = copy.deepcopy(pins)
    del unlisted['current'][path]
    rejections = {}
    for name, bad, reason in (('wrong-hash', wrong_hash, 'current-pin-drift:' + path),
                              ('wrong-size', wrong_size, 'current-pin-drift:' + path),
                              ('unlisted-file', unlisted, 'current-pin-unlisted:' + path),
                              ('changed-bytes', pins, 'current-pin-drift:' + path)):
        try:
            check_pin(bad, path, data + b' ' if name == 'changed-bytes' else data)
        except Inconsistent as error:
            need(str(error) == reason, 'pin-control-wrong-reason:' + name + ':' + str(error))
            rejections[name] = reason
        else:
            raise Inconsistent('pin-control-accepted:' + name)
    malformed = json.loads(read_repository(CURRENT_PINS_PATH))
    malformed['current'][path]['sha256'] = 'not-a-hash'
    try:
        parse_pins(json.dumps(malformed))
    except Inconsistent as error:
        need(str(error) == 'current-pin-file', 'pin-control-wrong-reason:malformed-hash')
        rejections['malformed-hash'] = 'current-pin-file'
    else:
        raise Inconsistent('pin-control-accepted:malformed-hash')
    return rejections


def file_pin(path):
    data = read_repository(path)
    return {'size': len(data), 'sha256': digest(data)}


def check_integration_inputs():
    global PROPOSAL
    need(digest(read_repository(REVIEW_PATH)) == REVIEW_SHA256, 'preserved-review-pin-drift')
    review = json.loads(read_repository(REVIEW_PATH))
    need(review['overall_recommendation'] == 'CLEAR'
         and review['later_integration_assessment']['assessed_not_modified'] is True,
         'review-scope')
    need(digest(read_repository(PROPOSAL_PATH)) == PROPOSAL_SHA256, 'proposal-pin-drift')
    PROPOSAL = json.loads(read_repository(PROPOSAL_PATH))
    need(PROPOSAL['integration_after_review']['existing_files_to_change'] == CHANGED_EXISTING,
         'integration-scope')
    # Historical changed-input hashes remain historical, not current pins.
    baseline_pins = {p: PROPOSAL['input_pins'][p] for p in CHANGED_EXISTING}
    historical = {p: pin for p, pin in {
        **PROPOSAL['input_pins'], **PROPOSAL['supplementary_pins']
    }.items() if p not in CHANGED_EXISTING}
    historical[PROPOSAL_PATH] = {'size': 20557, 'sha256': PROPOSAL_SHA256}
    for path, pin in review['scoped_files'].items():
        historical[path] = {'size': pin['size'], 'sha256': pin['sha256']}
    for path, sha256 in EXTRA_HISTORICAL.items():
        actual = file_pin(path)
        need(actual['sha256'] == sha256, 'historical-pin-drift:' + path)
        historical[path] = actual
    live = current_pins()['current']
    for path, expected in historical.items():
        if path in live:
            # The historical pin stays frozen (compared with the provenance
            # addendum below); the live bytes were already checked against
            # current-pins.json when read.
            file_pin(path)
            continue
        need(same(file_pin(path), expected), 'historical-pin-drift:' + path)
    envelope = json.loads(read_repository(ENVELOPE))
    need(envelope['report']['issue'] == 547 and envelope['report']['snapshot'] ==
         'd6eb2085115b86ba4e78c52b2307ddf0d700826dc74a4d31043d5e6f9d7303ef',
         'review-envelope-identity')
    provenance = json.loads(read_repository(PROVENANCE_PATH))
    need(provenance['schema_version'] == 1 and provenance['issue'] == 554
         and provenance['status'] == 'author-integration-awaiting-independent-review',
         'integration-provenance-status')
    need(same(provenance['baseline'], BASELINE), 'integration-baseline')
    need(same(provenance['reviewed_identities'], review['identities']), 'reviewed-identities')
    need(same(provenance['baseline_files'], baseline_pins), 'integration-baseline-pins')
    need(same(provenance['historical_unchanged'], historical), 'historical-pin-inventory')
    need(provenance['changed_existing'] == CHANGED_EXISTING and provenance['new_files'] ==
         [PROVENANCE_PATH, PROVENANCE_MD], 'integration-path-inventory')
    need(provenance['historical_checker']['run_on_integration'] is False
         and provenance['historical_checker']['status'] == 'invalidated-for-current-writing-inputs'
         and provenance['historical_checker']['path'] == 'benchmark/scripts/check_project_text_writing_0109.py'
         and same(provenance['historical_checker']['historical_tree'], review['identities']['accepted_candidate']),
         'historical-checker-boundary')
    need(provenance['independent_integration_review'] == 'pending'
         and provenance['owner_method_acceptance'] == 'pending'
         and provenance['candidate_identity'] == 'parent must pin final committed candidate commit/tree; no self-referential identity',
         'integration-authority')
    need(same(provenance['review'], {
        'path': REVIEW_PATH, 'sha256': REVIEW_SHA256, 'recommendation': 'CLEAR',
        'scope': review['recommendation_scope'],
        'C1': 'Retain independent semantic, extra-claim, contradiction and citation review; structured checks do not validate arbitrary prose or future answers.'}), 'integration-review-boundary')
    need(same(provenance['limits'], {
        'project_files_edited': 0, 'agent_runs': 0, 'native_executions': 0,
        'benchmark_ready': False, 'key_approval': 'pending',
        'native_save_version': 'unavailable', 'overall_writing': 'unverified',
        'allocation_budgets_quota_isolation': 'pending',
        'public_lineage': 'NI Actor Framework; familiar-possible; one lineage'}),
        'integration-limits')
    need(provenance['historical_checker']['sha256'] ==
         file_pin('benchmark/scripts/check_project_text_writing_0109.py')['sha256'],
         'historical-checker-pin')
    need(same(provenance['mapping'], PROPOSAL['requirements']), 'integration-mapping')
    need(set(provenance['outputs']) == INTEGRATION_OUTPUTS, 'integration-output-inventory')
    for path, expected in provenance['outputs'].items():
        if path in live:
            # Recorded in 0112 for the bytes of that day; later corrections
            # re-pin in current-pins.json, which file_pin already enforced.
            file_pin(path)
            continue
        need(same(file_pin(path), expected), 'integration-output-pin-drift:' + path)
    return {'status': 'integration-pins-consistent', 'historical_unchanged_count': len(historical),
            'current_output_pins': len(INTEGRATION_OUTPUTS), 'review_sha256': REVIEW_SHA256,
            'historical_checker': 'not-run; historical-tree-only',
            'hash_graph': 'provenance pins method/controls/README/verifier/documentation; stdout pins provenance; verification records stdout; no self-hashes'}


def check_wp1_method(method):
    wp = method['tasks'][4]
    task = PROPOSAL['task']
    need(wp['stratum'] == 'public-development-project-text-preparation', 'project-task-stratum')
    need(same(wp['text_contract'], {k: task[k] for k in ('locator', 'precondition', 'delta')}),
         'project-task-contract')
    need(same(wp['preconditions'][0], task['precondition']) and wp['request'] == task['request']
         and same(wp['expected_semantics'], {'kind': 'exact-text-only', 'locator': task['locator'],
                                            'delta': task['delta']}), 'project-task-contract')
    need(same(wp['originals'], [{'commit': PROPOSAL['source']['commit'],
         'path': PROPOSAL['source']['path'], 'snapshot': PROPOSAL['source']['snapshot'],
         'sha256': PROPOSAL['source']['sha256'], 'save_version': 'unavailable'}]),
         'project-native-save-version-unavailable')
    need(wp['output_paths'] == [task['output_path']] and wp['semantic_ids'] == task['text_ids']
         and wp['preservation_ids'] == task['preservation_ids'] and wp['answer_ids'] == task['answer_ids'],
         'project-task-ids')
    for field, expected in [('preservation', PROPOSAL['preservation']),
                            ('planned_results', PROPOSAL['planned_results']),
                            ('trial_artifacts', PROPOSAL['trial_artifacts']),
                            ('lineage', PROPOSAL['isolation']),
                            ('comparison', PROPOSAL['comparison']),
                            ('requirements_mapping', PROPOSAL['requirements'])]:
        need(same(wp[field], expected), 'project-task-' + field)
    need(wp['oracle']['text_key_status'] == 'proposed-awaiting-separate-check'
         and wp['oracle']['preflight'] == PROPOSAL['oracle']['preflight']
         and wp['oracle']['native_recipe'] == PROPOSAL['oracle']['native_recipe'],
         'project-oracle-boundary')
    coverage = method['coverage']['project_text_preparation']
    need(coverage['case_id'] == wp['id'] and coverage['native_save_version'] == 'unavailable'
         and coverage['native_validation'] == 'unexecuted' and coverage['root_version_declaration'] == '20008000'
         and '.lvlib and .lvproj direct creation/modification' in method['coverage']['uncovered_families'],
         'project-coverage-boundary')
    need(digest(canonical(method['tasks'][:4]).encode()) ==
         'c12b0686ebfe6a0e15c563734d12dae1b30b6496e3d25110ba048e1cff937875',
         'synthetic-task-definition-drift')


def apply_byte_edits(original, edits):
    # Fixture-only splices reference offsets in the preserved original. They do
    # not locate or edit arbitrary project inputs; no file is ever emitted.
    result = original
    previous = len(original) + 1
    for edit in sorted(edits, key=lambda row: row['offset'], reverse=True):
        offset = edit['offset']
        removed, inserted = bytes.fromhex(edit['remove_hex']), bytes.fromhex(edit['insert_hex'])
        need(type(offset) is int and 0 <= offset <= len(original)
             and offset + len(removed) <= previous
             and original[offset:offset + len(removed)] == removed, 'project-fixture-edit')
        result = result[:offset] + inserted + result[offset + len(removed):]
        previous = offset
    return result


def project_fixture(example, original):
    source = apply_byte_edits(original, example['input_edits'])
    files = {'sentinel.txt': example['sentinel'].encode()}
    if not example['omit_project']:
        files[PROPOSAL['task']['output_path']] = apply_byte_edits(original, example['project_edits'])
    files.update({path: value.encode() for path, value in example['extra_files'].items()})
    return {'original': source,
            'original_after': apply_byte_edits(source, example['original_after_edits']),
            'files': files, 'contract': example['contract'], 'outcomes': example['outcomes']}


def check_project_text(example):
    original = example['original']
    need(digest(original) == PROPOSAL['source']['sha256'] and len(original) == 5806,
         'project-original-hash')
    contract, task = example['contract'], PROPOSAL['task']
    need(contract['locator'] == task['locator'], 'project-locator')
    need(same(contract['precondition'], task['precondition']), 'project-precondition')
    need(same(contract['delta'], task['delta']), 'project-delta-contract')
    root = ET.fromstring(original)
    pre = task['precondition']
    need(root.tag == pre['root_tag'] and same(root.attrib, pre['root_attributes']),
         'project-precondition')
    selected = root.findall(contract['locator'])
    need(len(selected) == pre['match_count'] == 1, 'project-precondition')
    prop = selected[0]
    need(same(prop.attrib, pre['property_attributes']) and prop.text == pre['text']
         and len(prop) == pre['property_children'] == 0, 'project-precondition')
    need(original[3347:3348] == b'2' and original[:3347].count(b'\n') + 1 == 42,
         'project-precondition')
    need(example['original_after'] == original, 'project-original-not-preserved')
    path = task['output_path']
    need(set(example['files']) == {path, 'sentinel.txt'}, 'project-file-set')
    need(example['files']['sentinel.txt'] == b'unchanged unrelated bytes', 'project-unrelated-file')
    output = example['files'][path]
    need(output != original, 'project-no-op')
    need(output.startswith(b'\xef\xbb\xbf') and output.split(b'\n', 1)[0] == original.split(b'\n', 1)[0]
         and b'\r' not in output and output.endswith(b'\n')
         and output.count(b'\n') == original.count(b'\n'), 'project-serialization')
    changed_root = ET.fromstring(output)
    need(changed_root.attrib.get('LVVersion') == '20008000', 'project-version-declaration')
    selected = changed_root.findall(contract['locator'])
    need(changed_root.tag == 'Project' and len(selected) == 1, 'project-locator-count')
    need(same(selected[0].attrib, pre['property_attributes']) and len(selected[0]) == 0,
         'project-property-precondition')
    need(selected[0].text == '3', 'project-value')
    # This equality protects every byte: ancestor/sibling order, attributes,
    # auto-increment, entity spelling, whitespace and all metadata included.
    expected = original[:3347] + b'3' + original[3348:]
    need(output == expected and len(output) == 5806, 'project-byte-delta')
    need(same(example['outcomes'], dict(PROPOSAL['planned_results'],
         text_correctness='correct', root_version_declaration='correct')), 'project-unsupported-pass')
    return 'project-text-consistent;native-unexecuted;save-version-unverified'


def check_project_controls(controls, method):
    need(set(controls['strata']) == {'synthetic', 'project_text'}, 'fixture-strata-inventory')
    project = controls['project_text']
    need(project['visibility'] == 'public-development-project-text-only'
         and project['case_id'] == PROPOSAL['case_id'] and same(project['source'], PROPOSAL['source']),
         'project-fixture-scope')
    synthetic = {key: value for key, value in controls.items() if key not in {'strata', 'project_text'}}
    synthetic['visibility'] = 'public-development-synthetic-only'
    need(digest(canonical(synthetic).encode()) ==
         'edb6c3324d50ca9693c3326583a4ca5f679c6428f6e521552e36f560a4c5231d',
         'synthetic-control-definition-drift')
    original = read_repository(PROPOSAL['source']['snapshot'])
    positive = project['positive']
    need(positive['id'] == 'project-text-positive', 'project-positive-inventory')
    result = check_project_text(project_fixture(positive, original))
    need(result == project['expected'], 'project-positive-outcome')
    rows = project['rejecting_controls']
    need(len(rows) == len(PROJECT_REASONS)
         and {row['id']: row['reason'] for row in rows} == PROJECT_REASONS,
         'project-rejecting-control-inventory')
    rejections = {}
    for row in rows:
        try:
            if row.get('target') == 'method':
                check_method(mutate(method, row['changes']))
            else:
                need('target' not in row, 'project-control-target')
                check_project_text(project_fixture(mutate(positive, row['changes']), original))
        except Inconsistent as error:
            need(str(error) == row['reason'], 'project-wrong-rejection-reason:' + row['id'] + ':' + str(error))
            rejections[row['id']] = str(error)
        else:
            raise Inconsistent('project-negative-control-accepted:' + row['id'])
    return {'positive_controls': {'project-text-positive': result},
            'rejected_controls': rejections, 'rejected_count': len(rejections),
            'fixture_output_sha256': digest(original[:3347] + b'3' + original[3348:]),
            'project_files_written': 0, 'trial_executed': False,
            'native_executions': 0, 'native_save_version': 'unverified',
            'overall_writing': 'unverified', 'independent_key_approval': 'pending',
            'meaning': 'public-development text preparation only; C1 semantic/extra/contradiction/citation review remains required'}


# R4a/R5a/R6b design records (issue #958, review #954 finding 1). Each check reads the
# named method.json key and recomputes from the files themselves; none adds coverage.
LINEAGE_PATH = 'benchmark/lineage.json'
METHOD_PATH = 'benchmark/writing/method.json'
ADDENDUM_PATH = 'benchmark/writing/baseline-addendum.json'
ADDENDUM_BUILDER = 'benchmark/writing/build_addendum.py'
MATRIX_KINDS = {'task', 'uncovered-family', 'version', 'limitation'}


def check_lineage_map(method, lineage, lineage_sha256):
    # method.json key lineage_map (review #938 row R4a) against benchmark/lineage.json.
    lmap = method['lineage_map']
    need(lmap['source'] == LINEAGE_PATH and lmap['source_sha256'] == lineage_sha256,
         'lineage-map-source-hash')
    need(lmap['source_status'] == lineage['status'], 'lineage-map-source-status')
    need(lmap['partition'] == 'development' and lmap['restricted_claim'] is False,
         'lineage-map-claim')
    group = lineage['lineage_groups'].get(lmap['group_id'])
    need(group is not None and lmap['group_status'] == group['status'], 'lineage-map-group')
    members = set(group['members'])
    artifacts = {a['id']: a for a in lineage['artifacts']}
    candidates = {c['id']: c for c in lineage['candidate_variants']}
    exact = {g['sha256']: g['members'] for g in lineage['exact_copy_groups']}
    cases = {c['artifact_id']: c for c in lineage['development_case_map']}

    def check_artifact(row, sha256):
        artifact = artifacts.get(row['artifact_id'])
        need(artifact is not None and artifact['sha256'] == sha256, 'lineage-map-artifact')
        need(artifact['path'] == row['artifact_path'], 'lineage-map-path')
        need(row['lineage_group_id'] == lmap['group_id'] and row['artifact_id'] in members,
             'lineage-map-group')

    def check_candidates(rows, artifact_id, complete):
        for row in rows:
            real = candidates.get(row['id'])
            need(real is not None and artifact_id in real['members']
                 and row['members'] == real['members'] and row['rule'] == real['rule']
                 and row['status'] == real['status'] == 'candidate-unadjudicated',
                 'lineage-map-candidate')
        if complete:
            need({row['id'] for row in rows} ==
                 {name for name, real in candidates.items() if artifact_id in real['members']},
                 'lineage-map-candidate')

    tasks = method['tasks']
    need([e['task'] for e in lmap['entries']] == [t['id'] for t in tasks], 'lineage-map-tasks')
    for entry, task in zip(lmap['entries'], tasks):
        if entry.get('lineage_status') == 'gap':
            # A task without an original is a gap: no group, artifact or credit.
            need(not task['originals'] and entry['original_sha256'] is None
                 and set(entry) == {'task', 'original_sha256', 'lineage_status',
                                    'blocking_row', 'reason'}
                 and entry['blocking_row'] and entry['reason'], 'lineage-map-gap-credited')
            continue
        need(len(task['originals']) == 1 and entry['original_sha256'] == task['originals'][0]['sha256'],
             'lineage-map-original-hash')
        check_artifact(entry, entry['original_sha256'])
        need(entry['partition'] == lmap['partition'], 'lineage-map-claim')
        need(entry['exact_copy_group_members'] == exact.get(entry['original_sha256']),
             'lineage-map-exact-copy')
        check_candidates(entry['candidate_variants'], entry['artifact_id'], True)
        real_case = cases.get(entry['artifact_id'])
        case = entry['development_case_map_entry']
        need(case is False if real_case is None else
             (case is not False and case['path'] == real_case['path']
              and case['sha256'] == real_case['sha256']), 'lineage-map-case-map')
        consumers = entry.get('consumer_artifacts', [])
        need({c['sha256'] for c in consumers} ==
             {p['sha256'] for p in task.get('consumer_source_pins', [])}, 'lineage-map-consumers')
        for consumer in consumers:
            check_artifact(consumer, consumer['sha256'])
            listed = consumer.get('candidate_variants', [])
            check_candidates(listed, consumer['artifact_id'], False)
            for member in consumer.get('variant_member_artifacts', []):
                check_artifact(member, member['sha256'])
                need(any(member['artifact_id'] in row['members'] for row in listed),
                     'lineage-map-candidate')
    need(lmap['gaps'] and all(g['gap'] and g['blocking_row'] for g in lmap['gaps']),
         'lineage-map-gaps')
    return 'lineage-map-consistent'


def check_matrix(method):
    # method.json key coverage.matrix (review #938 row R5a, finding UF-D), recounted from its rows.
    matrix = method['coverage']['matrix']
    rows, tasks = matrix['rows'], method['tasks']
    need(rows and len({r['id'] for r in rows}) == len(rows)
         and all(set(r) == set(rows[0]) for r in rows) and {r['kind'] for r in rows} <= MATRIX_KINDS,
         'matrix-rows')
    by_kind = {kind: [r for r in rows if r['kind'] == kind] for kind in MATRIX_KINDS}
    product = matrix['counts']['task_product']
    factors = [product[k] for k in ('tasks', 'families_per_task', 'original_save_versions_per_task',
                                    'validation_versions', 'targets_per_task')]
    need(product['tasks'] == len(tasks) and product['product'] == len(by_kind['task'])
         and product['product'] == factors[0] * factors[1] * factors[2] * factors[3] * factors[4]
         and [r['task'] for r in by_kind['task']] == [t['id'] for t in tasks], 'matrix-task-rows')
    need([r['subject'] for r in by_kind['uncovered-family']] ==
         method['coverage']['uncovered_families'], 'matrix-family-rows')
    need([r['subject'] for r in by_kind['limitation']] ==
         method['common']['limitation_codes'], 'matrix-limitation-rows')
    expected_covered = {t['id']: t['operation'] == 'create' or bool(t['originals']) for t in tasks}
    for row in rows:
        need(row['native'] == 'gap', 'matrix-native-credited')
        need(row['executed'] is False, 'matrix-executed')
        need(row['coverage'] == ('covered' if row['kind'] == 'task' and expected_covered[row['task']]
                                 else 'gap'), 'matrix-gap-credited')
    need(same(matrix['counts'], {
        'rows': len(rows), 'task_rows': len(by_kind['task']), 'task_product': product,
        'uncovered_family_rows': len(by_kind['uncovered-family']),
        'version_rows': len(by_kind['version']), 'limitation_rows': len(by_kind['limitation']),
        'covered_design_only': sum(r['coverage'] == 'covered' for r in rows),
        'gap': sum(r['coverage'] == 'gap' for r in rows),
        'native_covered': sum(r['native'] != 'gap' for r in rows),
        'executed': sum(r['executed'] is not False for r in rows)}), 'matrix-counts')
    return 'matrix-consistent'


def check_addendum(overrides):
    # Reuses build_addendum.py --check (pinned in current-pins.json); no second builder.
    # The pinned source runs with its file reads routed through read_repository (or the
    # in-memory overrides of a control) and without LABVIEW_ENVIRONMENT.
    module = types.ModuleType('build_addendum')
    module.__file__ = str(ROOT / ADDENDUM_BUILDER)
    exec(compile(read_repository(ADDENDUM_BUILDER), ADDENDUM_BUILDER, 'exec'), module.__dict__)
    module.os = types.SimpleNamespace(environ={})
    module.read = lambda path: overrides[path] if path in overrides else read_repository(path)
    try:
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            module.check()
    except SystemExit as error:
        raise Inconsistent('addendum:' + str(error).removeprefix('baseline addendum: '))
    need(json.loads(printed.getvalue())['status'] == 'addendum-consistent', 'addendum-status')
    return 'addendum-consistent'


def check_coverage_controls(method, lineage, lineage_sha256):
    positive = {'lineage-map': check_lineage_map(method, lineage, lineage_sha256),
                'coverage-matrix': check_matrix(method),
                'baseline-addendum': check_addendum({})}
    entry = {e['task']: ['lineage_map', 'entries', i] for i, e in enumerate(method['lineage_map']['entries'])}
    row = {r['id']: ['coverage', 'matrix', 'rows', i] for i, r in enumerate(method['coverage']['matrix']['rows'])}
    wm1, wc1 = entry['WM1-diagram-not'], entry['WC1-create-vi']
    wp1 = method['tasks'][4]['originals'][0]['snapshot']

    def lineage_case(changes):
        return lambda: check_lineage_map(mutate(method, changes), lineage, lineage_sha256)

    def matrix_case(changes):
        return lambda: check_matrix(mutate(method, changes))

    def addendum_hash_drift():
        document = json.loads(read_repository(ADDENDUM_PATH))
        document['tasks'][0]['request']['sha256'] = '0' * 64
        return check_addendum({ADDENDUM_PATH: (json.dumps(document, indent=2, ensure_ascii=False)
                                                + '\n').encode()})

    cases = [
        ('lineage-map-source-hash-drift', 'lineage-map-source-hash',
         lineage_case([{'path': ['lineage_map', 'source_sha256'], 'value': '0' * 64}])),
        ('lineage-map-restricted-claim', 'lineage-map-claim',
         lineage_case([{'path': ['lineage_map', 'restricted_claim'], 'value': True}])),
        ('lineage-map-original-hash-drift', 'lineage-map-original-hash',
         lineage_case([{'path': wm1 + ['original_sha256'], 'value': '0' * 64}])),
        ('lineage-map-wrong-artifact-id', 'lineage-map-artifact',
         lineage_case([{'path': wm1 + ['artifact_id'], 'value': 'artifact-0086'}])),
        ('lineage-map-wrong-path', 'lineage-map-path',
         lineage_case([{'path': wm1 + ['artifact_path'], 'value': 'Core/Other.vi'}])),
        ('lineage-map-gap-credited', 'lineage-map-gap-credited',
         lineage_case([{'path': wc1 + ['artifact_id'], 'value': 'artifact-0087'}])),
        ('lineage-map-candidate-dropped', 'lineage-map-candidate',
         lineage_case([{'path': wm1 + ['candidate_variants'], 'value': []}])),
        ('matrix-task-row-missing', 'matrix-task-rows',
         matrix_case([{'path': row['task-WC1-create-vi'], 'delete': True}])),
        ('matrix-family-row-dropped', 'matrix-family-rows',
         matrix_case([{'path': row['family-01'], 'delete': True}])),
        ('matrix-limitation-row-dropped', 'matrix-limitation-rows',
         matrix_case([{'path': row['limitation-missing-runtime'], 'delete': True}])),
        ('matrix-gap-row-credited', 'matrix-gap-credited',
         matrix_case([{'path': row['family-01'] + ['coverage'], 'value': 'covered'}])),
        ('matrix-gap-task-credited', 'matrix-gap-credited',
         matrix_case([{'path': row['task-WB1-source-rebuild'] + ['coverage'], 'value': 'covered'}])),
        ('matrix-count-drift', 'matrix-counts',
         matrix_case([{'path': ['coverage', 'matrix', 'counts', 'rows'], 'value': 39}])),
        ('matrix-executed-row', 'matrix-executed',
         matrix_case([{'path': row['family-01'] + ['executed'], 'value': True}])),
        ('addendum-request-hash-drift', 'addendum:addendum-differs-from-recomputed-build',
         addendum_hash_drift),
        ('addendum-method-drift', 'addendum:addendum-differs-from-recomputed-build',
         lambda: check_addendum({METHOD_PATH: json.dumps(mutate(method, [
             {'path': ['tasks', 1, 'request'], 'value': method['tasks'][1]['request'] + ' '}])).encode()})),
        ('addendum-original-drift', 'addendum:snapshot-hash:' + wp1,
         lambda: check_addendum({wp1: read_repository(wp1) + b'\n'})),
    ]
    rejected = {}
    for name, reason, run in cases:
        try:
            run()
        except Inconsistent as error:
            need(str(error) == reason, 'wrong-rejection-reason:' + name + ':' + str(error))
            rejected[name] = str(error)
        else:
            raise Inconsistent('negative-control-accepted:' + name)
    return {'positive': positive, 'rejected': rejected}


def main():
    need(len(sys.argv) == 1, "no-external-inputs-supported")
    integration = check_integration_inputs()
    method_bytes = read_repository("benchmark/writing/method.json")
    control_bytes = read_repository("benchmark/writing/controls.json")
    method, controls = json.loads(method_bytes), json.loads(control_bytes)
    need(controls["schema_version"] == 1 and controls["visibility"] == "public-development-synthetic-and-project-text-only",
         "fixture-scope")
    frozen = controls["frozen"]
    need(same(frozen["graph"], {"input": "x", "output": "y", "type": "I32", "operation": "add", "constant": 1})
         and same(frozen["vectors"], [[-2, -1], [0, 1], [7, 8]]), "frozen-requirement-drift")
    need(same(frozen["native"], {"load": "unexecuted", "compile": "unexecuted", "run": "unexecuted",
                              "reason": "missing-runtime"}), "frozen-native-drift")
    rebuild_frozen = controls["frozen_source_rebuild"]
    need(same(rebuild_frozen["graph"], {"input": "x", "output": "y", "type": "I32",
                                      "operation": "add", "constant": 2})
         and same(rebuild_frozen["vectors"], [[-2, 0], [0, 2], [7, 9]])
         and same(rebuild_frozen["native"], frozen["native"]), "frozen-rebuild-drift")
    positives = {"method": check_method(method)}
    examples = {e["id"]: e for e in controls["examples"]}
    need(len(controls["examples"]) == 3 and set(examples) == {"synthetic-create", "synthetic-modify",
         "synthetic-source-rebuild"},
         "positive-inventory")
    for example in examples.values():
        reference = controls["frozen_source_rebuild"] if example.get("requirement") else frozen
        actual = check_example(example, reference)
        expected = ("synthetic-source-consistent;build-unexecuted" if example.get("requirement")
                    else "synthetic-consistent;native-unexecuted")
        need(actual == example["expected"] == expected, "positive-outcome")
        positives[example["id"]] = actual
    positives["pair"] = check_pair(controls["pair"])
    need(positives["pair"] == controls["pair"]["expected"], "positive-pair-outcome")
    rows = controls["rejecting_controls"]
    need(len(rows) == len(CONTROL_REASONS) and {r["id"]: r["reason"] for r in rows} == CONTROL_REASONS,
         "rejecting-control-inventory")
    rejections = {}
    for row in rows:
        try:
            if row["target"] == "method":
                check_method(mutate(method, row["changes"]))
            elif row["target"] == "pair":
                check_pair(mutate(controls["pair"], row["changes"]))
            else:
                example = copy.deepcopy(examples[row["example"]])
                target = row["target"]
                if target == "example":
                    # Version-linkage controls preserve the original before/after
                    # while changing its version relative to the output/reference.
                    example = mutate(example, row["changes"])
                else:
                    example[target] = mutate(example[target], row["changes"])
                reference = controls["frozen_source_rebuild"] if example.get("requirement") else frozen
                check_example(example, reference)
        except Inconsistent as error:
            need(str(error) == row["reason"], "wrong-rejection-reason:" + row["id"] + ":" + str(error))
            rejections[row["id"]] = str(error)
        else:
            raise Inconsistent("negative-control-accepted:" + row["id"])
    ledger = check_answer_ledger_controls(method)
    positives.update(ledger["positive"])
    need(not set(ledger["rejected"]) & set(rejections), "ledger-control-name-clash")
    rejections.update(ledger["rejected"])
    project_text = check_project_controls(controls, method)
    pin_controls = check_pin_controls()
    lineage_bytes = read_repository(LINEAGE_PATH)
    coverage = check_coverage_controls(method, json.loads(lineage_bytes), digest(lineage_bytes))
    need(not set(coverage["rejected"]) & set(rejections), "coverage-control-name-clash")
    rejections.update(coverage["rejected"])
    positives.update(coverage["positive"])
    print(json.dumps({
        "status": "design-consistent", "positive_controls": positives,
        "current_pin_controls": pin_controls,
        "rejected_controls": rejections, "rejected_count": len(rejections),
        "project_text_preparation": project_text, "integration": integration,
        "checker_sha256": digest(read_repository("benchmark/writing/verify_method.py")),
        "inputs_sha256": {path: digest(data) for path, data in sorted(READ_INPUTS.items())},
        "native_executions": 0, "agent_runs": 0, "benchmark_ready": False,
        "independent_review": "pending", "meaning": "design consistency only",
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Inconsistent, KeyError, IndexError, TypeError, ValueError, OSError, ET.ParseError) as error:
        print("writing method verification failed: " + str(error), file=sys.stderr)
        sys.exit(1)
