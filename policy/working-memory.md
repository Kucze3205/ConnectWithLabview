# Policy working memory

Considered: iteration records 0000–0021; reviews #146/#147; #150/#151; #157/#161;
re-review #166; reports #170/#172/#175/#179/#180/#184/#185/#188/#189; acceptances #176/#190.
Updated by Policymaker #192, iteration 0022.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
selected reports `.session/history/sessions/<issue>/` (.md; list with python glob, not Glob).

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; without valid orders the iteration fails (0017 failed so).
- Protocol re-review #166 (codex) closed F1/F2 at 2669ec4, overall accept; design review lacked model-family diversity.
- Dev cases (11 public, on main via #175/#176): review #179 recomputed 1,053/1,053 XML agreements, 23 native slots
  unresolvable; accepted as development evidence only. Gaps: typedef-impact and diagram-difference cases,
  VI semantic key, native evidence.
- Lineage LANDED via #188/#190, commit 8d3403c. `benchmark/scripts/lineage.py` exists on main.
  Review #185 independently rehashed 829 artifacts, 24 duplicate groups/50 members, zero mismatches;
  accept as split preparation evidence only, revise before allocation. Split remains `not-started`.
- Main evaluator check in #192: exit 0, errors [], missing [baseline, challenges], benchmark_ready false,
  benchmark_executed false, tool_quality null. An evidence index does not establish substantive readiness.
- #189 challenge work saved at ecd17c4ccbd8671fcaa0c72451ac4e295ee955cd, unmerged (input_budget), branch task/189.
  Four files: generator and three JSON fixtures; despite the report, no README was committed.
  #192 inspected the generator: it submits only 2 of 50/141 required claims yet expects correct positive controls;
  mutations are descriptions rather than materialized records; no per-required-ID expected ledger.
  Thus repair before pinning/review/scorer work. Do not land the saved files unchanged.
- Owner acceptance of the method NOT requested: needs reviewed split/baseline/challenge evidence first.
  No reader implementation or planning before the evaluation protocol and independent review/owner gate.

## Model diversity and resource evidence
- Do not trust report/startup model labels; inspect each record's `models` block.
- #179/#185 reviewing diversity doubtful: authors used codex, most review input used codex or copilot luna (GPT family).
- Iteration 0021: #188 accepted using 27,554 input; #189 partial using 460,178 input in 18 turns.
  Both started Sonnet but overwhelmingly used copilot/gpt-5.6-luna; #189 stopped at input_budget.
  No measured subscription-quota figures justify a routing change yet. Cache/input-budget accounting is not quota use.
  Keep tasks small, bounded reads, checkpointing. Prefer another model family for independent review when available.

## Iteration 0022 orders (#192, wake true)
- `challenge-fixtures-2` (benchmark, high, 60 min/30 turns, start_branch task/189): repair saved fixtures,
  favor library-icon-tests/library-specialty (12 IDs each) plus native-gap VI; materialize actual submissions,
  freeze per-ID outcomes and ledgers, generate README with protocol-row coverage/gaps, pin challenges and
  mark prepared-not-reviewed. Verification runs generator --check and evaluator --check without environment.
- Expected gain: reviewable public development fixtures; main evaluator no longer lists challenges missing.
  No scorer, challenge execution, readiness, scope restriction or product work authorized by this order.

## Next Policymaker
- Wake after the repair task: read its report, actual model usage and Verification outcome. Check main vs saved branch.
- Inspect denominator-correct positive controls, actual mutation records, per-ID ledgers and README coverage/gaps.
  Generation/byte equality cannot establish semantic correctness. Fidelity still lacks native reference alignment.
- If landed and reviewable: order independent review before evaluator/scorer work; prefer a different model family,
  verify actual model usage. Scorer changes require evaluator role plus separate verifier on policy-layer orders.
- If budget stop: use saved commit, read the exact failure and restore/repair only missing work; avoid repeating reads.
- Ready later: baseline design (manifest and development-only precision/cost plan), typedef-impact and diagram-difference
  dev cases, native-job input/output schema. Resource-dependent execution waits for verified readiness.
- Capability #169 (native jobs) and engine-change #165 remain waiting; do not duplicate or block ready work on them.
- All-version effort estimate remains outstanding before any LabVIEW 2024 fallback choice.

## Evidence and mechanisms to preserve
- Sources: #134 revise → #139 fix → #140 accept at d588fa9. Coverage: #133 accept at 6933e17 as limited inventory.
- Input ceiling 800k: #179/#180/#185/#189 hit input_budget. Keep smaller limits, bounded JSON inspection,
  write report first and checkpoint commits. Public case JSON ranges from ~11k to ~445k serialized characters.
- Task Verification runs in-session AND in an engine epilogue WITHOUT LABVIEW_ENVIRONMENT (#184 failed there).
  Use environment-free generator/evaluate.py checks in Verification. Rebase runs evaluator --check.
- Changed pinned evidence requires preparation.json re-pinning, including every reference to preparation-status.json.
  Parent commits accepted changes.
- Orders: `.github/loop/task-graph.md`; ids unique within iteration. Requests: `.github/loop/session-protocol.md`.
  Check `.session/exports/manifest.json` before relying on exported artifacts; no exports requested this iteration.
- Read evaluation.md before reader planning/implementation; accepted-limits.md before private data, disclosure,
  publication or new spending. Optional access must not block ready work.
- Do not reinstate the crashed script shaper without contract review. Notices #92/#100/#158 approved.
