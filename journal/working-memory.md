# Execution working memory

## Considered
- Iteration 0104: startup issue #521, orchestrator skill, loop-state, capabilities, prior memory read once. Live no_progress=2 (Policymaker trigger at 3), no accepted goal gate.
- Read `.session/history/records/0103.json`: one task `preserve-pair-review` (#518, researcher), ended `blocked`, unmerged, branch `task/518`, commit `67412de`; 21 attempts/limit hits, parked 25,945 s (quota waits, not work).
- Read trusted `.session/reports/518.json` (snapshot `9a62eba046e42f4e0c74450d632d0dc76ebdc82f44788adf0f9091805f779fd9`): both outputs written and hash/pin-verified; the only failure is the shaper's verification asserting eight probes while the artifact lists nine (ninth: `protocol_blocks_virtual_execution`).
- Read `.github/loop/task-graph.md` (graph schema, `start_branch` resume from tag `iter/NNNN/N`, one plain python3 verification).
- NOT read by this shaper: the review artifact itself, the four reviewed pair files, `docs/perpetua/roles.md`, `evaluation.md`, `operating-parameters.md`. Older findings below are inherited, not remeasured.
- Owner request #516 (author eight public controlled LabVIEW examples) is still pending; do not file a duplicate.
- History entry point: `.session/history/manifest.json`. Broker Glob ignores its path field: use the complete pattern.

## State
- Bounded unsuccessful POC delivered in accepted iteration 0093: `docs/research/poc/delivery.md` records missing changed VI/fresh-agent demonstration, unknown semantics/save-version preservation and no LabVIEW validation, with evidence, two exits and reproduction steps. Failure delivery is neither success nor impossibility.
- Eight selected VIs parsed without a supported executable semantic edit. POC code stays under `docs/research/poc/`; restart only on new bounded controlled evidence. No session can run LabVIEW. A fresh describing/editing session must receive tool and unseen VI without prior analysis.
- POC exit 1: #509 delivered `docs/research/poc/pair/owner-instructions.md`, `pair_diff.py`, `protocol.md`, `selfcheck.json` (task commit `53816a08feeb89a2747bf63ce8338ea315e06518`). Instructions specify add/subtract and constant-1/constant-2, each normal and separate-compiled-code: eight VIs plus fixtures/authoring.md. No controlled pair exists yet; open because request #516 is pending. Owner silence is not acceptance.
- #513 independently reviewed main `8f5ae4c48581459aa09b3f5e56f79db56188b86c`; four reviewed files match #509; recommends `closed`, no major finding. Its report text says eight passed probes; the saved artifact lists nine, all passed (#518 report). No VI written and no native claim established.
- #513 minor R1 open: pair_diff.py self-check rewrites tracked selfcheck.json. Deferred: fixing it changes reviewed bytes and would need re-review; fix only when the tool is next changed for a real reason (for example when #516 pairs arrive).
- Review preservation thread: #518 wrote `docs/research/poc/pair/review-0102.json` (SHA256 `562467370d558b15eb9a7faf8cb1bc283365f99ef3c8cada9c6f54f1ead8249f`) and `review-0102-provenance.md` on unmerged `task/518` (tag `iter/0103/518`). Open because the check was wrong, not the work; 0104 resumes it with a check that asserts no probe count.
- POC exit 2 (missing pinned source rules for BDPW, compiled cache, DTHP/VCTP, ConstValue) remains deferred: no new pinned source staged; delivery.md forbids further format research inside its delivery. No corpus restart.
- Benchmark resumed in 0094 after permitted failure delivery: #481 public synthetic writing requirements under `benchmark/writing/` (W1–W8 extending E1–E8); #485 findings S1/S2/S3 corrected by #489, independently closed by #493. Synthetic preparation establishes no real edit or execution.
- #493 reviewed commit `d3c697c375ed7dc880e55ab3cc2219577cd133a5`, tree `689ed2757ca4eb413cd37dc4f0cfcbc2fa90ba14`; seven writing hashes match #489. Re-pin if writing bytes change.
- Writing baseline `486030b461e57ca0f322a17a5b7853e83e9655e3` / tree `cf75cf6892de2f9410fa09ee2589dcba47d825a4`; candidate `7435c05c4fd7ddbaafb6f5db9081ad5a4f5db427` / tree `555960a979f4bec474850a39bd9b284b7188496a`. Inherited pins; a mismatch against git is a transcription question first.
- #497 closed #443 finding 1 on accepted `8aefb1583265f097a8569d76b4f8e5a0b0782833`, tree `94c6df4711068611c1c2eb3f7f5b54d150c1ea78`; do not repeat unchanged completion review.
- #501 effort study: 33–99 versus 89–264 engineer-days are reading-only, assume unverified 8.0–2025, not measured costs. No 2024 fallback selected or supported. Independent study review deferred until a fallback proposal would use it.
- #505 measured WM1 original `@environment/actor-framework/Core/ActorFramework/Message Dequeuer/Equals Not A Refnum.vi` (SHA256 `19b5dcd98b3b2e83e2b533d9227bd07d16837f350243377292b7c0b8a935338c`): vers IDs 4/7/8/9/10 and LVSR ID 0 declare raw `20008000`. Replay `python3 docs/research/0100-wm1-version-evidence.py` with LABVIEW_ENVIRONMENT. Closed measurement, not NI save-version authority; original-save-version remains missing.
- Native capability #169/grants and substantive independent native oracles remain open, availability unknown. Declined method request #430 (`not_planned`) must not be resubmitted unchanged.
- Last readiness read (0101): `@environment/readiness.json`: public_sources ready, pylavi `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75`, actor-framework `371c631c16155d88f02be11a953e4964d7452fd8`; labview_ide/model_access not_checked, semantic_reading not_measured.
- Open writing prerequisites: independent original-version authority/confirmed consumers, matched sources/builders, independent keys/checkers, restricted allocation/verified isolation and quota/precision decisions. Synthetic review closes none.
- Benchmark thread has had no new ordered work since 0101 (three iterations spent on the pair tool and its review record). Open because the next ready step was not chosen: it requires a fresh read of `docs/perpetua/roles.md` and `evaluation.md`. Next shaper does that read first.
- Product requires independently checked method/evidence and explicit owner method acceptance; writing also needs accepted writing coverage. Routine merges and silence confer no approval. No accepted goal gate.

## This iteration
- `.session/tasks.json`: one task `finish-pair-review-record`, researcher/default/low, `start_branch: task/518`, 20 minutes/20 turns, no edges, no inputs (the files are already on the branch).
- Expected gain: the #513 review becomes a committed record on main without a new review session. The corrected verification drops the probe count (asserts a nonempty list, all passed) and keeps hash, reviewed commit, verdict, four file pins, limitations and provenance presence.
- Next cold session checks: status of that task in record 0104 and its report; on main, `docs/research/poc/pair/review-0102.json` and `review-0102-provenance.md` exist.
- If done: the preservation thread is closed; do not order further pair-tool work until #516 delivers VIs. Read `docs/perpetua/roles.md` and `evaluation.md`, then order one ready benchmark preparation task (reading or writing) that does not depend on #516 or native capability. no_progress will be 3 if 0104 is not accepted as an improvement: prefer a task whose result can be accepted.
- If blocked again on a missing branch/tag: order the copy again from input `{issue:513,name:review-0102.json}` (staged flat as `.session/inputs/513-review-0102.json`) with the same corrected check. If pins drift: investigate only the changed bytes.
- When #516 supplies actual pairs, pin and compare using the reviewed protocol; any fresh-agent POC description/edit session must remain blind to the target VI's analysis. Native behaviour/save version still require owner checking.

## Tried, do not repeat
- #465/#468 established RSRC/BDHb framing. #468 in-memory 103->104 mutation wrote no VI and ran no LabVIEW, never Add-to-Subtract evidence.
- 0092 inspected eight fixtures (edit-readiness.md/json: null recipe, semantic/type/BDPW/cache blockers); 0093 delivered negative POC. No fabricated output, corpus restart, repeated delivery or waiting for owner.
- #481/#485/#489/#493 synthetic writing sequence is complete. Old `iter-0097/493-review-evidence.md` pointer is unverified.
- #443 checked allocator determinism/reordering and F3 infeasibility; #497 closes #446 guard correction. #501 scope reconciliation and #505 WM1 declarations already measured.
- #509 built pair preparation; #513 completed the independent review; #518 verified hash, commit, four pins and copied the artifact. None of these is to be repeated.
- 0103 lesson (#518): a verification count taken from a report summary was wrong (eight versus nine probes). Assert only values read from the source; otherwise check identity and leave counts out. Historical inputs are staged flat as `.session/inputs/N-X`, not under the release folder.
- No global gap maps #282/#330/#400, lineage batches without allocation effect or store-readiness reviews without a concrete new question.
- Engine verification lacks LABVIEW_ENVIRONMENT, session artifacts and report.md. Parent commits; no git commit or git-status acceptance requirement. One plain python3 command over committed files.
- Researcher staging omitted loop-state.json in #501; give explicit immutable pins. Graph inputs must be objects (strings are silently dropped).
- Reviewer outputs belong in `.session/report.md` and `.session/artifacts/`; a separate permitted writer preserves pinned evidence if a committed record is needed.
- Shaper empty Write erases a file; always write nonempty text and read outputs back. Broker Grep no-match establishes no absence. Avoid broad Glob using only path scoping.
