# Execution working memory

## Considered
- Iteration 0215 / #918: startup documents read once. Iteration 0214 closed, verdict none, not improved; no_progress=1; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #911 done.
- Record 0214 read: one task review-score-record-0214 -> #916 (reviewer, sonnet, 12 turns, done, merged false, 1 artifact).
- Session #916 report (`.session/history/sessions/916/0e9e4c5e...md`) read: verdict NOT-CLEAR; finding 1 medium (credit gate is only self-reported outcome/truncated; no evidence_record passed, so score.py:259-260, 326-327 treat native_run/independent_key as absent-and-fine; non-synthetic record can reach `correct`, bypassing challenges/README.md:8); findings 2-4 low. Q1-Q4 answered fine (chain ok, absent response harmless, mutation real, fidelity honest). Pins: score_record.py 38f48f2b..., score.py 101cf13f..., run_record.py b39c3060....
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- CLOSED citation thread: specialty (#897, CLEAR #898), icon-tests (#905, CLEAR #906). vi-actor-core-native-gap not applicable (#902). Do not reopen.
- CLOSED XML key-agreement scope (#881, CLEAR #882). CLOSED citation-resolution check (#889 + #893, CLEAR #894; minor S1 duplicated resolve_locator, S2 --check needs LABVIEW_ENVIRONMENT).
- OPEN reader / probes / scorer integration. score_record.py done (#913, 39b006f0); review #916 NOT-CLEAR finding 1. Ordered 0215: correction + changed-scope review in one graph. Next: read the review verdict. CLEAR -> close scorer-intake scope (carry #916 f2-f4 low), move to next gap. NOT-CLEAR -> one more narrow correction only for named findings (fix_rounds limit 2; this is round 1).
- OPEN blocker 7 (reader-integration-0212): #916 Discoveries confirms the "scorer never checks citations" note is stale (score.py:146-169 resolves, needs LABVIEW_ENVIRONMENT); covered by closed #889/#893/#894. Treat blocker 7 as resolved-stale; a doc note update is optional, low value.
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only; challenges.json self-comparison (quality_measured false).
- OPEN other gaps (next-gap-0202): dependency/native keys (needs LabVIEW); restricted split/allocation/isolation (#636 blockers); whole-method review + owner acceptance; sources/tasks/oracle/coverage/baseline rows not re-measured. benchmark_ready=false. After scorer scope closes, pick one of these with its expected gain.
- Reader attempts blocked: no reader (product), no native refs (LabVIEW), no model/quota/repetition decisions (owner) - reader-integration-0212 blockers 1-4.
- No-environment limit: score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; score_record.py --check does not.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #916 f2 (synthetic claim id only exercises extras path), f3 (real-path citation untested), f4 (probe/alignment from positive-control); #809 f2, #809 f4; #763 f6; #898 hash-only re-pin check; #873 N/M count approximate; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode: run benchmark python with `python3 -B -I`; check with pathlib rglob('__pycache__'), not git status.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- fix-score-record-0215 (benchmark/default/medium, 60 min/40 turns): correct #916 f1 only in score_record.py: non-validated (non-synthetic) records cannot reach `correct` (evidence_record with native_run/independent_key None, or cap at `unverified`); document `executed` self-reported; new --check stage asserting a non-synthetic keyed record is not `correct`; keep mutation stage; re-pin any live map listing score_record.py.
- review-score-record-fix-0215 (reviewer/default/medium, 45 min/30 turns, blocked_by fix): changed-scope review, 5 questions, pins itself, input producer artifact score-record-check.txt.
- Expected gain: credit gate closed; check: `verdict:` line in the review report and the new stage in the --check artifact.

## Tried, do not repeat
- score_record.py review done (#916); do not re-review the whole script; only changed scope.
- reader-integration survey done (0212, reader-integration-0212.md); do not re-survey.
- score_record.py written (#913); do not rewrite; corrections only by named finding.
- Citation thread done end-to-end (#885, #889, #893, #894, #897, #898, #902, #905, #906); do not re-measure or re-review.
- XML key thread: cold keys 0191, 0203 (#872), 0204 (#877); checker + 10/10 (#873, #878); agreement (#881), CLEAR (#882). Closed.
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control thread (#820 ... CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190).
- Write the graph by ~10th call (0206-0215 at 8-11). Shaper #847 crashed at 21 turns: stay short.
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
