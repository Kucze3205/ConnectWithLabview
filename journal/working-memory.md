# Execution working memory

## Considered
- Iteration 0198 / #851: startup documents read once. Iteration 0197 closed, verdict none, not improved, 2 tasks (record .session/history/records/0197.json). no_progress=6; rollback streak 1 (0190, quiet time); outboxes 787, 837; no open requests; goal gate unaccepted; policy_rev now eab63e96... (changed from 5e598014).
- Record 0197: #848 benchmark step-4 author blocked at 10 turns, branch task/848 commit de641e19, nothing changed; #849 reviewer blocked by dependency (0 turns); shaper #847 crashed after 21 turns (graph from #846 used).
- #848 report (.session/reports/848.json): Read worked twice, then Read and Grep "disabled for this session"; Grep returned empty matches on existing benchmark/scripts/score.py.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Positive-control thread (#763 f4): step 1 plan DONE (#820). Step 2 cold key DONE (0191). Step 3 review: F1 CLEAR (#828), F3 closed (library-specialty.json:2513), F2 answered from code (#831). Step 4 failed three times on tools (#834, #838, #848). 0198 SPLITS it: read-only researcher patch plan (artifact step4-patch.md), then a short apply task (<=15 turns) and a changed-scope review.
- Tool-disable pattern: #828, #831, #834, #838, #848 plus 0-turn sessions (#794, #813) and interruptions (#788, #800, 0190). Probe #842 passed: intermittent, turn-dependent (disable after ~3 turns in #848). Suggestion re-raised in 0198 .session/suggestions.json with #848 evidence.
- Grep empty-match on existing file (#848): tasks must fall back to Read in ranges.
- Deferred gap: XML key independent confirmation (after positive-control thread). Also #831: citations are never checked against the XML artifact (scorer design limit; carry).
- Carried minor findings: #809 f2, #809 f4 (silent skip when control absent); #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- CLOSED: matched comparison #722; attempt-ledger seam #703; attempt policy #685; constant-export thread (#817 CLEAR); zero-execution scorer scope (#779, #785).
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- step4-patch-plan-0198 (researcher/default/medium, 45 min/30 turns): no repository edits; writes `.session/artifacts/step4-patch.md` with exact old/new score.py text for A0001 wrong-literal and A0002 wrong-locator mutations, F4 answer with inventory lines, file/pin list and regeneration commands. Exports #828, #831, #848 reports; input 828-pins.txt.
- Expected gain: artifact exists and record 0198 shows it (artifacts >= 1). Next: order an apply task (benchmark, <=15 turns, input `{issue: <this task's issue>, name: step4-patch.md}`) plus a blocked_by changed-scope review in one graph.
- If the researcher is also blocked by tools: stop ordering step 4; the Policymaker suggestion is the path; move to independent work that needs few turns.

## Tried, do not repeat
- Positive-control gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic read (#831 F2), inventory path (F3, line 2513). Do not re-derive, re-hash or re-review these.
- Step 4 full attempts #834 (0194), #838 (0195), #848 (0197): blocked by disabled tools. Do not order a fourth full author attempt. Tool probes #842/#843 (0196) done.
- Regeneration of challenges.json: done (#812/#816, CLEAR #817).
- Keyed-literal probe (0183) and control (#808, CLEAR #809): done. Constant-export probe #791/#797 done. Mutation check #785 done. #779 done. #766/#778 re-pin done.
- Before re-ordering "paused" or failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0187-0198 at 8-11; 0198 at 8). Shaper #847 crashed at 21 turns: stay short.
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
