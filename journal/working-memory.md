# Execution working memory

## Considered
- Iteration 0189 / #819: startup documents read once. no_progress=0 (0188 accepted, improved); outbox 787 pending; no open requests; goal gate unaccepted. Rollback streak 1 (old, 2026-11-17).
- Record 0188 (.session/history/records/0188.json): #816 benchmark finish done, merged (f248bedf), check pass; #817 reviewer done, not merged (review only).
- #817 report (.github/loop/data/session-reports/817/884955975e87....json): CLEAR on commit 86408131. Diff confined (4 changed, 1022 added, 0 removed; controls 33->35); pins match; historical snapshots c1-challenges-0125-pins.json and reviews-0128/c1-artifact-manifest-0126.json correctly left unchanged. Minor: did not re-run git status after last read-only checks.
- docs/perpetua/evaluation.md:69 row `challenges` (Grep only this iteration).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Constant-export thread and its regeneration: CLOSED by #808/#809 CLEAR and #812/#816 + #817 CLEAR. Do not reopen.
- Chosen next gap (0189): independent positive-control key (#763 f4: no `correct`-path/citation-grounding control). Gain: a control that proves the scorer can award `correct`, derived without score.py output (#763 f5). Step 1 = measure + plan (this iteration); step 2 = cold key derivation by a separate session; step 3 = author control + review.
- Deferred gap: XML key independent confirmation (after positive-control thread, or in parallel if a plan shows disjoint files).
- Carried minor findings: #809 f2 (control note wording), #809 f4 (silent skip when control absent); #763 f6 (null native_run cases do not assert extras_ledger).
- Zero-execution scorer scope: CLOSED (#779 CLEAR; #785 mutation check CLEAR). Do not re-run.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- Sessions with 0 turns (#794, #813), runtime interruption (#788), provider pause (#800) recur. Tool loss mid-session recurs: short limits, save files first.
- CLOSED: matched comparison #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row (positive-control key; XML key confirmation); dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- positive-control-key-plan-0189 (benchmark/default/medium, 45 min/35 turns): measure-only; writes benchmark/challenges/positive-control-plan-0189.md (## Gap with script counts of controls expecting `correct`, ## Independent derivation, ## Proposed control, ## Limits). No fixture/score.py/results edits.
- Check: record 0189 merged status; plan file headings; whether `## Gap` confirms zero positive controls. Next: order the cold key derivation session named in `## Proposed control` (separate session, key saved in artifacts before reading author material), then authoring + review.

## Tried, do not repeat
- Regeneration of challenges.json: done (#812/#816, CLEAR #817). Do not regenerate or re-review.
- Verification paths: score.py writes benchmark/results/challenges.json; benchmark/cases/dev/ holds copies of library-*.json not read by score.py. Glob a path before asserting it in a check (#812).
- Keyed-literal probe (0183) and control (#808, CLEAR #809): done.
- Before re-ordering "paused" work, Glob its expected output on main first (#800).
- Paused task branches are NOT resumable (no task/800). Partial with recorded branch is the resumable case (#812 -> #816 worked).
- Constant-export probe: done by #791, merged by #797.
- Mutation check of the positive guard: done by #785 (CLEAR).
- #779 derived the independent expectation and checked all pins; do not repeat.
- #766/#778 fix and re-pin done and merged.
- Write the graph by ~10th call (0185 at 11, 0186 at 12, 0187 at 8, 0188 at 9, 0189 at 9).
- Grep patterns with alternation are unreliable here; prefer Glob + Read.
- Session report snapshots: .session/history/sessions/<issue>/<sha>.md and .github/loop/data/session-reports/<issue>/.
- #763 findings 1-3 closed; do not re-review logic, old pins or the 558 fixture leaves.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #739/#766: a change to any pinned file must update all its pins in the same task.
- #743: long inline python3 one-liners stall; use file-based helper scripts. #747 importlib helper stalled; guarded exec works.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158, 0176, 0186, 0188).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 finding 5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Expectations before author applications (#567). Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Avoid `\\0` in verification strings; use bytes(1). Empty Write erases files. Read report before Finish.
