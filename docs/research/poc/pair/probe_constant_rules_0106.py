#!/usr/bin/env python3
"""Read-only, bounded session probe; needs prepared sources, never writes a VI.

The separate check_constant_rules_0106.py verifies committed evidence offline.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'docs/research/poc/pair'
ENV = Path(os.environ['LABVIEW_ENVIRONMENT'])
REV = '35d2a0318f71dcb87bb9c431dc00700ee6b9fb75'
SNAP_REV = '5f20e23de6a386021eb955c825cc43d221f09ff1'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def relative(path):
    return str(path.relative_to(ROOT))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def main():
    status = read_json(BASE / 'replay-0105-status.json')
    names = ['findings-0105.md', 'candidates-0105.json', 'replay-0105-status.json',
             'constant-1-separate--constant-2-separate.json',
             'constant-1-normal--constant-2-normal.json',
             'constant-1-normal--constant-1-separate.json',
             'constant-2-normal--constant-2-separate.json']
    paths = {BASE / n for n in names}
    paths.update(ROOT / p for p in status['input_hashes'])
    paths.update(ROOT / run['output'] for run in status['runs'])
    paths.update(ROOT / p for p in [
        'docs/perpetua/environment.md', 'docs/research/poc/inspect_vi.py',
        'docs/research/poc/heap-labels.json', 'docs/research/poc/edit-readiness.md',
        'docs/research/poc/heap-format-source.md', 'docs/research/poc/source-provenance.json',
        'docs/research/poc/LVheap-source.txt', 'docs/research/poc/LVmisc-source.txt',
        'docs/research/poc/LVparts-source.txt', 'docs/research/poc/step3/source-search.json',
        'docs/research/poc/step3/source-provenance.json'])
    paths.add(Path(__file__).resolve())
    hashes = {relative(p): sha(p.read_bytes()) for p in sorted(paths)}
    probes = []

    def probe(pid, hypothesis, provenance, observed, conclusion, reason):
        probes.append(dict(id=pid, hypothesis=hypothesis, provenance=provenance,
                           observed=observed, conclusion=conclusion, reason=reason))

    comparisons = {mode: read_json(BASE / f'constant-1-{mode}--constant-2-{mode}.json')
                   for mode in ('separate', 'normal')}
    manifest = read_json(BASE / 'fixtures/pins.json')
    checks = []
    for mode, comparison in comparisons.items():
        for side, item in comparison['inputs'].items():
            actual = hashes[item['path']]
            expected_manifest = manifest['files'][Path(item['path']).name]
            expected_replay = status['input_hashes'][item['path']]
            checks.append(dict(path=item['path'], actual_sha256=actual,
                               comparison_sha256=item['sha256'], manifest_sha256=expected_manifest,
                               replay_sha256=expected_replay,
                               match=actual == item['sha256'] == expected_manifest == expected_replay))
    protected = {p: hashes[p] == h for p, h in status['input_hashes'].items()}
    probe('P0', 'Original constant VIs match saved pins before any heap/password probes.',
          ['docs/research/poc/pair/fixtures/pins.json#files',
           'docs/research/poc/pair/replay-0105-status.json#input_hashes'] +
          [relative(BASE / f'constant-1-{m}--constant-2-{m}.json') + '#inputs' for m in comparisons],
          dict(checks=checks, protected_replay_inputs=protected),
          'supported' if all(c['match'] for c in checks) and all(protected.values()) else 'refuted',
          'Saved expected pins were compared, never refreshed.')
    assert all(c['match'] for c in checks) and all(protected.values()), 'Original pin mismatch; do not probe or refresh pins'

    old = read_json(ROOT / 'docs/research/poc/step3/source-search.json')
    source_pins = []
    prior_checks = []
    citations = {
        '__init__.py': [(1, 3, 'package imports')],
        'assembler.py': [(1, 53, 'assembler; unchanged prior search')],
        'data_types.py': [(383, 450, 'Array; unchanged prior search')],
        'file.py': [(421, 465, 'Resources resource access; unchanged prior search')],
        'resource_types.py': [(54, 93, 'TypeBDPW'), (97, 121, 'TypeLVSR flags'),
                              (205, 215, 'TypeLVSR.separate_code/from_bytes')],
        'validate.py': [(418, 431, 'validate_locked_password')],
    }
    actual_rev = subprocess.check_output(['git', '-C', str(ENV / 'pylavi'), 'rev-parse', 'HEAD'], text=True).strip()
    tracked_status = subprocess.check_output(['git', '-C', str(ENV / 'pylavi'), 'status', '--porcelain', '--untracked-files=no'], text=True).strip()
    assert actual_rev == REV and not tracked_status
    for item in old['files']:
        if item['origin'] != 'prepared':
            continue
        p = ENV / item['path']
        digest = sha(p.read_bytes())
        prior_checks.append(dict(path='@environment/' + item['path'], sha256=digest,
                                 prior_sha256=item['sha256'], unchanged=digest == item['sha256']))
        source_pins.append(dict(path='@environment/' + item['path'], original_path=str(Path(item['path']).relative_to('pylavi')),
                                revision=REV, sha256=digest, kind='source',
                                citations=[dict(lines=[a, min(b, len(p.read_text().splitlines()))], symbol=s)
                                           for a, b, s in citations[p.name]]))
    test = ENV / 'pylavi/tests/test_resource_type_BDPW.py'
    source_pins.append(dict(path='@environment/pylavi/tests/test_resource_type_BDPW.py',
                            original_path='tests/test_resource_type_BDPW.py', revision=REV,
                            sha256=sha(test.read_bytes()), kind='source',
                            citations=[dict(lines=[7, 23], symbol='test_basics')]))
    source_pins.append(dict(path='@environment/readiness.json', original_path='readiness.json',
                            revision=REV, sha256=sha((ENV / 'readiness.json').read_bytes()),
                            kind='prepared-metadata', citations=[dict(symbol='sources[ name=pylavi ].commit')]))
    assert all(c['unchanged'] for c in prior_checks)
    absent = {pattern: [str(p.relative_to(ENV)) for p in ENV.rglob(pattern)]
              for pattern in ('LVblock*', 'LVdatatype*', 'LVrsrc*')}
    probe('P4', 'Prepared sources add a heap/type or BDPW integrity implementation beyond the prior POC search.',
          ['docs/research/poc/step3/source-search.json#files',
           'docs/research/poc/edit-readiness.md#source-derived-limitation'],
          dict(pylavi_revision=actual_rev, tracked_status=tracked_status, prior_source_checks=prior_checks,
               inventory_roots=sorted(p.name for p in ENV.iterdir()), missing_module_globs=absent,
               prior_terms=['BDPW', 'ConstValue', 'DTHP', 'VCTP', 'integrity_cache', 'constant_encoding'],
               stop='Six production source hashes match the previous search: reuse its absence; no repeated broad search.',
               available_dependency='TypeBDPW chunk-0 ASCII-password MD5 only; test_basics tests serialization/password checks.'),
          'refuted', 'No additional prepared implementation was found in this bounded inventory; no LVblock/LVdatatype/LVrsrc is staged.')

    inspector = module('inspect_0106', ROOT / 'docs/research/poc/inspect_vi.py')
    labels = inspector.load_labels()
    fixture_data, parsed = {}, {}
    for mode, comp in comparisons.items():
        for side, item in comp['inputs'].items():
            p = ROOT / item['path']
            raw = p.read_bytes()
            resources = inspector.rsrc_resources(raw)
            data = {r['type']: raw[r['payload_offset']:r['payload_offset'] + r['payload_length']]
                    for r in resources if r['id'] == 0}
            d = inspector.inspect(p)
            assert d['status'] == 'complete'
            inspector.annotate(d, labels)
            fixture_data[p.name] = data
            parsed[p.name] = d

    def compact(node):
        keys = ('heap_offset', 'end', 'header', 'scope', 'tag', 'name', 'size_spec',
                'data_offset', 'data_length', 'content_hex', 'attributes')
        return {k: node[k] for k in keys}

    contexts = {}
    for name, d in parsed.items():
        entries = d['entries']
        context = [compact(n) for n in entries if 306 <= n['heap_offset'] <= 330 or
                   n['name'] == 'OF__ConstValue' or n['name'] == 'OF__typeDesc']
        contexts[name] = dict(heap_bytes=d['heap_bytes'], heap_length=d['heap_length'],
                              heap_sha256=d['heap_sha256'], parse_status=d['status'], consumed=d['consumed'],
                              nodes=context,
                              constant_parent=compact(next(n for n in entries if n['heap_offset'] == 201)),
                              numeric_display=compact(next(n for n in entries if n['heap_offset'] == 217)))
    probe('P1', 'The aligned four-byte insertion is a complete textRec flags leaf, separate from the constant value.',
          ['docs/research/poc/inspect_vi.py:80-123#parse_heap',
           'docs/research/poc/LVheap-source.txt:1489-1530#HeapNode.parseRSRCData',
           'docs/research/poc/LVheap-source.txt:1113-1130#OBJ_TEXT_HAIR_TAGS',
           'docs/research/poc/pair/candidates-0105.json#bdhb_alignments[2:4]'],
          dict(contexts=contexts, inserted_hex='44200200', inserted_span=[312, 316], header_hex='4420',
               header_decode=dict(size_spec=2, scope=1, raw_tag=32, tag=1),
               body_hex='0200', body_span=[314, 316], parent_class=1,
               parent_tag=270, parent_offset=306, prior_child='OF__mode',
               meaning='Source labels flags in textHair; no bit-0x0200 meaning or mandatory insertion rule is supplied.'),
          'supported', 'The parser resolves boundaries; SequenceMatcher alone did not. The cause and general requirement remain unknown.')
    probe('P2', 'The candidate value byte lies inside a four-byte ConstValue body of constant DCO UID 118.',
          ['docs/research/poc/LVheap-source.txt:693#OF__ConstValue',
           'docs/research/poc/LVheap-source.txt:750#SL__bDConstDCO',
           'docs/research/poc/inspect_vi.py:80-123#parse_heap'],
          dict(left_node_span=[540, 546], right_node_span=[544, 550],
               left_body_span=[542, 546], right_body_span=[546, 550],
               left_hex='00000001', right_hex='00000002', header_hex='866c',
               changed_offsets=[545, 549], parent_class=19, parent_uid=118,
               type_references=dict(dco='03', display='04'),
               note='Type references are heap IDs, not decoded I32 descriptors. Body length is in sizeSpec=4, not a separate length byte.'),
          'supported', 'Observed bodies agree with the author-reported I32 1-to-2 edit in these fixtures only.')
    probe('P3', 'The available source proves a general typed I32 ConstValue encoding/edit rule.',
          ['docs/research/poc/LVheap-source.txt:1951-1979#HeapNodeTDDataFill.findAndStoreTD',
           'docs/research/poc/LVheap-source.txt:2555-2561#NODE_TYPEID_TAGS_LIST',
           'docs/research/poc/LVheap-source.txt:2590-2594#NODE_DATAFILL_TAGS_LIST',
           'docs/research/poc/LVheap-source.txt:2796-2840#createObjectNode',
           'docs/research/poc/edit-readiness.md'],
          dict(typed_constvalue=False, heap_type_resolution='getHeapTD implementation not staged',
               generic_factory='ConstValue is not in typed datafill tags; generic HeapNode fallback',
               body_interpretation='big-endian 32-bit 1/2 is consistent with author claims, not independently resolved signed type',
               flags_insertion_requirement='unknown'),
          'unknown', 'No DTHP/VCTP resolver or typed ConstValue dispatch for this case is available; prior absence unchanged.')

    sys.path.insert(0, str(ENV / 'pylavi'))
    from pylavi.resource_types import TypeBDPW, TypeLVSR
    password_results = []
    for name, data in sorted(fixture_data.items()):
        record = TypeBDPW().from_bytes(data['BDPW'])
        password_results.append(dict(fixture=name, chunks=record.to_value(),
                                     has_password=record.has_password(),
                                     empty_ascii_password_matches=record.password_matches(''),
                                     lvsr_locked=TypeLVSR().from_bytes(data['LVSR']).locked()))
    probe('P5', 'The source-defined chunk-0 MD5 dependency predicts an empty password in all four constants.',
          ['@environment/pylavi/pylavi/resource_types.py:54-90#TypeBDPW',
           '@environment/pylavi/tests/test_resource_type_BDPW.py:7-23#test_basics'],
          dict(md5_empty_ascii=hashlib.md5(b'').hexdigest(), results=password_results,
               checks_only='chunk 0 / password classification; no integrity derivation for chunks 1/2'),
          'supported', 'All four records match empty ASCII MD5 and has_password=false. No passwords were changed or bypassed.')
    probe('P6', 'Prepared source supplies testable BDPW chunk-1/2 dependencies on RTSG/LVSR/BDHb.',
          ['@environment/pylavi/pylavi/resource_types.py:54-93#TypeBDPW',
           'docs/research/poc/step3/source-search.json#files',
           'docs/research/poc/heap-format-source.md#BDPW'],
          dict(recipe_available=False, tested_recipes=[],
               missing='No digest input order, version gates, salts or excluded ranges are specified.',
               opaque_resources=['BDPW[16:48]', 'RTSG', 'LVSR[52:68]', 'LVSR[80:96]', 'LVSR[120:136]']),
          'unknown', 'The only explicit hash recipe is chunk 0; unavailable recipes cannot be tested, and no guessed recipes were tried.')
    same_heap = []
    for value in (1, 2):
        normal = fixture_data[f'constant-{value}-normal.vi']
        separate = fixture_data[f'constant-{value}-separate.vi']
        same_heap.append(dict(value=value, raw_BDHb_equal=normal['BDHb'] == separate['BDHb'],
                              BDPW_equal=normal['BDPW'] == separate['BDPW'],
                              chunks_1_2_equal=normal['BDPW'][16:] == separate['BDPW'][16:],
                              RTSG_equal=normal['RTSG'] == separate['RTSG']))
    probe('P7', 'BDPW chunks 1/2 are a function of BDHb alone across these save modes.',
          ['docs/research/poc/pair/constant-1-normal--constant-1-separate.json#resources',
           'docs/research/poc/pair/constant-2-normal--constant-2-separate.json#resources'],
          dict(save_mode_controls=same_heap), 'refuted',
          'Identical BDHb inputs have different BDPW tails. This does not identify which other input caused the change.')
    summaries = {}
    for mode, comp in comparisons.items():
        selected = {}
        for r in comp['resources']:
            if r['type'] in ('BDHb', 'DFDS', 'VCTP', 'DTHP', 'VICD', 'CPC2', 'BDPW', 'RTSG', 'LVSR'):
                selected[r['type']] = dict(raw_different=r['raw']['different'],
                    left_length=r['raw']['left_length'], right_length=r['raw']['right_length'])
                if 'decompressed' in r:
                    de = r['decompressed']
                    selected[r['type']]['decompressed'] = {k: de[k] for k in
                        ('left_length', 'right_length', 'left_sha256', 'right_sha256', 'different')}
                    if r['type'] == 'DFDS':
                        selected[r['type']]['ranges'] = de['ranges']
        summaries[mode] = selected
    probe('P8', 'Both save modes reproduce BDHb changes; normal DFDS changes while type tables and normal VICD remain equal.',
          [relative(BASE / f'constant-1-{m}--constant-2-{m}.json') + '#resources' for m in comparisons],
          dict(resource_summary=summaries, cross_modes=same_heap,
               DFDS_separate_present=False, normal_DFDS_offset=223,
               equality_scope='Within each constant logic pair; VCTP/DTHP differ across save modes.'),
          'supported', 'These correlations repeat in both modes but do not give a general editing, cache retention or type-binding rule.')
    probe('P9', 'The pair/source evidence establishes a safe dependency update or cache invalidation rule.',
          ['docs/research/poc/pair/findings-0105.md#not-established',
           '@environment/pylavi/pylavi/resource_types.py:97-121#TypeLVSR',
           '@environment/pylavi/pylavi/resource_types.py:205-215#TypeLVSR.separate_code'],
          dict(lvsr_flags_word_offset=8, normal_flags_word='20000200', separate_flags_word='20000600',
               unknowns=['RTSG derivation/role', 'LVSR identifier-like regions', 'BDPW integrity tails',
                         'code/data/type rebuild dependency', 'effect of textRec flags'],
               unchanged_save_control_present=False, native_validation=False),
          'unknown', 'The source names the separate-code bit only; no rebuild/integrity rule or unchanged-save control is available.')

    repo_sources = []
    for item in read_json(ROOT / 'docs/research/poc/source-provenance.json'):
        if item['file'] not in ('LVheap-source.txt', 'LVmisc-source.txt', 'LVparts-source.txt', 'heap-format-source.md'):
            continue
        path = 'docs/research/poc/' + item['file']
        assert hashes[path] == item['sha256']
        symbols = {'LVheap-source.txt': 'HeapNode.parseRSRCData; createObjectNode; OBJ_TEXT_HAIR_TAGS; OF__ConstValue',
                   'LVmisc-source.txt': 'readVariableSizeFieldU124; readVariableSizeFieldS124; readVariableSizeFieldS24',
                   'LVparts-source.txt': 'PARTID; OBJ_FLAGS; DSINIT; DCO (prior unchanged search)',
                   'heap-format-source.md': 'BDHb/BDHc; BDPW'}
        repo_sources.append(dict(path=path, sha256=item['sha256'], revision=SNAP_REV,
                                 url=item['url'], symbol=symbols[item['file']]))
    repository_revision = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    evidence = dict(schema_version=1, verdict='source-blocked', input_hashes=hashes,
                    repository_revision=repository_revision,
                    repository_input_basis='Existing evidence at repository_revision; new probe script pinned as working-tree research output.',
                    source_pins=source_pins, repository_source_pins=repo_sources,
                    probes=probes,
                    unresolved=['Typed ConstValue and heap type resolution', 'textHair flags 0x0200 meaning/cause',
                                'BDPW chunk-1/2 derivation', 'RTSG and LVSR integrity roles',
                                'DFDS and code/type dependency handling', 'Unchanged Save As/re-save control'],
                    limitations=['No LabVIEW ran; no native validity, behavior, unbroken arrow, save-version preservation, 2024 or all-version evidence.',
                                 'Parser labels/boundaries are source-derived observations, not native semantics.',
                                 'No VI, reviewed tool, replay output or saved pin was changed; no cache removal, transplant or product code.',
                                 'Only the four owner constant fixtures were probed; authoring reports 2026 26.1.1f1 32-bit Windows 11.',
                                 'Source absence is limited to this pinned prepared inventory and saved snapshots.',
                                 'rules-supported would describe evidence support only, never native validity.'],
                    invocation='python3 -B docs/research/poc/pair/probe_constant_rules_0106.py',
                    offset_basis='Half-open decompressed BDHb offsets include the inner 4-byte length prefix.',
                    native_validity_established=False)
    for p, h in hashes.items():
        assert sha((ROOT / p).read_bytes()) == h, 'Input changed during probe: ' + p
    (BASE / 'constant-rules-0106.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps(dict(verdict=evidence['verdict'], input_files=len(hashes),
                          source_pins=len(source_pins), probes={p['id']: p['conclusion'] for p in probes},
                          original_inputs_unchanged=True)))


if __name__ == '__main__':
    main()
