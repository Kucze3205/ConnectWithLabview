# Policy working memory

Considered: iteration records 0000–0016; reviews #146/#147; #150 report and acceptance #151; #157 report and
acceptance #161; re-review #166 (iteration 0015); #170 report snapshot a18d21b5 and commit d0e14f6 (iteration 0016);
engine code `run_policy_script` (.github/loop/iteration.py:511-548).
Updated by Policymaker #172, iteration 0017.
Historical inputs: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json` (4-digit);
reports `.github/loop/data/session-reports/<issue>/*.json` and `.session/history/sessions/<issue>/`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; it supplies the iteration's work.
- Protocol design: re-review #166 (codex) accepted F1/F2 revision at 2669ec4. Author #150 also codex, so a later
  cross-family review of case evidence should prefer Claude.
- Milestones on main: sources, coverage prepared-not-reviewed; tasks, oracle, split, baseline, challenges
  not-started. benchmark_ready=false. Coverage incomplete; quality unmeasured.
- Session #170 (order-168-dev-case-specs) ended `partial`, cause `input_budget`: 904k input, 22 turns, Claude
  spent ~1k out tokens then fell back to codex. Its report stayed at the initial wip text (stale), but commit d0e14f6
  holds `benchmark/scripts/dev_cases.py`, `benchmark/cases/dev/README.md` and 11 cases (3 lvproj, 3 lvclass,
  4 lvlib, 1 VI native-gap; 1076 fixed slots per dimension, 23 native-required, all native refs unavailable) plus
  preparation pins/status. Not merged; no task/170 ref in this checkout, but the commit object is readable.
  No successor was opened (report had no Successor section).
- Lesson: a session can save substantial work and still lose it when the report is not updated before the budget
  ends. Orders now require a report update right after verification and a low turn cap.
- Owner question on accepting the method deliberately NOT filed yet: needs evidence across tasks/oracle/split/
  baseline/challenges first.
- Engine-change #165 and capability #169 (native inspection, resources row 2) pending.

## Orders for iteration 0017 (wake: true)
- `order-172-recover-dev-cases` (benchmark, default, high, 60 min/16 turns): restore only generator and
  `benchmark/cases/dev` from d0e14f6, run generate + `--check`, re-pin tasks/oracle against current main, write
  `benchmark/cases/dev/verification.json`, report counts and gaps.
- `order-172-input-budget-audit` (audit, 60 min/16 turns; exports records 15-16, reports/streams 166 and 170):
  measure why #170 hit the input budget with a stale report; at most two measured recommendations; `audit/0017.md`.

## Next Policymaker (wake after these orders)
- Recovery done -> order an independent cross-family review of the dev cases (author family is in the record;
  prefer Claude if author was codex) against protocol `## tasks`/`## oracle`, claim-level agreement on a sample
  plus the generator. Partial -> let the successor run; do not reorder the same work.
- Read audit/0017.md; act on at most the smallest supported change (task size, report checkpoint, routing).
  Consider whether benchmark should go codex-first or Claude-first given Claude delivered ~1k out tokens in #170.
- Only after `capability-ready` on #169 order native-reference work.
- Next public preparation candidates: challenge fixtures (constant/empty/wrong-citation outputs) against the dev
  cases; lineage/duplicate analysis for split; native-job input/output schema.
- All-version effort estimate still needed before any LabVIEW 2024 fallback choice; not started.

## Milestone evidence
- sources: review #134 revise -> fix #139 -> re-review #140 accept at d588fa9. Coverage review #133 accept at
  6933e17 as limited inventory. Both prepared-not-reviewed; owner gate decides.
- protocol: reviews #146/#147 revise -> #150 -> re-review #166 accept at 2669ec4.

## Mechanisms to preserve
- Input ceiling 800k unique input; codex counts all non-cached input (#166: 320k/19 turns; #170: 904k/22 turns).
  Never read sources.json/coverage.json or case JSON whole; bounded Python summaries. Keep sessions short (~16 turns).
- Require report update immediately after the main verification, before optional work.
- Task Verification runs in-session and again offline over committed files.
- Rebase runs evaluator --check; changed pinned files need preparation.json re-pinning.
- Missing git identity: leave changes staged; parent engine commits.
- Requests: `.session/requests.json`, format `.github/loop/session-protocol.md` ("Three additional kinds").
  Orders: `.github/loop/task-graph.md`; order ids must not repeat ids used in the same iteration.
- Read docs/perpetua/evaluation.md before product planning; accepted-limits.md before private data or spending.

## Open questions
- Notice #92 pending for the owner. Do not reinstate the crashed script shaper without contract review.
- Duplicate sessions per order seen in 0012 and 0014; not in 0015-0016. Collect engine evidence before an engine-change.
- Claude availability: 0011-0016 sessions mostly finished on codex; review-family diversity is weak.
- How a commit-bound review recommendation becomes milestone `reviewed` status: unresolved; owner gate decides.
