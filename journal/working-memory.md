# Execution working memory

## Considered
- Iteration 0204 / #876: startup documents read once. Iteration 0203 closed, verdict accepted, improved (record 0203). no_progress=0; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; policy_rev 5f32c870... (Policymaker #875).
- #873 report read (snapshot 402f14f6...): `benchmark/challenges/check_xml_keys.py` written; `--inventory` and `--artifact` on keys 0191+0203: `xml keys: 10/10 OK`; mutation check exits 1 in both modes (artifact `iter-0203/873-mutated-key-0203.json`). Key shapes differ (0191 dict, 0203 list); script handles both. `$LABVIEW_ENVIRONMENT` is not `/resources/environment` in sessions.
- #872 (cold key 0203) done, verification pass; `benchmark/challenges/positive-control-key-0203.json`.
- `benchmark/cases/dev/library-icon-tests.json` read whole: artifact `Tooling/Unit tests/Text-Based VI Icon/Text-Based VI Icon Unit Tests.lvlib`, sha256 5f30ea51...3130; A0001-A0010 locators (@LVVersion, Property[3] @Name/@Type/text(), Item[1..2] @Name/@Type/@URL); N0001/N0002 native null; `oracle.independent_checker.status` pending; no cold key exists yet.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN XML independent-key thread: library-specialty 10/10 confirmed (#873). library-icon-tests 0/10; 0204 orders cold key + check. After it: (a) record agreement in both fixtures' `oracle.independent_checker` (claim_agreements, identity, session) via a permitted writer (benchmark), then a reviewer on the changed scope; that changes pinned fixtures, so the task must recompute every live pin map entry (`benchmark/writing/input-pins.json`, `benchmark/preparation.json`) against disk; (b) README.md:28 "Next" update.
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only; challenges.json self-comparison (quality_measured false).
- #831: scorer never checks citations against the XML artifact (design limit; carry). check_xml_keys.py checks keys, not submitted answers.
- Other method gaps (next-gap-0202 `## Gaps`): dependency/native keys OPEN; restricted split/allocation/isolation OPEN (#636 blockers); reader/probes/scorer integration PARTIAL; whole-method review + owner acceptance OPEN; sources/tasks/oracle/coverage/baseline rows not re-measured. benchmark_ready=false.
- #873 minor: failure N/M count counts distinct mismatching IDs (approximate); MISMATCH lines authoritative.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #809 f2, #809 f4; #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: tasks running benchmark python use `python3 -B -I`, check `git status --porcelain` (#785).
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- xml-key-cold-0204 (benchmark/default/medium, 45 min/25 turns): writes `benchmark/challenges/positive-control-key-0204-icon-tests.json` (list-shaped claims A0001-A0010) from the artifact only; forbidden: cases/dev, other keys, check script, next-gap, plan-0189, README, scripts, results. Verification asserts sha256 and ID set.
- xml-key-check-0204 (benchmark/default/low, 30 min/20 turns, blocked_by cold): runs existing check_xml_keys.py `--inventory` and `--artifact` on the 0204 key; writes nothing. Verification runs `--inventory`.
- Expected gain: library-icon-tests 10/10 or named mismatches. If the cold session read a forbidden file, re-derive with a fresh session; a mismatch is a finding to adjudicate against the artifact, not to edit away.

## Tried, do not repeat
- XML key thread: cold key 0191 (A0001-A0002), cold key 0203 (#872), checker + 10/10 library-specialty (#873). Do not re-derive library-specialty keys or rewrite the checker.
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control: gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic (#831 F2), inventory path (F3), F4 + edit points (#852), controls (#856), review (#857 f1-3), old-prefix classification (#860/#861), preparation.json re-pin (#865, CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0204 at 11). Shaper #847 crashed at 21 turns: stay short.
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
