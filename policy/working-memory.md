# Policy working memory

Considered: iteration records 0000–0017; reviews #146/#147; #150 and acceptance #151; #157 and acceptance #161;
re-review #166; reports #170/#172; saved commit d0e14f68458acfe7bab0327ad33d15529480ce44.
Updated by Policymaker #174, iteration 0018.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
selected reports `.session/history/sessions/<issue>/`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; without valid orders the iteration fails. Iteration 0017
  failed for this reason after #172 exhausted its input budget before ordering work.
- Protocol re-review #166 (codex/gpt-6.1-sol, report d35c2aac) closed F1/F2 at 2669ec4, overall accept.
  Author #150 also used codex; this is a design review without model-family diversity. Prefer Claude for case review,
  but report actual fallback models rather than claiming independence from routing alone.
- Main still has sources/coverage prepared-not-reviewed; tasks/oracle/split/baseline/challenges not-started.
  Benchmark readiness remains false, coverage incomplete, product quality unmeasured.
- Owner acceptance of the method has NOT been requested: evaluation.md requires substantive tasks/oracle/split/
  baseline/challenge evidence first. Accepted design changes do not accept the method or authorize product work.

## Saved work and recovery order
- #170 (iteration 0016) ended partial on input_budget: 904,013 input tokens, 22 turns; most input was codex fallback.
  Its report is stale: it says preparation remains to be implemented, but commit d0e14f6 contains a 332-line generator,
  11 JSON cases, README and updated preparation manifests. The commit is available but not merged; no branch currently
  contains it (`git branch -a --contains d0e14f6` returned empty). Do not assume task/170 still resolves.
- Saved cases: 3 .lvproj, 3 .lvclass, 4 .lvlib, 1 .vi native-gap. README declares 1,053 XML slots and 23 native-required
  slots; these are author-reported inventories, not independently verified results. Every native reference is unavailable.
  Files are 12–544 KB, total roughly 2.4 MB; do not print whole JSON files.
- #172 (iteration 0017) also ended partial on input_budget (866,953 input tokens, 22 turns), with no orders or policy changes.
- Iteration 0018 order `order-174-land-dev-cases`: benchmark restores only the saved benchmark paths from d0e14f6,
  runs generator --check and evaluator --check, fixes concrete failures within budget, and reports exit codes plus
  bounded spot-checks. Expected gain: verified development evidence available for independent review without rebuilding it.
  No wake requested. Tasks/oracle remain prepared-not-reviewed; do not claim readiness from passing checks.
- Startup #174: 12,285 estimated tokens against 100,000 warning, status ok. Later reads and cumulative provider input
  caused previous failures; startup diagnostics alone do not measure those costs.

## Next Policymaker
- Read the recovery report and accepted commit. If complete, order independent review of generator, cases and original
  evidence against protocol tasks/oracle, preferably a different model family from the actual author.
- If partial, inspect saved commit and actual continuation state before ordering only unfinished work. A partial label
  does not prove a successor is running or that files were not written.
- Verify capability #169 readiness before any native-reference work. Request remains pending; do not duplicate it or
  hold the iteration open. Engine-change #165 (tokenless policy-script failures) also remains pending.
- Ready later preparation: challenge fixtures, lineage/duplicate analysis for split, native-job input/output schema.
  Restricted-store proposal needs owner answers on store/custodian before private split work.
- All-version effort estimate remains outstanding before any LabVIEW 2024 fallback choice.

## Evidence and mechanisms to preserve
- Sources: #134 revise → #139 fix → #140 accept at d588fa9. Coverage: #133 accept at 6933e17 as limited inventory.
  Milestones stay prepared-not-reviewed; method acceptance still requires the owner's existing change gate.
- Input ceiling 800k: codex counts all non-cached input. Keep sessions short; bounded Python summaries for case JSON,
  sources.json and coverage.json. Reports should be written early and updated with verification results immediately.
- Task Verification runs in-session and offline over committed files; rebase runs evaluator --check.
  Changed pinned evidence requires preparation.json re-pinning. Parent commits accepted changes.
- Orders: `.github/loop/task-graph.md`; ids unique within an iteration. Requests: `.github/loop/session-protocol.md`.
  Export availability comes from `.session/exports/manifest.json`; absence is not evidence of no historical work.
- Read evaluation.md before reader planning/implementation; accepted-limits.md before private data, disclosure,
  publication or new spending. Optional access must not block ready work.
- Do not reinstate the crashed script shaper without contract review. Duplicate sessions occurred in 0012/0014;
  collect fresh evidence before proposing an engine change. Notices #92/#100/#158 are approved in current loop state.
