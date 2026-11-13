# Authoring record for the controlled pairs

Issue: #516. Instructions: [owner-instructions.md](../owner-instructions.md).

## Environment

| Item | Value |
|---|---|
| LabVIEW | LabVIEW 2026, version 26.1.1f1 (read from `LabVIEW.exe` file version) |
| Bitness | 32-bit (`C:\Program Files (x86)\National Instruments\LabVIEW 2026\LabVIEW.exe`; this is the only LabVIEW executable installed on the machine) |
| Operating system | Microsoft Windows 11 Pro 64-bit, version 10.0.26200 |
| Date authored | 2026-11-13 |

## Save settings (same for all eight files unless noted)

| Setting | Value |
|---|---|
| Separate compiled code from source file | Off for `*-normal.vi`, on for `*-separate.vi` (the only setting varied) |
| Allow debugging (VI Properties > Execution) | On (LabVIEW default, not changed) |
| Optimization / other execution settings | LabVIEW defaults, not changed |
| Password protection | Off for every file |
| Save for previous version | Not used; every file saved in 26.1.1f1 |

## Files

| File | Source baseline | Separate compiled code | Exact change |
|---|---|---|---|
| `add-normal.vi` | new blank VI | off | baseline: I32 controls `x` (upper Add input) and `y` (lower Add input), Add, I32 indicator `result` |
| `subtract-normal.vi` | `add-normal.vi` (Save As) | off | Add replaced with Subtract (Replace menu); terminals, wires, input order kept |
| `add-separate.vi` | `add-normal.vi` (Save As) | on | separate compiled code enabled; diagram unchanged |
| `subtract-separate.vi` | `add-separate.vi` (Save As) | on | Add replaced with Subtract (Replace menu); terminals, wires, input order kept |
| `constant-1-normal.vi` | new blank VI | off | baseline: I32 constant 1 wired to one I32 indicator |
| `constant-2-normal.vi` | `constant-1-normal.vi` (Save As) | off | constant value 1 changed to 2 |
| `constant-1-separate.vi` | `constant-1-normal.vi` (Save As) | on | separate compiled code enabled; diagram unchanged |
| `constant-2-separate.vi` | `constant-1-separate.vi` (Save As) | on | constant value 1 changed to 2 |

## Load warnings, conversions and unintended changes

None observed. LabVIEW showed no load warning, conversion dialog or "save changes?" prompt during authoring or when closing. No unintended edits were made. No wire broke during the Add to Subtract replacements, so neither copy was recreated.

Save times (local, 2026-11-13) show that each baseline was not resaved after its copies were made:

| File | Saved | Bytes |
|---|---|---|
| `add-normal.vi` | 13:25:31 | 6334 |
| `subtract-normal.vi` | 13:30:26 | 6335 |
| `add-separate.vi` | 13:34:05 | 4128 |
| `subtract-separate.vi` | 13:40:34 | 4129 |
| `constant-1-normal.vi` | 13:43:20 | 5937 |
| `constant-2-normal.vi` | 13:45:24 | 5941 |
| `constant-1-separate.vi` | 13:46:19 | 3919 |
| `constant-2-separate.vi` | 13:47:21 | 3923 |

All eight VIs are newly authored public examples with no private project material.
