# Scorer probe (scorer-probe-0164)

Measurement only. Question: does `benchmark/scripts/score.py` deny credit to each control kind named in `benchmark/challenges/gap-0160.md`? Expectations were written from the code before the run. The run called `score.generate()` through `importlib` with `python3 -I`, with no network, model, reader, evaluator or native call. Output went only to `.session/artifacts/scorer-probe-0164-generate.json`; `main()` was not called, so `benchmark/results/challenges.json` was not written. All fixtures are synthetic and the key is the provisional XML key, so "denies credit" here means "no `correct` outcome on these fixtures". No native behaviour is claimed.

Run totals (artifact): 3 fixtures, 33 controls, 33 matches against authored expectations, 0 cannot-evaluate. Every control declares planned 1, attempted/executed/scored 0.

## wrong-answer
Expectation from code: a submitted value that differs from the keyed value gets `incorrect` (score.py lines 206-207, `any(v != target)`). The dimensions of that claim then take that outcome (lines 214-221), and `assessment` (lines 34-49) lets `incorrect` dominate. Extra (non-required) false claims get `incorrect` through `extra_outcome` (lines 94-122).
Run: yes. Artifact `scorer-probe-0164-generate.json`. `library-icon-tests` control 1 `wrong-answer-declared-dependency` gives correctness incorrect and grounding incorrect. Controls 5 and 10 (extra-false, contradiction) also give incorrect.
Caveat: the comparison is against the author-derived provisional key. It covers XML literal facts only, not computed or native answers.
Verdict: denies-credit

## wrong-source
Expectation from code: grounding is assessed only when the value is already `correct` (lines 216-218). It then calls `citation_support` (lines 67-75). That function returns `incorrect` unless every citation, including hash and exact property, is in the keyed list, and it returns `missing` for no citation. So a real locator of another member, or an unresolvable locator, should give grounding `incorrect`.
Run: yes. Controls 2 `wrong-citation-existing` and 3 `wrong-citation-unresolvable` give grounding incorrect. The aggregate correctness is `unverified`. I did not check per-id values, so I did not establish why. The fixture's other required ids are probably unverified.
Caveat: citation checks cover XML inventory locators only. There are no native-diagram or VI-source citations.
Verdict: denies-credit

## constant-or-empty-export
Expectation from code: no code detects constant output as such. Credit depends only on values matching the key. A constant export asserting wrong values should get `incorrect` (line 207). An empty, wrapper-only or truncated reader response has no records and gets `missing` (line 203). A constant export that happened to match the key would get credit, and the scorer cannot tell.
Run: yes. `library-icon-tests` 26 and `library-specialty` 1 (`constant-export`) give fidelity incorrect. Controls 18-20 (empty, wrapper-only, truncated) give fidelity missing. Control 22 (failed) gives `error`.
Caveat: the denial comes from the authored constants differing from the authored expectation, not from constant-ness. No real exporter output was scored.
Verdict: denies-credit (only for these fixtures; constant detection is not handled)

## unsupported-case
Expectation from code: a status of `unsupported` with no records gives `unsupported` for each required id (lines 198-199). This is a separate category, not `correct`.
Run: yes. All four `vi-actor-core-native-gap` controls (missing runtime, dependency, license, inaccessible diagram) give `unsupported` on all three dimensions. `library-icon-tests` 21 gives fidelity unsupported.
Caveat: these are injected declarations, not observed environment failures. The scorer does not check that the unsupported claim is true.
Verdict: denies-credit

## no-credit-for-zero-execution
Expectation from code: `declared_execution` is copied to the output at line 243 and never used in a decision (a grep for `executed` in logic finds nothing). A missing key (`independent_key` null, line 147) gives `unverified` (lines 204-205). Zero executed tests or a missing native run are not read, so they have no effect on the outcome. A submission whose values match the key would get `correct` (line 213) whatever the execution counts say.
Run: yes. Controls 23 `missing-independent-key`, 24 `missing-native-run` and 25 `zero-executed-tests` all give `unverified` on all dimensions. This is not `correct`, but I did not isolate the cause for 24 and 25. Nothing tested a matching answer with zero execution, so I did not show that credit is withheld for that reason.
Verdict: not-handled (a missing key gives `unverified`, but execution counts are not consulted)

## Pins
HEAD: c89990eedfcee8e421541b70ec48b5cd92976e63 (measured with `git rev-parse HEAD`; gap-0160 pinned e5d2db7b, an earlier commit)

SHA256 (measured this session):
- benchmark/scripts/score.py 810a5457c3c32ff8c856ae3d960ea06a495860b1efa5c78a8a895610eb649aac
- benchmark/challenges/library-icon-tests.json ad0413fda8f0e75c18a87aadec0cd18abe2733dea5c896f1dcbeb0505836b2a4
- benchmark/challenges/library-specialty.json d34933b668f556323ce13c4a03d548b83a0de6eef168421494bff86e3769c752
- benchmark/challenges/vi-actor-core-native-gap.json ee3bc374b0fe5878c43c449850654d2101bf45bc30f8748cbd94a450ec7d5bcf
- .session/artifacts/scorer-probe-0164-generate.json f3640eca35d7779fa52fb6a29a69f0e86430bb8b85e26f267bbdbc61046d2225

The fixtures' inventory files were loaded by score.py through `source.inventory_path` and were not hashed separately here.

## Not counted
- benchmark/writing/check_c1_challenges_0125.py: invalidated (#544 / 0125); not run.
- benchmark/results/challenges.json and the 33/33 totals: not counted as evidence. They compare the scorer with the same author's expectations, and the file records `quality_measured` false and `independently_reviewed` false. The probe regenerated the numbers in memory only.
- The `regression_self_test` mutations inside score.py: inspected only as code. They check that outcomes change, not that credit is denied.
- Native behaviour, real exporter output and any reader or model run: none exist or were attempted.
- Per-id attribution for controls 2, 3, 24 and 25: not extracted, so reasons for the aggregate `unverified` values are inferred, not measured.
- The positive controls themselves score `unverified`, not `correct`, on every dimension. This was not investigated, and it means no fixture shows the scorer awarding credit.
