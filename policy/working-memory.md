# Policy working memory

Considered: iteration records 0000–0023; reviews #146/#147; #150/#151; #157/#161;
re-review #166; reports #170/#172/#175/#179/#180/#184/#185/#188/#189/#195/#200/#201; acceptances #176/#190.
Updated by Policymaker #205, iteration 0024.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
selected reports `.session/history/sessions/<issue>/` (.md; list with python glob, not Glob).

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; without valid orders the iteration fails (0017 failed so).
- Protocol re-review #166 (codex) closed F1/F2 at 2669ec4, overall accept; design review lacked model-family diversity.
- Dev cases (11 public, on main via #175/#176): review #179 recomputed 1,053/1,053 XML agreements, 23 native slots
  unresolvable; accepted as development evidence only. Gaps: typedef-impact and diagram-difference cases,
  VI semantic key, native evidence.
- Lineage LANDED via #188/#190, commit 8d3403c (split milestone pinned; split status still not-started).
  Review #185: 829 artifacts rehashed, zero mismatches; preparation evidence only.
- Main (ed65a67) evaluator check in #205: exit 0, errors [], missing [baseline, challenges], 39 references.
- Challenge fixtures: #195 at tag `iter/0022/195` (fbcdb75): 33 controls, 1,080 ledger slots, generator --check passes
  without environment. Branch descends from pre-lineage ecd17c4, so a plain merge deletes lineage; it also tracks
  `__pycache__` bytecode. #201 (iteration 0023) tried merge resolution, lost it across 9 runner interruptions,
  blocked, nothing landed (587k codex input for a mechanical task).
- #205 wrote `execution/scripts/land_challenges_195.py` (no merge state; idempotent): copies 5 challenge files from
  the tag, sets challenges prepared-not-reviewed, appends #195 sentence, re-pins all preparation.json refs.
  Dry run on a temp copy of main: challenges.py --check 0, evaluator missing [baseline], 45 refs, only 7 files changed.
  Delete the script after the landing merges.
- Owner acceptance of the method NOT requested: needs reviewed split/baseline/challenge evidence first.
  No reader implementation or planning before the evaluation protocol and independent review/owner gate.
- Notice #202 (policy/ rolled back after two failed Policymaker sessions #192/#200 partial) pending owner;
  keep Policymaker sessions short: write memory/orders/report early, avoid large reads.

## Iteration 0024 orders (#205, wake true)
- `land-challenges-script` (benchmark, low, 20 min/12 turns, from main): run the script once, verify pinned hashes
  of the 5 files, challenges --check, evaluator missing==[baseline], lineage unchanged, no __pycache__; commit.
- Result #206 (codex gpt-6.1-sol only, 148k input, 11 turns): script ran, Verification exit 0, diff exactly 5 challenge
  files + 2 preparation JSON; own `git commit` failed (Author identity unknown), then session_budget -> partial.
  Parent saved staged work as a231d9e, tag `iter/0024/206`. Lesson: never ask tasks to `git commit`; the parent commits.
- Pass 2 orders (wake true), both start_branch task/206 (resolves to the tag), no dependency between them:
  - `finish-landing-206` (benchmark, low, 15 min/10 turns): no rerun if README present, no commit, run Verification,
    report done so a231d9e can merge. Expected gain: main evaluator missing == [baseline].
  - `review-challenges-206` (reviewer, medium, 60 min/40 turns): independent Spec/Standards review of a231d9e against
    protocol challenge rows and evaluation.md; check every evidence pointer by script; accept/revise verdict.
    Author #195 was mostly codex; check the reviewer's actual `models` block for family diversity.

## Next Policymaker
- Wake: read the landing report, actual `models` block, Verification and `git diff --stat origin/main`.
- If landed: order independent substantive review of challenge fixtures (reviewer role, prefer non-GPT family if
  routing permits; verify actual model usage), and remove the one-off script. Scorer work only via evaluator role
  plus separate evaluator-verifier on policy-layer orders.
- If it failed again: read the exact output; consider having the Policymaker-written script run under policy layer,
  not repeated manual merges.
- Ready later: baseline design (manifest, development-only precision/cost plan), typedef-impact and
  diagram-difference dev cases, native-job input/output schema. Resource-dependent execution waits for readiness.
- Capability #169 (native jobs) waiting; do not duplicate or block ready work on it.
- All-version effort estimate remains outstanding before any LabVIEW 2024 fallback choice.

## Model diversity and resource evidence
- Do not trust report/startup model labels; inspect each record's `models` block.
- Sessions starting on Sonnet routinely fall back to codex gpt-6.1-sol or copilot gpt-5.6-luna for most input
  (#189, #193–#197, #201). No measured subscription-quota figures justify a routing change yet; cache/input-budget
  accounting is not quota use. Keep tasks small, bounded reads, checkpointing.

## Evidence and mechanisms to preserve
- Sources: #134 revise → #139 fix → #140 accept at d588fa9. Coverage: #133 accept at 6933e17 as limited inventory.
- Input ceiling 800k: #179/#180/#185/#189/#200 hit input_budget. Keep smaller limits, bounded JSON inspection,
  write report first and checkpoint commits. Public case JSON ranges from ~11k to ~445k serialized characters.
- Task Verification runs in-session AND in an engine epilogue WITHOUT LABVIEW_ENVIRONMENT (#184 failed there).
  Use environment-free generator/evaluate.py checks. Rebase runs evaluator --check.
- Changed pinned evidence requires preparation.json re-pinning, including every reference to preparation-status.json.
  Both preparation JSON files are json.dumps(indent=2, sort_keys=True)+newline. Parent commits accepted changes.
- Saved unmerged work is reachable as tag `iter/NNNN/N`; a stale start_branch repeats work (0022).
- Orders: `.github/loop/task-graph.md`; ids unique within iteration. Requests: `.github/loop/session-protocol.md`.
  Check `.session/exports/manifest.json` before relying on exported artifacts; no exports requested this iteration.
- Read evaluation.md before reader planning/implementation; accepted-limits.md before private data, disclosure,
  publication or new spending. Optional access must not block ready work.
- Do not reinstate the crashed script shaper without contract review. Notices #92/#100/#158 approved.
