# WP1 independent review preservation

Issue #551 preserves the completed independent reviewer session **#547, iteration 0110**. This is preservation of historical evidence, not a repeated review or method integration.

## Artifact and report identity

- Original artifact: `project-text-review.json`; release: `iter-0110/547-project-text-review.json`; staged input: `.session/inputs/547-project-text-review.json`.
- Durable exact copy: [review-0110.json](review-0110.json), **74,366 bytes**, SHA256 `2dc007939a4b0637716027ef6e5a874702c9be7288daf80c3f007c07f382cdaf`. The staged bytes were hashed and verified before copying with `write_bytes`; no JSON reserialization or reconstruction occurred.
- Named #547 report snapshot: `d6eb2085115b86ba4e78c52b2307ddf0d700826dc74a4d31043d5e6f9d7303ef`. Its named `.session/history/sessions/547/<snapshot>.md` was absent; the current history manifest contains zero records/snapshots.
- Read the matching [repository report envelope](../../.github/loop/data/session-reports/547/ba754b9a0cc86b2d1cd17aa6287c05ad71696775c9e2c92a22f9db02415d6861.json), SHA256 `ba754b9a0cc86b2d1cd17aa6287c05ad71696775c9e2c92a22f9db02415d6861`. Its `report.issue` is 547 and `report.snapshot` equals the named snapshot. This envelope hash and the report snapshot are distinct identities; the unavailable Markdown was not reconstructed. The envelope records reviewer completion with no repository merge; routine task completion is not owner method acceptance.

## Git and scoped byte identity checks

The following pins come from the actual artifact's `/identities`; each commit's tree was independently resolved with `git rev-parse <commit>^{tree}` and matched exactly.

| Artifact identity | Commit | Tree |
| --- | --- | --- |
| Baseline | `8b93818c2779be00a2e267a3588eadcdaf665911` | `e5cdbf5a3bf02dce5de55e0b0cd3fc27bb744c31` |
| Accepted candidate | `e5165269b5625455ad17bf34a3a8d1be95ee362f` | `385ea919fc4f7714aa7bbdd29fd48ef60eaa74bb` |
| Full #544 task | `34cd2b3ae9277a3c163be16379c5286c328a05d0` | `87bf20af3c32808b66b400f1382fd271b766ed31` |
| Reviewed checkout | `668b9bedb30188100ab1c54e81436d674feea1a8` | `e9a20bf69df2e366a47a612da6a6d8c80c8eb2c0` |

Preservation checkout: commit `1bcbf896678af5c0b5398f691247f09421598e64`, tree `014fcbd67c3261016114e4451bdb563c30d254f5`.
For each of the five scoped paths, SHA256 of working bytes and `git show <commit>:<path>` bytes at accepted candidate, full #544 task and reviewed checkout matched the artifact's `/scoped_files` values. Sizes also match. **No scoped drift was found.**

| Scoped repository path | Bytes | SHA256 |
| --- | ---: | --- |
| `benchmark/project-text-writing-0109.md` | 11908 | `fd84b4d10a33fa2c32bb1b1f4a07cde5c35272620cdccd45599fd8dfbb21835e` |
| `benchmark/project-text-writing-0109.json` | 20557 | `74b6346cb646a8caa10a90462edee266832260d26c6f3685d7fd461cb56abdf8` |
| `benchmark/scripts/check_project_text_writing_0109.py` | 20719 | `35ab8c6725fb7affc7f38075f906c798f3278b5c894d812223df06425b120596` |
| `benchmark/project-text-writing-0109/verification.json` | 11943 | `71eadececba5619d8f4582b106e49a9ca137daeaff2773f13a56ba9d39596704` |
| `benchmark/real-project-0107/review-0108.json` | 75758 | `6ad9596c1c5e05f08ee3647ae3af1596f1882944e2397ac9efcd79383aa78894` |

Checkout differences from the reviewed commit are unrelated to these five paths: added frozen reports for #547/#549/#550, iteration records `iterations/0110.json` and `iterations/0111/tasks.json`, changed `journal/working-memory.md`, added `policy/observations/0111-review-and-cadence.md`, and changed `policy/working-memory.md`. Relative to accepted candidate, the #546 report and `iterations/0110/tasks.json` are also additions. Only their path/status listings were inspected; these checkout changes do not refresh or extend the historical review. Artifact-recorded historical input comparisons remain attributed to #547; they were not remeasured here.

## Preserved assessment and authority boundary

The artifact's overall recommendation is **CLEAR for proposal integration preparation only**: the pinned #544 WP1 proposal may inform a separately ordered bounded writing-method integration.

- **Standards: CLEAR**, no blocking findings. Scope, role separation, locality and historical integrity were accepted for the five-file preparation proposal; no evaluator verification or owner/product approval was issued.
- **Spec: CLEAR**, no blocking findings; **C1 remains Low and nonblocking** for proposal integration. The source/request text delta was independently confirmed for that review; complete future trial keys, native validity/semantics and benchmark readiness were not approved.
- **C1 — structured preparation consistency does not establish narrative truth.** See `/findings`, `/narrative_review` and `/independent_probe_summary`: #547 records four accepted false narrative counterexamples, including rehashed Markdown, while honest structured flags stayed unchanged. Its semantic review found no corresponding unsupported native/readiness assertion in the committed proposal. A checker pass establishes neither arbitrary narrative/native/isolation truth nor future agent-answer correctness. Later integration/trials still require independent semantic and claim review; any future answer scorer needs frozen answer, extra-claim, contradiction and citation-adjudication tests.

The original source/request evidence concerns the unique `Bld_version.build` text `2` to requested `3`, one byte at zero-based offset 3347, line 42. It does not establish native property semantics, actual build version or artifact save-version authority. Root `LVVersion` text is a separate declaration. The inherited #541 CLEAR and its C1 boundary remain historical evidence, not reissued approval.

All limitations in `/readiness_dimensions`, `/W1_W8_assessment` and `/later_integration_assessment` remain in force: text trial and native load/dependency/build/behavior observations are unexecuted; native semantics keys are unavailable; native save version and overall writing are unverified. Complete independently approved text/preservation/answer keys and full-native eligibility remain missing. Public original and derivative belong to one Actor Framework development lineage, never withheld/unseen evidence. Restricted whole-lineage allocation and executed allowed/denied/leakage checks are not established. Actual matched budgets/model/settings/repetitions/quota/arm order, fresh-session/workspace isolation, raw complete artifacts and failure accounting remain prerequisites; four proposed pilot repeats are conditional design, not executed evidence or resolved evaluation allocation.

## Later integration requirements

Use a **new integration provenance addendum and pins**, preserve this exact review/hash, and obtain **separate independent review of the changed integration tree**. The five contemplated integration files are `benchmark/writing/{method.json,README.md,verify_method.py,controls.json,verification.json}`. Historical `input-pins.json`, `review-corrections.json`, #541 evidence, original/license bytes and preparation-index entries must retain their historical identities.

The frozen #544 checker pins those writing-method inputs. Legitimate later integration will intentionally invalidate its current-input hash checks. Historical checker/input hashes remain evidence **at their pinned tree**; do not refresh them to make the historical checker pass on a changed integration tree. A new addendum and the separately ordered method verifier changes must validate that changed tree. Extend the explicit inventory and distinct project-text controls; synthetic graph controls provide no native XML measurement. WP1 remains narrow public-development text preparation, with direct creation, LVLIB, other projects/properties and untested families/versions uncovered.

Before either trial arm, independently freeze every text/preservation/answer key, exact prompt, manifests, dependencies, allowed inputs, documentation/key revision and preparer/checker agreement. Owner acceptance of the independently checked method and evidence is explicitly required before product work; readiness, thresholds and goal decisions remain owner decisions. Executable evaluator changes additionally require Policymaker order and the protected evaluator-verifier. Preservation grants none of those approvals.

This session performs identity/preservation checks only: no #547/#541/#493 probe replay, native work, trial, project source edit, method/checker/evidence refresh, preparation-index edit or readiness promotion. Only this provenance and the exact new review copy are repository additions. Durable hash/JSON/provenance-presence checks passed, and `git diff --check` against the preservation start commit passed. The parent checkpoints accepted writes, so repository change scope is checked against start commit `1bcbf896678af5c0b5398f691247f09421598e64` rather than by expecting untracked files: exactly the two authorized additions were present. The preparation-index check (`python3 policy/evaluator/evaluate.py --check`) exited 0 with no errors, 80 evidence references, `benchmark_executed: false` and `benchmark_ready: false`. Existing frozen checker outputs and counts are retained as historical evidence rather than new test results.
