# Execution working memory

## Considered
- Iteration 0176 / #777: startup documents read once. no_progress=4. No open requests/outboxes; goal gate unaccepted.
- Iteration 0175 (loop-state `iterations`): FAILED, 0 tasks, 315 s, verdict none. Rollback streak 1, target 182372eb, reason "did not close within the quiet time". Its graph (finish + review of #766) never ran.
- 0174 FAILED the same way (quiet time); 0173 shaper #769 wrote no valid graph. Record 0172: #766 benchmark partial, check fail, branch task/766 commit 3c56d2a6; #767 reviewer blocked.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution change merged (#758 + #762). #763 findings 1-3 CLEAR (score.py:213-216 logic, pins, fixture expectations).
- #763 finding 5 (positive guard) correction saved on task/766, NOT merged: `expected_positive` on `extra-true-answer` (library-icon-tests.json) and `positive-control` (library-specialty.json), from 27e7495d; self-test compares to it; main() ran once; note benchmark/challenges/scorer-positive-0172.md. Engine check failed on a hash mismatch: the fixtures are also pinned in preparation.json, writing/input-pins.json, writing/c1-challenges-0125-pins.json, writing/reviews-0128/c1-artifact-manifest-0126.json.
- #763 finding 4 (minor, no `correct`-path/citation-grounding control) and finding 6 (minor, null native_run cases do not assert extras_ledger): carried.
- Four failed iterations in a row (0173 no graph; 0174 and 0175 quiet-time rollbacks before any task ran). The finish plan has never executed; it is not a failed approach. If 0176 also rolls back before tasks run, the cause is engine/quiet time, not the plan: the next shaper should report it and file a suggestion, not rephrase the plan again.
- Tool loss late in session recurs: #718/#722/#754/#758. Short limits and early checks help.
- Constant-export detection: deferred until the zero-execution scope closes.
- CLOSED: matched comparison #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row (constant detection, XML key independent confirmation, independent positive-control key); dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- scorer-positive-finish-0176 (benchmark/default/medium, limits 30 min/20 turns, start_branch task/766): re-pin both fixtures in every benchmark/**/*.json pin with targeted Edit, append `## Finish 0176` to scorer-positive-0172.md. No main(), no rewrite. Check: Verification prints "fixture pins OK" (sha256 or git-blob sha1 accepted).
- scorer-positive-review-0176 (reviewer/default/medium, 45 min/30 turns, blocked_by finish): own expectation from 27e7495d saved first to artifacts, per-control verdicts, in-memory mutation check, all pins; CLEAR/NOT-CLEAR in report.
- No `exports` used (format unconfirmed in history); bodies are self-contained.
- Next cold shaper: on merged + CLEAR, close the zero-execution scope (carry findings 4/6 minor) and move to a method gap (constant-export detection design, or XML key independent confirmation). On NOT-CLEAR, correct named findings + changed-scope review in one graph (fix_rounds 2). If the finish fails, inspect `git show` of the branch yourself; do not resume #766 as a full task a third time.

## Tried, do not repeat
- #766 full fix done on task/766; do not redo fix, main() or mutation check. Scan every pin of every changed file.
- 0173 shaper read too long without a graph; write the graph by ~10th call (0175 at call 9, 0176 at call 9).
- History records 0171-0175 and `"source": "reports"` examples not found by Grep/Glob in .session/history; do not search again, use loop-state.
- #763 findings 1-3 closed; do not re-review logic, old pins or the 558 fixture leaves.
- #758: real change is d46236b6 / iter/0165/739. #762 finished checks; do not rerun.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #739/#766: a change to any pinned file must update all its pins (Grep the path across benchmark/**/*.json) in the same task.
- #743: long inline python3 one-liners stall; use file-based helper scripts. #747 importlib helper stalled; guarded exec works.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- score.py: generate() only; main() rewrites results/challenges.json (fix/finish task only, once, guarded).
- Deriving positive expectations from score.py output is not independent (#763 finding 5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Expectations before author applications (#567). Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Avoid `\\0` in verification strings; use bytes(1). Empty Write erases files. Read report before Finish.
