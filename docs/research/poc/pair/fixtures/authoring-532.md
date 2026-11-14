# Authoring record for the unchanged Save As control

Issue: #532. Baseline record: [authoring.md](authoring.md) (#516).

## Environment

| Item | Value |
|---|---|
| LabVIEW | LabVIEW 2026, version 26.1.1f1 |
| Bitness | 32-bit (`C:\Program Files (x86)\National Instruments\LabVIEW 2026\LabVIEW.exe`), the same installation used for #516 |
| Operating system | Microsoft Windows 11 Pro 64-bit, version 10.0.26200 |
| Date authored | 2026-11-14 |

## File

| File | Source | Separate compiled code | Exact change |
|---|---|---|---|
| `constant-1-separate-control.vi` | disposable copy of `constant-1-separate.vi` (Save As) | on (inherited, not touched) | none |

## Save operation

1. Opened a disposable copy of `constant-1-separate.vi`.
2. Used Save As to write `constant-1-separate-control.vi`.
3. Did not edit the diagram, front panel, VI properties or the separate-compiled-code setting.

The repository's `constant-1-separate.vi` was not opened for saving and is unchanged (SHA256 still matches `pins.json`).

## Warnings, conversions and result

- Automatic conversion: none.
- Load or save warning, or dialog: none observed.
- Broken arrow: none. The Run arrow is intact when the VI opens.

| File | Saved | Bytes |
|---|---|---|
| `constant-1-separate-control.vi` | 2026-11-14 19:03:45 | 3927 |

The VI is a newly authored public example with no private project material.

This control is not listed in `pins.json`; that manifest pins the #516 set and its `authoring.md` hash. It only helps separate saving effects from logic effects and does not by itself prove a safe edit rule.
