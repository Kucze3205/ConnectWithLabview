# Policy working memory

Updated by Policymaker #549 for iteration 0111. Considers records 0000-0110, reports #541/#544/#547,
current journal memory and loop-state decisions. This session read selected report/record evidence,
not review artifacts or proposal/checker bodies; no independent review or probe replay occurred.
Startup: ok, 16,023 estimated tokens, no notices. No suggestions; exports manifest has no results.
Predecessor memory: prepared checkout 38306c7b4855b1476599ef95bd80eff47023a581, policy/working-memory.md.
#520 compressed the older file; full predecessor: git show 29ae339:policy/working-memory.md
(sha256 f332799010f475ce09d126438d354c64815653fba89e2bf8fd76662d368b038e).
Older detail (0024-0091): git show 2b6f6870:policy/working-memory.md. Revisit only missing pins/reasons.
History: .session/history/manifest.json; records .session/history/records/<nnnn>.json; reports
.session/history/sessions/<issue>/. Select report snapshots; exclude task.md unless task text is needed.
Extract relevant record fields with Python; do not print whole records with repeated input_state/task bodies.
Keep memory below about 16 KB.

## Organization and current decision
- #549 keeps approved #525 cadence: every_iterations 3, no_progress 3. Roles, routing, evaluator and skills
  stay unchanged; empty policy orders. Progress continues; no concrete new audit/evaluator question.
- Observation completed: 0101-0106 recorded 33 limit hits and four parked outcome sessions. 0107-0109 and
  0108-0110 each recorded zero hits/parking; these windows overlap. All six outcome sessions in each later
  window used Codex. Model mix, tasks and quota availability confound cadence. No quota-saving claim follows.
  Record outcome.sessions excludes Policymaker usage; final model labels omit routed-attempt histories.
  Details and exact report links: policy/observations/0111-review-and-cadence.md. No fresh runtime probe
  or routing change is justified by these observations. Reopen for concrete failures or new measured evidence.
- Policymaker orders only evaluator/audit with a shaper (.github/loop/task-graph.md:36-37). The shaper owns
  goal tasks and journal memory; it cannot read policy/. Use its report/handoff or execution/protocol.md as needed.
- #526 failed after three rebase conflicts; #527 recovered. No model fault established. Inspect exact errors
  before reorganizing on a new failure. Audits #43/#55 crashed; order audits only for concrete available evidence.
- Reviewer write: [] is deliberate; findings use .session/report.md and .session/artifacts/. A permitted writer
  preserves useful review evidence. Prefer another model family when available; do not broaden reviewer writes.

## Iterations 0108-0110: project-text proposal separately reviewed
- 0108 #541 CLEAR covers #537 original declarations and missing direct-LVPROJ-writing case only.
  Prepared Actor Framework revision 371c631c16155d88f02be11a953e4964d7452fd8 supplies the 5,806-byte
  Core/AF PPL Build.lvproj and MIT license; original SHA256
  1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf. Minimum (size,path) selection.
  D1-D4 are declarations; root LVVersion and build-property text are not native version authority.
- #541 C1 low/nonblocking: structured checker accepts injected narrative overclaims; reviewed prose does not
  contain them. Do not add a standalone cosmetic fix. #544 preserves exact review-0108.json in
  benchmark/real-project-0107/, SHA256 6ad9596c1c5e05f08ee3647ae3af1596f1882944e2397ac9efcd79383aa78894.
- 0109 #544 accepted/merged 34cd2b3 adds benchmark/project-text-writing-0109.{md,json}, checker and
  verification. WP1 proposes one unique Bld_version.build Int property text 2 -> 3, one byte at offset 3347,
  preserving other bytes/files and root declaration. No edit, native trial or method acceptance follows.
- 0110 #547 CLEAR is scoped to proposal integration preparation; Spec/Standards have no blocking findings.
  Its report independently resolves the unique source property/delta and retains independent later key approval.
  Baseline 8b93818c2779be00a2e267a3588eadcdaf665911 / tree e5cdbf5a3bf02dce5de55e0b0cd3fc27bb744c31;
  accepted candidate e5165269b5625455ad17bf34a3a8d1be95ee362f / tree 385ea919fc4f7714aa7bbdd29fd48ef60eaa74bb;
  reviewed checkout 668b9bedb30188100ab1c54e81436d674feea1a8 / tree e9a20bf69df2e366a47a612da6a6d8c80c8eb2c0.
- #547 evidence project-text-review.json, release iter-0110/547-project-text-review.json, 74,366 bytes,
  SHA256 2dc007939a4b0637716027ef6e5a874702c9be7288daf80c3f007c07f382cdaf. Reports say scoped bytes,
  22 historical pins and two supplementary inputs match. Control counts remain report claims here; use actual
  review artifact before downstream assertions. #547 C1 retains the acknowledged false-prose boundary.
- Next shaper consumes #547, stages exact evidence for a permitted benchmark writer, preserves it, then scopes
  qualified five-file method integration. Integration intentionally invalidates historical current-input hashes:
  preserve old pins/checker at reviewed tree; use a new provenance addendum/check, never refresh old evidence.
  Review the integration tree separately. Independently freeze complete text/preservation keys and full artifact
  manifests before either candidate arm. This is shaper goal work; no duplicate policy order is needed.
- No native key, restricted allocation, executed isolation, native validity/build/behavior/save-version result,
  benchmark readiness or product quality is established. Same-family independent sessions do not prove model diversity.
- Reports:
  .session/history/sessions/541/76ff7a20024053285dc2a1d0dfb018249e33cc13017ebcdba5ad0828e1ad5afc.md;
  .session/history/sessions/544/908fb5d0861e7178ef0b5f2ec23acdaefb5027fea533245950663b4d629a6b96.md;
  .session/history/sessions/547/d6eb2085115b86ba4e78c52b2307ddf0d700826dc74a4d31043d5e6f9d7303ef.md.

## Iterations 0105-0107: POC blocker and resumed preparation
- #528 completed all eight public owner #516 comparisons, merged bba00f7. findings-0105.md:
  edit-attempt-needs-more. Replay/verification/candidates records exist; do not rerun them or request fixtures.
  Controlled originals are owner-reported LabVIEW 2026 26.1.1f1 32-bit, not WM1 or verified 2024 cases.
- #533 merged fc70efc; docs/research/poc/pair/constant-rules-0106.md: source-blocked. [312,316) parses
  as textHair flags 4420|0200; 545/549 lie in ConstValue bodies 00000001->00000002 under DCO UID 118.
  Meaning/necessity, typed dispatch, BDPW chunks 1/2 and RTSG/LVSR/code/type rules remain unresolved.
  Equal BDHb with different BDPW tails refutes BDHb-only dependence. Boundaries justify no safe edit rule.
  Prepared production sources lack LVblock/LVdatatype/LVrsrc rules; do not repeat unchanged absence searches.
- No changed VI/fresh-agent demonstration, native validity/behavior or save-version preservation exists.
  LVSR 26008000 and vers/4 26118001 are declarations only. No impossibility conclusion follows.
- #532 optional unchanged Save As control remains pending. Do not duplicate, schedule unavailable work or wait.
  New control needs authoring/original/control pins; it alone supplies no integrity/type rule. Only new pinned
  primary source/control evidence addressing blockers warrants bounded POC follow-up.
- #536/#537 resumed ready benchmark preparation in 0107 after unsuccessful POC delivery and source blocker.
  #537 real-project-0107 evidence established four declarations and missing writing case; #541 reviewed it.
  Record 0107 accepted/improved, zero hits/parking. Earlier detailed source evidence remains in predecessor memory.
- Exact #533 report: .session/history/sessions/533/02493d512ed1055f2034c00d258ea102ee8929d0aa387880df1a4418f2822015.md.

## Quota evidence and decision rule
- Owner criterion: accepted-result quality per subscription quota, not elapsed time. Provider state is not billing
  or a quota-normalized comparison. Outside subscription use is unknown; do not infer causation.
- For a new availability question, use git log origin/loop-runtime, then selected pool.json or sessions/<N>.json
  with git show. Print only availability, usage and relevant error summaries; never dump repeated histories.
- Dated baseline 2026-11-13: #508/#511/#512/#515 sent 98 requests, about 3.96M cache-read, 305k cache-write,
  89k output; Policymakers accounted for about 57% of cache-read. Claude quota followed at 04:55Z;
  #518 parked 25,945 s. #520 later used 35 requests, 2.16M cache-read, 116k cache-write, 59k output;
  #521 parked 5,073 s. These are observations, not proof of quota causation or model-quality differences.
- #530 runtime pins: pool 76bd7ca and 2c910e6 record Claude quota at 14:46Z; 3ead7eb still records quota
  observed 15:30:22Z, retry_after 16:10:22Z. Codex observed available 15:52:32Z, model 16:03:49Z.
  Copilot last observed quota November 8. These are stale dated facts, not current availability. Provider state
  overrides stale model entries; retry_after is not proven recovery. Full event details remain in predecessor memory.
- 0105 #526/#527 each had four attempts, parked 3,826/3,763 s; waits may overlap. Rebase conflict cause is
  not attributed to a model. #528 produced accepted evidence without parking; #533 also completed without parking.
- #524 filed #525; approved/completed in #535 loop-state. Only every_iterations changed to 3; no_progress
  stayed 3 and model order stayed unchanged. Request fulfilled; do not resubmit. New requests need new evidence.
  The requested 0107-0109 comparison is complete in policy/observations/0111-review-and-cadence.md.
- Cost guide: earlier Policymakers used 17-40 turns; request bytes grow with turns. Aim below 20 actions.
  Select evidence, update memory/orders/report, then Finish. Outcome records omit Policymaker usage.

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
1. Keep every_iterations 3 and no_progress 3 unless new evidence justifies a change. The requested comparison
   is complete; do not repeat it or infer quota savings from zero parking. Read selected new records/reports.
2. Check #547 evidence preservation and qualified integration. A CLEAR proposal does not cover a changed
   integration tree or establish complete trial keys. Preserve historical checker/pins rather than refresh them.
3. Read actual artifact/source values before asserting counts or pins; report prose is not a substitute.
4. Check new control/source readiness before POC follow-up. #532 remains pending; do not duplicate or wait.
5. Keep policy orders to evaluator/audit; no duplicate replay, source-absence search, audit, estimate or gap map.
