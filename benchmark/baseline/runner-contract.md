# Runner contract (design only)

Status: design over SYNTHETIC data. No runs executed, no model calls, no real cases, no spending. The benchmark is not ready and tool quality is unmeasured. Provider and infrastructure resource rows (#169/#268) are still needed.

Check: `python3 -I -B benchmark/scripts/runner_contract.py --check` (exit 0).

## Inputs
- `benchmark/baseline/run-manifest.synthetic.json`: populated with synthetic values for 19 of the template fields; every other field stays null with the exact template reason. Regenerate with `--write-manifest`; `--check` fails if the file differs from the generator.
- `run-manifest.template.json`: field names and null reasons. The synthetic manifest must have exactly these names.
- `run-record.template.json` and `run_record.py`: per-run record, `validate` and `bind_manifest` (imported by path, unchanged).

## Plan
Runs = cases x repetitions x arms (`no-tool`, `tool`). Cases are sorted by id. Within each (case, repetition) pair the arm order is sorted by sha256(`seed:pair_id:arm`), with the seed taken from `paired_arm_randomization`. The plan is deterministic and carries the manifest sha256 and a plan hash. The synthetic plan has 3 cases x 2 arms x 2 repetitions = 12 runs.

## Audit of a record set
1. Manifest bytes must still hash to the planned manifest hash.
2. Each record passes `validate` and `bind_manifest`.
3. No duplicate repetition ids or record ids.
4. Each record's case, arm, pair and record id match the planned run; unknown case or repetition ids are rejected.
5. No planned run is missing (for example, a whole arm for a case).
6. Total-token, output, context, wall-time and tool-call budgets from the manifest are respected.

## Rejection controls
The check runs 10 mutations, each required to fail for its specific reason: missing arm, duplicate repetition id, manifest bytes changed after planning, unknown case id, unknown arm, record bound to another manifest, token budget exceeded, removed manifest field, altered null reason, and populated field without synthetic provenance.

## Still undecided
All null manifest fields, in particular: provider and model snapshot choice (only synthetic placeholders here), generation settings, real budgets and the affordable run ceiling, repetition count and stopping rule (synthetic values are not a precision plan), reader commit/config/tool schema, restricted storage and isolation evidence, scorer and claim-mapping revisions, uncertainty procedure, and owner precision targets. The synthetic budgets and seed are design fixtures only.

## Limits
Nothing here shows that a real runner can execute the plan, that records are preserved in a restricted boundary, or that either arm performs well. Independent review is required before pinning in `benchmark/preparation.json`; this change does not edit it.
