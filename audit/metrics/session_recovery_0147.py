"""Summarize staged recovery metadata; never execute historical workloads.
Run from repository root: python3 -I audit/metrics/session_recovery_0147.py
Runtime blobs are hashed in memory; only allowlisted fields leave the process.
"""
import datetime as dt
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path('.')
EXPORT = ROOT / '.session/exports'
PIN = '510fc5af213cbe9f66dde42a27e3467bc225afcd'
SPECS = {
    '643': ('0138', '2026-11-14T23:34:33Z', '2026-11-15T00:33:13Z'),
    '653': ('0141', '2026-11-15T01:42:29Z', '2026-11-15T07:02:51Z'),
    '663': ('0144', '2026-11-15T08:39:14Z', '2026-11-15T14:35:51Z'),
    '669': ('0146', None, None),
}
POLICY = 'policy/observations/0147-policy-check.md'

def read(path):
    return json.loads(pathlib.Path(path).read_text())

def stamp(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00'))

def duration(name, start, end, evidence):
    seconds = (stamp(end) - stamp(start)).total_seconds()
    assert seconds >= 0, (name, start, end)
    return dict(name=name, start=start, end=end, seconds=seconds, evidence=evidence)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

manifest = read(EXPORT / 'manifest.json')
paths = [str(EXPORT / 'manifest.json'), '.session/startup.json', '.session/issue.md', '.session/role/SKILL.md', POLICY,
         'docs/perpetua/operating-parameters.md', 'docs/perpetua/engine.md', '.github/workflows/session.yml', '.github/loop/loop.py']
paths += [str(ROOT / '.session' / x['path']) for x in manifest['results'] if x.get('path')]
sources = {p: dict(availability='available', bytes=len(pathlib.Path(p).read_bytes()), sha256=sha(pathlib.Path(p).read_bytes())) for p in paths}
checkout = subprocess.run(['git', 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
doc = dict(schema_version=1,
    method='Reuse policy-check 0147 checkpoint measurements; join staged Actions run/job/step metadata to report headers and iteration outcome.sessions by issue. Preserve exact JSON pointers and SHA256 bytes. Timestamp differences are wall intervals only, not agent-active time. Read only allowlisted runtime fields at a fixed git pin; no historical command, probe, evaluator, transport or native replay. cause_status describes root cause, not whether the failed step is located.',
    checkout=checkout, runtime_pin=PIN, sources=sources,
    availability=manifest['results'],
    source_interpretation='Manifest report/record snapshot identifiers and actual staged-file SHA256 values are retained separately; they need not match because the staged JSON is a wrapper. Stream absence has multiple possible causes. Source-code hashes describe the audit checkout, not a proven checkout of every historical run.',
    source_sections=['docs/perpetua/engine.md:301-307', '.github/workflows/session.yml:247-307', '.github/loop/loop.py:903-947', '.github/loop/loop.py:1449-1465'],
    sessions={})
rows = []
for number, (iteration, first, later) in SPECS.items():
    evidence = [POLICY + '#recovery-discovery-and-audit-evidence']
    missing = ['All selected stream exports unavailable; absence does not distinguish retention, expiry or upload failure.',
               'Original result bundle contents, pack inventory, tree admission diagnostics and epilogue exception logs are not staged.',
               'Exact publication time and per-transition artifact inventory are unavailable.',
               'Continuation-only tokens are unmeasured: available usage is cumulative and no checkpoint usage delta is reused here. Tokens do not measure subscription quota or money.']
    if first:
        missing += ['Exact report/artifact disappearance time and causal link between epilogue failure and missing recovery files are undetermined.',
                    'Watchdog decisions and other concurrent commitments are not staged; recovery delay cause is undetermined.']
    record_path = f'.session/exports/records/{iteration}.json'
    record = read(record_path)
    idx, saved = next((i, s) for i, s in enumerate(record['outcome']['sessions']) if str(s['issue']) == number)
    record_pointer = record_path + f'#/outcome/sessions/{idx}'
    evidence.append(record_pointer)
    report_path = f'.session/exports/reports/{number}.json'
    report = read(report_path)
    header = report['body'].split('```yaml\n', 1)[1].split('```', 1)[0]
    header_fields = dict(line.split(': ', 1) for line in header.splitlines() if ': ' in line)
    evidence += [report_path + '#/body', report['source']]
    assert int(header_fields.get('artifacts', '0')) == saved['artifacts']
    runs = []
    durations = []
    for item in manifest['results']:
        if item['source'] != 'actions' or str(item.get('issue')) != number or item['status'] != 'downloaded':
            continue
        path = '.session/' + item['path']
        raw = read(path)
        pointer = path + '#'
        evidence.append(pointer)
        run = {k: raw[k] for k in ('id', 'name', 'status', 'conclusion', 'created_at', 'run_started_at', 'updated_at', 'run_attempt', 'html_url')}
        run['source'] = pointer
        run['jobs'] = []
        durations.append(duration(f"run {raw['id']} created-to-updated (metadata interval)", raw['created_at'], raw['updated_at'], pointer))
        for ji, job in enumerate(raw['jobs']):
            jp = path + f'#/jobs/{ji}'
            entry = {k: job[k] for k in ('id', 'name', 'status', 'conclusion', 'started_at', 'completed_at', 'html_url')}
            entry['source'] = jp
            entry['steps'] = []
            if job['name'] in ('session', 'epilogue'):
                for si, step in enumerate(job['steps']):
                    if step['name'] not in ('Routed session', 'Session', 'Pack the results', 'Epilogue', 'Run actions/upload-artifact@v4', 'Run actions/download-artifact@v4'):
                        continue
                    sp = jp + f'/steps/{si}'
                    entry['steps'].append(dict(step, source=sp))
                    durations.append(duration(f"run {raw['id']} job {job['id']} step {si}: {step['name']}", step['started_at'], step['completed_at'], sp))
            run['jobs'].append(entry)
        runs.append(run)
    runs.sort(key=lambda r: r['created_at'])
    runtime_source = f'git:{PIN}:sessions/{number}.json'
    blob = subprocess.run(['git', 'show', f'{PIN}:sessions/{number}.json'], check=True, capture_output=True).stdout
    runtime = json.loads(blob)
    sources[runtime_source] = dict(availability='available', bytes=len(blob), sha256=sha(blob))
    actions = []
    for hi, h in enumerate(runtime['history']):
        action = h.get('action', {})
        if action.get('tool') == 'Finish' or (hi >= len(runtime['history']) - 3 and action.get('tool') == 'Write'):
            projected = {k: action[k] for k in ('tool', 'path', 'status') if k in action}
            projected['source'] = runtime_source + f'#/history/{hi}'
            outcome = h.get('outcome', {})
            projected['outcome_status'] = outcome.get('status')
            projected['rejected_missing_report'] = 'Use Write to create .session/report.md before Finish' in outcome.get('detail', '')
            actions.append(projected)
    evidence.append(runtime_source + '#/history')
    timeline = []
    if first:
        assert len(runs) == 2 and runs[0]['conclusion'] == 'failure' and runs[1]['conclusion'] == 'success'
        for r in runs:
            sj = next(j for j in r['jobs'] if j['name'] == 'session')
            assert sj['conclusion'] == 'success'
            assert all(s['conclusion'] == 'success' for s in sj['steps'] if s['name'] in ('Pack the results', 'Run actions/upload-artifact@v4'))
        first_epi = next(j for j in runs[0]['jobs'] if j['name'] == 'epilogue')
        failed = next(s for s in first_epi['steps'] if s['name'] == 'Epilogue')
        assert failed['conclusion'] == 'failure'
        assert stamp(failed['started_at']) <= stamp(first) <= stamp(failed['completed_at'])
        kick = header_fields['kicked']
        timeline += [dict(event='First checkpoint already contains accepted Finish and final result; timestamp reused from policy measurement (not tool execution time)', at=first, source=evidence[0]),
                     dict(event='Original workflow fails in Epilogue after successful results upload and both downloads', at=failed['completed_at'], source=failed['source']),
                     dict(event='Report records one kick', at=kick, source=report_path + '#/body'),
                     dict(event='Later checkpoint contains report recreation and accepted Finish', at=later, source=evidence[0])]
        durations += [duration('first-to-later checkpoint gap; not agent-active time', first, later, evidence[0]),
                      duration('original run updated to recorded kick; not proven watchdog wait', runs[0]['updated_at'], kick, [runs[0]['source'], report_path + '#/body'])]
        location = 'Supported failed step: original Epilogue; exception/root cause and artifact-loss mechanism undetermined.'
        gap = int((stamp(later) - stamp(first)).total_seconds())
    else:
        assert len(runs) == 1 and runs[0]['conclusion'] == 'success' and saved['artifacts'] == 12
        timeline.append(dict(event='Single final checkpoint and accepted Finish; exact checkpoint timestamp not reused', at=None, source=evidence[0]))
        location = 'Successful publication control; no failed step or failure cause observed.'
        gap = None
    timeline.append(dict(event='Published report and final artifact count confirmed by staged report/record; exact publication time unavailable', at=None, source=[record_pointer, report_path + '#/body']))
    runtime_projection = dict(source=runtime_source, outputs_asset=runtime['outputs_asset'], final_status=runtime['result']['status'], history_actions=actions,
                              usage_scope='Cumulative session usage only; no continuation attribution.')
    assert runtime_projection['outputs_asset'] is None
    doc['sessions'][number] = dict(cause_status='undetermined', failure_location=location, evidence=evidence, missing=missing, durations=durations,
        runs=runs, timeline=timeline, runtime=runtime_projection,
        checkpoint_timestamp_interpretation='Policy-saved checkpoint/commit timestamps, not exact Finish action timestamps; full first checkpoint records not reread.',
        saved_metrics={k: saved[k] for k in ('agent_s', 'gate_s', 'total_s', 'parked_s', 'artifacts', 'turns', 'tokens', 'models', 'status', 'commit')},
        metrics_interpretation='Reuse recorded values without summing checkpoint gaps or treating short final-run measurements as lifetime agent time.',
        report=dict(source=report['source'], snapshot=report['snapshot'], kicks=int(header_fields.get('kicks', '0')), kicked=header_fields.get('kicked'),
                    artifact_entries=[line for line in report['body'].splitlines() if line.startswith('- artifact:')]))
    rows.append(f"| #{number} | {', '.join(str(r['id']) + ' ' + r['conclusion'] for r in runs)} | {gap if gap is not None else 'single checkpoint'} | {saved['artifacts']} | {saved['agent_s']}/{saved['gate_s']}/{saved['total_s']}/{saved['parked_s']} |")
doc['next_action'] = dict(action='Policymaker should request only the existing failed Epilogue step log/exception for job 132628109954 (run 43652564966) first, if retained; compare its terminal boundary with the pinned receive_status/receive_tree/receive_commits/publish_runtime_state/finalize sequence. Do not replay the session.',
    expected_gain='Identify one exception and last completed publication boundary before deciding whether an engine-change request is supported.',
    verification='Pin returned log bytes by SHA256 and run/job/step identity; confirm exception location and whether report/artifact inventory was received. If unavailable, close historical root-cause attribution at Epilogue; a future narrowly scoped diagnostic proposal must capture inventory and terminal boundary, not reconstruct old artifacts.')
(ROOT / 'audit').mkdir(exist_ok=True)
(ROOT / 'audit/session-recovery-0147.json').write_text(json.dumps(doc, indent=2) + '\n')
text = '''# Recovery and publication audit 0147

3/3 original workflows failed in **Epilogue**, after successful routed-session, result packing, results upload and both epilogue downloads; 3/3 recovery workflows succeeded. #669 passed the same chain and published 12 artifacts.

| Session | Run identity / workflow outcome (attempt 1 each) | Checkpoint gap s | Published artifacts | Saved agent/gate/total/parked s |
| --- | --- | ---: | ---: | --- |
''' + '\n'.join(rows) + '''

Checkpoint gaps reuse [policy measurements](../policy/observations/0147-policy-check.md#recovery-discovery-and-audit-evidence), not agent-active time. Their first checkpoint timestamps fall inside the failed Epilogue steps; they are not exact Finish execution times. Short saved runtimes are preserved as recorded, not lifetime work measurements.
The [detailed timelines, exact run/job/step pointers, source SHA256 values and runtime projections](session-recovery-0147.json) retain all seven runs. Runtime pin: `510fc5af213cbe9f66dde42a27e3467bc225afcd`; source-code inspection describes the audit checkout, without asserting every historical run used those bytes.
Each affected session already had an accepted Finish, then later received “Use Write to create .session/report.md before Finish”, wrote the report and finished again. Reports record one kick each at 00:30:08, 06:59:29 and 14:32:53 UTC on November 15. Recovery published reports but zero artifacts; #663's saved 21-artifact command result is not recovered bytes.
**Root causes remain undetermined.** Metadata locates failure at the Epilogue step, not a Python function or the point files disappeared. Successful upload/download steps establish workflow outcomes, not complete bundle contents or successful admission. Missing logs/bundles prevent distinguishing admission, finalization and other exceptions.
All four streams are unavailable (retention, expiry and never-uploaded remain alternatives). `outputs_asset=null` occurs in all four runtime records, including #669; neither null nor zero artifacts alone diagnoses failure. Watchdog commitments are a possible delay mechanism, without historical decision evidence.
Continuation-only tokens are **unmeasured**; saved usage is cumulative. Tokens measure neither subscription quota nor money. No evaluator, historical command, benchmark probe, model/reader/native execution or artifact reconstruction was run.
**Smallest next action:** Policymaker should obtain only failed job `132628109954`'s Epilogue exception/log, if retained. Expected gain: locate one exception before considering an engine change. Verify its run/job identity, byte hash and last completed receive/finalize boundary; if unavailable, close historical attribution at the step-level limit and capture that boundary plus inventory on a future occurrence.
Benchmark_ready=false; missing benchmark coverage, whole-method review and owner acceptance remain unchanged. Product quality is unmeasured. This audit measures recovery only.
'''
(ROOT / 'audit/0147.md').write_text(text)
(ROOT / 'audit/latest.md').write_text(text)
print(json.dumps(dict(sessions=list(doc['sessions']), sources=len(sources), checkpoint_gaps={n: next((d['seconds'] for d in s['durations'] if d['name'].startswith('first-to-later')), None) for n, s in doc['sessions'].items()}), sort_keys=True))
