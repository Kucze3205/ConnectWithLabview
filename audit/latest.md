# Recovery and output publication audit 0147

Three of three affected initial runs failed in the **Epilogue step** after successful routed-session, packing, result-upload and both epilogue-download steps; all three recovery runs and control #669 succeeded. Root cause of missing files remains **undetermined**. Metadata does not expose the failed exception or archive contents.

| Session | Actions runs (initial, recovery) | First accepted Finish checkpoint UTC | Later checkpoint UTC | Gap s | Published artifacts | Saved agent/gate/total/parked s |
| --- | --- | --- | --- | ---: | ---: | --- |
| #643 | 43652564966, 43658484769 | 2026-11-14T23:34:33Z | 2026-11-15T00:33:13Z | 3520 | 0 | 19/0/46/0 |
| #653 | 43663290752, 43687899425 | 2026-11-15T01:42:29Z | 2026-11-15T07:02:51Z | 19222 | 0 | 17/0/52/0 |
| #663 | 43694128074, 43724956130 | 2026-11-15T08:39:14Z | 2026-11-15T14:35:51Z | 21397 | 0 | 18/0/44/0 |
| #669 | 43728358074 | 2026-11-15T15:22:35Z | none | — | 12 | 576/0/606/0 |

Checkpoint times are commit/publication times, not exact Finish times. The 3,520/19,222/21,397-second gaps are elapsed time, never agent-active time. Saved record timings are reused unchanged and largely describe recovery; they do not measure the original invocation or full recovery gap. Full per-run job/step timestamps, zero-based source pointers and paired durations are in [the evidence JSON](session-recovery-0147.json) under `sessions.N.timeline`, `runs` and `durations`.

Each affected first checkpoint already contains an accepted Finish and final result. The later history preserves that complete prefix and adds exactly: Finish rejected with `Use Write to create .session/report.md before Finish`; Write report; accepted Finish. Reports record one kick at 00:30:08 / 06:59:29 / 14:32:53 UTC. Exact file-loss, publication and watchdog transitions are unavailable. #669 has one checkpoint, no kick, successful Epilogue and 12 recorded artifacts. All four `outputs_asset` values are null: null and zero artifacts alone cannot diagnose failure. Workflow transfer artifacts and published session artifacts are different inventories.

| Continuation | Input counter delta | Output counter delta | Cache-read delta | Cache-write delta |
| --- | ---: | ---: | ---: | ---: |
| #643 | 6 | 1819 | 219762 | 112061 |
| #653 | 6 | 1674 | 295926 | 149937 |
| #663 | 6 | 2050 | 251292 | 127944 |

These are cumulative runtime-counter differences across the verified three-action extensions, all attributed to `claude/claude-sonnet-5-5`; Codex counters did not increase. They are not subscription-quota or monetary-cost measurements. No continuation is observed for #669. Recovery Routed-session steps lasted 20/17/18 s; control lasted 576 s. Different saved `agent_s` boundaries are retained, not substituted.

Availability: 7 Actions metadata exports, 4 report snapshots and 4 iteration records downloaded; all 4 streams unavailable. Each report-body hash matches its advertised snapshot. Exact byte hashes, record snapshot identifiers and runtime pins are in [sources](session-recovery-0147.json) (`sources`, `availability`, `runtime_pin`). [Measurement script](metrics/session_recovery_0147.py) selects only non-sensitive fields; staged inputs and named git objects are required to rerun it. No historical artifacts were reconstructed and no historical commands, evaluator, probes, reader, model or native executions were replayed.

Current-source boundary: [session.yml](../.github/workflows/session.yml) lines 247–307 separates diagnostic-stream upload, packing/results upload, downloads and the Epilogue step. Stream/results uploads ignore missing files, so metadata-success is not proof of payload contents. [loop.py](../.github/loop/loop.py) lines 903–947 receives results, publishes runtime state, then finalizes; lines 831–840 fetch the candidate and publish session artifacts. The observed checkpoint commits fall inside their respective Epilogue step intervals. This supports a durable continuation despite failed epilogue step, not a specific failing function. Exact historical source revisions and stderr are absent. The staged evidence establishes neither runner death, artifact-quota exhaustion, a receive/admission exception, provider limits nor watchdog deferral. Policy preserves #663's saved command result claiming 21 verified indexed artifacts; their bytes are unavailable, so that count is not a recovered inventory. [Policy measurements](../policy/observations/0147-policy-check.md) and [engine recovery contract](../docs/perpetua/engine.md) lines 301–307 are context, not proof of those explanations.

## What next

Policymaker: seek only retained, redacted Epilogue exception/phase logs for jobs **132628109954 / 132660262717 / 132754986114** in initial runs **43652564966 / 43663290752 / 43694128074**. Expected gain: identify the failed command phase/exception; verify run, job, attempt, timestamps and excerpt hashes before proposing a fix. If absent, close historical root-cause attribution at this precise step boundary; do not keep the iteration open for another general audit. Any future engine proposal should capture non-sensitive phase outcomes and file counts/digests at pack/receive/final-publication boundaries and verify them on isolated synthetic success/interruption cases. No engine change is made here. Resume from this JSON and pinned measurements; do not reconstruct lost artifacts or replay completed benchmark work.

This audit does not establish benchmark readiness or product quality. Missing real coverage, controlled comparisons, independent whole-method review and owner method acceptance remain explicit in policy evidence; product quality is unmeasured here.
