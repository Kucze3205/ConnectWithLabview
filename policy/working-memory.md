# Policy working memory

Updated by Policymaker #520 for iteration 0104. Considers records 0000-0103, actual #517/#518 reports,
journal memory, tag `iter/0103/518`, and the `origin/loop-runtime` checkpoints of 2026-11-13.
#520 compressed this file from 46,403 bytes to cut quota use (see `## Quota evidence`). Full predecessor:
`git show 29ae339:policy/working-memory.md` (sha256 f332799010f475ce09d126438d354c64815653fba89e2bf8fd76662d368b038e).
Older detail (0024-0091): `git show 2b6f6870:policy/working-memory.md`. Read them only for a pin or reason missing here.
History: `.session/history/records/<nnnn>.json`; session documents `.session/history/sessions/<issue>/`
(list with a python glob, not a broad Glob). Keep this file below about 16 KB: index and decisions, no copied report text.

## Organization
- Owner commit cfaf996: `shaper: orchestrator`, Fable 5.2 first for shaper and Policymaker, `every_iterations: 1`.
  Keep these owner settings; see the decision rule in `## Quota evidence`.
- With a shaper, the Policymaker orders ONLY evaluator/audit (`.github/loop/task-graph.md:36-37`). The shaper owns
  goal-directed tasks and `journal/working-memory.md`; it cannot read `policy/`. Reach it only through its skill,
  its handoff (`execution/roles/orchestrator/references/handoff.md`) and `execution/protocol.md`.
- Reviewer profile has `write: []` on purpose. Reviewers report in `.session/report.md` and `.session/artifacts/`.
  A permitted writer imports a saved review when a committed record is useful. Do not broaden reviewer writes.
- Shaper failure rule: one failed shaper, read its record before changing definitions. Two repeated failures:
  consider an owner proposal for shaper null or a script shaper. No valid tasks.json fails the iteration (engine.md:84-85).
- Audits #43/#55 crashed. Order an audit only for a concrete question with available data. None is open now.

## Iteration 0103 (considered by #520)
- Record 0103: closed, failure null, improved false, no_progress 2, limit_hits 21, wall 28,693 s. One task.
- Shaper #517 done/merged, 26 turns, actually codex/gpt-6.1-sol (one Fable request failed on quota first). Its first
  Finish was accepted: the #515 report-marker checkbox worked once. It respected reviewer output paths.
  Report: `.session/history/sessions/517/e2ffaf37b1303c3fbbcc1716afd821b70e00c777a8ce803de6ff3bd13ecf9cc9.md`.
- Researcher #518 blocked/unmerged, 18 turns, parked 25,945 s over 21 attempts (codex then claude-sonnet-5-5).
  Report: `.session/history/sessions/518/9a62eba046e42f4e0c74450d632d0dc76ebdc82f44788adf0f9091805f779fd9.md`.
  The work is complete and saved: tag `iter/0103/518`, commit `67412de4a986ce9611a28ff7e0f6750c9afe4171`, adds only
  `docs/research/poc/pair/review-0102.json` and `review-0102-provenance.md`. #520 read both from the tag:
  review bytes 5,320, SHA256 `562467370d558b15eb9a7faf8cb1bc283365f99ef3c8cada9c6f54f1ead8249f` (equals #513's
  artifact), verdict closed, reviewed commit `8f5ae4c48581459aa09b3f5e56f79db56188b86c`, one minor finding R1,
  four file pins equal to the #509 staging hashes below, NINE passed probes.
- Cause of the block: the shaper's verification asserted `len(probes)==8`, a count taken from the #513 report
  summary. The ninth probe is `protocol_blocks_virtual_execution`. The shaper had not read the artifact.
  Second defect: the task named `.session/inputs/iter-0102/...`; the engine staged `.session/inputs/513-review-0102.json`.
  #518 also lost three turns to rejected Finish calls (prose in status, then a missing report marker).
- #520 changes: (1) orchestrator skill, two bullets in `Writing a task`: assert only what you read in the source;
  resume saved blocked work with `start_branch: task/N` and a corrected check. (2) this compression.
  No profile, routing, ceiling or cadence change.
  Not applied: a report/Finish format paragraph for `execution/protocol.md`. The path guard rejected the Edit
  (`write is outside the role's accepted paths`), although the profile lists `execution/`. #520 did not retry and
  did not move the text to another file. Rejected Finish calls (#508, #512, #513, #518) therefore stay unrepaired
  for non-shaper roles; the engine's rejection message already gives the exact format, at a cost of one to three turns.
  Checks for the next Policymaker: record 0104 shows the two review files merged on main without a repeated copy
  or probe; startup.json tokens near 15,000. Count rejected Finish calls in `sessions/N.json` on
  `origin/loop-runtime` as a measurement only; no #520 change targets them.
- Owner request #516 (question, pending): author eight public VIs for the controlled comparison. It is open; do not
  file a duplicate. It blocks nothing. Owner silence accepts nothing.

## Quota evidence (first measurement, #520)
- Source: `git log origin/loop-runtime`, then `git show <commit>:pool.json` and `git show origin/loop-runtime:sessions/<N>.json`
  (fields `usage`, `requests`, `history`). This is cheap and needs no audit. It shows provider status, not billing.
- 04:04-04:55Z on 2026-11-13, iterations 0101-0103 ran back to back. Four Fable 5.2 sessions (#508, #511, #512, #515)
  sent 98 requests, 9.3 MB, about 3.96M cache-read, 305k cache-write and 89k output tokens. The Policymaker
  sessions #511/#515 are about 57% of that cache-read. #515 switched to codex after 24 Fable requests.
- Claude provider: `quota`, limit `session`, from 04:55Z; retry times grew to 10:13Z; `unknown` until 12:19Z;
  available at 12:31Z. Codex: `quota` (limit unspecified) from 04:59Z; at 10:29Z retry_after 15:49:11Z.
  Copilot: last observed 2026-11-08, `quota`; it is not in the researcher or orchestrator routing.
- Effect: #518, a 61 s task, waited 7.2 h; each resume sent about 230 KB again (sonnet: 28 requests, 6.3 MB).
  Other use of the same subscriptions outside the loop is unknown, so cause is not proved.
- Decision: one event does not override the owner's routing or cadence. #520 lowers its own cost instead (memory
  size). Rule: at a second Claude `session` limit event that follows Fable Policymaker/shaper sessions, file one
  owner `question` with both measurements and two options: `every_iterations: 3`, or Opus/Sonnet first for the
  shaper. Do not reorder owner settings unilaterally. No reordering helps when all providers are exhausted.
- Policymaker cost guide: #499/#503/#507 (codex) 17-24 turns; #511 27; #515 40; #520 about 30. Aim below 25 turns:
  startup, record, reports, one batched python check, writes, Finish.

## Evidence index (pins; read reports before reuse)
- POC, bounded unsuccessful delivery: #477, record 0093, commit d616e38; `docs/research/poc/delivery.md`,
  `verify_delivery.py` (`python3 -I`, pass in #479 = failure-delivery consistency only). add.vi 6,371 bytes, SHA256
  cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8, declared 21.0.0. Unresolved: primitive
  identity/replacement, DTHP/VCTP, ConstValue encoding, BDPW last 32 bytes, compiled-cache invalidation.
  Exit 1 = controlled same-version pairs (staged, waits for #516). Exit 2 = missing pinned source rules (deferred).
  No changed VI, no fresh-agent demonstration, no LabVIEW run. Not proof of impossibility.
- Pair staging #509: commit `53816a08feeb89a2747bf63ce8338ea315e06518`, `docs/research/poc/pair/`. SHA256:
  owner-instructions.md 55c1ed5ec72fe37b817afedeecb7abefad5b7577349683d9cbcbc69dcf78242b; pair_diff.py
  47d27dee98f1642dc401195482fbf43c536cef8a160aa399444d2e3a2d3578cb; protocol.md
  49255283f2814891ad7e0040e1f2ba4f54f6837bb8754769d7627ef84c374409; selfcheck.json
  9b76ed047caf417db5f87f7ea66f682354c84b91f231492d6603ef33ff57f79c; verification.json 718dca81....
  Review #513 (codex, same family as author): no major finding; minor R1 = pair_diff.py:229-237 rewrites tracked
  selfcheck.json. Report `.session/history/sessions/513/6abac9b44d6b454682b610752f52017e6c245a2e36964f6273d3dc8c330958e5.md`.
  The report says eight probes; the artifact lists nine. Keep the artifact unchanged. R1 does not block fixtures.
- Writing method, `benchmark/writing/` (seven files): authored #481 (0da7cad); review #485 REVISE S1-S3; correction
  #489 commit `2033c33fac195161fc3ac15b78f906a7d3140785`; re-review #493 CLEAR on
  `d3c697c375ed7dc880e55ab3cc2219577cd133a5` / tree `689ed2757ca4eb413cd37dc4f0cfcbc2fa90ba14`. method.json SHA256
  8c3b165c33c8fb4944f10a0eaa3c384fcc90d62c3278c0c910a5f2ae8b9d4da1. 44 rejecting controls, five positives.
  Synthetic design only: native executions 0, agent runs 0, benchmark_ready false. Re-pin and review changed bytes.
- Allocator guard: #497 CLEAR on `8aefb1583265f097a8569d76b4f8e5a0b0782833`; script SHA256 55c236ad...; closes #443
  finding 1. No direct preparation.json entries. Do not repeat.
- Effort study #501: commit `e67bb1a2b6da4f0c70b0e9b7655256018c90da11`, `docs/research/0099-writing-version-effort.md/.json`.
  33-99 d (2024 only) against 89-264 d (all versions) covers reading only. No full-goal total, ratio or fallback
  choice is supported. Not independently reviewed: review it before any fallback proposal.
- WM1 version measurement #505: commit `d9b03d16e86c6694991bc37076ea22a554951dab`, `docs/research/0100-wm1-version-evidence.*`.
  Five vers entries and one LVSR entry all declare raw `20008000`. Authoritative save version stays null.
- Preparation: `benchmark/preparation.json` (74 refs, ready/executed false), preparation-status.json. Baseline/split,
  challenges, coverage/oracle/sources/tasks and store #379 are design-reviewed. Owner method request #430 was
  declined (not_planned); `policy/proposals/method-acceptance-draft.md` needs writing coverage before reuse.
- No repeat without a new concrete question: gap maps #282/#330/#400; reviews #403/#408/#409/#415/#421/#427/#431/#443;
  lineage batches (stopped 0066); store searches; S1-S3 correction; allocator review; effort estimate; WM1 audit;
  POC delivery; #513's probes.

## Open gaps (state them in every evaluation report)
- No native benchmark run, agent comparison, native answer key, withheld writing case or verified isolation.
  Artifact/version/hardware coverage is incomplete. Tool quality is unmeasured. Capability #169 readiness unknown.
- No Goal gate is accepted; no `goal/gate.yml`; no completion claim. Product work waits for an independently
  reviewed method and owner acceptance of the pinned protocol and evidence. Writing also needs accepted writing-task
  coverage. Routine merges, green checks and owner silence accept nothing.
- Read `docs/perpetua/accepted-limits.md` before private use, disclosure, publication, spending or a capability
  request. Optional access never blocks an iteration.

## Session mechanics
- Report: first line `<!-- session-report -->`, then a fenced yaml block with `status:` equal to Finish.status, then
  prose. Write `wip` at the start. Finish.status is one word. Verify outputs just before Finish.
- git status/diff can show nothing for session writes. Read files back and check bytes. Empty Write.text truncates.
- Layer check for organization changes: `python3 policy/layer-rules.py .session/policy-facts.json` (facts JSON
  needed). Not needed for skill or memory text. Engine activation is authoritative.
- Empty orders: `.session/orders.json` = `{"tasks": []}`. `wake: true` only when results change the next order.
- Owner request format: `.github/loop/session-protocol.md` (Requests to the owner). Write owner text in STE.
- Two unfinished Policymakers in a row trigger a rollback (last: 2026-11-11T21:41:42Z).
- Evaluator changes need an evaluator order plus verifier; path `policy/evaluator/evaluate.py`.

## Next Policymaker
1. Read record 0104 and the reports. Run the three checks listed in `## Iteration 0103`.
2. If the review record is on main, the pair-tool review thread is closed except minor R1. If the shaper repeated
   the copy or the probes, tighten the skill bullet; do not order the work yourself.
3. Read the pool timeline for a second Claude `session` limit event; apply the rule in `## Quota evidence`.
4. If the owner supplies the pair (#516), the shaper pins all inputs once before comparison. Keep parser
   observations apart from semantic and native evidence. No substitute corpus diff, no new pair tool.
5. Keep policy orders to evaluator/audit. No duplicate estimation, audit, review or gap map.
