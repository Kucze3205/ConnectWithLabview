# Constant / empty export detection: measurement and design

Development only; no LabVIEW behaviour is claimed and benchmark readiness stays false.
Probe: `benchmark/challenges/constant_probe_tmp.py` (loads `benchmark/scripts/score.py` with
importlib, never runs `main()`, never writes results). Output with the commit tested
(`0f6009a29b3f6e34843654008700199fcd59db3b`): `benchmark/challenges/constant_probe_out_tmp.txt`.
The `.session/artifacts/` paths named in the task did not persist in this session, so the probe
and its output live under `benchmark/challenges/` instead.

## Measured

The probe took each fixture's `positive-control` submission, replaced it in memory, re-hashed the
raw JSON and called `score.compute` with executed=scored=1 and with the declared execution.

| Probe | Fixture | Verdict | Deciding score.py line |
|---|---|---|---|
| empty export (no claims, no observations) | library-icon-tests | DETECTED: all 12 required ids `missing` in correctness, grounding, fidelity | line 204 (`common = 'missing'`, `not records`) |
| empty export | library-specialty | DETECTED: same, 12 `missing` | line 204 |
| constant export (same string for every claim and observation) | library-icon-tests | DETECTED: 10 `incorrect`, 2 `unverified`; every dimension `incorrect` | lines 207-208 (`any(v != target ...)`) |
| constant export | library-specialty | DETECTED: same | lines 207-208 |
| empty / constant | vi-actor-core-native-gap | NOT-APPLICABLE: the fixture has only `unsupported-*` controls, no positive control to perturb | n/a |

Baseline for comparison (unperturbed positive control, executed=1): 10 `correct`, 2 `unverified`;
with the declared (zero) execution all 12 are `unverified`. So the perturbed outputs differ from
both baselines. `compare` against the authored expectations reported many mismatches (72-86) for
the perturbed runs, i.e. they are not mistaken for the control.

Both fixtures also already list a control named `constant-export`. I did not read its content, so
this document does not assess it.

## Design

Gap: detection today is incidental. A constant is caught only because the string differs from each
key, and an empty export is only `missing`, with no `cannot_evaluate_reasons` entry and no distinct
label. Neither run is flagged as a degenerate export. Proposed controls, written before any code change:

1. `constant-matching-one` fixture: the same string for every claim, chosen to equal the key of one
   required id. Expected: that id `correct`, the other keyed ids `incorrect`, dimension `incorrect`
   (`assessment` returns `incorrect` if any item is). This pins that partial luck is not credit for the export.
2. `empty-status-ok` fixture: `status` is ok but there are zero claims and observations. Expected: all
   required ids `missing`, dimensions `missing`, never `correct` or `unsupported`.
3. Scorer control (a later, separately reviewed change): add a ledger entry `degenerate_export` when
   at least 3 distinct required ids share one identical submitted value, or when the submission has zero items
   while `status` is not `unsupported`/`error`. Expected: the entry appears for probes 1-2 and for the
   existing `constant-export` control, and not for `positive-control`. The threshold of 3 is a proposal,
   not an owner-approved number.

Any change to score.py or a fixture needs its pins and `results/challenges.json` regenerated together.

## Limits

- Synthetic fixtures only; no native reader, no model output was scored.
- The mutation was applied to the positive control; other controls were not perturbed.
- The existing `constant-export` control and the pinned results were not inspected.
- The review #779 mutation check remains an accepted, unrepeated limit.
- A constant that matches every key (impossible while keys differ) is untested.
- Verdicts hold at the commit above; the reviewer has not independently checked them.
