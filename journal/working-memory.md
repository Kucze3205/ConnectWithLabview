# Execution working memory

## Considered
- Iteration 0179 / #787: startup documents read once. no_progress=2. No open requests/outboxes; goal gate unaccepted. Rollback streak 1 (old, 2026-11-17).
- Record 0178 (.session/history/records/0178.json): closed, verdict none, not improved. Task #785 (scorer-positive-mutation-0178) has no session entry in outcome.sessions: never started, second time after #782 (0177).
- docs/perpetua/evaluation.md read whole: `challenges` row requires trials on wrong answers, wrong citations, constant/empty export, unsupported case.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md, table row `challenges`). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution scorer scope: CLOSED with a documented limit. #763 findings 1-3 CLEAR; finding 5 corrected by #778 (582b0afe), review #779 CLEAR on expected values and pins (static), in-memory mutation check unexecuted. Re-orders #782 and #785 never started (engine-side), so per the 0178 rule it is not ordered a third time; suggestion filed for the Policymaker (.session/suggestions.json).
- #763 finding 4 (minor, no `correct`-path/citation-grounding control) and finding 6 (minor, null native_run cases do not assert extras_ledger): carried.
- NEW thread: constant/empty-export detection (challenges row). Ordered 0179 as a measurement + design (graph task constant-export-probe-0179, its own issue; #787 is the 0179 shaper issue). Next: on design delivered, order fixture+scorer change per design and its changed-scope review in one graph; on NOT-APPLICABLE (scorer has no export input), record why and design the missing seam.
- Task-start failure: #782 and #785 (both reviewer/default/low, 15 turns) never started; if constant-export-probe-0179 (benchmark role) also never starts, the problem is not role-specific: report a concrete blocker, do not keep re-ordering.
- Iterations 0173-0175 failed (no graph / quiet-time rollbacks); 0176 ran fine.
- Tool loss late in session recurs: #718/#722/#754/#758/#779. Short limits, Bash first.
- CLOSED: matched comparison #722 CLEAR 81d309e5; attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner); attempt policy #685 CLEAR cf0c84e5.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row (constant detection — in progress; XML key independent confirmation; independent positive-control key); dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- constant-export-probe-0179 (benchmark/default/medium, 60 min/40 turns): in-memory probe of score.py with an empty and a constant export via .session/artifacts/constant_probe.py; writes benchmark/challenges/constant-export-design.md (`## Measured`, `## Design`, `## Limits`, verdicts DETECTED/NOT-DETECTED/NOT-APPLICABLE). Modifies no existing file. Check: the design file headings and per-probe verdicts; report verdicts.
- Next cold shaper: read the design and the report; order the change+review pair, or the seam design if NOT-APPLICABLE.

## Tried, do not repeat
- Mutation check of the positive guard: #782 (0177) and #785 (0178) never started. Banned to order again; accepted as documented limit of #779.
- #779 derived the independent expectation and checked all pins; do not repeat.
- #766/#778 fix and re-pin done and merged; do not redo fix, main() or pins.
- 0173 shaper read too long without a graph; write the graph by ~10th call (0177 at 11, 0178 at 9, 0179 at 11).
- History records 0171-0175 and `"source": "reports"` examples not found by Grep/Glob in .session/history; use loop-state. Session report snapshots live under .github/loop/data/session-reports/<issue>/.
- Grep for constant/export/"kind" in benchmark/ and evaluation.md returned nothing useful in 0179; the probe task reads score.py itself.
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
