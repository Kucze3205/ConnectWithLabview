#!/usr/bin/env python3
"""Read-only integrity and coverage checker for the WP1 frozen key package (issue #571; revision 0117).

Standard library only; reads repository files, writes nothing. It re-derives the
obligation inventory from the current method.json and benchmark/protocol.md and
compares it with the package, so it does not merely compare two author lists.
Limits: this certifies package integrity and source coverage only. It does not
certify narrative truth, native behavior, independent approval or trial readiness.
Run from anywhere: python3 -I benchmark/writing/check_wp1_key_0117.py
"""
import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEY = 'benchmark/writing/wp1-key-0117.json'
MD = 'benchmark/writing/wp1-key-0117.md'
METHOD = 'benchmark/writing/method.json'
PROTOCOL = 'benchmark/protocol.md'
ORIG = 'benchmark/real-project-0107/original.lvproj'
LIC = 'benchmark/real-project-0107/LICENSE.txt'
PROPOSAL = 'benchmark/project-text-writing-0109.json'
CASE = 'WP1-project-build-text'
SECTIONS = ['revision', 'status', 'authority', 'claims', 'existing_requirements',
            'new_requirements', 'common', 'comparison', 'coverage']
# Pins stated independently of the key (README WP1 integration 0112 and the proposal).
ORIG_SHA = '1d5e140df788ce1f91c89241bbdb1227c5e4cc6fdf6efbbd820974bbe6082dcf'
LIC_SHA = '529e65e6fc185d39380efd3957ef1c9acd0aac31ed288bcb9d124840861f03a2'
START_COMMIT = '46e4d9d983df70e8382499c1781c861d0d327362'
START_TREE = 'aee7cb6ee94045e549912b91c1f6e517fcbc0fdb'
REQUIRED_INPUTS = [
    METHOD, PROTOCOL, ORIG, LIC, PROPOSAL, 'benchmark/project-text-writing-0109.md',
    'benchmark/writing/README.md', 'benchmark/baseline/runner-contract.md',
    'benchmark/precision/README.md', 'docs/perpetua/evaluation.md',
    'docs/perpetua/roles.md', 'goal/goal.md',
    'benchmark/writing/review-0113-provenance.md', 'benchmark/writing/review-0113.json']
# Protocol lines whose obligation I read independently; each must reach the named rule.
CRITICAL = {28: 'R-independent', 29: 'R-mapping', 36: 'R-citations', 38: 'R-reader',
            41: 'R-assessment', 59: 'R-docs', 60: 'R-independent', 62: 'R-native',
            73: 'R-split', 81: 'R-paired', 88: 'R-uncertainty', 99: 'R-citations',
            102: 'R-mapping', 106: 'R-controls', 110: 'R-controls', 111: 'R-owner'}
NA_LINES = {14, 15, 16, 18, 19, 20, 21, 22, 23, 27, 55}
STATUSES = {'proposed-awaiting-separate-check', 'not-applicable-to-WP1'}
GAP_STATUS = 'unavailable'


def H(b):
    return hashlib.sha256(b).hexdigest()


def blob_id(b):
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


def canon(v):
    return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def rd(rel):
    return (ROOT / rel).read_bytes()


def derive():
    """Obligation inventory re-derived from current method.json and protocol.md."""
    m = json.loads(rd(METHOD).decode('utf-8'))
    ti = [i for i, t in enumerate(m['tasks']) if t['id'] == CASE]
    assert len(ti) == 1, 'WP1 task must appear exactly once in method.json'
    ti = ti[0]
    ob = {}

    def leaves(v, p):
        if isinstance(v, dict) and v:
            for k, x in v.items():
                leaves(x, p + '/' + k.replace('~', '~0').replace('/', '~1'))
        elif isinstance(v, list) and v:
            for i, x in enumerate(v):
                leaves(x, p + '/' + str(i))
        else:
            ob['method#' + p] = (METHOD, p, H(canon(v)))

    for s in SECTIONS:
        leaves(m[s], '/' + s)
    leaves(m['tasks'][ti], '/tasks/' + str(ti))
    for n, line in enumerate(rd(PROTOCOL).decode('utf-8').splitlines(), 1):
        if not line.strip() or line.startswith('#') or line.startswith('|---'):
            continue
        ob['protocol#L%d' % n] = (PROTOCOL, 'L%d' % n, H(line.encode()))
    return m, m['tasks'][ti], ob


def original_facts(task):
    b = rd(ORIG)
    loc = task['text_contract']['locator']
    root = ET.fromstring(b)
    nodes = root.findall(loc)
    needle = b'Name="Bld_version.build" Type="Int">2<'
    idx = b.find(needle)
    off = idx + len(needle) - 2 if idx >= 0 and b.count(needle) == 1 else -1
    facts = {
        'sha': H(b), 'size': len(b), 'bom': b[:3].hex(), 'match_count': len(nodes),
        'attrs': dict(nodes[0].attrib) if len(nodes) == 1 else None,
        'text': nodes[0].text if len(nodes) == 1 else None,
        'children': len(nodes[0]) if len(nodes) == 1 else None,
        'root_attrs': dict(root.attrib), 'offset': off,
        'line': b[:off].count(b'\n') + 1 if off >= 0 else None,
        'removed_hex': b[off:off + 1].hex() if off >= 0 else None,
        'out_sha': H(b[:off] + b'3' + b[off + 1:]) if off >= 0 else None,
        'lic_sha': H(rd(LIC))}
    return facts


def check_key(key, ctx, md):
    m, task, ob = ctx['method'], ctx['task'], ctx['ob']
    facts = ctx['facts']
    e = []
    add = e.append
    # --- required IDs against the current method task ---
    want = {'semantic': task['semantic_ids'], 'preservation': task['preservation_ids'],
            'answer': task['answer_ids']}
    got = [(x.get('id'), x.get('dimension')) for x in key.get('required_ids', [])]
    ids = [g[0] for g in got]
    for d, lst in want.items():
        for i in lst:
            if ids.count(i) == 0:
                add('required-id-missing')
            elif (i, d) not in got:
                add('required-id-dimension')
    for i in set(ids):
        if ids.count(i) > 1:
            add('required-id-duplicate')
        if i not in sum(want.values(), []):
            add('required-id-extra')
    for x in key.get('required_ids', []):
        if x.get('status') not in STATUSES or x.get('checker_agreement') != 'pending':
            add('status-promotion')
        if not x.get('expected_result') or not x.get('original_output_citation_rule') \
                or not x.get('comparison_or_human_adjudication') or not x.get('uncertainty'):
            add('required-id-incomplete')
    if key.get('case_id') != CASE or key.get('source_revision') != m['revision']:
        add('source-revision')
    sp = [x for x in key.get('required_ids', []) if x.get('id') == 'WP1-property-text']
    if sp and sp[0]['expected_result'].get('output_sha256_requirement_derived') != facts['out_sha']:
        add('delta-mismatch')
    # --- rules ---
    rules = {}
    for r in key.get('rules', []):
        if r.get('id') in rules:
            add('rule-duplicate')
        rules[r.get('id')] = r
        if r.get('status') not in STATUSES:
            add('status-promotion')
        plines = rd(PROTOCOL).decode('utf-8').splitlines()
        for s in r.get('source_locators', []) or [None]:
            ok = bool(s) and s.get('path') == PROTOCOL and re.fullmatch(r'L\d+', s.get('locator', ''))
            ok = ok and 1 <= int(s['locator'][1:]) <= len(plines) and plines[int(s['locator'][1:]) - 1].strip()
            if not ok:
                add('rule-locator')
    # --- obligations: exact set, pins and rule links ---
    obs = key.get('source_obligations', [])
    oids = [o.get('id') for o in obs]
    for i in set(oids):
        if oids.count(i) > 1:
            add('obligation-duplicate')
    for i in ob:
        if i not in oids:
            add('obligation-missing')
    used = set()
    for o in obs:
        d = ob.get(o.get('id'))
        if d is None:
            add('obligation-extra')
            continue
        s = o.get('source', {})
        if (s.get('path'), s.get('locator')) != (d[0], d[1]):
            add('obligation-locator')
        elif s.get('value_sha256') != d[2]:
            add('obligation-pin')
        rr = o.get('expected_rule_ids') or []
        if not rr:
            add('rule-unknown')
        for r in rr:
            used.add(r)
            if r not in rules:
                add('rule-unknown')
        if o.get('status') not in STATUSES:
            add('status-promotion')
        if o.get('status') == 'not-applicable-to-WP1':
            n = int(o['id'].split('#L')[-1]) if o['id'].startswith('protocol#L') else -1
            if n not in NA_LINES or not o.get('applicability'):
                add('na-unsupported')
    by = {o.get('id'): o for o in obs}
    for n, rule in CRITICAL.items():
        if rule not in (by.get('protocol#L%d' % n, {}).get('expected_rule_ids') or []):
            add('critical-mapping')
    for x in key.get('required_ids', []):
        used.update(x.get('expected_rule_ids') or [])
        for r in x.get('expected_rule_ids') or []:
            if r not in rules:
                add('rule-unknown')
    if set(rules) - used:
        add('rule-unused')
    # --- source pins ---
    man = key.get('read_input_manifest', [])
    paths = [x.get('path') for x in man]
    for p in REQUIRED_INPUTS:
        if p not in paths:
            add('input-missing')
    for x in man:
        try:
            b = rd(x['path'])
        except OSError:
            add('input-hash')
            continue
        if x.get('sha256') != H(b) or x.get('bytes') != len(b):
            add('input-hash')
        if x.get('git_blob_at_start') != blob_id(b):
            add('input-blob')
        if '.session' in x['path']:
            add('input-external')
    pre = key.get('precondition', {})
    if not (pre.get('original_sha256') == ORIG_SHA == facts['sha']) or facts['size'] != 5806:
        add('original-pin')
    if [x.get('sha256') for x in key.get('original_manifest', [])] != [ORIG_SHA, LIC_SHA] \
            or facts['lic_sha'] != LIC_SHA:
        add('original-pin')
    if (pre.get('match_count'), pre.get('text'), pre.get('property_children'),
            pre.get('property_attributes'), pre.get('root_attributes')) != (
            facts['match_count'], facts['text'], facts['children'], facts['attrs'],
            facts['root_attrs']) or facts['bom'] != 'efbbbf':
        add('original-pin')
    dl = key.get('delta', {})
    if (dl.get('offset_zero_based'), dl.get('line_one_based'), dl.get('removed_hex'),
            dl.get('inserted_hex'), dl.get('output_size'), dl.get('allowed_changed_bytes'),
            dl.get('before'), dl.get('after')) != (
            facts['offset'], facts['line'], facts['removed_hex'], '33', 5806, 1, '2', '3'):
        add('delta-mismatch')
    tp = key.get('task_prompt', {})
    if tp.get('sha256') != H(task['request'].encode()) or tp.get('text') != task['request']:
        add('prompt-pin')
    up, pj = key.get('upstream_source', {}), json.loads(rd(PROPOSAL).decode('utf-8'))['source']
    if up != pj or up.get('sha256') != ORIG_SHA or up.get('license_sha256') != LIC_SHA:
        add('upstream-pin')
    st = key.get('starting_revision', {})
    if st.get('commit') != START_COMMIT or st.get('tree') != START_TREE \
            or not re.fullmatch(r'[0-9a-f]{40}', str(st.get('tree'))):
        add('starting-revision')
    # --- native / approval / readiness promotions and unallocated fields ---
    if key.get('native_key') != GAP_STATUS:
        add('native-promotion')
    if key.get('native_and_trial_results') != task['planned_results']:
        add('native-promotion')
    if any(v not in ('unexecuted', 'unverified') for v in key.get('native_and_trial_results', {}).values()):
        add('native-promotion')
    if sorted(g.get('id') for g in key.get('native_gap_records', [])) != sorted(task['oracle']['missing']) \
            or any(g.get('status') != GAP_STATUS or not g.get('next_evidence')
                   for g in key.get('native_gap_records', [])):
        add('native-gap-mismatch')
    ia = key.get('independent_approval', {})
    if ia.get('status') != 'pending' or ia.get('checker_identity') is not None \
            or ia.get('checker_session') is not None or ia.get('per_id_agreement') is not None:
        add('approval-promotion')
    if key.get('trial_readiness') != 'pending':
        add('readiness-promotion')
    cl = key.get('claims', {})
    if cl.get('agent_runs') != 0 or cl.get('native_executions') != 0 \
            or cl.get('project_files_written') != 0 or any(
            cl.get(k) is not False for k in ('key_independently_approved', 'benchmark_ready',
                                             'method_accepted', 'withheld', 'model_unseen')):
        add('readiness-promotion')
    al = key.get('allocation', {})
    if any(al.get(k) is not None for k in ('model', 'settings', 'quota', 'budgets', 'repetitions',
                                           'arm_order', 'retry_policy', 'workspaces', 'native_job')) \
            or not str(al.get('status', '')).startswith('unallocated') \
            or key.get('workspace_policy', {}).get('allocated_workspaces') != [] \
            or key.get('output_policy', {}).get('actual_outputs') != [] \
            or key.get('output_policy', {}).get('output_hashes') is not None:
        add('allocation-invented')
    ca = key.get('claim_adjudication', {})
    c1 = ca.get('C1', '')
    if not c1.startswith('open') or 'no structured flags' not in c1.lower() or 'substring' not in c1:
        add('c1-limit')
    dn = ca.get('required_denominators', {})
    if dn != {'artifact_semantic': len(task['semantic_ids']), 'preservation': len(task['preservation_ids']),
              'answer_correctness': len(task['answer_ids']), 'source_grounding': len(task['answer_ids']),
              'reading_fidelity': None}:
        add('denominator-mismatch')
    # --- markdown companion ---
    if md is None or not all(i in md for i in sum(want.values(), []) + list(rules)) \
            or key.get('revision', '\0') not in md or 'C1' not in md or 'pending' not in md:
        add('md-incomplete')
    return sorted(set(e))


def counterexamples(key, ctx, md):
    def mut(f):
        k = copy.deepcopy(key)
        f(k)
        return k

    def ob(k, i):
        return next(o for o in k['source_obligations'] if o['id'] == i)

    cases = [
        ('missing-required-id', 'required-id-missing', lambda k: k['required_ids'].pop(), md),
        ('duplicated-required-id', 'required-id-duplicate',
         lambda k: k['required_ids'].append(copy.deepcopy(k['required_ids'][0])), md),
        ('extra-required-id', 'required-id-extra',
         lambda k: k['required_ids'].append(dict(copy.deepcopy(k['required_ids'][0]), id='WP1-invented')), md),
        ('missing-obligation', 'obligation-missing', lambda k: k['source_obligations'].pop(100), md),
        ('duplicated-obligation', 'obligation-duplicate',
         lambda k: k['source_obligations'].append(copy.deepcopy(k['source_obligations'][5])), md),
        ('bad-method-locator', 'obligation-locator',
         lambda k: ob(k, 'method#/tasks/4/request')['source'].update(locator='/tasks/4/nope')
         if any(o['id'] == 'method#/tasks/4/request' for o in k['source_obligations'])
         else k['source_obligations'][0]['source'].update(locator='/nope'), md),
        ('bad-protocol-locator', 'obligation-locator',
         lambda k: ob(k, 'protocol#L60')['source'].update(locator='L9999'), md),
        ('bad-obligation-pin', 'obligation-pin',
         lambda k: ob(k, 'protocol#L60')['source'].update(value_sha256='0' * 64), md),
        ('bad-input-sha', 'input-hash', lambda k: k['read_input_manifest'][0].update(sha256='1' * 64), md),
        ('bad-input-blob', 'input-blob',
         lambda k: k['read_input_manifest'][0].update(git_blob_at_start='2' * 40), md),
        ('dropped-input', 'input-missing',
         lambda k: k.update(read_input_manifest=[x for x in k['read_input_manifest']
                                                 if x['path'] != PROTOCOL]), md),
        ('bad-original-pin', 'original-pin',
         lambda k: k['precondition'].update(original_sha256='3' * 64), md),
        ('bad-delta-offset', 'delta-mismatch', lambda k: k['delta'].update(offset_zero_based=3346), md),
        ('prompt-drift', 'prompt-pin', lambda k: k['task_prompt'].update(sha256='4' * 64), md),
        ('bad-starting-tree', 'starting-revision',
         lambda k: k['starting_revision'].update(tree=k['starting_revision']['tree'] + '3'), md),
        ('unknown-rule', 'rule-unknown',
         lambda k: ob(k, 'protocol#L60').update(expected_rule_ids=['R-nope']), md),
        ('critical-mapping-dropped', 'critical-mapping',
         lambda k: ob(k, 'protocol#L29').update(expected_rule_ids=['R-scope']), md),
        ('unsupported-not-applicable', 'na-unsupported',
         lambda k: ob(k, 'protocol#L60').update(status='not-applicable-to-WP1', applicability='x'), md),
        ('native-key-promoted', 'native-promotion', lambda k: k.update(native_key='available'), md),
        ('native-result-promoted', 'native-promotion',
         lambda k: k['native_and_trial_results'].update(native_validity='pass'), md),
        ('native-gap-dropped', 'native-gap-mismatch', lambda k: k['native_gap_records'].pop(), md),
        ('approval-promoted', 'approval-promotion',
         lambda k: k['independent_approval'].update(status='approved'), md),
        ('id-approved', 'status-promotion',
         lambda k: k['required_ids'][0].update(status='independently-approved'), md),
        ('readiness-promoted', 'readiness-promotion', lambda k: k.update(trial_readiness='ready'), md),
        ('benchmark-ready-claimed', 'readiness-promotion', lambda k: k['claims'].update(benchmark_ready=True), md),
        ('allocation-invented', 'allocation-invented', lambda k: k['allocation'].update(model='x'), md),
        ('workspace-allocated', 'allocation-invented',
         lambda k: k['workspace_policy'].update(allocated_workspaces=[{'path': '/w'}]), md),
        ('c1-settled-by-flags', 'c1-limit',
         lambda k: k['claim_adjudication'].update(C1='closed: structured flags certify narrative'), md),
        ('denominator-shrunk', 'denominator-mismatch',
         lambda k: k['claim_adjudication']['required_denominators'].update(answer_correctness=2), md),
        ('md-missing-id', 'md-incomplete', lambda k: None, md.replace('WP1-honest-limits', 'X')),
    ]
    out = {}
    for name, code, f, mdx in cases:
        found = check_key(mut(f), ctx, mdx)
        out[name] = {'expected': code, 'rejected_for': found, 'ok': code in found}
    return out



# Revision-0117 checks. The source-derived base above is adapted from 0115,
# not imported or executed from the historical checker.
_base_check_key = check_key
REVIEW = 'benchmark/writing/wp1-key-review-0116.json'
REVIEW_SHA = '2f127a7dad8e9719f6e026e1a1fce5aa1b0509f8503d5994771e0234c83a373e'
REVIEW_BYTES = 135476
OLD_KEY = 'benchmark/writing/wp1-key-0115.json'
OLD_PINS = {
    OLD_KEY: (262592, '960b72b0aabb3e0d8151ad4fd25452377d6c05e482c76601f99163b246381a24'),
    'benchmark/writing/wp1-key-0115.md': (9337, 'eb621c81154ccd537518bc0559e9a1fe8ed87e0e09b8418616fc3a5b52f42720'),
    'benchmark/writing/check_wp1_key_0115.py': (19779, 'e7d22309e7ccd1b8e33628b9c0c9c77b59c3b3602b15d06e1179d26478ebeeeb'),
    'benchmark/writing/wp1-key-0115-verification.json': (17358, 'bf131650bf56d136769fd720ce8e24611b4fbd04a811634fef7eb6f48c112497'),
}
# These pin the authored tests, not their semantic validity. Humans must review them.
TEST_PINS = {
    'WP1-describe-text-delta': '29da7aa23a95d314b791df3c6ae35e9ec020c5fd446cb9d51d3b263fde75078c',
    'WP1-original-output-grounding': '08200fddf0cd5e5bb589041e20b87b5fdd9d5830581e8c4b5ca0ce4972c3b285',
    'WP1-honest-limits': '5809bf4715308d39282b0f6fc3b8f81d7cf07a71192ba209fb725c0a13cc4b0f',
}
C, I, M, U, P = 'correct', 'incorrect', 'missing', 'unverified', 'partial'
# Proposed prescriptions for the preserved review's conditions, not probe results.
LEDGERS = {
    'C1-correct': ([C, C, C], [C, C, C], [], C, C),
    'C1-wrong-existing-citation': ([C, I, C], [I, I, C], [], I, I),
    'C1-unverified-extra': ([C, C, C], [C, C, C], [(U, M)], U, P),
    'C1-contradiction': ([I, I, C], [I, I, C], [(I, I)], I, I),
    'C1-native-overclaim': ([C, I, I], [C, I, I], [(I, I)], I, I),
    'C1-abstention': ([M, M, C], [M, M, C], [], P, P),
}


def resolve_pointer(value, pointer):
    for part in pointer.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def required_mapping_links(method, task):
    """Derive task index/leaf population from method, not the review's count."""
    ti = method['tasks'].index(task)
    prefix = 'method#/tasks/%d/' % ti
    links = {prefix + 'comparison/matched_fields/%d' % i: ['R-paired']
             for i, _ in enumerate(task['comparison']['matched_fields'])}
    links[prefix + 'comparison/rule'] = ['R-paired', 'R-account', 'R-uncertainty']
    # W7 contract refers to the entire comparison object including uncertainty.
    links[prefix + 'requirements_mapping/W7/contract'] = ['R-paired', 'R-account', 'R-uncertainty']
    # W7 review's literal clauses concern equality, isolation and accounting.
    links[prefix + 'requirements_mapping/W7/review'] = ['R-paired', 'R-account']
    return links


def assess(required, extras=(), inventory=True):
    """Protocol L41 only; takes HUMAN-assigned outcomes, never raw prose."""
    if not inventory or not required:
        return U
    outcomes = list(required) + list(extras)
    if I in outcomes:
        return I
    if U in outcomes:
        return U
    if all(x == C for x in outcomes):
        return C
    if any(x in (C, P) for x in outcomes):
        return P
    if 'error' in outcomes:
        return 'error'
    if all(x == 'unsupported' for x in required):
        return 'unsupported'
    return M


def check_key(key, ctx, md):
    errors = _base_check_key(key, ctx, md)
    add = errors.append
    old, review = ctx['old'], ctx['review']
    links = required_mapping_links(ctx['method'], ctx['task'])
    if key.get('revision') != 'wp1-key-0117-v1' or key.get('issue') != 571 \
            or key.get('status') != 'proposed-awaiting-separate-check':
        add('revision-status')
    provenance = key.get('revision_provenance', {})
    expected_pins = [p for p in review['pins'] if p['path'] in OLD_PINS]
    if provenance.get('predecessor_package') != expected_pins \
            or provenance.get('predecessor_revision') != old['revision'] \
            or provenance.get('predecessor_starting_revision') != old['starting_revision']:
        add('predecessor-provenance')
    rp = provenance.get('review', {})
    if (rp.get('path'), rp.get('source_issue'), rp.get('sha256'), rp.get('bytes'),
        rp.get('reviewed_revision')) != (REVIEW, 567, REVIEW_SHA, REVIEW_BYTES, review['reviewed_revision']) \
            or not rp.get('limitations'):
        add('review-provenance')
    if provenance.get('source_pin_comparison') != {
            'review_pins_checked': len(review['pins']),
            'predecessor_inputs_checked': len(old['read_input_manifest']), 'mismatches': []}:
        add('pin-comparison')
    if key.get('read_input_manifest') != old['read_input_manifest']:
        add('source-manifest-drift')
    # Original task, output and unsupported/native policies are inherited verbatim.
    for field in ('case_id', 'source_revision', 'task_prompt', 'citation_contract', 'precondition',
                  'delta', 'original_manifest', 'allowed_input_manifest', 'workspace_policy',
                  'output_policy', 'native_and_trial_results', 'native_key', 'native_gap_records',
                  'allocation', 'prerequisites', 'visibility', 'claims', 'independent_approval',
                  'trial_readiness', 'source_coverage_policy'):
        if key.get(field) != old[field]:
            add('unrelated-policy-drift')
    source_obs = {o['id']: o for o in old['source_obligations']}
    by = {o.get('id'): o for o in key.get('source_obligations', [])}
    for oid, orig in source_obs.items():
        expected = copy.deepcopy(orig)
        if oid in links:
            expected['expected_rule_ids'] = links[oid]
        if by.get(oid) != expected:
            add('f1-mapping' if oid in links else 'unrelated-mapping-drift')
    f1_review = next(f for f in review['findings'] if f['id'] == 'F1')
    if set(links) != set(f1_review['affected_obligation_ids']):
        add('review-source-locator-conflict')
    disp = key.get('finding_dispositions', {})
    mappings = disp.get('F1', {}).get('mappings', [])
    mids = [x.get('obligation_id') for x in mappings]
    if len(mids) != len(links) or set(mids) != set(links):
        add('f1-disposition')
    for mapping in mappings:
        oid = mapping.get('obligation_id')
        if oid not in links:
            add('f1-disposition')
            continue
        pointer = oid.split('#', 1)[1]
        if mapping.get('old_rule_ids') != source_obs[oid]['expected_rule_ids'] \
                or mapping.get('new_rule_ids') != links[oid] \
                or mapping.get('source_value') != resolve_pointer(ctx['method'], pointer) \
                or not mapping.get('rationale'):
            add('f1-disposition')
        refs = mapping.get('source_requirements', [])
        if {'path': METHOD, 'locator': pointer} not in refs:
            add('f1-disposition')
        required_lines = {79, 81, 83}
        if 'R-account' in links[oid]:
            required_lines.update({86, 87})
        if 'R-uncertainty' in links[oid]:
            required_lines.update({88, 89})
        if not required_lines.issubset({int(r['locator'][1:]) for r in refs
                                       if r.get('path') == PROTOCOL and re.fullmatch(r'L\d+', r.get('locator', ''))}):
            add('f1-disposition')
    for f in ('F1', 'F2'):
        if disp.get(f, {}).get('status') != 'corrected-proposed-awaiting-separate-check':
            add('finding-status')
    if disp.get('P1', {}).get('status') != 'open' or disp.get('C1', {}).get('status') != 'open':
        add('limitation-promotion')
    if not disp.get('F2', {}).get('interpretation') or disp.get('F2', {}).get('conflicts') != [] \
            or not disp.get('F2', {}).get('review_delta'):
        add('f2-disposition')
    # A changed test text is detectable, without pretending its hash proves truth.
    items = {i.get('id'): i for i in key.get('required_ids', [])}
    for aid, sha in TEST_PINS.items():
        tests = items.get(aid, {}).get('separate_dimension_tests', {})
        if H(canon(tests)) != sha or set(tests) != {'correctness', 'grounding'}:
            add('separate-dimension-tests')
    for item in old['required_ids']:
        if item['dimension'] != 'answer' and items.get(item['id']) != item:
            add('unrelated-id-drift')
    old_rules = {r['id']: r for r in old['rules']}
    rules = {r.get('id'): r for r in key.get('rules', [])}
    if set(rules) != set(old_rules):
        add('rule-inventory-drift')
    for rid, original in old_rules.items():
        current = copy.deepcopy(rules.get(rid, {}))
        if rid in ('R-citations', 'R-mapping', 'R-dimensions'):
            text = current.get('comparison_or_human_adjudication', '')
            if not text.startswith(original['comparison_or_human_adjudication']) \
                    or 'separate_dimension_tests' not in text or 'relational truth' not in text:
                add('f2-rule')
            current['comparison_or_human_adjudication'] = original['comparison_or_human_adjudication']
        if current != original:
            add('unrelated-rule-drift')
    ca = key.get('claim_adjudication', {})
    if not ca.get('ledger_policy') or not ca.get('source_map_scope'):
        add('ledger-policy')
    ledgers = ca.get('prescribed_ledgers', [])
    names = [x.get('id') for x in ledgers]
    if len(names) != len(LEDGERS) or set(names) != set(LEDGERS):
        add('ledger-inventory')
    for ledger in ledgers:
        name = ledger.get('id')
        if name not in LEDGERS:
            continue
        cs, gs, extras, csum, gsum = LEDGERS[name]
        rows = ledger.get('items', [])
        if [r.get('id') for r in rows] != ctx['task']['answer_ids']:
            add('ledger-denominator')
        if [r.get('correctness') for r in rows] != cs \
                or [r.get('grounding') for r in rows] != gs:
            add('ledger-item-outcome')
        got_extras = ledger.get('extras', [])
        if [(x.get('correctness'), x.get('grounding')) for x in got_extras] != extras \
                or any(not x.get('assertion') for x in got_extras):
            add('ledger-extra')
        if name in ('C1-contradiction', 'C1-native-overclaim'):
            target = 'WP1-describe-text-delta' if name == 'C1-contradiction' else 'WP1-honest-limits'
            if any(x.get('retain_both') is not True or x.get('contradicts') != target for x in got_extras):
                add('ledger-contradiction')
        got_cs = [r.get('correctness') for r in rows]
        got_gs = [r.get('grounding') for r in rows]
        if ledger.get('assessment') != {'answer_correctness': csum, 'source_grounding': gsum} \
                or assess(got_cs, [x.get('correctness') for x in got_extras]) != csum \
                or assess(got_gs, [x.get('grounding') for x in got_extras]) != gsum:
            add('ledger-assessment')
        ix = next(i for i, x in enumerate(review['c1_tests']['cases']) if x['id'] == name)
        if ledger.get('raw_answer_reference') != {'path': REVIEW, 'locator': '/c1_tests/cases/%d/answer' % ix} \
                or not ledger.get('conditions') or not ledger.get('rationale') \
                or ledger.get('duplicates') != []:
            add('ledger-evidence')
    return sorted(set(errors))


def revision_counterexamples(key, ctx, md):
    """Corrupt proposed package metadata in memory; never replay review probes."""
    out = {}

    def run(name, code, change):
        mutated = copy.deepcopy(key)
        change(mutated)
        errors = check_key(mutated, ctx, md)
        out[name] = {'expected': code, 'rejected_for': errors, 'ok': code in errors}

    def ledger(k, name):
        return next(x for x in k['claim_adjudication']['prescribed_ledgers'] if x['id'] == name)

    for oid in required_mapping_links(ctx['method'], ctx['task']):
        run('restore-bad-link:' + oid, 'f1-mapping',
            lambda k, oid=oid: next(x for x in k['source_obligations'] if x['id'] == oid)
            .update(expected_rule_ids=['R-scope', 'R-independent']))
    run('alter-unrelated-link', 'unrelated-mapping-drift',
        lambda k: k['source_obligations'][0].update(expected_rule_ids=['R-paired']))
    run('review-pin-forged', 'review-provenance',
        lambda k: k['revision_provenance']['review'].update(sha256='0' * 64))
    run('review-size-forged', 'review-provenance',
        lambda k: k['revision_provenance']['review'].update(bytes=1))
    run('predecessor-pin-forged', 'predecessor-provenance',
        lambda k: k['revision_provenance']['predecessor_package'][0].update(sha256='0' * 64))
    run('f1-record-missing', 'f1-disposition', lambda k: k['finding_dispositions']['F1']['mappings'].pop())
    run('separate-test-dropped', 'separate-dimension-tests',
        lambda k: next(x for x in k['required_ids'] if x['id'] == 'WP1-original-output-grounding')
        ['separate_dimension_tests'].pop('correctness'))
    for case in LEDGERS:
        run('ledger-required-slot-dropped:' + case, 'ledger-denominator',
            lambda k, case=case: ledger(k, case)['items'].pop())
    run('wrong-citation-map-correct', 'ledger-item-outcome',
        lambda k: ledger(k, 'C1-wrong-existing-citation')['items'][1].update(correctness=C))
    run('wrong-citation-delta-truth-downgraded', 'ledger-item-outcome',
        lambda k: ledger(k, 'C1-wrong-existing-citation')['items'][0].update(correctness=I))
    run('existing-citation-accepted', 'ledger-item-outcome',
        lambda k: ledger(k, 'C1-wrong-existing-citation')['items'][0].update(grounding=C))
    run('extra-erased', 'ledger-extra', lambda k: ledger(k, 'C1-unverified-extra').update(extras=[]))
    run('extra-credited', 'ledger-extra',
        lambda k: ledger(k, 'C1-unverified-extra')['extras'][0].update(correctness=C))
    run('contradiction-erased', 'ledger-contradiction',
        lambda k: ledger(k, 'C1-contradiction')['extras'][0].update(retain_both=False))
    run('native-overclaim-accepted', 'ledger-item-outcome',
        lambda k: ledger(k, 'C1-native-overclaim')['items'][2].update(correctness=C))
    run('honest-abstention-promoted', 'ledger-assessment',
        lambda k: ledger(k, 'C1-abstention')['assessment'].update(answer_correctness=C))
    run('cold-review-limitation-closed', 'limitation-promotion',
        lambda k: k['finding_dispositions']['P1'].update(status='closed'))
    return out


def assessment_checks():
    # Independently enumerate L41 precedence, including extras and unavailable IDs.
    rows = [
        ('absent-inventory', [], [], False, U),
        ('empty-inventory', [], [], True, U),
        ('incorrect-before-unverified', [I, U, C], [], True, I),
        ('false-extra', [C, C, C], [I], True, I),
        ('unverified-extra', [C, C, C], [U], True, U),
        ('complete', [C, C, C], [], True, C),
        ('true-extra-no-required-credit', [C, M, C], [C], True, P),
        ('missing-extra-citation', [C, C, C], [M], True, P),
        ('partial-before-error', [P, 'error', M], [], True, P),
        ('error', [M, 'error', 'unsupported'], [], True, 'error'),
        ('honest-unsupported', ['unsupported'] * 3, [], True, 'unsupported'),
        ('mixed-missing-unsupported', [M, 'unsupported', M], [], True, M),
        ('all-missing', [M] * 3, [], True, M),
    ]
    return {n: {'expected': expected, 'actual': assess(req, extras, inventory),
                'ok': assess(req, extras, inventory) == expected}
            for n, req, extras, inventory, expected in rows}


def main():
    # Fixed review/predecessor bytes are checked before using their contents.
    physical_errors = []
    for path, (size, sha) in {REVIEW: (REVIEW_BYTES, REVIEW_SHA), **OLD_PINS}.items():
        data = rd(path)
        if (len(data), H(data)) != (size, sha):
            physical_errors.append('preserved-review-pin' if path == REVIEW else 'predecessor-immutability')
    if physical_errors:
        print(json.dumps({'status': 'failed', 'package_errors': physical_errors}))
        return 1
    review, old = json.loads(rd(REVIEW)), json.loads(rd(OLD_KEY))
    for pin in review['pins'] + old['read_input_manifest']:
        data = rd(pin['path'])
        if (len(data), H(data)) != (pin['bytes'], pin['sha256']):
            physical_errors.append('review-source-pin:' + pin['path'])
    key = json.loads(rd(KEY))
    md = rd(MD).decode('utf-8')
    method, task, obligations = derive()
    ctx = {'method': method, 'task': task, 'ob': obligations,
           'facts': original_facts(task), 'old': old, 'review': review}
    errors = sorted(set(physical_errors + check_key(key, ctx, md)))
    cx = counterexamples(key, ctx, md)
    cx.update(revision_counterexamples(key, ctx, md))
    assessments = assessment_checks()
    ok = not errors and all(x['ok'] for x in cx.values()) and all(x['ok'] for x in assessments.values())
    np = sum(x.startswith('protocol#') for x in obligations)
    corrected = required_mapping_links(method, task)
    print(json.dumps({
        'status': 'package-integrity-consistent' if ok else 'failed',
        'package_errors': errors,
        'derived_obligations': {'method_pointers': len(obligations) - np, 'protocol_lines': np,
                                'key_obligations': len(key['source_obligations'])},
        'required_ids': [x['id'] for x in key['required_ids']], 'rules': len(key['rules']),
        'read_inputs': len(key['read_input_manifest']),
        'mapping_counts': {'corrected': len(corrected),
                           'unchanged': len(obligations) - len(corrected),
                           'predecessor_links': sum(len(o['expected_rule_ids']) for o in old['source_obligations']),
                           'new_links': sum(len(o['expected_rule_ids']) for o in key['source_obligations'])},
        'review': {'path': REVIEW, 'bytes': REVIEW_BYTES, 'sha256': REVIEW_SHA,
                   'source_pins_checked': len(review['pins']), 'mismatches': physical_errors},
        'predecessor_package_unchanged': not physical_errors,
        'prescribed_ledgers_checked': len(key['claim_adjudication']['prescribed_ledgers']),
        'counterexamples_rejected': sum(x['ok'] for x in cx.values()),
        'counterexamples_total': len(cx), 'counterexamples': cx,
        'assessment_checks': assessments,
        'independent_approval': key['independent_approval']['status'],
        'trial_readiness': key['trial_readiness'], 'benchmark_ready': False,
        'native_executions': 0, 'agent_runs': 0, 'P1': 'open', 'C1': 'open',
        'limits': 'Author integrity/source-mapping and prescribed-ledger checks only. No review probe '
                  'replay, narrative truth certification, native evidence, isolation or independent approval.',
        'file_sha256': {p: H(rd(p)) for p in (KEY, MD, REVIEW, *OLD_PINS)},
        'checker_sha256': H(Path(__file__).read_bytes()),
    }, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
