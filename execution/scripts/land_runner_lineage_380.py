"""Land the #369 runner pin and repair the stale lineage.py limitation text.

Step 1 runs execution/scripts/pin_runner_369.py (hash-gated, idempotent).
Step 2 makes benchmark/scripts/lineage.py generate the split limitation wording
that pin script #300 wrote into preparation-status.json (re-review #298), then
regenerates lineage outputs and re-pins lineage.py. Requires LABVIEW_ENVIRONMENT.
Idempotent: a second run changes nothing.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
LINEAGE = ROOT / 'benchmark/scripts/lineage.py'
OLD = '(not independently re-reviewed)'
NEW = ('(re-review #298 confirmed the live mutation checks and exact reasons; its own revert harness '
       'was masked, so Policymaker #300 reverted each fix in a temporary copy and --check exited 1 both times)')
STATUS_AFTER_PIN = '85b0f7192bc8df794b6637649c6a657b7270fc589033c13d4c1abecd6cfeb451'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args):
    result = subprocess.run([sys.executable, '-I', '-B', *args], cwd=ROOT, capture_output=True, text=True)
    print('$', ' '.join(args), '->', result.returncode)
    print(result.stdout[-1500:], result.stderr[-1500:])
    if result.returncode != 0:
        sys.exit('failed: ' + ' '.join(args))


def main():
    run('execution/scripts/pin_runner_369.py')
    status = ROOT / 'benchmark/preparation-status.json'
    if sha(status) != STATUS_AFTER_PIN:
        sys.exit('unexpected preparation-status.json sha256 ' + sha(status))
    text = LINEAGE.read_text()
    if NEW not in text:
        preparation = json.loads((ROOT / 'benchmark/preparation.json').read_text())
        pins = {e['sha256'] for entries in preparation['milestones'].values()
                for e in entries if e['path'] == 'benchmark/scripts/lineage.py'}
        if pins != {sha(LINEAGE)}:
            sys.exit('lineage.py does not match its pin')
        if text.count(OLD) != 1:
            sys.exit('old limitation text not found exactly once')
        LINEAGE.write_text(text.replace(OLD, NEW))
        run('benchmark/scripts/lineage.py')
    run('benchmark/scripts/lineage.py', '--check')
    if sha(status) != STATUS_AFTER_PIN:
        sys.exit('lineage regeneration changed preparation-status.json')
    for check in ['benchmark/scripts/runner_contract.py', 'benchmark/scripts/run_record.py',
                  'benchmark/scripts/split_boundary.py', 'policy/evaluator/evaluate.py']:
        run(check, '--check')
    for path in ['benchmark/scripts/lineage.py', 'benchmark/lineage.json', 'benchmark/lineage.md',
                 'benchmark/preparation-status.json', 'benchmark/preparation.json']:
        print(path, sha(ROOT / path))
    return 0


if __name__ == '__main__':
    sys.exit(main())
