"""Replace stale 'store not ready' text after review #431 and regenerate lineage pins.

Idempotent. Needs LABVIEW_ENVIRONMENT (lineage.py reads the prepared sources).
Run from the repository root: python3 -I -B execution/scripts/update_store_text_431.py
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
RECORD_SHA = '019a3e48cd2066aca423ea334631395299322cb50bf61f5be458d44f518a836f'

EDITS = {
    'benchmark/scripts/lineage.py': [(
        '"the restricted store (capability #268) is not ready, and no secrecy is claimed; "',
        '"the restricted store (capability #268) has an executed readiness record accepted by review #431 '
        'but holds no case, and no secrecy is claimed; "',
    )],
    'benchmark/split/README.md': [(
        'The restricted store and isolated runner are not ready; the Row 1 capability request is pending.',
        'The restricted store has an executed readiness record (benchmark/split/store-readiness-268.redacted.json, '
        'accepted by review #431) with synthetic sentinels only; it holds no case. The isolated runner is not ready.',
    ), (
        'Split remains blocked by store readiness, custodian checks, new/private cases, variant analysis, '
        'and native structural comparison.',
        'Split remains blocked by new/private cases, variant analysis, and native structural comparison.',
    )],
    'benchmark/preparation-status.json': [(
        "; no real case is allocated; this supersedes the clause 'the restricted store (capability #268) is not ready' "
        "in the lineage limitation, and the generator text in benchmark/scripts/lineage.py needs a later run with "
        "LABVIEW_ENVIRONMENT.",
        '; no real case is allocated.',
    )],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fail(message):
    print('update_store_text_431: ' + message, file=sys.stderr)
    sys.exit(1)


def run(*args):
    result = subprocess.run([sys.executable, '-I', '-B', *args], cwd=ROOT, capture_output=True, text=True)
    print(' '.join(args), 'exit', result.returncode, result.stdout.strip()[:300], result.stderr.strip()[:300])
    if result.returncode:
        fail('command failed: ' + ' '.join(args))


def main():
    if not os.environ.get('LABVIEW_ENVIRONMENT'):
        fail('LABVIEW_ENVIRONMENT is not set')
    record = (ROOT / 'benchmark/split/store-readiness-268.redacted.json').read_bytes()
    if sha(record) != RECORD_SHA:
        fail('store record hash differs')
    for path, pairs in EDITS.items():
        target = ROOT / path
        text = target.read_text()
        for old, new in pairs:
            if text.count(old) == 1:
                text = text.replace(old, new)
            elif text.count(new) != 1:
                fail('expected text not found once in ' + path)
        target.write_text(text)
    # Re-pin the README and the status file wherever the index names them; lineage.py
    # checks the status input pin before it regenerates and re-pins its own outputs.
    index_path = ROOT / 'benchmark/preparation.json'
    index = json.loads(index_path.read_text())
    repin = {path: sha((ROOT / path).read_bytes())
             for path in ('benchmark/split/README.md', 'benchmark/preparation-status.json')}
    found = set()
    for entries in index['milestones'].values():
        for entry in entries:
            if entry['path'] in repin:
                entry['sha256'] = repin[entry['path']]
                found.add(entry['path'])
    if found != set(repin):
        fail('pin not found: ' + ', '.join(sorted(set(repin) - found)))
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True) + '\n')
    run('benchmark/scripts/lineage.py')
    run('benchmark/scripts/lineage.py', '--check')
    run('benchmark/scripts/split_boundary.py', '--check')
    run('policy/evaluator/evaluate.py', '--check')
    for path in ('benchmark/scripts/lineage.py', 'benchmark/split/README.md',
                 'benchmark/preparation-status.json', 'benchmark/preparation.json'):
        print(path, sha((ROOT / path).read_bytes()))


if __name__ == '__main__':
    main()
