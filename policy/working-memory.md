# Policy working memory

Updated by Policymaker #530 for iteration 0106. Considers records 0000-0105, reports #526/#527/#528,
current journal memory, controlled-pair findings/status, and runtime checkpoints through 2026-11-13T16:04:11Z.
Startup diagnostic: ok, 15,160 estimated tokens, no notices. No pending suggestions; exports manifest has no results.
#520 compressed this file from 46,403 bytes. Full predecessor: `git show 29ae339:policy/working-memory.md`
(sha256 f332799010f475ce09d126438d354c64815653fba89e2bf8fd76662d368b038e).
Older detail (0024-0091): `git show 2b6f6870:policy/working-memory.md`. Read only for missing pins or reasons.
History entry: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`, reports
`.session/history/sessions/<issue>/`. List selected report paths with Python. Keep memory below about 16 KB.

## Organization and current decision
- Owner commit cfaf996: `shaper: orchestrator`, Fable 5.2 first for shaper and Policymaker, `every_iterations: 1`
  (`policy/params.yml:75`). #525 remains pending; leave settings unchanged and do not duplicate that request.
- With a shaper, Policymaker orders ONLY evaluator/audit (`.github/loop/task-graph.md:36-37`). The shaper owns
  goal-directed tasks and journal/working-memory.md; it cannot read policy/. Reach it through its skill,
  execution/roles/orchestrator/references/handoff.md or execution/protocol.md when a change is needed.
- #530: no role, routing, limit, evaluator or skill change. Empty policy orders. Iteration 0105 made an accepted
  improvement; no new audit question requires a session. Preserve quota by recording results and finishing.
- #526 crashed after three rebase conflicts; its report does not identify conflicting paths or prove a model fault.
  Successor #527 finished and merged a valid graph. This is one failed shaper followed by recovery, not two failures.
  If another shaper fails, inspect its exact conflict/error evidence before changing organization.
- Reviewer profile deliberately has `write: []`. Findings go to .session/report.md and .session/artifacts/.
  A permitted writer imports a saved review only if a committed record is useful. Do not broaden reviewer writes.
- Audits #43/#55 crashed. Order another only for a concrete question with available data; none is open now.

## Iteration 0105: controlled-pair measurement completed
- Record 0105: closed, accepted (routine change, not method acceptance), improved true, no_progress 0, one task,
  eight limit hits, wall 5,779 s, critical path 439 s. Task #528 merged commit bba00f7.
- Owner #516 is approved/completed. Eight public owner-authored VIs, fixtures/authoring.md and pins.json are on main
  under docs/research/poc/pair/. Authoring record identifies LabVIEW 2026 26.1.1f1, 32-bit. Do not ask for them again.
- #527 correctly prioritized newly available POC evidence over benchmark preparation. The task checked original
  fixture/authoring and reviewed-file pins before replay; its count of eight comes from the fixture manifest.
- #528 (Codex high, 28 turns, 410 agent s, 439 total s, no parking) ran all eight comparisons, exit 0 each.
  docs/research/poc/pair/findings-0105.md (94 lines) verdict: `edit-attempt-needs-more`.
  replay-0105-status.json preserves argv, exits, 15 input hashes, limitations and unchanged_inputs_after true.
  verification-0105.json records preflight/postflight checks; candidates-0105.json records derived byte alignments.
  These are measurements, not an independently reviewed edit rule or native validation.
- Candidate constant alignment repeats across save modes: BDHb insertion 44200200 at 312 and 01->02 at 545->549.
  Candidate primitive-associated transition: 1a->1b at normal BDHb 237; separate aligns left 237/right 232.
  They establish correlations only; shifted tails are not independent semantic changes.
- All eight comparisons change BDPW chunks 1/2, including save-setting pairs with identical BDHb.
  Separate files lack VICD but retain CPC2. Constant normal VICD is unchanged despite BDHb/DFDS changes.
  BDPW derivation, encoding/length rules, DFDS/VCTP dependencies and code/integrity handling remain unresolved.
- Raw declarations: every LVSR 26008000, vers/4 26118001. No changed VI, fresh-agent demonstration, LabVIEW run,
  behavior, unbroken arrow or save-version preservation was established. Coverage and tool quality remain unmeasured.
- Findings' smallest next measurement needs a new same-version, same-setting unchanged-diagram Save As/re-save
  control for constant-1-separate. That control is not established as available. Do not schedule its replay before
  readiness, invent a control, or repeat the eight completed comparisons. The control alone cannot make editing safe.
- Next shaper reads #528 report, findings, replay status and one comparison JSON. It decides on an exact owner
  question for the public control plus ready independent work, or another bounded measurement justified by available
  pinned sources. Any open request must not hold the iteration. If POC work waits, resume benchmark preparation
  after reading docs/perpetua/roles.md and evaluation.md. No new product work follows from these comparisons.
- Exact reports:
  .session/history/sessions/526/2123e2c05f68dc1404bc6814657b7c6a5d41b6cea87e84fd6031e860eff355fb.md;
  .session/history/sessions/527/3ec73801272ecbb295a01d5e3ee1ec913897ccb12f365b021d36e0e3b76c44c6.md;
  .session/history/sessions/528/115b26efbaf53b25a4ef8c66eacbb28ff1c9eda6e8a8dae8e653265d73094e52.md.

## Quota evidence and decision rule
- Owner criterion: accepted-result quality per subscription quota, not fastest elapsed time. Provider status is not
  billing or a quota-normalized model comparison. Outside subscription use is unknown; do not infer causation.
- Read actual runtime evidence using `git log origin/loop-runtime`, then selected `git show <commit>:pool.json`
  or `git show origin/loop-runtime:sessions/<N>.json`. Print only availability, usage and selected error summaries.
  Never dump histories: they contain whole repeated documents and can truncate away the relevant evidence.
- Event 1, 2026-11-13: iterations 0101-0103 ran 04:04-04:55Z. Four Fable sessions #508/#511/#512/#515 sent
  98 requests, 9.3 MB, about 3.96M cache-read, 305k cache-write, 89k output. Policymakers #511/#515 account for
  about 57% of cache-read. Claude session quota 04:55-12:31Z; #518's 61 s of work waited 7.2 h.
- Event 2: Policymaker #520 used 35 requests, 4.99 MB, 2.16M cache-read, 116k cache-write, 59k output.
  Claude session quota from 12:53:47Z; available 14:20:58Z. #521 had 146 s of work, parked 5,073 s (four attempts).
  In 0104 Policymaker used 80% of 2.68M cache-read; the task used 36k (1%).
- Event 3 measured by #530: pool 76bd7ca records Claude session quota at 14:46:05Z; 2c910e6 records it at
  14:46:30Z. Latest pool 3ead7eb (16:04:09Z) still records session quota observed 15:30:22Z, retry_after 16:10:22Z.
  Codex provider available observed 15:52:32Z; model available 16:03:49Z. Copilot last observed quota 2026-11-08.
  Provider state takes precedence over stale model-available entries. Do not treat retry_after as proven recovery.
- 0105 #526/#527 each had four attempts, parked 3,826/3,763 s respectively; these can overlap, do not add them
  into iteration downtime. Both used Fable and Codex. #528 used Codex without parking and produced accepted evidence.
  Record 0105 totals: 2,402,238 input, 42,977 output, 2,732,518 cache-read, 95,144 cache-write.
  No model attribution for conflict cause or scientific task quality is supported.
- #524 filed #525: "Decide if the Policymaker runs every 3 iterations to use less Claude quota".
  Completed means option A: change only every_iterations at policy/params.yml:75 to 3; no_progress stays 3,
  model order unchanged. Then compare the next three iterations' session-limit events and parked_s with prior events.
  Declined/pending means change nothing and do not resubmit. A new request needs a new kind of evidence,
  e.g. an iteration failure caused by quota. Event 3 repeats the existing kind; 0105 ultimately succeeded.
- Cost guide: #499/#503/#507 Codex 17-24 turns, #511 27, #515 40, #520 35, #524 about 19.
  Request bytes grow with turns; aim below 20 actions. Use focused reads, write memory/orders/report, then Finish.

## Evidence index (pins; read sources before reuse)
- POC bounded unsuccessful delivery #477, record 0093, commit d616e38: docs/research/poc/delivery.md,
  verify_delivery.py (`python3 -I`, pass in #479 means failure-delivery consistency only). Original add.vi 6,371 bytes,
  SHA256 cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8, declared 21.0.0.
  Controlled owner pairs now measured; missing source rules remain. Failure delivery is not proof of impossibility.
- Pair preparation #509 commit 53816a08feeb89a2747bf63ce8338ea315e06518, docs/research/poc/pair/:
  owner-instructions.md SHA256 55c1ed5ec72fe37b817afedeecb7abefad5b7577349683d9cbcbc69dcf78242b;
  pair_diff.py 47d27dee98f1642dc401195482fbf43c536cef8a160aa399444d2e3a2d3578cb;
  protocol.md 49255283f2814891ad7e0040e1f2ba4f54f6837bb8754769d7627ef84c374409;
  selfcheck.json 9b76ed047caf417db5f87f7ea66f682354c84b91f231492d6603ef33ff57f79c.
- Review #513 (Codex, same family as author) of 8f5ae4c48581459aa09b3f5e56f79db56188b86c: closed, no major,
  nine passed probes (report summary said eight). #522 preserved review-0102.json (5,320 bytes), SHA256
  562467370d558b15eb9a7faf8cb1bc283365f99ef3c8cada9c6f54f1ead8249f and review-0102-provenance.md, commit 5c6dc23.
  Minor R1: --self-check rewrites tracked selfcheck.json. Avoid it; fix only alongside a necessary tool change,
  then independently review changed bytes. No repeat copy, probe run, or review of unchanged preparation.
- #518 was blocked only by the shaper's false probe count. #520 added assert-only-source-values and saved-work
  resumption bullets to orchestrator skill. #521/#522 used them successfully; #522 completed in seven turns.
- Writing method benchmark/writing/ (seven files): #481 0da7cad, review #485 REVISE S1-S3, correction #489
  2033c33fac195161fc3ac15b78f906a7d3140785, re-review #493 CLEAR at d3c697c375ed7dc880e55ab3cc2219577cd133a5,
  tree 689ed2757ca4eb413cd37dc4f0cfcbc2fa90ba14. method.json SHA256
  8c3b165c33c8fb4944f10a0eaa3c384fcc90d62c3278c0c910a5f2ae8b9d4da1. 44 rejecting controls, five positives.
  Synthetic design only: native executions 0, agent runs 0, benchmark_ready false. Re-pin/review changed bytes.
- Allocator guard #497 CLEAR at 8aefb1583265f097a8569d76b4f8e5a0b0782833, script SHA256 55c236ad...;
  closes #443 finding 1. No direct preparation.json entries. Do not repeat.
- Effort study #501 commit e67bb1a2b6da4f0c70b0e9b7655256018c90da11, docs/research/0099-writing-version-effort.*:
  33-99 days (2024) versus 89-264 days (all versions) covers reading only. No full-goal total, ratio or fallback
  choice follows. Independently review before using for a fallback proposal. Study assumes 8.0-2025; fixtures are 2026.
- WM1 #505 commit d9b03d16e86c6694991bc37076ea22a554951dab, docs/research/0100-wm1-version-evidence.*:
  five vers and one LVSR declaration raw 20008000; authoritative save version null. Different file from 0105 fixtures.
- Preparation: benchmark/preparation.json (74 refs, ready/executed false), preparation-status.json. Baseline/split,
  challenges, coverage/oracle/sources/tasks and store #379 design-reviewed. Method request #430 declined;
  policy/proposals/method-acceptance-draft.md needs writing coverage before reuse.
- Do not repeat without a new question: gap maps #282/#330/#400, reviews #403/#408/#409/#415/#421/#427/#431/#443,
  lineage batches (stopped 0066), store searches, S1-S3 correction, allocator review, effort estimate, WM1 audit,
  negative POC delivery, #513 probes/review preservation, or #528's completed eight comparisons.

## Open gaps (state them in every evaluation report)
- No native benchmark run, agent comparison, native answer key, withheld writing case or verified isolation.
  Artifact/version/hardware coverage incomplete; tool quality unmeasured. Capability #169 readiness unknown.
- No Goal gate accepted; no goal/gate.yml; no completion claim. Product needs independently reviewed method
  and owner acceptance of pinned protocol/evidence. Writing also needs accepted writing coverage.
  Routine merges, green checks and owner silence do not establish acceptance or benchmark readiness.
- Read docs/perpetua/accepted-limits.md before private use, disclosure, publication, spending or capability requests.
  Optional access never blocks an iteration. Resource-dependent tasks wait for verified readiness.

## Session mechanics
- Report: first line <!-- session-report -->, fenced yaml status equal to Finish.status, then prose.
  Write wip early. Finish.status is one word. Read required outputs just before Finish.
- Session writes may not appear in git status/diff. Verify file content. Empty Write.text truncates.
  Continuations can contain successful historical Writes while current session files are absent (#526/#527).
  Read current outputs before trusting their presence; recreate only missing session outputs from saved work.
- Layer check for organization changes: python3 policy/layer-rules.py .session/policy-facts.json (facts needed).
  Not needed for memory/skill prose. Engine activation is authoritative.
- Empty orders: {"tasks": []}. wake true only if results change the next order.
- Owner request format: .github/loop/session-protocol.md, Requests to the owner. JSON list with kind/title/what/why/
  unblocks. Question means yes/no without engine effect. Owner text uses Simplified Technical English.
- Two unfinished Policymakers trigger rollback (last 2026-11-11T21:41:42Z). Keep this session bounded.
- Evaluator changes need evaluator order plus verifier; path policy/evaluator/evaluate.py.

## Next Policymaker
1. Read record 0106 and actual reports. Check the shaper judged #528's needs-more verdict without claiming edit readiness.
2. Check #525 decision and apply the exact cadence rule above; do not submit the same request again.
3. Verify any new control's readiness before scheduling comparison. Owner silence supplies neither files nor evidence.
4. If POC work waits, ensure ready benchmark preparation resumes only after roles.md/evaluation.md reads.
5. Inspect another shaper failure before changing organization. Do not infer conflict paths or model fault from counts.
6. Keep policy orders to evaluator/audit; avoid duplicate comparisons, audit, review, estimate or gap maps.
