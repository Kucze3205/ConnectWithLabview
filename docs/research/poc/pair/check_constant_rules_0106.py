#!/usr/bin/env python3
"""Validate committed #533 evidence, never native LabVIEW validity.

Standard library and committed files only. No prepared environment, session
artifacts, network, VI writes, replay rerun, or --self-check is used.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
BASE = 'docs/research/poc/pair/'
POC = 'docs/research/poc/'
REV = '35d2a0318f71dcb87bb9c431dc00700ee6b9fb75'
EXPECTED_CONCLUSIONS = dict(P0='supported', P1='supported', P2='supported',
    P3='unknown', P4='refuted', P5='supported', P6='unknown', P7='refuted',
    P8='supported', P9='unknown')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def keys(value, expected, label):
    require(isinstance(value, dict) and set(value) == set(expected.split()), 'Malformed ' + label)


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()), 'Missing ' + label)


def strings(value, label):
    require(isinstance(value, list) and bool(value), 'Missing ' + label)
    for item in value:
        nonempty(item, label)


def digest(value, count=64):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{' + str(count) + '}', value) is not None


def sha(data):
    return hashlib.sha256(data).hexdigest()


def validate(evidence, root=ROOT):
    keys(evidence, 'schema_version verdict input_hashes source_pins repository_source_pins probes unresolved limitations invocation offset_basis native_validity_established repository_revision repository_input_basis', 'evidence')
    require(type(evidence['schema_version']) is int and evidence['schema_version'] == 1, 'schema_version must be 1')
    require(evidence['verdict'] in ('rules-supported', 'needs-evidence', 'source-blocked'), 'Invalid verdict')
    require(evidence['native_validity_established'] is False, 'Evidence must not claim native validity')
    require(digest(evidence['repository_revision'], 40), 'Invalid repository revision')
    for field in ('invocation', 'offset_basis', 'repository_input_basis'):
        nonempty(evidence[field], field)
    strings(evidence['limitations'], 'limitations')
    strings(evidence['unresolved'], 'unresolved')
    hashes = evidence['input_hashes']
    require(isinstance(hashes, dict) and hashes, 'Missing repository evidence hashes')
    required = {BASE + n for n in ('findings-0105.md', 'candidates-0105.json',
        'replay-0105-status.json', 'fixtures/pins.json', 'fixtures/authoring.md',
        'constant-1-separate--constant-2-separate.json',
        'constant-1-normal--constant-2-normal.json',
        'constant-1-normal--constant-1-separate.json',
        'constant-2-normal--constant-2-separate.json', 'probe_constant_rules_0106.py')}
    required.update(POC + n for n in ('inspect_vi.py', 'heap-labels.json',
        'edit-readiness.md', 'source-provenance.json', 'heap-format-source.md',
        'LVheap-source.txt', 'LVmisc-source.txt', 'LVparts-source.txt',
        'step3/source-search.json', 'step3/source-provenance.json'))
    required.add('docs/perpetua/environment.md')
    require(required <= set(hashes), 'Missing required input hash')
    for path, expected in hashes.items():
        require(isinstance(path, str) and not Path(path).is_absolute() and
                '..' not in Path(path).parts and path.startswith('docs/'), 'Invalid repository input path')
        resolved = (root / path).resolve()
        require(resolved.is_relative_to(root.resolve()), 'Input escapes repository')
        require(digest(expected), 'Malformed SHA256: ' + path)
        require(resolved.is_file(), 'Missing evidence: ' + path)
        require(sha(resolved.read_bytes()) == expected, 'Input SHA256 mismatch: ' + path)

    def load(path):
        require(path in hashes, 'Unpinned consumed evidence: ' + path)
        return json.loads((root / path).read_text())

    replay = load(BASE + 'replay-0105-status.json')
    for path, expected in replay['input_hashes'].items():
        require(hashes.get(path) == expected, 'Original replay pin changed: ' + path)
    for run in replay['runs']:
        require(run['output'] in hashes, 'Unpinned saved replay output')
    manifest = load(BASE + 'fixtures/pins.json')
    comparisons = {m: load(BASE + f'constant-1-{m}--constant-2-{m}.json') for m in ('separate', 'normal')}
    probes = evidence['probes']
    require(isinstance(probes, list) and len(probes) == 10, 'Missing/extra probes')
    by_id = {}
    for p in probes:
        keys(p, 'id hypothesis provenance observed conclusion reason', 'probe')
        require(p['id'] in EXPECTED_CONCLUSIONS and p['id'] not in by_id, 'Invalid/duplicate probe ID')
        require(p['conclusion'] == EXPECTED_CONCLUSIONS[p['id']], 'Contradictory probe conclusion: ' + p['id'])
        strings(p['provenance'], 'probe provenance')
        for name in ('hypothesis', 'reason'):
            nonempty(p[name], 'probe ' + name)
        require(isinstance(p['observed'], dict) and p['observed'], 'Missing probe observations')
        by_id[p['id']] = p
    require(set(by_id) == set(EXPECTED_CONCLUSIONS), 'Incomplete probes')
    # For this pinned investigation P3/P6/P9 remain unknown. Any future positive
    # result needs new evidence and a revised checker, not a verdict-only change.
    require(evidence['verdict'] == 'source-blocked', 'Verdict contradicts unavailable source results')
    obs = {pid: p['observed'] for pid, p in by_id.items()}
    expected_checks = []
    for mode, comp in comparisons.items():
        for item in comp['inputs'].values():
            path = item['path']
            expected = manifest['files'][Path(path).name]
            require(hashes[path] == item['sha256'] == expected == replay['input_hashes'][path], 'Saved constant pin mismatch')
            expected_checks.append(dict(path=path, actual_sha256=hashes[path], comparison_sha256=item['sha256'],
                manifest_sha256=expected, replay_sha256=replay['input_hashes'][path], match=True))
    require(obs['P0'] == dict(checks=expected_checks, protected_replay_inputs={p: True for p in replay['input_hashes']}), 'P0 pin observations contradict committed inputs')

    pins = evidence['source_pins']
    require(isinstance(pins, list) and len(pins) == 8, 'Missing prepared source pins')
    source_by_path = {}
    for pin in pins:
        keys(pin, 'path original_path revision sha256 kind citations', 'prepared source pin')
        path = pin['path']
        require(isinstance(path, str) and path.startswith('@environment/') and '..' not in Path(path).parts, 'Invalid prepared path')
        require(path not in source_by_path, 'Duplicate prepared source pin')
        require(pin['revision'] == REV and digest(pin['sha256']), 'Malformed prepared source revision/hash')
        require(pin['kind'] in ('source', 'prepared-metadata'), 'Invalid prepared source kind')
        nonempty(pin['original_path'], 'original source path')
        require(not Path(pin['original_path']).is_absolute() and '..' not in Path(pin['original_path']).parts, 'Invalid original source path')
        require(isinstance(pin['citations'], list) and pin['citations'], 'Missing source citations')
        for cite in pin['citations']:
            require(isinstance(cite, dict) and set(cite) in ({'symbol'}, {'symbol', 'lines'}), 'Malformed source citation')
            nonempty(cite['symbol'], 'source symbol')
            if 'lines' in cite:
                lines = cite['lines']
                require(isinstance(lines, list) and len(lines) == 2 and all(type(n) is int for n in lines) and 0 < lines[0] <= lines[1], 'Invalid source lines')
        source_by_path[path] = pin
    old = load(POC + 'step3/source-search.json')
    prior = [f for f in old['files'] if f['origin'] == 'prepared']
    expected_paths = {'@environment/' + f['path'] for f in prior}
    expected_paths.update(('@environment/readiness.json', '@environment/pylavi/tests/test_resource_type_BDPW.py'))
    require(set(source_by_path) == expected_paths, 'Missing/wrong prepared source inventory')
    expected_prior = []
    for f in prior:
        path = '@environment/' + f['path']
        require(source_by_path[path]['sha256'] == f['sha256'], 'Prior unchanged-source claim contradicts pin')
        require(source_by_path[path]['original_path'] == str(Path(f['path']).relative_to('pylavi')), 'Original source path mismatch')
        expected_prior.append(dict(path=path, sha256=f['sha256'], prior_sha256=f['sha256'], unchanged=True))
    for comp in comparisons.values():
        loader = comp['loader_provenance']
        require(source_by_path['@environment/readiness.json']['sha256'] == loader['readiness']['sha256'], 'Readiness pin differs from replay')
        for f in loader['source_pins']:
            require(source_by_path[f['path']]['sha256'] == f['sha256'], 'Parser source pin differs from replay')
    p4 = obs['P4']
    keys(p4, 'pylavi_revision tracked_status prior_source_checks inventory_roots missing_module_globs prior_terms stop available_dependency', 'P4 observations')
    require(p4['prior_source_checks'] == expected_prior and p4['pylavi_revision'] == REV and p4['tracked_status'] == '', 'P4 prior-source mismatch')
    require(p4['missing_module_globs'] == {'LVblock*': [], 'LVdatatype*': [], 'LVrsrc*': []}, 'P4 unavailable-source contradiction')
    require(p4['inventory_roots'] == ['actor-framework', 'pylavi', 'readiness.json'], 'P4 unexpected inventory')
    strings(p4['prior_terms'], 'prior search terms')
    nonempty(p4['stop'], 'source branch stopping reason')
    nonempty(p4['available_dependency'], 'available dependency')
    repo_sources = evidence['repository_source_pins']
    require(isinstance(repo_sources, list) and len(repo_sources) == 4, 'Missing saved-source provenance')
    original_sources = {POC + f['file']: f for f in load(POC + 'source-provenance.json')}
    require({p['path'] for p in repo_sources} == {POC + n for n in ('LVheap-source.txt', 'LVmisc-source.txt', 'LVparts-source.txt', 'heap-format-source.md')}, 'Wrong saved-source inventory')
    for p in repo_sources:
        keys(p, 'path sha256 revision url symbol', 'repository source pin')
        require(p['sha256'] == hashes[p['path']] == original_sources[p['path']]['sha256'], 'Saved source pin mismatch')
        require(digest(p['revision'], 40) and '/' + p['revision'] + '/' in p['url'] and p['url'] == original_sources[p['path']]['url'], 'Saved source revision mismatch')
        nonempty(p['symbol'], 'saved source symbol')

    # Reparse only original committed artifacts with the existing pinned inspector.
    spec = importlib.util.spec_from_file_location('inspect_0106_check', root / (POC + 'inspect_vi.py'))
    inspector = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inspector)
    labels = load(POC + 'heap-labels.json')
    parsed, resources = {}, {}
    node_keys = 'heap_offset end header scope tag name size_spec data_offset data_length content_hex attributes'.split()
    for comp in comparisons.values():
        for item in comp['inputs'].values():
            path = root / item['path']
            d = inspector.inspect(path)
            require(d['status'] == 'complete', 'Original heap parse failed')
            inspector.annotate(d, labels)
            parsed[path.name] = d
            raw = path.read_bytes()
            resources[path.name] = {r['type']: raw[r['payload_offset']:r['payload_offset'] + r['payload_length']]
                                     for r in inspector.rsrc_resources(raw) if r['id'] == 0}
    contexts = obs['P1']['contexts']
    require(set(contexts) == set(parsed), 'Missing bounded heap context')
    for name, d in parsed.items():
        compact = lambda n: {k: n[k] for k in node_keys}
        expected = dict(heap_bytes=d['heap_bytes'], heap_length=d['heap_length'], heap_sha256=d['heap_sha256'],
            parse_status=d['status'], consumed=d['consumed'],
            nodes=[compact(n) for n in d['entries'] if 306 <= n['heap_offset'] <= 330 or n['name'] in ('OF__ConstValue', 'OF__typeDesc')],
            constant_parent=compact(next(n for n in d['entries'] if n['heap_offset'] == 201)),
            numeric_display=compact(next(n for n in d['entries'] if n['heap_offset'] == 217)))
        require(contexts[name] == expected, 'Recorded node context differs from committed fixture: ' + name)
    p1 = obs['P1']
    keys(p1, 'contexts inserted_hex inserted_span header_hex header_decode body_hex body_span parent_class parent_tag parent_offset prior_child meaning', 'P1 observations')
    fixed = dict(inserted_hex='44200200', inserted_span=[312, 316], header_hex='4420',
        header_decode=dict(size_spec=2, scope=1, raw_tag=32, tag=1), body_hex='0200',
        body_span=[314, 316], parent_class=1, parent_tag=270, parent_offset=306, prior_child='OF__mode')
    require(all(p1[k] == v for k, v in fixed.items()), 'P1 boundary contradiction')
    nonempty(p1['meaning'], 'P1 interpretation limit')
    p2 = obs['P2']
    keys(p2, 'left_node_span right_node_span left_body_span right_body_span left_hex right_hex header_hex changed_offsets parent_class parent_uid type_references note', 'P2 observations')
    fixed2 = dict(left_node_span=[540, 546], right_node_span=[544, 550], left_body_span=[542, 546],
        right_body_span=[546, 550], left_hex='00000001', right_hex='00000002', header_hex='866c',
        changed_offsets=[545, 549], parent_class=19, parent_uid=118, type_references=dict(dco='03', display='04'))
    require(all(p2[k] == v for k, v in fixed2.items()), 'P2 value/type boundary contradiction')
    nonempty(p2['note'], 'P2 type limit')
    for name, d in parsed.items():
        const = [n for n in d['entries'] if n['name'] == 'OF__ConstValue']
        require(len(const) == 1, 'Ambiguous constant node')
        n = const[0]
        value = 1 if 'constant-1-' in name else 2
        delta = 0 if value == 1 else 4
        require((n['heap_offset'], n['data_offset'], n['end'], n['header'], n['content_hex']) ==
                (540 + delta, 542 + delta, 546 + delta, 0x866c, f'{value:08x}'), 'ConstValue body mismatch')
        entries = {n['heap_offset']: n for n in d['entries']}
        require(entries[306]['tag'] == 270 and entries[306]['attributes'][0]['value'] == 1, 'textRec context mismatch')
        require(entries[312]['name'] == ('OF__mode' if value == 1 else 'OF__flags'), 'Inserted node mismatch')
        require([a['value'] for a in entries[201]['attributes']] == [19, 118], 'Constant parent class/UID mismatch')
        refs = [n['content_hex'] for n in d['entries'] if n['name'] == 'OF__typeDesc']
        require('03' in refs and '04' in refs, 'Heap type reference mismatch')
    p3 = obs['P3']
    keys(p3, 'typed_constvalue heap_type_resolution generic_factory body_interpretation flags_insertion_requirement', 'P3 observations')
    require(p3['typed_constvalue'] is False and p3['flags_insertion_requirement'] == 'unknown', 'P3 unknown encoding contradicted')
    for k in ('heap_type_resolution', 'generic_factory', 'body_interpretation'):
        nonempty(p3[k], 'P3 ' + k)
    p5 = obs['P5']
    keys(p5, 'md5_empty_ascii results checks_only', 'P5 observations')
    require(p5['md5_empty_ascii'] == hashlib.md5(b'').hexdigest(), 'Wrong empty ASCII MD5')
    expected_passwords = []
    for name, data in sorted(resources.items()):
        payload = data['BDPW']
        require(len(payload) == 48, 'Unexpected BDPW length')
        expected_passwords.append(dict(fixture=name, chunks=[payload[o:o + 16].hex() for o in (0, 16, 32)],
            has_password=False, empty_ascii_password_matches=True, lvsr_locked=False))
        require(payload[:16] == hashlib.md5(b'').digest(), 'Chunk-0 dependency failed')
        require(int.from_bytes(data['LVSR'][4:8], 'big') & 0x2000 == 0, 'Unexpected locked flag')
    require(p5['results'] == expected_passwords, 'P5 password observations contradict inputs')
    nonempty(p5['checks_only'], 'P5 scope')
    p6 = obs['P6']
    keys(p6, 'recipe_available tested_recipes missing opaque_resources', 'P6 observations')
    require(p6['recipe_available'] is False and p6['tested_recipes'] == [], 'Unavailable recipe contradiction')
    nonempty(p6['missing'], 'P6 missing source')
    strings(p6['opaque_resources'], 'P6 opaque resources')
    controls = []
    for value in (1, 2):
        a, b = (resources[f'constant-{value}-{mode}.vi'] for mode in ('normal', 'separate'))
        controls.append(dict(value=value, raw_BDHb_equal=a['BDHb'] == b['BDHb'], BDPW_equal=a['BDPW'] == b['BDPW'],
            chunks_1_2_equal=a['BDPW'][16:] == b['BDPW'][16:], RTSG_equal=a['RTSG'] == b['RTSG']))
    require(obs['P7'] == dict(save_mode_controls=controls), 'P7 control observations mismatch')
    require(all(c['raw_BDHb_equal'] and not c['chunks_1_2_equal'] for c in controls), 'P7 refutation lacks counterexample')
    p8 = obs['P8']
    keys(p8, 'resource_summary cross_modes DFDS_separate_present normal_DFDS_offset equality_scope', 'P8 observations')
    summaries = {}
    for mode, comp in comparisons.items():
        selected = {}
        for r in comp['resources']:
            if r['type'] in ('BDHb', 'DFDS', 'VCTP', 'DTHP', 'VICD', 'CPC2', 'BDPW', 'RTSG', 'LVSR'):
                selected[r['type']] = dict(raw_different=r['raw']['different'], left_length=r['raw']['left_length'], right_length=r['raw']['right_length'])
                if 'decompressed' in r:
                    de = r['decompressed']
                    selected[r['type']]['decompressed'] = {k: de[k] for k in ('left_length', 'right_length', 'left_sha256', 'right_sha256', 'different')}
                    if r['type'] == 'DFDS':
                        selected[r['type']]['ranges'] = de['ranges']
        summaries[mode] = selected
    require(p8['resource_summary'] == summaries and p8['cross_modes'] == controls, 'P8 differs from saved comparison')
    require(p8['DFDS_separate_present'] is False and p8['normal_DFDS_offset'] == 223, 'P8 DFDS contradiction')
    require(all('DFDS' not in resources[f'constant-{v}-separate.vi'] for v in (1, 2)), 'Separate DFDS unexpectedly present')
    require(summaries['normal']['DFDS']['ranges'] == [dict(offset=223, length=1, left_hex='01', right_hex='02')], 'Normal DFDS result mismatch')
    for mode in summaries:
        require(not summaries[mode]['VCTP']['raw_different'] and not summaries[mode]['DTHP']['raw_different'], 'Type equality contradicted')
    require(not summaries['normal']['VICD']['raw_different'], 'Normal VICD equality contradicted')
    nonempty(p8['equality_scope'], 'P8 limits')
    p9 = obs['P9']
    keys(p9, 'lvsr_flags_word_offset normal_flags_word separate_flags_word unknowns unchanged_save_control_present native_validation', 'P9 observations')
    require(p9['unchanged_save_control_present'] is False and p9['native_validation'] is False, 'P9 claims unavailable validation')
    strings(p9['unknowns'], 'P9 unknowns')
    require(p9['lvsr_flags_word_offset'] == 8 and p9['normal_flags_word'] == '20000200' and p9['separate_flags_word'] == '20000600', 'P9 LVSR flag contradiction')
    for name, data in resources.items():
        require(data['LVSR'][8:12].hex() == p9['normal_flags_word' if '-normal.' in name else 'separate_flags_word'], 'LVSR word differs from fixture')
    for p in probes:
        for cite in p['provenance']:
            path = cite.split('#', 1)[0].split(':', 1)[0]
            require(path in hashes or path in source_by_path, 'Unpinned probe provenance: ' + path)
    return dict(status='passed', verdict=evidence['verdict'], repository_inputs=len(hashes),
                prepared_source_pins=len(pins), probes=len(probes), native_validity_established=False)


def main():
    try:
        evidence = json.loads((ROOT / (BASE + 'constant-rules-0106.json')).read_text())
        print(json.dumps(validate(evidence), sort_keys=True))
    except (ValueError, KeyError, TypeError, OSError, StopIteration, IndexError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
