# Recovery/output publication audit 0147

Three initial workflows failed specifically in **Epilogue**, after successful result packing, result upload and both epilogue downloads; the internal exception and point of output loss remain **undetermined**. Later workflows succeeded but final records contain zero artifacts. This supports an epilogue failure finding, not an upload-loss root cause.

Availability: Actions 2/2/2/1 runs and reports 1/1/1/1 for #643/#653/#663/#669; records 0138/0141/0144/0146 downloaded; streams unavailable for all four. [Normalized evidence](session-recovery-0147.json) records every selector, exact staged SHA256 under `sources`, report snapshot identities, runtime blob hashes, job/step pointers and supported durations. Manifest SHA256: `9090ae6d4f1cb2664794b4ea7ecb17722d077f63dbd612dc3e67ed09e112d8e5`.

All times below are UTC; dates are November 2026. Each distinct run has attempt 1. Full workflow, job, runtime-step, packing, upload/download and epilogue timestamps/outcomes are in `sessions.<issue>.runs`; these rows show the observed failure/recovery boundary.

| Session / run | Epilogue step start–end | Outcome | Final checkpoint publication |
| --- | --- | --- | --- |
| #643 / 43652564966 | 14 23:34:25–23:34:48 | failure | 14 23:34:33 |
| #643 / 43658484769 | 15 00:33:10–00:35:34 | success | 15 00:33:13 |
| #653 / 43663290752 | 15 01:42:25–01:42:47 | failure | 15 01:42:29 |
| #653 / 43687899425 | 15 07:02:47–07:06:04 | success | 15 07:02:51 |
| #663 / 43694128074 | 15 08:39:11–08:39:26 | failure | 15 08:39:14 |
| #663 / 43724956130 | 15 14:35:48–14:38:02 | success | 15 14:35:51 |
| #669 / 43728358074 | 15 15:22:29–15:25:06 | success | 15 15:22:35 |

Checkpoint times fall inside epilogue: they date continuation publication, not the original Finish execution. Reused [policy measurements](../policy/observations/0147-policy-check.md#recovery-discovery-and-audit-evidence) match git checkpoint pins in `sessions.*.checkpoint`; final runtime pin is `510fc5af213cbe9f66dde42a27e3467bc225afcd`. First-to-later checkpoint gaps are 3,520/19,222/21,397 seconds, **not agent-active time**.

Reports record kicks at 15 00:30:08 / 06:59:29 / 14:32:53, respectively 3,317/18,998/21,205 seconds after initial workflow `updated_at`; each recovery run was created six seconds after its kick. Why the watchdog waited is unmeasured: no intervening watchdog/commitment trace is staged. Final records reuse `agent_s` 19/17/18 (control 576), `total_s` 46/52/44 (606), and zero gate/parked seconds; these fields do not account for the checkpoint gaps.

Each affected runtime has an accepted original Finish, then exactly three appended actions: Finish rejected for missing `.session/report.md`, report Write, accepted Finish. Prefix-equal checkpoint histories and cumulative counters attribute **three extra Claude requests each**: #643 tokens in/out/cache-read/cache-write = 6/1,819/219,762/112,061; #653 = 6/1,674/295,926/149,937; #663 = 6/2,050/251,292/127,944. Codex deltas are zero. Total: nine requests, 18 input and 5,543 output tokens, with cache counters kept separate; no quota or monetary inference.

Control #669 has one checkpoint, no recorded kick, and 12 artifacts in both record and published report manifest; all four runtime `outputs_asset` fields are null. Neither null nor zero artifacts alone diagnoses failure. Exact publication instants and any historical partial uploads are unavailable; iteration closure is not substituted for publication time.

The [workflow](../.github/workflows/session.yml#L247) distinguishes diagnostic stream upload, results upload and release publication. Current [epilogue source](../.github/loop/loop.py#L903) publishes runtime state before finalize; [finalize](../.github/loop/loop.py#L745) separately publishes the report and [artifacts](../.github/loop/loop.py#L356). This is consistent with a durable terminal checkpoint and unfinished finalization, but does not identify the failing historical statement. Successful transport steps do not establish complete packaged/admitted output contents.

## What next

Policymaker's smallest next action: request only the retained **Epilogue step error tail and executed engine revision** for initial runs 43652564966 (job 132628109954), 43663290752 (132660262717), and 43694128074 (132754986114). Expected gain: identify the failing finalization statement; check matching run/job identity and exception against the executed revision before requesting a repair. If unavailable, close this historical cause as undetermined; do not extend this iteration or seek broad private access/spending.

Saved work: [measuring script](metrics/session_recovery_0147.py) and normalized evidence preserve availability, hashes, timelines and attributable deltas. Next cold session should consume those outputs and only newly supplied bounded logs; avoid repeating the history survey, reconstructing missing artifacts or replaying historical probes. Missing coverage comprises original results bytes/per-file boundary manifests, within-epilogue logs, watchdog trace and historical publication events. Benchmark readiness and product quality remain unmeasured.
