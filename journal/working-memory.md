# Execution working memory

## Considered
- Iteration 0199 / #855: startup documents read once. Iteration 0198 closed, verdict none, not improved, 1 task (record .session/history/records/0198.json). no_progress=7; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; policy_rev now 79065a0f... (Policymaker #854 added the "Role tools" section to the orchestrator skill).
- Record 0198: #852 researcher partial, 26 turns, branch task/852 commit e8c4e3c2, artifacts 0 recorded, nothing merged.
- #852 report (.session/reports/852.json): located step-4 edit points (score.py 311-319, 337, 344-345, 352-353); F4 answered (inventory A0001 lines 323, 330-331; A0002 357, 364-365; scheme xml-positional-path; citation_support score.py:74 whole-dict membership; literal equality score.py:207). Not read: score.py 381-430, control A0001/A0002 claims. Stopped on "Read is disabled" message.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Positive-control thread (#763 f4): step 1 plan DONE (#820). Step 2 cold key DONE (0191). Step 3 review: F1 CLEAR (#828), F3 closed, F2 answered (#831). Step 4 F4 answered and edit points located (#852). 0199 orders apply + changed-scope review in one graph.
- Tool-disable message: Policymaker #854 says it is a native-tool refusal, not a broker failure; re-propose as JSON action. Per skill: re-order same work once with a pointer; do not split or suggest again. 0199 tasks carry that pointer.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Deferred gap: XML key independent confirmation (after positive-control thread). #831: citations never checked against the XML artifact (scorer design limit; carry).
- Carried minor findings: #809 f2, #809 f4 (silent skip when control absent); #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: any task importing benchmark/scripts/*.py uses `python3 -B`, `sys.dont_write_bytecode = True`, checks `git status --porcelain` (#785).
- CLOSED: matched comparison #722; attempt-ledger seam #703; attempt policy #685; constant-export thread (#817 CLEAR); zero-execution scorer scope (#779, #785).
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- step4-apply-0199 (benchmark/default/medium, 60 min/40 turns): adds `wrong-literal-a0001` (20008001) and `wrong-locator-a0002` (Property[3]) to `regression_self_test` in score.py, regenerates results with python3 -B, updates all pins, saves `.session/artifacts/step4-diff.txt`. Exports #852 report.
- step4-review-0199 (reviewer/default/medium, 45 min/30 turns, blocked_by apply): changed-scope review, CLEAR/NOT-CLEAR in report, evidence in artifacts/review.md.
- Check: score.py contains both control names on main; review verdict in .session/reports/<review issue>.json. If CLEAR: step 4 closed; next gap is XML key independent confirmation. If apply again stops on the tool message: do not re-order; Policymaker path.

## Tried, do not repeat
- Positive-control gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic read (#831 F2), inventory path (F3), F4 + edit points (#852). Do not re-derive these.
- Step 4 full attempts #834, #838, #848 and plan #852: stopped on the native-tool message. 0199 is the one allowed re-order with pointer.
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0199 at 8). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #739/#766: a change to any pinned file updates all its pins in the same task.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158, 0176, 0186, 0188).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
