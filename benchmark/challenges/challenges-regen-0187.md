# challenges-regen-0187: regenerate benchmark/results/challenges.json

The file is `benchmark/results/challenges.json` (the issue says `results/challenges.json`; score.py `OUT` is the benchmark path). Regenerated once by `.session/artifacts/challenges_regen.py` (`python3 -B`, `sys.dont_write_bytecode = True`, `score.main()` once). Output: `.session/artifacts/challenges-regen-output.txt`. score.py and the fixtures were not changed.

## Diff
Key-level comparison of old (copy in `.session/artifacts/challenges-old.json`) and new, leaf paths:
- leaves old 15821, new 16843; changed 4, added 1022, removed 0.
- Changed: `/fixtures/0/sha256` (library-icon-tests), `/fixtures/1/sha256` (library-specialty), `/totals/controls` 33 -> 35, `/totals/matches` 33 -> 35.
- Added: control `constant-keyed-literal-export` in library-icon-tests (`/fixtures/0/controls/27`, 511 leaves) and in library-specialty (`/fixtures/1/controls/2`, 511 leaves). Both have match true.
- No other outcome changed. `mismatches` 0, `cannot_evaluate` 0. vi-actor-core-native-gap is unchanged (same hash).
- Size: 890160 -> 947058 bytes.

## Pins
Pins of benchmark/results/challenges.json, old sha256 `45381537c7f3992e56251fa544c169118d8a2dc527f0c8db0057a09a4ceca15e`, new `a78df4950339b8ea60521eb855ae43a8f6aa12d3d71b58e297712ee6b7ef9d46`:
- benchmark/preparation.json (updated)
- benchmark/writing/input-pins.json (updated)

Embedded fixture hashes (old -> new):
- library-icon-tests.json `e4ef68c4c2f3ce25b9ea1ab50297f13e229b7373b0430a97667de6610c3e13fa` -> `5c1b6873499b08f67c1be60abe73135788b86da5ef70a2696dd57c76c4fc5c57`
- library-specialty.json `b62e249554b25fa67ec5726d9751f52bda74a982914ab53df0b5917a68604a2e` -> `42480b8ca50ed3ad3c2b6a3328992b19e230c65fe87e62ba95968411903fab3f`

## Checks
- Regeneration reports 35 controls, 35 matches, 0 mismatches, 0 cannot_evaluate.
- Verification command: see `.session/report.md`.

## Limits
- Still a synthetic self-comparison: quality_measured false, no LabVIEW behaviour claimed, benchmark readiness false.
- Not edited (historical records): benchmark/challenges/scorer-positive-0172.md and other challenges/*.md with old hashes; benchmark/writing/c1-challenges-0125-pins.json and benchmark/writing/reviews-0128/c1-artifact-manifest-0126.json record the earlier file (885172 bytes, same old sha256), which already differed from the pre-regeneration size 890160, so they are task-time snapshots. A reviewer should confirm that reading.
- benchmark/preparation-status.json mentions the file only in prose (33 controls); not changed.
