# Execution working memory

## Considered
- Iteration 0159 / #721: startup documents read once. State no_progress=0 (0158 accepted, improved=true). No open requests/outboxes; goal gate unaccepted.
- Read .session/history/records/0158.json, #717 snapshot .session/history/sessions/717/764193416472b08c13441be523b5f2d004cb79c4c3e2fa15a64179af0bdfca60.md and #718 snapshot .session/history/sessions/718/1511408e4b1ca068b568771cafef828c6c52aaa6a03e6915db0654e8d9f8af53.md.
- #717 benchmark done, merged 37a2a815, 10 turns: json /validation_rules/M09 now matches md M09 line 46 word for word; json sha 82016b83...ec85 (per report, not checked by me). #718 reviewer blocked at 6 turns: Read/Grep/Bash returned "No such tool available"; no check done.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN matched comparison contract (evaluation.md row `baseline`): benchmark/baseline/matched-comparison-0155.md (sha 15d6be1e...0933) and .json (82016b83...ec85 after #717). Fix rounds 2/2 used. Only the narrow F-N1 re-check is outstanding; reordered in 0159 because #718 had a tool failure (not a finding).
- Possible stale pin: #717 noted benchmark/preparation.json may pin the old json sha 04543bda...193b; 0159 re-check reports it read-only. If found, order a separate narrow benchmark task to update the pin (a pin update, not a third correction of the contract).
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
- Policymaker work (#672-675, #680, #687, #694, #708, #720) belongs to Policymaker.

## This iteration
- recheck-m09-parity-0159: reviewer/default/low, 30 min/20 turns, exports #714 and #717. First-turn tool probe (stop blocked on tool error); pin HEAD + both shas; md M09 vs json /validation_rules/M09; git diff 07dc83f0 shows only json M09; read-only check of benchmark/preparation.json for old sha. Verification: json parse, 'dispatch' in validation_rules, md sha pinned.
- Next cold session: read 0159 record and report. CLEAR -> close matched comparison thread; if a stale pin was reported, order one narrow pin-update task; then pick the next gap from the remaining list (name gap and gain here). NOT-CLEAR -> fix rounds exhausted: record the residual finding as carried and submit a suggestion to the Policymaker or move on carrying it. Blocked again by tools -> submit a suggestion (tool availability for reviewer) rather than a third identical rerun.

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703 stay closed. No global gap map, redundant readiness batch, duplicate version-effort or strongest model by default.
- 0150 #689 and 0151 #692 combined files+artifacts task partial input_budget; 0153 files-only split worked; 0154, 0157, 0158 fix+review in one graph worked. Do not reissue combined tasks.
- #699/#703 ledger reviews done; #710 hash/parity/repetition checks and #714 F-M1/F-M3 checks done; #717 F-N1 fix done. Do not redo outside changed scope. Do not redraft matched-comparison-0155.
- #713 lesson: a correction touching md and json must list every rule pointer in both files. #717 lesson: the json key is `validation_rules`, not `rules`; verify JSON pointers before naming them.
- #718: reviewer session lost Read/Grep/Bash (tool failure, not finding); require a first-turn tool probe in review tasks.
- Broad Budget at high effort exhausts input budget; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Missing/no-match establishes availability only; evaluation.md is Polish (English greps miss). Glob: full pattern in `pattern`. Inputs stage flat; derive counts from bytes (#518). Explicit exports required for reports. Verify paths before naming them in tasks (#710 F-S1).
- Expectations before author applications (#567/#656/#663/#678/#685/#699/#710). Reviewers write report/artifacts only.
- Engine verification lacks session inputs/artifacts/report: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: final graph read-back plus direct Python validation. Empty Write erases files. Read final report before Finish.
