#!/usr/bin/env python3
"""Read-only packaging checks; no human scoring, historical code or native execution."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[2]
B = "benchmark/writing/"
HANDOFF_SHA256 = "e520cd5917ede71b6bf1342cb2ceb9991dd9092c7cff82bc64e4dcd2e10ef45b"
PAGE_SHA256 = "ae7e6474b17cdff7e034ebfdaf860599607676b5db635e8149bd9dadc71237b6"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local(path):
    parts = PurePosixPath(path)
    require(not parts.is_absolute() and str(parts) == path and
            all(x not in (".", "..") for x in parts.parts), "nonlocal path: " + path)
    p = ROOT
    for part in parts.parts:
        p = p / part
        require(not p.is_symlink(), "symlink: " + path)
    require(p.is_file(), "missing file: " + path)
    return p


def measure(path):
    raw = local(path).read_bytes()
    require(0 < len(raw) < 2_000_000, "file size: " + path)
    return {"path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def load(path):
    return json.loads(local(path).read_text(encoding="utf-8"))


def pointer(value, locator):
    if locator == "whole-file":
        return value
    require(locator.startswith("/"), "bad JSON pointer: " + locator)
    for token in locator[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def blank(value):
    if isinstance(value, dict):
        return all(blank(v) for v in value.values())
    return value is None or (isinstance(value, list) and not value)


def main():
    require(measure(B + "human-c1-0130.json")["sha256"] == HANDOFF_SHA256,
            "handoff bytes changed; packaging contract requires explicit revision")
    require(measure(B + "human-c1-0130.md")["sha256"] == PAGE_SHA256,
            "ordered human instructions changed")
    d = load(B + "human-c1-0130.json")
    require(d["benchmark_ready"] is False and d["recording_state"] ==
            "unexecuted-blank-handoff", "readiness or execution promotion")
    pins = {f["path"]: f for f in d["source_pins"]}
    require(len(pins) == len(d["source_pins"]) == 27, "missing/duplicate source pins")
    for path, expected in pins.items():
        require(measure(path) == expected, "protected input changed: " + path)
    stages = d["reading_order"]
    require([s["stage"] for s in stages] ==
            ["orientation", "source_evidence", "save_initial", "comparison", "return"],
            "source/save/comparison/return ordering")
    require(all(s["before_initial_save"] is True for s in stages[:2]) and
            stages[2]["before_comparison"] is True and
            stages[3]["requires_saved_initial"] is True and
            stages[3]["execution_allowed"] is False, "missing ordering boundary")
    for stage in stages:
        for ref in stage.get("inputs", []):
            path, loc = ref["path"], ref["locator"]
            require(path in pins, "unpinned reading input: " + path)
            raw = local(path).read_text(encoding="utf-8")
            if loc.startswith("L"):
                ends = [int(x) for x in re.findall(r"\d+", loc)]
                require(len(ends) in (1, 2) and 1 <= ends[0] <= ends[-1] <=
                        len(raw.splitlines()), "line range: " + loc)
            elif loc != "whole-file":
                pointer(json.loads(raw), loc)
    early = [(r["path"], r["locator"]) for s in stages[:2] for r in s["inputs"]]
    require(not any(p.endswith(("c1-challenges-0125-expectations.json",
                               "c1-f1-0129.json", "c1-f1-0129.md", ".py"))
                    for p, _ in early), "early judgment or script exposure")
    require([loc for p, loc in early if p.endswith("c1-challenges-0125-verification.json")] ==
            ["/new_file_manifest"], "early historical verification results")
    require({loc for p, loc in early if p.endswith("wp1-key-review-0124.json")} ==
            {"/reviewed_revision", "/recommendation", "/uncertainty"}, "early prior review")
    cases = load(B + "c1-challenges-0125-cases.json")
    require(len(cases["cases"]) == 8 and all(
        (B + "c1-challenges-0125-cases.json", "/cases/" + str(i)) in early
        for i in range(8)), "case coverage navigation")
    # Validate frozen citation paths/JSON pointers, without interpreting support or labels.
    def references(value):
        if isinstance(value, dict):
            if "path" in value and "sha256" in value and "locator" in value:
                path = value["path"]
                require(path in pins and pins[path]["sha256"] == value["sha256"],
                        "unfrozen citation: " + path)
                if value["locator"].startswith("/"):
                    pointer(load(path), value["locator"])
            for item in value.values():
                references(item)
        elif isinstance(value, list):
            for item in value:
                references(item)
    references(cases["conditions"])
    references(cases["citation_registry"])
    e = d["exposure_boundary"]
    require(e["public"] is True and all(e[x] is False for x in
            ("enforced_blinding", "withheld", "model_unseen_demonstrated")),
            "unsupported exposure/isolation claim")
    require(set(e["no_execution"]) == {"historical checkers", "author scripts",
            "cold probes", "trial arms", "native jobs"}, "execution boundary")
    o = d["overlay_application"]
    frozen = load(B + "c1-f1-0129.json")["application"]
    require((o["base_path"], o["historical_pointer"], o["replacement_pointer"]) ==
            (frozen["base_expectations"], frozen["replace_pointer"], frozen["replacement_pointer"]),
            "overlay application locator")
    require(o["inherit_unchanged_cases"] == list(range(7)) and
            o["comparison_only_after_initial_save"] is True and
            o["general_B_rule"] is False and o["raw_answer_or_V_repaired"] is False,
            "overlay scope broadened")
    pointer(load(o["base_path"]), o["historical_F1_atom_pointer"])
    for loc in [o["replacement_pointer"]] + o["active_replacement_atoms"]:
        pointer(load(o["overlay_path"]), loc)
    receipt = d["review_receipt"]
    require(receipt["transient_input"]["bytes"] == 19785 and
            receipt["transient_input"]["sha256"] ==
            "9dd1a2bd58cb23bd4e43a0fdb93c8cc417aa30dd20c7b3e33e5e9c95809498a6" and
            receipt["total_pin_matches"] == 19 and receipt["protected_pin_matches"] == 15,
            "review receipt identity")
    require(all(pins[f["path"]] == f for f in receipt["measured_package_pins"]),
            "reviewed package identity")
    response = d["response_template"]
    require(blank(response), "fabricated human response")
    require(set(response) == {"existing_ledger_copy_path", "commissioning_coordinator",
            "return_channel", "exposure", "input_freeze", "initial_record", "comparison",
            "completed_record", "return_record"}, "response sections")
    for section in ("initial_record", "completed_record"):
        require({"path", "bytes", "sha256", "saved_at_utc"} <= set(response[section]),
                "missing saved-record identity")
    require("saved_before_comparison" in response["initial_record"] and
            {"historical_0125_disagreements", "overlay_0129_disagreements",
             "unresolved_results", "next_resolver", "first_0125_expectations_read_at_utc",
             "first_0129_overlay_read_at_utc"} <= set(response["comparison"]) and
            {"prior_0125_expectations", "prior_0129_overlay", "accidental_early_exposure",
             "read_events"} <= set(response["exposure"]) and
            {"human_result", "returned_at_utc", "files", "manifest"} <=
            set(response["return_record"]), "response capture fields")
    template = load(d["source_finding"]["reuse_ledger"])
    require(template["human_result"] is None and template["case_records"] == [] and
            template["case_record_template"]["required_denominators"] ==
            {"correctness": 3, "grounding": 3}, "existing ledger boundary")
    require(d["limits"]["actual_human_C1"] == "pending" and
            all(d["limits"][k] == "blocked" for k in
                ("historical_F4", "general_established_key_release", "full_trial_release")) and
            all(d["limits"][k] is None for k in
                ("human_result", "cold_result", "native_result", "trial_result", "quality_result")),
            "unearned result or release")
    page = local(B + "human-c1-0130.md").read_text(encoding="utf-8")
    for link in re.findall(r"\]\(([^)]+)\)", page):
        local(B + link)
    require([int(n) for n in re.findall(r"^(\d+)\. \*\*", page, re.M)] == list(range(1, 8)),
            "ordered human steps missing")
    print(json.dumps({"result": "pass", "scope": "repository packaging only",
                      "protected_source_pins": len(pins), "human_result": None,
                      "benchmark_ready": False}, sort_keys=True))


if __name__ == "__main__":
    main()
