#!/usr/bin/env python3
"""Read-only stdlib check of the bounded failure delivery, not POC success.

Schema v1 is enforced below. Paths are relative to this directory. The session
original is a provenance string only: never opened, needed or executed here.
No environment, network, .session report, original VI or LabVIEW is required.
"""
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import os

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
INVENTORY_SHA256 = 'df6f13b787c828bb9f0f28a816d60f9f51523e274accf10172f4f9f62ab4f6b0'
ORIGINAL_SHA256 = 'cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8'
REVISION = '35d2a0318f71dcb87bb9c431dc00700ee6b9fb75'
LIMIT = 'Passing validates failure-delivery consistency only.'
CONTEXT = set(['../../../goal/goal.md', '../../../journal/working-memory.md', '../../perpetua/roles.md', '../../perpetua/evaluation.md', '../../../benchmark/preparation-status.json'])
STATUSES = {
    'concept_feasibility': 'unestablished',
    'poc_before_further_benchmark': 'established',
    'fresh_agent': 'not_attempted', 'semantic_description': 'unestablished',
    'logic_edit_without_labview': 'not_attempted',
    'opens_without_broken_arrow': 'not_attempted',
    'requested_behavior': 'not_attempted', 'preserved_save_version': 'unestablished',
    'files_report_owner_instructions': 'established',
    'failure_evidence_and_exits': 'established',
    'separate_from_product_quality': 'established',
    'continue_without_owner_wait': 'established', 'silence_not_acceptance': 'established',
}
TOP = {'schema_version', 'outcome', 'goal_source', 'scope', 'original', 'criteria',
       'blockers', 'exits', 'reproduction', 'owner_checks', 'resume', 'context_gaps',
       'evidence', 'delivery_md_sha256'}
NEW = {'delivery.md', 'delivery.json', 'delivery-verification.json', 'verify_delivery.py'}

class DeliveryError(ValueError):
    pass

def need(condition, message):
    if not condition:
        raise DeliveryError(message)

def shape(value, keys, label):
    need(isinstance(value, dict) and set(value) == set(keys), label + ' schema')

def text(value):
    return isinstance(value, str) and bool(value.strip())

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def local(name):
    need(text(name) and not Path(name).is_absolute(), 'invalid evidence path')
    path = (BASE / name).resolve()
    need(path.is_relative_to(ROOT) and '.session' not in path.relative_to(ROOT).parts,
         'evidence path escapes repository or requires session data')
    need(path.is_file(), 'missing evidence: ' + name)
    return path

def read(name):
    return json.loads(local(name).read_text())

def validate(d):
    shape(d, TOP, 'delivery')
    need(type(d['schema_version']) is int and d['schema_version'] == 1, 'schema version')
    need(d['outcome'] == 'unsuccessful', 'failure outcome required')
    need(d['goal_source'] == '../../../goal/goal.md#proof-of-concept', 'goal source')
    need(d['scope'] == {
        'selected_originals': 8, 'changed_vi_produced': False,
        'fresh_agent_edit_demonstration_produced': False, 'labview_run': False,
        'semantic_diagram_description_established': False,
        'structural_parsing_established': True, 'general_impossibility_claim': False,
        'product_or_benchmark_changes': False}, 'scope contradicts bounded evidence')
    need(all(type(v) is bool for k, v in d['scope'].items() if k != 'selected_originals')
         and type(d['scope']['selected_originals']) is int, 'scope field types')
    inventory = d['evidence']
    need(isinstance(inventory, list) and inventory, 'evidence inventory')
    canonical = json.dumps(inventory, sort_keys=True, separators=(',', ':')).encode()
    need(digest(canonical) == INVENTORY_SHA256, 'pinned baseline inventory changed')
    names = set()
    for item in inventory:
        shape(item, {'path', 'bytes', 'sha256'}, 'evidence')
        name = item['path']
        need(text(name) and name not in names, 'duplicate evidence path')
        names.add(name)
        raw = local(name).read_bytes()
        need(type(item['bytes']) is int and len(raw) == item['bytes']
             and digest(raw) == item['sha256'], 'pinned evidence changed: ' + name)
    def refs(values):
        need(isinstance(values, list) and values and all(text(v) for v in values), 'citation list')
        for value in values:
            need(value in names | NEW | CONTEXT, 'uninventoried citation: ' + value)
            local(value)
    refs(['inspect_vi.py', 'heap-labels.json', 'README.md', 'edit-readiness.md',
          'edit-readiness.json', 'verify_edit_readiness.py', 'verify_poc.py',
          'source-provenance.json', 'step3/source-provenance.json',
          'pylabview-LICENSE.txt', 'step3/pylavi-LICENSE.txt'])
    original = d['original']
    shape(original, {'prepared_path', 'command_path', 'upstream_path', 'revision', 'url',
          'license', 'license_file', 'bytes', 'sha256', 'declared_save_version_hex',
          'declared_save_version', 'save_version_evidence', 'artifact',
          'artifact_status', 'copy_check'}, 'original')
    need(original == {
        'prepared_path': '@environment/pylavi/tests/add.vi',
        'command_path': '$LABVIEW_ENVIRONMENT/pylavi/tests/add.vi',
        'upstream_path': 'tests/add.vi', 'revision': REVISION,
        'url': 'https://github.com/marcpage/pylavi/blob/' + REVISION + '/tests/add.vi',
        'license': 'Unlicense', 'license_file': 'step3/pylavi-LICENSE.txt',
        'bytes': 6371, 'sha256': ORIGINAL_SHA256,
        'declared_save_version_hex': '21008000',
        'declared_save_version': '21.0.0 final build 0',
        'save_version_evidence': 'README.md',
        'artifact': '.session/artifacts/poc-original.vi',
        'artifact_status': 'copied_unchanged', 'copy_check': 'delivery-verification.json'},
        'original provenance or copy claim changed')
    criteria = d['criteria']
    shape(criteria, STATUSES, 'goal criterion coverage')
    for name, status in STATUSES.items():
        value = criteria[name]
        shape(value, {'status', 'finding', 'evidence'}, 'criterion ' + name)
        need(value['status'] == status and text(value['finding']), 'criterion status: ' + name)
        refs(value['evidence'])
    need('add.tree.txt' in criteria['semantic_description']['evidence']
         and 'verification.json' in criteria['semantic_description']['evidence'], 'structural evidence')
    need('candidate-change.json' in criteria['logic_edit_without_labview']['evidence']
         and 'edit-readiness.json' in criteria['logic_edit_without_labview']['evidence'], 'edit evidence')
    readiness = read('edit-readiness.json')
    need(readiness['verdict'] == 'partial' and readiness['recipe'] is None
         and readiness['scope']['edited_vi'] is False
         and readiness['scope']['behavior_claim'] is False, 'negative readiness changed')
    candidate = read('candidate-change.json')
    need(candidate['vi_written'] is False and candidate['LabVIEW_tested'] is False,
         'candidate is not a VI or runtime demonstration')
    shape(d['blockers'], {'semantics', 'encoding', 'integrity', 'compiled_cache'}, 'blockers')
    for key, value in d['blockers'].items():
        shape(value, {'finding', 'evidence'}, 'blocker ' + key)
        need(value == {k: readiness['requirements'][key][k] for k in value},
             'blocker differs from pinned readiness: ' + key)
        refs(value['evidence'])
    exits = d['exits']
    need(isinstance(exits, list) and len(exits) == 2, 'two concrete exits required')
    need({x['id'] for x in exits} == {'controlled_same_version_fixtures', 'missing_pinned_source_rules'}, 'exit coverage')
    for value in exits:
        shape(value, {'id', 'action', 'resolves', 'does_not_prove', 'evidence'}, 'exit')
        need(all(text(value[k]) for k in ('action', 'resolves', 'does_not_prove')), 'exit limits')
        refs(value['evidence'])
    reproduction = d['reproduction']
    shape(reproduction, {'inspector_argv', 'offline_argv', 'readiness_argv', 'evidence', 'offline_limit'}, 'reproduction')
    for key, script in [('inspector_argv', 'inspect_vi.py'), ('offline_argv', 'verify_delivery.py'), ('readiness_argv', 'verify_edit_readiness.py')]:
        expected = ['python3', '-I', 'docs/research/poc/' + script]
        if key == 'inspector_argv':
            expected.append(original['artifact'])
        need(reproduction[key] == expected, 'reproduction argv: ' + key)
    need(reproduction['offline_limit'] == LIMIT, 'verification limit')
    refs(reproduction['evidence'])
    owner = d['owner_checks']
    shape(owner, {'original_only', 'limitation', 'future_changed_vi_checks', 'status'}, 'owner checks')
    need(text(owner['original_only']) and 'none exists' in owner['limitation']
         and owner['status'] == 'outstanding', 'owner check limitations')
    need(owner['future_changed_vi_checks'] == ['No broken arrow', 'Requested behavior', 'Preserved save version and runtime validity'], 'future runtime checks')
    resume = d['resume']
    shape(resume, {'action', 'read_first', 'avoid', 'silence_is_acceptance'}, 'resume')
    need(text(resume['action']) and 'benchmark preparation' in resume['action']
         and 'without waiting' in resume['action'] and text(resume['avoid'])
         and resume['silence_is_acceptance'] is False, 'resume contract')
    refs(resume['read_first'])
    need({'../../perpetua/roles.md', '../../perpetua/evaluation.md',
          '../../../benchmark/preparation-status.json', '../../../journal/working-memory.md'}
         <= set(resume['read_first']), 'readiness/role and paused-thread pointers')
    need(isinstance(d['context_gaps'], list) and len(d['context_gaps']) == 2
         and all(map(text, d['context_gaps'])), 'missing state disclosure')
    md = local('delivery.md').read_bytes()
    need(digest(md) == d['delivery_md_sha256'], 'delivery prose hash mismatch')
    prose = md.decode()
    targets = re.findall(r'\]\(([^)]+)\)', prose)
    session_link = '../../../.session/artifacts/poc-original.vi'
    for target in targets:
        if target.startswith('https://'):
            continue
        name = target.split('#')[0]
        if name == session_link:
            continue  # Intentional session-only artifact reference; do not stat it.
        refs([name])
    for required in ['delivery.json', 'edit-readiness.md', 'edit-readiness.json',
                     'inspect_vi.py', 'heap-labels.json', 'source-provenance.json',
                     'step3/source-provenance.json', 'pylabview-LICENSE.txt',
                     'step3/pylavi-LICENSE.txt', 'delivery-verification.json', session_link]:
        need(required in {t.split('#')[0] for t in targets}, 'required delivery link: ' + required)
    need('cannot validate a changed VI because none exists' in prose
         and 'structural' in prose and 'semantic' in prose
         and 'No changed VI and no fresh-agent edit demonstration were produced' in prose,
         'essential delivery limitations missing')
    record = read('delivery-verification.json')
    shape(record, {'schema_version', 'original_copy_check', 'offline_check', 'inspector_reproduction', 'limitations'}, 'verification record')
    offline = record['offline_check']
    need(offline['status'] == 'pass' and offline['returncode'] == 0
         and offline['argv'] == reproduction['offline_argv']
         and offline['LABVIEW_ENVIRONMENT'] == 'unset'
         and offline['dependency_guard']['status'] == 'pass'
         and offline['dependency_guard']['same_stdout'] is True,
         'recorded offline check inconsistent')
    lines = offline['stdout'].splitlines()
    need(len(lines) == 2 and lines[1] == LIMIT, 'recorded verification limitation')
    saved = json.loads(lines[0])
    need(saved['status'] == 'pass' and saved['outcome'] == 'unsuccessful'
         and saved['criteria'] == len(criteria) and saved['pinned_files'] == len(inventory)
         and saved['exits'] == 2 and saved['negative_checks'] == 9
         and saved['original_rehashed_offline'] is False
         and saved['session_artifacts_required'] is False
         and saved['readiness_verifier'] == 'pass', 'recorded offline result')
    inspection = record['inspector_reproduction']
    need(inspection['status'] == 'pass' and inspection['returncode'] == 0
         and inspection['argv'] == reproduction['inspector_argv']
         and re.fullmatch('[0-9a-f]{64}', inspection['stdout_sha256']) is not None
         and inspection['stdout_bytes'] > 0 and inspection['stderr'] == '',
         'recorded original inspector reproduction')
    check = record['original_copy_check']
    need(record['schema_version'] == 1 and check['status'] == 'pass'
         and check['artifact'] == original['artifact'] and check['byte_identical'] is True
         and check['source_sha256'] == check['artifact_sha256'] == ORIGINAL_SHA256
         and check['source_bytes'] == check['artifact_bytes'] == 6371
         and check['prepared_path'] == original['prepared_path'] and text(check['method']),
         'recorded session copy check inconsistent')
    return {'status': 'pass', 'outcome': d['outcome'], 'criteria': len(criteria),
            'pinned_files': len(inventory), 'exits': len(exits)}

def main():
    document = read('delivery.json')
    result = validate(document)
    mutations = [
        ('success claim', lambda d: d.update(outcome='successful')),
        ('missing criterion', lambda d: d['criteria'].pop('fresh_agent')),
        ('semantic success', lambda d: d['criteria']['semantic_description'].update(status='established')),
        ('changed VI claim', lambda d: d['scope'].update(changed_vi_produced=True)),
        ('missing citation', lambda d: d['blockers']['integrity'].update(evidence=['missing.txt'])),
        ('corrupt pinned inventory', lambda d: d['evidence'][0].update(sha256='0' * 64)),
        ('missing exit', lambda d: d['exits'].pop()),
        ('wrong original hash', lambda d: d['original'].update(sha256='0' * 64)),
        ('owner silence accepted', lambda d: d['resume'].update(silence_is_acceptance=True)),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(document)
        mutate(candidate)
        try:
            validate(candidate)
        except (DeliveryError, KeyError, TypeError, ValueError):
            continue
        raise DeliveryError('negative self-check accepted: ' + name)
    # Execute only the pinned read-only verifier. verify_poc.py rewrites evidence.
    env = dict(os.environ)
    env.pop('LABVIEW_ENVIRONMENT', None)
    completed = subprocess.run([sys.executable, '-I', str(local('verify_edit_readiness.py'))],
                               env=env, capture_output=True, text=True, check=False)
    need(completed.returncode == 0, 'pinned readiness verifier failed: ' + completed.stderr.strip())
    readiness_result = json.loads(completed.stdout)
    need(readiness_result['status'] == 'pass' and readiness_result['verdict'] == 'partial', 'readiness result')
    result.update(negative_checks=len(mutations), readiness_verifier='pass',
                  original_rehashed_offline=False, session_artifacts_required=False)
    print(json.dumps(result, sort_keys=True))
    print(LIMIT)
    return result

if __name__ == '__main__':
    try:
        main()
    except (DeliveryError, OSError, KeyError, TypeError, ValueError) as exc:
        print('delivery: FAIL: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
