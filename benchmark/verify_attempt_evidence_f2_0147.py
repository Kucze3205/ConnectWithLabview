#!/usr/bin/env python3
"""Saved #669 F2 regressions; standard library, repository bytes, no real runs.

Public synthetic expectations were fixed before pre-correction execution. They
follow the pinned two-slot plan and diagnostic-retention contract, not checker
outputs. No session files, evaluator, runner, model or native execution is used.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
UNPLANNED = 'synthetic-unplanned-arm'
# Derived from the source plan, the two intact attempts and their event/response
# bytes. The mutation preserves slot_ref, payloads and all evidence entries.
COUNTS = {
    'planned_slots': 2, 'present_slots': 2, 'missing_slots': 0,
    'attempts_retained': 2, 'unplanned_attempts': 0, 'multiple_attempt_slots': 0,
    'responses_present': 2, 'responses_absent': 0, 'response_evidence_missing': 0,
    'empty_responses': 0, 'invalid_utf8_responses': 0, 'malformed_json_responses': 0,
    'unreadable_responses': 0, 'parseable_responses': 2,
    'legacy_records_present': 2, 'legacy_valid_records': 2,
    'failed_attempts': 0, 'interrupted_attempts': 0, 'unsupported_attempts': 0,
    'succeeded_attempts': 2, 'outcome_unavailable_attempts': 0,
    'selection_unresolved_slots': 0, 'synthetic_complete_comparisons': 1,
    'correctness_denominator': 4, 'grounding_denominator': 4,
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False).encode('utf-8')


def setup():
    # Reuse only setup: it verifies source pins and loads inspected legacy helpers.
    f1 = runpy.run_path(str(ROOT / 'benchmark/verify_attempt_evidence_f1_0145.py'))
    return f1['setup']()


def build_cases(fixture):
    cases = []
    for index, arm in enumerate(('no-tool', 'tool')):
        changed = deepcopy(fixture)
        attempt = changed['envelope']['attempts'][index]
        assert attempt['arm'] == arm
        attempt['arm'] = UNPLANNED
        attempt['legacy_record']['fields']['arm']['value'] = UNPLANNED
        cases.append(('unplanned arm replacing ' + arm, changed, index))
    cases.append(('consistent positive control', deepcopy(fixture), None))
    return cases


def catalog(fixture):
    """Independent byte inventory, including unreferenced catalog originals."""
    return {ref: {'hex': item['hex'], 'byte_size': len(bytes.fromhex(item['hex'])),
                  'sha256': sha(bytes.fromhex(item['hex']))}
            for ref, item in fixture['payloads'].items()}


def retained_expected(fixture):
    # Decode source bytes directly, without checker payload/response helpers.
    rows = []
    for attempt in fixture['envelope']['attempts']:
        row = {k: attempt[k] for k in ('attempt_id', 'attempt_order', 'slot_ref')}
        entries = {e['kind']: e for e in attempt['evidence']}
        raw_response = bytes.fromhex(fixture['payloads'][entries['raw_response']['payload_ref']]['hex'])
        json.loads(raw_response.decode('utf-8'))
        row['response_state'] = 'parseable_json'
        for kind in ('raw_request', 'raw_response', 'errors'):
            item = entries[kind]
            assert item['presence'] == 'present'
            raw = bytes.fromhex(fixture['payloads'][item['payload_ref']]['hex'])
            row[kind] = {'presence': 'present', 'byte_size': len(raw),
                         'sha256': sha(raw), 'round_trip': True}
        rows.append(row)
    return rows


def expectations(fixture, source):
    """Fixed outcomes with independently checked source-byte prerequisites."""
    plan = json.loads(source['base']['plan_text'])
    assert len(plan['slots']) == 2 and len(plan['comparisons']) == 1
    assert [s['arm'] for s in plan['slots']] == ['no-tool', 'tool']
    assert [a['arm'] for a in source['base']['attempts']] == ['no-tool', 'tool']
    assert UNPLANNED not in {a['arm'] for a in source['base']['attempts']}
    assert len(source['base']['source_inventory']['original_artifact_set_and_hashes']) == 1
    assert len(fixture['payloads']) == 48 and len(fixture['envelope']['attempts']) == 2
    for attempt in fixture['envelope']['attempts']:
        entries = {e['kind']: e for e in attempt['evidence']}
        assert len(entries) == len(attempt['evidence']) == 24
        event = json.loads(bytes.fromhex(fixture['payloads'][entries['attempt_event']['payload_ref']]['hex']))
        assert event['transport_outcome'] == 'succeeded'
        fields = {k: v['value'] for k, v in attempt['legacy_record']['fields'].items()}
        assert fields['outcome'] == fields['answer_status'] == 'complete'
        assert not fields['errors'] and not fields['truncated'] and not fields['exhausted_budgets']
        assert all(c['error'] is None for c in fields['tool_calls'])
    for dimension in ('correctness', 'grounding'):
        assert source['manifest']['fields']['fixed_denominators']['value'][dimension] == {
            'ids': ['D1', 'D2', 'D3', 'D4'], 'total': 4}
    expected = []
    for name, changed, index in build_cases(fixture):
        counts = dict(COUNTS)
        states = ['pass', 'pass']
        if index is not None:
            states[index] = 'invalid'
            counts['legacy_valid_records'] = 1
            counts['synthetic_complete_comparisons'] = 0
        expected.append({'name': name, 'mutated_index': index,
                         'fixture_sha256': sha(canonical(changed)),
                         'decision': 'pass' if index is None else 'slot identity',
                         'legacy_results': states, 'accounting': counts,
                         'direct_consistent_accounting': dict(counts),
                         'retained_payloads': retained_expected(fixture),
                         'payload_catalog': catalog(fixture),
                         'fixture_unchanged_by_observation': True})
    return expected


def observe(checker, group, legacy, source, fixture):
    before = canonical(fixture)
    try:
        decision = checker['validate'](fixture, source, group, legacy)
    except ValueError as exc:
        decision = str(exc)
    result = {'decision': decision,
              'legacy_results': [checker['legacy_result'](fixture, a, source, legacy)
                                 for a in fixture['envelope']['attempts']],
              'accounting': checker['accounting'](fixture, source, legacy, decision == 'pass'),
              'direct_consistent_accounting': checker['accounting'](fixture, source, legacy, True),
              'retained_payloads': checker['retained_payloads'](fixture),
              'payload_catalog': catalog(fixture),
              'fixture_unchanged_by_observation': canonical(fixture) == before}
    return result


def main():
    checker, group, legacy, data, source = setup()
    saved = expectations(data['fixture'], source)
    matched = []
    for (name, fixture, index), expected in zip(build_cases(data['fixture']), saved):
        observed = observe(checker, group, legacy, source, fixture)
        for key, value in observed.items():
            assert value == expected[key], name + ': ' + key
        assert sha(canonical(fixture)) == expected['fixture_sha256'], name + ': fixture bytes changed'
        matched.append({'name': name, 'decision': observed['decision'],
                        'legacy_results': observed['legacy_results'],
                        'complete': observed['accounting']['synthetic_complete_comparisons'],
                        'direct_consistent_complete': observed['direct_consistent_accounting']['synthetic_complete_comparisons'],
                        'attempts_retained': observed['accounting']['attempts_retained'],
                        'payloads_retained': len(observed['payload_catalog'])})
    # Exactly one F1 invocation also checks the saved 92 and grouping 60 controls.
    compatibility = subprocess.run(
        [sys.executable, '-I', str(ROOT / 'benchmark/verify_attempt_evidence_f1_0145.py')],
        capture_output=True, text=True, check=False)
    assert compatibility.returncode == 0, 'F1 failed: ' + compatibility.stderr.strip()
    summary = json.loads(compatibility.stdout)
    assert summary == {'status': 'pass', 'f1_controls_matched': 8,
                       'saved_controls_matched': len(data['controls']),
                       'retained_grouping_controls': 60,
                       'consistent_complete_comparisons': 1, 'benchmark_ready': False}, 'F1 summary'
    print(json.dumps({'status': 'pass', 'f2_controls_matched': len(matched),
                      'observed': matched, 'f1_compatibility': {
                          'exit': compatibility.returncode, 'summary': summary,
                          'stdout_sha256': sha(compatibility.stdout.encode()),
                          'stderr_sha256': sha(compatibility.stderr.encode())},
                      'actual_counts': data['actual_counts'], 'benchmark_ready': False}, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (AssertionError, ValueError, KeyError, TypeError, UnicodeError, OSError, StopIteration) as exc:
        print('attempt-evidence-f2-0147: ' + str(exc), file=sys.stderr)
        sys.exit(1)
