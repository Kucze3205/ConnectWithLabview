#!/usr/bin/env python3
"""Read-only integrity and coverage checker for the WP1 frozen key package (issue #577; revision 0119).

Standard library only; reads repository files, writes nothing. It re-derives the
obligation inventory from the current method.json and benchmark/protocol.md and
compares it with the package, so it does not merely compare two author lists.
Limits: this certifies package integrity and source coverage only. It does not
certify narrative truth, native behavior, independent approval or trial readiness.
Run from anywhere: python3 -I benchmark/writing/check_wp1_key_0119.py
"""
import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEY = 'benchmark/writing/wp1-key-0119.json'
MD = 'benchmark/writing/wp1-key-0119.md'
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
START_COMMIT = '3963123388e34ddfcad83daf81fd6facf8bf0529'
START_TREE = '35af29e3fecfe7fd42469f57a5ffce965d5d3f66'
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




# These hashes freeze authored text, not semantic validity.
AUTHORED_PINS = {'F3': '9fbd75d2b43d93a073bbd2c6b7ea4cdb6584d0fd36665fa9bb86e89782032880', 'F4': '3180d3b91a89373727d8b0cd5f9cce06fa4d3c1279198bf05d96bfb03a660a5b', 'preparer': '3dc3dd8400541d8ddf63b5662003971851e22f459440896e230ce3ee591c27f4', 'map_block': '7b1043fbc82e307a502fea34e8b8ab07251b4f8b0306a2ba7627095e57f06847', 'C1-correct:evidence': '716297651f50b980fe75495c98261e9d0bf03555825510717373d457ead169b9', 'C1-correct:context': '36bee5cbbcb957e6bf97f9d79202d8ecde0fce5ebe8ccf06ccf2043e8cd915c1', 'C1-unverified-extra:evidence': '23cf9789257090e8a8cad41f928c31af1b5c9f633c5940ab2f25f68691b5769f', 'C1-unverified-extra:context': '1b30b29a0b2a9cbbd891cdb9533c3a47252f16d62a8d96149a9d71d3709fbae4'}
DOC_PINS = {'pre_edit_findings': {'path': 'benchmark/writing/wp1-key-0119-pre-edit-findings.md', 'bytes': 3688, 'sha256': 'c393b7bbfaf7ecb593688b1bbaf1827ce70a720ae7bc5d676430800b1785b3db'}, 'preservation_provenance': {'path': 'benchmark/writing/review-0118-provenance.md', 'bytes': 2809, 'sha256': '22b4d2a6f0aad05db01c7e2f52fd5aeab2e93dd977b8ee0d9b8ff2167ba91969'}}
COLD_NOTE = 'Unchanged 0118 artifact /session_identity and /cold_derivation; satisfied for that reviewer session only; this author is exposed.'

# Revision 0119 controls appended to an adapted source-derived integrity core.
# No historical checker or review audit is imported or executed.
_base_check_key = check_key
D = 'benchmark/writing/'
REVIEW = D + 'wp1-key-review-0118.json'
PREDECESSOR = D + 'wp1-key-0117.json'
MAP_ID = 'WP1-original-output-grounding'
AFFECTED = ['C1-correct', 'C1-unverified-extra']
PRESERVED = {
    REVIEW: (569049, '410b0ebf7d3135521d10bd32d3b1102769caa848f5e5c7278d8e9a29eefd9a55'),
    D + 'wp1-cold-expectation-0118.json': (5036, '7ca817b22c430ece354287b0e42cd3deb106afaeee9a0d3d6c9d7dfd4dad141c'),
    D + 'wp1-source-interpretation-0118.json': (2257, 'b18eb04d01455a3d4b539a67042a83c4efc5d627f73ccd309ba6f1e7f48ea46b'),
    D + 'wp1-review-audit-0118.py': (31314, '8fc53c741b4d6628228e0abae53fbf3c64200c3f318d6ac903c8bbf73b13e833'),
}
PREDECESSOR_PINS = {
    PREDECESSOR: (306601, '008b4078d7f50610c7eb74e7d880e20602416130398fabf7a7534ae2a6b60982'),
    D + 'wp1-key-0117.md': (11253, 'ba62fabd3324329447515728d38113185ee7e7702faead0f6ca7f68a5a0a97a3'),
    D + 'check_wp1_key_0117.py': (37193, 'f23b829059ace8a5e77b017779c60902020057809c10663b2892ea210c31925d'),
    D + 'wp1-key-0117-verification.json': (57834, 'e3e7b3da3d354b61a978d6458f7e5e523ba425dcec7ecc5699a7a513e25ea27a'),
}
# Authored semantic choice: checked against literal source leaves before editing.
# These links and frozen texts still need a separate human semantic review.
F3_LINKS = {
    'method#/common/artifact_fidelity_rule': ['R-text', 'R-bytes', 'R-files', 'R-root', 'R-native', 'R-dimensions'],
    'method#/tasks/4/requirements_mapping/W1/review': ['R-text', 'R-files'],
    'method#/tasks/4/requirements_mapping/W2/review': ['R-preflight', 'R-native'],
    'method#/tasks/4/requirements_mapping/W3/review': ['R-text', 'R-bytes', 'R-files'],
    'method#/tasks/4/requirements_mapping/W4/review': ['R-root', 'R-native'],
    'method#/tasks/4/requirements_mapping/W5/review': ['R-dimensions', 'R-limits', 'R-native'],
    'method#/tasks/4/requirements_mapping/W8/review': ['R-controls', 'R-native'],
}


def pointer(value, locator):
    for s in locator.strip('/').split('/'):
        s = s.replace('~1', '/').replace('~0', '~')
        value = value[int(s)] if isinstance(value, list) else value[s]
    return value


def pins(records):
    return [{'path': p, 'bytes': n, 'sha256': h} for p, (n, h) in records.items()]


def assess(required, extras=(), inventory=True):
    """Protocol L41, on human-assigned outcomes; never accepts narrative text."""
    if not inventory or not required:
        return 'unverified'
    values = list(required) + list(extras)
    if 'incorrect' in values:
        return 'incorrect'
    if 'unverified' in values:
        return 'unverified'
    if all(x == 'correct' for x in values):
        return 'correct'
    if any(x in ('correct', 'partial') for x in values):
        return 'partial'
    if 'error' in values:
        return 'error'
    if all(x == 'unsupported' for x in required):
        return 'unsupported'
    return 'missing'


def check_key(key, ctx, md):
    errors = _base_check_key(key, ctx, md)
    add = errors.append
    old, review = ctx['old'], ctx['review']
    if key.get('revision') != 'wp1-key-0119-v1' or key.get('issue') != 577 or key.get('status') != 'proposed-awaiting-separate-check':
        add('revision-status')
    allowed = {'revision', 'issue', 'starting_revision', 'preparer', 'revision_provenance',
               'source_obligations', 'required_ids', 'claim_adjudication', 'finding_dispositions'}
    if set(key) != set(old):
        add('top-level-inventory')
    for field in set(old) - allowed:
        if key.get(field) != old[field]:
            add('unrelated-policy-drift')
    by = {x.get('id'): x for x in key.get('source_obligations', [])}
    for source in old['source_obligations']:
        expected = copy.deepcopy(source)
        oid = source['id']
        if oid in F3_LINKS:
            expected['expected_rule_ids'] = F3_LINKS[oid]
        if by.get(oid) != expected:
            add('f3-operative-mapping' if oid in F3_LINKS else 'unrelated-mapping-drift')
    finding = next(f for f in review['findings'] if f['id'] == 'F3')
    if {e['id'] for e in finding['evidence']} != set(F3_LINKS):
        add('review-f3-locators')
    for e in finding['evidence']:
        if pointer(ctx['method'], e['source']['locator']) != e['source']['value']:
            add('review-source-semantics-drift')
    disp = key.get('finding_dispositions', {})
    for name in old['finding_dispositions']:
        if disp.get(name) != old['finding_dispositions'][name]:
            add('historical-disposition-drift')
    if set(disp) != set(old['finding_dispositions']) | {'F3', 'F4'}:
        add('finding-inventory')
    f3, f4 = disp.get('F3', {}), disp.get('F4', {})
    if f3.get('status') != 'corrected-proposed-awaiting-separate-check':
        add('f3-status')
    if H(canon(f3)) != AUTHORED_PINS['F3']:
        add('f3-disposition')
    if f4.get('status') != 'blocked-for-missing-evidence' or f4.get('affected_required_ids') != [MAP_ID] or f4.get('affected_examples') != AFFECTED:
        add('f4-block')
    if H(canon(f4)) != AUTHORED_PINS['F4']:
        add('f4-disposition')
    mappings = f3.get('mappings', [])
    if {x.get('obligation_id') for x in mappings} != set(F3_LINKS) or len(mappings) != 7:
        add('f3-disposition')
    for row in mappings:
        oid = row.get('obligation_id')
        if oid not in F3_LINKS or row.get('new_rule_ids') != F3_LINKS[oid]:
            add('f3-disposition')
    items = {x.get('id'): x for x in key.get('required_ids', [])}
    for old_item in old['required_ids']:
        current = copy.deepcopy(items.get(old_item['id'], {}))
        block = current.pop('established_key_use', None) if old_item['id'] == MAP_ID else None
        if current != old_item:
            add('required-id-continuity')
        if old_item['id'] == MAP_ID:
            if not isinstance(block, dict) or block.get('status') != 'blocked' or block.get('finding') != 'F4' or block.get('affected_examples') != AFFECTED:
                add('f4-block')
            elif H(canon(block)) != AUTHORED_PINS['map_block']:
                add('f4-block-evidence')
    ca = key.get('claim_adjudication', {})
    for field in set(old['claim_adjudication']) - {'prescribed_ledgers'}:
        if ca.get(field) != old['claim_adjudication'][field]:
            add('adjudication-continuity')
    ledgers = ca.get('prescribed_ledgers', [])
    names = [x.get('id') for x in ledgers]
    old_names = [x['id'] for x in old['claim_adjudication']['prescribed_ledgers']]
    if names != old_names:
        add('ledger-inventory')
    for ledger in ledgers:
        name = ledger.get('id')
        original = next((x for x in old['claim_adjudication']['prescribed_ledgers'] if x['id'] == name), None)
        if original is None:
            continue
        if name not in AFFECTED:
            if ledger != original:
                add('unaffected-ledger-drift')
            continue
        expected = copy.deepcopy(original)
        expected['items'][1].update(correctness='partial', grounding='partial', established_key_use='blocked-F4')
        expected['assessment'] = {'answer_correctness': 'partial' if name == 'C1-correct' else 'unverified', 'source_grounding': 'partial'}
        for field in set(original) - {'conditions', 'rationale'}:
            if ledger.get(field) != expected[field]:
                add('f4-ledger-outcome' if field in ('items', 'assessment') else 'affected-ledger-continuity')
        if not ledger.get('conditions', '').startswith(original['conditions']) or not ledger.get('rationale'):
            add('f4-evidence-context')
        evidence = ledger.get('evidence_reservation', {})
        if evidence.get('status') != 'blocked-missing-complete-preservation-map' or evidence.get('unseen_sidecars_assumed') is not False or evidence.get('complete_preservation_map_supplied') is not False:
            add('f4-evidence-context')
        coverage = evidence.get('coverage', [])
        if [x.get('required_id') for x in coverage] != ctx['task']['semantic_ids'] + ctx['task']['preservation_ids'] or any(not x.get('evidence') for x in coverage):
            add('f4-evidence-inventory')
        if evidence.get('missing_evidence') != f4.get('missing_evidence') or len(evidence.get('missing_evidence', [])) != 3:
            add('f4-missing-evidence')
        if H(canon(evidence)) != AUTHORED_PINS[name + ':evidence']:
            add('f4-evidence-pin')
        if H(canon({'conditions': ledger.get('conditions'), 'rationale': ledger.get('rationale')})) != AUTHORED_PINS[name + ':context']:
            add('f4-evidence-context')
        ref = evidence.get('review_reference', {})
        try:
            reviewed = pointer(review, ref['locator'])
            if ref.get('path') != REVIEW or reviewed['id'] != name or evidence.get('raw_answer_utf8_sha256') != H(reviewed['raw_answer'].encode()) or ledger.get('raw_answer_reference') != reviewed['raw_reference']:
                add('f4-raw-evidence')
        except (KeyError, IndexError, TypeError, ValueError):
            add('f4-raw-evidence')
        for dimension, field in [('correctness', 'answer_correctness'), ('grounding', 'source_grounding')]:
            values = [x.get(dimension) for x in ledger.get('items', [])]
            extras = [x.get(dimension) for x in ledger.get('extras', [])]
            if ledger.get('assessment', {}).get(field) != assess(values, extras):
                add('ledger-assessment')
    provenance = key.get('revision_provenance', {})
    if provenance.get('predecessor_revision') != old['revision'] or provenance.get('predecessor_package') != pins(PREDECESSOR_PINS) or provenance.get('predecessor_revision_provenance') != old['revision_provenance']:
        add('predecessor-provenance')
    if provenance.get('preserved_inputs') != pins(PRESERVED) or provenance.get('review_issue') != 574 or provenance.get('reviewed_revision') != review['reviewed_revision'] or provenance.get('historical_verdicts') != review['verdicts'] or provenance.get('historical_P1') != review['P1']:
        add('review-provenance')
    if provenance.get('source_pin_comparison') != {'scoped_pins_checked': len(review['scoped_pins']), 'mismatches': []}:
        add('review-source-pins')
    for field, record in DOC_PINS.items():
        if provenance.get(field) != record or H(rd(record['path'])) != record['sha256'] or len(rd(record['path'])) != record['bytes']:
            add('provenance-document-pin')
    if H(canon(key.get('preparer'))) != AUTHORED_PINS['preparer'] or provenance.get('cold_provenance') != COLD_NOTE:
        add('author-exposure-provenance')
    return sorted(set(errors))


def focused_counterexamples(key, ctx, md):
    """Current-package metadata mutations only: no historical probe replay."""
    results = {}
    def run(name, expected, change):
        altered = copy.deepcopy(key)
        change(altered)
        errors = check_key(altered, ctx, md)
        results[name] = {'expected': expected, 'rejected_for': errors, 'ok': expected in errors}
    def obligation(k, oid):
        return next(x for x in k['source_obligations'] if x['id'] == oid)
    def ledger(k, name):
        return next(x for x in k['claim_adjudication']['prescribed_ledgers'] if x['id'] == name)
    for oid, links in F3_LINKS.items():
        run('f3-restore-scope-only:' + oid, 'f3-operative-mapping', lambda k, oid=oid: obligation(k, oid).update(expected_rule_ids=['R-scope', 'R-independent']))
        for missing in links:
            run('f3-drop:' + oid + ':' + missing, 'f3-operative-mapping', lambda k, oid=oid, missing=missing: obligation(k, oid)['expected_rule_ids'].remove(missing))
    run('unrelated-mapping-changed', 'unrelated-mapping-drift', lambda k: k['source_obligations'][0].update(expected_rule_ids=['R-controls']))
    run('review-pin-forged', 'review-provenance', lambda k: k['revision_provenance']['preserved_inputs'][0].update(sha256='0' * 64))
    run('predecessor-pin-forged', 'predecessor-provenance', lambda k: k['revision_provenance']['predecessor_package'][0].update(sha256='0' * 64))
    run('map-ID-unblocked', 'f4-block', lambda k: next(x for x in k['required_ids'] if x['id'] == MAP_ID)['established_key_use'].update(status='approved'))
    run('F4-closed', 'f4-block', lambda k: k['finding_dispositions']['F4'].update(status='resolved'))
    run('author-relabelled-cold', 'author-exposure-provenance', lambda k: k['preparer'].update(exposure='cold'))
    for name in AFFECTED:
        run(name + ':map-credit-without-evidence', 'f4-ledger-outcome', lambda k, name=name: ledger(k, name)['items'][1].update(correctness='correct', grounding='correct'))
        run(name + ':map-slot-unblocked', 'f4-ledger-outcome', lambda k, name=name: ledger(k, name)['items'][1].pop('established_key_use'))
        run(name + ':invented-sidecars', 'f4-evidence-context', lambda k, name=name: ledger(k, name)['evidence_reservation'].update(unseen_sidecars_assumed=True))
        run(name + ':complete-map-asserted', 'f4-evidence-context', lambda k, name=name: ledger(k, name)['evidence_reservation'].update(complete_preservation_map_supplied=True))
        run(name + ':evidence-list-removed', 'f4-missing-evidence', lambda k, name=name: ledger(k, name)['evidence_reservation'].update(missing_evidence=[]))
        for index in range(5):
            run(name + ':coverage-removed:' + str(index), 'f4-evidence-inventory', lambda k, name=name, index=index: ledger(k, name)['evidence_reservation']['coverage'].pop(index))
        run(name + ':raw-evidence-forged', 'f4-raw-evidence', lambda k, name=name: ledger(k, name)['evidence_reservation'].update(raw_answer_utf8_sha256='0' * 64))
    return results


def main():
    physical_errors = []
    for path, (size, sha) in {**PRESERVED, **PREDECESSOR_PINS}.items():
        data = rd(path)
        if (len(data), H(data)) != (size, sha):
            physical_errors.append('fixed-input-pin:' + path)
    if physical_errors:
        print(json.dumps({'status': 'failed', 'package_errors': physical_errors}))
        return 1
    review, old = json.loads(rd(REVIEW)), json.loads(rd(PREDECESSOR))
    for pin in review['scoped_pins']:
        data = rd(pin['path'])
        if (len(data), H(data)) != (pin['bytes'], pin['sha256']):
            physical_errors.append('review-scoped-pin:' + pin['path'])
    key, md = json.loads(rd(KEY)), rd(MD).decode()
    method, task, obligations = derive()
    ctx = {'method': method, 'task': task, 'ob': obligations, 'facts': original_facts(task), 'old': old, 'review': review}
    errors = sorted(set(physical_errors + check_key(key, ctx, md)))
    controls = counterexamples(key, ctx, md)
    controls.update(focused_counterexamples(key, ctx, md))
    # Small current F4 precedence checks; no completed F1/F2 review is replayed.
    assessments = {
        'incomplete-positive': assess(['correct', 'partial', 'correct']) == 'partial',
        'unverified-extra-retained': assess(['correct', 'partial', 'correct'], ['unverified']) == 'unverified',
        'missing-extra-support-retained': assess(['correct', 'partial', 'correct'], ['missing']) == 'partial',
    }
    ok = not errors and all(x['ok'] for x in controls.values()) and all(assessments.values())
    print(json.dumps({
        'status': 'package-integrity-consistent-with-explicit-F4-block' if ok else 'failed',
        'revision': key['revision'], 'package_errors': errors,
        'mapping_counts': {'changed_from_0117': 7, 'unchanged_from_0117': len(obligations) - 7,
                           'predecessor_links': sum(len(o['expected_rule_ids']) for o in old['source_obligations']),
                           'new_links': sum(len(o['expected_rule_ids']) for o in key['source_obligations'])},
        'derived_obligations': len(obligations), 'required_ids': len(key['required_ids']), 'rules': len(key['rules']),
        'review_scoped_pins_checked': len(review['scoped_pins']), 'preserved_inputs_checked': len(PRESERVED),
        'predecessor_package_unchanged': not physical_errors,
        'counterexamples_rejected': sum(x['ok'] for x in controls.values()), 'counterexamples_total': len(controls),
        'counterexamples': controls, 'assessment_checks': assessments,
        'blocked_required_ids': [MAP_ID], 'blocked_example_map_slots': AFFECTED,
        'F3': 'author-corrected-awaiting-separate-semantic-recheck', 'F4': 'blocked-for-missing-evidence',
        'C1': 'open', 'historical_P1': 'unchanged; 0118 satisfaction is session-specific', 'author_exposure': 'exposed',
        'independent_approval': 'pending', 'trial_readiness': 'pending', 'benchmark_ready': False,
        'native_executions': 0, 'agent_runs': 0, 'project_files_written': 0,
        'limits': 'Repository-only package consistency, not semantic clearance. F4 remains blocked; human mapping, atomic truth, completeness, extras, contradictions and citation support adjudication remain required. No historical audit/checker/probe execution.',
        'file_sha256': {p: H(rd(p)) for p in (KEY, MD, *PRESERVED, *PREDECESSOR_PINS)},
        'checker_sha256': H(Path(__file__).read_bytes()),
    }, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, KeyError, IndexError, TypeError, ValueError, AssertionError) as exc:
        print(json.dumps({'status': 'failed', 'package_errors': ['malformed-or-missing-evidence'], 'detail': str(exc)}))
        sys.exit(1)
