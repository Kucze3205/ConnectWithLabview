# Execution working memory

## Considered
- Iteration 0154 / #701: startup documents read once. State no_progress=0; 0153 accepted/improved. No open requests/outboxes; goal gate unaccepted.
- Read .session/history/records/0153.json and #699 snapshot .session/history/sessions/699/4944df3ed1857870e273f6d1efe68bdd04f6f79e9c51e4bc1a6033274cf03495.md. #698 (files task) done, merged ef6a6fd9, 11 turns, check pass. #699 reviewer done, NOT-CLEAR, five findings, artifact attempt-ledger-review-expectations-0153.json (sha256 e866d547...1530).
- #698 report snapshot not read by this shaper; ledger file contents not read by this shaper (pins come from #699 report).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN, attempt-ledger integration seam: files benchmark/baseline/attempt-ledger-0150.md/.json merged by #698. #699 NOT-CLEAR at HEAD 210e445f (md a805b8ec..., json f4fcafb8...). Findings: 1 receipt self-hash cycle (verification_receipt_ref in /freeze_receipt/fields); 2 unverifiable 35/631/28 counts restated in md; 3 usage_reconciled lacks actual time/calls, delta, remaining, overrun V-rule; 4 no V-rules freeze_utc < first event/dispatch, preflight seq 1, recovery UTC; 5 answer_class and plan-state mapping not enumerated. Minor F-A1 (V20 redundant with V17), F-A2 (slot-level NONE) open for owner decision; synthetic-vs-real mode flag absent (minor).
- Infrastructure note: #689/#692 partial input_budget was solved by the narrow files-only cut (#698: 11 turns). Keep tasks narrow.
- CLOSED prospective attempt policy: #685 CLEAR on attempt-policy-0148 at cf0c84e5; md 22c83760...79e39, json 15ccbdf6...797df. Design scope only.
- Real-envelope authority is a separate unresolved contract; do not broaden.
- Legacy multiple-attempt selection unresolved/zero completion; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition maps, project-paired-0136 design, precision README/plan sizing, lineage uncertainty and freeze procedure. No gap re-survey/count redesign/synthetic-to-real promotion.
- CLOSED F1/F2 lineage #659 -> #663 -> #666 -> #669 -> #677/#678 at e15a5033. Independence is procedural, not provider-guaranteed.
- Remaining method gaps after the seam: dependency/native keys/access/grants/logs; restricted split/allocation/executed isolation; matched provider/settings/budgets/repetitions/stopping; reader/probes/scorer integration; independent whole-method review and owner acceptance/quality thresholds. benchmark_ready=false. Actual admissions, model/reader/native executions, scored runs and real comparisons remain zero.
- Closed grouping #649/#653/#656 at 51e672d0; #639 CLEAR project-paired-0136 bb3f5312; #636 isolation blockers remain.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md; native behavior/save-version unknown. No session can run LabVIEW. POC code researcher-only.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined.
- #533 constant-rules-0106.md source-blocked. Pair originals 26.1.1f1 32-bit; pair #509/#513/#522 closed. W1-W8 closed d3c697c3; AF declarations 371c631c. #633 CLEAR dependency-byte scope 8d824c68.
- WP1 #544 frozen checker invalidated: never refresh/run. WP1 key/c1 chains closed; general key/full trial blocked.
- #501 version-effort; #622/#625/#626 CLEAR 60a4a737. #505 WM1 parser-only. benchmark/sources.md pins.
- Policymaker work (#672-675, #680, #687, #694) belongs to Policymaker.

## This iteration
- attempt-ledger-fix-0154: benchmark/default/medium, 60 min/35 turns, exports #699 report. Targeted Edit of findings 1-5 in both ledger files; new V-rules after V28; F-A1/F-A2 stay open. Verification: JSON parse, md size, both hashes differ from #699 pins.
- attempt-ledger-rereview-0154: reviewer/default/medium, 60 min/35 turns, blocked_by fix; exports #699 report, input #699 expectations artifact. Per-finding verdict; changed scope only.
- Next cold session: read 0154 record and both reports. If CLEAR, close integration-seam design scope and pick the next named method gap (suggest matched provider/settings/budgets/repetitions/stopping, or reader/probes/scorer integration) with expected gain. If NOT-CLEAR on named findings, one more narrow correction+review (fix_rounds limit 2); then report as blocker instead of looping.

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685 stay closed. No global gap map, redundant readiness batch, duplicate version-effort or strongest model by default.
- 0150 #689 and 0151 #692 combined files+artifacts task partial input_budget; 0153 files-only split worked. Do not reissue combined tasks.
- #699 full review done; do not re-review unchanged ledger sections.
- Broad Budget at high effort exhausts input budget; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Missing/no-match establishes availability only; Glob: full pattern in `pattern`. Inputs stage flat; derive counts from bytes (#518). Explicit exports required for reports.
- Expectations before author applications (#567/#656/#663/#678/#685/#699). Reviewers write report/artifacts only.
- Engine verification lacks session inputs/artifacts/report: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: final graph read-back plus direct Python validation. Empty Write erases files. Read final report before Finish.
