# Policy check, iteration 0147

Policymaker #671. Starting HEAD `3709db3eb849d90b7abb516d0e68c4d15b984798`, tree `936a20dc88a50d8a8b10ff6eec14434b89cc0e76`; measured clean. Startup documents were read once. Startup estimate: 15,866 tokens, no notices. This check directly considers records 0144–0146, selected older timing records and reports #663, #666, #668 and #669. Earlier results come through [predecessor memory](../working-memory.md) and [0144 evidence](0144-policy-check.md), not replay. History discovery: `.session/history/manifest.json`, checkout matching starting HEAD, 147 records and 690 report snapshots. Export manifest is empty; suggestions and Owner requests are empty. No benchmark checker, evaluator, model trial, reader or native execution was run here.

## Decisions and expected effects

Retain the shaper, profiles, routing, cadence, limits and evaluator. Records do not measure normalized subscription-quota use or comparable accepted quality. Mixed provider blocks cannot certify different-family review. Current no_progress=1 is consistent with a review reporting a new defect; it does not establish an evaluator defect.

Add one paragraph to `execution/roles/orchestrator/SKILL.md`: a narrow correction and its dependent changed-scope review normally share one graph. The reviewer pins the actual merged files and consumes named producer artifacts. Separate iterations remain appropriate when correction results are needed to define review. Record 0129 supplies a working precedent (#611 then #612, width 1); records 0145–0146 used two shaper sessions for correction then review. Expected gain: remove one redundant shaping session when the changed scope is already known. Check the next applicable graph for a correction, a `blocked_by` reviewer, explicit artifact inputs and independent pinning. This does not establish quota savings or relax review.

Order one bounded policy audit of completed-session recovery and missing outputs. Its question is distinct from benchmark correctness: why did #643/#653/#663 checkpoint a successful Finish, later require report recreation, and publish no artifacts? Use available Actions metadata and selected streams, with #669 as a control. The audit must separate established transitions from missing evidence. Expected gain: identify a specific recovery/output defect or an explicit measurement limit, then decide whether an engine-change request is justified. Wake Policymaker after the audit. No engine patch or Owner request is justified by the current evidence alone.

Execution work remains the shaper's responsibility: correct #669 F2 and independently review that changed path. Policy cannot order execution roles while the shaper is set. The shaper receives the graph instruction through its skill; policy memory is not visible to execution.

## Recent execution findings

- [#663 report](https://github.com/Kucze3205/ConnectWithLabview/issues/663#issuecomment-6891809187), snapshot `6a6052a8b7f41aa12af62c8571dcd51af1327fbf39f79402b95681520da5ea1d`: NOT-CLEAR for #659's three-file attempt-retention package. F1 high: inherited model/common-prompt/original-input/tool-content joins were omitted, admitting contradictory evidence with one synthetic completion. Reports 75 independent probes, 69 initially matched, five F1 variants and one corrected harness expectation. Record 0144 confirms zero uploaded artifacts; its ledger and scripts remain unavailable, not reconstructed. Broad normative excerpt and inherited exposure limit independence.
- [#666 report](https://github.com/Kucze3205/ConnectWithLabview/issues/666#issuecomment-6896487778), snapshot `1e8b07f2043351badd2420d653e38d686cf1360bd83b18e503368feeb41d97b7`: accepted/merged `cfce83a`, tree `be8501895b679cf3cad85c2308f5c77c9cbf01a7`. Reports pre-correction reproductions, new inherited joins, eight saved regressions plus 92 existing controls and 60 grouping controls. An initial correction broke missing-evidence diagnostics and was corrected. Record 0145 confirms 22 artifacts. These are author results, not independent closure.
- [#669 report](https://github.com/Kucze3205/ConnectWithLabview/issues/669#issuecomment-6896786397), snapshot `38fc61c9f34a2a7032d89e0c3280bd4b8cf7da1b2fe2cc65743c577f90c9ae6e`: NOT-CLEAR, F2 medium. F1 joins work on tested cases, but an attempt and attached record agreeing on an unplanned arm cause `legacy_result` to raise uncaught `StopIteration`. Validation rejects with slot identity, yet accounting loses the retained-attempt inventory. The old checker reportedly returned diagnostics. Record 0146 confirms 12 artifacts. Correction and narrow review remain required; no whole-package CLEAR.
- #669 reports 41 probes, 40 initial matches and one harness error: direct `accounting(..., consistent=True)` trusted the caller, while actual validation correctly suppressed completion. Preserve the original observation and adjudication. This caller contract predates the correction and is outside F1. Do not silently expand F2 into a general checker rewrite.
- #669 expectations reportedly preceded correction evidence. Runtime history confirms a saved expectations Write before reports #666/#663, correction note and checker reads. This supports the sequence, not blindness or unfamiliarity. Codex/Claude fallback retains earlier exposure. No repository writes or evaluator invocation were reported. No replay of its 41 probes is needed.

### Measured current identity, not semantic recertification

All five files match #666's report hashes and the corresponding `cfce83a` git blobs:

| File under benchmark/ | Bytes | SHA256 |
| --- | ---: | --- |
| attempt-evidence-0143.md | 12638 | 5d66520b202d01d48921cdd6bfc8146bc9692e4f7a62a0426f1b4a99d6adce79 |
| attempt-evidence-0143.json | 1240407 | 2489bf601856ddafc22315a67b0d076d316f793277e11e7e793261fba2e63651 |
| verify_attempt_evidence_0143.py | 23434 | f208c1f558537cb4dacaca6b2e60a4ebc5f133802c072d3697a823beb2cd7b98 |
| verify_attempt_evidence_f1_0145.py | 7186 | fb5f3dba19625cfcd51ee2feaf68274c21d5a0aede98f390d74d554ea50f4af9 |
| attempt-evidence-f1-0145.md | 5306 | b042d37a853a3c5af4ac4593ed8ce5906a5ba7c542c30630a1a3405091ed80c3 |

Read bounded checker excerpts: line 137 uses `next(...)` without a default; line 165 catches ValueError/KeyError/TypeError/UnicodeError, not StopIteration; line 271 evaluates every attempt's legacy result. This inspection corroborates the reported failure path without executing it. Do not claim a new reproduction. The correction should preserve rejection and zero completion while returning diagnostic inventories for unsupported arms. Use #669's exact reproduction artifact after availability/hash checks.

### Iteration/resource records

| Iteration | Verdict | Improved | Wall s | Critical path s | Input tokens | Output tokens | Cache-read share |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 0144 | none | false | 23649 | 44 | 2327591 | 36296 | .493 |
| 0145 | accepted | true | 1471 | 674 | 2018985 | 43599 | .608 |
| 0146 | none | false | 1330 | 606 | 1811643 | 30286 | .524 |

Each record has one execution task, zero recorded limit hits, no refused orders and no Owner requests. Session totals exclude Policymaker consumption. Wall time and reported critical path are not interchangeable; neither is subscription quota. Do not infer causal savings or provider superiority.

## Recovery discovery and audit evidence

Pinned runtime: `510fc5af213cbe9f66dde42a27e3467bc225afcd`, committed 2026-11-15T15:22:35Z. Inspected selected fields from `sessions/{643,653,663,669}.json` and availability-only pool fields. Credential values were not printed. Runtime source is available through `git show <pin>:sessions/N.json`; do not print entire records, request payloads or credentials.

| Session | First final checkpoint UTC | Later checkpoint UTC | Gap s | Final history extension |
| --- | --- | --- | ---: | --- |
| #643 | 2026-11-14 23:34:33 | 2026-11-15 00:33:13 | 3520 | Finish partial rejected for missing report; Write report; Finish partial |
| #653 | 2026-11-15 01:42:29 | 2026-11-15 07:02:51 | 19222 | Finish done rejected for missing report; Write report; Finish done |
| #663 | 2026-11-15 08:39:14 | 2026-11-15 14:35:51 | 21397 | Finish done rejected for missing report; Write report; Finish done |

Each first checkpoint already records an accepted Finish and a final result. The later history includes `Use Write to create .session/report.md before Finish` as the exact rejection. #663's earlier command output reports 21 verified indexed artifacts and existing report links. That is a saved command result, not recovered artifact bytes. Do not reconstruct those artifacts from runtime text. Final records confirm zero artifacts for all three sessions. Reports carry one kick each, at 00:30:08, 06:59:29 and 14:32:53 respectively. #669 has one final checkpoint, 12 published artifacts and no kick.

The correlation merits audit, but proves neither root cause nor that every zero-artifact session failed: many earlier tasks intentionally produced none. Two-checkpoint gaps do not measure runner-active time or the exact time data disappeared. All runtime `outputs_asset` fields inspected were null, including successful control #669; null alone cannot diagnose loss.

Bounded engine source inspection: `docs/perpetua/engine.md:301–307` says interrupted operations are not automatically replayed and a runner killed before upload loses session source. `.github/workflows/session.yml` packs/uploads results after the routed runtime and downloads them in epilogue; a diagnostic stream upload can fail without failing the session. `loop.py:1449–1465` treats queued/in_progress/waiting session runs as commitments; the watchdog can defer a kick while such a run exists. No Actions metadata was available in this session to establish what actually happened. Do not promote these possible explanations to findings.

Pool snapshots at first #653/#663 completion have recent Claude unknown/cooldown observations and Codex available observations. Later Claude is available. These do not establish the cause of the recovery gap or current entitlement. No route change follows from them. `docs/perpetua/operating-parameters.md` was read; owner safeguards and subscription-only limits remain unchanged.

## Recovery of this session

After the recorded accepted Finish, Read of `.session/report.md` returned FileNotFoundError. A direct Python existence check also found `.session/orders.json` missing. The shaper skill and policy memory retained their exact earlier hashes: 4aa723e17d5d4f5f1bc8c74c87b3f4b6f856298e1d2c905c899faaf419754ef4 and bccb0fb8af7317cb5257fa92b426eee1c40a22e2bfdeab778b183455265c561d. This evidence file existed at 12,027 bytes, SHA256 b8d454e0981657b052e9918f43dc4ead309aeaac331ca6f1792d3881cf21adcc before this addition. Recreated the missing report and restored the audit order from its recorded text. This establishes missing session files during recovery, not the cause or timing of their loss. Do not repeat completed benchmark work.

## Verification of this policy change

Read back the actual order and changed files. Direct Python checks passed for the audit role, model alias, effort, limits, dependency list, explicit exports and required task sections. The audit's repository-only verification command parses; it was not executed before the audit outputs exist. Compared the skill against starting HEAD: four added lines and no removed lines. An initial assertion incorrectly expected five added lines; inspected the actual diff and corrected that verification assumption, without changing the skill. Predecessor memory size/hash matched the pinned source. Whitespace check exited 0. No benchmark, evaluator or historical probe was executed. Memory decreased from 16,120 to 13,656 bytes; detailed evidence remains here and in prior observations.

## Continuing boundaries

Benchmark_ready=false. Real admissions, model/reader/native trials, semantic passes and real controlled comparisons remain unperformed in this work. Product quality is unmeasured. Human C1, trusted native/dependency evidence, enforced withheld allocation/isolation, matched settings/budgets/repeats, complete artifact/version/hardware coverage, independent whole-method review, owner method acceptance and quality thresholds remain missing. No accepted Goal gate exists. Full scope and all-version priority remain; no 2024 fallback was selected.

Do not reopen closed #656/#639/#633 reviews, reconstruct #653/#663 artifacts, replay #643's prohibited evaluator call, duplicate declined #618 or repackage human C1. Negative POC delivery and its limits remain in predecessor memory. Audit addresses recovery only; it cannot establish benchmark readiness or repair historical process claims.
