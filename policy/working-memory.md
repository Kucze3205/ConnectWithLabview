# Policy working memory

Updated by Policymaker #535 for iteration 0107. Considers records 0000-0106, reports #524/#531/#533,
current journal memory, constant-rules-0106.md, and loop-state owner decisions. Older runtime evidence remains dated below.
Startup diagnostic: ok, 15,559 estimated tokens, no notices. No pending suggestions; exports manifest has no results.
#520 compressed this file from 46,403 bytes. Full predecessor: `git show 29ae339:policy/working-memory.md`
(sha256 f332799010f475ce09d126438d354c64815653fba89e2bf8fd76662d368b038e).
Older detail (0024-0091): `git show 2b6f6870:policy/working-memory.md`. Read only for missing pins or reasons.
History entry: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`, reports
`.session/history/sessions/<issue>/`. List selected report paths with Python. Keep memory below about 16 KB.

## Organization and current decision
- #535 applies approved/completed Owner request #525 option A: `every_iterations: 3` in policy/params.yml.
  Keep `no_progress: 3`, shaper, model order and other settings unchanged. Do not duplicate the request.
  Compare iterations 0107-0109 session-limit events, parked_s and accepted outcomes with the dated baseline below.
  Expected benefit: about two thirds fewer regularly triggered Policymaker sessions; quota saving is not measured yet.
- With a shaper, Policymaker orders ONLY evaluator/audit (`.github/loop/task-graph.md:36-37`). The shaper owns
  goal-directed tasks and journal/working-memory.md; it cannot read policy/. Reach it through its skill,
  execution/roles/orchestrator/references/handoff.md or execution/protocol.md when a change is needed.
- #535: cadence change only; no role, routing, evaluator or skill change. Empty policy orders. Iteration 0106
  made an accepted improvement; no new audit question requires a session. The shaper continues goal work.
- #526 crashed after three rebase conflicts; its report does not identify conflicting paths or prove a model fault.
  Successor #527 finished and merged a valid graph. This is one failed shaper followed by recovery, not two failures.
  If another shaper fails, inspect its exact conflict/error evidence before changing organization.
- Reviewer profile deliberately has `write: []`. Findings go to .session/report.md and .session/artifacts/.
  A permitted writer imports a saved review only if a committed record is useful. Do not broaden reviewer writes.
- Audits #43/#55 crashed. Order another only for a concrete question with available data; none is open now.

## Iterations 0105-0106: controlled-pair result and source blocker
- 0105 #528 merged bba00f7: eight controlled comparisons, all exit 0, unchanged_inputs_after true.
  Owner #516 supplied all eight public fixtures; do not request them again. LabVIEW 2026 26.1.1f1 32-bit.
  findings-0105.md verdict edit-attempt-needs-more; replay-0105-status.json, verification-0105.json and
  candidates-0105.json save the measurements. No rerun or pin creation is needed.
- Record 0106: closed, accepted (routine change, not method acceptance), improved true, no_progress 0,
  one task, zero limit hits, wall 1,898 s, critical path 638 s. #531 shaper and #533 researcher both Codex,
  parked_s 0 each, 22/27 turns respectively. Totals 3,753,489 input, 28,546 output, 3,476,224 cache-read.
  These tokens do not establish quota-normalized efficiency or the cause of prior Claude limits.
- #531 judged the replay as needs-more, ordered bounded source research and opened optional public control
  request #532. It did not schedule the unavailable control or authorize an edit. Request #532 remains pending.
  No duplicate request or control comparison before original/control pins and authoring establish readiness.
- #533 merged fc70efc. docs/research/poc/pair/constant-rules-0106.md verdict source-blocked. Its JSON records
  38 repository hashes, eight prepared-file pins and ten probes; read only relevant probes before reuse.
  P1 parses BDHb [312,316) as textHair OF__flags leaf 4420|0200; meaning/necessity remains unknown.
  P2 places 545/549 inside four-byte ConstValue bodies 00000001->00000002 under DCO UID 118.
  Typed dispatch remains unresolved. The same BDHb transitions occur in both save modes; normal DFDS
  also changes at 223. This supports boundaries for these originals, not a safe general editing rule.
- P4/P6: prepared pylavi production hashes equal the prior source-search hashes; LVblock/LVdatatype/LVrsrc
  implementations are absent. Reuse prior absence; do not repeat unchanged source searches.
  P5 tests empty-password MD5 for BDPW chunk 0 only. Chunks 1/2 have no staged recipe.
  P7 equal BDHb with different BDPW tails refutes BDHb-only dependence. RTSG/LVSR/code/type rules remain open.
- #533 reports checker exit 0 with empty-environment success and ten rejected malformed/contradictory controls.
  Policymaker read the report and findings, not checker code, full JSON or prepared sources; no independent
  review or repeated measurement occurred here. Original fixtures and replay inputs are reported unchanged.
- No changed VI, fresh-agent demonstration, LabVIEW run, behavior, unbroken arrow or save-version preservation
  was established. Raw LVSR 26008000 and vers/4 26118001 are declarations, not native authority.
  Artifact/version coverage remains incomplete; benchmark readiness and tool quality remain unmeasured.
- Next shaper reads #533 and the source-blocked findings. Only a newly available pinned primary BDPW source
  or a verified new control justifies bounded POC follow-up; neither supplies a general edit rule by itself.
  If neither is ready, resume ready benchmark preparation after roles.md/evaluation.md reads. No owner wait,
  product implementation, repeated replay, corpus discovery or unchanged-source-absence investigation.
- Exact reports:
  .session/history/sessions/531/38ea44b7693439c45b723fd125147437d5013d25d0d7930ec914b2448b3893ee.md;
  .session/history/sessions/533/02493d512ed1055f2034c00d258ea102ee8929d0aa387880df1a4418f2822015.md.

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
  #535 sees approved/completed in loop-state and applies option A: only every_iterations becomes 3.
  no_progress stays 3, model order unchanged. Compare 0107-0109 session-limit events and parked_s with prior events.
  Request #525 is fulfilled; do not resubmit. A different request needs new evidence, such as an iteration
  failure caused by quota. Event 3 repeats the existing kind; 0105 and 0106 ultimately succeeded.
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
1. Confirm cadence activation from loop-state: every_iterations 3, no_progress 3, other settings unchanged.
2. Compare 0107-0109 session-limit events, parked_s and accepted results with the dated quota baseline.
   Read actual runtime summaries if needed; no causal quota-saving claim from fewer sessions alone.
3. Read intervening records and reports. Check that source-blocked #533 did not become edit readiness.
4. Verify any new control/source readiness before follow-up. #532 is pending; do not duplicate it or wait.
5. If no ready POC evidence arrives, ensure benchmark preparation resumes after roles.md/evaluation.md reads.
6. Keep policy orders to evaluator/audit; no duplicate replay, source-absence search, audit, estimate or gap map.
