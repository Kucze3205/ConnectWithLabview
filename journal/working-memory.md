# Execution working memory

## Considered
- Iteration 0216 / #923: startup documents read once. Iteration 0215 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #922 done.
- Record 0215 read: fix-score-record-0215 -> #919 (benchmark, sonnet, 17 turns, done, check pass, merged, commit 26b3e18b); review-score-record-fix-0215 -> #920 (reviewer, sonnet, 12 turns, done, not merged, 1 artifact).
- Session #920 report (`.session/history/sessions/920/002b6376...md`) read: verdict CLEAR on commit b0dca39d; score_record.py 2597f67b..., score.py 101cf13f... and run_record.py b39c3060... equal #916 pins; stage-3 cap shown real by in-memory mutant. Finding 1 low (`validated` flag caller-supplied, score_record.py:55,61); finding 2 info (CLI never validates, conservative).
- `benchmark/challenges/next-gap-0202.md` read whole: sources/tasks/oracle/coverage/baseline rows NOT RE-MEASURED (EV:63-68).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- CLOSED scorer-intake scope: score_record.py (#913), review #916 NOT-CLEAR f1, correction #919, CLEAR #920. Carry low: #920 f1 (trusted-caller `validated` flag), #916 f2-f4. Do not reopen.
- CLOSED citation thread: specialty (#897, CLEAR #898), icon-tests (#905, CLEAR #906). vi-actor-core-native-gap not applicable (#902).
- CLOSED XML key-agreement scope (#881, CLEAR #882). CLOSED citation-resolution check (#889 + #893, CLEAR #894).
- Blocker 7 (reader-integration-0212, "scorer never checks citations") resolved-stale: score.py:146-169 resolves (#916 Discoveries). Doc note update optional, low value.
- OPEN rows not re-measured: sources/tasks/oracle/coverage/baseline (EV:63-68) and write-task coverage of the method (goal: write implementation waits for a method covering write tasks). Ordered 0216: measure-rows-0216 -> `benchmark/challenges/rows-0216.md`. Next: read its `## Recommendation` and order that task (no LabVIEW, no owner material, no product code).
- OPEN challenges row (EV:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only.
- OPEN other gaps (next-gap-0202): dependency/native keys (needs LabVIEW); restricted split/allocation/isolation (#636 blockers); whole-method review + owner acceptance. benchmark_ready=false.
- Reader attempts blocked: no reader (product), no native refs (LabVIEW), no model/quota/repetition decisions (owner) - reader-integration-0212 blockers 1-4.
- No-environment limit: score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; score_record.py --check does not.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #920 f1; #916 f2-f4; #809 f2, f4; #763 f6; #898 hash-only re-pin check; #873 N/M count approximate; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode: run benchmark python with `python3 -B -I`; check with pathlib rglob('__pycache__'), not git status.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- measure-rows-0216 (benchmark/default/medium, 60 min/40 turns): measurement only; writes `benchmark/challenges/rows-0216.md` with `## Rows` (EV:63-68 status with file:line), `## Write tasks` (what exists for change-artifact tasks), `## Recommendation` (one next task, gain, verification command).
- Expected gain: the next gap chosen from a measured table, incl. write-task coverage; check: the file's headings (verification command) and its Recommendation section.

## Tried, do not repeat
- Scorer-intake thread done (#913, #916, #919, #920 CLEAR); do not re-review score_record.py.
- reader-integration survey done (0212, reader-integration-0212.md); do not re-survey.
- Citation thread done end-to-end (#885, #889, #893, #894, #897, #898, #902, #905, #906).
- XML key thread: cold keys 0191, 0203 (#872), 0204 (#877); checker + 10/10 (#873, #878); agreement (#881), CLEAR (#882). Closed.
- next-gap survey done (0202, next-gap-0202.md); rows-0216 completes only its NOT RE-MEASURED row; do not re-survey the rest.
- Positive-control thread (#820 ... CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190).
- Write the graph by ~10th call (0206-0216 at 8-11). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash. HEAD may be an epilogue commit; diff against the task commit's parent.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866/#882/#894/#898/#906/#920 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154-0215 several).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
