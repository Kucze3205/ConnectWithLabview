# Policy working memory

Considered: iteration records 0000–0025; reviews #146/#147; #150/#151; #157/#161;
re-review #166; reports #170/#172/#175/#179/#180/#184/#185/#188/#189/#195/#200/#201/#206–#212/#215/#216;
acceptances #176/#190/#211/#217; record 0026, reports #220/#221; records 0027–0030, reports #224/#228/#231/#232/#236,
acceptances #225/#233/#237; records 0031–0033, reviews #241/#247, report #244. Updated by Policymaker #249, iteration 0034.
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

## Iteration 0028 (#227, wake false)
- Result of 0027: #224 (sonnet only, 9 turns, ~57k tokens) ran the landing script, done, owner accepted (#225).
  Main evaluator --check: exit 0, errors [], missing [], 49 refs; README has `Diagram difference`; baseline
  milestone `design-reviewed`. Script deleted by #227. Lesson confirmed: Policymaker-written idempotent script +
  one low-effort run from main lands cheaply (vs 2 partials resuming tags).
- Milestones: split not-started; others prepared-not-reviewed (baseline design-reviewed). No scorer, no executed
  challenge. evaluator/README untouched; policy/evaluator stays the preparation-index check.
- Order `dev-scorer-challenges` (benchmark, medium, 90/60, from main): stdlib `benchmark/scripts/score.py` +
  `benchmark/challenges/results.json` (--check), computed independently of `expected` fields, then compared;
  mismatches reported, not edited away. Not policy/evaluator (benchmark-side development scorer only).
- Next: read results.json (controls, matches, mismatches). Then order ONE independent review (reviewer, from main)
  of scorer + results + challenge fixtures; check actual `models` (prefer non-GPT if author was codex). If the scorer
  task ends partial, write a narrower order from its saved tag only if the work is mostly done; else re-scope.
  Still pending after that: split/isolation design, typedef-impact/diagram-difference dev cases, all-version effort
  estimate, reviewer routing diversity (reviewer route list sonnet->codex; `opus` alias did not hold in #221).

## Iteration 0029 (#230, wake false)
- Result of 0028: #228 scorer `partial` on input_budget (codex gpt-6.1-sol 917k input, 19 turns). Work saved at tag
  `iter/0028/228` (a9d0b1a): score.py (sha f0a2907…), results.json (sha 4c87180…, 882 KB; 33 controls, 33 matches,
  0 mismatches, 0 unevaluable), challenges-score-evidence.json, tracked __pycache__. Real defect: my order put
  results.json inside benchmark/challenges/, which challenges.py --check rejects as an extra entry (my mistake).
- Wrote `execution/scripts/land_scorer_228.py`: copies score.py from the tag, retargets output to
  `benchmark/results/challenges.json`, regenerates, requires byte identity with the tag's results, drops bytecode.
  Dry run on temp copy of main: idempotent; score/challenges/evaluator --check all 0, evaluator missing [] 49 refs.
  The evidence JSON (benchmark/challenges-score-evidence.json) is intentionally not landed.
- Orders (parallel): `land-scorer-228` (benchmark, low, 20/15, main); `review-scorer-228` (reviewer, alias opus,
  medium, 60/40, main, reads tag read-only, mutation checks in temp copy).
- Next: delete the landing script after merge. Check reviewer `models` block for family diversity (author codex).
  If revise: order fixes from main. If accept: remaining preparation gaps are split/isolation design (split
  not-started), typedef-impact/diagram-difference dev cases, native evidence (#169 waiting), all-version effort
  estimate. Owner method acceptance still not requested.
- Lesson: before naming an output path in an order, check the directory's generator for exhaustive --check.

## Iteration 0030 (#235, wake false)
- Results of 0029: #231 landed scorer (codex 87k input, 13 turns), owner accepted #233. Main has
  benchmark/scripts/score.py (295 lines) + benchmark/results/challenges.json totals 33/33/0/0; neither is pinned in
  preparation.json. Deleted execution/scripts/land_scorer_228.py.
- Review #232 (actual models: codex 435k input, again same family as author) verdict REVISE: (1) hygiene .pyc on tag
  (not landed, moot); (2) conditions ignored: score.py:146/175-187 compare values only; A0005 with an added
  "resolved native runtime dependency" condition stayed correct (protocol.md:35-36, :29). Passing items verified:
  compute never reads expected/purpose/evidence/expected_outcome; denominators, duplicates, contradictions, extras OK.
  Status partial only because its Verification read `.session/report.md`, absent in the epilogue (reviewer write: []).
  Lesson: reviewer Verification must not read .session/report.md; use a trivially true repo check or the evaluator.
- Measured by Policymaker: all 348 keyed claims in current controls carry conditions equal to key conditions (4 unkeyed
  extras), so a condition-aware fix keeps 33/33.
- Order `condition-aware-scorer` (benchmark, medium, 45/30, main): exact-string set comparison, extra condition ->
  incorrect + `condition_ledger`, missing key condition -> partial at best; in-memory 5-mutation self-test in --check.
- Next: order independent re-review of the fix (reviewer, from main, git-free Verification without .session/report.md;
  reviewer routing keeps falling to codex — consider an explicit Claude-first route or accept and record the limit).
  Then pin scorer/results in preparation.json (challenges milestone) after accept. Remaining: split design (not-started),
  typedef-impact/diagram-difference dev cases, native evidence (#169 waiting), all-version effort estimate.

## Iteration 0031 (#239, wake false)
- Result of 0030: #236 condition-aware scorer DONE, merged a480014 (owner #237). Actual models: codex gpt-6.1-sol
  398k input, 18 turns (sonnet only 202 out). score.py:166 condition set comparison, condition_ledger, :263 five
  in-memory mutations in --check; totals still 33/33/0/0. Scorer and results still not pinned in preparation.json.
- Order `rereview-condition-scorer` (reviewer, alias opus, medium, 60/40, from main, Verification score.py --check
  only): spec vs protocol :29/:35-36, extra temp-copy mutations (duplicates, whitespace/case, moved conditions,
  other controls), determinism of regeneration. Check: verdict + numbered findings in its report.
- Next: check the reviewer's actual `models` (author codex; `opus` alias fell to codex in #221/#232). If accept:
  write an idempotent landing script that pins score.py + results/challenges.json under the challenges milestone
  and records the review; one low-effort run from main. If revise: narrow fix from main.
  Then remaining preparation gaps: split (not-started; needs restricted store/custodian -> capability request,
  per protocol ## split), typedef-impact/diagram-difference dev cases, native evidence (#169 waiting).
  All-version vs 2024 effort estimate EXISTS: docs/research/0002-delivery.md (#49; e.g. metadata tier 5-14 d
  2024-only vs 16-49 d all versions; corpus has 2 files saved in 2024, none before 2020). It still needs owner
  presentation before any fallback choice; do not re-order the research.

## Iteration 0032 (#243, wake false)
- Result of 0031: re-review #241 DONE, verdict REVISE at main f913eb8 (actual models: codex 640k input, same family
  as author #236 again; `opus` alias fell to codex a 3rd time). Finding 1: derivable extra claims
  (score.py:77-98 extra_outcome, called :137-142) bypass condition policy (:166-179); X-true + native-runtime
  condition stays correct, empty ledger. Standards clean; regeneration byte-identical (sha e4bfc5a5…).
  Verified passing: duplicates/reorder ok, whitespace/case -> incorrect, moved condition -> donor partial, A0008 ok.
  Evidence artifact iter-0031/241-condition-review.md.
- Measured by Policymaker: only derivable extras are X-false/X-true(x2) in library-icon-tests, all matched to A0005
  with equal conditions, expected condition_ledger absent -> fix keeps 33/33.
- Order `extra-claim-conditions` (benchmark, medium, 45/30, main): shared condition helper for extras, 6th mutation
  `extra-claim-condition`, regenerate. Check: --check 0, totals 33/33/0/0, six regression_self_test entries.
- Next: order re-review (reviewer from main; only finding 1 + spot check). Fix rounds: this is round 2 of
  fix_rounds 2 for the scorer; if the next review revises again, re-scope instead of a 3rd fix. Reviewer
  diversity: routing `reviewer` list is sonnet->codex but sessions land on codex; record as a known limit or
  propose a Claude-first `review` route with measured evidence. Then pin scorer/results (landing script).

## Iteration 0033 (#246, wake false)
- Result of 0032: #244 DONE, merged 1da24f3 (routine, check passed, no owner acceptance needed). Actual models: codex
  gpt-6.1-sol 733k input (near the 800k ceiling), 25 turns; sonnet 4 input. Shared condition helper for required and
  derivable extras; sixth mutation `extra-claim-condition` -> incorrect/incorrect, ledger pointer /claims/12/conditions/3.
  Verified by Policymaker on main: score.py --check exit 0, totals 33/33/0/0, six self-test entries,
  score.py sha 810a5457…, results sha a5b97984… (matches #244's byte-identical regeneration).
- Order `rereview-extra-conditions` (reviewer, alias opus, medium, 45/30, from main, Verification score.py --check):
  spec of shared helper, reader/non-derivable unchanged vs 1da24f3^, 4 temp-copy mutations, regeneration identity.
- Next: if accept -> write idempotent landing script pinning score.py + results/challenges.json under the challenges
  milestone (+ review record), one low-effort run from main, then delete the script. If revise -> fix_rounds exhausted
  for the scorer: re-scope (e.g. a narrower design note or a different author model), not a 3rd blind fix.
  Check the reviewer's `models` block; if codex again (4th time), record no-diversity as a known limit in the
  landing record rather than keep retrying the alias.
- Cost note: codex benchmark sessions keep landing near the input ceiling (#228 917k partial, #244 733k); keep
  bounded-read budgets in every order.

## Iteration 0034 (#249, wake false)
- Result of 0033: re-review #247 ACCEPT at main 8a8455f, no numbered findings (actual models: codex 325k input, 14
  turns; 4th same-family review -> recorded as a known limit, stop retrying the `opus` alias for reviewers). Mutations
  a-d as expected; regeneration byte-identical (results a5b97984…, score.py 810a5457…). Scorer fix rounds closed.
- Wrote `execution/scripts/land_scorer_review_247.py`: hash-gates the reviewed bytes, adds score.py + results to
  challenges pins, challenges milestone -> `scorer-reviewed`, replaces stale "no scorer" limitation sentence (keeps
  same-family and #212 gap-row-not-re-reviewed limits), re-pins preparation-status refs. Dry run on temp copy:
  idempotent; score/challenges/baseline/lineage/dev_cases/sources --check 0 (with env); evaluator missing [] 51 refs;
  only the 2 preparation JSON files change; new status sha d32ec550….
- Orders (parallel, from main): `land-scorer-review-247` (benchmark, low, 20/15) and `typedef-impact-feasibility`
  (benchmark, medium, 45/30, report only: .ctl counts, up to 5 candidates with static users, unmeasurable kinds).
- Next: verify main challenges milestone `scorer-reviewed`, 51 refs; then delete the landing script. Read the typedef
  report: order a typedef-impact dev case only if independent user evidence exists, else record the gap. Then remaining:
  diagram-difference case (needs paired revisions), split (restricted store/custodian -> capability request per
  protocol ## split), native evidence (#169 waiting), owner presentation of docs/research/0002-delivery.md estimate.

## Iteration 0035 (#253, wake false)
- Result of 0034: #250 landing ran the script correctly (score/challenges/evaluator --check 0, missing [], 51 refs,
  preparation.json 07e30c21…, status d32ec550…) but ended `partial` on session_budget at 14/15 turns -> not merged.
  Saved as tag iter/0034/250 (diff vs main = only the 2 preparation JSON + session data). Main still has challenges
  `prepared-not-reviewed`, status sha 1199295c…. Script execution/scripts/land_scorer_review_247.py still on main.
  Actual models: codex 139k input (sonnet 8). Lesson: even one-script landings need max_turns >= 25 under codex fallback.
- #251 typedef feasibility DONE (codex 880k input, near ceiling; report-only, nothing to merge): actor-framework has
  9 loose .ctl (LVSR 20008000) + 7 .vip members, pylavi 0. Candidates with XML declarations + binary name hits:
  Dequeue Priority.ctl (1 VI), DVR Contents.ctl (6 VIs), Time-Delay Override Options.ctl (6 VIs). Static reading
  cannot confirm typedef vs custom control, instances, transitive users or change effects. Prepared actor-framework
  checkout has 1 commit (rev-list --count 1): no paired revisions. DECISION: no typedef-impact dev case now; the gap
  stays visible (challenges README:15 already names it) until native evidence (#169 waiting) and authorized paired
  revisions exist. Do not re-order the feasibility measurement.
- Order `land-scorer-review-247-retry` (benchmark, low, 20 min/25 turns, from main, <=6 tool calls).
- Not filed: split capability request. resources-proposal.md row 1 still has owner questions (which store exists,
  custodian, separate identities); a capability needs concrete owner steps. Next option: one `question` request
  asking the owner to name the store/custodian, combined with the presentation of docs/research/0002-delivery.md.
- Next: verify main challenges `scorer-reviewed` + 51 refs, then delete the landing script. Then consider the owner
  question/presentation above; remaining preparation gaps: split, native evidence, diagram-difference/typedef cases.

## Iteration 0036 (#256, wake false)
- Result of 0035: #254 landing DONE, merged c940ed2 (sonnet only, 9 turns, ~54k tokens; 25-turn limit worked).
  Verified on main: preparation-status.json sha d32ec550…, challenges `scorer-reviewed`, evaluator exit 0, errors [],
  missing [], 51 refs. Deleted execution/scripts/land_scorer_review_247.py (execution/scripts now empty).
- Order `native-job-records` (benchmark, medium, 75/45, from main): design-only benchmark/native/ (README, recipes.json,
  output-record.template.json) + stdlib benchmark/scripts/native_jobs.py --check; maps the 23 native-required dev slots
  to recipes with input sha256, versions, permitted ops, staged outputs; one recipe matching #169 readiness check.
  No preparation.json edits (pin after review). Check: --check exit 0, 23/23 mapped or each unmapped named.
- Request filed: `question` asking whether a private repo in the owner's existing GitHub account (no cost) can be the
  restricted store, with owner as/naming custodian; also points the owner to docs/research/0002-delivery.md estimate
  (information only, no fallback choice). Yes -> draft a concrete Row 1 `capability`; No -> record split blocked.
- Next: read the native-job report; if done, order ONE independent review (reviewer from main, Verification
  native_jobs.py --check, not .session/report.md), then pin under oracle/tasks via an idempotent landing script
  (max_turns >= 25). Read the question's decision from loop state. Remaining gaps: split, native evidence (#169),
  typedef-impact/diagram-difference cases (blocked on native evidence + paired revisions).

## Next Policymaker
- Ready later: baseline design (manifest, development-only precision/cost plan), typedef-impact and
  diagram-difference dev cases, native-job input/output schema. Resource-dependent execution waits for readiness.
- Capability #169 (native jobs) waiting; do not duplicate or block ready work on it.
- All-version effort estimate exists (docs/research/0002-delivery.md); it must be presented to the owner before any
  LabVIEW 2024 fallback choice. Do not re-order the research.

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
