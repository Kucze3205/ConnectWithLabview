# Policy working memory

Updated by Policymaker #524 for iteration 0105. Considers records 0000-0104, actual #521/#522 reports,
journal memory, the two review files on the checkout, and the `origin/loop-runtime` checkpoints of 2026-11-13.
#520 compressed this file from 46,403 bytes to cut quota use (see `## Quota evidence`). Full predecessor:
`git show 29ae339:policy/working-memory.md` (sha256 f332799010f475ce09d126438d354c64815653fba89e2bf8fd76662d368b038e).
Older detail (0024-0091): `git show 2b6f6870:policy/working-memory.md`. Read them only for a pin or reason missing here.
History: `.session/history/records/<nnnn>.json`; session documents `.session/history/sessions/<issue>/`
(list with a python glob, not a broad Glob). Keep this file below about 16 KB: index and decisions, no copied report text.

## Organization
- Owner commit cfaf996: `shaper: orchestrator`, Fable 5.2 first for shaper and Policymaker, `every_iterations: 1`
  (`policy/params.yml:75`). Keep these owner settings until the owner decides the #524 request (`## Quota evidence`).
- With a shaper, the Policymaker orders ONLY evaluator/audit (`.github/loop/task-graph.md:36-37`). The shaper owns
  goal-directed tasks and `journal/working-memory.md`; it cannot read `policy/`. Reach it only through its skill,
  its handoff (`execution/roles/orchestrator/references/handoff.md`) and `execution/protocol.md`.
- Reviewer profile has `write: []` on purpose. Reviewers report in `.session/report.md` and `.session/artifacts/`.
  A permitted writer imports a saved review when a committed record is useful. Do not broaden reviewer writes.
- Shaper failure rule: one failed shaper, read its record before changing definitions. Two repeated failures:
  consider an owner proposal for shaper null or a script shaper. No valid tasks.json fails the iteration (engine.md:84-85).
- Audits #43/#55 crashed. Order an audit only for a concrete question with available data. None is open now.

## Iterations 0103-0104 (pair-tool review record: closed)
- 0103: researcher #518 blocked/unmerged after 21 quota attempts. Cause: the shaper's check asserted `len(probes)==8`,
  a count from the #513 report summary; the artifact lists nine. #520 added two bullets to the orchestrator skill
  (`Writing a task`): assert only what you read in the source; resume saved blocked work with `start_branch: task/N`.
- 0104: record closed, verdict accepted (issuer owner, routine change), improved true, no_progress now 0, one task,
  limit_hits 4, wall 6,978 s, critical path 66 s. Policy change-520 applied at 12:49:59Z.
- Shaper #521 (Fable 5.2, 17 turns, 21 requests, 1.28 MB, 487k cache-read): one task with `start_branch: task/518`
  and a check without a probe count. Both #520 bullets worked on first use. Its first report write was empty text.
  Report: `.session/history/sessions/521/8852d277fe05653d4a6f71deac8a82857163717c2c9e24ca8b7e10457987b100.md`.
- Researcher #522 (sonnet, low, 7 turns, 66 s, 36k cache-read): done, merged, commit 5c6dc23. No copy or probe repeated.
  Report: `.session/history/sessions/522/dcf6e5bc11fc2567795a993fa6c56496fc92efb9271239aa129d84b900d2434a.md`.
- #524 read the checkout: `docs/research/poc/pair/review-0102.json` SHA256
  `562467370d558b15eb9a7faf8cb1bc283365f99ef3c8cada9c6f54f1ead8249f`; `review-0102-provenance.md` states nine probes.
  The thread is closed. Minor R1 stays open (see the pair staging pin). No native claim follows from it.
- Rejected Finish calls: #522 one (report without marker), #521 none. Still unrepaired for non-shaper roles: the path
  guard rejected #520's Edit of `execution/protocol.md`. #524 did not act: one cheap worker turn costs less than the
  Policymaker turns needed. If a costly session loses turns to it, add one line on the report format to the task
  template in the orchestrator skill (a writable path) instead of `execution/protocol.md`.
- Shaper plan for 0105 (its report): one ready benchmark preparation task that needs neither #516 nor native capability.
- Owner request #516 (question, pending): author eight public VIs for the controlled comparison. Do not file a
  duplicate. It blocks nothing. Owner silence accepts nothing.

## Quota evidence (two measurements)
- Source: `git log origin/loop-runtime`, then `git show <commit>:pool.json` and `git show origin/loop-runtime:sessions/<N>.json`
  (fields `usage`, `requests`, `history`). This is cheap and needs no audit. It shows provider status, not billing.
- Event 1, 2026-11-13: iterations 0101-0103 ran back to back 04:04-04:55Z. Four Fable 5.2 sessions (#508, #511, #512,
  #515) sent 98 requests, 9.3 MB, about 3.96M cache-read, 305k cache-write, 89k output. Policymakers #511/#515 are
  about 57% of that cache-read. Claude `quota`, limit `session`, 04:55Z to 12:31Z. #518 (61 s of work) waited 7.2 h.
- Event 2, 2026-11-13: Policymaker #520 (35 requests, 4.99 MB, 2.16M cache-read, 116k cache-write, 59k output) ended
  about 12:50Z. Shaper #521 started; Claude `quota`, limit `session`, from 12:53:47Z; retry steps to 14:17:53Z;
  available at 14:20:58Z. #521 had 146 s of work and was parked 5,073 s (4 attempts). In 0104 the Policymaker used
  2.16M of 2.68M cache-read (80%); the work task used 36k (1%).
- Codex: `quota` (limit unspecified) from 04:59Z, retry_after 15:49:11Z at the last checkpoint. Copilot: last observed
  2026-11-08, `quota`. Other use of the subscriptions outside the loop is unknown, so cause is not proved.
- Decision by #524 (the #520 rule fired): one owner `question` filed in `.session/requests.json`, title
  "Decide if the Policymaker runs every 3 iterations to use less Claude quota". Completed = option A
  (`every_iterations: 3`, `no_progress: 3` and model order unchanged). Not planned = keep settings; the owner can
  apply option B (Opus/Sonnet before Fable in the `orchestrator` list) by hand. Find its number in
  `owner_requests` of loop-state.
  - Accepted: change only `policy/params.yml:75` to 3; then compare `session` limit events and `parked_s` of the next
    three iterations with events 1 and 2.
  - Declined or pending: change nothing and do not file it again. A new request needs a new kind of evidence
    (for example a failed iteration caused by quota).
- Policymaker cost guide: #499/#503/#507 (codex) 17-24 turns; #511 27; #515 40; #520 35; #524 about 19. Request bytes
  grow with each turn, so cost is roughly quadratic in turns. Aim below 20 turns: startup, record, one batched python
  read of reports and pool, writes, Finish. With nothing to decide: record, memory header, empty orders, Finish.

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
  Review #513 (codex, same family as author) of commit `8f5ae4c48581459aa09b3f5e56f79db56188b86c`: verdict closed, no
  major finding, nine passed probes (its report text says eight), minor R1 = pair_diff.py:229-237 rewrites tracked
  selfcheck.json. Committed record on main since #522: `review-0102.json` (5,320 bytes, SHA256 above) and
  `review-0102-provenance.md`. Keep the artifact unchanged. R1 does not block fixtures; fix it only when the tool
  changes for another reason, then re-review the changed bytes.
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
  POC delivery; #513's probes; the review-record copy and its hash/pin checks.

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
- Owner request format: `.github/loop/session-protocol.md` (Requests to the owner): JSON list with `kind`, `title`,
  `what`, `why`, `unblocks`. A `question` is yes/no with no engine effect. Write owner text in STE.
- Two unfinished Policymakers in a row trigger a rollback (last: 2026-11-11T21:41:42Z).
- Evaluator changes need an evaluator order plus verifier; path `policy/evaluator/evaluate.py`.

## Next Policymaker
1. Read record 0105 and the reports. Check that the shaper ordered ready benchmark preparation work that needs
   neither #516 nor native capability, and that its checks assert only values read from the source.
2. Read `owner_requests` in loop-state for the quota request filed by #524; apply the rule in `## Quota evidence`.
3. Read the pool timeline after 14:28Z on 2026-11-13 for another Claude `session` limit event; record it as a
   measurement. Do not file a second request for the same evidence.
4. If the owner supplies the pair (#516), the shaper pins all inputs once before comparison. Keep parser
   observations apart from semantic and native evidence. No substitute corpus diff, no new pair tool.
5. Keep policy orders to evaluator/audit. No duplicate estimation, audit, review or gap map.
