# F1 correction and saved regressions, iteration 0145

**Reproduced before correction:** the unchanged checker accepted detached attached-record model, common-prompt, original-input and tool-call content, reporting one complete synthetic comparison for each mutation and for their combination. Starting commit: `4d177993bf1ba87ff4a1cddc6d6d0fc70835eb23`. [Expectations](../.session/artifacts/attempt-evidence-f1-expectations-0145.json) preceded [pre-correction observations](../.session/artifacts/attempt-evidence-f1-pre-0145.json). Reports #663 and #659 were read; #663's ledger, script and variants were not uploaded (record 0144: zero artifacts), so these are fresh probes without reconstruction or replay of its successful probes.

**Corrected joins:** [attachment validation](verify_attempt_evidence_0143.py#L126) now requires model equality to the pinned manifest and returned-model content (line 139), common-prompt equality to the pinned hash/content (143), complete original-input kind/identity/hash equality (146), and canonical tool-call equality to the pinned tool inventory (150). These follow [0138 linkage](verify_project_run_binding_0138.py#L222), lines 222–246 and 265–285; legacy validation alone checks representation, not those equalities. Existing sidecar source-content validation (0143 line 230) remains intact. Completion uses the same strengthened attachment decision (lines 271–276), including when called directly with a consistent-envelope label; the grouping boundary is unchanged.

| Fresh variant | Before: decision / completions | After: decision / completions |
| --- | --- | --- |
| Attached model identity changed | pass / 1 | reject / 0 |
| Common-prompt hash changed | pass / 1 | reject / 0 |
| Original-input hash changed | pass / 1 | reject / 0 |
| Tool response content changed | pass / 1 | reject / 0 |
| All four contradictions together | pass / 1 | reject / 0 |
| Four contradictory attached records | pass / 0 | reject / 0 |
| Tool error | pass / 0 | reject / 0 |
| Unmodified consistent control | pass / 1 | pass / 1 |

The pinned plan has two slots: the literal four-record probe duplicates slots and was already incomplete. The combined four-join probe covers simultaneous contradictions without changing the plan. All rejections above are `legacy record mismatch`; [final observations](../.session/artifacts/attempt-evidence-f1-post-final-0145.json) retain byte inventories and all eight original fixtures. Failed attempts, absent versus zero-byte responses, unresolved multiple attempts, separate D1–D4 denominators, legacy schema/null reasons and all existing controls remain intact. No retry, selection or stopping policy is authorized.

`python3 -I benchmark/verify_attempt_evidence_f1_0145.py` exits 0: eight new cases, 92 existing saved controls and 60 retained grouping controls match. Counts derive from repository bytes at run time; no session artifacts are needed. [Saved execution](../.session/artifacts/attempt-evidence-f1-regression-0145.json). The first correction changed diagnostic counts for a missing common-prompt object; [failure and adjudication](../.session/artifacts/attempt-evidence-f1-adjudication-0145.json) preserve that correction defect, not a harness error. Binding attachments to pinned source values fixed it while unchanged evidence checks still reject missing/corrupt sidecar objects. No saved decision or accounting expectation was weakened or deleted.

## Changed files and SHA256

| File | Before | After |
| --- | --- | --- |
| `attempt-evidence-0143.md` | `a61bc54a41d9a66d65f202a8ad711f1d75848922e7da4ecf0fc86485353074eb` | `5d66520b202d01d48921cdd6bfc8146bc9692e4f7a62a0426f1b4a99d6adce79` |
| `attempt-evidence-0143.json` | `a8c4d2a1ee0e9bed311c5f002bd4a107ab4784fc9791f35625649ec25fad1a78` | `2489bf601856ddafc22315a67b0d076d316f793277e11e7e793261fba2e63651` |
| `verify_attempt_evidence_0143.py` | `582b5c27275d62c5fdaa1e948cc3bb7f08dfd2be8b282b86fbd2cd677480a799` | `f208c1f558537cb4dacaca6b2e60a4ebc5f133802c072d3697a823beb2cd7b98` |
| `verify_attempt_evidence_f1_0145.py` | absent | `fb5f3dba19625cfcd51ee2feaf68274c21d5a0aede98f390d74d554ea50f4af9` |
| `attempt-evidence-f1-0145.md` | absent | [final-byte SHA256 ledger](../.session/artifacts/attempt-evidence-f1-final-0145.json) |

This note's digest is external to avoid a self-referential hash; the ledger and session report provide every changed file's final digest. Original Markdown edits: expand attachment joins and diagnostic inventory meaning; make #659's three-file scope explicitly historical; name the current five-file follow-up scope. JSON edits are only `/contract/attempt_fields/legacy_record` and `/contract/accounting`; source pins, controls and expected accounting are untouched.

Expectations were authored after reading the review: no blind or model-unseen claim. Actual admissions, model/reader/native executions, scored runs, semantic passes and real comparisons remain zero; costs unavailable; `benchmark_ready=false`. This is an F1 correction, not method acceptance or a readiness verdict. Next: separate changed-scope review of exactly the five files above. Whole-method review and owner acceptance still precede product implementation; no owner request, index promotion, evaluator or historical builder invocation was made.
