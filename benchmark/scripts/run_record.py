#!/usr/bin/env python3
"""Synthetic raw-record contract check only: no runner, model calls or scoring.

All populated template fields carry synthetic provenance; null fields carry a
reason. This is not a validator for populated production records. Restricted
storage, manifest binding and provider accounting require independent review.
"""
import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / 'benchmark/baseline/run-record.template.json'
MANIFEST = ROOT / 'benchmark/baseline/run-manifest.template.json'
POPULATED = frozenset('''schema_version record_id case_id pair_id arm repetition_id
manifest_sha256 common_prompt_sha256 effective_prompt_sha256 model_identity
session_id started_at finished_at elapsed_ms tool_time_ms queue_time_ms
input_tokens output_tokens total_tokens reader_context_tokens cached_input_tokens
retry_count tool_call_count tool_calls truncated exhausted_budgets outcome
raw_request raw_response answer_claims answer_status answer_limitations
input_evidence errors reader_fidelity'''.split())
UNDECIDED = frozenset('''restricted_storage provider_usage_mapping provider_cost
infrastructure_cost interruption_policy claim_mapping_revision
manifest_binding_evidence isolation_evidence'''.split())
# Record field -> exact existing manifest field names. These are schema links,
# not evidence that synthetic hashes bind an actual populated manifest.
MANIFEST_LINKS = {
    'manifest_sha256': ('raw_run_record_schema_and_storage',),
    'case_id': ('question_input_hashes', 'case_key_revision', 'split_revision'),
    'pair_id': ('paired_arm_randomization', 'sampling_order'),
    'repetition_id': ('independent_repetitions_per_case_arm',),
    'common_prompt_sha256': ('common_prompt_and_hash',),
    'effective_prompt_sha256': ('common_prompt_and_hash', 'arm_specific_tool_instructions'),
    'model_identity': ('provider', 'exact_model_snapshot', 'runner_version', 'scorer_version'),
    'input_evidence': ('original_artifact_set_and_hashes', 'permitted_documentation_and_hashes',
                       'native_images_and_unavailable_modalities'),
    'total_tokens': ('matched_total_token_budget', 'input_output_token_accounting'),
    'reader_context_tokens': ('matched_context_budget',),
    'output_tokens': ('matched_output_budget',),
    'elapsed_ms': ('matched_wall_time_budget', 'elapsed_and_tool_time_accounting'),
    'tool_calls': ('tool_call_limits_and_accounting', 'reader_commit',
                   'reader_configuration', 'tool_schema'),
    'truncated': ('truncation_and_exhaustion_recording',),
    'exhausted_budgets': ('truncation_and_exhaustion_recording',),
    'provider_usage_mapping': ('input_output_token_accounting', 'cache_retry_queue_and_unpriced_accounting'),
    'provider_cost': ('provider_cost_basis',),
    'infrastructure_cost': ('infrastructure_cost_basis',),
    'restricted_storage': ('raw_run_record_schema_and_storage', 'data_recipients_retention_and_grant'),
    'isolation_evidence': ('fresh_session_and_memory_isolation', 'restricted_access_evidence'),
    'interruption_policy': ('stopping_rule', 'missing_pair_treatment'),
    'claim_mapping_revision': ('claim_mapping_and_adjudication_revision',),
    'manifest_binding_evidence': ('case_key_revision', 'runner_version', 'scorer_version'),
    'reader_fidelity': ('no_reader_fidelity_not_applicable_record', 'separate_probe_session_limits'),
}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def exact(value, keys, label):
    require(isinstance(value, dict) and set(value) == set(keys), label + ': fields')


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def is_hash(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('nonstandard JSON constant: ' + value)


def parse(text):
    return json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_constant)


def score_answer(record):
    """Return score.py compute()'s answer_record/raw_answer_record inputs.

    source_pointer addresses the preserved model response, not the original
    artifact. citations preserve the separate original-artifact locators.
    No keys, fidelity probes, denominators or correctness are manufactured.
    """
    f = {key: item['value'] for key, item in record['fields'].items()}
    claims = [{key: deepcopy(claim[key]) for key in
               ('claim_id', 'answer', 'conditions', 'citations')}
              for claim in f['answer_claims']]
    answer = {'status': f['answer_status'], 'claims': claims,
              'limitations': deepcopy(f['answer_limitations'])}
    return {'answer_record': answer, 'raw_answer_record': deepcopy(f['raw_response'])}


def validate(record, manifest):
    exact(record, ('fields',), 'record')
    fields = record['fields']
    exact(fields, POPULATED | UNDECIDED, 'record field list')
    for key, item in fields.items():
        if key in UNDECIDED:
            exact(item, ('value', 'reason'), key)
            require(item['value'] is None and isinstance(item['reason'], str)
                    and bool(item['reason'].strip()), key + ': null with reason required')
        else:
            exact(item, ('value', 'provenance'), key)
            require(item['provenance'] == 'synthetic' and item['value'] is not None,
                    key + ': synthetic provenance required')
    require(set(MANIFEST_LINKS) <= set(fields), 'unknown record link')
    require(isinstance(manifest.get('fields'), dict), 'manifest fields absent')
    for names in MANIFEST_LINKS.values():
        require(set(names) <= set(manifest['fields']), 'unknown manifest field reference')
    f = {key: item['value'] for key, item in fields.items()}
    require(type(f['schema_version']) is int and f['schema_version'] == 1, 'schema version')
    for key in ('record_id', 'case_id', 'pair_id', 'repetition_id', 'model_identity', 'session_id'):
        require(isinstance(f[key], str) and f[key].startswith('synthetic:')
                and len(f[key]) > 10, key + ': synthetic identifier required')
    require(f['arm'] in ('no-tool', 'tool'), 'unknown arm')
    for key in ('manifest_sha256', 'common_prompt_sha256', 'effective_prompt_sha256'):
        require(is_hash(f[key]), key + ': SHA256 required')
    integers = ('elapsed_ms', 'tool_time_ms', 'queue_time_ms', 'input_tokens',
                'output_tokens', 'total_tokens', 'reader_context_tokens',
                'cached_input_tokens', 'retry_count', 'tool_call_count')
    for key in integers:
        require(type(f[key]) is int and f[key] >= 0, key + ': nonnegative integer required')
    require(f['total_tokens'] == f['input_tokens'] + f['output_tokens'], 'token total mismatch')
    require(max(f['reader_context_tokens'], f['cached_input_tokens']) <= f['input_tokens'],
            'input token subsets exceed input')
    start, end = [datetime.strptime(f[key], '%Y-%m-%dT%H:%M:%SZ')
                  for key in ('started_at', 'finished_at')]
    require((end - start).total_seconds() * 1000 == f['elapsed_ms'], 'elapsed timestamp mismatch')
    require(f['tool_time_ms'] + f['queue_time_ms'] <= f['elapsed_ms'], 'time components exceed elapsed')
    require(isinstance(f['tool_calls'], list) and len(f['tool_calls']) == f['tool_call_count'],
            'tool call count mismatch')
    for call in f['tool_calls']:
        exact(call, ('call_id', 'request', 'response', 'elapsed_ms', 'error'), 'tool call')
        require(call['call_id'].startswith('synthetic:') and
                all(isinstance(call[k], str) and call[k].startswith('SYNTHETIC')
                    for k in ('request', 'response')), 'synthetic tool payload required')
        require(type(call['elapsed_ms']) is int and call['elapsed_ms'] >= 0, 'tool time invalid')
        require(call['error'] is None or isinstance(call['error'], str), 'tool error invalid')
    require(sum(c['elapsed_ms'] for c in f['tool_calls']) == f['tool_time_ms'], 'tool time sum mismatch')
    require(type(f['truncated']) is bool, 'truncated flag invalid')
    require(isinstance(f['exhausted_budgets'], list) and
            all(x in ('total_tokens', 'context', 'output', 'wall_time', 'tool_calls', 'quota')
                for x in f['exhausted_budgets']), 'unknown exhausted budget')
    require(f['outcome'] in ('complete', 'unsupported', 'error', 'interrupted'), 'unknown outcome')
    require(f['answer_status'] in ('complete', 'unsupported', 'error'), 'unknown answer status')
    for key in ('answer_limitations', 'errors'):
        require(isinstance(f[key], list) and all(isinstance(x, str) for x in f[key]), key + ': string list required')
    for key in ('raw_request', 'raw_response'):
        exact(f[key], ('text', 'sha256'), key)
        require(isinstance(f[key]['text'], str) and sha(f[key]['text']) == f[key]['sha256'],
                key + ': raw hash mismatch')
    require(f['effective_prompt_sha256'] == f['raw_request']['sha256'], 'effective prompt hash mismatch')
    require(f['raw_request']['text'].startswith('SYNTHETIC'), 'synthetic request required')
    require(isinstance(f['answer_claims'], list), 'claims list required')
    for index, claim in enumerate(f['answer_claims']):
        require(isinstance(claim, dict) and 'source_pointer' in claim, 'claim source pointer missing')
        exact(claim, ('claim_id', 'answer', 'conditions', 'citations', 'source_pointer'), 'claim')
        require(claim['source_pointer'] == '/claims/' + str(index), 'claim source pointer mismatch')
        require(isinstance(claim['claim_id'], str) and claim['claim_id'].startswith('synthetic:')
                and isinstance(claim['answer'], str) and claim['answer'].startswith('SYNTHETIC'),
                'synthetic claim required')
        require(isinstance(claim['conditions'], list) and
                all(isinstance(x, str) and x.startswith('synthetic:') for x in claim['conditions']),
                'synthetic conditions required')
        require(isinstance(claim['citations'], list) and bool(claim['citations']), 'claim citation missing')
        for citation in claim['citations']:
            exact(citation, ('artifact_sha256', 'locator'), 'citation')
            exact(citation['locator'], ('expression',), 'locator')
            require(is_hash(citation['artifact_sha256']) and
                    citation['locator']['expression'].startswith('synthetic:'), 'synthetic citation required')
    require(isinstance(f['input_evidence'], list) and bool(f['input_evidence']), 'input evidence required')
    for item in f['input_evidence']:
        exact(item, ('kind', 'identity', 'sha256'), 'input evidence')
        require(all(isinstance(item[k], str) and item[k].startswith('synthetic:')
                    for k in ('kind', 'identity')) and is_hash(item['sha256']), 'synthetic input evidence required')
    require(f['reader_fidelity'] == ('not_applicable' if f['arm'] == 'no-tool' else 'not_measured'),
            'reader fidelity applicability mismatch')
    if f['arm'] == 'no-tool':
        require(f['tool_call_count'] == f['tool_time_ms'] == f['reader_context_tokens'] == 0,
                'no-tool arm has reader usage')
    converted = score_answer(record)
    require(parse(converted['raw_answer_record']['text']) == converted['answer_record'],
            'score conversion disagrees with raw response')
    return converted


def check():
    record, manifest = parse(TEMPLATE.read_text()), parse(MANIFEST.read_text())
    converted = validate(record, manifest)
    # Explicit substantive mapping check, independent of the conversion loop.
    expected_claim = {
        'claim_id': 'synthetic:claim-1',
        'answer': 'SYNTHETIC answer; no artifact fact asserted.',
        'conditions': ['synthetic:condition'],
        'citations': [{'artifact_sha256': sha('SYNTHETIC original artifact'),
                       'locator': {'expression': 'synthetic:original/object/property'}}],
    }
    require(converted['answer_record'] == {'status': 'complete', 'claims': [expected_claim],
            'limitations': ['SYNTHETIC design fixture only.']}, 'unexpected synthetic conversion')
    mutations = (
        ('missing repetition id', lambda r: r['fields'].pop('repetition_id'), 'record field list: fields'),
        ('token total mismatch', lambda r: r['fields']['total_tokens'].update(value=31), 'token total mismatch'),
        ('claim without source pointer', lambda r: r['fields']['answer_claims']['value'][0].pop('source_pointer'),
         'claim source pointer missing'),
        ('unknown arm', lambda r: r['fields']['arm'].update(value='synthetic:unknown'), 'unknown arm'),
        ('wrong raw response hash', lambda r: r['fields']['raw_response']['value'].update(sha256='0' * 64),
         'raw_response: raw hash mismatch'),
        ('wrong claim answer', lambda r: r['fields']['answer_claims']['value'][0].update(answer='SYNTHETIC wrong'),
         'score conversion disagrees with raw response'),
    )
    results = []
    for name, mutate, reason in mutations:
        altered = deepcopy(record)
        mutate(altered)
        try:
            validate(altered, manifest)
        except ValueError as exc:
            require(str(exc) == reason, name + ': failed for unexpected reason: ' + str(exc))
            results.append({'mutation': name, 'result': 'rejected', 'reason': str(exc)})
        else:
            raise ValueError(name + ': mutation accepted')
    no_tool = deepcopy(record)
    for key, value in {'arm': 'no-tool', 'tool_calls': [], 'tool_call_count': 0,
                       'tool_time_ms': 0, 'reader_context_tokens': 0,
                       'reader_fidelity': 'not_applicable'}.items():
        no_tool['fields'][key]['value'] = value
    validate(no_tool, manifest)
    print(json.dumps({'status': 'pass', 'design_only': True, 'runs': 0,
                      'benchmark_ready': False, 'tool_quality': None,
                      'conversion': converted['answer_record'],
                      'no_tool_variant': 'pass', 'mutations': results,
                      'undecided': {k: record['fields'][k]['reason'] for k in sorted(UNDECIDED)}},
                     indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    try:
        check()
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
        print('run-record check failed: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
