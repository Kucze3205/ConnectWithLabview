#!/usr/bin/env python3
"""Validate the issue #405 design; never execute model runs or write files."""
import argparse
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / 'benchmark/precision/plan.json'
MANIFEST = ROOT / 'benchmark/baseline/run-manifest.template.json'
MATCHES = (
    'provider exact_model_snapshot snapshot_pinning_limitations_and_run_window '
    'model_image_capabilities independent_repetitions_per_case_arm sampling_order '
    'paired_arm_randomization stopping_rule affordable_run_ceiling '
    'precision_cost_plan_revision per_case_tolerances_and_nondeterminism '
    'uncertainty_procedure confidence_level resampling_seed_and_count '
    'independent_lineage_units_and_repeat_preservation missing_pair_treatment '
    'exclusions_and_aggregation_weights small_sample_and_unavailable_scope_reporting '
    'owner_precision_target_and_acceptance_record'
).split()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def positive_int(value):
    return type(value) is int and value > 0


def contains(value, fragments, reason):
    require(isinstance(value, str) and all(x in value for x in fragments), reason)


def validate(plan, template):
    require(plan['schema_version'] == 1 and plan['status'] == 'design-only', 'design status')
    require(plan['model_runs_executed'] == 0 and plan['quality_threshold_proposed'] is False,
            'no executed runs or quality threshold')
    names = plan['manifest_field_matches']
    fields = plan['manifest_fields']
    require(isinstance(names, list) and len(names) == len(set(names))
            and set(names) == set(MATCHES) == set(fields), 'manifest match inventory')
    require(set(names) <= set(template['fields']), 'manifest field names')
    for name in ('provider', 'exact_model_snapshot',
                 'snapshot_pinning_limitations_and_run_window', 'affordable_run_ceiling',
                 'owner_precision_target_and_acceptance_record'):
        require(fields[name]['value'] is None and bool(fields[name]['reason']),
                'unresolved owner/provider fields')
    repetitions = fields['independent_repetitions_per_case_arm']
    require(repetitions['development_pilot'] == 4 and repetitions['evaluation'] is None,
            'development pilot only; evaluation count unresolved')
    counts = repetitions['candidate_counts']
    require(isinstance(counts, list) and counts and all(positive_int(n) for n in counts)
            and counts == sorted(set(counts)), 'positive ordered candidate repetitions')
    require(repetitions['arms'] == ['no-tool', 'tool'], 'matched arms')
    contains(repetitions['pairing'], ['Same case/key', 'fresh isolated session', 'equally'],
             'matched repetition pairing')
    require(fields['confidence_level'] == 0.95, 'confidence level fixed at 0.95')
    resampling = fields['resampling_seed_and_count']
    require(type(resampling['seed']) is int and resampling['seed'] == 40502
            and resampling['count'] == 10000, 'fixed resampling seed and count')
    contains(resampling['generator'], ['random.Random', 'pin Python'], 'resampling generator')
    uncertainty = fields['uncertainty_procedure']
    require(uncertainty['method'] == 'paired-cluster-percentile-bootstrap', 'paired cluster method')
    require(uncertainty['paired_dimensions'] == ['answer_correctness', 'source_grounding'],
            'separate paired dimensions')
    contains(uncertainty['fidelity'], ['not applicable', 'no paired fidelity gain'],
             'fidelity has no no-tool comparison')
    contains(uncertainty['estimand'], ['frozen required-item denominator', 'tool minus no-tool',
                                      'full outcome counts', 'extras', 'precedence rules'],
             'fixed-denominator descriptive estimand')
    contains(uncertainty['aggregation'], ['within case', 'within each lineage',
                                         'independent lineages', 'never combine dimensions'],
             'nested aggregation')
    contains(uncertainty['resampling'], ['G lineage IDs with replacement',
                                        'whole project/case/repetition block', 'preserving paired arms',
                                        '2.5th and 97.5th', '(B-1)*p',
                                        'No resampling of files or repetitions'], 'lineage resampling')
    units = fields['independent_lineage_units_and_repeat_preservation']
    require(units['unit'] == 'independent project/lineage connected group'
            and units['preserve_all_nested_repetitions'] is True, 'independent units and nested repeats')
    missing = fields['missing_pair_treatment']
    require(missing['impute'] is False and missing['comparison_complete_requires_all_planned_pairs'] is True,
            'missing pairs cannot be imputed or complete')
    contains(missing['rule'], ['both arms', 'independently scored', 'never replace', 'incomplete'],
             'missing pair eligibility')
    contains(missing['report'], ['planned/attempted/executed/scored/complete', 'conditional',
                                 'lower/upper bounds', '-1/+1', '[-1,1]', 'no point estimate'],
             'missing coverage and bounds')
    tolerances = fields['per_case_tolerances_and_nondeterminism']
    require(tolerances['source'] == 'independently checked case oracles'
            and tolerances['global_numeric_tolerance'] is None
            and tolerances['dimensions'] == ['reading_fidelity', 'answer_correctness', 'source_grounding'],
            'case oracle tolerances, not a global tolerance')
    contains(fields['small_sample_and_unavailable_scope_reporting'],
             ['fewer than two', 'no inferential interval', 'unstable', 'missing lineage diversity'],
             'small sample limits')
    contains(fields['exclusions_and_aggregation_weights'],
             ['No result-dependent exclusions', 'equal case weights', 'equal lineage weights',
              'planned denominators', 'eligible denominator'], 'fixed aggregation weights')
    contains(fields['stopping_rule'], ['no optional stopping', 'Quota exhaustion', 'incomplete',
                                      'no selective replacement'], 'fixed stopping rule')
    contains(fields['sampling_order'], ['Sort case IDs and repetition IDs', 'before evaluation'],
             'frozen sampling order')
    randomization = fields['paired_arm_randomization']
    require(randomization['seed'] == 40501, 'fixed arm order seed')
    contains(randomization['method'], ['sha256(seed:pair_id:arm)', 'runner-contract.md'],
             'runner arm order method')
    contains(fields['model_image_capabilities']['requirement'],
             ['Both arms', 'identical native panel/diagram images', 'Verify', 'unsupported modalities'],
             'image capability verification')
    pilot = plan['pilot_sizing']
    require(pilot['data_partition'] == 'development-only' and pilot['evaluation_results_used'] is False,
            'development-only sizing')
    contains(pilot['variance_model'], ['paired differences', 'lineage intercept', 'repeat residual',
                                      'tau2', 'sigma2', 'case covariance', 'block sizing'],
             'development variance model and failure rule')
    contains(pilot['prediction'], ['tau2/G + sigma2/(G*r)', '1.96*sqrt',
                                  'not the final cluster-bootstrap interval', 'development cluster resampling'],
             'variance-based repetition prediction')
    contains(pilot['selection'], ['owner targets', 'smallest candidate r', 'every declared',
                                 'quota ceiling', 'infeasible', 'do not tune against evaluation gains'],
             'pilot selection and infeasibility rule')
    contains(pilot['cost'], ['2 * case_count * r', '2 * development_case_count * 4',
                            'probes', 'retried', 'reserve', 'Unknown conversion or quota'],
             'pilot and evaluation resource accounting')
    contains(pilot['freeze'], ['Before any evaluation request', 'evidence hashes',
                              'selected integer r per case/arm', 'owner targets/acceptance',
                              'evaluation results cannot influence'], 'pre-evaluation freeze')
    quota = plan['quota']
    require(quota['status'] == 'owner-decision' and quota['allocated_quota'] is None
            and quota['extra_spending_authorized'] is False, 'owner quota decision; no spending')
    routes = quota['candidate_routes']
    require(len(routes) == 3 and {(r['provider'], r['model']) for r in routes} == {
        ('claude', 'claude-sonnet-5-5'), ('codex', 'gpt-6.1-sol'), ('codex', 'gpt-5.6-luna')},
        'candidate routing inventory')
    require(all(r['evidence'] for r in routes), 'candidate provenance')
    contains(quota['capability_status'], ['image support', 'snapshot pinning', 'retention',
                                         'no capability or quota has been verified'], 'unverified capabilities')
    contains(quota['owner_decision'], ['Which existing subscription quota', 'account/service/interface',
                                       'remaining units', 'renewal/run window', 'rate limits',
                                       'hard total ceiling', 'no extra spending'], 'exact owner quota decision')


def rejection_controls(plan, template):
    controls = [
        (('manifest_fields', 'confidence_level'), 0.5, 'confidence level fixed at 0.95'),
        (('manifest_fields', 'missing_pair_treatment', 'impute'), True,
         'missing pairs cannot be imputed or complete'),
        (('pilot_sizing', 'evaluation_results_used'), True, 'development-only sizing'),
        (('quota', 'extra_spending_authorized'), True, 'owner quota decision; no spending'),
        (('manifest_fields', 'independent_lineage_units_and_repeat_preservation',
          'preserve_all_nested_repetitions'), False, 'independent units and nested repeats'),
        (('manifest_fields', 'uncertainty_procedure', 'resampling'),
         'Resample individual files independently.', 'lineage resampling'),
        (('manifest_fields', 'independent_repetitions_per_case_arm', 'evaluation'), 8,
         'development pilot only; evaluation count unresolved'),
    ]
    def expect_reject(path, mutated, expected):
        try:
            validate(mutated, template)
        except ValueError as error:
            if str(error) != expected:
                raise AssertionError(f'{path}: expected {expected!r}, got {str(error)!r}') from error
        else:
            raise AssertionError(f'{path}: mutation accepted')

    for path, value, expected in controls:
        mutated = copy.deepcopy(plan)
        node = mutated
        for part in path[:-1]:
            node = node[part]
        node[path[-1]] = value
        expect_reject(path, mutated, expected)

    path, value, actual_reason = controls[0]
    mutated = copy.deepcopy(plan)
    node = mutated
    for part in path[:-1]:
        node = node[part]
    node[path[-1]] = value
    wrong_reason = actual_reason + ' [deliberately wrong suffix]'
    try:
        expect_reject(path, mutated, wrong_reason)
    except AssertionError as error:
        require(str(error) == f'{path}: expected {wrong_reason!r}, got {actual_reason!r}',
                f'reason comparison self-test: wrong mismatch error: {error}')
    else:
        raise ValueError('reason comparison self-test: mismatch accepted')
    print('PASS: reason comparison self-test rejects a deliberately wrong expected reason')
    changed_template = copy.deepcopy(template)
    del changed_template['fields']['confidence_level']
    try:
        validate(plan, changed_template)
    except ValueError as error:
        if str(error) != 'manifest field names':
            raise AssertionError('wrong manifest-field rejection reason') from error
    else:
        raise AssertionError('removed template field accepted')
    return (len(controls) + 1, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    try:
        plan = json.loads(PLAN.read_text(encoding='utf-8'))
        template = json.loads(MANIFEST.read_text(encoding='utf-8'))
        validate(plan, template)
        completed = rejection_controls(plan, template)
        require(completed == (8, 1), 'rejecting controls did not complete: expected (8, 1)')
        count = completed[0]
    except (OSError, ValueError, KeyError, TypeError, AssertionError) as error:
        print(f'FAIL precision plan: {error}', file=sys.stderr)
        return 1
    print(f'PASS precision plan: {len(MATCHES)} manifest field matches; {count} rejecting mutations with asserted reasons.')
    print('Design only: no model runs, no verified quota, no precision target or quality threshold; independent review and owner decisions remain.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
