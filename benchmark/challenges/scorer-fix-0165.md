# Scorer fix (scorer-fix-0165)

## Positive-control cause

Written before the code change. Measured in memory with `python3 -I`, calling `compute()` only; `main()` was not called. Control `library-icon-tests` /controls/0 `positive-control` (control 24 `missing-native-run` gives identical per-id values):
- correctness: A0001-A0010 `correct`; N0001, N0002 `unverified`.
- grounding: A0001-A0010 `correct`; N0001, N0002 `unverified`.
- fidelity: R0001-R0010, RN0001, RN0002 all `unverified`.

So the probe's aggregate `unverified` comes from `assessment` (score.py lines 34-49), where any `unverified` id makes the dimension `unverified`. The per-id values do contain `correct`.
Lines that produce them (branch order in `compute`, original numbering):
- N0001/N0002 on the answer channel reach lines 204-205 (`key is None or target is None` gives `unverified`). I read this from branch order and did not isolate which of the two conditions holds.
- Fidelity ids reach lines 210-211 (`channel == 'reader' and native == 'unavailable'` gives `unverified`), after the value (207) and scope (209) checks pass. The key-absent branch (147, 204) is not the cause: the control has no `evidence_record`, so `key_absent` is false.
- A0001-A0010 reach lines 212-213 (`correct`); grounding stays `correct` through `citation_support` (67-75).

This is the intended effect of the provisional key and of missing native references (no independent key or native reference gives `unverified`). I did not change that behaviour.

Also measured: every control in all three fixtures declares `actual_execution` as planned 1, attempted 0, executed 0, scored 0 (27 + 2 + 4 controls). Gap (1) therefore touches every fixture.

## Change

Edited `benchmark/scripts/score.py` (line numbers after the change):
- Line 148: `execution = probe['actual_execution']` in `compute`.
- Lines 213-216: a new `elif` before the final `else: common = 'correct'`. It sets `common = 'unverified'` when `executed <= 0`, when `scored <= 0`, or when `evidence_record` has `native_run` present and null.
- Lines 287-290: `regression_self_test`'s `score()` helper now takes an `execution` argument. Its default `ran` (line 287) declares attempted 1, executed 1, planned 1, scored 1, so the existing mutation checks run on a positive execution.
- Lines 307-313: the new regression cases (below).

Outcome chosen: `unverified`. It already exists, and the file already uses it for "a match that cannot be credited" (no key, lines 204-205; no native reference, lines 210-211). `missing` would claim no answer was submitted, `error` would claim a failure, `incorrect` would claim a wrong value; none is true for a matching answer with no execution. The branch comes after the `incorrect`, scope and key checks, so wrong answers stay `incorrect`. It applies to both channels, so fidelity is covered too.

Side effect, measured: all 33 existing controls declare zero execution, so the frozen `expected` blocks no longer match. `generate()` now reports 5 matches and 28 mismatches (0 cannot-evaluate), against 33/33 before. `benchmark/results/challenges.json` was not rewritten and now differs from regeneration, so `score.py --check` would fail. Fixing that needs fixture or expectation changes, which this task forbids.

## Regression

Added to `regression_self_test` (run on `library-specialty` positive-control, id A0005 plus all ids):
- `zero-executed`: the key-matching submission with `executed=0` must give no `correct` on any id in any dimension.
- `zero-scored`: the same with `scored=0`, same requirement.
- Positive execution (`ran`): the A0005 outcomes must equal the baseline outcomes (the outcome it had before the change). The baseline itself still has to match the control's `expected`, as before.

Command: `python3 -I -c "...importlib...; m.generate()"` (no `main()`).
Short output: `{'fixtures': 3, 'controls': 33, 'matches': 5, 'mismatches': 28, 'cannot_evaluate': 0}`; the self-test returned 6 mutation results (extra-condition, missing-condition, wrong-literal, missing-claim, wrong-citation, extra-claim-condition) and did not raise.
Full output: `.session/artifacts/scorer-fix-0165-generate.json`.
Limit: the new cases check the zero-execution withholding on the existing positive control only. I did not separately test the `native_run` null branch in the self-test; control 24 `missing-native-run` also has zero execution, so it does not isolate that condition.

## Pins

- HEAD: 2f91dff53e5e97e5269455aa9d8856bb7e7f9209 (`git rev-parse HEAD`)
- benchmark/scripts/score.py SHA256 before: 810a5457c3c32ff8c856ae3d960ea06a495860b1efa5c78a8a895610eb649aac
- benchmark/scripts/score.py SHA256 after: 296e2354e312d5a69fe62e9629bc085376c0fa523fbf21ad6601fdf1dad8def8

## Not changed

- Positive-control behaviour (cause 2): untouched; the provisional key and missing native references still give `unverified`.
- Fixtures, `benchmark/results/challenges.json`, and every other file.
- Expectations in the fixtures: they are now stale for 28 controls (see `## Change`); someone with permission must decide how to update them.
- No LabVIEW, native, model, reader, network or evaluator call; no native behaviour is claimed.
- Constant-export detection is still not handled.
