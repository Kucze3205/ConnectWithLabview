# Execution working memory

## Considered
- Iteration 0195 / #837: startup documents read once. Iteration 0194 closed, verdict none, not improved, 2 tasks (record 0194). no_progress=3; rollback streak 1 (0190, quiet time); outbox 787 pending; no open requests; goal gate unaccepted.
- Record .session/history/records/0194.json: #834 benchmark blocked, branch task/834 commit b1074717, 8 turns, 0 artifacts; #835 reviewer blocked, 0 turns (dependency).
- #834 report (.session/reports/834.json): file tools returned "disabled for this session"; nothing saved, no file read. Step 4 work not started.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Positive-control thread (#763 f4): step 1 plan DONE (#820). Step 2 cold key DONE (0191). Step 3 review: F1 CLEAR (#828), F3 closed (library-specialty.json:2513), F2 answered from code (#831). Step 4 ordered 0194 (#834) BLOCKED by disabled tools, nothing saved; re-ordered 0195 unchanged plus a tool probe first. After CLEAR -> close thread.
- Tool-disable pattern: #828, #831, #834 (three in a row) plus 0-turn sessions (#794, #813) and interruptions (#788, #800, 0190). Suggestion raised to the Policymaker in 0195 (.session/suggestions.json). If 0195 is blocked the same way, do not order the same task a third time: order one short measurement-only task (tool probe + report) or wait for Policymaker action.
- Deferred gap: XML key independent confirmation (after positive-control thread). Also #831: citations are never checked against the XML artifact (scorer design limit; carry).
- Carried minor findings: #809 f2, #809 f4 (silent skip when control absent); #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- CLOSED: matched comparison #722; attempt-ledger seam #703; attempt policy #685; constant-export thread (#817 CLEAR); zero-execution scorer scope (#779, #785).
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- positive-control-author-0195 (benchmark/default/medium, 60 min/45 turns): same work as #834 (A0001/A0002 wrong-literal/wrong-citation mutations in score.py self-test, F4 from inventory citation dicts, regenerate challenges.json, update pins incl. fixture `inventory_sha256` if the inventory changes); first acceptance item is a tool probe. Exports #828/#831/#834 reports, input #828 pins.txt.
- positive-control-review-0195 (reviewer/default/medium, 40 min/30 turns), blocked_by author: pins-0195.txt first, self-test on temp copy, verdict.
- Check next: author status and tool probe line; review verdict. CLEAR -> close positive-control thread, pick next method gap. NOT-CLEAR -> correct named findings only.

## Tried, do not repeat
- Positive-control gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic read (#831 F2), inventory path (F3, line 2513). Do not re-derive, re-hash or re-review these.
- Step 4 attempt #834 (0194): blocked by disabled tools, no branch content to resume (nothing saved).
- Regeneration of challenges.json: done (#812/#816, CLEAR #817).
- Keyed-literal probe (0183) and control (#808, CLEAR #809): done. Constant-export probe #791/#797 done. Mutation check #785 done. #779 done. #766/#778 re-pin done.
- Before re-ordering "paused" or failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0187-0194 at 8-10; 0195 at 11).
- Grep alternation unreliable (`inventory_(path|sha256)` returned nothing); use single literal patterns. Glob of history sessions/session-reports for fresh issues returns nothing; use .session/reports/index.json and .session/reports/<issue>.json.
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
