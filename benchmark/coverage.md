# Prepared-source coverage

Public development inventory; independent review pending. native_labview: not executed.
Regenerate: `python3 -I benchmark/scripts/coverage.py`; verify: add `--check`.
See [coverage.json](coverage.json) for every artifact, raw version field and gap.

| Family | Entries | Version fields (occurrences) | No version |
|---|---:|---|---:|
| .aliases text/other | 2 | unavailable | 2 |
| .aliases text/other (zip member) | 5 | unavailable | 5 |
| .ctl RSRC LVCC | 9 | LVSR: 20008000: 9; vers: 20008000: 33; vers: 20018007: 12 | 0 |
| .ctl RSRC LVCC (zip member) | 7 | LVSR: 20008000: 7; vers: 20008000: 14; vers: 20018007: 21 | 0 |
| .lvclass XML | 48 | XML root @LVVersion: 20008000: 48 | 0 |
| .lvclass XML (zip member) | 47 | XML root @LVVersion: 13008000: 2; XML root @LVVersion: 14008000: 16; XML root @LVVersion: 15006000: 5; XML root @LVVersion: 15008000: 1; XML root @LVVersion: 20008000: 23 | 0 |
| .lvlib XML | 12 | XML root @LVVersion: 20008000: 11; XML root @LVVersion: 21008000: 1 | 0 |
| .lvlib XML (zip member) | 13 | XML root @LVVersion: 14008000: 7; XML root @LVVersion: 15006000: 2; XML root @LVVersion: 15008000: 1; XML root @LVVersion: 20008000: 3 | 0 |
| .lvlibp text/other | 1 | unavailable | 1 |
| .lvlibp text/other (zip member) | 11 | unavailable | 11 |
| .lvlps text/other | 1 | unavailable | 1 |
| .lvlps text/other (zip member) | 5 | unavailable | 5 |
| .lvproj XML | 5 | XML root @LVVersion: 20008000: 5 | 0 |
| .lvproj XML (zip member) | 5 | XML root @LVVersion: 14008000: 3; XML root @LVVersion: 15006000: 1; XML root @LVVersion: 15008000: 1 | 0 |
| .mnu RSRC LMNU | 5 | unavailable | 5 |
| .mnu RSRC LMNU (zip member) | 5 | unavailable | 5 |
| .vi RSRC LVIN | 432 | LVSR: 20008000: 385; LVSR: 21000000: 1; LVSR: 21002000: 1; LVSR: 21004000: 1; LVSR: 21006000: 1; LVSR: 21008000: 31; LVSR: 23008000: 5; LVSR: 24008000: 2; LVSR: 26008000: 5; vers: 20008000: 1336; vers: 20018000: 1; vers: 20018007: 124; vers: 21000000: 5; vers: 21002000: 5; vers: 21004000: 5; vers: 21006000: 5; vers: 21008000: 96; vers: 21018002: 2; vers: 21018006: 9; vers: 23008000: 25; vers: 24008000: 2; vers: 24118001: 1; vers: 24318001: 3; vers: 26308000: 5 | 0 |
| .vi RSRC LVIN (zip member) | 200 | LVSR: 13008000: 8; LVSR: 14008000: 41; LVSR: 15006000: 12; LVSR: 15008000: 4; LVSR: 16008000: 1; LVSR: 20008000: 134; vers: 13008000: 16; vers: 13008051: 24; vers: 14008000: 82; vers: 14008034: 48; vers: 14008036: 75; vers: 15006011: 12; vers: 15008000: 8; vers: 15008029: 12; vers: 16008010: 1; vers: 20008000: 6; vers: 20018007: 140 | 0 |
| .viancfg XML | 1 | unavailable | 1 |
| .vim RSRC LVIN | 1 | LVSR: 20008000: 1; vers: 20018007: 1 | 0 |
| .vim RSRC LVIN (zip member) | 1 | LVSR: 20008000: 1; vers: 20018007: 1 | 0 |
| .vip zip | 1 | unavailable | 1 |
| .vipb XML | 3 | unavailable | 3 |
| .vipc zip | 2 | unavailable | 2 |
| .vsix zip | 2 | unavailable | 2 |
| .zip zip | 5 | unavailable | 5 |

Version-field occurrences are not additional artifacts. Archive members remain separate entries, including copies.
No version or family is removed from the goal; the 2024 fallback is not selected.

- Every native LabVIEW reading environment and cross-version compatibility remains unexamined in this inventory
- All goal families and versions absent from these public sources remain uncovered, not excluded
- Modules, targets, licenses and dependencies require native and independent evidence
- Protected or removed diagrams, behavior and semantic fidelity cannot be established from headers
- Missing extensions: .ctt, .gbl, .glb, .llb, .lsb, .lvsc, .lvtest, .rtexe, .rtm, .uir, .vit, .xctl, .xnode
- Missing major save-version fields (1..26 navigation): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 18, 19, 22, 25
- No authoritative save-version field selected: multiple vers resources can describe different metadata; all raw fields retained
- Packed PE/MZ libraries remain opaque; embedded artifact counts and versions are unknown
- Archive inspection is one level; nested archives and nonselected member formats are not recursively interpreted
- Typedef status, protected/removed diagrams, tests, build behavior and module requirements need independent native inspection
- This extension and magic based inventory is not proof of exhaustive discovery of every possible LabVIEW artifact format
