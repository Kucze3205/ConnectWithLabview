#!/usr/bin/env python3
"""Replay issue #528's reviewed comparisons without writing any VI."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
BASE = Path('docs/research/poc/pair')
STATUS = BASE / 'replay-0105-status.json'
LIMITATIONS = [
    'No LabVIEW runs; parser success does not establish behavior, an unbroken arrow, native compatibility or save-version preservation.',
    'Positional byte differences and candidate dependencies do not establish semantic identities, general integrity rules or a safe edit rule.',
    'Authoring and save settings are owner claims; unrelated Save As metadata can differ.',
    'The reviewed self-check is not rerun because it rewrites tracked selfcheck.json (review R1).',
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    record = {'schema_version': 1, 'status': 'blocked', 'runs': [],
              'input_hashes': {}, 'limitations': LIMITATIONS}
    verification = {'schema_version': 1, 'status': 'blocked', 'checks': []}
    try:
        manifest_path = BASE / 'fixtures/pins.json'
        review_path = BASE / 'review-0102.json'
        manifest = json.loads(manifest_path.read_text())
        review = json.loads(review_path.read_text())
        if len(manifest['files']) != 8 or len(review['files']) != 4:
            raise ValueError('Expected exactly eight VI pins and four reviewed-file pins')
        expected = {str(BASE / 'fixtures' / name): value
                    for name, value in manifest['files'].items()}
        expected[str(BASE / 'fixtures' / manifest['authoring']['path'])] = manifest['authoring']['sha256']
        expected.update(review['files'])
        for path, wanted in expected.items():
            actual = digest(path)
            record['input_hashes'][path] = actual
            verification['checks'].append({'path': path, 'expected_sha256': wanted,
                                           'sha256': actual, 'matched': actual == wanted})
            if actual != wanted:
                raise ValueError('SHA256 mismatch: ' + path + ': expected ' + wanted + ', observed ' + actual)
        for path in (manifest_path, review_path):
            record['input_hashes'][str(path)] = digest(path)
        verification['status'] = 'verified'
        verification['input_hashes'] = record['input_hashes'].copy()
        save(BASE / 'verification-0105.json', verification)
        pairs = [('add-' + mode, 'subtract-' + mode) for mode in ('normal', 'separate')]
        pairs += [('constant-1-' + mode, 'constant-2-' + mode) for mode in ('normal', 'separate')]
        pairs += [(stem + '-normal', stem + '-separate')
                  for stem in ('add', 'subtract', 'constant-1', 'constant-2')]
        for left, right in pairs:
            output = BASE / (left + '--' + right + '.json')
            argv = [sys.executable, '-I', str(BASE / 'pair_diff.py'), '--pins',
                    str(manifest_path), str(BASE / 'fixtures' / (left + '.vi')),
                    str(BASE / 'fixtures' / (right + '.vi'))]
            completed = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            output.write_bytes(completed.stdout)
            run = {'argv': argv, 'exit_code': completed.returncode, 'output': str(output),
                   'stderr': completed.stderr.decode('utf-8', errors='replace')}
            record['runs'].append(run)
            save(STATUS, record)
            result = json.loads(completed.stdout)
            if not isinstance(result, dict):
                raise ValueError('Tool output is not a JSON object: ' + str(output))
            if completed.returncode != 0 or result.get('status') != 'compared':
                record['blocker'] = result.get('blocker', 'Comparison did not complete: ' + str(output))
                break
        else:
            record['status'] = 'measured'
        changed = {path: {'before': wanted, 'after': digest(path)}
                   for path, wanted in record['input_hashes'].items() if digest(path) != wanted}
        record['unchanged_inputs_after'] = not changed
        if changed:
            record.update(status='blocked', blocker='Inputs changed during replay', changed_inputs=changed)
    except Exception as exc:
        record.update(status='blocked', blocker=type(exc).__name__ + ': ' + str(exc))
        if verification['status'] != 'verified':
            verification['blocker'] = record['blocker']
            save(BASE / 'verification-0105.json', verification)
    save(STATUS, record)
    print(json.dumps({'status': record['status'], 'runs': len(record['runs']),
                      'blocker': record.get('blocker'), 'report': str(STATUS)}))
    return 0 if record['status'] == 'measured' else 1


if __name__ == '__main__':
    sys.exit(main())
