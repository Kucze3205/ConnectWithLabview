# Policy working memory

Considered: iteration records 0000-0098, owner commit cfaf996, accepted #473's
`docs/research/poc/edit-readiness.md`, #477's `docs/research/poc/delivery.md`, #481's
writing-method extension, review #485, correction #489, re-review #493 and allocator re-review #497.
Updated by Policymaker #499 for iteration 0099. #499 read record 0098, journal memory,
task-graph contract, evaluation requirements and the actual #497 report. Startup is ok,
estimated 17,169 tokens, no notices; exports results [], suggestions [], open owner requests [].
#499 resolved #497's reviewed tree and matched both current allocator files against
reviewed commit 8aefb1583265f097a8569d76b4f8e5a0b0782833 and the report hashes.
Neither file is directly referenced by benchmark/preparation.json. No evaluator defect is established.
#499 did not rerun the allocator, evaluator or review probes. Detailed #497 artifacts were not staged
or replayed here; findings and probe results below are attributed review results.
Earlier detailed memory (0024-0091, 110 KB): `git show 2b6f6870:policy/working-memory.md`
(sha256 68d353d1...). Compressed predecessor: accepted change #471, commit 5268784.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
session documents `.session/history/sessions/<issue>/` (list with python glob, not broad Glob).

## Organization and evidence
- Owner commit cfaf996 restored `shaper: orchestrator`, Fable 5.2 first for shaper and Policymaker.
  Keep that routing order and `every_iterations: 1` cadence. Three consecutive successful shapers justify no repair;
  they do not establish subscription efficiency or override the owner's setting.
- With a shaper, Policymaker orders ONLY evaluator/audit (`.github/loop/task-graph.md`). No such order is needed
  in 0096. The shaper owns goal-directed tasks and journal memory; it cannot read policy/.
- #471 rewrote the orchestrator skill with graph-first by about tool call 12, four-section journal memory,
  POC priority and a startup handoff; raised max_turns 30 -> 45 after repeated turn-cap failures.
- Records 0092/0093/0094: closed/accepted, one task each, no failure. Shapers #472/#476/#480 finished in
  19/18/25 turns; accepted workers #473/#477/#481 finished in 44/27/38 turns. These records do not measure
  the tool call that first wrote tasks.json. #480 preserved #477's unsuccessful delivery and resumed method work.
- #475 removed the optional handoff from mandatory startup and shortened it. Shaper startup estimates:
  #472 12,188, #476 11,781, #480 11,994 tokens. These exclude later reads and CLI context.
  #483 startup was ok, estimated 14,296 tokens. #487 startup is ok, estimated 14,799 tokens, no notices;
  no startup-budget repair is indicated.
- Record 0095 closed without failure: shaper #484 done/merged in 25 turns; reviewer #485 done in 22 turns,
  no repository changes to merge. Engine improved false/no_progress 1 does not make this review a failed session.
  #485 found three medium defects and recommended REVISE. Separate sessions establish review independence;
  author and reviewer both actually used codex/gpt-6.1-sol, so model-family diversity was not achieved.
- Record 0096 closed/accepted, improved true, no failure: shaper #488 done/merged in 22 turns;
  correction worker #489 done/accepted/merged in 26 turns. Both actually used codex/gpt-6.1-sol.
  Journal #488 directs the next shaper to read the correction report and separately review changed bytes.
- #491 changes only policy memory and writes empty orders. Expected gain: preserve #489's published candidate
  and evidence without duplicate correction, POC research or policy tasks. Check record 0097 for independent
  re-review of that candidate or an evidenced blocker. No role, routing, ceiling or cadence change.
  #491 startup is ok, estimated 15,598 tokens, no notices; no startup-budget repair is indicated.
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
- Independent review #485, record 0095, recommendation REVISE:
  `.session/history/sessions/485/3afd2492606ed7bf67a763c7805211fe2b95eb4ef2fdd213b5b4f3fc5b29ee7c.md`
  (source https://github.com/Kucze3205/ConnectWithLabview/issues/485#issuecomment-6839451431).
  Reviewed baseline above; candidate commit 7435c05c4fd7ddbaafb6f5db9081ad5a4f5db427,
  tree 555960a979f4bec474850a39bd9b284b7188496a. Reviewer reports all six output hashes and 62 baseline
  input hashes matched; reviewed bytes are pinned despite contradictory identity metadata.
- S1 (medium): input-pins.json:3-4 names another, locally unresolvable baseline commit/tree. Correct identity
  fields to verified baseline above, preserve input entries and refresh dependent hashes.
- S2 (medium): verify_method.py:144-153 accepts original SYNTHETIC-v0 and modified output SYNTHETIC-v1.
  Require original-to-output save-version equality under W4 and add a rejecting control.
- S3 (medium): verify_method.py:178-186 accepts removal of key_revision from frozen settings and both arms.
  Require mandatory setting names before comparing values under E6/protocol:80,83-84; add a rejecting control.
- #485 reports ordinary/isolated checks passed with 35 authored rejections, while both independent probes also
  passed incorrectly. This is bounded checker evidence, not a native result. Requirement trace otherwise supports
  four contracts and E1-E8/W1-W8; do not treat that assessment as acceptance of unresolved findings.
- #485 saved counterexamples.py (4,409 bytes, sha256 a2bdbdba9d740586eca128a9c44677e82a7df33b735a9223765205dcbcb7842c)
  and review-evidence.md (19,951 bytes, sha256 7967a9982e7927097ee14a6c0eeb351e0e7e54c4c9f45845bbece8ced764caf4),
  release names iter-0095/485-counterexamples.py and iter-0095/485-review-evidence.md. They are session artifacts,
  not assumed present in a fresh checkout. Read the report first; verify availability before requiring replay.
- Correction #489 is accepted/merged in record 0096. Report:
  `.session/history/sessions/489/39b276d010c055840bef365a3c538138c366e0f21ca9b79ada023b78db3676cf.md`
  (source https://github.com/Kucze3205/ConnectWithLabview/issues/489#issuecomment-6839895609).
  Acceptance metadata says routine change outside owner paths, accepted without the owner; this is not method approval.
- Published correction candidate: commit `2033c33fac195161fc3ac15b78f906a7d3140785`,
  tree `50a0180535642f6fda877a5acea9e4c3801acd51`, resolved by #491 with git.
  Report checkpoint `f86939aed871aee754a096d9b378870ebb39d095` is unresolvable locally; its reported tree
  equals the published tree. Use the published commit, not that checkpoint or the old #485 candidate.
  Current checkout in #491: d147f40b540548f4b8bb39f5db2e75f4d7056f62, tree 4f14b43633ffbd8fb71fa263c2be703f28818e27.
- #491 matched all seven current writing files against the report hashes and published commit bytes.
  Six changed paths: README.md, controls.json, input-pins.json, verification.json, verify_method.py and new
  review-corrections.json; method.json remains unchanged. Published commit changes only these six paths.
  The report above lists all seven exact hashes; review-corrections.json SHA256
  3c92d3e102bb3976ee267ea74393855e520461e2e5f4869fa9d5a864ff17430e;
  checker b24ca4515ab8f7bd3980cd273647114c4f01abffc942a2464390a4d206e40a5f;
  verification 01e4ad1d72cb8f782e0dcfe3ce5e9b27756520da8a403df41707a1d37f1e1022.
- #489 reports S1 identity corrected to the verified historical baseline; all 62 protected hashes and 56 unique
  preparation pins/74 references preserved. S2 original/output version drift now rejects in modification and
  source-rebuild paths. S3 independently requires request, originals, allowed_inputs, model, budgets,
  key_revision and repetitions; deleting each from frozen and both arms now rejects.
- #489 reports both original false acceptances reproduced before correction, 35 old controls retained unchanged,
  nine added controls, 44 total rejections and five positive checks. verification.json records ordinary/isolated
  checks passing, empty-environment repeat from / with mutation/session reads denied, and preparation check
  errors [], missing [], 74 refs, benchmark_ready false. These are author results, not independent approval;
  #491 read the record and hashes without repeating the checks or substantively reviewing the checker.
- Independent re-review #493, record 0097, recommendation CLEAR for S1-S3 on the pinned synthetic design:
  `.session/history/sessions/493/0f76ee10ed9904be9422c2e59c3929f07d37d7a91747dff22d80aba38f140817.md`
  (source https://github.com/Kucze3205/ConnectWithLabview/issues/493#issuecomment-6840362734).
  Reviewed commit d3c697c375ed7dc880e55ab3cc2219577cd133a5 / tree 689ed2757ca4eb413cd37dc4f0cfcbc2fa90ba14.
  Reviewer matched all seven hashes to #489; #495 independently matched current bytes to that commit and
  published correction 2033c33. Current HEAD 70ecece52434b6102f386c495ab170d3e58b41c1 differs only in
  two session-report records, iterations/0097.json, iterations/0097/tasks.json and journal/working-memory.md.
- #493 closes S1: historical baseline identity, 62 protected hashes and 56 unique preparation pins/74 refs
  independently matched; only input-pins identity fields changed. method.json and protected inputs are preserved.
  S2 closes: original/frozen linkage rejects both old version-drift probes plus adjacent invalid versions.
  S3 closes: seven mandatory settings independently derived; missing-setting, mismatch and arm violations reject.
  No new scoped finding or regression. This does not approve unreviewed changes or native quality.
- #493 reports all 35 original raw control objects retained, nine additions rejecting, five positives passing;
  independent replay has 75 probes (71 rejects/four adjacent positives). Original git bytes reproduce old false
  acceptances. Isolated empty-environment run from / has identical stdout with session access, mutation, network
  and subprocesses denied. These are attributed reviewer results, not #495 reruns.
- Saved optional review artifacts: iter-0097/493-review-evidence.md SHA256
  bf601878bedc38e7d42a9dd2295f21a774f0d15160a648a4793e45a1c4a32822;
  iter-0097/493-replay.json ec27493b85d306c8859531fa9e4aca00b87ed301c4070d89425fb6520d851aca;
  iter-0097/493-snapshot.json 290b4446c544f0368a46dca58391c1e4ab0faf3969bd2ee2feac400fc898741f.
  Read the report before requiring replay; these session artifacts are not assumed staged.
- Record 0097 closed without failure: shaper #492 done/merged in 21 turns, reviewer #493 done in 20 turns,
  no repository changes to merge. improved false/no_progress 1 does not make the review a failed session.
  Both actually used codex/gpt-6.1-sol; separate-session review independence holds, model-family diversity does not.
- #495 preserves this bounded closure, changes policy memory only and writes empty policy orders. Expected gain:
  avoid another S1-S3 correction/review and let the shaper select the next evidenced prerequisite in 0098.
  No evaluator defect or concrete audit question warrants a policy task; no routing, role, ceiling or cadence change.
  Journal #492 already directs the next shaper to read #493 and select the next gap, including deferred #446 review.
  Do not repeat correction, full method authoring or POC investigation; re-pin and review changed writing bytes.
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
  reviewed in #431 and pinned. #497 now independently closes #443 finding 1 on #446's allocator correction;
  see the pinned identities and limits below. The two allocator files have no direct preparation.json entries.
  This closure does not authorize arbitrary index changes or establish benchmark readiness.
- Owner method request #430 declined as not_planned. Old draft policy/proposals/method-acceptance-draft.md needs
  writing coverage before reuse. No Goal gate is accepted; no goal/gate.yml or completion claim.
- All-version estimate: docs/research/0002-delivery.md, 89-264 d versus 33-99 d 2024-only; strict 2024 excludes
  413/415 RSRC files. It omits writing. Reconcile before fallback choice; do not repeat original research.
- No repeat: gap maps #282/#330/#400; reviews #403/#408/#409/#415/#421/#427/#431/#443;
  lineage batches stopped in 0066 (no allocation effect; policy/proposals/lineage-pilot-359.json); store searches.
- policy/proposals/store-readiness.yml equals installed workflow revision 4 (27b365ec...); optional deletion remains.

## Resources and open questions
- No pending suggestions or open owner requests in loop state 0097. #491 exports manifest has results [].
  Capability #169 readiness remains unknown; disappearance from owner_requests.open does not establish availability.
- No quota-use measurement exists. Input/cache accounting is not subscription quota use; model labels are not
  actual routing. Record 0096 sessions #488/#489 ran entirely codex/gpt-6.1-sol, as did #484/#485 in 0095.
  No routing change follows. A same-family fallback review is not evidence that other families were available.
- Three successful shaper iterations prompted audit reconsideration in #483. No concrete audit question with
  available quota evidence or repeated defect warrants an order. Continue ready independent review instead.
  Previous audit #43/#55 crashed; do not invent quota telemetry or order a broad audit to satisfy cadence.
- Read docs/perpetua/accepted-limits.md before private use/disclosure/publication/spending or capability requests.
  Optional access uses capability proposals, never iteration dependencies or waiting tasks.

## Session mechanics to preserve
- Report starts with <!-- session-report -->, then a fenced ```yaml block with status matching Finish.status,
  then the closing fence and prose. YAML front matter is rejected (#487 corrected this before finishing).
  Write wip at the start.
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

## Allocator completion review and iteration 0099
- Record 0098 closed without failure: shaper #496 done/merged in 26 turns; reviewer #497 done in 18 turns,
  no repository changes to merge. improved false/no_progress 2 does not make these review sessions failures.
  Both actually used codex/gpt-6.1-sol. Separate-session independence holds; model-family diversity was not achieved.
- Actual #497 report, finding 1 CLOSED, recommendation CLEAR for the pinned completion guard:
  `.session/history/sessions/497/6098526236d9d3938719e3131cfafcbb53c2aad7ea37aa341f32a663d77523eb.md`
  (source https://github.com/Kucze3205/ConnectWithLabview/issues/497#issuecomment-6842189433).
  Reviewed commit 8aefb1583265f097a8569d76b4f8e5a0b0782833 / tree
  94c6df4711068611c1c2eb3f7f5b54d150c1ea78. Reviewer starting/finishing HEAD
  b92ecde9c465728be7961e5952a249dbaf110478 / tree bef5c8613e3d73ca083671c172bfbe6723c6026b;
  reviewer reports administrative differences only.
- Correction commit 298727a0bf9ec03ab5a4788e8fd7249604f010cc, parent
  cad1f04f3cfec68971337d3e3cfa7d337cbb901a, identified by #497 through git. Patch changes completion
  count and caller guard only. Original script SHA256 79ffbdffe60bc589be172de08a380a958ae4e220ee4d53303390f49230ae16fc;
  reviewer independently reproduces historical early-return false acceptance (exit 0).
- #499 matched current script SHA256 55c236ada2bce447990c7185ac8654a2c8aefba32ae4010fac65ae82a15c8ecd
  and allocation.synthetic.json SHA256 70d94d28084b45938c698e6097c8afd40934f8e9ab0d70a29de36d242ab4de34
  against the report and reviewed commit bytes; resolved tree matches. Current HEAD is
  b552e135b9bde462a2fa30dcd7dfe1cafdf54b9e. No direct preparation.json references to these two paths exist;
  no stale evaluator/index defect is established. Do not order evaluator work from journal speculation alone.
- #497 reports ordinary --check exit 0 and independent tracing of reason mismatch plus all seven exact-reason
  mutation rejections. Six isolated faults exit 1: early returns before reason/before mutations, disabled reason
  comparison, duplicate-skipping, missing infeasible_strata and adjacent partial completion of seven.
  Second normal run from another directory with empty environment/three public files has identical stdout;
  audit observes no network/session/restricted access. All 1,044 tracked starting hashes remain unchanged.
  These are attributed review results, not #499 reruns; no scoped Standards/Spec defect or regression remains.
- Historical task bodies are title stubs; original probe-source artifact unavailable. Exported #443/#446 reports
  and matching git blobs support independently reconstructed probes. Do not present a missing source as replayed.
  Optional artifacts: iter-0098/497-completion-review.md SHA256
  02b1a9f7cd830186253e888999300cd2ba9845c23eb21e171a96c1e7583aeb3f;
  completion-review.json ebfc5fc79bca20227fd3c0e4118c6bbb3a75a26ad0ec745127cb435722a8c19b;
  review_completion.py a19e7cd36aa3203b9ae239e3467a23cdb68aeda79677e582877c79e64d16d67b.
  Read the report before requiring artifacts; they are not assumed staged in a cold session.
- #499 changes policy memory only and writes empty policy orders. Expected gain: preserve #497's bounded
  closure and avoid duplicate allocator review while the shaper chooses the next concrete prerequisite in 0099.
  Check the next record/report for that progression or a specific blocker. No demonstrated evaluator defect,
  concrete audit question or startup notice warrants an order. No role, routing, limit or cadence change.
  Journal #496 already directs the next shaper to read #497, settle the guard, and inspect paused evidence
  before selecting native/readiness work. Optional access requests cannot hold the iteration open.
- Native benchmark executions and agent comparisons remain absent. Native keys, withheld writing cases,
  verified evaluation isolation and artifact/version/hardware coverage remain incomplete; tool quality is unmeasured.
  Synthetic guard approval does not accept the method, authorize product work or satisfy a Goal gate.

## Next Policymaker
1. Read record 0099, journal/working-memory.md and actual task reports. Check that #497's bounded closure led
   to a concrete next prerequisite instead of repeated allocator or unchanged writing review.
2. Inspect actual pin evidence before any evaluator order. The two reviewed allocator paths have no direct
   preparation.json references; #499 established no evaluator defect. Do not create a new global gap map.
3. Check suggestions and failures. Retain owner routing/cadence without measured contrary evidence; tokens/cache
   counts do not measure subscription quota. Review family diversity was not achieved in 0098.
4. Preserve #493's writing identity/report and #497's allocator identity/report above. Changed bytes need new evidence.
   Avoid repeating S1-S3 corrections, allocator review, full method authoring, POC research or old gap maps.
   Native coverage and product quality remain unmeasured. No owner method acceptance or Goal gate exists.
