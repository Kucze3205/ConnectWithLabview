"""Rebuild the saved partial verdict from committed small evidence only."""
import hashlib
import json
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]

def read(name):
    return json.loads((BASE / name).read_text())

def main():
    fixtures = read('step3/fixture-probe.json')
    constant = read('step3/constant-candidate.json')
    spans = [{'fixture': 'pylavi/tests/add.vi', 'start': p, 'end': p+1, 'hex': '67', 'field': 'OF__primIndex'} for p in (112, 171, 223, 258)]
    spans.append({'fixture': 'pylavi/tests/add.vi', 'start': 254, 'end': 256, 'hex': '041a', 'field': 'OF__primResID'})
    for observation in constant['observations']:
        e = observation['entry']
        if e['name'] in ('OF__ConstValue', 'OF__typeDesc'):
            spans.append({'fixture': constant['path'], 'start': e['data_offset'], 'end': e['end'], 'hex': e['content_hex'], 'field': e['name']})
    def requirement(status, finding, *evidence):
        return {'status': status, 'finding': finding, 'evidence': list(evidence)}
    result = {
        'schema_version': 1,
        'verdict': 'partial',
        'summary': 'Primitive and connected constant candidates located; no evidenced semantic replacement with integrity/cache rules. Do not order a disk edit.',
        'scope': {'fixture_limit': 12, 'edited_vi': False, 'behavior_claim': False, 'save_version_policy': 'Preserve each original declared save version; add.vi declares 21.0.0 final build 0. Constant candidate version not decoded; no cross-version claim.', 'runtime_checks': ['Owner opens without broken arrow', 'Owner observes intended changed behavior', 'Owner checks runtime validity and preserved save version']},
        'sources': ['source-provenance.json', 'step3/source-provenance.json', 'step3/source-search.json'],
        'fixtures': 'step3/fixture-probe.json',
        'requirements': {
            'semantics': requirement('unresolved', 'No independent primitive discriminator/replacement contract; no typed ConstValue interpretation.', 'LVheap-source.txt', 'step3/constant-candidate.json', 'step3/source-search.json'),
            'connectivity': requirement('unresolved', 'Stored endpoint pairs known, but direction, consumer semantics and compatible replacement terminal contract are unproved.', 'add.tree.txt', 'step3/constant-candidate.json'),
            'encoding': requirement('unresolved', 'ConstValue bodies and heap-type references observed; DTHP/VCTP indirection and actual constant encoding unresolved. Numeric range-field decoder is not a ConstValue decoder.', 'LVheap-source.txt', 'step3/constant-candidate.json'),
            'container_rebuild': requirement('resolved', 'Necessary framing checklist: fresh zlib checksum, length prefixes, resource size/padding, downstream offsets, both RSRC headers and affected map offsets. This alone is insufficient for an edit.', 'README.md', 'candidate-change.json'),
            'integrity': requirement('unresolved', 'BDPW first MD5-sized chunk interpreted as password; remaining two add.vi chunks have no inspected derivation/update rule. No absence-of-integrity inference.', 'step3/pylavi-resource-types-source.txt', 'step3/fixture-probe.json', 'step3/source-search.json'),
            'compiled_cache': requirement('unresolved', 'VICD/CPC2 observed; no safe invalidation, regeneration or dependent-flag rule in inspected sources.', 'step3/source-search.json', 'step3/fixture-probe.json'),
            'save_version': requirement('unresolved', 'Preservation is mandatory; constant candidate declared version not decoded and no version-specific edit rule established.', 'README.md', 'edit-readiness.md'),
            'owner_runtime': requirement('owner_check', 'Future edited artifact must pass owner opening, behavior and runtime/save-version checks in an appropriate LabVIEW environment.', 'edit-readiness.md'),
        },
        'blockers': [
            'Independent primitive identity and compatible terminal/resource-family replacement contract absent.',
            'Constant heap-type resolution and ConstValue value/encoding contract absent.',
            'BDPW non-password chunk derivation/update rules absent from inspected sources.',
            'Compiled-code/cache invalidation and dependent flag rules absent.',
            'Candidate-specific save-version preservation not demonstrated; no runtime check possible here.',
        ],
        'exits': [
            'Obtain pinned owner-authored same-version I32 1/2 or independently identified Add/Subtract pairs, including normal/separate-code variants; compare type/value spans, all BDPW chunks, flags and code resources. Controlled differences locate candidate dependencies but still need validated rules.',
            'Pin missing BDPW, code-cache and DTHP/VCTP/ConstValue implementations with revision/license/hash; otherwise deliver a bounded documented step-3 POC failure and retain the inspector.',
        ],
        'recipe': None,
        'spans': spans,
        'evidence': [],
    }
    names = ['README.md', 'edit-readiness.md', 'inspect_vi.py', 'heap-labels.json', 'source-provenance.json', 'LVheap-source.txt', 'LVmisc-source.txt', 'LVparts-source.txt', 'heap-format-source.md', 'pylabview-LICENSE.txt', 'candidate-change.json', 'add.tree.txt', 'verify_edit_readiness.py']
    names += [str(p.relative_to(BASE)) for p in (BASE / 'step3').iterdir() if p.is_file() and p.suffix in ('.py', '.json', '.md', '.txt')]
    for name in sorted(set(names)):
        raw = (BASE / name).read_bytes()
        result['evidence'].append({'path': name, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
    (BASE / 'edit-readiness.json').write_text(json.dumps(result, indent=2) + '\n')
    print('saved partial verdict;', len(fixtures['fixtures']), 'fixtures;', len(spans), 'original spans;', len(result['evidence']), 'evidence files')

if __name__ == '__main__':
    main()
