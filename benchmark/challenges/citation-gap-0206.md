# Citation gap (#831): the scorer never resolves a submitted citation in the XML artifact

Measured by reading `benchmark/scripts/score.py` and `benchmark/challenges/check_xml_keys.py` in this session (#885). Nothing was implemented or run. No LabVIEW is available: native N0001/N0002 stay unverified. Line numbers are as read; `check_xml_keys.py` numbers were counted from the full file read, so re-check them with a 3-line margin before editing.

## Current behaviour

`score.py` handles citations only as identity matches against the key. It never opens the artifact, never hashes it, and never evaluates a locator.

- `citation_support(citations, key)` (score.py:67-74): no submitted citations gives `missing`. A key with no `citations` gives `unverified`. Otherwise it gives `correct` only if every submitted citation dict is `in key['citations']` (whole-dict equality: repository, commit, path, sha256, archive chain, locator), else `incorrect`. Its comment (68-69) says existence alone earns no credit.
- `compute` (score.py:125) calls it at score.py:221-223, only when the value comparison already gave `common == 'correct'`. The result goes through `assessment(supports, [])` (34) and fills the `grounding` dimension. The `correctness` dimension never looks at citations.
- `extra_outcome` (score.py:94-122) uses citations in two ways. At score.py:101 it finds the key by matching `locator.expression` against a keyed citation, which is a lookup, not a resolution. At score.py:110 it calls `citation_support` for grounding.
- The reader channel (`observations`) has no citations. It is matched on `scope` against `reference_scope` (the `common` chain around score.py:195).
- Existing citation controls: `regression_self_test` (score.py:283) mutates a locator to `/Library/Property[3]/@Name` (score.py:343, "wrong-locator-a0002") and copies A0001's citations onto another claim (score.py:353, "wrong-citation"). Both are caught only because they differ from the keyed dict.

Consequences (by reading the code, not by running it):
1. A submission that copies the key's citation dict exactly passes grounding without any artifact check. The key is the only authority.
2. The `sha256` inside a citation is compared as a string to the key's. It is never compared to the bytes of the artifact.
3. If the key's own locator or value were wrong, the scorer could not tell. Only `check_xml_keys.py` guards that, and only for key files.
4. `answer_record_contract` in `benchmark/cases/dev/library-specialty.json` describes `citations` as strings ("original hash/path/member chain and exact original locator"). The fixtures and the key use dicts. The submitted shape is not pinned in one place.

## Reuse

`check_xml_keys.py` is a CLI over key files, but two functions can be reused.

- `resolve(root, locator)` (check_xml_keys.py:35-60): takes a parsed `ElementTree` root and a locator `/Root/Child[n]/.../(@Attr|text())`. It returns the string, or raises `ValueError` for root mismatch, bad step, missing element, missing attribute, a leaf-less locator or an unsupported leaf. It is pure and standard-library only, so it works for submitted locators unchanged.
- Hash gate: in `main` (check_xml_keys.py:74-78) the artifact bytes are hashed with `hashlib.sha256` and parsed with `ET.fromstring`. The comparison against the key's `artifact_sha256` is at check_xml_keys.py:92-93. This is inline, so a scorer needs its own 3-line equivalent, or a function extracted from here.
- The `(line N)` suffix strip (check_xml_keys.py:30) is key-file hygiene. A submitted locator should not get that tolerance.
- Not reusable as-is: `main` and `load_claims` (16-32) assume key files and `argparse`, and `sys.exit` is in `main`.
- Quirks to keep or decide on: `text()` returns `node.text` without stripping (59), which is fine for exact literals. A locator with a single segment raises. Predicates other than `[n]` are unsupported. Locators and values are compared by exact string equality.
- Import: `score.py` is run as a script from `benchmark/scripts/` and the checker sits in `benchmark/challenges/`. Importing it needs `sys.path` or `importlib` handling. Python is run with `-I` (#785), which drops the script directory from `sys.path`, so an explicit path-based import is required.

Recommendation on reuse: do not edit `check_xml_keys.py`. Its sha256 `63f01c0e...` is pinned in the fixture (`benchmark/cases/dev/library-specialty.json` `oracle.independent_checker.identity.checker_sha256`) and the keys were agreed against it (#873, #878). Copy the roughly 25 lines of `resolve` into a new module instead.

## Design

**Input shape.** A submitted claim keeps its current form: `{claim_id, answer, citations: [ {repository, commit, path, sha256, archive_member_chain, locator: {scheme, expression}} ], conditions}`. The check needs no new field. The `answer` string is the "answered literal". Only citations with `scheme == "xml-positional-path"` are checked. Other schemes are `unverified`.

**Artifact access.** The scorer needs the original bytes for a citation's `path`. Source: the pinned identity manifest `benchmark/sources.json` (`identity_manifest_sha256` is in the fixture) plus the prepared read-only sources (`LABVIEW_ENVIRONMENT`). The exact path mapping under the environment was not read in this session. The implementer must confirm it before coding.

**Pass/fail rule.** Per submitted citation C of claim X with answer literal V:
1. Look up the artifact for C.path and C.commit through the manifest. If unavailable, the result is `unverified` (never `correct`).
2. If `sha256(bytes) != C.sha256`, or `C.sha256 != fixture.artifact.sha256`, the result is `incorrect` (wrong artifact).
3. Parse the bytes and call `resolve(root, C.locator.expression)`. On `ValueError` the result is `incorrect` (locator does not resolve).
4. If the resolved text `!= V` (exact string equality), the result is `incorrect`.
5. Otherwise `correct`. Existing key-identity matching stays as an additional gate. The resolution check only adds fail paths and never upgrades a result.

All citations of a claim must pass. The outcome feeds `assessment` as today.

**Where it plugs in.**
- New helper `citation_resolves(citation, literal, fixture_artifact, load_bytes)` next to `citation_support` (score.py:67).
- Call it inside the grounding branch at score.py:221-223 and in `extra_outcome` at score.py:110, combining its result with `citation_support`: any `incorrect` wins, `unverified` blocks `correct`.
- `compute` (125) receives no artifact today. It needs a bytes loader, either a new argument or one taken from `source`. `generate` (371) and `regression_self_test` (283) are the callers to update. The loader must be injectable so that controls can supply bytes without the real sources.
- Keep it deterministic: no network, no clock.

**Pin maps that would need re-pinning if implemented.** Pin maps only: `benchmark/writing/input-pins.json` `protected_inputs_sha256` and `benchmark/preparation.json`.

| File changed | `input-pins.json` entry | `preparation.json` entry |
|---|---|---|
| `benchmark/scripts/score.py` (sha `21329d0d...`) | `"benchmark/scripts/score.py"` (line 57) | `milestones.challenges` score.py entry |
| `benchmark/results/challenges.json` (regenerated by `score.py`, sha `a3466ad8...`) | `"benchmark/results/challenges.json"` (line 46) | `milestones.challenges` challenges.json entry |
| `benchmark/challenges/library-specialty.json` (only if controls are added to the fixture, sha `42480b8c...`) | `"benchmark/challenges/library-specialty.json"` (line 28) | `milestones.challenges`, preparation.json:67 |
| `benchmark/cases/dev/library-specialty.json` (only if the contract text or `answer_record_contract` is changed, sha `1f1bc985...`) | line 21 | `milestones.oracle` (preparation.json:139) and `milestones.tasks` (preparation.json:293) |
| `benchmark/preparation-status.json` (only if it mirrors the changed hashes) | not checked | listed in every milestone |

A new helper module under `benchmark/scripts/` would be a new file, so it needs new entries in both maps. Putting the code inside `score.py` avoids that. `check_xml_keys.py` must stay unchanged for the reason given in `## Reuse`. Whether `check_xml_keys.py` itself is in `input-pins.json` was not checked.

The same change would apply to the other two fixtures (`library-icon-tests`, `vi-actor-core-native-gap`) when they are scored, and the table would then also list their fixture files and `benchmark/cases/dev` files.

## Controls

Written before any implementation. Each uses the A0002 claim of `library-specialty` (`/Library/Property[4]/@Name`, value `NI.LV.All.SourceOnly`, artifact sha256 `83bd1049...87d0`) unless stated. Expected outcome is the new `grounding` outcome for that claim, with the correct literal answered.

1. **Correct citation.** Input: answer `NI.LV.All.SourceOnly`; citation with the real path, commit, sha256 `83bd1049...87d0`, locator `/Library/Property[4]/@Name`; the real artifact bytes. Expected: `correct`. Reason: hash matches, locator resolves, text equals the literal.
2. **Wrong locator.** Input: same, but locator `/Library/Property[3]/@Name` (the mutation already at score.py:343). Expected: `incorrect`. Reason: the locator resolves to a different property (or fails), so the text differs from the literal. Today this is only caught by identity against the key.
3. **Right locator, wrong-hash artifact.** Input: locator `/Library/Property[4]/@Name`, but the supplied bytes are a different file or a modified copy, with the citation's `sha256` set to the hash of those bytes, or the citation's `sha256` altered to a wrong value over the right bytes. Expected: `incorrect`. Reason: the hash does not equal the fixture's `artifact.sha256`, so a resolving locator proves nothing about the pinned artifact.
4. **Self-consistent key but wrong locator (key corruption).** Input: a key whose citation is also edited to `/Library/Property[3]/@Name` and a submission that copies it. Expected: `incorrect`. Reason: today `citation_support` returns `correct` here, because identity matches the key. The new rule fails it because the text at the locator does not equal the literal. This shows the gain over the current scorer.
5. **Unresolvable locator.** Input: `/Library/NoSuch[1]/@Name`. Expected: `incorrect`. Reason: `resolve` raises `ValueError`.
6. **Artifact not available.** Input: correct citation, loader returns nothing. Expected: `unverified`, never `correct`. Reason: absence of evidence earns no credit (evaluation.md EV:78 and the "no key, no credit" rule in the challenges row).
7. **Wrong literal, right citation.** Input: answer `Wrong`, correct citation. Expected: grounding `incorrect` and correctness `incorrect` (already the case through the value comparison). Reason: pins that the new check does not turn a wrong answer into a pass.
8. **Constant export.** Existing control "constant-keyed-literal-export" must keep its expected outcomes (`incorrect` correctness and grounding, fidelity `unverified`).

Controls 1-3 are the required three. Control 4 is the one that no current control covers. All existing controls in `benchmark/results/challenges.json` must be unchanged except where a control's citation locator was inconsistent with the artifact, which would itself be a finding.

## Recommendation

Order one implementation task and one separate review, in that order.

1. Implementation (benchmark role, `benchmark/**`): add `citation_resolves` inside `score.py` (copying `resolve` from check_xml_keys.py:35-60; do not edit or import-by-path `check_xml_keys.py`), wire it at score.py:110 and score.py:221-223, add an injectable artifact loader to `compute`/`generate`/`regression_self_test`, add controls 1-7 above to `regression_self_test` (or to fixtures), regenerate `benchmark/results/challenges.json`, and re-pin `score.py` and `results/challenges.json` in both pin maps in the same change. First step: confirm how the artifact bytes are reached from `benchmark/sources.json` and `LABVIEW_ENVIRONMENT` (not read here).
2. The evaluator verifier does not cover this. Request a separate method-review session, since `score.py` is documented as unreviewed.
3. Decide in the same task whether the submitted citation shape in `answer_record_contract` (strings) is rewritten to the dict form. That edit changes a fixture pinned in three places.

Limits: this check proves only that the cited XML text equals the answered literal in the pinned original. It says nothing about native meaning, effective scope or resolved membership (N0001/N0002), and it does not measure reader fidelity.
