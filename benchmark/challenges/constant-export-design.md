# Constant / empty export detection design

Probe: `.session/artifacts/constant_probe.py`, output `.session/artifacts/constant-probe-output.txt`, commit 557a2868366a42bd2a787b169ed71a61de59fcb8. Development-only; no LabVIEW behaviour is claimed.

## Measured

In-memory calls to `score.compute` (score.py:125) on the positive control of each fixture, with executed and scored set to 1.

| Probe | library-icon-tests | library-specialty | vi-actor-core-native-gap |
|---|---|---|---|
| Empty export (no claims, no observations) | DETECTED: all dimensions `missing` (score.py:203-204) | DETECTED: all `missing` (score.py:203-204) | NOT-APPLICABLE: controls have no claims; stays `unsupported` (score.py:199-200) |
| Constant export (the string "constant" for every claim and observation, citations removed) | DETECTED: all `incorrect` (score.py:207-208) | DETECTED: all `incorrect` (score.py:207-208) | NOT-APPLICABLE: stays `unsupported` (score.py:199-200) |

The unmodified base submission gives `unverified` dimensions, with 10 correct per-claim correctness and grounding outcomes. Mutated variants score zero correct.

## Design

Proposed before any code change. For each claim-bearing fixture, add or confirm a control named `constant-keyed-literal-export`:

- Fixture shape: every required claim answers with the same keyed literal, taken from one real claim, with that claim's citations.
- Expected scorer outcome: only the claim whose key matches that literal may be `correct`. All other required claims are `incorrect`, so no dimension is `correct` or `partial`. The `incorrect` claims come from the score.py:207-208 mismatch branch.
- Add an explicit assertion in `regression_self_test` that a uniform answer across all required ids never yields a `correct` dimension. This is a count check, not a per-claim one, so it would also catch a scorer change that stops comparing against the key.
- Keep the empty-export and constant-export controls as regression controls, with expected values frozen from the measured results above. Any change to a pinned fixture or to results needs its pins updated and an independent review.

## Limits

- Not measured: a constant equal to a keyed literal for a claim, which is the design case above.
- The existing `constant-export` controls in the fixtures were not read, and no overlap with them was checked.
- Only the positive control was mutated. Other controls were not mutated.
- The synthetic fixture scoring is not reader execution. No native evidence exists, and benchmark readiness stays false.
- Detection here depends on the key comparison. It is not an independent check on the key itself.
