#!/usr/bin/env python3
"""Land the #228 development scorer without the results.json directory conflict.

Idempotent. Copies benchmark/scripts/score.py from tag iter/0028/228 (sha256-checked),
moves its output from benchmark/challenges/results.json (rejected as an extra entry by
challenges.py --check) to benchmark/results/challenges.json, regenerates the output and
requires it to be byte-identical to the tag's results.json. Drops tracked bytecode.
Does not touch fixtures, challenges.py or preparation*.json. Delete after landing.
"""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys

TAG = 'iter/0028/228'
SCORE_SHA = 'f0a290794a8a8f136a14d875c7bbc5c290200c8fe7019cf8c279c5e746ced89e'
RESULTS_SHA = '4c871803f66422817cfb2825f8ac5f6d5917479cedae35372186e297120b977a'
OLD = "OUT = ROOT / 'benchmark/challenges/results.json'"
NEW = "OUT = ROOT / 'benchmark/results/challenges.json'"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[2]))
    root = Path(parser.parse_args().root).resolve()
    repo = Path(__file__).resolve().parents[2]
    score = root / 'benchmark/scripts/score.py'
    original = subprocess.run(['git', '-C', str(repo), 'show', TAG + ':benchmark/scripts/score.py'],
                              capture_output=True, check=True).stdout
    if sha(original) != SCORE_SHA:
        raise SystemExit('score.py at tag has unexpected sha256')
    text = original.decode('utf-8')
    if text.count(OLD) != 1:
        raise SystemExit('output path line not found exactly once')
    patched = text.replace(OLD, NEW).replace('results.json is missing', 'results/challenges.json is missing')
    if not score.is_file() or score.read_text(encoding='utf-8') != patched:
        score.write_text(patched, encoding='utf-8')
    (root / 'benchmark/results').mkdir(exist_ok=True)
    stale = root / 'benchmark/challenges/results.json'
    if stale.exists():
        stale.unlink()
    subprocess.run([sys.executable, '-I', '-B', str(score)], check=True, cwd=str(root))
    out = (root / 'benchmark/results/challenges.json').read_bytes()
    if sha(out) != RESULTS_SHA:
        raise SystemExit('regenerated results differ from the #228 results.json: ' + sha(out))
    for cache in (root / 'benchmark/scripts/__pycache__',):
        if cache.exists():
            shutil.rmtree(cache)
    print('landed', sha(score.read_bytes()), RESULTS_SHA)
    return 0


if __name__ == '__main__':
    sys.exit(main())
