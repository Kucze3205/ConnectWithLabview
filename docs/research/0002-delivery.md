# 0002 Delivery options and all-versions vs 2024-only effort

Task: issue #49 (`delivery`). Role: researcher. Branch `task/49`.

## Statement of scope

This report compares four delivery forms that would let AI agents read LabVIEW artifacts like ordinary code: a CLI text export, a Python library, an MCP server, and a committed text mirror. It also estimates the effort of supporting all LabVIEW versions against a LabVIEW 2024-only fallback.

**This report makes no choice for the owner.** It does not pick a delivery form and it does not choose the 2024 fallback or reject it. Per `journal/0001.md` `## State`, that decision belongs to the owner, through a request, after this estimate. Where the text says "would", it describes a consequence, not a recommendation.

## Sources and evidence classes

Prepared sources (`@environment/readiness.json`):

- pylavi commit `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75`, Unlicense.
- actor-framework commit `371c631c16155d88f02be11a953e4964d7452fd8`, MIT.
- Fixture `Core/ActorFramework/Actor/Actor Core.vi`, sha256 `135d50e68f002aea9c6a08d0265cc6178b326f1af99353755064c953eaec063c`, 30 resource types.
- Project `Core/Actor Framework Core.lvproj`, `project_lvversion` `20008000`.
- `labview_ide: not_checked`, `model_access: not_checked`, `semantic_reading: not_measured`.

Evidence classes used below:

- **[parser]**: a fact read from the pylavi source code. It shows what pylavi does, not what LabVIEW does.
- **[artifact]**: a fact observed in an original LabVIEW file from the prepared sources, produced by the scripts below.
- **[unverified]**: an inference or assumption that has not been tested. Each one has a matching entry (`M1`…) in `## Open measurements`.

Reproducible measurement scripts (read-only, offline, prepared pylavi tree only):

- `docs/research/scripts/delivery/versions.py`: counts file extensions, RSRC files loaded/failed by pylavi, `vers` versions, XML `LVVersion` values, resource type frequency.
- `docs/research/scripts/delivery/types_by_version.py`: groups resource types and `LVSR` flag-block sizes by saved major.minor version.

Run as `python3 -I docs/research/scripts/delivery/<script>.py /resources/environment`.

### Corpus facts used throughout [artifact]

From `versions.py` and `types_by_version.py` over `@environment/actor-framework/`:

| Fact | Value |
|---|---|
| RSRC files (magic `RSRC` at offset 0) | 420: 405 `.vi`, 9 `.ctl`, 5 `.mnu`, 1 `.vim` |
| Loaded by `pylavi.file.Resources.load` | 420 of 420, 0 failures |
| RSRC file types | `LVIN` 406, `LVCC` 9, `LMNU` 5 |
| Files with a `vers` resource | 415 (the 5 `.mnu` files have none) |
| Saved version (`vers`, major.minor) | 20.0: 395, 21.0: 18, 24.1: 1, 24.3: 1 |
| XML files with `LVVersion` | `.lvclass` 48 (`20008000`), `.lvlib` 11 (`20008000`) + 1 (`21008000`), `.lvproj` 5 (`20008000`) |
| Other LabVIEW-related files, not RSRC at offset 0 | `.lvlibp` 1, `.lvlps` 1, `.vipb` 3, `.vipc` 2, `.vip` 1 |
| `LVSR` flag block size | 156 bytes in every group 20.0, 21.0, 24.1, 24.3 |
| `LVSR.version` equals `vers.version` | 278 files yes, 137 files no |
| Types present only in the 20.0 group | `HLPU`, `HLPW`, `MNGI`, `TITL`, `VINS` |

Only 2 of 415 versioned files were saved by LabVIEW 2024 (`actor-framework/Tooling/Post Build Icon Editor PPL.vi` 24.1, `actor-framework/Tooling/VIP_Post-Install Custom Action.vi` 24.3). No file in the corpus was saved before LabVIEW 2020. The corpus cannot measure any format older than 2020.

### What pylavi reads and does not read [parser]

- Container layer: header, second header, metadata header, type list, resource list, names, raw resource bytes (`@environment/pylavi/pylavi/file.py`, `Resources.load`).
- Decoded resource types: `vers` (`Typevers`), `LVSR` flags (`TypeLVSR`), `BDPW` password hashes (`TypeBDPW`), path resources `PATH`, `DLLP`, `HLPP`, `RTMP`, `LPTH` (`@environment/pylavi/pylavi/resource_types.py`).
- Not decoded: everything else, including the front panel and block diagram heaps (`FPHb`, `BDHb`), type descriptors (`VCTP`), connector pane (`CONP`, `CPC2`), link/dependency info (`LIvi`, `LIbd`, `LIfp`, `LIds`), data space (`DFDS`). pylavi returns these as raw bytes from `Resources.get_resource`.

So pylavi gives an agent file metadata (version, flags, password state, paths, resource inventory), not code. Showing a block diagram as readable text needs a new decoder for at least `BDHb`, `VCTP` and the `LI*` link resources. Whether that decoder is feasible offline is `semantic_reading: not_measured` [unverified, M1].

## Option: CLI text export

How an agent uses it: the agent runs a command such as `lvtext dump "Actor Core.vi"` through its shell tool and reads stdout (text or JSON). It can pipe output to `grep`/`diff`. Every read is a process launch; the agent must know the command exists (documented in `CONTEXT.md` or a skill).

Runtime needs: a Python 3 interpreter plus the exporter package (pylavi is pure Python, standard library only: `struct`, `enum`, `re`, `hashlib` in `@environment/pylavi/pylavi/data_types.py` and `resource_types.py`) [parser]. No LabVIEW install. Shell access for the agent.

Offline and licensing: fully offline. pylavi is Unlicense (public domain), so it can be vendored or forked without notice obligations. actor-framework fixtures are MIT; committing them as test data needs the MIT notice kept. No NI licence needed while the tool parses files itself. If a variant used the LabVIEW IDE to export (for example VI Server scripting), it would need a licensed LabVIEW install on the machine that runs the export; `labview_ide: not_checked` [unverified, M6].

Artifact families it can serve: every family the core decoder supports. Today, with pylavi: RSRC containers `.vi`, `.ctl`, `.vim`, `.mnu` at metadata level (420/420 loaded) [artifact]; pylavi also lists `.vit`, `.ctt`, `.llb`, `.uir`, `.lsb`, `.rtexe`, `.gbl`, `.glb` in `Resources.EXTENSIONS` (`file.py`), but the corpus has none of them [unverified, M4]. XML families `.lvproj`, `.lvclass`, `.lvlib` are already text; the CLI would only normalize them. `.lvlibp`, `.lvlps`, `.vip*` are not RSRC at offset 0 in this corpus and pylavi does not read them [artifact].

## Option: Python library

How an agent uses it: the agent writes and runs short Python (`from lvtext import load; load(p).diagram()`), or another tool (CLI, MCP server, mirror generator) imports it. This is the shape pylavi already has (`Resources.load`, `get_resource`, `Typevers().from_bytes`).

Runtime needs: Python 3 and the package on `sys.path` or installed. The agent needs a code-execution tool and must know the API, which costs more context per task than a single CLI command.

Offline and licensing: same as the CLI (offline, Unlicense base, MIT fixtures, no NI licence for a pure parser).

Artifact families it can serve: same as the CLI; the library is the shared core. The other three options are wrappers around it. Its effort is the decoder effort in `## Effort: all versions vs 2024-only`; the wrappers add small, fixed costs.

## Option: MCP server

How an agent uses it: an MCP client (the agent host) starts the server, usually over stdio, and the agent calls typed tools such as `list_resources(path)`, `read_vi(path, section)`, `find_callers(vi)`. The results come back as tool output; the agent needs no shell and no knowledge of the API beyond the tool descriptions.

Runtime needs: the Python library, an MCP SDK or a hand-written JSON-RPC stdio loop, and an agent host that is configured to start MCP servers. Whether the agent hosts used in this loop can attach an MCP server is `model_access: not_checked` [unverified, M7].

Offline and licensing: a stdio server runs offline. No extra licence beyond the library's. A remote (HTTP) MCP server would send artifact content off the machine; that is a separate publishing decision for the owner.

Artifact families it can serve: same as the library. It can add cross-file tools (dependency graph from `LI*` resources, project tree from `.lvproj`) that a per-file CLI returns less naturally; those tools still depend on decoding `LI*` [unverified, M1].

## Option: committed text mirror

How an agent uses it: a generator writes a text file next to each binary (for example `Actor Core.vi.txt`) or in a mirror tree, and commits it. The agent uses ordinary `Read`, `Grep`, `Glob`, `git diff`, and `git log` with no special tool. Review tools and humans see text diffs too.

Runtime needs: none at read time. At write time: the generator (the library + CLI) in a pre-commit hook or a CI job, plus a check that fails when a binary changed and its mirror did not.

Offline and licensing: offline. The mirror text is derived from the artifacts, so it carries the artifact licence (MIT for actor-framework). Committing it increases repo size: one text file per RSRC file (420 here) [artifact count; size unverified, M8].

Artifact families it can serve: same as the library, at the moment the mirror was generated. Constraints: a stale mirror misleads the agent if the hook or CI check is skipped; merge conflicts appear in both the binary and its mirror; the mirror is read-only (editing the text does not change the VI).

## Effort: all versions vs 2024-only

### Definitions and assumptions

- "2024-only" means: the tool supports files whose `vers` major is 24 (LabVIEW 2024 Q1/Q3 and patches) and rejects or warns on others. It does **not** mean "requires the LabVIEW 2024 IDE"; an IDE-based variant is listed separately in the limits section.
- "All versions" means: files saved by every LabVIEW release that still produces RSRC files, assumed here as LabVIEW 8.0 through 2025 [unverified range, M3].
- Unit: engineer-days for one Python developer, no LabVIEW IDE available (`labview_ide: not_checked`), working from pylavi and public files only.
- Scope of "read like code": metadata (version, flags, resource inventory, password state, paths), connector pane and type descriptors, dependency links, and a text rendering of front panel and block diagram objects. Heap decoding feasibility is not measured (`semantic_reading: not_measured`); every range that includes heap decoding is therefore an assumption [unverified, M1].
- Ranges are wide on purpose. They do not include the owner's review time.

### Estimate per component

| Component | 2024-only | All versions | Main driver of the difference |
|---|---|---|---|
| Container read (RSRC headers, resource list) | 0.5–2 d | 1–4 d | pylavi asserts `format_version == 3` for every file (`Header.VERSION`, `Header.validate` in `@environment/pylavi/pylavi/file.py`) [parser]; older files may use other container versions [unverified, M2] |
| Metadata decoders (`vers`, `LVSR`, `BDPW`, paths) | 1–3 d | 3–8 d | `LVSR` flag offsets are fixed constants and `breakpoint_count` returns `None` when the flag block is short (`TypeLVSR.__get_flag_set`, `@environment/pylavi/pylavi/resource_types.py`) [parser], so block size is expected to vary; observed 156 bytes for 20.0–24.3 [artifact]; older sizes [unverified, M2] |
| Path decoding | 0.5–1 d | 1–3 d | pylavi knows `PTH0`, `PTH1`, `PTH2`; `PTH2` names are UTF-8, others ASCII-escaped (`Path`, `@environment/pylavi/pylavi/data_types.py`) [parser]; which versions write which format [unverified, M5] |
| Type descriptors and connector pane (`VCTP`, `CONP`, `CPC2`) | 5–15 d | 15–40 d | not decoded by pylavi [parser]; per-version layout changes [unverified, M2] |
| Link / dependency info (`LI*`, `LIBN`) | 3–10 d | 8–25 d | not decoded by pylavi [parser]; per-version layout [unverified, M2] |
| Front panel / block diagram heaps (`FPHb`, `BDHb`) to text | 20–60 d | 50–150 d | not decoded by pylavi [parser]; heap resource names `FPHb`/`BDHb` are present in all observed groups 20.0–24.3 [artifact]; older heap formats and object class tables [unverified, M1, M2] |
| XML families (`.lvproj`, `.lvclass`, `.lvlib`) normalization | 1–3 d | 1–4 d | already text; `LVVersion` is a hex-like version string (`20008000`, `21008000`) [artifact]; schema drift by version [unverified, M9] |
| Fixtures and regression suite | 2–5 d | 10–30 d | the corpus has only 2 files saved by 2024 and none before 2020 [artifact]; all-versions needs files from each release, and with no IDE they must be found in public repositories [unverified, M3] |
| **Core subtotal** | **33–99 d** | **89–264 d** | |

Wrapper cost on top of the core (same for both variants, because wrappers do not depend on file versions):

| Delivery form | Added effort | Notes |
|---|---|---|
| Python library | 0 d (it is the core) + 1–2 d packaging | |
| CLI text export | 1–3 d | argument parsing, text/JSON output, exit codes |
| MCP server | 2–5 d | tool schema, stdio loop, host configuration docs; host support [unverified, M7] |
| Committed text mirror | 2–6 d | generator, pre-commit hook or CI check, staleness check |

### Metadata-only tier (lower bound)

If the owner accepted metadata only (no heap or type decoding) as a first step, the core would be container + metadata + paths + XML + fixtures: about 5–14 d for 2024-only and 16–49 d for all versions, using the same per-row ranges. pylavi already reads this tier for 420/420 corpus files [artifact], so the 2020–2024 part of it is mostly packaging.

### Version-format differences that drive the estimate

1. RSRC container version: pylavi accepts only `format_version == 3` (`@environment/pylavi/pylavi/file.py`, `Header.VERSION = 3`). All 420 corpus files pass [artifact]. Whether pre-2020 files use another value is [unverified, M2].
2. Version number encoding: `Version` packs major as two BCD nibbles, then minor, patch, a 3-bit phase and a BCD build (`Version.__compose`, `major()`, `phase()`, `build()` in `@environment/pylavi/pylavi/data_types.py`) [parser]. This is how a tool would detect 2024 files (major 24). Observed values: `20`, `20.0.1f7`, `21.0.1f6`, `24.1.1f1`, `24.3.1f1` [artifact].
3. `LVSR` flag block: fixed offsets (`TypeLVSR` constants, `BREAKPOINT_COUNT_INDEX = 28`) and a length check that returns `None` for short blocks (`@environment/pylavi/pylavi/resource_types.py`) [parser]. All observed blocks are 156 bytes [artifact]. Older sizes and moved bits [unverified, M2].
4. `LVSR.version` differs from `vers.version` in 137 of 415 files [artifact]. Which one marks the saved format is [unverified, M10]; a 2024-only gate built on the wrong field would accept or reject the wrong files.
5. Path formats `PTH0`/`PTH1`/`PTH2` with different string prefixes and encodings (`Path.from_bytes`, `@environment/pylavi/pylavi/data_types.py`) [parser]. Mapping to versions [unverified, M5].
6. Resource type set: the same core set (`FPHb`, `BDHb`, `VCTP`, `LIvi`, `LVSR`, `vers`, …) appears in 20.0, 21.0, 24.1 and 24.3; the five types seen only in 20.0 (`HLPU`, `HLPW`, `MNGI`, `TITL`, `VINS`) appear in few files and are more likely content-dependent than version-dependent [artifact counts; cause unverified, M2].
7. Heap and type-descriptor layouts: not visible in pylavi at all [parser]; any per-version difference is [unverified, M1, M2].
8. XML `LVVersion` attribute in project/library/class files: `20008000`, `21008000` [artifact]; schema changes across versions [unverified, M9].

## Compatibility limits of the 2024 fallback

A tool that supports only files saved by LabVIEW 2024 would not read, or would read only with "unsupported version" warnings:

- **413 of 415 versioned RSRC files in the prepared corpus** (395 saved by 2020, 18 by 2021) [artifact]. Only `Post Build Icon Editor PPL.vi` and `VIP_Post-Install Custom Action.vi` are 2024 files. Actor Framework itself, the prepared target, is saved in 2020 (`project_lvversion` `20008000`, `@environment/readiness.json`).
- The prepared fixture `Core/ActorFramework/Actor/Actor Core.vi` unless it is resaved in 2024: its `vers` version is `20.0.1f7` and its `LVSR.version` is `20`, with 30 resource types [artifact, measured with `Resources.load` + `Typevers` + `TypeLVSR` on the prepared file].
- Any file saved before LabVIEW 2024 (2023 and earlier, including all 8.x–2019 files) that is not resaved. Resaving needs a LabVIEW 2024 licence and IDE (`labview_ide: not_checked`) and changes the files in the user's repository, which may not be acceptable for libraries that must stay loadable in older LabVIEW.
- Files saved by releases after 2024 (2025 and later) if their format changes [unverified, M2].
- `.mnu` files: they have no `vers` resource [artifact], so a gate on `vers` major would reject them unless a separate rule is added.
- XML files (`.lvproj`, `.lvclass`, `.lvlib`) whose `LVVersion` is not 24: 64 of 65 are `20008000`, 1 is `21008000` [artifact]. These are text already, so a strict gate would lose readable content for no format reason.
- Families neither variant reads today: `.lvlibp`, `.lvlps`, `.vip`, `.vipc`, `.vipb` (not RSRC at offset 0 in the corpus) [artifact]; `.llb`, `.vit`, `.ctt`, `.rtexe` are listed by pylavi but absent from the corpus [unverified, M4].

A softer form of the fallback, "decode 2024 formats, but also accept older files when their container and resource layout match", might cover the 2020–2024 corpus, because the observed container version, resource type set and `LVSR` block size are the same across 20.0–24.3 [artifact]. Whether heap and type-descriptor contents also match is [unverified, M1, M2]. This report states that option; it does not choose it.

An IDE-based fallback (use LabVIEW 2024 to export text) would add: a licensed install, Windows or supported Linux host, no headless CI by default, and a per-machine dependency for every agent run [unverified, M6].

## Open measurements

Each item turns an [unverified] claim into a measurement a later task can run. None needs internet unless stated.

- **M1 Heap decodability.** Take `Core/ActorFramework/Actor/Actor Core.vi` and the two 2024 files. Extract `BDHb`, `FPHb`, `VCTP` with `Resources.get_resource`. Measure: does each blob start with a known compression header (try `zlib.decompress` at offsets 0 and 4); after decompression, list the tag/size structure of the first 200 bytes. Output: per-file table "compressed? (y/n), decompressed size, first tags". Pass: a structure is identifiable in all three files.
- **M2 Cross-version layout drift.** Obtain 1 VI per release from 8.0 to 2025 (needs internet or an owner-provided set; record source and licence). Run `versions.py` and `types_by_version.py` on it, extended to print `Header.format_version`, `LVSR` block size, and the first 64 bytes of decompressed `VCTP`/`BDHb` per version. Output: per-version table. This sets the all-versions decoder count.
- **M3 Version range and per-file versions.** Extend `versions.py` to print the `vers` version of each named fixture (including `Actor Core.vi`) and confirm the oldest release that still writes RSRC `format_version == 3`. Output: list of fixture → version; earliest supported release.
- **M4 Missing families.** Find public `.llb`, `.vit`, `.ctt`, `.rtexe` files (internet) and run `Resources.load` on each. Output: loaded / failed with assertion text.
- **M5 Path format by version.** For every file with `PATH`, `LPTH`, `DLLP`, `HLPP`, `RTMP` resources, print `Path.format` against `vers` version. Output: format × version counts.
- **M6 IDE-based export cost.** On a machine with LabVIEW 2024 (if the owner provides one), time a VI Server or scripting export of `Actor Core.vi` and record licence and OS requirements. Output: steps, run time, licence notes.
- **M7 MCP host support.** In each agent host used by this loop, configure a minimal stdio MCP server exposing `list_resources(path)` and call it once. Output: host → works / not supported.
- **M8 Mirror size.** Generate a metadata-only text dump for all 420 RSRC files and record total bytes and median per file. Output: total size, median, largest file.
- **M9 XML schema drift.** Diff element and attribute names of `.lvproj`/`.lvclass`/`.lvlib` files with `LVVersion` `20008000` vs `21008000` (and newer, if obtained in M2). Output: list of names present in only one version.
- **M10 `LVSR.version` vs `vers.version`.** For the 137 files where they differ, print both values and the `HIST` resource size. Output: table; decide which field reflects the saved format, with the files that show it.
- **M11 Agent usefulness.** For a fixed question set on `Actor Core.vi` (inputs, outputs, called subVIs), compare agent answers using (a) raw pylavi metadata dump and (b) a heap-decoded dump if M1 succeeds. Output: correct answers per question. This measures `semantic_reading`.
