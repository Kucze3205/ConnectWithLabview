# Keyed-literal constant export probe (0183)

Probe: `.session/artifacts/keyed_literal_probe.py`, output `.session/artifacts/keyed-literal-probe-output.txt`. Run with `python3 -B`; it sets `sys.dont_write_bytecode = True` before importing `benchmark/scripts/score.py` and never calls `main()`. Development-only; no LabVIEW behaviour is claimed. Nothing in score.py, fixtures, results or pins was changed.

## Measured

In-memory calls to `score.compute` (score.py:125) on the positive control of each fixture, executed and scored set to 1. Every required claim (12 ids: A0001-A0010, N0001, N0002) was given the same answer and the same citations taken from one real claim. This was repeated with each of the 12 claims as the source ("chosen literal's claim id"), and in a second variant that also copies that claim's conditions. Representative choice: A0001; all 12 ids give the same verdict.

| Fixture | Verdict | Dimensions (all 24 mutations per fixture) |
|---|---|---|
| library-icon-tests | SAFE | correctness `incorrect`, grounding `incorrect`, fidelity `unverified`; none `correct` or `partial` |
| library-specialty | SAFE | same as above |
| vi-actor-core-native-gap | NOT-APPLICABLE | controls have no claims; stays `unsupported` (score.py:199-200) |

Lines behind the outcomes:
- score.py:207-208: `any(v != target ...)` gives `incorrect` for every claim whose key differs from the literal.
- score.py:34-40 (`assessment`): any `incorrect` among required ids makes the dimension `incorrect`, so one matching claim cannot lift it.
- score.py:218: `correct` is reachable only for a claim whose key equals the literal, so the per-claim correct count is 1 (2 for the A0006 and A0009 sources, whose literal also matches another claim's key). The dimension stays `incorrect`.
- Fidelity stays `unverified` because the reader channel was not altered.
- No `cannot_evaluate_reasons` arose in any run.

The unmodified base gives `unverified` for all dimensions.

## Existing controls

- library-icon-tests has 27 controls, including `constant-export` (the last). library-specialty has 2: `positive-control`, `constant-export`. vi-actor-core-native-gap has 4 unsupported-* controls. No control is named `constant-keyed-literal-export`. The shaper's Grep found none because its pattern matched nothing; a direct listing of control names shows `constant-export` exists in both claim-bearing fixtures.
- The contents of those `constant-export` controls were not read here, so overlap with this probe is not known.
- `regression_self_test` exists at score.py:283.

## Limits

- Only the positive control was mutated; the other controls were not.
- Only the answer channel was made constant; reader observations were left as in the control.
- Variants were limited to answer plus citations, and answer plus citations plus conditions.
- Synthetic fixture scoring is not reader execution. No native evidence exists. Benchmark readiness stays false.
- Detection depends on the key comparison, not on an independent check of the key.
- No control for this case was added; the next shaper must order it and its review.
