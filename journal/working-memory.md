# Execution working memory

## Considered
- Iteration 0173 / #769: startup documents read once. no_progress=1 (0172 closed, not improved). No open requests/outboxes; goal gate unaccepted.
- Record 0172: #766 benchmark partial, check fail, branch task/766 commit 3c56d2a6 (report snapshot .session/history/sessions/766/8b97eae5....md, read directly); #767 reviewer blocked (never ran, blocked_by #766).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution change merged (#758 + #762). #763 findings 1-3 CLEAR (score.py:213-216 logic, pins, fixture expectations).
- #763 finding 5 (positive guard) correction saved on task/766, NOT merged: `expected_positive` added to `extra-true-answer` (benchmark/challenges/library-icon-tests.json) and `positive-control` (benchmark/challenges/library-specialty.json), from 27e7495d via .session/artifacts/insert_expected_positive_0172.py; self-test compares baseline+mutations to it; self-comparison removed; main() already ran once; note benchmark/challenges/scorer-positive-0172.md. Engine check failed: `empty evidence or hash mismatch: benchmark/challenges/library-icon-tests.json`. Cause (read via Grep on main): both fixtures are also pinned in preparation.json (~63/67), writing/input-pins.json (~27-28), writing/c1-challenges-0125-pins.json (~99/104), writing/reviews-0128/c1-artifact-manifest-0126.json (~209/214); #766 wrongly said only in results/challenges.json.
- #763 finding 4 (minor): no fixture control exercises `correct` path / citation-grounding failure. Finding 6 (minor): null native_run cases do not assert extras_ledger. Carried.
- Stall (#743/#747) not reproduced by #751 (scorer-stall-0168.md). Guarded exec probe works.
- Tool loss late in session recurs: #718/#722/#754/#758. Short limits and early checks help.
- Constant-export detection: deferred until the zero-execution scope closes.
- 0161-0163 failures: policy/session-state.py output over 8 MiB (Policymaker side).
- CLOSED: matched comparison #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition, project-paired-0136 design, precision sizing, lineage/freeze procedure.
- Remaining method gaps: challenges row (constant detection, XML key independent confirmation, independent positive-control key); dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- scorer-positive-finish-0173 (benchmark/default/medium, 30 min/20 turns, start_branch task/766, exports 766): re-pin the two fixtures in the four pin files (cascade if pin files are themselves pinned), full 64-hex pin scan helper, append `## Finish 0173` to scorer-positive-0172.md. No main(), no rewrite.
- scorer-positive-review-0173 (reviewer/default/medium, blocked_by finish, exports 763/766): own 27e7495d equality per control, numbered verdicts, in-memory mutation check, all pins of changed files, CLEAR/NOT-CLEAR.
- Next cold shaper: on merged + CLEAR, close the zero-execution scope (carry findings 4/6 minor) and move to a method gap (constant-export detection design, or XML key independent confirmation). On NOT-CLEAR, correct named findings + changed-scope review in one graph (fix_rounds 2; this is round 1 of finding 5's finish). If the finish fails the check again, inspect `git show` of the branch yourself before ordering anything; do not resume #766 a third time as a full task.

## Tried, do not repeat
- #766 full fix done on task/766; do not redo fix, main() or mutation check. Its pin helpers searched only old score.py/results hashes; scan every pin of every changed file.
- #763 findings 1-3 closed; do not re-review logic, old pins or the 558 fixture leaves.
- #758: real change is d46236b6 / iter/0165/739. #762 finished checks; do not rerun.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #739/#766: a change to any pinned file must update all its pins (Grep the path across benchmark/**/*.json) in the same task.
- #743: long inline python3 one-liners stall; use file-based helper scripts. #747 importlib helper stalled; guarded exec works.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- Tools intermittently lost (#718/#722/#754/#758): first-turn probe, early Verification.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- score.py: generate() only; main() rewrites results/challenges.json (fix/finish task only, once, guarded).
- Deriving positive expectations from score.py output is not independent (#763 finding 5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518). Explicit exports for reports.
- Expectations before author applications (#567). Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
