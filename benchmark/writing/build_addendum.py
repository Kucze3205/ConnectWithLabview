#!/usr/bin/env python3
"""Build or check the writing baseline addendum (whole-method review #938, row R6b).

    python3 -I -B benchmark/writing/build_addendum.py --write   # regenerate the addendum
    python3 -I -B benchmark/writing/build_addendum.py --check   # recompute every hash on disk

Everything in the addendum is derived from benchmark/writing/method.json and the pinned
original files; nothing is invented. Model, budgets, repetitions, prompt wrapper, allowed
inputs and key revision stay null with an explicit status. --check also recomputes the
original hashes under LABVIEW_ENVIRONMENT when that variable is set, and says so when not.
Design record only: no agent run, no native execution, no LabVIEW behaviour.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
METHOD = 'benchmark/writing/method.json'
ADDENDUM = 'benchmark/writing/baseline-addendum.json'
REVIEW_ROW = ('Frozen, hashed baseline addendum (prompts, output schema, ID lists, budgets) | '
              'UF (for prompts, schema, IDs, manifests) | method.json:768 `freeze`; '
              'protocol-link-0217 reports no addendum file | UF-E. Model, quota and repetition '
              'count within it are BLOCKED owner decision (method.json:769)')

PENDING = {
    'allowed_inputs_hash': ('pending-preparer-freeze', 'Allowed documentation and images are not selected or hashed.'),
    'common_prompt_hash': ('pending-preparer-freeze', 'The common prompt wrapper around each request is not authored; only the per-task requests are frozen here.'),
    'model_snapshot_and_generation': ('owner-pending', 'Model, snapshot and generation settings are an owner decision (review #938 row R6b).'),
    'total_token_budget': ('owner-pending', 'Budgets need owner quota decisions.'),
    'context_budget': ('owner-pending', 'Budgets need owner quota decisions.'),
    'output_token_and_artifact_byte_budget': ('owner-pending', 'Budgets need owner quota decisions.'),
    'wall_time_budget': ('owner-pending', 'Budgets need owner quota decisions.'),
    'ordinary_editing_capabilities': ('pending-preparer-freeze', 'method.json requires identical ordinary editing facilities in both arms but names no concrete list.'),
    'case_key_revision': ('unavailable', 'No independently established key exists; every task oracle.native_key is unavailable.'),
    'repetition_count': ('owner-pending', 'method.json#/comparison/repetitions records four conditional pilots as design only and leaves evaluation count null.'),
    'retry_policy': ('owner-pending', 'No retry policy is frozen.'),
    'arm_order_seed': ('owner-pending', 'The runner contract derives order from a seed that is not chosen for writing.'),
}
# Matched fields of method.json#/comparison that this addendum derives from method.json itself.
DERIVED = ('requested_change_hash', 'original_manifest_hash', 'native_access_policy')


def need(condition, reason):
    if not condition:
        raise SystemExit('baseline addendum: ' + reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def read(path):
    return (ROOT / path).read_bytes()


def originals_of(task):
    rows = []
    for original in task['originals']:
        if 'snapshot' in original:
            location, read_path = 'repository', original['snapshot']
            need(sha(read(read_path)) == original['sha256'], 'snapshot-hash:' + read_path)
        else:
            location, read_path = 'environment', original['path']
        rows.append({'path': original['path'], 'sha256': original['sha256'], 'role': 'original',
                     'location': location, 'read_path': read_path})
    for pin in task.get('consumer_source_pins', []):
        rows.append({'path': pin['path'], 'sha256': pin['sha256'], 'role': 'consumer-' + pin['status'],
                     'location': 'environment', 'read_path': pin['path']})
    return rows


def build():
    method_bytes = read(METHOD)
    method = json.loads(method_bytes)
    common, comparison = method['common'], method['comparison']
    tasks, requests, manifests = [], [], []
    for index, task in enumerate(method['tasks']):
        originals = originals_of(task)
        ids = {'semantic_ids': task['semantic_ids'], 'preservation_ids': task['preservation_ids'],
               'answer_ids': task['answer_ids']}
        request_hash = sha(task['request'].encode())
        requests.append([task['id'], request_hash])
        manifests.append([task['id'], originals])
        tasks.append({
            'id': task['id'], 'operation': task['operation'], 'method_locator': '/tasks/%d' % index,
            'request': {'locator': '/tasks/%d/request' % index, 'sha256': request_hash},
            'expected_semantics': {'locator': '/tasks/%d/expected_semantics' % index,
                                   'sha256': sha(canon(task['expected_semantics']))},
            **ids, 'id_lists_sha256': sha(canon(ids)),
            'output_paths': task['output_paths'],
            'output_manifest_rule_sha256': sha(task['output_manifest_rule'].encode()),
            'originals': originals,
            'workspace_manifest': {'status': 'unavailable', 'reason': 'A separate preparer/checker freezes workspace and dependency manifests before exposure (method.json#/common/preflight); no workspace or dependency tree exists.'},
            'native_outcome': task['native_outcome'],
        })
    all_ids = [i for t in tasks for k in ('semantic_ids', 'preservation_ids', 'answer_ids') for i in t[k]]
    need(len(all_ids) == len(set(all_ids)), 'duplicate-required-id')
    need(set(comparison['matched_fields']) == set(DERIVED) | (set(PENDING) - {'arm_order_seed'}),
         'matched-field-coverage')
    return {
        'schema_version': 1,
        'kind': 'writing-baseline-addendum',
        'status': 'draft-unreviewed; not accepted or frozen by the owner; no run executed',
        'requirement': {
            'review': '#938', 'row': 'R6b', 'row_text': REVIEW_ROW,
            'staged_line': '.session/inputs/938-method-review-0220.md:42',
            'method_rule_locator': '/comparison/freeze',
            'method_rule_sha256': sha(comparison['freeze'].encode()),
        },
        'method': {'path': METHOD, 'sha256': sha(method_bytes), 'revision': method['revision']},
        'arms': {
            'matched_fields': comparison['matched_fields'],
            'no-tool': {'definition': 'Same ordinary file editing facilities and inputs as the tool arm; no evaluated tool and no substitute semantic writer or exporter.',
                        'source_locator': '/comparison/tool_difference'},
            'tool': {'definition': 'Evaluated tool access and its minimal instruction are the only difference; tool output, time and cost count against the shared totals.',
                     'source_locator': '/comparison/tool_difference'},
            'tool_difference_sha256': sha(comparison['tool_difference'].encode()),
            'native_access_policy_sha256': sha(comparison['native_access_policy'].encode()),
        },
        'tasks': tasks,
        'output_schema': {
            'source_locator': '/common',
            'artifact_record': common['artifact_record'], 'dimensions': common['dimensions'],
            'outcomes': common['outcomes'], 'limitation_codes': common['limitation_codes'],
            'sha256': sha(canon([common['artifact_record'], common['dimensions'],
                                 common['outcomes'], common['limitation_codes']])),
        },
        'id_lists': {'count': len(all_ids), 'unique': True,
                     'sha256': sha(canon([[t['id'], t['id_lists_sha256']] for t in tasks]))},
        'derived_matched_fields': {
            'requested_change_hash': sha(canon(requests)),
            'original_manifest_hash': sha(canon(manifests)),
            'native_access_policy': comparison['native_access_policy'],
        },
        'owner_pending': {name: {'value': None, 'status': status, 'reason': reason}
                          for name, (status, reason) in PENDING.items()},
        'limits': {'agent_runs': 0, 'native_executions': 0, 'benchmark_ready': False,
                   'meaning': 'Draft baseline definition for review. It claims no LabVIEW behaviour and supplies no model, budget or repetition choice.'},
    }


def serialize(document):
    return (json.dumps(document, indent=2, ensure_ascii=False) + '\n').encode()


def check():
    actual = read(ADDENDUM)
    need(actual == serialize(build()), 'addendum-differs-from-recomputed-build')
    document = json.loads(actual)
    need(all(row['value'] is None for row in document['owner_pending'].values()), 'invented-pending-value')
    environment = os.environ.get('LABVIEW_ENVIRONMENT')
    repository_checked = environment_checked = 0
    for task in document['tasks']:
        for original in task['originals']:
            if original['location'] == 'repository':
                need(sha(read(original['read_path'])) == original['sha256'], 'original-drift:' + original['path'])
                repository_checked += 1
            elif environment:
                need(sha((Path(environment) / original['read_path']).read_bytes()) == original['sha256'],
                     'original-drift:' + original['path'])
                environment_checked += 1
    print(json.dumps({'status': 'addendum-consistent', 'addendum_sha256': sha(actual),
                      'method_sha256': document['method']['sha256'], 'tasks': len(document['tasks']),
                      'required_ids': document['id_lists']['count'],
                      'originals_repository_checked': repository_checked,
                      'originals_environment_checked': environment_checked,
                      'environment': 'checked' if environment else 'LABVIEW_ENVIRONMENT unset; environment originals not rechecked',
                      'owner_pending_fields': len(document['owner_pending'])}, sort_keys=True))


def main():
    need(len(sys.argv) == 2 and sys.argv[1] in ('--write', '--check'), 'usage: --write | --check')
    if sys.argv[1] == '--write':
        (ROOT / ADDENDUM).write_bytes(serialize(build()))
    check()


if __name__ == '__main__':
    main()
