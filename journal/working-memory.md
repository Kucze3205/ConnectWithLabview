# Execution working memory

## Considered
- Iteration 0197 / #846: startup documents read once. Iteration 0196 closed, verdict none, not improved, 2 tasks (record .session/history/records/0196.json). no_progress=5; rollback streak 1 (0190, quiet time); outboxes 787, 837; no open requests; goal gate unaccepted; policy_rev unchanged 5e598014...
- Record 0196: #842 benchmark tool probe partial (cause session_budget at 12 turns, but table complete), branch task/842 commit dc27afe6, 1 artifact; #843 researcher tool probe partial, 12 turns, 1 artifact (report not read; not needed once the benchmark probe passed).
- #842 report (.session/reports/842.json): all 7 tools ok (Read, Grep, Glob, python3, git, Write, Edit); "disabled for this session" did not recur.
- Record 0195: #838 blocked by disabled Read/Grep, nothing saved; #839 blocked by dependency.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Positive-control thread (#763 f4): step 1 plan DONE (#820). Step 2 cold key DONE (0191). Step 3 review: F1 CLEAR (#828), F3 closed (library-specialty.json:2513), F2 answered from code (#831). Step 4 RE-ORDERED in 0197 after probe #842 passed (third order; #834/#838 failed only on tools). After CLEAR -> close the thread.
- Tool-disable pattern: #828, #831, #834, #838 plus 0-turn sessions (#794, #813) and interruptions (#788, #800, 0190). Probe #842 passed, so the block is intermittent, not role-wide. Suggestion raised in 0195 (.session/suggestions.json) still stands.
- Probe limits: 12 turns were just enough for 7 tools + report; #842/#843 ended partial (session_budget). Give probes >=16 turns.
- Deferred gap: XML key independent confirmation (after positive-control thread). Also #831: citations are never checked against the XML artifact (scorer design limit; carry).
- Carried minor findings: #809 f2, #809 f4 (silent skip when control absent); #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- CLOSED: matched comparison #722; attempt-ledger seam #703; attempt policy #685; constant-export thread (#817 CLEAR); zero-execution scorer scope (#779, #785).
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- positive-control-author-0197 (benchmark/default/medium, 60 min/45 turns): #838 body unchanged except pins file and history; adds A0001/A0002 wrong-literal and wrong-locator mutations, answers F4, regenerates challenges.json, updates pins. Exports #828, #831 reports; input 828-pins.txt.
- positive-control-review-0197 (reviewer/default/medium, 40 min/30 turns), blocked_by the author; changed-scope review, artifacts pins-0197.txt and review-0197.md.
- Expected gain: step 4 merged plus CLEAR closes the positive-control thread. Check next: author status/merged in record 0197 and the reviewer's first report line.
- If the author is blocked by tools again: do not order a fourth full attempt; escalate to the Policymaker in .session/suggestions.json with #834/#838/new issue evidence. If partial with a branch: finishing task with start_branch, <=20 turns.
- After CLEAR: move to the deferred XML key independent confirmation gap.

## Tried, do not repeat
- Positive-control gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic read (#831 F2), inventory path (F3, line 2513). Do not re-derive, re-hash or re-review these.
- Step 4 attempts #834 (0194) and #838 (0195): blocked by disabled tools. Tool probes #842/#843 (0196) done; do not probe again unless a new block appears.
- Regeneration of challenges.json: done (#812/#816, CLEAR #817).
- Keyed-literal probe (0183) and control (#808, CLEAR #809): done. Constant-export probe #791/#797 done. Mutation check #785 done. #779 done. #766/#778 re-pin done.
- Before re-ordering "paused" or failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0187-0196 at 8-11; 0197 at 9).
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
