# Policy working memory

Considered: iteration records 0000-0004 (`.session/history/records/`), Policymaker reports #78, #87, #91, #94, #98,
planner session #99, git log up to `abf90c5`. Updated by Policymaker session #102 (start of iteration 0005).

## Current organization
- `shaper: null` (restored by rollback `6a324a2`, which removed `execution/planner.py` and the planner profile).
  The Policymaker's `.session/orders.json` is the iteration's only work. Never end a session without it while
  `shaper: null` (iterations 0001-0003 failed that way).
- Benchmark state (HEAD `benchmark/preparation-status.json`): `sources: prepared-not-reviewed`, other six milestones
  `not-started`, `independent_review: pending`, `native_labview: not executed`. Readiness not established.

## History in brief
- 0000: orders review-sources (#79, codex, 60/60 turns, wrote nothing) + bench-coverage (blocked, never ran).
- 0001-0003: Policymaker sessions ended `partial` (input/session budget) before writing orders; no tasks; failed.
  Two partial sessions in a row rolled `policy/` back (notice #92).
- 0004: script shaper `planner` (commit `45c8062`) crashed with 0 turns, report "Script failed (exit )"
  (`.session/history/sessions/99/`); `policy/` and `execution/` rolled back (notice #100). Cause unknown.

## Iteration 0005 decision (session #102)
- Ordered directly, no wake: `review-sources` (reviewer) and `bench-coverage` (benchmark), independent, 100 turns
  each, artifact written first. Same bodies the planner would have emitted.
- Expected: `.session/artifacts/review-sources.md` with a verdict naming the reviewed commit;
  `python3 -I benchmark/scripts/coverage.py --check` exits 0 and `coverage: prepared-not-reviewed`.

## Open questions
- Why did the script shaper crash with an empty exit code? Do not reinstate it until the engine's script-role
  contract (`.github/loop/task-graph.md`, `docs/perpetua/engine.md`) is checked; an `engine-change` or a fix may be needed.
- How a review verdict moves a milestone to `reviewed` (owner change gate per evaluation.md) must be decided before
  ordering the next review.
- Notices #92 and #100 remain pending for the owner.
