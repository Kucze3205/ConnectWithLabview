# Policy working memory

Updated by Policymaker #559 for iteration 0114. Considers records 0000–0113, selected new records
0111–0113, reports #551/#554/#557, current journal memory and loop-state decisions. This session
read integration provenance and evaluation rules; measured preserved #547 review bytes and resolved
baseline/admitted-candidate Git identities. It did not read #557 artifacts or replay checks/probes.
Startup: ok, 15,954 estimated tokens, no notices. No suggestions; exports manifest has no results.
Predecessor: prepared checkout 712c2501da9b8f0153a5ecf1cb8a2348832586b6, policy/working-memory.md,
SHA256 36eca808ea0491c5fb24070bb1147d2ead4360900c7fa22da3431faaca32f9cd.
#520 compressed older memory: git show 29ae339:policy/working-memory.md
(SHA256 f332799010f475ce09d126438d354c64815653fba89e2bf8fd76662d368b038e).
Older 0024–0091 detail: git show 2b6f6870:policy/working-memory.md. Revisit only missing pins/reasons.
History: .session/history/manifest.json; records .session/history/records/<nnnn>.json;
reports .session/history/sessions/<issue>/. Select actual report snapshots; exclude task.md unless needed.
Extract selected record fields with Python; omit repeated input_state/task bodies and duplicated shaper.
Keep memory below about 16 KB. Exact recent report links are in policy/observations/0114-integration-review.md.

## Organization and current decision
- #559 keeps roles, routing, evaluator, skills and approved #525 cadence unchanged: every_iterations=3,
  no_progress=3. Empty policy orders. Goal preparation progresses; no concrete new audit/evaluator question.
- 0111 #551 preservation and 0112 #554 integration were accepted. 0113 #557 completed scoped independent
  review with no repository changes, as intended. Its iteration verdict none is not a failed review or a stall.
- Policymaker orders only evaluator/audit when a shaper exists (.github/loop/task-graph.md). The shaper owns
  goal tasks and journal memory; it cannot read policy/. Use its report/handoff or execution/protocol.md as needed.
- Reviewer write: [] is deliberate; findings use .session/report.md and .session/artifacts/. A permitted writer
  preserves useful evidence. Prefer another model family when available; do not broaden reviewer writes.
- #526 failed after three rebase conflicts; #527 recovered. No model fault established. Inspect exact errors
  before reorganizing on a new failure. Audits #43/#55 crashed; order audits only for concrete available evidence.

## Latest results: 0111–0113
- #551 preservation accepted/merged a4bb56a. Current benchmark/project-text-writing-0109/review-0110.json
  directly measured by #559: 74,366 bytes, SHA256
  2dc007939a4b0637716027ef6e5a874702c9be7288daf80c3f007c07f382cdaf. Exact #547 review is preserved;
  review-0110-provenance.md records scoped identities and limitations. Do not repeat preservation or review.
- #554 integration accepted/merged 0e371f84162004146990cb1262b044dd4bf0dd79, tree
  557a725623d04d1df5415751c4079bca056034f3. Baseline 575d59ef8fcaf1f81a81d2eb605f52eb94053839,
  tree bd09e3a07e772337a3f045f69611b9f51dd3e227. #559 directly resolved these Git identities.
  The author-reported checkpoint object did not resolve here; admitted candidate is available and reviewed.
  Do not mistake missing transient objects for scoped candidate drift or repeat failed object lookups.
- Seven integration paths: benchmark/writing/{method.json,README.md,controls.json,verify_method.py,
  verification.json,integration-0112-provenance.json,integration-0112-provenance.md}. Five changed, two added.
  Current command: python3 -I benchmark/writing/verify_method.py. No session/cache/environment dependency.
  #559 read provenance, not verifier/results bodies, and did not execute this command.
- #557 report gives separate Standards CLEAR and Spec CLEAR for integration preparation only. Candidate/tree
  above matches the reviewed identity. It reports preserved synthetic tasks/control reasons and historical pins,
  exact WP1 locator/delta, reproduced verifier stdout and focused probe success. Counts remain report claims
  here; read the actual artifact before asserting detailed results. No historical probes were replayed.
- Exact #557 review to stage: wp1-integration-review.json, release iter-0113/557-wp1-integration-review.json,
  20,056 bytes, SHA256 1d5af5e7fb6b7ecdf58877a4e30e616a8d4a588d4cf51d4fd68265ddb96bfa3c.
  Probe JSON: 67,202 bytes, SHA256 084653d5eb0dbf5f2effed50f1e10132b94e5d3ac82e790b268d57172bcd796d;
  script: 20,784 bytes, SHA256 3890ced11b9144dece07fafbed590188bb78dd759a005c60b910883127fe76eb.
  Those sizes/hashes come from #557 report; #559 did not obtain or hash those artifacts. Exports are empty,
  not evidence that artifacts were lost. Downstream writer must stage exact evidence and check actual bytes.
- C1 Low/nonblocking remains: structured checks/hashes do not establish arbitrary narrative or future answers.
  Semantic, extra-claim, contradiction and original/output citation adjudication remains independent work.
- Shaper next: consume #557, preserve exact artifact through a permitted writer if durable evidence is needed,
  then select the next substantive preparation gap. Do not repeat review merely to repair output paths.
  Freeze complete independent text/preservation/answer keys, full manifests and revisions before either arm.
  No native keys, withheld allocation, executed isolation, native validity/build/behavior/save-version result,
  benchmark readiness or product quality follows. Same-family sessions do not establish model diversity.

## Project-text lineage: 0107–0110
- #537 real-project-0107 measured four declarations and a missing direct-LVPROJ-writing case. #541 CLEAR
  covers those declarations only. Actor Framework revision 371c631c16155d88f02be11a953e4964d7452fd8,
  MIT, Core/AF PPL Build.lvproj, 5,806 bytes, SHA256
  1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf; minimum (size,path) selection.
  D1 root LVVersion, D2 dependency URL, D3 Packed Library type, D4 Bld_version.build text/Type Int.
  These are declarations, not native version/resolution/build authority. Do not inspect another project
  without a new question. WC1/WM1/WM2/WB1 did not supply a direct text-writing case.
- #541 C1 acknowledged narrative overclaims accepted by the structured checker; reviewed prose had none.
  #544 preserved review-0108.json at benchmark/real-project-0107/, SHA256
  6ad9596c1c5e05f08ee3647ae3af1596f1882944e2397ac9efcd79383aa78894. No standalone cosmetic fix.
- #544 proposal accepted/merged 34cd2b3: benchmark/project-text-writing-0109.{md,json}, checker/results.
  WP1 fixes unique Bld_version.build text 2 -> 3, byte 3347/line 42 only, preserving other bytes/files and root
  declaration. No project edit/native trial follows. Baseline 8b93818c2779be00a2e267a3588eadcdaf665911,
  tree e5cdbf5a3bf02dce5de55e0b0cd3fc27bb744c31; accepted e5165269b5625455ad17bf34a3a8d1be95ee362f,
  tree 385ea919fc4f7714aa7bbdd29fd48ef60eaa74bb.
- #547 CLEAR covers proposal integration preparation only; reviewed 668b9bedb30188100ab1c54e81436d674feea1a8,
  tree e9a20bf69df2e366a47a612da6a6d8c80c8eb2c0. Its exact review is now preserved by #551.
- #554 integration intentionally invalidates frozen #544 checker's old writing-input hashes. Preserve historical
  checker/evidence at historical pins; never refresh them to fit current inputs. Use new integration provenance
  and verifier. #557 separately reviewed the changed integration tree; do not reopen unchanged review.

## POC blocker and ready work
- Bounded unsuccessful POC #477 accepted in 0093, commit d616e38: docs/research/poc/delivery.md,
  verify_delivery.py. #479 pass establishes failure-delivery consistency only. No changed VI, fresh-agent
  description/edit demonstration, native validity/behavior or save-version preservation exists. No impossibility
  conclusion follows. Benchmark preparation resumed with #536/#537 after unsuccessful delivery/source blocker.
- Original add.vi: 6,371 bytes, SHA256 cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8,
  declared 21.0.0. Controlled owner #516 fixtures are different: owner-reported 2026 26.1.1f1 32-bit, not WM1
  or verified 2024 cases. #528 completed all eight comparisons, bba00f7, findings-0105.md:
  edit-attempt-needs-more. Do not repeat comparisons, delivery or fixture requests.
- #533 merged fc70efc; docs/research/poc/pair/constant-rules-0106.md: source-blocked. [312,316) parses
  as textHair flags 4420|0200; 545/549 lie in ConstValue bodies 00000001->00000002 under DCO UID 118.
  Meaning/necessity, typed dispatch, BDPW chunks 1/2 and RTSG/LVSR/code/type rules remain unresolved.
  Equal BDHb/different BDPW tails refutes BDHb-only dependence. Boundaries justify no safe edit rule.
  Prepared sources lack LVblock/LVdatatype/LVrsrc rules. Do not repeat unchanged absence searches.
  LVSR 26008000 and vers/4 26118001 are declarations, not native save-version authority.
- #532 optional unchanged Save As control remains pending. Do not duplicate, schedule unavailable work or wait.
  New control needs authoring/original/control pins; it alone supplies no integrity/type rule. Reopen bounded
  POC work only for newly pinned primary source/control evidence addressing concrete blockers.
- Pair preparation #509: commit 53816a08feeb89a2747bf63ce8338ea315e06518, docs/research/poc/pair/.
  Exact original instructions/tool/protocol/selfcheck hashes remain in predecessor memory; review is closed.
- #513 independent session (same model family), reviewed 8f5ae4c48581459aa09b3f5e56f79db56188b86c:
  no major; nine probes, not report summary's eight. #522 preserved review-0102.json, 5,320 bytes, SHA256
  562467370d558b15eb9a7faf8cb1bc283365f99ef3c8cada9c6f54f1ead8249f and provenance, commit 5c6dc23.
  R1 low: --self-check rewrites tracked selfcheck.json. Avoid it; fix only with necessary tool change/re-review.
- #518 failed only on false shaper probe count. #520 added assert-only-source-values and saved-work resumption
  rules to orchestrator. #521/#522 used them; #522 completed in seven turns. Never replay probes to fix paths.

## Quota evidence and decision rule
- Owner criterion: accepted-result quality per subscription quota. Provider state is not billing or a quota-normalized
  comparison. Outside use is unknown. Read docs/perpetua/operating-parameters.md before tuning/stall responses.
- Cadence observation completed by #549: 0101–0106 recorded 33 hits/four parked outcome sessions;
  0107–0109 and 0108–0110 each recorded zero hits/parking (overlap). Each later window used Codex for all six
  outcome sessions. Model/tasks/availability confound cadence; no quota-saving claim follows.
  Details: policy/observations/0111-review-and-cadence.md. Do not repeat that comparison.
- New 0111–0113 records: zero hits, zero parked time, all six outcome sessions Codex. No current-availability,
  quota-saving or comparative-quality claim follows. Records omit Policymaker usage and routed-attempt history.
- #524 filed #525; approved/completed by #535 loop-state. Only every_iterations became 3; no_progress stayed 3,
  model order unchanged. Do not resubmit. Routing/catalog changes need fresh concrete evidence.
- Earlier quota evidence and exact #530 runtime pins remain in predecessor memory. They are dated observations,
  not current availability; retry_after is not proven recovery. #526/#527 rebases do not prove model fault.
- New availability question: git log origin/loop-runtime, then selected pool.json or sessions/<N>.json via git show.
  Print only availability/usage/relevant errors, never repeated histories. No new runtime probe justified here.
- Cost guide: earlier Policymakers used 17–40 turns; aim below 20 actions. Select evidence, update memory,
  orders/report, then Finish. Avoid repeated evidence reads and speculative machinery.

## Other closed evidence and remaining limits
- Synthetic writing #481/#485/#489/#493: corrected 2033c33fac195161fc3ac15b78f906a7d3140785; CLEAR at
  d3c697c375ed7dc880e55ab3cc2219577cd133a5, tree 689ed2757ca4eb413cd37dc4f0cfcbc2fa90ba14;
  original method.json SHA256 8c3b165c33c8fb4944f10a0eaa3c384fcc90d62c3278c0c910a5f2ae8b9d4da1.
  Historical 44 rejecting/five positive controls were design-only. #554 changed five files; #557 reviewed those.
- Allocator #497 CLEAR at 8aefb1583265f097a8569d76b4f8e5a0b0782833 closes #443 finding 1. Do not repeat.
- #501 effort study e67bb1a2b6da4f0c70b0e9b7655256018c90da11, docs/research/0099-writing-version-effort.*:
  33–99 days (2024) versus 89–264 (all versions) is reading only. No full-goal ratio/fallback follows. Study
  assumes 8.0–2025; controlled fixtures are 2026. Independently review before any fallback proposal.
- WM1 #505 d9b03d16e86c6694991bc37076ea22a554951dab, docs/research/0100-wm1-version-evidence.*:
  five vers/one LVSR declarations 20008000, authoritative save version null. Different file from owner fixtures.
- Preparation-index reference counts change; read actual source before asserting current count. Index remains
  navigation, not evidence of benchmark readiness. #430 declined; policy/proposals/method-acceptance-draft.md
  needs writing coverage before reuse. Full independent method review/owner acceptance remains pending.
- No native benchmark run, agent comparison, native answer key, withheld writing case or verified isolation.
  Artifact/version/hardware coverage incomplete; tool quality unmeasured. Capability #169 readiness unknown.
- No Goal gate accepted; no goal/gate.yml; no completion claim. Product needs independently reviewed method
  and owner acceptance of pinned protocol/evidence. Writing also needs accepted writing coverage. Routine
  merges, green checks and silence do not establish acceptance or readiness. State gaps in every evaluation report.
- Read docs/perpetua/accepted-limits.md before private use/disclosure/publication/spending/capability requests.
  Optional access never blocks an iteration; resource-dependent tasks wait for verified readiness.
- Do not repeat without a new question: gap maps #282/#330/#400, reviews #403/#408/#409/#415/#421/#427/#431,
  lineage batches (stopped 0066), store searches/reviews, S1–S3 correction, allocator review, effort estimate,
  WM1 audit, POC failure delivery, completed pair comparisons or preserved historical reviews.

## Session mechanics
- Report starts <!-- session-report -->, fenced yaml status equals Finish.status. Write wip early; Finish status
  is one word. Read required outputs immediately before Finish. Owner-facing report uses short STE sentences.
- Session writes can be absent from git status/diff. Verify content and compare actual start commit if needed.
  Continuations may show historical successful Writes while current outputs are absent. Recreate only missing
  session outputs from saved work; empty Write.text truncates.
- Layer check for organization changes: python3 policy/layer-rules.py .session/policy-facts.json (facts needed).
  Not needed for memory/observation prose. Engine activation is authoritative.
- Empty orders: {"tasks": []}. wake true only if results change next order. Evaluator changes need evaluator
  order plus separate verifier; path policy/evaluator/evaluate.py. No policy-only goal tasks with a shaper.
- Requests: .github/loop/session-protocol.md, Requests to the owner. JSON list with kind/title/what/why/unblocks.
  Question means yes/no without engine effect. Read limits before relevant requests. No new request here.
- Two unfinished Policymakers trigger rollback (last 2026-11-11T21:41:42Z); keep sessions bounded.

## Next Policymaker
1. Keep cadence and routing unless new concrete evidence justifies change. Completed cadence comparison stays closed.
2. Check #557 consumption/preservation and the next substantive preparation step, using selected new records/reports.
   Verify actual staged artifact bytes before detailed claims. Do not repeat review/probes to fix output paths.
3. Retain historical pins/checkers. Complete independent keys and actual isolation/native evidence remain separate
   from scoped integration review and owner method acceptance. No product start/readiness claim follows.
4. Check new source/control readiness before POC follow-up. #532 pending; do not duplicate or wait.
5. Keep orders to evaluator/audit. No duplicate audit, gap map, source-absence search or replay without a new question.
