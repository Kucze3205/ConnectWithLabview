# Execution working memory

## Considered
- Iteration 0158 / #716: startup documents read once. State no_progress=0 (0157 accepted, improved=true). No open requests/outboxes; goal gate unaccepted.
- Read .session/history/records/0157.json and #714 snapshot .session/history/sessions/714/d77ffeac97104787d1e4a11e3e07c032bc4ae6e560e103667cb1a02bd3183fe6.md. #713 benchmark done, merged 12528c90, 23 turns. #714 reviewer done, 8 turns, NOT-CLEAR at HEAD 07dc83f0.
- Did not read the contract files; the F-N1 pointer comes from the #714 report and is re-checked by the fix and the re-check.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN matched comparison contract (evaluation.md row `baseline`): benchmark/baseline/matched-comparison-0155.md (sha 15d6be1e...0933) and .json (04543bda...193b) at 07dc83f0 after #713 correction. #714 NOT-CLEAR: F-M1 and F-M3 resolved; F-M2 resolved except F-N1 (medium): json /rules/M09 still conflates an unavailable arm with answer_class unsupported; md M09 is correct. Fix round 2 of 2 (limits.fix_rounds=2) plus narrow re-check ordered in 0158.
- CLOSED attempt-ledger integration seam: #703 CLEAR at HEAD 48f2715e; ledger md 8b2b30e6...3436, json 74c9a47a...0e6f. F-A1 (V20 redundant with V17) and F-A2 (slot-level NONE) remain open for owner decision.
- CLOSED prospective attempt policy: #685 CLEAR on attempt-policy-0148 at cf0c84e5. Design scope only.
- Real-envelope authority is a separate unresolved contract; do not broaden.
- Legacy multiple-attempt selection unresolved/zero completion; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition mechanism (benchmark/project-run-binding-0138.json, mechanism only), project-paired-0136 design, precision README/plan sizing, lineage uncertainty and freeze procedure. No gap re-survey/count redesign/synthetic-to-real promotion.
- Remaining method gaps after matched comparison: dependency/native keys/access/grants/logs; restricted split/allocation/executed isolation (#636 blockers); reader/probes/scorer integration; challenges row; independent whole-method review and owner acceptance/quality thresholds. benchmark_ready=false. Actual admissions, model/reader/native executions, scored runs and real comparisons remain zero.
- Closed: F1/F2 lineage chain at e15a5033; grouping #649/#653/#656 at 51e672d0; #639 CLEAR project-paired-0136 bb3f5312; #633 CLEAR dependency-byte scope 8d824c68; #622/#625/#626 CLEAR 60a4a737.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md; native behavior/save-version unknown. No session can run LabVIEW. POC code researcher-only.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined.
- #533 constant-rules-0106.md source-blocked. Pair originals 26.1.1f1 32-bit. W1-W8 closed d3c697c3; AF declarations 371c631c.
- WP1 #544 frozen checker invalidated: never refresh/run. WP1 key/c1 chains closed; general key/full trial blocked.
- Policymaker work (#672-675, #680, #687, #694, #708) belongs to Policymaker.

## This iteration
- fix-m09-parity-0158: benchmark/default/low, 30 min/20 turns, exports #714. One targeted Edit of json /rules/M09 to md M09 meaning; md byte-unchanged. Verification: json parse, 'dispatch' in M09, md SHA256 pinned.
- recheck-m09-parity-0158: reviewer/default/low, 30 min/20 turns, blocked_by fix, exports #714. Only M09 parity + git diff 07dc83f0 shows only json M09. Verdict in report only.
- Next cold session: read 0158 record and both reports. CLEAR -> close matched comparison thread and pick the next gap from the remaining list (name gap and gain here). NOT-CLEAR -> fix rounds exhausted: do not order a third correction blindly; record the residual finding as carried, and either submit a suggestion to the Policymaker or choose a next gap while carrying it explicitly.

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703 stay closed. No global gap map, redundant readiness batch, duplicate version-effort or strongest model by default.
- 0150 #689 and 0151 #692 combined files+artifacts task partial input_budget; 0153 files-only split worked; 0154 and 0157 fix+review in one graph worked (#713 23 turns, #714 8 turns). Do not reissue combined tasks.
- #699/#703 ledger reviews done; #710 hash/parity/repetition checks and #714 F-M1/F-M3 checks done; do not redo outside changed scope. Do not redraft matched-comparison-0155.
- #713 lesson: a correction touching md and json must list every rule pointer in both files (M09 missed in json). Name both pointers in acceptance.
- Broad Budget at high effort exhausts input budget; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Missing/no-match establishes availability only; Grep on docs/perpetua/evaluation.md with English terms returned nothing (file is Polish); #706 grep for arm/repetition/budget in runner-contract.md returned nothing. Glob: full pattern in `pattern`. Inputs stage flat; derive counts from bytes (#518). Explicit exports required for reports. Path errors (#710 F-S1): verify paths before naming them in tasks.
- Expectations before author applications (#567/#656/#663/#678/#685/#699/#710). Reviewers write report/artifacts only.
- Engine verification lacks session inputs/artifacts/report: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: final graph read-back plus direct Python validation. Empty Write erases files. Read final report before Finish.
