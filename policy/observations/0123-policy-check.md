# Policy check 0123 — Policymaker #589

## Scope and sources

Considered iterations 0120–0122 through `.session/history/manifest.json`: records `0120.json`–`0122.json`, task
bodies and these trusted report snapshots under `.session/history/sessions/<issue>/`:

- #581 reviewer: `57400a385d1a0be55b6b28e13a95c1088d45379d400b2cf5814ade9804d8b8c2`.
- #584 benchmark: `8efd2c135225a9fe28bfb2c68543a0512353288b3a8492baa6fa83e0950db737`.
- #586 shaper: `4872a1f0ceb2ee20e28d0883cbeae6de2c851dcf6057a8bdf26115f1b416c3e6`.
- #587 reviewer: `9a349ed01acce9c301db87334db5a94e43f00e8f6a77d27606335d9fd8284472`.

Runtime evidence: `origin/loop-runtime` at `533a7411ff9549edd3c82fcd09dedbd8cb1af011`; read candidate sequences,
Finish calls and Write targets from `sessions/{580,581,583,584,586,587}.json` and provider availability from
`pool.json` (last commit `33bf594e3c82fde60a556435db7dd78d3d4a60bc`, 2026-11-14T02:18:22Z). Checkout HEAD
`50bfbe4cbf94ec0ffbc4bd39f8c512bc777fa2fb`, tree `8fda972a7d960fd578a13282ce48ffc21e31f36f`. Read
`journal/working-memory.md`, all `execution/` definitions, `.github/loop/task-graph.md` and the audit skill.
This session ran no checker, audit or probe and did not open the 0121 package, the review artifacts, `method.json`
or `protocol.md`. Package and review content below is report evidence, not measured here.

## Result of the #579 reviewer reorder (measured from runtime histories)

Action indexes are zero-based positions in `history`.

| Session | Role | Candidate sequence | Evidence written by |
|---|---|---|---|
| #577 (0119) | benchmark author of key 0119 | Codex only (0120 check) | Codex |
| #581 (0120) | reviewer | Claude Sonnet 0–8, Codex 9–24, Claude Sonnet 25–27 | review artifact Codex (24); final report Claude (26) |
| #584 (0121) | benchmark author of examples | Claude Sonnet 0–8, Codex 9–19, Claude Sonnet 20–23 | package Markdown (15) and checker (16) Codex |
| #587 (0122) | reviewer | Claude Sonnet 0–5, Codex 6–25, Claude Sonnet 26, Codex 27–28 | cold artifact (9) and review artifact (25) Codex |

- The reorder took effect: both reviews started on Claude Sonnet. Both moved to Codex before the review evidence
  was written. The family difference between author and reviewer is therefore partial, not established.
- The histories hold no reason for a candidate change (entries have `action`, `candidate`, `outcome` only, no
  timestamps). The cause of the mid-session changes is unknown. No audit was ordered: the available data cannot
  answer the question and the Claude share is small (#587: 9 requests, 4087 output tokens, 207285 cache-write).
- Decision: keep `routing.tasks.reviewer` Claude Sonnet, Codex, Copilot. Record the same-family part as a limit.
  Do not wait for another family and do not request spending.

## Availability and resource use

| Iteration | Verdict | Input / output tokens | Limit hits | Parked s | Sessions |
|---|---|---|---:|---:|---|
| 0120 | none (review) | 1709052 / 36026 | 0 | 0 | #580 shaper 19 turns, #581 28 turns |
| 0121 | accepted, improved | 771987 / 55067 | 0 | 0 | #583 shaper 15 turns, #584 24 turns |
| 0122 | none (review) | 1996143 / 51497 | 0 | 0 | #586 shaper 17 turns, #587 29 turns |

Totals exclude Policymaker use and are not subscription quota. Pool provider states: Claude `quota` until
retry_after 01:15:38Z, `available` observed 01:25:38Z and 01:55:08Z, `unknown` observed 02:17:08Z with
retry_after 02:22:08Z; Codex `available` (provider observation 2026-11-13T23:17:31Z, model 02:18:05Z); Copilot
`quota`, retry_after 02:16:05Z, not observed again. Retry times do not establish recovery.

## Finish calls

- #584: action 20 `Finish status=complete` rejected ("Finish requires an agent terminal status"); action 21
  `done` rejected (report without marker and matching yaml status); action 23 accepted. Two lost calls.
- #581, #587, #580, #583, #586: one accepted `done` Finish each. The reviewer rule of #569 held in two more
  sessions; the benchmark skill had no such rule.
- Change: `execution/roles/benchmark/SKILL.md` now carries the report-marker and Finish-status rule.
  Check: the next benchmark session history shows one accepted Finish and no rejected Finish.

## WP1 thread and the review-chain rule

- The shaper followed the #579 handoff: #581 exposed recheck (F3 agree on seven mappings; F4 blocked disposition
  adequate, F4 not cleared), #584 new package `wp1-examples-0121-v1` with `wp1-key-0119` unchanged, #587 review
  with a cold expectation saved first. #587 reports Standards CLEAR and Spec CLEAR for the conditional examples
  and states that it releases nothing. No cold derivation or completed probe was replayed.
- The WP1 key thread used iterations 0115–0122: packages #564, #571, #577, #584 and reviews #567, #574, #581,
  #587. `no_progress` is 1 because 0122 was a review. The journal already plans one key revision and its review.
- No cleared key, native key, withheld case, matched agent comparison or accepted method exists. The gaps that
  block owner acceptance of the method are outside this key.
- Change: `execution/roles/orchestrator/SKILL.md` has a new rule "Close a review chain": a CLEAR review closes
  its pinned scope; repeated review requires changed evidence or a concrete unresolved finding. Correct named
  NOT-CLEAR findings and review the changed scope. After the next key revision and review, reassess the next
  task against the remaining method gaps. Carry unresolved findings explicitly and never lift a block to end a chain.
  Check: records 0123–0125 and `journal/working-memory.md` name each task's gap and expected gain; any repeated
  review identifies changed evidence or an unresolved finding. The initial fixed review cap was replaced before
  completion because it could prevent a necessary correction. No arbitrary review count grants clearance.
- Read `docs/perpetua/evaluation.md` and `.github/loop/session-protocol.md` before the final rule and report.
  They retain separate method review, owner acceptance, explicit coverage gaps and engine-owned report fields.

## Validation

Final inspection confirmed the two intended skill additions against starting HEAD. Both skill YAML headers parse,
and `policy/params.yml` parses and is byte-identical to the starting version. `.session/orders.json` parses as
`{"tasks": []}`. Working memory is 15,750 bytes. Both #587 artifacts are absent from `benchmark/writing/`, so
preservation remains a next-task requirement. The activation check was not run: `.session/policy-facts.json` is
absent. These checks validate local definitions and outputs; future session results must test their effect.

## Not established

Benchmark readiness, method acceptance, native validity or behaviour, save-version preservation, dependency
closure, isolation, tool quality and any quota saving. C1 human narrative adjudication stays open. Owner request
#532 stays pending and blocks nothing.
