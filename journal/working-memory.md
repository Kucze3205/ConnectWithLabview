# Execution working memory

## Considered
- Iteration 0210 / #901: startup documents read once. Iteration 0209 closed, verdict accepted, improved (record 0209.json); no_progress=0; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #900 done.
- #897 (citation-contract-0209): done, check pass, merged (7f9dde12). #898 review report snapshot `.github/loop/data/session-reports/898/1b5d55b8...json` read whole: CLEAR. Pins: dev library-specialty 82e0f1e6, input-pins 87bafc0c (62 entries OK), preparation.json aa90829b (80 entries OK), challenges.json 2465d5cc; --check 35/35; OLD fixture hash 1f1bc985 has no hit left.
- citation-gap-0206.md line 67 (Grep `icon-tests`): extension to library-icon-tests / vi-actor-core-native-gap "when they are scored".
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- CLOSED XML key-agreement scope for library inventories (#881, CLEAR #882). Do not reopen.
- CLOSED citation-resolution check (#831 gap): #889 + #893, CLEAR #894. Minor S1 (resolve_locator duplicates ~25 lines of check_xml_keys.py), S2 (--check/generate need LABVIEW_ENVIRONMENT), S3 note.
- CLOSED design Limit 4 (citation-gap-0206.md:19, :90): dict citation shape in `answer_record_contract`, #897, CLEAR #898. #898 did not diff the four re-pinned files line by line (hash matches only); minor, carried.
- OPEN citation extension to library-icon-tests / vi-actor-core-native-gap (citation-gap-0206.md:67). Reason open: unknown whether those fixtures are scored and what pin maps they touch. 0210 measures it. Next: read `benchmark/challenges/citation-extend-0210.md` `## Verdict`; ready -> order extension + review in one graph; blocked/not applicable -> move to the next method gap (next-gap-0202 `## Gaps`).
- No-environment limit (#889/S2): score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; engine verification cannot see the environment. Open question whether a no-environment mode is needed.
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only; challenges.json self-comparison (quality_measured false).
- Other method gaps (next-gap-0202 `## Gaps`): dependency/native keys OPEN (N0001/N0002 native-unverified; needs LabVIEW); restricted split/allocation/isolation OPEN (#636 blockers); reader/probes/scorer integration PARTIAL (zero reader attempts); whole-method review + owner acceptance OPEN; sources/tasks/oracle/coverage/baseline rows not re-measured. benchmark_ready=false.
- #873 minor: failure N/M count counts distinct mismatching IDs (approximate); MISMATCH lines authoritative.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #809 f2, #809 f4; #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: tasks running benchmark python use `python3 -B -I`, check `git status --porcelain` (#785).
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- citation-extend-measure-0210 (benchmark/default/medium, 45 min/30 turns): report, do not fix. Writes only `benchmark/challenges/citation-extend-0210.md` with `## Fixtures` (scored? citations count? XML key?), `## Extension needs` (files + live pin maps via search script), `## Verdict` per fixture.
- Expected gain: a decision input for the next shaper: extension task with exact file/pin list, or move to another gap. Check = the file's `## Verdict` lines and git status showing only that file.

## Tried, do not repeat
- Citation contract shape fixed (#897), reviewed CLEAR (#898); do not re-review.
- Citation check implemented (#889), finished (#893), reviewed CLEAR (#894); do not re-review score.py citation logic.
- Citation gap measurement + design done (#885, citation-gap-0206.md); do not re-measure.
- XML key thread: cold keys 0191, 0203 (#872), 0204 (#877); checker + 10/10 specialty (#873); 10/10 icon-tests (#878); agreement recorded (#881), CLEAR (#882). Closed.
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control thread (#820, 0191, #828, #831, #852, #856, #857, #860/#861, #865, CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1); #881, #889, #893, #897 did it right.
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0206 at 10, 0207-0210 at 8-9). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash. #882/#894: HEAD may be an epilogue commit; diff against the task commit's parent.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866/#882/#894/#898 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154-0209 several).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
