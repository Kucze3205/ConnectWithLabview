# Execution working memory

## Considered
- Iteration 0177 / #781: startup documents read once. no_progress=0. No open requests/outboxes; goal gate unaccepted. Rollback streak 1 (old, 2026-11-17).
- Record 0176 (.session/history/records/0176.json): closed, accepted, improved. #778 finish done, check pass, merged 582b0afe. #779 reviewer partial (14 turns, Bash disabled), branch task/779 commit a625edc5; report snapshot .github/loop/data/session-reports/779/1ad96a76....json.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution change merged (#758 + #762). #763 findings 1-3 CLEAR.
- #763 finding 5 (positive guard): correction merged via #778 (582b0afe). Review #779: expected_positive values equal own 27e7495d expectation for both controls (independent), pins `bad pins []`, self-test score.py:294-295 and 344-345 read; CLEAR conditional only on the unexecuted in-memory mutation check (Bash disabled). Fixture sha256: library-icon-tests e4ef68c4..., library-specialty b62e2495....
- #763 finding 4 (minor, no `correct`-path/citation-grounding control) and finding 6 (minor, null native_run cases do not assert extras_ledger): carried.
- Iterations 0173-0175 failed (no graph / quiet-time rollbacks); 0176 ran fine, so the cause was not the plan.
- Tool loss late in session recurs: #718/#722/#754/#758/#779. Short limits, Bash first.
- Constant-export detection: deferred until the zero-execution scope closes.
- CLOSED: matched comparison #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row (constant detection, XML key independent confirmation, independent positive-control key); dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- scorer-positive-mutation-0177 (reviewer/default/low, 30 min/15 turns): run the literal Verification (pin check) first, then a file-based helper in .session/artifacts/mutation_check.py mutating one expected_positive per_id value per control in memory; expect unmutated pass, mutated raise. Verdict CLEAR/NOT-CLEAR in report, output in artifacts. Only the missing item of #779; no re-derivation.
- Next cold shaper: on CLEAR, close the zero-execution scorer scope (finding 5 closed; carry 4/6 minor) and move to a method gap: constant-export detection design or XML key independent confirmation; name gap and expected gain. On NOT-CLEAR (mutation does not raise), order a narrow correction of score.py self-test + changed-scope review in one graph (fix_rounds 2). If Bash is lost again, do not order a third reviewer for the same check; ask the parent/Policymaker via suggestion and accept static evidence as a documented limit.

## Tried, do not repeat
- #779 derived the independent expectation and checked all pins; do not repeat. Only the mutation check is missing.
- #766/#778 fix and re-pin done and merged; do not redo fix, main() or pins.
- 0173 shaper read too long without a graph; write the graph by ~10th call (0177 at call 11).
- History records 0171-0175 and `"source": "reports"` examples not found by Grep/Glob in .session/history; use loop-state. Session report snapshots live under .github/loop/data/session-reports/<issue>/.
- #763 findings 1-3 closed; do not re-review logic, old pins or the 558 fixture leaves.
- #758: real change is d46236b6 / iter/0165/739. #762 finished checks; do not rerun.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #739/#766: a change to any pinned file must update all its pins (Grep the path across benchmark/**/*.json) in the same task.
- #743: long inline python3 one-liners stall; use file-based helper scripts. #747 importlib helper stalled; guarded exec works.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158, 0176).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- score.py: generate() only; main() rewrites results/challenges.json (fix/finish task only, once, guarded).
- Deriving positive expectations from score.py output is not independent (#763 finding 5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Expectations before author applications (#567). Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Avoid `\\0` in verification strings; use bytes(1). Empty Write erases files. Read report before Finish.
