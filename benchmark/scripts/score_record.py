#!/usr/bin/env python3
"""Record-intake scorer for the library-specialty dev fixture; no reader or model is run.

Reads one run record (benchmark/scripts/run_record.py format), builds `submitted` with
run_record.score_answer and scores correctness and grounding with score.compute against the
library-specialty fixture. Prints outcome counts per frozen ID as JSON on stdout. Writes no file.
Fidelity is reported 'not-applicable/unexecuted': compute needs a reader_response, so an empty
placeholder is passed and compute's own fidelity result is discarded.
Execution is taken from the record (executed/scored = 1 only for a complete, untruncated record);
`executed` is therefore self-reported by the record, not verified. Credit gate: only a record that
run_record.validate accepted (synthetic provenance only) may reach `correct`. Any other record,
including every record read from the command line, is scored with an evidence_record whose
native_run and independent_key are None, so correctness and grounding cap at `unverified`.
Without LABVIEW_ENVIRONMENT, cited artifact bytes are unreachable and grounding stays unverified.

--check uses the synthetic record from runner_contract.py plus an in-memory loader that returns no
artifact bytes. It checks that formats compose and that an altered claim answer changes the outcome.
It does not cover: citation resolution against real bytes, real records (run_record.validate accepts
synthetic provenance only, so it is not applied to input), native behaviour or any quality result.
"""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'benchmark/challenges/library-specialty.json'
NA = 'not-applicable/unexecuted'


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'benchmark/scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture_inputs(score):
    fixture = json.loads(FIXTURE.read_bytes())
    inventory_bytes = (ROOT / fixture['source']['inventory_path']).read_bytes()
    if score.digest(inventory_bytes) != fixture['source']['inventory_sha256']:
        raise ValueError('inventory SHA256 mismatch')
    control = next(c for c in fixture['controls'] if c['name'] == 'positive-control')
    return fixture, json.loads(inventory_bytes), control


def sync_raw(submitted, score):
    text = json.dumps(submitted['answer_record'], ensure_ascii=False)
    submitted['raw_answer_record'] = {'text': text, 'sha256': score.digest(text.encode('utf-8'))}


def score_record(record, score, run_record, load_bytes=None, validated=False):
    fixture, inventory, control = fixture_inputs(score)
    submitted = run_record.score_answer(record)
    return score_submitted(submitted, record, fixture, inventory, control, score, load_bytes, validated)


def score_submitted(submitted, record, fixture, inventory, control, score, load_bytes, validated=False):
    f = {k: v['value'] for k, v in record['fields'].items()}
    ran = f['outcome'] == 'complete' and not f['truncated']
    execution = {'attempted': 1, 'executed': int(ran), 'planned': 1, 'scored': int(ran)}
    submitted = dict(submitted, reader_response={},
                     raw_reader_response={'text': '', 'sha256': score.digest(b'')})
    if not validated:
        # No native run and no independent key exist for this record: score.compute caps credit.
        submitted['evidence_record'] = {'native_run': None, 'independent_key': None}
    probe = dict(control['probe'], actual_execution=execution)
    computed = score.compute(fixture['source'], fixture['denominators'], inventory, submitted,
                             probe, control['alignment'], load_bytes)
    return {'per_id': {d: computed['per_id'][d] for d in ('correctness', 'grounding')},
            'counts': {d: computed['counts'][d] for d in ('correctness', 'grounding')},
            'extras': [{'assertion_id': e['assertion_id'], 'outcomes': e['outcomes']}
                       for e in computed['extras_ledger']],
            'fidelity': NA, 'cannot_evaluate_reasons': computed['cannot_evaluate_reasons']}


def check():
    score, run_record, contract = load('score'), load('run_record'), load('runner_contract')
    manifest_bytes = contract.SYNTHETIC.read_bytes()
    manifest = run_record.parse(manifest_bytes.decode())
    plan = contract.plan_runs(manifest, manifest_bytes)
    record = contract.build_record(plan['runs'][0], manifest, manifest_bytes)
    run_record.validate(record, manifest)
    nothing = lambda citation: None
    fixture, inventory, control = fixture_inputs(score)

    # Stage 1: the synthetic record as it stands (its claim id is not a frozen ID).
    plain = score_record(record, score, run_record, nothing)
    assert not plain['cannot_evaluate_reasons'], plain['cannot_evaluate_reasons']
    assert plain['counts']['correctness']['missing'] == 12, plain['counts']
    assert [e['assertion_id'] for e in plain['extras']] == ['synthetic:claim-1'], plain['extras']
    assert plain['fidelity'] == NA

    # Stage 2: remap the synthetic claim onto A0001 with the keyed literal, then alter its answer.
    key = next(k for k in inventory['reference_inventory'] if k['claim_id'] == 'A0001')
    keyed = deepcopy(record)
    claim = keyed['fields']['answer_claims']['value'][0]
    claim.update(claim_id='A0001', answer=key['atomic_fact']['value'],
                 conditions=list(key.get('conditions', [])), citations=deepcopy(key['citations']))
    submitted = run_record.score_answer(keyed)
    sync_raw(submitted, score)

    def run(sub):
        return score_submitted(sub, keyed, fixture, inventory, control, score, nothing, True)

    base = run(submitted)
    assert not base['cannot_evaluate_reasons'], base['cannot_evaluate_reasons']
    assert base['per_id']['correctness']['A0001'] == 'correct', base['per_id']['correctness']['A0001']
    altered = deepcopy(submitted)
    altered['answer_record']['claims'][0]['answer'] = 'Deliberately wrong A0001 literal.'
    sync_raw(altered, score)
    changed = run(altered)
    assert changed['per_id']['correctness']['A0001'] == 'incorrect', changed['per_id']['correctness']['A0001']
    assert changed['per_id'] != base['per_id'], 'altered claim answer did not change the outcome'

    # Stage 3: a non-synthetic record carrying the keyed literal must not reach `correct`.
    real = deepcopy(keyed)
    for item in real['fields'].values():
        if 'provenance' in item:
            item['provenance'] = 'recorded'
    try:
        run_record.validate(real, manifest)
        raise AssertionError('run_record.validate accepted non-synthetic provenance')
    except ValueError:
        pass
    real_submitted = run_record.score_answer(real)
    sync_raw(real_submitted, score)
    unvalidated = score_submitted(real_submitted, real, fixture, inventory, control, score, nothing)
    assert not unvalidated['cannot_evaluate_reasons'], unvalidated['cannot_evaluate_reasons']
    for d in ('correctness', 'grounding'):
        assert unvalidated['per_id'][d]['A0001'] != 'correct', (d, unvalidated['per_id'][d]['A0001'])
    print(json.dumps({'status': 'pass', 'synthetic_record': record['fields']['record_id']['value'],
                      'baseline_A0001': {d: base['per_id'][d]['A0001'] for d in base['per_id']},
                      'altered_A0001': {d: changed['per_id'][d]['A0001'] for d in changed['per_id']},
                      'non_synthetic_A0001': {d: unvalidated['per_id'][d]['A0001'] for d in unvalidated['per_id']},
                      'executed': 'self-reported by the record, not verified',
                      'fidelity': NA, 'benchmark_executed': False}, indent=2))



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', nargs='?', help='run-record JSON file')
    parser.add_argument('--check', action='store_true', help='run the synthetic round trip')
    args = parser.parse_args()
    try:
        if args.check:
            check()
        elif args.record:
            score, run_record = load('score'), load('run_record')
            record = run_record.parse(Path(args.record).read_text())
            print(json.dumps(score_record(record, score, run_record), indent=2, sort_keys=True))
        else:
            parser.error('record path or --check required')
    except (ValueError, TypeError, KeyError, AttributeError, OSError, AssertionError) as exc:
        print('score-record failed: %s: %s' % (type(exc).__name__, exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
