# scorer-finish-0170: finish the #739 zero-execution scorer change

No LabVIEW or native behaviour is claimed. No evaluator, network, model or reader call was made.

## Source

Found, not reimplemented. Candidates checked by `.session/artifacts/find_score.py` (SHA256 of `git show <c>:benchmark/scripts/score.py` against 296e2354e312d5a69fe62e9629bc085376c0fa523fbf21ad6601fdf1dad8def8):

- `d46236b6d1d7acda845684562ae3873e2b29eda8` (#739 commit): 296e2354... MATCH
- tag `iter/0165/739` (peels to the empty commit 5db2610e, but its tree holds the file): 296e2354... MATCH
- `1da24f36...`: 810a5457... (pre-change)
- `a9d0b1ac...`: f0a29079...; `265ad84f...`: 9d4e9433...; `e3c73a94...`: f68e260b...

No `*739*` branch was listed.

## Restored

`benchmark/scripts/score.py` and `benchmark/challenges/scorer-fix-0165.md` from `d46236b6` via `.session/artifacts/restore_score.py`. Restored score.py SHA256 296e2354...; scorer-fix-0165.md b8ce07f2....

Added on top of the restored file (score.py is now c2d20475f7a8009fc55097233f5a6e54dbfc2ef45204172fef50dcbd8855efd3):
- A `native_run` null self-test case with executed and scored both 1 (isolated from the zero cases).
- The self-test baseline no longer calls `compare(baseline, control['expected'])`. The control's `expected` now describes the zero-execution outcome, while the baseline runs with positive execution. It still fails on `cannot_evaluate_reasons`, and a positive-execution outcome comparison remains in the self-test.

## Pins

Re-pinned by exact old-hash replacement in `benchmark/preparation.json`, `benchmark/writing/c1-challenges-0125-pins.json`, `benchmark/writing/input-pins.json` and `benchmark/writing/reviews-0128/c1-artifact-manifest-0126.json`:
- score.py 810a5457... -> c2d20475...
- results/challenges.json a5b97984... -> 1c78ff28...
- library-icon-tests.json ad0413fd... -> 0d77d414...
- library-specialty.json d34933b6... -> e5798d0a...

The final scan reported no stale old hash left in `benchmark/**/*.json`.

## Expectations

Compared fixture `expected` with `generate()`: 5 matches / 28 mismatches. Every mismatch is `unverified` replacing `correct` or `incorrect` (plus matching counts and dimensions), because all controls declare zero execution. `.session/artifacts/update_expect_0170.py` updated only mismatching leaves:
- `library-icon-tests.json`: 26 controls (all except `missing-independent-key`).
- `library-specialty.json`: `positive-control`, `constant-export`.
- `vi-actor-core-native-gap.json`: unchanged (4 controls already matched).

Typical per-control change: about 18-20 `correct -> unverified`, 4 `incorrect -> unverified` in `wrong-citation-*`, counts such as correct `10 -> 0` and unverified `2 -> 12`.

## Checks

- `generate()` after the update: 33 matches, 0 mismatches, 0 cannot_evaluate.
- `main()` ran once successfully (`.session/artifacts/finish_0170.py`) and rewrote `benchmark/results/challenges.json`; `quality_measured` is false.
- Helpers ran under `python3 -I` with faulthandler and stdin on devnull; no stall.
- The first `main()` attempt failed in the self-test baseline compare; fixed as described under Restored, then rerun.
- The final acceptance command and `.session/report.md` were not run or written in this session (Write and Bash became unavailable).
