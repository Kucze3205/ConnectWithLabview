#!/usr/bin/env python3
"""Probe score.py with in-memory empty and constant exports. Never runs main(), never writes results."""
import hashlib, importlib.util, json, sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path('.').resolve()
spec = importlib.util.spec_from_file_location('score_mod', ROOT / 'benchmark/scripts/score.py')
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)  # __name__ != '__main__', so main() is not run

RAN = {'attempted': 1, 'executed': 1, 'planned': 1, 'scored': 1}


def rehash(sub):
    for rec, raw in (('answer_record', 'raw_answer_record'), ('reader_response', 'raw_reader_response')):
        text = json.dumps(sub[rec], ensure_ascii=False)
        sub[raw]['text'] = text
        sub[raw]['sha256'] = hashlib.sha256(text.encode('utf-8')).hexdigest()


def empty(sub):
    s = deepcopy(sub)
    s['answer_record']['claims'] = []
    s['reader_response']['observations'] = []
    rehash(s)
    return s


def constant(sub, value='CONSTANT'):
    s = deepcopy(sub)
    for c in s['answer_record'].get('claims', []):
        c['answer'] = value
    for o in s['reader_response'].get('observations', []):
        o['value'] = value
    rehash(s)
    return s


def run(fx, inv, control, sub, execution):
    return score.compute(fx['source'], fx['denominators'], inv, sub,
                         dict(control['probe'], actual_execution=execution), control['alignment'])


for fid in score.FIXTURES:
    fx = json.loads((ROOT / 'benchmark/challenges' / (fid + '.json')).read_bytes())
    inv = json.loads((ROOT / fx['source']['inventory_path']).read_bytes())
    names = [c['name'] for c in fx['controls']]
    print('FIXTURE', fid, 'controls', names)
    pc = next((c for c in fx['controls'] if c['name'] == 'positive-control'), None)
    if pc is None:
        print('  no positive-control: NOT-APPLICABLE for synthetic perturbation')
        continue
    for label, sub in (('baseline', pc['submitted']), ('empty', empty(pc['submitted'])),
                       ('constant', constant(pc['submitted']))):
        for exn, ex in (('executed', RAN), ('declared', pc['probe']['actual_execution'])):
            try:
                r = run(fx, inv, pc, sub, ex)
            except Exception as e:
                print('  %s/%s EXC %r' % (label, exn, e))
                continue
            print('  %s/%s dims=%s corr=%s gnd=%s reasons=%s' % (
                label, exn, r['dimensions'], {k: v for k, v in r['counts']['correctness'].items() if v},
                {k: v for k, v in r['counts']['grounding'].items() if v}, r['cannot_evaluate_reasons']))
            if label != 'baseline' and exn == 'executed':
                ref = pc.get('expected_positive') or pc['expected']
                print('    compare-vs-%s mismatches:' % ('expected_positive' if 'expected_positive' in pc else 'expected'), len(score.compare(r, ref)))
