# Policy working memory

Considered: iteration records 0000–0022; reviews #146/#147/#166/#179/#185;
reports #150/#157/#170/#172/#175/#180/#184/#188/#189/#193/#195/#196/#197;
acceptances #151/#161/#176/#190 and current loop-state #200.
Updated by Policymaker #200, iteration 0023.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
selected reports `.session/history/sessions/<issue>/` (.md; list with python glob).

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; without valid orders the iteration fails (0017 failed so).
- Protocol re-review #166 (codex) closed F1/F2 at 2669ec4, overall accept; design review lacked model-family diversity.
- Dev cases (11 public, landed via #175/#176): #179 recomputed 1,053/1,053 XML agreements;
  23 native slots unresolvable. Development evidence only; typedef-impact, diagram-difference,
  VI semantic key and native evidence remain gaps.
- Lineage landed via #188/#190, commit 8d3403c. #185 rehashed 829 artifacts,
  24 duplicate groups/50 members, zero mismatches; accepted as split preparation only,
  revise before allocation. Split remains not-started despite pinned lineage references.
- Owner acceptance of the method has NOT been requested: reviewed split/baseline/challenge evidence remains needed.
  No reader planning or implementation before independent method review and owner acceptance of pinned protocol/evidence.
  Goal gate remains unaccepted; no quality measurement or benchmark readiness established.

## Saved challenge work: recover #195, do not repeat repair
- Iteration 0022 ran four partial sessions from the same stale task/189 starting point:
  #193 d58d58f, #195 fbcdb75, #196 a09009e, #197 dfa289a. None merged.
  All four commits are available locally and retained under origin tags `iter/0022/<issue>`.
  Remote task branches 193/195/196/197 are deleted; task/189 still points to ecd17c4.
  Task-graph contract resolves deleted task/N branches through their retained iteration tags.
- #195 is the useful completed checkpoint: `fbcdb75e5687955c0cda49bd1f40014b1647e726`,
  tag `iter/0022/195`. Its report records 33 materialized controls, 1,080 required ledger slots,
  generated README, preparation pins, passing Verification and six no-write drift trials.
  This is author-reported structural verification, not independent semantic acceptance.
- #200 inspected #195's README: two libraries freeze 12 IDs each (10 XML plus 2 unavailable native);
  VI freezes 3 native IDs. Native answers stay null and whole positive outcomes unverified.
  Fidelity lacks native alignment; computation/typedef-impact and full partial-case demonstrations remain gaps.
  Inputs are synthetic public development fixtures, unexecuted, without scorer or concrete reader adapter.
- #195 descends from pre-lineage ecd17c4. A whole-tree restore would delete landed lineage.
  `git merge-tree` against current main 1d6b97b conflicts only in preparation.json and preparation-status.json.
  Preserve main's split references/limitations while adding #195's challenges and refreshing status hashes.
  Remove tracked benchmark/scripts/__pycache__/challenges.cpython-312.pyc.
- #195 evaluator missing [split, baseline] reflects its old branch; main already pins lineage under split.
  Expected after integration: missing [baseline], still benchmark_ready false and quality unmeasured.
  Evidence-index completeness cannot establish substantive readiness.

## Iteration 0023 order (#200, wake true)
- `.session/orders.json`: `land-challenges-195`, benchmark/medium, 40 minutes/25 turns,
  start_branch task/195 (retained tag fallback). Merge origin/main, resolve only the two preparation JSONs,
  preserve lineage bytes and split entries, remove bytecode, run environment-free generator/evaluator checks.
  Do not redesign or alter fixtures/generator/README; stop with exact evidence if checks fail.
- Expected gain: reviewable challenge preparation on main alongside lineage; evaluator missing only baseline.
  No scorer, reader work, challenge execution, readiness, threshold or scope change authorized.

## Next Policymaker
- Wake after landing: inspect report, actual model usage, Verification and landed-vs-saved state.
  Check preservation of lineage, split pins/limitations, challenge hashes and removal of bytecode.
- If landed, order independent substantive challenge review: original locators, frozen denominators,
  mutation records, per-ID outcomes, extras/duplicates/contradictions and README gaps.
  Prefer Claude family because #195 authorship was predominantly codex; confirm actual usage afterward.
  Generator equality does not establish semantic correctness or positive-control validity.
- Scorer work follows review and requires evaluator role plus separate policy-layer verifier.
- If partial, resume the newest saved checkpoint; never restart repair from task/189 by default.
  Each wake must inspect the result before issuing another order; do not repeat identical stale-branch orders.
- Ready later: baseline design, typedef-impact/diagram-difference development cases, native-job schemas.
  Resource-dependent execution waits for verified readiness. All-version effort estimate remains outstanding
  before choosing any LabVIEW 2024 fallback.
- Capability #169 remains waiting for explicit capability-ready; do not duplicate or block ready work on it.
  Engine-change #165 is approved/engine-applied according to current loop-state; earlier memory was stale.

## Model and resource evidence
- Inspect record `models` blocks; startup/report labels are insufficient.
- Iteration 0022: four partial tasks, 2,642,518 input tokens, no merged output;
  #193 input_budget, #195 session_budget, #196/#197 input_budget (see record 0022 and selected reports).
  #195 achieved passing checks but subsequent tasks restarted from task/189, wasting saved progress.
  Recover checkpoints and bound reads before changing routing. No measured subscription-quota figures
  justify provider ranking changes; cache/input accounting is not subscription quota use.
- #179/#185 diversity doubtful: authors used codex, reviews largely codex/copilot (GPT family).

## Evidence and mechanisms to preserve
- Sources: #134 revise → #139 fix → #140 accept at d588fa9; #133 coverage accepted at 6933e17 as limited inventory.
- Input ceiling 800k: use bounded JSON summaries; never print whole case JSON, lineage, sources or coverage.
  Write reports early and checkpoint completed work. Startup #200: 12,612 estimated tokens, status ok.
- Verification runs in-session AND engine epilogue without LABVIEW_ENVIRONMENT (#184 failed there).
  Use environment-free checks. Changed evidence requires preparation.json repinning, including every status reference.
  Parent commits accepted changes.
- Orders: `.github/loop/task-graph.md`; request formats: `.github/loop/session-protocol.md`.
  Check `.session/exports/manifest.json` before relying on exported artifacts; no exports requested for landing.
- Read evaluation.md before reader planning/implementation; accepted-limits.md before private-data use,
  disclosure, publication or new spending. Optional access requests must not hold an iteration open.
- Do not reinstate the crashed script shaper without contract review. Notices #92/#100/#158 approved.
