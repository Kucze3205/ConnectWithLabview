#!/usr/bin/env python3
"""Derive bounded research summaries; SequenceMatcher is not a semantic parser."""
import difflib
import hashlib
import json
from pathlib import Path
import zlib

BASE = Path('docs/research/poc/pair')
sha = lambda data: hashlib.sha256(data).hexdigest()
status = json.loads((BASE / 'replay-0105-status.json').read_text())
assert status['status'] == 'measured' and len(status['runs']) == 8
result = {'schema_version': 1, 'invocation': ['python3', str(BASE / 'summarize_0105.py')],
          'limitations': ['Sequence alignment is ambiguous; edits are candidate byte correspondences only, not type/value encoding rules.'],
          'bdhb_alignments': [], 'version_declarations': {}, 'comparison_summary': []}
for run in status['runs']:
    source = Path(run['output'])
    data = json.loads(source.read_text())
    row = next(r for r in data['resources'] if r['type'] == 'BDHb')
    heaps, payloads = [], {}
    for side in ('left', 'right'):
        raw = Path(data['inputs'][side]['path']).read_bytes()
        assert sha(raw) == data['inputs'][side]['sha256']
        payloads[side] = {}
        for resource in data['resources']:
            if resource[side] is not None:
                off, size = resource[side]['file_payload_offset'], resource[side]['length']
                payloads[side][(resource['type'], resource['id'], resource['occurrence'])] = raw[off:off + size]
        heap = zlib.decompress(payloads[side][('BDHb', 0, 0)][4:])
        assert sha(heap) == row['decompressed'][side + '_sha256']
        heaps.append(heap)
        result['version_declarations'][data['inputs'][side]['path']] = [
            {'type': r['type'], 'id': r['id'], 'fields': r['version_fields'][side]}
            for r in data['resources'] if 'version_fields' in r and r[side] is not None]
    edits = [{'tag': tag, 'left_offset': a, 'right_offset': b,
              'left_hex': heaps[0][a:ae].hex(), 'right_hex': heaps[1][b:be].hex()}
             for tag, a, ae, b, be in difflib.SequenceMatcher(None, *heaps, autojunk=False).get_opcodes()
             if tag != 'equal']
    result['bdhb_alignments'].append({'source': str(source), 'source_sha256': sha(source.read_bytes()),
        'resource': {'type': 'BDHb', 'id': 0, 'occurrence': 0},
        'method': 'difflib.SequenceMatcher(autojunk=False); byte alignment hypothesis, not a semantic parse',
        'edits': edits})
    result['comparison_summary'].append({'file': source.name, 'differing_resources': data['differing_resources'],
        'resource_counts': [sum(r[side] is not None for r in data['resources']) for side in ('left', 'right')],
        'name_changes': [r['type'] for r in data['resources'] if r['name_changed']],
        'resource_inventory': [{'type': r['type'], 'id': r['id'], 'occurrence': r['occurrence'],
            'lengths': [r['raw'][side + '_length'] for side in ('left', 'right')],
            'presence': r['present_in_one_only'], 'different': r['different']} for r in data['resources']],
        'cpc2_hex': [payloads[side][('CPC2', 0, 0)].hex() for side in ('left', 'right')],
        'lvsr_bytes_8_12_hex': [payloads[side][('LVSR', 0, 0)][8:12].hex() for side in ('left', 'right')]})
output = BASE / 'candidates-0105.json'
output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'output': str(output), 'comparisons': len(result['comparison_summary']),
                  'cpc2': [r['cpc2_hex'] for r in result['comparison_summary']],
                  'lvsr_bytes_8_12': [r['lvsr_bytes_8_12_hex'] for r in result['comparison_summary']],
                  'versions': {Path(path).name: [[r['type'], r['id'], r['fields']['raw_hex']]
                              for r in rows] for path, rows in result['version_declarations'].items()}}))
