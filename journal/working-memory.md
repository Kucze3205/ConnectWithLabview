# Execution working memory

## Considered
- Iteration 0105: startup issue #526, orchestrator skill, loop-state, capabilities, prior memory read once. Live no_progress=0, no accepted goal gate. Open owner request: #525 (Policymaker cadence question, pending; not ours to act on).
- Read `.session/history/records/0104.json`: one task `finish-pair-review-record` (#522, researcher), `done`, accepted, improved, merged (commit `5c6dc23`). Review preservation thread is closed.
- Loop-state `recently_closed`: owner request #516 (eight controlled VIs) is `approved` / `completed`.
- Glob `docs/research/poc/pair/**` on main: eight VIs, `fixtures/authoring.md`, `fixtures/pins.json`, `fixtures/.gitattributes`, `review-0102.json`, `review-0102-provenance.md`, plus the four reviewed files and `verification.json`.
- Read `docs/research/poc/pair/fixtures/pins.json` (schema 1, eight VI hashes, authoring hash `78fa8be7a97869a346f56fad4627a58c8132fa9788e6f1f7da539987f0b011ee`), `docs/research/poc/pair/verification.json` (#509's tool check on pylavi add.vi, not on the owner pairs), `docs/research/poc/pair/protocol.md` (replay loop, pair list), `.github/loop/task-graph.md`.
- NOT read by this shaper: `fixtures/authoring.md`, any VI, `pair_diff.py`, `review-0102.json` content, `docs/perpetua/roles.md`, `evaluation.md`, `operating-parameters.md`. Who wrote `pins.json` (owner or a session) is unknown. Older findings below are inherited, not remeasured.
- History entry point: `.session/history/manifest.json`. Broker Glob ignores its path field: use the complete pattern.

## State
- Bounded unsuccessful POC delivered in accepted iteration 0093: `docs/research/poc/delivery.md` records missing changed VI/fresh-agent demonstration, unknown semantics/save-version preservation and no LabVIEW validation, with evidence, two exits and reproduction steps. Failure delivery is neither success nor impossibility.
- POC exit 1 is now ACTIVE: the owner completed #516 and the eight controlled VIs (add/subtract, constant-1/constant-2, each normal and separate-compiled) are on main with pins. No replay on them has been run yet; 0105 orders it. Open because the replay result decides whether a bounded edit attempt has evidence.
- POC code stays under `docs/research/poc/` (role `researcher`), nothing under `src/`. No session can run LabVIEW. A fresh describing/editing session must receive tool and unseen VI without prior analysis; the owner checks native behaviour and save version by hand.
- Pair tool: #509 delivered `owner-instructions.md`, `pair_diff.py`, `protocol.md`, `selfcheck.json` (task commit `53816a08feeb89a2747bf63ce8338ea315e06518`). #513 reviewed main `8f5ae4c48581459aa09b3f5e56f79db56188b86c`, verdict `closed`, no major finding; committed record `docs/research/poc/pair/review-0102.json` (SHA256 `562467370d558b15eb9a7faf8cb1bc283365f99ef3c8cada9c6f54f1ead8249f`) with `review-0102-provenance.md` (#522). The artifact lists nine probes, all passed.
- #513 minor R1 open: `pair_diff.py --self-check` rewrites tracked `selfcheck.json`. Deferred: fixing it changes reviewed bytes and needs re-review; fix only when the tool is changed for a real reason (for example a blocker found by the 0105 replay). Until then no task runs `--self-check`.
- POC exit 2 (missing pinned source rules for BDPW, compiled cache, DTHP/VCTP, ConstValue) remains deferred: no new pinned source staged. The 0105 replay may narrow it by observation (which BDPW chunks and VICD/CPC2 payloads change); observation is not a derivation rule.
- Benchmark thread: paused again by the goal's POC priority now that exit 1 has real material. Last ordered benchmark work was 0101. Resume after the pair findings are judged; first read `docs/perpetua/roles.md` and `evaluation.md` (still unread by recent shapers).
- Benchmark resumed in 0094 after permitted failure delivery: #481 public synthetic writing requirements under `benchmark/writing/` (W1–W8 extending E1–E8); #485 findings S1/S2/S3 corrected by #489, independently closed by #493. Synthetic preparation establishes no real edit or execution.
- #493 reviewed commit `d3c697c375ed7dc880e55ab3cc2219577cd133a5`, tree `689ed2757ca4eb413cd37dc4f0cfcbc2fa90ba14`; seven writing hashes match #489. Re-pin if writing bytes change.
- Writing baseline `486030b461e57ca0f322a17a5b7853e83e9655e3` / tree `cf75cf6892de2f9410fa09ee2589dcba47d825a4`; candidate `7435c05c4fd7ddbaafb6f5db9081ad5a4f5db427` / tree `555960a979f4bec474850a39bd9b284b7188496a`. Inherited pins; a mismatch against git is a transcription question first.
- #497 closed #443 finding 1 on accepted `8aefb1583265f097a8569d76b4f8e5a0b0782833`, tree `94c6df4711068611c1c2eb3f7f5b54d150c1ea78`; do not repeat unchanged completion review.
- #501 effort study: 33–99 versus 89–264 engineer-days are reading-only, assume unverified 8.0–2025, not measured costs. No 2024 fallback selected or supported. Independent study review deferred until a fallback proposal would use it.
- #505 measured WM1 original `@environment/actor-framework/Core/ActorFramework/Message Dequeuer/Equals Not A Refnum.vi` (SHA256 `19b5dcd98b3b2e83e2b533d9227bd07d16837f350243377292b7c0b8a935338c`): vers IDs 4/7/8/9/10 and LVSR ID 0 declare raw `20008000`. Replay `python3 docs/research/0100-wm1-version-evidence.py` with LABVIEW_ENVIRONMENT. Closed measurement, not NI save-version authority; original-save-version remains missing.
- Native capability #169/grants and substantive independent native oracles remain open, availability unknown. Declined method request #430 (`not_planned`) must not be resubmitted unchanged.
- Last readiness read (0101): `@environment/readiness.json`: public_sources ready, pylavi `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75`, actor-framework `371c631c16155d88f02be11a953e4964d7452fd8`; labview_ide/model_access not_checked, semantic_reading not_measured.
- Open writing prerequisites: independent original-version authority/confirmed consumers, matched sources/builders, independent keys/checkers, restricted allocation/verified isolation and quota/precision decisions. Synthetic review closes none.
- Product requires independently checked method/evidence and explicit owner method acceptance; writing also needs accepted writing coverage. Routine merges and silence confer no approval. No accepted goal gate.

## This iteration
- `.session/tasks.json`: one task `replay-owner-pairs`, researcher/default/medium, 60 minutes/60 turns, no edges, no inputs, from main.
- It runs the reviewed protocol replay on the eight owner VIs (four logic pairs, four save-setting pairs) through a new `docs/research/poc/pair/replay.py` (the protocol's heredoc is not runnable with session tools), without touching the four reviewed files, pins, authoring record or VIs, and without `--self-check`.
- Outputs to check next: `docs/research/poc/pair/pair-findings.md` (section `## Supports an edit attempt?`), `pair-findings.json` (`labview_run` false, eight `pairs` with `exit`/`status`), eight `<left>--<right>.json` files, record 0105 and the task report.
- Expected gain: evidence on which bytes differ for Add versus Subtract and constant 1 versus 2, and which dependent bytes (BDPW, VICD/CPC2) have no known derivation rule.
- If findings localize a small span with no unexplained dependent change (most plausible in the separate-compiled variants): order a bounded POC edit attempt under `docs/research/poc/` (researcher) that produces a changed VI from one fixture, compares it byte-for-byte against the owner's counterpart as the check, then a blind describe/edit session and owner instructions. A byte-identical reproduction of the owner's file is the strongest evidence available without LabVIEW.
- If dependent bytes change without a rule (BDPW hash, compiled code): record the named blocker; decide between a measurement task on that dependency using the eight files, or an owner question for further controlled pairs. Do not order format research without pinned sources.
- If the replay blocked (pin mismatch, load failure, unsupported heap): read the blocked JSON message; a tool fix is then a real reason to change `pair_diff.py` (fix R1 in the same task, then re-review).
- If the task ended partial/blocked: resume from tag `iter/0105/<issue>` with `start_branch`, correcting only the failing piece.
- Afterwards return to the benchmark thread (read `roles.md` and `evaluation.md` first).

## Tried, do not repeat
- #465/#468 established RSRC/BDHb framing. #468 in-memory 103->104 mutation wrote no VI and ran no LabVIEW, never Add-to-Subtract evidence.
- 0092 inspected eight corpus fixtures (edit-readiness.md/json: null recipe, semantic/type/BDPW/cache blockers); 0093 delivered negative POC. No fabricated output, corpus restart, repeated delivery or waiting for owner.
- #481/#485/#489/#493 synthetic writing sequence is complete. Old `iter-0097/493-review-evidence.md` pointer is unverified.
- #443 checked allocator determinism/reordering and F3 infeasibility; #497 closes #446 guard correction. #501 scope reconciliation and #505 WM1 declarations already measured.
- #509 built pair preparation; #513 reviewed it; #518/#522 preserved the review record on main. None of these is to be repeated. Do not re-request the eight VIs (#516 completed).
- 0103 lesson (#518): a verification count taken from a report summary was wrong (eight versus nine probes). Assert only values read from the source; otherwise check identity and leave counts out. Historical inputs are staged flat as `.session/inputs/N-X`, not under the release folder.
- 0104 lesson (#522): resuming saved work with `start_branch` and a corrected check cost 7 turns and was accepted; prefer it over redoing.
- No global gap maps #282/#330/#400, lineage batches without allocation effect or store-readiness reviews without a concrete new question.
- Engine verification lacks LABVIEW_ENVIRONMENT, session artifacts and report.md. Parent commits; no git commit or git-status acceptance requirement. One plain python3 command over committed files; no heredocs, pipes or redirection in session commands.
- Researcher staging omitted loop-state.json in #501; give explicit immutable pins. Graph inputs must be objects (strings are silently dropped).
- Reviewer outputs belong in `.session/report.md` and `.session/artifacts/`; a separate permitted writer preserves pinned evidence if a committed record is needed.
- Shaper empty Write erases a file; always write nonempty text and read outputs back. Broker Grep no-match establishes no absence. Avoid broad Glob using only path scoping.
