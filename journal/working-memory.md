# Execution working memory

## Considered
- Iteration 0212 / #908: startup documents read once. Iteration 0211 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #900 done.
- Record 0211: #905 (icon-citation-shape-0211) done, accepted, merged 4eef3934; #906 review done, verdict CLEAR (session snapshot `.session/history/sessions/906/49315a36...md`): 62/62 protected_inputs_sha256 match, 80/80 preparation.json pins match, score.py --check 35/35, old hashes only in historical session-report JSONs (882, 898).
- `benchmark/challenges/next-gap-0202.md` `## Gaps` re-read for the next gap choice.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- CLOSED citation thread: specialty (#897, CLEAR #898), icon-tests (#905, CLEAR #906, caveat: reviewer inferred the four candidate pin files from old hashes, not from the producer report; no live stale pin found). vi-actor-core-native-gap not applicable (#902). Do not reopen.
- CLOSED XML key-agreement scope (#881, CLEAR #882). CLOSED citation-resolution check (#889 + #893, CLEAR #894; minor S1 duplicated resolve_locator, S2 --check needs LABVIEW_ENVIRONMENT).
- OPEN (0212) reader / probes / scorer integration (next-gap-0202 row PARTIAL: zero reader attempts, scorer only on synthetic controls, benchmark_executed false). Measurement ordered this iteration. Next: read `benchmark/challenges/reader-integration-0212.md` `## Recommendation` and order its task if doable-now-as-preparation; if all blockers are needs-LabVIEW/owner/product-code, pick the next row below.
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only; challenges.json self-comparison (quality_measured false).
- OPEN other gaps (next-gap-0202): dependency/native keys (N0001/N0002 native-unverified; needs LabVIEW); restricted split/allocation/isolation (#636 blockers); whole-method review + owner acceptance; sources/tasks/oracle/coverage/baseline rows not re-measured. benchmark_ready=false.
- No-environment limit: score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; engine verification cannot see the environment.
- #873 minor: failure N/M count approximate; MISMATCH lines authoritative.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #809 f2, #809 f4; #763 f6; #898 hash-only re-pin check; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: tasks running benchmark python use `python3 -B -I`, check `git status --porcelain` (#785).
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- reader-integration-measure-0212 (benchmark/default/medium, 60 min/40 turns): measurement only, writes `benchmark/challenges/reader-integration-0212.md` with `## Requirements`, `## Existing`, `## Blockers` (each classed needs-LabVIEW/needs-owner/needs-product-code/doable-now-as-preparation, file:line), `## Recommendation`. Check: headings present, only the new file changed.
- Expected gain: the next shaper orders the next integration step from `## Recommendation` without re-surveying.

## Tried, do not repeat
- Citation thread done end-to-end (#885, #889, #893, #894, #897, #898, #902, #905, #906); do not re-measure or re-review.
- XML key thread: cold keys 0191, 0203 (#872), 0204 (#877); checker + 10/10 (#873, #878); agreement (#881), CLEAR (#882). Closed.
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control thread (#820 ... CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190).
- Write the graph by ~10th call (0206-0212 at 8-11). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash. #882/#894/#906: HEAD may be an epilogue commit; diff against the task commit's parent.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866/#882/#894/#898/#906 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154-0211 several).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
