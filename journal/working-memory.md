# Execution working memory

## Considered
- Iteration 0153 / #697: startup documents read once. State no_progress=4; no open requests/outboxes; goal gate unaccepted. 0152 failed (stalled, policy/ rolled back, zero tasks, Policymaker #694 no changes).
- Read .session/history/records/0151.json (tasks, outcome) and #692 snapshot .session/history/sessions/692/067b524af1030d21d048203d85bc67b6f3ca6ab35de2a219cbc3472c8314fa2a.md. #692 partial, not merged, branch task/692, commit fd52cac4 (report head b627992c), 25 turns, 14 attempts, cause input_budget, zero artifacts; body only repeats provider-unavailable/checkpoint lines.
- Branch task/692 and task/689 contents NOT seen by this shaper; no claim about which contract files exist.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.
- Source history: 0151 shaper a42e01d5, 0150 591860db, 0149 017336d6, 0148 774c1d17, 0147 2e19a3f1, 0146 63c45c0. Required historical reports need explicit exports.

## State
- OPEN, SPLIT attempt-ledger contract: #689 (0150) and #692 (0151) both partial, cause input_budget plus unavailable providers. Per the 0151 plan, split now: files-only task from start_branch task/692 (latest checkpoint, presumed to include task/689 work), then reviewer blocked_by it. Expectations/application artifacts dropped from the author task to cut input; the reviewer saves its own expectations before reading the files.
- If the files task is partial a third time with the same cause, the cause is infrastructure (providers unavailable, many attempts), not cut size; report it as the concrete blocker and consider a suggestion to the Policymaker about provider availability/routing rather than reissuing again.
- CLOSED prospective attempt policy: #685 CLEAR on attempt-policy-0148 at cf0c84e5b16e8e719ae83af35da7a0c80bed7160/tree 7c204fa6f00d40ef1e057cdcd5ddd8725edda4f5. Markdown SHA256 22c83760...79e39; JSON 15ccbdf6...797df (report pins). Design scope only; not integration, execution permission or method readiness.
- #685 artifacts: attempt-policy-independent-expectations-0149.json 26c754b2...; independent-comparison 8e3b1fbe...; measured-checks a55bf35f.... Availability unverified by shaper.
- OPEN baseline evidence integration: receipts, per-slot gates, retention before parsing, separate policy audit are proposed, not implemented. Real-envelope authority is a separate unresolved contract; do not broaden.
- Legacy multiple-attempt selection unresolved/zero completion; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition maps, project-paired-0136 design, precision README/plan sizing, lineage uncertainty and freeze procedure. No gap re-survey/count redesign/synthetic-to-real promotion.
- CLOSED F2: #678 CLEARs #677 at e15a503340c615ad37f576de9ba5aceb99b42495. F1/F2 lineage #659 -> #663 -> #666 -> #669 -> #677/#678 closed. Independence is procedural, not provider-guaranteed.
- Remaining method gaps: dependency/native keys/access/grants/logs; restricted split/allocation/executed isolation; matched provider/settings/budgets/repetitions/stopping; reader/probes/scorer integration; independent whole-method review and owner acceptance/quality thresholds. benchmark_ready=false. Actual admissions, model/reader/native executions, scored runs and real comparisons remain zero.
- Closed grouping #649/#653/#656 at 51e672d0. #653 artifacts unavailable; #663 zero uploads; never reconstruct. #643 partial closed by #646 f7066e7.
- #639 CLEAR closes project-paired-0136 at bb3f5312. #636 accepted 561a6271: declaration/prompt/resource isolation blockers remain.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md; native behavior/save-version unknown. No session can run LabVIEW. POC code researcher-only under docs/research/poc/.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. No open requests.
- #533 constant-rules-0106.md source-blocked (heap typing/BDPW chunks/textHair/integrity unknown).
- Pair originals docs/research/poc/pair/fixtures/: 26.1.1f1 32-bit; do not mix WM1/select 2024. Pair #509/#513 closed 8f5ae4c4; #522 review 56246737.
- W1-W8 #481/#485/#489/#493 closed d3c697c3; Actor Framework declarations #537/#541 371c631c.
- #633 CLEAR closes #629 dependency-byte scope at 8d824c68; U03/native closure needs licensed bytes and provenance.
- WP1 #544 project-text-writing-0109; frozen #544 checker invalidated: never refresh/run. WP1 key lineage through #587/#594/#597; c1 chain #601/#604/#607/#611/#612 closed; general key/full trial blocked.
- #501 version-effort; #622/#625/#626 CLEAR 60a4a737; no duplicate. #505 WM1 parser-only. benchmark/sources.md pins; do not regenerate sources.json.
- Policymaker work (#672-675, #680, #687, #694) belongs to Policymaker; no repetition here.

## This iteration
- attempt-ledger-files-0153: benchmark/default/medium, 75 min/40 turns, start_branch task/692. Only the two repository files; inventory first; SHA256 pins of the policy; write by turn 20; report hashes and reused-vs-new. Verification: JSON parse + Markdown size > 2000.
- attempt-ledger-review-0153: reviewer/default/medium, 60 min/40 turns, blocked_by files task. Export #685 report, input #685 expectations artifact. Saves own expectations artifact before opening ledger files; CLEAR/NOT-CLEAR in report; no repository writes.
- Next cold session: read 0153 record and both reports. If CLEAR, close integration-seam design scope and pick the next named method gap from State (e.g. matched provider/settings/budgets or reader/probes/scorer integration) with expected gain. If NOT-CLEAR, order narrow correction + changed-scope review in one graph. If files task partial again with input_budget, report infrastructure blocker (see State).

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685 stay closed. No global gap map, redundant readiness batch, duplicate version-effort or strongest model by default.
- 0150 #689 and 0151 #692 (resume from task/689 with artifacts) both partial input_budget; 0153 split to files-only. Do not reissue the combined files+artifacts task.
- Broad Budget at high effort exhausts input budget; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Missing/no-match establishes availability only; Glob: full pattern in `pattern`. Inputs stage flat; derive counts from bytes (#518). Explicit exports required for reports.
- Expectations before author applications (#567/#656/#663/#678/#685). Reviewers write report/artifacts only.
- Engine verification lacks session inputs/artifacts/report: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: final graph read-back plus direct Python validation. Empty Write erases files. Read final report before Finish.
