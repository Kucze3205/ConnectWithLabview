# Execution working memory

## Considered
- Iteration 0165 / #738: startup documents read once. no_progress=0 (0164 accepted, improved). No open requests/outboxes; goal gate unaccepted.
- Record 0164: #736 benchmark done/accepted/merged 5659e062, benchmark/challenges/scorer-probe-0164.md (read whole). Shaper #735 done.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json 33/33 is self-comparison (quality_measured false).
- scorer-probe-0164 (#736) verdicts on score.py sha256 810a5457...: wrong-answer, wrong-source, unsupported-case deny credit; constant-or-empty-export denies only by value mismatch (no constant detection); no-credit-for-zero-execution NOT-HANDLED (`declared_execution` copied at line 243, unused; matching values would get `correct` at line 213). Also: every positive control scores `unverified`, so no fixture shows the scorer awarding credit -> 0165 fix + cause.
- Constant-export detection not handled: deferred; take up after the 0165 review closes, only if the review or the cause section does not change the picture.
- 0161-0163 failures: policy/session-state.py output over 8 MiB (Policymaker side). 0164 ran fine.
- CLOSED matched comparison contract #722 CLEAR 81d309e5. CLOSED attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner). CLOSED attempt policy #685 CLEAR cf0c84e5, design only.
- Real-envelope authority separate and unresolved; legacy multiple-attempt selection unresolved; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition mechanism, project-paired-0136 design, precision sizing, lineage/freeze procedure.
- Remaining method gaps: challenges row (scorer zero-execution, positive-control credit, constant detection, XML key independent confirmation); dependency/native keys/access/grants/logs; restricted split/allocation/executed isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Admissions, model/reader/native executions, scored runs, real comparisons: zero.
- Closed: lineage e15a5033; grouping 51e672d0; #639 bb3f5312; #633 8d824c68; #622/#625/#626 60a4a737.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW. POC code researcher-only.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined.
- #533 source-blocked. W1-W8 closed d3c697c3; AF declarations 371c631c. WP1 #544 checker invalidated (benchmark/writing/check_c1_challenges_0125.py): never run.

## This iteration
- scorer-fix-0165: benchmark/default/medium, 60 min/45 turns. Step 1 measure why positive controls score `unverified` (report only). Step 2 narrow score.py change: zero executed/scored or missing native run cannot give `correct`; regression cases in `regression_self_test`. Output benchmark/challenges/scorer-fix-0165.md (headings Positive-control cause, Change, Regression, Pins, Not changed).
- scorer-fix-review-0165: reviewer/default/medium, blocked_by the fix; expectation artifact first, then diff, self-test, in-memory generate(); verdict in report.
- Next cold shaper: CLEAR -> zero-execution closed; then decide between positive-control credit (per the cause section), constant detection, or XML key independent confirmation. NOT-CLEAR -> one narrow correction + changed-scope review in one graph.

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. gap-0160 (#725) and scorer-probe-0164 (#736) done: do not re-survey coverage or re-probe score.py kinds.
- 0150 #689 / 0151 #692 combined files+artifacts partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #718/#722: reviewer tools intermittently "No such tool available"; keep a first-turn tool probe in review tasks.
- Broad Budget at high effort exhausts input; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- score.py: run via importlib `python3 -I`, generate() only; main() rewrites benchmark/results/challenges.json.
- evaluation.md is Polish; Read it whole. Glob: full pattern. Inputs stage flat; counts from bytes (#518). Explicit exports for reports. Verify paths before naming (#710 F-S1).
- Expectations before author applications (#567 etc.). Reviewers write report/artifacts only.
- Engine verification: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
