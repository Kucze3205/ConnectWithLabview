#!/usr/bin/env python3
"""Regenerate the prepared public-source coverage record, offline and without LabVIEW.

Run with python3 -I. Original files and archive members are never modified or
extracted. This inventories metadata; it does not measure semantic reading.
"""
import argparse
from collections import Counter, defaultdict
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('coverage_sources', ROOT / 'benchmark/scripts/sources.py')
sources = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sources)
EXTENSIONS = sources.EXTENSIONS | {'.rtm', '.lvsc'}
ARCHIVES = {'.zip', '.vip', '.vipc', '.vsix', '.lvlibp'}
OUTPUTS = ('benchmark/coverage.json', 'benchmark/coverage.md')


def resources(data):
    """Bounded RSRC format-3 resource table, independent of pylavi decoding."""
    sources.require(len(data) >= 32, 'Truncated RSRC header')
    magic, check, fmt, kind, creator, meta, meta_size, start, size = struct.unpack_from('>4s2sH4s4sIIII', data)
    sources.require(magic == b'RSRC' and check == b'\r\n', 'Invalid RSRC marker')
    sources.require(fmt == 3, 'Unsupported RSRC format ' + str(fmt))
    sources.require(start == 32 and start + size == meta and meta_size >= 68 and meta + meta_size <= len(data), 'Invalid RSRC bounds')
    sources.require(data[meta:meta + 32] == data[:32], 'Secondary RSRC header differs')
    base = meta + 52
    count = struct.unpack_from('>I', data, base)[0] + 1
    sources.require(count <= (meta_size - 56) // 12, 'Invalid RSRC type count')
    result = []
    for index in range(count):
        code, last, offset = struct.unpack_from('>4sII', data, base + 4 + index * 12)
        table, entries = base + offset, last + 1
        sources.require(table >= base + 4 + count * 12 and table + entries * 20 <= meta + meta_size, 'Invalid resource table')
        for entry in range(entries):
            rid, name, unused, offset, unused2 = struct.unpack_from('>IIIII', data, table + entry * 20)
            location = start + offset
            sources.require(start <= location and location + 4 <= meta, 'Invalid resource offset')
            length = struct.unpack_from('>I', data, location)[0]
            sources.require(location + 4 + length <= meta, 'Truncated resource body')
            result.append((code.decode('latin-1'), rid, location + 4, data[location + 4:location + 4 + length]))
    return kind.decode('latin-1'), result


def artifact(path, data, archive=None, index=None):
    ext = Path(path).suffix.lower()
    record = {'path': path, 'archive': archive, 'member_index': index,
              'size': len(data), 'sha256': sources.sha256(data),
              'magic': data[:8].hex(), 'extension': ext,
              'save_versions': [], 'gaps': [], 'native_labview': 'not executed'}
    container = 'text/other'
    if data.startswith(b'RSRC'):
        container = 'RSRC'
        try:
            kind, entries = resources(data)
            container += ' ' + kind
            record['resource_types'] = dict(sorted(Counter(code for code, _, _, _ in entries).items()))
            for code, rid, offset, body in entries:
                if code in ('vers', 'LVSR') and len(body) >= 4:
                    record['save_versions'].append({'field': code, 'resource_id': rid,
                                                   'byte_offset': offset, **sources.version(body[:4].hex())})
            values = {v['raw_hex'] for v in record['save_versions']}
            if len(values) > 1:
                record['gaps'].append('Version fields disagree; authoritative native save-version semantics unverified')
            record['gaps'].append('Resource table access does not establish diagram, panel or type semantics')
        except (ValueError, struct.error) as error:
            record['gaps'].append('Unreadable/unsupported RSRC: ' + str(error))
    elif zipfile.is_zipfile(io.BytesIO(data)):
        container = 'zip'
        record['gaps'].append('Package installation and dependency resolution not executed')
    elif data.lstrip(b'\xef\xbb\xbf \r\n\t').startswith(b'<'):
        container = 'XML'
        try:
            element = ET.fromstring(data)
            raw = element.attrib.get('LVVersion')
            if raw is not None:
                if len(raw) != 8 or any(c not in '0123456789abcdefABCDEF' for c in raw):
                    raise ValueError('Invalid XML LVVersion')
                record['save_versions'].append({'field': 'XML root @LVVersion', **sources.version(raw)})
            record['gaps'].append('XML syntax and declarations do not establish native project/dependency behavior')
        except (ET.ParseError, ValueError) as error:
            record['gaps'].append('Unreadable XML: ' + str(error))
    else:
        record['gaps'].append('Opaque or unsupported container; contents not semantically read')
    if not record['save_versions']:
        record['gaps'].append('Save version unavailable; retained in denominator')
    if any(v['decoded'] is None for v in record['save_versions']):
        record['gaps'].append('Unrecognized packed version encoding; raw field retained')
    record['family'] = ext + ' ' + container + (' (zip member)' if archive else '')
    return record


def inventory(environment):
    provenance = sources.inventory(environment)
    sources.require(sources.OUTPUT.read_bytes() == sources.encoded(provenance), 'sources.json differs; investigate provenance drift first')
    records, archive_gaps = [], []
    for repo in provenance['repositories']:
        directory = environment / repo['name']
        tree = sources.git(directory, 'ls-tree', '-rz', '--full-tree', repo['commit'])
        for item in tree.split(b'\0'):
            if not item:
                continue
            relative = item.split(b'\t', 1)[1].decode('utf-8')
            data = sources.regular_file(directory, relative)
            path = repo['name'] + '/' + relative
            ext = Path(relative).suffix.lower()
            if ext in EXTENSIONS or data.startswith(b'RSRC') or ext in ARCHIVES:
                records.append(artifact(path, data))
            if ext in ARCHIVES and zipfile.is_zipfile(io.BytesIO(data)):
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    for index, member in enumerate(archive.infolist()):
                        if member.is_dir():
                            continue
                        try:
                            body = archive.read(member)
                            if Path(member.filename).suffix.lower() in EXTENSIONS or body.startswith(b'RSRC'):
                                records.append(artifact(member.filename, body, path, index))
                        except (OSError, RuntimeError, ValueError, zipfile.BadZipFile, NotImplementedError) as error:
                            archive_gaps.append({'archive': path, 'member': member.filename,
                                                 'member_index': index, 'status': 'unreadable', 'reason': str(error)})
    records.sort(key=lambda r: (r['archive'] or r['path'], r['archive'] is not None, r['path'], r['member_index'] or 0))
    families = defaultdict(lambda: {'count': 0, 'version_fields': Counter(), 'without_version': 0})
    for record in records:
        family = families[record['family']]
        family['count'] += 1
        family['without_version'] += not record['save_versions']
        for version in record['save_versions']:
            family['version_fields'][version['field'] + ': ' + version['raw_hex']] += 1
    return {'schema_version': 1, 'scope': 'Pinned public development sources only; full goal unchanged',
            'sources_json_sha256': sources.sha256(sources.encoded(provenance)),
            'selection': {'extensions': sorted(EXTENSIONS), 'archive_extensions': sorted(ARCHIVES),
                          'tracked_only': True, 'originals_modified': False, 'members_extracted': False},
            'reading_environment': {'implementation': 'Python standard library, read-only git, bounded metadata parser',
                                    'native_labview': 'not executed', 'semantic_reading': 'not measured'},
            'version_policy': 'Retain every vers, LVSR and XML field; disagreements and unknown encodings are gaps, no authoritative-field assumption',
            'fallback_2024_selected': False,
            'families': dict(sorted(families.items())), 'artifacts': records,
            'archive_gaps': archive_gaps,
            'gaps': ['Every native LabVIEW reading environment and cross-version compatibility remains unexamined in this inventory',
                     'All goal families and versions absent from these public sources remain uncovered, not excluded',
                     'Modules, targets, licenses and dependencies require native and independent evidence',
                     'Protected or removed diagrams, behavior and semantic fidelity cannot be established from headers']}


def enrich(result, environment):
    """Declarations are observations, never proof of installed modules or access."""
    import ast
    decoder_source = sources.regular_file(environment / 'pylavi', 'pylavi/resource_types.py')
    decoder_names = sorted(node.name for node in ast.parse(decoder_source).body
                           if isinstance(node, ast.ClassDef) and node.name.startswith('Type'))
    result['pylavi_decoder_scope'] = {
        'method': 'Static class-name inventory of the pinned resource_types.py; no prepared Python executed',
        'source_sha256': sources.sha256(decoder_source), 'classes': decoder_names,
        'decoding_executed': False,
        'limitation': 'Class presence does not establish decoding correctness or semantic support'}
    declarations = []
    for record in result['artifacts']:
        if 'resource_types' in record:
            record['resources_without_pylavi_decoder'] = sorted(
                code for code in record['resource_types'] if 'Type' + code.strip() not in decoder_names)
            if record['resources_without_pylavi_decoder']:
                record['gaps'].append('Opaque to pinned pylavi decoder inventory: ' + ', '.join(record['resources_without_pylavi_decoder']))
        if record['extension'] not in ('.lvproj', '.vipb', '.lvlib', '.lvclass', '.viancfg'):
            continue
        if record['archive']:
            archive_path = environment / record['archive']
            with zipfile.ZipFile(archive_path) as archive:
                data = archive.read(archive.infolist()[record['member_index']])
        else:
            data = sources.regular_file(environment, record['path'])
        if not data.lstrip(b'\xef\xbb\xbf \r\n\t').startswith(b'<'):
            continue
        try:
            root = ET.fromstring(data)
        except ET.ParseError:
            continue
        location = {'path': record['path'], 'archive': record['archive'],
                    'member_index': record['member_index'], 'sha256': record['sha256']}
        items = list(root.iter('Item'))
        dependencies = [dict(item.attrib) for group in items if group.get('Type') == 'Dependencies'
                        for item in group.iter('Item') if item is not group]
        declaration = dict(location, root_tag=root.tag, root_attributes=dict(root.attrib),
                           item_types=dict(sorted(Counter(item.get('Type', '') for item in items).items())),
                           targets=[dict(item.attrib) for item in items
                                    if item.get('Type') in ('My Computer', 'Target') or 'Target' in item.get('Type', '')],
                           build_specifications=[dict(child.attrib) for item in items if item.get('Type') == 'Build'
                                                 for child in item.findall('Item')],
                           dependencies=dependencies,
                           package_labview_versions=[element.text for element in root.iter('Package_LabVIEW_Version')],
                           status='Declared only; dependencies, module installation, target access and builds not executed')
        declarations.append(declaration)
    result['project_and_package_declarations'] = declarations
    observed_extensions = {record['extension'] for record in result['artifacts']}
    result['missing_extensions'] = sorted(EXTENSIONS - observed_extensions)
    raw_versions = sorted({version['raw_hex'] for record in result['artifacts'] for version in record['save_versions']})
    majors = sorted({int(raw[:2]) for raw in raw_versions if all(c in '0123456789' for c in raw[:2])})
    result['save_version_inventory'] = {
        'raw_fields_found': raw_versions,
        'decoded_fields_found': sorted({version['decoded'] for record in result['artifacts']
                                        for version in record['save_versions'] if version['decoded'] is not None}),
        'major_numbers_observed': majors,
        'unobserved_major_numbers_1_through_26': [major for major in range(1, 27) if major not in majors],
        'native_versions_examined_by_this_run': [],
        'gap': 'Every LabVIEW release is unexamined natively here, including versions with header evidence. The 1..26 list is navigation, not a closed denominator; intermediate releases, patches, platforms and future versions remain in scope.'}
    result['module_and_target_conditions'] = {
        'declaration_evidence': 'project_and_package_declarations; source attributes preserved without inferring installed capabilities',
        'module_installation': 'not examined', 'hardware_access': 'not examined',
        'variants_requiring_evidence': [
            {'variant': name, 'status': 'unexamined; retained coverage gap'}
            for name in ('Desktop development systems and operating systems', 'Real-Time', 'FPGA',
                         'DSC', 'Vision and other add-on modules/toolkits', 'Hardware and remote targets')],
        'open_scope': True}
    result['access_conditions'] = {
        'public_sources': [{'name': name, 'commit': pin[1], 'license': pin[2]}
                           for name, pin in sorted(sources.PINS.items())],
        'originals': 'Read-only pinned tracked bytes; archive members read in memory, never installed or extracted',
        'network': 'No network operations; prepared environment required',
        'native_labview': 'not executed',
        'native_licensing': 'Not checked by this run; source licenses do not grant runtime/module licenses',
        'dependencies': 'XML declarations inventoried; resolution, installation and transitive dependencies not executed',
        'diagrams': 'Password protection, removed diagrams and accessibility not established from resource presence',
        'historical_runtime': {
            'evidence': 'docs/perpetua/environment.md#hosted-result-18-october-2026',
            'observation': 'Separate hosted NI 2026 Q1 mass-compile of a 2014 fixture; not this corpus or a coverage test',
            'native_2024': 'unverified', 'all_version_compatibility': 'unverified'}}
    result['denominator'] = {
        'artifact_entries': len(result['artifacts']),
        'disk_entries': sum(record['archive'] is None for record in result['artifacts']),
        'archive_member_entries': sum(record['archive'] is not None for record in result['artifacts']),
        'unreadable_archive_members': len(result['archive_gaps']),
        'policy': 'Copies and variants remain separate entries; no unsupported, opaque or versionless entry is removed. Unreadable members remain separately listed, with family/version unknown.'}
    result['gaps'] += [
        'Missing extensions: ' + ', '.join(result['missing_extensions']),
        'Missing major save-version fields (1..26 navigation): ' + ', '.join(map(str, result['save_version_inventory']['unobserved_major_numbers_1_through_26'])),
        'No authoritative save-version field selected: multiple vers resources can describe different metadata; all raw fields retained',
        'Packed PE/MZ libraries remain opaque; embedded artifact counts and versions are unknown',
        'Archive inspection is one level; nested archives and nonselected member formats are not recursively interpreted',
        'Typedef status, protected/removed diagrams, tests, build behavior and module requirements need independent native inspection',
        'This extension and magic based inventory is not proof of exhaustive discovery of every possible LabVIEW artifact format']
    return result


def markdown(result):
    lines = ['# Prepared-source coverage', '',
             'Public development inventory; independent review pending. native_labview: not executed.',
             'Regenerate: `python3 -I benchmark/scripts/coverage.py`; verify: add `--check`.',
             'See [coverage.json](coverage.json) for every artifact, raw version field and gap.', '',
             '| Family | Entries | Version fields (occurrences) | No version |', '|---|---:|---|---:|']
    for name, family in result['families'].items():
        versions = '; '.join(f'{v}: {n}' for v, n in sorted(family['version_fields'].items())) or 'unavailable'
        lines.append(f"| {name} | {family['count']} | {versions} | {family['without_version']} |")
    lines += ['', 'Version-field occurrences are not additional artifacts. Archive members remain separate entries, including copies.',
              'No version or family is removed from the goal; the 2024 fallback is not selected.', '']
    lines += ['- ' + gap for gap in result['gaps']]
    return ('\n'.join(lines) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        location = os.environ.get('LABVIEW_ENVIRONMENT')
        sources.require(bool(location), 'LABVIEW_ENVIRONMENT required; no download fallback')
        result = enrich(inventory(Path(location)), Path(location))
        # Keep the complete per-artifact record below the evidence index size limit.
        coverage_bytes = (json.dumps(result, indent=1, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')
        outputs = (coverage_bytes, markdown(result))
        for relative, content in zip(OUTPUTS, outputs):
            path = ROOT / relative
            sources.require(not path.is_symlink(), 'Output must not be a symlink: ' + relative)
            if args.check:
                sources.require(path.is_file() and path.read_bytes() == content, relative + ' differs; regenerate and review')
            else:
                path.write_bytes(content)
        print(('Verified' if args.check else 'Generated') + f" coverage: {len(result['artifacts'])} entries, {len(result['families'])} families; native_labview: not executed")
        return 0
    except (ValueError, KeyError, TypeError, OSError, struct.error, zipfile.BadZipFile) as error:
        print('coverage: ERROR: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
