# Policy working memory

Considered: iteration records 0000-0007 (`.session/history/records/`), session reports #109-#112
(`.github/loop/data/session-reports/`), `.github/loop/loop.py:427-445,802-809`, `.github/loop/task-graph.md`,
git up to `7500e77`. Updated by Policymaker session #116 (start of iteration 0008).

## Current organization
- `shaper: null`. The Policymaker's `.session/orders.json` is the iteration's only work. Never end a session
  without it while `shaper: null`. Iteration 0007 failed because `every_iterations: 5` skipped the Policymaker;
  commit `9bc8016` set it to 1 (fixed).
- Routing (`policy/params.yml`): `benchmark` Claude-first; reviewer/audit codex-first (other family than the work).
- Benchmark state on main: `sources: prepared-not-reviewed`, others `not-started`, `independent_review: pending`,
  `native_labview: not executed`. Readiness not established.

## Key mechanisms
- Input budget: a session stops `partial/input_budget` at 800k unique input (`role_runtime.py`). Codex counts
  `in - cache_read`, Claude excludes cache reads. Keep orders small; Claude-first gives ~20 turns at ~300k.
- **`## Verification` runs twice: in-session (environment present) and in the engine epilogue in the tokenless job,
  which has NO `LABVIEW_ENVIRONMENT`** (`loop.py:802-809`). `sources.py --check` / `coverage.py --check` need the
  environment, so they always fail in the epilogue -> `partial`, nothing merges after fix rounds. Iteration 0006
  lost all four sessions this way (#109-#112 `verification: fail`). Rule: an order's `## Verification` must be an
  offline check over committed files (e.g. `python3 -I -c` JSON assertions); environment-dependent checks go into
  Acceptance as in-session steps with reported exit codes. Report-only reviews: no backticked command at all.
- Each order of 0005 and 0006 was issued twice (109/111, 110/112: same id, pass 1). Duplicate sessions both ran;
  cause still unknown. If 0008 repeats it, consider an `engine-change` request with the record as evidence.

## Iteration 0006 results
- Coverage: #109 and #111 restored `c6830d1` correctly; finished result is commit `0285248` (no branch, in object store).
- Sources review: #110 and #112 independently -> `Recommendation: revise at 52d2aa1`; sole finding: dependency
  identities/constraints missing per source (`benchmark/sources.md:41,48`). Everything else checked (523 hashes).

## Iteration 0008 decision (session #116)
- `bench-coverage-land` (benchmark, 30 turns): restore `0285248`, offline Verification. Expect `coverage:
  prepared-not-reviewed` on main.
- `bench-sources-deps` (benchmark, 45 turns, after land): per-repository `dependencies` in `sources.json`, unknowns
  explicit. Expect every repository to carry a non-empty `dependencies` object; then order a sources re-review.
- `review-coverage` (reviewer, 15 turns, after land): expect `Recommendation: ... at <commit>` in its report.

## Open questions
- How a review verdict moves a milestone to `reviewed` (owner change gate per evaluation.md) is undecided.
- Script shaper crash (0004, #99): do not reinstate without checking the script-role contract.
- Notices #92 and #100 remain pending for the owner.
