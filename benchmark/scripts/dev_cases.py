#!/usr/bin/env python3
"""Freeze public development inventories from preserved originals, stdlib only.
Run with python3 -I. Never imports or executes prepared source code.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'benchmark/cases/dev'
PINS = {
    'actor-framework': '371c631c16155d88f02be11a953e4964d7452fd8',
    'pylavi': '35d2a0318f71dcb87bb9c431dc00700ee6b9fb75',
}
# One conservative project lineage deliberately groups copies, archives and variants.
# It is a split constraint, not a claim that these public inputs can be withheld.
LINEAGE = 'public-ni-actor-framework-all-projects-copies-variants'
CASES = [
    ('project-ppl', 'Core/AF PPL Build.lvproj', None),
    ('project-debug-ppl', 'Core/AF Debug PPL Build.lvproj', None),
    ('project-archive-ppl', 'PPL Test/AF PPL.lvproj', 'Documentation/Test Plan/PPL Test.zip'),
    ('class-actor', 'Core/ActorFramework/Actor/Actor.lvclass', None),
    ('class-stop-msg', 'Core/ActorFramework/Stop Msg/Stop Msg.lvclass', None),
    ('class-archive-another-actor', 'Rescripter Test Harness/Another Actor/Another Actor/Another Actor.lvclass', 'Documentation/Test Plan/Test Harness Master.zip'),
    ('library-framework', 'Core/ActorFramework/Actor Framework.lvlib', None),
    ('library-debug', 'Core/AFDebug/AF Debug.lvlib', None),
    ('library-specialty', 'Core/ActorFramework/AF Specialty Messages.lvlib', None),
    ('library-icon-tests', 'Tooling/Unit tests/Text-Based VI Icon/Text-Based VI Icon Unit Tests.lvlib', None),
    ('vi-actor-core-native-gap', 'Core/ActorFramework/Actor/Actor Core.vi', None),
]
PROPERTY_NAMES = {
    'NI.Lib.ContainingLib', 'NI.Lib.ContainingLibPath', 'NI.LibItem.Scope',
    'NI.ClassItem.MethodScope', 'NI.ClassItem.MustCallParent',
    'NI.ClassItem.DynamicDispatch', 'NI.ClassItem.IsDynamicDispatch',
    'NI.PreserveRelativePath', 'CCSymbols', 'NI.LV.All.SourceOnly',
}
BUILD_PREFIXES = ('Bld_', 'Source[', 'Destination[', 'SourceCount', 'DestinationCount', 'PackedLib_', 'TgtF_')
OPAQUE_NAMES = {'NI.LVClass.Geneology', 'NI.LVClass.ParentClassLinkInfo'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')


def read_regular(base, relative):
    rel = Path(relative)
    require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe path: ' + relative)
    current = base
    require(not current.is_symlink(), 'Symlink root: ' + str(base))
    for part in rel.parts:
        current = current / part
        require(not current.is_symlink(), 'Symlink: ' + str(current))
    require(current.is_file(), 'Missing original: ' + str(current))
    return current.read_bytes()


def git_head(directory):
    result = subprocess.run([
        'git', '--no-replace-objects', '--no-optional-locks',
        '-c', 'safe.directory=' + str(directory), '-c', 'core.fsmonitor=false',
        '-C', str(directory), 'rev-parse', 'HEAD'], capture_output=True, check=False)
    require(result.returncode == 0, 'Cannot inspect prepared Git HEAD')
    return result.stdout.decode('ascii').strip()


def load_original(environment, sources, coverage, path, archive):
    repo = next(r for r in sources['repositories'] if r['name'] == 'actor-framework')
    container = archive or path
    source = next((a for a in repo['artifacts'] if a['path'] == container), None)
    if source is None and archive:
        containers = [a for a in coverage['artifacts']
                      if a['archive'] is None and a['path'] == repo['name'] + '/' + container]
        require(len(containers) == 1, 'Missing or ambiguous archive container: ' + container)
        source = containers[0]
    require(source is not None, 'Missing original identity: ' + container)
    raw = read_regular(environment / repo['name'], container)
    require(sha(raw) == source['sha256'], 'Original drift: ' + container)
    chain = []
    if archive:
        matched = [a for a in coverage['artifacts'] if a['archive'] == repo['name'] + '/' + archive and a['path'] == path]
        require(len(matched) == 1, 'Ambiguous coverage member: ' + path)
        record = matched[0]
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            members = z.infolist()
            index = record['member_index']
            require(0 <= index < len(members), 'Invalid archive index')
            member = members[index]
            require(member.filename == path and member.file_size == record['size'], 'Archive member identity drift')
            require(member.file_size < 2_000_000, 'Member exceeds preparation bound')
            raw = z.read(member)
        require(sha(raw) == record['sha256'], 'Archive member hash drift')
        chain = [{'container_path': archive, 'container_sha256': source['sha256'],
                  'member_path': path, 'member_index': index, 'member_sha256': record['sha256']}]
        versions = record['save_versions']
        save_version = {'status': 'recorded' if versions else 'unavailable', 'fields': versions}
        manifest = 'benchmark/coverage.json'
    else:
        record = source
        save_version = source['save_version']
        manifest = 'benchmark/sources.json'
    identity = {'repository': repo['name'], 'repository_url': repo['upstream_url'],
                'commit': repo['commit'], 'path': path, 'archive_member_chain': chain,
                'sha256': record['sha256'], 'identity_manifest': manifest,
                'identity_manifest_sha256': sha((ROOT / manifest).read_bytes())}
    return raw, identity, save_version


def walk_xml(element, locator=None, ancestors=()):
    locator = locator or '/' + element.tag
    yield element, locator, ancestors
    counts = {}
    for child in element:
        counts[child.tag] = counts.get(child.tag, 0) + 1
        yield from walk_xml(child, locator + '/' + child.tag + '[' + str(counts[child.tag]) + ']', ancestors + (element,))


def xml_facts(raw, family):
    require(b'<!DOCTYPE' not in raw.upper() and b'<!ENTITY' not in raw.upper(), 'DTD/entity input forbidden')
    root = ET.fromstring(raw)
    facts = []

    def add(locator, value, kind):
        facts.append({'locator': locator, 'value': value, 'kind': kind})

    add('/' + root.tag + '/@LVVersion', root.attrib['LVVersion'], 'original-save-version-declaration')
    for element, locator, ancestors in walk_xml(root):
        if element.tag == 'Item':
            types = [x.get('Type') for x in ancestors]
            kind = 'declared-item'
            if 'Dependencies' in types or element.get('Type') == 'Dependencies':
                kind = 'declared-dependency-item'
            elif 'Build' in types or element.get('Type') == 'Build':
                kind = 'declared-build-item'
            elif 'Friends List' in types or element.get('Type') == 'Friends List':
                kind = 'declared-friend-item'
            for attribute in sorted(element.attrib):
                add(locator + '/@' + attribute, element.attrib[attribute], kind)
        elif element.tag == 'Property':
            name = element.get('Name', '')
            if name in PROPERTY_NAMES or (family == '.lvproj' and name.startswith(BUILD_PREFIXES)):
                # Preserve literal XML strings and type tags; do not interpret scope enums.
                add(locator + '/@Name', name, 'property-name')
                add(locator + '/@Type', element.get('Type'), 'property-type')
                add(locator + '/text()', element.text or '', 'literal-property-value')
            elif name in OPAQUE_NAMES:
                add(locator + '/@Name', name, 'opaque-lineage-property-name')
                add(locator + '/@Type', element.get('Type'), 'opaque-lineage-property-type')
                # Geneology uses a nested String/Val; hashing preserves its literal payload
                # without claiming to decode or establish the actual parent class.
                if len(element):
                    for child, child_path, _ in walk_xml(element, locator):
                        if child.tag == 'Val':
                            add(child_path + '/text()/utf8-sha256', sha((child.text or '').encode('utf-8')), 'opaque-lineage-payload-fingerprint')
                else:
                    add(locator + '/text()/utf8-sha256', sha((element.text or '').encode('utf-8')), 'opaque-lineage-payload-fingerprint')
    require(facts, 'Empty XML reference inventory')
    return root, facts


def make_case(case_id, raw, identity, save_version):
    family = Path(identity['path']).suffix.lower()
    is_vi = family == '.vi'
    questions = {
        '.lvproj': 'Inventory every declared Item attribute and the selected build/source/destination properties. Separate declared dependencies, project items and build specifications from native resolution, inclusion effects and successful builds.',
        '.lvclass': 'Inventory every declared Item attribute, containing-library and literal scope/method properties, and fingerprint encoded genealogy/parent-link fields. Identify the native evidence still needed to establish inheritance, effective scope and dispatch.',
        '.lvlib': 'Inventory every declared Item attribute, containing-library and literal scope properties. Distinguish friends, folders and members; identify native evidence needed for effective scope and resolved membership.',
        '.vi': 'Explain Actor Core computation, connector/types, diagram dataflow and execution dependencies under a declared input/state/target fixture. Identify native evidence missing before any semantic answer can be established.',
    }
    conditions = ['Preserved original bytes at the pinned commit and SHA256; no conversion.',
                  'Public development evidence; no native LabVIEW inspection or execution in this preparation.',
                  'XML values mean literal declarations only; no URL resolution, enum interpretation or runtime compatibility inference.']
    if is_vi:
        conditions[-1] = 'Controlled input/state/target fixture is not yet established; semantic expectations remain null.'
    claims = []
    observations = []
    if not is_vi:
        root, facts = xml_facts(raw, family)
        version_fields = save_version.get('fields', [save_version])
        require(any(v.get('raw_hex') == root.get('LVVersion').lower() for v in version_fields), 'Save version differs from manifest')
        for number, fact in enumerate(facts, 1):
            claim_id = 'A' + str(number).zfill(4)
            observation_id = 'R' + str(number).zfill(4)
            citation = {k: identity[k] for k in ('repository', 'commit', 'path', 'sha256', 'archive_member_chain')}
            citation['locator'] = {'scheme': 'xml-positional-path', 'expression': fact['locator']}
            claims.append({'claim_id': claim_id, 'atomic_fact': {'relation': 'literal-value-at-location', 'kind': fact['kind'], 'value': fact['value']},
                           'conditions': conditions, 'reference_status': 'provisional-xml-derived-unverified-independent-check',
                           'xml_evidence': 'available', 'native_reference': 'unavailable', 'citations': [citation],
                           'acceptable_alternatives': ['Equivalent wording preserving the exact literal value, original locator and conditions.'],
                           'comparison': 'Exact Unicode XML-parsed string equality; payload hashes are lowercase SHA256 of XML-parsed text encoded UTF-8.',
                           'numerical_tolerance': None})
            observations.append({'observation_id': observation_id, 'aligned_claim_id': claim_id,
                                 'scope': fact['locator'], 'expected': fact['value'],
                                 'native_reference_status': 'unverified-native-required',
                                 'xml_reference_status': 'provisional-author-extraction',
                                 'alignment_rule': 'Map the preserved raw output location to this exact locator and value; no reconstruction of absent content.'})
    native_topics = {
        '.lvproj': ['resolved-dependencies', 'effective-build-inclusion-and-build-result'],
        '.lvclass': ['resolved-direct-parent-and-inheritance', 'effective-scope-and-dispatch'],
        '.lvlib': ['resolved-membership', 'effective-scope'],
        '.vi': ['connector-terminals-and-types', 'diagram-nodes-wires-and-execution-dependencies', 'controlled-input-output-behavior'],
    }[family]
    for number, topic in enumerate(native_topics, 1):
        cid, rid = 'N' + str(number).zfill(4), 'RN' + str(number).zfill(4)
        claims.append({'claim_id': cid, 'atomic_fact': {'relation': topic, 'value': None},
                       'conditions': conditions, 'reference_status': 'unverified-native-required',
                       'native_reference': 'unavailable', 'citations': [],
                       'required_reference': {'original_sha256': identity['sha256'], 'original_path': identity['path'],
                                              'archive_member_chain': identity['archive_member_chain'],
                                              'native_locator': None, 'required_view': topic},
                       'acceptable_alternatives': [], 'numerical_tolerance': None,
                       'uncertainty': 'Native property/diagram/capture or controlled experiment and independent check not available. A limitation declaration earns no correct credit for this slot.'})
        observations.append({'observation_id': rid, 'aligned_claim_id': cid, 'scope': topic,
                             'expected': None, 'native_reference_status': 'unverified-native-required',
                             'alignment_rule': 'Unverified until a separately reviewed revision supplies native original-object locators and expected values; retain this slot.'})
    answer_ids = [c['claim_id'] for c in claims]
    reader_ids = [o['observation_id'] for o in observations]
    return {
        'schema_version': 1, 'case_id': case_id, 'case_revision': 1, 'inventory_revision': 1,
        'visibility': 'public-development-cannot-be-withheld', 'lineage_group_id': LINEAGE,
        'lineage_rule': 'Keep all NI Actor Framework projects, archive copies and variants together in any later split; public history remains exposed.',
        'question': questions[family], 'artifact': identity, 'family': family, 'save_version': save_version,
        'expected_observable': 'Literal XML declaration inventory and explicit native gaps.' if not is_vi else 'Native diagram, properties and controlled I/O; currently unavailable.',
        'conditions': conditions,
        'dependencies_and_environment': {'preparation': 'Python standard library, local Git HEAD, prepared read-only sources via LABVIEW_ENVIRONMENT; no prepared code executed.',
                                         'native_labview': 'unavailable-for-this-case; not executed', 'native_version_build_os': None,
                                         'modules_licenses_targets': 'unverified', 'dependency_resolution': 'unverified-native-required'},
        'oracle': {'status': 'unavailable' if is_vi else 'provisional-xml-only-native-unavailable',
                   'method': 'Direct stdlib ElementTree inspection of hash-verified original XML; no evaluated reader used.' if not is_vi else 'No semantic extraction attempted from binary VI.',
                   'native_status': 'unavailable', 'independent_checker': {'status': 'pending', 'identity': None, 'session': None, 'claim_agreements': []},
                   'required_followup': 'Resolve every ID against original evidence in a separate reviewer session; native claims require bounded native inspection/experiment and hashed captures/object maps. Disagreement blocks key establishment.'},
        'required_answer_claim_ids': answer_ids, 'reference_inventory': claims,
        'required_reader_observation_ids': reader_ids, 'reader_reference_inventory': observations,
        'reader_probe_contract': {'probe_id': case_id + '-probe-1', 'status': 'specification-only-not-executed',
                                  'entry_point': 'abstract reader inspect-original operation; concrete adapter unavailable and must be frozen before exposure',
                                  'arguments': {'artifact': identity, 'scope': 'all-required-observation-ids-in-order', 'observation_ids': reader_ids},
                                  'ordering': reader_ids, 'adaptive_branches': [], 'limit': 'No truncation permitted; every required ID remains in denominator.',
                                  'unprobed_scope': 'All content outside listed locators, binary private data, diagrams, runtime semantics and native resolution.',
                                  'execution_evidence_required': ['exact request', 'reader/configuration revision', 'environment', 'timestamps', 'raw response bytes/files and SHA256', 'exit/error and truncation records', 'independent alignment ledger retaining extras, omissions, duplicates and contradictions']},
        'denominators': {'answer_correctness': {'count': len(answer_ids), 'required_ids': answer_ids},
                         'source_grounding': {'count': len(answer_ids), 'required_ids': answer_ids},
                         'reading_fidelity': {'count': len(reader_ids), 'required_ids': reader_ids},
                         'unavailable_items_retained': True, 'submitted_extras_change_denominator': False},
        'answer_record_contract': {'case_id': case_id, 'status': 'required',
                                   'claims': [{'claim_id': '<required ID>', 'answer': '<atomic assertion>', 'conditions': [], 'citations': ['original hash/path/member chain and exact original locator']}],
                                   'limitations': 'Map every limitation to affected IDs; preserve all factual assertions.'},
        'adjudication': {'protocol': 'benchmark/protocol.md#tasks',
                         'mapping': 'Freeze these IDs before exposure; split compound assertions into atomic statements. Preserve submitted text and mappings; equivalent duplicates count once, contradictions make affected items incorrect.',
                         'extras': 'Retain separate ledger for every unmatched factual assertion, including prose/limitations. Independently check true/false/unverified extras; extras never replace omissions.',
                         'assessment': 'Apply protocol F1/F2 precedence independently per dimension; pending/unavailable references are unverified and cannot earn correct credit.',
                         'outcome_categories': ['correct', 'partial', 'incorrect', 'missing', 'unsupported', 'unverified', 'error'],
                         'reporting': 'Report every outcome count over each fixed denominator, separate extra outcomes/contradictions/duplicates and planned/attempted/executed/scored counts. No combined score or quality threshold.'},
        'acceptable_alternatives': ['Equivalent presentation with atomic IDs, exact literal values and resolvable original citations; no substitutions for missing required items.'],
        'disallowed_inferences': ['Declared URL implies resolved file or successful load.', 'Build settings imply successful build or effective inclusion.',
                                  'Numeric scope code implies public/private/protected semantics without independently pinned interpretation.',
                                  'Genealogy fingerprint or missing ParentClassLinkInfo identifies a direct parent or proves no inheritance.',
                                  'XML names, descriptions, membership or method flags establish VI behavior, diagram content or dispatch execution.',
                                  'Save-version declaration proves compatibility with a reading environment.',
                                  'Public development cases or their copies can become withheld/unseen.', 'Unavailable references or honest limitations earn full-read/correct credit.'],
        'uncertainties': ['All native references unavailable; inheritance payloads remain encoded.', 'XML expectations await independent original-source checking.',
                          'Concrete reader adapter and native object/capture maps unavailable; no reader runs or scoring performed.',
                          'No native version, module, license, hardware or dependency-resolution coverage established.'],
        'execution': {'planned': True, 'attempted': False, 'executed': False, 'scored': False},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare byte-identically; never write')
    args = parser.parse_args()
    sources_bytes = (ROOT / 'benchmark/sources.json').read_bytes()
    coverage_bytes = (ROOT / 'benchmark/coverage.json').read_bytes()
    sources, coverage = json.loads(sources_bytes), json.loads(coverage_bytes)
    require(coverage['sources_json_sha256'] == sha(sources_bytes), 'Coverage/source pin mismatch')
    for relative, digest in [('benchmark/sources.json', sha(sources_bytes)), ('benchmark/coverage.json', sha(coverage_bytes))]:
        preparation = json.loads((ROOT / 'benchmark/preparation.json').read_bytes())
        pinned = [p['sha256'] for entries in preparation['milestones'].values() for p in entries if p['path'] == relative]
        require(pinned and all(p == digest for p in pinned), 'Evidence pin mismatch: ' + relative)
    environment_value = os.environ.get('LABVIEW_ENVIRONMENT')
    require(environment_value, 'LABVIEW_ENVIRONMENT must name the prepared read-only cache')
    environment = Path(environment_value)
    for name, commit in PINS.items():
        repo = next(r for r in sources['repositories'] if r['name'] == name)
        require(repo['commit'] == commit and git_head(environment / name) == commit, 'Prepared commit drift: ' + name)
    generated = {}
    for case_id, path, archive in CASES:
        raw, identity, version = load_original(environment, sources, coverage, path, archive)
        generated[case_id + '.json'] = encode(make_case(case_id, raw, identity, version))
    require(all(len(data) < 2_000_000 for data in generated.values()), 'Evidence file exceeds 2 MB')
    existing = set(p.name for p in OUT.glob('*.json'))
    require(not (existing - set(generated)), 'Unexpected existing development JSON; investigate rather than delete')
    # Preflight every existing output before writing any missing outputs.
    for name, data in generated.items():
        target = OUT / name
        require(not target.is_symlink(), 'Symlink output forbidden')
        if target.exists():
            require(target.read_bytes() == data, 'Development inventory drift: ' + name)
        else:
            require(not args.check, 'Missing development case: ' + name)
    if not args.check:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, data in generated.items():
            target = OUT / name
            if not target.exists():
                target.write_bytes(data)
    print(json.dumps({'mode': 'check' if args.check else 'generate', 'cases': len(generated),
                      'families': {'.lvproj': 3, '.lvclass': 3, '.lvlib': 4, '.vi': 1},
                      'native_references': 'unavailable for every case', 'all_public': True,
                      'maximum_case_bytes': max(map(len, generated.values()))}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, StopIteration, ET.ParseError, zipfile.BadZipFile) as error:
        print('dev_cases: ' + str(error), file=sys.stderr)
        sys.exit(1)
