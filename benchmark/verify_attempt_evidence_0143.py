#!/usr/bin/env python3
"""Repository-only synthetic retention rehearsal; no runner, scorer or real admission.

All payload originals are embedded in the JSON. Nothing is written. The inspected,
pinned grouping checker supplies selected legacy helpers and the retained boundary.
"""
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'benchmark/attempt-evidence-0143.json'
IDENTITY = ('case_id', 'pair_id', 'repetition_id', 'arm', 'record_id')
FORMAT = 'synthetic-attempt-evidence/1'
EVENT_KEYS = {'attempt_id', 'attempt_order', 'transport_outcome', 'started_at',
              'finished_at', 'truncated', 'exhausted_budgets', 'cache_events',
              'queue_time_ms', 'tool_time_ms'}
ATTEMPT_KEYS = set(IDENTITY) | {'slot_ref', 'attempt_id', 'attempt_order',
    'transport_outcome', 'response_parsing', 'input_binding', 'legacy_record', 'evidence'}
ENTRY_KEYS = {'kind', 'object_id', 'attempt_id', 'producer', 'producer_version',
              'created_at', 'verification', 'presence', 'payload_ref', 'content_type'}
ENVELOPE_KEYS = {'schema_version', 'synthetic', 'manifest_sha256', 'plan_sha256',
    'settings_sha256', 'verification', 'real_admission', 'attempt_selection', 'attempts'}
OUTCOMES = {'succeeded': 'complete', 'failed': 'error',
            'interrupted': 'interrupted', 'unsupported': 'unsupported'}


def require(value, reason):
    if not value:
        raise ValueError(reason)


def unique(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def nonfinite(value):
    raise ValueError('nonfinite JSON')


def parse(text):
    return json.loads(text, object_pairs_hook=unique, parse_constant=nonfinite)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pack(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False).encode('utf-8')


def payload(value, integrity=True):
    require(isinstance(value, dict) and set(value) ==
            {'encoding', 'hex', 'byte_size', 'sha256', 'utf8'}, 'payload fields')
    require(value['encoding'] == 'hex', 'payload encoding')
    require(isinstance(value['hex'], str) and
            re.fullmatch('(?:[0-9a-f]{2})*', value['hex']) is not None, 'payload hex')
    raw = bytes.fromhex(value['hex'])
    if integrity:
        require(value['sha256'] == sha(raw), 'payload hash')
        require(type(value['byte_size']) is int and value['byte_size'] == len(raw),
                'payload size')
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            text = None
        require(value['utf8'] == text, 'payload UTF-8 view')
    return raw


def entry(attempt, kind):
    return next((e for e in attempt['evidence'] if e.get('kind') == kind), None)


def raw_at(fixture, attempt, kind, integrity=False):
    item = entry(attempt, kind)
    if item is None or item.get('presence') != 'present':
        return None
    return payload(fixture['payloads'][item['payload_ref']], integrity)


def event_at(fixture, attempt):
    raw = raw_at(fixture, attempt, 'attempt_event')
    require(raw is not None, 'event unavailable')
    return parse(raw.decode('utf-8'))


def response_state(fixture, attempt):
    item = entry(attempt, 'raw_response')
    if item is None:
        return 'missing_evidence'
    if item.get('presence') == 'absent':
        return 'absent'
    try:
        raw = raw_at(fixture, attempt, 'raw_response')
        if raw is None:
            return 'unreadable'
        if not raw:
            return 'empty'
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            return 'invalid_utf8'
        try:
            parse(text)
        except ValueError:
            return 'malformed_json'
        return 'parseable_json'
    except (ValueError, KeyError, TypeError):
        return 'unreadable'


def legacy_result(fixture, attempt, source, legacy):
    record = attempt['legacy_record']
    if record is None:
        return 'unavailable'
    try:
        f = {k: v['value'] for k, v in record['fields'].items()}
        require(all(f[k] == attempt[k] for k in IDENTITY), 'legacy identity')
        # Bind attachments to pinned source content. validate() separately binds
        # every sidecar object to that source. Missing/corrupt sidecar objects
        # still reject without changing rejected-fixture attachment inventories.
        inv = source['base']['source_inventory']
        old = next((a for a in source['base']['attempts'] if a['arm'] == attempt['arm']), None)
        require(old is not None, 'legacy source arm')
        expected = {e['kind']: e['text'].encode('utf-8') for e in old['evidence']}
        require(f['model_identity'] ==
                source['manifest']['fields']['exact_model_snapshot']['value'] and
                f['model_identity'].encode('utf-8') == expected['returned_model'],
                'legacy model binding')
        require(f['common_prompt_sha256'] == inv['common_prompt_and_hash']['sha256'] and
                f['common_prompt_sha256'] == sha(expected['common_prompt']),
                'legacy common prompt binding')
        require(f['input_evidence'] == [{
            'kind': 'synthetic:original', 'identity': 'synthetic:original-1',
            'sha256': inv['original_artifact_set_and_hashes'][0]['sha256']
        }], 'legacy original input binding')
        require(pack(f['tool_calls']) == expected['tool_inventory'],
                'legacy tool content binding')
        for kind in ('raw_request', 'raw_response'):
            require(f[kind]['text'].encode('utf-8') == raw_at(fixture, attempt, kind),
                    'legacy raw bytes')
        require(pack(f['errors']) == raw_at(fixture, attempt, 'errors'), 'legacy error bytes')
        event = event_at(fixture, attempt)
        require(f['outcome'] == OUTCOMES[event['transport_outcome']] and
                f['truncated'] == event['truncated'] and
                f['exhausted_budgets'] == event['exhausted_budgets'], 'legacy outcome')
        for key in legacy['UNDECIDED']:
            require(record['fields'][key] == source['template']['fields'][key],
                    'legacy null reasons')
        legacy['validate'](record, source['manifest'])
        legacy['bind_manifest'](record, source['base']['manifest_text'].encode('utf-8'))
    except (ValueError, KeyError, TypeError, UnicodeError):
        return 'invalid'
    return 'pass'


def validate(fixture, source, group, legacy):
    require(set(fixture) == {'payloads', 'envelope'}, 'fixture fields')
    envelope = fixture['envelope']
    require(set(envelope) == ENVELOPE_KEYS and envelope['schema_version'] == FORMAT,
            'envelope version/fields')
    require(envelope['synthetic'] is True, 'synthetic only')
    require(envelope['verification'] == 'not_performed', 'verification unavailable')
    require(envelope['real_admission'] == 'blocked', 'real admission unavailable')
    require(envelope['attempt_selection'] == 'unresolved', 'selection unavailable')
    base = source['base']
    require(envelope['manifest_sha256'] == sha(base['manifest_text'].encode()),
            'manifest binding')
    require(envelope['plan_sha256'] == sha(base['plan_text'].encode()), 'plan binding')
    require(envelope['settings_sha256'] == sha(pack(base['settings'])), 'settings binding')
    plan = parse(base['plan_text'])
    group['planned_groups'](plan)
    slots = {s['record_id']: s for s in plan['slots']}
    require(isinstance(fixture['payloads'], dict), 'payload inventory')
    for key, item in fixture['payloads'].items():
        require(isinstance(key, str) and key.startswith('synthetic:payload-'), 'payload identity')
        payload(item)
    attempts = envelope['attempts']
    require(isinstance(attempts, list), 'attempt inventory')
    ids = [a.get('attempt_id') for a in attempts]
    require(all(isinstance(x, str) and x.startswith('synthetic:attempt-') for x in ids)
            and len(ids) == len(set(ids)), 'attempt identity')
    orders = [a.get('attempt_order') for a in attempts]
    require(all(type(x) is int and x > 0 for x in orders)
            and len(orders) == len(set(orders)) and orders == sorted(orders), 'attempt order')
    kinds = set(group['EVIDENCE_KINDS']) | {'attempt_event'}
    for attempt in attempts:
        require(set(attempt) == ATTEMPT_KEYS, 'attempt fields')
        require(attempt['slot_ref'] in slots, 'slot reference')
        slot = slots[attempt['slot_ref']]
        require(all(attempt[k] == slot[k] for k in IDENTITY), 'slot identity')
        require(attempt['transport_outcome'] in OUTCOMES, 'transport outcome')
        evidence = attempt['evidence']
        require(isinstance(evidence, list) and len(evidence) == len(kinds) and
                {e.get('kind') for e in evidence} == kinds, 'required evidence')
        old = next(a for a in base['attempts'] if a['arm'] == attempt['arm'])
        expected = {e['kind']: e['text'].encode('utf-8') for e in old['evidence']}
        for e in evidence:
            require(set(e) == ENTRY_KEYS, 'evidence fields')
            require(e['verification'] == 'not_performed', 'verification unavailable')
            require(e['attempt_id'] == attempt['attempt_id'], 'evidence attempt')
            require(e['object_id'] == 'synthetic://' + attempt['attempt_id'] + '/' + e['kind'],
                    'evidence object')
            require(e['producer'] == 'synthetic:fixture-0143' and e['producer_version'] == '1',
                    'evidence producer')
            require(e['created_at'] == '2000-01-01T00:00:00Z', 'evidence UTC')
            datetime.strptime(e['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            require(e['content_type'] == 'application/octet-stream', 'evidence content type')
            require(e['presence'] in ('present', 'absent'), 'evidence presence')
            if e['presence'] == 'absent':
                require(e['kind'] == 'raw_response' and e['payload_ref'] is None,
                        'absent representation')
                continue
            require(e['payload_ref'] in fixture['payloads'], 'payload reference')
            raw = raw_at(fixture, attempt, e['kind'], True)
            if e['kind'] not in ('raw_request', 'raw_response', 'errors', 'attempt_event'):
                require(raw == expected[e['kind']], 'source evidence binding')
        event = event_at(fixture, attempt)
        require(isinstance(event, dict) and set(event) == EVENT_KEYS, 'event fields')
        require(all(event[k] == attempt[k] for k in
                    ('attempt_id', 'attempt_order', 'transport_outcome')), 'event identity/outcome')
        for key in ('started_at', 'finished_at'):
            require(event[key] == '2000-01-01T00:00:00Z', 'event UTC')
        require(type(event['truncated']) is bool and
                isinstance(event['exhausted_budgets'], list) and
                all(x in ('total_tokens', 'context', 'output', 'wall_time', 'tool_calls', 'quota')
                    for x in event['exhausted_budgets']), 'event interruption')
        require(event['cache_events'] == [] and event['queue_time_ms'] is None and
                event['tool_time_ms'] is None, 'event unavailable accounting')
        require(attempt['response_parsing'] == response_state(fixture, attempt), 'response parsing')
        request = raw_at(fixture, attempt, 'raw_request')
        binding = 'byte_match' if request == expected['raw_request'] else 'not_bound'
        require(attempt['input_binding'] == binding, 'request binding label')
        require(legacy_result(fixture, attempt, source, legacy) in ('pass', 'unavailable'),
                'legacy record mismatch')
    return 'pass'


def accounting(fixture, source, legacy, consistent):
    """Inventory supplied bytes even on rejected fixtures; never infer semantic scores.

    present_slots means referenced planned slots, not validated links. A malformed
    envelope's inventories are diagnostic only. Outcome counts read event bytes;
    parse counts read original response bytes, never reported response_parsing.
    """
    attempts = fixture['envelope']['attempts']
    slots = parse(source['base']['plan_text'])['slots']
    slot_ids = {s['record_id'] for s in slots}
    refs = [a['slot_ref'] for a in attempts]
    present = slot_ids & set(refs)
    states = [response_state(fixture, a) for a in attempts]
    events = []
    for a in attempts:
        try:
            events.append(event_at(fixture, a))
        except (ValueError, KeyError, TypeError, UnicodeError):
            events.append({})
    legacy_states = [legacy_result(fixture, a, source, legacy) for a in attempts]
    complete = consistent and len(attempts) == len(slots) and all(refs.count(s) == 1 for s in slot_ids)
    if complete:
        for attempt, event, old in zip(attempts, events, legacy_states):
            record = attempt['legacy_record']
            if (old != 'pass' or event.get('transport_outcome') != 'succeeded'
                    or attempt['input_binding'] != 'byte_match'):
                complete = False
                break
            f = {k: v['value'] for k, v in record['fields'].items()}
            if not (f['outcome'] == f['answer_status'] == 'complete' and not f['errors']
                    and not f['truncated'] and not f['exhausted_budgets']
                    and all(c['error'] is None for c in f['tool_calls'])):
                complete = False
    return {
        'planned_slots': len(slots), 'present_slots': len(present),
        'missing_slots': len(slot_ids - present), 'attempts_retained': len(attempts),
        'unplanned_attempts': sum(r not in slot_ids for r in refs),
        'multiple_attempt_slots': sum(refs.count(s) > 1 for s in slot_ids),
        'responses_present': sum(entry(a, 'raw_response') is not None and
            entry(a, 'raw_response').get('presence') == 'present' for a in attempts),
        'responses_absent': states.count('absent'),
        'response_evidence_missing': states.count('missing_evidence'),
        'empty_responses': states.count('empty'),
        'invalid_utf8_responses': states.count('invalid_utf8'),
        'malformed_json_responses': states.count('malformed_json'),
        'unreadable_responses': states.count('unreadable'),
        'parseable_responses': states.count('parseable_json'),
        'legacy_records_present': sum(a['legacy_record'] is not None for a in attempts),
        'legacy_valid_records': legacy_states.count('pass'),
        'failed_attempts': sum(e.get('transport_outcome') == 'failed' for e in events),
        'interrupted_attempts': sum(e.get('transport_outcome') == 'interrupted' for e in events),
        'unsupported_attempts': sum(e.get('transport_outcome') == 'unsupported' for e in events),
        'succeeded_attempts': sum(e.get('transport_outcome') == 'succeeded' for e in events),
        'outcome_unavailable_attempts': sum(e.get('transport_outcome') not in OUTCOMES for e in events),
        'selection_unresolved_slots': sum(refs.count(s) > 1 for s in slot_ids),
        'synthetic_complete_comparisons': int(complete),
        'correctness_denominator': 4, 'grounding_denominator': 4,
    }


def retained_payloads(fixture):
    """Expose substantive byte observations, independently of declared sizes/hashes."""
    observed = []
    for attempt in fixture['envelope']['attempts']:
        row = {k: attempt[k] for k in ('attempt_id', 'attempt_order', 'slot_ref')}
        row['response_state'] = response_state(fixture, attempt)
        for kind in ('raw_request', 'raw_response', 'errors'):
            item = entry(attempt, kind)
            if item is None:
                row[kind] = {'presence': 'missing_evidence'}
            elif item['presence'] == 'absent':
                row[kind] = {'presence': 'absent'}
            else:
                try:
                    raw = raw_at(fixture, attempt, kind)
                    row[kind] = {'presence': 'present', 'byte_size': len(raw),
                                 'sha256': sha(raw), 'round_trip': bytes.fromhex(raw.hex()) == raw}
                except (ValueError, KeyError, TypeError):
                    row[kind] = {'presence': 'unreadable'}
        observed.append(row)
    return observed


def mutate(fixture, operations):
    for op, pointer, value in operations:
        require(pointer.startswith('/'), 'mutation pointer')
        parts = pointer[1:].split('/')
        parent = fixture
        for key in parts[:-1]:
            parent = parent[int(key)] if isinstance(parent, list) else parent[key]
        key = int(parts[-1]) if isinstance(parent, list) else parts[-1]
        if op == 'set':
            parent[key] = deepcopy(value)
        elif op == 'delete':
            del parent[key]
        else:
            raise ValueError('mutation operation')


def main():
    data = parse(DATA.read_text(encoding='utf-8'))
    require(data['schema_version'] == 1 and data['predeclared'] is True, 'saved expectations')
    require(data['contract']['envelope_version'] == FORMAT, 'contract version')
    pins = data['pins']
    require(len({p['path'] for p in pins}) == len(pins), 'duplicate source pin')
    required_pins = {'benchmark/project-run-binding-0138.json',
        'benchmark/project-run-binding-0138.md', 'benchmark/verify_project_run_binding_0138.py',
        'benchmark/scripts/run_record.py', 'benchmark/baseline/run-record.template.json',
        'benchmark/baseline/run-manifest.template.json', 'benchmark/project-paired-0136.json',
        'benchmark/preparation.json'}
    require(required_pins <= {p['path'] for p in pins}, 'required source pins')
    for pin in pins:
        path = ROOT / pin['path']
        require(not Path(pin['path']).is_absolute() and '..' not in Path(pin['path']).parts
                and path.resolve().is_relative_to(ROOT) and
                all(not part.is_symlink() for part in [path, *path.parents] if part.is_relative_to(ROOT)),
                'source path')
        raw = path.read_bytes()
        require(0 < len(raw) < 2_000_000 and len(raw) == pin['byte_size'] and
                sha(raw) == pin['sha256'], 'source pin: ' + pin['path'])
    group = runpy.run_path(str(ROOT / 'benchmark/verify_project_run_binding_0138.py'))
    legacy = group['load_legacy_functions']()
    original = parse((ROOT / 'benchmark/project-run-binding-0138.json').read_text())
    source = {'base': original['rehearsal']['fixture'],
              'template': parse((ROOT / 'benchmark/baseline/run-record.template.json').read_text())}
    source['manifest'] = parse(source['base']['manifest_text'])
    require(set(data['contract']['required_evidence']) == set(group['EVIDENCE_KINDS']) | {'attempt_event'},
            'contract evidence kinds')
    for dim in ('correctness', 'grounding'):
        require(source['manifest']['fields']['fixed_denominators']['value'][dim] ==
                {'ids': ['D1', 'D2', 'D3', 'D4'], 'total': 4}, 'source denominators')
    compatibility = []
    for saved in data['compatibility']['observed']:
        control = next(c for c in original['rehearsal']['controls'] if c['name'] == saved['name'])
        fixture = deepcopy(source['base'])
        group['mutate'](fixture, control['mutations'])
        observed = group['legacy_decision'](fixture, legacy)
        raw = fixture['records'][1]['fields']['raw_response']['value']['text'].encode()
        require(observed == saved['observed'] and raw.hex() == saved['response_utf8_hex'] and
                len(raw) == saved['byte_size'] and sha(raw) == saved['sha256'], 'legacy compatibility')
        compatibility.append({'name': saved['name'], 'result': observed, 'byte_size': len(raw)})
    require(len(compatibility) == 4, 'compatibility coverage')
    stages = data['expectation_stages']
    require([s['stage'] for s in stages] == ['initial', 'extension'] and
            [len(s['controls']) for s in stages] == [76, 16] and
            [name for stage in stages for name in stage['controls']] ==
            [c['name'] for c in data['controls']], 'expectation stage inventory')
    observed = []
    names = set()
    for control in data['controls']:
        require(control['name'] not in names, 'duplicate control')
        names.add(control['name'])
        fixture = deepcopy(data['fixture'])
        mutate(fixture, control['mutations'])
        try:
            decision = validate(fixture, source, group, legacy)
        except (ValueError, KeyError, TypeError, UnicodeError) as exc:
            decision = str(exc)
        counts = accounting(fixture, source, legacy, decision == 'pass')
        require(decision == control['expected'], control['name'] + ': decision ' + decision)
        require(counts == control['expected_accounting'], control['name'] + ': accounting ' +
                json.dumps({k: [control['expected_accounting'].get(k), v]
                    for k, v in counts.items() if control['expected_accounting'].get(k) != v}))
        observed.append({'name': control['name'], 'decision': decision, 'accounting': counts,
                         'retained_payloads': retained_payloads(fixture)})
    require(any(c['decision'] == 'pass' for c in observed) and
            any(c['decision'] != 'pass' for c in observed), 'positive/negative controls')
    require(set(data['actual_counts']) == {'real_admissions', 'model_executions',
            'reader_executions', 'native_executions', 'scored_runs', 'semantic_passes',
            'real_complete_comparisons'} and
            all(type(v) is int and v == 0 for v in data['actual_counts'].values()) and
            data['actual_counts'] and data['benchmark_ready'] is False and
            data['actual_costs'] == {'provider': None, 'infrastructure': None, 'probe': None} and
            data['semantic_scores'] == {'correctness': None, 'grounding': None, 'fidelity': None},
            'actual execution/score boundary')
    result = subprocess.run([sys.executable, '-I', str(ROOT / 'benchmark/verify_project_run_binding_0138.py')],
                            capture_output=True, text=True, check=False)
    require(result.returncode == 0, 'retained grouping checker failed: ' + result.stderr)
    retained = parse(result.stdout)
    require(retained['status'] == 'pass' and retained['controls_matched'] == 60,
            'retained grouping results')
    print(json.dumps({'status': 'pass', 'scope': 'synthetic retention consistency only',
        'controls_matched': len(observed), 'compatibility': compatibility,
        'retained_grouping': {'exit': result.returncode, 'controls_matched': retained['controls_matched'],
                              'stdout_sha256': sha(result.stdout.encode())},
        'observed': observed, 'actual_counts': data['actual_counts'],
        'actual_costs': data['actual_costs'], 'semantic_scores': data['semantic_scores'],
        'real_admission': 'blocked', 'trusted_authority': 'unavailable',
        'method_accepted': False, 'benchmark_ready': False}, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as exc:
        print('attempt-evidence-0143: ' + str(exc), file=sys.stderr)
        sys.exit(1)
