# Execution working memory

## Considered
- Iteration 0196 / #841: startup documents read once. Iteration 0195 closed, verdict none, not improved, 2 tasks (record .session/history/records/0195.json). no_progress=4; rollback streak 1 (0190, quiet time); outboxes 787, 837; no open requests; goal gate unaccepted.
- Record 0195: #838 benchmark blocked, branch task/838 commit 058dbd51, 6 turns, 0 artifacts; #839 reviewer blocked, 0 turns (dependency).
- #838 report (.session/reports/838.json): tool probe failed: "No such tool available: Read. Read is disabled for this session..." and the same for Grep. Nothing saved, no command run.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Positive-control thread (#763 f4): step 1 plan DONE (#820). Step 2 cold key DONE (0191). Step 3 review: F1 CLEAR (#828), F3 closed (library-specialty.json:2513), F2 answered from code (#831). Step 4 BLOCKED twice by disabled file tools (#834 in 0194, #838 in 0195), nothing saved either time. PAUSED until a tool probe shows Read/Grep work. Then re-order the #838 body (record 0195, task positive-control-author-0195) unchanged, plus its review (positive-control-review-0195). After CLEAR -> close the thread.
- Tool-disable pattern: #828, #831, #834, #838 plus 0-turn sessions (#794, #813) and interruptions (#788, #800, 0190). Suggestion to the Policymaker raised in 0195 (.session/suggestions.json); no Policymaker change seen yet (policy_rev unchanged 5e598014...).
- Deferred gap: XML key independent confirmation (after positive-control thread). Also #831: citations are never checked against the XML artifact (scorer design limit; carry).
- Carried minor findings: #809 f2, #809 f4 (silent skip when control absent); #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- CLOSED: matched comparison #722; attempt-ledger seam #703; attempt policy #685; constant-export thread (#817 CLEAR); zero-execution scorer scope (#779, #785).
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- tool-probe-benchmark-0196 (benchmark/default/low, 15 min/12 turns) and tool-probe-researcher-0196 (researcher/default/low, 15 min/12 turns), parallel, no shared files (each writes its own .session/artifacts/tool-probe-<role>-0196.txt). Measurement only: Read, Grep, Glob, Bash python3, Bash git, Write, Edit, once each; per-tool table on the report's first lines.
- Expected gain: tells a role-specific tool block (benchmark only) from a global one, and whether step 4 can resume.
- Check next: both reports' tables. Benchmark ok -> re-order step 4 + review (0195 bodies). Benchmark failed but researcher ok -> role-specific; raise evidence in .session/suggestions.json, plan useful researcher-role work meanwhile. Both failed -> global; report the blocker, do not order busywork.

## Tried, do not repeat
- Positive-control gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic read (#831 F2), inventory path (F3, line 2513). Do not re-derive, re-hash or re-review these.
- Step 4 attempts #834 (0194) and #838 (0195): both blocked by disabled tools, nothing saved. Do not order the same full task a third time without a passing tool probe.
- Regeneration of challenges.json: done (#812/#816, CLEAR #817).
- Keyed-literal probe (0183) and control (#808, CLEAR #809): done. Constant-export probe #791/#797 done. Mutation check #785 done. #779 done. #766/#778 re-pin done.
- Before re-ordering "paused" or failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0187-0195 at 8-11; 0196 at 8).
- Grep alternation unreliable; use single literal patterns. Use .session/reports/index.json and .session/reports/<issue>.json for fresh reports.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #739/#766: a change to any pinned file updates all its pins in the same task.
- #743: long inline python3 one-liners stall; use file-based helpers. Guarded exec works.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158, 0176, 0186, 0188).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
