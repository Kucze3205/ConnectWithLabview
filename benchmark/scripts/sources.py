#!/usr/bin/env python3
"""Inventory prepared public sources offline; never accept drift over an existing lock.

Run with python3 -I. No prepared code is imported or executed. No originals are
converted. Git is used only to read HEAD and its tree; blob integrity is checked
from bytes independently of worktree timestamps and git's stat cache.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'benchmark/sources.json'
PINS = {
    'pylavi': ('https://github.com/marcpage/pylavi',
               '35d2a0318f71dcb87bb9c431dc00700ee6b9fb75', 'Unlicense', 'LICENSE'),
    'actor-framework': ('https://github.com/ni/actor-framework',
                        '371c631c16155d88f02be11a953e4964d7452fd8', 'MIT', 'LICENSE.txt'),
}
FIXTURE = 'Core/ActorFramework/Actor/Actor Core.vi'
FIXTURE_SHA256 = '135d50e68f002aea9c6a08d0265cc6178b326f1af99353755064c953eaec063c'
# Selection is intentionally explicit. Archives are not unpacked or executed.
EXTENSIONS = {
    '.vi', '.vit', '.ctl', '.ctt', '.vim', '.mnu', '.llb', '.rtexe',
    '.gbl', '.glb', '.lsb', '.uir', '.lvlibp', '.lvproj', '.lvlib',
    '.lvclass', '.xctl', '.xnode', '.lvtest', '.vip', '.vipc', '.vipb',
    '.aliases', '.lvlps', '.viancfg',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')


def git(directory, *args):
    command = ['git', '--no-replace-objects', '--no-optional-locks',
               '-c', 'safe.directory=' + str(directory),
               '-c', 'core.fsmonitor=false', '-C', str(directory), *args]
    result = subprocess.run(command, capture_output=True, check=False)
    require(result.returncode == 0,
            'git ' + ' '.join(args) + ': ' + result.stderr.decode('utf-8', 'replace'))
    return result.stdout


def regular_file(root, relative):
    rel = Path(relative)
    require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe path: ' + relative)
    current = root
    for part in rel.parts:
        current = current / part
        require(not current.is_symlink(), 'Symlink is not an original regular file: ' + str(current))
    require(current.is_file(), 'Missing regular file: ' + str(current))
    return current.read_bytes()


def version(raw):
    """Decode the packed LabVIEW BCD version, retaining the exact header value."""
    value = int(raw, 16)
    major_tens, major_units = (value >> 28) & 15, (value >> 24) & 15
    minor, patch = (value >> 20) & 15, (value >> 16) & 15
    phase = (value >> 13) & 7
    build_digits = [(value >> shift) & 15 for shift in (8, 4, 0)]
    valid = all(x <= 9 for x in [major_tens, major_units, minor, patch, *build_digits])
    decoded = None
    if valid and phase in (1, 2, 3, 4):
        build = ((value >> 12) & 1) * 1000 + build_digits[0] * 100 + build_digits[1] * 10 + build_digits[2]
        decoded = f'{major_tens * 10 + major_units}.{minor}.{patch}{"?dabf"[phase]}{build}'
    return {'raw_hex': raw.lower(), 'decoded': decoded}


def save_version(data):
    """Read only container metadata, never diagrams or semantic oracle answers."""
    if data.startswith(b'RSRC'):
        require(len(data) >= 32, 'Truncated RSRC header')
        signature, check, fmt, kind, creator, meta, meta_size, start, size = struct.unpack_from('>4s2sH4s4sIIII', data)
        if fmt != 3:
            return {'status': 'unavailable', 'reason': f'Unsupported RSRC format {fmt}'}
        require(check == b'\r\n', 'Corrupt RSRC marker')
        require(start == 32 and start + size == meta and meta + meta_size <= len(data), 'Invalid RSRC bounds')
        require(meta_size >= 68 and data[meta:meta + 32] == data[:32], 'Invalid secondary RSRC header')
        base = meta + 52
        count = struct.unpack_from('>I', data, base)[0] + 1
        require(count <= (meta_size - 56) // 12, 'Invalid RSRC type count')
        found = {}
        for index in range(count):
            resource_type, entries_minus_one, offset = struct.unpack_from('>4sII', data, base + 4 + index * 12)
            entries = entries_minus_one + 1
            table = base + offset
            require(table >= base + 4 + count * 12 and table + entries * 20 <= meta + meta_size, 'Invalid RSRC resource table')
            for entry in range(entries):
                resource_id, name_offset, unused, data_offset, unused2 = struct.unpack_from('>IIIII', data, table + entry * 20)
                location = start + data_offset
                require(start <= location and location + 4 <= meta, 'Invalid RSRC data offset')
                length = struct.unpack_from('>I', data, location)[0]
                require(location + 4 + length <= meta, 'Truncated RSRC resource')
                if resource_type in (b'LVSR', b'vers') and length >= 4:
                    found.setdefault(resource_type, []).append((location + 4, data[location + 4:location + 8]))
        for resource_type in (b'LVSR', b'vers'):
            if resource_type in found:
                values = found[resource_type]
                require(len({raw for _, raw in values}) == 1, 'Conflicting version resources')
                offset, raw = values[0]
                return {'status': 'recorded', 'method': 'RSRC/' + resource_type.decode('ascii') + ' first UInt32',
                        'byte_offset': offset, **version(raw.hex())}
        return {'status': 'unavailable', 'reason': 'No LVSR or vers version resource'}
    # XML LVVersion is the file header declaration, not a runtime compatibility claim.
    if data.lstrip(b'\xef\xbb\xbf \r\n\t').startswith(b'<?xml'):
        element = ET.fromstring(data)
        raw = element.attrib.get('LVVersion')
        if raw is not None:
            require(len(raw) == 8 and all(c in '0123456789abcdefABCDEF' for c in raw), 'Invalid XML LVVersion')
            return {'status': 'recorded', 'method': 'XML root @LVVersion', **version(raw)}
        return {'status': 'unavailable', 'reason': 'XML header has no LVVersion attribute'}
    return {'status': 'unavailable', 'reason': 'No supported RSRC or XML version header; archive contents not inspected'}


def inventory(environment):
    require(environment.is_dir() and not environment.is_symlink(), 'Invalid LABVIEW_ENVIRONMENT directory')
    readiness_bytes = regular_file(environment, 'readiness.json')
    readiness = json.loads(readiness_bytes)
    expected = {name: {'name': name, 'commit': pin[1], 'license': pin[2]} for name, pin in PINS.items()}
    actual = {source['name']: source for source in readiness['sources']}
    require(len(actual) == len(readiness['sources']) and actual == expected, 'Prepared readiness source pins/licenses differ')
    require(readiness.get('public_sources') == 'ready', 'Public sources are not prepared')
    require(readiness.get('fixture') == FIXTURE and readiness.get('sha256') == FIXTURE_SHA256, 'Prepared fixture pin differs')
    repositories = []
    for name, (url, commit, license_name, license_path) in sorted(PINS.items()):
        directory = environment / name
        require(directory.is_dir() and not directory.is_symlink(), 'Missing source directory: ' + name)
        require(git(directory, 'rev-parse', 'HEAD').decode().strip() == commit, 'HEAD pin differs: ' + name)
        tree = git(directory, 'ls-tree', '-rz', '--full-tree', commit)
        all_files, artifacts = [], []
        for item in tree.split(b'\0'):
            if not item:
                continue
            header, path_bytes = item.split(b'\t', 1)
            mode, object_type, oid = header.split()
            relative = path_bytes.decode('utf-8')
            require(mode in (b'100644', b'100755') and object_type == b'blob', 'Unsupported git entry: ' + name + '/' + relative)
            data = regular_file(directory, relative)
            blob_oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            require(blob_oid == oid.decode(), 'Prepared bytes differ from pinned git blob: ' + name + '/' + relative)
            record = {'path': relative, 'size': len(data), 'sha256': sha256(data)}
            all_files.append(record)
            if Path(relative).suffix.lower() in EXTENSIONS:
                try:
                    artifact = dict(record, save_version=save_version(data))
                except (ValueError, struct.error, ET.ParseError) as error:
                    raise ValueError(name + '/' + relative + ': ' + str(error)) from error
                artifacts.append(artifact)
        all_files.sort(key=lambda record: record['path'])
        artifacts.sort(key=lambda record: record['path'])
        license_data = regular_file(directory, license_path)
        require(any(record['path'] == license_path for record in all_files), 'License is not tracked: ' + name)
        marker = b'free and unencumbered software' if license_name == 'Unlicense' else b'MIT License'
        require(marker.lower() in license_data.lower(), 'License marker differs: ' + name)
        repositories.append({
            'name': name, 'upstream_url': url, 'commit': commit, 'license': license_name,
            'license_file': {'path': license_path, 'sha256': sha256(license_data), 'size': len(license_data)},
            'tracked_file_count': len(all_files), 'tracked_files_sha256': sha256(encoded(all_files)),
            'artifacts': artifacts,
        })
    fixture = regular_file(environment / 'actor-framework', FIXTURE)
    require(sha256(fixture) == FIXTURE_SHA256, 'Prepared fixture hash differs')
    return {
        'schema_version': 1,
        'scope': 'Public prepared development-source candidates only; no withheld evaluation cases or answers',
        'preparation_readiness_sha256': sha256(readiness_bytes),
        'selection': {'tracked_artifact_extensions': sorted(EXTENSIONS), 'archives_unpacked': False,
                      'untracked_files_used': False, 'originals_modified': False},
        'reading_environment': {'command': 'python3 -I benchmark/scripts/sources.py',
                                'implementation': 'Python standard library and read-only local git metadata; no source code imported',
                                'native_labview': 'not executed', 'semantic_reading': 'not measured',
                                'dependencies': 'Artifact dependency resolution not performed'},
        'repositories': repositories,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare without writing; missing or changed manifest fails')
    args = parser.parse_args()
    try:
        location = os.environ.get('LABVIEW_ENVIRONMENT')
        require(bool(location), 'LABVIEW_ENVIRONMENT is required; no download fallback')
        generated = inventory(Path(location))
        expected_bytes = encoded(generated)
        if OUTPUT.exists():
            require(not OUTPUT.is_symlink(), 'sources.json must not be a symlink')
            previous = json.loads(OUTPUT.read_bytes())
            require(previous == generated, 'Recorded provenance differs from prepared files; sources.json preserved. Investigate drift before changing pins or hashes.')
            if args.check:
                require(OUTPUT.read_bytes() == expected_bytes, 'sources.json is not in canonical generated format')
        else:
            require(not args.check, 'Missing benchmark/sources.json; generate it first')
        if not args.check:
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_bytes(expected_bytes)
        count = sum(len(repo['artifacts']) for repo in generated['repositories'])
        print(('Verified' if args.check else 'Generated') + f' benchmark/sources.json: {len(PINS)} repositories, {count} artifacts; no native or semantic verification')
        return 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as error:
        print('sources: ERROR: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
