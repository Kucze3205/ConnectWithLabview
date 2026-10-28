# 0002 Coverage: artifact families, save versions and pylavi decoding

Scope: only the prepared public sources under `$LABVIEW_ENVIRONMENT` (seen as `@environment/`). This report measures and does not fix anything. pylavi was not patched and no reader was written.

## Inputs (pinned)

- pylavi `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75` (Unlicense) and actor-framework `371c631c16155d88f02be11a953e4964d7452fd8` (MIT): `@environment/readiness.json`.
- Fixture `actor-framework/Core/ActorFramework/Actor/Actor Core.vi`, sha256 `135d50e68f002aea9c6a08d0265cc6178b326f1af99353755064c953eaec063c`: `@environment/readiness.json`.

## Method

Script: `docs/research/scripts/coverage/inventory.py`. It is offline, uses only the standard library plus pylavi imported from `$LABVIEW_ENVIRONMENT/pylavi`, and runs under `python3 -I`.

- It walks `$LABVIEW_ENVIRONMENT` (skipping `.git` and `node_modules`) and opens zip containers (`.zip .vip .vipc .vsix .lvlibp`) to look at the LabVIEW members inside them. Zip members are counted as separate `(zip member)` families: `pylavi.file.Resources.load` takes a path on disk, so the script does not run a whole-file pylavi load on zip members.
- A family is named `<extension> <container>`. The container is one of:
  - `RSRC <file_type>`: the magic is `RSRC`.
  - `XML`: the first 64 KiB contain an `LVVersion="…"` attribute.
  - `zip`.
  - `text/other`: the first 8 bytes are recorded as `magic` in the JSON output.
- **Save version (RSRC):** read from the `vers` resource with the lowest id and cross-checked against the 4-byte version prefix of `LVSR`. The script parses the RSRC container itself, so the version does not depend on pylavi. **Save version (XML):** the `LVVersion` attribute.
- **pylavi decoding:** `@environment/pylavi/pylavi/resource_types.py` has no type registry. Its decoders are classes named `Type<fourcc>`: `TypeBDPW TypeDLLP TypeHLPP TypeLPTH TypeLVSR TypePATH TypeRTMP Typevers` (from the script output, `pylavi_decoders`). The script looks each resource up by that name and calls `from_bytes`.
  - `decoded`: `to_bytes()` reproduces the original bytes exactly.
  - `decoded-not-roundtrip`: decoding works but `to_bytes()` differs.
  - `error`: decoding raises an exception.
  - `opaque`: pylavi has no class for the type.
- Whole-file load: `pylavi.file.Resources.load` (`@environment/pylavi/pylavi/file.py`).

Commands:
- `python3 -I docs/research/scripts/coverage/inventory.py`: JSON output, which is the verification command.
- `python3 -I docs/research/scripts/coverage/inventory.py --table`: the Markdown tables below, which are copied from its output on 2026-10-24.

## Families x save versions

Output of `python3 -I docs/research/scripts/coverage/inventory.py --table` (first table). Versions appear as `major.minor.fix<stage><build> (raw hex)`, with stage d/a/b/f.

| Family | Files | Save versions (count) | pylavi load ok/error |
|---|---|---|---|
| .aliases text/other | 2 | no version in header: 2 | n/a |
| .aliases text/other (zip member) | 5 | no version in header: 5 | n/a |
| .ctl RSRC LVCC | 9 | 20.0.0f0 (20008000): 5; 20.0.1f7 (20018007): 4 | 9/0 |
| .ctl RSRC LVCC (zip member) | 7 | 20.0.1f7 (20018007): 7 | n/a |
| .lvclass XML | 48 | 20.0.0f0 (20008000): 48 | n/a |
| .lvclass XML (zip member) | 47 | 13.0.0f0 (13008000): 2; 14.0.0f0 (14008000): 16; 15.0.0b0 (15006000): 5; 15.0.0f0 (15008000): 1; 20.0.0f0 (20008000): 23 | n/a |
| .lvlib XML | 12 | 20.0.0f0 (20008000): 11; 21.0.0f0 (21008000): 1 | n/a |
| .lvlib XML (zip member) | 13 | 14.0.0f0 (14008000): 7; 15.0.0b0 (15006000): 2; 15.0.0f0 (15008000): 1; 20.0.0f0 (20008000): 3 | n/a |
| .lvlibp text/other | 1 | no version in header: 1 | n/a |
| .lvlibp text/other (zip member) | 11 | no version in header: 11 | n/a |
| .lvlps text/other | 1 | no version in header: 1 | n/a |
| .lvlps text/other (zip member) | 5 | no version in header: 5 | n/a |
| .lvproj XML | 5 | 20.0.0f0 (20008000): 5 | n/a |
| .lvproj XML (zip member) | 5 | 14.0.0f0 (14008000): 3; 15.0.0b0 (15006000): 1; 15.0.0f0 (15008000): 1 | n/a |
| .mnu RSRC LMNU | 5 | no version in header: 5 | 5/0 |
| .mnu RSRC LMNU (zip member) | 5 | no version in header: 5 | n/a |
| .vi RSRC LVIN | 432 | 20.0.0f0 (20008000): 266; 20.0.1f0 (20018000): 1; 20.0.1f7 (20018007): 118; 21.0.0?000 (21000000): 1; 21.0.0a0 (21004000): 1; 21.0.0b0 (21006000): 1; 21.0.0d0 (21002000): 1; 21.0.0f0 (21008000): 20; 21.0.1f2 (21018002): 2; 21.0.1f6 (21018006): 9; 23.0.0f0 (23008000): 5; 24.1.1f1 (24118001): 1; 24.3.1f1 (24318001): 1; 26.3.0f0 (26308000): 5 | 432/0 |
| .vi RSRC LVIN (zip member) | 200 | 13.0.0f51 (13008051): 8; 14.0.0f34 (14008034): 16; 14.0.0f36 (14008036): 25; 15.0.0b11 (15006011): 12; 15.0.0f29 (15008029): 4; 16.0.0f10 (16008010): 1; 20.0.1f7 (20018007): 134 | n/a |
| .viancfg text/other | 1 | no version in header: 1 | n/a |
| .vim RSRC LVIN | 1 | 20.0.1f7 (20018007): 1 | 1/0 |
| .vim RSRC LVIN (zip member) | 1 | 20.0.1f7 (20018007): 1 | n/a |
| .vip zip | 1 | no version in header: 1 | n/a |
| .vipb text/other | 3 | no version in header: 3 | n/a |
| .vipc zip | 2 | no version in header: 2 | n/a |

Observations from the same output:
- Every on-disk RSRC file loads in pylavi without error: 432 `.vi`, 9 `.ctl`, 5 `.mnu` and 1 `.vim`.
- `vers` and `LVSR` disagree in some files. In the fixture, `vers` = 20.0.1f7 and `LVSR` = 20.0.0f0. The script records these files in the JSON under `families[*].vers_lvsr_mismatch`, with 4 `.ctl` files and many `.vi` files listed. Which field LabVIEW treats as the save version is an **untested inference**. This report uses `vers`.
- One `.vi` file has stage byte `00` (`21.0.0?000`). The script does not recognise this stage code.
- The five 26.3.0f0 VIs are pylavi's own test files (`@environment/pylavi/tests/reentrancy/26.0/*.vi`), not Actor Framework.

## pylavi decoding per resource type

Source of the decoder set: `@environment/pylavi/pylavi/resource_types.py`. The `Path` and `Version`/`PString` bases come from `@environment/pylavi/pylavi/data_types.py`. In the whole corpus, no resource that pylavi has a class for fails to decode or fails to round-trip: there are no `error` and no `decoded-not-roundtrip` statuses in the `--table` output. `TypePATH`, `TypeDLLP` and `TypeRTMP` exist, but none of the scanned files contains those resource types.

One example file per family. The lists come from the JSON `examples[*].pylavi` field, printed with the one-off `python3 -I -c` command that loads the script's JSON:

| Family | Example file | pylavi decodes | Opaque to pylavi |
|---|---|---|---|
| .vi RSRC LVIN (**fixture**) | `actor-framework/Core/ActorFramework/Actor/Actor Core.vi`: 20.0.1f7, 30 types, `Resources.load` ok | `BDPW`, `LVSR`, `vers` | `BDEx BDHb BDSE CONP CPC2 DTHP FPEx FPHb FPSE FTAB HIST HLPU HLPW LIBN LIbd LIfp LIvi MUID PICC PRT  RTSG STRG TITL VCTP VITS VPDP icl8` |
| .vi RSRC LVIN (zip member) | `actor-framework/Builds/actor_framework_2024_for_2020-2.0.0.23.vip!File Group 0/vi.lib/ActorFramework/tracing/Generate Custom Trace.vi` | `BDPW`, `LVSR`, `vers` | `BDEx BDHb BDSE CONP CPC2 DTHP FPEx FPHb FPSE FTAB HIST HLPU HLPW ICON LIBN LIbd LIfp LIvi MUID RTSG STRG VCTP VITS VPDP icl4 icl8` |
| .vim RSRC LVIN | `actor-framework/Core/ActorFramework/Actor/Casting Utility For Actors.vim` (and the same file inside the .vip) | `BDPW`, `LVSR`, `vers` | `BDEx BDHb BDSE CONP CPC2 DTHP FPEx FPHb FPSE FTAB HIST ICON LIbd LIfp LIvi MUID PICC RTSG STRG VCTP VITS VPDP icl8` |
| .ctl RSRC LVCC | `actor-framework/Core/ActorFramework/Message Dequeuer/Dequeue Priority.ctl` | `LVSR`, `vers` | `BDEx BDHb BDSE CCST CONP CPC2 DFDS DTHP FPEx FPHb FPSE FTAB GCDI GCPR HIST ICON LIBN LIbd LIds LIfp LIvi MUID RTSG TM80 VCTP VITS VPDP icl8` |
| .ctl RSRC LVCC (zip member) | `…2.0.0.23.vip!File Group 0/vi.lib/ActorFramework/tracing/Support/Registration Mode.ctl` | `LVSR`, `vers` | same set as above, without `CPC2`/`GCDI` and with `VICD`, `icl4` |
| .mnu RSRC LMNU | `actor-framework/Core/Menus/Categories/Data Communication/_actorframework_experttools.mnu` | `LPTH` | `CPST FLAG HLPT ICON LST# PLM2 STR# icl4 icl8` |
| .mnu RSRC LMNU (zip member) | `…2.0.0.23.vip!File Group 0/menus/Controls/actorframework_controls.mnu` | `LPTH` | `CPST FLAG ICON PLM2 STR# icl8` |
| .lvclass / .lvlib / .lvproj XML (on disk and zip member) | e.g. `actor-framework/Core/AFDebug/DETT Format/DETT Format.lvclass`, `actor-framework/Core/AFDebug/AF Debug.lvlib`, `actor-framework/Core/AF Debug PPL Build.lvproj` | nothing | the whole file: XML, not RSRC, and pylavi has no XML reader in `resource_types.py` |
| .lvlibp | `actor-framework/Core/builds/AF PPL Build/AF PPL/Actor Framework.lvlibp` | nothing | the whole file: magic `4d5a9000…` (`MZ`), a PE-style container, not RSRC |
| .aliases / .lvlps / .vipb / .viancfg text | e.g. `actor-framework/Core/AF PPL Build.aliases` (`[My Comp…`), `.lvlps` (`[Project…`), `.vipb` (`<VI_Pack…`), `.viancfg` (`<?xml ve…`) | nothing | the whole file: text, outside pylavi's scope |
| .vip / .vipc zip | `actor-framework/Builds/actor_framework_2024_for_2020-2.0.0.23.vip`, `actor-framework/Tooling/deployment/Dependencies.vipc` | nothing directly | LabVIEW members are counted in the `(zip member)` rows |

Other resource types seen in `.vi` files, all opaque (full list in `--table`): `CCST DFDS DLDR DSIM FPTD GCDI GCPR LIds TM80 VICD SCSR BFAL NUID SUID BNID CNST LPIN MNGI HLPT OBSG IPSR BKMK VINS CPMp`. `HLPP` is decoded (`TypeHLPP`) in the one `.vi` and two `.mnu` files that contain it.

## Gaps

These are visible gaps. None of them is an exclusion.

- **Families not present:** the scan found no file with any of these extensions: `.vit`, `.ctt`, `.llb`, `.rtm`, `.uir`, `.xctl`, `.lvtest`, `.lvsc`, `.gbl`, `.lvclass`/`.lvlib` in binary form, or `.lvlibp` in RSRC form. These extensions are listed in `LV_EXTS` in the script but do not appear as families in the output. Templates, LLBs, run-time menus and XControls are therefore unmeasured.
- **Versions not present:**
  - **RSRC:** nothing older than 13.0 (LabVIEW 2013). 16.x has a single VI (16.0.0f10, zip member). No 17.x, 18.x, 19.x, 22.x or 25.x. 23.x has 5 VIs and 24.x has 2. 26.x appears only in pylavi's own test VIs.
  - **Release builds:** most versions come from a single release build each (for example, all 13.0 files are 13.0.0f51 zip members).
  - **XML families:** only 13.0, 14.0, 15.0, 20.0 and 21.0.
  - **Container scope:** Version 13–16 RSRC files exist only inside zip containers (`.vip`/`.zip`). pylavi's whole-file load was not exercised on them; their per-resource decode was.
- **Block diagram not decodable:**
  - **Fixture:** the diagram and front-panel heap resources are all opaque to pylavi: `BDHb` (block diagram heap), `BDEx`, `BDSE` and `LIbd`, plus `FPHb`/`FPEx`/`FPSE`/`LIfp`.
  - **Every family:** these resources are also opaque in every `.vi`, `.vim` and `.ctl` scanned.
  - **What pylavi does decode:** only metadata, namely version, flags and password hash (`LVSR`, `vers`, `BDPW`) plus paths. There is no pylavi decoder in `@environment/pylavi/pylavi/resource_types.py` for the diagram, the connector pane (`CONP`, `CPC2`), types (`VCTP`, `DTHP`) or link info (`LIvi`, `LIBN`).
  - **Untested inference:** these types are probably compressed or encoded heaps. This was not measured.
- **Version semantics:**
  - `vers` and `LVSR` disagree in the files listed in the JSON's `vers_lvsr_mismatch`.
  - One `.vi` has an unknown stage byte `00`.
  - The authoritative meaning of these fields was not established. No native LabVIEW is available to confirm it.
- **Container gaps:**
  - `.lvlibp` files are PE (`MZ`) containers. The scan did not look inside them, so any VIs embedded in packed libraries are uncounted.
  - `.vipc` and `.vip` were only searched for members with LabVIEW extensions.
- **License and dependency limits:**
  - pylavi is under the Unlicense and Actor Framework under MIT (`@environment/readiness.json`).
  - The corpus is one framework plus pylavi's tests, so it is not representative of LabVIEW code in general.
  - No NI-licensed artifacts (vi.lib from an installed LabVIEW) and no private material are present.
  - There is no native LabVIEW runtime, so no parser claim here is checked against LabVIEW itself. Everything in this report is either from the script's own RSRC parser or from pylavi.

## Next decision supported

Any reader work must decode the opaque heap and type resources (`BDHb`/`FPHb`, `VCTP`, `CONP`/`CPC2`, `LIvi`), because pylavi offers nothing beyond metadata for them. To measure whether results generalise beyond the Actor Framework's 20.x/21.x files, the corpus needs more save versions (17–19, 22, 24–25) and the missing families.
