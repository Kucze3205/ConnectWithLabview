"""Entry point staged from trusted engine code, outside the role filesystem."""
import json
import os
from pathlib import Path
import time

from role_runtime import Runtime
from runtime_checkpoint import Checkpoint
from runtime_store import GitHubBackend, Store
from tool_broker import Broker


def main():
    trusted = Path(__file__).resolve().parent
    options = json.loads((trusted / 'runtime.json').read_text())
    output = Path(os.environ['RUNNER_TEMP'])
    (output / 'agent-start').write_text(str(int(time.time())))
    result = {'status': 'crashed', 'reason': 'runtime_not_ready'}
    try:
        broker = Broker(os.environ['WORK'], options['profile'], options['config'])
        checkpoint = Checkpoint(broker, os.environ['GITHUB_REPOSITORY'], os.environ['ISSUE'])
        backend = GitHubBackend(os.environ['GITHUB_REPOSITORY'], base=os.environ['DEFAULT_BRANCH'])
        backend.initialize()
        store = Store(backend)
        key = 'sessions/' + os.environ['ISSUE'] + '.json'
        state = store.read(key)
        if state:
            checkpoint.restore(state)
        checkpoint.git('checkout', '-B', 'task/' + os.environ['ISSUE'])
        credentials = {provider: os.environ.get(secret, '') for provider, secret in {
            'claude': 'CLAUDE_CODE_OAUTH_TOKEN', 'codex': 'CODEX_WORKER_AUTH_JSON',
            'copilot': 'COPILOT_GITHUB_TOKEN'}.items()}
        runtime = Runtime(options['owner'], options['policy'], options['task'], store, key, broker,
                          checkpoint, credentials, (trusted / 'prompt.md').read_text(), options['fingerprint'],
                          effort=os.environ['EFFORT'])
        result = runtime.run(int(os.environ['MAX_TURNS']), int(os.environ['AGENT_TIMEOUT']) * 60)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError):
        # Do not echo exceptions from subprocesses or account documents.
        pass
    finally:
        (output / 'provider-execution-output.json').write_text(json.dumps(result))
        (output / 'agent-exit').write_text('0' if result['status'] != 'crashed' else '1')
        (output / 'agent-end').write_text(str(int(time.time())))
    return 0 if result['status'] != 'crashed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
