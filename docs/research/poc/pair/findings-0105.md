# Controlled owner-pair replay (#528, iteration 0105)

## Inputs

**Measured; verdict: edit-attempt-needs-more.** All eight comparisons exited 0; no VI was written and no LabVIEW ran.
[Authoring record](fixtures/authoring.md): the owner reports Windows 11, LabVIEW 2026 26.1.1f1 32-bit, I32 terminals, unchanged wiring, no password or warnings, and only the separate-code setting intentionally varied.
These are author claims; this session observes bytes and parser results.
[Verification](verification-0105.json) `checks` matches all eight VI hashes and authoring.md against [pins.json](fixtures/pins.json), and all four reviewed files against [review-0102.json](review-0102.json), before tool execution.
Review pins identify commit `8f5ae4c48581459aa09b3f5e56f79db56188b86c`; the loader pins pylavi `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75` and checks source hashes/readiness in each output's `loader_provenance`.
Run from repository root: `python3 docs/research/poc/pair/replay_0105.py`.
[Replay status](replay-0105-status.json) records each exact `runs[].argv`, `exit_code`, output path, original fixture/manifest hashes, and `unchanged_inputs_after: true` (including reviewed files).
The reviewed self-check was not run because it rewrites tracked evidence (R1); neither pins nor reviewed files were regenerated.
All measurements below cite `resources[]` by type/ID/occurrence; IDs/occurrences are 0/0 unless specified. Raw offsets exclude the outer length word; decompressed offsets include the inner heap-length prefix.
[Derived candidates](candidates-0105.json) retain source-output hashes, inventories and byte alignments; reproduce with `python3 docs/research/poc/pair/summarize_0105.py`.

## Logic pairs

The output links supply `whole_file`, `differing_resources`, `resources[].raw`, `.decompressed`, and `.present_in_one_only` for these measurements:

| Pair/output | File bytes left→right | Resource counts | Changed resources | BDHb raw bytes | BDHb decompressed bytes; positional differing bytes |
|---|---:|---:|---:|---:|---:|
| [Add→Subtract, normal](add-normal--subtract-normal.json) | 6334→6335 | 42→42 | 10 | 494→495 | 857→857; 30 |
| [Add→Subtract, separate](add-separate--subtract-separate.json) | 4128→4129 | 24→24 | 4 | 494→489 | 857→849; 630 |
| [1→2, normal](constant-1-normal--constant-2-normal.json) | 5937→5941 | 43→43 | 6 | 489→493 | 674→678; 350 |
| [1→2, separate](constant-1-separate--constant-2-separate.json) | 3919→3923 | 24→24 | 5 | 489→493 | 674→678; 350 |

No resource is added/removed in a logic pair. Only LVSR resource names change, encoding the respective filenames (`left/right.name_hex`, `name_changed`).
Normal Add/Subtract changes BDHb, BDPW, BFAL, GCDI, HIST, LVSR, MUID, NUID, SUID and VICD; separate changes BDHb, BDPW, HIST and LVSR.
Normal constants change BDHb, BDPW, DFDS, HIST, LVSR and RTSG; separate constants change BDHb, BDPW, HIST, LVSR and RTSG.
Other than BDHb and normal Add/Subtract VICD (875→872), changed logic-pair payload lengths remain fixed; inventories are in `comparison_summary[].resource_inventory` of the derived candidates.

Candidate primitive-associated observations: normal BDHb offset 237 changes `1a→1b`; separate BDHb contains the same candidate transition at left 237/right 232 after alignment.
Normal GCDI decompressed offset 58 also changes `1a→1b` (89-byte heaps). These correlate with the owner's replacement; they do not establish primitive IDs or terminal meaning.
The normal BDHb has 29 positional ranges, including repeated `67→68` at 94, 153, 205 and 240 and numerous other changes; no individual repeated byte is assigned arithmetic semantics.
Separate BDHb has 36 positional ranges. `bdhb_alignments[1].edits` suggests removal of `643a020003` at left 229 and `247201` at left 816, alongside changed bytes at other offsets; this is an ambiguous byte alignment, not a parsed deletion rule.
Normal VICD decompresses to 1764 bytes on both sides; offsets 701–703 change `090308→002b01`, and 705 changes `8e→86` (`decompressed.ranges`).

Candidate constant-associated observations repeat exactly across both save modes: the entire corresponding BDHb payloads match across modes (`raw.different: false` in constant save-setting outputs).
The positional comparison includes heap-length byte 3 `9e→a2` and many shifted ranges starting at 312; it does not represent 350 independent semantic edits.
`bdhb_alignments[2/3].edits` aligns these heaps as insertion of `44200200` at 312 and value byte `01→02` at left 545/right 549, besides the length-prefix change.
This localizes a candidate value and accompanying encoding change; it does not prove the four inserted bytes' type/tag meaning or a general I32 encoding rule.
Normal DFDS additionally changes decompressed byte 223 `01→02` (300-byte heaps, 108-byte compressed payloads); DFDS is absent in separate files.
Normal constant VICD is byte-identical (798 bytes), despite the observed BDHb/DFDS changes; no explanation of executable data binding is established.

BDPW in **all eight** outputs is 48 bytes: `chunks_16_bytes` indices 0/1/2 at offsets 0/16/32, with `chunk_alignment_valid: true`.
Chunk 0 stays `d41d8cd98f00b204e9800998ecf8427e`; chunks 1 and 2 change in every comparison (32 differing bytes). Exact values remain in each named JSON.
Because BDPW also changes in save-setting pairs with identical BDHb, it cannot be treated as a function of BDHb alone from these observations. Its derivation and integrity role remain unknown.

## Save-setting pairs

Evidence fields are the same as above plus `code_resource_presence` and LVSR `version_fields`:

| Output, normal→separate | File bytes | Resource counts | Changed resources | BDHb raw / decompressed | VICD raw presence/length | CPC2 bytes |
|---|---:|---:|---:|---|---|---|
| [Add](add-normal--add-separate.json) | 6334→4128 | 42→24 | 27 | 494/857 unchanged | 875→absent | `0018→0002` |
| [Subtract](subtract-normal--subtract-separate.json) | 6335→4129 | 42→24 | 29 | 495/857→489/849 | 872→absent | `0018→0002` |
| [Constant 1](constant-1-normal--constant-1-separate.json) | 5937→3919 | 43→24 | 28 | 489/674 unchanged | 798→absent | `0010→0002` |
| [Constant 2](constant-2-normal--constant-2-separate.json) | 5941→3923 | 43→24 | 28 | 493/678 unchanged | 798→absent | `0010→0002` |

CPC2 remains present, two bytes, in every file; each logic pair preserves its CPC2 bytes. VICD is present only in normal files. Presence is not evidence of cache validity.
Common normal-only resources: BFAL, BNID, CCST, CPMp, DFDS, DLDR, FPTD, GCDI, GCPR, LIds, NUID, SCSR, SUID, TM80, VICD and vers IDs 7–10; constants additionally lose CNST (8 bytes).
All four separate files add VITS (53 bytes). Exact removed lengths and retained lengths/hashes are in each `resources[]` and the derived inventory.
Retained DTHP stays 4 bytes but changes; VCTP raw sizes are 295→83 for arithmetic, 258→70 for constants, with decompressed sizes 675→232 and 591→208 respectively.
FPHb raw sizes are 925→916 for arithmetic (heaps 2746→2743; 65 positional differing bytes), 713→715 for constants (heaps 1274→1274; 3 differing bytes).
Subtract additionally changes BDHb (627 positional differing bytes) and MUID; the author's unchanged diagram therefore does not imply identical diagram serialization across save settings.
HIST, BDPW and LVSR names also differ in every save-setting comparison; other retained resources are unchanged except LVSR payload changes described next.

LVSR is 160 bytes everywhere. `version_fields.*.flags_hex` records all 156 bytes after the version word; the field name covers more than the single flag word.
Payload bytes 8–11 change `20000200→20000600` in every save-setting pair: raw byte 10 is `02→06`, and `separate_code_parser_flag` changes false→true.
Within each logic pair that word and parser flag stay fixed. Separate Add→Subtract and separate 1→2 also change raw byte 26 `02→22`; no meaning is assigned to it.
LVSR ranges at 52–67, 80–95 and 120–135 differ in logic pairs and in the Subtract/constant-2 save-setting pairs (some equal bytes split ranges).
Those regions stay unchanged in Add and constant-1 save-setting pairs. Filenames and the HIST changes demonstrate save-related differences; the other regions' identities/causes remain unproven.

## Version fields

Every file has LVSR/0 raw declaration `26008000`, parser tuple `[26,0,0,4,0]`, parser value `26`; every file has vers/4 `26118001`, tuple `[26,1,1,4,1]`, value `26.1.1f1`.
Normal files also have vers/7 and /9 `26008000`, and vers/8 and /10 `26118001`; those four resources are absent in separate files.
See each output's `version_resource_presence` and `resources[].version_fields.{left,right}.{raw_hex,tuple_major_minor_patch_phase_build,parser_value}`, or derived `version_declarations`.
No present declaration changes within a logic pair or within retained save-setting resources. These are distinct version declarations, not proof of identical meanings, a native load, or future save-version preservation.

## Not established

No native execution, behavior, unbroken arrow, unchanged terminal interpretation, valid edited artifact, save-version preservation, native 2024 support or all-version compatibility was measured.
Parser success cannot independently confirm the author's no-warning/wiring claims. Positional comparisons exaggerate shifted tails; SequenceMatcher correspondences remain hypotheses.
There is no unchanged-diagram repeated-save/Save As control isolating serialization churn, filename changes, history and identifier-like regions from the requested logic change.
BDPW derivation, LVSR integrity/identifier fields, compiled-code/data/type dependencies, and safe rebuild or invalidation rules remain unresolved. VICD absence does not justify deleting code resources, and constant VICD equality does not justify retaining it after edits.
No product, VI patch, cache deletion or old 103/104 mutation inference was used; original fixtures and the four reviewed files remain unchanged.

## Verdict

**edit-attempt-needs-more.** The eight owner pairs localize repeatable candidate constant spans and a primitive-associated transition, while exposing save-dependent type/code resources and unrelated Save As changes.
The smallest next measurement is a pinned, same-version, unchanged-diagram Save As/re-save control for constant-1-separate, compared with the existing baseline using the same read-only protocol; compare BDHb, BDPW, HIST, LVSR names and raw ranges before attributing churn to logic.
That control alone will not make editing safe: source-grounded encoding/length rules and BDPW/code/integrity handling must explain the candidate insertion, DFDS/VCTP dependencies and observed save-mode differences before an edit attempt.
Resume from the saved JSON and candidate alignment; do not rerun pin creation, the mutating self-check, RSRC discovery or benchmark preparation. This report makes no owner request and no commit.
