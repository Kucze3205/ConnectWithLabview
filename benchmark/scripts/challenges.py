#!/usr/bin/env python3
"""Materialize public development challenge inputs and frozen expectations.

Stdlib only; no reader, native runtime or scoring implementation is invoked.
Expected ledgers are authored fixture data, not results from scoring submissions.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = ROOT / 'benchmark/cases/dev'
OUT_DIR = ROOT / 'benchmark/challenges'
CASE_IDS = ('library-icon-tests', 'library-specialty', 'vi-actor-core-native-gap')
DIMENSIONS = {'correctness': 'answer_correctness',
              'grounding': 'source_grounding', 'fidelity': 'reading_fidelity'}
OUTCOMES = ('correct', 'partial', 'incorrect', 'missing', 'unsupported',
            'unverified', 'error')
LIMITATION = ('Native references and independent review are unavailable. '
              'XML literal expectations are provisional author expectations. '
              'Null native slots assert no semantic answer and earn no credit.')


def dumps(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory_evidence(case, claim_id):
    row = next(r for r in case['reference_inventory'] if r['claim_id'] == claim_id)
    return {'inventory': 'benchmark/cases/dev/' + case['case_id'] + '.json',
            'claim_id': claim_id, 'atomic_fact': deepcopy(row['atomic_fact']),
            'citations': deepcopy(row['citations']),
            'reference_status': row['reference_status']}


def answer_record(case):
    return {'case_id': case['case_id'], 'status': 'complete-with-reference-gaps',
            'claims': [{'claim_id': r['claim_id'],
                        'answer': r['atomic_fact']['value'],
                        'conditions': deepcopy(r['conditions']),
                        'citations': deepcopy(r['citations'])}
                       for r in case['reference_inventory']],
            'limitations': LIMITATION + ' Affected native IDs: ' +
                ', '.join(r['claim_id'] for r in case['reference_inventory']
                          if r['atomic_fact']['value'] is None)}


def reader_record(case):
    by_id = {r['claim_id']: r for r in case['reference_inventory']}
    return {'probe_id': case['reader_probe_contract']['probe_id'],
            'status': 'complete-with-reference-gaps',
            'observations': [
                {'observation_id': r['observation_id'],
                 'scope': r['scope'], 'value': r['expected'],
                 'conditions': deepcopy(by_id[r['aligned_claim_id']]['conditions']),
                 'citations': deepcopy(by_id[r['aligned_claim_id']]['citations'])}
                for r in case['reader_reference_inventory']],
            'limitations': LIMITATION}


def base_ledger(case):
    answer = {r['claim_id']: {
        'outcome': 'correct' if r['citations'] else 'unverified',
        'evidence': inventory_evidence(case, r['claim_id']),
        'reason': ('Exact provisional XML literal and supporting original locator.'
                   if r['citations'] else 'Native key and supporting native locator unavailable.')}
        for r in case['reference_inventory']}
    fidelity = {r['observation_id']: {
        'outcome': 'unverified',
        'evidence': inventory_evidence(case, r['aligned_claim_id']),
        'reason': 'No independently checked native reference; matching XML is insufficient.'}
        for r in case['reader_reference_inventory']}
    return {'correctness': deepcopy(answer), 'grounding': deepcopy(answer),
            'fidelity': fidelity}


def set_outcome(control, dimension, item_id, outcome, reason):
    control['expected']['per_id'][dimension][item_id].update(
        outcome=outcome, reason=reason)


def control(case, name):
    return {'name': name,
            'submitted': {'answer_record': answer_record(case),
                          'reader_response': reader_record(case)},
            'probe': {'request': deepcopy(case['reader_probe_contract']),
                      'input_kind': 'synthetic-fixture-not-reader-execution',
                      'reader_revision': None, 'environment': None,
                      'timestamps': None, 'exit_code': 0, 'error': None,
                      'truncated': False},
            'coverage': {'planned_cases': 1, 'attempted_cases': 0,
                         'executed_cases': 0, 'scored_cases': 0},
            'expected': {'dimensions': {'correctness': 'unverified',
                                        'grounding': 'unverified',
                                        'fidelity': 'unverified'},
                         'per_id': base_ledger(case),
                         'counts': {}, 'extras_ledger': [],
                         'duplicates': [], 'contradictions': [],
                         'assessment_basis': LIMITATION},
            'gaps': []}


def add_extra(case, item, target, kind):
    """Materialize a distinct relational assertion, with explicit evidence."""
    a = next(r for r in case['reference_inventory'] if r['claim_id'] == 'A0006')
    b = next(r for r in case['reference_inventory'] if r['claim_id'] == 'A0009')
    texts = {
        'true': 'The literal @Type values of Library Item[1] and Item[2] are equal.',
        'false': 'The literal @Type values of Library Item[1] and Item[2] differ.',
        'unverified': 'Library Item[1] resolves successfully in native LabVIEW.'}
    evidence_ids = ['N0001'] if kind == 'unverified' else ['A0006', 'A0009']
    evidence = [inventory_evidence(case, i) for i in evidence_ids]
    citations = (deepcopy(a['citations'] + b['citations']) if kind == 'true'
                 else deepcopy(case['reference_inventory'][0]['citations']))
    extra_id = 'X-' + target + '-' + kind
    if target == 'answer':
        rows = item['submitted']['answer_record']['claims']
        rows.append({'claim_id': extra_id, 'answer': texts[kind],
                     'conditions': deepcopy(a['conditions']), 'citations': citations})
        outcomes = {'correctness': {'true': 'correct', 'false': 'incorrect',
                                    'unverified': 'unverified'}[kind],
                    'grounding': {'true': 'correct', 'false': 'incorrect',
                                  'unverified': 'incorrect'}[kind]}
    else:
        rows = item['submitted']['reader_response']['observations']
        rows.append({'observation_id': extra_id, 'scope': 'additional assertion',
                     'value': texts[kind], 'conditions': deepcopy(a['conditions']),
                     'citations': citations})
        outcomes = {'fidelity': 'incorrect' if kind == 'false' else 'unverified'}
    item['expected']['extras_ledger'].append({
        'submitted_id': extra_id, 'target': target, 'assertion': texts[kind],
        'raw_pointer': ('/claims/' if target == 'answer' else '/observations/') +
                       str(len(rows) - 1),
        'outcomes': outcomes, 'evidence': evidence,
        'reason': ('The two pinned literal type values are equal.' if kind != 'unverified'
                   else 'Native resolution is unavailable; the save-version citation cannot support resolution.'),
        'required_credit': 0, 'changes_denominator': False})
    for dimension, outcome in outcomes.items():
        if outcome == 'incorrect':
            item['expected']['dimensions'][dimension] = 'incorrect'


def library_controls(case):
    controls = [control(case, 'positive-control')]
    controls[0]['gaps'] = [
        'Every required ID is submitted. N0001/N0002 have null answers and no invented supporting locators.',
        'Ten XML claims can be positive literal controls after independent checking; a fully correct 12-ID native control is unavailable.',
        'Otherwise matching reader observations remain unverified, never correct.']
    wrong = control(case, 'wrong-answer-declared-dependency')
    claim = next(r for r in wrong['submitted']['answer_record']['claims']
                 if r['claim_id'] == 'A0007')
    claim['answer'] = '../DELIBERATELY-WRONG-MEMBER.vi'
    for dimension in ('correctness', 'grounding'):
        set_outcome(wrong, dimension, 'A0007', 'incorrect',
                    'Replacement URL conflicts with the literal at the retained original supporting location.')
        wrong['expected']['dimensions'][dimension] = 'incorrect'
    wrong['gaps'] = ['Tests a declared membership/dependency URL literal, not computation or typedef impact; those native controls remain unavailable.']
    controls.append(wrong)
    for suffix in ('existing', 'unresolvable'):
        item = control(case, 'wrong-citation-' + suffix)
        claim = next(r for r in item['submitted']['answer_record']['claims']
                     if r['claim_id'] == 'A0007')
        claim['citations'] = deepcopy(case['reference_inventory'][0]['citations'])
        if suffix == 'unresolvable':
            claim['citations'][0]['locator']['expression'] = '/Library/Item[999999]/@URL'
        set_outcome(item, 'grounding', 'A0007', 'incorrect',
                    ('Existing /Library/@LVVersion does not support the unchanged member URL.'
                     if suffix == 'existing' else 'Valid positional XML syntax; Item[999999] does not exist.'))
        item['expected']['dimensions']['grounding'] = 'incorrect'
        controls.append(item)
    for target in ('answer', 'reader'):
        item = control(case, 'selective-omission-' + target)
        if target == 'answer':
            item['submitted']['answer_record']['claims'] = [
                r for r in item['submitted']['answer_record']['claims'] if r['claim_id'] != 'A0007']
            for dimension in ('correctness', 'grounding'):
                set_outcome(item, dimension, 'A0007', 'missing', 'Required claim omitted; fixed slot retained.')
        else:
            item['submitted']['reader_response']['observations'] = [
                r for r in item['submitted']['reader_response']['observations']
                if r['observation_id'] != 'R0007']
            set_outcome(item, 'fidelity', 'R0007', 'missing', 'Required observation omitted; fixed slot retained.')
        item['gaps'] = ['Overall assessment stays unverified under reference precedence; partial overall requires established native references. The omission is explicitly missing.']
        controls.append(item)
        if target == 'answer':
            with_extra = deepcopy(item)
            with_extra['name'] = 'selective-omission-answer-with-true-extra'
            add_extra(case, with_extra, 'answer', 'true')
            controls.append(with_extra)
        for kind in ('false', 'true', 'unverified'):
            item = control(case, 'extra-' + kind + '-' + target)
            add_extra(case, item, target, kind)
            controls.append(item)
        for variant in ('duplicate', 'contradiction'):
            item = control(case, variant + '-' + target)
            key = 'claims' if target == 'answer' else 'observations'
            record = item['submitted']['answer_record' if target == 'answer' else 'reader_response']
            id_key = 'claim_id' if target == 'answer' else 'observation_id'
            item_id = 'A0007' if target == 'answer' else 'R0007'
            original = next(r for r in record[key] if r[id_key] == item_id)
            second = deepcopy(original)
            if variant == 'contradiction':
                value_key = 'answer' if target == 'answer' else 'value'
                second[value_key] = 'NOT (' + str(original[value_key]) + ')'
            record[key].append(second)
            ledger = {'target': target, 'required_id': item_id,
                      'raw_pointers': ['/' + key + '/6', '/' + key + '/12'],
                      'assertions': [deepcopy(original), deepcopy(second)],
                      'evidence': inventory_evidence(case, 'A0007'),
                      'additional_required_credit': 0, 'changes_denominator': False}
            item['expected']['duplicates' if variant == 'duplicate' else 'contradictions'].append(ledger)
            if variant == 'contradiction':
                for dimension in (('correctness', 'grounding') if target == 'answer' else ('fidelity',)):
                    set_outcome(item, dimension, item_id, 'incorrect',
                                'Both the literal URL and its negation are present; retain both assertions.')
                    item['expected']['dimensions'][dimension] = 'incorrect'
            controls.append(item)
    for variant in ('empty', 'wrapper-only', 'truncated', 'unsupported', 'error'):
        item = control(case, variant + '-probe')
        record = item['submitted']['reader_response']
        if variant in ('empty', 'wrapper-only'):
            record['observations'] = []
            record['status'] = 'complete'
            record['limitations'] = ''
            outcome = 'missing'
            if variant == 'empty':
                item['probe']['raw_response_utf8'] = ''
                item['submitted']['reader_response'] = None
        elif variant == 'truncated':
            record['observations'] = record['observations'][:1]
            item['probe']['truncated'] = True
            record['status'] = 'truncated'
            outcome = 'missing'
        else:
            record['observations'] = []
            record['status'] = variant
            record['limitations'] = ('Controlled synthetic missing-runtime condition.'
                                     if variant == 'unsupported' else 'Controlled synthetic reader failure.')
            outcome = 'unsupported' if variant == 'unsupported' else 'error'
            if variant == 'error':
                item['probe'].update(exit_code=17, error='controlled synthetic reader failure')
        for observation_id in item['expected']['per_id']['fidelity']:
            set_outcome(item, 'fidelity', observation_id, outcome,
                        'Synthetic raw probe condition: ' + variant + '; no matching native observation established.')
        if variant == 'truncated':
            set_outcome(item, 'fidelity', 'R0001', 'unverified',
                        'The retained first observation has no native reference; all omitted slots remain missing.')
            outcome = 'unverified'
        item['expected']['dimensions']['fidelity'] = outcome
        controls.append(item)
    item = control(case, 'missing-key-zero-execution')
    item['reference_availability'] = {'independent_key': None, 'native_run': None,
                                      'execution_report': {'executed_tests': 0}}
    for dimension, rows in item['expected']['per_id'].items():
        for row in rows.values():
            row.update(outcome='unverified', reason='Independent key removed; no execution. Never infer a key from this submission.')
    controls.append(item)
    return controls


def constant_control(case):
    item = control(case, 'constant-export')
    # This literal is intentionally identical for both probes, including its probe ID.
    raw_record = {'probe_id': 'fixed-library-export', 'status': 'complete',
                  'observations': [
                      {'observation_id': 'R0001', 'scope': '/Library/@LVVersion', 'value': '14008000'},
                      {'observation_id': 'R0007', 'scope': '/Library/Item[1]/@URL', 'value': '../Actor/Actor.lvclass'}],
                  'limitations': ''}
    item['submitted']['reader_response'] = deepcopy(raw_record)
    item['probe']['raw_response_utf8'] = dumps(raw_record)
    item['comparison_group'] = 'identical-fixed-export-two-small-libraries'
    for observation_id, claim_id in (('R0001', 'A0001'), ('R0007', 'A0007')):
        set_outcome(item, 'fidelity', observation_id, 'incorrect',
                    'Concrete fixed export contradicts the pinned XML literal; native fidelity alignment remains unavailable.')
    for observation_id in item['expected']['per_id']['fidelity']:
        if observation_id not in ('R0001', 'R0007'):
            set_outcome(item, 'fidelity', observation_id, 'missing', 'Fixed export contains no assertion for this required observation.')
    item['expected']['dimensions']['fidelity'] = 'incorrect'
    item['contradicted_observations'] = [
        {'observation_id': r, 'evidence': inventory_evidence(case, a)}
        for r, a in (('R0001', 'A0001'), ('R0007', 'A0007'))]
    item['gaps'] = ['Discriminates literal declaration conflicts in each case; independent native-reference comparison remains unavailable.']
    return item


def vi_controls(case):
    controls = []
    for reason in ('missing-runtime', 'missing-dependency', 'missing-license', 'inaccessible-diagram'):
        item = control(case, 'unsupported-' + reason)
        item['submitted']['answer_record']['status'] = 'unsupported'
        item['submitted']['answer_record']['limitations'] = 'Controlled synthetic condition: ' + reason + '; affects N0001, N0002, N0003.'
        item['submitted']['reader_response']['status'] = 'unsupported'
        item['submitted']['reader_response']['limitations'] = 'Controlled synthetic condition: ' + reason + '; affects RN0001, RN0002, RN0003.'
        for dimension, rows in item['expected']['per_id'].items():
            for row in rows.values():
                row.update(outcome='unsupported', reason='Declared synthetic access condition: ' + reason + '; no semantic credit.')
            item['expected']['dimensions'][dimension] = 'unsupported'
        item['gaps'] = ['This is a synthetic abstention input, not evidence of an actual missing runtime, dependency, license or protected diagram. Native keys remain unavailable.']
        controls.append(item)
    return controls


def finalize(case, item):
    probe = item['probe']
    if 'raw_response_utf8' not in probe:
        probe['raw_response_utf8'] = dumps(item['submitted']['reader_response'])
    probe['raw_response_sha256'] = digest(probe['raw_response_utf8'].encode('utf-8'))
    probe['raw_request_utf8'] = dumps(probe['request'])
    probe['raw_request_sha256'] = digest(probe['raw_request_utf8'].encode('utf-8'))
    item['submitted']['answer_record_raw_utf8'] = dumps(item['submitted']['answer_record'])
    for dimension, denominator in DIMENSIONS.items():
        rows = item['expected']['per_id'][dimension]
        assert set(rows) == set(case['denominators'][denominator]['required_ids'])
        counts = Counter(r['outcome'] for r in rows.values())
        item['expected']['counts'][dimension] = {k: counts[k] for k in OUTCOMES}
        assert sum(counts.values()) == case['denominators'][denominator]['count']
    item['expected']['extra_counts'] = {
        dimension: {outcome: sum(e['outcomes'].get(dimension) == outcome
                                for e in item['expected']['extras_ledger'])
                    for outcome in OUTCOMES} for dimension in DIMENSIONS}
    item['expected']['duplicate_count'] = len(item['expected']['duplicates'])
    item['expected']['contradiction_count'] = len(item['expected']['contradictions'])
    # Alignment points into preserved synthetic raw JSON; never reconstruct missing facts.
    response = item['submitted']['reader_response']
    observations = response['observations'] if response is not None else []
    item['alignment'] = [
        {'observation_id': observation_id,
         'raw_pointers': ['/observations/' + str(i) for i, row in enumerate(observations)
                          if row['observation_id'] == observation_id],
         'native_reference_status': 'unavailable',
         'evidence': row['evidence']}
        for observation_id, row in item['expected']['per_id']['fidelity'].items()]
    item['answer_mapping'] = [
        {'claim_id': claim_id,
         'raw_pointers': ['/claims/' + str(i) for i, row in enumerate(item['submitted']['answer_record']['claims'])
                          if row['claim_id'] == claim_id]}
        for claim_id in case['denominators']['answer_correctness']['required_ids']]
    return item


def readme():
    return '''# Public development challenge fixtures

Generated by `python3 -I benchmark/scripts/challenges.py`; verify with the same command plus `--check`. Generation uses checked-in case inventories only, without `LABVIEW_ENVIRONMENT`. Check regenerates in memory and compares every file recursively, including this README; it never writes. Unexpected files must be reviewed and removed explicitly.

All inputs are synthetic public development submissions. They are not reader executions, scorer outputs, independent approvals, withheld keys or challenge results. Three cases are planned; zero attempted, executed or scored. Raw JSON text, request/response hashes, per-ID mappings, expected outcome counts and separate extras/duplicates/contradictions accompany every control. Probe exit/error fields describe synthetic inputs, not observed process results. No concrete reader adapter is supplied.

Each library freezes 12 slots per dimension (ten provisional XML literals plus two unavailable native slots); the VI freezes three. Positive controls submit all IDs, exact available literals and supporting inventory citations; native slots retain null values with explicit limitations and no invented supporting locators. Positive correctness and grounding are therefore **unverified overall**, with ten provisionally correct XML items and two unverified items. A fully correct native positive control is an explicit gap. Every otherwise matching reader observation remains **unverified**, because XML extraction does not supply the required native reference. These are frozen author expectations pending independent original-source review, not established measurement results.

The `per_id` ledgers and `counts` retain the full denominator, and `dimensions` follow the protocol precedence. Thus omissions keep missing slots but remain unverified overall while native references are absent. True extras never replace omitted IDs. Literal contradictions and independently falsified extras are expected incorrect even when other references remain unavailable; a native comparison is still missing. Duplicate credit is zero beyond the first assertion. Conditions and limitation statements preserve preparation status without asserting runtime behavior.

| Protocol challenge row | Fixture / control names | Setup or explicit gap, and why |
|---|---|---|
| Wrong answer | Both library fixtures / `wrong-answer-declared-dependency` | Replace A0007's declared member URL and retain its locator; false content makes correctness and grounding incorrect. This uses a membership/dependency literal. Computation and typedef-impact discrimination require unavailable native controlled evidence. |
| Wrong citation | Both / `wrong-citation-existing`, `wrong-citation-unresolvable` | Preserve the member URL; cite existing save-version attribute or syntactically valid absent Item[999999]. Grounding is incorrect independently of the unchanged answer. |
| Selective omission | Both / `selective-omission-answer`, `selective-omission-reader`, `selective-omission-answer-with-true-extra` | Remove A0007 or R0007 from a full submission. The slot remains missing in 12; the true relational extra earns no required credit. Overall remains unverified; a partial overall demonstration is a native-reference gap. |
| Extra false claim | Both / `extra-false-answer`, `extra-false-reader`, `extra-true-answer`, `extra-true-reader`, `extra-unverified-answer`, `extra-unverified-reader` | Assert the two declared item types differ (falsified by A0006/A0009), are equal (supported), or a member resolves natively (unverified N0001). Answer false/unverified extras cite an existing non-supporting save-version location. Separate ledgers retain every assertion; native fidelity of true content remains unverified. |
| Duplicate and contradiction | Both / `duplicate-answer`, `duplicate-reader`, `contradiction-answer`, `contradiction-reader` | Repeat A0007/R0007 or append its explicit negation. Retain both raw assertions and locations; count duplicates once separately, and mark contradictions incorrect. |
| Constant export | Both / `constant-export` | Byte-identical concrete export uses save version 14008000 and member URL ../Actor/Actor.lvclass. Each fixture names R0001/R0007 and its conflicting actual literal; ten other observations remain missing. Native alignment remains an explicit gap. |
| Empty, truncated or failed probe | Both / `empty-probe`, `wrapper-only-probe`, `truncated-probe`, `unsupported-probe`, `error-probe` | Exact empty bytes, valid empty JSON wrapper, one-observation prefix, explicit unsupported response and exit-17 error response. All slots retain missing/unsupported/error records; a retained XML prefix is unverified. |
| Unsupported or inaccessible case | [VI fixture](vi-actor-core-native-gap.json) / `unsupported-missing-runtime`, `unsupported-missing-dependency`, `unsupported-missing-license`, `unsupported-inaccessible-diagram` | Concrete synthetic access conditions affect all three native slots. Null answers, raw responses and zero execution counts preserve honest abstention without asserting actual runtime/access failures or semantic success. |
| Missing evidence or execution | Both libraries / `missing-key-zero-execution`; all fixtures' coverage records | Explicit null independent key/native run and a concrete zero-test report leave every dimension unverified. All challenge execution remains pending. |
| Positive controls | [Icon fixture](library-icon-tests.json), [specialty fixture](library-specialty.json) / `positive-control` | All 12 IDs materialized; ten available literals with correct locators, two native gaps. Cannot justify a full semantic pass or verified fidelity. Independent key review and native positives are required to rule out a scorer that rejects everything. |

The case files pin original artifact identities; fixture sources additionally pin the case bytes. Review [protocol accounting](../protocol.md#tasks), the [challenge contract](../protocol.md#challenges) and [case locator syntax](../cases/dev/README.md). Do not treat a valid hash or successful generator check as semantic validation. Next: independently inspect original literals/citations and the complete ledgers; obtain native references and positive controls; then request a Policymaker-ordered scorer with its separate verifier. Method review and owner acceptance remain prerequisites for implementation.
'''


def rendered():
    files = {'README.md': readme().encode('utf-8')}
    for case_id in CASE_IDS:
        path = CASE_DIR / (case_id + '.json')
        raw = path.read_bytes()
        case = json.loads(raw)
        items = (vi_controls(case) if case_id.startswith('vi-')
                 else library_controls(case) + [constant_control(case)])
        fixture = {'schema_version': 2, 'fixture_id': case_id,
                   'public_development_only': True,
                   'source': {'path': path.relative_to(ROOT).as_posix(),
                              'sha256': digest(raw), 'case_revision': case['case_revision'],
                              'inventory_revision': case['inventory_revision'],
                              'artifact': case['artifact']},
                   'denominators': deepcopy(case['denominators']),
                   'evidence_status': LIMITATION,
                   'controls': [finalize(case, item) for item in items]}
        files[case_id + '.json'] = dumps(fixture).encode('utf-8')
    assert all(len(data) < 2_000_000 for data in files.values())
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = rendered()
    actual = {p.relative_to(OUT_DIR).as_posix(): p for p in OUT_DIR.rglob('*')
              if p.is_file() or p.is_symlink()} if OUT_DIR.exists() else {}
    missing = sorted(set(files) - set(actual))
    extra = sorted(set(actual) - set(files))
    changed = sorted(name for name in set(files) & set(actual)
                     if actual[name].is_symlink() or actual[name].read_bytes() != files[name])
    if args.check:
        if missing or extra or changed:
            raise SystemExit('challenge bytes differ: ' + json.dumps(
                {'missing': missing, 'extra': extra, 'changed': changed}, sort_keys=True))
        print('challenge fixtures and README match; no challenges executed')
        return
    if extra:
        raise SystemExit('unexpected files require explicit review/removal: ' + ', '.join(extra))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        if (OUT_DIR / name).is_symlink():
            raise SystemExit('refusing symlink output: ' + name)
    for name, data in files.items():
        (OUT_DIR / name).write_bytes(data)
    print('wrote %d public preparation files; no challenges executed' % len(files))


if __name__ == '__main__':
    main()
