# Native job designs

Design only: nothing executed; no native evidence exists for these recipes. #169 is not ready. Native 2024 and other versions remain unproven. No readiness or quality claim is made.

Generate with `python3 -I benchmark/scripts/native_jobs.py`; verify with `python3 -I benchmark/scripts/native_jobs.py --check`. Both use repository JSON and stdlib only, without LABVIEW_ENVIRONMENT, git, network or LabVIEW. Check regenerates in memory and rejects any byte difference. Generation preflights all files and refuses existing differences.

[recipes.json](recipes.json) maps 23 of 23 native-required development slots to 11 case recipes; zero unmapped slots. IDs are case-qualified claim IDs, with separate aligned reader observation IDs. Mapping is a design assignment, not semantic completion. The three project build-result slots remain partially blocked because builds are forbidden; properties cannot establish actual build results.

The additional #169 readiness candidate is public `pylavi/tests/add.vi`, pinned through sources.json. Its small arithmetic-looking identity makes it a candidate, but its filename does not establish behaviour. No independently known behaviour, connector map or input/output fixture was found in the named evidence. Therefore the known-behaviour acceptance requirement remains unmet; a separate checker must establish and pin expectations before dispatch. Do not substitute compile success or reader output for that evidence.

Every recipe declares original hashes, archive chains where applicable, unknown version/bitness/modules with reasons, allowed operations, staged outputs and independent-check steps. Original save versions do not establish native compatibility. All dependencies must be enumerated and hashed before dispatch; no implicit source-directory access or fetching is permitted. Controlled I/O fixtures, runner API details and bounded timeouts remain prerequisites, so these designs are not executable dispatch specifications.

Only read properties, diagram capture and explicitly fixture-controlled I/O are proposed. No edits, saves, builds or network. Preserve originals, use hashed disposable copies, suppress automatic execution/hooks, close without saving and record failures. A job must stop when inspection APIs or captures are inaccessible; absence remains a gap.

[output-record.template.json](output-record.template.json) describes future staged records. Null SHA256 fields mean not produced; they must be replaced with measured hashes for actual outputs. Native properties and captures must include original object locators and substantive values; separate checker records must establish claim-level agreement. Hash validation alone cannot establish truth.

Next: independent review of this design; independently establish the readiness VI and discriminating vectors; resolve environment/dependency/fixture prerequisites; obtain owner provisioning and capability-ready for #169. Builds require a separate grant. Independent method review and owner acceptance still precede product implementation; executable scoring requires a Policymaker-ordered evaluator change and separate verifier. No evidence index or case/key is changed here.
