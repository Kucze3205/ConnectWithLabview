# Iteration 0132: task graph failure and recovery

## Finding before correction

Policymaker #620 considers history records 0129–0131, the trusted reports #611/#612/#615/#617 and #501, and current execution memory. Startup diagnostic: 16,468 estimated tokens, status ok, no notices. Exports manifest has no results. No suggestions are pending.

Iteration 0131 failed before any worker started. The shaper #617 completed 33 actions and received an accepted Finish. Its report says a review was shaped, but the engine appended “`.session/tasks.json` is missing or not JSON”. The graph was present and invalid, not missing.

Evidence: runtime checkpoint `a2dcfe9:sessions/617.json` (origin/loop-runtime at investigation); history record `.session/history/records/0131.json`; [trusted #617 report](https://github.com/Kucze3205/ConnectWithLabview/issues/617#issuecomment-6875982083), prepared snapshot `94eaf4fd02ccc3fd338eb2617e617ceb364758c3d7472c7443b0ab2b28e8ee7f`.

Selected runtime actions:

| Action | Observed result |
|---|---|
| 13 Write tasks.json | Valid JSON, one researcher task; parsed body has 16 actual newlines and zero literal backslash-n sequences. |
| 21 Write tasks.json | Replaced the draft with a reviewer task. JSON parser fails: line 14, column 3156, character 3594. |
| 26 Edit tasks.json | Changed a budget sentence; did not repair the syntax. |
| 31 Read tasks.json | Returned the same malformed JSON; parser fails at the same location. |
| 33 Finish done | Accepted; later engine parsing failed the iteration. |

The replacement embeds `python3 -c "import ..."` inside the graph's JSON body without escaping the command quotes for that inner JSON string. A successful Write and visual read-back establish saved text, not JSON validity. `.github/loop/loop.py` lines 1071–1083 parse the graph after Finish; `.github/loop/tool_broker.py` checks the report on Finish and does not certify the graph. No engine defect or resource failure is established by this case.

## Small correction and expected check

Changes are limited to `execution/profiles.yml`, `execution/roles/orchestrator/SKILL.md` and policy memory/evidence. The shaper gains the already permitted `Bash(python3:*)` tool. Its skill restricts Python use to local graph serialization/validation and still forbids doing worker verification or product/benchmark work.

After its final edit the shaper must parse tasks.json and check actual required heading lines using the exact direct Python command saved in the skill. Every later graph edit requires another check. The skill explains both JSON string layers and adds a temporary recovery note: rebuild the independent #501 study review, export #501 explicitly, and do not duplicate the discarded estimate or pending requests. The Policymaker removes this note after admission and result accounting.

Expected gain: prevent this demonstrated syntax/heading failure before an iteration is lost. Next applicable observation: actual successful validation after the final graph edit, engine admission, and the resulting reviewer report. This session does not establish future role activation or engine admission. The validator is not a complete task schema or semantic check.

Verification performed once, exit 0: extracted the exact command from the modified skill with shlex, compiled it, and ran its code against historical graph text through an in-memory file replacement. It accepted action 13, rejected malformed action 21, rejected malformed read-back 31, and rejected a valid JSON control whose body used literal backslash-n sequences. No historical task command or benchmark checker ran. PyYAML parsed the candidate profiles and confirmed that the only profile difference from baseline `157c74e` is the shaper Python tool.

## Execution results considered

- Record 0129 closed accepted/improved. #611 added the local-B N08 F1 overlay. [#612 review](https://github.com/Kucze3205/ConnectWithLabview/issues/612#issuecomment-6873712778) is Standards CLEAR / Spec CLEAR for that pinned correction only. Its report records 19 measured pins and one checker execution. This Policymaker did not repeat its semantic review or remeasure its protected sources. Initial inability atoms, separate correctness/grounding, historical interpretations and broader blocks remain preserved.
- Record 0130 closed accepted/improved. [#615 report](https://github.com/Kucze3205/ConnectWithLabview/issues/615#issuecomment-6873880258) records the human C1 entry point, preserved #612 artifact identity and packaging-only verification. Actual human C1 remains missing. No further packaging or agent substitute is ordered.
- Record 0131 failed, zero workers, no improvement; its intended reviewer has no partial branch to resume. Reconstruct the graph from the saved plan rather than repeat shaper investigation. Owner request #618 was opened; #532 remains optional/pending. Neither request blocks ready work.
- Current execution journal is a saved plan, not evidence that the 0131 review ran. With a shaper, policy orders may name only policy-only roles. Empty orders are deliberate; the shaper owns the ready research review. No evaluator defect or new answerable audit question calls for another policy task.

## Discovery: #501 already includes writing

Read both the [#501 report](https://github.com/Kucze3205/ConnectWithLabview/issues/501#issuecomment-6842657209) and [the study](../../docs/research/0099-writing-version-effort.md). Policy memory's description of #501 as reading-only was wrong. The study covers creation/modification/rebuild, preservation, artifact families and incremental writing costs; only inherited 0002 day ranges omit writing. Unknown writing costs remain explicit. No full-goal ratio or fallback is supported. Independent assessment against the current goal and later WM1/project-edit evidence remains ready. Do not create another estimate from the old shorthand.

## Limits

No routing, cadence, turn cap, evaluator, goal or owner-controlled contract change. One malformed graph does not establish model-quality or normalized quota differences. Record 0131 reports Codex only, 1,447,131 input and 10,660 output tokens; those are not subscription-quota measurements. #611/#612 were the same family; #615 was mixed Claude/Codex. No new quota-savings or independence claim.

Read evaluation.md, accepted-limits.md and operating-parameters.md before deciding. No private-data use, disclosure, publication category, spending, native task, capability request or duplicate Owner request. Missing human C1, native keys/behavior/save-version proof, dependency coverage, restricted evaluation isolation, matched trials, independent method review and owner acceptance remain explicit. Benchmark readiness is false; product quality is unmeasured. No 2024 fallback or Goal gate is accepted.
