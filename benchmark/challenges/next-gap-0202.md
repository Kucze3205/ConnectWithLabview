# Next-gap measurement (next-gap-0202)

Measurement only. No repository file other than this one was changed. No LabVIEW behaviour is claimed. Benchmark readiness stays false.
Export check: `.session/exports/manifest.json` lists one result (#866 report, downloaded). The #866 verdict is **CLEAR**: 62 of 62 `protected_inputs_sha256` pins match disk after #865 (f8670d5, one file changed). The positive-control pin thread is closed.
Not re-surveyed, cited: `gap-0160.md` (challenges row) and `scorer-probe-0164.md` (scorer behaviour).

## Gaps

Line numbers refer to `docs/perpetua/evaluation.md` (EV) unless stated.

| Gap | Status | EV line | Repository evidence |
|---|---|---|---|
| challenges row | PARTIAL | EV:69 (row), EV:61-69 (table) | `benchmark/challenges/gap-0160.md:5-28`: all five control kinds partial. `scorer-probe-0164.md:11,17,23,29` deny credit for four kinds. `scorer-probe-0164.md:34`: zero execution is not handled. `README.md:14`: positive controls stay unverified. `README.md:24`: the diagram-difference control is absent. Controls are author-written synthetic inputs (`README.md:6`). |
| dependency / native keys | OPEN | EV:65 (oracle: LabVIEW-derived answers, no exporter self-reference), EV:63 (sources: dependencies) | `README.md:8`: two unavailable native IDs per library, three per VI, all null. `README.md:8`: no complete positive control can earn `correct`. `protocol.md:120-121`: native jobs and environment strata are listed as missing resources. |
| restricted split / allocation / isolation | OPEN | EV:66 (split), EV:12 (owner gate) | `protocol.md:71-75`: restricted cases, custodian and an executed access-boundary test are required; `protocol.md:119` lists the restricted store as a missing resource. `README.md:30`: public inputs are unsuitable as withheld evidence. Public-side split scripts exist (`benchmark/scripts/split_allocate.py`, `split_boundary.py`); I did not read them or `benchmark/split/`. No executed boundary evidence was found in the files I read. |
| reader / probes / scorer integration | PARTIAL | EV:78 (separate fidelity, correctness, grounding), EV:40 (`benchmark_executed: false`) | `benchmark/scripts/score.py:414` (`main`) exists, but `scorer-probe-0164.md:3,5` shows it runs only on synthetic controls (33 of 33, planned 1, executed 0). `README.md:6`: the concrete reader adapter is unavailable and there are zero reader attempts. `scorer-probe-0164.md:54`: no fixture shows credit awarded. The scorer never checks citations against the XML artifact (#831 carry). `protocol.md:83-90` requires fresh-session runs; none exist. |
| independent whole-method review + owner acceptance | OPEN | EV:12 (gate.kind owner), EV:59 (independent verifier, then owner), EV:86-92 (independent change control) | `protocol.md:125` lists the independent reviewer and key checker as a missing resource. `scorer-probe-0164.md:50`: the 33/33 match is not evidence, and `independently_reviewed` is false for the results. `goal/gate.yml` is declared absent at EV:12-20. Only pin and preparation reviews (#866 and earlier) exist, not a whole-method review. |
| sources / tasks / oracle(XML) / coverage / baseline rows | NOT RE-MEASURED | EV:63-68 | Out of this task's read budget. The #820 and #763 measurements closed them. The row status here is unknown, not CLOSED. |

No row is CLOSED.

## XML key confirmation

Status: **PARTIAL**. Two of the ten XML literals are independently confirmed. Eight are not.

Covered, with evidence:
- `benchmark/challenges/positive-control-key-0191.json` (keys `artifact_path`, `artifact_sha256`, `claims`) holds the cold derivation of A0001 (`20008000`, `/Library/@LVVersion`, line 2) and A0002 (`NI.LV.All.SourceOnly`, `/Library/Property[4]/@Name`, line 6).
- This session re-read the artifact in the read-only environment. Its sha256 is `83bd1049...87d0`, equal to `artifact_sha256` and to the fixture `source.artifact.sha256`. Line 2 is `<Library LVVersion="20008000">`. Line 6 is the fourth `<Property>`, `Name="NI.LV.All.SourceOnly"`. The key matches the bytes.
- The fixture `library-specialty.json` carries the same two literals and scopes (lines 13 and 24, `reference_scope`). The task statement records the literal/locator/hash comparison as #828 F1. I did not re-read it, because history is outside the budget. This session saw the key first, so it is not an independent confirmation.

Not covered, and the exact missing check:
- Targets: the remaining eight XML IDs of both inventories (A0003 to A0010 in `benchmark/cases/dev/library-specialty.json`; the matching IDs in `library-icon-tests`). The key file has only two claims, and `README.md:28` still asks for all provisional XML expectations to be checked.
- Inputs: the artifact bytes (sha256 above), the claim question text for each ID, and `docs/perpetua/evaluation.md`.
- Who must not have seen the key: the deriver must not read `positive-control-key-0191.json`, the inventory `reference_inventory` values, any `expected*` block, `score.py` or `benchmark/results/**`. This session and the 0189 author have seen the values, so neither may derive.
- Output: a new JSON file with, for each of the eight IDs, `value`, `locator` (XPath-positional, 1-based line) and `derivation`, plus the artifact sha256. The file is written before any comparison.
- Expected result of the comparison, done by a separate reviewer: all eight literals are byte-equal to the text at the locator in the artifact, and equal to the inventory literal and locator. Any difference is reported, not reconciled.
- Limit: this confirms XML text facts only. It does not confirm what LabVIEW resolves, and it does not close the #831 gap (citations are never checked against the XML artifact by the scorer).

## Recommendation

**Task: cold derivation of the eight missing XML keys (A0003 to A0010), plus a stdlib checker.** It needs no LabVIEW, owner material or product code. It needs only the public artifact in the read-only environment.

- Step 1: a cold benchmark-role session writes `benchmark/challenges/positive-control-key-<id>.json` in the shape of the 0191 key, without reading the forbidden files above.
- Step 2: a separate task writes `benchmark/challenges/check_xml_keys.py`, a stdlib script that parses the artifact and fails unless every key file's value is the text at its locator and its sha256 matches.
- Expected gain: the XML independent-key gap goes from 2 of 10 to 10 of 10 confirmed. The README "Next" item (`README.md:28`) can then be updated. The positive control's conditional XML key becomes independently confirmed for all XML IDs. The remaining blocker is then only native evidence and the scorer's citation check (#831), so the next shaper does not need to survey again.
- Verification command, to be written in step 2:
  `python3 -B -I benchmark/challenges/check_xml_keys.py --artifact "$LABVIEW_ENVIRONMENT/actor-framework/Core/ActorFramework/AF Specialty Messages.lvlib" benchmark/challenges/positive-control-key-0191.json benchmark/challenges/positive-control-key-<id>.json`
  It must print `xml keys: 10/10 OK` and exit 0, and it must exit 1 when one literal is altered. Check `git status --porcelain` for `__pycache__` afterwards (#785).
