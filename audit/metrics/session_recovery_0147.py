"""Normalize only selected staged metadata; never emit runtime payloads or pool data."""
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path('.')
PIN = '510fc5af213cbe9f66dde42a27e3467bc225afcd'
ITERATIONS = {'643': '0138', '653': '0141', '663': '0144', '669': '0146'}
FIRST = {
    '643': '898877dd115aa8267a010119d1f09ef481d83f31',
    '653': '9f8a23ad1b1b4a4d90fe9aa8739558b766606bc5',
    '663': '13817283b1c0e4670fb8e5da236c27521b8be969',
    '669': PIN,
}
LAST = {
    '643': '3b16ea14e0cc9a66af9e916a15470f289b356119',
    '653': 'd9511a814bf67e4e075e02ffa5c2fe608d838f00',
    '663': '9ba5a679ca67a783661f43245f13480bccde3baa',
    '669': PIN,
}

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def load(path):
    return json.loads(pathlib.Path(path).read_text())

def git(*args):
    return subprocess.check_output(['git', *args])

def runtime(pin, issue):
    pointer = pin + ':sessions/' + issue + '.json'
    raw = git('show', pointer)
    return json.loads(raw), {'pointer': pointer, 'sha256': digest(raw)}

def stamp(pin):
    return git('show', '-s', '--format=%cI', pin).decode().strip()

def duration(name, start, end):
    seconds = (dt.datetime.fromisoformat(end.replace('Z', '+00:00')) -
               dt.datetime.fromisoformat(start.replace('Z', '+00:00'))).total_seconds()
    assert seconds >= 0, (name, start, end)
    return {'name': name, 'start': start, 'end': end, 'seconds': seconds}

manifest = load('.session/exports/manifest.json')
paths = [pathlib.Path('.session/exports/manifest.json')]
paths += sorted(pathlib.Path('.session/exports').glob('*/*.json'))
paths += [pathlib.Path(p) for p in (
    '.session/issue.md', '.session/role/SKILL.md', '.session/startup.json',
    '.session/history/manifest.json', 'policy/observations/0147-policy-check.md',
    'docs/perpetua/operating-parameters.md', 'docs/perpetua/engine.md',
    '.github/workflows/session.yml', '.github/loop/loop.py',
    'audit/metrics/session_recovery_0147.py')]
sources = {str(p): {'sha256': digest(p.read_bytes()), 'bytes': p.stat().st_size} for p in paths}
doc = {
    'schema_version': 1,
    'method': {
        'selection': 'Issue #672 explicit exports only; policy observation 0147 runtime measurements reused. Selected runtime fields at the named final pin and its first final checkpoints verify continuation attribution, without replay or artifact reconstruction.',
        'checkout': git('rev-parse', 'HEAD').decode().strip(),
        'runtime_pin': PIN,
        'availability': manifest['results'],
        'hashes': 'SHA256 over actual staged file bytes and git-show runtime blob bytes; report snapshot hashes are separate identities, not export file hashes.',
        'time': 'UTC. Git checkpoint times date publication of a continuation, not Finish execution. Run updated_at is an observation of workflow completion, not a precise output-publication timestamp. Durations use explicit pairs only; step wall intervals are not model-active time.',
        'actions_mapping': 'Each run retains id, attempt, job id and zero-based JSON pointers. Workflow checkout maps session upload immediately before Pack to diagnostic stream, after Pack to results; epilogue first download to results and second to baseline. This mapping is source-based, not historical artifact-content inspection.',
        'limitations': ['No streams or Actions step logs staged; manifest cannot distinguish expiry, pruning or never-uploaded streams.', 'No original results archive, per-file packing manifest, historical release catalogue or exact output publication timestamp staged.', 'Current engine source explains possible control flow only; historical executed source and exception are not certified.', 'Zero final recorded artifacts does not prove none were ever partially uploaded. Null outputs_asset also occurs in successful control.', 'No benchmark quality, readiness, subscription quota or monetary cost measured.'],
    },
    'sources': sources,
    'sessions': {},
}
for issue, iteration in ITERATIONS.items():
    initial, initial_source = runtime(FIRST[issue], issue)
    final, final_source = runtime(PIN, issue)
    assert final['history'][:len(initial['history'])] == initial['history']
    first_time, last_time = stamp(FIRST[issue]), stamp(LAST[issue])
    evidence = [initial_source['pointer'] + '#/history/' + str(len(initial['history']) - 1), final_source['pointer'],
                'policy/observations/0147-policy-check.md#recovery-discovery-and-audit-evidence']
    missing = ['Original results archive and contents at packaging/download/admission boundaries', 'Epilogue stderr/exception and within-step progress', 'Exact final artifact publication time and historical partial-upload state', 'Stream artifact retention/upload history']
    s = {'cause_status': 'undetermined', 'evidence': evidence, 'missing': missing, 'durations': [],
         'runtime_sources': {'first': initial_source, 'final': final_source},
         'checkpoint': {'first_final': first_time, 'last_final': last_time,
                        'first_pin': FIRST[issue], 'last_pin': LAST[issue],
                        'first_status': initial['result']['status'], 'final_status': final['result']['status'],
                        'note': 'Checkpoint publication occurs inside epilogue, after successful session result upload/download; not the Finish execution timestamp.'},
         'outputs_asset': {'first': initial['outputs_asset'], 'final': final['outputs_asset']},
         'runs': []}
    if issue != '669':
        s['durations'].append(duration('first_to_later_final_checkpoint_gap_not_agent_active', first_time, last_time))
    indices = list(range(len(initial['history']) - 1, len(final['history'])))
    s['terminal_transitions'] = []
    for i in indices:
        h = final['history'][i]
        a, o = h['action'], h['outcome']
        assert a['tool'] in ('Finish', 'Write')
        s['terminal_transitions'].append({'pointer': final_source['pointer'] + '#/history/' + str(i),
            'tool': a['tool'], 'path': a.get('path', ''), 'status': a.get('status', ''),
            'candidate': h['candidate'], 'outcome_status': o.get('status'),
            'error': o.get('error'), 'detail': o.get('detail') if a['tool'] == 'Finish' else None,
            'written': o.get('written') if a['tool'] == 'Write' else None})
    delta = {}
    for model in sorted(set(initial['requests']) | set(final['requests'])):
        req = final['requests'].get(model, {}).get('count', 0) - initial['requests'].get(model, {}).get('count', 0)
        usage = {k: final['usage'].get(model, {}).get(k, 0) - initial['usage'].get(model, {}).get(k, 0)
                 for k in ('in', 'out', 'cache_read', 'cache_write')}
        assert req >= 0 and all(v >= 0 for v in usage.values())
        delta[model] = {'requests': req, 'tokens': usage}
    s['later_continuation'] = {'history_extension_actions': len(final['history']) - len(initial['history']),
        'delta': delta, 'attribution': 'Prefix-equal first/final histories and cumulative request/usage subtraction; only three report-recreation operations extend each affected session. Control has no later continuation.'}
    report_path = '.session/exports/reports/' + issue + '.json'
    report = load(report_path)
    fields = dict(re.findall(r'^([a-z_]+): ([^\n]+)$', report['body'].split('```')[1], re.M))
    s['report'] = {'pointer': report_path, 'source': report['source'], 'snapshot': report['snapshot'],
                   'kicks': int(fields.get('kicks', 0)), 'kicked': fields.get('kicked'),
                   'listed_artifacts': sum(line.startswith('- artifact: ') for line in report['body'].splitlines())}
    evidence.append(report_path + '#/body')
    record_path = '.session/exports/records/' + iteration + '.json'
    record = load(record_path)
    ix, recorded = next((i, x) for i, x in enumerate(record['outcome']['sessions']) if str(x['issue']) == issue)
    s['record'] = {'pointer': record_path + '#/outcome/sessions/' + str(ix), 'iteration': int(iteration),
                   'iteration_ended': record['ended'],
                   **{k: recorded[k] for k in ('status', 'artifacts', 'agent_s', 'gate_s', 'total_s', 'parked_s', 'turns', 'tokens')}}
    evidence.append(s['record']['pointer'])
    for entry in manifest['results']:
        if entry['source'] != 'actions' or str(entry.get('issue')) != issue:
            continue
        path = '.session/' + entry['path']
        run = load(path)
        r = {k: run[k] for k in ('id', 'run_attempt', 'status', 'conclusion', 'created_at', 'run_started_at', 'updated_at', 'html_url')}
        r['pointer'] = path
        r['jobs'] = []
        for ji, job in enumerate(run['jobs']):
            if job['name'] not in ('prep', 'stage', 'session', 'epilogue'):
                continue
            j = {k: job[k] for k in ('id', 'name', 'status', 'conclusion', 'started_at', 'completed_at')}
            j['pointer'] = path + '#/jobs/' + str(ji)
            j['steps'] = []
            if job['name'] in ('session', 'epilogue'):
                selected = ('Routed session', 'Pack the results', 'Epilogue', 'Run actions/upload-artifact@v4', 'Run actions/download-artifact@v4')
                for si, step in enumerate(job['steps']):
                    if step['name'] not in selected:
                        continue
                    item = {k: step[k] for k in ('name', 'status', 'conclusion', 'started_at', 'completed_at')}
                    item['pointer'] = j['pointer'] + '/steps/' + str(si)
                    j['steps'].append(item)
                    s['durations'].append(duration(str(run['id']) + ' ' + job['name'] + ' step ' + str(si) + ' ' + step['name'], step['started_at'], step['completed_at']))
            s['durations'].append(duration(str(run['id']) + ' job ' + job['name'], job['started_at'], job['completed_at']))
            r['jobs'].append(j)
        s['durations'].append(duration(str(run['id']) + ' workflow_start_to_updated_at', run['run_started_at'], run['updated_at']))
        s['runs'].append(r)
        evidence.append(path + '#/jobs')
    s['runs'].sort(key=lambda r: r['created_at'])
    if issue != '669':
        failed = s['runs'][0]
        assert failed['conclusion'] == 'failure'
        ej = next(j for j in failed['jobs'] if j['name'] == 'epilogue')
        assert ej['conclusion'] == 'failure'
        s['observed_failure_stage'] = 'Initial Epilogue step failed after successful session packing/upload and both epilogue downloads; output-loss cause undetermined.'
        s['durations'].append(duration('initial_workflow_updated_at_to_reported_kick_not_agent_active', failed['updated_at'], fields['kicked']))
        s['durations'].append(duration('reported_kick_to_recovery_run_created', fields['kicked'], s['runs'][1]['created_at']))
    else:
        s['observed_failure_stage'] = 'None observed: one successful workflow, one final checkpoint, no kick, 12 recorded/listed published artifacts; exact publication instant unavailable.'
        assert recorded['artifacts'] == s['report']['listed_artifacts'] == 12
    doc['sessions'][issue] = s
out = pathlib.Path('audit/session-recovery-0147.json')
out.write_text(json.dumps(doc, indent=2) + '\n')
assert out.stat().st_size < 2_000_000
for issue, s in doc['sessions'].items():
    print(issue, 'runs', [(r['id'], r['conclusion']) for r in s['runs']], 'continuation', s['later_continuation']['delta'], 'artifacts', s['record']['artifacts'])
print('Normalized measurements written:', out, out.stat().st_size, 'bytes')
