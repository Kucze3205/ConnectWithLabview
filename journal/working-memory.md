# Execution working memory

## Considered
- Iteration 0171 / #761: startup documents read once. no_progress=2 (0170 closed, not improved). No open requests/outboxes; goal gate unaccepted.
- Record 0170: #758 benchmark partial (43 turns, task/758 commit 7e1d0cab, Bash lost at end, Verification never run); #759 reviewer blocked (dependency, 0 turns). Read #758 report snapshot (.session/history/sessions/758/7941a1f1....md) directly.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution fix: #758 FOUND the real change at d46236b6 (tag iter/0165/739, score.py SHA256 296e2354...), restored it, added native_run-null isolated self-test, dropped baseline `compare` vs control `expected` in regression_self_test (new score.py SHA256 c2d20475...), updated 26 controls in library-icon-tests.json + 2 in library-specialty.json to `unverified`, pins in preparation.json, writing/c1-challenges-0125-pins.json, writing/input-pins.json, writing/reviews-0128/c1-artifact-manifest-0126.json; main() ran once; generate() 33 match / 0 mismatch; note benchmark/challenges/scorer-finish-0170.md. Unverified: Verification one-liner not run. Saved on task/758 (not merged).
- Open question for review: does dropping the baseline compare remove a regression guard (#758 report "Self-test changes").
- Stall (#743/#747): NOT reproduced by #751 (scorer-stall-0168.md `## Cause`). Guarded exec probe works.
- Tool loss late in session recurs: #718/#722/#754/#758. Short task limits help.
- Positive-control cause (#739): `unverified` from provisional key and missing native refs; intended.
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
- scorer-finish-check-0171 (benchmark/default/low, start_branch task/758, 30 min/20 turns, exports report 758): checks only — Verification one-liner, pin-hash helper, guarded self-test + generate() totals; append to note `## Checks`. No rewrite, no main().
- scorer-finish-review-0171 (reviewer/default/medium, blocked_by check): pins HEAD and hashes, per-expectation verdicts, own verdict on the dropped baseline compare, CLEAR/NOT-CLEAR.
- Next cold shaper: if done + CLEAR, close zero-execution scope; move to a method gap (constant-export detection design, or XML key independent confirmation). If NOT-CLEAR, correction + changed-scope review in one graph. If the finishing task fails again from tool loss, file a runner suggestion in .session/suggestions.json; do not resume the full #758 task (finishing-only already used once now).

## Tried, do not repeat
- #758: real change is d46236b6 / iter/0165/739; do not re-search. Do not rerun main() or update scripts on task/758.
- #754: `git show 5db2610e` is empty. Report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. gap-0160 (#725), scorer-probe-0164 (#736), positive-control cause (#739), stall probe (#751): do not re-survey or re-probe.
- #739: a score.py change without updating pins and stale fixture expectations fails the engine check (#117/#122). Any change to a pinned file must update its pin in the same task.
- #743: long inline python3 one-liners stall the runner / break on `\n`; use file-based helper scripts.
- #747: importlib load-and-print helper stalled; #751 guarded exec probe works.
- 0150 #689 / 0151 #692 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #718/#722/#754/#758: tools intermittently "No such tool available"/disabled; keep a first-turn tool probe and run Verification early.
- Broad Budget at high effort exhausts input; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- score.py: generate() only; main() rewrites benchmark/results/challenges.json (only a finish task may call it).
- evaluation.md is Polish; Read it whole. Glob: full pattern. Inputs stage flat; counts from bytes (#518). Explicit exports for reports. Verify paths before naming (#710 F-S1).
- Expectations before author applications (#567 etc.). Reviewers write report/artifacts only.
- Engine verification: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
