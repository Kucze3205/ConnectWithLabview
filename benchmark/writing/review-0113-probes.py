"""Bounded independent #557 checks of the changed integration, never old probes.
Replay from repository root: python3 -I .session/artifacts/wp1-integration-probes.py
Writes only this session's evidence JSON; edited project bytes stay in memory.
"""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path.cwd()
BASE = '575d59ef8fcaf1f81a81d2eb605f52eb94053839'
CAND = '0e371f84162004146990cb1262b044dd4bf0dd79'
SCRIPT = 'benchmark/writing/verify_method.py'
PROV = 'benchmark/writing/integration-0112-provenance.json'
REPORT = ROOT / '.session/artifacts/wp1-integration-probes.json'
sha = lambda data: hashlib.sha256(data).hexdigest()
canonical = lambda obj: json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()
read = lambda path: (ROOT / path).read_bytes()
load = lambda path: json.loads(read(path))
result = {'schema_version': 1, 'issue': 557, 'scope': 'independent changed-integration preparation checks only', 'commands': [], 'checks': [], 'probes': []}

def command(argv, **kwargs):
    done = subprocess.run(argv, capture_output=True, **kwargs)
    row = {'argv': argv, 'exit_code': done.returncode,
           'stdout': done.stdout.decode(errors='replace'), 'stderr': done.stderr.decode(errors='replace')}
    result['commands'].append(row)
    return done

def git(*args):
    done = command(['git', *args])
    if done.returncode:
        raise RuntimeError(done.stderr.decode())
    return done.stdout

def check(name, condition, detail=None):
    result['checks'].append({'name': name, 'passed': bool(condition), 'detail': detail})

for label, commit, expected_tree in [
    ('baseline', BASE, 'bd09e3a07e772337a3f045f69611b9f51dd3e227'),
    ('candidate', CAND, '557a725623d04d1df5415751c4079bca056034f3'),
    ('checkout', 'HEAD', None),
]:
    resolved = git('rev-parse', commit + '^{commit}', commit + '^{tree}').decode().splitlines()
    identities = result.setdefault('identities', {})
    identities[label] = {'commit': resolved[0], 'tree': resolved[1]}
    check(label + '-tree', expected_tree is None or resolved[1] == expected_tree, resolved)
    for typ, oid in zip(('commit', 'tree'), resolved):
        raw = git('cat-file', typ, oid)
        actual = hashlib.sha1(typ.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        check(label + '-' + typ + '-object-address', actual == oid, actual)
        # Raw tree bytes are binary; replace command log stdout with its hash.
        result['commands'][-1]['stdout'] = {'size': len(raw), 'sha256': sha(raw), 'git_object_hash': actual}

allowed = {
    'benchmark/writing/method.json': 'M', 'benchmark/writing/README.md': 'M',
    'benchmark/writing/controls.json': 'M', SCRIPT: 'M',
    'benchmark/writing/verification.json': 'M', PROV: 'A',
    'benchmark/writing/integration-0112-provenance.md': 'A',
}
delta = {p: status for status, p in (s.split('\t') for s in git('diff', '--name-status', BASE, CAND).decode().splitlines())}
check('exact-seven-file-scope', delta == allowed, delta)
check('candidate-direct-parent-is-starting-baseline', git('rev-parse', CAND + '^').decode().strip() == BASE)
result['later_parent_changes'] = git('diff', '--name-status', CAND, 'HEAD').decode().splitlines()
check('diff-check', command(['git', 'diff', '--check', BASE, CAND]).returncode == 0)
check('initial-worktree-clean', not git('status', '--short').strip())
result['candidate_files'] = {}
for path in sorted(allowed):
    candidate = git('show', CAND + ':' + path)
    result['commands'][-1]['stdout'] = {'size': len(candidate), 'sha256': sha(candidate)}
    result['candidate_files'][path] = {'size': len(candidate), 'sha256': sha(candidate)}
    check('checkout-matches-candidate:' + path, read(path) == candidate)

prov = load(PROV)
proposal = load('benchmark/project-text-writing-0109.json')
review_path = 'benchmark/project-text-writing-0109/review-0110.json'
review = load(review_path)
check('preserved-review-exact-pin', len(read(review_path)) == 74366 and sha(read(review_path)) == '2dc007939a4b0637716027ef6e5a874702c9be7288daf80c3f007c07f382cdaf')
result['historical_identity_checks'] = {}
for name, identity in review['identities'].items():
    actual = git('rev-parse', identity['commit'] + '^{tree}').decode().strip()
    check('historical-review-tree:' + name, actual == identity['tree'], actual)
    result['historical_identity_checks'][name] = dict(identity, resolved_tree=actual)
for path, pin in review['scoped_files'].items():
    for name in ('accepted_candidate', 'task_544', 'reviewed_checkout'):
        data = git('show', review['identities'][name]['commit'] + ':' + path)
        result['commands'][-1]['stdout'] = {'size': len(data), 'sha256': sha(data)}
        check('historical-scoped-pin:' + name + ':' + path, len(data) == pin['size'] and sha(data) == pin['sha256'])
result['historical_unchanged'] = {}
for path, pin in prov['historical_unchanged'].items():
    baseline = git('show', BASE + ':' + path)
    result['commands'][-1]['stdout'] = {'size': len(baseline), 'sha256': sha(baseline)}
    ok = read(path) == baseline and len(baseline) == pin['size'] and sha(baseline) == pin['sha256']
    result['historical_unchanged'][path] = dict(pin, baseline_and_current_match=ok)
    check('historical-preservation:' + path, ok)
for path, pin in prov['baseline_files'].items():
    data = git('show', BASE + ':' + path)
    result['commands'][-1]['stdout'] = {'size': len(data), 'sha256': sha(data)}
    check('integration-baseline-pin:' + path, len(data) == pin['size'] and sha(data) == pin['sha256'])
for path, pin in prov['outputs'].items():
    check('integration-output-pin:' + path, len(read(path)) == pin['size'] and sha(read(path)) == pin['sha256'])
envelope_path = '.github/loop/data/session-reports/547/ba754b9a0cc86b2d1cd17aa6287c05ad71696775c9e2c92a22f9db02415d6861.json'
envelope = load(envelope_path)
check('review-envelope-provenance', sha(read(envelope_path)) == Path(envelope_path).stem and envelope['report']['issue'] == 547 and envelope['report']['snapshot'] == 'd6eb2085115b86ba4e78c52b2307ddf0d700826dc74a4d31043d5e6f9d7303ef')
export = load('.session/exports/records/0112.json')
check('staged-spec-outcome', any(s.get('issue') == 554 and s.get('commit') == '0e371f8' and s.get('merged') and s.get('verdict') == 'accepted' for s in export['outcome']['sessions']))
result['specification'] = {'path': '.session/exports/records/0112.json#/tasks/0/body', 'file_sha256': sha(read('.session/exports/records/0112.json')), 'body_sha256': sha(export['tasks'][0]['body'].encode()), 'outcome_commit': '0e371f8'}

method = load('benchmark/writing/method.json')
controls = load('benchmark/writing/controls.json')
old_method = json.loads(git('show', BASE + ':benchmark/writing/method.json'))
result['commands'][-1]['stdout'] = {'sha256': sha(canonical(old_method))}
old_controls = json.loads(git('show', BASE + ':benchmark/writing/controls.json'))
result['commands'][-1]['stdout'] = {'sha256': sha(canonical(old_controls))}
check('four-synthetic-tasks-unchanged', canonical(method['tasks'][:4]) == canonical(old_method['tasks']))
synthetic = {k: v for k, v in controls.items() if k not in ('strata', 'project_text')}
synthetic['visibility'] = old_controls['visibility']
check('all-synthetic-controls-unchanged', canonical(synthetic) == canonical(old_controls))
check('synthetic-digest-is-baseline', sha(canonical(old_controls)) == 'edb6c3324d50ca9693c3326583a4ca5f679c6428f6e521552e36f560a4c5231d')
check('task-digest-is-baseline', sha(canonical(old_method['tasks'])) == '1b6c682e02afa1763109b0d250e8be8a0145db685953f20386753bd6128ec414')
check('W1-W8-preserved-with-only-W2-qualification', all(canonical(a) == canonical(b) for a,b in zip(method['new_requirements'], old_method['new_requirements']) if a['id'] != 'W2') and method['new_requirements'][1]['requirement'].startswith(old_method['new_requirements'][1]['requirement']))
check('comparison-and-uncovered-inventory-preserved', canonical(method['comparison']) == canonical(old_method['comparison']) and method['coverage']['uncovered_families'] == old_method['coverage']['uncovered_families'])
check('mapping-copies-reviewed-proposal', canonical(method['tasks'][4]['requirements_mapping']) == canonical(proposal['requirements']) == canonical(prov['mapping']))

original = read('benchmark/real-project-0107/original.lvproj')
source = ET.fromstring(original)
locator = "./Item[@Name='My Computer']/Item[@Name='Build Specifications']/Item[@Name='AF PPL']/Property[@Name='Bld_version.build']"
selected = source.findall(locator)
marker = b'<Property Name="Bld_version.build" Type="Int">'
offset = original.index(marker) + len(marker)
positive_bytes = original[:offset] + b'3' + original[offset+1:]
check('independent-source-precondition', len(selected) == 1 and selected[0].text == '2' and selected[0].attrib == {'Name': 'Bld_version.build', 'Type': 'Int'} and len(selected[0]) == 0 and source.attrib == {'Type': 'Project', 'LVVersion': '20008000'})
check('independent-byte-locator', offset == 3347 and original[:offset].count(b'\n') + 1 == 42 and original[offset:offset+1] == b'2' and len(original) == 5806)
result['source_observation'] = {'path': proposal['source']['snapshot'], 'size': len(original), 'sha256': sha(original), 'root': source.attrib, 'match_count': len(selected), 'property': selected[0].attrib, 'original_text': selected[0].text, 'offset': offset, 'line': 42, 'allowed_output_sha256': sha(positive_bytes), 'changed_offsets': [i for i,(a,b) in enumerate(zip(original,positive_bytes)) if a != b], 'auto_increment': source.find(".//Property[@Name='Bld_autoIncrement']").text}

# Load only the changed integration verifier, without __main__ or bytecode writes.
ns = {'__file__': str(ROOT / SCRIPT), '__name__': 'independent_wp1_review'}
exec(compile(read(SCRIPT), str(ROOT / SCRIPT), 'exec'), ns)
ns['check_integration_inputs']()
base_example = {'original': original, 'original_after': original,
    'contract': copy.deepcopy(proposal['task']),
    'files': {proposal['task']['output_path']: positive_bytes, 'sentinel.txt': b'unchanged unrelated bytes'},
    'outcomes': dict(proposal['planned_results'], text_correctness='correct', root_version_declaration='correct')}
project_path = proposal['task']['output_path']

def probe(name, callback, expected):
    try:
        returned = callback()
        actual = 'accepted'
    except Exception as error:
        returned = None
        actual = str(error)
    row = {'name': name, 'expected': expected, 'actual': actual, 'matched': actual == expected}
    if returned is not None and name == 'independent-positive':
        row['return'] = returned
    result['probes'].append(row)

probe('independent-positive', lambda: ns['check_project_text'](base_example), 'accepted')
def byte_probe(name, data, expected):
    e = copy.deepcopy(base_example)
    e['files'][project_path] = data
    probe(name, lambda: ns['check_project_text'](e), expected)
byte_probe('original-no-op', original, 'project-no-op')
byte_probe('adjacent-major-instead-of-build', original.replace(b'Name="Bld_version.major" Type="Int">1', b'Name="Bld_version.major" Type="Int">3'), 'project-value')
for text in (b'4', b'03', b'3 ', b'&#51;'):
    byte_probe('nonexact-request-value:' + text.decode(), original[:offset] + text + original[offset+1:], 'project-value' if text in (b'4', b'03', b'3 ') else 'project-byte-delta')
for name, before, after, reason in [
    ('unrelated-auto-increment', b'Name="Bld_autoIncrement" Type="Bool">true', b'Name="Bld_autoIncrement" Type="Bool">false', 'project-byte-delta'),
    ('ancestor-type', b'Name="AF PPL" Type="Packed Library"', b'Name="AF PPL" Type="Library"', 'project-byte-delta'),
    ('root-type', b'Project Type="Project"', b'Project Type="Changed"', 'project-byte-delta'),
    ('root-version', b'LVVersion="20008000"', b'LVVersion="21008000"', 'project-version-declaration'),
    ('entity-reencode', b'&lt;', b'&#60;', 'project-byte-delta'),
    ('indentation', b'\t<Property Name="CCSymbols"', b' <Property Name="CCSymbols"', 'project-byte-delta'),
]:
    assert before in positive_bytes
    byte_probe(name, positive_bytes.replace(before, after, 1), reason)
byte_probe('BOM-removal', positive_bytes[3:], 'project-serialization')
byte_probe('all-lines-CRLF', positive_bytes.replace(b'\n', b'\r\n'), 'project-serialization')
byte_probe('remove-terminal-LF', positive_bytes[:-1], 'project-serialization')
byte_probe('XML-reserialization', ET.tostring(ET.fromstring(positive_bytes), encoding='utf-8', xml_declaration=True), 'project-serialization')
byte_probe('malformed-XML', positive_bytes.replace(b'</Project>', b'</Broken>'), 'mismatched tag: line 76, column 2')
for name, mutate, reason in [
    ('wrong-original-precondition', lambda e:e.update(original=positive_bytes), 'project-original-hash'),
    ('original-overwrite', lambda e:e.update(original_after=positive_bytes), 'project-original-not-preserved'),
    ('wrong-locator-contract', lambda e:e['contract'].update(locator='.//Property'), 'project-locator'),
    ('wrong-text-precondition-contract', lambda e:e['contract']['precondition'].update(text='3'), 'project-precondition'),
    ('two-byte-allowance-contract', lambda e:e['contract']['delta'].update(allowed_changed_bytes=2), 'project-delta-contract'),
    ('missing-sentinel', lambda e:e['files'].pop('sentinel.txt'), 'project-file-set'),
    ('missing-project', lambda e:e['files'].pop(project_path), 'project-file-set'),
    ('unexpected-license-output', lambda e:e['files'].update({'LICENSE.txt':b'other'}), 'project-file-set'),
    ('changed-sentinel', lambda e:e['files'].update({'sentinel.txt':b'changed'}), 'project-unrelated-file'),
]:
    e = copy.deepcopy(base_example)
    mutate(e)
    probe(name, lambda e=e:ns['check_project_text'](e), reason)
for field in ('native_validity', 'dependency_resolution', 'build', 'behavior', 'save_version', 'overall_writing'):
    e = copy.deepcopy(base_example)
    e['outcomes'][field] = 'correct'
    probe('unsupported-pass:' + field, lambda e=e:ns['check_project_text'](e), 'project-unsupported-pass')

# Rehash only new in-memory integration output pins to get past integrity and
# independently exercise inventory/reason enforcement. No repository bytes change.
def main_overlay(method_value=None, controls_value=None, provenance_value=None, rehash=True):
    saved = ns['READ_INPUTS']
    ns['READ_INPUTS'] = {}
    p = copy.deepcopy(prov if provenance_value is None else provenance_value)
    for path,value in [('benchmark/writing/method.json', method_value), ('benchmark/writing/controls.json', controls_value)]:
        if value is not None:
            data = canonical(value)
            ns['READ_INPUTS'][path] = data
            if rehash:
                p['outputs'][path] = {'size': len(data), 'sha256': sha(data)}
    ns['READ_INPUTS'][PROV] = canonical(p)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            ns['main']()
    finally:
        ns['READ_INPUTS'] = saved

for name, modify, reason in [
    ('drop-project-control', lambda c:c['project_text']['rejecting_controls'].pop(), 'project-rejecting-control-inventory'),
    ('change-project-reason', lambda c:c['project_text']['rejecting_controls'][0].update(reason='other'), 'project-rejecting-control-inventory'),
    ('duplicate-project-id', lambda c:c['project_text']['rejecting_controls'].append(copy.deepcopy(c['project_text']['rejecting_controls'][0])), 'project-rejecting-control-inventory'),
    ('project-control-wrong-cause', lambda c:c['project_text']['rejecting_controls'][0].update(changes=[{'path':['sentinel'], 'value':'wrong'}]), 'project-wrong-rejection-reason:project-no-op:project-unrelated-file'),
    ('drop-synthetic-control', lambda c:c['rejecting_controls'].pop(), 'rejecting-control-inventory'),
    ('change-synthetic-reason', lambda c:c['rejecting_controls'][0].update(reason='other'), 'rejecting-control-inventory'),
]:
    changed = copy.deepcopy(controls)
    modify(changed)
    probe(name, lambda changed=changed:main_overlay(controls_value=changed), reason)
changed = copy.deepcopy(method)
changed['tasks'].pop()
probe('drop-WP1-method-task', lambda:main_overlay(method_value=changed), 'task-inventory')
changed2 = copy.deepcopy(method)
changed2['tasks'][4]['originals'][0]['save_version'] = '20008000'
probe('declare-root-as-native-save-version', lambda:main_overlay(method_value=changed2), 'invented-original-version')
changed3 = copy.deepcopy(method)
changed3['tasks'][4]['text_contract']['delta']['offset_zero_based'] += 1
probe('method-offset-drift', lambda:main_overlay(method_value=changed3), 'project-task-contract')
probe('changed-method-without-new-pin', lambda:main_overlay(method_value=changed3, rehash=False), 'integration-output-pin-drift:benchmark/writing/method.json')
p = copy.deepcopy(prov)
p['historical_unchanged'].pop('benchmark/preparation.json')
probe('drop-historical-preparation-pin', lambda:main_overlay(provenance_value=p), 'historical-pin-inventory')
p2 = copy.deepcopy(prov)
p2['outputs'][PROV] = {'size':len(read(PROV)), 'sha256':sha(read(PROV))}
probe('introduce-circular-self-pin', lambda:main_overlay(provenance_value=p2), 'integration-output-inventory')

# Independent runtime verification plus audited environment/cwd/CLI boundaries.
normal = command(['python3', '-I', SCRIPT])
recorded = load('benchmark/writing/verification.json')
actual = json.loads(normal.stdout)
check('current-verifier-exit', normal.returncode == 0 and normal.stderr == b'')
check('recorded-stdout-and-result-reproduce', normal.stdout.decode() == recorded['stdout'] and actual == recorded['result'] and sha(normal.stdout) == recorded['stdout_sha256'])
check('recorded-checker-pin', sha(read(SCRIPT)) == actual['checker_sha256'] == recorded['checker_sha256'])
check('recorded-all-actual-input-pins', all(sha(read(p)) == pin for p,pin in actual['inputs_sha256'].items()))
check('acyclic-integration-pin-graph', PROV not in prov['outputs'] and 'benchmark/writing/verification.json' not in prov['outputs'] and 'benchmark/writing/verification.json' not in actual['inputs_sha256'])
audit = '''import os,sys,runpy
from pathlib import Path
script=sys.argv[1]
sys.argv=[script]
sys.dont_write_bytecode=True
def audit(event,args):
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes,os.PathLike)) and '.session' in Path(os.fsdecode(path)).parts:
            raise PermissionError('session read denied')
        if (isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):
            raise PermissionError('file write denied')
    if event in {'os.remove','os.rename','os.rmdir','os.mkdir','os.link','os.symlink','os.chmod','os.truncate','os.utime','subprocess.Popen','os.system','socket.__new__','socket.connect','socket.bind','socket.getaddrinfo'}:
        raise PermissionError('filesystem/process/network mutation denied')
sys.addaudithook(audit)
runpy.run_path(script,run_name='__main__')
'''
isolated = command([sys.executable, '-I', '-c', audit, str(ROOT / SCRIPT)], cwd='/', env={})
check('isolated-no-write-no-session-no-network-repeat', isolated.returncode == 0 and isolated.stderr == b'' and isolated.stdout == normal.stdout, {'cwd':'/', 'environment':{}, 'stdout_sha256':sha(isolated.stdout)})
extra = command([sys.executable, '-I', str(ROOT / SCRIPT), '--candidate'], cwd='/', env={})
check('external-candidate-argument-rejected', extra.returncode == 1 and extra.stdout == b'' and extra.stderr == b'writing method verification failed: no-external-inputs-supported\n')
check('final-worktree-clean', not git('status', '--short').strip())
result['summary'] = {'checks': len(result['checks']), 'failed_checks': [r for r in result['checks'] if not r['passed']], 'probes': len(result['probes']), 'mismatched_probes': [r for r in result['probes'] if not r['matched']], 'verifier_stdout_sha256':sha(normal.stdout), 'synthetic_rejections': actual['rejected_count'], 'project_rejections': actual['project_text_preparation']['rejected_count'], 'no_frozen_checkers_executed':True, 'no_historical_probes_replayed':True, 'no_native_or_agent_execution':True}
# Avoid binary or repetitive command dumps: retain exact verifier stdout once.
for row in result['commands']:
    if isinstance(row['stdout'],str) and row['stdout'] == normal.stdout.decode() and row['argv'] != ['python3','-I',SCRIPT]:
        row['stdout'] = {'identical_to_primary_verifier':True, 'sha256':sha(normal.stdout)}
REPORT.write_text(json.dumps(result,indent=2,ensure_ascii=False) + '\n')
print(json.dumps(result['summary'],indent=2))
print('EVIDENCE', REPORT.relative_to(ROOT), 'SHA256', sha(REPORT.read_bytes()))
