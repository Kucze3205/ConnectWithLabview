# Policy working memory

Considered: iteration records 0000-0005 (`.session/history/records/`), Policymaker reports #78-#102,
sessions #99, #103-#106, `.github/loop/role_runtime.py`, git up to `0350fd9`. Updated by Policymaker session #108
(start of iteration 0006).

## Current organization
- `shaper: null`. The Policymaker's `.session/orders.json` is the iteration's only work. Never end a session
  without it while `shaper: null` (iterations 0001-0003 failed that way).
- Routing (`policy/params.yml`): `benchmark` now Claude-first (`*implementation`); reviewer/audit stay codex-first
  so review runs on another family than the work.
- Benchmark state (HEAD `benchmark/preparation-status.json`): `sources: prepared-not-reviewed`, other milestones
  `not-started`, `independent_review: pending`, `native_labview: not executed`. Readiness not established.

## Key mechanism (why sessions stop `partial`)
- `role_runtime.py`: a session stops `partial/input_budget` when unique input >= 800k tokens (`CONTEXT`).
  For codex/copilot, unique input = `in - cache_read`; for claude, `in` already excludes cache reads.
  Every turn resends the whole history, so cost grows quadratically with turns.
- Iteration 0005, all codex: #103 reviewer 12 turns/855k, #104 benchmark 28 turns/947k, #106 benchmark 26 turns/883k,
  cache_read share 5%. All `partial`, nothing merged. #105 crashed with 0 turns.
- Consequence: codex sessions get ~12-28 turns. Orders must be small, write early, and Finish well before that.

## Iteration 0006 decision (session #108)
- `bench-coverage` (benchmark, Claude-first, 40 turns): restore commit `c6830d1` (coverage.py, coverage.json 83k lines,
  coverage.md from #104), verify, set status, finish. Expected: `python3 -I benchmark/scripts/coverage.py --check`
  exits 0 on the main line and `coverage: prepared-not-reviewed`.
- `review-sources` (reviewer, codex, 12 turns): sources row only; expected `.session/artifacts/review-sources.md`
  ending with `Recommendation: ... at <commit>` and status `done`.
- Measure: Claude benchmark turns/unique input vs codex in 0005, to decide routing for later benchmark tasks.

## Open questions
- Was `c6830d1` reachable for the next session? It is in the object store of this checkout but on no branch.
  If the benchmark session reports it missing, ask for an `engine-change`: merge or preserve partial branches.
- Each order of 0005 was issued twice (issues 103/105, 104/106, same ids, pass 1). Cause unknown; check 0006 record.
- #103's partial artifact is in release `iter-0005/103-review-sources.md`; not reachable as an order input.
- Script shaper crash (0004, session #99): do not reinstate without checking the script-role contract.
- How a review verdict moves a milestone to `reviewed` (owner change gate per evaluation.md) is undecided.
- Notices #92 and #100 remain pending for the owner.
