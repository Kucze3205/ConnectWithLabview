# Controlled same-version pair protocol

Scope: stage exit 1 of [delivery.md](../delivery.md#two-concrete-exits), addressing [0099's open uncertainty](../../0099-writing-version-effort.md#what-next). No real pair exists yet.
Read [owner-instructions.md](owner-instructions.md); do not fabricate a pair or write a changed VI with this tool.
The owner must supply eight VIs and `fixtures/authoring.md`, with one consistent recorded version/bitness, no password, exact changes, and save settings.
Before hashing, review that record: each logic pair changes only the specified primitive or I32 value; terminals and other settings stay fixed.
File names, save events, and automatic metadata changes can introduce unrelated differences. Retain all such differences; do not classify them as semantics without evidence.

A real pair can localize candidate primitive identity and constant value spans, including accompanying type/heap changes.
It can show which 16-byte BDPW chunks change and whether LVSR flags and VICD/CPC2 payloads or presence change.
Compare each logic pair with normal code and with separate compiled code; then compare each unchanged diagram across those save settings.
This observes candidate dependencies, not their derivation or a safe invalidation rule.
It cannot establish general integrity rules, other versions, validity of a future edit, terminal meaning beyond the author's record, or behavior.
No session runs LabVIEW; parser success and agreeing declarations are not native compatibility evidence.

Pin inputs once, before comparing. From the repository root, after the owner supplies the files, run:
```sh
python3 - <<'PY'
import hashlib, json
from pathlib import Path
p = Path('docs/research/poc/pair/fixtures')
names = ['add-normal.vi', 'subtract-normal.vi', 'add-separate.vi', 'subtract-separate.vi',
         'constant-1-normal.vi', 'constant-2-normal.vi', 'constant-1-separate.vi', 'constant-2-separate.vi']
hash_file = lambda n: hashlib.sha256((p / n).read_bytes()).hexdigest()
m = {'schema_version': 1, 'files': {n: hash_file(n) for n in names},
     'authoring': {'path': 'authoring.md', 'sha256': hash_file('authoring.md')}}
with (p / 'pins.json').open('x') as f:
    f.write(json.dumps(m, indent=2) + '\n')
PY
```
Retain the manifest and settings together. Never regenerate pins to dismiss a mismatch; resolve it and document a new authoring set instead.
Exact replay (prepared `LABVIEW_ENVIRONMENT` required) compares all four logic pairs and all four save-setting pairs:
```sh
python3 - <<'PY'
import subprocess, sys
from pathlib import Path
p = Path('docs/research/poc/pair')
pairs = [('add-' + mode, 'subtract-' + mode) for mode in ('normal', 'separate')]
pairs += [('constant-1-' + mode, 'constant-2-' + mode) for mode in ('normal', 'separate')]
pairs += [(stem + '-normal', stem + '-separate') for stem in ('add', 'subtract', 'constant-1', 'constant-2')]
for a, b in pairs:
    with (p / (a + '--' + b + '.json')).open('w') as output:
        subprocess.run([sys.executable, '-I', str(p / 'pair_diff.py'), '--pins', str(p / 'fixtures/pins.json'),
                        str(p / 'fixtures' / (a + '.vi')), str(p / 'fixtures' / (b + '.vi'))], stdout=output, check=True)
PY
```
The manifest option checks both VI hashes and the authoring record before loading; any pin/load failure emits `blocked` JSON and exits nonzero. Stop there.
For a direct two-path invocation, run `python3 -I docs/research/poc/pair/pair_diff.py LEFT.vi RIGHT.vi`; JSON goes to stdout, with no VI output.
Resources retain type/ID/duplicate occurrence, names, presence, lengths and SHA256s. Differing spans have offset, length, and both hex values, split into at most 32 bytes each; no spans are omitted.
Raw resource offsets exclude the outer resource-length word. Decompressed offsets include the inner heap-length word. Whole-file spans also capture framing, padding and metadata changes.
BDHb/FPHb and other recognized UInt32-size-prefixed zlib payloads are decompressed using [inspect_vi.py's framing and bound](../inspect_vi.py). Unsupported known heaps block. Other codecs remain unsupported.
The pinned pylavi loader and version classes are reused; [file.py:331–338,420–465](https://github.com/marcpage/pylavi/blob/35d2a0318f71dcb87bb9c431dc00700ee6b9fb75/pylavi/file.py#L331) preserve resource enumeration; [resource_types.py](https://github.com/marcpage/pylavi/blob/35d2a0318f71dcb87bb9c431dc00700ee6b9fb75/pylavi/resource_types.py#L54) supplies BDPW/version/flag interpretations.
Replay today's controls: `python3 -I docs/research/poc/pair/pair_diff.py --self-check`. Read [selfcheck.json](selfcheck.json) field `status`; only `passed` establishes these tool controls.
The identical pinned add.vi control requires zero differences. The one-byte decompressed-heap control exists only in memory and must localize exactly one resource/offset; it is not LabVIEW evidence.
Next session: inspect the author's settings and hashes, run the replay, then report observed candidate spans/dependencies and remaining uncertainty. Do not repeat RSRC discovery or infer Add/Subtract from 103/104.
