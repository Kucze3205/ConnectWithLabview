# 0100 — WM1 original version declarations

**Measured: all six declarations agree on raw version bytes `20 00 80 00`.** The pinned parser interprets these as `(20, 0, 0, 4, 0)` in `(major, minor, patch, phase, build)` order, value `"20"`; phase 4 means release in that parser. Independent authoritative original-save-version confirmation remains unavailable. [Raw evidence JSON](0100-wm1-version-evidence.json) preserves each entry separately, full payload hex/SHA256, field offset, decoded structure and input pins.

| Observed resource | ID | Payload bytes | Version offset within payload | Raw version bytes | Pinned-class interpretation |
|---|---:|---:|---:|---|---|
| `vers` | 4 | 12 | 0 | `20008000` | `Typevers`: `(20,0,0,4,0)`, `"20"` |
| `vers` | 7 | 12 | 0 | `20008000` | `Typevers`: `(20,0,0,4,0)`, `"20"` |
| `vers` | 8 | 12 | 0 | `20008000` | `Typevers`: `(20,0,0,4,0)`, `"20"` |
| `vers` | 9 | 12 | 0 | `20008000` | `Typevers`: `(20,0,0,4,0)`, `"20"` |
| `vers` | 10 | 12 | 0 | `20008000` | `Typevers`: `(20,0,0,4,0)`, `"20"` |
| `LVSR` | 0 | 160 | 0 | `20008000` | `TypeLVSR`: `(20,0,0,4,0)`, `"20"` |

No absent target resource types, duplicate IDs, malformed entries, trailing payload bytes or conflicting version declarations were observed. `Resources.get_resources()` enumerates lists without deduplicating IDs; the five `vers` payloads are byte-identical but remain five records. Offsets are zero-based relative to the returned payload, excluding the resource's four-byte length prefix.

The only parsed original was `@environment/actor-framework/Core/ActorFramework/Message Dequeuer/Equals Not A Refnum.vi`, Actor Framework revision `371c631c16155d88f02be11a953e4964d7452fd8`, SHA256 `19b5dcd98b3b2e83e2b533d9227bd07d16837f350243377292b7c0b8a935338c`. Starting repository commit `06cadfb64f1412f11a8e670f13b15a0f48711375`, tree `e7a2dd977f6a1930522b28d439bcece18ea01fa6`; initial `git status --short` was empty. Prepared readiness reported `public_sources=ready`; JSON records its hash and both source revisions. Startup diagnostic was `ok`.

The method SHA256 recheck matched `8c3b165c33c8fb4944f10a0eaa3c384fcc90d62c3278c0c910a5f2ae8b9d4da1`. Pylavi HEAD matched `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75`; `file.py` SHA256 matched `f3c9d38054291d02bf48e7f2658c2b012e0c0b7a7fb55731710e985d7df2cce9` and `resource_types.py` matched `ce333fba1b8dc689197e18e4a1acedf77b786f098f5039e4234c136f73512756`, the [0099 S22/S23 pins](0099-writing-version-effort.json). The directly required `data_types.py` hash is also recorded. No fixture substitution occurred.

Reproduce from the repository root with prepared sources exposed through `LABVIEW_ENVIRONMENT`:

```text
python3 docs/research/0100-wm1-version-evidence.py
```

The [replay script](0100-wm1-version-evidence.py) checks pins/readiness before loading this one original, saves raw entries before interpreting them and stops on pin/parse failure. The actual invocation exited 0, reporting `measured`, counts `vers=5`, `LVSR=1`, agreement `agree`. It requires Python and the prepared pinned source checkout, with no LabVIEW execution.

Primary parser locators at that revision: `pylavi/file.py:420–465` (`Resources.load`), `331–338` (all-entry enumeration), `413–418` (payload framing); `pylavi/resource_types.py:221–268` (`Typevers`) and `115–121,210–215` (`TypeLVSR`); `pylavi/data_types.py:334–340` (field order), `74–101,158–162` (big-endian UInt32), `657–664,744–782,802–825` (`Version` value/tuple decoding). These are third-party interpretation rules, not an independent NI save-version authority. `Header.VERSION` (`file.py:27,75`) concerns container framing and was not used to infer save version; neither filename nor project version was used.

[WM1's unchanged requirement](../../benchmark/writing/method.json), `/tasks/1/originals/0/save_version`, remains `"unavailable"`; its oracle still lists `original-save-version` as missing and requires `WM1-original-save-version` preservation. This study replaces the unmeasured declaration question with six reproducible agreeing observations. It does not replace the missing independent authority, establish an emitted format or native compatibility/preservation, resolve semantic writing feasibility, accept the method or support a 2024 fallback. No original, parser, prior study, POC, benchmark pin or product/policy/evaluator file was changed; no native or benchmark execution was attempted.

## What next

Use this saved one-original record as supporting evidence in independent original-save-version confirmation before freezing WM1 original/output preservation checks; retain the authority gap until confirmation exists. The measurement is complete. A cold session should start here and at [0099's bounded next measurement](0099-writing-version-effort.json), replay only if needed against the same pins, and avoid corpus searches, closed synthetic/completion-guard reviews, fixture substitution or treating field agreement as authority. No new owner request is made.
