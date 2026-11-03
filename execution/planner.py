#!/usr/bin/env python3
"""Script shaper: a deterministic rule that writes the iteration's task graph to `.session/tasks.json`.

Runs without a model or credential in the worker tree (`planner` in `execution/profiles.yml`, named by `shaper` in
`policy/params.yml`). It exists because with `shaper: null` an iteration lived or died by whether the Policymaker
managed to write `.session/orders.json`; iterations 0001-0003 failed because it never did (issue 95).

The rule follows the benchmark-before-product sequence of `docs/perpetua/evaluation.md` through the milestones in
`benchmark/preparation-status.json`. When it has no work for the current state it exits non-zero with the reason:
the iteration then fails and the Policymaker, who is always called after a failed iteration, extends this file.
"""
import json
import os
import sys

STATUS = "benchmark/preparation-status.json"
OUT = ".session/tasks.json"

REVIEW_BODY = """## Goal
Independently review the prepared `sources` milestone (`benchmark/`, status `prepared-not-reviewed`) and the measurement in `docs/research/0002-coverage.md` against `docs/perpetua/evaluation.md`. Expected gain: the first milestone of the verification method gets a reviewed verdict, so later milestones build on checked provenance instead of unreviewed input.
## Acceptance
- [ ] FIRST (within your first 15 turns): run `python3 -I benchmark/scripts/sources.py --check` and `python3 -I docs/research/scripts/coverage/inventory.py`; write the exit codes and any divergence from the committed records to `.session/artifacts/review-sources.md`, so the file exists even if you run out of turns.
- [ ] Check the `sources` row of evaluation.md: origin, license, pinned commit and SHA256 of originals; dependencies, artifact save version and reading environment recorded separately; originals preserved before conversion. Append the findings to the same file after each check.
- [ ] Note what 0002 implies for the `coverage` row (families, versions, modules, access conditions, gaps kept in the denominator) and what is missing.
- [ ] Separate Standards and Spec findings, each with path/line, evidence, impact and correction; end with an overall recommendation tied to the reviewed commit.
## Verification
`python3 -I benchmark/scripts/sources.py --check`
## Context
- docs/perpetua/evaluation.md: the contract being checked
- benchmark/preparation-status.json, benchmark/sources.md, benchmark/sources.json: the candidate
- docs/research/0002-coverage.md: coverage measurement input
- docs/perpetua/environment.md: prepared read-only sources (`$LABVIEW_ENVIRONMENT`)
## Budget
- benchmark/**, docs/research/0002-coverage.md, docs/research/scripts/coverage/inventory.py, docs/perpetua/evaluation.md, docs/perpetua/environment.md
- Do not read other docs broadly; report, do not fix. Do not re-read a file you already read; keep notes in the artifact file.
"""

COVERAGE_BODY = """## Goal
Prepare the `coverage` milestone of `docs/perpetua/evaluation.md`: a repeatable inventory of artifact families, save versions, reading environments, modules and access conditions of the prepared public sources, building on `docs/research/0002-coverage.md`. Expected gain: two of seven milestones prepared with explicit gaps, so the next review can check `coverage` and the next iteration can start `tasks`/`oracle`. The next session checks `benchmark/preparation-status.json` milestones and the verification command below.
## Acceptance
- [ ] `benchmark/scripts/coverage.py` regenerates a committed coverage record (JSON + short markdown) from `$LABVIEW_ENVIRONMENT`; `--check` exits non-zero when the record differs. Follow the generator/--check pattern of `benchmark/scripts/sources.py` and reuse the method of `docs/research/scripts/coverage/inventory.py`; do not copy blindly.
- [ ] The record lists every family and save version found, unsupported/opaque/unreadable cases and unexamined LabVIEW versions as explicit gaps; nothing is removed from the denominator and the 2024 fallback is not chosen.
- [ ] `benchmark/preparation-status.json` sets `coverage` to `prepared-not-reviewed` and keeps `independent_review` pending; do not mark any milestone reviewed or ready.
- [ ] Your report lists what coverage cannot show without native LabVIEW (`native_labview: not executed`).
## Verification
`python3 -I benchmark/scripts/coverage.py --check`
## Context
- docs/perpetua/evaluation.md: `coverage` and `sources` rows
- docs/research/0002-coverage.md and docs/research/scripts/coverage/inventory.py: the method to reuse
- benchmark/scripts/sources.py: existing generator/--check pattern
## Budget
- benchmark/**, docs/research/0002-coverage.md, docs/research/scripts/coverage/inventory.py, docs/perpetua/evaluation.md, docs/perpetua/environment.md, goal/goal.md
- Commit a first working `coverage.py` early; refine afterwards. Do not re-read a file you already read.
"""


def plan(milestones):
    """The tasks for the given milestone statuses, or None when this rule has no work for them."""
    if milestones.get("coverage") == "not-started":
        # Independent of each other: a review that ends `partial` must not leave the coverage task blocked (iteration 0000).
        return [
            {"id": "review-sources", "title": "Independent review of the `sources` milestone and coverage research 0002",
             "role": "reviewer", "effort": "high", "body": REVIEW_BODY, "blocked_by": [],
             "limits": {"timeout_minutes": 120, "max_turns": 100}},
            {"id": "bench-coverage", "title": "Prepare the `coverage` milestone record",
             "role": "benchmark", "effort": "high", "body": COVERAGE_BODY, "blocked_by": [],
             "limits": {"timeout_minutes": 120, "max_turns": 100}},
        ]
    return None


def main():
    try:
        with open(STATUS, encoding="utf-8") as fh:
            milestones = json.load(fh).get("milestones", {})
    except (OSError, ValueError) as error:
        print("planner: cannot read %s: %s" % (STATUS, error), file=sys.stderr)
        return 1
    tasks = plan(milestones)
    if not tasks:
        print("planner: no rule for milestones %s; the Policymaker must extend execution/planner.py" %
              json.dumps(milestones, sort_keys=True), file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"tasks": tasks}, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
