#!/usr/bin/env python3
"""Synthetic runner-contract check only: no runner, model calls, real cases or scoring.

Validates the synthetic populated manifest against the manifest template, plans
cases x arms x repetitions deterministically, builds one synthetic record per
planned run in memory and audits the set with run_record.py validate/bind_manifest.
Fields needing owner or resource decisions stay null in the manifest.
"""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / 'benchmark/baseline'
TEMPLATE = BASELINE / 'run-manifest.template.json'
SYNTHETIC = BASELINE / 'run-manifest.synthetic.json'
RECORD_TEMPLATE = BASELINE / 'run-record.template.json'


def load_run_record():
    spec = importlib.util.spec_from_file_location('run_record', ROOT / 'benchmark/scripts/run_record.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RR = load_run_record()
require = RR.require

CASES = ('synthetic:case-a', 'synthetic:case-b', 'synthetic:case-c')
ARMS = ('no-tool', 'tool')
REPETITIONS = 2
SEED = 20000101
PROMPT = 'SYNTHETIC common prompt; no model call.'
MODEL = 'synthetic:provider/model/snapshot'
CLAIM_ANSWER = 'SYNTHETIC answer; no artifact fact asserted.'


def slug(case):
    return case.split(':', 1)[1]


def artifact_hash(case):
    return RR.sha('SYNTHETIC original artifact ' + slug(case))


def synthetic_values():
    return {
        'provider': 'synthetic:provider',
        'exact_model_snapshot': MODEL,
        'common_prompt_and_hash': {'text': PROMPT, 'sha256': RR.sha(PROMPT)},
        'question_input_hashes': {c: RR.sha('SYNTHETIC question ' + slug(c)) for c in CASES},
        'original_artifact_set_and_hashes': {c: artifact_hash(c) for c in CASES},
        'arm_specific_tool_instructions': {'no-tool': 'SYNTHETIC none', 'tool': 'SYNTHETIC use reader'},
        'runner_version': 'synthetic:runner-0',
        'scorer_version': 'synthetic:scorer-0',
        'split_revision': 'synthetic:split-0',
        'case_key_revision': 'synthetic:keys-0',
        'matched_total_token_budget': {'max_total_tokens': 1000},
        'matched_context_budget': {'max_context_tokens': 800},
        'matched_output_budget': {'max_output_tokens': 500},
        'matched_wall_time_budget': {'max_wall_ms': 60000},
        'tool_call_limits_and_accounting': {'max_tool_calls': 5},
        'independent_repetitions_per_case_arm': REPETITIONS,
        'sampling_order': 'case-major, repetition, arm order by sha256(seed:pair_id:arm)',
        'paired_arm_randomization': {'arms': list(ARMS), 'seed': SEED},
        'stopping_rule': 'SYNTHETIC fixed plan, run every planned run',
    }


def build_manifest_text():
    template = RR.parse(TEMPLATE.read_text())
    values = synthetic_values()
    require(set(values) <= set(template['fields']), 'synthetic value for unknown manifest field')
    fields = {}
    for name, item in template['fields'].items():
        if name in values:
            fields[name] = {'value': values[name], 'provenance': 'synthetic'}
        else:
            fields[name] = {'value': None, 'reason': item['reason']}
    return json.dumps({'schema_version': 1, 'fields': fields}, indent=2) + '\n'


def validate_manifest(manifest, template):
    require(isinstance(manifest, dict) and set(manifest) == {'schema_version', 'fields'},
            'manifest: top-level fields')
    require(manifest['schema_version'] == template['schema_version'], 'manifest: schema version')
    require(set(manifest['fields']) == set(template['fields']),
            'manifest field names differ from template')
    for name, item in manifest['fields'].items():
        if item.get('value') is None:
            require(item == {'value': None, 'reason': template['fields'][name]['reason']},
                    name + ': null field must keep the template reason')
        else:
            require(item.get('provenance') == 'synthetic' and set(item) == {'value', 'provenance'},
                    name + ': synthetic provenance required')
    val = {k: v['value'] for k, v in manifest['fields'].items()}
    cases = val['question_input_hashes']
    require(isinstance(cases, dict) and cases and all(RR.is_hash(h) for h in cases.values()),
            'question_input_hashes: case hashes required')
    require(set(val['original_artifact_set_and_hashes']) == set(cases), 'artifact set does not match cases')
    prompt = val['common_prompt_and_hash']
    require(RR.sha(prompt['text']) == prompt['sha256'], 'common prompt hash mismatch')
    arms = val['paired_arm_randomization']['arms']
    require(sorted(arms) == sorted(ARMS), 'arms must be no-tool and tool')
    require(type(val['independent_repetitions_per_case_arm']) is int
            and val['independent_repetitions_per_case_arm'] >= 1, 'repetitions must be a positive integer')


def plan_runs(manifest, manifest_bytes):
    val = {k: v['value'] for k, v in manifest['fields'].items()}
    cases = sorted(val['question_input_hashes'])
    arms, seed = val['paired_arm_randomization']['arms'], val['paired_arm_randomization']['seed']
    runs = []
    for case in cases:
        for rep in range(1, val['independent_repetitions_per_case_arm'] + 1):
            pair = 'synthetic:pair-%s-%d' % (slug(case), rep)
            for arm in sorted(arms, key=lambda a: RR.sha('%s:%s:%s' % (seed, pair, a))):
                tag = '%s-%s-%d' % (slug(case), arm, rep)
                runs.append({'index': len(runs), 'case_id': case, 'arm': arm, 'repetition': rep,
                             'pair_id': pair, 'repetition_id': 'synthetic:rep-' + tag,
                             'record_id': 'synthetic:record-' + tag})
    return {'manifest_sha256': RR.hashlib.sha256(manifest_bytes).hexdigest(), 'cases': cases,
            'runs': runs, 'plan_sha256': RR.sha(json.dumps(runs, sort_keys=True))}


def build_record(run, manifest, manifest_bytes):
    val = {k: v['value'] for k, v in manifest['fields'].items()}
    record = RR.parse(RECORD_TEMPLATE.read_text())
    f = record['fields']
    case, arm = run['case_id'], run['arm']
    request = 'SYNTHETIC full request; %s; %s' % (arm, run['repetition_id'])
    claim = {'claim_id': 'synthetic:claim-1', 'answer': CLAIM_ANSWER,
             'conditions': ['synthetic:condition'],
             'citations': [{'artifact_sha256': val['original_artifact_set_and_hashes'][case],
                            'locator': {'expression': 'synthetic:original/object/property'}}]}
    limitations = ['SYNTHETIC design fixture only.']
    response = json.dumps({'status': 'complete', 'claims': [claim], 'limitations': limitations},
                          sort_keys=True)
    values = {
        'record_id': run['record_id'], 'case_id': case, 'pair_id': run['pair_id'], 'arm': arm,
        'repetition_id': run['repetition_id'],
        'manifest_sha256': RR.hashlib.sha256(manifest_bytes).hexdigest(),
        'common_prompt_sha256': val['common_prompt_and_hash']['sha256'],
        'effective_prompt_sha256': RR.sha(request), 'model_identity': val['exact_model_snapshot'],
        'session_id': 'synthetic:session-' + run['record_id'].split('record-', 1)[1],
        'raw_request': {'text': request, 'sha256': RR.sha(request)},
        'raw_response': {'text': response, 'sha256': RR.sha(response)},
        'answer_claims': [dict(claim, source_pointer='/claims/0')],
        'answer_limitations': limitations,
        'input_evidence': [{'kind': 'synthetic:original', 'identity': 'synthetic:artifact-' + slug(case),
                            'sha256': val['original_artifact_set_and_hashes'][case]}],
    }
    if arm == 'no-tool':
        values.update(tool_calls=[], tool_call_count=0, tool_time_ms=0, reader_context_tokens=0,
                      reader_fidelity='not_applicable')
    for key, value in values.items():
        f[key]['value'] = value
    return record


def audit(plan, records, manifest_bytes, manifest):
    """Accept a record set only if it matches the plan, manifest bytes and budgets."""
    require(RR.hashlib.sha256(manifest_bytes).hexdigest() == plan['manifest_sha256'],
            'manifest bytes changed after planning')
    for record in records:
        RR.validate(record, manifest)
        RR.bind_manifest(record, manifest_bytes)
    flat = [{k: v['value'] for k, v in r['fields'].items()} for r in records]
    seen = set()
    for f in flat:
        require(f['repetition_id'] not in seen, 'duplicate repetition id: ' + f['repetition_id'])
        seen.add(f['repetition_id'])
    require(len({f['record_id'] for f in flat}) == len(flat), 'duplicate record id')
    by_rep = {r['repetition_id']: r for r in plan['runs']}
    for f in flat:
        require(f['case_id'] in plan['cases'], 'unknown case id: ' + f['case_id'])
        run = by_rep.get(f['repetition_id'])
        require(run is not None, 'unknown repetition id: ' + f['repetition_id'])
        require((run['case_id'], run['arm'], run['pair_id'], run['record_id']) ==
                (f['case_id'], f['arm'], f['pair_id'], f['record_id']),
                'record disagrees with plan: ' + f['repetition_id'])
    missing = [r for r in plan['runs'] if r['repetition_id'] not in seen]
    require(not missing, 'missing planned run: %s (%s, %s)' %
            (missing[0]['repetition_id'], missing[0]['case_id'], missing[0]['arm']) if missing else '')
    val = {k: v['value'] for k, v in manifest['fields'].items()}
    for f in flat:
        limit = val['matched_total_token_budget']['max_total_tokens']
        require(f['total_tokens'] <= limit, 'total token budget exceeded: %d > %d' % (f['total_tokens'], limit))
        require(f['output_tokens'] <= val['matched_output_budget']['max_output_tokens'],
                'output token budget exceeded')
        require(f['reader_context_tokens'] <= val['matched_context_budget']['max_context_tokens'],
                'context budget exceeded')
        require(f['elapsed_ms'] <= val['matched_wall_time_budget']['max_wall_ms'], 'wall time budget exceeded')
        require(f['tool_call_count'] <= val['tool_call_limits_and_accounting']['max_tool_calls'],
                'tool call limit exceeded')


def expect_reject(name, reason, action):
    try:
        action()
    except ValueError as exc:
        require(str(exc) == reason, '%s: unexpected reason: %s' % (name, exc))
        return {'mutation': name, 'result': 'rejected', 'reason': str(exc)}
    raise ValueError(name + ': mutation accepted')


def check():
    expected_text = build_manifest_text()
    manifest_bytes = SYNTHETIC.read_bytes()
    require(manifest_bytes == expected_text.encode(), 'synthetic manifest file differs from generator')
    template = RR.parse(TEMPLATE.read_text())
    manifest = RR.parse(manifest_bytes.decode())
    validate_manifest(manifest, template)
    plan = plan_runs(manifest, manifest_bytes)
    require(plan == plan_runs(deepcopy(manifest), manifest_bytes), 'plan is not deterministic')
    require(len(plan['runs']) == len(CASES) * len(ARMS) * REPETITIONS, 'unexpected run count')
    records = [build_record(r, manifest, manifest_bytes) for r in plan['runs']]
    audit(plan, records, manifest_bytes, manifest)

    def mutated(change, subset=None):
        copy = deepcopy(records)
        change(copy)
        return subset(copy) if subset else copy

    rep0 = records[0]['fields']['repetition_id']['value']
    results = []

    def record_case(name, reason, change, data=manifest_bytes):
        results.append(expect_reject(name, reason,
                       lambda: audit(plan, mutated(change), data, manifest)))

    record_case('missing arm for one case', 'missing planned run: synthetic:rep-case-a-tool-1 (synthetic:case-a, tool)',
                lambda rs: rs.__setitem__(slice(None), [r for r in rs
                    if not (r['fields']['case_id']['value'] == 'synthetic:case-a'
                            and r['fields']['arm']['value'] == 'tool')]))
    record_case('duplicate repetition id', 'duplicate repetition id: ' + rep0,
                lambda rs: rs[1]['fields']['repetition_id'].update(value=rep0))
    record_case('manifest bytes changed after planning', 'manifest bytes changed after planning',
                lambda rs: None, manifest_bytes + b' ')
    record_case('unknown case id', 'unknown case id: synthetic:case-zzz',
                lambda rs: rs[0]['fields']['case_id'].update(value='synthetic:case-zzz'))
    record_case('unknown arm', 'unknown arm',
                lambda rs: rs[0]['fields']['arm'].update(value='synthetic:unknown'))
    record_case('record bound to another manifest', RR.BINDING_REASON,
                lambda rs: rs[0]['fields']['manifest_sha256'].update(value=RR.sha('SYNTHETIC other manifest')))
    record_case('total token budget exceeded', 'total token budget exceeded: 2020 > 1000',
                lambda rs: [rs[0]['fields']['output_tokens'].update(value=2000),
                            rs[0]['fields']['total_tokens'].update(value=2020)])

    def manifest_case(name, reason, change):
        altered = deepcopy(manifest)
        change(altered)
        results.append(expect_reject(name, reason, lambda: validate_manifest(altered, template)))

    manifest_case('manifest field removed', 'manifest field names differ from template',
                  lambda m: m['fields'].pop('provider_cost_basis'))
    manifest_case('null field reason changed', 'provider_cost_basis: null field must keep the template reason',
                  lambda m: m['fields']['provider_cost_basis'].update(reason='other'))
    manifest_case('populated field lacks synthetic provenance', 'runner_version: synthetic provenance required',
                  lambda m: m['fields']['runner_version'].update(provenance='measured'))

    nulls = sorted(k for k, v in manifest['fields'].items() if v['value'] is None)
    print(json.dumps({'status': 'pass', 'design_only': True, 'model_calls': 0, 'runs_executed': 0,
                      'benchmark_ready': False, 'tool_quality': None,
                      'planned_runs': len(plan['runs']), 'plan_sha256': plan['plan_sha256'],
                      'manifest_sha256': plan['manifest_sha256'],
                      'run_order': [r['repetition_id'] for r in plan['runs']],
                      'mutations': results, 'undecided_null_fields': nulls}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--write-manifest', action='store_true',
                       help='regenerate benchmark/baseline/run-manifest.synthetic.json')
    args = parser.parse_args()
    try:
        if args.write_manifest:
            SYNTHETIC.write_text(build_manifest_text())
        else:
            check()
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
        print('runner-contract check failed: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
