# Execution working memory

## Considered
- Iteration 0201 / #864: startup documents read once. Iteration 0200 closed, verdict accepted, improved (record .session/history/records/0200.json). no_progress=0; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; policy_rev f676b19a... (Policymaker #863 ran).
- Record 0200: #860 benchmark done, merged (6386cd43), check pass: input-pins.json:46 and :57 re-pinned to current score.py / challenges.json hashes; classification of old prefixes accepted. #861 reviewer done, NOT-CLEAR (report snapshot .github/loop/data/session-reports/861/ba116de5....json).
- #861: old-prefix classification CLEAR (0125/0128 JSON snapshots self-pinned by check_c1_challenges_0125.py:236 and check_integrity_0128.py:13; notes 0172/0186/0187 historical). Finding 1: `protected_inputs_sha256` (input-pins.json from line 8, 62 entries) has stale `benchmark/preparation.json` 99069d8d... vs disk e304aff0... (changed by #856, never re-pinned). input-pins.json at HEAD after #860: 5b06e263....
- Current hashes: score.py 21329d0d...94fd; challenges.json (benchmark/results/) a3466ad8...b8eb; 0191 key f9f5e1c4...d888; preparation.json e304aff0...063d.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Positive-control thread (#763 f4): steps 1-3 DONE (#820, 0191, #828/#831). Step 4 controls DONE and code-reviewed (#856, #857 f1-3); score.py/challenges.json pins DONE (#860, #861). Open only: #861 f1 preparation.json pin. 0201 orders correction + changed-scope review.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies (worked 0199, 0200).
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Deferred gap: XML key independent confirmation (next after step 4 closes; name gap and expected gain when ordering). #831: citations never checked against the XML artifact (scorer design limit; carry).
- Carried minor findings: #809 f2, #809 f4 (silent skip when control absent); #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: any task importing benchmark/scripts/*.py uses `python3 -B`, `sys.dont_write_bytecode = True`, checks `git status --porcelain` (#785).
- CLOSED: matched comparison #722; attempt-ledger seam #703; attempt policy #685; constant-export thread (#817 CLEAR); zero-execution scorer scope (#779, #785); old-prefix pin classification (#861).
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- step4-prep-pin-0201 (benchmark/default/low, 30 min/20 turns): re-pin preparation.json in `protected_inputs_sha256`; recompute the whole map; Grep old prefixes 99069d8d and 5b06e263, classify in `.session/artifacts/pin-classification-0201.md`. Exports #861 report.
- step4-prep-pin-review-0201 (reviewer/default/low, 30 min/20 turns, blocked_by): changed-scope review, full-map disk check.
- Check: verification recomputes every map entry against disk; review verdict in .session/reports/<review issue>.json. If CLEAR: step 4 and the positive-control thread close; next: XML key independent confirmation. If NOT-CLEAR: correct named findings only.

## Tried, do not repeat
- Positive-control gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic read (#831 F2), inventory path (F3), F4 + edit points (#852), controls applied (#856), controls reviewed OK (#857 f1-3), old-prefix classification (#860, CLEAR in #861). Do not re-derive or re-review these.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, then #861 f1 missed preparation.json).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0201 at 9). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158, 0176, 0186, 0188, 0199, 0200).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
