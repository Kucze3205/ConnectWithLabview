# Policy working memory

Considered: iteration records 0000-0008 (`.session/history/records/`), session reports #109-#112, #117
(`.github/loop/data/session-reports/`), `policy/evaluator/evaluate.py`, `benchmark/preparation.json`,
`.github/loop/loop.py:427-445,802-809`, `.github/loop/task-graph.md`. Updated by Policymaker session #121
(start of iteration 0009).

## Current organization
- `shaper: null`. The Policymaker's `.session/orders.json` is the iteration's only work. Never end a session
  without it while `shaper: null`. `every_iterations: 1` (commit `9bc8016`).
- Routing (`policy/params.yml`): `benchmark` Claude-first; reviewer/audit codex-first (other family than the work).
- Benchmark state on main: `sources: prepared-not-reviewed`, others `not-started`, `independent_review: pending`,
  `native_labview: not executed`. Readiness not established. `evaluate.py --check` on main (checkout 66ff557):
  exit 0, 4 evidence refs, missing all except `sources`.

## Key mechanisms
- Input budget: a session stops `partial/input_budget` at 800k unique input. Keep orders small.
- **`## Verification` runs twice: in-session and in the engine epilogue without `LABVIEW_ENVIRONMENT`**
  (`loop.py:802-809`). Verification must be offline over committed files; environment-dependent checks go into
  Acceptance. Report-only reviews: no backticked command.
- **After rebase the engine also runs `python3 policy/evaluator/evaluate.py --check`.** `benchmark/preparation.json`
  pins sha256 per evidence file (max 2 MB each); any change to a pinned file without re-pinning rejects the session.
  #117 (iteration 0008) lost a correct coverage restore this way (preparation-status.json is pinned under
  `sources`). Fixed in #121: `execution/roles/benchmark/SKILL.md` now requires re-pinning + running the check;
  orders' Verification now also asserts all pinned hashes match.
- Sessions have no git identity; `git commit` fails (exit 128). Changes are left staged; the engine commits.
- Blocked successors: when a predecessor ends `partial`, dependants end `blocked` with 0 tokens (#118, #119).
- Duplicate issuance (0005/0006) did not recur in 0008.

## Iteration 0006/0008 results
- Coverage: finished result is commit `0285248` (no branch, object store); `coverage.json` 1,776,486 bytes (<2 MB).
- Sources review: #110 and #112 -> `Recommendation: revise at 52d2aa1`; sole finding: per-source dependency
  identities/constraints missing (`benchmark/sources.md:41,48`).

## Iteration 0009 decision (session #121)
- `bench-coverage-land2` (benchmark, 30 turns): restore `0285248`, re-pin `preparation.json` (sources hash of
  preparation-status.json; new coverage refs). Expect on main: `evaluate.py --check` exit 0, `coverage` not missing,
  `coverage: prepared-not-reviewed`.
- `bench-sources-deps` (benchmark, 45 turns, after land): per-repository `dependencies` in `sources.json`, re-pin.
  Expect every repository to carry a non-empty `dependencies` object; then order a sources re-review.
- `review-coverage` (reviewer, 15 turns, after land): expect `Recommendation: ... at <commit>` in its report.
- If land2 fails again, read its report's check output before re-ordering; do not reissue blindly.

## Open questions
- How a review verdict moves a milestone to `reviewed` (owner change gate per evaluation.md) is undecided.
- Script shaper crash (0004, #99): do not reinstate without checking the script-role contract.
- Notices #92 and #100 remain pending for the owner.
- `no_progress` is 9 (engine stalls at 10, `engine_params.no_progress_iterations`); `improved` stays false because
  the evaluator only returns `inconclusive`/`rejected` in this phase. Check whether a stall notice follows 0009.
