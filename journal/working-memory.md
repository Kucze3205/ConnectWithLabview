# Execution working memory

## Considered
- Iteration 0211 / #904: startup documents read once. Iteration 0210 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #900 done.
- #902 measurement `benchmark/challenges/citation-extend-0210.md` read whole: library-icon-tests ready to extend (one string citation in dev file `answer_record_contract`; generic score.py citation check already runs; --check 35/35); vi-actor-core-native-gap not applicable (binary, no XML key, no dict citations).
- `benchmark/writing/input-pins.json:8` holds `protected_inputs_sha256`.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- CLOSED XML key-agreement scope for library inventories (#881, CLEAR #882). Do not reopen.
- CLOSED citation-resolution check (#831 gap): #889 + #893, CLEAR #894. Minor S1 (resolve_locator duplicates ~25 lines of check_xml_keys.py), S2 (--check/generate need LABVIEW_ENVIRONMENT), S3 note.
- CLOSED design Limit 4 for library-specialty: dict citation shape, #897, CLEAR #898 (hash-only check of re-pins; minor, carried).
- OPEN (0211) citation shape for library-icon-tests: one string citation -> dict shape, re-pin dev file, challenge fixture source.inventory_sha256, results/challenges.json, input-pins.json, preparation.json. Producer must decide live vs historical for c1-challenges-0125-pins.json, lineage.json, reviews-0128/c1-artifact-manifest-0126.json, preparation-status.json. Next: read the review verdict; CLEAR closes the citation thread -> move to next method gap (next-gap-0202 `## Gaps`); NOT-CLEAR -> correct named findings + changed-scope review in one graph.
- CLOSED as not applicable: citation extension to vi-actor-core-native-gap (#902 Verdict).
- No-environment limit (#889/S2): score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; engine verification cannot see the environment.
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only; challenges.json self-comparison (quality_measured false).
- Other method gaps (next-gap-0202 `## Gaps`): dependency/native keys OPEN (N0001/N0002 native-unverified; needs LabVIEW); restricted split/allocation/isolation OPEN (#636 blockers); reader/probes/scorer integration PARTIAL (zero reader attempts); whole-method review + owner acceptance OPEN; sources/tasks/oracle/coverage/baseline rows not re-measured. benchmark_ready=false. Candidate next after citation thread: reader/probes/scorer integration (zero reader attempts) — measure first.
- #873 minor: failure N/M count approximate; MISMATCH lines authoritative.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #809 f2, #809 f4; #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: tasks running benchmark python use `python3 -B -I`, check `git status --porcelain` (#785).
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- icon-citation-shape-0211 (benchmark/default/medium, 60 min/40 turns): rewrite string citation, re-pin whole live maps, record live/historical decision for four candidate pin files. Check: verification recomputes whole protected_inputs_sha256 map, no string-first citations list, fixture inventory sha matches.
- icon-citation-review-0211 (reviewer/default/medium, 45 min/30 turns, blocked_by the shape task): pins commit + hashes itself, five checks, CLEAR/NOT-CLEAR in report.
- Expected gain: both XML-keyed fixtures share one citation shape; CLEAR closes the citation thread.

## Tried, do not repeat
- Citation extension measured (#902, citation-extend-0210.md); do not re-measure.
- Citation contract shape fixed for specialty (#897), reviewed CLEAR (#898); do not re-review.
- Citation check implemented (#889), finished (#893), reviewed CLEAR (#894); do not re-review score.py citation logic.
- Citation gap measurement + design done (#885, citation-gap-0206.md); do not re-measure.
- XML key thread: cold keys 0191, 0203 (#872), 0204 (#877); checker + 10/10 specialty (#873); 10/10 icon-tests (#878); agreement (#881), CLEAR (#882). Closed.
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control thread (#820 ... CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190).
- Write the graph by ~10th call (0206-0211 at 8-10). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash. #882/#894: HEAD may be an epilogue commit; diff against the task commit's parent.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866/#882/#894/#898 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154-0211 several).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
