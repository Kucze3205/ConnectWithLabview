#!/usr/bin/env python3
"""Check this public writing DESIGN and its fictional examples; never score LabVIEW.

No CLI input, native APIs, environment, session state, subprocesses or file writes.
The only accepted inputs are the adjacent committed method and synthetic controls.
These checks deliberately do not implement an artifact reader, writer or evaluator.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys

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
}


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
         "WM2-typedef-cluster", "WB1-source-rebuild"], "task-inventory")
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
    for arm in arms:
        settings = arm["settings"]
        need(set(settings) == set(pair["frozen"]), "pair-setting-set")
        for name, value in pair["frozen"].items():
            need(same(settings[name], value), "pair-" + name + "-mismatch")
        need("output_artifacts" in arm and arm["output_artifacts"] == [], "output-accounting-missing")
        need(arm["attempt_status"] == "unexecuted" and bool(arm["failure_reason"]),
             "failure-accounting-missing")
    return "synthetic-pair-consistent;zero-agent-runs"


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


def main():
    need(len(sys.argv) == 1, "no-external-inputs-supported")
    method_bytes = (HERE / "method.json").read_bytes()
    control_bytes = (HERE / "controls.json").read_bytes()
    method, controls = json.loads(method_bytes), json.loads(control_bytes)
    need(controls["schema_version"] == 1 and controls["visibility"] == "public-development-synthetic-only",
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
                example[target] = mutate(example[target], row["changes"])
                reference = controls["frozen_source_rebuild"] if example.get("requirement") else frozen
                check_example(example, reference)
        except Inconsistent as error:
            need(str(error) == row["reason"], "wrong-rejection-reason:" + row["id"] + ":" + str(error))
            rejections[row["id"]] = str(error)
        else:
            raise Inconsistent("negative-control-accepted:" + row["id"])
    print(json.dumps({
        "status": "design-consistent", "positive_controls": positives,
        "rejected_controls": rejections, "rejected_count": len(rejections),
        "inputs_sha256": {"method.json": hashlib.sha256(method_bytes).hexdigest(),
                          "controls.json": hashlib.sha256(control_bytes).hexdigest()},
        "native_executions": 0, "agent_runs": 0, "benchmark_ready": False,
        "independent_review": "pending", "meaning": "design consistency only",
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Inconsistent, KeyError, TypeError, ValueError, OSError) as error:
        print("writing method verification failed: " + str(error), file=sys.stderr)
        sys.exit(1)
