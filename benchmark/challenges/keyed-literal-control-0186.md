# Keyed-literal constant-export control (0186)

Development-only synthetic fixture scoring; no LabVIEW behaviour is claimed. Benchmark readiness stays false.

## Overlap

Existing `constant-export` control, per fixture (benchmark/challenges/library-icon-tests.json and benchmark/challenges/library-specialty.json, key path `/controls/<index of constant-export>/submitted`): it sets only `reader_response` (and `raw_reader_response`) to the fixed bytes with two observations, R0001=20008000 and R0005=Actor.lvclass. Its `answer_record` is the unchanged positive-control answer. It therefore never makes every required claim answer with one real claim's key and citations. Verdict: **ADDED** (not ALREADY-COVERED).

## Change

- Control `constant-keyed-literal-export` appended to `/controls` of both fixtures, copied from `positive-control`: every claim (A0001-A0010, N0001, N0002) gets A0001's literal and citations; conditions, reader channel and probe unchanged; raw answer text and SHA256 regenerated. Authored expected: correctness and grounding `incorrect`, fidelity `unverified`. Built by `.session/artifacts/add_keyed_literal_control.py`, which compared against `score.compute` first (0 mismatches, no cannot_evaluate reasons for both fixtures).
- benchmark/scripts/score.py `regression_self_test`: new block asserts the control is `incorrect`/`incorrect`/`unverified` at zero and at positive execution, and matches its authored `expected`. Scoring logic untouched.
- Pins updated (old -> new sha256; bytes where pinned):
  - library-icon-tests.json e4ef68c4c2f3ce25b9ea1ab50297f13e229b7373b0430a97667de6610c3e13fa -> 5c1b6873499b08f67c1be60abe73135788b86da5ef70a2696dd57c76c4fc5c57 (1057554 -> 1098900 bytes)
  - library-specialty.json b62e249554b25fa67ec5726d9751f52bda74a982914ab53df0b5917a68604a2e -> 42480b8ca50ed3ad3c2b6a3328992b19e230c65fe87e62ba95968411903fab3f (83146 -> 123963 bytes)
  - score.py b27042995d14b98fa351cbf5bb7bce9179b77f403490d9941b14da6871481537 -> 978982273f2ce670f3b94bd1dc75cf251301549b2d45c36f312a3cbe3245a644 (20858 -> 23471 bytes)
  - in each of benchmark/preparation.json, benchmark/writing/input-pins.json, benchmark/writing/c1-challenges-0125-pins.json, benchmark/writing/reviews-0128/c1-artifact-manifest-0126.json (via `.session/artifacts/update_pins.py`).

## Checks

`python3 -B .session/artifacts/keyed_literal_control_check.py` (guarded, `sys.dont_write_bytecode = True`, `main()` not called) ran `regression_self_test` on both fixtures: both OK, `has_control True`; the specialty run lists mutations extra-condition, missing-condition, wrong-literal, missing-claim, wrong-citation; icon-tests lists extra-claim-condition. Output: `.session/artifacts/keyed-literal-control-output.txt`. benchmark/results/challenges.json is unchanged (sha256 45381537c7f3992e56251fa544c169118d8a2dc527f0c8db0057a09a4ceca15e).

## Limits

- Only answer-channel constant tested; reader channel left as in the positive control. Detection relies on key comparison, not an independent key check.
- benchmark/results/challenges.json embeds the old fixture SHA256s and 33 controls, so `score.py --check` will differ until results are regenerated; this task was forbidden to change it. A separate task must regenerate it.
- `challenges.py --check` already failed on main before this change (fixture bytes and extra .md files differ); the generator does not emit this control.
- No native evidence; synthetic scoring is not reader execution. A reviewer session is still needed.
