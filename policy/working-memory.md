# Policy working memory

Considered: iteration records 0000-0092, owner commit cfaf996, and accepted #473's
`docs/research/poc/edit-readiness.md`. Updated by Policymaker #475 for iteration 0093.
Earlier detailed memory (0024-0091, 110 KB): `git show 2b6f6870:policy/working-memory.md`
(sha256 68d353d1...). Compressed predecessor: accepted change #471, commit 5268784.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
session documents `.session/history/sessions/<issue>/` (list with python glob, not broad Glob).

## Organization and evidence
- Owner commit cfaf996 restored `shaper: orchestrator`, Fable 5.2 first for shaper and Policymaker.
  Keep that routing order. Cadence stays `every_iterations: 1`; one measured success is insufficient to change it.
- With a shaper, Policymaker orders ONLY evaluator/audit (task-graph.md:36). No such order is needed in 0093.
  The shaper owns goal-directed tasks and journal memory; it cannot read policy/.
- #471 rewrote the orchestrator skill with graph-first by about tool call 12, four-section journal memory,
  POC priority and a startup handoff; raised max_turns 30 -> 45. Repeated shaper turn-cap failures motivated it.
- Record 0092 confirms recovery: closed/accepted, one task, no failure; #472 done in 19 turns; all four journal
  sections exist. #473 accepted/merged 7b37e07, 44 turns. Rollback timestamp remains 2026-11-11T21:41:42Z.
  The record does not show which tool call first wrote tasks.json; do not claim that deadline was measured.
- #472 startup estimate 12,188 tokens is consistent with the added package; journal memory cites the staged handoff.
  A report snapshot exists. No report/request permission failure was observed; requests permission remains untested.
- #475 removes the handoff from mandatory startup and the Cold start read rule. The journal now carries execution
  state. The optional handoff is shorter, removes stale empty-journal claims and unmeasured hypotheses, preserves
  task-writing lessons/paused-thread pointers, and links #473's result. No limits, routing or cadence changed.
  Expected gain: fewer repeated startup reads without losing the task graph or POC continuity. Check record 0093
  startup estimate, shaper done status, valid tasks, and journal update incorporating #473.
- If the shaper fails, read its record before changing definitions. One failure: tighten graph-first if evidence
  supports it. Two repeated failures: consider an owner proposal for shaper null or a script shaper, with reasons.
  An iteration with a shaper fails on no valid tasks.json, not on empty Policymaker orders (engine.md:84-85).

## POC state and next work
- Goal adds writing and POC before further benchmark preparation. POC is the method-first exception, not a product
  or quality result. No session can run LabVIEW. Successful delivery needs files, report, owner manual instructions,
  save-version preservation and a fresh-agent demonstration. Unsuccessful delivery needs evidence and possible exits.
  Do not wait for owner replies after delivery; silence does not accept the method or quality.
- #465: RSRC/save version of pylavi add.vi. #468 (merged 0f35a16): inspect_vi.py, complete BDHb framing,
  162 entries/842 bytes; no semantic edit. Do not repeat container/decompression/framing research.
- #473: `docs/research/poc/edit-readiness.md` and `.json`, verdict partial after eight original VIs.
  Neither primitive nor constant route supplies an executable semantic recipe. Do not order a disk edit from it.
  Primitive identity/replacement remains unknown; ConstValue needs DTHP/VCTP type resolution/encoding;
  BDPW's last 32 bytes and compiled-cache invalidation remain unexplained. LVparts lacks the relevant classes.
  No edited VI, native behavior result or unseen-VI demonstration exists.
- Shaper next reads #473's result and linked evidence, then chooses a bounded missing-source follow-up or
  documented unsuccessful POC delivery. Controlled same-version fixture pairs are another exit only after verified
  availability. No broad corpus search or repeat of 103 -> 104 speculation. No task waits for optional access.
- `journal/working-memory.md` currently precedes #473; its This iteration section already directs the next shaper
  to read edit-readiness. The optional handoff also carries the new result. Policymaker does not edit journal memory.

## Paused benchmark and gate
- Benchmark work not needed for POC waits for POC delivery. Read `docs/perpetua/evaluation.md` before planning
  reader/product work or resuming benchmark planning. Independent method review and owner acceptance still apply.
- Existing preparation: preparation.json 99069d8d..., preparation-status.json 8f64e982...; prior evaluator check
  errors [], missing [], 74 refs, ready/executed false. Not rerun in #475. Quality is unmeasured; missing native,
  artifact/version, held-out and write-task coverage stays visible. A functioning checker does not establish readiness.
- Baseline/split design-reviewed; challenges scorer-reviewed; coverage/oracle/sources/tasks reviewed. Store #379
  reviewed in #431 and pinned. Unpinned review pending: allocation.synthetic.json 70d94d28... and split_allocate.py
  55c236ad... (fix #446 for #443 finding 1, fix round 1 used). Recheck before resuming.
- Owner method request #430 declined as not_planned. Old draft policy/proposals/method-acceptance-draft.md needs
  writing coverage before reuse. No Goal gate is accepted; no goal/gate.yml or completion claim.
- All-version estimate: docs/research/0002-delivery.md, 89-264 d versus 33-99 d 2024-only; strict 2024 excludes
  413/415 RSRC files. It omits writing. Reconcile before fallback choice; do not repeat the original research.
- No repeat: gap maps #282/#330/#400; reviews #403/#408/#409/#415/#421/#427/#431/#443;
  lineage batches stopped in 0066 (no allocation effect; policy/proposals/lineage-pilot-359.json); store searches.
- policy/proposals/store-readiness.yml equals installed workflow revision 4 (27b365ec...); optional deletion remains.

## Resources and open questions
- No pending suggestions in loop state 0093. No owner requests listed open. Capability #169 readiness remains
  unknown; disappearance from owner_requests.open is not proof of availability or closure.
- No quota-use measurement exists. Input/cache accounting is not subscription quota use; model labels are not
  actual routing. Record 0092: #473 entirely codex; #472 Fable plus codex. No routing change from these counts.
- After two consecutive shaper iterations with tasks, reconsider Policymaker cadence; owner set every iteration.
  After three, an audit can measure accepted results/resource evidence if it has a concrete question and real inputs.
  No audit ordered now; previous #43/#55 crashed. Keep the current iteration short.
- Read docs/perpetua/accepted-limits.md before private use/disclosure/publication/spending or capability requests.
  Optional access uses capability proposals, never iteration dependencies or waiting tasks.

## Session mechanics to preserve
- Report starts with <!-- session-report --> and yaml status matching Finish.status. Verify session outputs just
  before Finish: provider switches lost them in #368/#402/#429. Two unfinished Policymakers trigger rollbacks.
- git status/diff can show nothing for session writes (#471). Read back files and check bytes/hashes instead.
  Empty Write.text truncates. Verify each managed write. Layer check needs a facts JSON argument:
  `python3 policy/layer-rules.py .session/policy-facts.json`. #475's first call omitted it and failed;
  regenerated facts from current profiles/params then passed with errors []. Startup references and empty orders
  also passed local assertions. Engine activation remains authoritative.
- wake true only when results change the next policy order; iteration 0055 wasted eight tasks/2.7M input.
- Task lessons live in the optional shaper handoff: parent commits; offline plain python3 verification; reviewer
  starts from main/report only; bounded reads; at least 25 turns; repin changed benchmark files; resume via task/N.
- Preparation JSON uses json.dumps(indent=2, sort_keys=True) + newline; changes to preparation-status.json need
  every reference re-pinned. lineage.py --check needs LABVIEW_ENVIRONMENT. Evaluator changes require evaluator
  order plus verifier; path policy/evaluator/evaluate.py.

## Next Policymaker
1. Read record 0093 and journal/working-memory.md. Check tasks, shaper status, startup estimate and #473 continuity.
2. Check suggestions. Keep role changes tied to measured failures or unnecessary repeated reads.
3. Avoid repeating #465/#468/#473, benchmark gap maps, or speculative format claims. Let the shaper choose POC work.
