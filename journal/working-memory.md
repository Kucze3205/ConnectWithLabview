# Execution working memory

## Considered
- Iteration 0205 / #880: startup documents read once. Iteration 0204 closed, verdict accepted, improved (record 0204). no_progress=0; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; policy_rev 5f32c870... (Policymaker #875).
- #877 (cold key 0204 icon-tests) done, verification pass, merged 491c1386: `benchmark/challenges/positive-control-key-0204-icon-tests.json`.
- #878 report read (snapshot da485a77...): check_xml_keys.py `--inventory` and `--artifact` on the 0204 key: `xml keys: 10/10 OK`, exit 0 both; no file changed. `$LABVIEW_ENVIRONMENT` = `/home/runner/work/_temp/connectwithlabview-environment` (not /resources/environment).
- `benchmark/cases/dev/library-specialty.json` read whole: `oracle.independent_checker` (line 137) = `{claim_agreements: [], identity: null, session: null, status: pending}`.
- Pin maps grepped: `benchmark/writing/input-pins.json` protected_inputs_sha256 lines 20-21 pin both library fixtures; `benchmark/preparation.json` pins them twice (lines 135-140, 289-294).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN XML independent-key thread: library-specialty 10/10 (#872/#873), library-icon-tests 10/10 (#877/#878). 0205 records agreement in both fixtures + re-pins + README Next, then reviews it. After CLEAR: XML key scope for library inventories closed; move to the next gap from next-gap-0202 `## Gaps`.
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only; challenges.json self-comparison (quality_measured false).
- #831: scorer never checks citations against the XML artifact (design limit; carry). check_xml_keys.py checks keys, not submitted answers. Candidate next gap after 0205.
- Other method gaps (next-gap-0202 `## Gaps`): dependency/native keys OPEN (N0001/N0002 native-unverified); restricted split/allocation/isolation OPEN (#636 blockers); reader/probes/scorer integration PARTIAL; whole-method review + owner acceptance OPEN; sources/tasks/oracle/coverage/baseline rows not re-measured. benchmark_ready=false.
- #873 minor: failure N/M count counts distinct mismatching IDs (approximate); MISMATCH lines authoritative.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #809 f2, #809 f4; #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: tasks running benchmark python use `python3 -B -I`, check `git status --porcelain` (#785).
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- xml-agree-record-0205 (benchmark/default/medium, 60 min/35 turns): edits only `oracle.independent_checker` in both library fixtures (status `xml-agreed-A0001-A0010-native-pending`, ten claim_agreements with key sha, identity with checker sha, session pairs 872/873 and 877/878), re-pins input-pins.json + preparation.json (all entries vs disk), README Next line. Verification recomputes every entry of both maps and checks claim_agreements IDs.
- xml-agree-review-0205 (reviewer/default/medium, 45 min/30 turns, blocked_by record): pins merged commit and hashes, diff-only-checker check, whole-map pin recompute, checker rerun. Findings in report/artifacts only.
- Expected gain: both library fixtures carry a recorded, reviewed independent XML check. NOT-CLEAR -> correct named findings + changed-scope review in one graph.

## Tried, do not repeat
- XML key thread: cold keys 0191, 0203 (#872), 0204 (#877); checker + 10/10 specialty (#873); 10/10 icon-tests (#878). Do not re-derive keys or rewrite the checker.
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control: gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic (#831 F2), inventory path (F3), F4 + edit points (#852), controls (#856), review (#857 f1-3), old-prefix classification (#860/#861), preparation.json re-pin (#865, CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0205 at 13). Shaper #847 crashed at 21 turns: stay short.
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
