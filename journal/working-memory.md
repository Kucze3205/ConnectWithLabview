# Execution working memory

## Considered
- Iteration 0094 startup documents read once: issue, orchestrator skill, loop state, capabilities, previous memory and startup diagnostics (`ok`, estimated 11,994 tokens).
- Loop state: iteration 0093 accepted/improved, one task; checkout identified by `.session/history/manifest.json` as `1d4e33205c9f206c32c700f48fa24bc017dba8af`. Read substantive result directly in `docs/research/poc/delivery.md`.
- Read `.github/loop/task-graph.md`, `docs/perpetua/roles.md`, `evaluation.md` and `operating-parameters.md`; live loop-state parameters supersede dated cadence statements.
- Read `benchmark/preparation-status.json`, `benchmark/protocol.md` and `benchmark/change-cases/README.md`. No files matched `benchmark/writing/**`. A combined-term Grep on protocol returned no matches; the subsequent full Read supplies evidence, not that search result.
- Earlier benchmark and POC details below are inherited pointers unless explicitly noted as read above; not a fresh audit of every linked result.

## State
- Bounded unsuccessful POC is delivered and iteration 0093 accepted. `docs/research/poc/delivery.md` accounts for missing changed VI, missing fresh-agent demonstration, unestablished semantics/version preservation and absent LabVIEW validation; it gives concrete blockers, two exits and owner reproduction instructions. This satisfies the permitted failure-delivery route, not POC success or proof of impossibility.
- POC code/evidence remain under `docs/research/poc/`; no product work is authorized. Eight selected VIs parsed, but no executable semantic edit was supported. Preserve the saved candidates rather than restarting open-ended reverse engineering.
- No session can run LabVIEW. If new controlled evidence later warrants another POC, the describing/editing session must receive a tool and an unseen VI without prior analysis of that VI.
- Benchmark preparation resumes without waiting for owner action. Existing protocol covers read fidelity, answers/source support, controlled-change analysis and paired reading comparisons, but does not explicitly specify creation/modification outcome accounting. Writing-method extension is the selected next useful work; it must build on existing method and change-case designs, not recreate the benchmark.
- `benchmark/preparation-status.json` records scoped reviewed designs, public development examples, zero native executions and unavailable native answers. Its review labels are not benchmark readiness; its long limitations text is more authoritative than shorthand milestone names. Do not change pinned status/index merely to claim writing coverage.
- Split allocator fix #446 still needs independent re-review according to inherited memory. Deferred this iteration to address the goal's explicit writing-method requirement. Before ordering re-review, locate and read actual #446 task/report and pin baseline/candidate trees via `.session/history/manifest.json`; do not infer its review status from stale preparation-status wording.
- Native capability #169 and substantive independent native oracles remain open because structural/public XML checks cannot establish runtime or diagram semantics. Read concrete paused evidence before deciding the next native work. Declined method assessment #430 (`not_planned`) must not be resubmitted unchanged.
- Product implementation remains deferred until independently checked benchmark method/evidence and owner method acceptance; writing implementation additionally needs writing-task coverage. No accepted goal gate exists; owner silence grants nothing.
- All-version effort/compatibility estimate remains open, inherited pointer `docs/research/0002-delivery.md`; writing coverage reportedly missing. Reconcile before choosing LabVIEW 2024 fallback; none selected.

## This iteration
- `.session/tasks.json` orders one benchmark task, `writing-method-extension`, default model/high effort, 120 minutes/65 turns, main, no dependencies, inputs or exports. One bounded authoring session keeps changes disjoint from pinned evidence and avoids premature parallel review.
- Expected gain: `benchmark/writing/README.md`, `method.json`, `verify_method.py` and compact committed verification evidence. Specifications cover creation and modification, independently established expected results, semantic/unrelated-content/save-version preservation, source/rebuild treatment, paired comparisons and honest missing-native outcomes.
- Existing protocol, change-case files, preparation index/status and reviewed evidence must remain byte-identical. No actual edit experiment, writer, product code, runner or evaluator implementation is ordered.
- Verification: `python3 -I benchmark/writing/verify_method.py`; offline/read-only rerun with positive and rejecting synthetic controls and asserted reasons. Passing means specification consistency only, never native or quality success.
- Next cold shaper: read the task report and actual new writing specification/verification evidence. If usable, order a separate reviewer session with exact accepted baseline/candidate trees, protocol and original evidence; do not let the author approve readiness. If incomplete, address the concrete omission without repeating a global gap inventory. Independent review is deliberately left to a later graph once pinned output exists.

## Tried, do not repeat
- #465/#468 established RSRC containers, BDHb decompression and entry framing; see POC README/comparison.json. Framing and endpoint pairs are not primitive semantics.
- #468's in-memory 103 -> 104 mutation was syntactic only; candidate-change.json records no written VI or LabVIEW test. Never treat it as Add-to-Subtract evidence.
- Iteration 0092 inspected eight fixtures and source slices; edit-readiness.md/json retain null recipe and semantic/type/BDPW/cache blockers. Resume only with new bounded evidence, not indiscriminate corpus searches.
- Iteration 0093 delivered the negative POC package. Do not repeat delivery or keep benchmark preparation paused for owner response. No changed VI was fabricated.
- Existing edit-readiness.json pins README/evidence hashes. Add separate documents rather than modifying those dependencies for navigation.
- Do not repeat global gap maps #282/#330/#400, lineage batches without allocation effect or store-readiness reviews without a concrete new question.
- Use path-specific Glob patterns; broad **/* previously truncated. Verification reruns lack LABVIEW_ENVIRONMENT, session artifacts and .session/report.md; rely on small committed evidence and one plain python3 command. Parent commits; no git commit or git-status acceptance requirement.
