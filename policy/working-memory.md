# Policy working memory

Updated by Policymaker #589 for iteration 0123. Considers records 0000–0122 through
.session/history/manifest.json, especially 0120–0122 and trusted reports #581/#584/#586/#587.
Detailed findings, exact report snapshots, runtime pins and change expectations:
policy/observations/0123-policy-check.md. Previous detailed evidence: policy/observations/0120-policy-check.md.
Read journal memory, execution definitions, task-graph/session contracts and docs/perpetua/evaluation.md.
Inspected runtime candidate sequences, Finish outcomes, selected Write targets and availability only.
Did not execute a benchmark checker, historical audit or probe; did not open 0121 package/review JSON.
Package content and semantic verdicts below remain report evidence, not a fresh policy review.
Startup: ok, 16,057 estimated tokens, no notices. No suggestions; exports manifest has no results.
Predecessor memory: 16,328 bytes, SHA256 02789be0aef12ad6aab7a997ce4a62de58590f77d073fc9949e9b9eba59c99cf;
accepted change #579 commit 1635a3ff1786cc505630bd5bf1d5e0ed0946053f. Retrieve with git show <commit>:policy/working-memory.md.
Older compression: #520 at 29ae339; 0024–0091 at 2b6f6870. Revisit only missing evidence or reconsidered decisions.
History manifest keys scope/checkout/records/report_snapshots/paths/search; counts are not arrays.
Records: .session/history/records/<nnnn>.json. Reports: .session/history/sessions/<issue>/<snapshot>.md and task.md.
Use short python3 -I queries; exclude input_state and duplicate outcome.shaper. Keep memory near 16 KB.

## Organization and current decisions
- #589 adds the report-marker and matching Finish-status rule to execution/roles/benchmark/SKILL.md. #584 lost
  two Finish calls: complete was invalid, then done lacked the report marker/yaml. Third Finish succeeded.
  Expected check: next benchmark session has one accepted Finish and no rejected Finish.
- #589 adds Close a review chain to execution/roles/orchestrator/SKILL.md. A CLEAR review closes its pinned scope;
  repeat only for changed evidence or a concrete unresolved finding. Correct NOT-CLEAR findings and review changed
  scope. After the key revision following #587 and its review, reassess against remaining method gaps and name
  each task's gap/expected gain in journal memory. No fixed review cap; never lift a block to end a chain.
  Expected check: records 0123–0125 show the gap/expected gain; repeated review names its new evidence or finding.
- Keep #579 reviewer routing Claude Sonnet, Codex, Copilot. Both #581 and #587 started on Claude, then used Codex
  for their evidence. Different-family review is partial, not established throughout either session. No further
  routing change without evidence; preserve fallback and disclose shared-family work. Never wait for another family.
- Keep #569 cold-order and reviewer Finish rules. #587 saved its expectation at action 9 before later reads;
  report discloses HEAD captured after source reads and whole-protocol read. Cold relative to package exposure,
  with startup-order deviation; no model-continuity certification. #581 is expressly exposed, not cold.
- Roles, evaluator, cadence, limits stay. #525 approved every_iterations=3, no_progress=3. Empty orders;
  no specific evaluator defect or answerable audit question requires a task. Shaper owns goal work and journal.
- With a shaper, Policymaker orders only evaluator/audit (.github/loop/task-graph.md). Execution cannot read policy/;
  communicate execution rules through execution/roles/orchestrator/. Reviewer write: [] is deliberate: report and
  .session/artifacts/ only. A permitted writer preserves evidence without replaying completed checks.
- Task model values are params aliases (default, opus), never model IDs. Routing selects by role class.
- #569 edit of execution/protocol.md was rejected despite profile execution/ access; cause unknown. Do not retry
  without checking contract. execution/roles/ and policy/ succeeded. Put role rules in skills.
- Audits #43/#55 crashed; order audits only for concrete available evidence. #526 conflict recovered by #527.

## Latest results: 0120–0122
- 0120 #581 reviewer done, 28 turns, no merge by design. Exposed semantic recheck of 0119: Standards CLEAR;
  Spec disposition CLEAR within assigned scope, complete key NOT-CLEAR. Reports agreement on all seven F3
  mappings, 422/429 records unchanged; F4 blocked disposition adequate, missing evidence still blocks F4.
  Review HEAD 19d43f01e6022a8ab269f04b2b88c12c98bf53b3, tree f08b518974955b5ab746f027123cd97322f23aa3.
  #584 preserved artifact benchmark/writing/wp1-disposition-review-0120.json, 38470 bytes, SHA256
  bd2cd46a79bfcaf56a033b631c5b29196545283a547af86c6bcb8e9150c54141. No preservation replay needed.
- 0121 #584 benchmark accepted/merged 4a0d8b3, 24 turns. New wp1-examples-0121-v1: proposed-awaiting-separate-check,
  benchmark_ready false. Reports complete conditional maps for WP1-0121-positive-map-v1 and
  WP1-0121-unverified-extra-map-v1; five relations each, stipulated two-file project/LICENSE workspace,
  eleven declared dependency references absent. Six of thirteen trial-artifact categories unavailable.
  Positive correct/correct applies only to the stipulated model. Extra startup-time assertion unverified/missing;
  whole answer unverified/partial. Authored expected bytes, not trial/native output. Historical key stays blocked.
  Reports checker exit 0, 55/55 rejecting controls; integrity only. Policy did not rerun.
- 0121 file pins under benchmark/writing/ (author/reviewer reports, not measured #589):
  wp1-examples-0121.json 8c6f6d82e4fdc9db268827fd1cc942daebf84319336bba3e7141a7a110a8e382;
  wp1-examples-0121.md b450a9d0b2d5abe9c72a7f16514705b2f72a8c4d835131843f59c2b17c3e0120;
  check_wp1_examples_0121.py 2050ffc23448503f96ea1b5a5769f47260cb67ca478c38f2967e9276d3cf46c1;
  wp1-examples-0121-verification.json d7a0bc9caab9e32a265f5645ecb3dbe47c5b05146078ffb63af9f7c667e0bcd3;
  wp1-examples-0121-pre-edit.md 649b71383e6f0467d41e97db38a3cb660a75d9e631abc411295b05fa0e35fa4b.
- 0122 #587 reviewer done, 29 turns, no merge. Reports Standards CLEAR / Spec CLEAR for conditional examples;
  all ten relation prescriptions agree. Adequate evidence for a later separate key revision to consider F4
  release for NEW conditional examples only. Review releases nothing and grants no historical complete-map credit.
  Historical F4 and both historical example slots remain blocked; no general usable key or readiness clearance.
  Reviewed HEAD 650c282024d073a59710cdb0b2cfe5463f9b4a9d, tree 752cb3a6b4010e6af388a1445402679aa564830d.
  Reports six package/five source pins match; once-run checker exit 0, 55 mutations, saved stdout matches.
- #587 release artifacts are NOT yet preserved in repository as of #589. Stage them for the next permitted writer:
  wp1-examples-cold-0122.json, 6414 bytes, SHA256
  e1676c54e3e980f488bbb4dcc9ec8bc981890a22ae5dbcce26a62b02cf8f51e7;
  wp1-examples-review-0122.json, 30049 bytes, SHA256
  6c7735d2c53e924075c14d68c83ba2b9c844e708778cfe563943f1c55e0b960b.
  Use inputs {issue: 587, name: <artifact>} (staged flat .session/inputs/587-<artifact>). Verify exact bytes;
  do not rerun checks for preservation. Artifact content remains report evidence until read by that writer.
- Next shaper: journal #586 already plans a new key revision with preserved reviewer input, unchanged 0119 and
  separate pinned review. Keep conditional scope explicit and historical blocks intact. Reuse #587 expectation;
  do not derive it again just to revise the key. After review, compare the next task's gain to other method gaps.
  Carry C1 human adjudication, native/dependency, isolation/allocation, method review and owner acceptance gaps.

## Key and project-text lineage
- Project original: Actor Framework 371c631c16155d88f02be11a953e4964d7452fd8, MIT, Core/AF PPL Build.lvproj;
  benchmark/real-project-0107/original.lvproj, 5806 bytes, SHA256
  1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf.
  LICENSE.txt, 1060 bytes, 529e65e6fc185d39380efd3957ef1c9acd0aac31ed288bcb9d124840861f03a2.
  #537/#541 established four declarations only (root version, URL, Packed Library, build text); no native authority.
- WP1 fixes unique Bld_version.build text 2 -> 3, byte 3347/line 42, size 5806, output SHA256
  8d984c2efd827a7b16f0f44fbaaf89adba0e031e2af743444f09f674c96e0e42. No actual trial/native output exists.
  #544 proposal, #547 review, #551 preservation, #554 integration, #557 review and #561 preservation closed.
  Historical checkers stay at historical pins; integration intentionally invalidated #544 frozen hashes.
  Integration command python3 -I benchmark/writing/verify_method.py; do not run without a concrete new question.
- Key thread 0115–0122: four author packages (#564/#571/#577/#584), four reviews (#567/#574/#581/#587).
  #567 F1/F2/P1 addressed by #571 and #569 rules; #574 F3/F4 prompted #577 correction and later #584 examples.
  Do not replay completed F1/F2/cold probes or re-review unchanged seven F3 mappings/adequacy of F4 containment.
- Current historical 0119 package (measured #579; retain byte-identical): wp1-key-0119.json SHA256
  2afdca4bfc6feaa9464348bed7709b0657ea1ccbbe5d6b0a33b549c78f41c142;
  .md 5f18384ed27e6b995426704f40316e69ee09a52084767304c15738f6e78980ac;
  check_wp1_key_0119.py 28ee70435c6a4fea7a79d942e7d90e9e3174ec31d64d741f93447000bc093d99;
  wp1-key-0119-verification.json bd6054c90b5264bb9e7909937dfabae39bd919665f869a8424d1346aaa5e6cfd.
  Source method.json 276f2881c70eae311195a4cc0a802e316ca06a206a0f1d16e7f041205fd3b0ac;
  protocol.md 1aeb83227dc11761160ff80d24eb03a216a2531d90c1a6d10ccb25bb85c7eb2f.
- #574 artifacts preserved by #577 under benchmark/writing/: wp1-key-review-0118.json,
  wp1-cold-expectation-0118.json, wp1-source-interpretation-0118.json, wp1-review-audit-0118.py.
  Exact hashes/sizes in policy/observations/0120-policy-check.md and predecessor memory. Do not execute audit.
  Earlier preserved #567 review: wp1-key-review-0116.json. Preserve all historical packages unchanged.

## POC blocker and other ready work
- Unsuccessful bounded POC #477 accepted in 0093, d616e38: docs/research/poc/delivery.md, verify_delivery.py.
  #479 pass established failure-delivery consistency only. No changed VI, fresh-agent demonstration, native
  validity/behaviour or save-version preservation. No impossibility conclusion follows. Benchmark preparation resumed.
- Original add.vi 6371 bytes, cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8,
  declared 21.0.0. #516 controlled fixtures owner-reported 2026 26.1.1f1 32-bit. #528 completed eight comparisons
  (bba00f7, findings-0105.md), edit-attempt-needs-more. No replay or duplicate fixture request.
- #533 fc70efc, docs/research/poc/pair/constant-rules-0106.md: source-blocked; ConstValue bodies 00000001->00000002
  at 545/549 under DCO UID 118; typed dispatch, BDPW, RTSG/LVSR/code/type rules unknown. Prepared sources lack
  LVblock/LVdatatype/LVrsrc recipes. No repeated absence searches. Reopen only with newly pinned primary evidence.
- #532 optional unchanged Save As control pending. Do not duplicate, schedule unavailable work or wait.
  Pair #509 reviewed #513, preserved #522 review-0102.json. --self-check rewrites tracked selfcheck.json; avoid it.
  #518 failed on summary-derived count; #520 added source-count/saved-work rules. Never replay probes to fix paths.
- Synthetic writing #481/#485/#489/#493 and allocator #497 closed. Effort #501 e67bb1a estimates 33–99 days
  (2024) vs 89–264 (all), READING ONLY, assumes 8.0–2025. Independent review and writing estimate precede fallback.
  #505 WM1 d9b03d1: declarations only, save-version authority null. No new survey without a concrete question.

## Quota evidence and routing
- Owner criterion: accepted-result quality per subscription quota. Tokens/provider availability are not normalized
  quota or billing; outside use unknown. Read docs/perpetua/operating-parameters.md before changing limits/routes.
- 0120/0121/0122: zero limit hits and parked seconds, all sessions done; verdicts none/accepted/none. No saving
  claim. 0122 no_progress=1 is expected for completed review, not a stall. Exact totals in 0123 observation.
- Runtime pin 533a7411ff9549edd3c82fcd09dedbd8cb1af011: #581 Claude actions 0–8, Codex 9–24, Claude 25–27;
  #584 Claude 0–8, Codex 9–19, Claude 20–23; #587 Claude 0–5, Codex 6–25, Claude 26, Codex 27–28.
  #581/#587 review evidence and #584 package Markdown/checker were written by Codex. Shared families remain a limit.
  Histories contain no switch reason/timestamps. No answerable audit question established; do not infer quota cause.
- Pool last modification 33bf594e3c82fde60a556435db7dd78d3d4a60bc at 02:18:22Z: Claude unknown observed 02:17:08Z,
  retry_after 02:22:08Z (earlier available 01:25:38Z/01:55:08Z); Codex available, model observation 02:18:05Z;
  Copilot quota, retry_after 02:16:05Z with no recovery observation. Retry times prove no recovery. No waiting/spending.
- Inspect availability/candidates/errors/selected actions only via git show <pin>:pool.json or sessions/<N>.json.
  Whitelist availability; never print credentials or whole runtime records. Older quota windows in predecessor
  memory/0111 observation; do not replay comparisons. #525 approved cadence only.

## Remaining limits and mechanics
- No native benchmark run, matched agent comparison, native key, withheld writing case or verified isolation.
  Artifact/version/hardware coverage incomplete, tool quality unmeasured. Capability #169 readiness unknown.
- Preparation index is navigation, not readiness. #430 declined; no unchanged acceptance request or request from
  partial key work. Product needs independent method review AND owner acceptance of pinned protocol/evidence;
  writing also accepted writing coverage. Merges, green checks and silence establish neither acceptance nor quality.
- No accepted Goal gate, no goal/gate.yml, no completion claim. Full goal and all-version priority remain.
- Read docs/perpetua/accepted-limits.md before private use/disclosure/publication/spending/capability proposals.
  Optional access never blocks an iteration. No such action or owner request proposed #589.
- Avoid unchanged gap maps #282/#330/#400, reviews #403–#431, lineage batches and store-readiness searches.
- Report starts <!-- session-report --> then fenced yaml status matching Finish: done/partial/blocked/rejected.
  Write wip early. Empty Write truncates. Read required outputs immediately before Finish.
- Session writes may be absent from git diff/status. Verify actual outputs; recreate only missing ones on continuation.
  Layer checker needs real .session/policy-facts.json (absent); do not invent facts to claim activation passed.
  PyYAML available for catalog validation. Orders empty {"tasks": []}; wake only for results affecting the next order.
- Evaluator changes require evaluator and separate protected verifier; no evaluator defect established here.
  Two unfinished Policymakers trigger rollback. Keep work bounded and finish outputs.

## Next Policymaker
1. Check benchmark Finish rule against actual next session, and review-chain rule against named gains/new evidence.
2. Check new key keeps conditions/historical partial blocks and gets separate pinned review; no clearance from a count.
3. Reassess next method gap after review. Do not replay #581/#587 or a saved cold derivation for preservation.
4. Check actual author/reviewer families, retain fallback, and report shared-family work. No quota-saving inference.
5. Keep cadence unless new evidence; #532 stays optional and pending. No unavailable task or duplicate request.
