# Execution working memory

## Considered
- Iteration 0170 / #757: startup documents read once. no_progress=1 (0169 closed, not improved). No open requests/outboxes; goal gate unaccepted.
- Record 0169: #754 benchmark blocked (11 turns, commit fee03868, nothing changed); #755 reviewer blocked (dependency, 0 turns). Read #754 report snapshot and #739 report snapshot directly.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution fix (#739): commit 5db2610e named in #739 report is EMPTY (#754: `git diff --name-status 2c2150bf 5db2610e` prints nothing). Real change identity from #739 report: score.py SHA256 810a5457... -> 296e2354e312d5a69fe62e9629bc085376c0fa523fbf21ad6601fdf1dad8def8 at HEAD 2f91dff5. Behaviour: compute returns `unverified` when executed<=0, scored<=0, or native_run present and null. Missing on main: the change itself, pins, 28 stale fixture expectations (#739: 5 match / 28 mismatch), native_run-null isolated self-test, regenerated results. Ordered 0170: locate by hash in tags/branches/log, else reimplement.
- Stall (#743/#747): NOT reproduced by #751 (scorer-stall-0168.md `## Cause`). Guarded exec probe works; importlib load-and-print stalled.
- #754 saw Read/Bash/Write tools "disabled" late in the session (same intermittent tool loss as #718/#722).
- Positive-control cause (#739): `unverified` from provisional key and missing native refs; intended, not a bug.
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
- scorer-finish-0170 (benchmark/default/medium, 60 min/50 turns, exports reports 739/751/754): locate the real score.py by SHA256 296e2354 in iter/0165 tags, *739* branches, git log; else reimplement by hand by turn 12. Then pins, stale expectations, isolated native_run-null self-test, main() once. Note benchmark/challenges/scorer-finish-0170.md with `## Source`, `## Restored`, `## Pins`, `## Expectations`, `## Checks`.
- scorer-finish-review-0170 (reviewer/default/medium, blocked_by finish): pins HEAD and hashes itself, per-expectation verdicts, CLEAR/NOT-CLEAR.
- Next cold shaper: if done + CLEAR, close zero-execution scope and move to a method gap (constant-export detection design, or XML key independent confirmation). If NOT-CLEAR, correction + changed-scope review in one graph. If blocked by tool loss again, file a runner suggestion in .session/suggestions.json and switch to non-execution work. Never resume this full task a third time.

## Tried, do not repeat
- #754: `git show 5db2610e` is empty; do not restore from it. Report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. gap-0160 (#725), scorer-probe-0164 (#736), positive-control cause (#739), stall probe (#751): do not re-survey or re-probe.
- #739: a score.py change without updating pins and stale fixture expectations fails the engine check (same as #117/#122). Any change to a pinned file must update its pin in the same task.
- #743: long inline python3 one-liners stall the runner / break on `\n`; use file-based helper scripts.
- #747: importlib load-and-print helper stalled; #751 guarded exec probe works.
- 0150 #689 / 0151 #692 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #718/#722/#754: tools intermittently "No such tool available"/disabled; keep a first-turn tool probe.
- Broad Budget at high effort exhausts input; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- score.py: generate() only; main() rewrites benchmark/results/challenges.json (only the finish task may call it).
- evaluation.md is Polish; Read it whole. Glob: full pattern. Inputs stage flat; counts from bytes (#518). Explicit exports for reports. Verify paths before naming (#710 F-S1).
- Expectations before author applications (#567 etc.). Reviewers write report/artifacts only.
- Engine verification: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
