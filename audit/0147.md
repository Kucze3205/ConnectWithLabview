# Recovery/output publication audit 0147

Three initial runs reached successful results packing/upload and both epilogue downloads, then failed in the **Epilogue command step**; all three recovery runs succeeded. This supports a failure stage, not the underlying exception or a proven mechanism of output loss.

| Session | Initial run; failed Epilogue step UTC | Kick UTC → recovery run | Final artifacts |
| --- | --- | --- | ---: |
| #643 | 43652564966; Nov 14 23:34:25–23:34:48 (23 s) | Nov 15 00:30:08 → 43658484769 | 0 |
| #653 | 43663290752; Nov 15 01:42:25–01:42:47 (22 s) | Nov 15 06:59:29 → 43687899425 | 0 |
| #663 | 43694128074; Nov 15 08:39:11–08:39:26 (15 s) | Nov 15 14:32:53 → 43724956130 | 0 |
| #669 control | 43728358074; successful Epilogue Nov 15 15:22:29–15:25:06 | No kick observed | 12 |

Availability: seven Actions runs (each attempt 1), four report snapshots and records 0138/0141/0144/0146 downloaded; streams unavailable for all four sessions. [Normalized evidence](session-recovery-0147.json) retains each run/job/step pointer, outcome, timestamp, supported duration, availability entry and exact staged SHA-256; report snapshot identities are separate from wrapper hashes.

Reuse [0147's measurements](../policy/observations/0147-policy-check.md#recovery-discovery-and-audit-evidence), pinned to runtime `510fc5af213cbe9f66dde42a27e3467bc225afcd`: #643 first/later final checkpoints Nov 14 23:34:33 → Nov 15 00:33:13 (3,520 s); #653 Nov 15 01:42:29 → 07:02:51 (19,222 s); #663 Nov 15 08:39:14 → 14:35:51 (21,397 s). These persistence gaps are not agent-active time. Each first checkpoint already accepted Finish; later recovery rejected Finish for missing `.session/report.md`, then accepted report recreation. #669 has one checkpoint; its exact timestamp is absent from the reused observation.

The [checkout workflow](../.github/workflows/session.yml#L247) separates diagnostic streams from results and allows missing files without upload failure. Successful transport therefore does not establish package completeness. [Epilogue code](../.github/loop/loop.py#L903) explains admission/runtime-publication/finalization order only; historical workflow revisions are absent. The failing step also includes dependency installation and git identity setup. No staged traceback, failure annotation or package inventory locates the failing subcommand. All underlying causes remain **undetermined**.

Final records establish 0/0/0/12 artifacts, not exact publication times; workflow `updated_at` is not a measured completion event. Missing streams cannot distinguish expiry/pruning from non-upload. Null `outputs_asset` also occurs in #669 and proves no loss. Zero artifacts alone is not a general failure test. Report/artifact disappearance timing and original package contents remain unavailable; nothing was reconstructed.

Continuation-only model requests/tokens are unmeasured: aggregate session usage cannot establish the extra recovery consumption. Existing record `agent_s/gate_s/total_s/parked_s` values are preserved without relabeling them as lifetime timing. No quota or monetary inference. This environment audit measures no benchmark quality or readiness; benchmark coverage and acceptance gaps remain unchanged.

## What next

Policymaker: seek only existing failure annotations or short redacted tracebacks for initial Epilogue jobs **132628109954, 132660262717, 132754986114**, retaining their run IDs above. Expected gain: identify the failing phase before requesting a repair; check that each error identifies its exact run/job/subcommand. If expired, close this audit and propose only safe phase markers plus retained results-inventory hashes for engine-owned failure-path verification. No broad access or historical model rerun is justified.

Resume from [saved measurements](session-recovery-0147.json) and [normalizer](metrics/session_recovery_0147.py); do not repeat the history survey, reconstruct artifacts or replay evaluator/probe commands. Input hashes and source pins permit checking any newly supplied narrow evidence against this audit.