# Execution working memory

## Considered
- Iteration 0166 / #742: startup documents read once. no_progress=1 (0165 not improved). No open requests/outboxes; goal gate unaccepted.
- Record 0165: #739 benchmark partial, check fail, branch task/739 commit 5db2610e, not merged; #740 reviewer blocked (never ran). Report of #739 read (.session/history/sessions/739/1e5beba4...md). benchmark/preparation.json read whole (challenges milestone pins score.py 810a5457..., results/challenges.json a5b97984...).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution fix (#739, task/739 5db2610e): score.py gives `unverified` when executed<=0, scored<=0 or native_run null (lines 148, 213-216); regression cases added; note benchmark/challenges/scorer-fix-0165.md. Failed engine check: `empty evidence or hash mismatch: benchmark/scripts/score.py` (preparation.json pin not updated). Side effect: all 33 controls declare zero execution, generate() gives 5 match / 28 mismatch against frozen `expected`; native_run-null branch not isolated by a test.
- Positive-control cause (#739): `unverified` from provisional key and missing native refs (score.py lines 204-205, 210-211, assessment 34-49); intended, not a bug. A0001-A0010 score `correct` in library-icon-tests control 0.
- Constant-export detection not handled: deferred until the zero-execution review closes.
- 0161-0163 failures: policy/session-state.py output over 8 MiB (Policymaker side).
- CLOSED: matched comparison contract #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5, design only.
- Real-envelope authority separate and unresolved; legacy multiple-attempt selection unresolved; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition, project-paired-0136 design, precision sizing, lineage/freeze procedure.
- Remaining method gaps: challenges row (constant detection, XML key independent confirmation, independent positive-control key); dependency/native keys/access/grants/logs; restricted split/allocation/executed isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Admissions, model/reader/native executions, scored runs, real comparisons: zero.
- Closed: lineage e15a5033; grouping 51e672d0; #639 bb3f5312; #633 8d824c68; #622/#625/#626 60a4a737.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW. POC code researcher-only.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined.
- #533 source-blocked. W1-W8 closed d3c697c3; AF declarations 371c631c. WP1 #544 checker invalidated: never run.

## This iteration
- scorer-finish-0166: benchmark/default/medium, start_branch task/739, 60 min/40 turns, #739 report exported. Finish only: update stale fixture `expected` outcomes explained by the zero-execution rule, add native_run-null self-test, regenerate results/challenges.json via main() once, update preparation.json pins. Check: all preparation.json pins match bytes; note gains `## Expectation update`.
- scorer-finish-review-0166: reviewer/default/medium, blocked_by finish; expectation artifact first; diff vs 810a5457 commit; in-memory generate(); CLEAR/NOT-CLEAR.
- Next cold shaper: CLEAR -> zero-execution closed; pick constant detection or XML key independent confirmation. NOT-CLEAR -> one narrow correction + changed-scope review in one graph. If finish partial again: do not resume a third time; split pins/results from fixtures.

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. gap-0160 (#725), scorer-probe-0164 (#736), positive-control cause (#739): do not re-survey or re-probe.
- #739: a score.py change without updating benchmark/preparation.json pins and stale fixture expectations fails the engine check (same as #117/#122). Any change to a pinned file must update its pin in the same task.
- 0150 #689 / 0151 #692 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #718/#722: reviewer tools intermittently "No such tool available"; keep a first-turn tool probe.
- Broad Budget at high effort exhausts input; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- score.py: run via importlib `python3 -I`, generate() only; main() rewrites benchmark/results/challenges.json (only the finish task may call it).
- evaluation.md is Polish; Read it whole. Glob: full pattern. Inputs stage flat; counts from bytes (#518). Explicit exports for reports. Verify paths before naming (#710 F-S1).
- Expectations before author applications (#567 etc.). Reviewers write report/artifacts only.
- Engine verification: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
