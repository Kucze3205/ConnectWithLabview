"""Normalize explicitly staged recovery evidence; never executes historical work.
Run from repository root: python3 -I audit/metrics/session_recovery_0147.py
Runtime checkpoint observations are reused from policy observation 0147, not remeasured.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT = Path('.')
OUT = Path('audit/session-recovery-0147.json')
PIN = '510fc5af213cbe9f66dde42a27e3467bc225afcd'
CHECKOUT = 'e066c82bb70fa289e3ba55a2b2d65af4cd5dbc40'
manifest_path = '.session/exports/manifest.json'
manifest = json.loads(Path(manifest_path).read_text())
hashes = {}

def load(path):
    b = Path(path).read_bytes()
    hashes[path] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    return json.loads(b)

for path in [manifest_path, '.session/issue.md', '.session/role/SKILL.md', '.session/startup.json',
             'policy/observations/0147-policy-check.md', 'docs/perpetua/operating-parameters.md',
             '.github/workflows/session.yml', '.github/loop/loop.py', 'docs/perpetua/engine.md']:
    b = Path(path).read_bytes()
    hashes[path] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

checkpoints = {
    '643': ('2026-11-14T23:34:33Z', '2026-11-15T00:33:13Z', 53),
    '653': ('2026-11-15T01:42:29Z', '2026-11-15T07:02:51Z', 54),
    '663': ('2026-11-15T08:39:14Z', '2026-11-15T14:35:51Z', 55),
}
iterations = {'643': 138, '653': 141, '663': 144, '669': 146}
sessions = {}

def duration(name, start, end, source):
    seconds = (dt.datetime.fromisoformat(end.replace('Z', '+00:00')) -
               dt.datetime.fromisoformat(start.replace('Z', '+00:00'))).total_seconds()
    assert seconds >= 0
    return {'name': name, 'start': start, 'end': end, 'seconds': seconds, 'evidence': source}

for sid, iteration in iterations.items():
    selected = [x for x in manifest['results'] if x.get('issue') == int(sid) or
                (x['source'] == 'records' and x.get('iteration') == iteration)]
    s = {
        'cause_status': 'undetermined',
        'cause_scope': 'Underlying epilogue error and mechanism/timing of missing output; successful control has no observed failure.',
        'availability': selected,
        'evidence': [manifest_path + '#/results', 'policy/observations/0147-policy-check.md:49-59'],
        'missing': [
            'Diagnostic stream unavailable; catalogue absence does not distinguish pruning, expiry or non-upload.',
            'No staged Actions step logs, failure annotations, traceback or results package bytes/inventory.',
            'No independently timestamped final release-asset publication event.',
            'Actions exports supply updated_at, not completed_at for workflows; exact workflow completion time unavailable.',
            'Historical workflow/code revision not supplied by Actions exports; checkout code is explanatory only.',
            'Continuation-only model request count and tokens unmeasured; staged records aggregate session usage.'
        ],
        'durations': [], 'runs': [],
        'runtime': {'pin': PIN, 'record': 'sessions/' + sid + '.json',
                    'measurement_source': 'policy/observations/0147-policy-check.md:49-59',
                    'outputs_asset': None, 'outputs_asset_diagnostic': False},
        'extra_continuation_usage': {'requests': None, 'tokens': None,
                                    'status': 'unmeasured; no request-level or checkpoint usage delta measured'},
    }
    if sid in checkpoints:
        first, later, line = checkpoints[sid]
        pointer = 'policy/observations/0147-policy-check.md:' + str(line)
        s['runtime'].update(first_final_checkpoint=first, later_final_checkpoint=later,
                            first_finish_accepted=True,
                            recovery_history=['Finish rejected: Use Write to create .session/report.md before Finish',
                                              'Write report', 'Finish accepted'],
                            finish_status='partial' if sid == '643' else 'done')
        s['durations'].append(duration('runtime checkpoint gap (not agent-active time)', first, later, pointer))
        s['missing'].append('Exact report/artifact disappearance time and original packaged content; no artifacts reconstructed.')
        s['evidence'].append(pointer)
    else:
        s['runtime'].update(final_checkpoint_count=1, first_final_checkpoint=None,
                            note='One final checkpoint and no kick, per reused observation; exact timestamp not reported there.')
        s['missing'].append('Exact final runtime checkpoint timestamp not in reused observation; no historical reread required.')
    for entry in selected:
        if entry['status'] != 'downloaded':
            continue
        path = '.session/' + entry['path']
        d = load(path)
        if entry['source'] == 'actions':
            r = {k: d.get(k) for k in ['id', 'run_attempt', 'status', 'conclusion', 'created_at', 'run_started_at', 'updated_at', 'html_url']}
            r['phase'] = 'control' if sid == '669' else ('recovery' if d['created_at'] > s['runtime']['first_final_checkpoint'] else 'initial')
            r['evidence'] = path
            r['jobs'] = []
            for ji, job in enumerate(d['jobs']):
                if job['name'] not in ['session', 'epilogue']:
                    continue
                jp = path + '#/jobs/' + str(ji)
                normalized = {k: job.get(k) for k in ['id', 'name', 'status', 'conclusion', 'started_at', 'completed_at']}
                normalized['evidence'] = jp
                normalized['steps'] = []
                pack_index = next((i for i, step in enumerate(job.get('steps', [])) if step['name'] == 'Pack the results'), None)
                for si, step in enumerate(job.get('steps', [])):
                    name = step['name']
                    if name not in ['Routed session', 'Pack the results', 'Epilogue', 'Run actions/upload-artifact@v4', 'Run actions/download-artifact@v4']:
                        continue
                    sp = jp + '/steps/' + str(si)
                    n = {k: step.get(k) for k in ['name', 'status', 'conclusion', 'started_at', 'completed_at']}
                    n.update(index=si, evidence=sp)
                    if name == 'Run actions/upload-artifact@v4':
                        n['channel_from_checkout_workflow'] = 'results' if pack_index is not None and si > pack_index else 'diagnostic stream'
                    if name == 'Run actions/download-artifact@v4':
                        n['channel_from_checkout_workflow'] = ('results' if not normalized['steps'] else 'baseline') if job['name'] == 'epilogue' else 'staged session input'
                    normalized['steps'].append(n)
                    s['durations'].append(duration(str(d['id']) + ' / ' + job['name'] + ' / step[' + str(si) + '] ' + name,
                                                    step['started_at'], step['completed_at'], sp))
                r['jobs'].append(normalized)
                s['evidence'].append(jp)
            s['runs'].append(r)
        elif entry['source'] == 'reports':
            kicked = next((line.split(': ', 1)[1] for line in d['body'].splitlines() if line.startswith('kicked: ')), None)
            s['report'] = {'source': d['source'], 'comment': d['comment'], 'snapshot': d['snapshot'],
                           'evidence': path + '#/body', 'kick': kicked,
                           'kick_count': 0 if kicked is None else 1,
                           'note': 'No kick field in control report; no-kick finding also comes from policy observation.'}
            s['evidence'].append(path + '#/body')
        elif entry['source'] == 'records':
            i, record = next((i, v) for i, v in enumerate(d['outcome']['sessions']) if v['issue'] == int(sid))
            s['record'] = {k: record[k] for k in ['status', 'artifacts', 'agent_s', 'gate_s', 'total_s', 'parked_s', 'turns']}
            s['record'].update(iteration=iteration, iteration_ended=d['ended'], engine_version=d['engine_version'],
                               evidence=path + '#/outcome/sessions/' + str(i),
                               timing_note='Existing record values reused; not lifetime elapsed time or continuation usage attribution.')
            s['publication'] = {'observed_artifacts': record['artifacts'], 'timestamp': None,
                                'evidence': s['record']['evidence'],
                                'status': '12 final artifacts recorded' if sid == '669' else 'zero final artifacts recorded'}
            s['evidence'].append(s['record']['evidence'])
    s['runs'].sort(key=lambda r: r['created_at'])
    if sid != '669':
        initial = s['runs'][0]
        failed = next(j for j in initial['jobs'] if j['name'] == 'epilogue')
        step = next(t for t in failed['steps'] if t['name'] == 'Epilogue')
        s['observed_failure'] = {'status': 'supported', 'stage': 'Epilogue command step after successful results packaging/upload and both epilogue downloads',
                                 'run': initial['id'], 'job': failed['id'], 'start': step['started_at'],
                                 'end': step['completed_at'], 'evidence': step['evidence'],
                                 'limit': 'Step spans pip install, git-identity and epilogue command; failing subcommand/exception unavailable.'}
        kick = s['report']['kick']
        s['durations'].append(duration('initial failed Epilogue step end to reported kick (elapsed only)', step['completed_at'], kick, step['evidence'] + '; ' + s['report']['evidence']))
        recovery = s['runs'][1]
        s['durations'].append(duration('reported kick to recovery run creation', kick, recovery['created_at'], s['report']['evidence'] + '; ' + recovery['evidence'] + '#/created_at'))
    else:
        s['observed_failure'] = {'status': 'none observed', 'stage': None}
    sessions[sid] = s

result = {
    'schema_version': 1,
    'method': {
        'selection': 'Manifest first; all seven downloaded Actions runs retained separately (attempt 1 each), four report snapshots and four requested records; all four streams unavailable.',
        'runtime': 'Reuse observation 0147 checkpoints, accepted Finish/recovery sequence and outputs_asset findings at runtime pin ' + PIN + '; no broad history survey or runtime record reread.',
        'pointers': 'JSON pointers use zero-based array indices. Source hashes cover actual staged wrapper bytes; report.snapshot separately identifies the report snapshot, not its wrapper hash.',
        'timing': 'UTC timestamp pairs only; step boundaries are Actions observations, runtime checkpoints are persistence observations. Gaps are elapsed intervals, never agent-active time. Publication counts are final observations with no exact event timestamp.',
        'cause': 'Supported localization is the initial Epilogue command step; cause_status remains undetermined for the underlying error and output loss. Successful transport steps do not prove package completeness or later admission.',
        'code_checkout': CHECKOUT,
        'code_sections': ['.github/workflows/session.yml:247-307', '.github/loop/loop.py:903-947', '.github/loop/loop.py:1469-1490', 'docs/perpetua/engine.md:301-307'],
        'code_limit': 'Checkout code explains ordering and channel mapping; exports omit historical workflow revision, step logs and package contents. Do not assign an exception to a particular epilogue function.',
        'usage': 'Request/token continuation deltas unmeasured; aggregate models/turns are not attributable incremental recovery usage. No subscription-quota or monetary inference.',
        'scope': 'Environment audit only. No historical commands, probes, evaluator or native execution replayed; no artifact reconstruction. Benchmark readiness and product quality unmeasured.'
    },
    'source_hashes': hashes,
    'sessions': sessions,
    'next_action': {
        'owner': 'Policymaker',
        'action': 'Seek only existing failure annotations or short redacted traceback from the three initial Epilogue command steps, keyed by the recorded run/job IDs. Close this audit without waiting for unavailable logs.',
        'expected_gain': 'Distinguish dependency/setup, baseline/tree/commit admission, runtime publication and finalization failure before proposing a repair.',
        'check': 'Each error must identify its exact run/job and failing subcommand/phase; successful transport alone is insufficient.',
        'fallback': 'If logs are expired, propose narrowly scoped engine diagnostics: retain a safe failing-phase marker and results inventory hashes across epilogue failure; verify through engine-owned failure-path checks. Do not rerun historical model work or request broad private access.'
    }
}
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(result, indent=2) + '\n')
assert OUT.stat().st_size < 2_000_000
print('Wrote', str(OUT), OUT.stat().st_size, 'bytes;', len(hashes), 'hashed inputs;', sum(len(s['runs']) for s in sessions.values()), 'distinct runs')
