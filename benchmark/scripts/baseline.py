#!/usr/bin/env python3
"""Validate the undecided baseline design template; never execute a benchmark."""

import argparse
import json
from pathlib import Path
import sys


# Frozen design contract. Do not derive required fields from the input template.
REQUIRED_FIELDS = frozenset("""
provider
exact_model_snapshot
snapshot_pinning_limitations_and_run_window
model_image_capabilities
generation_settings
generation_seeds_and_support
common_prompt_and_hash
question_input_hashes
original_artifact_set_and_hashes
permitted_documentation_and_hashes
native_images_and_unavailable_modalities
arm_specific_tool_instructions
reader_commit
reader_configuration
tool_schema
runner_version
scorer_version
split_revision
case_key_revision
native_evidence_versions
matched_total_token_budget
matched_context_budget
matched_output_budget
matched_wall_time_budget
tool_call_limits_and_accounting
truncation_and_exhaustion_recording
independent_repetitions_per_case_arm
sampling_order
paired_arm_randomization
stopping_rule
affordable_run_ceiling
precision_cost_plan_revision
fresh_session_and_memory_isolation
restricted_access_evidence
data_recipients_retention_and_grant
raw_run_record_schema_and_storage
task_reference_inventory_revision
claim_mapping_and_adjudication_revision
dimension_outcome_rules_revision
fixed_denominators
probe_suite_revision
probe_native_reference_revision
separate_probe_session_limits
probe_raw_alignment_and_outcome_records
no_reader_fidelity_not_applicable_record
coverage_strata_and_pair_accounting
required_item_and_extra_claim_reporting
elapsed_and_tool_time_accounting
input_output_token_accounting
provider_cost_basis
infrastructure_cost_basis
cache_retry_queue_and_unpriced_accounting
separate_probe_time_and_cost_accounting
per_case_tolerances_and_nondeterminism
uncertainty_procedure
confidence_level
resampling_seed_and_count
independent_lineage_units_and_repeat_preservation
missing_pair_treatment
exclusions_and_aggregation_weights
small_sample_and_unavailable_scope_reporting
owner_precision_target_and_acceptance_record
""".split())

TEMPLATE = Path(__file__).resolve().parents[1] / "baseline" / "run-manifest.template.json"


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("nonstandard JSON constant: " + value)


def validate(document):
    errors = []
    if not isinstance(document, dict) or set(document) != {"schema_version", "fields"}:
        return ["root must contain exactly schema_version and fields"]
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        errors.append("schema_version must be integer 1")
    fields = document["fields"]
    if not isinstance(fields, dict):
        return errors + ["fields must be an object"]
    for key in sorted(REQUIRED_FIELDS - set(fields)):
        errors.append("missing field: " + key)
    for key in sorted(set(fields) - REQUIRED_FIELDS):
        errors.append("extra field: " + key)
    for key in sorted(REQUIRED_FIELDS & set(fields)):
        entry = fields[key]
        if not isinstance(entry, dict) or set(entry) != {"value", "reason"}:
            errors.append(key + ": must contain exactly value and reason")
            continue
        if entry["value"] is not None:
            errors.append(key + ": undecided value must be null")
        if not isinstance(entry["reason"], str) or not entry["reason"].strip():
            errors.append(key + ": requires a nonempty reason")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True,
                        help="check the frozen undecided template structure")
    parser.parse_args()
    try:
        document = json.loads(TEMPLATE.read_text(encoding="utf-8"),
                              object_pairs_hook=unique_object,
                              parse_constant=reject_constant)
        errors = validate(document)
    except (OSError, ValueError, RecursionError) as exc:
        print("baseline template check failed: " + str(exc), file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("baseline template structure valid: " + str(len(REQUIRED_FIELDS))
          + " undecided fields; no runs or readiness verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
