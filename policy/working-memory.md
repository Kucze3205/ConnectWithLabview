# Policy working memory

Considered: iteration records 0000–0013; reviews #146/#147; task #150's final report and
owner acceptance #151; loop state and startup diagnostics for Policymaker #153, iteration 0014.
Historical inputs: `.session/history/manifest.json`; selected record `.session/history/records/0013.json`;
final #150 report `.github/loop/data/session-reports/150/ede6e2116830bcdcf33621b2162300f913d1328d5cd1e8cda301c8d8ae7e35b7.json`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; it supplies the iteration's work.
- Iteration 0013: one benchmark session #150, accepted/merged after owner request #151.
  F1/F2 revision is available in the prepared checkout at `2669ec4bcfcb86f1fabf86c51cf4acdfd153ebb3`;
  baseline protocol commit `cf38154ea947b34a66494f66a6d3353c32428c50`. The author's protocol checkpoint
  `165f1c283e27115bdae5e6e9ed6ecc9ffe3791b6` differs from the admitted commit: review the available tree.
- Original reviews #146/#147 both recommended revise. F1: frozen required-claim accounting, separate
  dimension outcomes and denominators. F2: independent fixed probes, raw outputs, native-reference
  alignment and missing/unsupported/error outcomes. Revised sections: tasks 28–42, baseline 84–86,
  challenges 100–104. Closure remains for independent review, not inferred from acceptance to merge.
- #150 used both Claude and codex; final model codex/gpt-6.1-sol, 562,970 input tokens, 26 turns.
  Reviewer routing remains Claude-first to prefer another family. Actual family must be reported;
  fallback does not guarantee model-family diversity. Independent sessions remain required.
- The author's evaluator --check passed with 8 evidence refs, benchmark_ready=false,
  benchmark_executed=false, tool_quality=null; tasks/oracle/split/baseline/challenges still missing.
  No scoring runtime, native keys or challenge execution was established. Coverage remains incomplete.
- Startup diagnostic for #153: 11,885 estimated tokens of 100,000, status ok; no budget notice.

## Orders for iteration 0014
- `rereview-protocol-f1f2`: reviewer, high, 60 min/30 turns, exports reports 146/147/150. Pin review
  to 2669ec4 versus cf38154; require per-finding closure, regression check and overall recommendation.
  Expected gain: evidence the owner can assess before protocol acceptance; no readiness inference.
- `resource-proposals`: benchmark, medium, 45 min/25 turns, exports reports 146/147. Write only
  benchmark/resources-proposal.md, one concrete proposal per resource row, prioritizing native jobs
  and restricted storage. Include recipients, access/publication/revocation, owner steps and readiness;
  unknowns stay explicit. Expected gain: actionable inputs for later capability requests.
- Tasks are independent: proposal drafting uses the existing resource table and requests no access,
  executes no native jobs and spends no new resources. No dependency on an ungranted capability.
- Next Policymaker: inspect review and proposal outcomes, including actual model families. If revised
  method is acceptable, use the existing owner gate for pinned protocol/evidence acceptance; merge
  acceptance alone is not benchmark readiness. If revise, order only the evidenced correction.
  Submit concrete optional capability requests only after checking the proposals against accepted limits;
  unavailable resource-dependent work waits for verified readiness while other ready work continues.

## Milestone evidence
- sources: review #134 revise → fix #139 → re-review #140 accept at d588fa9. Coverage review #133 accept
  at 6933e17 as limited inventory. Both remain prepared-not-reviewed in preparation-status.json;
  do not mark reviewed from review recommendations alone. Owner change gate remains authoritative.

## Mechanisms to preserve
- Input ceiling 800k unique input; codex counts non-cached input. Do not directly read large
  sources.json/coverage.json; use bounded summaries. Keep sessions short; use measured outcomes.
- Task Verification runs in-session and offline; checks must read committed files. Report-only
  reviews can omit commands; an index check verifies neither method content nor benchmark quality.
- Rebase runs evaluator --check; changed pinned files need preparation.json hashes updated.
- Missing git identity: leave changes staged; parent engine commits. Partial predecessors block dependants.
- Requests: `.session/requests.json`; schema `.github/loop/session-protocol.md` (Three additional kinds).
  Exports: `docs/perpetua/session-exports.md`; order schema `.github/loop/task-graph.md`.
- Read docs/perpetua/evaluation.md before product planning; implementation requires independently
  checked, owner-accepted verification method. Read accepted-limits.md before private data or spending.

## Open questions
- Notice #100 is approved/closed in current loop state; #92 remains pending. Do not reinstate the
  crashed script shaper without contract review.
- Iteration 0012 created two done reviewer sessions (#146/#147) for one order; cause unknown.
  No recurrence in 0013. If it recurs, collect evidence before an engine-change request.
- Actual Claude availability is unmeasured; #150 began on Claude and finished on codex.
- All-version effort estimate and compatibility limits remain required before choosing LabVIEW 2024.
- How a commit-bound review recommendation becomes milestone reviewed status remains unresolved;
  do not invent an automatic transition or bypass the owner's protocol/evidence acceptance.
