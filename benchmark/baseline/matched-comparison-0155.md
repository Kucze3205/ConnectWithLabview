# Matched with/without-tool comparison contract, 0155 (design only)

Status: design over SYNTHETIC data. No model, reader, evaluator or native run, no admissions, no scored results, no quality threshold. LabVIEW cannot be run in any session. The benchmark is not ready and tool quality is unmeasured. Machine-readable twin: [matched-comparison-0155.json](matched-comparison-0155.json); both files carry the same rules M01-M16 and open items O01-O06.

## Pins and reuse
- Ledger review #703 is CLEAR at HEAD 48f2715e05b9c212eaeb62b64e41b3846d846d90 (found in the staged export manifest). Ledger md SHA256 `8b2b30e63fd095dcdbc1aeb52ad14886d99035107a84fcd5183fb43119a35436`, json `74c9a47ab4966f79aec887f7bd72b1dd418cd8f0d9e9af13e6240baaf9690e6f`. Policy attempt-policy-0148 is CLEAR by #685.
- Reused and not edited: attempt-policy-0148, attempt-ledger-0150, runner-contract.md and the 0138 binding contract. The 0138 file was reached only through the 0148 text and was not reopened here (O06).

## Arms
`without-tool` (runner name `no-tool`), `with-tool` (runner `tool`) and optional `with-images`. The images arm exists only when native images exist for the case and the pinned model accepts images; otherwise it is recorded as unavailable, never dropped silently or replaced by text. Arm order per (case, repetition) pair is ascending sha256(`seed:pair_id:arm`) as in the runner contract; ties are rejected before dispatch. The runner does not yet know the images arm (O05). Only reader access and its minimal arm instruction may differ between arms.

## Matched fields (identical across arms)
Provider; model id and snapshot; effort and generation settings (temperature, max output, seeds where supported); prompt template hash; tool-free context (question, original artifacts as text, documentation, presentation order); token budget (total, output, context); wall-time budget; call budget (same ceiling value, the without-tool arm having zero available calls); environment pins (reader commit/config, tool schema, runner, scorer, split, key revisions, claim mapping). Tool output is not tool-free context and is recorded per attempt. All values are frozen in the manifest and plan hash before the first dispatch; later change is settings drift.

## Repetitions
Slots reuse the full tuple `record_id, case_id, pair_id, repetition_id, arm` joined by `slot_ref`, with the explicit 0138 per-arm repetition maps authoritative even when arms use different labels. 0138 supplies the mechanism only: one synthetic comparison, null independent repetitions per case/arm, no with-images slot (O06). This contract mints no repetition ids. Four paired development repetitions per case is a pilot allocation from 0148; the evaluation count is null (O04). One eligible attempt per slot.

## Stopping, mapped onto the ledger
| Condition | Ledger event | Terminal | answer_class |
|---|---|---|---|
| budget does not fit before dispatch | stop_recorded budget | stopped_budget | none (unstarted) |
| budget exhausted in attempt | usage_reconciled exhausted, stop_recorded budget | stopped_budget | exhausted / truncated, ineligible |
| external interruption | delivery_interpreted | `interrupted` alone never stops a plan (ledger R08). stopped_hard_failure only when a separate stop_recorded hard_evidence_failure exists; otherwise derived by the ledger order (hard_evidence_failure > settings_drift > budget, else finished_incomplete) | interrupted |
| (a) arm unavailable before dispatch (no native images, model rejects images) | none: unstarted slot, no dispatch, no delivery_interpreted | none by itself; pair stays incomplete and visible, terminal derived only at plan end | none (unstarted) |
| (b) dispatched attempt classed unsupported (e.g. tool cannot read the artifact family) | delivery_interpreted after dispatch and delivery_retained | finished_incomplete only as the plan-end derivation by the ledger order | unsupported, ineligible |
| settings drift | stop_recorded settings_drift | stopped_settings_drift | n/a |
| preflight blocked | preflight_result blocked | blocked_preflight | n/a |

The closed answer_class list of the ledger (12 values: ok, interrupted, unsupported, absent, empty, invalid_utf8, malformed, legacy_invalid, truncated, exhausted, error, failed_tool_call) is reused unchanged. No retry, no replacement, no resume; the first detected stop prevents all later dispatch. A case is comparable only when every mapped slot of every required arm closed attempted_eligible with answer_class ok; otherwise the pair is reported incomplete and stays visible.

## Cost and time
Taken only from ledger `usage_reconciled` (usage_known, actual tokens/time/calls, reserved_ref, delta, overrun, remaining_after, exhausted, cost). One charge per distinct attempt_id; redelivery never charges again. Cost is null without a verified price. Cost and time are reported per arm and per pair beside, not inside, quality results.

## Uncertainty and nondeterminism (stated before any comparison)
Fixed: model snapshot, prompt, settings and seeds where supported, budgets, case/repetition/arm order, scorer and key revisions, the uncertainty procedure, repetition count per stage. Reported as intervals: output variation across repetitions, the paired arm difference for correctness and for grounding separately, and cost/time differences. Procedure reused from 0148: 95% paired cluster percentile bootstrap, 10,000 resamples, seed 40502, resampling whole lineage/case/repetition/arm blocks; fewer than two complete independent lineages gives no inferential interval. Provider nondeterminism may remain despite fixed seeds and is recorded as a limitation, not removed by selection. No quality threshold is set; thresholds are an owner decision.

## Validation rules
- M01 Each run belongs to exactly one declared arm bound to the runner sha256 arm order; unknown arms or ordering ties reject the plan.
- M02 Any mismatch of a matched field between arms rejects the comparison for the affected cases; no after-the-fact normalisation.
- M03 Only reader access and its minimal arm instruction may differ; any other difference is an M02 mismatch.
- M04 Repetitions reuse the 0138 per-arm repetition mechanism only (one synthetic comparison, independent_repetitions_per_case_arm null, no with-images slot; no real repetition map exists and none is invented); new, missing or duplicated repetition ids reject the plan.
- M05 Exactly one attempt per slot counts; selection among multiple attempts after the fact (best, last, first successful, majority) is rejected and extra attempts make the slot unresolved.
- M06 Stopping uses only the ledger phases and terminals; the first stop prevents later dispatch; nothing resumes.
- M07 Budget exhaustion maps to stop_recorded budget and stopped_budget; an exhausted or truncated attempt is ineligible.
- M08 Interruption is answer_class interrupted, stays ineligible and is never replaced by a rerun.
- M09 (a) An arm unavailable before dispatch is an unstarted slot (no dispatch, no delivery_interpreted, no answer_class); (b) a dispatched attempt classed answer_class unsupported is ineligible; both stay visible and are neither dropped nor scored as wrong. `unsupported -> finished_incomplete` is only the plan-end derivation.
- M10 An incomplete pair (missing or ineligible slot in any required arm) prevents a completed comparison for that case.
- M11 Cost and time come only from usage_reconciled; cost is null without a verified price; budget overrun is reported.
- M12 The uncertainty procedure and the fixed-versus-interval split are frozen before any comparison; later change rejects the report.
- M13 No quality threshold, pass mark or ready verdict appears here or in records built on this contract.
- M14 All content is synthetic design; any claim of an executed run, real model call, native LabVIEW evidence or measured quality rejects the file.
- M15 Open items O01-O06 stay listed until an owner or independent reviewer resolves them; silent resolution rejects the file.
- M16 Matched values and environment pins are frozen in the manifest and plan hash before the first dispatch; drift maps to stopped_settings_drift.

## Open items (none resolved here)
- O01 Real-envelope authority: who may admit real provider, model and budget values; none admitted here.
- O02 F-A1 from attempt-ledger-0150 stays open.
- O03 F-A2 from attempt-ledger-0150 stays open.
- O04 Evaluation repetition count, run ceiling and precision targets are null owner decisions.
- O05 Provider-independence limits: matched model and settings do not make arms equal if the provider changes behaviour, updates snapshots silently or lacks seed support; the with-images arm is not in the runner and image support varies by provider.
- O06 The 0138 repetition maps were reused by reference via 0148 and not reopened; the reviewer should check them directly.

## Handoff
Independent review returns CLEAR or NOT-CLEAR on M01-M16 and O01-O06; the next shaper reads those. Not claimed: any run, benchmark readiness, tool quality.
