#!/usr/bin/env python3
"""Read-only, research-only VI pair comparison. No LabVIEW or VI writer.

python3 -I docs/research/poc/pair/pair_diff.py LEFT.vi RIGHT.vi
python3 -I docs/research/poc/pair/pair_diff.py --self-check
Stdlib plus the existing pinned, prepared pylavi and sibling POC inspector.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import zlib

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REVISION = '35d2a0318f71dcb87bb9c431dc00700ee6b9fb75'
FIXTURE_SHA = 'cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8'
SOURCE_PINS = {
    'file.py': 'f3c9d38054291d02bf48e7f2658c2b012e0c0b7a7fb55731710e985d7df2cce9',
    'resource_types.py': 'ce333fba1b8dc689197e18e4a1acedf77b786f098f5039e4234c136f73512756',
    'data_types.py': '5ee827ae02abad1e37fd0c54f0ca5a9df491e2ed639bf12b807c76368d932cea',
}
HEX_BOUND = 32
LIMITATIONS = [
    'No owner-authored pair exists in this self-check; the perturbation is a tool control, not LabVIEW evidence.',
    'No VI is written, no LabVIEW runs, and no behavior, valid edit or native compatibility is established.',
    'Offsets are positional comparisons, not an insertion/deletion alignment or semantic interpretation.',
    'Known BDHb/FPHb and other valid size-prefixed zlib payloads are decompressed; unsupported known heaps block rather than silently pass.',
    'Observed spans and dependencies from a real pair cannot establish general integrity rules or other-version behavior.',
]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def prepare(inputs):
    """Check pins before any VI load; retain observed values on failure."""
    env = Path(os.environ['LABVIEW_ENVIRONMENT']).resolve()
    root = env / 'pylavi'
    inputs['prepared_root'] = str(env)
    actual = git(root, 'rev-parse', 'HEAD')
    inputs['pylavi_revision'] = actual
    require(actual == REVISION, 'pylavi revision mismatch: ' + actual)
    changes = git(root, 'status', '--porcelain', '--untracked-files=all', '--', 'pylavi')
    inputs['pylavi_source_status'] = changes
    require(not changes, 'pylavi source tree is modified: ' + changes)
    inputs['source_pins'] = []
    for name, expected in SOURCE_PINS.items():
        data = (root / 'pylavi' / name).read_bytes()
        observed = sha(data)
        inputs['source_pins'].append({'path': '@environment/pylavi/pylavi/' + name,
                                     'sha256': observed, 'expected_sha256': expected})
        require(observed == expected, 'source SHA256 mismatch: ' + name)
    readiness_path = env / 'readiness.json'
    readiness_raw = readiness_path.read_bytes()
    readiness = json.loads(readiness_raw)
    inputs['readiness'] = {'path': '@environment/readiness.json', 'sha256': sha(readiness_raw)}
    require(readiness.get('public_sources') == 'ready', 'prepared sources not ready')
    require(any(s.get('name') == 'pylavi' and s.get('commit') == REVISION
                for s in readiness.get('sources', [])), 'readiness pylavi revision mismatch')
    sys.path.insert(0, str(root))
    from pylavi.file import Resources
    from pylavi.resource_types import Typevers, TypeLVSR
    inspector_path = HERE.parent / 'inspect_vi.py'
    inputs['inspector'] = {'path': 'docs/research/poc/inspect_vi.py',
                           'sha256': sha(inspector_path.read_bytes())}
    spec = importlib.util.spec_from_file_location('pair_existing_inspector', inspector_path)
    inspector = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inspector)
    return env, Resources, Typevers, TypeLVSR, inspector


def byte_diff(left, right):
    """Every differing positional byte; each hex field is at most 32 bytes.

    Split long runs rather than dropping ranges. Absent tails have empty hex on
    the shorter side. The offset and length cover the union of both inputs.
    """
    rows = []
    pos, end, count = 0, max(len(left), len(right)), 0
    while pos < end:
        if pos < min(len(left), len(right)) and left[pos] == right[pos]:
            pos += 1
            continue
        start = pos
        while pos < end and pos - start < HEX_BOUND:
            if pos < min(len(left), len(right)) and left[pos] == right[pos]:
                break
            pos += 1
        rows.append({'offset': start, 'length': pos - start,
                     'left_hex': left[start:pos].hex(), 'right_hex': right[start:pos].hex()})
        count += pos - start
    return {'different': left != right, 'left_length': len(left), 'right_length': len(right),
            'left_sha256': sha(left), 'right_sha256': sha(right),
            'differing_byte_count': count, 'hex_bound_bytes': HEX_BOUND, 'ranges': rows}


def decompressed(kind, payload, inspector):
    known = kind in ('BDHb', 'FPHb')
    # Recognize the same outer UInt32 + zlib framing without inventing a codec.
    zheader = len(payload) >= 6 and payload[4] & 15 == 8 and payload[4] >> 4 <= 7
    zheader = zheader and int.from_bytes(payload[4:6], 'big') % 31 == 0
    if not known and not zheader:
        return None
    require(len(payload) >= 6, 'truncated compressed payload: ' + kind)
    size = int.from_bytes(payload[:4], 'big')
    require(4 <= size <= inspector.MAX_HEAP, 'unsupported decompressed size: ' + kind)
    stream = zlib.decompressobj()
    heap = stream.decompress(payload[4:], size + 1)
    require(stream.eof and not stream.unused_data and not stream.unconsumed_tail,
            'incomplete/trailing compressed stream: ' + kind)
    require(len(heap) == size, 'decompressed-size mismatch: ' + kind)
    return heap


def version_fields(kind, payload, Typevers, TypeLVSR):
    cls = Typevers if kind == 'vers' else TypeLVSR
    require(len(payload) >= 4, 'truncated version: ' + kind)
    decoded = cls().from_bytes(payload)
    v = decoded.version
    result = {'offset': 0, 'length': 4, 'raw_hex': payload[:4].hex(),
              'uint32': v.value, 'tuple_major_minor_patch_phase_build':
              [v.major(), v.minor(), v.patch(), v.phase(), v.build()],
              'parser_value': v.to_value()}
    if kind == 'LVSR':
        result['flags_offset'] = 4
        result['flags_hex'] = payload[4:].hex()
        result['separate_code_parser_flag'] = decoded.separate_code()
    return result


def load(path, prepared):
    _, Resources, Typevers, TypeLVSR, inspector = prepared
    path = Path(path)
    raw = path.read_bytes()
    framed = inspector.rsrc_resources(raw)
    loaded = Resources.load(str(path))
    entries = {}
    for kind in dict.fromkeys(loaded.types()):
        counts = {}
        for rid, name, payload in loaded.get_resources(kind):
            occurrence = counts.get(rid, 0)
            counts[rid] = occurrence + 1
            key = (kind, rid, occurrence)
            matches = [r for r in framed if r['type'] == kind and r['id'] == rid]
            require(occurrence < len(matches), 'loader/inspector resource identity disagreement')
            location = matches[occurrence]
            start, size = location['payload_offset'], location['payload_length']
            require(raw[start:start + size] == payload, 'loader/inspector payload disagreement')
            entry = {'payload': payload, 'name': name, 'file_payload_offset': start,
                     'decompressed': decompressed(kind, payload, inspector)}
            if kind in ('vers', 'LVSR'):
                entry['version'] = version_fields(kind, payload, Typevers, TypeLVSR)
            entries[key] = entry
    require(len(entries) == len(framed), 'loader/inspector resource count disagreement')
    require(path.read_bytes() == raw, 'input changed while loading: ' + str(path))
    return {'path': str(path), 'sha256': sha(raw), 'raw': raw, 'resources': entries}


def compare(left, right):
    rows = []
    for key in sorted(left['resources'].keys() | right['resources'].keys()):
        kind, rid, occurrence = key
        a, b = left['resources'].get(key), right['resources'].get(key)
        row = {'type': kind, 'id': rid, 'occurrence': occurrence,
               'present_in_one_only': None if a is not None and b is not None else ('left' if a is not None else 'right')}
        row['raw'] = byte_diff(a['payload'] if a else b'', b['payload'] if b else b'')
        for side, entry in [('left', a), ('right', b)]:
            row[side] = None if entry is None else {
                'length': len(entry['payload']), 'sha256': sha(entry['payload']),
                'name_hex': None if entry['name'] is None else entry['name'].hex(),
                'file_payload_offset': entry['file_payload_offset']}
        row['name_changed'] = (a['name'] if a else None) != (b['name'] if b else None)
        ha, hb = a['decompressed'] if a else None, b['decompressed'] if b else None
        if ha is not None or hb is not None:
            row['decompressed'] = byte_diff(ha if ha is not None else b'', hb if hb is not None else b'')
            row['decompressed']['left_present'] = ha is not None
            row['decompressed']['right_present'] = hb is not None
            row['decompressed']['offset_basis'] = 'decompressed payload byte 0, including inner heap length prefix'
        if kind == 'BDPW':
            pa, pb = a['payload'] if a else b'', b['payload'] if b else b''
            row['chunks_16_bytes'] = []
            for offset in range(0, max(len(pa), len(pb)), 16):
                ca, cb = pa[offset:offset + 16], pb[offset:offset + 16]
                row['chunks_16_bytes'].append({'index': offset // 16, 'offset': offset,
                                               'left_hex': ca.hex(), 'right_hex': cb.hex(),
                                               'different': ca != cb})
            row['chunk_alignment_valid'] = len(pa) % 16 == 0 and len(pb) % 16 == 0
        if kind in ('vers', 'LVSR'):
            row['version_fields'] = {'left': a.get('version') if a else None,
                                     'right': b.get('version') if b else None}
        row['different'] = bool(row['present_in_one_only'] or row['name_changed'] or row['raw']['different']
                                or row.get('decompressed', {}).get('different'))
        rows.append(row)
    code = {kind: {side: [{'id': k[1], 'occurrence': k[2], 'length': len(v['payload']),
                          'sha256': sha(v['payload'])} for k, v in snap['resources'].items() if k[0] == kind]
                   for side, snap in [('left', left), ('right', right)]} for kind in ('VICD', 'CPC2')}
    return {'schema_version': 1, 'status': 'compared',
            'inputs': {side: {'path': snap['path'], 'sha256': snap['sha256']}
                       for side, snap in [('left', left), ('right', right)]},
            'differing_resources': sum(r['different'] for r in rows), 'resources': rows,
            'code_resource_presence': {k: {**v, 'left_present': bool(v['left']),
                                           'right_present': bool(v['right'])} for k, v in code.items()},
            'version_resource_presence': {kind: {side: any(k[0] == kind for k in snap['resources'])
                                                  for side, snap in [('left', left), ('right', right)]}
                                          for kind in ('LVSR', 'vers')},
            'whole_file': byte_diff(left['raw'], right['raw']),
            'offset_basis': 'raw resource offsets exclude its outer resource-length UInt32; whole_file offsets are absolute',
            'duplicate_ids': 'Matched by occurrence within each type/ID; reordered duplicates require manual interpretation.',
            'limitations': LIMITATIONS}


def self_check():
    target = HERE / 'selfcheck.json'
    record = {'schema_version': 1, 'status': 'blocked', 'blocker': 'Self-check in progress.',
              'inputs': {'paths': ['@environment/pylavi/tests/add.vi'],
                         'pylavi_revision_required': REVISION, 'expected_sha256': FIXTURE_SHA},
              'controls': [], 'limitations': LIMITATIONS,
              'invocation': 'python3 -I docs/research/poc/pair/pair_diff.py --self-check'}

    def save():
        target.write_text(json.dumps(record, indent=2) + '\n')

    save()
    try:
        prepared = prepare(record['inputs'])
        fixture = prepared[0] / 'pylavi/tests/add.vi'
        observed = sha(fixture.read_bytes())
        record['inputs']['sha256'] = observed
        record['inputs']['resolved_path'] = str(fixture)
        save()
        require(observed == FIXTURE_SHA, 'fixture SHA256 mismatch: ' + observed)
        original = load(fixture, prepared)
        require(original['sha256'] == FIXTURE_SHA, 'fixture changed after pin check')
        identical = compare(original, load(fixture, prepared))
        require(identical['differing_resources'] == 0 and not identical['whole_file']['different'],
                'identical pair yielded differences')
        record['controls'].append({'name': 'identical_pair', 'status': 'passed',
                                   'left_path': str(fixture), 'right_path': str(fixture),
                                   'differing_resources': 0, 'whole_file_differing_bytes': 0,
                                   'resource_count': len(identical['resources'])})
        save()
        key, offset = ('BDHb', 0, 0), 112
        altered = copy.deepcopy(original)
        heap = bytearray(altered['resources'][key]['decompressed'])
        before = heap[offset]
        heap[offset] ^= 1
        altered['resources'][key]['decompressed'] = bytes(heap)
        difference = compare(original, altered)
        changed = [r for r in difference['resources'] if r['different']]
        expected = {'offset': offset, 'length': 1, 'left_hex': bytes([before]).hex(),
                    'right_hex': bytes([before ^ 1]).hex()}
        require(len(changed) == 1 and (changed[0]['type'], changed[0]['id'], changed[0]['occurrence']) == key,
                'perturbation localized to wrong resource(s)')
        require(changed[0]['decompressed']['ranges'] == [expected], 'perturbation localized to wrong offset')
        require(all(not r['raw']['different'] for r in difference['resources'])
                and not difference['whole_file']['different'], 'in-memory control changed raw bytes')
        record['controls'].append({'name': 'single_decompressed_payload_byte', 'status': 'passed',
                                   'classification': 'Tool control only; not LabVIEW evidence.',
                                   'type': key[0], 'id': key[1], 'occurrence': key[2],
                                   'differing_resources': 1, 'observed_range': expected,
                                   'raw_resources_unchanged': True, 'vi_written': False})
        # Exercise long bounded runs, a same-prefix tail, and an absent payload.
        for a, b, expected_count in [(b'a' * 70, b'b' * 70, 70), (b'x', b'xyz', 2),
                                      (b'xyz', b'x', 2), (b'', b'abc', 3)]:
            diff = byte_diff(a, b)
            offsets = [i for r in diff['ranges'] for i in range(r['offset'], r['offset'] + r['length'])]
            expected_offsets = [i for i in range(max(len(a), len(b)))
                                if a[i:i + 1] != b[i:i + 1]]
            require(offsets == expected_offsets and diff['differing_byte_count'] == expected_count,
                    'byte-range coverage control failed')
            require(all(len(r['left_hex']) <= 2 * HEX_BOUND and len(r['right_hex']) <= 2 * HEX_BOUND
                        for r in diff['ranges']), 'hex bound control failed')
        record['controls'].append({'name': 'bounded_ranges_and_length_tails', 'status': 'passed',
                                   'classification': 'Synthetic byte-string tool control only.', 'cases': 4})
        require(sha(fixture.read_bytes()) == FIXTURE_SHA, 'fixture changed during self-check')
        record['inputs']['fixture_sha256_after'] = FIXTURE_SHA
        record['status'] = 'passed'
        record.pop('blocker', None)
        save()
        print(json.dumps({'status': record['status'], 'controls': len(record['controls']),
                          'report': str(target)}))
        return 0
    except Exception as exc:
        record.update(status='blocked', blocker=type(exc).__name__ + ': ' + str(exc))
        save()
        print(json.dumps({'status': 'blocked', 'blocker': record['blocker']}))
        return 1


def check_pair_pins(manifest_path, paths, inputs):
    manifest_path = Path(manifest_path).resolve()
    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw)
    inputs['pair_manifest'] = {'path': str(manifest_path), 'sha256': sha(manifest_raw), 'checks': []}
    authoring = manifest['authoring']
    settings = manifest_path.parent / authoring['path']
    observed = sha(settings.read_bytes())
    inputs['pair_manifest']['authoring_sha256'] = observed
    require(observed == authoring['sha256'], 'authoring settings SHA256 mismatch')
    for path in paths:
        path = Path(path).resolve()
        logical = path.relative_to(manifest_path.parent).as_posix()
        expected = manifest['files'][logical]
        observed = sha(path.read_bytes())
        inputs['pair_manifest']['checks'].append({'path': str(path), 'sha256': observed,
                                                  'expected_sha256': expected})
        require(observed == expected, 'pair SHA256 mismatch: ' + logical)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('left', nargs='?')
    parser.add_argument('right', nargs='?')
    parser.add_argument('--self-check', action='store_true')
    parser.add_argument('--pins', help='optional pre-recorded pair/settings manifest; see protocol.md')
    args = parser.parse_args()
    if args.self_check:
        require(args.left is None and args.right is None and args.pins is None,
                '--self-check takes no VI paths or pair manifest')
        return self_check()
    if args.left is None or args.right is None:
        parser.error('provide two VI paths, or --self-check')
    inputs = {}
    try:
        if args.pins:
            check_pair_pins(args.pins, [args.left, args.right], inputs)
        prepared = prepare(inputs)
        left, right = load(args.left, prepared), load(args.right, prepared)
        if args.pins:
            for snap, checked in zip((left, right), inputs['pair_manifest']['checks']):
                require(snap['sha256'] == checked['expected_sha256'], 'pair changed after pin check')
        result = compare(left, right)
        result['loader_provenance'] = inputs
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({'schema_version': 1, 'status': 'blocked', 'inputs': inputs,
                          'blocker': type(exc).__name__ + ': ' + str(exc)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
