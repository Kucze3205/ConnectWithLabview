# Policy working memory

Considered: iteration records 0000–0010; reports #132/#133/#134 (iteration 0010); commits 6933e17,
bb56af2 and 071efa7; evaluator check at 071efa7. Updated by Policymaker #138, iteration 0011.
Historical inputs: `.session/history/manifest.json`; iteration 0010: `.session/history/records/0010.json`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; it supplies the iteration's work.
- Routing unchanged. Iteration 0010 ran almost entirely on codex/gpt-6.1-sol (1.08M input) after Claude fallback;
  all three sessions finished done within budget. No measured quota comparison justifies a routing change.
- #132 landed sources dependency records (owner acceptance #136). Iteration 0010 accepted/improved; `no_progress` 0.
- At 071efa7, `python3 -I policy/evaluator/evaluate.py --check` exited 0: errors [], 8 evidence refs;
  missing tasks, oracle, split, baseline, challenges. Benchmark readiness false, not executed, tool quality unmeasured.
  Independent method review and owner acceptance remain required before product implementation.

## Review results from iteration 0010
- Coverage review #133: Recommendation accept at 6933e17 as a limited preparation inventory (not full coverage).
  Diff 6933e17→HEAD on coverage.json is only the `sources_json_sha256` field, so the recommendation still applies
  substantively. Gaps it kept: 13 absent extensions, no native version examined, modules/targets/licenses/
  protected diagrams unexamined, one archive level, 829 is the prepared denominator not the goal denominator.
- Sources review #134: Recommendation revise at bb56af2, single finding: sources.py:172-175 stores VIPB
  `Package_Conflicts` as identity `package conflict` with the package name inside version_constraint
  (`zyah_solutions_lib_interface_for_actor_ini >=1.0.1.2`). Six sampled declarations, folder exclusion,
  save/env separation, pins, licenses and original hashes passed.
- Milestone status stays prepared-not-reviewed in preparation-status.json; how a recommendation becomes
  `reviewed` is undecided and goes through the owner change gate. Do not mark it from reviews alone.

## Orders for iteration 0011
- `bench-sources-conflict-fix`: real package identity, constraint, explicit relationship, raw text; re-pin hashes.
- `review-sources3` (blocked by fix): focused re-review of the diff since bb56af2; reuse #134's passing checks.
- `bench-protocol-draft` (parallel): benchmark/protocol.md for tasks/oracle/split/baseline/challenges plus a
  resources table (restricted store, native LabVIEW jobs). Unpinned, unreviewed draft; no status changes.
- Next Policymaker: check fix verification + evaluator exit, review #3 recommendation, and protocol.md resource
  table; then order an independent method review of protocol.md (different family than its author) and file
  concrete `capability` requests for resources it names, per accepted-limits.md, without blocking ready work.

## Mechanisms to preserve
- Input ceiling is 800k unique input. Never read large sources.json/coverage.json directly; bounded Python summaries.
- Task Verification runs in-session and again offline in the engine epilogue; keep it over committed files.
  Report-only reviews use no command. Reviews write report findings from the start (worked in 0010).
- After rebase the engine runs evaluator --check; changed pinned files require preparation.json re-pinning.
- Missing git identity: leave changes staged; parent engine commits. Partial predecessors block dependants.
- Exports contract: `docs/perpetua/session-exports.md`; explicit selectors only. Order format: `.github/loop/task-graph.md`.

## Open questions
- Duplicate task issuance (iteration 0009) did not recur in 0010; no audit ordered.
- Notices #92/#100 remain pending for the owner. Do not reinstate the crashed script shaper without contract review.
- Fallback variant (LabVIEW 2024) needs an effort estimate before any choice; not yet started.
