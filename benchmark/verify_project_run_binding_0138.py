#!/usr/bin/env python3
"""Read-only, stdlib, data-only preparation check. Never admits or scores a run."""
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'benchmark/project-run-binding-0138.json'
SOURCE = ROOT / 'benchmark/project-paired-0136.json'
INVENTORY_FIELDS = (
    'common_prompt_and_hash', 'question_input_hashes',
    'original_artifact_set_and_hashes', 'permitted_documentation_and_hashes',
    'native_images_and_unavailable_modalities', 'case_key_revision',
    'task_reference_inventory_revision', 'claim_mapping_and_adjudication_revision',
    'dimension_outcome_rules_revision', 'fixed_denominators',
)
EVIDENCE_KINDS = (
    'manifest', 'plan', 'settings', 'common_prompt', 'question',
    'original_inventory', 'documentation_inventory', 'image_inventory',
    'tool_schema', 'raw_request', 'raw_response', 'transcript', 'tool_inventory',
    'usage', 'errors', 'timestamps', 'returned_model', 'scorer_ledger',
    'mapping_ledger', 'isolation', 'routing_retention', 'cost', 'probe_unavailable',
)
IDENTITY = ('case_id', 'pair_id', 'repetition_id', 'arm', 'record_id')
ATTEMPT_KEYS = set(IDENTITY) | {
    'attempt_id', 'manifest_sha256', 'plan_sha256', 'settings_sha256', 'evidence'
}
EVIDENCE_KEYS = {
    'kind', 'text', 'sha256', 'byte_size', 'location', 'encoding', 'content_type',
    'producer', 'attempt_id', 'created_at', 'verification'
}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def unique(pairs):
    out = {}
    for k, v in pairs:
        require(k not in out, 'duplicate JSON key: ' + k)
        out[k] = v
    return out


def invalid_constant(value):
    raise ValueError('nonstandard JSON constant: ' + value)


def parse(text):
    return json.loads(text, object_pairs_hook=unique, parse_constant=invalid_constant)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pack(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False).encode('utf-8')


def values(record):
    return {k: v['value'] for k, v in record['fields'].items()}


def load_legacy_functions():
    """Execute ONLY inspected validation/binding/conversion definitions.

    No module import, historical check(), main(), builders or scorer execution.
    AST selection keeps the original function bodies, rather than reimplementing
    their behavior. The source's pinned bytes are checked before this call.
    """
    path = ROOT / 'benchmark/scripts/run_record.py'
    source = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    functions = {
        'require', 'exact', 'sha', 'is_hash', 'strict_pairs', 'reject_constant',
        'parse', 'score_answer', 'validate', 'bind_manifest',
    }
    constants = {'POPULATED', 'UNDECIDED', 'MANIFEST_LINKS', 'BINDING_REASON'}
    imports = {'copy', 'datetime', 'hashlib', 'json', 're'}
    nodes = []
    for node in source.body:
        if isinstance(node, ast.Import):
            require(all(a.name in imports | {'argparse', 'sys'} for a in node.names),
                    'unexpected legacy import')
            if all(a.name in imports for a in node.names):
                nodes.append(node)
        elif isinstance(node, ast.ImportFrom) and node.module in imports:
            nodes.append(node)
        elif isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id in constants for t in node.targets):
            nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in functions:
            nodes.append(node)
    namespace = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
    require(functions <= set(namespace) and constants <= set(namespace),
            'legacy definition selection')
    return namespace


def check_mapping(data, source, record_template, manifest_template):
    """Full leaf-byte coverage, not a claimed inventory item count."""
    raw = source['raw_evidence_contract']
    mapped = {}
    ids = set()
    for row in data['mapping']:
        require(row['id'] not in ids, 'duplicate mapping id')
        ids.add(row['id'])
        prefix = '/raw_evidence_contract/'
        require(row['source_pointer'].startswith(prefix), 'mapping source pointer')
        key = row['source_pointer'][len(prefix):]
        require(key in raw, 'unknown source inventory leaf')
        mapped.setdefault(key, []).append(row)
        require(set(row['record_fields']) <= set(record_template['fields']),
                'unknown record field in mapping')
        require(set(row['manifest_fields']) <= set(manifest_template['fields']),
                'unknown manifest field in mapping')
        require(row['representation'] in
                ('existing-synthetic', 'design-only-linkage', 'unsupported')
                and bool(row['boundary'].strip()), 'mapping boundary')
    require(set(mapped) == set(raw), 'incomplete source inventory leaves')
    covered = 0
    for key, source_text in raw.items():
        encoded = source_text.encode('utf-8')
        offset = 0
        for row in sorted(mapped[key], key=lambda x: x['utf8_start']):
            require(row['utf8_start'] == offset and
                    row['utf8_end'] > row['utf8_start'], 'mapping gap/overlap')
            end = row['utf8_end']
            require(encoded[offset:end] == row['source_text'].encode('utf-8'),
                    'mapping source byte mismatch')
            offset = end
        require(offset == len(encoded), 'mapping source tail missing')
        covered += offset
    return {'source_leaves': len(raw), 'fragments': len(data['mapping']),
            'covered_utf8_bytes': covered}


def legacy_decision(fixture, legacy):
    try:
        manifest = parse(fixture['manifest_text'])
        for record in fixture['records']:
            legacy['validate'](record, manifest)
            legacy['bind_manifest'](record, fixture['manifest_text'].encode('utf-8'))
    except ValueError as exc:
        return str(exc)
    return 'pass'


def planned_groups(plan):
    """One design-only comparison; repetition identities use an explicit arm map.

    Legacy runner repetitions may be arm-specific. Do not infer a comparison
    from equal repetition strings, parse identifier spellings or use attempts
    as independent repetitions. No real repetition allocation is selected here.
    """
    slots = plan['slots']
    arms = {'no-tool', 'tool'}
    require(isinstance(slots, list) and len(slots) == 2 and
            all(isinstance(s, dict) for s in slots) and
            {s.get('arm') for s in slots} == arms, 'synthetic plan inventory')
    for slot in slots:
        require(set(slot) == set(IDENTITY) and all(
            isinstance(slot[k], str) and slot[k].startswith('synthetic:')
            and len(slot[k]) > 10 for k in IDENTITY if k != 'arm'),
            'synthetic slot identity')
    require(len({s['record_id'] for s in slots}) == len(slots), 'duplicate plan slot')
    groups = {}
    for slot in slots:
        groups.setdefault((slot['case_id'], slot['pair_id']), []).append(slot)
    require(len(groups) == 1, 'comparison group identity')
    comparisons = plan.get('comparisons')
    require(isinstance(comparisons, list) and len(comparisons) == len(groups)
            and all(isinstance(c, dict) and
                    set(c) == {'case_id', 'pair_id', 'repetitions'}
                    for c in comparisons), 'synthetic comparison inventory')
    for comparison in comparisons:
        key = (comparison['case_id'], comparison['pair_id'])
        require(key in groups, 'comparison group identity')
        repetitions = comparison['repetitions']
        require(isinstance(repetitions, dict) and set(repetitions) == arms and
                all(s['repetition_id'] == repetitions[s['arm']] for s in groups[key]),
                'comparison repetition mapping')
    return list(groups.values())


def linkage(fixture, source):
    """Proposed sidecar joins; never trusted verification or real admission."""
    require(fixture['synthetic'] is True, 'synthetic fixture required')
    require(fixture['verification'] == 'not_performed', 'verification unavailable')
    manifest = parse(fixture['manifest_text'])
    expected_inventory = {k: source['fields'][k]['value'] for k in INVENTORY_FIELDS}
    require(fixture['source_inventory'] == expected_inventory, 'source inventory')
    inv = fixture['source_inventory']
    require(set(manifest['fields']) == set(source['fields']), 'manifest field inventory')
    for k, envelope in source['fields'].items():
        if k not in ('generation_settings', 'exact_model_snapshot'):
            require(manifest['fields'][k] == envelope, 'manifest source inventory')
    require(fixture['settings'] == manifest['fields']['generation_settings']['value'],
            'settings manifest identity')
    require(fixture['settings'] == {
        'fixture': 'SYNTHETIC settings A; no actual generation parameters selected'
    }, 'synthetic settings fixture')
    mh = sha(fixture['manifest_text'].encode('utf-8'))
    ph = sha(fixture['plan_text'].encode('utf-8'))
    sh = sha(pack(fixture['settings']))
    plan = parse(fixture['plan_text'])
    require(plan['synthetic'] is True and plan['manifest_sha256'] == mh,
            'manifest binding')
    planned_groups(plan)
    slots = plan['slots']
    records = [values(r) for r in fixture['records']]
    require(len(records) == len(slots) and
            {r['record_id'] for r in records} == {s['record_id'] for s in slots},
            'planned records')
    for r in records:
        slot = next(s for s in slots if s['record_id'] == r['record_id'])
        require(all(r[k] == slot[k] for k in IDENTITY), 'slot identity')
        require(r['manifest_sha256'] == mh, 'manifest binding')
        require(r['common_prompt_sha256'] == inv['common_prompt_and_hash']['sha256'],
                'common prompt binding')
        require(r['model_identity'] == manifest['fields']['exact_model_snapshot']['value'],
                'model manifest identity')
        require(r['input_evidence'] == [{
            'kind': 'synthetic:original', 'identity': 'synthetic:original-1',
            'sha256': inv['original_artifact_set_and_hashes'][0]['sha256']
        }], 'input inventory')
        prefix = 'SYNTHETIC data-only request; no model call.\n'
        require(r['raw_request']['text'].startswith(prefix), 'synthetic request wrapper')
        request = parse(r['raw_request']['text'][len(prefix):])
        original = ROOT / inv['original_artifact_set_and_hashes'][0]['path']
        require(request == {
            'common_prompt': inv['common_prompt_and_hash']['text'],
            'question': inv['question_input_hashes']['text'],
            'original_text': original.read_bytes().decode('utf-8'),
            'original_sha256': inv['original_artifact_set_and_hashes'][0]['sha256'],
            'documentation_inventory': inv['permitted_documentation_and_hashes'],
            'image_inventory': inv['native_images_and_unavailable_modalities'],
            'arm_instruction': source['arm_parity']['minimal_instruction_draft'][r['arm']],
        }, 'request pinned input binding')
    attempts = fixture['attempts']
    require(len(attempts) == len(slots), 'attempt inventory')
    aids = [a.get('attempt_id') for a in attempts]
    require(all(isinstance(a, str) and a.startswith('synthetic:attempt-') for a in aids)
            and len(set(aids)) == len(aids), 'attempt identity')
    require({a['record_id'] for a in attempts} == {s['record_id'] for s in slots},
            'attempt record inventory')
    for a in attempts:
        require(set(a) == ATTEMPT_KEYS, 'attempt envelope')
        r = next(r for r in records if r['record_id'] == a['record_id'])
        require(all(a[k] == r[k] for k in IDENTITY), 'attempt slot identity')
        require(a['manifest_sha256'] == mh and a['plan_sha256'] == ph,
                'attempt manifest/plan binding')
        require(a['settings_sha256'] == sh, 'settings binding')
        evidence = a['evidence']
        require(len(evidence) == len(EVIDENCE_KINDS) and
                {e['kind'] for e in evidence} == set(EVIDENCE_KINDS),
                'evidence inventory')
        expected_text = {k: 'SYNTHETIC ' + k + ' evidence; no real object'
                         for k in EVIDENCE_KINDS}
        expected_text.update(
            manifest=fixture['manifest_text'], plan=fixture['plan_text'],
            settings=pack(fixture['settings']).decode(),
            common_prompt=inv['common_prompt_and_hash']['text'],
            question=inv['question_input_hashes']['text'],
            original_inventory=pack(inv['original_artifact_set_and_hashes']).decode(),
            documentation_inventory=pack(inv['permitted_documentation_and_hashes']).decode(),
            image_inventory=pack(inv['native_images_and_unavailable_modalities']).decode(),
            raw_request=r['raw_request']['text'], raw_response=r['raw_response']['text'],
            tool_inventory=pack(r['tool_calls']).decode(), errors=pack(r['errors']).decode(),
            returned_model=r['model_identity'])
        for e in evidence:
            require(set(e) == EVIDENCE_KEYS, 'evidence envelope')
            require(e['verification'] == 'not_performed', 'verification unavailable')
            require(e['attempt_id'] == a['attempt_id'], 'evidence attempt identity')
            payload = e['text'].encode('utf-8')
            require(e['sha256'] == sha(payload) and type(e['byte_size']) is int
                    and e['byte_size'] == len(payload), 'evidence byte identity')
            require(e['text'] == expected_text[e['kind']], 'evidence content binding')
            require(e['location'] == 'synthetic://' + a['attempt_id'] + '/' + e['kind']
                    and e['producer'] == 'synthetic:fixture-0138'
                    and e['created_at'] == '2000-01-01T00:00:00Z'
                    and e['content_type'] == 'text/plain' and e['encoding'] == 'UTF-8',
                    'synthetic evidence metadata')
    return 'pass'


def mutate(fixture, operations):
    for op, pointer, value in operations:
        parts = pointer.lstrip('/').split('/')
        parent = fixture
        for key in parts[:-1]:
            parent = parent[int(key)] if isinstance(parent, list) else parent[key]
        key = int(parts[-1]) if isinstance(parent, list) else parts[-1]
        if op == 'set':
            parent[key] = deepcopy(value)
        elif op == 'delete':
            del parent[key]
        else:
            raise ValueError('unknown mutation operation')


def synthetic_accounting(fixture, old, joined):
    """Count only valid groups with their unique records and retained attempts."""
    records = [values(r) for r in fixture['records']]
    attempts = fixture['attempts']
    counts = {
        'planned_slots': 0, 'present_records': len(records),
        'attempts_retained': len(attempts),
        'interrupted_records': sum(r['outcome'] == 'interrupted' for r in records),
        'synthetic_structurally_complete_pairs': 0,
    }
    try:
        plan = parse(fixture['plan_text'])
        if isinstance(plan.get('slots'), list):
            counts['planned_slots'] = len(plan['slots'])
        groups = planned_groups(plan)
        if old != 'pass' or joined != 'pass':
            return counts
        slots = plan['slots']
        record_ids = {s['record_id'] for s in slots}
        require(len(records) == len(attempts) == len(record_ids) and
                {r['record_id'] for r in records} == record_ids and
                {a['record_id'] for a in attempts} == record_ids and
                len({a['attempt_id'] for a in attempts}) == len(attempts),
                'accounting inventory')
        for group in groups:
            group_records = []
            for slot in group:
                record = next(r for r in records if r['record_id'] == slot['record_id'])
                attempt = next(a for a in attempts if a['record_id'] == slot['record_id'])
                require(all(record[k] == attempt[k] == slot[k] for k in IDENTITY),
                        'accounting slot identity')
                group_records.append(record)
            complete = all(
                r['outcome'] == r['answer_status'] == 'complete' and not r['errors']
                and not r['truncated'] and not r['exhausted_budgets']
                and all(c['error'] is None for c in r['tool_calls'])
                for r in group_records)
            counts['synthetic_structurally_complete_pairs'] += int(complete)
    except (ValueError, KeyError, TypeError, StopIteration):
        # Invalid plans/joins retain inventory counts but can never complete.
        counts['synthetic_structurally_complete_pairs'] = 0
    return counts


def main():
    data = parse(DATA.read_text(encoding='utf-8'))
    require(data['schema_version'] == 1, 'data schema')
    require(data['rehearsal']['predeclared'] is True, 'expectations not predeclared')
    for pin in data['pins']:
        path = ROOT / pin['path']
        require(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'pin path')
        require(0 < path.stat().st_size < 2_000_000, 'pin evidence size')
        require(sha(path.read_bytes()) == pin['sha256'], 'stale source pin: ' + pin['path'])
    source = parse(SOURCE.read_text(encoding='utf-8'))
    rt = parse((ROOT / 'benchmark/baseline/run-record.template.json').read_text())
    mt = parse((ROOT / 'benchmark/baseline/run-manifest.template.json').read_text())
    coverage = check_mapping(data, source, rt, mt)
    legacy = load_legacy_functions()
    require(set(source['fields']) == set(mt['fields']), 'source manifest names')
    require(set(data['rehearsal']['required_evidence_kinds']) == set(EVIDENCE_KINDS),
            'required evidence definition')
    base = data['rehearsal']['fixture']
    # Mandatory-null reasons remain the exact old template reasons.
    for record in base['records']:
        for key in legacy['UNDECIDED']:
            require(record['fields'][key] == rt['fields'][key], 'null envelope drift')
    for dim in ('correctness', 'grounding'):
        require(source['fields']['fixed_denominators']['value'][dim] ==
                {'ids': ['D1', 'D2', 'D3', 'D4'], 'total': 4}, 'dimension denominator')
    for name in ('common_prompt_and_hash', 'question_input_hashes'):
        value = source['fields'][name]['value']
        require(sha(value['text'].encode()) == value['sha256'], 'source text identity')
    observed = []
    names = set()
    for control in data['rehearsal']['controls']:
        require(control['name'] not in names, 'duplicate control name')
        names.add(control['name'])
        fixture = deepcopy(base)
        mutate(fixture, control['mutations'])
        old = legacy_decision(fixture, legacy)
        if old not in ('pass', legacy['BINDING_REASON']):
            new = 'legacy rejected'
        else:
            # Observe linkage independently, including a legacy byte-binding failure.
            try:
                new = linkage(fixture, source)
            except ValueError as exc:
                new = str(exc)
        result = {'legacy': old, 'linkage': new,
                  'real_admission': 'blocked', 'semantic_passes': 0}
        require(result == control['expected'],
                control['name'] + ': expected ' + repr(control['expected']) +
                ', observed ' + repr(result))
        item = {'name': control['name'], **result}
        accounting = synthetic_accounting(fixture, old, new)
        require(accounting == control['expected_accounting'],
                control['name'] + ': accounting mismatch')
        item['synthetic_accounting'] = accounting
        observed.append(item)
    require(any(x['legacy'] == x['linkage'] == 'pass' for x in observed),
            'positive consistency control missing')
    require(any(x['legacy'] == 'pass' and x['linkage'] != 'pass' for x in observed),
            'unchanged contract boundary control missing')
    require(all(type(v) is int and v == 0 for v in data['actual_counts'].values()),
            'actual execution/admission counts')
    summary = {
        'status': 'pass', 'scope': 'preparation consistency only',
        'coverage': coverage, 'controls_matched': len(observed),
        'observed': observed, 'actual_counts': data['actual_counts'],
        'trusted_substantive_verification': 'blocked',
        'method_accepted': False, 'benchmark_ready': False,
    }
    if data['rehearsal']['observed'] is not None:
        require(data['rehearsal']['observed'] == summary, 'saved observations differ')
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as exc:
        print('project-run-binding-0138: ' + str(exc), file=sys.stderr)
        sys.exit(1)
