#!/usr/bin/env python3
"""Synthetic whole-group allocation; no cases, keys, store access or readiness claim.

Enumerate whole-group assignments and maximize fulfilled requested family strata.
Ties use SHA256(seed, sorted group assignments), avoiding input-order dependence.
The exhaustive design is deliberately bounded to 10 groups; scaling and allocation
priorities need later review before adapting this to a custodian's private inputs.
"""
import argparse
from copy import deepcopy
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SYNTHETIC = ROOT / 'benchmark/split/allocation.synthetic.json'
TEMPLATE = ROOT / 'benchmark/split/allocation-manifest.template.json'
PARTITIONS = ('development', 'eval-unseen-lineage', 'eval-held-out-family')
INFEASIBLE_REASON = 'whole-group constraints prevent jointly fulfilling this requested stratum'


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def unique(items, key, reason):
    require(len({item[key] for item in items}) == len(items), reason)


def inventory(data):
    require(data['schema_version'] == 1 and data['synthetic_only'] is True,
            'synthetic schema required')
    require(type(data['seed']) is int, 'integer seed required')
    families, projects, groups = (data[k] for k in ('families', 'projects', 'lineage_groups'))
    require(0 < len(groups) <= 10, 'synthetic exhaustive allocator requires 1 to 10 groups')
    unique(families, 'family_id', 'duplicate family id')
    unique(projects, 'project_id', 'duplicate project id')
    unique(groups, 'lineage_group_id', 'duplicate group id')
    for rows, key, prefix in ((families, 'family_id', 'F'), (projects, 'project_id', 'P'),
                              (groups, 'lineage_group_id', 'G')):
        require(rows and all(re.fullmatch('SYN-' + prefix + r'[1-9][0-9]*', r[key]) for r in rows),
                'synthetic identifiers required')
    require(re.fullmatch(r'SYN-SPLIT-[1-9][0-9]*', data['split_revision']) is not None,
            'synthetic split revision required')
    requests = {f['family_id']: f['requested_stratum'] for f in families}
    require(all(s in PARTITIONS[1:] for s in requests.values()), 'unknown requested stratum')
    project_map = {p['project_id']: p for p in projects}
    for project in projects:
        fs = project['family_ids']
        require(fs and len(fs) == len(set(fs)) and set(fs) <= set(requests),
                'invalid project families')
    owners = []
    group_map, group_families = {}, {}
    for group in groups:
        gid, ps = group['lineage_group_id'], group['project_ids']
        require(type(group['required_development']) is bool, 'development anchor must be boolean')
        require(ps and len(ps) == len(set(ps)) and set(ps) <= set(project_map),
                'invalid group projects')
        owners.extend(ps)
        group_map[gid] = group
        group_families[gid] = set().union(*(set(project_map[p]['family_ids']) for p in ps))
    require(len(owners) == len(set(owners)) and set(owners) == set(project_map),
            'each whole project must belong to exactly one group')
    require(set().union(*group_families.values()) == set(requests), 'family without projects')
    family_groups = {f: {g for g, fs in group_families.items() if f in fs} for f in requests}
    return requests, group_map, group_families, family_groups


def constraint_reason(assignment, requests, groups, group_families, family_groups):
    for gid in sorted(groups):
        if groups[gid]['required_development'] and assignment[gid] != 'development':
            return 'required development group moved: ' + gid
    for family in sorted(requests):
        partitions = {assignment[g] for g in family_groups[family]}
        if 'eval-held-out-family' in partitions:
            if 'development' in partitions:
                return 'held-out family member in development: ' + family
            if partitions != {'eval-held-out-family'}:
                return 'held-out family crosses evaluation strata: ' + family
            if requests[family] != 'eval-held-out-family':
                return 'unrequested held-out family: ' + family
    for gid in sorted(groups):
        if assignment[gid] == 'eval-unseen-lineage':
            for family in sorted(group_families[gid]):
                if not any(assignment[g] == 'development' for g in family_groups[family]):
                    return 'unseen family absent from development: ' + family
    return None


def fulfilled(assignment, requests, family_groups):
    result = set()
    for family, stratum in requests.items():
        partitions = {assignment[g] for g in family_groups[family]}
        if stratum == 'eval-held-out-family':
            if partitions == {stratum}:
                result.add(family)
        elif 'development' in partitions and stratum in partitions:
            result.add(family)
    return result


def plan(data):
    requests, groups, group_families, family_groups = inventory(data)
    gids = sorted(groups)
    best, best_rank = None, None
    for partitions in itertools.product(PARTITIONS, repeat=len(gids)):
        assignment = dict(zip(gids, partitions))
        if constraint_reason(assignment, requests, groups, group_families, family_groups):
            continue
        satisfied = fulfilled(assignment, requests, family_groups)
        tie = sha(json.dumps([data['seed'], sorted(assignment.items())], separators=(',', ':')))
        rank = (-len(satisfied), tie)
        if best_rank is None or rank < best_rank:
            best, best_rank = assignment, rank
    require(best is not None, 'no legal whole-group allocation')
    satisfied = fulfilled(best, requests, family_groups)
    infeasible = [{'family_id': f, 'stratum': requests[f], 'reason': INFEASIBLE_REASON}
                  for f in sorted(requests) if f not in satisfied]
    return best, infeasible


def build(data):
    assignment, infeasible = plan(data)
    _, groups, _, _ = inventory(data)
    records = []
    for gid in sorted(groups):
        records.append({
            'split_revision': data['split_revision'],
            'lineage_group_id': gid,
            'partition': assignment[gid],
            'group_member_hashes': [sha('SYNTHETIC project ' + p)
                                    for p in sorted(groups[gid]['project_ids'])],
            'adjudication_notes': 'Synthetic pre-adjudicated connected group; no real lineage assertion.',
            'key_revision_hashes': None,
            'access_configuration_hash': None,
            'custodian_label': 'SYN-CUSTODIAN',
        })
    return {'schema_version': 1, 'synthetic_only': True, 'seed': data['seed'],
            'allocation_method': 'maximize fulfilled family requests; SHA256 seeded tie break',
            'lineage_groups': {'records': records}, 'infeasible_strata': infeasible}


def validate(result, data, template):
    requests, groups, group_families, family_groups = inventory(data)
    require(result['schema_version'] == template['schema_version'], 'manifest schema version')
    require(result['synthetic_only'] is True and result['seed'] == data['seed'],
            'synthetic seed mismatch')
    records = result['lineage_groups']['records']
    assignment = {}
    for record in records:
        require(set(record) == set(template['fields']), 'manifest field names differ from template')
        gid, partition = record['lineage_group_id'], record['partition']
        require(partition in PARTITIONS, 'unknown partition: ' + str(partition))
        require(gid in groups, 'unknown group id: ' + str(gid))
        if gid in assignment:
            require(assignment[gid] == partition, 'group split across partitions: ' + gid)
            raise ValueError('duplicate group id: ' + gid)
        assignment[gid] = partition
        require(record['split_revision'] == data['split_revision'], 'split revision mismatch')
        require(record['group_member_hashes'] == [sha('SYNTHETIC project ' + p)
                    for p in sorted(groups[gid]['project_ids'])], 'whole-group member hashes mismatch')
        require(record['key_revision_hashes'] is None and record['access_configuration_hash'] is None,
                'synthetic key and access fields must remain null')
        require(record['custodian_label'] == 'SYN-CUSTODIAN' and
                record['adjudication_notes'] ==
                'Synthetic pre-adjudicated connected group; no real lineage assertion.',
                'synthetic custodian and adjudication required')
    require(set(assignment) == set(groups), 'missing lineage group')
    reason = constraint_reason(assignment, requests, groups, group_families, family_groups)
    require(reason is None, reason)
    satisfied = fulfilled(assignment, requests, family_groups)
    expected = [{'family_id': f, 'stratum': requests[f], 'reason': INFEASIBLE_REASON}
                for f in sorted(requests) if f not in satisfied]
    require(result['infeasible_strata'] == expected, 'infeasible stratum silently dropped or changed')
    optimum, _ = plan(data)
    require(len(satisfied) == len(fulfilled(optimum, requests, family_groups)),
            'allocation needlessly forfeits a requested stratum')


def expect_reject(name, reason, action):
    try:
        action()
    except ValueError as exc:
        require(str(exc) == reason, '%s: unexpected reason: %s' % (name, exc))
        return {'mutation': name, 'result': 'rejected', 'reason': str(exc)}
    raise ValueError(name + ': mutation accepted')


def check():
    data = json.loads(SYNTHETIC.read_text())
    template = json.loads(TEMPLATE.read_text())
    result = build(data)
    validate(result, data, template)
    require(result == build(deepcopy(data)), 'allocation is not deterministic')
    reordered = deepcopy(data)
    for key in ('families', 'projects', 'lineage_groups'):
        reordered[key].reverse()
    for group in reordered['lineage_groups']:
        group['project_ids'].reverse()
    require(result == build(reordered), 'allocation depends on input order')
    records = result['lineage_groups']['records']
    by_id = {r['lineage_group_id']: r for r in records}
    # Independent fixture expectations: two F2-only groups can be held out; the
    # F1/F3 development anchor prevents F3 holdout; F1 has two other groups.
    require(by_id['SYN-G1']['partition'] == 'development', 'mixed-family anchor changed')
    require(all(by_id[g]['partition'] == 'eval-held-out-family' for g in ('SYN-G3', 'SYN-G4')),
            'feasible whole-family holdout missing')
    require(any(by_id[g]['partition'] == 'eval-unseen-lineage' for g in ('SYN-G2', 'SYN-G5')),
            'feasible unseen lineage missing')
    require(result['infeasible_strata'] == [{'family_id': 'SYN-F3',
            'stratum': 'eval-held-out-family', 'reason': INFEASIBLE_REASON}],
            'expected mixed-family infeasibility missing')

    def actual_reason():
        raise ValueError('actual reason')

    try:
        expect_reject('reason comparison self-test', 'expected reason', actual_reason)
    except ValueError as exc:
        require(str(exc) == 'reason comparison self-test: unexpected reason: actual reason',
                'reason comparison self-test: wrong mismatch error')
    else:
        raise ValueError('reason comparison self-test: mismatch accepted')

    mutations = []

    def mutation(name, reason, change):
        altered = deepcopy(result)
        change(altered)
        mutations.append(expect_reject(name, reason, lambda: validate(altered, data, template)))

    def split_group(r):
        extra = deepcopy(r['lineage_groups']['records'][0])
        extra['partition'] = 'eval-unseen-lineage'
        r['lineage_groups']['records'].append(extra)

    def holdout_leak(r):
        next(x for x in r['lineage_groups']['records']
             if x['lineage_group_id'] == 'SYN-G3')['partition'] = 'development'

    mutation('group split across partitions', 'group split across partitions: SYN-G1', split_group)
    mutation('held-out family member in development',
             'held-out family member in development: SYN-F2', holdout_leak)
    mutation('unknown partition', 'unknown partition: SYN-UNKNOWN',
             lambda r: r['lineage_groups']['records'][0].update(partition='SYN-UNKNOWN'))
    mutation('duplicate group id', 'duplicate group id: SYN-G1',
             lambda r: r['lineage_groups']['records'].append(deepcopy(r['lineage_groups']['records'][0])))
    mutation('infeasible stratum silently dropped', 'infeasible stratum silently dropped or changed',
             lambda r: r.update(infeasible_strata=[]))
    mutation('manifest field removed', 'manifest field names differ from template',
             lambda r: r['lineage_groups']['records'][0].pop('custodian_label'))
    altered_data = deepcopy(data)
    altered_data['lineage_groups'].append(deepcopy(altered_data['lineage_groups'][0]))
    mutations.append(expect_reject('duplicate input group id', 'duplicate group id',
                                  lambda: build(altered_data)))

    counts = {p: {'lineage_groups': 0, 'projects': 0} for p in PARTITIONS}
    _, groups, _, _ = inventory(data)
    for record in records:
        count = counts[record['partition']]
        count['lineage_groups'] += 1
        count['projects'] += len(groups[record['lineage_group_id']]['project_ids'])
    print(json.dumps({'status': 'pass', 'synthetic_only': True, 'benchmark_ready': False,
                      'seed': data['seed'], 'allocation_method': result['allocation_method'],
                      'partition_counts': counts,
                      'allocations': {r['lineage_group_id']: r['partition'] for r in records},
                      'infeasible_strata': result['infeasible_strata'],
                      'mutation_count': len(mutations), 'mutations': mutations,
                      'undecided_fields': ['key_revision_hashes', 'access_configuration_hash'],
                      'later_review': ['stratum size minimums and allocation priorities',
                                       'scale beyond 10 pre-adjudicated connected groups',
                                       'private input adapter and independent lineage review']}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    try:
        check()
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
        print('split allocation check failed: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
