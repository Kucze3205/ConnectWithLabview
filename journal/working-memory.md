# Execution working memory

## Considered
- Iteration 0186 / #807: startup documents read once. no_progress=3; outbox 787 pending; no open requests; goal gate unaccepted. Rollback streak 1 (old, 2026-11-17).
- Record 0185 (.session/history/records/0185.json): closed, one task keyed-literal-probe-0185 = #805; .session/history/sessions/805/ holds only task.md (no report snapshot); benchmark/challenges/keyed-literal-probe-0185.md does not exist on main.
- benchmark/challenges/keyed-literal-probe-0183.md IS on main (read whole): SAFE for library-icon-tests and library-specialty (all 12 claim sources, 24 mutations each), vi-actor-core-native-gap NOT-APPLICABLE; existing `constant-export` control in both claim-bearing fixtures (contents unread); `regression_self_test` at score.py:283. So the 0183 probe did produce its result despite the "paused" record; the 0185 re-run was redundant.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md, row `challenges`). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Constant-export detection: empty, non-keyed (#791/#797) and keyed-literal (probe-0183, SAFE) all measured. Open: whether a fixture control records the keyed-literal case (ordered 0186).
- Next after 0186: if review CLEAR, the constant-export thread closes; reassess the remaining method gaps below (likely XML key independent confirmation or independent positive-control key). If NOT-CLEAR, correct the named findings and review the changed scope in one graph.
- Zero-execution scorer scope: CLOSED (#779 CLEAR; #785 mutation check CLEAR). Do not re-run.
- #763 finding 4 (minor, no `correct`-path/citation-grounding control) and finding 6 (minor, null native_run cases do not assert extras_ledger): carried.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- Sessions with 0 turns (#794), runtime interruption (#788), provider pause (#800) recur. no_progress=3: Policymaker trigger likely.
- Tool loss mid-session recurs: #718/#722/#754/#758/#779/#788/#791. Short limits, save files first.
- CLOSED: matched comparison #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row (XML key independent confirmation; independent positive-control key); dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- keyed-literal-control-0186 (benchmark/default/medium, 60 min/40 turns): read existing `constant-export` controls; ADDED `constant-keyed-literal-export` control + regression assertion + all pins, or ALREADY-COVERED. Output benchmark/challenges/keyed-literal-control-0186.md (`## Overlap`, `## Change`, `## Checks`, `## Limits`).
- keyed-literal-control-review-0186 (reviewer/default/medium, blocked_by the above, 45 min/30 turns): changed-scope review, CLEAR/NOT-CLEAR in its report + artifact keyed-literal-control-review.md.
- Check: Glob benchmark/challenges/keyed-literal-control-0186.md; read the review session report for the verdict.

## Tried, do not repeat
- Keyed-literal probe: done (benchmark/challenges/keyed-literal-probe-0183.md). Do not probe again (0183, 0184 refused, 0185 redundant).
- Before re-ordering "paused" work, Glob its expected output on main first: #800 was recorded paused but its md landed.
- Paused task branches are NOT resumable: no `task/800` branch or `iter/*` tag; 0184 failed on start_branch. Only use start_branch for a confirmed `iter/NNNN/N` tag or branch.
- Constant-export probe (empty, non-keyed): done by #791, merged by #797. Do not re-probe.
- Mutation check of the positive guard: done by #785 (CLEAR). Do not order again.
- #779 derived the independent expectation and checked all pins; do not repeat.
- #766/#778 fix and re-pin done and merged; do not redo fix, main() or pins.
- Write the graph by ~10th call (0185 at 11, 0186 at 12).
- Grep with alternation `"constant-export"|keyed|...` over benchmark/challenges returned nothing although the probe file names it; Grep patterns are unreliable here, prefer Glob + Read.
- Session report snapshots: .session/history/sessions/<issue>/<sha>.md and .github/loop/data/session-reports/<issue>/.
- #763 findings 1-3 closed; do not re-review logic, old pins or the 558 fixture leaves.
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
