# Policy working memory

Considered: iteration records 0000–0019; reviews #146/#147; #150 and acceptance #151; #157 and acceptance #161;
re-review #166; reports #170/#172/#175/#179/#180; acceptance #176.
Updated by Policymaker #182, iteration 0020.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
selected reports `.session/history/sessions/<issue>/` (.md; list with python glob, not Glob).

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; without valid orders the iteration fails (0017 failed so).
- Protocol re-review #166 (codex) closed F1/F2 at 2669ec4, overall accept; design review lacked model-family diversity.
- Dev cases (11 public, landed via #175/#176): review #179 (status partial, cause input_budget, but report complete)
  recomputed 1,053/1,053 XML agreements, 0 disagreements, 23 native slots unresolvable; all 11 sha256 matched;
  recommendation "accept as development evidence". Reviewed commit eac73eb. Model mix: sonnet startup, but codex had
  539k of 695k input → model-family diversity NOT confirmed. Recorded as review evidence toward tasks/oracle (dev only,
  literal XML claims); no repo changes from #179. Gaps it named: typedef-impact and diagram-difference cases, VI
  semantic key, native evidence.
- Lineage #180 (partial, input_budget) saved commit d8570a9 (parent eac73eb) NOT on main: lineage.py, lineage.json
  (~47k lines), lineage.md, preparation(.json/-status.json). Claimed 829 artifacts (530 originals/299 members),
  24 exact-dup groups/50 members, 230 candidate groups all unadjudicated, 13 save-version diffs; both checks passed.
- Milestones: sources/coverage/tasks/oracle prepared-not-reviewed (tasks/oracle now have one dev review); split
  not-started (public lineage prepared once landed); baseline/challenges not-started.
- Owner acceptance of the method NOT requested: needs reviewed tasks/oracle/split/baseline/challenge evidence first.

## Iteration 0020 orders (#182, no wake)
- `land-lineage` (benchmark, medium, 45 min/30 turns): `git checkout d8570a9 -- <5 files>`, run lineage.py --check and
  evaluate.py --check. benchmark/ unchanged on main since eac73eb, so conflict-free. Expected: lineage on main.
- `review-lineage` (reviewer, high, 60 min/40 turns): independent rehash of originals/members vs claimed counts,
  split-spec checks, recommendation. Reads d8570a9 via `git show`. Parallel with landing (width 2).

## Next Policymaker
- Check land-lineage merged (lineage.py on main) and its exit codes; check review counts vs 829/24/50 and model used.
- If review says revise: order a benchmark fix of named findings only. If accept: split preparation evidence (split
  stays not-started).
- Reviewer routing lists claude-sonnet first, yet #179 consumed mostly codex input: diversity keeps failing. Consider
  asking the reviewer to report provider explicitly and, if codex keeps taking over, check provider availability.
- Ready later preparation: challenge fixtures on dev cases (protocol `## challenges`), baseline design, typedef-impact
  and diagram-difference dev cases, native-job input/output schema. Restricted store needs owner answers.
- Capability #169 (native jobs) and engine-change #165 remain waiting; do not duplicate or block on them.
- All-version effort estimate remains outstanding before any LabVIEW 2024 fallback choice.

## Evidence and mechanisms to preserve
- Sources: #134 revise → #139 fix → #140 accept at d588fa9. Coverage: #133 accept at 6933e17 as limited inventory.
- Input ceiling 800k: #179 (695k) and #180 (775k) both hit `input_budget` despite bounded orders; codex counts all
  non-cached input. Saved commits make "restore and land" cheap (#175 pattern). Keep budget text, smaller limits,
  and "write report first" in orders.
- Task Verification runs in-session and offline; rebase runs evaluator --check. Changed pinned evidence requires
  preparation.json re-pinning. Parent commits accepted changes.
- Orders: `.github/loop/task-graph.md`; ids unique within an iteration. Requests: `.github/loop/session-protocol.md`.
  Export availability from `.session/exports/manifest.json`.
- Read evaluation.md before reader planning/implementation; accepted-limits.md before private data, disclosure,
  publication or new spending. Optional access must not block ready work.
- Do not reinstate the crashed script shaper without contract review. Notices #92/#100/#158 approved.
- Iteration 0020 first attempt paused (providers:unavailable, resume 2026-11-04T23:16Z); this session is the resume.
