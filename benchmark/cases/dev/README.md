# Public development case inventories

These 11 specifications are preparation evidence for `tasks` and public development keys for `oracle`, pending separate review. None can be withheld or treated as unseen, including copies, variants or public history. No reader execution, native semantic validation, scoring, quality threshold or readiness claim is supplied.

| Family | Cases | XML declaration slots | Native-required slots | Fixed slots per dimension |
|---|---:|---:|---:|---:|
| `.lvproj` | 3 | 528 | 6 | 534 |
| `.lvclass` | 3 | 339 | 6 | 345 |
| `.lvlib` | 4 | 186 | 8 | 194 |
| `.vi` | 1 | 0 | 3 | 3 |
| Total | 11 | 1053 | 23 | 1076 |

Every case separately freezes answer-correctness and source-grounding IDs and reader-observation IDs. Equal counts do not merge these dimensions. All 11 are planned; zero have been attempted, executed or scored. Unavailable references remain in every denominator. Extras, omissions, duplicates and contradictions follow [the protocol](../../protocol.md#tasks) and cannot change those denominators.

## Reproduce and inspect

From the repository root, with the prepared read-only cache exposed as `LABVIEW_ENVIRONMENT`:

```sh
python3 -I benchmark/scripts/dev_cases.py
python3 -I benchmark/scripts/dev_cases.py --check
python3 -I policy/evaluator/evaluate.py --check
```

The stdlib generator verifies source/coverage evidence pins, prepared repository commits, original/container hashes and archive-member identities before extracting facts directly from original XML. It neither imports nor executes prepared source code. Generation writes missing files only after preflighting every output; existing differences fail without replacement. `--check` requires all case files, compares bytes, and never writes. Intentional inventory revisions require review of generator and case changes together, rather than deleting a mismatching inventory to accept input drift.

Each case embeds its reference inventory, so the same JSON files are evidence for `tasks` and `oracle`. XML positional locators use one-based sibling indices per element tag, as in `/Project/Item[1]/Item[2]/@URL`. `text()` means the XML-parsed element text, preserving whitespace and decoded XML entities. The suffix `/text()/utf8-sha256` fingerprints that parsed text encoded as UTF-8; it does not decode LabVIEW binary encodings. Ordinary values remain literal strings, including booleans and numeric scope codes. Item attributes are atomic claims; selected property names, types and values have separate IDs.

Project cases include all declared Item attributes and selected build/source/destination properties, separating Dependencies and Build ancestry. Class/library cases preserve membership, friends, containing-library declarations and literal scope/method flags. Encoded genealogy and parent-link payloads are fingerprinted only: direct-parent identities, inheritance and effective scope/dispatch remain unverified. Missing scope properties do not imply a default. XML extraction is author preparation; every claim still awaits independent original-source checking. Reading fidelity also requires the unavailable native reference alignment.

## Provenance, lineage and limits

All cases use NI Actor Framework commit `371c631c16155d88f02be11a953e4964d7452fd8`, with artifact hashes matching [sources.json](../../sources.json) or [coverage.json](../../coverage.json). Two cases read archive members without extracting them: `PPL Test.zip` member 2 and `Test Harness Master.zip` member 45. Their case records pin container and member hashes and member paths. The original XML save-version declarations represented are `14008000` (one class), `15008000` (one project), `20008000` (seven XML cases) and `21008000` (one library); the additional VI has source-inventory LVSR `20008000`. These fields establish no native compatibility. The VI coverage inventory also records a differing `vers` value (`20018007`); it is not substituted for the source inventory's LVSR field.

Every case uses the conservative lineage group `public-ni-actor-framework-all-projects-copies-variants`; a later split must keep all related NI Actor Framework projects, archives and variants together. This grouping prevents cross-split copies by overgrouping the entire repository; it does not establish a withheld boundary or complete duplicate analysis for other sources.

Native references are unavailable for **every case**: resolved project dependencies and build effects/results; class inheritance, effective scope and dispatch; resolved library membership/effective scope; and the VI connector/types, diagrams/dataflow and controlled behavior. The VI oracle is explicitly `unavailable`, with three null reference slots and no inferred semantic answer. The concrete reader adapter, native object/capture maps, input/state/target fixtures and independent checker records remain missing. Probe specifications freeze observation IDs and ordering, prohibit adaptive selection and truncation, and require a reviewed concrete adapter before exposure; no runnable reader probe is claimed.

Other families, unrepresented save versions, native reading versions, modules, targets/hardware, licenses, dependencies and protected/removed diagrams remain coverage gaps. Consult [coverage.md](../../coverage.md) for the broader inventory. No fallback or scope change is selected.

## Review next

Request a separate cross-family reviewer session against the pinned tree and prepared originals. Resolve every XML claim and citation, inspect omitted scope and encoded inheritance limitations, check archive lineage and fixed denominators, and record claim-level agreement or disagreement before treating any provisional key as established. Native claims require bounded native jobs with hashed original-object/capture evidence and independent checking. Executable scoring requires a Policymaker-ordered evaluator change and its separate verifier; method review and owner acceptance remain prerequisites for product implementation.
