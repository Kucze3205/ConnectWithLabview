# Execution working memory

## Considered
- Iteration 0203 / #871: startup documents read once. Iteration 0202 closed, verdict accepted, improved (loop-state `iterations`). no_progress=0; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; policy_rev f676b19a... (Policymaker #863).
- 0202 output read whole: `benchmark/challenges/next-gap-0202.md` (Gaps table, XML key confirmation PARTIAL 2/10, Recommendation: cold derivation of A0003-A0010 + stdlib checker).
- `benchmark/cases/dev/library-specialty.json` read: reference_inventory A0001-A0010 locators (Property[4] @Name/@Type/text(), Item[1..2] @Name/@Type/@URL), N0001/N0002 native null; artifact sha256 83bd1049...87d0; `oracle.independent_checker.status` pending.
- Current hashes (per #866): preparation.json e304aff0...063d; input-pins.json 8e919d48...a975.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN XML independent-key thread (next-gap-0202): 2/10 confirmed for library-specialty (key-0191). 0203 orders cold derivation + checker. After it: decide on (a) recording agreement in the fixture's `oracle.independent_checker` via a permitted writer + review, (b) the same for `library-icon-tests` (0202 says "both inventories"; 0203 covers library-specialty only), (c) README.md:28 "Next" update.
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only; challenges.json self-comparison (quality_measured false).
- #831: scorer never checks citations against the XML artifact (design limit; carry).
- Other method gaps (next-gap-0202 `## Gaps`): dependency/native keys OPEN; restricted split/allocation/isolation OPEN (#636 blockers); reader/probes/scorer integration PARTIAL; whole-method review + owner acceptance OPEN; sources/tasks/oracle/coverage/baseline rows not re-measured. benchmark_ready=false.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies (worked 0199-0202).
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #809 f2, #809 f4; #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: tasks running benchmark python use `python3 -B -I`, check `git status --porcelain` (#785).
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- xml-key-cold-0203 (benchmark/default/medium, 45 min/25 turns): writes `benchmark/challenges/positive-control-key-0203.json` with A0003-A0010 values/locators/lines from the artifact only; forbidden files listed (key-0191, cases/dev, next-gap-0202, plan-0189, README, scripts, results). Check: verification asserts sha256 and ID set.
- xml-key-check-0203 (benchmark/default/medium, 60 min/35 turns, blocked_by cold): writes `benchmark/challenges/check_xml_keys.py` (`--artifact`, `--inventory`), runs on keys 0191+0203, mutation check in artifacts. Report, do not fix. Check: report's `xml keys: N/N OK` line for both modes; verification runs `--inventory`.
- Expected gain: XML key confirmation 10/10 for library-specialty, or named mismatches. If the cold session read a forbidden file, its key is not independent: re-derive with a fresh session, do not review.

## Tried, do not repeat
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control: gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic (#831 F2), inventory path (F3), F4 + edit points (#852), controls (#856), review (#857 f1-3), old-prefix classification (#860/#861), preparation.json re-pin (#865, CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0203 at 8). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154-0201 several).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
