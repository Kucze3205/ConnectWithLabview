# Execution working memory

## Considered
- Iteration 0180 / #790: startup documents read once. no_progress=3. Outbox 787 pending; no open requests; goal gate unaccepted. Rollback streak 1 (old, 2026-11-17).
- Record 0179 (.session/history/records/0179.json): closed, verdict none. Task constant-export-probe-0179 (#788) has only task.md in .session/history/sessions/788/; no report, no session entry.
- Session report #785 (.session/history/sessions/785/da40b75d...md): it DID run (status blocked). Reviewer verdict CLEAR on the in-memory mutation check; merge refused because importing score.py wrote benchmark/scripts/__pycache__/score.cpython-314.pyc outside write paths. Earlier memory "never started" was wrong for #785; #782 report snapshot exists (.github/loop/data/session-reports/782/) but not inspected in detail.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md, row `challenges`). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution scorer scope: CLOSED. #779 CLEAR on expected values and pins; #785 report: mutation check of positive guard (score.py lines 294-296) CLEAR for both fixtures, artifacts iter-0178/785-mutation-output.txt and 785-mutation_check.py. Merge refused only for the .pyc; review result stands as evidence; no repository file was needed. Do not re-run.
- #763 finding 4 (minor, no `correct`-path/citation-grounding control) and finding 6 (minor, null native_run cases do not assert extras_ledger): carried.
- Constant/empty-export detection (challenges row): #788 (0179) left no report; re-ordered 0180 as constant-export-probe-0180 with `python3 -B` / no __pycache__. Next: on design delivered, order fixture+scorer change per design and its changed-scope review in one graph; on NOT-APPLICABLE, design the missing seam. If 0180 also leaves no report, inspect its branch/tag iter/0180/* and report a concrete blocker rather than re-ordering.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain`; otherwise merge is refused (#785).
- Iterations 0173-0175 failed (no graph / quiet-time rollbacks); 0176+ ran fine.
- Tool loss late in session recurs: #718/#722/#754/#758/#779. Short limits, Bash first.
- CLOSED: matched comparison #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row (constant detection in progress; XML key independent confirmation; independent positive-control key); dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- constant-export-probe-0180 (benchmark/default/medium, 60 min/40 turns): same probe as #788 plus no-bytecode rule; writes benchmark/challenges/constant-export-design.md (`## Measured`, `## Design`, `## Limits`, verdicts DETECTED/NOT-DETECTED/NOT-APPLICABLE); modifies no existing file. Check: verification asserts headings, a verdict word, and no benchmark/scripts/__pycache__.
- Next cold shaper: read the design and the report; order the change+review pair, or the seam design if NOT-APPLICABLE.

## Tried, do not repeat
- Mutation check of the positive guard: done by #785 (CLEAR, merge refused for .pyc only). Do not order again.
- #779 derived the independent expectation and checked all pins; do not repeat.
- #766/#778 fix and re-pin done and merged; do not redo fix, main() or pins.
- 0173 shaper read too long without a graph; write the graph by ~10th call (0177 at 11, 0178 at 9, 0179 at 11, 0180 at 12).
- Before calling a task "never started", Glob .session/history/sessions/<issue>/ for a report snapshot (0178/0179 missed #785's report).
- Session report snapshots: .session/history/sessions/<issue>/<sha>.md and .github/loop/data/session-reports/<issue>/.
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
