# Recovery and publication audit 0147

3/3 original workflows failed in **Epilogue**, after successful routed-session, result packing, results upload and both epilogue downloads; 3/3 recovery workflows succeeded. #669 passed the same chain and published 12 artifacts.

| Session | Run identity / workflow outcome (attempt 1 each) | Checkpoint gap s | Published artifacts | Saved agent/gate/total/parked s |
| --- | --- | ---: | ---: | --- |
| #643 | 43652564966 failure, 43658484769 success | 3520 | 0 | 19/0/46/0 |
| #653 | 43663290752 failure, 43687899425 success | 19222 | 0 | 17/0/52/0 |
| #663 | 43694128074 failure, 43724956130 success | 21397 | 0 | 18/0/44/0 |
| #669 | 43728358074 success | single checkpoint | 12 | 576/0/606/0 |

Checkpoint gaps reuse [policy measurements](../policy/observations/0147-policy-check.md#recovery-discovery-and-audit-evidence), not agent-active time. Their first checkpoint timestamps fall inside the failed Epilogue steps; they are not exact Finish execution times. Short saved runtimes are preserved as recorded, not lifetime work measurements.
The [detailed timelines, exact run/job/step pointers, source SHA256 values and runtime projections](session-recovery-0147.json) retain all seven runs. Runtime pin: `510fc5af213cbe9f66dde42a27e3467bc225afcd`; source-code inspection describes the audit checkout, without asserting every historical run used those bytes.
Each affected session already had an accepted Finish, then later received “Use Write to create .session/report.md before Finish”, wrote the report and finished again. Reports record one kick each at 00:30:08, 06:59:29 and 14:32:53 UTC on November 15. Recovery published reports but zero artifacts; #663's saved 21-artifact command result is not recovered bytes.
**Root causes remain undetermined.** Metadata locates failure at the Epilogue step, not a Python function or the point files disappeared. Successful upload/download steps establish workflow outcomes, not complete bundle contents or successful admission. Missing logs/bundles prevent distinguishing admission, finalization and other exceptions.
All four streams are unavailable (retention, expiry and never-uploaded remain alternatives). `outputs_asset=null` occurs in all four runtime records, including #669; neither null nor zero artifacts alone diagnoses failure. Watchdog commitments are a possible delay mechanism, without historical decision evidence.
Continuation-only tokens are **unmeasured**; saved usage is cumulative. Tokens measure neither subscription quota nor money. No evaluator, historical command, benchmark probe, model/reader/native execution or artifact reconstruction was run.
**Smallest next action:** Policymaker should obtain only failed job `132628109954`'s Epilogue exception/log, if retained. Expected gain: locate one exception before considering an engine change. Verify its run/job identity, byte hash and last completed receive/finalize boundary; if unavailable, close historical attribution at the step-level limit and capture that boundary plus inventory on a future occurrence.
Benchmark_ready=false; missing benchmark coverage, whole-method review and owner acceptance remain unchanged. Product quality is unmeasured. This audit measures recovery only.
