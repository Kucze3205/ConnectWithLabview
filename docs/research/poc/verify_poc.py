#!/usr/bin/env python3
"""Offline structural checks against pinned primary-source field readers.

Run: python3 -I docs/research/poc/verify_poc.py
Writes verification.json and candidate-change.json beside this script.
No original or edited VI is written; the candidate mutation stays in memory.
"""
import ast
from hashlib import sha256
import importlib.util
import io
import json
import os
from pathlib import Path
import types
import warnings
import zlib

HERE = Path(__file__).resolve().parent
warnings.simplefilter('ignore', SyntaxWarning)
spec = importlib.util.spec_from_file_location('inspect_vi', HERE / 'inspect_vi.py')
inspector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inspector)


def source_function(path, name, namespace):
    module = ast.parse(path.read_text())
    functions = [n for n in ast.walk(module) if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(functions) == 1, name
    compiled = ast.Module(body=functions, type_ignores=[])
    exec(compile(compiled, str(path), 'exec'), namespace)
    return namespace[name]


def original_heap(path, result):
    raw = path.read_bytes()
    resource = result['resource']
    start = resource['payload_offset']
    return zlib.decompress(raw[start + 4:start + resource['payload_length']])


def main():
    provenance = json.loads((HERE / 'source-provenance.json').read_text())
    for record in provenance:
        assert sha256((HERE / record['file']).read_bytes()).hexdigest() == record['sha256']
    misc_ns = {}
    misc = types.SimpleNamespace(**{name: source_function(HERE / 'LVmisc-source.txt', name, misc_ns)
                                  for name in ('readVariableSizeFieldU124', 'readVariableSizeFieldS124', 'readVariableSizeFieldS24')})
    errors = []
    namespace = {'LVmisc': misc, 'attributeValueIntToIntOrEn': lambda key, val, obj: val,
                 'eprint': lambda *args: errors.append(str(args))}
    source_reader = source_function(HERE / 'LVheap-source.txt', 'parseRSRCData', namespace)
    evidence = {'scope': 'structural, no LabVIEW execution', 'primary_source_hashes': 'pass', 'fixtures': {}}
    root = Path(os.environ['LABVIEW_ENVIRONMENT']) / 'pylavi/tests'
    labels = inspector.load_labels()
    for name in ('add', 'empty', 'empty_separate_code', 'add_breakpoints'):
        path = root / (name + '.vi')
        result = inspector.inspect(path)
        assert result['status'] == 'complete', result
        inspector.annotate(result, labels)
        assert result == json.loads((HERE / (name + '.json')).read_text()), 'saved evidence is stale'
        heap = original_heap(path, result)
        for entry in result['entries']:
            stream = io.BytesIO(heap)
            # This artifact uses compact tag IDs. Extended headers have separate coverage below.
            assert entry['header'] & 1023 != 1023
            stream.seek(entry['heap_offset'] + 2)
            obj = types.SimpleNamespace(po=types.SimpleNamespace(verbose=0),
                                        parseRSRCContent=lambda: None)
            source_reader(obj, stream, bool(entry['header'] & 0x1000), entry['size_spec'])
            assert stream.tell() == entry['end']
            assert obj.attribs == {a['id']: a['value'] for a in entry['attributes']}
            content = bytes.fromhex(entry['content_hex']) if entry['data_length'] else entry.get('inline_bool')
            assert obj.content == content
        truncated = inspector.parse_heap(heap[:-1])
        assert truncated['status'] == 'partial' and truncated['failure_entry_offset'] == 0
        # Correct length to reach the truncated last entry, rather than fail on the size prefix.
        truncated_heap = (len(heap) - 5).to_bytes(4, 'big') + heap[4:-1]
        truncated = inspector.parse_heap(truncated_heap)
        assert truncated['status'] == 'partial' and truncated['failure_entry_offset'] >= 4
        malformed = bytearray(heap)
        malformed[4] = (malformed[4] & ~12) | 12
        assert inspector.parse_heap(malformed)['status'] == 'partial'
        evidence['fixtures'][name] = {'sha256': result['sha256'], 'entries': len(result['entries']),
                                     'source_reader_matches': True, 'truncation_and_scope_failure': 'pass'}
    assert not errors, errors
    # Exercise source-defined U124/S124/S24 escape encodings and extended tag IDs.
    for field, raw, expected in [('u124', b'\xff\x01\x00', 256), ('u124', b'\xfe\x00\x01\x00\x00', 65536),
                                 ('s124', b'\x80\xff\x7f', -129), ('s124', b'\x81\x00\x01\x00\x00', 65536),
                                 ('s24', b'\x80\x00\x00\x01\x00\x00', 65536)]:
        c = inspector.Cursor(b'\0' * 4 + raw)
        assert getattr(c, field)() == expected and c.pos == len(c.data)
    extended = b'\x07\xff' + (1000).to_bytes(4, 'big', signed=True)
    parsed = inspector.parse_heap(len(extended).to_bytes(4, 'big') + extended)
    assert parsed['status'] == 'complete' and parsed['entries'][0]['tag'] == 1000
    add = inspector.inspect(root / 'add.vi')
    inspector.annotate(add, labels)
    heap = original_heap(root / 'add.vi', add)
    fields = [e for e in add['entries'] if e['name'] == 'OF__primIndex']
    assert [e['data_offset'] for e in fields] == [112, 171, 223, 258]
    assert all(e['content_hex'] == '67' and e['data_length'] == 1 for e in fields)
    changed = bytearray(heap)
    replacements = []
    for entry in fields:
        offset = entry['data_offset']
        changed[offset] = 104
        replacements.append({'heap_offset': offset, 'body_offset_excluding_UInt32': offset - 4,
                             'old_hex': '67', 'new_hex': '68', 'field': entry['name']})
    after = inspector.parse_heap(changed)
    assert after['status'] == 'complete' and len(after['entries']) == len(add['entries'])
    assert [i for i, (a, b) in enumerate(zip(heap, changed)) if a != b] == [112, 171, 223, 258]
    packed = zlib.compress(changed)
    assert zlib.decompress(packed) == changed
    candidate = {'status': 'syntactic candidate only; target primitive semantics and terminal compatibility unknown',
                 'artifact_sha256': add['sha256'], 'original_index': 103, 'hypothetical_target_index': 104,
                 'primitive_uid': 43, 'primitive_resource_id_retained': 1050, 'replacements': replacements,
                 'heap_length_unchanged': len(changed), 'reparse': after['status'],
                 'original_BDHb_payload_bytes': add['resource']['payload_length'],
                 'candidate_BDHb_payload_bytes_default_zlib': 4 + len(packed),
                 'zlib_runtime_version': zlib.ZLIB_RUNTIME_VERSION,
                 'original_heap_sha256': sha256(heap).hexdigest(),
                 'candidate_heap_sha256': sha256(changed).hexdigest(),
                 'original_adler32': zlib.adler32(heap), 'candidate_adler32': zlib.adler32(changed),
                 'vi_written': False, 'LabVIEW_tested': False}
    (HERE / 'candidate-change.json').write_text(json.dumps(candidate, indent=2) + '\n')
    evidence['escape_fields_and_extended_tag'] = 'pass'
    evidence['candidate_reparse_and_zlib_roundtrip'] = 'pass'
    readme = (HERE / 'README.md').read_text()
    assert 'heap-decode:' in readme and 'poc-feasibility:' in readme
    evidence['issue_marker_check'] = 'pass'
    (HERE / 'verification.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps(evidence, indent=2))
    print('Candidate:', json.dumps(candidate))


if __name__ == '__main__':
    main()
