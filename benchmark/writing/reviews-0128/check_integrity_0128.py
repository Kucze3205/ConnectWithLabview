#!/usr/bin/env python3
"""Verify repository preservation; session measurements remain attributed records.

Reads only files beside this script. Never accesses session inputs, the environment,
network, native tools, or the original comparison release. No semantic scoring.
"""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
PINS = {
    "c1-artifact-manifest-0126.json": (601, 28787, "9a655f487a30539450c0abe36d4ebe570b43dc6fbddba914fae0fbd638121bc7"),
    "c1-challenges-review-0126.json": (601, 956134, "cf55770e01161a961b53cced969e81acb7c03223cf7bcf9ad061f38ecfc69e27"),
    "c1-findings-0126.md": (601, 7179, "519fe802c72d1089b55425936ce31485d9d7502b2c602b72bdda92c11f4fbf41"),
    "c1-pins-0126.json": (601, 4511, "916bd993cf979e0ff3810ac3503c9bb1008f6ed564749fd3c3962691698fd690"),
    "c1-checker-run-0126.json": (601, 2378, "04a2146d44bfe5a1a9fb1a775bbec897df3db776c973550dc2569bb13527d49e"),
    "c1-review-completion-0127.json": (604, 10038, "fc11233cd67752355607350a4a223395db07ee65a7933004517f85225d6cf600"),
}
REPORTS = {
    601: ("37d677d796c4460ccc6c613d4952529a5bf7a502bca2cd20e4e3f8465bdec04a", "https://github.com/Kucze3205/ConnectWithLabview/issues/601#issuecomment-6872748257"),
    604: ("9555aca246a03e77e03953bba86010e2c66d1acadfe84670e328ccdacd0c7d87", "https://github.com/Kucze3205/ConnectWithLabview/issues/604#issuecomment-6872958175"),
}
LARGE = "c1-challenges-review-0126.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name):
    return json.loads((BASE / name).read_bytes())


def verify():
    record = load("integrity-0128.json")
    require(record["schema_version"] == 1 and record["issue"] == 607, "record identity")
    require(record["benchmark_ready"] is False, "readiness must remain false")
    require(record["verdicts"] == {"Standards": "CLEAR", "Spec": "NOT-CLEAR"}, "preserved verdicts")
    require(len(record["source_reports"]) == 2, "report count")
    require({r["issue"] for r in record["source_reports"]} == set(REPORTS), "report identities")
    for report in record["source_reports"]:
        snapshot, source = REPORTS[report["issue"]]
        require(report["source"] == source, "report source")
        for key in ("expected_body_sha256", "source_report_asserted_snapshot", "observed_body_sha256"):
            require(report[key] == snapshot, "report snapshot: " + key)
        require(report["equality"] is True, "report snapshot equality")
        require(report["measurement"]["session_issue"] == 607 and report["measurement"]["method"], "report measurement attribution")
    entries = record["artifacts"]
    require(len(entries) == len(PINS), "artifact count")
    require({e["artifact_name"] for e in entries} == set(PINS), "artifact names")
    completion = load("c1-review-completion-0127.json")
    manifest = load("c1-artifact-manifest-0126.json")
    for entry in entries:
        name = entry["artifact_name"]
        issue, size, digest = PINS[name]
        pin = {"bytes": size, "sha256": digest}
        source = f".session/inputs/{issue}-{name}"
        release = f"iter-{'0127' if issue == 604 else '0126'}/{issue}-{name}"
        require(entry["issue"] == issue and entry["source_path"] == source, name + ": identity")
        require(entry["expected"] == pin and entry["observed"] == pin, name + ": fixed pin")
        require(entry["equality"] is True, name + ": equality")
        require(entry["release_reference"] == release, name + ": release")
        require(entry["release_url"] == "https://github.com/Kucze3205/ConnectWithLabview/releases/download/" + release, name + ": release URL")
        measurement = entry["measurement"]
        require(measurement["session_issue"] == 607 and measurement["source_path"] == source, name + ": measurement attribution")
        require(measurement["method"] == "python3 pathlib.Path.read_bytes; len; hashlib.sha256", name + ": measurement method")
        require(measurement["kind"] == "session input byte measurement, not a source-report assertion", name + ": measurement kind")
        assertions = entry["source_report_assertions"]
        require(len(assertions) == (2 if issue == 601 else 1), name + ": assertion count")
        require({a["report_issue"] for a in assertions} == ({601, 604} if issue == 601 else {604}), name + ": assertion provenance")
        for assertion in assertions:
            require(assertion["snapshot"] == REPORTS[assertion["report_issue"]][0], name + ": assertion snapshot")
            require({k: assertion[k] for k in pin} == pin, name + ": asserted pin")
            expected_locator = "c1-review-completion-0127.json#/input_pins" if issue == 601 and assertion["report_issue"] == 604 else "body / Artifacts footer"
            require(assertion["locator"] == expected_locator, name + ": assertion locator")
        if issue == 601:
            saved = next(p for p in completion["input_pins"] if p["path"] == source)
            require({k: saved[k] for k in pin} == pin, name + ": saved #604 pin")
        if issue == 601 and name != "c1-artifact-manifest-0126.json":
            saved = next(p for p in manifest["entries"] if p["path"] == ".session/artifacts/" + name)
            require({k: saved[k] for k in pin} == pin, name + ": saved #601 manifest pin")
        if name == LARGE:
            require(entry["destination"] is None and entry["destination_equals_source"] is None, "large comparison must remain in release")
            require(not (BASE / name).exists(), "large comparison unexpectedly copied")
        else:
            require(entry["destination"] == "benchmark/writing/reviews-0128/" + name, name + ": destination")
            require(entry["destination_equals_source"] is True, name + ": source equality record")
            data = (BASE / name).read_bytes()
            require(len(data) == size and hashlib.sha256(data).hexdigest() == digest, name + ": repository bytes differ")
    print(json.dumps({"status": "ok", "copies_rehashed": 5, "fixed_artifact_pins_checked": 6, "source_report_snapshot_records_checked": 2, "large_comparison": "fixed published pin and attributed #607 measurement checked; original release not rehashed", "benchmark_ready": False}, sort_keys=True))


if __name__ == "__main__":
    try:
        verify()
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as error:
        raise SystemExit("Integrity verification failed: " + str(error))
