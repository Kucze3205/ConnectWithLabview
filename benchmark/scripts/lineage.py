#!/usr/bin/env python3
"""Inventory public copies and possible variants, using only the standard library.
Run with python3 -I. Prepared source code is never imported or executed.
All pinned inputs and original/member bytes are checked before any output write.
"""
import argparse
from collections import defaultdict
import hashlib
import io
import itertools
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
GROUP_PREFIX = 'public-repository-'
MISSING = ['restricted store', 'custodian', 'private/new cases',
           'native structural comparison', 'tested isolation']
def split_text(split):
    reference = " (benchmark/split/, review #273)" if split == "design-reviewed" else ""
    return "Split is " + split + reference + "; no evaluation partitions are allocated."


def limitation(split):
    detail = (
        " Split is a reviewed design only (benchmark/split/ with benchmark/scripts/split_boundary.py, "
        "review #273 accept, the two non-blocking checker findings of #273 were fixed by #281 "
        "(re-review #298 confirmed the live mutation checks and exact reasons; its own revert harness was masked, so Policymaker #300 reverted each fix in a temporary copy and --check exited 1 both times)): no allocation exists, no isolation step is executed, "
        "the restricted store (capability #268) has an executed readiness record accepted by review #431 but holds no case, and no secrecy is claimed; "
        "author (copilot gpt-5.6-luna) and reviewer (codex gpt-6.1-sol) are both GPT-family models."
    ) if split == "design-reviewed" else ""
    return ("Public lineage inventory is prepared, unreviewed preparation only. "
            + split_text(split) + detail + " Still missing: " + ", ".join(MISSING)
            + ". Hash inequality does not establish independence. No evaluation allocation or readiness claim.")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')


def safe_path(relative):
    require(isinstance(relative, str) and relative and '\\' not in relative,
            'Invalid relative path')
    path = PurePosixPath(relative)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == relative,
            'Unsafe/noncanonical path: ' + relative)
    return path


def read_regular(base, relative):
    path = safe_path(relative)
    current = base
    require(not current.is_symlink(), 'Symlink root: ' + str(base))
    for part in path.parts:
        current = current / part
        require(not current.is_symlink(), 'Symlink: ' + str(current))
    require(current.is_file(), 'Missing regular file: ' + str(current))
    return current.read_bytes()


def git_head(directory):
    result = subprocess.run([
        'git', '--no-replace-objects', '--no-optional-locks',
        '-c', 'safe.directory=' + str(directory), '-c', 'core.fsmonitor=false',
        '-C', str(directory), 'rev-parse', 'HEAD'], capture_output=True, check=False)
    require(result.returncode == 0, 'Cannot inspect prepared Git HEAD')
    return result.stdout.decode('ascii').strip()


def pinned_inputs():
    preparation = json.loads(read_regular(ROOT, 'benchmark/preparation.json'))
    pins = defaultdict(set)
    for entries in preparation['milestones'].values():
        for entry in entries:
            pins[entry['path']].add(entry['sha256'])
    paths = ['benchmark/sources.json', 'benchmark/coverage.json',
             'benchmark/preparation-status.json']
    paths += sorted(str(p.relative_to(ROOT)) for p in
                    (ROOT / 'benchmark/cases/dev').glob('*.json'))
    require(len(paths) > 3, 'No development cases')
    contents = {}
    for path in paths:
        data = read_regular(ROOT, path)
        require(pins[path] == {sha(data)}, 'Missing/conflicting/stale input pin: ' + path)
        contents[path] = data
    sources = json.loads(contents['benchmark/sources.json'])
    coverage = json.loads(contents['benchmark/coverage.json'])
    require(coverage['sources_json_sha256'] == sha(contents['benchmark/sources.json']),
            'Coverage was generated from different sources')
    status = json.loads(contents['benchmark/preparation-status.json'])
    require(status['milestones']['split'] in ('not-started', 'design-reviewed'),
            'Unexpected split status')
    return preparation, contents, sources, coverage, status


def inventory(environment, sources, coverage):
    repositories = {r['name']: r for r in sources['repositories']}
    require(len(repositories) == len(sources['repositories']), 'Duplicate repository name')
    for name, repository in sorted(repositories.items()):
        safe_path(name)
        require('/' not in name, 'Invalid repository name')
        require(git_head(environment / name) == repository['commit'], 'Prepared commit mismatch: ' + name)
    require(sha(read_regular(environment, 'readiness.json')) == sources['preparation_readiness_sha256'],
            'Prepared readiness hash mismatch')
    originals = {}
    for name, repository in sorted(repositories.items()):
        for artifact in repository['artifacts']:
            path = name + '/' + artifact['path']
            data = read_regular(environment, path)
            require(sha(data) == artifact['sha256'] and len(data) == artifact['size'],
                    'Source original mismatch: ' + path)
            require(path not in originals, 'Duplicate source original: ' + path)
            originals[path] = data
    records = {}
    for artifact in coverage['artifacts']:
        archive = artifact['archive']
        path = artifact['path']
        safe_path(path)
        if archive is None:
            repository, relative = path.split('/', 1)
            require(repository in repositories, 'Unknown coverage repository')
            data = originals.get(path)
            if data is None:
                data = read_regular(environment, path)
            originals[path] = data
            key = (repository, '', relative, -1)
        else:
            safe_path(archive)
            repository = archive.split('/', 1)[0]
            require(repository in repositories, 'Unknown archive repository')
            index = artifact['member_index']
            require(type(index) is int and index >= 0, 'Invalid archive member index')
            key = (repository, archive, path, index)
            data = None
        require(key not in records, 'Duplicate coverage location')
        records[key] = (artifact, data)
    disk_paths = {k[0] + '/' + k[2] for k in records if not k[1]}
    require(set(originals) <= disk_paths, 'Source original missing from coverage denominator')
    disk_pins = {k[0] + '/' + k[2]: a for k, (a, _) in records.items() if not k[1]}
    for path, data in originals.items():
        require(sha(data) == disk_pins[path]['sha256'] and len(data) == disk_pins[path]['size'],
                'Coverage original mismatch: ' + path)
    archives = {}
    for key, (artifact, data) in list(records.items()):
        if key[1]:
            archive = key[1]
            require(archive in disk_pins, 'Unpinned archive container: ' + archive)
            if archive not in archives:
                archives[archive] = zipfile.ZipFile(io.BytesIO(originals[archive]))
            handle = archives[archive]
            entries = handle.infolist()
            require(key[3] < len(entries), 'Missing member index')
            info = entries[key[3]]
            require(info.filename == key[2] and not info.is_dir(), 'Archive member identity mismatch')
            require(info.file_size == artifact['size'], 'Archive member size mismatch')
            data = handle.read(info)
            records[key] = (artifact, data)
        require(sha(data) == artifact['sha256'] and len(data) == artifact['size'],
                'Coverage member/original hash mismatch: ' + str(key))
    for handle in archives.values():
        handle.close()
    artifacts = []
    payloads = {}
    for index, (key, (artifact, data)) in enumerate(sorted(records.items())):
        repository, archive, path, member_index = key
        item = {
            'id': 'artifact-%04d' % index, 'repository': repository,
            'path': path, 'archive': archive or None,
            'member_index': member_index if archive else None,
            'sha256': artifact['sha256'], 'size': artifact['size'],
            'family': artifact['family'], 'save_versions': artifact['save_versions'],
            'declared_qualified_names': [],
        }
        if archive:
            item['container_sha256'] = disk_pins[archive]['sha256']
        artifacts.append(item)
        payloads[item['id']] = data
    require(len(artifacts) == coverage['denominator']['artifact_entries'], 'Coverage count mismatch')
    return artifacts, payloads, repositories


def declared_names(artifacts, payloads):
    """Static XML membership clues, never a native name/structural assertion."""
    locations = defaultdict(list)
    for item in artifacts:
        locations[(item['repository'], item['archive'], item['path'])].append(item['id'])
    by_id = {item['id']: item for item in artifacts}
    parents = defaultdict(set)
    declarations = []
    containers = set()
    gaps = []
    for item in artifacts:
        if PurePosixPath(item['path']).suffix.lower() not in ('.lvlib', '.lvclass'):
            continue
        try:
            root = ET.fromstring(payloads[item['id']])
        except ET.ParseError:
            gaps.append({'artifact': item['id'], 'reason': 'Container is not parseable XML'})
            continue
        containers.add(item['id'])
        for ordinal, member in enumerate(root.iter('Item')):
            url = member.get('URL', '')
            name = member.get('Name', '')
            if not url or not name:
                continue
            # LabVIEW symbolic/absolute URLs require native resolution; retain the gap.
            if url.startswith('/') or ':' in url or '\\' in url:
                gaps.append({'artifact': item['id'], 'item_ordinal': ordinal,
                             'reason': 'Nonrelative membership URL not resolved'})
                continue
            # These serialized URLs traverse from the container path itself.
            # Parent/friend references express relationships, not ownership.
            if member.get('Type') in ('Parent', 'Friended VI', 'Class Private Data'):
                gaps.append({'artifact': item['id'], 'item_ordinal': ordinal,
                             'reason': 'Nonownership or implicit private-data declaration excluded from name inference'})
                continue
            target = posixpath.normpath(posixpath.join(item['path'], url))
            if target.startswith('../'):
                gaps.append({'artifact': item['id'], 'item_ordinal': ordinal,
                             'reason': 'Membership URL escapes inventory root'})
                continue
            matches = locations.get((item['repository'], item['archive'], target), [])
            if not matches:
                gaps.append({'artifact': item['id'], 'item_ordinal': ordinal,
                             'reason': 'Membership URL target absent from pinned inventory'})
            for target_id in matches:
                parents[target_id].add((item['id'], name))
                declarations.append({'container': item['id'], 'item_ordinal': ordinal,
                                     'name': name, 'url': url, 'target': target_id})
    def names(identity, visited):
        if identity in visited:
            return set()
        result = set()
        for parent, name in sorted(parents[identity]):
            for prefix in names(parent, visited | {identity}):
                result.add(prefix + ':' + name)
        if not parents[identity] and identity in containers:
            result.add(PurePosixPath(by_id[identity]['path']).name)
        return result
    for item in artifacts:
        item['declared_qualified_names'] = sorted(names(item['id'], set()))
    return declarations, gaps


def group_candidates(artifacts):
    buckets = defaultdict(list)
    for item in artifacts:
        buckets[('same-relative-name', item['path'])].append(item)
        for name in item['declared_qualified_names']:
            buckets[('same-declared-qualified-name', name)].append(item)
        # Additional conservative clue for moved/binary files whose native names are unavailable.
        buckets[('same-basename', PurePosixPath(item['path']).name)].append(item)
    candidates = []
    pairs = set()
    for (rule, name), members in sorted(buckets.items()):
        if len(members) < 2:
            continue
        hashes = {m['sha256'] for m in members}
        versions = {v['decoded'] for m in members for v in m['save_versions']
                    if v.get('decoded') and v['field'] in ('LVSR', 'XML root @LVVersion')}
        if len(hashes) < 2 and len(versions) < 2:
            continue
        reasons = ['different-sha256'] if len(hashes) > 1 else []
        if len(versions) > 1:
            reasons.append('different-recorded-save-versions')
        ids = sorted(m['id'] for m in members)
        candidates.append({'id': 'candidate-%04d' % len(candidates),
                           'status': 'candidate-unadjudicated', 'rule': rule,
                           'matching_name': name, 'reasons': reasons,
                           'distinct_hashes': len(hashes), 'recorded_save_versions': sorted(versions),
                           'members': ids})
        pairs.update(tuple(sorted((a['id'], b['id']))) for a, b in itertools.combinations(members, 2)
                     if a['sha256'] != b['sha256'])
    return candidates, len(pairs)


def lineage_map(artifacts, exact, candidates, cases, repositories):
    by_id = {a['id']: a for a in artifacts}
    joins = {name: {name} for name in repositories}
    for group in exact + candidates:
        names = {by_id[identity]['repository'] for identity in group['members']}
        for name in names:
            joins[name].update(names)
    for name in sorted(joins):
        frontier = list(joins[name])
        while frontier:
            other = frontier.pop()
            new = joins[other] - joins[name]
            joins[name].update(new)
            frontier.extend(new)
    mapped = defaultdict(list)
    case_records = []
    dev_repositories = defaultdict(set)
    for path, data in sorted(cases.items()):
        case = json.loads(data)
        original = case['artifact']
        repository = original['repository']
        require(repository in repositories and original['commit'] == repositories[repository]['commit'],
                'Development repository pin mismatch: ' + path)
        require(original['identity_manifest_sha256'] == sha(read_regular(ROOT, original['identity_manifest'])),
                'Development identity manifest changed: ' + path)
        chain = original['archive_member_chain']
        require(len(chain) <= 1, 'Nested development archive requires explicit support')
        archive = repository + '/' + chain[0]['container_path'] if chain else None
        matches = [a for a in artifacts if a['repository'] == repository and
                   a['path'] == original['path'] and a['archive'] == archive and
                   a['sha256'] == original['sha256'] and
                   (not chain or (a['member_index'] == chain[0]['member_index'] and
                                  a['container_sha256'] == chain[0]['container_sha256'] and
                                  a['sha256'] == chain[0]['member_sha256'] and
                                  a['path'] == chain[0]['member_path']))]
        require(len(matches) == 1, 'Development artifact does not resolve uniquely: ' + path)
        group = case['lineage_group_id']
        require(isinstance(group, str) and group, 'Missing development lineage ID')
        dev_repositories[group].add(repository)
        case_records.append({'path': path, 'sha256': sha(data), 'lineage_group_id': group,
                             'artifact_id': matches[0]['id']})
    groups = {}
    for group, names in sorted(dev_repositories.items()):
        closure = set().union(*(joins[name] for name in names))
        mapped[group] = [a['id'] for a in artifacts if a['repository'] in closure]
        groups[group] = {'members': mapped[group], 'repositories': sorted(closure),
                         'status': 'conservative-public-development-constraint',
                         'method': 'Whole repositories plus cross-repository exact/candidate closure; preserves existing dev lineage IDs.'}
    for name in sorted(repositories):
        if not any(name in g['repositories'] for g in groups.values()):
            closure = joins[name]
            group = GROUP_PREFIX + '-and-'.join(sorted(closure))
            groups[group] = {'members': [a['id'] for a in artifacts if a['repository'] in closure],
                             'repositories': sorted(closure), 'status': 'provisional-public-project-envelope',
                             'method': 'Conservative whole-repository envelope; absence of matches is not independence.'}
    for case in case_records:
        require(case['artifact_id'] in groups[case['lineage_group_id']]['members'], 'Dev lineage disagreement')
    return groups, case_records


def build():
    preparation, contents, sources, coverage, status = pinned_inputs()
    environment_value = os.environ.get('LABVIEW_ENVIRONMENT')
    require(environment_value, 'LABVIEW_ENVIRONMENT is required')
    environment = Path(environment_value)
    require(environment.is_absolute() and environment.is_dir(), 'Invalid LABVIEW_ENVIRONMENT')
    artifacts, payloads, repositories = inventory(environment, sources, coverage)
    declarations, name_gaps = declared_names(artifacts, payloads)
    hashes = defaultdict(list)
    for artifact in artifacts:
        hashes[artifact['sha256']].append(artifact['id'])
    exact = [{'sha256': digest, 'members': members} for digest, members in sorted(hashes.items())]
    candidates, pair_count = group_candidates(artifacts)
    cases = {p: d for p, d in contents.items() if p.startswith('benchmark/cases/dev/')}
    groups, case_records = lineage_map(artifacts, exact, candidates, cases, repositories)
    duplicate = [g for g in exact if len(g['members']) > 1]
    counts = {'repositories': len(repositories), 'artifacts': len(artifacts),
              'originals': sum(a['archive'] is None for a in artifacts),
              'archive_members': sum(a['archive'] is not None for a in artifacts),
              'exact_hash_groups_including_singletons': len(exact),
              'exact_duplicate_groups': len(duplicate),
              'exact_duplicate_members': sum(len(g['members']) for g in duplicate),
              'candidate_groups': len(candidates), 'distinct_different_hash_candidate_pairs': pair_count,
              'candidate_groups_with_version_difference': sum('different-recorded-save-versions' in c['reasons'] for c in candidates),
              'conservative_lineage_groups': len(groups), 'development_cases': len(case_records),
              'development_lineage_ids': len({c['lineage_group_id'] for c in case_records}),
              'static_membership_declarations': len(declarations), 'static_name_gaps': len(name_gaps)}
    result = {'schema_version': 1, 'scope': 'Public development sources only; no allocation into evaluation partitions.',
              'status': 'prepared-unreviewed', 'split_milestone': status['milestones']['split'],
              'input_pins': {p: sha(d) for p, d in sorted(contents.items()) if not p.endswith('preparation-status.json')},
              'repository_commits': {n: r['commit'] for n, r in sorted(repositories.items())},
              'method': [
                  'Preflight evidence pins, manifest linkage, prepared commits/readiness, every original and indexed archive member SHA256/size, and dev identities before writing.',
                  'One location per original or archive member index; exact-copy groups partition all locations by SHA256, including singletons. Duplicate counts exclude singletons.',
                  'Candidate groups overlap: equal relative paths across repositories/archive roots, equal static XML-declared qualified names, and additional equal basenames; require different hashes or recorded save versions.',
                  'Static qualified names follow relative library/class XML Item membership URLs from the container path itself and declared names, recording zero-based Item ordinals; parent, friend and implicit private-data declarations are excluded. They are clues pending native verification, not native name assertions.',
                  'Version differences use pinned LVSR or XML root LVVersion fields within matched-name groups; vers-only metadata stays visible but is not treated as an authoritative save-version difference.',
                  'Whole-repository envelopes conservatively preserve the existing dev lineage IDs and merge cross-repository exact/candidate constraints. These are public development constraints, not adjudicated independent project lineages.',
                  'No prepared code imports, execution, archive extraction, conversion, native execution or network operations. Output is deterministic; --check recomputes and compares bytes without writing.'
              ], 'counts': counts, 'artifacts': artifacts, 'exact_copy_groups': exact,
              'candidate_variants': candidates, 'static_membership_declarations': declarations,
              'static_name_gaps': name_gaps, 'lineage_groups': groups, 'development_case_map': case_records,
              'remaining_uncertainty': [
                  'Hash inequality never establishes independence; renamed, edited, resaved and binary-internal variants can escape these name heuristics.',
                  'Equal names can be unrelated; candidate relationships remain candidate-unadjudicated and require provenance/manual/native structural review.',
                  'Static XML declarations do not prove loaded native qualified names, ownership or dependency resolution. Missing/external URLs, symbolic paths, nested archives, opaque binaries and unavailable diagrams remain unresolved.',
                  'Archive inventory scope is the pinned coverage denominator, not a claim that every possible nested container member was decoded.',
                  'All public repositories, history and derivatives remain development material; unlinked repository envelopes are not evidence of independent evaluation lineages.',
                  'Independent method review and owner acceptance remain pending; no product implementation or readiness claim.'
              ], 'missing_split_prerequisites': MISSING}
    summary = '# Public lineage preparation\n\n' + '\n'.join('- ' + k.replace('_', ' ') + ': ' + str(v) for k, v in counts.items()) + '\n\n'
    summary += ('Counts describe the [public inventory](lineage.json); candidate groups overlap and remain unadjudicated. '
                'This summary contains no case keys. Hash inequality does not establish independence.\n\n'
                + split_text(status['milestones']['split']) + ' Public inventory preparation is unreviewed. '
                'Missing: restricted store, custodian, private/new cases, native structural comparison and tested isolation. '
                'Independent method review and owner acceptance are still required; no readiness or product claim.\n\n'
                'Generate: `python3 -I benchmark/scripts/lineage.py`. '
                'Verify: `python3 -I benchmark/scripts/lineage.py --check` and '
                '`python3 -I policy/evaluator/evaluate.py --check`.\n')
    old_limitations = status['limitations']
    prefix = 'Public lineage inventory is prepared, unreviewed preparation only.'
    suffix = 'No evaluation allocation or readiness claim.'
    current = limitation(status['milestones']['split'])
    require(old_limitations.count(prefix) <= 1, 'Duplicate lineage limitation')
    if prefix in old_limitations:
        before, _, tail = old_limitations.partition(prefix)
        _, marker, after = tail.partition(suffix)
        require(marker, 'Incomplete lineage limitation')
        status['limitations'] = before + current + after
    else:
        status['limitations'] = old_limitations + ' ' + current
    outputs = {'benchmark/lineage.json': encode(result), 'benchmark/lineage.md': summary.encode(),
               'benchmark/preparation-status.json': encode(status)}
    evidence_paths = ['benchmark/scripts/lineage.py', 'benchmark/lineage.json',
                      'benchmark/lineage.md', 'benchmark/preparation-status.json']
    split = {entry['path']: entry for entry in preparation['milestones']['split']}
    for path in evidence_paths:
        data = outputs[path] if path in outputs else read_regular(ROOT, path)
        split[path] = {'path': path, 'sha256': sha(data)}
    preparation['milestones']['split'] = [split[path] for path in sorted(split)]
    for entries in preparation['milestones'].values():
        for entry in entries:
            if entry['path'] in outputs:
                entry['sha256'] = sha(outputs[entry['path']])
    outputs['benchmark/preparation.json'] = encode(preparation)
    for path, data in outputs.items():
        require(0 < len(data) <= 2_000_000, 'Evidence size limit: ' + path)
        destination = ROOT / path
        require(not destination.is_symlink() and not destination.parent.is_symlink(), 'Symlink output')
        require(not destination.exists() or destination.is_file(), 'Nonregular output')
    return outputs, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        outputs, counts = build()
        if args.check:
            for path, expected in outputs.items():
                require(read_regular(ROOT, path) == expected, 'Stale generated output: ' + path)
        else:
            # Build completes all input and output preflight before this first write.
            for path, data in outputs.items():
                (ROOT / path).write_bytes(data)
        print(json.dumps({'status': 'pass', 'mode': 'check' if args.check else 'generate', 'counts': counts}, sort_keys=True))
        return 0
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile, ET.ParseError) as error:
        print('lineage: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
