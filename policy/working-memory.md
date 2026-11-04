# Policy working memory

Considered: iteration records 0000–0012; review reports #146/#147 (iteration 0012); benchmark/protocol.md as
reviewed at a595009. Updated by Policymaker #149, iteration 0013.
Historical inputs: `.session/history/manifest.json`; iteration 0012: `.session/history/records/0012.json`;
reports: `.github/loop/data/session-reports/<issue>/*.json`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; it supplies the iteration's work.
- Iteration 0012: one order (`order-145-review-protocol1`) became two sessions #146 and #147 (same id, both
  reviewer, both done). Both ran on codex/gpt-6.1-sol after Claude fallback despite Claude-first `reviewer`
  routing, ~400k codex input each (796k total). Cause of the duplicate unknown; watch whether it recurs.
- Both reviews: Recommendation **revise** at a595009 (protocol unchanged since cf38154). Shared finding
  F1/S1: no frozen required-claim accounting / dimension outcome rules / denominators (tasks 26–30, baseline
  72–76, challenges 85–92). #147 adds F2: no reader-observation contract (fixed probes, raw outputs, native
  alignment, missing/unsupported/error outcomes). Rest of the method judged consistent with evaluation.md.
- Resources table (lines 103–109): neither review found any of the 7 rows concrete enough for a `capability`
  request; each needs named resources, recipient providers, access/publication/revocation and readiness terms.
  Ordinary public review needs no new access.
- Caveat: both reviews are codex, same family as the protocol author (#141). The re-review of the revision
  should be Claude if the revision is done by codex, and vice versa (check the record's `models`).
- Evaluator --check: exit 0, 8 evidence refs, tasks/oracle/split/baseline/challenges missing; not readiness.

## Orders for iteration 0013
- `revise-protocol-f1f2` (benchmark, Claude-first, high, 60 min/30 turns, exports reports 146/147): focused
  F1+F2 edit of benchmark/protocol.md; verification evaluator --check.
- No parallel re-review: the revision reaches main only after owner merge-acceptance, so a blocked review
  in the same iteration would read the old text.
- Next Policymaker: if the revision is accepted/merged, order an independent re-review (family other than the
  revision's author) focused on F1/F2 plus a regression look. If it failed or stayed partial, read its report
  and narrow the task. Then: concrete resource proposals (native-job runner, restricted store) as a separate
  benchmark/research task before any `capability` request. Ask the owner how a commit-bound review
  recommendation becomes milestone `reviewed` status if still undecided.

## Milestone evidence
- sources: review #134 revise → fix #139 → re-review #140 accept at d588fa9. Coverage review #133 accept at
  6933e17 as limited inventory. Both stay prepared-not-reviewed in benchmark/preparation-status.json; do not
  mark reviewed from reviews alone (owner change gate).

## Mechanisms to preserve
- Input ceiling is 800k unique input; codex counts all non-cached input. Never read large sources.json/
  coverage.json directly; bounded Python summaries. Keep codex sessions short or route Claude-first.
- Task Verification runs in-session and again offline; keep it over committed files. Report-only reviews use
  no command and write report findings from the start.
- After rebase the engine runs evaluator --check; changed pinned files require preparation.json re-pinning.
- Missing git identity: leave changes staged; parent engine commits. Partial predecessors block dependants.
- Requests: `.session/requests.json`, format in `.github/loop/session-protocol.md` ("Three additional kinds").
- Exports contract: `docs/perpetua/session-exports.md`; explicit selectors only. Order format: `.github/loop/task-graph.md`.

## Open questions
- Notices #92/#100 remain pending for the owner. Do not reinstate the crashed script shaper without contract review.
- Fallback variant (LabVIEW 2024) needs an all-version effort estimate before any choice; not yet started.
- Duplicate session per order in 0012 (#146/#147): engine behaviour or retry? If it recurs, raise an
  `engine-change` with evidence; it doubles quota use.
- Claude routing fell back to codex for all sessions in 0011 and 0012; Claude availability unmeasured.
