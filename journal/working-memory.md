# Execution working memory

## Considered
- Iteration 0202 / #868: startup documents read once. Iteration 0201 closed, verdict accepted, improved (record .session/history/records/0201.json). no_progress=0; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; policy_rev f676b19a... (Policymaker #863).
- Record 0201: #865 benchmark done, merged (f8670d52), check pass: preparation.json re-pinned in `protected_inputs_sha256`. #866 reviewer done, CLEAR (snapshot .github/loop/data/session-reports/866/3a38ca01....json): all 62 entries match disk; old prefixes 99069d8d/5b06e263 only in historical text. Minor discoveries: classification omitted session-reports/865; one 861 history citation not confirmed (historical either way).
- Current hashes: preparation.json e304aff0...063d; input-pins.json 8e919d48...a975 (per #866).
- Grep of benchmark/challenges for "xml" in key-0191.json: no hit; plan-0189:37,46,52,60 describe the XML-literal derivation (LVVersion 20008000, library-specialty.json fixture).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- Positive-control thread (#763 f4): CLOSED. Steps 1-4 done; pins CLEAR (#866).
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false).
- Deferred gap now being scoped: XML key independent confirmation (key-0191 vs fixture XML). 0202 measures whether it is already covered (0191 cold derivation, #828 F1) and recommends one next task. #831: citations never checked against the XML artifact (scorer design limit; carry).
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies (worked 0199-0201).
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #809 f2, #809 f4 (silent skip when control absent); #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: any task importing benchmark/scripts/*.py uses `python3 -B`, checks `git status --porcelain` (#785).
- CLOSED: positive-control thread (#866); matched comparison #722; attempt-ledger seam #703; attempt policy #685; constant-export thread (#817); zero-execution scorer scope (#779, #785); old-prefix pin classification (#861).
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- next-gap-0202 (benchmark/default/medium, 60 min/35 turns): writes `benchmark/challenges/next-gap-0202.md` with `## Gaps` (status + evaluation.md line per gap), `## XML key confirmation` (covered with evidence, or the exact missing check), `## Recommendation` (one task, gain, verification command). Report, do not fix. Exports #866 report.
- Expected gain: the next shaper orders the recommendation directly, no re-survey. Check: the file's headings (verification) and its `## Recommendation`; read the cited lines before trusting them.

## Tried, do not repeat
- Positive-control: gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic (#831 F2), inventory path (F3), F4 + edit points (#852), controls (#856), review (#857 f1-3), old-prefix classification (#860/#861), preparation.json re-pin (#865, CLEAR #866). Do not re-derive or re-review these.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0202 at 11). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154-0201 several).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
