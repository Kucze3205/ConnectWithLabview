#!/usr/bin/env python3
"""Generate public native-job designs, never dispatch or execute LabVIEW."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'benchmark/native'
PERMITTED = {'read-properties', 'diagram-capture', 'controlled-io'}
FAMILIES = {
    'class-actor': '.lvclass', 'class-archive-another-actor': '.lvclass',
    'class-stop-msg': '.lvclass', 'library-debug': '.lvlib',
    'library-framework': '.lvlib', 'library-icon-tests': '.lvlib',
    'library-specialty': '.lvlib', 'project-archive-ppl': '.lvproj',
    'project-debug-ppl': '.lvproj', 'project-ppl': '.lvproj',
    'vi-actor-core-native-gap': '.vi',
}
TOPICS = {
    '.lvproj': ['resolved-dependencies', 'effective-build-inclusion-and-build-result'],
    '.lvclass': ['resolved-direct-parent-and-inheritance', 'effective-scope-and-dispatch'],
    '.lvlib': ['resolved-membership', 'effective-scope'],
    '.vi': ['connector-terminals-and-types', 'diagram-nodes-wires-and-execution-dependencies',
            'controlled-input-output-behavior'],
}
PROCEDURES = {
    'resolved-dependencies': 'For every declared dependency and target, record native resolved path, identity/hash, resolution status and unresolved reason; compare against original project XML. Never fetch missing dependencies.',
    'effective-build-inclusion-and-build-result': 'Inspect native build properties and source/destination inclusion with original XML locators. Record build-result as unavailable: builds and build hooks are forbidden. Settings alone cannot establish a build result.',
    'resolved-direct-parent-and-inheritance': 'Inspect native direct parent and complete inheritance chain, including qualified identities and hashed resolved files. Encoded XML payloads alone are insufficient; capture the native inheritance view.',
    'effective-scope-and-dispatch': 'Inspect each member native access scope, dispatch mode, overrides and parent-call requirement. Capture property values and original member locators; absence of XML flags does not establish defaults.',
    'resolved-membership': 'Enumerate native qualified members and resolved paths, pin resolved file hashes, compare membership with original XML and list unresolved/missing members explicitly.',
    'effective-scope': 'Inspect native effective access for each member, accounting for containing libraries. Capture native properties and match original member locators; do not infer defaults from absent XML properties.',
    'connector-terminals-and-types': 'Capture connector pane and front panel. Enumerate terminal direction, position, required/optional status, exact type and typedef identity with original object-to-capture mapping.',
    'diagram-nodes-wires-and-execution-dependencies': 'Capture all accessible diagram frames and nested structures. Map node/terminal/wire identities and endpoints to capture regions. Record inaccessible diagrams; distinguish dataflow guarantees from one observed schedule.',
    'controlled-input-output-behavior': 'Before execution, independently freeze hashed input vectors, initial state/reset, dependency set, target, timeout, stop condition, expected outputs/errors, units, precision and allowed variation. Select vectors separating plausible wrong computations. No I/O until these fixtures are reviewed; record actual outputs, errors and execution observations without deriving expectations from the reader.',
}
CHECK = [
    'A separate checker session records checker identity/role/session, recipe revision, case/key revision and every evidence hash; this author cannot approve its own native expectations.',
    'Rehash preserved original and separately hashed working copy before/after with python3 -I; compare to the declared manifest identity. Capture git status --porcelain before/after on the mounted source checkout; require no source mutation. Close without saving.',
    'Resolve every covered claim and aligned reader observation against original native objects, property values and capture regions. Hashes and filenames alone are insufficient. Do not use an evaluated reader/export to establish expectations.',
    'Record claim-level agreement/disagreement, native locator, evidence path/hash, substantive observed value, derivation method and uncertainty. Disagreement or missing evidence leaves the claim unverified until adjudicated and independently rechecked.',
    'For I/O, freeze independent expectations before running, inspect full logs and compare every vector using its declared comparison rules. Challenge wrong answers and wrong source locations; reject constant outputs that fail discriminating vectors.',
]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value),
            'Missing or invalid input sha256')
    return value


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')


def identity_check(identity, sources, coverage):
    sha(identity['sha256'])
    repo = next(r for r in sources['repositories'] if r['name'] == identity['repository'])
    require(repo['commit'] == identity['commit'], 'Repository commit mismatch')
    chain = identity['archive_member_chain']
    if chain:
        require(len(chain) == 1, 'Unsupported archive chain')
        member = chain[0]
        matches = [a for a in coverage['artifacts']
                   if a['archive'] == repo['name'] + '/' + member['container_path']
                   and a['path'] == identity['path'] and a['member_index'] == member['member_index']]
        containers = [a for a in repo['artifacts'] if a['path'] == member['container_path']]
        containers += [a for a in coverage['artifacts'] if a['archive'] is None
                       and a['path'] == repo['name'] + '/' + member['container_path']]
        require(containers and all(sha(a['sha256']) == member['container_sha256'] for a in containers),
                'Archive container hash mismatch')
        require(member['member_path'] == identity['path'] and member['member_sha256'] == identity['sha256'],
                'Archive member identity mismatch')
    else:
        matches = [a for a in repo['artifacts'] if a['path'] == identity['path']]
    require(len(matches) == 1 and sha(matches[0]['sha256']) == identity['sha256'],
            'Input identity missing from sources/coverage or hash mismatch')
    manifest = identity['identity_manifest']
    require(manifest in {'benchmark/sources.json', 'benchmark/coverage.json'}, 'Unknown identity manifest')
    require(digest((ROOT / manifest).read_bytes()) == identity['identity_manifest_sha256'],
            'Identity manifest drift')


def unknown(reason):
    return {'value': None, 'reason': reason}


def environment():
    return {
        'required_labview_version': unknown('Native compatibility is unproven; original save-version evidence is recorded separately. Select and pin a suitable reading version before dispatch.'),
        'required_bitness': unknown('No native load/property/capture experiment establishes required bitness.'),
        'required_modules': unknown('Dependencies, modules, targets and licences have not been resolved natively. Null does not mean no modules required.'),
        'candidate_path': 'Owner-provisioned #169 NI 2026 Q1 cloud path; load/compile evidence does not prove property inspection, capture or controlled I/O.',
    }


def output(name, content):
    return {'path': name, 'sha256': None, 'status': 'not-produced', 'required_content': content}


def recipe(identifier, artifact, slots, save_version):
    operations = ['read-properties', 'diagram-capture']
    if any(s['topic'] == 'controlled-input-output-behavior' for s in slots):
        operations.append('controlled-io')
    return {
        'id': identifier, 'revision': 1, 'status': 'design-only-not-dispatchable',
        'covered_slot_ids': [s['slot_id'] for s in slots], 'input': artifact,
        'original_save_version_evidence': save_version, 'environment_requirements': environment(),
        'permitted_operations': operations, 'forbidden_operations': ['edits', 'saves', 'builds', 'network'],
        'execution_boundary': 'Trusted job receives only predeclared hashed public originals/dependencies and licence access. Preserve originals read-only; inspect separately hashed disposable copies, never save. Disable network and automatic execution/build hooks. Roles receive staged outputs, no runner credentials or Docker daemon. Abort on undeclared input, unsupported API or side effect.',
        'dependency_inputs': unknown('Before dispatch enumerate every needed dependency with source path, commit/archive identity and sha256; missing inputs stay unavailable and cannot be fetched.'),
        'slot_procedures': slots,
        'expected_staged_outputs': [
            output('environment.json', 'Actual native version/build/bitness, OS, image digest, modules, licence/target availability and API support/failures.'),
            output('preservation.json', 'Original and working-copy pre/post SHA256, source status before/after, load/save warnings and mutation verdict.'),
            output('properties.json', 'Native property names, typed values, original object locators, resolved identities/hashes and inaccessible/unresolved reasons for every requested slot.'),
            output('captures/index.json', 'Every capture path and SHA256, original object locator, view/frame and region; capture binaries separately hashed. Include unavailable views explicitly.'),
            output('slot-results.json', 'One record per covered slot with aligned reader observation, substantive value or null/unavailable reason, native locator, evidence hashes and uncertainty. Partial coverage cannot establish the full slot.'),
            output('job.log', 'Complete bounded operation log, timestamps, warnings/errors, timeouts, forbidden-operation refusal and clean shutdown.'),
            output('independent-check.json', 'Separate checker identity/session, frozen key/fixture hashes and claim-level substantive agreements/disagreements with original/native citations.'),
        ],
        'controlled_io_fixture': unknown('Connector identity, state/reset, discriminating vectors, independent expected values, comparison rules, timeout and safe stop must be frozen before any execution.') if 'controlled-io' in operations else {'value': None, 'reason': 'No execution permitted by this inspection recipe.'},
        'independent_check_procedure': CHECK,
    }


def documents():
    sources, coverage = load('benchmark/sources.json'), load('benchmark/coverage.json')
    files = sorted((ROOT / 'benchmark/cases/dev').glob('*.json'))
    require({p.stem for p in files} == set(FAMILIES), 'Unknown or missing development case')
    recipes, expected = [], set()
    for path in files:
        case = json.loads(path.read_text(encoding='utf-8'))
        cid = case['case_id']
        require(cid == path.stem and case['family'] == FAMILIES[cid], 'Case/family mismatch')
        identity_check(case['artifact'], sources, coverage)
        claims = [c for c in case['reference_inventory'] if c.get('reference_status') == 'unverified-native-required']
        require([c['claim_id'] for c in claims] == ['N%04d' % n for n in range(1, len(TOPICS[case['family']]) + 1)], 'Unknown or missing native slot id')
        require([c['atomic_fact']['relation'] for c in claims] == TOPICS[case['family']], 'Native topic drift')
        slots = []
        for claim in claims:
            slot = cid + ':' + claim['claim_id']
            expected.add(slot)
            topic = claim['atomic_fact']['relation']
            observation = 'R' + claim['claim_id']
            require(any(o['observation_id'] == observation and o['aligned_claim_id'] == claim['claim_id'] for o in case['reader_reference_inventory']), 'Reader alignment mismatch')
            slots.append({'slot_id': slot, 'case_id': cid, 'claim_id': claim['claim_id'],
                          'reader_observation_id': observation, 'topic': topic,
                          'procedure': PROCEDURES[topic], 'expected_value': None,
                          'reference_status': 'unavailable-native-not-executed'})
        recipes.append(recipe('native-' + cid, case['artifact'], slots, case['save_version']))
    require(len(expected) == 23, 'Native denominator changed')
    # A public candidate, never represented as an independently established oracle.
    repo = next(r for r in sources['repositories'] if r['name'] == 'pylavi')
    artifact = next(a for a in repo['artifacts'] if a['path'] == 'tests/add.vi')
    readiness_input = {'repository': repo['name'], 'repository_url': repo['upstream_url'],
                       'commit': repo['commit'], 'path': artifact['path'], 'sha256': sha(artifact['sha256']),
                       'archive_member_chain': [], 'identity_manifest': 'benchmark/sources.json',
                       'identity_manifest_sha256': digest((ROOT / 'benchmark/sources.json').read_bytes())}
    readiness = recipe('capability-169-readiness-candidate', readiness_input, [], artifact['save_version'])
    readiness['permitted_operations'].append('controlled-io')
    readiness['controlled_io_fixture'] = unknown('No independent behaviour evidence or connector mapping is available for this candidate; filename add.vi is not evidence of addition. Dispatch is blocked until a separate session establishes and pins expected vectors.')
    readiness['readiness_selection'] = {'candidate_vi': 'pylavi/tests/add.vi',
        'why': 'Public, small, source-hashed VI intended as a candidate for a discriminating arithmetic check; semantics have not been established.',
        'independently_known_behavior': False,
        'acceptance_gap': 'No VI with independently known behaviour was established in this design session. This candidate does not yet satisfy the known-behaviour prerequisite of #169.'}
    readiness['expected_staged_outputs'].append(output('controlled-io.json', 'Pre-frozen independent input/output expectations and hashes, reset/stop/timeout, exact typed actual values/errors and per-vector comparison. Compile success alone fails readiness.'))
    recipes.append(readiness)
    for item in recipes:
        require(set(item['permitted_operations']) <= PERMITTED, 'Operation outside permitted list')
        sha(item['input']['sha256'])
    mapped = [slot for item in recipes for slot in item['covered_slot_ids']]
    require(len(mapped) == len(set(mapped)) and set(mapped) == expected, 'Unknown, duplicate or missing slot mapping')
    manifest = {'schema_version': 1, 'status': 'design-only', 'native_executed': False,
                'capability_169_ready': False, 'mapped_slot_count': 23, 'unmapped_slot_ids': [],
                'recipes': recipes}
    template = {
        'schema_version': 1, 'status': 'not-executed', 'recipe_id': None, 'recipe_revision': None,
        'recipe_sha256': None, 'job_id': None, 'operator_identity': None,
        'started_at': None, 'ended_at': None, 'actual_environment': None,
        'input_identities': [], 'original_before_after_sha256': [],
        'working_copy_before_after_sha256': [], 'source_git_status_before_after': None,
        'operations_attempted': [], 'outputs': [{'path': None, 'sha256': None, 'status': 'not-produced'}],
        'controlled_io': {'fixture_path': None, 'fixture_sha256': None, 'independent_expectations_sha256': None,
                          'vectors': [], 'reset_procedure': None, 'comparison_rules': None,
                          'timeout': None, 'stop_condition': None},
        'slot_results': [{'slot_id': None, 'reader_observation_id': None, 'status': 'unavailable',
                          'value': None, 'reason': 'No native evidence produced.', 'native_locator': None,
                          'evidence': [], 'uncertainty': None}],
        'independent_check': {'checker_identity': None, 'role': None, 'session': None,
                              'case_key_revision': None, 'agreements': [], 'disagreements': [],
                              'unresolved': [], 'status': 'pending'},
        'schema_notes': 'Copy per job. Null hashes are placeholders, never evidence. Every produced file requires actual lowercase SHA256; every unavailable output/slot needs a reason. Complete original object locators, capture regions and substantive values before independent checking. Retain all fixed slots. This generator checks design files only, not filled records or native results.',
    }
    readme = '''# Native job designs

Design only: nothing executed; no native evidence exists for these recipes. #169 is not ready. Native 2024 and other versions remain unproven. No readiness or quality claim is made.

Generate with `python3 -I benchmark/scripts/native_jobs.py`; verify with `python3 -I benchmark/scripts/native_jobs.py --check`. Both use repository JSON and stdlib only, without LABVIEW_ENVIRONMENT, git, network or LabVIEW. Check regenerates in memory and rejects any byte difference. Generation preflights all files and refuses existing differences.

[recipes.json](recipes.json) maps 23 of 23 native-required development slots to 11 case recipes; zero unmapped slots. IDs are case-qualified claim IDs, with separate aligned reader observation IDs. Mapping is a design assignment, not semantic completion. The three project build-result slots remain partially blocked because builds are forbidden; properties cannot establish actual build results.

The additional #169 readiness candidate is public `pylavi/tests/add.vi`, pinned through sources.json. Its small arithmetic-looking identity makes it a candidate, but its filename does not establish behaviour. No independently known behaviour, connector map or input/output fixture was found in the named evidence. Therefore the known-behaviour acceptance requirement remains unmet; a separate checker must establish and pin expectations before dispatch. Do not substitute compile success or reader output for that evidence.

Every recipe declares original hashes, archive chains where applicable, unknown version/bitness/modules with reasons, allowed operations, staged outputs and independent-check steps. Original save versions do not establish native compatibility. All dependencies must be enumerated and hashed before dispatch; no implicit source-directory access or fetching is permitted. Controlled I/O fixtures, runner API details and bounded timeouts remain prerequisites, so these designs are not executable dispatch specifications.

Only read properties, diagram capture and explicitly fixture-controlled I/O are proposed. No edits, saves, builds or network. Preserve originals, use hashed disposable copies, suppress automatic execution/hooks, close without saving and record failures. A job must stop when inspection APIs or captures are inaccessible; absence remains a gap.

[output-record.template.json](output-record.template.json) describes future staged records. Null SHA256 fields mean not produced; they must be replaced with measured hashes for actual outputs. Native properties and captures must include original object locators and substantive values; separate checker records must establish claim-level agreement. Hash validation alone cannot establish truth.

Next: independent review of this design; independently establish the readiness VI and discriminating vectors; resolve environment/dependency/fixture prerequisites; obtain owner provisioning and capability-ready for #169. Builds require a separate grant. Independent method review and owner acceptance still precede product implementation; executable scoring requires a Policymaker-ordered evaluator change and separate verifier. No evidence index or case/key is changed here.
'''
    return {'README.md': readme.encode('utf-8'), 'recipes.json': encode(manifest),
            'output-record.template.json': encode(template)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        outputs = documents()
        for name, data in outputs.items():
            path = OUT / name
            require(not path.is_symlink(), 'Symlink output: ' + name)
            require(len(data) < 2_000_000, 'Oversized output: ' + name)
            if path.exists():
                require(path.read_bytes() == data, 'Byte difference: ' + name)
            else:
                require(not args.check, 'Missing output: ' + name)
        if not args.check:
            require(not OUT.is_symlink(), 'Symlink output directory')
            OUT.mkdir(parents=True, exist_ok=True)
            for name, data in outputs.items():
                if not (OUT / name).exists():
                    (OUT / name).write_bytes(data)
        print('Native design valid: 23/23 slots mapped; 12 recipes; zero native executions. Known-behaviour readiness prerequisite unresolved.')
        return 0
    except (OSError, ValueError, KeyError, StopIteration, TypeError) as exc:
        print('Native design failed: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
