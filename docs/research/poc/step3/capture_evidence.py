"""Save small original-byte evidence; no modified VI is generated."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[1]
ENV = Path(os.environ['LABVIEW_ENVIRONMENT'])

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    spec = importlib.util.spec_from_file_location('inspector', BASE / 'inspect_vi.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    fixtures = json.loads((BASE / 'step3/fixture-probe.json').read_text())['fixtures']
    fixture = fixtures[5]
    path = ENV / fixture['path']
    raw = path.read_bytes()
    parsed = m.inspect(path)
    labels = m.load_labels()
    m.annotate(parsed, labels)
    stack = []
    selected = []
    for e in parsed['entries']:
        if e['scope'] == 'close':
            stack.pop()
            continue
        own_class = next((a['value'] for a in e['attributes'] if a['id'] == -2), None)
        uid = next((a['value'] for a in e['attributes'] if a['id'] == -3), None)
        ancestors = list(stack)
        constant = any(a['class_id'] == 19 for a in ancestors)
        signal = any(a['class_id'] == 23 for a in ancestors)
        if own_class in (19, 23) or (constant and e['name'] in ('OF__typeDesc', 'OF__ConstValue')) or (signal and e['name'] == 'OF__termList') or (signal and e['name'] == 'SL__arrayElement'):
            selected.append({'entry': e, 'ancestors': ancestors})
        if e['scope'] == 'open':
            stack.append({'offset': e['heap_offset'], 'name': e['name'], 'class_id': own_class, 'uid': uid})
    r = parsed['resource']
    payload = raw[r['payload_offset']:r['payload_offset'] + r['payload_length']]
    out = {'path': fixture['path'], 'sha256': digest(raw), 'heap_sha256': parsed['heap_sha256'], 'heap_bytes': parsed['heap_bytes'], 'resource': r, 'payload_hex': payload.hex(), 'offset_basis': 'decompressed heap including four-byte length; spans half-open', 'observations': selected, 'interpretation': 'Parser-labelled constant objects and raw values only. Heap type references 18/20 and child-display references must be resolved independently; no signedness, numeric/string value, direction or primitive behavior asserted.'}
    (BASE / 'step3/constant-candidate.json').write_text(json.dumps(out, indent=2) + '\n')
    revision = '35d2a0318f71dcb87bb9c431dc00700ee6b9fb75'
    provenance = []
    for rel, saved in [('pylavi/resource_types.py', 'pylavi-resource-types-source.txt'), ('LICENSE', 'pylavi-LICENSE.txt')]:
        source = ENV / 'pylavi' / rel
        if not source.exists() and rel == 'LICENSE':
            source = ENV / 'pylavi' / 'UNLICENSE'
            rel = 'UNLICENSE'
        data = source.read_bytes()
        (BASE / 'step3' / saved).write_bytes(data)
        provenance.append({'url': 'https://raw.githubusercontent.com/marcpage/pylavi/' + revision + '/' + rel, 'revision': revision, 'original_path': rel, 'license': 'Unlicense', 'license_file': 'step3/pylavi-LICENSE.txt', 'file': 'step3/' + saved, 'sha256': digest(data), 'bytes': len(data), 'acquisition': 'copied from prepared pinned checkout; no network retrieval'})
    (BASE / 'step3/source-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print('constant observations:', len(selected))
    for o in selected:
        e = o['entry']
        if e['name'] in ('OF__ConstValue', 'OF__typeDesc'):
            print(e['name'], e['data_offset'], e['end'], e['content_hex'])
    print('saved original heap payload and two pinned source/license snapshots')

if __name__ == '__main__':
    main()
