# Policy working memory

Considered: iteration records 0000–0025; reviews #146/#147; #150/#151; #157/#161;
re-review #166; reports #170/#172/#175/#179/#180/#184/#185/#188/#189/#195/#200/#201/#206–#212/#215/#216;
acceptances #176/#190/#211/#217; record 0026, reports #220/#221. Updated by Policymaker #223, iteration 0027.
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
- Pass 2 results: #207 (sonnet only, 14 turns) in-session Verification exit 0, but the engine epilogue FAILED:
  `git diff --quiet origin/main` printed git usage text; the exact cause remains unconfirmed. Saved as 449f3d7
  (tag `iter/0024/207`; challenge content = a231d9e). #208 reviewer ended `blocked` with no report and no tag diff;
  cause unknown.
  Lesson: Verification must be git-free (pin sha256 values instead of git diff/ls-files).
- Pass 3 orders (wake true): `finish-landing-207` (benchmark, low, 15/8, start task/207, git-free sha256 Verification
  incl. lineage pins from main) -> `review-challenges-207` (reviewer, medium, 60/40, blocked_by landing, report in
  first turns). If the reviewer blocks again with no report, investigate the reviewer profile/routing before re-ordering.
- Pass 4 results: #209 (codex only, 91k input, 7 turns) done; owner accepted (#211), merged. Main 2e1422c evaluator:
  exit 0, errors [], missing [baseline], 45 refs. CHALLENGES LANDED (prepared-not-reviewed).
  #210 reviewer blocked again, no report, tag diff empty. Likely cause (unconfirmed): reviewer profile has `write: []`
  and started from a task branch whose benchmark/ changes vs main count as out-of-scope writes -> blocked at merge
  (session-protocol "Git" section). Reviewer tasks must start from main (start_branch null).
- Pass 5 (#205): deleted `execution/scripts/land_challenges_195.py`. Ordered `review-challenges-main` (reviewer,
  medium, 60/40, from main), wake false: the next iteration's Policymaker acts on its verdict.
- Next: if review blocks again from main, the cause is elsewhere: read its issue comments/record before re-ordering;
  consider an engine-change or reviewer profile fix. If revise: order fixes (benchmark role). If accept: scorer
  design via evaluator role + evaluator-verifier. Check the reviewer's actual `models` (author was codex).

## Iteration 0025 (#214, wake false)
- Review #212 (from main) DONE: reviewer start-from-main fix confirmed (#208/#210 blocked from task branches).
  Actual models: codex gpt-6.1-sol 631k input, same family as author #195 -> no family diversity. Verdict revise,
  one finding: README.md:15 / challenges.py:345 omit the explicit diagram-difference gap. All 33 controls, 1,080
  slots, 23 pointers, 20 XML literals verified; do not repeat. Evidence artifact iter-0024/212-challenge-review-evidence.md.
- Orders (parallel, disjoint files, both start from main):
  - `fix-diagram-gap-disclosure` (benchmark, low, 25/15): README text in challenges.py, regenerate, re-pin.
    Check: Verification exit 0, README mentions diagram-difference gap, preparation pins updated.
  - `draft-baseline-manifest` (benchmark, medium, 60/40): new benchmark/baseline/ README + run-manifest template +
    scripts/baseline.py --check; no preparation.json edits (pin after review). Check: baseline.py --check 0,
    unresolved-field list in report.
- Next: after both merge, order ONE reviewer task (from main) covering the README fix and the baseline design;
  try to get a non-GPT reviewer (codex took #212). Then pin baseline (baseline milestone) only after accept.
  Then scorer via evaluator role + evaluator-verifier (policy orders). Owner method acceptance still not requested.

## Iteration 0026 (#219, wake false)
- Results of 0025: #216 baseline design DONE, merged (owner #217): benchmark/baseline/README.md,
  run-manifest.template.json (62 null fields with reasons), scripts/baseline.py --check exit 0 on main.
  Author codex gpt-6.1-sol (423k input). Not pinned in preparation.json; evaluator still missing [baseline].
  #215 gap row done (diff verified: README + challenges.py one row each, preparation.json re-pinned) but
  `partial` on session_budget (14 turns, low effort) -> not merged; saved as tag iter/0025/215 (756f8a1).
  Main README lacks the row (checked).
- Orders (parallel, both no dependency):
  - `finish-gap-disclosure-215` (benchmark, low, 15/8, start task/215): Verification only, report done.
    Check: main README contains `Diagram difference`.
  - `review-baseline-design` (reviewer, model alias `opus` for family diversity vs codex author, medium, 60/40,
    from main): spec check of template vs protocol ## baseline, README claims/blockers, baseline.py mutation
    checks, read-only git show of the 215 gap row. Check: verdict + numbered findings in its report.
- Next: verify the reviewer's actual `models` block (opus requested). If accept: order benchmark task to pin
  baseline design in preparation.json (baseline milestone -> prepared-not-reviewed/reviewed per evaluator),
  then scorer design (evaluator role + evaluator-verifier). If revise: order fixes from main.
  If #215 finish fails again, apply the one-row edit fresh from main instead of resuming the tag.
- Lesson: low-effort 15-turn tasks can still hit session_budget; prefer max_turns >= 15 for regenerate+re-pin.

## Iteration 0027 (#223, wake false)
- Results of 0026: review #221 ACCEPT of baseline design (actual models: codex gpt-6.1-sol 481k input despite
  `opus` alias -> same family as author #216; no diversity again). Findings: none actionable; 62 null fields,
  mutation checks rejected. #220 finish-gap: Verification exit 0 but `partial` session_budget at 7/8 turns,
  not merged (2nd partial for the same row). Main README still lacks `Diagram difference` (checked).
- Lesson: "resume a saved tag" tasks with tiny max_turns keep ending partial; instead write an idempotent
  git-free script in `execution/scripts/` and order one run from main with max_turns 15.
- Wrote `execution/scripts/land_gap_and_baseline.py`: adds gap row (hash-checked against #215's values),
  sets baseline milestone `design-reviewed` + limitation note, pins 3 baseline files + preparation-status.json,
  re-pins changed refs. Dry run on temp copy: all --check 0, evaluator missing [] with 49 refs, 4 files changed.
- Order `land-gap-and-baseline` (benchmark, low, 20/15, from main). Check: main evaluator missing == [],
  README has `Diagram difference`. Then delete the script.
- Next after landing: all seven milestones indexed but split `not-started`, no scorer, no native evidence,
  no executed challenges. Next substantive work: scorer design (evaluator role + evaluator-verifier, policy
  orders) and split/isolation design; typedef-impact/diagram-difference dev cases. Owner method acceptance
  still not requested. `opus` alias did not hold for reviewers: investigate routing (reviewer route list
  starts with sonnet, falls to codex) before relying on it for diversity.

## Next Policymaker
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
