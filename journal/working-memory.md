# Execution working memory

## Considered
- Iteration 0106 / #531: read issue, orchestrator skill, loop-state, capabilities, prior memory and startup diagnostics once. Startup ok (13,602 estimated tokens); no_progress=0; no open owner requests at startup; #525 cadence request now approved/completed. No accepted goal gate.
- Read history manifest (checkout 74e247484dd767ec25363e7d555768ae3434329c) and record 0105: #528 researcher done/accepted/improved/merged, commit bba00f7. No resume branch needed.
- Read docs/research/poc/pair/findings-0105.md, constant-1-separate--constant-2-separate.json and replay-0105-status.json. All eight runs exit 0, status measured, unchanged_inputs_after true; these are saved results, not shaper-recomputed hashes.
- Read .github/loop/task-graph.md, docs/perpetua/operating-parameters.md and accepted-limits.md. Single researcher task, default/high, bounded below role/policy ceilings; no sequencing change or product planning.
- NOT read by this shaper: candidates-0105.json, other comparison JSON, tool implementation, prepared sources, roles.md or evaluation.md. Earlier evidence below is inherited unless stated otherwise.
- History entry point: .session/history/manifest.json. Broker Glob needs the complete pattern; its path scoping has been unreliable.

## State
- Bounded unsuccessful POC delivered in accepted iteration 0093: docs/research/poc/delivery.md records missing changed VI/fresh-agent demonstration, unknown semantics/save-version preservation, absent LabVIEW validation, two exits and reproduction steps. Failure delivery is neither success nor impossibility.
- POC exit 1 resumed with the owner's eight public controlled VIs (#516). Replay #528 has now completed. Verdict: edit-attempt-needs-more, not edit-ready. Parser loaded LabVIEW 2026 fixtures; do not order the hypothetical loader-failure investigation from old memory.
- Findings localize constant BDHb insertion candidate 44200200 at decompressed 312 and value 01->02 at left 545/right 549, repeating across save modes. Candidate arithmetic transition 1a->1b remains unproven. Normal constant DFDS also changes; code/type/integrity handling is unresolved.
- Shaper-read separate constant JSON: BDHb, BDPW, HIST, LVSR and RTSG differ; DTHP/VCTP and front-panel heap are identical in that pair. BDPW chunk 0 is empty-MD5 bytes; chunks 1/2 differ. These observations do not identify safe patch rules.
- All eight comparisons show BDPW changes, including save-setting pairs with unchanged BDHb; BDHb-only derivation is unsupported. Encoding/length rules, integrity dependencies and unchanged-save control remain open. 0106 narrows source-grounded work to constants; do not restart general format discovery.
- .session/requests.json asks for one unchanged same-version Save As control from constant-1-separate.vi, plus authoring note. It is optional, public synthetic material only, and does not block the graph. Next shaper checks loop-state for the new request's assigned number/result; do not request the original eight fixtures again.
- No session can run LabVIEW. No native validity, behaviour, unbroken arrow or save-version preservation established. Raw LVSR 26008000 and vers/4 26118001 declarations in fixtures are distinct declarations, not native version authority.
- Original fixtures remain under docs/research/poc/pair/fixtures/ with pins.json and authoring.md (owner reports 2026 26.1.1f1 32-bit). Do not mix them with older WM1 evidence or convert to 2024.
- Pair tool/protocol from #509, independently reviewed by #513 at 8f5ae4c48581459aa09b3f5e56f79db56188b86c. Review preserved by #522 as docs/research/poc/pair/review-0102.json (SHA256 562467370d558b15eb9a7faf8cb1bc283365f99ef3c8cada9c6f54f1ead8249f) and review-0102-provenance.md; preservation thread closed.
- #513 minor R1 remains deferred: pair_diff.py --self-check rewrites tracked selfcheck.json. Do not run it. Fix only with a substantive tool change and re-review; the replay found no loader failure requiring such change.
- POC code stays under docs/research/poc/ with researcher, nothing under src/. A later fresh describing/editing session must receive tool and unseen VI without these analyses. No fresh session or edit is authorized by measured pair differences alone.
- POC exit 2 (source-grounded rules for BDPW, cache, DTHP/VCTP, ConstValue) remains open. 0106 determines whether existing prepared sources plus new pair evidence resolve a bounded part; unchanged prior source absences must be cited, not remeasured indefinitely.
- Benchmark preparation remains deferred while this concrete POC follow-up runs. If the source investigation ends at unavailable evidence and no new control is ready, return to benchmark work rather than waiting or repeating source absence. First read docs/perpetua/roles.md and evaluation.md.
- Inherited benchmark state: #481 W1-W8 synthetic writing extension, #485 corrected by #489 and independently closed by #493 (commit d3c697c375ed7dc880e55ab3cc2219577cd133a5, tree 689ed2757ca4eb413cd37dc4f0cfcbc2fa90ba14). Synthetic preparation proves no real edit/execution.
- Inherited writing baseline 486030b461e57ca0f322a17a5b7853e83e9655e3 / tree cf75cf6892de2f9410fa09ee2589dcba47d825a4; candidate 7435c05c4fd7ddbaafb6f5db9081ad5a4f5db427 / tree 555960a979f4bec474850a39bd9b284b7188496a. Re-pin/review if bytes change; investigate transcription before declaring drift.
- #497 closed #443 finding 1 at 8aefb1583265f097a8569d76b4f8e5a0b0782833 / tree 94c6df4711068611c1c2eb3f7f5b54d150c1ea78; do not repeat unchanged review.
- #501 effort estimates (33-99 vs 89-264 engineer-days) are reading-only and assume unverified 8.0-2025, not measured costs. No 2024 fallback selected; review deferred until a fallback proposal would use it. New fixtures are 2026, outside study range.
- #505 WM1 original @environment/actor-framework/Core/ActorFramework/Message Dequeuer/Equals Not A Refnum.vi declares raw 20008000 in vers IDs 4/7/8/9/10 and LVSR/0. Closed measurement, not NI save-version authority; replay docs/research/0100-wm1-version-evidence.py only for a new question.
- Native capability #169/grants and substantive independent native oracles remain open, availability unknown. Method request #430 declined/not_planned; do not resubmit unchanged.
- Prepared pylavi revision 35d2a0318f71dcb87bb9c431dc00700ee6b9fb75 is recorded in shaper-read replay output. Prior readiness: actor-framework 371c631c16155d88f02be11a953e4964d7452fd8; labview_ide/model_access not_checked, semantic_reading not_measured (inherited 0101).
- Writing prerequisites still include original-version authority/confirmed consumers, matched builders/sources, independent keys/checkers, restricted allocation/isolation and quota/precision decisions. Product needs independently reviewed method/evidence and explicit owner method acceptance; writing also needs accepted writing coverage. Merges and silence confer none.

## This iteration
- .session/tasks.json orders one task measure-constant-edit-rules, researcher/default/high, from main, 90 minutes/70 turns, no dependencies or historical artifact inputs. One bounded session avoids splitting intertwined heap/integrity evidence across workers.
- Expected outputs: docs/research/poc/pair/constant-rules-0106.md and .json, plus check_constant_rules_0106.py. Investigate candidate encoding and source-derived integrity rules; save probe provenance and negative results. No changed VI or tool changes.
- Verification: python3 docs/research/poc/pair/check_constant_rules_0106.py, over committed files only. It checks schema/input identities/probe consistency; prepared source hashes are recorded for provenance, not reread by engine.
- Next cold session: read record 0106 and task report, then constant-rules-0106.md Verdict and relevant JSON probes/source citations. Verdict rules-supported still does not prove native validity or authorize implementation. Read evidence before deciding on a bounded POC edit.
- If needs-evidence/source-blocked, identify exactly what was unavailable. Do not repeat unchanged source searches. If the optional Save As control arrives, verify original/control authoring and pins, then order the same read-only protocol comparison without refreshing original pins. Otherwise resume one ready benchmark preparation task after the required roles/evaluation reads.
- Optional owner request records exact unchanged Save As steps and explicitly keeps independent work running; no wait on owner or change to the goal.

## Tried, do not repeat
- #465/#468 established RSRC/BDHb framing; 103->104 mutation was in-memory only, no VI/native execution and no Add-to-Subtract evidence.
- 0092 inspected eight corpus fixtures (null recipe; semantic/type/BDPW/cache blockers); 0093 delivered negative POC. No fabricated output, corpus restart, repeated delivery or owner wait.
- #481/#485/#489/#493 completed synthetic writing sequence; old iter-0097/493-review-evidence.md pointer unverified.
- #443 allocator determinism/reordering/F3, #497 guard correction, #501 scope reconciliation and #505 WM1 declarations already measured.
- #509 preparation, #513 review, #518/#522 review preservation, #516 eight fixtures and #528 eight successful comparisons are complete. Resume saved JSON; never rerun pin creation or mutating self-check.
- #518 verification failed from a summary-derived eight-versus-nine probe count. Assert counts only after source read; historical inputs stage flat as .session/inputs/N-X and graph inputs are objects, not strings.
- Engine verification lacks LABVIEW_ENVIRONMENT, session artifacts and report.md. Parent commits; no git commit/status acceptance. One plain python3 command, no shell redirection/heredoc.
- Reviewer evidence belongs in .session/report.md and .session/artifacts/; permitted writer preserves exact pins when repository record is needed. Do not repeat probes to repair output-path mistakes.
- No global gap maps #282/#330/#400, lineage batches without allocation effect or store-readiness reviews without a new concrete question.
- Shaper empty Write erases files: use nonempty text and read required outputs back. Broker Grep no-match establishes no absence. Read .session/tasks.json and report before Finish.
