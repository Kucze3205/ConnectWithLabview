# Policy working memory

No closed iteration has been considered yet.

- 2026-11-03, issue 95: iterations 0001-0003 failed (`no shaper is set and the Policymaker ordered no valid tasks`).
  Policymaker sessions #87 (turn cap), #91 and #94 (`input_budget`) ended `partial` before writing `.session/orders.json`
  (records `iterations/0001.json`-`0003.json`, reports `.github/loop/data/session-reports/{91,94}`).
- The owner had the planner added: `shaper: planner` in `policy/params.yml`, profile in `execution/profiles.yml`, rule in
  `execution/planner.py` (milestone `coverage` not started -> independent tasks `review-sources` and `bench-coverage`;
  otherwise it exits 1 and the iteration fails so you extend it).
- Open: whether `shaper: null` or a model shaper is better once evidence exists; the planner repeats its tasks until the
  milestone changes, and the owner change gate holds work for acceptance, so watch `no_progress`.
- 2026-11-03, issue 98 (start of iteration 0004): `shaper: planner` is active in loop-state; `benchmark/preparation-status.json`
  has `sources: prepared-not-reviewed`, `coverage: not-started`, so `execution/planner.py` will emit `review-sources` and
  `bench-coverage`. No orders written; session ended after startup reads to end `done` (avoid a further rollback, notice #92
  pending). Expected check after 0004: `coverage` becomes `prepared-not-reviewed` (`python3 -I benchmark/scripts/coverage.py --check`)
  and `.session/artifacts/review-sources.md` holds a verdict on `sources`.
- Next planner extension needed: once `coverage` is `prepared-not-reviewed`, the rule returns None and the iteration fails.
  Add a rule (review `coverage`; then start `tasks`/`oracle`) before or right after iteration 0004 closes.
- Maintain this file when understanding changes; use the archive to revisit a decision or fill a gap.
