# Policy working memory

Considered: iteration records 0000–0011; reports #139/#140/#141 (iteration 0011); benchmark/protocol.md at the
prepared checkout 932ec4a. Updated by Policymaker #145, iteration 0012.
Historical inputs: `.session/history/manifest.json`; iteration 0011: `.session/history/records/0011.json`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; it supplies the iteration's work.
- Iteration 0011 ran almost entirely on codex/gpt-6.1-sol (1.12M input) after Claude fallback; three sessions done,
  accepted/improved, `no_progress` 0. Owner accepted #142 (conflict fix) and #143 (protocol draft).
- Routing change in 0012: `reviewer` is now Claude-first (sonnet, then codex, luna) because the reviewed work
  (protocol.md, #141) was authored by codex. `review` and `evaluator-verifier` stay codex-first. When ordering a
  review, check the author's family in the record's `models` and pick the class whose first candidate differs.
- Evaluator --check (per #139 report): exit 0, errors [], 8 evidence refs; missing tasks, oracle, split, baseline,
  challenges. Benchmark readiness false, not executed, tool quality unmeasured.

## Milestone evidence
- sources: review #134 revise → fix #139 → re-review #140 Recommendation accept at d588fa9 (focused correction;
  actor-framework 356 requires + 1 conflict, pylavi 0). Coverage review #133 accept at 6933e17 as limited inventory.
- Both stay prepared-not-reviewed in benchmark/preparation-status.json. How a recommendation becomes `reviewed`
  is undecided; it goes through the owner change gate. Do not mark it from reviews alone.
- protocol.md (#141, 114 lines, unpinned, unreviewed): sections tasks/oracle/split/baseline/challenges plus a
  resources table of 7 rows (restricted store, native cloud jobs, native versions/licenses, private projects,
  new restricted cases, model quota/runner, reviewers/scorer). It states no concrete service is identified yet.

## Orders for iteration 0012
- `review-protocol1` (reviewer, Claude-first, high, 60 min/25 turns): independent method review against
  evaluation.md, goal.md and accepted-limits.md; per resources row, whether it is concrete enough for a
  `capability` request. No parallel development work: it would be built on an unreviewed method.
- Next Policymaker: read the review's recommendation; on revise order a focused benchmark revision then
  re-review; on accept, file `capability` requests only for rows the review called concrete (fields: what,
  frozen owner steps, readiness), and order public development work the protocol lists (case specs, answer/
  citation schema, lineage analysis, native-job input/output records). Ask the owner how a commit-bound review
  recommendation becomes a milestone `reviewed` status if still undecided.

## Mechanisms to preserve
- Input ceiling is 800k unique input; codex counts all non-cached input. Never read large sources.json/
  coverage.json directly; bounded Python summaries. Keep codex sessions short or route Claude-first.
- Task Verification runs in-session and again offline; keep it over committed files. Report-only reviews use
  no command and write report findings from the start (worked in 0010 and 0011).
- After rebase the engine runs evaluator --check; changed pinned files require preparation.json re-pinning.
- Missing git identity: leave changes staged; parent engine commits. Partial predecessors block dependants.
- Requests: `.session/requests.json`, format in `.github/loop/session-protocol.md` ("Three additional kinds").
- Exports contract: `docs/perpetua/session-exports.md`; explicit selectors only. Order format: `.github/loop/task-graph.md`.

## Open questions
- Notices #92/#100 remain pending for the owner. Do not reinstate the crashed script shaper without contract review.
- Fallback variant (LabVIEW 2024) needs an all-version effort estimate before any choice; not yet started.
- cache_read_share 0.053 in 0011 reflects codex sessions; not a Claude transport problem.
