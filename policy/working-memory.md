# Policy working memory

Considered: iteration records 0000–0015; reviews #146/#147; #150 report and acceptance #151; #157 report and
acceptance #161; re-review #166 (iteration 0015); engine code `run_policy_script` (.github/loop/iteration.py:511-548).
Updated by Policymaker #168, iteration 0016.
Historical inputs: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json` (4-digit);
reports `.github/loop/data/session-reports/<issue>/*.json` and `.session/history/sessions/<issue>/`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; it supplies the iteration's work.
- Protocol design: re-review #166 (codex/gpt-6.1-sol, report d35c2aac) closed F1 and F2 at 2669ec4, overall
  **accept**. Caveat: author #150 was also codex, so not a different family; reviewer routing is Claude-first but the
  session fell back to codex (Claude spent only ~5k out tokens). Accept as design review; a later cross-family review
  of the case evidence should prefer Claude.
- Milestones (preparation-status.json): sources, coverage prepared-not-reviewed; tasks, oracle, split, baseline,
  challenges not-started. Evaluator --check exit 0, benchmark_ready=false. Coverage incomplete; quality unmeasured.
- Owner question on accepting the method deliberately NOT filed yet: evaluation.md needs evidence (tasks/oracle/split/
  baseline/challenges) before owner acceptance; asking on a design-only protocol would be premature.
- Engine-change #165 (missing stdout.txt -> TokenlessUnavailable) pending. Iteration 0015 ran without a repeat of the
  0014 failure.

## Orders and requests for iteration 0016
- `order-168-dev-case-specs` (benchmark, default model, high, 90 min/60 turns): first public development cases from
  XML-readable families (.lvproj/.lvclass/.lvlib) plus one .vi case with native oracle `unavailable`; generator
  `benchmark/scripts/dev_cases.py` with `--check`; pin under tasks/oracle; status prepared-not-reviewed.
- `capability` request filed: resources-proposal row 2 (bounded native inspection on the existing NI 2026 Q1
  container path, public development artifacts only, no spending, providers Anthropic/OpenAI/Copilot for public
  outputs). Row 1 (restricted store) not filed: needs owner answers (which store, custodian) — ask as a question
  when split work is next.
- No wake.

## Next Policymaker
- Read the benchmark report: case counts per family, native-unavailable items, --check result. done -> order an
  independent review (prefer Claude family; author model is in the record) of the cases against protocol `## tasks`.
  partial -> let the successor run; do not reorder the same work.
- Check the capability request decision; only after `capability-ready` order native-reference work.
- Next public preparation candidates (no new access): challenge fixtures (constant/empty/wrong-citation outputs)
  against the dev cases; lineage/duplicate analysis for split; native-job input/output schema.
- All-version effort estimate is still needed before any LabVIEW 2024 fallback choice; not started.

## Milestone evidence
- sources: review #134 revise -> fix #139 -> re-review #140 accept at d588fa9. Coverage review #133 accept at
  6933e17 as limited inventory. Both stay prepared-not-reviewed; owner gate decides.
- protocol: reviews #146/#147 revise -> #150 -> re-review #166 accept at 2669ec4.

## Mechanisms to preserve
- Input ceiling 800k unique input; codex counts all non-cached input (#166: 320k in for 19 turns). Never read
  sources.json/coverage.json directly; bounded Python summaries. Keep sessions short.
- Task Verification runs in-session and again offline over committed files.
- Rebase runs evaluator --check; changed pinned files need preparation.json re-pinning.
- Missing git identity: leave changes staged; parent engine commits.
- Requests: `.session/requests.json`, format `.github/loop/session-protocol.md` ("Three additional kinds").
  Orders: `.github/loop/task-graph.md`; order ids must not repeat ids used in the same iteration.
- Read docs/perpetua/evaluation.md before product planning; accepted-limits.md before private data or spending.

## Open questions
- Notice #92 pending for the owner. Do not reinstate the crashed script shaper without contract review.
- Duplicate sessions per order seen in 0012 and 0014; not in 0015. Collect engine evidence before an engine-change.
- Claude availability: 0011-0015 sessions mostly finished on codex; review-family diversity is therefore weak.
- How a commit-bound review recommendation becomes milestone `reviewed` status: unresolved; owner gate decides.
