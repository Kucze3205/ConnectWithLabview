# Policy working memory

Updated by Policymaker #569 for iteration 0117. Considers records 0000–0116, selected new records
0114–0116, report snapshots #561/#564/#566/#567, task body #567, origin/loop-runtime sessions/564.json,
sessions/567.json and pool.json history of 2026-11-13, and journal memory "This iteration".
This session did not read the key files or the #567 review artifact and ran no checker or probe.
Counts and hashes for 0114–0116 below are report claims unless marked measured.
Startup: ok, 16,087 estimated tokens, no notices. No suggestions; exports manifest has no results.
Predecessor: policy/working-memory.md at startup, 16,448 bytes, SHA256
230b60a2dc42ae58db9cb3992e9e5bbb8ff4adeb958af696144dc0c911fa06ac; last accepted policy change
38ceeb008f84575fae77f98ab5ef60a4f6b68e46 (change-559). Use git show <commit>:policy/working-memory.md.
#520 compressed older memory: git show 29ae339:policy/working-memory.md. Older 0024–0091 detail:
git show 2b6f6870:policy/working-memory.md. Revisit only for missing pins/reasons.
History: .session/history/manifest.json (keys scope/checkout/records/report_snapshots/paths/search; records and
report_snapshots are counts). Records .session/history/records/<nnnn>.json; reports
.session/history/sessions/<issue>/<snapshot>.md plus task.md (task JSON and body). Extract selected record fields
with python3 -I; skip input_state and the duplicated outcome.shaper. Keep memory below about 16 KB.

## Organization and current decision
- #569 changed three definitions; roles, evaluator, cadence (#525: every_iterations=3, no_progress=3) stay. Empty orders.
  1. execution/roles/orchestrator/SKILL.md, "Writing a task": new rule "Keep a cold check cold". Reason: #567 P1.
     Task #567 required own derivation first, but its Budget listed wp1-key-0115.md to read whole; the session read
     it at action 5 and the key IDs at action 13, and derived at action 24. Expected effect: the next cold key
     review saves its derivation before opening key files and reports no P1-type limitation.
  2. execution/roles/reviewer/SKILL.md: report marker/status rule. Reason: #567 lost three Finish calls
     (NOT-CLEAR, completed, missing marker); #564 lost one. Expected effect: no rejected Finish in reviewer history.
  3. policy/params.yml routing.tasks.reviewer: Codex first, Sonnet second, Luna third. Reason: benchmark route is
     Claude-first; key #564 was written mainly by claude-sonnet-5-5 and reviewer #567 also started on Sonnet
     (actions 0–17, 29–32; Codex 18–28, 33–40). Expected effect: review of Claude-written work starts on another
     family when Codex is available. Check: candidate fields in origin/loop-runtime sessions/<N>.json history.
     Re-check when the author route changes. Fallback inside one session still mixes families; record as a limit.
- Edit of execution/protocol.md was rejected (PermissionError: outside accepted paths) although the profile lists
  execution/. Edits under execution/roles/ and policy/ succeeded. Cause unknown; not retried. Put execution work
  rules in role skills unless the engine contract is read first for this restriction.
- Policymaker orders only evaluator/audit when a shaper exists (.github/loop/task-graph.md). The shaper owns goal
  tasks and journal memory; it cannot read policy/. Reach it through execution/roles/orchestrator/.
- Reviewer write: [] is deliberate; findings use .session/report.md and .session/artifacts/. A permitted writer
  preserves useful evidence. Do not broaden reviewer writes.
- Task `model` is an alias from params models (default, opus), never a model id; routing chooses by role class.
- Audits #43/#55 crashed; order audits only for concrete available evidence. #526 failed on rebase conflicts;
  #527 recovered. Inspect exact errors before reorganizing on a new failure.

## Latest results: 0114–0116
- 0114 #561 (benchmark, Codex, 26 turns) accepted/merged c10f05e: benchmark/writing/review-0113.json (20,056 bytes),
  review-0113-probes.json (67,202), review-0113-probes.py (20,784), review-0113-provenance.md. Three #557 pins
  matched before copying. #557 integration review is preserved; do not repeat review or preservation.
  Candidate 0e371f84162004146990cb1262b044dd4bf0dd79 / tree 557a725623d04d1df5415751c4079bca056034f3;
  baseline 575d59ef8fcaf1f81a81d2eb605f52eb94053839 / tree bd09e3a07e772337a3f045f69611b9f51dd3e227.
- 0115 #564 (benchmark, mainly Sonnet, 22 turns, 4 attempts, parked 1944 s) accepted/merged ae579a8:
  benchmark/writing/wp1-key-0115.{json,md}, check_wp1_key_0115.py, wp1-key-0115-verification.json; revision
  wp1-key-0115-v1. Start e57b1c0fa9c88be18eadf4ed0cdc3f92665e1f4d / tree 354b36e13ea0953207d8e1d02fcdd8c4bd6b3b3b.
  Claims: 36 read inputs, 8 IDs (1 text, 4 preservation, 3 answer), 23 rules, 429 obligations (334 method.json
  pointers, 95 protocol lines); checker rejects 30/30 in-memory counterexamples; integrity/coverage only.
  Proposed key, author did not approve it. Native key unavailable; workspaces/model/quota/arm order unallocated.
- 0116 #567 (reviewer, 41 turns, 13 attempts, parked 6775 s, no merge by design): **NOT-CLEAR** for key correctness.
  Reviewed 7f480824a8fe64ac5082ce021a85ba7879c4b991 / tree aa0f52d802f2f453d4826fe8f06dca941b937b05.
  Six IDs agree; WP1-property-text blocked (P1) and WP1-original-output-grounding blocked (F2).
  F1 medium: 17 mappings under /tasks/4/comparison/matched_fields, /comparison/rule, /requirements_mapping/W7 point
  only to R-scope/R-independent; need R-paired, R-account and where required R-uncertainty.
  F2 high: wrong-existing-citation case has ambiguous answer correctness; R-mapping and R-dimensions blocked;
  freeze separate correctness/grounding tests per ID and one ledger. Other 21 rule texts agree.
  P1 high review limitation: derivation was not blind. Numerical recalculation agrees: Bld_version.build 2 -> 3,
  byte 3347, line 42, size 5806, output SHA256 8d984c2efd827a7b16f0f44fbaaf89adba0e031e2af743444f09f674c96e0e42.
  Artifact wp1-key-review-0116.json, release iter-0116/567-wp1-key-review-0116.json, 135,476 bytes, SHA256
  2f127a7dad8e9719f6e026e1a1fce5aa1b0509f8503d5994771e0234c83a373e; builder 33,740 bytes, SHA256
  d47e0cb6829f7b057189db1cfd5b859a48480f4df512e9d01685e4d9a02ad370. Not preserved in the repository yet.
- Iteration verdict none in 0116 is a completed review with findings, not a failed session or a stall.
  no_progress is 1. Shaper next (its journal memory already says so): key revision limited to F1/F2, then a fresh
  cold check; preserve exact review evidence through a permitted writer when needed. Do not replay probes.
- C1 stays open: structured checks/hashes do not establish narrative truth; extra claims, contradictions and
  citations need independent adjudication. No native keys, withheld allocation, executed isolation, native
  validity/build/behavior/save-version result, benchmark readiness or product quality follows from any of this.

## Project-text lineage: 0107–0113
- #537 real-project-0107 measured four declarations; #541 CLEAR covers them only. Actor Framework revision
  371c631c16155d88f02be11a953e4964d7452fd8, MIT, Core/AF PPL Build.lvproj, 5,806 bytes, SHA256
  1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf. D1 root LVVersion, D2 dependency URL,
  D3 Packed Library type, D4 Bld_version.build. Declarations, not native authority. No other project without a
  new question. #544 preserved review-0108.json (SHA256 6ad9596c…a78894) at benchmark/real-project-0107/.
- #544 proposal merged 34cd2b3: benchmark/project-text-writing-0109.{md,json}. WP1: unique Bld_version.build text
  2 -> 3 only. #547 CLEAR (proposal integration preparation only) preserved by #551 a4bb56a as
  benchmark/project-text-writing-0109/review-0110.json, 74,366 bytes, SHA256
  2dc007939a4b0637716027ef6e5a874702c9be7288daf80c3f007c07f382cdaf (measured by #559).
- #554 integration merged 0e371f8: seven paths under benchmark/writing/ (method.json, README.md, controls.json,
  verify_method.py, verification.json, integration-0112-provenance.{json,md}). Command:
  python3 -I benchmark/writing/verify_method.py. It intentionally invalidates the frozen #544 checker's old input
  hashes; keep historical checkers at historical pins, never refresh them. #557 Standards CLEAR and Spec CLEAR for
  integration preparation only; C1 Low/nonblocking. Earlier commit/tree pins: predecessor memory.

## POC blocker and ready work
- Bounded unsuccessful POC #477 accepted in 0093, d616e38: docs/research/poc/delivery.md, verify_delivery.py.
  #479 pass establishes failure-delivery consistency only. No changed VI, fresh-agent demonstration, native
  validity/behavior or save-version preservation exists. No impossibility conclusion follows.
- Original add.vi: 6,371 bytes, SHA256 cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8,
  declared 21.0.0. Owner #516 fixtures differ: owner-reported 2026 26.1.1f1 32-bit. #528 completed all eight
  comparisons (bba00f7, findings-0105.md: edit-attempt-needs-more). Do not repeat comparisons or fixture requests.
- #533 merged fc70efc, docs/research/poc/pair/constant-rules-0106.md: source-blocked. ConstValue bodies
  00000001->00000002 under DCO UID 118 at 545/549; typed dispatch, BDPW chunks, RTSG/LVSR/code/type rules
  unresolved. Prepared sources lack LVblock/LVdatatype/LVrsrc rules. Do not repeat unchanged absence searches.
- #532 optional unchanged Save As control remains pending. Do not duplicate, schedule unavailable work or wait.
  Reopen bounded POC work only for newly pinned primary source/control evidence addressing concrete blockers.
- Pair preparation #509 (53816a0), review #513 (no major; R1 low: --self-check rewrites tracked selfcheck.json,
  avoid it), preserved by #522 (5c6dc23). #518 failed on a false probe count; #520 added assert-only-source-values
  and saved-work resumption rules to the orchestrator. Never replay probes to fix paths.

## Quota evidence and decision rule
- Owner criterion: accepted-result quality per subscription quota. Provider state is not billing or a normalized
  comparison; outside use is unknown. Read docs/perpetua/operating-parameters.md before tuning/stall responses.
- 0114–0116: limit_hits 0/4/13, parked 0/1944/6775 s. Measured from pool.json checkpoints on origin/loop-runtime:
  2026-11-13 20:16–23:05Z Codex was quota (attempts 1 to 5) while Claude was unknown with 5–20 minute retries and
  Copilot was quota (retry_after 2026-11-14T02:16:05Z). At 23:27Z Codex available, Claude unknown. Selected checkpoints
  recorded no available provider. Claude's unknown state does not prove quota
  exhaustion, and these snapshots do not establish whether reordering would avoid parking. No quota-based
  routing change is justified here; the reviewer reorder is for family independence. retry_after is not proven recovery.
- Earlier windows (policy/observations/0111-review-and-cadence.md): 0101–0106 33 hits; 0107–0113 zero hits.
  Tasks/models/availability confound cadence; no quota-saving claim. Do not repeat that comparison.
- #525 approved; only every_iterations became 3. Do not resubmit. Records omit Policymaker usage.
- Availability question: git log origin/loop-runtime -- pool.json, then git show <commit>:pool.json or
  sessions/<N>.json (keys history/requests/result/usage; history items have action/candidate/outcome).
  Print only availability/candidate/errors, never whole histories (files exceed 300 KB).
- Cost guide: #569 used about 28 actions; aim below 20. Combine reads into one python3 -I command. Select
  evidence, change definitions, update memory, orders, report, Finish.

## Other closed evidence and remaining limits
- Synthetic writing #481/#485/#489/#493 CLEAR at d3c697c375ed7dc880e55ab3cc2219577cd133a5; controls design-only.
- Allocator #497 CLEAR at 8aefb1583265f097a8569d76b4f8e5a0b0782833 closes #443 finding 1.
- #501 effort study e67bb1a, docs/research/0099-writing-version-effort.*: 33–99 days (2024) versus 89–264 (all
  versions) is reading only; assumes 8.0–2025. Independently review before any fallback proposal.
- WM1 #505 d9b03d1, docs/research/0100-wm1-version-evidence.*: declarations only, save-version authority null.
- Preparation index is navigation, not readiness; read the source before stating its count. #430 declined;
  policy/proposals/method-acceptance-draft.md needs writing coverage before reuse.
- No native benchmark run, agent comparison, native answer key, withheld writing case or verified isolation.
  Coverage by artifact/version/hardware incomplete; tool quality unmeasured. Capability #169 readiness unknown.
- No Goal gate accepted; no goal/gate.yml; no completion claim. Product needs an independently reviewed method and
  owner acceptance of pinned protocol/evidence; writing also needs accepted writing coverage. Merges, green
  checks and silence establish no acceptance. State gaps in every evaluation report.
- Read docs/perpetua/accepted-limits.md before private use/disclosure/publication/spending/capability requests.
  Optional access never blocks an iteration.
- Do not repeat without a new question: gap maps #282/#330/#400, reviews #403–#431, lineage batches, store
  searches, allocator review, effort estimate, WM1 audit, POC failure delivery, pair comparisons, preserved
  reviews #541/#547/#557, key authorship #564 outside F1/F2.

## Session mechanics
- Report starts <!-- session-report -->, fenced yaml status equals Finish.status (done/partial/blocked/rejected).
  Write wip early. Empty Write.text truncates the file: the first report Write of #569 produced 0 bytes.
  Read required outputs immediately before Finish. Owner-facing report uses short STE sentences.
- Session writes can be absent from git status/diff. Continuations may show historical Writes while outputs are
  absent; check .session/ for report.md and orders.json and recreate only what is missing.
- Layer check python3 policy/layer-rules.py .session/policy-facts.json needs facts; the file was absent in #569.
  PyYAML is available: yaml.safe_load(policy/params.yml) checks syntax and anchors after a routing edit.
- Empty orders: {"tasks": []}. wake true only if results change the next order. Evaluator changes need an
  evaluator order plus separate verifier; path policy/evaluator/evaluate.py. No policy-only goal tasks.
- Requests: .github/loop/session-protocol.md, Requests to the owner. Read limits first. None filed by #569.
- Two unfinished Policymakers trigger rollback (last 2026-11-11T21:41:42Z); keep sessions bounded.

## Next Policymaker
1. Check the three #569 changes against new records: P1-type limitation absent in the next cold key review,
   no rejected reviewer Finish, first reviewer candidate Codex when available. Revert or adjust what failed.
2. Check that the shaper ordered a key revision limited to F1/F2 and then a fresh cold check, and that review
   evidence is preserved by a permitted writer when needed. Verify actual bytes before detailed claims.
3. Keep cadence unless new evidence; provider-state snapshots do not prove a routing fault. No runtime probe without a question.
4. #532 pending; do not duplicate or wait. POC follow-up only on new pinned source/control evidence.
5. Orders stay evaluator/audit only. No readiness, method-acceptance or product-start claim follows from key work.
