#!/usr/bin/env python3
"""Deterministic public development scoring; no native reader is executed.

Computation receives only submissions, probes, frozen denominators, inventory keys
and alignment facts. Authored expected outcomes enter only the comparison stage.
XML credit is conditional on the provisional key; current-evidence credit is
reported separately. This same-role-family implementation is unreviewed.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'benchmark/results/challenges.json'
FIXTURES = ('library-icon-tests', 'library-specialty', 'vi-actor-core-native-gap')
DIMS = {'correctness': 'answer_correctness', 'grounding': 'source_grounding',
        'fidelity': 'reading_fidelity'}
CATEGORIES = ('correct', 'partial', 'incorrect', 'missing', 'unsupported', 'unverified', 'error')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def counts(values):
    values = list(values)
    return {x: values.count(x) for x in CATEGORIES}


def assessment(required, extras):
    if not required:
        return 'unverified'
    values = list(required) + list(extras)
    for outcome in ('incorrect', 'unverified'):
        if outcome in values:
            return outcome
    if all(x == 'correct' for x in values):
        return 'correct'
    if any(x in ('correct', 'partial') for x in values):
        return 'partial'
    if 'error' in values:
        return 'error'
    if all(x == 'unsupported' for x in required):
        return 'unsupported'
    return 'missing'


def raw_record(record, materialized, label, problems, allow_incomplete=False):
    text = record['text']
    if digest(text.encode('utf-8')) != record['sha256']:
        problems.append(label + ': raw SHA256 mismatch')
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        if not allow_incomplete:
            problems.append(label + ': invalid raw JSON')
        return None
    if parsed != materialized:
        problems.append(label + ': raw and materialized content disagree')
    return parsed


def citation_support(citations, key):
    # Whole citation identities, including original hash and exact property,
    # must match a keyed supporting locator. Existence alone earns no credit.
    if not citations:
        return 'missing'
    if not key.get('citations'):
        return 'unverified'
    return 'correct' if all(c in key['citations'] for c in citations) else 'incorrect'


STEP = re.compile(r'^([A-Za-z_][\w.-]*)(?:\[(\d+)\])?$')
MANIFEST = {}


def resolve_locator(root, locator):
    # Copied from benchmark/challenges/check_xml_keys.py resolve (that file's SHA256 is pinned
    # elsewhere and must not change). Evaluates /Root/Child[n]/.../(@Attr|text()).
    parts = locator.strip('/').split('/')
    if not parts or parts[0] != root.tag:
        raise ValueError('root mismatch')
    node = root
    for part in parts[1:-1]:
        m = STEP.match(part)
        if not m:
            raise ValueError('bad step ' + part)
        tag, idx = m.group(1), int(m.group(2) or 1)
        kids = [k for k in node if k.tag == tag]
        if idx < 1 or idx > len(kids):
            raise ValueError('no element ' + part)
        node = kids[idx - 1]
    last = parts[-1] if len(parts) > 1 else None
    if last is None:
        raise ValueError('locator has no leaf')
    if last.startswith('@'):
        name = last[1:]
        if name not in node.attrib:
            raise ValueError('no attribute ' + name)
        return node.attrib[name]
    if last == 'text()':
        return node.text
    raise ValueError('unsupported leaf ' + last)


def manifest_pins():
    # repository name -> (pinned commit, set of inventoried artifact paths) from benchmark/sources.json
    if not MANIFEST:
        data = json.loads((ROOT / 'benchmark/sources.json').read_bytes())
        for repo in data['repositories']:
            MANIFEST[repo['name']] = (repo['commit'], {a['path'] for a in repo['artifacts']})
    return MANIFEST


def environment_loader(citation):
    # Original bytes of a cited artifact: benchmark/sources.json must list the repository at the
    # cited commit and the path; bytes are read from $LABVIEW_ENVIRONMENT/<repository>/<path>
    # (the layout benchmark/scripts/sources.py reads). Anything unreachable returns None.
    location = os.environ.get('LABVIEW_ENVIRONMENT')
    if not location:
        return None
    try:
        commit, paths = manifest_pins()[citation['repository']]
        if (citation['commit'] != commit or citation['path'] not in paths
                or citation.get('archive_member_chain')):
            return None
        relative = Path(citation['path'])
        if relative.is_absolute() or '..' in relative.parts:
            return None
        current = Path(location) / citation['repository']
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                return None
        return current.read_bytes() if current.is_file() else None
    except (KeyError, TypeError, OSError, ValueError):
        return None


def citation_resolves(citation, literal, artifact, load_bytes):
    # Opens the cited original and evaluates the submitted locator. Only adds failures:
    # `incorrect` for a wrong artifact, unresolvable locator or text differing from the literal;
    # `unverified` when the scheme is unsupported or the bytes are unreachable.
    try:
        scheme = citation['locator']['scheme']
        expression = citation['locator']['expression']
    except (KeyError, TypeError):
        return 'unverified'
    if scheme != 'xml-positional-path':
        return 'unverified'
    data = load_bytes(citation)
    if data is None:
        return 'unverified'
    if digest(data) != citation.get('sha256') or citation.get('sha256') != artifact.get('sha256'):
        return 'incorrect'
    try:
        got = resolve_locator(ET.fromstring(data), expression)
    except (ValueError, ET.ParseError):
        return 'incorrect'
    return 'correct' if got == literal else 'incorrect'


def citations_resolve(citations, literal, artifact, load_bytes):
    if not citations:
        return 'missing'
    return assessment([citation_resolves(c, literal, artifact, load_bytes) for c in citations], [])


def combine_grounding(support, resolution):
    # Any `incorrect` wins, `unverified` blocks `correct`; resolution never upgrades the key match.
    for outcome in ('incorrect', 'unverified'):
        if outcome in (support, resolution):
            return outcome
    return support if support != 'correct' else resolution


def condition_policy(records, key, identifier, condition_ledger):
    keyed_conditions = set(key.get("conditions", []))
    unsupported = missing = False
    for record, pointer in records:
        submitted_conditions = record.get("conditions", [])
        missing |= bool(keyed_conditions - set(submitted_conditions))
        seen_conditions = set()
        for index, condition in enumerate(submitted_conditions):
            if condition not in keyed_conditions:
                unsupported = True
                if condition not in seen_conditions:
                    condition_ledger.append({"claim_id": identifier, "condition": condition,
                        "raw_json_pointer": pointer + "/conditions/" + str(index)})
                    seen_conditions.add(condition)
    return unsupported, missing


def extra_outcome(item, channel, keys, key_absent, pointer, condition_ledger, artifact, load_bytes):
    value = item.get('answer' if channel == 'answer' else 'value')
    match = re.fullmatch(r'The XML-parsed literal at (.+) has UTF-8 byte length (\d+)\.', value or '')
    key = None
    if match:
        scope, length = match.groups()
        for candidate in keys.values():
            if any(c.get('locator', {}).get('expression') == scope for c in candidate.get('citations', [])):
                key = candidate
                break
        if key is not None and isinstance(key['atomic_fact'].get('value'), str) and not key_absent:
            actual = len(key['atomic_fact']['value'].encode('utf-8'))
            correct = int(length) == actual
            if channel == 'reader':
                outcomes = {'fidelity': 'unverified' if correct else 'incorrect'}
            else:
                grounding = combine_grounding(
                    citation_support(item.get('citations', []), key),
                    citations_resolve(item.get('citations', []), key['atomic_fact']['value'],
                                      artifact, load_bytes))
                outcomes = {'correctness': 'correct' if correct else 'incorrect',
                            'grounding': grounding if correct else 'incorrect'}
                unsupported, missing = condition_policy(
                    [(item, pointer)], key, item["claim_id"], condition_ledger)
                for dimension, outcome in outcomes.items():
                    if unsupported:
                        outcomes[dimension] = "incorrect"
                    elif missing and outcome == "correct":
                        outcomes[dimension] = "partial"
            return outcomes, {'actual_byte_length': actual, 'utf8_literal': key['atomic_fact']['value']}
    return ({'fidelity': 'unverified'} if channel == 'reader' else
            {'correctness': 'unverified', 'grounding': 'unverified'}), None


def compute(source, denominators, inventory, submitted, probe, alignment, load_bytes=None):
    # load_bytes(citation) returns the cited original's bytes or None; default reads the prepared
    # environment. Controls inject their own loader so they need no real sources.
    load_bytes = load_bytes or environment_loader
    artifact = source.get('artifact') or {}
    problems = []
    answer = submitted['answer_record']
    response = submitted['reader_response']
    operation = probe['simulated_operation']
    raw_record(submitted['raw_answer_record'], answer, 'answer', problems)
    parsed = raw_record(submitted['raw_reader_response'], response, 'reader', problems,
                        allow_incomplete=operation.get('truncated') or not submitted['raw_reader_response']['text'])
    request = probe['raw_request'].encode('utf-8')
    if digest(request) != probe['raw_request_sha256'] or json.loads(request) != probe['request']:
        problems.append('probe: raw request identity mismatch')
    # Incomplete raw bytes supply no invented observations. Simulated conditions
    # are retained as operational evidence, never represented as native runs.
    observations = parsed.get('observations', []) if isinstance(parsed, dict) else []
    keys = {k['claim_id']: k for k in inventory['reference_inventory']}
    align = {a['observation_id']: {k: a[k] for k in
             ('aligned_claim_id', 'native_reference', 'reference_scope', 'xml_expected')} for a in alignment}
    required = {d: denominators[name]['required_ids'] for d, name in DIMS.items()}
    for d, name in DIMS.items():
        if len(set(required[d])) != denominators[name]['count'] or len(required[d]) != len(set(required[d])):
            problems.append(d + ': invalid frozen denominator')
    evidence_record = submitted.get('evidence_record', {})
    key_absent = 'independent_key' in evidence_record and evidence_record['independent_key'] is None
    execution = probe['actual_execution']
    per_id = {d: {} for d in DIMS}
    extras, duplicates, contradictions = [], [], []
    condition_ledger = []
    details = {d: {} for d in DIMS}

    for channel, items, id_field, value_field, dimensions in (
        ('answer', answer.get('claims', []), 'claim_id', 'answer', ('correctness', 'grounding')),
        ('reader', observations, 'observation_id', 'value', ('fidelity',))):
        groups = {}
        prefix = '/claims/' if channel == 'answer' else '/observations/'
        for index, item in enumerate(items):
            identifier = item[id_field]
            pointer = prefix + str(index)
            if identifier not in required[dimensions[0]]:
                outcomes, derivation = extra_outcome(
                    item, channel, keys, key_absent, pointer, condition_ledger, artifact, load_bytes)
                entry = {'channel': channel, 'assertion_id': identifier, 'assertion': item.get(value_field),
                         'raw_json_pointer': pointer, 'outcomes': outcomes, 'required_credit': 0,
                         'derivation': derivation}
                extras.append(entry)
            else:
                groups.setdefault(identifier, []).append((item, pointer))
        status = answer.get('status') if channel == 'answer' else response.get('status')
        for identifier in required[dimensions[0]]:
            records = groups.get(identifier, [])
            values = [record[value_field] for record, _ in records]
            unique = {json.dumps(v, sort_keys=True) for v in values}
            duplicate_count = len(values) - len(unique)
            contradiction = len(unique) > 1
            if duplicate_count:
                duplicates.append({'channel': channel, 'required_id': identifier, 'count': duplicate_count,
                                   'raw_json_pointers': [p for _, p in records]})
            if contradiction:
                contradictions.append({'channel': channel, 'required_id': identifier, 'count': 1,
                                       'raw_json_pointers': [p for _, p in records], 'assertions': values})
            if channel == 'answer':
                key = keys.get(identifier)
                target = key['atomic_fact'].get('value') if key else None
                native = key.get('native_reference', 'unavailable') if key else 'unavailable'
            else:
                key = align.get(identifier)
                target = key['xml_expected'] if key else None
                native = key.get('native_reference', 'unavailable') if key else 'unavailable'
            unsupported_conditions = missing_conditions = False
            if channel == 'answer' and key is not None:
                unsupported_conditions, missing_conditions = condition_policy(
                    records, key, identifier, condition_ledger)
            common = None
            if contradiction or unsupported_conditions:
                common = 'incorrect'
            elif status == 'unsupported' and not records:
                common = 'unsupported'
            elif channel == 'reader' and (status == 'error' or operation.get('error') or operation.get('exit_code')) and not records:
                common = 'error'
            elif not records:
                common = 'missing'
            elif key_absent or key is None or target is None:
                common = 'unverified'
            elif any(v != target for v in values):
                common = 'incorrect'
            elif channel == 'reader' and any(r.get('scope') != key['reference_scope'] for r, _ in records):
                common = 'incorrect'
            elif channel == 'reader' and native == 'unavailable':
                common = 'unverified'
            elif (execution.get('executed', 0) <= 0 or execution.get('scored', 0) <= 0 or
                  ('native_run' in evidence_record and evidence_record['native_run'] is None)):
                # Zero executed or scored work, or a missing native run, earns no credit.
                common = 'unverified'
            else:
                common = 'correct'
            for dimension in dimensions:
                outcome = common
                if dimension == 'grounding' and common == 'correct':
                    supports = [combine_grounding(citation_support(r.get('citations', []), key),
                                                  citations_resolve(r.get('citations', []), target,
                                                                    artifact, load_bytes))
                                for r, _ in records]
                    outcome = assessment(supports, [])
                if missing_conditions and outcome == 'correct':
                    outcome = 'partial'
                per_id[dimension][identifier] = outcome
                details[dimension][identifier] = {'outcome': outcome, 'submitted_values': values,
                    'reference_value': target, 'native_reference': native,
                    'raw_json_pointers': [p for _, p in records]}

    extra_values = {d: [e['outcomes'][d] for e in extras if d in e['outcomes']] for d in DIMS}
    dimensions = {d: assessment(per_id[d].values(), extra_values[d]) for d in DIMS}
    # Independent XML review is unavailable: conditional matches are not current
    # evidence passes. Explicit falsifications remain visible in both views.
    current = {d: {i: ('unverified' if v == 'correct' else v) for i, v in ids.items()}
               for d, ids in per_id.items()}
    current_dimensions = {d: assessment(current[d].values(),
                           ['unverified' if v == 'correct' else v for v in extra_values[d]]) for d in DIMS}
    return {'per_id': per_id, 'dimensions': dimensions,
            'counts': {d: counts(per_id[d].values()) for d in DIMS},
            'required_ids': required, 'fixed_denominators': {d: len(required[d]) for d in DIMS},
            'extra_counts': {d: counts(extra_values[d]) for d in DIMS},
            'condition_ledger': condition_ledger,
            'extras_ledger': extras, 'duplicates_ledger': duplicates, 'contradictions_ledger': contradictions,
            'current_evidence_per_id': current, 'current_evidence_dimensions': current_dimensions,
            'details': details, 'cannot_evaluate_reasons': problems,
            'operation': operation, 'limitations': {'answer': answer.get('limitations'),
            'reader': response.get('limitations')}, 'declared_execution': probe['actual_execution'],
            'evidence_record': evidence_record}


def ledger_projection(entries, kind):
    if kind == 'condition_ledger':
        fields = ('claim_id', 'condition', 'raw_json_pointer')
    elif kind == 'extras_ledger':
        fields = ('channel', 'assertion_id', 'assertion', 'raw_json_pointer', 'outcomes', 'required_credit', 'derivation')
    else:
        fields = ('channel', 'required_id', 'count', 'raw_json_pointers')
    return [{k: e[k] for k in fields if k in e} for e in entries]


def compare(computed, expected):
    mismatches = []
    fields = ('per_id', 'dimensions', 'counts', 'required_ids', 'fixed_denominators', 'extra_counts',
              'current_evidence_per_id', 'current_evidence_dimensions',
              'condition_ledger', 'extras_ledger', 'duplicates_ledger', 'contradictions_ledger')
    def walk(actual, wanted, path):
        if isinstance(actual, dict) and isinstance(wanted, dict):
            for key in sorted(set(actual) | set(wanted)):
                walk(actual.get(key), wanted.get(key), path + '/' + key)
        elif actual != wanted:
            mismatches.append({'location': path, 'computed': actual, 'expected': wanted,
                               'reason': 'Independently computed submission/key result differs from frozen expectation.'})
    for field in fields:
        actual = computed[field]
        wanted = expected.get(field, []) if field == 'condition_ledger' else expected[field]
        if field.endswith('_ledger'):
            actual, wanted = ledger_projection(actual, field), ledger_projection(wanted, field)
        walk(actual, wanted, '/' + field)
    return mismatches


def regression_self_test(fixture, inventory, extra_claim=False, load_bytes=None):
    # Mutate only in memory; keep preserved raw JSON and its hash consistent.
    control_name = "extra-true-answer" if extra_claim else "positive-control"
    control = next(c for c in fixture["controls"] if c["name"] == control_name)
    ran = {'attempted': 1, 'executed': 1, 'planned': 1, 'scored': 1}
    def score(submitted, execution=ran):
        return compute(fixture['source'], fixture['denominators'], inventory,
                       submitted, dict(control['probe'], actual_execution=execution), control['alignment'],
                       load_bytes)
    baseline = score(control['submitted'])
    # The control's `expected` reflects its own (zero) execution; the baseline here runs with
    # positive execution, so it is checked against the authored `expected_positive`.
    positive = control['expected_positive']
    if baseline['cannot_evaluate_reasons'] or compare(baseline, positive):
        raise ValueError('regression self-test: positive control does not match')
    keyed = next((c for c in fixture["controls"] if c["name"] == "constant-keyed-literal-export"), None)
    if keyed is not None:
        # Every claim answers with A0001's literal and citations: keyed-literal constant export.
        for execution in (keyed["probe"]["actual_execution"], ran):
            got = compute(fixture['source'], fixture['denominators'], inventory, keyed['submitted'],
                          dict(keyed['probe'], actual_execution=execution), keyed['alignment'])
            if (got['cannot_evaluate_reasons'] or
                    any(got['dimensions'][d] != 'incorrect' for d in ('correctness', 'grounding')) or
                    got['dimensions']['fidelity'] != 'unverified'):
                raise ValueError('regression self-test failed: constant-keyed-literal-export')
        if compare(compute(fixture['source'], fixture['denominators'], inventory, keyed['submitted'],
                           keyed['probe'], keyed['alignment']), keyed['expected']):
            raise ValueError('regression self-test failed: constant-keyed-literal-export expected')
    results = []
    mutations = (("extra-claim-condition",) if extra_claim else
                 ("extra-condition", "missing-condition", "wrong-literal",
                  "missing-claim", "wrong-citation", "wrong-literal-a0001",
                  "wrong-locator-a0002"))
    identifier = "X-true" if extra_claim else "A0005"
    def outcomes_for(computed, target=identifier):
        if extra_claim:
            return next(e["outcomes"] for e in computed["extras_ledger"]
                        if e["assertion_id"] == target and e["channel"] == "answer")
        return {d: computed["per_id"][d][target] for d in ("correctness", "grounding")}
    baseline_outcomes = outcomes_for(baseline)
    if extra_claim and any(v != "correct" for v in baseline_outcomes.values()):
        raise ValueError("regression self-test: extra baseline is not correct")
    # Same key-matching answer: zero execution earns no credit, positive execution keeps it.
    for name, execution in (('zero-executed', dict(ran, executed=0)), ('zero-scored', dict(ran, scored=0))):
        withheld = score(control['submitted'], execution)
        if any(v == 'correct' for ids in withheld['per_id'].values() for v in ids.values()):
            raise ValueError('regression self-test failed: ' + name + ' earned credit')
    # native_run null in isolation: executed and scored stay positive.
    null_run = deepcopy(control['submitted'])
    null_run.setdefault('evidence_record', {})['native_run'] = None
    withheld = score(null_run, dict(ran))
    if any(v == 'correct' for ids in withheld['per_id'].values() for v in ids.values()):
        raise ValueError('regression self-test failed: null native_run earned credit')
    for mutation in mutations:
        submitted = deepcopy(control['submitted'])
        claims = submitted['answer_record']['claims']
        target = {"wrong-literal-a0001": "A0001", "wrong-locator-a0002": "A0002"}.get(mutation, identifier)
        claim = next(c for c in claims if c["claim_id"] == target)
        if mutation == "wrong-literal-a0001":
            claim['answer'] = '20008001'
        elif mutation == "wrong-locator-a0002":
            claim['citations'][0]['locator']['expression'] = '/Library/Property[3]/@Name'
        elif mutation in ("extra-condition", "extra-claim-condition"):
            claim['conditions'].append('Native runtime dependency resolved successfully.')
        elif mutation == 'missing-condition':
            claim['conditions'].pop(0)
        elif mutation == 'wrong-literal':
            claim['answer'] = 'Deliberately wrong A0005 literal.'
        elif mutation == 'missing-claim':
            claims.remove(claim)
        else:
            claim['citations'] = deepcopy(next(c for c in claims if c['claim_id'] == 'A0001')['citations'])
        text = json.dumps(submitted['answer_record'], ensure_ascii=False)
        submitted['raw_answer_record']['text'] = text
        submitted['raw_answer_record']['sha256'] = digest(text.encode('utf-8'))
        computed = score(submitted)
        outcomes = outcomes_for(computed, target)
        changed = any(value != outcomes_for(baseline, target)[d] for d, value in outcomes.items())
        if extra_claim and (any(v != "incorrect" for v in outcomes.values()) or
                            not computed["condition_ledger"]):
            raise ValueError("regression self-test failed: extra-claim-condition policy")
        mismatches = compare(computed, positive)
        if not changed or not mismatches or computed['cannot_evaluate_reasons']:
            raise ValueError('regression self-test failed: ' + mutation)
        results.append({'mutation': mutation, 'outcomes': outcomes,
                        'mismatches': len(mismatches), 'condition_ledger': computed['condition_ledger']})
    if not extra_claim:
        results += citation_controls(fixture, inventory, control, ran, load_bytes)
    return results


def citation_controls(fixture, inventory, control, ran, load_bytes):
    # citation-gap-0206 controls 1-7 on the A0002 claim (/Library/Property[4]/@Name). Expected
    # outcomes are written here, before the first run, from the design's reasons; they are not
    # derived from the scorer output.
    load_bytes = load_bytes or environment_loader
    claim0 = next(c for c in control['submitted']['answer_record']['claims'] if c['claim_id'] == 'A0002')
    good = claim0['citations'][0]
    literal = claim0['answer']
    artifact = fixture['source']['artifact']
    real = load_bytes(good)
    if real is None:
        raise ValueError('regression self-test: artifact bytes unreachable; set LABVIEW_ENVIRONMENT')

    def run(mutate, loader=load_bytes, key_locator=None):
        submitted = deepcopy(control['submitted'])
        claim = next(c for c in submitted['answer_record']['claims'] if c['claim_id'] == 'A0002')
        mutate(claim)
        text = json.dumps(submitted['answer_record'], ensure_ascii=False)
        submitted['raw_answer_record']['text'] = text
        submitted['raw_answer_record']['sha256'] = digest(text.encode('utf-8'))
        inv = deepcopy(inventory)
        key = next(k for k in inv['reference_inventory'] if k['claim_id'] == 'A0002')
        if key_locator:
            key['citations'][0]['locator']['expression'] = key_locator
        computed = compute(fixture['source'], fixture['denominators'], inv, submitted,
                           dict(control['probe'], actual_execution=ran), control['alignment'], loader)
        if computed['cannot_evaluate_reasons']:
            raise ValueError('regression self-test: citation control cannot evaluate')
        return {d: computed['per_id'][d]['A0002'] for d in ('correctness', 'grounding')}, key

    def locator(expression):
        def mutate(claim):
            claim['citations'][0]['locator']['expression'] = expression
        return mutate

    def wrong_sha(claim):
        claim['citations'][0]['sha256'] = '0' * 64

    def wrong_literal(claim):
        claim['answer'] = 'Wrong'

    modified = real + b'\n'  # still parses and resolves to the same text, but different bytes

    def modified_citation(claim):
        claim['citations'][0]['sha256'] = digest(modified)

    bad = {'correctness': 'correct', 'grounding': 'incorrect'}
    cases = (
        (1, 'correct-citation', lambda: run(lambda c: None), {'correctness': 'correct', 'grounding': 'correct'}),
        (2, 'wrong-locator', lambda: run(locator('/Library/Property[3]/@Name')), bad),
        (3, 'right-locator-wrong-hash-over-right-bytes', lambda: run(wrong_sha), bad),
        (3, 'right-locator-modified-bytes-own-hash',
         lambda: run(modified_citation, lambda c: modified), bad),
        (4, 'self-consistent-key-wrong-locator',
         lambda: run(locator('/Library/Property[3]/@Name'), key_locator='/Library/Property[3]/@Name'), bad),
        (5, 'unresolvable-locator',
         lambda: run(locator('/Library/NoSuch[1]/@Name'), key_locator='/Library/NoSuch[1]/@Name'), bad),
        (6, 'artifact-not-available', lambda: run(lambda c: None, lambda c: None),
         {'correctness': 'correct', 'grounding': 'unverified'}),
        (7, 'wrong-literal-right-citation', lambda: run(wrong_literal),
         {'correctness': 'incorrect', 'grounding': 'incorrect'}),
    )
    results = []
    for number, name, act, expected in cases:
        actual, key = act()
        if actual != expected:
            raise ValueError('regression self-test failed: citation control %d %s: %r != %r'
                             % (number, name, actual, expected))
        entry = {'citation_control': number, 'name': name, 'expected': expected, 'actual': actual}
        if number in (4, 5):
            # The identity-only check passes these: the submission copies the corrupted key citation.
            copied = [dict(good, locator=dict(good['locator'],
                                              expression=key['citations'][0]['locator']['expression']))]
            entry['identity_only_outcome'] = citation_support(copied, key)
            if entry['identity_only_outcome'] != 'correct':
                raise ValueError('regression self-test: control %d premise failed' % number)
        results.append(entry)
    # The helper called directly agrees with the full scoring path.
    wrong = dict(good, locator=dict(good['locator'], expression='/Library/Property[3]/@Name'))
    if (citation_resolves(good, literal, artifact, load_bytes) != 'correct' or
            citation_resolves(wrong, literal, artifact, load_bytes) != 'incorrect'):
        raise ValueError('regression self-test failed: citation_resolves direct check')
    return results


def generate(load_bytes=None):
    fixtures = []
    regression_results = []
    extra_regression_results = []
    total = matched = unevaluable = 0
    for fixture_id in FIXTURES:
        path = ROOT / 'benchmark/challenges' / (fixture_id + '.json')
        data_bytes = path.read_bytes()
        fixture = json.loads(data_bytes)
        inventory_bytes = (ROOT / fixture['source']['inventory_path']).read_bytes()
        if digest(inventory_bytes) != fixture['source']['inventory_sha256']:
            raise ValueError(fixture_id + ': inventory SHA256 mismatch')
        inventory = json.loads(inventory_bytes)
        if fixture_id == "library-icon-tests":
            extra_regression_results = regression_self_test(fixture, inventory, extra_claim=True, load_bytes=load_bytes)
        if fixture_id == 'library-specialty':
            regression_results = regression_self_test(fixture, inventory, load_bytes=load_bytes)
        controls = []
        for control in fixture['controls']:
            # Never pass expected, purpose, evidence, or alignment's authored
            # expected_outcome to the computation function.
            computed = compute(fixture['source'], fixture['denominators'], inventory,
                               control['submitted'], control['probe'], control['alignment'], load_bytes)
            expected = control['expected']
            mismatches = compare(computed, expected)
            reasons = computed['cannot_evaluate_reasons']
            match = not mismatches and not reasons
            controls.append({'control': control['name'], 'computed': computed,
                             'expected': expected, 'match': match, 'mismatches': mismatches,
                             'cannot_evaluate': bool(reasons)})
            total += 1
            matched += int(match)
            unevaluable += int(bool(reasons))
        fixtures.append({'fixture_id': fixture_id, 'path': str(path.relative_to(ROOT)),
                         'sha256': digest(data_bytes), 'controls': controls})
    return {'schema_version': 1, 'development_only': True, 'independently_reviewed': False,
            'native_evidence_available': False, 'quality_measured': False,
            'method': 'Conditional provisional XML key comparison; native matches stay unverified. Current-evidence view separately retains pending XML review. Synthetic fixture scoring is not reader execution.',
            'totals': {'fixtures': len(fixtures), 'controls': total, 'matches': matched,
                       'mismatches': total - matched, 'cannot_evaluate': unevaluable},
            'regression_self_test': regression_results + extra_regression_results, 'fixtures': fixtures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare generated bytes without writing')
    args = parser.parse_args()
    result = generate()
    rendered = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode('utf-8')
    if args.check:
        if not OUT.is_file() or OUT.read_bytes() != rendered:
            print('results/challenges.json is missing or differs from deterministic regeneration', file=sys.stderr)
            return 1
    else:
        OUT.write_bytes(rendered)
    print(json.dumps(result['totals'], sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
