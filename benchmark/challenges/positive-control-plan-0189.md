# Positive-control plan (issue #820, #763 finding 4)

Plan only. No control, fixture, score.py or results file was changed. No LabVIEW behaviour is claimed.
Benchmark readiness stays false.

## Gap

Command (run with `python3 -B -I`, reads fixture bytes only, no score.py import):

```
python3 -B -I -c "import json,glob,sys
sys.dont_write_bytecode=True
for f in sorted(glob.glob('benchmark/challenges/library-*.json')):
    c=json.load(open(f,encoding='utf-8'))['controls']
    ok=lambda e:sum(v=='correct' for d in('correctness','grounding') for v in e['per_id'][d].values())
    dim=sum(1 for x in c if 'correct' in (x['expected']['dimensions']['correctness'],x['expected']['dimensions']['grounding']))
    print(f,'controls',len(c),'dim_correct',dim,'per_id_correct_expected',sum(ok(x['expected']) for x in c),'with_expected_positive',sum('expected_positive' in x for x in c),'positive_per_id_correct',sum(ok(x['expected_positive']) for x in c if 'expected_positive' in x))"
```

Output:

```
library-icon-tests.json controls 28 dim_correct 0 per_id_correct_expected 0 with_expected_positive 1 positive_per_id_correct 20
library-specialty.json controls 3 dim_correct 0 per_id_correct_expected 0 with_expected_positive 1 positive_per_id_correct 20
```

Reading: 31 controls in library-*.json (28 + 3). The 35 in results/challenges.json also include the 4 controls of vi-actor-core-native-gap.json, which this script does not count.
Kinds present: positive-control (2, both expect `unverified` on every dimension), wrong answer/citation (4), extras/omission/duplicate/contradiction
(icon-tests only), probe-failure shapes (empty, wrapper-only, truncated, unsupported, failed), absence-of-evidence (3), constant exports (constant-export and constant-keyed-literal-export, in both files).
**0 of 31 controls expect a `correct` correctness or grounding outcome in `expected`.** The only `correct` outcomes appear in the `expected_positive` block of the two positive-control entries (20 per-id outcomes each: 10 correctness + 10 grounding). `regression_self_test` consumes them only with synthetic execution counters (executed=1, scored=1). Those blocks are authored in the same fixture and role family as the scorer, and their key is the inventory key, not an independently derived one. The current-evidence view is `unverified` throughout (no native reference exists).

## Independent derivation

Goal: obtain the expected answer for a claim from the artifact bytes and `docs/perpetua/evaluation.md` alone, never from score.py output or from the existing control's `expected`/`expected_positive`.

1. Open the original artifact `Core/ActorFramework/AF Specialty Messages.lvlib` (commit 371c631c, sha256 83bd1049...87d0, from the read-only environment copy).
2. Parse it as XML (stdlib `xml.etree`, or by eye). Read the `LVVersion` attribute of the root `<Library>`: the file text is `<Library LVVersion="20008000">`. Literal `20008000`; locator `/Library/@LVVersion`.
3. Count `<Property>` children of `<Library>` in document order: 1 NI.Lib.Icon, 2 NI.Lib.SourceVersion, 3 NI.Lib.Version, 4 NI.LV.All.SourceOnly. Literal at `/Library/Property[4]/@Name`: `NI.LV.All.SourceOnly`.
4. evaluation.md (tasks/oracle rows) requires an answer plus a source location in the original, and says the exporter's own output is not a reference. Structure checks without native evidence do not confirm LabVIEW behaviour. So the derived key is a literal-at-location fact only; it must not be stated as what LabVIEW resolves or displays.
5. Compare the derived literals with the inventory (`benchmark/cases/dev/library-specialty.json`) only afterwards, in the reviewer step. Any disagreement is reported, not reconciled by the deriver.

Independence caveat: the author of this plan saw the A0001/A0002 inventory values while measuring, so this session must not be the deriver.

## Proposed control

- Fixture: `benchmark/challenges/library-specialty.json` (3 controls today; one small artifact whose XML literals are checkable by eye).
- New case name (added by a later task, not now): `positive-control-independent-key`.
- Submission: answer claims A0001 and A0002 as the key-bearing items; other required IDs submitted as in the current positive-control; reader channel unchanged.
- Expected keys (to be confirmed cold, not trusted from here):
  - A0001: value `20008000`, citation locator `/Library/@LVVersion`, scheme xml-positional-path.
  - A0002: value `NI.LV.All.SourceOnly`, citation locator `/Library/Property[4]/@Name`.
- Expected outcome for those two items: correctness `correct` and grounding `correct` under the provisional XML key with positive execution counters; current-evidence view `unverified` (no native reference). Do not mark the whole-case dimension `correct`.
- Who derives: a separate benchmark-role session started cold, given only the artifact path, evaluation.md and the claim question text. It must not read score.py, results/challenges.json, the inventory `reference_inventory` values or any existing `expected*` block. It writes its key to a new file before looking at anything else.
- Who reviews: a separate reviewer-role session (not the deriver, not this author) compares the deriver's key with the inventory and the control, and checks that the control fails when the literal or citation is wrong.
- A third task adds the control and regenerates results (score.py/results edits are out of scope here).

## Limits

- Counts cover only `library-*.json`; `vi-actor-core-native-gap.json` was not counted.
- The derived literals are XML text facts. No native reference exists, so `correct` stays conditional on the provisional key and `current_evidence` stays `unverified`.
- A0001/A0002 values above were read from the artifact and the inventory in the same session, so they are candidates for the cold deriver, not a verified key.
- score.py logic was not reviewed (closed scopes #779/#785/#797/#809) and `main()` was not run.
- `expected_positive` blocks were counted from authored fixture bytes, not from a score run.
- No LabVIEW was run. Benchmark readiness: false.
