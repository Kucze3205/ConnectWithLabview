# Execution working memory

## Considered
- Iteration 0193 / #830: startup documents read once. Iteration 0192 closed, verdict none, not improved, 1 task (record 0192). no_progress=1; rollback streak 1 (0190, quiet time); outbox 787 pending; no open requests; goal gate unaccepted.
- Record .session/history/records/0192.json: #828 reviewer partial, branch task/828 commit 53c4c4f5, 14 turns, 1 artifact (pins.txt).
- #828 report snapshot .github/loop/data/session-reports/828/9471d70c....json read whole: F1 info (key/plan/inventory agree on A0001, A0002; hash matches), F2 medium (fail-on-wrong unchecked, score.py unread), F3 medium (which copy score.py reads unknown), F4 low (locator scheme name "xpath-positional" vs inventory `xml-positional-path`). Grep/Bash disabled mid-session; review-0192.md not written; verification not run. Reviewed main f80826a3.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, author-written synthetic fixtures only; benchmark/results/challenges.json self-comparison (quality_measured false; 35 controls incl. 4 of vi-actor-core-native-gap.json).
- Positive-control thread (#763 f4): step 1 plan DONE (#820). Step 2 cold key DONE (0191, key-0191.json). Step 3 review: literals/locators CLEAR (#828 F1); F2/F3/F4 open -> finishing review ordered 0193. Step 4 (after final CLEAR): author control in the inventory score.py actually reads + mutation test (wrong digit, wrong Property index, per #828 F2) + align scheme name (F4) + regenerate results + update pins (#739/#766), then changed-scope review in the same graph.
- Inventory already records both literals as `provisional-xml-derived-unverified-independent-check` (#828). Step 4 may only need to flip status/add control, not new literals.
- Deferred gap: XML key independent confirmation (after positive-control thread).
- Carried minor findings: #809 f2 (control note wording), #809 f4 (silent skip when control absent); #763 f6 (null native_run cases do not assert extras_ledger); plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Constant-export thread, regeneration: CLOSED (#808/#809, #812/#816, #817 CLEAR). Zero-execution scorer scope CLOSED (#779, #785).
- Bytecode trap: any task importing benchmark/scripts/*.py must use `python3 -B` and `sys.dont_write_bytecode = True` and check `git status --porcelain` (#785).
- Sessions with 0 turns (#794, #813), runtime interruption (#788), provider pause (#800), iteration not closing in quiet time (0190), tools disabled mid-session (#828) recur. Short limits, save files first.
- CLOSED: matched comparison #722; attempt-ledger seam #703 (F-A1, F-A2 open for owner); attempt policy #685.
- Real-envelope authority, legacy multiple-attempt selection: unresolved; no retrospective selection.
- Remaining method gaps: challenges row; dependency/native keys/access/grants/logs; restricted split/allocation/isolation (#636 blockers); reader/probes/scorer integration; independent whole-method review and owner acceptance/thresholds. benchmark_ready=false. Zero admissions, executions, scored runs, real comparisons.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- positive-control-review-finish-0193 (reviewer/default/medium, 40 min/30 turns): input #828 pins.txt, exports #828 report. Closes F3 (exact inventory file score.py reads, line), F2 (literal vs locator comparison, line refs; optional mutation on temp copy outside repo), F4. Artifacts pins-0193.txt, review-0193.md; git status clean.
- Check next: report verdict. CLEAR -> order step 4 (benchmark author + changed-scope reviewer in one graph) targeting the file named in F3. NOT-CLEAR -> correct named findings only.

## Tried, do not repeat
- Positive-control gap measurement: done (#820, plan-0189). Cold key: done (0191). Literal/locator/hash check: done (#828 F1). Do not re-derive or re-hash.
- Regeneration of challenges.json: done (#812/#816, CLEAR #817).
- Verification paths: score.py writes benchmark/results/challenges.json; benchmark/cases/dev/ holds copies of library-*.json not read by score.py (to be confirmed by 0193). Glob a path before asserting it (#812).
- Keyed-literal probe (0183) and control (#808, CLEAR #809): done. Constant-export probe #791/#797 done. Mutation check #785 done. #779 independent expectation done. #766/#778 re-pin done.
- Before re-ordering "paused" or failed work, Glob its expected output on main first (#800, 0190). Paused branches not resumable; partial with recorded branch is (#812 -> #816).
- Write the graph by ~10th call (0187 at 8, 0188 at 9, 0189 at 9, 0190 at 8, 0191 at 9, 0192 at 8, 0193 at 8).
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
