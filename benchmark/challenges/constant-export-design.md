# Constant/empty export probe design

Question: does benchmark/scripts/score.py reject (a) an empty export and (b) a constant export on the synthetic challenge fixtures? No LabVIEW behaviour is claimed. Benchmark readiness stays false. This is a report, not a scorer fix.

## Measured

Repo HEAD 692825640aab4d81045a6b3095c418204e8b932d. Helper: `.session/artifacts/constant_probe.py` (guarded exec of score.py, main() never run, nothing written). Output: `.session/artifacts/constant-probe-output.txt`. Mutations were applied in memory to each fixture's positive control, with raw JSON text and SHA256 kept consistent and execution forced to attempted/executed/planned/scored = 1. The constant export replaces every claim `answer` and every observation `value` with the string `CONSTANT`. The empty export sets claims and observations to `[]`.

| Fixture | Probe | Verdict | Result (3 dimensions) | Deciding line in score.py |
|---|---|---|---|---|
| library-icon-tests | empty export | DETECTED | `missing` x3, 0 correct of 12 | line 204 (`elif not records: common = 'missing'`) |
| library-icon-tests | constant export | DETECTED | `incorrect` x3, 0 correct of 12 | line 208 (`elif any(v != target for v in values): common = 'incorrect'`) |
| library-specialty | empty export | DETECTED | `missing` x3, 0 correct of 12 | line 204 |
| library-specialty | constant export | DETECTED | `incorrect` x3, 0 correct of 12 | line 208 |
| vi-actor-core-native-gap | empty export | NOT-APPLICABLE | `unsupported` x3, identical to baseline | line 200 (`status == 'unsupported' and not records`) |
| vi-actor-core-native-gap | constant export | NOT-APPLICABLE | `unsupported` x3, identical to baseline | line 200 |

For the positive-control baseline, both library fixtures score 10 of 12 `correct` per answer dimension, with the dimension verdict `unverified`. So the two probes are separated from a correct export by their per-id outcomes.

The vi-actor-core-native-gap controls hold no claims or observations to mutate and declare status `unsupported`. The scorer returns `unsupported` whatever is exported, so the probe cannot distinguish anything there.

Both library fixtures already carry a control named `constant-export` (library-icon-tests, library-specialty at line 1328). This probe did not read or run those controls. It only confirms that the scoring path rejects an in-memory constant on its own.

## Design

Proposed fixture shape, for the next shaper to order and review:
- Add two named controls per library fixture, `empty-export` and `constant-export-all`. Each has an expected block of per-id `missing` (empty) or `incorrect` (constant), with a dimension verdict and zero `correct` counts. `compare()` then pins the outcome in results/challenges.json.
- Add a regression self-test mutation in `regression_self_test` that fails the run if either probe yields any `correct` or `partial` per-id outcome. The current mutations (lines ~307-330) cover extra-condition, missing-condition, wrong-literal, missing-claim and wrong-citation, but not a whole-export empty or constant case.
- Expected scorer outcome: empty gives `missing` for every required id. Constant gives `incorrect` for every required id. Neither earns credit even with positive execution.
- A stronger probe, still unmeasured: a constant that equals the literal target of exactly one required id. Expect `correct` for that id only, with the other ids `incorrect`, so a constant cannot pass more than the ids whose key equals it.

## Limits

- The probes were synthetic and in memory. No LabVIEW, native reader or real agent export was involved.
- Only the positive control of each fixture was mutated. Other controls (for example `empty-probe`) were not re-run here.
- The constant value `CONSTANT` is not a key literal. A constant that happens to match a key literal was not tested.
- `dimensions` stays `unverified` for the baseline because the XML key is provisional and unreviewed, so DETECTED here means "earns no per-id credit", not "scorer is validated".
- The scorer remains an unreviewed same-role-family implementation. Benchmark readiness stays false.
