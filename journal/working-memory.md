# Execution working memory

## Considered
- Iteration 0191 / #824: startup documents read once. Iteration 0190 status `failed`, 0 tasks, verdict none (loop-state `iterations[0]`); rollback streak 1, reason "did not close within the quiet time" (2026-11-17). no_progress=1; outbox 787 pending; no open requests; goal gate unaccepted.
- Glob `benchmark/challenges/positive-control-*` on main: only positive-control-plan-0189.md exists, so the 0190 cold-key task never produced output.
- benchmark/challenges/positive-control-plan-0189.md (read whole this session; author saw candidate values).
- Artifact located: `@environment/actor-framework/Core/ActorFramework/AF Specialty Messages.lvlib`.
- Record 0189: #820 benchmark done, merged (65cd271a), check pass.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false; 35 controls incl. 4 of vi-actor-core-native-gap.json).
- Positive-control thread (#763 f4): step 1 plan DONE (#820). Step 2 cold key derivation: ordered 0190 (iteration failed, never ran), re-ordered 0191. Step 3: reviewer compares cold key with inventory (benchmark/cases/dev/library-specialty.json) and plan candidates; checks control would fail on a wrong literal/citation. Step 4: author control in library-specialty.json + regenerate results + update pins (#739/#766), then changed-scope review.
- Plan candidates (do NOT give to the deriver): A0001 `20008000`, A0002 `NI.LV.All.SourceOnly`. Use them only in the reviewer task.
- Deferred gap: XML key independent confirmation (after positive-control thread).
- Carried minor findings: #809 f2 (control note wording), #809 f4 (silent skip when control absent); #763 f6 (null native_run cases do not assert extras_ledger); plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Constant-export thread, regeneration: CLOSED (#808/#809, #812/#816, #817 CLEAR). Zero-execution scorer scope CLOSED (#779, #785).
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- Sessions with 0 turns (#794, #813), runtime interruption (#788), provider pause (#800), iteration not closing in quiet time (0190) recur. Short limits, save files first.
- CLOSED: matched comparison #722; attempt-ledger seam #703 (F-A1, F-A2 open for owner); attempt policy #685.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- positive-control-cold-key-0191 (benchmark/default/medium, 40 min/30 turns): cold derivation from artifact bytes + evaluation.md only; writes benchmark/challenges/positive-control-key-0191.json (`claims.A0001/A0002` with value, locator, scheme, derivation; artifact_path, artifact_sha256). Forbidden reads: plan-0189, library-*.json, cases/dev/**, results/**, scripts/**, journal/**, #820 reports.
- Check next: record 0191 merged status; key file parses; report lists reads in order and confirms no forbidden read. Then order the reviewer (step 3) with the key file, plan-0189 and the inventory pinned by hash (reviewer writes report/artifacts only).

## Tried, do not repeat
- Positive-control gap measurement: done (#820, plan-0189). Do not re-measure.
- Regeneration of challenges.json: done (#812/#816, CLEAR #817).
- Verification paths: score.py writes benchmark/results/challenges.json; benchmark/cases/dev/ holds copies of library-*.json not read by score.py. Glob a path before asserting it (#812).
- Keyed-literal probe (0183) and control (#808, CLEAR #809): done. Constant-export probe #791/#797 done. Mutation check #785 done. #779 independent expectation done. #766/#778 re-pin done.
- Before re-ordering "paused" or failed work, Glob its expected output on main first (#800, 0190). Paused branches not resumable; partial with recorded branch is (#812 -> #816).
- Write the graph by ~10th call (0187 at 8, 0188 at 9, 0189 at 9, 0190 at 8, 0191 at 9).
- Grep alternation unreliable; prefer Glob + Read.
- Session report snapshots: .session/history/sessions/<issue>/<sha>.md and .github/loop/data/session-reports/<issue>/.
- #763 findings 1-3 closed. #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #739/#766: a change to any pinned file updates all its pins in the same task.
- #743: long inline python3 one-liners stall; use file-based helpers. #747 importlib helper stalled; guarded exec works.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154, 0157, 0158, 0176, 0186, 0188).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks.
- #617 invalid quoting: read-back plus direct Python validation. Avoid `\\0` in verification strings. Empty Write erases files. Read report before Finish.
