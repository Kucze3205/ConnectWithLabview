# Bounded unsuccessful POC delivery

**Outcome: unsuccessful within the inspected scope.** Eight selected original VIs parsed, but no supported executable semantic edit was established. No changed VI and no fresh-agent edit demonstration were produced; no session ran LabVIEW. This closes this bounded attempt under the [goal's unsuccessful-POC provision](../../../goal/goal.md#proof-of-concept), without changing the goal or claiming editing impossible in general. [Machine-readable delivery](delivery.json); [step-3 verdict](edit-readiness.md), [requirements and pinned evidence](edit-readiness.json).

## Criterion accounting

| Goal criterion | Status | Exact evidence and limit |
|---|---|---|
| Demonstrates that the concept works and a finished product can exist | Unestablished | [Bounded negative verdict](edit-readiness.json): structural reading and syntactic mutation do not demonstrate semantic editing feasibility; this result also does not prove impossibility. |
| Agent has not previously seen the VI | Not attempted | [Working memory](../../../journal/working-memory.md#state) records no successful cold-agent demonstration; public fixtures cannot establish model-unseen provenance. |
| Correctly describes its diagram | Unestablished | [Original tree](add.tree.txt), [structural comparison](comparison.json), [verification](verification.json): 162 entries consume 842 bytes for add.vi; stored endpoint pairs and source-derived names are established, mathematical meaning, terminal direction and complete semantic description are not. |
| Changes diagram logic without LabVIEW | Not attempted | [Syntactic candidate](candidate-change.json) changes only an in-memory heap; `vi_written=false`, `LabVIEW_tested=false`. [Readiness](edit-readiness.json) has `recipe=null`, `edited_vi=false`; there is no supported semantic replacement. |
| Result opens without a broken arrow | Not attempted | [Runtime requirement](edit-readiness.json): no changed VI exists and no LabVIEW check occurred. |
| Result behaves as requested | Not attempted | [Semantic/runtime gaps](edit-readiness.md): neither an executable edit nor behavioral validation exists. |
| Result preserves save version | Unestablished | [Original declaration](README.md#artifact-and-primary-source-provenance) is `21008000`, LabVIEW 21.0.0 final build 0; unchanged copying preserves bytes, but no changed artifact demonstrates version preservation. |
| Deliver files, report and short manual instructions | Established | This report, [manifest](delivery.json), retained [inspector](inspect_vi.py)/[labels](heap-labels.json), original artifact and instructions below deliver the permitted failure package. This does not satisfy the missing changed-VI criterion. |
| On failure, show evidence and possible exits | Established | [Saved negative result](edit-readiness.md#what-next), blockers and two exits below. |
| POC precedes further benchmark preparation | Established | This bounded failure package supplies the permitted delivery before resuming preparation; [working memory](../../../journal/working-memory.md#state) records the pause. No benchmark changes are made here. |
| POC is separate from product and quality proof | Established | Retained code is research; the [goal](../../../goal/goal.md#proof-of-concept) requires the normal testing/review path before product use. This task changes only delivery files and session outputs. |
| Continue after delivery without waiting for owner | Established | Resume instruction below directs benchmark preparation; this document does not claim benchmark readiness or select benchmark work. |
| Silence is not method, quality or product acceptance | Established | Explicit [goal provision](../../../goal/goal.md#proof-of-concept); no acceptance or goal completion is claimed here. |

## Original and retained evidence

Original prepared input: `@environment/pylavi/tests/add.vi` (commands: `$LABVIEW_ENVIRONMENT/pylavi/tests/add.vi`), upstream [pylavi tests/add.vi at 35d2a0318f71dcb87bb9c431dc00700ee6b9fb75](https://github.com/marcpage/pylavi/blob/35d2a0318f71dcb87bb9c431dc00700ee6b9fb75/tests/add.vi), [Unlicense](step3/pylavi-LICENSE.txt). Size **6,371 bytes**; SHA256 **cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8**; declared save version **21008000 / 21.0.0 final build 0**, as recorded in the [pinned README](README.md). The unchanged session copy is [poc-original.vi](../../../.session/artifacts/poc-original.vi); [verification record](delivery-verification.json) records the separate source/copy hash check. That binary is a session artifact, not an offline-verifier dependency or an edited result.

Retain the [inspector](inspect_vi.py), [contextual labels](heap-labels.json), [source provenance](source-provenance.json), [pylabview MIT license](pylabview-LICENSE.txt), [pylavi provenance](step3/source-provenance.json), [comparison runs](comparison-runs.json), [candidate mutation](candidate-change.json), [step-3 fixture probe](step3/fixture-probe.json), [constant candidate](step3/constant-candidate.json), [source search](step3/source-search.json) and [verification limits](step3/schema.md). Existing evidence, verifiers and README remain unchanged; this delivery links them without rewriting them.

## Why no executable edit was delivered

[Readiness](edit-readiness.md) identifies four specific blockers. **Semantics:** `primIndex=103`, `primResID=1050` and endpoint pairs do not establish Add identity, Subtract identity for 104, direction, or a compatible terminal/resource-family replacement. The four `67 -> 68` heap-byte changes prove framing survives only. **Type encoding:** the two `ConstValue` bodies `00000001` and `000000055c2e76693a` and type-reference bytes do not establish typed values or replacements. [LVheap](LVheap-source.txt) lines 1969–1979 call `getHeapTD`; lines 2590–2594/2814–2815 select the numeric reader for range fields, not ConstValue. DTHP/VCTP indirection and actual constant encoding remain unresolved.

**BDPW:** [pinned TypeBDPW](step3/pylavi-resource-types-source.txt) lines 54–93 reads 16-byte chunks and checks password chunk zero; the last 32 bytes of add.vi's 48-byte BDPW lack an inspected derivation/update rule. **Compiled cache:** [inventory/search](step3/source-search.json) and [fixture probe](step3/fixture-probe.json) show VICD (968 bytes) and CPC2 (2 bytes), without a safe invalidation/regeneration or dependent-flag rule. Missing matches do not establish absence of integrity rules. [Container recompression and offset requirements](README.md#re-encoding-and-remaining-gaps) are necessary structural steps, insufficient for semantic or runtime validity.

## Two concrete exits

1. **Controlled same-version fixtures:** obtain independently authored, documented connected I32 1-to-2 or identified Add/Subtract pairs with unchanged terminals, normal and separate-compiled-code variants. Pin hashes, authoring/save settings and exact requested change; compare type/value spans, every BDPW chunk, LVSR flags and code resources. This can establish identity/value spans and candidate dependencies. Differences alone do not prove general integrity/cache rules, all-version compatibility or a valid future edit.
2. **Missing pinned source rules:** obtain relevant LVblock/LVdatatype/RSRC implementations for BDPW derivation, compiled-cache/flag handling, DTHP/VCTP indirection and ConstValue encoding; pin revision, original paths, license and hashes. These can supply an executable encoding/rebuild contract. Source rules alone do not prove correctness on this VI, a fresh-agent demonstration or LabVIEW behavior. This session performs no new format research, corpus expansion, speculative disk patch or cache deletion.

## Owner reproduction and limits

Run the following from the repository root, substituting the session artifact's downloaded path if necessary:

```text
python3 -I docs/research/poc/inspect_vi.py .session/artifacts/poc-original.vi
python3 -I docs/research/poc/verify_delivery.py
python3 -I docs/research/poc/verify_edit_readiness.py
```

The inspector needs [heap-labels.json](heap-labels.json) beside it for source-derived names. Exact earlier commands/output are retained in [comparison-runs.json](comparison-runs.json) and [verification-run.txt](verification-run.txt); [verify_poc.py](verify_poc.py) requires the prepared four-fixture environment and rewrites its evidence, so it is not this delivery's offline check.

In an appropriate LabVIEW installation supporting the original declared save version (preferably the same version), open a disposable copy of the original, inspect its front panel and block diagram, and record the editor version and any load/dependency diagnostics. Avoid saving over the original. This inspects the original only and **cannot validate a changed VI because none exists**. Future changed-VI checks remain outstanding: open without a broken arrow, observe the requested behavior, and verify preserved save version and runtime validity. They require an actual changed artifact and an appropriate LabVIEW environment; this session cannot run LabVIEW. Passing the offline command validates failure-delivery consistency only.

## What next

Return to benchmark preparation after this delivery, without waiting for owner action; silence is not acceptance. First read [role contracts](../../perpetua/roles.md), [evaluation/readiness contract](../../perpetua/evaluation.md), [benchmark preparation status](../../../benchmark/preparation-status.json), and the relevant actual paused-thread evidence selected using [working memory](../../../journal/working-memory.md). Its inherited pointers include split allocator #446 re-review, native #169, and writing-method coverage; do not repeat declined #430 unchanged. Do not implement the product or change benchmarks in this task. Preserve the saved candidates; do not rediscover RSRC framing or treat filenames, raw integers or 103/104 as an arithmetic oracle.

The requested `.session/loop-state.json` was absent (FileNotFoundError); `.session/history/manifest.json` contained zero records. Criterion accounting therefore uses the committed goal and saved working memory rather than inventing missing session state. No goal gate or method acceptance is inferred.
