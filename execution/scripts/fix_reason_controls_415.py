#!/usr/bin/env python3
"""Apply fix round 2 for review #415 after isolated bypass checks."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    'change_cases.py': 'ac84acaf7cf6931670f9964f90d4f68b72e7b446927459ce92681c401ab2167e',
    'precision_plan.py': '234a235cd230f70ce95ac303cc4f77b1a19ee11b5443c73a0f5d6bd8e8089ec7',
}
DEPENDENCIES = [
    'benchmark/change-cases/typedef-impact.spec.json',
    'benchmark/change-cases/diagram-difference.spec.json',
    'benchmark/precision/plan.json',
    'benchmark/baseline/run-manifest.template.json',
]


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f'expected one replacement: {old!r}')
    return text.replace(old, new, 1)


def revised(name, original):
    if name == 'change_cases.py':
        text = replace_once(original,
            '    wrong_reason = "deliberately wrong expected reason"',
            '    wrong_reason = actual_reason + " [deliberately wrong suffix]"')
        text = replace_once(text,
            '    print(f"PASS: {len(tests)} in-memory rejecting mutations with asserted reasons")',
            '    return (len(tests), 1)')
        text = replace_once(text,
            '    rejecting_mutations(specs)\n    check_sources(specs)',
            '    completed = rejecting_mutations(specs)\n'
            '    require(completed == (10, 1), "rejecting controls did not complete: expected (10, 1)")\n'
            '    print(f"PASS: {completed[0]} in-memory rejecting mutations with asserted reasons")\n'
            '    check_sources(specs)')
        return text
    text = replace_once(original,
        "    wrong_reason = 'deliberately wrong expected reason'",
        "    wrong_reason = actual_reason + ' [deliberately wrong suffix]'")
    text = replace_once(text,
        '    return len(controls) + 1',
        '    return (len(controls) + 1, 1)')
    return replace_once(text,
        '        count = rejection_controls(plan, template)',
        '        completed = rejection_controls(plan, template)\n'
        "        require(completed == (8, 1), 'rejecting controls did not complete: expected (8, 1)')\n"
        '        count = completed[0]')


def already_revised(name, text):
    expected = 'expected (10, 1)' if name == 'change_cases.py' else 'expected (8, 1)'
    return '[deliberately wrong suffix]' in text and expected in text


def run(path):
    env = os.environ.copy()
    env.pop('LABVIEW_ENVIRONMENT', None)
    result = subprocess.run([sys.executable, '-I', '-B', str(path), '--check'],
                            capture_output=True, text=True, env=env)
    return result.returncode, result.stdout + result.stderr


def verify(candidates):
    with tempfile.TemporaryDirectory(prefix='reason-controls-415-') as directory:
        root = Path(directory)
        for relative in DEPENDENCIES:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        script_dir = root / 'benchmark/scripts'
        script_dir.mkdir(parents=True, exist_ok=True)
        for name, text in candidates.items():
            target = script_dir / name
            target.write_text(text, encoding='utf-8')
            code, output = run(target)
            if code != 0:
                raise ValueError(f'{name}: baseline failed ({code}): {output}')
            if name == 'change_cases.py':
                comparison = 'assert str(exc) == reason, (reason, str(exc))'
                probes = {
                    'first-character': (comparison, 'assert str(exc)[:1] == reason[:1], (reason, str(exc))'),
                    'ten-character-prefix': (comparison, 'assert str(exc)[:10] == reason[:10], (reason, str(exc))'),
                    'disabled-comparison': (comparison, 'assert True, (reason, str(exc))'),
                    'early-return': ('    case, mutate, actual_reason = tests[0]', '    return\n    case, mutate, actual_reason = tests[0]'),
                }
            else:
                comparison = 'if str(error) != expected:'
                probes = {
                    'first-character': (comparison, 'if str(error)[:1] != expected[:1]:'),
                    'ten-character-prefix': (comparison, 'if str(error)[:10] != expected[:10]:'),
                    'disabled-comparison': (comparison, 'if False:'),
                    'early-return': ('    path, value, actual_reason = controls[0]', '    return\n    path, value, actual_reason = controls[0]'),
                }
            for label, (old, new) in probes.items():
                target.write_text(replace_once(text, old, new), encoding='utf-8')
                code, output = run(target)
                if code == 0:
                    raise ValueError(f'{name}: bypass survived: {label}: {output}')
                expected = 'rejecting controls did not complete' if label == 'early-return' else 'reason comparison self-test: mismatch accepted'
                if expected not in output:
                    raise ValueError(f'{name}: {label} failed for an unexpected reason: {output}')
                print(f'PROBE {name} {label}: exit {code}; intended diagnostic confirmed')
            target.write_text(text, encoding='utf-8')
            code, output = run(target)
            if code != 0:
                raise ValueError(f'{name}: restoration failed ({code}): {output}')
            print(f'CHECK {name}: baseline and restoration exit 0')


def main():
    candidates = {}
    original_bytes = {}
    for name, digest in PINS.items():
        path = ROOT / 'benchmark/scripts' / name
        data = path.read_bytes()
        original_bytes[name] = data
        text = data.decode('utf-8')
        if hashlib.sha256(data).hexdigest() == digest:
            candidates[name] = revised(name, text)
        elif already_revised(name, text):
            candidates[name] = text
        else:
            raise ValueError(f'{name}: unexpected source SHA256; no changes applied')
    verify(candidates)
    for name in candidates:
        if (ROOT / 'benchmark/scripts' / name).read_bytes() != original_bytes[name]:
            raise ValueError(f'{name}: changed during verification; no changes applied')
    for name, text in candidates.items():
        path = ROOT / 'benchmark/scripts' / name
        data = text.encode('utf-8')
        if path.read_bytes() != data:
            path.write_bytes(data)
        print(f'SHA256 {name} {hashlib.sha256(data).hexdigest()}')
    print('Source-pin verification skipped in isolated checks; no native execution or model runs.')
    print('Design checks only; quality remains unmeasured; independent review remains required.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
