# POC: inspect one public VI without LabVIEW

## Measured result so far

The RSRC container and compressed block diagram of `pylavi/tests/add.vi` are readable without LabVIEW. Diagram semantics and an executable logic edit remain unverified; this is an initial research checkpoint, not a successful editing demonstration.

## Selected artifact and provenance

- Original path: `$LABVIEW_ENVIRONMENT/pylavi/tests/add.vi` (prepared public source, read-only).
- Upstream: https://github.com/marcpage/pylavi/tree/35d2a0318f71dcb87bb9c431dc00700ee6b9fb75 ; license: Unlicense.
- File size: 6,371 bytes; SHA256: `cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8`.
- RSRC format: 3, file type `LVIN`, creator `LBVW`.
- Saved-version bytes: `21008000`, representing LabVIEW 21.0.0 final build 0, in `LVSR` at absolute offset 36 and every observed `vers` entry (IDs 4, 7, 8, 9, 10; offsets 1532, 1548, 1564, 1580, 1596). These are original artifact declarations, not runtime compatibility evidence.

## Observations from original bytes

`BDHb` resource 0 has a 477-byte payload at absolute offset 4032. Its first four bytes are `0000034a` (842); zlib decompression beginning at payload offset 4 returns exactly 842 bytes. Decompression at offsets 0 and 8 fails. The decompressed prefix is `00000346101802fe007efd000210f502fe001bfd000364cb084000114e01fb0004`; the leading UInt32 is 838, equal to the remaining decompressed byte count. This exposes a compact binary heap, not textual node or primitive names.

The source inventory and container interpretation reuse the research in [0002-delivery.md](../0002-delivery.md), `benchmark/scripts/sources.py::save_version`, and pinned upstream `pylavi/pylavi/file.py`. None of those sources decodes block diagram semantics. `benchmark/native/readiness-case.json` supplies saved-property expectations for other public fixtures, not an arithmetic oracle for this file. The filename `add.vi` is a selection hint, not evidence that its diagram performs addition.

## Explicit gaps and candidate change

Nodes, primitive identities, constant values, terminal identities, wire endpoints and execution behavior have not yet been decoded. The candidate is to replace an arithmetic Add primitive with Subtract if a primitive discriminator and compatible terminals can be established from evidence. No responsible byte patch can yet be specified; locating that field is the next measurement.

## Container consistency and native risk

The original header declares data offset 32, data size 4980, metadata offset 5012 and metadata size 1359; its duplicated header starts at 5012. A changed compressed payload needs its resource length, four-byte alignment, subsequent resource offsets, both headers' data size and metadata offset, and any affected metadata-relative offsets kept consistent. Recompression must update the zlib stream and its Adler-32 checksum; a same-length decompressed edit preserves the outer uncompressed-size prefix and inner heap length. Unknown semantic signatures, compiled-code consistency and heap invariants remain gaps. `BDPW` contains 48 bytes; the pinned pylavi parser identifies the first 16 as a password MD5 but does not establish the meaning or update rules of the remaining bytes.

No LabVIEW was executed. Opening without a broken arrow, changed behavior and preservation of the save version after an edit remain owner checks. A byte-level decoder or successful decompression alone cannot establish them.

poc-feasibility: partial — container and diagram decompression measured; semantic decoding and a concrete patch are still under investigation.
