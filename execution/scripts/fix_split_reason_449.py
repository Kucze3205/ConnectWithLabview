"""Fix review #449 finding 1 in benchmark/scripts/split_allocate.py (fix round 2).

The reason self-test used 'expected reason' against 'actual reason'; these differ in
the first character, so a first-character-only comparison passed. The new wrong
expected reason keeps the complete actual reason as a prefix (#418 pattern).
Hash-gated and idempotent. Usage: python3 -I -B fix_split_reason_449.py [repo_root]
"""
import hashlib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
TARGET = ROOT / 'benchmark/scripts/split_allocate.py'
OLD_SHA = '55c236ada2bce447990c7185ac8654a2c8aefba32ae4010fac65ae82a15c8ecd'
NEW_SHA = '3ba01f035967ce67c7e98b02581491abd170dce278adb085bb04d751c35674bd'

OLD = """    try:
        expect_reject('reason comparison self-test', 'expected reason', actual_reason)
    except ValueError as exc:
"""
NEW = """    # The wrong expected reason keeps the complete actual reason as a prefix, so
    # prefix-only or first-character-only comparisons fail this self-test.
    wrong_reason = 'actual reason [deliberately wrong suffix]'
    try:
        expect_reject('reason comparison self-test', wrong_reason, actual_reason)
    except ValueError as exc:
"""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    data = TARGET.read_bytes()
    current = sha(data)
    if NEW_SHA is not None and current == NEW_SHA:
        print('unchanged: ' + current)
    else:
        if current != OLD_SHA:
            raise SystemExit('unexpected split_allocate.py sha256: ' + current)
        text = data.decode()
        if text.count(OLD) != 1:
            raise SystemExit('self-test block not found exactly once')
        out = text.replace(OLD, NEW).encode()
        if NEW_SHA is not None and sha(out) != NEW_SHA:
            raise SystemExit('result sha256 differs from expected: ' + sha(out))
        TARGET.write_bytes(out)
        print('wrote: ' + sha(out))
    run = subprocess.run([sys.executable, '-I', '-B', str(TARGET), '--check'],
                         capture_output=True, text=True)
    print('split_allocate.py --check exit %d' % run.returncode)
    if run.returncode != 0:
        print(run.stderr, file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
