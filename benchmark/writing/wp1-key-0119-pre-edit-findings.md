# Issue #577: evidence established before proposal edits

All four staged #574 input SHA256 pins matched on first inspection; all 45 review `/scoped_pins` match this checkout. No source discrepancy was found. Observed clean checkout: commit `3963123388e34ddfcad83daf81fd6facf8bf0529`, tree `35af29e3fecfe7fd42469f57a5ffce965d5d3f66`. The review actually inspected commit `16a825da7c7c72b93424f5449a08e86f513b0855`, tree `153b39cd1371f9c7652c75eca3edb8a7e6637dc1`; its intended identity differed, with equal scoped bytes.

The staged `574-wp1-key-review-0118.json#/findings/0` defines F3 as seven operative leaves mapped only to `R-scope,R-independent`. Each exact value and old mapping was compared with current method/0117 bytes. Proposed replacements follow the operative meanings of the existing rules:

| Exact locator in `benchmark/writing/method.json` | Proposed concrete rule links | Source meaning |
|---|---|---|
| `/common/artifact_fidelity_rule` | R-text, R-bytes, R-files, R-root, R-native, R-dimensions | Fixed semantics, unrelated bytes/files, source-version evidence, native maps for binaries and separate unavailable outcomes. WP1 remains text only. |
| `/tasks/4/requirements_mapping/W1/review` | R-text, R-files | Explicit changed project and complete output; explanation alone is insufficient. |
| `/tasks/4/requirements_mapping/W2/review` | R-preflight, R-native | Original hash/XML locator available; native locators and full eligibility unavailable. |
| `/tasks/4/requirements_mapping/W3/review` | R-text, R-bytes, R-files | Fixed IDs, exact one-byte allowance, no metadata or unrelated-content exception. |
| `/tasks/4/requirements_mapping/W4/review` | R-root, R-native | Preserved declaration supplies no native save-version evidence. |
| `/tasks/4/requirements_mapping/W5/review` | R-dimensions, R-limits, R-native | Separate text/native judgments; missing evidence earns no overall pass. |
| `/tasks/4/requirements_mapping/W8/review` | R-controls, R-native | Discriminating preparation controls; unavailable native/behavior evidence. |

F4 is `/findings/1`, an evidence-scope reservation, not a request to replay probes. Review `/F2/all_prescribed_ledgers` entries `C1-correct` and `C1-unverified-extra` retain the exact raw answers and original references (`wp1-key-review-0116.json#/c1_tests/cases/0/answer` and `/1/answer`). They cite the property/whole project and limits but supply no complete file-set/dependency, immutable-original or license preservation map. Method `/common/answer_rule`, `/tasks/4/request`, `/tasks/4/preservation`, `/tasks/4/output_manifest_rule`, `/tasks/4/trial_artifacts`, protocol L26–41 and README L54–62 require these obligations. Existing map tests expressly require required text/preservation coverage and complete inventories.

Proposed F4 disposition: keep those requirements and both independent dimension tests unchanged; prescribe map partial/partial on the explicit answers, retain unavailable sidecar evidence explicitly, and block use of `WP1-original-output-grounding` as an established key and the two affected example map slots until complete evidence and separate recheck. No unseen sidecars will be inferred. C1-correct therefore becomes partial/partial; unverified-extra remains unverified/partial by L41. The determinately incorrect wrong-citation, contradiction and native-overclaim prescriptions remain unchanged.

Historical Standards CLEAR / Spec NOT-CLEAR and session-specific cold/P1 provenance remain historical. This exposed author is not cold. F1 corrections, F2 relational interpretation and all unrelated mappings stay unchanged; no old checker, preserved audit or historical probe will execute.
