# Execution working memory

## Considered
- Iteration 0206 / #884: startup documents read once. Iteration 0205 closed, verdict accepted, improved (record 0205). no_progress=0; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; policy_rev 5f32c870... (Policymaker #875).
- #881 (xml-agree-record-0205) done, verification pass, merged abd491f9: both library fixtures carry `oracle.independent_checker` status `xml-agreed-A0001-A0010-native-pending`; pins re-pinned.
- #882 report read (snapshot e57b8acd...): CLEAR. 62/62 input-pins and 80/80 preparation.json path/sha256 entries match disk; diff only touched independent_checker; checker: specialty 8/8 (key 0203) + 2/2 (key 0191), icon-tests 10/10 (key 0204).
- `benchmark/challenges/next-gap-0202.md` read whole (gaps table, recommendation).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- CLOSED XML key-agreement scope for library inventories (#881, CLEAR #882 at abd491f9). Do not reopen.
- OPEN #831 citation gap (scorer never checks citations against the XML artifact; grounding EV:78 unmeasured). 0206 measures and designs it (citation-gap-0206). Next: implementation of the check + controls, then changed-scope review in one graph, re-pinning every live map.
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only; challenges.json self-comparison (quality_measured false).
- Other method gaps (next-gap-0202 `## Gaps`): dependency/native keys OPEN (N0001/N0002 native-unverified; needs LabVIEW, no session can run it); restricted split/allocation/isolation OPEN (#636 blockers); reader/probes/scorer integration PARTIAL (zero reader attempts); whole-method review + owner acceptance OPEN; sources/tasks/oracle/coverage/baseline rows not re-measured. benchmark_ready=false.
- #873 minor: failure N/M count counts distinct mismatching IDs (approximate); MISMATCH lines authoritative.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #809 f2, #809 f4; #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: tasks running benchmark python use `python3 -B -I`, check `git status --porcelain` (#785).
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- citation-gap-0206 (benchmark/default/medium, 60 min/35 turns): measurement + design only, writes `benchmark/challenges/citation-gap-0206.md` (headings Current behaviour, Reuse, Design, Controls, Recommendation), cites score.py / check_xml_keys.py functions and lines, names pin-map entries the design would change, three+ pre-written controls. No code edits.
- Expected gain: exact edit points for a citation check so 0207 can order implementation + review in one graph. Check: verification heading line passes and the `## Recommendation` section names files, functions and pin entries.

## Tried, do not repeat
- XML key thread: cold keys 0191, 0203 (#872), 0204 (#877); checker + 10/10 specialty (#873); 10/10 icon-tests (#878); agreement recorded (#881), CLEAR (#882). Closed.
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control: gap measurement (#820), cold key (0191), literal/locator/hash check (#828 F1), scorer logic (#831 F2), inventory path (F3), F4 + edit points (#852), controls (#856), review (#857 f1-3), old-prefix classification (#860/#861), preparation.json re-pin (#865, CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1); #881 did it right.
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0206 at 10). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash. #882: HEAD may be an epilogue commit; diff against the task commit's parent.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866/#882 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154-0205 several).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
