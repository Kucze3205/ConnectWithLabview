# Execution working memory

## Considered
- Iteration 0172 / #765: startup documents read once. no_progress=0 (0171 accepted, improved). No open requests/outboxes; goal gate unaccepted.
- Record 0171: #762 benchmark done/accepted/merged (952c840e, checks-only finish of #758); #763 reviewer done, NOT-CLEAR (report snapshot .session/history/sessions/763/67b96181....md, read directly).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; results/challenges.json self-comparison (quality_measured false).
- Zero-execution change merged (#758 + #762). #763 pins: HEAD 674c29e9, score.py c2d20475..., preparation.json b19feb8e..., results/challenges.json 1c78ff28.... Findings 1-3 CLEAR (logic score.py:213-216, pins, fixture expectations: 550 correct->unverified, 8 incorrect->unverified, 114 counts; generate() 33/0).
- #763 finding 5 OPEN (being corrected in 0172): dropped baseline compare made mutation check vacuous (score.py:345-347) and the positive-execution compare at score.py:314 a tautology. Agreed replacement: authored `expected_positive` per baseline control, taken from `expected` at 27e7495d (parent of 8cb25137), not derived from score.py output.
- #763 finding 4 (minor): no fixture control exercises the `correct` path or citation-grounding failure; finding 5 fix restores it in the self-test only. Finding 6 (minor): null native_run / zero-execution cases do not assert extras_ledger; low risk, carried.
- Stall (#743/#747): NOT reproduced by #751 (scorer-stall-0168.md `## Cause`). Guarded exec probe works.
- Tool loss late in session recurs: #718/#722/#754/#758. Short task limits and early checks help (#762 worked).
- Constant-export detection not handled: deferred until the zero-execution scope closes.
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
- scorer-positive-fix-0172 (benchmark/default/medium, 50 min/40 turns, exports reports 758/762/763): add `expected_positive` from 27e7495d to baseline controls, compare baseline and mutations to it, remove tautology, re-pin, guarded self-test + generate() + one main(), in-memory mutation check; note benchmark/challenges/scorer-positive-0172.md.
- scorer-positive-review-0172 (reviewer/default/medium, blocked_by fix, exports 763): own equality helper vs 27e7495d, numbered verdicts, own in-memory mutation check, CLEAR/NOT-CLEAR.
- Next cold shaper: on done + CLEAR, close the zero-execution scope (carry findings 4/6 as minor) and move to a method gap (constant-export detection design, or XML key independent confirmation). On NOT-CLEAR, correct named findings + changed-scope review in one graph (fix_rounds limit 2). On tool-loss partial, finishing-only task on start_branch.

## Tried, do not repeat
- #763 review findings 1-3 closed; do not re-review logic, old pins or the 558 fixture leaves.
- #758: real change is d46236b6 / iter/0165/739; do not re-search. #762 finished checks; do not rerun them.
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
- score.py: generate() only; main() rewrites benchmark/results/challenges.json (only a fix/finish task may call it, once, guarded).
- Deriving positive expectations by rewriting score.py output is not independent (#763 finding 5).
- evaluation.md is Polish; Read it whole. Glob: full pattern. Inputs stage flat; counts from bytes (#518). Explicit exports for reports. Verify paths before naming (#710 F-S1).
- Expectations before author applications (#567 etc.). Reviewers write report/artifacts only.
- Engine verification: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
