# Constant-pair encoding and integrity investigation (#533, iteration 0106)

## Inputs

**Verdict: source-blocked.** [Evidence JSON](constant-rules-0106.json) records 38 repository SHA256 pins, eight prepared-file pins, source revisions, bounded node contexts and ten probes; `P0` verifies both separate VI hashes against the saved comparison, manifest and replay before probing (normal originals also match).
Continue accepted #528: [findings](findings-0105.md), constant-only `bdhb_alignments` in [candidates](candidates-0105.json), [separate](constant-1-separate--constant-2-separate.json)/[normal](constant-1-normal--constant-2-normal.json) comparisons, [replay status](replay-0105-status.json), [pins](fixtures/pins.json), and [authoring](fixtures/authoring.md).
Author reports Windows 11, LabVIEW 2026 26.1.1f1 32-bit and I32 1→2; no native execution is possible here. `repository_revision` identifies the evidence checkout; the new probe script has its own SHA256.
Prepared pylavi is clean at `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75`; saved pylabview snapshots are at `5f20e23de6a386021eb955c825cc43d221f09ff1` ([provenance](../source-provenance.json)). JSON `source_pins`/`repository_source_pins` identify original paths, hashes and exact symbols/lines.

## Findings

`P1`: decompressed offset [312,316) in constant-2 parses as a complete leaf `4420 | 0200`: sizeSpec 2, scope 1, tag 1; body [314,316). Its parent is `OF__textRec` at 306, class 1 (`textHair`), inside the numeric display. Source [LVheap](../LVheap-source.txt) lines 735, 1113–1130 and 1489–1530 names this child `OF__flags`; it precedes the unchanged `mode`/background children. The aligned insertion therefore has parsed boundaries independent of the value body; the source does not explain flag `0x0200` or why it appears.
`P2`: header `866c` names tag 589 `OF__ConstValue` with sizeSpec 4: node [540,546)→[544,550), body [542,546) `00000001`→[546,550) `00000002`. Thus left 545/right 549 are the last body byte, not tags or length fields. Parent `bDConstDCO` class 19 has UID 118; heap type-reference bodies remain `03` for the DCO and `04` for its `stdNum` display (LVheap lines 397, 693, 750, 809, 1747–1761, 2555–2561).
`P1/P8`: heaps consume 674→678 bytes, with inner lengths 670→674 and outer decompressed sizes 674→678. Both normal and separate modes have identical corresponding BDHb raw/decompressed payloads and the same insertion/value transition; this resolves this alignment, not a general required insertion rule.
`P8`: normal DFDS additionally changes only decompressed offset 223 `01→02`; separate files have no DFDS. VCTP/DTHP remain byte-identical within each logic pair but differ across save modes. Normal VICD remains equal despite the constant/DFDS changes; code retention, data binding and type rebuild rules do not follow from equality.
`P5`: pylavi `pylavi/resource_types.py:54–93` (`TypeBDPW`) derives only chunk 0 from MD5 of an ASCII password. On all four constants, chunk 0 equals MD5(empty), `has_password=false`, empty-password comparison is true, and LVSR's source-defined locked bit is clear. This tests password classification only; it neither verifies nor bypasses integrity.
`P7`: both constant save-mode comparisons have equal BDHb and different BDPW chunks 1/2, refuting dependence on BDHb alone. RTSG is equal across modes for each value and changes 1→2 in both modes; this correlation supplies no RTSG derivation or integrity role.
`P4/P6`: all six prepared pylavi production-file hashes exactly match the [prior source search](../step3/source-search.json). Reuse that search's heap/type/integrity absence and stop that branch. Prepared roots are actor-framework/pylavi/readiness.json; scoped `LVblock*`, `LVdatatype*`, `LVrsrc*` inventory searches return no files. `TypeBDPW` and `tests/test_resource_type_BDPW.py:test_basics` provide no chunk-1/2 digest inputs, ordering, version gates or update rule; no speculative recipes were tried.
`P9`: pylavi `TypeLVSR` lines 97–121/205–215 explains the separate-code mask, matching payload word [8,12) `20000200`→`20000600`. It does not identify changed LVSR [52,68), [80,96), [120,136) regions or their dependencies on BDPW/RTSG.

## Not established

`P3`: four big-endian bytes agree with the author-reported I32 values, but heap type IDs are not independently resolved. LVheap `HeapNodeTDDataFill.findAndStoreTD` lines 1969–1979 needs absent `getHeapTD`; typed dispatch covers StdNumMin/Max/Inc (2590–2594), while ConstValue reaches generic `HeapNode` (2796–2840). The prior typed-constant blocker remains.
`P6/P9`: BDPW tails, RTSG/LVSR integrity roles, textHair flag semantics, and code/data/type dependencies remain unknown. The normal DFDS correlation supplies no standalone encoding/edit rule. There is no unchanged-diagram Save As/re-save control separating churn from the intended value change.
No LabVIEW ran; parser completeness and hash agreement establish neither native behavior, an unbroken arrow, edited-VI validity, save-version preservation, native 2024 support nor all-version compatibility. No original VI, reviewed file, replay output or saved pin changed; no VI was rebuilt, cache deleted or target resource transplanted.

## Verdict

**source-blocked:** node/value/length boundaries are supported for these originals; sufficient typed editing and integrity rules are unavailable. A bounded VI edit is not justified by this evidence.
Run `python3 docs/research/poc/pair/check_constant_rules_0106.py`: it checks committed hashes/schema, prepared-pin format and prior-pin consistency, reparses original bounded contexts and checks conclusions without environment/session access. Even `rules-supported` would not establish native validity; this record retains the negative verdict.
The session-only [probe](probe_constant_rules_0106.py) uses `LABVIEW_ENVIRONMENT`; it is not imported by the offline check. Resume from this JSON and the prior source search; do not rerun replay, pin creation, the mutating self-check or corpus discovery.
Smallest next step: stage one pinned primary-source implementation or specification of BDPW chunks 1/2 for these save-version declarations, then test only its explicit dependency recipe against the same four originals.
