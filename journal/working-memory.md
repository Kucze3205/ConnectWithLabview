# Execution working memory

## Considered
- Iteration 0209 / #896: startup documents read once. Iteration 0208 closed, verdict accepted, improved (record 0208.json); no_progress=0; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #887 done.
- #893 (citation-check-finish-0208): done, check pass, merged (38a3e203). #894 review report snapshot `.github/loop/data/session-reports/894/e7e407c2...json` read whole: CLEAR, pins score.py 101cf13f, challenges.json e3fb477f, input-pins 7133f52a (62 entries OK), preparation.json a87f1437 (80 entries OK), dev library-specialty 1f1bc985, check_xml_keys 63f01c0e.
- citation-gap-0206.md lines 19, 62, 90 (Grep `answer_record_contract`).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- CLOSED XML key-agreement scope for library inventories (#881, CLEAR #882). Do not reopen.
- CLOSED citation-resolution check (#831 gap): #889 + #893, CLEAR #894. Minor S1 (resolve_locator duplicates ~25 lines of check_xml_keys.py, documented), S2 (--check/generate need LABVIEW_ENVIRONMENT; CI must set it), S3 note.
- OPEN design Limit 4 (citation-gap-0206.md:19, :90): `answer_record_contract` in benchmark/cases/dev/library-specialty.json describes citations as strings; fixtures/key/score.py use dicts. 0209 orders the fix + review. Next: read review verdict; CLEAR -> close; then consider extending citations to library-icon-tests / vi-actor-core-native-gap (no citations there) or move to the next method gap.
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
- citation-contract-0209 (benchmark/default/medium, 60 min/35 turns): rewrite `answer_record_contract` citation shape to the dict fields citation_resolves reads; helper script finds every OLD sha256 of the dev fixture in benchmark/ and updates it; full input-pins + preparation.json recomputation; --check with env.
- citation-contract-review-0209 (reviewer/default/medium, 45 min/30 turns, blocked_by producer): one-hunk diff, fields match score.py, no OLD hash left, full pin maps, --check.
- Expected gain: one pinned citation shape, Limit 4 closed with CLEAR/NOT-CLEAR. Check = producer report (hit list, pin counts) + reviewer verdict.

## Tried, do not repeat
- Citation check implemented (#889), finished (#893), reviewed CLEAR (#894); do not re-review score.py citation logic.
- Citation gap measurement + design done (#885, citation-gap-0206.md); do not re-measure.
- XML key thread: cold keys 0191, 0203 (#872), 0204 (#877); checker + 10/10 specialty (#873); 10/10 icon-tests (#878); agreement recorded (#881), CLEAR (#882). Closed.
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control thread (#820, 0191, #828, #831, #852, #856, #857, #860/#861, #865, CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1); #881, #889, #893 did it right.
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0206 at 10, 0207 at 8, 0208 at 8, 0209 at 8). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash. #882/#894: HEAD may be an epilogue commit; diff against the task commit's parent.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866/#882/#894 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154-0208 several).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
