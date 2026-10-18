"""Real cloud fallback/checkpoint exercise without arming or merging the loop."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

from role_runtime import Runtime
from runtime_checkpoint import Checkpoint
from runtime_store import GitHubBackend, Store
from tool_broker import Broker


def main():
    repository = os.environ['GITHUB_REPOSITORY']
    # No live issue can have this synthetic number. Separate task ref and state
    # per run, so repeated cloud tests do not rewrite a user's work.
    issue = '9000' + os.environ['GITHUB_RUN_ID']
    owner = {'providers': {'claude': {'models': ['claude-sonnet-5-5']},
                           'codex': {'models': ['gpt-6.1-sol']}},
             'backoff': {'initial_seconds': 300, 'max_seconds': 21600}}
    candidates = [{'provider': provider, 'model': entry['models'][0]} for provider, entry in owner['providers'].items()]
    policy = {'tasks': {'proof': candidates}}
    report = {'status': 'failed', 'stage': 'prepare'}
    try:
        with tempfile.TemporaryDirectory(prefix='runtime-proof-') as directory:
            work = Path(directory, 'work')
            # Plain git checkout; the model cannot see either this process's
            # environment or git metadata as writable mounts.
            subprocess.run(['git', 'clone', '--quiet', '--no-checkout',
                            'https://github.com/' + repository + '.git', str(work)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
            subprocess.run(['git', '-C', str(work), 'checkout', '--quiet', '--detach',
                            'origin/' + os.environ.get('DEFAULT_BRANCH', 'main')], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            (work / '.git/info/exclude').write_text('.session/\n')
            (work / '.session').mkdir()
            (work / '.session/issue.md').write_text('Write src/provider-proof.txt containing exactly BROKER_TASK_READY. '
                'Read it back to verify. Write .session/report.md with the session report marker and YAML status done. '
                'Then propose Finish with status done. Use only role tools, no native tools.')
            broker = Broker(work, {'tools': ['Read', 'Write', 'Edit', 'Glob', 'Grep'], 'write': ['src/**']},
                            {'protected': ['.github/', 'engine.yml', 'goal/'], 'evaluator_paths': ['policy/evaluator/']})
            backend = GitHubBackend(repository, base=os.environ.get('DEFAULT_BRANCH', 'main'))
            backend.initialize()
            store = Store(backend)
            # Keep smoke availability distinct from real loop availability.
            class SmokeStore:
                def read(self, key):
                    return store.read('proof-' + os.environ['GITHUB_RUN_ID'] + '/' + key)
                def update(self, key, change):
                    return store.update('proof-' + os.environ['GITHUB_RUN_ID'] + '/' + key, change)
            durable = SmokeStore()
            checkpoint = Checkpoint(broker, repository, issue)
            credentials = {'claude': os.environ.get('CLAUDE_CODE_OAUTH_TOKEN', ''),
                           'codex': os.environ.get('CODEX_WORKER_AUTH_JSON', '')}
            report['stage'] = 'execute'
            runtime = Runtime(owner, policy, 'proof', durable, 'sessions/' + issue + '.json', broker,
                              checkpoint, credentials, 'Read .session/issue.md and complete its task.', 'smoke-v1')
            result = runtime.run(12, 240)
            report.update(result)
            state = durable.read('sessions/' + issue + '.json')
            if result['status'] != 'done' or (work / 'src/provider-proof.txt').read_text().strip() != 'BROKER_TASK_READY':
                raise RuntimeError('proof task incomplete')
            # Replace session outputs as if the runner were lost, restore from
            # remote release, then confirm the report and source both survived.
            (work / '.session/report.md').unlink()
            checkpoint.restore(state)
            if not (work / '.session/report.md').read_text():
                raise RuntimeError('proof report missing after restore')
            remote = checkpoint.git('ls-remote', 'origin', 'refs/heads/task/' + issue, remote=True).stdout
            if state['head'] not in remote:
                raise RuntimeError('proof code checkpoint missing')
            report.update(status='success', stage='complete', checkpoint=state['head'], branch='task/' + issue,
                          availability=durable.read('pool.json').get('availability', {}))
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError):
        report['status'] = 'failed'
    Path(os.environ['RUNNER_TEMP'], 'runtime-proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))
    return 0 if report['status'] == 'success' else 1


if __name__ == '__main__':
    raise SystemExit(main())
