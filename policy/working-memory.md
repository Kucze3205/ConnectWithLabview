# Policy working memory

Considered: iteration records 0000–0014; reviews #146/#147; #150 report and acceptance #151; #157 report and
acceptance #161; engine code `run_policy_script` (.github/loop/iteration.py:511-548), tokenless-job.yml, commit
a9a3a30. Updated by Policymaker #164, iteration 0015 (restores #153's memory, which rollback d546ab6 discarded).
Historical inputs: `.session/history/manifest.json`; records `.session/history/records/<n>.json`;
reports `.github/loop/data/session-reports/<issue>/*.json`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; it supplies the iteration's work.
- Iteration 0014 FAILED: `policy/session-state.py returned no output from the tokenless job`. Sessions #154-#157
  were marked crashed; policy/ was rolled back to 830b7b73 (d546ab6). The script itself is fine: the same facts run
  locally exit 0 in 0.04 s and print 494 kB of valid JSON (limit 8 MB, 4 kB is only for other scripts). #157 later
  re-ran through the tokenless job and finished `done`. Cause: the engine treats a missing stdout.txt/exit-code
  as a policy fault (iteration.py:536-537), though the job's redirect makes stdout.txt before the script starts.
- Filed `engine-change` (iteration 0015, .session/requests.json): missing stdout.txt -> TokenlessUnavailable (no
  rollback). `git apply --check` passed on d7ba8a0. Does not cover missing exit-code with stdout present (timeout).
- benchmark/resources-proposal.md is on main (#157 done, owner-accepted #161): 7 rows plus a filing checklist;
  rows 1 (restricted store) and 2 (native job runner) most developed; rows 1, 4, 5 need non-public access;
  row 7 needs no new access. Not yet turned into `capability` requests.
- Protocol F1/F2 revision 2669ec4 (vs cf38154) is still unreviewed: #154/#156 never ran.
- Evaluator --check (as of #150): exit 0, 8 evidence refs, benchmark_ready=false; tasks/oracle/split/baseline/
  challenges missing. Not readiness. Coverage incomplete; quality unmeasured.

## Orders for iteration 0015
- `order-164-rereview-protocol-f1f2` (reviewer, high, 60 min/30 turns, exports reports 146/147/150): same task as
  0014's crashed one. Reviewer routing is Claude-first (author #150 finished on codex); actual family must be reported.
- No wake. Resource-capability drafting deferred: needs a Policymaker check of the proposal against
  docs/perpetua/accepted-limits.md first; do it next session (read only the proposal + limits, ~13 kB + 6 kB).

## Next Policymaker
- Read the re-review report. accept -> ask the owner (question request) to accept the pinned protocol and evidence
  through the change gate; revise -> order only the evidenced correction, author family other than reviewer.
- Check the engine-change request outcome. If 0015 fails the same way again, the request is the fix; do not edit
  session-state.py for it (its output is valid).
- Draft `capability` requests for rows 1 and 2 of resources-proposal.md if they satisfy the filing checklist;
  unknowns become owner questions. Open requests must not block other ready work.

## Milestone evidence
- sources: review #134 revise -> fix #139 -> re-review #140 accept at d588fa9. Coverage review #133 accept at
  6933e17 as limited inventory. Both stay prepared-not-reviewed in preparation-status.json; owner gate decides.

## Mechanisms to preserve
- Input ceiling 800k unique input; codex counts all non-cached input. Never read sources.json/coverage.json
  directly; bounded Python summaries. Keep sessions short.
- Task Verification runs in-session and again offline over committed files.
- Rebase runs evaluator --check; changed pinned files need preparation.json re-pinning.
- Missing git identity: leave changes staged; parent engine commits.
- Requests: `.session/requests.json`, format `.github/loop/session-protocol.md` ("Three additional kinds").
  Orders: `.github/loop/task-graph.md`; order ids must not repeat ids used in the same iteration.
- Read docs/perpetua/evaluation.md before product planning; accepted-limits.md before private data or spending.

## Open questions
- Notice #92 pending for the owner. Do not reinstate the crashed script shaper without contract review.
- Duplicate sessions per order: 0012 (#146/#147) and 0014 (#154/#156, #155/#157), same ids, different issues.
  Recurring; doubles quota when both run. Collect engine evidence (task_graph.create_tasks / policy_pass settle
  called twice?) before an engine-change.
- Claude availability unmeasured; 0011-0013 sessions mostly finished on codex.
- All-version effort estimate needed before any LabVIEW 2024 fallback choice; not started.
- How a commit-bound review recommendation becomes milestone `reviewed` status: unresolved; owner gate decides.
