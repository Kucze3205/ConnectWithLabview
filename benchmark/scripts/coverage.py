#!/usr/bin/env python3
"""Inventory prepared public artifact coverage offline; --check never writes.

Reuses sources.py's provenance verification and the research inventory's family,
archive-member, dual-version and per-resource decoder observations. Neither
metadata parsing nor byte round-tripping establishes semantic reading.
"""
import argparse
import collections
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / 'benchmark/coverage.json'
MD_PATH = ROOT / 'benchmark/coverage.md'
EXTENSIONS = {
    '.vi', '.vit', '.vim', '.ctl', '.ctt', '.llb', '.mnu', '.rtm', '.uir',
    '.lvclass', '.lvlib', '.lvlibp', '.lvproj', '.lvlps', '.lvsc', '.xctl',
    '.xnode', '.lvtest', '.viancfg', '.vipb', '.vip', '.vipc', '.aliases',
    '.gbl', '.glb', '.lsb', '.rtexe', '.dll', '.exe', '.so',
}
ARCHIVES = {'.zip', '.vip', '.vipc', '.vsix', '.lvlibp'}
LIMITS = {'archive_depth': 8, 'member_bytes': 32 * 1024 * 1024,
          'total_member_bytes': 256 * 1024 * 1024, 'archive_entries': 50000}


def load_sources():
    spec = importlib.util.spec_from_file_location('coverage_sources', ROOT / 'benchmark/scripts/sources.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_rsrc(data, sources):
    """Bounded format-3 table inspection, retaining both vers and LVSR claims."""
    require = sources.require
    require(len(data) >= 32, 'Truncated RSRC header')
    magic, check, fmt, kind, creator, meta, meta_size, start, size = struct.unpack_from('>4s2sH4s4sIIII', data)
    require(check == b'\r\n' and fmt == 3, 'Unsupported RSRC marker/format: ' + str(fmt))
    require(start == 32 and start + size == meta and meta + meta_size <= len(data), 'Invalid RSRC bounds')
    require(meta_size >= 68 and data[meta:meta + 32] == data[:32], 'Invalid secondary RSRC header')
    base = meta + 52
    count = struct.unpack_from('>I', data, base)[0] + 1
    require(count <= (meta_size - 56) // 12, 'Invalid RSRC type count')
    resources = []
    for index in range(count):
        code, n, offset = struct.unpack_from('>4sII', data, base + 4 + index * 12)
        table = base + offset
        require(table >= base + 4 + count * 12 and table + (n + 1) * 20 <= meta + meta_size, 'Invalid resource table')
        for entry in range(n + 1):
            rid, name, unused, data_offset, unused2 = struct.unpack_from('>IIIII', data, table + entry * 20)
            location = start + data_offset
            require(start <= location and location + 4 <= meta, 'Invalid resource offset')
            length = struct.unpack_from('>I', data, location)[0]
            require(location + 4 + length <= meta, 'Truncated resource body')
            resources.append((code.decode('latin-1'), rid, location + 4, data[location + 4:location + 4 + length]))
    versions = {}
    for code in ('vers', 'LVSR'):
        values = [{'resource_id': rid, 'byte_offset': offset, **sources.version(body[:4].hex())}
                  for name, rid, offset, body in resources if name == code and len(body) >= 4]
        if values:
            versions[code] = sorted(values, key=lambda item: (item['resource_id'], item['byte_offset']))
    return kind.decode('latin-1'), versions, resources


def inventory(environment, sources):
    provenance = sources.inventory(environment)
    sources.require(sources.OUTPUT.read_bytes() == sources.encoded(provenance),
                    'sources.json differs from prepared originals; investigate provenance drift first')
    # Import only after every tracked source byte has passed pinned-blob verification.
    sys.path.insert(0, str(environment / 'pylavi'))
    try:
        from pylavi import file as pl_file, resource_types as pl_types
        decoder_import = 'ok'
    except Exception as error:
        pl_file, pl_types = None, None
        decoder_import = type(error).__name__ + ': ' + str(error)
    artifacts, archive_gaps = [], []
    families = {}
    all_extensions = collections.Counter()
    resource_counts = {}
    xml_types, target_types, dependency_refs = collections.Counter(), collections.Counter(), []
    consumed = 0

    def add(path, data, disk_path=None, depth=0, force=False):
        nonlocal consumed
        ext = Path(path.rsplit('!', 1)[-1]).suffix.lower()
        is_zip = data[:4] in (b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08')
        if not (force or ext in EXTENSIONS or ext in ARCHIVES or data.startswith(b'RSRC') or is_zip):
            return
        nested = disk_path is None
        record = {'path': path, 'size': len(data), 'sha256': sources.sha256(data),
                  'location': 'archive member' if nested else 'tracked original',
                  'save_versions': {}, 'metadata_status': 'unavailable',
                  'native_access': 'not examined', 'semantic_reading': 'not measured'}
        container = 'text/other'
        resources = []
        if data.startswith(b'RSRC'):
            try:
                kind, versions, resources = parse_rsrc(data, sources)
                container = 'RSRC ' + kind
                record.update(save_versions=versions, metadata_status='parsed',
                              resource_types=sorted(set(r[0] for r in resources)))
                a, b = versions.get('vers', []), versions.get('LVSR', [])
                record['vers_lvsr_disagree'] = bool(a and b and {v['raw_hex'] for v in a} != {v['raw_hex'] for v in b})
                if disk_path is not None and pl_file:
                    try:
                        pl_file.Resources.load(str(disk_path))
                        record['pylavi_load'] = 'ok'
                    except Exception as error:
                        record['pylavi_load'] = 'error: ' + type(error).__name__
                else:
                    record['pylavi_load'] = 'not executed: archive member or unavailable importer'
            except (ValueError, struct.error) as error:
                container = 'RSRC unreadable/unsupported'
                record.update(metadata_status='unreadable/unsupported', metadata_gap=str(error))
        elif is_zip:
            container = 'zip'
            record['metadata_status'] = 'container only'
        elif data.startswith(b'MZ'):
            container = 'PE/opaque'
            record['metadata_gap'] = 'Packed/compiled contents not inspected; embedded artifacts unknown'
        elif data.lstrip(b'\xef\xbb\xbf \r\n\t').startswith(b'<?xml'):
            container = 'XML'
            try:
                element = ET.fromstring(data)
                record['metadata_status'] = 'parsed'
                raw = element.attrib.get('LVVersion')
                if raw is not None:
                    sources.require(len(raw) == 8 and all(c in '0123456789abcdefABCDEF' for c in raw), 'Invalid XML LVVersion')
                    record['save_versions'] = {'XML @LVVersion': [sources.version(raw)]}
                for item in element.iter('Item'):
                    typ = item.get('Type', '(missing)')
                    xml_types[typ] += 1
                    if typ in ('My Computer', 'RT Target', 'FPGA Target') or 'Target' in typ:
                        target_types[typ] += 1
                    if typ == 'Dependencies':
                        dependency_refs.append({'path': path, 'declared_child_items': len(item.findall('Item'))})
            except (ET.ParseError, ValueError) as error:
                record.update(metadata_status='unreadable/unsupported', metadata_gap=str(error))
        record['family'] = (ext or '(no extension)') + ' ' + container + (' (archive member)' if nested else '')
        if not record['save_versions']:
            record['save_version_gap'] = 'No supported version declaration observed; filenames are not version evidence'
        if container == 'text/other':
            record['magic_hex'] = data[:8].hex()
            record['metadata_gap'] = 'No supported RSRC/XML metadata; semantic contents unexamined'
        artifacts.append(record)
        fam = families.setdefault(record['family'], {'count': 0, 'save_versions': collections.Counter(),
                      'metadata_status': collections.Counter(), 'pylavi_load': collections.Counter(), 'resources': {}})
        fam['count'] += 1
        fam['metadata_status'][record['metadata_status']] += 1
        fam['pylavi_load'][record.get('pylavi_load', 'not applicable')] += 1
        values = {v['raw_hex'] for group in record['save_versions'].values() for v in group}
        fam['save_versions'].update(values or ['unavailable'])
        for code, rid, offset, body in resources:
            entry = fam['resources'].setdefault(code, {'instances': 0, 'decoder': None, 'statuses': collections.Counter()})
            entry['instances'] += 1
            cls = getattr(pl_types, 'Type' + code.strip(), None) if pl_types else None
            status = 'opaque: no decoder' if pl_types else 'not executed: importer unavailable'
            if cls:
                entry['decoder'] = cls.__name__
                try:
                    value = cls().from_bytes(body)
                    status = 'decoded-roundtrip' if value.to_bytes() == body else 'decoded-not-roundtrip'
                except Exception as error:
                    status = 'error: ' + type(error).__name__
            entry['statuses'][status] += 1
        if not is_zip:
            if ext in ARCHIVES and container != 'PE/opaque':
                archive_gaps.append({'path': path, 'reason': 'Archive-like extension without ZIP signature; contents unexamined'})
            return
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                members = archive.infolist()
                record['archive_entry_count'] = len(members)
                record['archive_members_examined'] = 0
                if depth >= LIMITS['archive_depth'] or len(members) > LIMITS['archive_entries']:
                    archive_gaps.append({'path': path, 'reason': 'Archive depth/entry safety bound; contents unexamined', 'entries': len(members)})
                    return
                for index, member in enumerate(members):
                    if member.is_dir():
                        continue
                    member_path = path + '!' + member.filename
                    if member.file_size > LIMITS['member_bytes'] or consumed + member.file_size > LIMITS['total_member_bytes']:
                        archive_gaps.append({'path': member_path, 'entry_index': index, 'size': member.file_size, 'reason': 'Uncompressed-byte safety bound; member unexamined'})
                        continue
                    try:
                        body = archive.read(member)
                    except (OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError) as error:
                        archive_gaps.append({'path': member_path, 'entry_index': index, 'reason': 'Unreadable member: ' + type(error).__name__})
                        continue
                    consumed += len(body)
                    record['archive_members_examined'] += 1
                    before = len(artifacts)
                    add(member_path, body, depth=depth + 1)
                    if len(artifacts) > before:
                        artifacts[before]['archive_entry_index'] = index
        except (OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError) as error:
            record['metadata_status'] = 'unreadable/unsupported'
            archive_gaps.append({'path': path, 'reason': 'Unreadable archive: ' + type(error).__name__})

    tracked = 0
    for repo in provenance['repositories']:
        directory = environment / repo['name']
        tree = sources.git(directory, 'ls-tree', '-rz', '--full-tree', repo['commit'])
        for entry in tree.split(b'\0'):
            if not entry:
                continue
            relative = entry.split(b'\t', 1)[1].decode('utf-8')
            tracked += 1
            all_extensions[Path(relative).suffix.lower() or '(none)'] += 1
            data = sources.regular_file(directory, relative)
            add(repo['name'] + '/' + relative, data, disk_path=directory / relative)
    versions = {}
    for artifact in artifacts:
        for field, values in artifact['save_versions'].items():
            for value in values:
                item = versions.setdefault(value['raw_hex'], {'decoded': value['decoded'], 'artifacts': set(), 'fields': set()})
                item['artifacts'].add(artifact['path'])
                item['fields'].add(field)
    for item in versions.values():
        item['artifact_count'] = len(item.pop('artifacts'))
        item['fields'] = sorted(item['fields'])
    observed_extensions = {Path(a['path'].rsplit('!', 1)[-1]).suffix.lower() for a in artifacts}
    return {
        'schema_version': 1,
        'scope': 'Prepared public development candidates only; all-version/all-family goal unchanged',
        'sources_sha256': sources.sha256(sources.OUTPUT.read_bytes()),
        'source_pins': [{'name': r['name'], 'commit': r['commit'], 'license': r['license']} for r in provenance['repositories']],
        'method': {'research': 'docs/research/scripts/coverage/inventory.py',
                   'selection': 'All pinned tracked files inspected for listed extensions, RSRC or ZIP signature; recursive ZIP members inspected similarly',
                   'artifact_extensions': sorted(EXTENSIONS), 'archive_extensions': sorted(ARCHIVES),
                   'version_semantics': 'vers and LVSR retained separately, including disagreements; neither established as authoritative; XML root LVVersion separately',
                   'resource_decoding': 'Pinned pylavi per-resource from_bytes/to_bytes; roundtrip is metadata evidence, not semantic correctness',
                   'archive_limits': LIMITS, 'originals_modified': False, 'archives_extracted_to_disk': False},
        'denominator': {'tracked_files_inspected': tracked, 'artifact_occurrences': len(artifacts),
                        'tracked_artifacts': sum(a['location'] == 'tracked original' for a in artifacts),
                        'archive_member_artifacts': sum(a['location'] == 'archive member' for a in artifacts),
                        'duplicates_retained': True, 'unresolved_archive_gaps': len(archive_gaps),
                        'unknown_embedded_artifact_count': 'Unknown for opaque/limited/unreadable containers; not zero'},
        'reading_environments': {
            'executed': {'command': 'python3 -I benchmark/scripts/coverage.py',
                         'implementation': 'Python standard library, local git and pinned pylavi',
                         'pylavi_import': decoder_import, 'native_labview': 'not executed',
                         'semantic_reading': 'not measured'},
            'documented_only': {'source': 'docs/perpetua/environment.md',
                'native_cloud': 'LabVIEW 2026 Q1: prior isolated LV2014 MassCompile; not this corpus or inventory',
                'native_2024': 'unverified', 'cross_version_compatibility': 'unverified'}},
        'access_conditions': {'public_sources': 'Prepared MIT and Unlicense sources; not withheld evaluation data',
            'native_labview': 'not executed', 'installed_modules': 'not inspected',
            'dependency_resolution': 'not performed; XML declarations only',
            'licenses_activation': 'not checked for native execution or modules',
            'diagrams': 'Protected, removed and inaccessible diagrams not determined; heaps remain opaque to metadata decoders',
            'hardware': 'not executed; static target declarations do not establish behavior'},
        'modules_and_targets': {'xml_item_types': dict(sorted(xml_types.items())),
            'xml_target_types': dict(sorted(target_types.items())), 'dependency_declarations': dependency_refs,
            'native_module_coverage': 'None established',
            'unexamined_dimensions': ['Real-Time', 'FPGA', 'DSC', 'Vision', 'DAQmx', 'MathScript', 'hardware targets', 'other modules/toolkits']},
        'gaps': {'missing_extensions': sorted(EXTENSIONS - observed_extensions),
            'missing_forms': ['Binary lvclass/lvlib', 'RSRC packed libraries', 'native build-spec interpretation', 'semantic diagrams/types/dependencies'],
            'unexamined_versions': 'Every native LabVIEW version/build remains unexamined by this inventory, including observed header versions; unobserved releases and older versions remain gaps',
            'fallback_2024_selected': False,
            'corpus_limits': 'One public framework and parser tests; metadata inventory does not establish representative or semantic coverage',
            'archive_gaps': archive_gaps},
        'tracked_file_extensions': dict(sorted(all_extensions.items())),
        'save_versions': dict(sorted(versions.items())),
        'families': dict(sorted(families.items())),
        'artifacts': sorted(artifacts, key=lambda a: (a['path'], a.get('archive_entry_index', -1))),
    }


def markdown(result):
    denominator = result['denominator']
    lines = ['# Prepared public coverage inventory', '',
        'Preparation evidence only, pending independent review; no benchmark readiness or product approval.', '',
        'Regenerate with `python3 -I benchmark/scripts/coverage.py`; verify with `python3 -I benchmark/scripts/coverage.py --check`.',
        'Inputs are the pinned read-only `$LABVIEW_ENVIRONMENT` sources, verified against [sources.json](sources.json).',
        'The complete path, hash, dual-header versions, archive/access gaps and resource decoder counts are in [coverage.json](coverage.json).', '',
        f"Inspected {denominator['tracked_files_inspected']} tracked files; retained {denominator['artifact_occurrences']} artifact occurrences ({denominator['tracked_artifacts']} originals and {denominator['archive_member_artifacts']} archive members), including duplicates and unsupported cases.",
        'Archive members are read in memory recursively; originals are preserved. Unknown embedded contents remain unknown, not zero.', '',
        '| Family | Occurrences | Header versions: raw hex (artifact count) |', '| --- | ---: | --- |']
    for family, value in result['families'].items():
        text = '; '.join(f'{version}: {count}' for version, count in sorted(value['save_versions'].items()))
        lines.append(f"| {family} | {value['count']} | {text} |")
    lines += ['', 'A file can contribute both vers and LVSR declarations; version columns are not mutually exclusive. Their authoritative save-version meaning is unverified.',
        'Raw values and decoded labels are listed in JSON; unknown phase codes retain their raw values. No filename is used as version evidence.', '',
        '## Reading environments, modules and access', '',
        '`native_labview: not executed`. This inventory executes Python, git metadata inspection and pinned pylavi metadata decoders.',
        'Byte round-tripping and whole-file resource loading do not establish diagram, type, dependency or answer correctness.',
        'XML target/item types and dependency declarations are recorded as static evidence; installed modules, licensing, activation and dependency resolution are unverified.',
        'The earlier documented 2026 Q1 cloud MassCompile is separate evidence for one LV2014 fixture, not execution on this corpus. Native 2024 and cross-version compatibility remain unverified.', '',
        '## Explicit gaps', '',
        '- Missing extension families: ' + ', '.join(result['gaps']['missing_extensions']) + '.',
        '- All native versions/builds remain unexamined here, including observed header versions; unrepresented versions are gaps. The 2024 fallback is not selected.',
        '- Opaque resources, PE packed libraries, unknown embedded contents and unreadable/archive-limit cases stay in the inventory. See per-family decoder counts and archive_gaps in JSON.',
        '- Native LabVIEW is needed to establish header semantics, protected/removed diagram access, actual loading/compatibility, installed modules, resolved dependencies, build behavior and hardware results.',
        '- Real-Time, FPGA, DSC, Vision, DAQmx, MathScript and other modules/targets have no established native coverage. The first public corpus does not redefine the goal.', '',
        'Next: request independent review of this preparation, then prepare tasks/oracle with independently established expectations. Sources and coverage are preparation only; all other milestones and owner gates remain pending.', '']
    return '\n'.join(lines).encode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        sources = load_sources()
        location = os.environ.get('LABVIEW_ENVIRONMENT')
        sources.require(bool(location), 'LABVIEW_ENVIRONMENT is required; no download fallback')
        result = inventory(Path(location), sources)
        outputs = [(JSON_PATH, sources.encoded(result)), (MD_PATH, markdown(result))]
        for path, expected in outputs:
            sources.require(not path.is_symlink(), 'Output must not be a symlink: ' + str(path))
            if args.check:
                sources.require(path.is_file() and path.read_bytes() == expected, 'Missing or differing generated record: ' + str(path.relative_to(ROOT)))
        if not args.check:
            for path, expected in outputs:
                path.write_bytes(expected)
        print(('Verified' if args.check else 'Generated') + ' coverage JSON + Markdown: ' + str(result['denominator']) + '; native_labview: not executed')
        return 0
    except (ValueError, KeyError, TypeError, OSError, struct.error, json.JSONDecodeError) as error:
        print('coverage: ERROR: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
