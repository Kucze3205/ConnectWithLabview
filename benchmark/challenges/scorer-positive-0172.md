# Scorer positive-execution guard (#766, task scorer-positive-fix-0172)

## Source
Corrects finding 5 of review #763. The `expected_positive` values are the `expected` objects of the controls at commit 27e7495d (the parent of 8cb25137, before the zero-execution change). They were extracted verbatim from `git show 27e7495d:<fixture>` by `.session/artifacts/insert_expected_positive_0172.py` (byte slice via `json.JSONDecoder.raw_decode`). score.py output was not used.

## Controls
- `benchmark/challenges/library-icon-tests.json`, control `extra-true-answer`: 7908 bytes, sha256 `41ed4e9979f2f8b7a861ede8949a321b1b7169d2ac19b697f22730b05df628ba`.
- `benchmark/challenges/library-specialty.json`, control `positive-control`: 6086 bytes, sha256 `b557fbe850d87a2873a3052ffccc86e596b43233e7b95907dc26569f1daf15ee`.

Helper output: the helper asserted that each `expected_positive` equals the 27e7495d `expected` parsed value and differs from the current zero-execution `expected`. It printed the byte counts and hashes above, and exited 0.

## Change
In `regression_self_test` of `benchmark/scripts/score.py`:
- The baseline is compared with `control['expected_positive']` and raises if it differs.
- Each mutation is compared with `expected_positive` (`mismatches = compare(computed, positive)`), so `not mismatches` is meaningful again.
- The tautological `baseline_outcomes != outcomes_for(score(..., dict(ran)))` check is removed.
- The zero-execution branch (the `executed<=0` / `scored<=0` / null `native_run` branch) is unchanged.

## Pins
`python3 -I .session/artifacts/repin_0172.py` ran `main()` once, then replaced the old hash of results/challenges.json in preparation.json, writing/input-pins.json, writing/c1-challenges-0125-pins.json and writing/reviews-0128/c1-artifact-manifest-0126.json (one occurrence each). Current hashes:
- score.py `b27042995d14b98fa351cbf5bb7bce9179b77f403490d9941b14da6871481537`
- library-icon-tests.json `e4ef68c4c2f3ce25b9ea1ab50297f13e229b7373b0430a97667de6610c3e13fa`
- library-specialty.json `b62e249554b25fa67ec5726d9751f52bda74a982914ab53df0b5917a68604a2e`
- results/challenges.json `45381537c7f3992e56251fa544c169118d8a2dc527f0c8db0057a09a4ceca15e`

Open issue: the verify helper found no pin of score.py or the two fixtures in any benchmark JSON file except results/challenges.json (which embeds the fixture hashes). Its "old" hashes also equal the new ones, so its stale-pin check was not informative (HEAD seemed to already contain the new bytes). I could not confirm that the old score.py hash (`c2d20475...`) is gone from the pin files, so a reviewer should grep for it.

## Checks
`python3 -I .session/artifacts/run_checks_0172.py` (faulthandler 60 s, stdin on os.devnull):
```
self-test pass library-icon-tests [('extra-claim-condition', 10)]
mutation detected library-icon-tests regression self-test: positive control does not match
self-test pass library-specialty [('extra-condition', 13), ('missing-condition', 8), ('wrong-literal', 12), ('missing-claim', 8), ('wrong-citation', 6)]
mutation detected library-specialty regression self-test: positive control does not match
generate totals {"cannot_evaluate": 0, "controls": 33, "fixtures": 3, "matches": 33, "mismatches": 0}
```
The in-memory mutation set one `expected_positive` correctness value to `incorrect`, and the self-test failed as expected. `main()` printed the same totals and returned 0. The pin helper output is listed under Pins. No evaluator, network, model or LabVIEW calls were made, and check_c1_challenges_0125.py was not run.
