# Execution working memory

## Considered
- Iteration 0157 / #712: startup documents read once. State no_progress=1 (0156 review-only, improved=false). No open requests/outboxes; goal gate unaccepted.
- Read .session/history/records/0156.json and #710 snapshot .session/history/sessions/710/b734834309daf4f27820124d5661a210827e0346438a64978cf3a2202c616ed2.md. #710 reviewer done, 21 turns, NOT-CLEAR, artifact expectations.md (iter-0156/710-expectations.md, sha 0429f3ac...4e0e).
- Did not read the contract files; pointers below come from the #710 report and are re-checked by the correction and the reviewer.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN matched comparison contract (evaluation.md row `baseline`): benchmark/baseline/matched-comparison-0155.md (pre-fix sha bacdb800...a021) and .json (888671cc...c598), merged 27dc789b. #710 NOT-CLEAR: F-M1 (medium) interruption row lacks selector vs ledger R08/stop-cause order, json /stopping/mapping[2]; F-M2 (medium) unavailable-before-dispatch arm conflated with dispatched answer_class unsupported, json /stopping/mapping[3], /arms/with_images_rule, md M09; F-M3 (low-medium) 0138 supplies mechanism only (one synthetic comparison, independent_repetitions_per_case_arm null, no images slot), json /repetitions, md M04, O06. F-S1: 0138 path is benchmark/project-run-binding-0138.json (not baseline/). F-S2 hedges inconclusive. Verified OK by #710: hashes, M01-M16 md/json parity, answer_class list, usage_reconciled, O01-O06 open, no thresholds. Correction + changed-scope review ordered in 0157.
- CLOSED attempt-ledger integration seam: #703 CLEAR at HEAD 48f2715e; ledger md 8b2b30e6...3436, json 74c9a47a...0e6f. F-A1 (V20 redundant with V17) and F-A2 (slot-level NONE) remain open for owner decision.
- CLOSED prospective attempt policy: #685 CLEAR on attempt-policy-0148 at cf0c84e5. Design scope only.
- Real-envelope authority is a separate unresolved contract; do not broaden.
- Legacy multiple-attempt selection unresolved/zero completion; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition mechanism, project-paired-0136 design, precision README/plan sizing, lineage uncertainty and freeze procedure. No gap re-survey/count redesign/synthetic-to-real promotion.
- Remaining method gaps after matched comparison: dependency/native keys/access/grants/logs; restricted split/allocation/executed isolation (#636 blockers); reader/probes/scorer integration; challenges row; independent whole-method review and owner acceptance/quality thresholds. benchmark_ready=false. Actual admissions, model/reader/native executions, scored runs and real comparisons remain zero.
- Closed: F1/F2 lineage chain at e15a5033; grouping #649/#653/#656 at 51e672d0; #639 CLEAR project-paired-0136 bb3f5312; #633 CLEAR dependency-byte scope 8d824c68; #622/#625/#626 CLEAR 60a4a737.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md; native behavior/save-version unknown. No session can run LabVIEW. POC code researcher-only.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined.
- #533 constant-rules-0106.md source-blocked. Pair originals 26.1.1f1 32-bit. W1-W8 closed d3c697c3; AF declarations 371c631c.
- WP1 #544 frozen checker invalidated: never refresh/run. WP1 key/c1 chains closed; general key/full trial blocked.
- Policymaker work (#672-675, #680, #687, #694, #708) belongs to Policymaker.

## This iteration
- correct-matched-comparison-0157: benchmark/default/medium, 60 min/35 turns, exports #710, #706. Targeted Edits for F-M1/F-M2/F-M3 only in both 0155 files; report changed pointers and new SHA256. Verification: JSON parse, stopping/mapping list >=4, md size.
- review-matched-comparison-fix-0157: reviewer/default/medium, 45 min/30 turns, blocked_by correction, exports #710. Changed scope only; pins HEAD + hashes; git diff vs 27dc789b for unrelated changes. Verdict in report only.
- Next cold session: read 0157 record and both reports. CLEAR -> close the matched comparison thread (design part of `baseline` row) and pick the next gap from the remaining list; name gap and gain here. NOT-CLEAR -> correct only named findings (fix_rounds=2; this was round 1).

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703 stay closed. No global gap map, redundant readiness batch, duplicate version-effort or strongest model by default.
- 0150 #689 and 0151 #692 combined files+artifacts task partial input_budget; 0153 files-only split worked; 0154 fix+review in one graph worked (#702 27 turns, #703 18 turns); 0155 #706 files-only design 19 turns; 0156 #710 review 21 turns. Do not reissue combined tasks.
- #699/#703 ledger reviews done; #710 hash/parity/repetition checks done; do not redo outside changed scope. Do not redraft matched-comparison-0155.
- Broad Budget at high effort exhausts input budget; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Missing/no-match establishes availability only; Grep on docs/perpetua/evaluation.md with English terms returned nothing (file is Polish); #706 grep for arm/repetition/budget in runner-contract.md returned nothing. Glob: full pattern in `pattern`. Inputs stage flat; derive counts from bytes (#518). Explicit exports required for reports. Path errors (#710 F-S1): verify paths before naming them in tasks.
- Expectations before author applications (#567/#656/#663/#678/#685/#699/#710). Reviewers write report/artifacts only.
- Engine verification lacks session inputs/artifacts/report: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: final graph read-back plus direct Python validation. Empty Write erases files. Read final report before Finish.
