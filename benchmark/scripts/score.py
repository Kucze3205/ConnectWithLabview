#!/usr/bin/env python3
"""Deterministic public development scoring; no native reader is executed.

Computation receives only submissions, probes, frozen denominators, inventory keys
and alignment facts. Authored expected outcomes enter only the comparison stage.
XML credit is conditional on the provisional key; current-evidence credit is
reported separately. This same-role-family implementation is unreviewed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'benchmark/results/challenges.json'
FIXTURES = ('library-icon-tests', 'library-specialty', 'vi-actor-core-native-gap')
DIMS = {'correctness': 'answer_correctness', 'grounding': 'source_grounding',
        'fidelity': 'reading_fidelity'}
CATEGORIES = ('correct', 'partial', 'incorrect', 'missing', 'unsupported', 'unverified', 'error')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def counts(values):
    values = list(values)
    return {x: values.count(x) for x in CATEGORIES}


def assessment(required, extras):
    if not required:
        return 'unverified'
    values = list(required) + list(extras)
    for outcome in ('incorrect', 'unverified'):
        if outcome in values:
            return outcome
    if all(x == 'correct' for x in values):
        return 'correct'
    if any(x in ('correct', 'partial') for x in values):
        return 'partial'
    if 'error' in values:
        return 'error'
    if all(x == 'unsupported' for x in required):
        return 'unsupported'
    return 'missing'


def raw_record(record, materialized, label, problems, allow_incomplete=False):
    text = record['text']
    if digest(text.encode('utf-8')) != record['sha256']:
        problems.append(label + ': raw SHA256 mismatch')
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        if not allow_incomplete:
            problems.append(label + ': invalid raw JSON')
        return None
    if parsed != materialized:
        problems.append(label + ': raw and materialized content disagree')
    return parsed


def citation_support(citations, key):
    # Whole citation identities, including original hash and exact property,
    # must match a keyed supporting locator. Existence alone earns no credit.
    if not citations:
        return 'missing'
    if not key.get('citations'):
        return 'unverified'
    return 'correct' if all(c in key['citations'] for c in citations) else 'incorrect'


def extra_outcome(item, channel, keys, key_absent):
    value = item.get('answer' if channel == 'answer' else 'value')
    match = re.fullmatch(r'The XML-parsed literal at (.+) has UTF-8 byte length (\d+)\.', value or '')
    key = None
    if match:
        scope, length = match.groups()
        for candidate in keys.values():
            if any(c.get('locator', {}).get('expression') == scope for c in candidate.get('citations', [])):
                key = candidate
                break
        if key is not None and isinstance(key['atomic_fact'].get('value'), str) and not key_absent:
            actual = len(key['atomic_fact']['value'].encode('utf-8'))
            correct = int(length) == actual
            if channel == 'reader':
                outcomes = {'fidelity': 'unverified' if correct else 'incorrect'}
            else:
                grounding = citation_support(item.get('citations', []), key)
                outcomes = {'correctness': 'correct' if correct else 'incorrect',
                            'grounding': grounding if correct else 'incorrect'}
            return outcomes, {'actual_byte_length': actual, 'utf8_literal': key['atomic_fact']['value']}
    return ({'fidelity': 'unverified'} if channel == 'reader' else
            {'correctness': 'unverified', 'grounding': 'unverified'}), None


def compute(source, denominators, inventory, submitted, probe, alignment):
    problems = []
    answer = submitted['answer_record']
    response = submitted['reader_response']
    operation = probe['simulated_operation']
    raw_record(submitted['raw_answer_record'], answer, 'answer', problems)
    parsed = raw_record(submitted['raw_reader_response'], response, 'reader', problems,
                        allow_incomplete=operation.get('truncated') or not submitted['raw_reader_response']['text'])
    request = probe['raw_request'].encode('utf-8')
    if digest(request) != probe['raw_request_sha256'] or json.loads(request) != probe['request']:
        problems.append('probe: raw request identity mismatch')
    # Incomplete raw bytes supply no invented observations. Simulated conditions
    # are retained as operational evidence, never represented as native runs.
    observations = parsed.get('observations', []) if isinstance(parsed, dict) else []
    keys = {k['claim_id']: k for k in inventory['reference_inventory']}
    align = {a['observation_id']: {k: a[k] for k in
             ('aligned_claim_id', 'native_reference', 'reference_scope', 'xml_expected')} for a in alignment}
    required = {d: denominators[name]['required_ids'] for d, name in DIMS.items()}
    for d, name in DIMS.items():
        if len(set(required[d])) != denominators[name]['count'] or len(required[d]) != len(set(required[d])):
            problems.append(d + ': invalid frozen denominator')
    evidence_record = submitted.get('evidence_record', {})
    key_absent = 'independent_key' in evidence_record and evidence_record['independent_key'] is None
    per_id = {d: {} for d in DIMS}
    extras, duplicates, contradictions = [], [], []
    details = {d: {} for d in DIMS}

    for channel, items, id_field, value_field, dimensions in (
        ('answer', answer.get('claims', []), 'claim_id', 'answer', ('correctness', 'grounding')),
        ('reader', observations, 'observation_id', 'value', ('fidelity',))):
        groups = {}
        prefix = '/claims/' if channel == 'answer' else '/observations/'
        for index, item in enumerate(items):
            identifier = item[id_field]
            pointer = prefix + str(index)
            if identifier not in required[dimensions[0]]:
                outcomes, derivation = extra_outcome(item, channel, keys, key_absent)
                entry = {'channel': channel, 'assertion_id': identifier, 'assertion': item.get(value_field),
                         'raw_json_pointer': pointer, 'outcomes': outcomes, 'required_credit': 0,
                         'derivation': derivation}
                extras.append(entry)
            else:
                groups.setdefault(identifier, []).append((item, pointer))
        status = answer.get('status') if channel == 'answer' else response.get('status')
        for identifier in required[dimensions[0]]:
            records = groups.get(identifier, [])
            values = [record[value_field] for record, _ in records]
            unique = {json.dumps(v, sort_keys=True) for v in values}
            duplicate_count = len(values) - len(unique)
            contradiction = len(unique) > 1
            if duplicate_count:
                duplicates.append({'channel': channel, 'required_id': identifier, 'count': duplicate_count,
                                   'raw_json_pointers': [p for _, p in records]})
            if contradiction:
                contradictions.append({'channel': channel, 'required_id': identifier, 'count': 1,
                                       'raw_json_pointers': [p for _, p in records], 'assertions': values})
            if channel == 'answer':
                key = keys.get(identifier)
                target = key['atomic_fact'].get('value') if key else None
                native = key.get('native_reference', 'unavailable') if key else 'unavailable'
            else:
                key = align.get(identifier)
                target = key['xml_expected'] if key else None
                native = key.get('native_reference', 'unavailable') if key else 'unavailable'
            common = None
            if contradiction:
                common = 'incorrect'
            elif status == 'unsupported' and not records:
                common = 'unsupported'
            elif channel == 'reader' and (status == 'error' or operation.get('error') or operation.get('exit_code')) and not records:
                common = 'error'
            elif not records:
                common = 'missing'
            elif key_absent or key is None or target is None:
                common = 'unverified'
            elif any(v != target for v in values):
                common = 'incorrect'
            elif channel == 'reader' and any(r.get('scope') != key['reference_scope'] for r, _ in records):
                common = 'incorrect'
            elif channel == 'reader' and native == 'unavailable':
                common = 'unverified'
            else:
                common = 'correct'
            for dimension in dimensions:
                outcome = common
                if dimension == 'grounding' and common == 'correct':
                    supports = [citation_support(r.get('citations', []), key) for r, _ in records]
                    outcome = assessment(supports, [])
                per_id[dimension][identifier] = outcome
                details[dimension][identifier] = {'outcome': outcome, 'submitted_values': values,
                    'reference_value': target, 'native_reference': native,
                    'raw_json_pointers': [p for _, p in records]}

    extra_values = {d: [e['outcomes'][d] for e in extras if d in e['outcomes']] for d in DIMS}
    dimensions = {d: assessment(per_id[d].values(), extra_values[d]) for d in DIMS}
    # Independent XML review is unavailable: conditional matches are not current
    # evidence passes. Explicit falsifications remain visible in both views.
    current = {d: {i: ('unverified' if v == 'correct' else v) for i, v in ids.items()}
               for d, ids in per_id.items()}
    current_dimensions = {d: assessment(current[d].values(),
                           ['unverified' if v == 'correct' else v for v in extra_values[d]]) for d in DIMS}
    return {'per_id': per_id, 'dimensions': dimensions,
            'counts': {d: counts(per_id[d].values()) for d in DIMS},
            'required_ids': required, 'fixed_denominators': {d: len(required[d]) for d in DIMS},
            'extra_counts': {d: counts(extra_values[d]) for d in DIMS},
            'extras_ledger': extras, 'duplicates_ledger': duplicates, 'contradictions_ledger': contradictions,
            'current_evidence_per_id': current, 'current_evidence_dimensions': current_dimensions,
            'details': details, 'cannot_evaluate_reasons': problems,
            'operation': operation, 'limitations': {'answer': answer.get('limitations'),
            'reader': response.get('limitations')}, 'declared_execution': probe['actual_execution'],
            'evidence_record': evidence_record}


def ledger_projection(entries, kind):
    if kind == 'extras_ledger':
        fields = ('channel', 'assertion_id', 'assertion', 'raw_json_pointer', 'outcomes', 'required_credit', 'derivation')
    else:
        fields = ('channel', 'required_id', 'count', 'raw_json_pointers')
    return [{k: e[k] for k in fields if k in e} for e in entries]


def compare(computed, expected):
    mismatches = []
    fields = ('per_id', 'dimensions', 'counts', 'required_ids', 'fixed_denominators', 'extra_counts',
              'current_evidence_per_id', 'current_evidence_dimensions',
              'extras_ledger', 'duplicates_ledger', 'contradictions_ledger')
    def walk(actual, wanted, path):
        if isinstance(actual, dict) and isinstance(wanted, dict):
            for key in sorted(set(actual) | set(wanted)):
                walk(actual.get(key), wanted.get(key), path + '/' + key)
        elif actual != wanted:
            mismatches.append({'location': path, 'computed': actual, 'expected': wanted,
                               'reason': 'Independently computed submission/key result differs from frozen expectation.'})
    for field in fields:
        actual, wanted = computed[field], expected[field]
        if field.endswith('_ledger'):
            actual, wanted = ledger_projection(actual, field), ledger_projection(wanted, field)
        walk(actual, wanted, '/' + field)
    return mismatches


def generate():
    fixtures = []
    total = matched = unevaluable = 0
    for fixture_id in FIXTURES:
        path = ROOT / 'benchmark/challenges' / (fixture_id + '.json')
        data_bytes = path.read_bytes()
        fixture = json.loads(data_bytes)
        inventory_bytes = (ROOT / fixture['source']['inventory_path']).read_bytes()
        if digest(inventory_bytes) != fixture['source']['inventory_sha256']:
            raise ValueError(fixture_id + ': inventory SHA256 mismatch')
        inventory = json.loads(inventory_bytes)
        controls = []
        for control in fixture['controls']:
            # Never pass expected, purpose, evidence, or alignment's authored
            # expected_outcome to the computation function.
            computed = compute(fixture['source'], fixture['denominators'], inventory,
                               control['submitted'], control['probe'], control['alignment'])
            expected = control['expected']
            mismatches = compare(computed, expected)
            reasons = computed['cannot_evaluate_reasons']
            match = not mismatches and not reasons
            controls.append({'control': control['name'], 'computed': computed,
                             'expected': expected, 'match': match, 'mismatches': mismatches,
                             'cannot_evaluate': bool(reasons)})
            total += 1
            matched += int(match)
            unevaluable += int(bool(reasons))
        fixtures.append({'fixture_id': fixture_id, 'path': str(path.relative_to(ROOT)),
                         'sha256': digest(data_bytes), 'controls': controls})
    return {'schema_version': 1, 'development_only': True, 'independently_reviewed': False,
            'native_evidence_available': False, 'quality_measured': False,
            'method': 'Conditional provisional XML key comparison; native matches stay unverified. Current-evidence view separately retains pending XML review. Synthetic fixture scoring is not reader execution.',
            'totals': {'fixtures': len(fixtures), 'controls': total, 'matches': matched,
                       'mismatches': total - matched, 'cannot_evaluate': unevaluable},
            'fixtures': fixtures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare generated bytes without writing')
    args = parser.parse_args()
    result = generate()
    rendered = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode('utf-8')
    if args.check:
        if not OUT.is_file() or OUT.read_bytes() != rendered:
            print('results/challenges.json is missing or differs from deterministic regeneration', file=sys.stderr)
            return 1
    else:
        OUT.write_bytes(rendered)
    print(json.dumps(result['totals'], sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
