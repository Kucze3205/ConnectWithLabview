# Execution working memory

## Considered
- Iteration 0194 / #833: startup documents read once. Iteration 0193 closed, verdict none, not improved, 1 task (record 0193). no_progress=2; rollback streak 1 (0190, quiet time); outbox 787 pending; no open requests; goal gate unaccepted.
- Record .session/history/records/0193.json: #831 reviewer partial, branch task/831 commit e558a30f, 13 turns, 0 artifacts. Reviewed main 97fa2f0f.
- #831 report snapshot .github/loop/data/session-reports/831/966b5570....json read whole: NOT-CLEAR to start step 4 (procedural). F2 answered from code: `compute()` exact equality on literal; locator only via `citation_support()` (grounding, whole-dict match against inventory citations, never against XML); `regression_self_test` wrong-literal/wrong-citation mutations target A0005 only. F3 left open. F4 unconfirmed. Tools disabled mid-session again; no pins-0193.txt.
- F3 closed by shaper Grep: benchmark/challenges/library-specialty.json:2513 `inventory_path` = `benchmark/cases/dev/library-specialty.json` (the dev file IS the scored inventory, not a copy).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Positive-control thread (#763 f4): step 1 plan DONE (#820). Step 2 cold key DONE (0191). Step 3 review: F1 CLEAR (#828), F3 closed (line 2513), F2 answered from code (#831). Step 4 ordered 0194: A0001/A0002 mutation controls + F4 + regenerate + pins, then changed-scope review in the same graph. After CLEAR -> close thread.
- Deferred gap: XML key independent confirmation (after positive-control thread). Also #831: citations are never checked against the XML artifact (scorer design limit; carry).
- Carried minor findings: #809 f2, #809 f4 (silent skip when control absent); #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- Tools disabled mid-session in #828 and #831 (two in a row), 0-turn sessions (#794, #813), interruptions (#788, #800, 0190). Short limits, save files first. If it recurs in 0194, raise a suggestion to the Policymaker.
- CLOSED: matched comparison #722; attempt-ledger seam #703; attempt policy #685; constant-export thread (#817 CLEAR); zero-execution scorer scope (#779, #785).
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- positive-control-author-0194 (benchmark/default/medium, 60 min/45 turns): inputs #828 pins.txt, exports #828/#831 reports. Adds wrong-literal/wrong-citation mutations for A0001/A0002 in score.py self-test, answers F4 from inventory citation dicts, regenerates challenges.json, updates pins (incl. fixture `inventory_sha256` if inventory changes).
- positive-control-review-0194 (reviewer/default/medium, 40 min/30 turns), blocked_by author: pins-0194.txt first, runs self-test on temp copy, verdict.
- Check next: review verdict. CLEAR -> close positive-control thread, pick next method gap (XML key independent confirmation or citation-vs-XML limit). NOT-CLEAR -> correct named findings only.

## Tried, do not repeat
- Positive-control gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic read (#831 F2), inventory path (F3, line 2513). Do not re-derive, re-hash or re-review these.
- Regeneration of challenges.json: done (#812/#816, CLEAR #817).
- Keyed-literal probe (0183) and control (#808, CLEAR #809): done. Constant-export probe #791/#797 done. Mutation check #785 done. #779 done. #766/#778 re-pin done.
- Before re-ordering "paused" or failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0187-0193 at 8-9; 0194 at 10).
- Grep alternation unreliable (0194 again: `inventory_(path|sha256)` returned nothing); use single literal patterns.
- Session report snapshots: .session/history/sessions/<issue>/<sha>.md and .github/loop/data/session-reports/<issue>/.
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
