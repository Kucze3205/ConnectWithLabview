# Execution working memory

## Considered
- Iteration 0156 / #709: startup documents read once. State no_progress=0; 0155 accepted/improved. No open requests/outboxes; goal gate unaccepted.
- Read .session/history/records/0155.json and #706 snapshot .session/history/sessions/706/61eff0a47e9ce1af472fefdefb55a037dd5fbee914dbc0ffe57b18b8d891b15b.md. #706 benchmark done, merged 27dc789b, 19 turns, check pass.
- Did not read the contract files themselves; pins below come from the #706 report and are re-checked by the reviewer.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN matched comparison contract (evaluation.md row `baseline`): #706 wrote benchmark/baseline/matched-comparison-0155.md (sha bacdb800...a021) and .json (sha 888671cc...c598), rules M01-M16, open items O01-O06 (O01 real-envelope authority, O02/O03 ledger F-A1/F-A2, O04 repetition count/precision targets, O05 provider independence, O06 0138 file not reopened). Author-flagged loose mappings: interruption terminal, unsupported -> finished_incomplete. Runner has no images arm. Under review in 0156.
- CLOSED attempt-ledger integration seam: #703 CLEAR at HEAD 48f2715e; ledger md 8b2b30e6...3436, json 74c9a47a...0e6f. F-A1 (V20 redundant with V17) and F-A2 (slot-level NONE) remain open for owner decision.
- CLOSED prospective attempt policy: #685 CLEAR on attempt-policy-0148 at cf0c84e5. Design scope only.
- Real-envelope authority is a separate unresolved contract; do not broaden.
- Legacy multiple-attempt selection unresolved/zero completion; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition maps, project-paired-0136 design, precision README/plan sizing, lineage uncertainty and freeze procedure. No gap re-survey/count redesign/synthetic-to-real promotion.
- Remaining method gaps after matched comparison: dependency/native keys/access/grants/logs; restricted split/allocation/executed isolation (#636 blockers); reader/probes/scorer integration; challenges row; independent whole-method review and owner acceptance/quality thresholds. benchmark_ready=false. Actual admissions, model/reader/native executions, scored runs and real comparisons remain zero.
- Closed: F1/F2 lineage chain at e15a5033; grouping #649/#653/#656 at 51e672d0; #639 CLEAR project-paired-0136 bb3f5312; #633 CLEAR dependency-byte scope 8d824c68; #622/#625/#626 CLEAR 60a4a737.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md; native behavior/save-version unknown. No session can run LabVIEW. POC code researcher-only.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined.
- #533 constant-rules-0106.md source-blocked. Pair originals 26.1.1f1 32-bit. W1-W8 closed d3c697c3; AF declarations 371c631c.
- WP1 #544 frozen checker invalidated: never refresh/run. WP1 key/c1 chains closed; general key/full trial blocked.
- Policymaker work (#672-675, #680, #687, #694, #708) belongs to Policymaker.

## This iteration
- review-matched-comparison-0156: reviewer/default/medium, 60 min/40 turns, exports #706 and #703 reports. Cold check: expectations.md saved in artifacts before reading the contract or #706; hash pins compared in report; M01-M16 md/json parity; loose stopping mappings vs ledger decision table; O06 checked against project-run-binding-0138.json; O01-O06 open, no thresholds. Verdict and F-M findings in report only. Verification: JSON parse + md size (repository-only).
- Next cold session: read 0156 record and reviewer report. CLEAR -> close the thread and pick the next gap from the remaining list (name gap and gain here). NOT-CLEAR -> one graph: benchmark correction of named findings + reviewer of changed scope blocked_by it, producer artifacts as inputs.

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703 stay closed. No global gap map, redundant readiness batch, duplicate version-effort or strongest model by default.
- 0150 #689 and 0151 #692 combined files+artifacts task partial input_budget; 0153 files-only split worked; 0154 fix+review in one graph worked (#702 27 turns, #703 18 turns); 0155 #706 files-only design 19 turns. Do not reissue combined tasks.
- #699/#703 ledger reviews done; do not re-review the ledger without changed evidence. Do not redraft matched-comparison-0155.
- Broad Budget at high effort exhausts input budget; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Missing/no-match establishes availability only; Grep on docs/perpetua/evaluation.md with English terms returned nothing (file is Polish); #706 grep for arm/repetition/budget in runner-contract.md returned nothing. Glob: full pattern in `pattern`. Inputs stage flat; derive counts from bytes (#518). Explicit exports required for reports.
- Expectations before author applications (#567/#656/#663/#678/#685/#699). Reviewers write report/artifacts only.
- Engine verification lacks session inputs/artifacts/report: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: final graph read-back plus direct Python validation. Empty Write erases files. Read final report before Finish.
