#!/usr/bin/env python3
"""Repository-only WP1 authored-example integrity/coverage controls, issue #584.

Standard library; no writes, subprocesses, environment inputs, native execution,
or imports/execution of historical checkers/audits. Passing certifies bounded
preparation consistency, not narrative truth, dependency closure or F4 clearance.
"""
import base64
import copy
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
D = 'benchmark/writing/'
PACKAGE = D + 'wp1-examples-0121.json'
MD = D + 'wp1-examples-0121.md'
PRE = D + 'wp1-examples-0121-pre-edit.md'
REVIEW = D + 'wp1-disposition-review-0120.json'
KEY = D + 'wp1-key-0119.json'
METHOD = D + 'method.json'
ORIGINAL = 'benchmark/real-project-0107/original.lvproj'
LICENSE = 'benchmark/real-project-0107/LICENSE.txt'
VERIFICATION = D + 'wp1-examples-0121-verification.json'
STATUS = 'proposed-awaiting-separate-check'
MAP = 'WP1-original-output-grounding'
AFFECTED = ['C1-correct', 'C1-unverified-extra']
NAMES = ['WP1-0121-positive-map-v1', 'WP1-0121-unverified-extra-map-v1']
TASK_FIELDS = ['originals', 'preconditions', 'request', 'semantic_ids',
               'expected_semantics', 'preservation_ids', 'preservation',
               'answer_ids', 'oracle', 'native_outcome', 'output_paths',
               'output_manifest_rule', 'text_contract', 'planned_results',
               'trial_artifacts', 'result_rule', 'reading_fidelity']
FIXED = {
    PRE: '649b71383e6f0467d41e97db38a3cb660a75d9e631abc411295b05fa0e35fa4b',
    PACKAGE: '8c6f6d82e4fdc9db268827fd1cc942daebf84319336bba3e7141a7a110a8e382',
    MD: 'b450a9d0b2d5abe9c72a7f16514705b2f72a8c4d835131843f59c2b17c3e0120',
    REVIEW: 'bd2cd46a79bfcaf56a033b631c5b29196545283a547af86c6bcb8e9150c54141',
}
ORIGINAL_SHA = '1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf'
LICENSE_SHA = '529e65e6fc185d39380efd3957ef1c9acd0aac31ed288bcb9d124840861f03a2'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False).encode()


def read(path):
    p = PurePosixPath(path)
    if p.is_absolute() or '..' in p.parts or not p.parts:
        raise ValueError('unsafe repository path')
    full = ROOT / path
    if any((ROOT.joinpath(*p.parts[:i])).is_symlink()
           for i in range(1, len(p.parts) + 1)):
        raise ValueError('symlink is not evidence')
    data = full.read_bytes()
    if len(data) >= 2_000_000:
        raise ValueError('evidence exceeds 2 MB')
    return data


def pointer(value, locator):
    if not locator.startswith('/'):
        raise ValueError('expected JSON pointer')
    for part in locator[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def source_requirements(method, key):
    """Independently enumerate actual leaves, rather than trust author counts."""
    records = []

    def leaves(value, loc, path):
        if isinstance(value, dict) and value:
            for name, child in value.items():
                leaves(child, loc + '/' + name.replace('~', '~0').replace('/', '~1'), path)
        elif isinstance(value, list) and value:
            for index, child in enumerate(value):
                leaves(child, loc + '/' + str(index), path)
        else:
            records.append({'path': path, 'locator': loc, 'value': value,
                            'value_sha256': sha(canon(value))})

    task = method['tasks'][4]
    if task['id'] != 'WP1-project-build-text':
        raise ValueError('WP1 task identity changed')
    leaves(method['common'], '/common', METHOD)
    for field in TASK_FIELDS:
        leaves(task[field], '/tasks/4/' + field, METHOD)
    for path, numbers in [('benchmark/protocol.md', list(range(26, 42)) + [60]),
                          (D + 'README.md', [54, 56, 58, 60, 62, 64, 66])]:
        lines = read(path).decode().splitlines()
        for number in numbers:
            value = lines[number - 1]
            records.append({'path': path, 'locator': 'L' + str(number),
                            'value': value, 'value_sha256': sha(canon(value))})
    leaves(key['finding_dispositions']['F4'], '/finding_dispositions/F4', KEY)
    for index, item in enumerate(key['required_ids']):
        if item['dimension'] == 'preservation' or item['id'] == MAP:
            leaves(item, '/required_ids/' + str(index), KEY)
    for index, item in enumerate(key['claim_adjudication']['prescribed_ledgers']):
        if item['id'] in AFFECTED:
            leaves(item['evidence_reservation'],
                   '/claim_adjudication/prescribed_ledgers/' + str(index) + '/evidence_reservation', KEY)
    return records


def derive(task, original):
    """Expectation comes only from pinned source and existing task definition."""
    root = ET.fromstring(original)
    contract = task['text_contract']
    pre = contract['precondition']
    nodes = root.findall(contract['locator'])
    if (root.tag != pre['root_tag'] or root.attrib != pre['root_attributes']
            or len(nodes) != pre['match_count'] or len(nodes) != 1
            or nodes[0].attrib != pre['property_attributes']
            or nodes[0].text != pre['text'] or len(nodes[0]) != pre['property_children']):
        raise ValueError('original XML precondition failed')
    needle = b'Name="Bld_version.build" Type="Int">2<'
    if original.count(needle) != 1:
        raise ValueError('unique literal locator failed')
    offset = original.index(needle) + len(needle) - 2
    delta = contract['delta']
    actual = {'before': nodes[0].text, 'after': '3',
              'offset_zero_based': offset,
              'line_one_based': original[:offset].count(b'\n') + 1,
              'removed_hex': original[offset:offset + 1].hex(), 'inserted_hex': '33',
              'output_size': len(original), 'allowed_changed_bytes': 1}
    if delta != actual or task['expected_semantics']['delta'] != actual:
        raise ValueError('task delta disagrees with independently located original')
    expected = original[:offset] + b'3' + original[offset + 1:]
    if sum(a != b for a, b in zip(original, expected)) != 1:
        raise ValueError('not a one-byte change')
    return expected, offset, root


def dependency_declarations(root, original):
    records = []

    def visit(element, indices):
        if 'URL' in element.attrib:
            records.append({'path': element.attrib['URL'],
                            'kind': element.attrib.get('Type'),
                            'declaration': {'path': ORIGINAL, 'sha256': sha(original),
                                            'locator': 'element-child-index:' + indices + '/@URL',
                                            'value': element.attrib['URL']}})
        for index in range(len(element)):
            visit(element[index], indices + '/' + str(index))

    visit(root, '')
    return records


def assessment(required, extras):
    """L41 accounting on prescribed items; never consumes narrative text."""
    if not required:
        return 'unverified'
    values = required + extras
    if 'incorrect' in values:
        return 'incorrect'
    if 'unverified' in values:
        return 'unverified'
    if all(v == 'correct' for v in values):
        return 'correct'
    if any(v in ('correct', 'partial') for v in values):
        return 'partial'
    if 'error' in values:
        return 'error'
    if all(v == 'unsupported' for v in required):
        return 'unsupported'
    return 'missing'


def historical_block_errors(key):
    errors = []
    finding = key['finding_dispositions']['F4']
    if (finding['status'] != 'blocked-for-missing-evidence'
            or finding['affected_required_ids'] != [MAP]
            or finding['affected_examples'] != AFFECTED):
        errors.append('historical-F4-block')
    item = next(x for x in key['required_ids'] if x['id'] == MAP)
    if (item['established_key_use']['status'] != 'blocked'
            or item['established_key_use']['finding'] != 'F4'):
        errors.append('historical-F4-block')
    for ledger in key['claim_adjudication']['prescribed_ledgers']:
        if ledger['id'] not in AFFECTED:
            continue
        slot = next(x for x in ledger['items'] if x['id'] == MAP)
        reservation = ledger['evidence_reservation']
        if (slot['correctness'], slot['grounding'], slot.get('established_key_use')) != (
                'partial', 'partial', 'blocked-F4'):
            errors.append('historical-complete-map-credit')
        if (reservation['unseen_sidecars_assumed'] is not False
                or reservation['complete_preservation_map_supplied'] is not False
                or reservation['missing_evidence'] != finding['missing_evidence']):
            errors.append('historical-complete-map-credit')
    return errors


def check_package(package, context):
    errors = []
    add = errors.append
    method, key = context['method'], context['key']
    task = method['tasks'][4]
    original, license_bytes = context['original'], context['license']
    if (len(original), sha(original)) != (5806, ORIGINAL_SHA):
        add('mutated-original')
    if (len(license_bytes), sha(license_bytes)) != (1060, LICENSE_SHA):
        add('mutated-license')
    if errors:
        return errors
    expected, offset, root = derive(task, original)
    declarations = dependency_declarations(root, original)
    errors.extend(historical_block_errors(key))
    baseline = context['baseline']
    required = {f: task[f] for f in ('semantic_ids', 'preservation_ids', 'answer_ids')}
    if package['required_ids'] != required:
        add('required-ID-inventory')
    actual_requirements = source_requirements(method, key)
    manifest = [{k: x[k] for k in ('path', 'locator', 'value_sha256')}
                for x in actual_requirements]
    if (package['requirement_inventory'] != manifest
            or baseline['requirements'] != actual_requirements
            or baseline['method_task_fields'] != TASK_FIELDS
            or baseline['derived_ids'] != required
            or baseline['derived_trial_artifacts'] != task['trial_artifacts']['required']):
        add('source-requirement-inventory')
    if package['protected_pins'] != baseline['protected_pins']:
        add('protected-pin-inventory')
    if (package['revision'] != 'wp1-examples-0121-v1'
            or package['issue'] != 584 or package['status'] != STATUS
            or package['benchmark_ready'] is not False or package['F4_released'] is not False
            or package['historical_map_credit'] is not False):
        add('status-or-historical-credit-promotion')
    if package['starting_revision'] != {'commit': baseline['observed_commit'],
                                        'tree': baseline['observed_tree']}:
        add('starting-identity')
    pre = package['pre_edit_record']
    if pre != {'path': PRE, 'size': len(read(PRE)), 'sha256': FIXED[PRE],
               'requirement_leaf_count': len(actual_requirements)}:
        add('pre-edit-evidence')
    provenance = package['review_provenance']
    if (provenance['issue'] != 581 or provenance['preserved_path'] != REVIEW
            or provenance['sha256'] != FIXED[REVIEW]
            or provenance['size'] != len(read(REVIEW))
            or provenance['reviewed_identity'] != context['review']['reviewed_identity']
            or provenance['preservation_only'] is not True
            or provenance['reviewer_checks_replayed'] is not False):
        add('review-provenance')
    if package['native_and_trial_results'] != task['planned_results']:
        add('native-or-trial-promotion')
    gaps = package['claims_and_gaps']
    expected_gaps = {'agent_runs': 0, 'native_executions': 0,
                     'actual_project_files_written': 0, 'trial_outputs_produced': 0,
                     'human_C1_adjudication': 'open', 'native_key': 'unavailable',
                     'dependency_bytes_and_transitive_closure': 'unavailable',
                     'allocation': 'unallocated', 'actual_isolation': 'untested',
                     'reading_fidelity': 'unmeasured', 'independent_method_review': 'pending',
                     'owner_acceptance': 'pending', 'readiness': 'pending',
                     'established_key_use': 'blocked-F4', 'both_historical_map_slots': 'blocked-F4',
                     'public_lineage': 'familiar-possible; not withheld or demonstrated model-unseen',
                     'trial_eligibility': 'blocked; the authored controls satisfy no missing trial prerequisite'}
    if gaps != expected_gaps:
        add('gap-or-readiness-promotion')
    objects = package['byte_objects']
    raw = {'original-project': original, 'expected-project': expected, 'mit-notice': license_bytes}
    if set(objects) != set(raw):
        add('invented-byte-object')
    for name, data in raw.items():
        obj = objects[name]
        if (obj['size'], obj['sha256']) != (len(data), sha(data)):
            add('byte-object-hash')
        if name == 'expected-project':
            if base64.b64decode(obj['base64'], validate=True) != expected:
                add('expected-output-bytes')
            if obj['kind'] != 'authored-expected-bytes' or obj['derivation'] != {
                    'source': ORIGINAL, 'source_sha256': ORIGINAL_SHA,
                    'method_locator': '/tasks/4/text_contract/delta', **task['text_contract']['delta']}:
                add('expected-output-derivation')
            if obj['raw_byte_reference'] != {'path': PACKAGE,
                    'locator': '/byte_objects/expected-project/base64', 'encoding': 'base64'}:
                add('byte-object-reference')
        else:
            source = ORIGINAL if name == 'original-project' else LICENSE
            if (obj['kind'] != 'repository-bytes' or obj['path'] != source
                    or obj['raw_byte_reference'] != {'path': source, 'offset': 0, 'length': len(data)}):
                add('byte-object-reference')

    def entry(path, obj):
        return {'path': path, 'kind': 'file', 'size': len(raw[obj]), 'sha256': sha(raw[obj]),
                'raw_byte_reference': {'path': PACKAGE, 'locator': '/byte_objects/' + obj},
                'byte_object': obj}

    def citation(obj, loc):
        return {'path': PACKAGE, 'locator': '/byte_objects/' + obj,
                'sha256': sha(raw[obj]), 'content_locator': loc}

    if [x['id'] for x in package['examples']] != NAMES:
        add('new-example-identities')
    if len(package['examples']) != 2:
        add('example-count')
    expected_test = next(x for x in key['required_ids'] if x['id'] == MAP)['separate_dimension_tests']
    for index, example in enumerate(package['examples']):
        base = 'hypothetical/wp1-examples-0121/' + str(index)
        ep = '/examples/' + str(index)
        inventory = example['inventories']
        inventory_names = {'workspace_pre', 'workspace_post', 'dependency_pre',
                           'dependency_post', 'immutable_pre', 'immutable_post', 'delivered'}
        if set(inventory) != inventory_names:
            add('inventory-collections')
        expected_entries = {}
        for phase in ('pre', 'post'):
            expected_entries['workspace_' + phase] = [
                entry(task['output_paths'][0], 'original-project' if phase == 'pre' else 'expected-project'),
                entry('LICENSE.txt', 'mit-notice')]
            expected_entries['immutable_' + phase] = [entry('original.lvproj', 'original-project'),
                                                      entry('LICENSE.txt', 'mit-notice')]
            expected_entries['dependency_' + phase] = []
        expected_entries['delivered'] = expected_entries['workspace_post']
        for name in sorted(inventory_names):
            record = inventory[name]
            entries = record['entries']
            want = expected_entries[name]
            paths, wanted = [x['path'] for x in entries], [x['path'] for x in want]
            if paths != wanted:
                add('invented-sidecar' if set(paths) - set(wanted) else 'inventory-completeness')
            if entries != want:
                add('inventory-entry-bytes-or-reference')
            if record['file_count'] != len(want) or record['entries_sha256'] != sha(canon(want)):
                add('inventory-count-or-hash')
            suffix = 'dependencies' if name.startswith('dependency_') else ''
            root_want = (base + '/writable/' + suffix if suffix else
                         base + '/immutable' if name.startswith('immutable_') else
                         base + '/delivered' if name == 'delivered' else base + '/writable')
            if record['root'] != root_want or record['root_kind'] != 'stipulated-logical-root':
                add('inventory-boundary')
            if name.startswith('dependency_'):
                refs = record['declared_references']
                if len(refs) != len(declarations) or record['declaration_count'] != len(declarations):
                    add('dependency-inventory-completeness')
                for actual, wanted_ref in zip(refs, declarations):
                    if any(actual.get(k) != v for k, v in wanted_ref.items()):
                        add('dependency-declaration-evidence')
                    if (actual.get('size') is not None or actual.get('sha256') is not None
                            or actual.get('raw_byte_reference') is not None
                            or actual.get('status') != 'unavailable' or not actual.get('reason')):
                        add('invented-dependency-bytes')
                if (record['materialized_dependency_bytes'], record['transitive_closure'],
                        record['resolution']) != ('unavailable', 'unavailable', 'unexecuted'):
                    add('dependency-closure-promotion')
            elif record.get('links') != []:
                add('cross-root-link')
            if name.startswith('immutable_') and record.get('writable') is not False:
                add('immutable-root-writable')
        expected_boundary = {'workspace_root': base + '/writable',
                             'dependency_root': base + '/writable/dependencies',
                             'immutable_root': base + '/immutable', 'delivered_root': base + '/delivered',
                             'other_arm_root': base + '/other-arm', 'record_location': PACKAGE,
                             'actual_workspaces_allocated': False,
                             'status': 'stipulated-model-only; actual runner isolation untested',
                             'forbidden_dependency_roots': [base + '/immutable', base + '/other-arm'],
                             'resolved_dependency_paths': [], 'resolution_status': 'unexecuted',
                             'cross_root_links': []}
        if example['boundaries'] != expected_boundary:
            add('boundary-or-isolation-promotion')
        differences = {'changed_workspace_paths': task['output_paths'], 'missing_workspace_paths': [],
                       'unexpected_workspace_paths': [], 'unrelated_files_byte_identical': ['LICENSE.txt'],
                       'materialized_dependencies_before': 0, 'materialized_dependencies_after': 0,
                       'missing_declared_dependencies': [x['path'] for x in declarations],
                       'missing_transitive_closure': 'unavailable'}
        if example['inventory_differences'] != differences:
            add('inventory-difference-accounting')

        def invref(name):
            return {'path': PACKAGE, 'locator': ep + '/inventories/' + name,
                    'entries_sha256': sha(canon(expected_entries[name]))}

        notice = example['notice_evidence']
        if (notice['immutable_pre'] != invref('immutable_pre')
                or notice['immutable_post'] != invref('immutable_post')
                or notice['delivered'] != {'path': PACKAGE,
                    'locator': ep + '/inventories/delivered/entries/1',
                    'logical_path': base + '/delivered/LICENSE.txt', 'size': len(license_bytes),
                    'sha256': LICENSE_SHA,
                    'raw_byte_reference': {'path': LICENSE, 'offset': 0, 'length': len(license_bytes)}}):
            add('delivered-notice-evidence')
        if notice['status'] != 'authored-delivery-control; no actual trial delivery':
            add('notice-trial-overclaim')
        relations = example['original_output_map']
        wanted_ids = task['semantic_ids'] + task['preservation_ids']
        if [x['id'] for x in relations] != wanted_ids:
            add('preservation-ID-map-completeness')
        locator = task['text_contract']['locator']
        textloc = locator + '; byte ' + str(offset) + '; line ' + str(task['text_contract']['delta']['line_one_based'])
        byteloc = ('whole-file; [0,' + str(offset) + '); [' + str(offset + 1) + ','
                   + str(len(original)) + '); autoIncrement line 33')
        expected_relations = {
            'WP1-property-text': ([citation('original-project', textloc)],
                                 [citation('expected-project', textloc)],
                                 {'operation': 'exact-one-byte-substitution', 'offset': offset,
                                  'before_hex': '32', 'after_hex': '33', 'size': len(expected)}),
            'WP1-other-project-bytes': ([citation('original-project', byteloc)],
                                        [citation('expected-project', byteloc)],
                                        {'operation': 'equal-complementary-byte-ranges',
                                         'ranges': [[0, offset], [offset + 1, len(original)]],
                                         'allowed_metadata_deltas': []}),
            'WP1-file-set-and-unrelated-files': ([invref('workspace_pre'), invref('dependency_pre')],
                                                [invref('workspace_post'), invref('dependency_post')],
                                                {'operation': 'complete-present-file-set-and-declared-reference-comparison',
                                                 'changed_paths': task['output_paths'], 'missing_workspace_paths': [],
                                                 'unexpected_workspace_paths': [], 'dependency_declarations_unchanged': True,
                                                 'actual_cross_root_resolution': 'unexecuted; forbidden by model conditions'}),
            'WP1-root-version-declaration': ([citation('original-project', '/Project/@Type; /Project/@LVVersion; line 2')],
                                             [citation('expected-project', '/Project/@Type; /Project/@LVVersion; line 2')],
                                             {'operation': 'exact-root-attributes',
                                              'attributes': dict(root.attrib), 'authority': 'declaration-only',
                                              'native_save_version': 'unverified'}),
            'WP1-original-and-license': ([invref('immutable_pre')],
                                         [invref('immutable_post'), invref('delivered'),
                                          citation('mit-notice', 'whole-file including copyright and permission notice')],
                                         {'operation': 'immutable-byte-and-delivered-notice-identity',
                                          'original_sha256': ORIGINAL_SHA, 'license_sha256': LICENSE_SHA,
                                          'delivered_notice_path': 'LICENSE.txt', 'boundaries_reference': ep + '/boundaries'}),
        }
        for relation in relations:
            if relation['id'] not in expected_relations:
                add('unexpected-map-ID')
                continue
            before, after, comparison = expected_relations[relation['id']]
            # Truth and supplied support are checked separately; no importing a
            # grounding outcome into correctness, and no field-only map credit.
            if relation['comparison'] != comparison:
                add('map-relation-truth')
            if relation['original'] != before or relation['output'] != after:
                add('map-support')
                add('map-relation-truth')
            for ref in relation['original'] + relation['output']:
                if ref['path'] != PACKAGE or not pointer(package, ref['locator']):
                    add('unresolvable-map-support')
            if (relation['correctness_prescription'], relation['grounding_prescription'],
                    relation['agreement']) != ('correct', 'correct', 'pending-separate-semantic-review'):
                add('map-prescription-promotion')
            if not relation['conditions'] or not relation['assertion']:
                add('map-claim-or-condition-missing')
        if example['separate_map_dimension_tests'] != expected_test:
            add('separate-dimension-test-drift')
        old = next(x for x in key['claim_adjudication']['prescribed_ledgers'] if x['id'] == AFFECTED[index])
        predecessor = example['predecessor']
        if (predecessor['id'] != old['id'] or predecessor['package_path'] != KEY
                or predecessor['package_sha256'] != next(x['sha256'] for x in baseline['protected_pins'] if x['path'] == KEY)
                or predecessor['raw_answer_reference'] != old['raw_answer_reference']
                or predecessor['raw_answer_utf8_sha256'] != old['evidence_reservation']['raw_answer_utf8_sha256']
                or predecessor['historical_answer_modified'] is not False
                or predecessor['complete_map_credit_to_predecessor'] is not False):
            add('historical-answer-credit-or-provenance')
        answer = example['answer']
        if (answer['case_id'] != NAMES[index] or answer['status'] != 'authored-expected-answer'
                or [x['claim_id'] for x in answer['claims']] != task['answer_ids']
                or not answer['limitations']):
            add('answer-ID-or-identity')
        for claim in answer['claims']:
            if not claim['answer'] or not claim['conditions'] or not claim['citations']:
                add('answer-evidence-missing')
            for ref in claim['citations']:
                if ref['path'] == PACKAGE:
                    pointer(package, ref['locator'])
                elif ref['path'] == METHOD:
                    pointer(method, ref['locator'])
                elif (ref['path'], ref['locator']) != (D + 'README.md', 'L60'):
                    add('answer-citation-unknown')
        extras = [] if index == 0 else [{'assertion': 'Startup time decreases 10 percent',
                    'correctness': 'unverified', 'grounding': 'missing', 'citations': [],
                    'reason': 'Deliberately retained unmeasured extra. No runtime/performance evidence exists.'}]
        prescribed = example['prescriptions']
        if (answer['extra_assertions'] != extras or prescribed['extras'] != extras):
            add('unverified-extra-retention')
        if (prescribed['required_items'] != [{'id': x, 'correctness': 'correct', 'grounding': 'correct'}
                                            for x in task['answer_ids']]
                or prescribed['status'] != STATUS or prescribed['not_executable_narrative_scoring'] is not True
                or prescribed['map_preservation_coverage'] != task['preservation_ids']
                or prescribed['duplicates'] != [] or prescribed['contradictions'] != []):
            add('prescription-inventory')
        for dimension, field in [('correctness', 'answer_correctness'), ('grounding', 'source_grounding')]:
            result = assessment([x[dimension] for x in prescribed['required_items']],
                                [x[dimension] for x in extras])
            if prescribed['assessment'][field] != result:
                add('separate-assessment')
        artifacts = example['trial_artifact_accounting']
        refs = {'complete-original-bytes': '/byte_objects/original-project',
                'complete-edited-bytes': '/byte_objects/expected-project',
                'license-notice': ep + '/notice_evidence',
                'workspace-dependency-manifest': ep + '/inventories',
                'output-path-size-sha256-manifest': ep + '/inventories/delivered',
                'original-output-source-map': ep + '/original_output_map',
                'missing-unexpected-paths': ep + '/inventory_differences'}
        if [x['id'] for x in artifacts] != task['trial_artifacts']['required']:
            add('trial-artifact-accounting')
        for number, item in enumerate(artifacts):
            status = 'authored-control-evidence' if item['id'] in refs else 'unavailable'
            evidence = {'path': PACKAGE, 'locator': refs[item['id']]} if item['id'] in refs else None
            if (item['status'] != status or item['evidence'] != evidence or not item['reason']
                    or item['source_locator'] != '/tasks/4/trial_artifacts/required/' + str(number)):
                add('unavailable-trial-evidence-promotion')
    return sorted(set(errors))


def controls(package, context):
    results = {}

    def run(name, code, mutate_package=None, mutate_context=None):
        changed = copy.deepcopy(package)
        ctx = dict(context)
        if mutate_package:
            mutate_package(changed)
        if mutate_context:
            mutate_context(ctx)
        found = check_package(changed, ctx)
        results[name] = {'expected_error': code, 'rejected_for': found, 'passed': code in found}

    def ex(p, index=0):
        return p['examples'][index]

    for index in range(2):
        for inv in ('workspace_pre', 'workspace_post', 'immutable_pre', 'immutable_post', 'delivered'):
            run(str(index) + ':missing-inventory-entry:' + inv, 'inventory-completeness',
                lambda p, index=index, inv=inv: ex(p, index)['inventories'][inv]['entries'].pop())
        run(str(index) + ':wrong-inventory-hash', 'inventory-entry-bytes-or-reference',
            lambda p, index=index: ex(p, index)['inventories']['workspace_post']['entries'][0].update(sha256='0' * 64))
        for preservation in context['method']['tasks'][4]['preservation_ids']:
            run(str(index) + ':missing-map-ID:' + preservation, 'preservation-ID-map-completeness',
                lambda p, index=index, preservation=preservation: ex(p, index).update(
                    original_output_map=[r for r in ex(p, index)['original_output_map'] if r['id'] != preservation]))
        run(str(index) + ':invented-sidecar', 'invented-sidecar',
            lambda p, index=index: ex(p, index)['inventories']['workspace_post']['entries'].append(
                dict(ex(p, index)['inventories']['workspace_post']['entries'][1], path='unseen-sidecar.txt')))
        run(str(index) + ':immutable-original-replaced', 'inventory-entry-bytes-or-reference',
            lambda p, index=index: ex(p, index)['inventories']['immutable_post']['entries'][0].update(
                byte_object='expected-project', sha256=p['byte_objects']['expected-project']['sha256']))
        run(str(index) + ':immutable-license-mutated', 'inventory-entry-bytes-or-reference',
            lambda p, index=index: ex(p, index)['inventories']['immutable_post']['entries'][1].update(size=1061))
        run(str(index) + ':missing-dependency-declaration', 'dependency-inventory-completeness',
            lambda p, index=index: ex(p, index)['inventories']['dependency_post']['declared_references'].pop())
        run(str(index) + ':invented-dependency-hash', 'invented-dependency-bytes',
            lambda p, index=index: ex(p, index)['inventories']['dependency_pre']['declared_references'][0].update(sha256='a' * 64))
        run(str(index) + ':notice-wrong-hash', 'delivered-notice-evidence',
            lambda p, index=index: ex(p, index)['notice_evidence']['delivered'].update(sha256='b' * 64))
        run(str(index) + ':wrong-existing-citation', 'map-support',
            lambda p, index=index: ex(p, index)['original_output_map'][0]['output'][0].update(
                content_locator=context['method']['tasks'][4]['text_contract']['locator'].replace('build', 'major')))
        run(str(index) + ':false-preservation-relation', 'map-relation-truth',
            lambda p, index=index: ex(p, index)['original_output_map'][1]['comparison'].update(ranges=[[0, 20]]))
        run(str(index) + ':historical-raw-answer-credited', 'historical-answer-credit-or-provenance',
            lambda p, index=index: ex(p, index)['predecessor'].update(complete_map_credit_to_predecessor=True))
        run(str(index) + ':invented-native-log', 'unavailable-trial-evidence-promotion',
            lambda p, index=index: ex(p, index)['trial_artifact_accounting'][-1].update(status='authored-control-evidence'))
    run('mutated-original-bytes', 'mutated-original', mutate_context=lambda c: c.update(original=c['original'] + b'\n'))
    run('mutated-license-bytes', 'mutated-license', mutate_context=lambda c: c.update(license=c['license'] + b'\n'))
    run('wrong-output-object-hash', 'byte-object-hash',
        lambda p: p['byte_objects']['expected-project'].update(sha256='c' * 64))
    run('constant-exporter-no-change', 'expected-output-bytes',
        lambda p: p['byte_objects']['expected-project'].update(base64=base64.b64encode(context['original']).decode()))
    run('wrong-output-property-value', 'expected-output-bytes',
        lambda p: p['byte_objects']['expected-project'].update(base64=base64.b64encode(
            base64.b64decode(p['byte_objects']['expected-project']['base64']).replace(
                b'Name="Bld_version.build" Type="Int">3<', b'Name="Bld_version.build" Type="Int">4<')).decode()))
    run('unverified-extra-disappears', 'unverified-extra-retention',
        lambda p: ex(p, 1)['answer'].update(extra_assertions=[]))
    run('extra-assessment-incorrectly-correct', 'separate-assessment',
        lambda p: ex(p, 1)['prescriptions']['assessment'].update(answer_correctness='correct'))
    run('benchmark-ready-promotion', 'status-or-historical-credit-promotion', lambda p: p.update(benchmark_ready=True))
    run('F4-release-promotion', 'status-or-historical-credit-promotion', lambda p: p.update(F4_released=True))
    run('source-requirement-dropped', 'source-requirement-inventory', lambda p: p['requirement_inventory'].pop())
    run('dependency-closure-invented', 'dependency-closure-promotion',
        lambda p: ex(p)['inventories']['dependency_post'].update(transitive_closure='complete'))
    run('actual-isolation-invented', 'boundary-or-isolation-promotion',
        lambda p: ex(p)['boundaries'].update(actual_workspaces_allocated=True))

    def mutate_key(ctx, name, unblock=False):
        key = copy.deepcopy(ctx['key'])
        if unblock:
            next(x for x in key['required_ids'] if x['id'] == MAP)['established_key_use']['status'] = 'approved'
        else:
            ledger = next(x for x in key['claim_adjudication']['prescribed_ledgers'] if x['id'] == name)
            next(x for x in ledger['items'] if x['id'] == MAP).update(correctness='correct', grounding='correct')
        ctx['key'] = key

    for name in AFFECTED:
        run('historical-ledger-credit:' + name, 'historical-complete-map-credit',
            mutate_context=lambda c, name=name: mutate_key(c, name))
    run('historical-established-key-unblocked', 'historical-F4-block',
        mutate_context=lambda c: mutate_key(c, '', unblock=True))
    return results


def main():
    physical_errors = []
    for path, digest in FIXED.items():
        if sha(read(path)) != digest:
            physical_errors.append('fixed-pin:' + path)
    baseline = json.loads(read(PRE).decode().split('```json\n', 1)[1].split('```', 1)[0])
    for pin in baseline['protected_pins']:
        data = read(pin['path'])
        if (len(data), sha(data)) != (pin['bytes'], pin['sha256']):
            physical_errors.append('unchanged-file-pin:' + pin['path'])
    for pin in baseline['context_pin_checks']:
        path = REVIEW if pin['path'].startswith('.session/') else pin['path']
        data = read(path)
        if pin['match'] is not True or (len(data), sha(data)) != (pin['bytes'], pin['sha256']):
            physical_errors.append('context-pin:' + path)
    if physical_errors:
        print(json.dumps({'package_status': STATUS, 'check_status': 'failed', 'errors': physical_errors}))
        return 1
    package = json.loads(read(PACKAGE))
    context = {'method': json.loads(read(METHOD)), 'key': json.loads(read(KEY)),
               'review': json.loads(read(REVIEW)), 'baseline': baseline,
               'original': read(ORIGINAL), 'license': read(LICENSE)}
    errors = check_package(package, context)
    rejecting = controls(package, context)
    failed = [name for name, result in rejecting.items() if not result['passed']]
    expected, _, root = derive(context['method']['tasks'][4], context['original'])
    # A saved observation pins outputs without circularly pinning itself. Its
    # presence is optional for a fresh execution; when present its pins must match.
    if (ROOT / VERIFICATION).exists():
        observation = json.loads(read(VERIFICATION))
        for pin in observation['file_pins']:
            data = read(pin['path'])
            if (len(data), sha(data)) != (pin['bytes'], pin['sha256']):
                errors.append('saved-verification-pin:' + pin['path'])
        if (observation['command'] != 'python3 -I benchmark/writing/check_wp1_examples_0121.py'
                or observation['exit_code'] != 0):
            errors.append('saved-verification-command')
    ok = not errors and not failed
    summary = {
        'package_status': package['status'], 'checker_exit_code': 0 if ok else 1,
        'check_status': 'authored-example-consistency-with-F4-block-intact' if ok else 'failed',
        'revision': package['revision'], 'errors': sorted(set(errors)),
        'context_pins_checked': len(baseline['context_pin_checks']),
        'unchanged_file_pins_checked': len(baseline['protected_pins']),
        'requirement_source_records': len(source_requirements(context['method'], context['key'])),
        'expected_output_size': len(expected), 'expected_output_sha256': sha(expected),
        'declared_dependency_references': len(dependency_declarations(root, context['original'])),
        'materialized_dependencies': 0, 'dependency_closure': 'unavailable',
        'examples': [{'id': x['id'], 'map_relations': len(x['original_output_map']),
                      'preservation_IDs': x['prescriptions']['map_preservation_coverage'],
                      'assessment': x['prescriptions']['assessment']} for x in package['examples']],
        'rejecting_controls_passed': len(rejecting) - len(failed), 'rejecting_controls_total': len(rejecting),
        'rejecting_controls': rejecting, 'failed_controls': failed,
        'F4': 'blocked; not cleared', 'historical_example_map_slots': 'blocked-F4; partial/partial',
        'benchmark_ready': False, 'C1': 'open', 'agent_runs': 0, 'native_executions': 0,
        'actual_project_files_written': 0, 'independent_approval': 'pending',
        'file_sha256': {p: sha(read(p)) for p in FIXED},
        'checker_sha256': sha(Path(__file__).read_bytes()),
        'limits': 'Authored conditional controls only. No actual trial, native evidence, complete dependency closure, tested isolation, narrative adjudication, independent method acceptance or F4 release.'}
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, IndexError, TypeError, ET.ParseError) as exc:
        print(json.dumps({'package_status': STATUS, 'check_status': 'failed',
                          'errors': ['malformed-or-missing-evidence'], 'detail': str(exc)}))
        sys.exit(1)
