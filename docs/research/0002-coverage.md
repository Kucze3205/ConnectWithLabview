# 0002 Coverage: artifact families, save versions and pylavi decoding

Status: partial (first commit). Sources: pylavi `35d2a03`, Actor Framework `371c631` (`@environment/readiness.json`).

## Families x save versions

Produced by:

```
python3 -I docs/research/scripts/coverage/inventory.py --table
```

Versions come from the file itself. RSRC files: the first `LVSR` resource's version word, or the lowest-id `vers` resource if there is no LVSR. XML files: the `LVVersion` attribute. `.vipb`: `<Package_LabVIEW_Version>`. Decoding uses the bit layout of `Version` in `@environment/pylavi/pylavi/data_types.py`. `unknown` means the script found no version field.

### Top-level files

| family | files | 20.0 | 20.0.0 | 21.0.0 | 21.0.0a0 | 21.0.0b0 | 21.0.0d0 | 21.0.0{0}0 | 23.0.0 | 24.0.0 | 26.0.0 | unknown |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `.aliases` project aliases | 2 |  |  |  |  |  |  |  |  |  |  | 2 |
| `.ctl` control / typedef | 9 |  | 9 |  |  |  |  |  |  |  |  |  |
| `.lvclass` class (XML) | 48 |  | 48 |  |  |  |  |  |  |  |  |  |
| `.lvlib` project library (XML) | 12 |  | 11 | 1 |  |  |  |  |  |  |  |  |
| `.lvlibp` packed project library | 1 |  |  |  |  |  |  |  |  |  |  | 1 |
| `.lvlps` project local settings | 1 |  |  |  |  |  |  |  |  |  |  | 1 |
| `.lvproj` project (XML) | 5 |  | 5 |  |  |  |  |  |  |  |  |  |
| `.mnu` run-time menu | 5 |  |  |  |  |  |  |  |  |  |  | 5 |
| `.vi` VI | 432 |  | 385 | 31 | 1 | 1 | 1 | 1 | 5 | 2 | 5 |  |
| `.vim` malleable VI | 1 |  | 1 |  |  |  |  |  |  |  |  |  |
| `.vip` VI package (zip) | 1 |  |  |  |  |  |  |  |  |  |  | 1 |
| `.vipb` VIPM build spec | 3 | 3 |  |  |  |  |  |  |  |  |  |  |
| `.vipc` VIPM configuration (zip) | 2 |  |  |  |  |  |  |  |  |  |  | 2 |

### Members of zip archives (`.zip`, `.vip`, `.vipc`, ...)

| family | files | 13.0.0 | 14.0.0 | 15.0.0 | 15.0.0b0 | 16.0.0 | 20.0.0 | unknown |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `.aliases` project aliases | 5 |  |  |  |  |  |  | 5 |
| `.ctl` control / typedef | 7 |  |  |  |  |  | 7 |  |
| `.lvclass` class (XML) | 47 | 2 | 16 | 1 | 5 |  | 23 |  |
| `.lvlib` project library (XML) | 13 |  | 7 | 1 | 2 |  | 3 |  |
| `.lvlibp` packed project library | 11 |  |  |  |  |  |  | 11 |
| `.lvlps` project local settings | 5 |  |  |  |  |  |  | 5 |
| `.lvproj` project (XML) | 5 |  | 3 | 1 | 1 |  |  |  |
| `.mnu` run-time menu | 5 |  |  |  |  |  |  | 5 |
| `.vi` VI | 200 | 8 | 41 | 4 | 12 | 1 | 134 |  |
| `.vim` malleable VI | 1 |  |  |  |  |  | 1 |  |

## pylavi decoding per family

TODO (next step): fill this in from `samples`, `archive_samples` and `fixture` in the JSON output of `python3 -I docs/research/scripts/coverage/inventory.py`.

## Gaps

TODO (next step).
