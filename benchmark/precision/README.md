# Development repetition, precision and quota plan

Design only. No run executed. No threshold proposed. No model calls, quota checks or development pilots have been performed. This plan closes the method-design item, not execution, acceptance or benchmark readiness.

[plan.json](plan.json) specifies four paired development repetitions per case/arm and candidate evaluation counts of 2, 4, 8, 16 or 32. The evaluation count remains null until development-only variance estimates, owner precision targets and verified existing quota support a frozen count. Four is a pilot design allocation, not a claim that variance can already be estimated adequately. Inadequate independent lineage groups or fit diagnostics block sizing. Repeats cannot compensate for missing independent projects.

For correctness and grounding separately, the descriptive estimand is tool minus no-tool required-item correctness fraction, averaged over repetitions, cases within lineage, then independent lineages. Full protocol outcome categories, extras, contradictions and case assessments remain mandatory; this fraction cannot override them. Reading fidelity is reported through separate required probes, with no-tool not applicable and no paired fidelity gain. Oracle tolerances and nondeterminism rules remain case-specific in all three dimensions.

The final uncertainty design uses a 95% paired cluster percentile bootstrap, 10,000 resamples, seed 40502. Resampling selects whole independent project/lineage groups and preserves their cases, repeats and paired arms. Fewer than two complete groups yields no inferential interval; small-group instability and unavailable scope must be disclosed. Missing arms are not imputed. Complete-pair estimates are conditional, retain coverage accounting and cannot establish a completed comparison; planned-weight worst-case bounds retain missing scope.

Pilot sizing uses development paired-difference between-lineage and repeat variance, with a normal planning approximation checked by development cluster resampling. Select the smallest candidate count meeting every owner-accepted paired dimension/stratum precision target within verified quota; otherwise report infeasibility. Freeze the pilot evidence, count, settings, ceiling and stopping rule before any evaluation request. No evaluation gains may influence sizing, exclusions or stopping.

## Manifest field matches

The plan's `manifest_fields` keys and explicit `manifest_field_matches` inventory match these existing names in [the read-only template](../baseline/run-manifest.template.json):

- `provider`
- `exact_model_snapshot`
- `snapshot_pinning_limitations_and_run_window`
- `model_image_capabilities`
- `independent_repetitions_per_case_arm`
- `sampling_order`
- `paired_arm_randomization`
- `stopping_rule`
- `affordable_run_ceiling`
- `precision_cost_plan_revision`
- `per_case_tolerances_and_nondeterminism`
- `uncertainty_procedure`
- `confidence_level`
- `resampling_seed_and_count`
- `independent_lineage_units_and_repeat_preservation`
- `missing_pair_treatment`
- `exclusions_and_aggregation_weights`
- `small_sample_and_unavailable_scope_reporting`
- `owner_precision_target_and_acceptance_record`

These are design records, not a populated executable manifest. The checker validates the names against the template; it does not change template null reasons. Arm ordering follows [the runner contract](../baseline/runner-contract.md): sha256(seed:pair_id:arm), with design seed 40501. See [protocol baseline](../protocol.md#baseline) for the governing matched-budget, isolation, outcome and uncertainty requirements.

## Quota: owner-decision

Candidate loop routes are `claude/claude-sonnet-5-5`, `codex/gpt-6.1-sol` and `codex/gpt-5.6-luna`. They are candidates supplied by the session/issue routing context, not verified service capabilities; `codex` names a loop adapter whose underlying account/interface still needs identification. Both arms need identical native panel/diagram images where available. Verify actual interface image support, limits, model identity, accounting, session isolation and permitted data routing/retention using development inputs before use.

Loop aliases do not establish immutable snapshot pinning. Record returned identifiers, available snapshot controls and seed support; disclose pinning limitations and freeze a bounded UTC run window if immutable pinning is unavailable. Do not claim exact reproducibility from an alias.

The exact owner decision is which existing subscription quota to allocate: select the route and underlying account/service/interface without credentials; approve data recipients/retention; specify remaining units, renewal/run window, rate limits and a hard ceiling covering pilots, paired runs, separate probes, retries and reserve. Confirm no extra spending. After development costs are measured, accept the affordable repetition plan or leave evaluation blocked. No allocation or additional spending is authorized here.

## Check and next step

Run `python3 -I -B benchmark/scripts/precision_plan.py --check`. The stdlib checker reads only the plan and manifest template, writes no files and exercises eight in-memory rejecting mutations with asserted reasons, including template-field drift. It validates design structure and declared constraints; it does not execute the statistical method, measure precision, prove capability or approve the method.

Next Policymaker: run that check on main and order one separate independent review. Keep this plan unpinned pending review; no pinned preparation evidence is edited. Owner quota/precision decisions and executed, independently checked development pilot evidence remain prerequisites to freezing a real evaluation manifest. Product implementation still waits for independent method review and owner acceptance of the protocol and evidence.
