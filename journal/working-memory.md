# Execution working memory

## Considered
- Iteration 0200 / #859: startup documents read once. Iteration 0199 closed, verdict accepted, improved (record .session/history/records/0199.json). no_progress=0; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; policy_rev 79065a0f...
- Record 0199: #856 benchmark done, merged (commit 83a4c7a8), check pass: step-4 controls added. #857 reviewer done, NOT-CLEAR (report .session/reports/857.json).
- #857: findings 1-3 OK (wrong-literal-a0001 12 mismatches detected; wrong-locator-a0002 6 mismatches detected; A0005 unchanged; `score.py --check` 35/35; 0191 key unchanged). Finding 4: stale old hashes score.py 978982...a644 (benchmark/writing/input-pins.json:57, c1-challenges-0125-pins.json:341, reviews-0128/c1-artifact-manifest-0126.json:451) and challenges.json 453815...a15e (c1 pins, that manifest, notes 0172/0186/0187 under benchmark/challenges/). Live vs historical not determined.
- Current hashes per #857: score.py 21329d0d...94fd, challenges.json a3466ad8...b8eb, 0191 key f9f5e1c4...d888.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Positive-control thread (#763 f4): steps 1-3 DONE (#820, 0191, #828/#831). Step 4 controls DONE and code-reviewed (#856, #857 f1-3). Open only: #857 f4 stale pins. 0200 orders correction + changed-scope review.
- Tool-disable message: native-tool refusal, not broker failure (#854); 0199 tasks with the pointer succeeded. Keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Deferred gap: XML key independent confirmation (next after step 4 closes). #831: citations never checked against the XML artifact (scorer design limit; carry).
- Carried minor findings: #809 f2, #809 f4 (silent skip when control absent); #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: any task importing benchmark/scripts/*.py uses `python3 -B`, `sys.dont_write_bytecode = True`, checks `git status --porcelain` (#785).
- CLOSED: matched comparison #722; attempt-ledger seam #703; attempt policy #685; constant-export thread (#817 CLEAR); zero-execution scorer scope (#779, #785).
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- step4-pins-0200 (benchmark/default/medium, 45 min/30 turns): Grep old prefixes 978982 / 453815, classify each hit LIVE/HISTORICAL in `.session/artifacts/pin-classification.md`, update LIVE pins only. Exports #856, #857 reports.
- step4-pins-review-0200 (reviewer/default/medium, 40 min/25 turns, blocked_by pins): changed-scope review of the classification and edits.
- Check: input-pins.json contains the current score.py hash on main; review verdict in .session/reports/<review issue>.json. If CLEAR: step 4 and the positive-control thread close; next gap is XML key independent confirmation. If NOT-CLEAR: correct the named classifications only.

## Tried, do not repeat
- Positive-control gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic read (#831 F2), inventory path (F3), F4 + edit points (#852), controls applied (#856), controls reviewed OK (#857 f1-3). Do not re-derive or re-review these.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0200 at 8). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #739/#766/#857 f4: a change to any pinned file updates all its live pins in the same task; tell the producer to Grep every old hash prefix repo-wide.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158, 0176, 0186, 0188, 0199).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
