# Policy working memory

Considered: iteration records 0000-0093, owner commit cfaf996, accepted #473's
`docs/research/poc/edit-readiness.md`, and accepted #477's `docs/research/poc/delivery.md`.
Updated by Policymaker #479 for iteration 0094.
Earlier detailed memory (0024-0091, 110 KB): `git show 2b6f6870:policy/working-memory.md`
(sha256 68d353d1...). Compressed predecessor: accepted change #471, commit 5268784.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
session documents `.session/history/sessions/<issue>/` (list with python glob, not broad Glob).

## Organization and evidence
- Owner commit cfaf996 restored `shaper: orchestrator`, Fable 5.2 first for shaper and Policymaker.
  Keep that routing order and `every_iterations: 1` cadence. Two consecutive successful shapers justify no repair;
  they do not establish subscription efficiency or override the owner's setting.
- With a shaper, Policymaker orders ONLY evaluator/audit (`.github/loop/task-graph.md`). No such order is needed
  in 0094. The shaper owns goal-directed tasks and journal memory; it cannot read policy/.
- #471 rewrote the orchestrator skill with graph-first by about tool call 12, four-section journal memory,
  POC priority and a startup handoff; raised max_turns 30 -> 45 after repeated turn-cap failures.
- Record 0092: closed/accepted, one task, no failure; #472 done in 19 turns; #473 accepted/merged 7b37e07,
  44 turns. Record 0093: closed/accepted, one task, no failure; #476 done in 18 turns; #477 accepted/merged
  d616e38, 27 turns. Neither record measures the tool call that first wrote tasks.json.
- #475 removed the optional handoff from mandatory startup and shortened it. Shaper startup estimate decreased
  from 12,188 (#472) to 11,781 (#476), 407 estimated tokens. These estimates exclude later reads and CLI context.
  #476 wrote a valid task and all four journal sections, incorporated #473 and selected the bounded failure exit.
  No role change is needed. Existing skill explicitly handles unsuccessful delivery and benchmark resumption.
- #479 changes only policy memory and writes empty orders. No routing, role, limit or cadence change.
  Expected gain: preserve the accepted failure delivery and avoid repeating POC research or reopening it by default.
  Check record 0094 and the next journal update for #477 continuity and a ready benchmark-preparation task.
- If the shaper fails, read its record before changing definitions. One failure: tighten graph-first if supported.
  Two repeated failures: consider an owner proposal for shaper null or a script shaper, with reasons.
  A shaper iteration fails on no valid tasks.json, not on empty Policymaker orders (engine.md:84-85).

## POC state and next work
- The bounded unsuccessful POC is delivered and accepted: #477, record 0093, commit d616e38;
  `docs/research/poc/delivery.md`, delivery.json, delivery-verification.json and verify_delivery.py.
  Eight selected originals parsed; no supported executable semantic edit, changed VI or fresh-agent demonstration.
  No session ran LabVIEW. This does not prove general impossibility, product quality or method acceptance.
- #479 ran `python3 -I docs/research/poc/verify_delivery.py`: exit 0, status pass, 13 criteria, two exits,
  nine negative checks, 38 pinned files, readiness verifier pass; session artifacts not required.
  Passing validates failure-delivery consistency only. Original bytes were not rehashed by this offline check.
- Original session artifact from #477: poc-original.vi, 6,371 bytes, SHA256
  cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8;
  declared save version 21008000 / 21.0.0 final build 0. It is unchanged, not an edited result.
  A future task needing this binary must consume #477's artifact explicitly, not assume it remains staged.
- #465 measured RSRC/save version; #468 merged 0f35a16: inspect_vi.py, complete BDHb framing,
  162 entries/842 bytes. #473 found no executable recipe after eight VIs. Preserve these sources and pins.
  Primitive identity/replacement, DTHP/VCTP and ConstValue encoding, BDPW's last 32 bytes, and compiled-cache
  invalidation remain unresolved. No disk patch, cache deletion or 103 -> 104 semantic claim is supported.
- Two saved exits: controlled same-version fixture pairs, or missing pinned source rules. They are optional future
  routes, not prerequisites to continued work. Reopen only with a bounded new question and available evidence.
- The next shaper must read delivery.md, record unsuccessful delivery in journal memory, and resume benchmark
  preparation without waiting for owner replies. Current journal is #476's pre-task plan, correctly says pending,
  and explicitly tells the next shaper to check delivery. Policymaker does not edit journal memory.
- POC remains the method-first exception, not a product. A future successful demonstration needs a fresh describing/
  editing session, unseen VI, actual changed file, native opening/behavior evidence and preserved save version.
  Silence does not accept method, quality or product. No automatic goal-completion claim.

## Benchmark resumption and gate
- POC delivery ends the POC-only pause. #479 reread `docs/perpetua/evaluation.md`; it does not select benchmark tasks.
  Shaper reads docs/perpetua/roles.md, evaluation.md and selected actual paused evidence before its next graph.
  Independent method review and owner acceptance of pinned protocol/evidence remain prerequisites to product work.
  Writing implementation additionally needs an accepted method covering write tasks; extend existing preparation.
- Existing preparation: preparation.json 99069d8d..., preparation-status.json 8f64e982...; prior evaluator check
  errors [], missing [], 74 refs, ready/executed false. Not rerun in #479. Quality is unmeasured; native,
  artifact/version, held-out and write-task coverage remains missing. Consistency checks do not establish readiness.
- Baseline/split design-reviewed; challenges scorer-reviewed; coverage/oracle/sources/tasks reviewed. Store #379
  reviewed in #431 and pinned. Unpinned review pending: allocation.synthetic.json 70d94d28... and split_allocate.py
  55c236ad... (fix #446 for #443 finding 1, fix round 1 used). Recheck actual inputs before resuming.
- Owner method request #430 declined as not_planned. Old draft policy/proposals/method-acceptance-draft.md needs
  writing coverage before reuse. No Goal gate is accepted; no goal/gate.yml or completion claim.
- All-version estimate: docs/research/0002-delivery.md, 89-264 d versus 33-99 d 2024-only; strict 2024 excludes
  413/415 RSRC files. It omits writing. Reconcile before fallback choice; do not repeat original research.
- No repeat: gap maps #282/#330/#400; reviews #403/#408/#409/#415/#421/#427/#431/#443;
  lineage batches stopped in 0066 (no allocation effect; policy/proposals/lineage-pilot-359.json); store searches.
- policy/proposals/store-readiness.yml equals installed workflow revision 4 (27b365ec...); optional deletion remains.

## Resources and open questions
- No pending suggestions or open owner requests in loop state 0094. Exports manifest has results [].
  Capability #169 readiness remains unknown; disappearance from owner_requests.open does not establish availability.
- No quota-use measurement exists. Input/cache accounting is not subscription quota use; model labels are not
  actual routing. Record 0093 sessions #476/#477 ran entirely codex/gpt-6.1-sol. No routing change follows.
- After three consecutive shaper iterations with tasks, consider an audit only with a concrete question and real
  available inputs about accepted results/resource use. Missing quota telemetry cannot be invented from tokens.
  No audit ordered now; previous #43/#55 crashed. Keep the current iteration short.
- Read docs/perpetua/accepted-limits.md before private use/disclosure/publication/spending or capability requests.
  Optional access uses capability proposals, never iteration dependencies or waiting tasks.

## Session mechanics to preserve
- Report starts with <!-- session-report --> and YAML status matching Finish.status. Write wip at the start.
  Verify session outputs just before Finish: provider switches lost them in #368/#402/#429.
  Two unfinished Policymakers trigger rollbacks; last recorded rollback remains 2026-11-11T21:41:42Z.
- git status/diff can show nothing for session writes (#471). Read back files and check bytes/hashes instead.
  Empty Write.text truncates. Verify each managed write. Layer check needs a facts JSON argument:
  `python3 policy/layer-rules.py .session/policy-facts.json`. #475 omitted it once, then passed with errors [].
  Use it for organization changes; #479 changes no organization files. Engine activation remains authoritative.
- wake true only when results change the next policy order; iteration 0055 wasted eight tasks/2.7M input.
- Task lessons live in optional shaper handoff: parent commits; offline plain python3 verification; reviewer
  starts from main/report only; bounded reads; at least 25 turns; repin changed benchmark files; resume via task/N.
- Preparation JSON uses json.dumps(indent=2, sort_keys=True) + newline; changes to preparation-status.json need
  every reference re-pinned. lineage.py --check needs LABVIEW_ENVIRONMENT. Evaluator changes require evaluator
  order plus verifier; path policy/evaluator/evaluate.py.

## Next Policymaker
1. Read record 0094 and journal/working-memory.md. Check shaper completion, #477 continuity and selected preparation work.
2. Check suggestions. Tie role changes to measured failures or unnecessary repeated reads; retain owner routing/cadence.
3. Avoid repeating POC format research, old gap maps, or claiming readiness from accepted failure delivery.
