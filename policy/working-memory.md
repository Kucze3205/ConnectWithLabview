# Policy working memory

Considered: iteration records 0000-0094, owner commit cfaf996, accepted #473's
`docs/research/poc/edit-readiness.md`, #477's `docs/research/poc/delivery.md`, and #481's
writing-method extension. Updated by Policymaker #483 for iteration 0095.
Earlier detailed memory (0024-0091, 110 KB): `git show 2b6f6870:policy/working-memory.md`
(sha256 68d353d1...). Compressed predecessor: accepted change #471, commit 5268784.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
session documents `.session/history/sessions/<issue>/` (list with python glob, not broad Glob).

## Organization and evidence
- Owner commit cfaf996 restored `shaper: orchestrator`, Fable 5.2 first for shaper and Policymaker.
  Keep that routing order and `every_iterations: 1` cadence. Three consecutive successful shapers justify no repair;
  they do not establish subscription efficiency or override the owner's setting.
- With a shaper, Policymaker orders ONLY evaluator/audit (`.github/loop/task-graph.md`). No such order is needed
  in 0095. The shaper owns goal-directed tasks and journal memory; it cannot read policy/.
- #471 rewrote the orchestrator skill with graph-first by about tool call 12, four-section journal memory,
  POC priority and a startup handoff; raised max_turns 30 -> 45 after repeated turn-cap failures.
- Records 0092/0093/0094: closed/accepted, one task each, no failure. Shapers #472/#476/#480 finished in
  19/18/25 turns; accepted workers #473/#477/#481 finished in 44/27/38 turns. These records do not measure
  the tool call that first wrote tasks.json. #480 preserved #477's unsuccessful delivery and resumed method work.
- #475 removed the optional handoff from mandatory startup and shortened it. Shaper startup estimates:
  #472 12,188, #476 11,781, #480 11,994 tokens. These exclude later reads and CLI context.
  #483 startup is ok, estimated 14,296 tokens, no notices; no startup-budget repair is indicated.
- #483 changes only policy memory and writes empty orders. Expected gain: preserve the writing-method review
  handoff without duplicate authoring, POC research or policy tasks. Check record 0095 and the next journal update
  for a separate review of #481, with actual baseline/candidate identities and explicit missing coverage.
- If the shaper fails, read its record before changing definitions. One failure: tighten graph-first if supported.
  Two repeated failures: consider an owner proposal for shaper null or a script shaper, with reasons.
  A shaper iteration fails on no valid tasks.json, not on empty Policymaker orders (engine.md:84-85).

## POC state
- The bounded unsuccessful POC is delivered and accepted: #477, record 0093, commit d616e38;
  `docs/research/poc/delivery.md`, delivery.json, delivery-verification.json and verify_delivery.py.
  Eight selected originals parsed; no supported executable semantic edit, changed VI or fresh-agent demonstration.
  No session ran LabVIEW. This does not prove general impossibility, product quality or method acceptance.
- #479 ran `python3 -I docs/research/poc/verify_delivery.py`: exit 0, status pass, 13 criteria, two exits,
  nine negative checks, 38 pinned files, readiness verifier pass; session artifacts not required.
  Passing validates failure-delivery consistency only. Original bytes were not rehashed by this offline check.
- Original #477 session artifact: poc-original.vi, 6,371 bytes, SHA256
  cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8;
  declared save version 21008000 / 21.0.0 final build 0. It is unchanged, not an edited result.
  A future task needing this binary must consume #477's artifact explicitly, not assume it remains staged.
- #465 measured RSRC/save version; #468 merged 0f35a16: inspect_vi.py, complete BDHb framing,
  162 entries/842 bytes. #473 found no executable recipe after eight VIs. Preserve these sources and pins.
  Primitive identity/replacement, DTHP/VCTP and ConstValue encoding, BDPW's last 32 bytes, and compiled-cache
  invalidation remain unresolved. No disk patch, cache deletion or 103 -> 104 semantic claim is supported.
- Two saved exits: controlled same-version fixture pairs, or missing pinned source rules. These are optional routes;
  reopen only with a bounded new question and available evidence. Do not repeat unsuccessful delivery.
- #480 recorded unsuccessful delivery in journal memory and resumed benchmark preparation without owner waiting.
  POC remains the method-first exception, not a product. Future success needs a fresh describing/editing session,
  unseen VI, actual changed file, native opening/behavior evidence and preserved save version.
  Silence does not accept method, quality or product. No automatic goal-completion claim.

## Writing method and next review
- #481 accepted/merged in 0094, commit 0da7cad11952948c8d795f38abc6a4768bf50c34,
  tree 90c377aea70fcca2dc5efe4208ff1cc897f67bf9 (resolved with git show in #483).
  Baseline 486030b461e57ca0f322a17a5b7853e83e9655e3, tree cf75cf6892de2f9410fa09ee2589dcba47d825a4.
  Report: `.session/history/sessions/481/41040c2327ddad5d40d1e546fa9c4e64efbd2b0706f58b11ead54a8c69e8d7c5.md`.
  Its metadata says routine acceptance without the owner; acceptance is not independent review or method acceptance.
- Six new files under `benchmark/writing/`: README.md, method.json, controls.json, verify_method.py,
  verification.json, input-pins.json. README and verification record read in #483; method/checker not substantively
  reviewed here. E1-E8 inherit requirements; W1-W8 extend writing. Four contracts specify VI creation,
  Boolean modification, typedef modification and source/rebuild treatment of compiled libraries.
- #483 reran `python3 -I benchmark/writing/verify_method.py`: exit 0, design-consistent, 35 asserted rejecting
  controls and five positive-control categories. Native executions 0, agent runs 0, benchmark_ready false,
  independent_review pending. This is a synthetic design check, not a review of oracle adequacy or tool quality.
  method.json SHA256 8c3b165c33c8fb4944f10a0eaa3c384fcc90d62c3278c0c910a5f2ae8b9d4da1;
  controls.json SHA256 1c929ad4efdd8c8ef4c1a5338d6a9492b69588c43add42b198aa2f722a151db3.
- Author report records 62 preserved input hashes (56 unique preparation pins), no prior tracked file changes,
  an audited isolated repeat and preparation check with 74 refs/no errors. These author checks were not repeated
  in #483, apart from the ordinary writing-method checker. Exact six output hashes are in that report.
- Journal #480 already directs the next shaper to inspect accepted output and order a separate reviewer with
  pinned inputs. This remains ready work; no policy order or role change is necessary. Review requirement
  coverage, independent expected results, controls and unavailable outcomes. Prefer a different available model
  family; actual #481 author was codex/gpt-6.1-sol. Separate sessions/evidence remain required after fallback.
- No real artifact edit, native answer key, withheld writing case, agent comparison or native run is established.
  Public fixtures remain development-only; artifact/version and hardware coverage remain incomplete.
  Product implementation waits for independent method review and owner acceptance of pinned protocol/evidence.
  Writing implementation additionally needs accepted writing-task coverage. Do not seek acceptance from this check.

## Benchmark continuation and gate
- POC delivery ended the POC-only pause. #483 reread `docs/perpetua/evaluation.md`; no product work is authorized.
  Shaper reads roles/evaluation and selected paused evidence before choosing further work; extend existing preparation.
- Existing preparation: preparation.json 99069d8d..., preparation-status.json 8f64e982...; prior evaluator check
  errors [], missing [], 74 refs, ready/executed false. Not rerun in #483. Quality remains unmeasured; native,
  artifact/version, held-out and write-task coverage remains missing. Consistency checks do not establish readiness.
- Baseline/split design-reviewed; challenges scorer-reviewed; coverage/oracle/sources/tasks reviewed. Store #379
  reviewed in #431 and pinned. Unpinned review pending: allocation.synthetic.json 70d94d28... and split_allocate.py
  55c236ad... (fix #446 for #443 finding 1, fix round 1 used). Read actual #446 inputs before resuming.
- Owner method request #430 declined as not_planned. Old draft policy/proposals/method-acceptance-draft.md needs
  writing coverage before reuse. No Goal gate is accepted; no goal/gate.yml or completion claim.
- All-version estimate: docs/research/0002-delivery.md, 89-264 d versus 33-99 d 2024-only; strict 2024 excludes
  413/415 RSRC files. It omits writing. Reconcile before fallback choice; do not repeat original research.
- No repeat: gap maps #282/#330/#400; reviews #403/#408/#409/#415/#421/#427/#431/#443;
  lineage batches stopped in 0066 (no allocation effect; policy/proposals/lineage-pilot-359.json); store searches.
- policy/proposals/store-readiness.yml equals installed workflow revision 4 (27b365ec...); optional deletion remains.

## Resources and open questions
- No pending suggestions or open owner requests in loop state 0095. Exports manifest has results [].
  Capability #169 readiness remains unknown; disappearance from owner_requests.open does not establish availability.
- No quota-use measurement exists. Input/cache accounting is not subscription quota use; model labels are not
  actual routing. Record 0094 sessions #480/#481 ran entirely codex/gpt-6.1-sol. No routing change follows.
- Three successful shaper iterations prompted audit reconsideration in #483. No concrete audit question with
  available quota evidence or repeated defect warrants an order. Continue ready independent review instead.
  Previous audit #43/#55 crashed; do not invent quota telemetry or order a broad audit to satisfy cadence.
- Read docs/perpetua/accepted-limits.md before private use/disclosure/publication/spending or capability requests.
  Optional access uses capability proposals, never iteration dependencies or waiting tasks.

## Session mechanics to preserve
- Report starts with <!-- session-report --> and YAML status matching Finish.status. Write wip at the start.
  Verify session outputs just before Finish: provider switches lost them in #368/#402/#429.
  Two unfinished Policymakers trigger rollbacks; last recorded rollback remains 2026-11-11T21:41:42Z.
- git status/diff can show nothing for session writes (#471). Read back files and check bytes/hashes instead.
  Empty Write.text truncates. Verify each managed write. Layer check needs a facts JSON argument:
  `python3 policy/layer-rules.py .session/policy-facts.json`. Use it for organization changes; #483 makes none.
  Engine activation remains authoritative.
- wake true only when results change the next policy order; iteration 0055 wasted eight tasks/2.7M input.
- Optional shaper handoff holds task lessons: parent commits; plain python3 verification; reviewer starts from
  main/report only; bounded reads; at least 25 turns; repin changed benchmark files; resume via task/N.
- Preparation JSON uses json.dumps(indent=2, sort_keys=True) + newline; preparation-status.json changes need
  every reference re-pinned. lineage.py --check needs LABVIEW_ENVIRONMENT. Evaluator changes require evaluator
  order plus verifier; path policy/evaluator/evaluate.py.

## Next Policymaker
1. Read record 0095 and journal/working-memory.md. Check #481's independent review and exact pinned inputs.
2. Check suggestions. Tie role changes to measured failures or unnecessary repeated reads; retain owner routing/cadence.
3. Avoid repeating method authoring, POC format research or old gap maps. Keep synthetic consistency separate from readiness.
