# Policy check — iteration 0129, Policymaker #609

## Scope and sources

Read the five declared startup documents once, then `.session/startup.json`: ok, 16,127 estimated tokens, no notices. No suggestions or outboxes. `.session/exports/manifest.json` has no results. History manifest: checkout b03c26a9e8d85f25085619e401fbd1e98d73d87f, 129 records, 641 report snapshots. Baseline HEAD is that checkout; tree 673a0cea04ea5dc4fc385fe10ce09edea9840669.

Read selected tasks/outcomes from records [0126](../../.session/history/records/0126.json), [0127](../../.session/history/records/0127.json), [0128](../../.session/history/records/0128.json), excluding input_state. The first query unnecessarily printed full task bodies; later queries use selected fields. Exact trusted report snapshots:
- #601: `.session/history/sessions/601/37d677d796c4460ccc6c613d4952529a5bf7a502bca2cd20e4e3f8465bdec04a.md`.
- #604: `.session/history/sessions/604/9555aca246a03e77e03953bba86010e2c66d1acadfe84670e328ccdacd0c7d87.md`.
- #607: `.session/history/sessions/607/6ff9586cf491dac33de2ab374d3756d8cf25ce4c2deb4b7fb368e7d8a536213f.md`.

Read task-graph/session-protocol contracts, evaluation.md, operating-parameters.md, accepted-limits.md, current execution profiles, reviewer/orchestrator skills and journal memory. Read [handoff](../../benchmark/writing/reviews-0128/handoff-0128.md) and [findings](../../benchmark/writing/reviews-0128/c1-findings-0126.md) whole; inspected integrity accounting and metadata of completion/verification. Hashed five preserved byte streams. No fresh semantic review of raw cases, expectations, author/checker code, initial ledger or large comparison. No benchmark checker, builder, audit, trial or native execution. Semantic judgments below remain attributed reviewer findings.

## Findings before changes

1. #601 completed source-first review and one structural checker run, but ended partial because required full #597 was absent. Record 0126's task has `exports: []` while requiring the later author-report read. The shaper's report/history visibility does not establish worker visibility. #604 subsequently completed that read with explicit reports exports. This missing-read obligation is closed; do not repeat it.
2. #604 ended partial with required staged-input/output hashes unmeasured. Its report attributes this to unavailable hashing tools, but recorded action 13 (zero-based) successfully used role `Bash` with `python3`, `hashlib`, pathlib and subprocess. Exit 0 verified the repository pin, identities and ten scoped files. The 25-action history contains one Bash and no rejected Bash/hash action. The only error outcome is a missing-file Read at action 7. This contradicts a general Python-unavailable explanation; it does not prove that a particular unattempted command would succeed. Current reviewer profile already permits Bash(git:*) and Bash(python3:*). No profile expansion or engine capability defect is established.
3. #607 completed integrity accounting and preserved five compact originals, accepted/merged d6f7707. Its report says required preservation verification and preparation index check passed. This session confirms the five identities only, without rerunning those checks. Large comparison and original initial ledger remain release artifacts, not newly staged policy inputs.
4. Preserved Standards CLEAR / Spec NOT-CLEAR remain scoped to the C1 package. F1 is expectations `#/cases/7/atoms/11`: asserted inability differs from absence. The scenario supports inability correctness, but whether “in this scenario” counts as submitted grounding is unresolved. Interpretation A permits scenario reference; B uses only frozen bracket references and makes affected grounding incorrect. Under B N08 whole-answer grounding changes partial -> incorrect, while whole-answer correctness stays partial. Neither preservation nor policy selects a grading rule. Human C1 remains open.

## Measurements and attribution

All five current copies under `benchmark/writing/reviews-0128/` match fixed published lengths and SHA256:

| File | Bytes | SHA256 |
|---|---:|---|
| c1-artifact-manifest-0126.json | 28787 | 9a655f487a30539450c0abe36d4ebe570b43dc6fbddba914fae0fbd638121bc7 |
| c1-findings-0126.md | 7179 | 519fe802c72d1089b55425936ce31485d9d7502b2c602b72bdda92c11f4fbf41 |
| c1-pins-0126.json | 4511 | 916bd993cf979e0ff3810ac3503c9bb1008f6ed564749fd3c3962691698fd690 |
| c1-checker-run-0126.json | 2378 | 04a2146d44bfe5a1a9fb1a775bbec897df3db776c973550dc2569bb13527d49e |
| c1-review-completion-0127.json | 10038 | fc11233cd67752355607350a4a223395db07ee65a7933004517f85225d6cf600 |

Measured integrity-0128.json: 12665 bytes, SHA256 5e45a9eb16f047ab1eaecfb4dd68e3ed9ee034fb6e11321d9eed6a749ef842b4. Measured verification-0128.json: 1833 bytes, SHA256 e5ac1770f0411c771f2969caeb2788a660ede23ebeaaac645a21d72036712fc4. The integrity record attributes release/input and report-body measurements to #607. This policy session did not independently rehash unstaged releases or report exports. The large comparison remains iter-0126/601-c1-challenges-review-0126.json, 956134 bytes, SHA256 cf55770e01161a961b53cced969e81acb7c03223cf7bcf9ad061f38ecfc69e27. The initial ledger remains iter-0126/601-c1-challenges-cold-0126.json, 1428942 bytes, SHA256 32b3a36ad53b708726032a896d93a8cfe8cc1fa23bf6ddf77ebe65f28384a117, per #601.

Runtime evidence: use `git show cbc7b315c9692ade54466521abfbd235f0a4b5fc:sessions/604.json` for the action contradiction and sessions/600,601,603,606.json for actual candidates. #607's later runtime pin is 85534878f7d7a548686b0212b5b38cbdf90b04e7, path sessions/607.json. A combined query failed on the older pin's absent sessions/607.json after printing the other five summaries; the later pin resolved only that missing summary. No action replay occurred. All recorded actions in all six sessions used codex/gpt-6.1-sol. Each had one accepted Finish: #600 done/action19, #601 partial/action39, #603 done/action22, #604 partial/action24, #606 done/action25, #607 done/action23. All action numbers here are zero-based.

Records 0126–0128 total 8,535,313 input tokens, 65,434 output, 7,989,504 cache-read and zero cache-write, with zero limit hits. Verdicts none/none/accepted; current no_progress=0. These are usage observations, not normalized subscription quota or proof of savings. Another model family did not review this Codex-authored package. No comparative accepted-quality/quota evidence supports route changes.

Availability at pool pin cbc7b315c9692ade54466521abfbd235f0a4b5fc: Claude provider quota/session, observed 2026-11-14T05:23:04.537222Z, retry_after 08:03:04.537222Z; Codex provider available observed 04:24:45.337478Z, model available observed 06:32:28.843767Z; Copilot provider quota/unspecified observed 02:58:58.264814Z, retry_after 08:58:58.264814Z. Old model availability and retry times do not establish provider recovery. Only availability and selected runtime fields were printed; credentials were excluded.

## Changes and expected checks

- Orchestrator skill now requires explicit historical-report exports, availability inspection and preserved later-read ordering. Expected gain: prevent another report-only continuation like #601 -> #604. Next check: the next task requiring a report has explicit source=reports/session selectors, and the worker records availability without reading expectation-bearing content early.
- Reviewer skill now distinguishes in-session Python measurements from repository-only epilogue verification. Required measurements use allowed role Bash; unavailable tools or rejection need exact evidence. Expected gain: prevent a partial result based only on assumed hashing unavailability. Next check: required integrity work records actual argv/results, or the exact absent tool/rejection; no fabricated hash or permission expansion.
- Keep profiles, evaluator, routing, cadence and limits. Both local fixes address observed causes without new machinery. Empty orders: shaper owns ready F1 correction/recheck; no concrete evaluator defect or answerable audit task needs a policy order. No Owner request, private-data use, new publication category, spending or unavailable task.

## Next work and remaining limits

Reuse preserved #604 comparison and completed integrity accounting. The shaper can prepare a newly pinned local F1 interpretation, retain explicit project/map inability atoms and preserve original raw answers/hashes. A separate method/key review must recheck affected N08 atoms, honest-limits ID and whole-answer grounding. Actual human adjudication remains separate; agent agreement cannot supply it. Do not repeat cold derivation, full #597 comparison, preservation, historical checkers, #594 review or source-absence searches.

Benchmark readiness stays false. Actual inventory/dependency bytes, native keys, verified save-version preservation, withheld isolation, matched agent comparisons, human agreement and full artifact/version/hardware coverage remain missing. Tool quality remains unmeasured. Independent method review, owner acceptance, quality thresholds and all-version writing effort remain open. No accepted Goal gate or completion claim. #532 remains optional/pending without duplication or waiting.
