# Prepared public coverage inventory

Preparation evidence only, pending independent review; no benchmark readiness or product approval.

Regenerate with `python3 -I benchmark/scripts/coverage.py`; verify with `python3 -I benchmark/scripts/coverage.py --check`.
Inputs are the pinned read-only `$LABVIEW_ENVIRONMENT` sources, verified against [sources.json](sources.json).
The complete path, hash, dual-header versions, archive/access gaps and resource decoder counts are in [coverage.json](coverage.json).

Inspected 1545 tracked files; retained 831 artifact occurrences (532 originals and 299 archive members), including duplicates and unsupported cases.
Archive members are read in memory recursively; originals are preserved. Unknown embedded contents remain unknown, not zero.

| Family | Occurrences | Header versions: raw hex (artifact count) |
| --- | ---: | --- |
| .aliases text/other | 2 | unavailable: 2 |
| .aliases text/other (archive member) | 5 | unavailable: 5 |
| .ctl RSRC LVCC | 9 | 20008000: 9; 20018007: 4 |
| .ctl RSRC LVCC (archive member) | 7 | 20008000: 7; 20018007: 7 |
| .docx zip | 2 | unavailable: 2 |
| .lvclass XML | 48 | 20008000: 48 |
| .lvclass XML (archive member) | 47 | 13008000: 2; 14008000: 16; 15006000: 5; 15008000: 1; 20008000: 23 |
| .lvlib XML | 12 | 20008000: 11; 21008000: 1 |
| .lvlib XML (archive member) | 13 | 14008000: 7; 15006000: 2; 15008000: 1; 20008000: 3 |
| .lvlibp PE/opaque | 1 | unavailable: 1 |
| .lvlibp PE/opaque (archive member) | 11 | unavailable: 11 |
| .lvlps text/other | 1 | unavailable: 1 |
| .lvlps text/other (archive member) | 5 | unavailable: 5 |
| .lvproj XML | 5 | 20008000: 5 |
| .lvproj XML (archive member) | 5 | 14008000: 3; 15006000: 1; 15008000: 1 |
| .mnu RSRC LMNU | 5 | unavailable: 5 |
| .mnu RSRC LMNU (archive member) | 5 | unavailable: 5 |
| .vi RSRC LVIN | 432 | 20008000: 385; 20018000: 1; 20018007: 118; 21000000: 1; 21002000: 1; 21004000: 1; 21006000: 1; 21008000: 31; 21018002: 2; 21018006: 9; 23008000: 5; 24008000: 2; 24118001: 1; 24318001: 1; 26008000: 5; 26308000: 5 |
| .vi RSRC LVIN (archive member) | 200 | 13008000: 8; 13008051: 8; 14008000: 41; 14008034: 16; 14008036: 25; 15006000: 12; 15006011: 12; 15008000: 4; 15008029: 4; 16008000: 1; 16008010: 1; 20008000: 134; 20018007: 134 |
| .viancfg XML | 1 | unavailable: 1 |
| .vim RSRC LVIN | 1 | 20008000: 1; 20018007: 1 |
| .vim RSRC LVIN (archive member) | 1 | 20008000: 1; 20018007: 1 |
| .vip zip | 1 | unavailable: 1 |
| .vipb text/other | 3 | unavailable: 3 |
| .vipc zip | 2 | unavailable: 2 |
| .vsix zip | 2 | unavailable: 2 |
| .zip zip | 5 | unavailable: 5 |

A file can contribute both vers and LVSR declarations; version columns are not mutually exclusive. Their authoritative save-version meaning is unverified.
Raw values and decoded labels are listed in JSON; unknown phase codes retain their raw values. No filename is used as version evidence.

## Reading environments, modules and access

`native_labview: not executed`. This inventory executes Python, git metadata inspection and pinned pylavi metadata decoders.
Byte round-tripping and whole-file resource loading do not establish diagram, type, dependency or answer correctness.
XML target/item types and dependency declarations are recorded as static evidence; installed modules, licensing, activation and dependency resolution are unverified.
The earlier documented 2026 Q1 cloud MassCompile is separate evidence for one LV2014 fixture, not execution on this corpus. Native 2024 and cross-version compatibility remain unverified.

## Explicit gaps

- Missing extension families: .ctt, .dll, .exe, .gbl, .glb, .llb, .lsb, .lvsc, .lvtest, .rtexe, .rtm, .so, .uir, .vit, .xctl, .xnode.
- All native versions/builds remain unexamined here, including observed header versions; unrepresented versions are gaps. The 2024 fallback is not selected.
- Opaque resources, PE packed libraries, unknown embedded contents and unreadable/archive-limit cases stay in the inventory. See per-family decoder counts and archive_gaps in JSON.
- Native LabVIEW is needed to establish header semantics, protected/removed diagram access, actual loading/compatibility, installed modules, resolved dependencies, build behavior and hardware results.
- Real-Time, FPGA, DSC, Vision, DAQmx, MathScript and other modules/targets have no established native coverage. The first public corpus does not redefine the goal.

Next: request independent review of this preparation, then prepare tasks/oracle with independently established expectations. Sources and coverage are preparation only; all other milestones and owner gates remain pending.
