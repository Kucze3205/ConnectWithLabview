# Execution working memory

## Considered
- Iteration 0160 / #724: startup documents read once. State no_progress=1 (0159 improved=false; a review verdict, nothing merged). No open requests/outboxes; goal gate unaccepted.
- Read .session/history/records/0159.json and #722 snapshot .session/history/sessions/722/e17670c6339acd80768933ae90312685895c8109ecf8c4f6622b9511688bfa53.md.
- #722 reviewer done, 11 turns: CLEAR on F-N1 at HEAD 81d309e5; md sha 15d6be1e...0933, json sha 82016b83...ec85 measured by the reviewer; diff vs 07dc83f0 = only json M09; benchmark/preparation.json does NOT hold the old json sha 04543bda...193b. Process note: Grep/Bash/Write briefly returned "No such tool available", then recovered.
- Read docs/perpetua/evaluation.md (table under `## Co musi powstać przed implementacją`). Measured benchmark/preparation.json milestone counts myself: baseline 12, challenges 8, coverage 4, oracle 18, sources 4, split 10, tasks 24.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- CLOSED matched comparison contract (evaluation.md row `baseline`, design part): #722 CLEAR at 81d309e5; benchmark/baseline/matched-comparison-0155.md 15d6be1e...0933, .json 82016b83...ec85. No stale pin in preparation.json (#722). Do not reopen.
- OPEN challenges row (evaluation.md last row: wrong answers, wrong source citations, constant/empty export, unsupported case; zero execution earns no credit). Existing evidence in preparation.json /milestones/challenges: benchmark/scripts/challenges.py, benchmark/challenges/README.md, library-icon-tests.json, library-specialty.json, vi-actor-core-native-gap.json, benchmark/preparation-status.json, benchmark/scripts/score.py, benchmark/results/challenges.json. Coverage of the four kinds unknown -> 0160 gap measurement.
- CLOSED attempt-ledger integration seam: #703 CLEAR at 48f2715e. F-A1 (V20 redundant with V17) and F-A2 (slot-level NONE) remain open for owner decision.
- CLOSED prospective attempt policy: #685 CLEAR on attempt-policy-0148 at cf0c84e5. Design scope only.
- Real-envelope authority is a separate unresolved contract; do not broaden.
- Legacy multiple-attempt selection unresolved/zero completion; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition mechanism (benchmark/project-run-binding-0138.json, mechanism only), project-paired-0136 design, precision README/plan sizing, lineage uncertainty and freeze procedure. No gap re-survey/count redesign/synthetic-to-real promotion.
- Remaining method gaps: challenges row (0160); dependency/native keys/access/grants/logs; restricted split/allocation/executed isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/quality thresholds. benchmark_ready=false. Actual admissions, model/reader/native executions, scored runs and real comparisons remain zero.
- Closed: F1/F2 lineage chain at e15a5033; grouping #649/#653/#656 at 51e672d0; #639 CLEAR project-paired-0136 bb3f5312; #633 CLEAR dependency-byte scope 8d824c68; #622/#625/#626 CLEAR 60a4a737.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md; native behavior/save-version unknown. No session can run LabVIEW. POC code researcher-only.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined.
- #533 constant-rules-0106.md source-blocked. Pair originals 26.1.1f1 32-bit. W1-W8 closed d3c697c3; AF declarations 371c631c.
- WP1 #544 frozen checker invalidated (benchmark/writing/check_c1_challenges_0125.py): never refresh/run. WP1 key/c1 chains closed; general key/full trial blocked.
- Policymaker work (#672-675, #680, #687, #694, #708, #720) belongs to Policymaker.

## This iteration
- challenges-gap-0160: benchmark/default/medium, 60 min/40 turns. Measure-only map of the five challenge requirements to existing evidence; output benchmark/challenges/gap-0160.md with sections `## wrong-answer`, `## wrong-source`, `## constant-or-empty-export`, `## unsupported-case`, `## no-credit-for-zero-execution`, `## Pins`, `## Not counted`. Verification: python3 heading check on that file.
- Expected gain: the named missing piece of the challenges row. Next cold session: read the 0160 record and gap-0160.md; order one narrow benchmark task for the first `missing`/`partial` kind (design + synthetic cases only), with its independent reviewer in the same graph (`blocked_by`) if the scope is narrow. If all kinds are covered, order an independent reviewer of gap-0160 before closing the row, then move to the next gap.

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. No global gap map, redundant readiness batch, duplicate version-effort or strongest model by default.
- 0150 #689 and 0151 #692 combined files+artifacts task partial input_budget; 0153 files-only split worked; 0154, 0157, 0158 fix+review in one graph worked. Do not reissue combined tasks.
- #699/#703 ledger reviews done; #710/#714/#717/#722 matched-comparison checks done. Do not redraft matched-comparison-0155.
- #713 lesson: a correction touching md and json must list every rule pointer in both files. #717 lesson: the json key is `validation_rules`, not `rules`; verify JSON pointers before naming them.
- #718/#722: reviewer tools intermittently returned "No such tool available"; keep a first-turn tool probe in review tasks. If it blocks a third time, submit a suggestion to the Policymaker.
- Broad Budget at high effort exhausts input budget; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Missing/no-match establishes availability only; evaluation.md is Polish (English greps miss; Grep on it returned nothing even for `^#`, so Read it whole, it is short). Glob: full pattern in `pattern`. Inputs stage flat; derive counts from bytes (#518). Explicit exports required for reports. Verify paths before naming them in tasks (#710 F-S1).
- Expectations before author applications (#567/#656/#663/#678/#685/#699/#710). Reviewers write report/artifacts only.
- Engine verification lacks session inputs/artifacts/report: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: final graph read-back plus direct Python validation. Empty Write erases files. Read final report before Finish.
