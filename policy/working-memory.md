# Policy working memory

Updated by Policymaker #579 for iteration 0120. Considers records 0000–0119, selected new records
0117–0119 and trusted report snapshots #571/#574/#577 found through .session/history/manifest.json.
Read journal memory, current 0119 Markdown/pre-edit findings, selected 0117/0119 JSON and preserved 0118
findings. Checked runtime #574 read/save/Finish/candidates, first candidates #571/#577 and provider availability.
Measured current package/review hashes and obligation continuity; ran no key checker, audit or probe.
Detailed evidence and pins: policy/observations/0120-policy-check.md. Report claims remain labelled there.
Startup: ok, 15,753 estimated tokens, no notices. No suggestions; exports manifest has no results.
Predecessor memory: 15,380 bytes, SHA256 6e5583619174c9e188dfac98bec625920e54f6f648ad0d235e638692cf0645af,
accepted policy commit 44dcab63ec581e2e50312eb053cf686fe256d513 (change-569). Use git show <commit>:policy/working-memory.md.
Older detail: #520 compressed at 29ae339; 0024–0091 at 2b6f6870. Revisit only missing pins/reasons.
History manifest keys scope/checkout/records/report_snapshots/paths/search; counts are not arrays. Records:
.session/history/records/<nnnn>.json. Reports: .session/history/sessions/<issue>/<snapshot>.md plus task.md.
Use short python3 -I queries; exclude input_state and duplicated outcome.shaper. Keep memory near 16 KB.

## Organization and current decision
- #579 changes only routing.tasks.reviewer in policy/params.yml to Claude Sonnet, Codex, Copilot. Actual authors
  #571/#577 and reviewer #574 all used Codex despite the Claude-first author route. Prefer another family for
  review of this work when available; keep fallback during quota limits. Select from actual author evidence,
  not configured routes. Check actual next-review candidates; no guaranteed family difference or quota saving.
- #569's cold-order and reviewer report/Finish rules stay. #574 actual history: limited reads/derivation actions
  3–8, cold artifact saved at action 9, first key access action 11; one accepted done Finish at action 33.
  P1 satisfied for #574 only. One successful observation supports retaining rules, not a general rate claim.
- Roles, evaluator, cadence and limits stay. #525 approved every_iterations=3, no_progress=3. Empty orders;
  no new audit/evaluator question needs a task. Shaper owns goal tasks and journal memory.
- With a shaper, Policymaker orders only evaluator/audit (.github/loop/task-graph.md). Shaper cannot read policy/;
  communicate execution rules through execution/roles/orchestrator/. It already carries the semantic-recheck handoff.
- Reviewer write: [] is deliberate. Findings go in .session/report.md and .session/artifacts/. A permitted writer
  preserves useful evidence without repeating completed probes. Do not broaden reviewer writes.
- Task model is a params alias (default, opus), never a model ID; routing chooses by role class.
- #569 edit of execution/protocol.md was rejected although profile lists execution/. Cause unknown; do not retry
  without checking contract. execution/roles/ and policy/ succeeded. Put work rules in role skills.
- Audits #43/#55 crashed; order audits only for concrete available evidence. #526 rebase conflict recovered by #527.

## Latest results: 0117–0119
- 0117 #571 benchmark accepted/merged 9be5934, 28 turns, all Codex. New wp1-key-0117 package and exact preserved
  benchmark/writing/wp1-key-review-0116.json, 135476 bytes, SHA256
  2f127a7dad8e9719f6e026e1a1fce5aa1b0509f8503d5994771e0234c83a373e (measured #579).
  Reports 17 F1 mapping corrections, F2 separate correctness/grounding tests and relational-map ledgers;
  68 rejecting controls/13 assessments. Historical key remains proposed. Do not replay authorship/preservation.
- 0118 #574 reviewer done, 34 turns, no merge by design. Actual runtime uses only Codex, one accepted Finish.
  Standards CLEAR / Spec NOT-CLEAR for wp1-key-0117-v1. Reviewed HEAD 16a825da7c7c72b93424f5449a08e86f513b0855,
  tree 153b39cd1371f9c7652c75eca3edb8a7e6637dc1; report says 45 scoped files match intended
  6ff164b101ee38dbc6f22fb9775d30d56f63364f. P1 satisfied for this session; F1/F2 agree, F3/F4 block approval.
  F3: seven operative leaves linked only to R-scope/R-independent omit concrete preservation/grading rules.
  F4: C1-correct/C1-unverified-extra lack complete preservation maps; WP1-original-output-grounding blocked.
- All four #574 artifacts are preserved by #577 under benchmark/writing/; hashes measured #579:
  wp1-key-review-0118.json (569049 bytes) 410b0ebf7d3135521d10bd32d3b1102769caa848f5e5c7278d8e9a29eefd9a55;
  wp1-cold-expectation-0118.json (5036) 7ca817b22c430ece354287b0e42cd3deb106afaeee9a0d3d6c9d7dfd4dad141c;
  wp1-source-interpretation-0118.json (2257) b18eb04d01455a3d4b539a67042a83c4efc5d627f73ccd309ba6f1e7f48ea46b;
  wp1-review-audit-0118.py (31314) 8fc53c741b4d6628228e0abae53fbf3c64200c3f318d6ac903c8bbf73b13e833.
  Preservation/provenance complete; do not repeat it or execute preserved audit. Numerical derivation remains
  public development evidence: Bld_version.build 2 -> 3, byte 3347/L42, size 5806, output SHA256
  8d984c2efd827a7b16f0f44fbaaf89adba0e031e2af743444f09f674c96e0e42; no actual trial output/native authority.
- 0119 #577 benchmark accepted/merged f4528e8, 28 turns, all Codex. Ten additions under benchmark/writing/.
  wp1-key-0119-v1 remains proposed-awaiting-separate-check. Actual JSON comparison by #579: both packages
  have 429 obligation records; exactly seven changed, 422 equal. Changed method leaves: /common/artifact_fidelity_rule
  and /tasks/4/requirements_mapping/W{1,2,3,4,5,8}/review. This is continuity, not semantic approval.
  F3 correction awaits separate check. F4 blocked-for-missing-evidence; map ID established_key_use.status blocked.
  Missing complete pre/post workspace/dependency inventories, immutable-original/license evidence and all map
  relations. Reports partial/partial map outcomes, assessments partial/partial and unverified/partial.
  Reports checker exit 0, 85 rejecting controls/3 assessments while block remains. #579 did not rerun it.
- Measured #579 package SHA256:
  wp1-key-0119.json 2afdca4bfc6feaa9464348bed7709b0657ea1ccbbe5d6b0a33b549c78f41c142;
  wp1-key-0119.md 5f18384ed27e6b995426704f40316e69ee09a52084767304c15738f6e78980ac;
  check_wp1_key_0119.py 28ee70435c6a4fea7a79d942e7d90e9e3174ec31d64d741f93447000bc093d99;
  wp1-key-0119-verification.json bd6054c90b5264bb9e7909937dfabae39bd919665f869a8424d1346aaa5e6cfd.
- Next shaper: separate pinned semantic recheck of F3 and F4 blocked prescriptions, using preserved #574 independent
  expectation and unchanged continuity. No new cold derivation just to repair those findings. Do not replay
  completed F1/F2 or #574 probes. A recheck cannot make an incomplete key ready. A complete-map example later
  needs a new identity, concrete missing evidence and separate review before lifting F4. Avoid indefinite review
  of unchanged evidence. Keep C1 human narrative adjudication and remaining readiness gaps visible.

## Project-text lineage: 0107–0116
- #537 real-project-0107 measured four declarations; #541 CLEAR covers them only. Actor Framework revision
  371c631c16155d88f02be11a953e4964d7452fd8, MIT, Core/AF PPL Build.lvproj, 5806 bytes, SHA256
  1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf. D1 root LVVersion, D2 dependency URL,
  D3 Packed Library type, D4 Bld_version.build. Declarations, not native authority. No other project without a
  new question. #544 preserved review-0108.json (6ad9596c…a78894) at benchmark/real-project-0107/.
- #544 proposal merged 34cd2b3: benchmark/project-text-writing-0109.{md,json}. WP1 unique build text 2 -> 3.
  #547 CLEAR for integration preparation only; #551 preserved project-text-writing-0109/review-0110.json,
  SHA256 2dc007939a4b0637716027ef6e5a874702c9be7288daf80c3f007c07f382cdaf (measured #559).
- #554 integration 0e371f84162004146990cb1262b044dd4bf0dd79 / tree 557a725623d04d1df5415751c4079bca056034f3;
  baseline 575d59ef8fcaf1f81a81d2eb605f52eb94053839 / tree bd09e3a07e772337a3f045f69611b9f51dd3e227.
  Seven paths under benchmark/writing/: method.json, README.md, controls.json, verify_method.py, verification.json,
  integration-0112-provenance.{json,md}. Command python3 -I benchmark/writing/verify_method.py. Integration
  intentionally invalidates #544 frozen input hashes; historical checkers stay at historical pins, never refresh.
- #557 Standards/Spec CLEAR for integration preparation only; C1 remains. #561 preserved review-0113.json,
  review-0113-probes.json, review-0113-probes.py and provenance, c10f05e. Never replay for preservation.
- #564 ae579a8 authored wp1-key-0115 package: proposed 8 IDs/23 rules/429 obligations, no native key or allocation.
  #567 NOT-CLEAR: F1 insufficient paired/accounted mappings; F2 ambiguous relational-map grade; P1 exposed cold
  derivation. #569 rules addressed P1 and rejected Finish calls. Selected pins/earlier model evidence in predecessor.
- Current 0117 predecessor JSON SHA256 008b4078d7f50610c7eb74e7d880e20602416130398fabf7a7534ae2a6b60982;
  Markdown ba62fabd3324329447515728d38113185ee7e7702faead0f6ca7f68a5a0a97a3. Preserve old packages unchanged.

## POC blocker and ready work
- Bounded unsuccessful POC #477 accepted in 0093, d616e38: docs/research/poc/delivery.md, verify_delivery.py.
  #479 pass establishes failure-delivery consistency only. No changed VI, fresh-agent demonstration, native
  validity/behavior or save-version preservation exists. No impossibility conclusion follows.
- Original add.vi: 6371 bytes, SHA256 cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8,
  declared 21.0.0. Owner #516 fixtures differ: owner-reported 2026 26.1.1f1 32-bit. #528 completed eight
  comparisons (bba00f7, findings-0105.md: edit-attempt-needs-more). Do not repeat comparisons or requests.
- #533 fc70efc, docs/research/poc/pair/constant-rules-0106.md: source-blocked. ConstValue bodies 00000001->00000002
  under DCO UID 118 at 545/549; typed dispatch, BDPW chunks, RTSG/LVSR/code/type rules unresolved. Prepared
  sources lack LVblock/LVdatatype/LVrsrc rules. Do not repeat unchanged absence searches.
- #532 optional unchanged Save As control pending. Do not duplicate, schedule unavailable work or wait. Reopen
  bounded POC work only with newly pinned primary source/control evidence addressing concrete blockers.
- Pair #509 (53816a0), review #513 no major, #522 preserved review-0102.json (5c6dc23). R1 low: --self-check
  rewrites tracked selfcheck.json; avoid it. #518 failed on false probe count; #520 added source-count and
  saved-work resumption rules. Never replay probes to fix paths.

## Quota evidence and decision rule
- Owner criterion: accepted-result quality per subscription quota. Provider state is not billing or normalized
  quota use; outside use unknown. Read docs/perpetua/operating-parameters.md before tuning/stall response.
- 0117–0119: zero limit hits/parked seconds each; all sessions done. Verdicts accepted/none/accepted.
  Token totals and actual availability pins in policy/observations/0120-policy-check.md. No savings claim.
- Runtime bbe678242c51d43c09950c8f5b0000f49cc7eccb pool: Claude quota observed 2026-11-14T00:35:38Z,
  retry_after 01:15:38Z; Codex available with model observation 00:53:26Z; Copilot quota retry_after 02:16:05Z.
  Older model available entries do not override newer provider quota. Retry times do not establish recovery.
  Claude-first reviewer may still fall back; no waiting or new spending follows. Recheck actual author family.
- Prior 0114–0116 limit hits 0/4/13, parked 0/1944/6775 s. Pool snapshots then showed Codex quota, Claude
  unknown and Copilot quota; no evidence reordering would avoid parking. No quota-based routing fault proven.
- Older windows policy/observations/0111-review-and-cadence.md: 0101–0106 33 hits, 0107–0113 zero; confounded
  by models/tasks/availability. Do not replay that comparison. #525 approved cadence only; do not resubmit.
- Availability questions: git log origin/loop-runtime -- pool.json; git show <commit>:pool.json or sessions/<N>.json.
  Query only availability/candidates/errors/selected actions; do not print credentials or whole histories.
- Policy sessions should stay bounded: combine independent reads, select evidence, change definitions, memory,
  orders, report, Finish. No runtime probe without a concrete question.

## Other closed evidence and remaining limits
- Synthetic writing #481/#485/#489/#493 CLEAR at d3c697c375ed7dc880e55ab3cc2219577cd133a5; design controls only.
- Allocator #497 CLEAR at 8aefb1583265f097a8569d76b4f8e5a0b0782833 closes #443 finding 1.
- #501 effort study e67bb1a, docs/research/0099-writing-version-effort.*: 33–99 days (2024) vs 89–264 (all)
  is reading only, assumes 8.0–2025. Independent review and writing estimate before any fallback proposal.
- #505 d9b03d1, docs/research/0100-wm1-version-evidence.*: declarations only, save-version authority null.
- Preparation index is navigation, not readiness. Read sources before counts. #430 declined; unchanged method
  acceptance draft needs writing coverage before reuse. No new acceptance request from partial key work.
- No native benchmark run, matched agent comparison, native key, withheld writing case or verified isolation.
  Artifact/version/hardware coverage incomplete; tool quality unmeasured. Capability #169 readiness unknown.
- No Goal gate accepted, no goal/gate.yml, no completion claim. Product requires independently reviewed method
  and owner acceptance of pinned protocol/evidence; writing also accepted writing coverage. Merges, green
  checks and silence establish no acceptance. Missing coverage stays explicit in evaluation reports.
- Read docs/perpetua/accepted-limits.md before private use/disclosure/publication/spending/capability proposals.
  Optional access never blocks an iteration. No such action or new owner request from #579.
- Do not repeat without a new question: gap maps #282/#330/#400, reviews #403–#431, lineage batches, store
  searches, allocator review, effort study, WM1 audit, POC delivery/pairs and preserved completed reviews.

## Session mechanics
- Report starts <!-- session-report -->, fenced yaml status equals Finish.status (done/partial/blocked/rejected).
  Write wip early. Empty Write.text truncates. Read required outputs immediately before Finish.
- Session writes can be absent from git status/diff. Verify outputs exist; recreate only missing outputs on
  continuation, never rerun completed work because the transcript shows a historical Write.
- Layer check python3 policy/layer-rules.py .session/policy-facts.json needs facts (absent #569). PyYAML is
  available; yaml.safe_load(policy/params.yml) checks anchors after routing edits. Check exact routing scope.
- Empty orders {"tasks": []}. wake true only when results change the next order. Evaluator changes require
  evaluator plus separate protected verifier; path policy/evaluator/evaluate.py. No policy-only goal tasks.
- Owner request contract: .github/loop/session-protocol.md. Read accepted limits first. Owner-facing report and
  request prose use short STE sentences. Do not change exact frozen/readiness/test content during prose edits.
- Two unfinished Policymakers trigger rollback (last 2026-11-11T21:41:42Z); keep work bounded.

## Next Policymaker
1. Check #579 reviewer reorder against actual next-review candidates and author family. Preserve fallback;
   unavailable other-family review is a disclosed limit, not a reason to wait. Reconsider from actual results.
2. Check shaper followed separate pinned F3/F4 recheck, kept F4 blocked until concrete complete-map evidence,
   and avoided another cold derivation or replay of completed work. Read actual findings before ordering fixes.
3. Check new scope is bounded. If F3/F4 evidence stays unchanged, do not repeat semantic reviews indefinitely.
   No key clearance establishes native authority, readiness, method acceptance or measured product quality.
4. Keep cadence absent new evidence. #532 pending; no duplicate or wait. POC follow-up needs new pinned evidence.
5. Orders stay evaluator/audit only. No new evaluator task without a specific defect in available evidence.
