# Policy working memory

Maintain the current organization, open questions and reasons for decisions here, with exact
record/report references. Update when understanding changes; use the archive to revisit a
decision or fill a gap.

## Current organization (iteration 0000, pass 2)
- Benchmark milestones (`benchmark/preparation-status.json`): `sources` prepared-not-reviewed;
  `coverage`, `tasks`, `oracle`, `split`, `baseline`, `challenges` not started. Product
  implementation stays blocked per `docs/perpetua/evaluation.md`.
- Orders (`.session/orders.json`, pass 2): `review-sources-r2` (reviewer, 100 turns) ->
  `bench-coverage` (benchmark, blocked by the review, input `review-sources.md`).

## Decisions and reasons
- Pass-1 review `review-sources` (session #79, codex/gpt-6.1-sol) ended `partial`, cause
  `session_budget`: 60/60 turns, 1.17M input / 8.7k output tokens, empty commit `c3afe18`
  (`.github/loop/data/session-reports/79/ef14b1cf….json`). Diagnosis: broad reading, no
  writing. Response: retry with a larger budget, a narrowed scope, and a required artifact
  created within 10 turns and appended to after each check. No profile reorder yet, because
  one data point is not enough.
- The `capability` proposal for native LabVIEW / restricted storage is deferred until `split`
  is ordered (no withheld cases exist yet).

## Open questions
- If `review-sources-r2` stalls again on the same model, reorder the reviewer candidates in
  `execution/profiles.yml`. Keep the reviewer's model family different from the author's.
- Policymaker sessions in this iteration reread the startup documents many times (context
  loss). Read them once, then work from this file and `.session/report.md`.
