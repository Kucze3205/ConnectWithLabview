"""Replay the single pinned WM1 declaration measurement; no LabVIEW or corpus scan.
Run from repository root: python3 docs/research/0100-wm1-version-evidence.py
Requires the prepared sources at LABVIEW_ENVIRONMENT; writes only the sibling JSON.
"""
import collections
import hashlib
import json
import os
import pathlib
import subprocess
import sys

sys.dont_write_bytecode = True
PREFIX = pathlib.Path('docs/research/0100-wm1-version-evidence')
PARSER_REV = '35d2a0318f71dcb87bb9c431dc00700ee6b9fb75'
ORIGINAL_REV = '371c631c16155d88f02be11a953e4964d7452fd8'
ORIGINAL = 'actor-framework/Core/ActorFramework/Message Dequeuer/Equals Not A Refnum.vi'
PINS = {
    'benchmark/writing/method.json': '8c3b165c33c8fb4944f10a0eaa3c384fcc90d62c3278c0c910a5f2ae8b9d4da1',
    '@environment/' + ORIGINAL: '19b5dcd98b3b2e83e2b533d9227bd07d16837f350243377292b7c0b8a935338c',
    '@environment/pylavi/pylavi/file.py': 'f3c9d38054291d02bf48e7f2658c2b012e0c0b7a7fb55731710e985d7df2cce9',
    '@environment/pylavi/pylavi/resource_types.py': 'ce333fba1b8dc689197e18e4a1acedf77b786f098f5039e4234c136f73512756',
}
record = {
    'schema_version': 1,
    'status': 'blocked',
    'blocker': 'Extraction not completed.',
    'starting_state': {
        'commit': '06cadfb64f1412f11a8e670f13b15a0f48711375',
        'tree': 'e7a2dd977f6a1930522b28d439bcece18ea01fa6',
        'git_status_short': '',
        'captured_before_outputs': True,
    },
    'inputs': {'pins': [], 'parser_revision_required': PARSER_REV},
    'entries': [],
    'conclusion': {'measurement': 'Not completed; do not infer a version.'},
    'limitations': [
        'Offline observation of one immutable original and third-party parser interpretation only.',
        'Independent authoritative original-save-version confirmation is unavailable; declarations alone do not discharge WM1-original-save-version.',
        'Agreeing declarations establish neither native compatibility nor preservation, semantic writing feasibility, method readiness or a 2024 fallback.',
        'No LabVIEW execution, semantic edit, benchmark run, corpus scan or protected-input change.',
    ],
    'invocation': 'python3 docs/research/0100-wm1-version-evidence.py',
    'environment_requirement': 'LABVIEW_ENVIRONMENT points to prepared source root; run from repository root with Python 3.',
    'parser_locators': {
        'Resources.load': 'pylavi/file.py:420-465',
        'Resources.get_resources': 'pylavi/file.py:331-338 (list preserves all entries, including duplicate IDs)',
        'resource_payload_framing': 'pylavi/file.py:413-418 (four-byte length prefix excluded from returned payload)',
        'Typevers': 'pylavi/resource_types.py:221-268; version is first field at payload byte 0',
        'TypeLVSR': 'pylavi/resource_types.py:115-121,210-215; version is first field at payload byte 0',
        'Structure.from_bytes': 'pylavi/data_types.py:334-340',
        'integer_decoding': 'pylavi/data_types.py:74-101,158-162 (unsigned big-endian UInt32)',
        'Version': 'pylavi/data_types.py:657-664,744-782,802-825 (tuple order major,minor,patch,phase,build; phase 4=release)',
        'Header.VERSION': 'pylavi/file.py:27,75 (container framing constant, not used as save-version evidence)',
    },
}

def save():
    PREFIX.with_suffix('.json').write_text(json.dumps(record, indent=2) + '\n')


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


save()
try:
    env = pathlib.Path(os.environ['LABVIEW_ENVIRONMENT'])
    record['inputs']['prepared_root_observed'] = str(env)
    record['invocation_state'] = {'commit': git('rev-parse', 'HEAD'), 'tree': git('rev-parse', 'HEAD^{tree}')}
    for logical, expected in PINS.items():
        path = env / logical.removeprefix('@environment/') if logical.startswith('@environment/') else pathlib.Path(logical)
        observed = digest(path.read_bytes())
        record['inputs']['pins'].append({'path': logical, 'expected_sha256': expected, 'sha256': observed, 'matches': observed == expected})
        save()
        require(observed == expected, 'SHA256 mismatch: ' + logical)
    for name, expected in [('pylavi', PARSER_REV), ('actor-framework', ORIGINAL_REV)]:
        actual = git('-C', str(env / name), 'rev-parse', 'HEAD')
        record['inputs'][name + '_revision'] = actual
        require(actual == expected, 'Revision mismatch: ' + name)
    readiness_bytes = (env / 'readiness.json').read_bytes()
    readiness = json.loads(readiness_bytes)
    record['inputs']['readiness'] = {'path': '@environment/readiness.json', 'sha256': digest(readiness_bytes), 'public_sources': readiness.get('public_sources'), 'sources': readiness.get('sources'), 'authority_limit': 'Prepared-source availability only; native/model fields are not current execution tests.'}
    require(readiness.get('public_sources') == 'ready', 'Prepared sources not ready')
    sources = {s['name']: s['commit'] for s in readiness['sources']}
    require(sources.get('pylavi') == PARSER_REV and sources.get('actor-framework') == ORIGINAL_REV, 'Readiness source revision mismatch')
    method = json.loads(pathlib.Path('benchmark/writing/method.json').read_text())
    wm1 = method['tasks'][1]
    record['inputs']['wm1_requirement'] = {'locator': 'benchmark/writing/method.json:/tasks/1', 'id': wm1['id'], 'original': wm1['originals'][0], 'preservation_id': 'WM1-original-save-version', 'oracle_missing': wm1['oracle']['missing'], 'changed': False}
    require(wm1['originals'][0]['path'] == ORIGINAL and wm1['originals'][0]['sha256'] == PINS['@environment/' + ORIGINAL], 'WM1 original pin differs')
    data_types = env / 'pylavi/pylavi/data_types.py'
    record['inputs']['directly_required_definition'] = {'path': '@environment/pylavi/pylavi/data_types.py', 'sha256': digest(data_types.read_bytes()), 'revision': PARSER_REV}
    sys.path.insert(0, str(env / 'pylavi'))
    from pylavi.file import Resources
    from pylavi.resource_types import Typevers, TypeLVSR
    resources = Resources.load(str(env / ORIGINAL))
    record['enumeration'] = {'method': 'Resources.get_resources for each of vers and LVSR; never get_resource by ID or a dictionary keyed by ID', 'counts': {}, 'duplicate_ids': {}, 'absent_types': [], 'malformed_entries': [], 'tuple_order': ['major', 'minor', 'patch', 'phase', 'build']}
    for resource_type, cls in [('vers', Typevers), ('LVSR', TypeLVSR)]:
        all_entries = resources.get_resources(resource_type)
        counts = collections.Counter(r[0] for r in all_entries)
        record['enumeration']['counts'][resource_type] = len(all_entries)
        record['enumeration']['duplicate_ids'][resource_type] = [{'id': k, 'count': v} for k, v in counts.items() if v > 1]
        if not all_entries:
            record['enumeration']['absent_types'].append(resource_type)
        for ordinal, (resource_id, name, payload) in enumerate(all_entries):
            entry = {'type': resource_type, 'ordinal_within_type': ordinal, 'resource_id': resource_id, 'name_hex': None if name is None else name.hex(), 'length': len(payload), 'payload_hex': payload.hex(), 'payload_sha256': digest(payload), 'version_field': {'offset': 0, 'offset_basis': 'zero-based within returned resource payload, excluding resource length prefix', 'length': 4, 'raw_hex': payload[:4].hex()}, 'parser_class': 'pylavi.resource_types.' + cls.__name__, 'decode_status': 'pending'}
            record['entries'].append(entry)
            save()
            try:
                decoded = cls().from_bytes(payload)
                v = decoded.version
                require(v.size() == 4 and len(payload) >= 4, 'Invalid version field width')
                entry.update({'decode_status': 'decoded', 'decoded_version_uint32': v.value, 'decoded_version_hex': format(v.value, '08x'), 'decoded_tuple': [v.major(), v.minor(), v.patch(), v.phase(), v.build()], 'decoded_value': v.to_value(), 'decoded_structure': decoded.to_value(), 'parsed_size': decoded.size(), 'trailing_hex': payload[decoded.size():].hex()})
            except Exception as exc:
                entry.update({'decode_status': 'malformed', 'error': type(exc).__name__ + ': ' + str(exc)})
                record['enumeration']['malformed_entries'].append({'type': resource_type, 'ordinal_within_type': ordinal, 'resource_id': resource_id})
                raise
            save()
    values = {tuple(e['decoded_tuple']) for e in record['entries']}
    record['status'] = 'measured'
    record.pop('blocker', None)
    record['conclusion'] = {
        'agreement': 'agree' if len(values) == 1 and not record['enumeration']['absent_types'] else ('conflict' if len(values) > 1 else 'absent-or-incomplete'),
        'decoded_tuples': [list(v) for v in sorted(values)],
        'measurement': 'Every vers/LVSR declaration in the one pinned original is retained above; values are pinned-parser interpretations of the recorded bytes.',
        'uncertainty_narrowed': 'WM1 original version declarations were unmeasured; their presence, raw bytes and pinned-class interpretations are now measured.',
        'authoritative_original_save_version': None,
        'independent_save_version_confirmation': 'unavailable',
        'wm1_requirement': 'Original save_version remains unavailable in unchanged method.json; observed declarations are supporting evidence, not an authoritative replacement.',
        'next_action': 'Carry this one-original evidence into independent save-version confirmation before freezing WM1 original/output version-preservation checks; retain the missing-authority status until then.',
    }
    save()
    print(json.dumps({'status': record['status'], 'counts': record['enumeration']['counts'], 'versions': [{'type': e['type'], 'id': e['resource_id'], 'raw': e['version_field']['raw_hex'], 'tuple': e['decoded_tuple'], 'value': e['decoded_value']} for e in record['entries']], 'agreement': record['conclusion']['agreement']}))
except Exception as exc:
    record['status'] = 'blocked'
    record['blocker'] = type(exc).__name__ + ': ' + str(exc)
    record['conclusion'] = {'measurement': 'Stopped at pin/readiness/parse failure; retained inputs and any raw entries, without substituting a fixture.', 'next_action': 'Resolve the exact saved blocker, then replay this script against the same pins only.'}
    save()
    print(json.dumps({'status': 'blocked', 'blocker': record['blocker']}))
    sys.exit(1)
