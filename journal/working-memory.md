# Execution working memory

## Considered
- Iteration 0185 / #804: startup documents read once. no_progress=2 (0183 #800 paused; 0184 failed: no valid graph). Outbox 787 pending; no open requests; goal gate unaccepted. Rollback streak 1 (old, 2026-11-17).
- Record 0184 (.session/history/records/0184.json): failed, "the shaper produced no valid task graph". Shaper #802 report (.github/loop/data/session-reports/802/897750b5...json) ends with the engine error: start_branch `task/800` is on origin neither as a branch nor as an `iter/*` tag.
- Record 0183 (.session/history/records/0183.json): one task keyed-literal-probe-0183 = #800, paused (providers unavailable); no iter tag exists for it.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md, row `challenges`). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Constant/empty-export detection: CLOSED for empty (DETECTED score.py:203-204), non-keyed constant (DETECTED score.py:207-208), vi-actor-core-native-gap NOT-APPLICABLE (score.py:199-200); merged by #797. Open: keyed-literal constant (fresh probe ordered 0185) and whether `constant` controls / `regression_self_test` exist.
- Next after the probe lands: if SAFE, order the `constant-keyed-literal-export` control addition (fixtures + regression assertion, all pins updated) and its changed-scope review in one graph; if UNSAFE, order the scorer correction plus review in one graph.
- Zero-execution scorer scope: CLOSED (#779 CLEAR; #785 mutation check CLEAR, merge refused for .pyc only). Do not re-run.
- #763 finding 4 (minor, no `correct`-path/citation-grounding control) and finding 6 (minor, null native_run cases do not assert extras_ledger): carried.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- Sessions with 0 turns (#794), runtime interruption (#788) or provider unavailability pause (#800) recur; if the 0185 probe also pauses, file a suggestion to the Policymaker instead of re-ordering.
- Tool loss mid-session recurs: #718/#722/#754/#758/#779/#788/#791. Short limits, save files first.
- CLOSED: matched comparison #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row (keyed-literal constant control; XML key independent confirmation; independent positive-control key); dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- keyed-literal-probe-0185 (benchmark/default/medium, fresh, no start_branch, 45 min/30 turns): measure keyed-literal constant export via score.compute in memory; report, do not fix. Check: Glob benchmark/challenges/keyed-literal-probe-0185.md on main; read its SAFE/UNSAFE verdicts and `## Existing controls`.

## Tried, do not repeat
- Paused task branches are NOT resumable: #800 (paused) left no `task/800` branch or `iter/*` tag; 0184 failed on start_branch task/800. Only use start_branch for an `iter/NNNN/N` tag or branch confirmed in a record/report; a paused session without such a tag gets a fresh task.
- Keyed-literal probe: 0183 #800 paused; 0184 resume refused; 0185 fresh. Do not order it a fourth time; suggest to Policymaker instead.
- Constant-export probe (empty, non-keyed): done by #791, merged by #797. Do not re-probe.
- Mutation check of the positive guard: done by #785 (CLEAR). Do not order again.
- #779 derived the independent expectation and checked all pins; do not repeat.
- #766/#778 fix and re-pin done and merged; do not redo fix, main() or pins.
- Write the graph by ~10th call (0177 at 11 ... 0184 at 10, 0185 at 11).
- Before calling a task "no report", Glob .session/history/sessions/<issue>/ for a snapshot other than task.md and read it; brace Glob patterns return nothing, use `sessions/80*/**`-style patterns.
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
