# Policy working memory

Considered: iteration records 0000–0020; reviews #146/#147; #150 and acceptance #151; #157 and acceptance #161;
re-review #166; reports #170/#172/#175/#179/#180/#184/#185; acceptance #176.
Updated by Policymaker #187, iteration 0021.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
selected reports `.session/history/sessions/<issue>/` (.md; list with python glob, not Glob).

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; without valid orders the iteration fails (0017 failed so).
- Protocol re-review #166 (codex) closed F1/F2 at 2669ec4, overall accept; design review lacked model-family diversity.
- Dev cases (11 public, on main via #175/#176): review #179 recomputed 1,053/1,053 XML agreements, 23 native slots
  unresolvable; "accept as development evidence" (dev only). Gaps: typedef-impact and diagram-difference cases,
  VI semantic key, native evidence.
- Lineage: #180 saved d8570a9 (NOT on main). #184 restored it, all in-session checks exit 0 (829 artifacts, 530/299,
  24 dup groups/50 members, 230 candidates, 13 version diffs), but the engine epilogue re-ran
  `lineage.py --check` WITHOUT `LABVIEW_ENVIRONMENT` → fail → not merged (commit 2e9ccf1 on task/184 identical).
  LESSON: `## Verification` must not need LABVIEW_ENVIRONMENT; the epilogue lacks it. Use evaluate.py-based checks.
- Review #185 of d8570a9: independent rehash 829/0 mismatches, 24/50 exact match; "accept as split preparation evidence
  only; revise before allocation". Recorded as split preparation review. Artifact recompute_lineage.py (iter-0020).
- Milestones on main: sources/coverage/tasks/oracle prepared-not-reviewed (tasks/oracle have dev review #179);
  split/baseline/challenges not-started. evaluate.py --check on main: missing split, baseline, challenges.
- Owner acceptance of the method NOT requested: needs reviewed split/baseline/challenge evidence first.

## Model diversity (open)
- #179 and #185 reports claim claude-sonnet, but token records show most input on codex (#179) or
  copilot/gpt-5.6-luna (#185, 387k of 388k input). Authors were codex/gpt-6.1-sol. Luna is also GPT family, so
  diversity of #185 is doubtful; session reports misstate the reviewing model (they see only startup model).
  Iteration 0020 ran mostly on copilot luna: claude likely quota-limited. Do not trust self-reported model; use
  the record's `models` block. Consider an audit of provider fallback once claude is available again.

## Iteration 0021 orders (#187, no wake)
- `land-lineage-2` (benchmark, low, 30 min/20 turns): restore 5 files from d8570a9; Verification via evaluate.py
  --check requiring no errors and `split` not in missing. Expected: lineage on main.
- `challenge-fixtures` (benchmark, high, 60/40): `benchmark/scripts/challenges.py` + `benchmark/challenges/`
  fixtures from 2-3 dev cases covering every protocol challenge row, frozen expected outcomes, explicit gaps; no
  scorer, no preparation.json/status edits (pinning pending). Parallel with landing.

## Next Policymaker
- Check lineage.py on main and evaluate.py missing list. If landing failed again, read the epilogue error.
- If fixtures landed: order pinning + challenges status `prepared-not-reviewed`, and an independent review
  (prefer a non-GPT family if available, check the record's `models`). Then consider an evaluator order for a
  scorer exercised on these fixtures (evaluator + verifier, policy layer).
- Ready later: baseline design (manifest, repetitions plan from dev pilots), typedef-impact and diagram-difference
  dev cases, native-job input/output schema. Restricted store needs owner answers.
- Capability #169 (native jobs) and engine-change #165 remain waiting; do not duplicate or block on them.
- All-version effort estimate remains outstanding before any LabVIEW 2024 fallback choice.

## Evidence and mechanisms to preserve
- Sources: #134 revise → #139 fix → #140 accept at d588fa9. Coverage: #133 accept at 6933e17 as limited inventory.
- Input ceiling 800k: #179 (695k), #180 (775k), #185 (input_budget at 388k counted) hit `input_budget`; keep budget
  text, smaller limits, "write report first" and "commit as you go" in orders. Saved commits make restore cheap.
- Task Verification runs in-session AND in an engine epilogue without LABVIEW_ENVIRONMENT; rebase runs evaluator
  --check. Changed pinned evidence requires preparation.json re-pinning. Parent commits accepted changes.
- Orders: `.github/loop/task-graph.md`; ids unique within an iteration. Requests: `.github/loop/session-protocol.md`.
  Export availability from `.session/exports/manifest.json`.
- Read evaluation.md before reader planning/implementation; accepted-limits.md before private data, disclosure,
  publication or new spending. Optional access must not block ready work.
- Do not reinstate the crashed script shaper without contract review. Notices #92/#100/#158 approved.
