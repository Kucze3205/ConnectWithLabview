# Policy check 0148 — session #680

## Decision and scope

Retain the shaper, profiles, routing, limits, cadence and evaluator. Add one continuation rule to policy/roles/policymaker/SKILL.md: check consumed orders and completed results before restoring a saved graph. Submit no policy tasks (`wake=false`, `tasks=[]`). Ordinary work remains shaper-owned. No Owner request, evaluator change or engine-change proposal.

Expected gain: prevent another audit of an already answered question after policy continuation. Check the next applicable continuation against its recorded tasks, available reports and submitted graph. This session applies the rule by consuming #675 and returning an empty graph. This is an observed decision, not measured quota savings or proof against future engine failures.

Starting HEAD bf9f556279e44575f19aa77aeb623d11124607a5; tree 27c9830f98d92a0d725471c9c9b114e5244d85a2. Startup documents read once: estimate 15,361 tokens, status ok, no notices. Startup memory: 14,180 bytes, SHA256 ba45c229ab6e3a3052b2ccd2fd4bea96986e89a446c7ed448d7f2f5f521b502e; recover from starting HEAD. Original Policymaker skill: 6,580 bytes, SHA256 a970a37d5dd4b8e93e68aebb251d43db571e8cc47a99a25e54b7c830ca69da9d. Read operating-parameters.md for recovery/resource boundaries; do not change owner safeguards.

Measurements here: selected iteration/report fields, local SHA256 and equality to named producer git blobs. No historical workload, benchmark checker, evaluator, reader, native execution or model trial was replayed. Audit findings and worker tests below remain report-attributed, not independently reproduced. Current exports manifest has results=[]; no new exception logs or worker artifacts are staged through it. This does not prove logs or artifacts do not exist elsewhere. A path-limited Glob returned repository-wide output; selected pathlib reads replaced it. No broad content survey followed.

## Repeated policy orders

[Iteration 0147](../../.session/history/records/0147.json), 57,061 bytes, SHA256 40b173954cc33133e4f15da6c1f00626017b462cd77138608113caeada6825f1, records five policy passes and four recovery-audit orders:

| Policy pass | Task issue | Recorded outcome | Turns | Input tokens | Output tokens | Cache-read tokens |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| 1 | 672 | done, merged | 25 | 1,052,596 | 11,348 | 973,440 |
| 2 | 673 | done, merged | 25 | 1,401,947 | 10,515 | 1,315,456 |
| 3 | 674 | done, merged | 28 | 1,397,379 | 9,585 | 1,318,272 |
| 4 | 675 | done, merged | 26 | 1,331,680 | 13,273 | 1,248,256 |

All four orders use the same historical sessions/control, source selectors, output paths and recovery question. Wording changes in later orders do not identify a new evidence question. Reports #672–#675 all locate initial failures at Epilogue and leave the underlying cause unknown. Later reports vary in details and attribution, so the current #675 measurements are the continuation source; they are not four independent confirmations. The three later audits record 79 turns, 4,131,006 input, 33,373 output and 3,881,984 cache-read tokens. These counters measure recorded work, not normalized subscription quota or recoverable financial cost.

Selected #671 report snapshots show passes 2–4 restoring missing session outputs and repeating the audit order. [Pass 2](../../.session/history/sessions/671/df612bd110675226a6350ec0a36d2d557f5e0043c8012f38fce4061617143d8a.md) explicitly says it restored the missing audit order; [pass 3](../../.session/history/sessions/671/dd28044865fef50c47220a8085a02cdb8c6e082afac6edf1681fc0db46316d1e.md) and [pass 4](../../.session/history/sessions/671/1ea90f93d95ff7380d524801349000583876cf7374207a4451fd350595903234.md) repeat the same next action. Its final snapshot is partial/input_budget; it does not show consideration of completed audits. This supports correcting policy continuation behavior. It does not establish the engine's file-loss mechanism or prove why each continuation restored files.

[policy/observations/0147-session-outputs.json](0147-session-outputs.json) is retained as historical evidence. Its audit graph is consumed and must not be restored as pending work. The new skill rule supersedes its restoration advice. No engine idempotency guarantee is inferred.

## Recovery audit disposition

Consumed [audit #675](../../.session/history/sessions/675/ee394c9aea41fd86193bc3fbc6616a2af6fee4166cec26cd571216d1fa60b762.md), accepted audit commit d0cf5005c6bf38d776155d691dbcf64864b6b6bb. Measured current files:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| audit/0147.md and identical audit/latest.md | 5711 each | f22224cd09cc690af25bd9ac57150b1147f931b7056fdf3a42fbf9e5b776c542 |
| audit/session-recovery-0147.json | 110375 | 7b397d387302f1a6eca86db8edb58e32ccb04a5760741ec11339cf42b81a6f76 |
| audit/metrics/session_recovery_0147.py | 20682 | c437cdbc43fdc7be7317da7bfbfe9022c07abc57caf6f0f817e08b3301e8fd1c |

The [audit](../../audit/0147.md) reports seven downloaded Actions metadata exports, four reports, four records and four unavailable streams. Three initial workflows failed in Epilogue after metadata-successful routing, packing/upload/download. Recovery workflows and control #669 succeeded. Affected final inventories are zero; control has 12 artifacts. Null outputs_asset occurs in all four and is not diagnostic. Original archive contents, historical exception/stderr, executed source revisions, watchdog decisions and loss/publication transitions remain missing.

Its runtime pin is 510fc5af213cbe9f66dde42a27e3467bc225afcd. First-to-later checkpoint gaps are 3,520 / 19,222 / 21,397 seconds, not agent-active time. Verified three-action continuations report output-counter deltas 1,819 / 1,674 / 2,050; these are not subscription-quota measurements. No failing internal function or transport fix follows from this evidence.

Close the historical audit at this Epilogue-step evidence boundary. Do not order another general audit or hold this iteration for logs. Reopen attribution only when retained, redacted exception/phase evidence is newly staged for runs/jobs 43652564966/132628109954, 43663290752/132660262717, 43694128074/132754986114. Verify run, job, attempt, timestamp and excerpt hash first. No optional access proposal is needed for the present decision. Before any later private-access proposal, read accepted-limits.md and use capability/readiness; keep independent work running. A future engine diagnostic proposal needs a concrete patch and isolated synthetic success/interruption verification, not a guessed repair or benchmark replay.

## F2 closure and execution graph

[Correction #677](../../.session/history/sessions/677/ad9d2d76efdc72398d90a7421f08f4ba5747cbcf7f88e40d0febb3bd91995272.md) is done/accepted/merged at e15a503340c615ad37f576de9ba5aceb99b42495, tree 607c255a8b091b0ab7932e9da9115dee7e6224c4. [Review #678](../../.session/history/sessions/678/20ebdbceff1d6d26d652559471fd83d531cffc162b6d1ac8105f01c22080d0b2.md) gives Spec CLEAR and no documented Standards violation for this narrow correction. Current bytes equal the named producer blobs and the review's hashes:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| benchmark/verify_attempt_evidence_0143.py | 23496 | 6b14d20fea17acc580f30e7da0a7218e0b2b7579516f9396a0facf0a2028ab6a |
| benchmark/verify_attempt_evidence_f2_0147.py | 9342 | e510915bcad307400a7f948dd97b9874e6dac6ef91986fe39ca612a664a62deb |
| benchmark/attempt-evidence-f2-0147.md | 5584 | c1c2abccbd315457d41255c34e3e77b2c8976eebbfb3a48914a21aaff57dd483 |

#678 reports 32 integrity checks, four independent cases without mismatch, and one repository regression. Each agreed unplanned arm rejects, returns invalid attachment, retains 48 payloads/50,016 bytes and completes zero, including direct consistent=True. The positive completes one synthetic comparison. Nested compatibility reports eight F1, 92 saved and 60 grouping controls; the closed 41-case suite was not replayed. These are worker-reported checks, not new policy execution.

Record0147 confirms four producer and seven reviewer artifacts. This session did not stage or inspect their bytes; their artifact hashes remain report-attributed. Review expectations preceded correction-code/results inspection according to the report. Task disclosure, inherited exposure and the same actual Codex family preclude blindness or different-family independence claims. A post-expectation inspection printed nested hex and was truncated; this budget error is reported, not evidence of an outcome mismatch. Close #669 F2 only; this is not whole-method approval.

Shaper #676 used one graph containing correction #677 and reviewer #678 with the correct dependency and explicit producer artifact inputs. This meets #671's structural expectation and avoids a separate shaping session for this pair. Quota savings and causality remain unmeasured.

## Continuation boundaries

Benchmark_ready=false. Product quality is unmeasured. Artifact/version/hardware coverage, human C1/agreement, trusted native/dependency evidence, isolation, matched real comparisons, independent whole-method review and owner acceptance remain missing. No accepted Goal gate, no product authorization, no 2024 fallback selection. The negative POC remains delivered; no new native evidence is claimed.

Next cold session: use updated working memory, #675's pinned audit and #678's scoped closure. Review the shaper's next ready work rather than repeating F2/grouping checks. Read exact sources only for a concrete contradiction. Do not restore the consumed 0147 graph, reconstruct lost artifacts, repeat the audit, reopen declined C1 or infer readiness from accepted merges and green synthetic checks.
