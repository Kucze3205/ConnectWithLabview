"""Entry point of a routed session, run in the session job (no GitHub token, ADR-0006).

`stage` seeds the runtime state from `loop-runtime` into the bundle (`runtime-pool.json`, `runtime-session.json`);
this run updates a local copy and leaves it in RUNNER_TEMP, where the epilogue takes it in as data and publishes it.
"""
import json
import os
from pathlib import Path
import shutil
import time
from datetime import datetime, timedelta, timezone

import cloud_probe
from role_runtime import Runtime
from runtime_checkpoint import Checkpoint
from runtime_store import LocalBackend, Store
from tool_broker import Broker


def main():
    trusted = Path(__file__).resolve().parent
    options = json.loads((trusted / 'runtime.json').read_text())
    output = Path(os.environ['RUNNER_TEMP'])
    (output / 'agent-start').write_text(str(int(time.time())))
    result = {'status': 'crashed', 'reason': 'runtime_not_ready'}
    key = 'sessions/' + os.environ['ISSUE'] + '.json'
    local = output / 'runtime-state'
    for name, staged in (('pool.json', 'runtime-pool.json'), (key, 'runtime-session.json')):
        if (trusted / staged).is_file():
            (local / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(trusted / staged, local / name)
    try:
        # `policy/prepare.sh` runs in this job, after staging: the prepared sources come from its environment.
        resources = {'environment': os.environ['LABVIEW_ENVIRONMENT']} if os.environ.get('LABVIEW_ENVIRONMENT') else {}
        broker = Broker(os.environ['WORK'], options['profile'], options['config'], resources)
        checkpoint = Checkpoint(broker, os.environ['GITHUB_REPOSITORY'], os.environ['ISSUE'])
        store = Store(LocalBackend(local))
        state = store.read(key)
        if state:
            checkpoint.restore(state)
        checkpoint.git('checkout', '-B', 'task/' + os.environ['ISSUE'])
        credentials = {provider: os.environ.get(secret, '') for provider, secret in {
            'claude': 'CLAUDE_CODE_OAUTH_TOKEN', 'codex': 'CODEX_WORKER_AUTH_JSON',
            'copilot': 'COPILOT_REQUESTS_TOKEN'}.items()}
        runtime = Runtime(options['owner'], options['policy'], options['task'], store, key, broker,
                          checkpoint, credentials, (trusted / 'prompt.md').read_text(), options['fingerprint'],
                          effort=os.environ['EFFORT'], context=options.get('context'),
                          probe=lambda provider, credential, timeout: cloud_probe.probe(provider, timeout, credential=credential))
        result = runtime.run(int(os.environ['MAX_TURNS']), int(os.environ['AGENT_TIMEOUT']) * 60)
    except Exception:
        # This is the credential-bearing outer boundary. Never echo arbitrary
        # subprocess exceptions (git argv can contain an encoded auth header).
        # Preserve pending intent and retry on a fresh runner after interruption.
        delay = options['owner']['backoff']['initial_seconds']
        result = {'status': 'paused', 'reason': 'checkpoint_or_execution_interrupted',
                  'retry_after': (datetime.now(timezone.utc) + timedelta(seconds=delay)).isoformat()}
    finally:
        for name, left in (('pool.json', 'runtime-pool.json'), (key, 'runtime-session.json')):
            if (local / name).is_file():
                shutil.copy(local / name, output / left)
        (output / 'provider-execution-output.json').write_text(json.dumps(result))
        (output / 'agent-exit').write_text('0' if result['status'] != 'crashed' else '1')
        (output / 'agent-end').write_text(str(int(time.time())))
    return 0 if result['status'] != 'crashed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
