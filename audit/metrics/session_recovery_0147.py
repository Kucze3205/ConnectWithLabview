"""Offline, read-only measurement of the explicitly selected recovery evidence.
Run: python3 -I audit/metrics/session_recovery_0147.py
Requires this session's staged exports and the named runtime git objects.
Writes only audit reports; never executes historical commands or imports engine code.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

PIN = '510fc5af213cbe9f66dde42a27e3467bc225afcd'
SOURCE = 'fe3bedc18e276a6cc718dbd4f50dc4a4f0e2523a'
CONFIG = {
    '643': (138, '898877dd115aa8267a010119d1f09ef481d83f31', '3b16ea14e0cc9a66af9e916a15470f289b356119', [43652564966, 43658484769]),
    '653': (141, '9f8a23ad1b1b4a4d90fe9aa8739558b766606bc5', 'd9511a814bf67e4e075e02ffa5c2fe608d838f00', [43663290752, 43687899425]),
    '663': (144, '13817283b1c0e4670fb8e5da236c27521b8be969', '9ba5a679ca67a783661f43245f13480bccde3baa', [43694128074, 43724956130]),
    '669': (146, PIN, PIN, [43728358074]),
}
SOURCES = {}

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def load(path):
    raw = Path(path).read_bytes()
    SOURCES[path] = {'sha256': digest(raw), 'bytes': len(raw), 'availability': 'present'}
    return json.loads(raw)

def git(*args):
    return subprocess.check_output(['git', *args])

def runtime(ref, n):
    locator = ref + ':sessions/' + n + '.json'
    raw = git('show', locator)
    SOURCES[locator] = {'sha256': digest(raw), 'bytes': len(raw), 'availability': 'present git object', 'disclosure': 'hash and selected non-sensitive fields only'}
    return json.loads(raw)

def timestamp(ref):
    return git('show', '-s', '--format=%cI', ref).decode().strip().replace('+00:00', 'Z')

def seconds(start, end):
    return int((dt.datetime.fromisoformat(end.replace('Z', '+00:00')) - dt.datetime.fromisoformat(start.replace('Z', '+00:00'))).total_seconds())

manifest = load('.session/exports/manifest.json')
assert len(manifest['results']) == 19
for path in ['.session/issue.md', '.session/role/SKILL.md', '.session/startup.json', '.session/history/manifest.json', 'policy/observations/0147-policy-check.md', 'docs/perpetua/operating-parameters.md', 'docs/perpetua/accepted-limits.md', 'docs/perpetua/engine.md', '.github/workflows/session.yml', '.github/loop/loop.py', 'audit/metrics/session_recovery_0147.py']:
    raw = Path(path).read_bytes()
    SOURCES[path] = {'sha256': digest(raw), 'bytes': len(raw), 'availability': 'present'}

result = {
    'schema_version': 1,
    'method': 'Reuse saved record timings; join explicit Actions exports by run/job identity to pinned runtime checkpoints and trusted report snapshots. All JSON pointers are zero-based. Hash exact input bytes; hash report bodies separately. Subtract cumulative per-model usage only after verifying an unchanged history prefix and the exact three-action continuation. Derive elapsed durations only from stored timestamp pairs. Commit timestamps date publication of checkpoints, not the Finish operation. No historical commands, probes, evaluators, model trials or native execution are replayed.',
    'source_checkout': SOURCE,
    'runtime_pin': PIN,
    'availability': manifest['results'],
    'sources': SOURCES,
    'sessions': {},
    'limits': [
        'All four diagnostic streams are unavailable; the catalogue cannot distinguish pruning, expiration or never-uploaded streams. A successful upload step with if-no-files-found=ignore does not prove a nonempty payload.',
        'Actions exports contain metadata, not step logs, exceptions, result archive bytes or publication inventories. Success does not prove archive content or complete admission.',
        'Current source explains possible boundaries; the exact source revision executed by each historical job is not staged. It cannot establish a historical exception.',
        'Runtime outputs_asset is null in all four cases, including the successful control; it cannot diagnose loss.',
        'Checkpoint gaps are elapsed time, not agent-active time or exact file-loss times. No watchdog invocation/decision history is staged.',
        'Usage deltas are provider-reported token counters, not normalized subscription quota or monetary cost; cache counters are kept separate from in/out.',
        'This recovery audit establishes no benchmark readiness or product quality. Real admissions, native/model/reader trials, semantic coverage and controlled comparisons remain unmeasured here; independent whole-method review, owner acceptance and other policy-listed readiness prerequisites remain missing.'
    ],
    'next_action': {
        'owner': 'Policymaker through trusted export/preparation',
        'action': 'Request only retained, redacted stderr/exception and phase diagnostics for Epilogue step jobs 132628109954, 132660262717 and 132754986114 in runs 43652564966, 43663290752 and 43694128074; do not rerun those jobs or hold this iteration open. If those logs are unavailable, close the historical root-cause question at the Epilogue-step boundary. Any future diagnostic engine-change proposal should be limited to non-sensitive phase outcomes and file counts/digests across pack, receive and final publication.',
        'expected_gain': 'Distinguish an archive/admission/finalization exception from other Epilogue step failures, or establish that historical root-cause attribution cannot be recovered.',
        'verification': 'Pin and hash any retained excerpt; match run, job, attempt and failing command timestamp. Attribute only the exception and phase actually shown. A future diagnostic change must demonstrate phase linkage and final inventory in an isolated synthetic success and interrupted-publication test before deployment; no benchmark rerun is needed.'
    }
}
rows = []
usage_rows = []
for n, (iteration, first_ref, last_ref, runs) in CONFIG.items():
    first = runtime(first_ref, n)
    last = runtime(PIN, n)
    assert runtime(last_ref, n) == last
    assert first['history'] == last['history'][:len(first['history'])]
    prefix = first_ref + ':sessions/' + n + '.json'
    final_prefix = PIN + ':sessions/' + n + '.json'
    assert first['result']['status'] in ['done', 'partial']
    finish_index = len(first['history']) - 1
    assert first['history'][finish_index]['action']['tool'] == 'Finish'
    assert first['history'][finish_index]['outcome']['status'] == first['result']['status']
    record_path = '.session/exports/records/' + str(iteration).zfill(4) + '.json'
    record = load(record_path)
    si, saved = next((i, s) for i, s in enumerate(record['outcome']['sessions']) if str(s['issue']) == n)
    report_path = '.session/exports/reports/' + n + '.json'
    report = load(report_path)
    assert digest(report['body'].encode()) == report['snapshot']
    SOURCES[report_path]['report_body_sha256'] = report['snapshot']
    fields = {}
    for line in report['body'].split('```')[1].splitlines():
        if ': ' in line:
            key, value = line.split(': ', 1)
            fields[key] = value
    session = {
        'cause_status': 'undetermined',
        'finding': 'Observed initial failure is localized to the Epilogue step after metadata-successful result transfer; file-loss and recovery-delay causes are undetermined.' if len(runs) == 2 else 'Successful control: no failure cause to attribute; one checkpoint, successful Epilogue and 12 recorded published artifacts.',
        'evidence': [prefix + '#/history/' + str(finish_index), prefix + '#/result/status', final_prefix + '#/history', final_prefix + '#/usage', record_path + '#/outcome/sessions/' + str(si), report_path + '#/body', report['source']],
        'missing': ['Exact Finish operation timestamp (only checkpoint commit time is available)', 'Original result archive contents and admission/publication inventory', 'Historical job stderr/traceback and exact executed source revision', 'Exact final artifact publication timestamp and watchdog decisions'],
        'durations': [],
        'timeline': [],
        'runtime': {'first_checkpoint': first_ref, 'later_checkpoint': last_ref, 'first_saved_at': timestamp(first_ref), 'last_saved_at': timestamp(last_ref), 'first_turns': first['turns'], 'last_turns': last['turns'], 'history_prefix_unchanged': True, 'outputs_asset': last['outputs_asset'], 'first_finish_status': first['result']['status'], 'first_finish_pointer': prefix + '#/history/' + str(finish_index)},
        'saved_record': {k: saved.get(k) for k in ['status', 'verdict', 'merged', 'commit', 'agent_s', 'gate_s', 'total_s', 'parked_s', 'artifacts', 'tokens', 'models', 'report_snapshots']},
        'report': {'source': report['source'], 'body_sha256': report['snapshot'], 'kicks': int(fields.get('kicks', '0')), 'kicked': fields.get('kicked')},
        'runs': [],
    }
    def duration(name, start, end, evidence):
        value = seconds(start, end)
        assert value >= 0
        session['durations'].append({'name': name, 'start': start, 'end': end, 'seconds': value, 'evidence': evidence})
    for ri, run_id in enumerate(runs):
        path = '.session/exports/actions/' + str(run_id) + '.json'
        run = load(path)
        assert run['id'] == run_id and '#' + n in run['name']
        session['evidence'].append(path + '#/jobs')
        session['runs'].append({k: run[k] for k in ['id', 'html_url', 'run_attempt', 'status', 'conclusion', 'created_at', 'run_started_at', 'updated_at']})
        phase = 'initial' if ri == 0 else 'recovery'
        duration(phase + ' workflow created to last update (not agent time)', run['created_at'], run['updated_at'], [path + '#/created_at', path + '#/updated_at'])
        for ji, job in enumerate(run['jobs']):
            jp = path + '#/jobs/' + str(ji)
            session['timeline'].append({'phase': phase, 'kind': 'job', 'name': job['name'], 'run_id': run_id, 'job_id': job['id'], 'conclusion': job['conclusion'], 'start': job.get('started_at'), 'end': job.get('completed_at'), 'source': jp})
            if job['name'] not in ['session', 'epilogue']:
                continue
            for sti, step in enumerate(job['steps']):
                if step['name'] not in ['Routed session', 'Pack the results', 'Epilogue', 'Run actions/upload-artifact@v4', 'Run actions/download-artifact@v4']:
                    continue
                sp = jp + '/steps/' + str(sti)
                session['timeline'].append({'phase': phase, 'kind': 'step', 'name': step['name'], 'run_id': run_id, 'job_id': job['id'], 'conclusion': step['conclusion'], 'start': step.get('started_at'), 'end': step.get('completed_at'), 'source': sp})
                if step.get('started_at') and step.get('completed_at'):
                    duration(phase + ' ' + job['name'] + ' step ' + str(sti) + ': ' + step['name'], step['started_at'], step['completed_at'], [sp + '/started_at', sp + '/completed_at'])
    for label, ref in [('first accepted Finish checkpoint publication', first_ref)] + ([('later accepted Finish checkpoint publication', last_ref)] if len(runs) == 2 else []):
        session['timeline'].append({'kind': 'checkpoint', 'name': label, 'at': timestamp(ref), 'source': ref + ':sessions/' + n + '.json', 'note': 'Commit timestamp is not the operation timestamp.'})
    session['timeline'].append({'kind': 'publication observation', 'name': 'Final record reports published session artifacts', 'artifacts': saved['artifacts'], 'at': None, 'source': record_path + '#/outcome/sessions/' + str(si) + '/artifacts'})
    if len(runs) == 2:
        extension = last['history'][len(first['history']):]
        assert [x['action']['tool'] for x in extension] == ['Finish', 'Write', 'Finish']
        assert extension[0]['outcome']['error'] == 'role tool rejected'
        assert 'Use Write to create .session/report.md before Finish' in extension[0]['outcome']['detail']
        assert extension[1]['action']['path'] == '.session/report.md'
        assert extension[2]['outcome']['status'] == first['result']['status']
        session['runtime']['extension'] = [{'index': len(first['history']) + i, 'tool': x['action']['tool'], 'path': x['action'].get('path', ''), 'status': x['action'].get('status', ''), 'source': final_prefix + '#/history/' + str(len(first['history']) + i)} for i, x in enumerate(extension)]
        session['runtime']['rejection'] = 'Use Write to create .session/report.md before Finish'
        delta = {}
        for model, counters in last['usage'].items():
            delta[model] = {key: value - first['usage'].get(model, {}).get(key, 0) for key, value in counters.items()}
            assert all(value >= 0 for value in delta[model].values())
        session['continuation_usage'] = {'status': 'measured cumulative counter delta over the verified three-action extension', 'by_model': delta, 'evidence': [prefix + '#/usage', final_prefix + '#/usage', final_prefix + '#/history']}
        duration('first to later checkpoint publication gap (not agent-active time)', timestamp(first_ref), timestamp(last_ref), [first_ref, last_ref])
        duration('first checkpoint publication to recorded kick (elapsed only)', timestamp(first_ref), fields['kicked'], [first_ref, report_path + '#/body'])
        session['timeline'].append({'kind': 'kick', 'at': fields['kicked'], 'source': report_path + '#/body'})
        session['missing'].extend(['Time and mechanism by which the report or artifact files became unavailable', 'Original session artifact bytes; do not reconstruct them from continuation text'])
        totals = {k: sum(v.get(k, 0) for v in delta.values()) for k in ['in', 'out', 'cache_read', 'cache_write']}
        usage_rows.append('| #' + n + ' | ' + ' | '.join(str(totals[k]) for k in ['in', 'out', 'cache_read', 'cache_write']) + ' |')
        gap = seconds(timestamp(first_ref), timestamp(last_ref))
    else:
        session['continuation_usage'] = {'status': 'not applicable: no later continuation observed', 'by_model': None}
        gap = None
    rows.append('| #' + n + ' | ' + ', '.join(str(r) for r in runs) + ' | ' + timestamp(first_ref) + ' | ' + (timestamp(last_ref) if len(runs) == 2 else 'none') + ' | ' + (str(gap) if gap is not None else '—') + ' | ' + str(saved['artifacts']) + ' | ' + '/'.join(str(saved.get(k)) for k in ['agent_s', 'gate_s', 'total_s', 'parked_s']) + ' |')
    for item in session['runtime'].get('extension', []):
        session['timeline'].append({'kind': 'recovery action', 'name': item['tool'], 'at': None, 'source': item['source'], 'note': 'Exact operation time unavailable; ordered by history index ' + str(item['index'])})
    session['timeline'].sort(key=lambda event: (event.get('start') or event.get('at') or '9999', event.get('kind', '')))
    result['sessions'][n] = session

# Preserve advertised record snapshots separately from hashes of staged envelope bytes.
for entry in manifest['results']:
    if entry.get('path') and '.session/' + entry['path'] in SOURCES and entry.get('snapshot'):
        SOURCES['.session/' + entry['path']]['manifest_snapshot'] = entry['snapshot']
Path('audit/session-recovery-0147.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
md = '''# Recovery and output publication audit 0147

Three of three affected initial runs failed in the **Epilogue step** after successful routed-session, packing, result-upload and both epilogue-download steps; all three recovery runs and control #669 succeeded. Root cause of missing files remains **undetermined**. Metadata does not expose the failed exception or archive contents.

| Session | Actions runs (initial, recovery) | First accepted Finish checkpoint UTC | Later checkpoint UTC | Gap s | Published artifacts | Saved agent/gate/total/parked s |
| --- | --- | --- | --- | ---: | ---: | --- |
''' + '\n'.join(rows) + '''

Checkpoint times are commit/publication times, not exact Finish times. The 3,520/19,222/21,397-second gaps are elapsed time, never agent-active time. Saved record timings are reused unchanged and largely describe recovery; they do not measure the original invocation or full recovery gap. Full per-run job/step timestamps, zero-based source pointers and paired durations are in [the evidence JSON](session-recovery-0147.json) under `sessions.N.timeline`, `runs` and `durations`.

Each affected first checkpoint already contains an accepted Finish and final result. The later history preserves that complete prefix and adds exactly: Finish rejected with `Use Write to create .session/report.md before Finish`; Write report; accepted Finish. Reports record one kick at 00:30:08 / 06:59:29 / 14:32:53 UTC. Exact file-loss, publication and watchdog transitions are unavailable. #669 has one checkpoint, no kick, successful Epilogue and 12 recorded artifacts. All four `outputs_asset` values are null: null and zero artifacts alone cannot diagnose failure. Workflow transfer artifacts and published session artifacts are different inventories.

| Continuation | Input counter delta | Output counter delta | Cache-read delta | Cache-write delta |
| --- | ---: | ---: | ---: | ---: |
''' + '\n'.join(usage_rows) + '''

These are cumulative runtime-counter differences across the verified three-action extensions, all attributed to `claude/claude-sonnet-5-5`; Codex counters did not increase. They are not subscription-quota or monetary-cost measurements. No continuation is observed for #669. Recovery Routed-session steps lasted 20/17/18 s; control lasted 576 s. Different saved `agent_s` boundaries are retained, not substituted.

Availability: 7 Actions metadata exports, 4 report snapshots and 4 iteration records downloaded; all 4 streams unavailable. Each report-body hash matches its advertised snapshot. Exact byte hashes, record snapshot identifiers and runtime pins are in [sources](session-recovery-0147.json) (`sources`, `availability`, `runtime_pin`). [Measurement script](metrics/session_recovery_0147.py) selects only non-sensitive fields; staged inputs and named git objects are required to rerun it. No historical artifacts were reconstructed and no historical commands, evaluator, probes, reader, model or native executions were replayed.

Current-source boundary: [session.yml](../.github/workflows/session.yml) lines 247–307 separates diagnostic-stream upload, packing/results upload, downloads and the Epilogue step. Stream/results uploads ignore missing files, so metadata-success is not proof of payload contents. [loop.py](../.github/loop/loop.py) lines 903–947 receives results, publishes runtime state, then finalizes; lines 831–840 fetch the candidate and publish session artifacts. The observed checkpoint commits fall inside their respective Epilogue step intervals. This supports a durable continuation despite failed epilogue step, not a specific failing function. Exact historical source revisions and stderr are absent. The staged evidence establishes neither runner death, artifact-quota exhaustion, a receive/admission exception, provider limits nor watchdog deferral. Policy preserves #663's saved command result claiming 21 verified indexed artifacts; their bytes are unavailable, so that count is not a recovered inventory. [Policy measurements](../policy/observations/0147-policy-check.md) and [engine recovery contract](../docs/perpetua/engine.md) lines 301–307 are context, not proof of those explanations.

## What next

Policymaker: seek only retained, redacted Epilogue exception/phase logs for jobs **132628109954 / 132660262717 / 132754986114** in initial runs **43652564966 / 43663290752 / 43694128074**. Expected gain: identify the failed command phase/exception; verify run, job, attempt, timestamps and excerpt hashes before proposing a fix. If absent, close historical root-cause attribution at this precise step boundary; do not keep the iteration open for another general audit. Any future engine proposal should capture non-sensitive phase outcomes and file counts/digests at pack/receive/final-publication boundaries and verify them on isolated synthetic success/interruption cases. No engine change is made here. Resume from this JSON and pinned measurements; do not reconstruct lost artifacts or replay completed benchmark work.

This audit does not establish benchmark readiness or product quality. Missing real coverage, controlled comparisons, independent whole-method review and owner method acceptance remain explicit in policy evidence; product quality is unmeasured here.
'''
Path('audit/0147.md').write_text(md)
Path('audit/latest.md').write_text(md)
print(json.dumps({'sessions': list(result['sessions']), 'sources': len(SOURCES), 'outputs': {p: {'bytes': Path(p).stat().st_size, 'sha256': digest(Path(p).read_bytes())} for p in ['audit/0147.md', 'audit/latest.md', 'audit/session-recovery-0147.json']}}))
