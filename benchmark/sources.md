# Prepared public source provenance

This is preparation evidence for the `sources` milestone in [the evaluation contract](../docs/perpetua/evaluation.md), pending independent review. It does not establish benchmark readiness or authorize product implementation. No tasks, oracle answers, evaluation split or scoring are supplied.

All sources are public. Neither these artifacts nor copies, variants or their public history can serve as withheld or unseen evaluation cases. Restricted evaluation storage and execution have not been established or tested.

## Sources and originals

| Source | Public upstream | Pinned commit | License | Selected artifacts |
| --- | --- | --- | --- | ---: |
| NI Actor Framework | https://github.com/ni/actor-framework | `371c631c16155d88f02be11a953e4964d7452fd8` | MIT, `LICENSE.txt` | 496 |
| pylavi | https://github.com/marcpage/pylavi | `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75` | Unlicense, `LICENSE` | 27 |

The starting evidence is the prepared read-only `$LABVIEW_ENVIRONMENT/readiness.json` and the source trees described in [environment readiness](../docs/perpetua/environment.md). Upstream URLs identify the declared public projects; they are not inferred from a local Git remote or revalidated online. The readiness file supplies commits, license identifiers and the Actor Core.vi fixture hash. The script pins those values and checks the corresponding tracked license bytes and license markers.

[`sources.json`](sources.json) records every selected artifact's repository-relative path, size, SHA256 and available header save version. It also records license-file hashes, the readiness-file SHA256, tracked-file counts and a digest of the sorted path/size/SHA256 inventory of every tracked file. Every tracked file's bytes must match its pinned Git blob, including files outside the artifact selection. The prepared trees contain 1,545 tracked files in total.

Originals remain in the prepared read-only cache, outside this repository. No conversion, archive extraction, native compilation or source modification is performed. The manifest contains metadata, not redistributed binaries. Preserve these originals before any future conversion and separately hash derived copies.

## Offline reproduction and drift detection

With the already prepared cache exposed as `LABVIEW_ENVIRONMENT`, run from the repository root:

```sh
python3 -I benchmark/scripts/sources.py
python3 -I benchmark/scripts/sources.py --check
```

Python's standard library and local Git metadata are sufficient; there is no download, package installation or import/execution of prepared source code. The first command generates a missing manifest or reproduces an identical existing one. Both commands reject changed pins, license declarations, tracked source bytes, the fixture hash or any difference from an existing manifest. `--check` requires the manifest to exist, checks canonical serialization and never writes it. A mismatch exits nonzero and preserves the existing manifest. Investigate drift rather than deleting the lock to accept changed inputs.

Selection is explicit: all tracked files with the extensions listed in `sources.json` under `selection.tracked_artifact_extensions`. Untracked files are excluded. Archive/package files are inventoried as original containers; their members are not independently selected or inspected. This selection defines this prepared inventory, not the product's required scope.

## Save-version evidence and limits

The observable is the save-version declaration in the original file, independently of any future product reader. The script reads the original RSRC resource table and the first UInt32 of `LVSR`, falling back to `vers`; it records the exact raw hexadecimal value and byte offset. For XML artifacts it records the root `LVVersion` attribute. Packed BCD decoding follows the version representation visible in the pinned pylavi `pylavi/data_types.py`, but no pylavi code is imported. This is container metadata inspection, not an independent semantic oracle or a claim about diagram contents.

Of 523 selected artifacts, 507 have a recorded raw version and 16 explicitly report an unavailable header version. There are 506 decoded versions: 459 at 20.0.0f0, 32 at 21.0.0f0, one each at 21.0.0a0, 21.0.0b0 and 21.0.0d0, five at 23.0.0f0, two at 24.0.0f0 and five at 26.0.0f0. The pylavi fixture `tests/empty_invalid.vi` retains raw `21000000` at byte offset 36 with `decoded: null`; its phase is not a supported named release phase. It is visible rather than coerced into a normal release.

The 16 unavailable entries comprise five menu files without an `LVSR` or `vers` resource, one XML configuration without `LVVersion`, and ten files without a supported RSRC/XML version header. Each path and reason is retained in the manifest. A filename or package label is not substituted for a header version. No runtime compatibility follows from a decoded save version.

The reading environment here is Python with local Git, as recorded by the generating command, not native LabVIEW. Native LabVIEW is not executed and semantic reading is not measured. Dependency resolution, installed modules, runtime versions, activation, protected/removed diagrams and successful native loading remain unverified. Previously documented cloud runtime results are separate environment evidence, not execution of this inventory.

## Visible gaps and next steps

- Only the two prepared public repositories are available. The separately documented pylabview/LV2014 cloud-runtime fixture is not present in this prepared source inventory; it is not silently treated as a third source.
- Older and other unrepresented save versions remain missing; the observed versions do not establish all-version coverage or select the LabVIEW 2024 fallback.
- Observed families include VI/VIM, controls, classes, libraries, projects, menus, configuration, packages and a packed library. No dedicated controlled sources establish coverage for templates, standalone test artifacts, XControls/XNodes, executables, shared libraries, FPGA/real-time targets, hardware-dependent modules or all resource families. Containers are not evidence that their contents are readable.
- Dependencies and package members have not been resolved, build specifications have not been interpreted, and diagram accessibility has not been established. Missing dependencies, licenses or native environments remain visible gaps rather than passing cases.
- No project/family split, duplicate/variant analysis, withheld storage boundary, independently established answers, matched model baselines or method challenges have been prepared. Those milestones remain not started.

Request a separate reviewer session against the pinned preparation tree and original prepared sources. A reviewer must assess substantive provenance and header evidence; valid filenames and hashes alone do not establish method quality. Executable scoring changes require a Policymaker-ordered evaluator change and its separate verifier. Independent method review and owner acceptance remain prerequisites for product implementation; quality thresholds and the final goal gate remain owner decisions.
