# Execution working memory

## Considered
- Iteration 0164 / #735: startup documents read once. no_progress=3 (0161-0163 failed). No open requests/outboxes; goal gate unaccepted.
- Records 0160-0163. 0160 #725 benchmark done/accepted/merged a6fd4304: benchmark/challenges/gap-0160.md (read whole). 0161 (#727 crashed), 0162 (Policymaker #729), 0163 (#731 crashed) all failed with "invalid policy script output: policy/session-state.py printed more than 8388608 bytes". Engine/Policymaker-side failure, not an execution task failure.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0. Glob confirmed benchmark/scripts/score.py exists. No task/product/benchmark/evaluator/native execution ran in the shaper.

## State
- OPEN challenges row (evaluation.md line 69). gap-0160 (#725): all five kinds `partial`; all evidence is author-written synthetic fixtures; benchmark/results/challenges.json 33/33 is self-comparison (quality_measured false). Cross-cutting gap: no scorer shown to deny credit; XML keys not independently confirmed; native controls unverifiable. score.py and preparation-status.json were not inspected by #725 -> 0164 scorer probe.
- 0161-0163 failure cause: policy/session-state.py output over 8 MiB. Belongs to Policymaker (policy/ not visible to execution). If 0164 fails the same way, do not change the graph; note it again and keep the graph small.
- CLOSED matched comparison contract: #722 CLEAR at 81d309e5 (matched-comparison-0155.md 15d6be1e...0933, .json 82016b83...ec85). Do not reopen.
- CLOSED attempt-ledger seam #703 CLEAR 48f2715e (F-A1, F-A2 open for owner). CLOSED attempt policy #685 CLEAR cf0c84e5, design only.
- Real-envelope authority separate and unresolved; legacy multiple-attempt selection unresolved; no retrospective selection.
- REUSE runner SHA256 arm order, 0138 per-arm repetition mechanism, project-paired-0136 design, precision sizing, lineage/freeze procedure. No gap re-survey/count redesign/synthetic-to-real promotion.
- Remaining method gaps: challenges row (scorer, key confirmation); dependency/native keys/access/grants/logs; restricted split/allocation/executed isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Admissions, model/reader/native executions, scored runs, real comparisons: zero.
- Closed: lineage e15a5033; grouping 51e672d0; #639 bb3f5312; #633 8d824c68; #622/#625/#626 60a4a737.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW. POC code researcher-only.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined.
- #533 source-blocked. W1-W8 closed d3c697c3; AF declarations 371c631c. WP1 #544 checker invalidated (benchmark/writing/check_c1_challenges_0125.py): never run.

## This iteration
- scorer-probe-0164: benchmark/default/medium, 60 min/40 turns. Measure-only: per challenge kind, what benchmark/scripts/score.py does (code expectation first, then run on committed synthetic fixtures if offline-runnable, output to .session/artifacts/). Output benchmark/challenges/scorer-probe-0164.md with the five kind headings plus `## Pins`, `## Not counted`. Verification: python3 heading check.
- Expected gain: verdict per kind (denies-credit / gives-credit / not-handled / not-runnable) with line refs. Next cold shaper: if any kind gives credit or is not handled, order one narrow benchmark correction of score.py for those kinds plus a reviewer `blocked_by` it in the same graph; if all deny credit, order an independent reviewer of the probe; then the XML key independent confirmation.

## Tried, do not repeat
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722 stay closed. gap-0160 (#725) done: do not re-survey challenge coverage.
- 0150 #689 / 0151 #692 combined files+artifacts partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #718/#722: reviewer tools intermittently "No such tool available"; keep a first-turn tool probe in review tasks.
- Broad Budget at high effort exhausts input; name extraction methods and an early write deadline.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- evaluation.md is Polish; Read it whole. Glob: full pattern. Inputs stage flat; counts from bytes (#518). Explicit exports for reports. Verify paths before naming (#710 F-S1).
- Expectations before author applications (#567 etc.). Reviewers write report/artifacts only.
- Engine verification: repository-only checks. No shell expansion/native tools.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
