# Execution working memory

## Considered
- Iteration 0187 / #811: startup documents read once. no_progress=0 (0186 accepted, improved); outbox 787 pending; no open requests; goal gate unaccepted. Rollback streak 1 (old, 2026-11-17).
- Record 0186 (.session/history/records/0186.json): #808 benchmark done, accepted, merged 14cbd047 (added `constant-keyed-literal-export` control to both claim-bearing fixtures, regression assertion score.py:297-309, pins updated); #809 reviewer done, CLEAR (report .github/loop/data/session-reports/809/cb3554f1....json). Finding 2 minor wording; finding 4 note: `if keyed is not None` skips silently if control removed; finding 6: results/challenges.json embeds old fixture hashes (stale), old hashes also in scorer-positive-0172.md.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md, row `challenges`). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Constant-export thread: CLOSED by #808/#809 CLEAR (empty, non-keyed, keyed-literal all measured and controlled). Only follow-up: stale results/challenges.json (ordered 0187).
- Carried minor findings: #809 f2 (control note wording), #809 f4 (silent skip when control absent); #763 f4 (no `correct`-path/citation-grounding control), #763 f6 (null native_run cases do not assert extras_ledger).
- Next after 0187: if regen review CLEAR, reassess remaining method gaps: XML key independent confirmation; independent positive-control key. Pick one, name gap and gain here. If NOT-CLEAR, correct named findings + changed-scope review in one graph.
- Zero-execution scorer scope: CLOSED (#779 CLEAR; #785 mutation check CLEAR). Do not re-run.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- Sessions with 0 turns (#794), runtime interruption (#788), provider pause (#800) recur. Tool loss mid-session recurs (#718/#722/#754/#758/#779/#788/#791): short limits, save files first.
- CLOSED: matched comparison #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row (XML key independent confirmation; independent positive-control key); dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- challenges-regen-0187 (benchmark/default/medium, 50 min/35 turns): run score.py `main()` once, guarded; update all pins of results/challenges.json; output benchmark/challenges/challenges-regen-0187.md (`## Diff`, `## Pins`, `## Checks`, `## Limits`). Stop and report if any outcome other than the new control/hashes changes.
- challenges-regen-review-0187 (reviewer/default/medium, blocked_by above, 40 min/30 turns): changed-scope review, CLEAR/NOT-CLEAR in report + artifact challenges-regen-review.md.
- Check: Glob benchmark/challenges/challenges-regen-0187.md; read the review session report for the verdict.

## Tried, do not repeat
- Keyed-literal probe (0183) and control (#808, CLEAR #809): done. Do not probe or add controls again.
- Before re-ordering "paused" work, Glob its expected output on main first: #800 was recorded paused but its md landed.
- Paused task branches are NOT resumable: no `task/800` branch or `iter/*` tag; 0184 failed on start_branch. Only use start_branch for a confirmed `iter/NNNN/N` tag or branch.
- Constant-export probe (empty, non-keyed): done by #791, merged by #797. Do not re-probe.
- Mutation check of the positive guard: done by #785 (CLEAR). Do not order again.
- #779 derived the independent expectation and checked all pins; do not repeat.
- #766/#778 fix and re-pin done and merged; do not redo fix, main() or pins.
- Write the graph by ~10th call (0185 at 11, 0186 at 12, 0187 at 8).
- Grep patterns with alternation are unreliable here; prefer Glob + Read.
- Session report snapshots: .session/history/sessions/<issue>/<sha>.md and .github/loop/data/session-reports/<issue>/.
- #763 findings 1-3 closed; do not re-review logic, old pins or the 558 fixture leaves.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #739/#766: a change to any pinned file must update all its pins (Grep the path across benchmark/**/*.json) in the same task.
- #743: long inline python3 one-liners stall; use file-based helper scripts. #747 importlib helper stalled; guarded exec works.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158, 0176, 0186).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- score.py: generate() only; main() rewrites results/challenges.json (fix/finish task only, once, guarded; ordered 0187).
- Deriving positive expectations from score.py output is not independent (#763 finding 5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Expectations before author applications (#567). Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Avoid `\\0` in verification strings; use bytes(1). Empty Write erases files. Read report before Finish.
