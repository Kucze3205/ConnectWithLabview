#!/usr/bin/env python3
"""Read-only, repository-only integrity check for the proposed 0123 extension.

Never imports/executes predecessor checkers or audits. Fixed authored examples only;
this is not independent narrative adjudication, native validation or readiness.
"""
import base64
import copy
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
WP = 'benchmark/writing/'
KEY = WP + 'wp1-key-0123.json'
BASE = WP + 'wp1-key-0119.json'
EXAMPLES = WP + 'wp1-examples-0121.json'
REVIEW = WP + 'wp1-examples-review-0122.json'
COLD = WP + 'wp1-examples-cold-0122.json'
METHOD = WP + 'method.json'
PROTOCOL = 'benchmark/protocol.md'
ORIGINAL = 'benchmark/real-project-0107/original.lvproj'
LICENSE = 'benchmark/real-project-0107/LICENSE.txt'
PIN_MANIFEST_SHA256 = 'cab26fceda72331871216f0c1fc83b5b76e3baace2efca0755f25eaade13ed05'
IDS = ['WP1-0121-positive-map-v1', 'WP1-0121-unverified-extra-map-v1']
PENDING = 'proposed-awaiting-separate-check'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def ref(path, locator):
    return {'path': path, 'locator': locator}


def repository_bytes(path):
    # Explicit repository roots only; no environment, staged input or artifact access.
    p = Path(path)
    if p.is_absolute() or '..' in p.parts or p.parts[0] not in ('benchmark', 'docs', 'goal'):
        raise ValueError('non-repository path: ' + path)
    target = ROOT / p
    if any((ROOT / Path(*p.parts[:i])).is_symlink() for i in range(1, len(p.parts) + 1)):
        raise ValueError('symlink: ' + path)
    return target.read_bytes()


def pointer(value, locator):
    if not locator.startswith('/'):
        raise ValueError('not a JSON pointer')
    for token in locator[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def leaves(value, locator):
    if isinstance(value, dict) and value:
        return [row for k, v in value.items() for row in leaves(v, locator + '/' + k.replace('~', '~0').replace('/', '~1'))]
    if isinstance(value, list) and value:
        return [row for i, v in enumerate(value) for row in leaves(v, locator + '/' + str(i))]
    return [{'path': METHOD, 'locator': locator, 'value': value}]


def source_requirements(method, protocol):
    # Derive from authoritative sources, never candidate source_requirements.
    return (leaves(method['common']['answer_rule'], '/common/answer_rule')
            + leaves(method['tasks'][4], '/tasks/4')
            + [{'path': PROTOCOL, 'locator': 'L' + str(i + 1), 'value': line}
               for i, line in enumerate(protocol.splitlines())
               if (25 <= i <= 40 and line.strip()) or i == 59])


def assess(required, extras):
    # Protocol L41 precedence, applied independently to each supplied dimension.
    if not required:
        return 'unverified'
    all_items = required + extras
    if 'incorrect' in all_items:
        return 'incorrect'
    if 'unverified' in all_items:
        return 'unverified'
    if all(x == 'correct' for x in all_items):
        return 'correct'
    if any(x in ('correct', 'partial') for x in all_items):
        return 'partial'
    if 'error' in all_items:
        return 'error'
    if all(x == 'unsupported' for x in required):
        return 'unsupported'
    return 'missing'


class Context:
    def __init__(self, pins):
        self.raw = {p['path']: repository_bytes(p['path']) for p in pins}
        self.docs = {p: json.loads(b) for p, b in self.raw.items() if p.endswith('.json')}
        self.old = self.docs[BASE]
        self.examples = self.docs[EXAMPLES]
        self.review = self.docs[REVIEW]
        self.cold = self.docs[COLD]
        self.method = self.docs[METHOD]
        self.task = self.method['tasks'][4]
        self.requirements = source_requirements(self.method, self.raw[PROTOCOL].decode())
        self.root = ET.fromstring(self.raw[ORIGINAL])
        self.urls = [(n.attrib['URL'], n.attrib['Type']) for n in self.root.iter() if 'URL' in n.attrib]
        self.byte_objects = {}
        for name, obj in self.examples['byte_objects'].items():
            data = base64.b64decode(obj['base64'], validate=True) if 'base64' in obj else self.raw[obj['path']]
            if len(data) != obj['size'] or sha(data) != obj['sha256']:
                raise ValueError('reviewed byte object integrity: ' + name)
            self.byte_objects[name] = data

    def resolve(self, link):
        path, loc = link['path'], link['locator']
        if path not in self.raw:
            raise ValueError('unpinned evidence path: ' + path)
        if path == ORIGINAL:
            prefix = 'element-child-index:'
            if not loc.startswith(prefix) or not loc.endswith('/@URL'):
                raise ValueError('unknown original locator')
            node = self.root
            for index in loc[len(prefix):].removesuffix('/@URL').strip('/').split('/'):
                node = list(node)[int(index)]
            value = node.attrib['URL']
            if link.get('value') != value or link.get('sha256') != sha(self.raw[ORIGINAL]):
                raise ValueError('wrong original declaration')
            return value
        if path.endswith('.json'):
            value = pointer(self.docs[path], loc)
        elif loc.startswith('L'):
            value = self.raw[path].decode().splitlines()[int(loc[1:]) - 1]
        else:
            raise ValueError('unknown evidence locator')
        for field in ('sha256', 'entries_sha256'):
            if field in link and (not isinstance(value, dict) or value.get(field) != link[field]):
                raise ValueError('wrong evidence digest')
        return value

    def resolve_links(self, value):
        count = 0
        if isinstance(value, dict):
            if 'path' in value and 'locator' in value:
                self.resolve(value)
                count += 1
            for item in value.values():
                count += self.resolve_links(item)
        elif isinstance(value, list):
            for item in value:
                count += self.resolve_links(item)
        return count


def check(key, ctx):
    errors = []
    def require(condition, code):
        if not condition and code not in errors:
            errors.append(code)
    old, package, review, task = ctx.old, ctx.examples, ctx.review, ctx.task
    try:
        require(set(key) == {'source_required_ids', 'status', 'source_requirements', 'next_review', 'revision', 'review_adoption', 'pins', 'verification_limits', 'case_id', 'schema_version', 'required_denominators', 'F3', 'issue', 'F4', 'composition', 'limits', 'starting_revision', 'new_examples', 'author', 'benchmark_ready'}, 'EXTENSION_SCHEMA')
        require(key['revision'] == 'wp1-key-0123-v1' and key['case_id'] == task['id'] and key['issue'] == 591, 'IDENTITY')
        require(key['status'] == PENDING and key['benchmark_ready'] is False, 'READINESS')
        require(key['author']['independent'] is False and key['author']['cold'] is False and key['author']['model_continuity'] == 'not certified', 'AUTHOR_PROVENANCE')
        comp = key['composition']
        excluded = ['schema_version', 'case_id', 'revision', 'issue', 'status', 'starting_revision', 'preparer', 'revision_provenance']
        require(comp['kind'] == 'operative-extension-by-pinned-reference' and comp['base_revision'] == old['revision'] and comp['base'] == next(p for p in key['pins'] if p['path'] == BASE), 'BASE')
        require(comp['inherited_operative_fields'] == [a for a in old if a not in excluded], 'INHERITANCE')
        require(key['source_requirements'] == ctx.requirements, 'SOURCE_REQUIREMENTS')
        require(key['source_required_ids'] == {a: task[a] for a in ('semantic_ids', 'preservation_ids', 'answer_ids')}, 'REQUIRED_IDS')
        den = {'artifact_semantic': len(task['semantic_ids']), 'preservation': len(task['preservation_ids']), 'answer_correctness': len(task['answer_ids']), 'source_grounding': len(task['answer_ids']), 'reading_fidelity': None}
        require(key['required_denominators'] == den, 'DENOMINATORS')
        require(key['F3'] == {'disposition': 'unchanged-by-reference; no replay', 'reference': ref(BASE, '/finding_dispositions/F3')}, 'F3_REFERENCE')
        adopt = key['review_adoption']
        require(adopt['reviewed_identity'] == review['review_identity'] and adopt['cold_provenance'] == review['cold_provenance'] and adopt['cold_record_provenance'] == ctx.cold['provenance'], 'REVIEW_PROVENANCE')
        require(adopt['standards'] == review['standards_assessment']['verdict'] == 'CLEAR' and adopt['spec'] == review['spec_assessment']['verdict'] == 'CLEAR', 'REVIEW_SCOPE')
        require(adopt['scope'] == 'conditional preparation examples only' and adopt['review_releases_F4'] is False and adopt['review_grants_readiness'] is False and adopt['replayed'] is False, 'REVIEW_SCOPE')
        require(adopt['reviewed_HEAD_equals_author_HEAD'] is False and adopt['scoped_bytes_agree'] is True, 'REVIEW_IDENTITY')
        require(review['recommendation']['F4_released_by_this_review'] is False and review['recommendation']['benchmark_ready'] is False and review['recommendation']['adequate_evidence_for_later_separate_key_revision_to_consider_F4_release'] is True, 'PRESERVED_REVIEW_SCOPE')
        for field, path in [('review', REVIEW), ('cold', COLD)]:
            require(adopt[field] == next(p for p in key['pins'] if p['path'] == path), 'REVIEW_PIN')
        require(sha(canonical(key['pins'])) == PIN_MANIFEST_SHA256, 'PIN_MANIFEST')
        historical = key['F4']['historical']
        require(historical == {'disposition_reference': ref(BASE, '/finding_dispositions/F4'), 'required_id_block_reference': ref(BASE, '/required_ids/6/established_key_use'), 'status': 'blocked-for-missing-evidence', 'map_outcomes': {'correctness': 'partial', 'grounding': 'partial'}, 'slots': [ref(BASE, '/claim_adjudication/prescribed_ledgers/0'), ref(BASE, '/claim_adjudication/prescribed_ledgers/2')], 'established_key_use': 'blocked'}, 'HISTORICAL_BLOCK')
        require(old['required_ids'][6]['established_key_use']['status'] == 'blocked' and old['finding_dispositions']['F4']['status'] == 'blocked-for-missing-evidence', 'BASE_BLOCK')
        for slot, historical_id in [(0, 'C1-correct'), (2, 'C1-unverified-extra')]:
            ledger = old['claim_adjudication']['prescribed_ledgers'][slot]
            item = next(x for x in ledger['items'] if x['id'] == 'WP1-original-output-grounding')
            require(ledger['id'] == historical_id and item['correctness'] == item['grounding'] == 'partial' and item['established_key_use'] == 'blocked-F4', 'HISTORICAL_SLOT')
            raw_answer = ctx.resolve(ledger['raw_answer_reference'])
            require(sha(raw_answer.encode()) == ledger['evidence_reservation']['raw_answer_utf8_sha256'], 'HISTORICAL_RAW')
        f4 = key['F4']
        conditional = f4['conditional']
        require(conditional['ids'] == IDS and conditional['status'] == 'proposed-conditional-clearance-awaiting-separate-check' and conditional['released'] is False and conditional['separate_review_required'] is True and conditional['map_outcomes'] == {'correctness': 'correct', 'grounding': 'correct'}, 'CONDITIONAL_F4')
        require(f4['general_established_key_use'] == 'blocked' and f4['full_trial_release'] is False and f4['benchmark_ready'] is False, 'GENERAL_RELEASE')
        require([x['id'] for x in key['new_examples']] == IDS, 'EXAMPLE_IDENTITIES')
        for i, example in enumerate(key['new_examples']):
            source = package['examples'][i]
            prefix = '/examples/' + str(i)
            require(example['id'] == source['id'] == IDS[i] and example['identity_type'] == 'new-authored-preparation-control', 'NEW_ID')
            require(example['conditions'] == source['conditions'], 'CONDITIONS')
            require(example['historical_predecessor'] == source['predecessor'] and example['complete_map_credit_to_historical_answer'] is False, 'NO_HISTORICAL_CREDIT')
            for field, suffix in [('evidence', ''), ('answer_reference', '/answer'), ('inventories_reference', '/inventories'), ('boundaries_reference', '/boundaries'), ('notice_reference', '/notice_evidence')]:
                require(example[field] == ref(EXAMPLES, prefix + suffix), 'OPERATIVE_LINKS')
            require(example['answer_utf8_json_sha256'] == sha(canonical(source['answer'])), 'ANSWER_IDENTITY')
            require(example['review_assessment'] == ref(REVIEW, '/answer_assessments/' + str(i)), 'REVIEW_LINK')
            require(example['map_dimension_tests'] == old['required_ids'][6]['separate_dimension_tests'], 'DIMENSION_TESTS')
            maps = example['operative_map']
            require([x['id'] for x in maps] == task['semantic_ids'] + task['preservation_ids'], 'MAP_COVERAGE')
            for j, row in enumerate(maps):
                expected = copy.deepcopy(source['original_output_map'][j])
                expected['agreement'] = 'proposed-key-incorporation-awaiting-separate-check'
                expected['review_evidence'] = ref(REVIEW, '/per_id_table/' + str(i * 5 + j))
                expected['operative_source'] = ref(EXAMPLES, prefix + '/original_output_map/' + str(j))
                require(row == expected, 'MAP_SOURCE')
                require(row['correctness_prescription'] == 'correct' and row['grounding_prescription'] == 'correct', 'MAP_DIMENSIONS')
                reviewed = ctx.resolve(row['review_evidence'])
                require(reviewed['example'] == example['id'] and reviewed['id'] == row['id'] and reviewed['correctness']['agreement'] == reviewed['grounding']['agreement'] == 'agree', 'MAP_REVIEW')
            prescribed = example['prescriptions']
            require(prescribed == source['prescriptions'], 'PRESCRIPTION_SOURCE')
            require(prescribed['status'] == PENDING and prescribed['not_executable_narrative_scoring'] is True, 'PRESCRIPTION_SCOPE')
            require(prescribed['required_items'] == [{'id': item, 'correctness': 'correct', 'grounding': 'correct'} for item in task['answer_ids']], 'REQUIRED_PRESCRIPTIONS')
            require(prescribed['map_preservation_coverage'] == task['preservation_ids'], 'PRESERVATION_COVERAGE')
            extras = source['answer']['extra_assertions']
            require(prescribed['extras'] == extras and prescribed['contradictions'] == prescribed['duplicates'] == [], 'EXTRAS')
            if i == 1:
                require(len(prescribed['extras']) == 1 and prescribed['extras'][0]['assertion'] == 'Startup time decreases 10 percent' and prescribed['extras'][0]['correctness'] == 'unverified' and prescribed['extras'][0]['grounding'] == 'missing' and prescribed['extras'][0]['citations'] == [], 'UNVERIFIED_EXTRA')
            else:
                require(prescribed['extras'] == [], 'POSITIVE_EXTRAS')
            for dimension, assessment_field in [('correctness', 'answer_correctness'), ('grounding', 'source_grounding')]:
                outcome = assess([x[dimension] for x in prescribed['required_items']], [x[dimension] for x in prescribed['extras']])
                require(prescribed['assessment'][assessment_field] == outcome, 'ASSESSMENT_' + dimension.upper())
            deps = example['unavailable_dependency_references']
            require(deps == source['inventories']['dependency_pre']['declared_references'], 'DEPENDENCY_SOURCE')
            require([(d['path'], d['kind']) for d in deps] == ctx.urls, 'DEPENDENCY_DECLARATIONS')
            require(all(d['status'] == 'unavailable' and d['size'] is None and d['sha256'] is None and d['raw_byte_reference'] is None and bool(d['reason']) for d in deps), 'DEPENDENCY_LIMITS')
            accounting = example['trial_artifact_accounting']
            require([x['id'] for x in accounting] == task['trial_artifacts']['required'] and accounting == source['trial_artifact_accounting'], 'TRIAL_ACCOUNTING')
            require(all(x['status'] == 'unavailable' and x['evidence'] is None and x['reason'] for x in accounting[7:]), 'TRIAL_UNAVAILABLE')
            try:
                ctx.resolve_links(example)
            except (ValueError, KeyError, TypeError, IndexError):
                require(False, 'EVIDENCE_RESOLUTION')
        limits = key['limits']
        require(limits['claims_and_gaps'] == package['claims_and_gaps'] and limits['native_and_trial_results'] == task['planned_results'], 'LIMITS')
        require(limits['root_version_authority'] == task['preservation']['root_version_authority'] == 'declaration-only' and limits['materialized_dependency_files'] == 0 and limits['dependency_declarations'] == len(ctx.urls), 'NATIVE_DEPENDENCY_LIMITS')
        require(limits['unavailable_trial_categories'] == task['trial_artifacts']['required'][7:], 'UNAVAILABLE_CATEGORIES')
        require(limits['trial_and_key_readiness'] == limits['owner_acceptance'] == 'pending' and limits['conditional_evidence_is_trial_evidence'] is False, 'TRIAL_READINESS')
        ctx.resolve_links(key['F3'])
        ctx.resolve_links(key['F4'])
    except (KeyError, ValueError, TypeError, IndexError, StopIteration) as exc:
        errors.append('MALFORMED:' + type(exc).__name__)
    return errors


def source_evidence_checks(ctx):
    # Bounded source/byte checks support incorporation; no historical code is run.
    task = ctx.task
    original = ctx.raw[ORIGINAL]
    output = ctx.byte_objects['expected-project']
    delta = task['text_contract']['delta']
    nodes = ctx.root.findall(task['text_contract']['locator'])
    assert len(nodes) == task['preconditions'][0]['match_count'] == 1
    assert nodes[0].attrib == task['preconditions'][0]['property_attributes'] and nodes[0].text == delta['before']
    offset = delta['offset_zero_based']
    assert len(original) == len(output) == delta['output_size']
    assert original[offset:offset + 1] == bytes.fromhex(delta['removed_hex'])
    assert output == original[:offset] + bytes.fromhex(delta['inserted_hex']) + original[offset + 1:]
    assert ET.fromstring(output).attrib == ctx.root.attrib == task['preconditions'][0]['root_attributes']
    assert len(ctx.urls) == 11
    for example in ctx.examples['examples']:
        inventories = example['inventories']
        for inventory in inventories.values():
            entries = inventory['entries']
            assert inventory['file_count'] == len(entries)
            assert inventory['entries_sha256'] == sha(canonical(entries))
            for entry in entries:
                data = ctx.byte_objects[entry['byte_object']]
                assert len(data) == entry['size'] and sha(data) == entry['sha256']
                assert ctx.resolve(entry['raw_byte_reference']) == ctx.examples['byte_objects'][entry['byte_object']]
        for name in ('dependency_pre', 'dependency_post'):
            inv = inventories[name]
            assert inv['entries'] == [] and inv['transitive_closure'] == 'unavailable' and inv['resolution'] == 'unexecuted'
            assert [(x['path'], x['kind']) for x in inv['declared_references']] == ctx.urls
        assert inventories['immutable_pre']['entries'] == inventories['immutable_post']['entries']
        assert inventories['immutable_pre']['writable'] is inventories['immutable_post']['writable'] is False
        assert inventories['workspace_pre']['entries'][1] == inventories['workspace_post']['entries'][1]
        assert inventories['delivered']['entries'] == inventories['workspace_post']['entries']
        assert example['boundaries']['actual_workspaces_allocated'] is False
        assert example['boundaries']['cross_root_links'] == []
    for row in ctx.review['pins_observed']:
        data = ctx.raw[row['path']]
        assert sha(data) == row['sha256'] and len(data) == row['bytes']
    assert ctx.review['cold_provenance']['procedural_deviations']
    assert ctx.review['review_identity']['model_limitation']
    assert ctx.cold['observed']['head'] == ctx.review['review_identity']['observed_head']


def controls(key, ctx):
    results = []
    def exercise(name, change, expected):
        changed = copy.deepcopy(key)
        change(changed)
        observed = check(changed, ctx)
        results.append({'name': name, 'expected_error': expected, 'actual_errors': observed, 'rejected_as_expected': expected in observed})
    def set_path(path, value):
        def change(k):
            obj = k
            for token in path[:-1]:
                obj = obj[token]
            obj[path[-1]] = value
        return change
    for i in range(2):
        p = ['new_examples', i]
        for j in range(1, 5):
            exercise('drop-preservation-map-' + str(i) + '-' + str(j), lambda k, i=i, j=j: k['new_examples'][i]['operative_map'].pop(j), 'MAP_COVERAGE')
        exercise('wrong-existing-property-' + str(i), set_path(p + ['operative_map', 0, 'original', 0, 'content_locator'], "Bld_version.major; line 43"), 'MAP_SOURCE')
        exercise('wrong-example-map-link-' + str(i), set_path(p + ['inventories_reference'], ref(EXAMPLES, '/examples/' + str(1-i) + '/inventories')), 'OPERATIVE_LINKS')
        exercise('unresolvable-map-evidence-' + str(i), set_path(p + ['operative_map', 0, 'original', 0, 'locator'], '/byte_objects/absent'), 'EVIDENCE_RESOLUTION')
        exercise('drop-condition-' + str(i), set_path(p + ['conditions'], ''), 'CONDITIONS')
        exercise('historical-credit-' + str(i), set_path(p + ['complete_map_credit_to_historical_answer'], True), 'NO_HISTORICAL_CREDIT')
        exercise('weaken-grounding-test-' + str(i), set_path(p + ['map_dimension_tests', 'grounding'], 'existing path suffices'), 'DIMENSION_TESTS')
        for dimension in ('correctness', 'grounding'):
            exercise('alter-map-' + dimension + '-' + str(i), set_path(p + ['prescriptions', 'required_items', 1, dimension], 'partial'), 'REQUIRED_PRESCRIPTIONS')
        exercise('invent-dependency-hash-' + str(i), set_path(p + ['unavailable_dependency_references', 0, 'sha256'], '0' * 64), 'DEPENDENCY_LIMITS')
        exercise('drop-dependency-' + str(i), lambda k, i=i: k['new_examples'][i]['unavailable_dependency_references'].pop(), 'DEPENDENCY_DECLARATIONS')
        exercise('invent-native-log-' + str(i), set_path(p + ['trial_artifact_accounting', 12, 'status'], 'passed'), 'TRIAL_UNAVAILABLE')
        exercise('relabel-historical-' + str(i), set_path(p + ['id'], ['C1-correct', 'C1-unverified-extra'][i]), 'NEW_ID')
    mutations = [
        ('inject-historical-override', ['historical_ledgers'], [], 'EXTENSION_SCHEMA'),
        ('promote-readiness', ['benchmark_ready'], True, 'READINESS'),
        ('release-conditional-F4', ['F4', 'conditional', 'released'], True, 'CONDITIONAL_F4'),
        ('skip-separate-review', ['F4', 'conditional', 'separate_review_required'], False, 'CONDITIONAL_F4'),
        ('release-general-key', ['F4', 'general_established_key_use'], 'clear', 'GENERAL_RELEASE'),
        ('release-full-trial', ['F4', 'full_trial_release'], True, 'GENERAL_RELEASE'),
        ('unblock-historical', ['F4', 'historical', 'established_key_use'], 'clear', 'HISTORICAL_BLOCK'),
        ('promote-historical-map', ['F4', 'historical', 'map_outcomes', 'correctness'], 'correct', 'HISTORICAL_BLOCK'),
        ('erase-review-deviations', ['review_adoption', 'cold_provenance', 'procedural_deviations'], [], 'REVIEW_PROVENANCE'),
        ('claim-independent', ['author', 'independent'], True, 'AUTHOR_PROVENANCE'),
        ('native-version-authority', ['limits', 'root_version_authority'], 'native', 'NATIVE_DEPENDENCY_LIMITS'),
        ('trial-evidence-promotion', ['limits', 'conditional_evidence_is_trial_evidence'], True, 'TRIAL_READINESS'),
        ('remove-unavailable-category', ['limits', 'unavailable_trial_categories'], [], 'UNAVAILABLE_CATEGORIES'),
        ('native-validity-promotion', ['limits', 'native_and_trial_results', 'native_validity'], 'passed', 'LIMITS'),
        ('remove-extra', ['new_examples', 1, 'prescriptions', 'extras'], [], 'EXTRAS'),
        ('credit-extra', ['new_examples', 1, 'prescriptions', 'extras', 0, 'correctness'], 'correct', 'UNVERIFIED_EXTRA'),
        ('support-extra', ['new_examples', 1, 'prescriptions', 'extras', 0, 'grounding'], 'correct', 'UNVERIFIED_EXTRA'),
        ('promote-extra-correctness', ['new_examples', 1, 'prescriptions', 'assessment', 'answer_correctness'], 'correct', 'ASSESSMENT_CORRECTNESS'),
        ('promote-extra-grounding', ['new_examples', 1, 'prescriptions', 'assessment', 'source_grounding'], 'correct', 'ASSESSMENT_GROUNDING'),
        ('change-denominator', ['required_denominators', 'source_grounding'], 2, 'DENOMINATORS'),
        ('remove-source-requirements', ['source_requirements'], [], 'SOURCE_REQUIREMENTS'),
        ('change-F3', ['F3', 'disposition'], 'revised', 'F3_REFERENCE'),
        ('omit-base-obligations', ['composition', 'inherited_operative_fields'], [], 'INHERITANCE'),
        ('forge-review-pin', ['review_adoption', 'review', 'sha256'], '0' * 64, 'REVIEW_PIN'),
    ]
    for name, path, value, expected in mutations:
        exercise(name, set_path(path, value), expected)
    return results


def main():
    try:
        key = json.loads(repository_bytes(KEY))
        if sha(canonical(key['pins'])) != PIN_MANIFEST_SHA256:
            raise ValueError('protected pin manifest differs')
        ctx = Context(key['pins'])
        pin_errors = [p['path'] for p in key['pins'] if len(ctx.raw[p['path']]) != p['bytes'] or sha(ctx.raw[p['path']]) != p['sha256']]
        if pin_errors:
            raise ValueError('pinned bytes differ: ' + repr(pin_errors))
        source_evidence_checks(ctx)
        errors = check(key, ctx)
        results = controls(key, ctx)
        failed = [x['name'] for x in results if not x['rejected_as_expected']]
        report = {'status': 'proposed-key-integrity-with-historical-F4-block-intact' if not errors and not failed else 'failed', 'errors': errors, 'failed_controls': failed, 'rejecting_controls_passed': sum(x['rejected_as_expected'] for x in results), 'rejecting_controls_total': len(results), 'source_requirement_records': len(ctx.requirements), 'pinned_files_checked': len(key['pins']), 'new_examples': IDS, 'historical_map_slots': 'partial/partial; blocked-F4', 'conditional_F4': 'proposed only; separate review pending', 'benchmark_ready': False, 'independent_semantic_approval': False, 'controls': results}
        print(json.dumps(report, sort_keys=True))
        return 1 if errors or failed else 0
    except (AssertionError, ValueError, KeyError, TypeError, OSError, IndexError) as exc:
        print(json.dumps({'status': 'failed', 'cause': type(exc).__name__ + ': ' + str(exc)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
