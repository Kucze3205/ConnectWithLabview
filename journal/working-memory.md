# Execution working memory

## Considered
- Iteration 0169 / #753: startup documents read once. no_progress=0 (0168 accepted, improved). No open requests/outboxes; goal gate unaccepted.
- Record 0168: #751 benchmark done, accepted, merged task/751 commit 0712fdec, 22 turns. Read benchmark/challenges/scorer-stall-0168.md directly.
- Records 0165-0167 (read in earlier iterations): #739 saved fix commit 5db2610e (local ref task/739 does not exist per #751); #743, #747 stalled finishes.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution fix (#739, commit 5db2610e): score.py gives `unverified` when executed<=0, scored<=0 or native_run null; note benchmark/challenges/scorer-fix-0165.md. Missing: pins in benchmark/preparation*.json, stale fixture `expected` (#739: 5 match / 28 mismatch), native_run-null self-test, regenerated results. Ordered as finish in 0169.
- Stall (#743/#747): NOT reproduced by #751 (scorer-stall-0168.md `## Cause`: not found). Import and generate() of both versions finish <20 s with faulthandler guard, stdin on devnull, exec of source, `python3 -I`. Suspects untested: importlib load-and-print, runner stdout handling.
- Pin location unverified by shaper: Grep for `score.py` in benchmark/preparation.json found nothing; finish task must locate pins itself (benchmark/preparation.json, benchmark/preparation-status.json exist).
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
- scorer-finish-0169 (benchmark/default/medium, 60 min/45 turns, exports reports 739/747/751): restore 5db2610e files via git show, update pins, fix stale expectations caused by the fix, add native_run-null self-test, main() once. Note benchmark/challenges/scorer-finish-0169.md with `## Restored`, `## Pins`, `## Expectations`, `## Checks`.
- scorer-finish-review-0169 (reviewer/default/medium, blocked_by finish): pins HEAD and hashes itself, per-expectation verdicts, CLEAR/NOT-CLEAR in report.
- Next cold shaper: if finish done and review CLEAR, close the zero-execution scope and move to a method gap (constant-export detection design, or XML key independent confirmation). If NOT-CLEAR, correct named findings + changed-scope review in one graph. If finish stalls again with frames, order one narrow fix of the named frame; if stall without frames, file a runner suggestion in .session/suggestions.json and switch to non-execution work.

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. gap-0160 (#725), scorer-probe-0164 (#736), positive-control cause (#739), stall probe (#751): do not re-survey or re-probe.
- #739: a score.py change without updating pins and stale fixture expectations fails the engine check (same as #117/#122). Any change to a pinned file must update its pin in the same task.
- #743: long inline python3 one-liners stall the runner / break on `\n`; use file-based helper scripts.
- #747: importlib load-and-print helper stalled; #751 guarded exec probe works.
- 0150 #689 / 0151 #692 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #718/#722: reviewer tools intermittently "No such tool available"; keep a first-turn tool probe.
- Broad Budget at high effort exhausts input; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- score.py: generate() only; main() rewrites benchmark/results/challenges.json (only the finish task may call it).
- evaluation.md is Polish; Read it whole. Glob: full pattern. Inputs stage flat; counts from bytes (#518). Explicit exports for reports. Verify paths before naming (#710 F-S1).
- Expectations before author applications (#567 etc.). Reviewers write report/artifacts only.
- Engine verification: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
