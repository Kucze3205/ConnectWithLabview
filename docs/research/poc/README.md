# POC: inspect one public VI without LabVIEW

## Measured result

`add.vi` now has a completely framed BDHb tag tree: 162 entries consume all 842 decompressed bytes, with matching open/close tags. The tree identifies a primitive discriminator and three signal endpoint pairs. An in-memory discriminator mutation reparses successfully; its mathematical meaning and LabVIEW validity remain unverified. No VI was edited on disk and no LabVIEW behavior is claimed.

## Artifact and primary-source provenance

- Input: `$LABVIEW_ENVIRONMENT/pylavi/tests/add.vi`, pylavi [35d2a0318f71dcb87bb9c431dc00700ee6b9fb75](https://github.com/marcpage/pylavi/tree/35d2a0318f71dcb87bb9c431dc00700ee6b9fb75), Unlicense; SHA256 `cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8`.
- Step 1 established the 6,371-byte RSRC format-3 `LVIN`/`LBVW` container and declared save version `21008000` (21.0.0 final build 0). Those measurements were reused, not repeated as a separate investigation. They establish artifact declarations, not runtime compatibility.
- Heap grammar and names come from pylabview [5f20e23de6a386021eb955c825cc43d221f09ff1](https://github.com/mefistotelis/pylabview/tree/5f20e23de6a386021eb955c825cc43d221f09ff1), `pylabview/LVheap.py` and `LVmisc.py`. [Source URLs and SHA256s](source-provenance.json), [MIT license](pylabview-LICENSE.txt), and exact [LVheap](LVheap-source.txt)/[LVmisc](LVmisc-source.txt) snapshots are saved. These are the upstream author's reverse-engineering rules, not an NI specification. The pinned wiki page contains no entry-level grammar; the executable source supplies it.
- RSRC traversal follows `benchmark/scripts/sources.py::save_version` and pinned pylavi `pylavi/file.py`; neither benchmark code nor prepared public artifacts were changed.

## Reproduce and inspect

```text
python3 -I docs/research/poc/inspect_vi.py /path/to/pylavi/tests/add.vi
python3 -I docs/research/poc/verify_poc.py
```

The inspector uses only stdlib and accepts a VI path; `heap-labels.json` supplies source-derived names beside the script. Without that sidecar it still prints numeric tags. `--output FILE` saves complete JSON offsets/content and `--tree-output FILE` saves the full tree; stdout defaults to 60 entries. Invalid input stops with the failing entry/cursor offset for heap errors, or a container/decompression diagnostic before heap parsing.

The 16-bit header hypothesis is confirmed structurally on all four fixtures: bits 15–13 are sizeSpec, bit 12 signals an attribute list, bits 11–10 encode open=0/leaf=1/close=2, and bits 9–0 contain tag+31. Raw tag 1023 introduces a signed UInt32-width tag ID. Attributes have a variable-width count and signed ID/value pairs. sizeSpec 1–4 gives literal body bytes; 6 introduces a variable-width body length; 0/7 encode no body/inline false/true. Reserved scope 3 and sizeSpec 5 stop this inspector. Sources: `LVheap.HeapNode.parseRSRCData`, `updateData`, `NODE_SCOPE`; `LVmisc.readVariableSizeField{U124,S124,S24}`.

Names depend on the nearest parent class (`LVheap.tagIdToEnum` and `CLASS_EN_TO_TAG_LIST_MAPPING`). In particular, text-hair tag 1 is `OF__flags`, not the global `OF__activeDiag`. All final JSON/tree files use this context. [First-run log](first-run.txt) preserves the initial framing checkpoint and is superseded for contextual names. Printed short bodies are unsigned raw integers; compound data remains uninterpreted bytes.

## Decoded tree summary

Offsets below are decimal positions in the decompressed heap **including its four-byte length prefix**; they are not compressed-file offsets. The complete [tree](add.tree.txt) and [JSON](add.json) retain every entry and exact byte span.

```text
0004 rootObject class=oHExt UID=2
  0013 root class=diag UID=3
    0027 zPlaneList elements=4
      0033/0039/0045 references UID=162/120/78
      0051 arrayElement class=prim UID=43
        0065 termList elements=3
          0071 term UID=51 -> overridableParm UID=52
            0110 primIndex body@112=103
          0132 term UID=54 -> parm UID=55, parmIndex=1
            0169 primIndex body@171=103
          0179 term UID=57 -> parm UID=58, parmIndex=2
            0221 primIndex body@223=103
        0252 primResID body@254..255=1050
        0256 primIndex body@258=103
    0263 nodeList elements=2
      0269 arrayElement class=sRN UID=7
        0282 termList elements=3
          0288 fPTerm UID=78 -> DCO reference UID=76
          0403 fPTerm UID=120 -> DCO reference UID=118
          0518 fPTerm UID=162 -> DCO reference UID=160
      0656 reference UID=43
    0664 signalList elements=3
      0670 signal UID=173 -> terminal UIDs [51,162]
      0712 signal UID=130 -> terminal UIDs [120,54]
      0754 signal UID=88  -> terminal UIDs [78,57]
    0798 bgColor; 0804 firstNodeIdx
  0809 pBounds; 0820 dBounds; 0831 origin; 0837 instrStyle
0840 close rootObject; end=842
```

`SL__prim=47`, `SL__term=21`, `SL__fPTerm=22`, `SL__signal=23`, and the `OF__primIndex=202`/`OF__primResID=203` names are parser-source identifications (see `LVheap` enum definitions and [labels](heap-labels.json)); UID values, body values and endpoint references are original-byte observations. The `sRN` scaffold is also present in the empty fixtures. The primitive is serialized in zPlaneList and referenced from nodeList; treating both occurrences as independent primitives would double-count it. The endpoint lists establish connectivity as stored, without asserting wire direction or arithmetic behavior.

## Fixture comparison and checks

| pylavi fixture | Heap bytes | Entries | Result |
|---|---:|---:|---|
| add.vi | 842 | 162 | Complete, balanced |
| empty.vi | 128 | 23 | Complete, balanced |
| empty_separate_code.vi | 128 | 23 | Complete, balanced |
| add_breakpoints.vi | 854 | 165 | Complete, balanced |

[Comparison](comparison.json) records all input/heap hashes and tag/class counts; [run evidence](comparison-runs.json) records argv, exit status and output. Both empty heaps are identical. Relative to those empties, add introduces primitive/terminal classes and fields including primIndex, primResID, dco, parmIndex and compressedWireTable; nodeList, termList and signalList themselves already exist in the empties. Those differences locate diagram-content candidates, not an arithmetic oracle. `add_breakpoints` retains the same named-tag set despite three additional entries; names alone cannot identify a breakpoint encoding.

[Verification](verification.json) passes all 373 entries against the pinned upstream attribute/body reader: end offsets, attributes and raw content match. The source method is extracted with AST and its semantic-content callback is stubbed, so this is a field-grammar cross-check, not full upstream semantic validation. Truncation, reserved-scope rejection, extended tags and variable-width escape fields also pass. The issue's `heap-decode:`/`poc-feasibility:` marker check passes. No tests use LabVIEW or expected arithmetic answers.

## Candidate logic field and exact mutation

The discriminator candidate is the primitive's `OF__primIndex` at heap offset **258**, one byte `67` hex / 103 decimal. The same value occurs in its three terminal DCOs at **112, 171 and 223**. A concrete **syntactic experiment** changes all four bytes `67 -> 68` (103 -> 104), retaining `primResID=1050` at offsets 254–255. Excluding the leading heap UInt32, the four offsets are 108, 167, 219 and 254. [Candidate evidence](candidate-change.json) pins the input hash, all replacements, resulting heap hash/checksum, and successful 162-entry reparse/zlib round trip.

Index 104 is a deliberately hypothetical replacement, **not an identified Subtract primitive**. No inspected source establishes that 103 means Add, that 104 means Subtract, that they share a resource family/terminal contract, or that all four copies must change together. This candidate locates an editable logic discriminator and proves framing survives that mutation; it does not establish a valid functional edit. Obtain an independently authored Add/Subtract pair or an authoritative discriminator table before choosing a behavioral patch.

## Re-encoding and remaining gaps

Re-encode the changed heap with zlib beginning at BDHb payload offset 4; the stream must carry the new Adler-32. Preserve/update the outer uncompressed size (842) and inner heap body length (838) according to actual lengths. The existing BDHb payload starts at absolute file offset 4032, with its resource-length UInt32 at 4028. In this experiment default zlib produces a 477-byte payload, equal to the original; the same-length candidate would leave resource length, alignment and RSRC offsets unchanged. This size result is specific to the zlib version recorded in candidate evidence.

If compression changes the payload length, update that resource length and four-byte padding, subsequent resource data offsets, both RSRC headers' data size/metadata offset, and any metadata-relative offsets affected by rebuilding the map. Original header values from step 1 are data start 32, data size 4980, metadata start 5012, metadata size 1359. Recompression itself updates Adler-32; changing lengths alone does not.

Gaps: primitive mathematical identity/replacement compatibility; front-panel DCO names/types and terminal directions; compound label/image/rectangle bodies and wire routing; compressed-code/cache consistency; BDPW integrity rules and other heap invariants; encrypted/other heap formats and cross-version compatibility. No numeric constant value was identified in this heap. No claim extends beyond these four public fixtures. Opening a future edited VI without a broken arrow, observing changed behavior, and preserving the save version remain owner checks in an appropriate LabVIEW environment.

## What next

Use the saved tree and offsets to request a discriminator mapping or a controlled Add/Subtract fixture pair, then decide whether to perform the edit/rebuild step or record a semantic-evidence POC exit. Do not repeat the RSRC/decompression investigation or assume the filename is an arithmetic oracle. The parser and verifier run offline against the prepared fixtures; saved source snapshots avoid repeating network retrieval.

poc-feasibility: partial — structural diagram description and discriminator mutation measured; meaningful executable logic editing still needs primitive semantics, integrity handling and an owner runtime check.

heap-decode: yes — complete entry framing on add.vi (162 entries/842 bytes) and three comparison fixtures; evidence: add.json, add.tree.txt, comparison-runs.json and verification.json; semantic gaps remain explicit.
