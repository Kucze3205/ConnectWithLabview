# Policy working memory

Updated by Policymaker #609 for iteration 0129. Considers records 0000–0128 through
.session/history/manifest.json; directly 0126–0128 and trusted reports #601/#604/#607.
Detailed findings, exact report/runtime pins, measured identities and expected checks:
policy/observations/0129-policy-check.md. Earlier: policy/observations/0126-policy-check.md and 0123-policy-check.md.
Read journal memory, current execution profiles/reviewer/orchestrator skills, task-graph/session-protocol contracts,
evaluation.md, operating-parameters.md and accepted-limits.md. Read 0128 handoff and preserved 0126 findings whole;
inspected integrity accounting and completion/verification metadata. Measured five preserved compact identities.
No fresh semantic review of cases, expectations, author/checker code, initial ledger or large comparison.
No benchmark checker, builder, audit, trial or native execution. Semantic judgments remain reviewer evidence.
Startup ok: 16,127 estimated tokens, no notices. No suggestions; exports manifest has no results.
Predecessor memory: 16,879 bytes, SHA256 1afd063b51deb647085de25b3c06dcd73b8da24dc32864dacf322a93293d4c7a;
retrieve with git show b03c26a9e8d85f25085619e401fbd1e98d73d87f:policy/working-memory.md.
Earlier #599 change accepted 9bdcf31a3a91b66c8fc05a342eaef199d5c4469f; #589 at 90cd7cc;
#579 at 1635a3f; #520 at 29ae339; 0024–0091 at 2b6f6870. Revisit missing detail, contradictions or reconsidered decisions only.
History manifest keys scope/checkout/records/report_snapshots/paths/search; counts are not arrays.
Records .session/history/records/<nnnn>.json; reports .session/history/sessions/<issue>/<snapshot>.md.
Use short python3 -I queries; select task metadata and outcomes, exclude input_state and duplicate outcome.shaper.
#609 first query printed full task bodies unnecessarily; do not repeat it. Keep memory near 16 KB; link detailed observations.

## Organization and current decisions
- #609 adds two small execution skill rules. Orchestrator must explicitly export each historical report required by
  a worker and check manifest availability; cold tasks defer content until the initial judgment is saved. #601
  required full #597 but exported nothing and needed a continuation. Next check: explicit reports/session selectors
  and no missing-report continuation for the next such task; never read expectation-bearing content early.
- Reviewer must use allowed role Bash/Python for required in-session integrity measurements, or record the exact
  missing tool/rejection. Repository-only engine verification does not prohibit session measurements. #604's action13
  successfully used Python/hashlib (exit0); its 25-action history has no rejected Bash/hash attempt. Its report's
  unavailable-hashing explanation is not established by actions. This does not prove every unattempted command works.
  Next check: actual required measurements/argv/results or precise capability evidence, never assumed failure.
- No profile expansion, evaluator change, routing/limits/cadence change or Owner request. Empty orders: no concrete
  evaluator defect or answerable audit task. Shaper owns ready F1 correction/recheck; no new integrity-only review.
- #589 report-marker/Finish rule retains expected observations: all six #600/#601/#603/#604/#606/#607 had one accepted
  Finish and zero rejected Finish calls. No causal or quota-savings claim. Close-review-chain rule remains: correct
  named NOT-CLEAR findings, review changed scope, carry unresolved blocks; never lift a block to end a chain.
- Next ready step: newly pinned local F1 correction followed by separate affected-scope review. Preserve inability
  atoms, both historical grounding interpretations and original raw hashes. Actual human C1 stays separate/open.
- Keep #579 reviewer routing Claude Sonnet, Codex, Copilot; every recorded action in the latest six sessions was Codex.
  Different-family review was not achieved. Prefer another available family, preserve fallback and disclose shared
  family. Do not wait for recovery; no cross-model accepted-quality/normalized-quota evidence supports route changes.
- #525 approved every_iterations=3, no_progress=3. 0126/0127 had no accepted improvement; 0128 accepted, current no_progress=0.
- With a shaper, Policymaker orders only evaluator/audit (.github/loop/task-graph.md). Execution cannot read policy/;
  communicate execution rules through execution/roles/. Reviewer write: [] is deliberate: report/session artifacts.
  A permitted writer preserves artifacts without replaying completed checks. Profiles already allow reviewer git/Python.
- Task model values are params aliases (default, opus), never model IDs; routing selects by role class.
- #569 execution/protocol.md edit rejected despite execution/ access; cause unknown. Do not retry without contract check.
  execution/roles/ and policy/ succeeded. Put role rules in skills. Audits #43/#55 crashed; only concrete audits.

## Latest results: 0126–0128
- 0126 #601 reviewer partial/unmerged, 40 turns, twelve artifacts. Standards CLEAR / Spec NOT-CLEAR for new C1 package.
  Reports source-first ledger saved before expectations/checker: 1428942 bytes, SHA256
  32b3a36ad53b708726032a896d93a8cfe8cc1fa23bf6ddf77ebe65f28384a117, 370 rows. Original stays immutable.
  Comparison crosswalks 265 authored atoms: 956134 bytes, cf55770e01161a961b53cced969e81acb7c03223cf7bcf9ad061f38ecfc69e27.
  Original releases iter-0126/601-c1-challenges-cold-0126.json and iter-0126/601-c1-challenges-review-0126.json.
  Neither is a newly staged policy input. Full cold review is complete; public familiarity/uncertified continuity remain.
- #601 all initial whole-answer/required-ID judgments agree; later N04 implicit-assertion omission and N03 evidence-label
  correction remain separate from cold bytes. Actual checker once exit0 is structural only. Partial reason was missing
  full #597 report, not incomplete cold work. F1 semantic finding is completed review work, not a missing cold derivation.
- F1 exact locator: benchmark/writing/c1-challenges-0125-expectations.json#/cases/7/atoms/11 (a11.1).
  Raw cases#/cases/7/raw_answer bytes [554,635): “I cannot supply an edited project or an original/output map in this scenario. [V]”.
  Absence of output does not establish inability; scenario stipulates both. Preserve separate project/map inability atoms.
  Source cases#/conditions/citations, /citation_registry/V and /conditions/scenarios/abstention. A permits explicit
  scenario reference (inability grounding correct). B restricts support to bracket registry (V lacks scenario pointer,
  inability/honest-limits grounding incorrect; whole-answer grounding partial -> incorrect). Scenario-based inability
  correctness correct either way; whole-answer correctness partial. No policy selection or new general grading rule.
- 0127 #604 reviewer partial/unmerged, 25 turns, one artifact. Explicit reports exports supplied #597/#601; author-report
  comparison complete, no evidence resolves F1. Only staged-byte/output integrity unmeasured. Do not repeat report read.
  #609 runtime review corrects unsupported tool explanation as above; no need for a capability request from this evidence.
- 0128 #607 benchmark done/accepted/merged d6f7707, 24 turns. Python measured six staged inputs and both report digests;
  reports all match fixed pins. Preserved five compact originals under benchmark/writing/reviews-0128/; large comparison
  stays in original release. Integrity-0128.json distinguishes measurement from assertions; verifier rehashes repository
  copies, only records attributed measurements for unstaged comparison/report exports. Handoff fixes no semantic finding.
- #609 measured five copies matching published bytes/hash: manifest 28787 / 9a655f487a30539450c0abe36d4ebe570b43dc6fbddba914fae0fbd638121bc7;
  findings 7179 / 519fe802c72d1089b55425936ce31485d9d7502b2c602b72bdda92c11f4fbf41;
  pins 4511 / 916bd993cf979e0ff3810ac3503c9bb1008f6ed564749fd3c3962691698fd690;
  checker-run 2378 / 04a2146d44bfe5a1a9fb1a775bbec897df3db776c973550dc2569bb13527d49e;
  completion 10038 / fc11233cd67752355607350a4a223395db07ee65a7933004517f85225d6cf600.
  Full basenames, integrity/verification pins and exact report snapshots are in 0129 observation. No semantic approval.
- Next shaper reads reviews-0128/handoff-0128.md and preserved findings, then orders only named F1 correction and separate
  pinned N08 recheck before human scoring/key promotion. Preserve original raw answers/hashes; changed answers get new
  identities. Recheck inability atoms, honest-limits ID and whole-answer grounding under explicit local interpretation.
  Agent work cannot produce actual human evidence. No general established-key/full-trial release or readiness from CLEAR.

## Prior C1/key results and project lineage
- 0123 #591 conditional key incorporation accepted 67ec6ec; 0124 #594 closes that scope Standards CLEAR / Spec CLEAR.
  Conditional F4 CLEAR applies ONLY to WP1-0121-positive-map-v1 and WP1-0121-unverified-extra-map-v1.
  Map judgments agree/correct; extra whole answer unverified/partial. Historical map slots stay partial/partial
  blocked-F4; historical whole answers partial/partial and unverified/partial. No general release.
- #597 preserved #594 at benchmark/writing/wp1-key-review-0124.json: 126735 bytes, SHA256
  23369a95a2c6a847dbe0bf09c9e19dc04c36b7a75269f03018dcbb6e282076a6. #599 confirmed identity only.
  #587 conditional examples and #594 incorporation stay closed; preserved reviews need no repeat preservation.
- #597 C1 package accepted a80ab6e3454dcb47c15457d7c10126a8b4a6cda3, tree 469bcfdfd331a3a07d549b5d081a342cb98be8bc.
  Eight public cases, separate expectations/procedure/template/author/checker; exposed, familiar-possible, never withheld.
  Script integrity cannot certify arbitrary prose. Frozen cases SHA256 73dfd06532782777d5cc7390fef290c5ef079730ed41ac9bd5786956d2b0a710;
  expectations 5b3761ae2b8e351038b9b2ace8b5a684940009b55e1fbee9d0907ff642864071;
  verification ce8642fc2c2b23e826cb24786fbc06c9a3319c978f30e4fdb1c7389a01540fbc.
  #599 verified nine manifest and 125 protected identities. Exact sizes/other pins in 0126 observation/predecessor.
  Never dump 1.11 MB expectations whole. Source-first work saves/hashes initial judgments before expectations;
  preserve revisions, uncertainty and exposure. Agent review is never human adjudication or continuity certification.
- Original Actor Framework 371c631c16155d88f02be11a953e4964d7452fd8, MIT, Core/AF PPL Build.lvproj:
  benchmark/real-project-0107/original.lvproj 5806 bytes / 1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf;
  LICENSE.txt 1060 / 529e65e6fc185d39380efd3957ef1c9acd0aac31ed288bcb9d124840861f03a2.
  #537/#541 declarations only. WP1 Bld_version.build 2 -> 3, byte 3347/line 42; expected output SHA256
  8d984c2efd827a7b16f0f44fbaaf89adba0e031e2af743444f09f674c96e0e42. No native/trial result.
- Integration #544–#561 and key author/review #564–#594 closed except explicit historical/general blocks.
  Historical 0119 package, method/protocol and other exact pins remain in immutable predecessor and 0123/0126 observations.
  #577 preserved #574; #591 preserved #587. Do not run preserved audit/checkers or replay probes. Integration intentionally
  invalidated #544 hashes. Current integration command python3 -I benchmark/writing/verify_method.py; no unchanged replay.
- Shared conditional model: project+LICENSE, eleven absent dependency references, authored expected bytes,
  declaration-only version authority, six unavailable trial categories, logical/unexecuted isolation. No dependency
  closure, actual trial/native output, verified save-version preservation or quality measurement. Missing coverage stays explicit.

## POC blocker and other ready work
- Bounded POC failure #477 accepted 0093, d616e38: docs/research/poc/delivery.md and verify_delivery.py. #479 pass means
  failure-delivery consistency only. No changed VI/fresh-agent demonstration/native validity/behavior/save-version proof.
  Failure proves no impossibility; benchmark preparation resumed. No session can run LabVIEW.
- add.vi 6371 bytes / cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8, declared21.0.0.
  #516 fixtures owner-reported 2026 26.1.1f1 32-bit; #528 eight comparisons bba00f7/findings-0105.md, edit-attempt-needs-more.
  No replay or duplicate fixture request. #533 fc70efc, constant-rules-0106.md: source-blocked; ConstValue 00000001->00000002
  at545/549, DCO UID118; type dispatch/BDPW/RTSG/LVSR/code rules unknown. Prepared sources lack LVblock/LVdatatype/LVrsrc
  recipes. Reopen only with newly pinned primary evidence, never repeated absence searches.
- #532 unchanged Save As control optional/pending; do not duplicate, wait or schedule unavailable work. Pair #509/#513
  closed, #522 preserved review-0102.json. --self-check rewrites tracked selfcheck.json; avoid it. #518 failed summary-derived
  counts; #520 saved-work/source-count rules remain. No probe replay to fix paths.
- Synthetic writing #481/#485/#489/#493, allocator #497 closed. #501 e67bb1a reading estimate 33–99 days (2024) vs89–264(all),
  assumes8.0–2025. Independent review AND writing estimate precede fallback. #505 WM1 d9b03d1 declarations only, native
  save-version authority null. No new survey without a concrete question; no 2024 fallback selected.

## Quota evidence and routing
- Criterion: accepted-result quality per subscription quota. Tokens/provider availability are not normalized quota/billing;
  outside use unknown. Read operating-parameters.md before tuning. No paid API/quota/runner/storage grant.
- 0126/0127/0128 verdicts none/none/accepted; zero limit hits. Six sessions all Codex, two reviewers partial for missing read
  and unmeasured integrity, writer completed preservation. Totals:8535313 input,65434 output,7989504 cache-read,0 cache-write.
  No savings claim. #599's prior window is in 0126 observation; no replay for comparison without a concrete question.
- Runtime pin cbc7b315c9692ade54466521abfbd235f0a4b5fc holds sessions/600,601,603,604,606.json and pool availability;
  later sessions/607.json at85534878f7d7a548686b0212b5b38cbdf90b04e7. Each one Finish accepted; exact action indices in0129 observation.
  Older pin lacked607; first combined query failed after five summaries, then latest607 resolved. Do not replay them.
- Pool atcbc7b3: Claude provider quota/session observed05:23:04Z retry_after08:03:04Z; Codex provider available04:24:45Z,
  model06:32:28Z; Copilot quota/unspecified02:58:58Z retry_after08:58:58Z, all2026-11-14. Old model records/retry times prove
  no provider recovery. No waiting/spending or causal quota inference from request bytes/counts.
- Read runtime only through git show <pin>:pool.json or sessions/<N>.json; whitelist availability, candidates/actions/errors.
  Never print credentials or whole runtime records. No answerable audit question remains after bounded contradiction check.

## Remaining limits and mechanics
- Human C1/use/agreement, actual inventory/dependency bytes/native keys/capability/grants/logs, restricted allocation and
  executed isolation, matched settings/budgets/repeats, independent method review, owner acceptance, thresholds and
  all-version writing effort remain open. Artifact/version/hardware coverage incomplete; tool quality unmeasured.
- No native benchmark, matched comparison, withheld writing case or verified isolation. Capability#169 readiness unknown.
  Preparation index is navigation, not readiness. #430 declined; no unchanged acceptance request from partial key work.
  Product requires independent method review AND owner acceptance of pinned protocol/evidence; writing also accepted
  writing coverage. Routine merge, green checks and silence establish neither acceptance nor measured quality.
- No accepted Goal gate, no goal/gate.yml, no completion claim. Full goal/all-version priority remains.
- Read accepted-limits.md before private use/disclosure/publication/spending/capability proposals. Optional access never
  blocks iterations. #609 read limits; no such action, Owner request or new resource-dependent task proposed.
- Avoid unchanged gap maps#282/#330/#400, reviews#403–#431, lineage/store-readiness/source-absence batches.
- Report starts <!-- session-report --> then fenced yaml status matching Finish:done/partial/blocked/rejected.
  Write wip early; empty Write truncates. Read required outputs immediately before Finish.
- Parent commits accepted actions; session writes may be absent from git diff/status. Compare start baseline and read
  actual outputs; recreate only missing files. No rebase/merge/push/commit or shell expansion.
- .session/policy-facts.json absent; never invent facts or claim layer activation passed. PyYAML available.
  Orders empty {"tasks":[]}; wake only for actionable policy results. Evaluator changes need evaluator+protected verifier.
  Two unfinished Policymakers trigger rollback; keep work bounded and finish outputs.

## Next Policymaker
1. Check new explicit-report export rule and actual reviewer integrity actions when next applicable; do not create busywork.
2. Inspect only changed F1 package and separate affected-scope review; preserve original interpretations and disagreements.
3. Confirm agent correction/review is not called human adjudication; historical/general/full-trial blocks stay explicit.
4. Reassess remaining evaluation gaps after F1, not another unchanged key/integrity review. Human evidence remains needed.
5. Check actual author/reviewer families and current availability; retain fallback and avoid quota-savings inference.
6. Keep cadence unless new evidence. #532 optional/pending; no duplicate request, unavailable task or wait.
