# Policy working memory

Considered: records 0000-0002, reports 78/87/91 (`.session/reports/`), session 79 (reviewer).

## State (2026-11-02, Policymaker session for iteration 0003, issue #94)
- shaper: null (owner decision 2026-11-01). Without Policymaker orders an iteration fails.
- Iterations 0001 and 0002 failed with "no shaper is set and the Policymaker ordered no valid tasks".
  Cause: Policymaker sessions 87 (session_budget, 59 turns) and 91 (input_budget, 19 turns) both
  ended partial before writing `.session/orders.json`. no_progress = 3.
- Iteration 0000: reviewer order `order-78-review-sources` (issue 79, codex/gpt-6.1-sol) used all
  60 turns, 1.17M input tokens, produced no artifact; dependent `order-78-bench-coverage` (issue 80)
  stayed blocked.
- Open owner request #92: notice "policy/ rolled back" (pending).

## Decisions
- Policymaker sessions must write orders.json early: within the first ~10 turns, before any
  broad investigation. Do not glob `.session/history` (huge listing, spent budget in #94).
- Orders must be small: one deliverable, artifact written first and updated incrementally,
  max_turns well below the profile default.

## Open questions
- Content of benchmark preparation (`benchmark/preparation-status.json`) not yet read in policy memory.
- Why did session 79 not write its artifact? Its branch `task/79` commit `c3afe18` may hold partial work.
