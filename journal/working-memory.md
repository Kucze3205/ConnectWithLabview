# Execution working memory

## Considered
- Iteration 0105, issue #526: startup issue, orchestrator skill, loop-state, capabilities and previous memory read once through the supplied continuation. Startup diagnostic `.session/startup.json` is ok (13,927 estimated tokens). Live no_progress=0; no accepted goal gate.
- Read record `.session/history/records/0104.json`: researcher #522 finished review preservation, accepted/improved/merged, commit `5c6dc23`. This thread is closed.
- Loop-state records owner request #516 approved/completed. #525 (Policymaker cadence question) remains pending; it does not block execution.
- Read `docs/research/poc/pair/protocol.md`, `fixtures/pins.json`, `verification.json`, and `.github/loop/task-graph.md`; Glob confirmed eight fixture VIs and authoring record on main.
- Read `docs/research/poc/pair/fixtures/authoring.md`: public examples, LabVIEW 2026 26.1.1f1, 32-bit, no password or previous-version save; exact edits and save settings recorded. Author reports are not independent native validation.
- Initial `.session/tasks.json` read after continuation returned FileNotFoundError despite historical Write results. Rewrote the graph explicitly; do not assume session output files survive a continuation.
- Historical entry point is `.session/history/manifest.json`. Older findings below are inherited, not remeasured. No VI or pair_diff.py content read by this shaper.

## State
- Accepted iteration 0093 delivered an unsuccessful bounded POC: `docs/research/poc/delivery.md` records missing changed VI/fresh-agent demonstration, semantic/save-version uncertainty, evidence, exits and owner instructions. Neither success nor impossibility was established.
- New controlled evidence makes POC exit 1 actionable: #516 supplied eight VIs (Add/Subtract and constant 1/2, normal/separate compiled code). Run the reviewed comparison protocol before deciding on an edit. No replay on these fixtures has been established by this shaper.
- `fixtures/pins.json` lists eight VI hashes and authoring SHA256 `78fa8be7a97869a346f56fad4627a58c8132fa9788e6f1f7da539987f0b011ee`. Verify, never regenerate to dismiss mismatch.
- #509 supplied pair_diff.py, protocol.md, owner-instructions.md and selfcheck.json. #513 reviewed commit `8f5ae4c48581459aa09b3f5e56f79db56188b86c`, verdict closed, no major finding. #522 preserved `review-0102.json` (SHA256 `562467370d558b15eb9a7faf8cb1bc283365f99ef3c8cada9c6f54f1ead8249f`) and provenance on main.
- Minor R1 remains: pair_diff.py --self-check rewrites tracked selfcheck.json. Avoid it. Fix only with a substantive tool change and then re-review changed bytes.
- POC code stays under docs/research/poc/, researcher role, no src/ implementation. No session runs LabVIEW. Future blind describe/edit sessions must receive the tool and unseen VI without analysis; owner must check behavior, broken arrow and save version.
- Exit 2 (missing derivation rules for BDPW, compiled cache, DTHP/VCTP and ConstValue) remains deferred without new pinned sources. Observed pair differences do not establish general derivation rules.
- Benchmark work resumes after this bounded evidence is judged; fresh reads of `docs/perpetua/roles.md` and `evaluation.md` are required before planning it. Do not let the new pair measurements become unbounded format research.
- Synthetic writing W1–W8 extending E1–E8: #481 prepared, #485 found S1/S2/S3, #489 corrected, #493 independently closed. No real edit/execution established. #493 reviewed commit `d3c697c375ed7dc880e55ab3cc2219577cd133a5`, tree `689ed2757ca4eb413cd37dc4f0cfcbc2fa90ba14`; re-pin if writing bytes change.
- Writing baseline `486030b461e57ca0f322a17a5b7853e83e9655e3`, tree `cf75cf6892de2f9410fa09ee2589dcba47d825a4`; candidate `7435c05c4fd7ddbaafb6f5db9081ad5a4f5db427`, tree `555960a979f4bec474850a39bd9b284b7188496a`. Inherited pins; discrepancies need transcription investigation first.
- #497 closed #443 finding 1 on accepted `8aefb1583265f097a8569d76b4f8e5a0b0782833`, tree `94c6df4711068611c1c2eb3f7f5b54d150c1ea78`; no repeat review.
- #501 effort study estimates 33–99 versus 89–264 engineer-days for reading only, assuming unverified 8.0–2025. Not measured costs, no 2024 fallback selected; independent review deferred until a fallback proposal uses it.
- #505 measured raw `20008000` vers/LVSR declarations in WM1 `@environment/actor-framework/Core/ActorFramework/Message Dequeuer/Equals Not A Refnum.vi`, SHA256 `19b5dcd98b3b2e83e2b533d9227bd07d16837f350243377292b7c0b8a935338c`. Replay `python3 docs/research/0100-wm1-version-evidence.py` with LABVIEW_ENVIRONMENT. Declaration measurement is not independent save-version authority.
- Native capability #169/grants and independent native oracles remain open, availability unknown. Declined method request #430 must not be resubmitted unchanged.
- Last readiness read (0101): public_sources ready; pylavi `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75`, actor-framework `371c631c16155d88f02be11a953e4964d7452fd8`; labview_ide/model_access not_checked, semantic_reading not_measured.
- Writing prerequisites remain: original-version authority/confirmed consumers, matched sources/builders, independent keys/checkers, restricted allocation/verified isolation and quota/precision decisions. Product requires independent readiness review and explicit owner method acceptance, including writing coverage for writing. No accepted goal gate.

## This iteration
- `.session/tasks.json`: one task `replay-owner-pairs`, researcher/default/medium, 60 minutes/60 turns, from main, no dependencies or artifact inputs.
- Integrity-check pinned fixtures, authoring and reviewed files; implement protocol replay in replay.py; compare all four logic and four save-setting pairs. Preserve failures and immutable inputs, do not run --self-check or edit VIs.
- Expected outputs: eight `<left>--<right>.json` files, `docs/research/poc/pair/pair-findings.json` and at-most-80-line pair-findings.md with `## Supports an edit attempt?`, plus replay.py.
- Next cold session reads record 0105/task report and findings: inspect exact candidate spans and unresolved BDPW/compiled-code dependencies before ordering any bounded edit. Author counterpart bytes can support comparison, but metadata differences and native validity must remain explicit.
- If initial integrity fails, investigate the named mismatch without regenerating pins. If parsing blocks, preserve exact JSON and decide on a narrowly scoped tool fix; changed reviewed bytes require independent review.
- If partial/blocked work is saved, resume its task branch/tag and correct only the missing piece. Do not rerun completed comparisons unnecessarily.
- Return to benchmark preparation after judging these findings; first read roles.md and evaluation.md. Do not duplicate completed owner request #516 or wait for #525.

## Tried, do not repeat
- #465/#468 established RSRC/BDHb framing; in-memory 103->104 mutation wrote no VI and proved no Add/Subtract semantics.
- 0092 inspected eight corpus fixtures with no supported edit recipe; 0093 delivered negative POC. No corpus restart or repeated delivery without new evidence.
- #481/#485/#489/#493 synthetic writing sequence completed; old iter-0097/493-review-evidence.md pointer is unverified.
- #443 measured allocator determinism/reordering and F3 infeasibility; #497 closed guard correction; #501 scope and #505 declarations already measured.
- #509 preparation, #513 review and #518/#522 review preservation are complete. Artifact lists nine probes, despite earlier report saying eight; verify source values, not summary counts.
- Saved-work resumption with corrected verification succeeded in #522 in seven turns; prefer that over reconstruction.
- No global gap maps #282/#330/#400, lineage batches without allocation effect, or store-readiness reviews without a concrete new question.
- Engine verifier lacks LABVIEW_ENVIRONMENT, session artifacts and report.md. Use one plain python3 command over committed outputs; parent commits, no git commit/status acceptance checks or shell heredocs/pipes.
- Historical artifact inputs are objects and staged flat as `.session/inputs/N-X`; strings are dropped. Researcher staging omitted loop-state in #501: provide explicit pins.
- Reviewer outputs go to report.md/session artifacts, not repository paths. Separate permitted writer preserves records if needed.
- Broker Glob needs a complete pattern; Grep no-match proves no absence. Never issue empty Write. Read required outputs back before Finish.
