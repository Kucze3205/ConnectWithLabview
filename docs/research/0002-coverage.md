# 0002 Coverage: artifact families, save versions and pylavi decoding

Status: **partial (first pass)**. The tables below are output from the script. Sections still being written are marked TODO.

## Inputs (pinned)

- Prepared sources, read-only: `$LABVIEW_ENVIRONMENT` (= `/resources/environment`, seen as `@environment/`).
- pylavi `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75` (Unlicense), actor-framework `371c631c16155d88f02be11a953e4964d7452fd8` (MIT): `@environment/readiness.json`.
- Fixture `Core/ActorFramework/Actor/Actor Core.vi`, sha256 `135d50e68f002aea9c6a08d0265cc6178b326f1af99353755064c953eaec063c`: `@environment/readiness.json`.

## Method

Script: `docs/research/scripts/coverage/inventory.py`.

- Walks `$LABVIEW_ENVIRONMENT` (skips `.git`, `node_modules`) and opens zip containers (`.zip .vip .vipc .vsix .lvlibp`) to look at LabVIEW members inside them.
- Families are named `<extension> <container>`: `RSRC <file_type>` for binary resource files (magic `RSRC`), `XML` when an `LVVersion="…"` attribute is present, `zip`, or `text/other`.
- The save version of an RSRC file comes from its `vers` resource with the lowest id. It is cross-checked against the version prefix of `LVSR`. The RSRC container is parsed by the script, not by pylavi, so the version does not depend on pylavi.
- pylavi decoding: `pylavi/resource_types.py` has no type registry. Its decoders are classes named `Type<fourcc>`. The script looks each resource up by that name, calls `from_bytes`, and records `decoded` only when `to_bytes()` round-trips byte-identically. Whole-file load uses `pylavi.file.Resources.load` (`@environment/pylavi/pylavi/file.py`).

Commands: `python3 -I docs/research/scripts/coverage/inventory.py` (JSON) and `python3 -I docs/research/scripts/coverage/inventory.py --table` (Markdown below).

## Families x save versions (first pass)

TODO: regenerate after the next script revision. Known issue: counts for `.vi`/`.ctl` include zip-nested members, which pylavi does not load.

## pylavi decoding per resource type

TODO.

## Gaps

TODO.
