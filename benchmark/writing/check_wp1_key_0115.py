#!/usr/bin/env python3
"""Read-only integrity and coverage checker for the WP1 frozen key package (issue #564).

Standard library only; reads repository files, writes nothing. It re-derives the
obligation inventory from the current method.json and benchmark/protocol.md and
compares it with the package, so it does not merely compare two author lists.
Limits: this certifies package integrity and source coverage only. It does not
certify narrative truth, native behavior, independent approval or trial readiness.
Run from anywhere: python3 -I benchmark/writing/check_wp1_key_0115.py
"""
import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEY = 'benchmark/writing/wp1-key-0115.json'
MD = 'benchmark/writing/wp1-key-0115.md'
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
START_COMMIT = 'e57b1c0fa9c88be18eadf4ed0cdc3f92665e1f4d'
START_TREE = '354b36e13ea0953207d8e1d02fcdd8c4bd6b3b3b'
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


def main():
    key = json.loads(rd(KEY).decode('utf-8'))
    md = (ROOT / MD).read_text(encoding='utf-8') if (ROOT / MD).is_file() else None
    m, task, ob = derive()
    ctx = {'method': m, 'task': task, 'ob': ob, 'facts': original_facts(task)}
    base = check_key(key, ctx, md)
    cx = counterexamples(key, ctx, md or '') if md else {}
    ok = not base and bool(cx) and all(v['ok'] for v in cx.values())
    nprot = sum(1 for i in ob if i.startswith('protocol#'))
    print(json.dumps({
        'status': 'package-integrity-consistent' if ok else 'failed',
        'package_errors': base,
        'derived_obligations': {'method_pointers': len(ob) - nprot, 'protocol_lines': nprot,
                                'key_obligations': len(key['source_obligations'])},
        'required_ids': [x['id'] for x in key['required_ids']],
        'rules': len(key['rules']), 'read_inputs': len(key['read_input_manifest']),
        'counterexamples_rejected': sum(v['ok'] for v in cx.values()),
        'counterexamples_total': len(cx), 'counterexamples': cx,
        'independent_approval': key['independent_approval']['status'],
        'trial_readiness': key['trial_readiness'], 'native_executions': 0, 'agent_runs': 0,
        'limits': 'Integrity and source-coverage checks only: not narrative truth, not C1 adjudication, '
                  'not native evidence, not isolation, not independent approval or trial readiness.',
        'checker_sha256': H(Path(__file__).read_bytes())}, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
