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
- Maintain this file when understanding changes; use the archive to revisit a decision or fill a gap.
