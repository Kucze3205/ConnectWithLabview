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

## Iteration 0037 (#260, wake false)
- Result of 0036: #258 native design `partial` on input_budget (codex 874k input, 15 turns), not merged; saved at tag
  iter/0036/258 (5056add). Policymaker verified on an extract without LABVIEW_ENVIRONMENT: native_jobs.py --check 0
  ("23/23 slots mapped; 12 recipes; zero native executions"), evaluator 0, missing [], 51 refs. Hashes: native_jobs.py
  081040ce…, README 78a54100…, recipes.json f292d56e…, output template 86ba84aa…. README honest: design only,
  readiness VI candidate pylavi/tests/add.vi lacks independently known behaviour (prerequisite unmet), build slots gaps.
- Question #257 APPROVED: loop may plan on a private repo in the owner's existing GitHub account (no cost) as the
  restricted store. Next: draft a concrete Row 1 `capability` (owner steps + readiness check) for split/custodian;
  read resources-proposal.md Row 1, protocol ## split and accepted-limits.md first. Not done in #260 (kept short).
- Wrote `execution/scripts/land_native_258.py` (hash-gated, idempotent; dry run twice on a temp copy of main: 4 files,
  --check 0, evaluator missing [] 51 refs, no __pycache__).
- Orders (parallel, both from main): `land-native-258` (benchmark, low, 20/25, <=6 calls) and
  `review-native-design-258` (reviewer, medium, 60/40, reads the tag read-only; spec vs protocol ## oracle + Row 2,
  4 mutations, slot/sha coverage by script; Verification evaluator --check).
- Next: verify main recipes.json sha f292d56e… then delete the landing script. Read review verdict: accept -> pin
  benchmark/native under oracle milestone via landing script (max_turns >= 25); revise -> one narrow fix from main.
  Then file the Row 1 capability. Lesson: codex design tasks keep hitting the 800k input ceiling (#228, #251, #258);
  the Policymaker-verify-tag + landing-script pattern recovers them cheaply.

## Iteration 0038 (#264, wake false)
- Results of 0037: #261 landing DONE, merged (copilot gpt-5.6-luna 16k input, 10 turns). Verified on main: native files
  sha native_jobs.py 081040ce…, README 78a54100…, recipes f292d56e…, template 86ba84aa…; native_jobs.py --check 0
  (23/23 slots, 12 recipes); evaluator 0, missing [], 51 refs (native design not yet pinned).
  #262 review `partial` on input_budget (copilot 429k input, 21 turns) but its report is complete: verdict ACCEPT,
  no blocking findings; mutations a-d failed --check as required; README honesty confirmed. Reviewer family GPT
  (copilot) vs author codex: both GPT family -> same-family limit recorded in the pin sentence.
- Deleted execution/scripts/land_native_258.py. Wrote execution/scripts/pin_native_262.py (hash-gated, idempotent;
  adds 4 native files to the oracle milestone, appends a review #262 limitation sentence, re-pins status refs; oracle
  label unchanged). Dry run twice on a copy of main without env: evaluator missing [] 55 refs, status sha 5c972a14…,
  preparation.json d4a37c5f…, no __pycache__.
- Order `pin-native-262` (benchmark, low, 20/25, from main, <=6 calls).
- Next: verify main 55 refs + status 5c972a14…, then delete pin_native_262.py. Then file the Row 1 `capability`
  (restricted store = private repo in owner's GitHub account, approved by question #257): read
  benchmark/resources-proposal.md Row 1, protocol ## split, accepted-limits.md and session-protocol.md request
  format first. Deferred twice now (#260, #264); do it first next session. Remaining gaps: split, native evidence
  (#169 waiting), typedef-impact/diagram-difference cases.

## Iteration 0039 (#267, wake false)
- Result of 0038: #265 pin DONE, merged e33073e (copilot 8k input, 8 turns). Verified on main: preparation-status.json
  sha 5c972a14…, preparation.json d4a37c5f…, evaluator exit 0, errors [], missing [], 55 refs. Deleted
  execution/scripts/pin_native_262.py (execution/scripts now empty). Milestones: split not-started, baseline
  design-reviewed, challenges scorer-reviewed, others prepared-not-reviewed (oracle includes the reviewed native design).
- Filed Row 1 `capability` (.session/requests.json): private repo in owner's existing GitHub account, custodian = owner,
  secret NAMES EVAL_STORE_CUSTODIAN_TOKEN (rw) / EVAL_STORE_SCORER_TOKEN (ro), synthetic sentinels only, model providers
  none; readiness steps (a)-(e): custodian clone+push, scorer push rejected, tokenless ls-remote denied, sentinel grep
  zero hits, revoked token denied; independent review of the record. No real cases/keys/private projects requested.
- Order `split-boundary-design` (benchmark, medium, 75/45, main): design-only benchmark/split/ (README, allocation
  manifest template, isolation-record template mirroring steps a-e) + stdlib split_boundary.py --check with >=4
  mutations; no preparation.json edits.
- Next: read the split design report; if done/merged, order ONE review (reviewer from main, Verification
  split_boundary.py --check, not .session/report.md); if partial near input ceiling, verify the tag and write a landing
  script (max_turns >= 25). After accept, pin under split milestone (label e.g. design-reviewed). Read the capability's
  decision from loop state; do not wait on it. Remaining: native evidence (#169 waiting), typedef-impact/diagram-
  difference cases (need native evidence + paired revisions), owner presentation of the 0002 estimate.

## Iteration 0040 (#271, wake false)
- Result of 0039: #269 split design `partial` on input_budget (copilot gpt-5.6-luna 399k input, 30 turns; sonnet 14),
  not merged; saved at tag iter/0039/269 (665409e). Report says completed. Policymaker extracted the 4 files without
  LABVIEW_ENVIRONMENT: split_boundary.py --check exit 0 ("templates valid; 4 rejecting mutations passed"). Hashes:
  split_boundary.py 1365e531…, README c2ecb9a7…, allocation template 5ebe26be…, isolation template 6d540b66….
  README is honest (design only, no allocation, no secrecy, store pending, two strata, infeasible-stratum rule).
- Checker weaknesses seen on reading (not yet probed): the token mutation sets custodian_label.value non-null, so it is
  rejected by the null rule and may never exercise TOKEN_VALUE_RE; the unknown-partition mutation is rejected by a
  special branch inside mutations(), and validate() would reject it only through the null rule. Passed to the reviewer as probes.
- Wrote execution/scripts/land_split_269.py (hash-gated, idempotent, copies 4 files, runs --check; no preparation
  edits). Dry run twice on a clone of origin/main without env: wrote then unchanged, --check 0; policy/evaluator/evaluate.py
  --check exit 0, missing [], 55 refs. (Evaluator path is policy/evaluator/evaluate.py, not evaluator/.)
- Orders (parallel, both from main): `land-split-269` (benchmark, low, 20/25, <=6 calls) and `review-split-design-269`
  (reviewer, medium, 60/40, reads the tag read-only, 4 checker probes, Verification score.py --check).
- Capability #268 (Row 1 store) pending; do not wait on it.
- Next: verify main split_boundary.py sha 1365e531… then delete land_split_269.py. If review accept (blocking
  findings none): write a pin script adding the 4 split files to the split milestone (label design-reviewed) + a review
  limitation sentence; one run from main (max_turns >= 25). If revise: one narrow checker fix from main (fix round 1).
  Remaining: native evidence (#169 waiting), store readiness (#268), typedef/diagram cases, owner presentation of 0002.

## Iteration 0041 (#275) FAILED, rolled back; Iteration 0042 (#277, wake false)
- 0040 results: #272 landing merged 88eb9a9 (split files on main, split_boundary.py 1365e531…). Review #273 (codex 388k)
  ACCEPT, no blocking findings; non-blocking: split_boundary.py:126 token mutation masked by null rule, :130 unknown-
  partition mutation rejected before validate(). Probes all rejected as expected. Author copilot, reviewer codex: both GPT.
- #275 wrote pin_split_273.py and deleted land_split_269.py but the iteration failed "ordered no valid tasks"
  (orders_refused null -> most likely .session/orders.json was never written). policy/ rolled back to e961b3dc, so
  land_split_269.py came back and pin script vanished. Main still: split not-started, status sha 5c972a14….
- #277: re-wrote execution/scripts/pin_split_273.py (same content as 0e2afd6), dry run twice on a copy without env:
  status fae1e26d…, preparation.json 98077172…, 59 refs, split design-reviewed. Deleted land_split_269.py again.
  Order `pin-split-273` (benchmark, low, 20/25, main, Verification evaluator --check).
- LESSON: write `.session/orders.json` FIRST, then verify it parses before Finish; a missing file costs a whole iteration.
- Next: verify main split design-reviewed + 59 refs, delete pin_split_273.py; then one checker fix for #273 findings 1-2
  (re-pin split_boundary.py via script); then consider review of prepared-not-reviewed milestones (coverage, sources,
  tasks) and the owner presentation of docs/research/0002-delivery.md. Do not repeat #273 probes; do not wait on #169/#268.

## Iteration 0043 (#280, wake false)
- Result of 0042: #278 pin DONE, merged 3b5bd32 (codex 65k input, 9 turns; 25-turn limit worked). Verified on main:
  preparation-status.json sha fae1e26d…, split design-reviewed, evaluator exit 0, errors [], missing [], 59 refs,
  benchmark_ready false. Deleted execution/scripts/pin_split_273.py (execution/scripts now empty).
- Milestones: baseline/split design-reviewed, challenges scorer-reviewed, coverage/oracle/sources/tasks prepared-not-reviewed.
- Orders written FIRST and parse-checked (parallel, both from main):
  - `split-checker-mutations-273` (benchmark, medium, 45/40): fix #273 findings 1-2 (token mutation via TOKEN_VALUE_RE,
    unknown-partition via validate()), assert specific reasons, revert-proof in temp copy, re-pin split_boundary.py +
    status in preparation.json. Check: evaluator 0, missing [], 59 refs; new split_boundary.py sha in pins.
  - `readiness-gap-map` (benchmark, medium, 60/40, report only): table evaluation.md/protocol.md requirement -> evidence ->
    state -> blocker; #169/#268 dependencies; now-doable vs owner-needed.
- Next: read the gap map; order only the listed now-doable items (likely reviews of coverage/oracle/sources/tasks
  milestones). If the checker fix ends partial, verify its tag and land via script (max_turns >= 25). Then prepare the
  owner presentation of docs/research/0002-delivery.md and, when only resource items remain, the method-acceptance request.

## Iteration 0044 (#285, wake false)
- Results of 0043: #281 split-checker fix DONE, merged 4332127 (codex 293k input, 16 turns); status now pins
  split_boundary_sha256 dc3e76b6…, but the limitations sentence still says "two non-blocking checker findings open"
  (stale; fix in the next pin script). #282 gap map DONE (codex 457k, report only, nothing merged): full table in
  `.session/history/sessions/282/82f3d038….md`. Key blockers: oracle/split/resources blocked on #169/#268; tasks/
  sources/coverage/challenges prepared-not-reviewed; baseline design-only; no owner method acceptance.
  Now-doable per #282: substantive reviews (sources, coverage, 1,053 XML slots), #212 gap-row re-review, public
  lineage adjudication, readiness-case/vector prep for #169, runner/manifest validation contract.
  Stale text: sources.md:57, lineage.md:21, baseline/README.md:3,27.
- Measured by Policymaker: sources.md, sources.json, coverage.md unchanged since d588fa9 (git diff --stat shows only
  baseline/dev/lineage README additions) -> reviews #140/#133 may still apply.
- Orders written FIRST and parse-checked (parallel, both from main):
  - `native-readiness-case` (benchmark, medium, 75/45): pick a public VI whose behaviour is stated outside the VI,
    write benchmark/native/readiness-case.json (vectors + independent pointers), extend native_jobs.py --check if
    needed. Check: --check 0, every expected output cites a non-VI source. Unblocks #169 readiness.
  - `review-currency-sources-coverage` (reviewer, medium, 60/40): byte identity vs reviewed commits, 10-row seeded
    spot check vs originals, verdict relabel-reviewed/revise per milestone.
- Next: if reviewer says relabel-reviewed -> one pin script: sources/coverage `reviewed`, fix stale split limitation
  sentence, re-pin status (max_turns >= 25). If readiness case exists -> order a review (non-author family if possible),
  then tell the owner #169 now has a concrete readiness VI. Then the 1,053-slot XML review (split into batches by case to
  stay under the input ceiling) and #212 gap-row re-review. Do not re-run the gap map.

## Iteration 0045 (#290, wake false)
- #286 (iteration 0044 Policymaker) loop state says `partial`, but its orders ran. Record 0044 shows 2 tasks: #287 and #288.
- #288 review DONE (codex 439k, report only): sources and coverage `relabel-reviewed`. The bytes are identical to d588fa9/6933e17,
  and the seed-288 10-row spot check matched. Findings 1-4: sources.md:57, lineage.md:21 and baseline/README.md:3,27 are stale,
  and status labels need a relabel. Evidence artifact iter-0044/288-review-evidence.md.
- #287 readiness case `partial` on input_budget (codex 940k in 18 turns). It left only a wip report and no result.
- FOUND by Policymaker: on main, `benchmark/scripts/lineage.py --check` exits 1 (`Unexpected split status`). lineage.py:93
  hardcodes split == not-started, and #278 set design-reviewed. The evaluator still passes (59 refs). The other 5 generator checks pass.
- Capability #268 (restricted store) APPROVED 2026-11-06T15:28Z, and the owner posted capability-ready. Readiness clause: "a loop session
  other than the author independently reviews the record before split work uses the store". The location of the record was not found yet
  (request-state/268.json has none). Next: find it (issue #268 comments) and order a review of it.
- Orders (parallel, from main): `status-currency-288` (benchmark, medium, 60/40) fixes lineage.py split handling, relabels sources/
  coverage reviewed, replaces the stale split-finding sentence and re-pins. It does not edit the reviewed sources.md/baseline README bytes; a status
  sentence records them as dated instead. `readiness-case-pylavi` (benchmark, medium, 45/30, report only, <=20 calls, <250k)
  uses pylavi/tests/test.yaml + args.yaml expected properties (eq 21.0f etc.) as independent evidence.
- Next: verify lineage.py --check 0, sources/coverage `reviewed`. Land the readiness case by script after an independent review.
  Find and review the #268 readiness record. Then split allocation planning can use the store.

## Iteration 0046 (#295, wake false)
- Results of 0045: #291 DONE, merged 4d1890a (codex 446k, 20 turns, routine accept): lineage.py reads split status
  (not-started|design-reviewed), sources/coverage `reviewed`, stale split sentence replaced; all 9 generator --check 0;
  evaluator 0, missing [], 59 refs; status sha ed298a85…, lineage.py f7a58168…. #292 DONE report only (codex 677k,
  18 turns, not merged): proposed readiness-case.json in its report (snapshot
  .github/loop/data/session-reports/292/d44dc437….json): empty_separate_code.vi (fdb970bf…) and empty_no_debugging.vi
  (7ca77f95…) with contrasting saved properties (21.0f, separate code, debuggable) from test.yaml:86-125; controlled
  I/O = explicit gap (none found). Key is `not_debuggable`, not `no_debugging`. Do not repeat the bounded search.
- #268 readiness record: not in request-state/268.json or any repo file; it lives only in issue #268 comments
  (owner's capability-ready post). No order reads GitHub comments yet; next: find whether a session can read it
  (exports `reports`? issue comments) or ask the owner to commit the redacted record, then order its review.
- Orders (parallel, reviewers from main, report only): `review-readiness-case-292` (verdict on #292 proposal: hashes,
  line pointers, honesty) and `rereview-gap-row-and-split-checker` (#212 gap row + #281 split fix, revert-proof).
- Next: if 292 review accepts -> idempotent landing script writing benchmark/native/readiness-case.json (+ native_jobs
  --check support if needed, pin under oracle), max_turns >= 25. If both re-reviews accept -> pin script replaces the two
  "not independently re-reviewed" limitation sentences. Then: #268 record review, split allocation planning.

## Iteration 0047 (#300, wake false)
- Results of 0046: #297 review DONE (copilot 141k + codex 128k, 13 turns): ACCEPT of the #292 readiness proposal (all 6
  sha256 match, line pointers hold, honesty flags false, controlled I/O gap). #298 re-review `partial` input_budget (610k,
  14 turns) but verdicts written: item A gap row ACCEPT (README:24, challenges.py:354); item B REVISE only because its
  own revert harness was masked.
- Measured by Policymaker #300 in temp copies: break TOKEN_VALUE_RE -> exit 1; remove partition check -> exit 1; move
  token mutation back to `value` -> exit 1; only disabling the reason comparison passes. So #281 fix is revert-proof;
  item B closed without another fix round.
- Wrote execution/scripts/pin_readiness_300.py: extracts the #292 JSON block (block sha bb6c4a41…), writes
  benchmark/native/readiness-case.json (896e3a56…), replaces the two "not re-reviewed" sentences, appends a readiness
  sentence, pins the case under oracle, re-pins status. Dry run twice on a copy without env: idempotent, status
  4b0ec6da…, preparation 2daa463f…, evaluator 0 missing [] 60 refs; native/split/challenges/score/baseline --check 0
  (lineage.py needs env, expected).
- Order `pin-readiness-and-rereviews-300` (benchmark, low, 20/25, main, <=8 calls).
- Next: verify main 60 refs + status 4b0ec6da…, delete pin_readiness_300.py. Then: #268 readiness record review
  (record only in issue #268 comments; ask owner to commit a redacted record or find an export route), tell the owner
  #169 now has a cited property-readiness case, split allocation planning, owner presentation of 0002 estimate.

## Iteration 0048 (#303, wake false)
- Result of 0047: #301 DONE, merged c903f9b (sonnet only, 8 turns, ~47k tokens, owner-accepted). Verified on main:
  evaluator exit 0, errors [], missing [], 60 refs; preparation-status.json sha 4b0ec6da…; benchmark/native/
  readiness-case.json present. Milestones: baseline/split design-reviewed, challenges scorer-reviewed, coverage/sources
  reviewed, oracle/tasks prepared-not-reviewed. Deleted execution/scripts/pin_readiness_300.py (scripts now empty).
- Orders written FIRST and parse-checked (parallel, both reviewer, from main, report only):
  - `relabel-review-tasks-oracle` (medium, 60/40): byte identity of dev cases vs #179-reviewed commit, seed-302
    10-slot spot check, oracle pin hashes + "zero native executions" honesty. Verdict per milestone.
  - `review-store-readiness-268` (medium, 30/25, exports reports sessions [268]): find the #268 readiness record
    (export status, git grep sentinel); review steps a-e if found, else `record-unavailable` with evidence.
- Next: if relabel-reviewed -> pin script relabels tasks/oracle `reviewed` (max_turns >= 25). If #268 record is
  unavailable -> file a `question`/request asking the owner to commit a redacted record (no token values) to the repo.
  If accepted -> split allocation planning (design of allocation using the store, synthetic only first).
  Then: tell the owner #169 has a cited property-readiness case; owner presentation of 0002 estimate; method acceptance
  request when only resource items remain.

## Iteration 0049 (#307, wake false)
- Considered record 0048 and reports #304/#305. Startup diagnostic: ok, estimated 23,392 tokens; no budget notice.
- #304 DONE (codex 632k input): tasks `relabel-reviewed`; all 11 case files identical to #179-reviewed eac73eb;
  seed-302 sample 10/10 XML slots matched originals. Oracle `relabel-reviewed` only for XML keys and native design;
  18 oracle pins match. Preserve 23 unresolved native slots, zero native executions, public visibility and model-family uncertainty.
  Evidence: .github/loop/data/session-reports/304/089b02b9e0170b4b737d43576fffb79f93605897ae0b308116a281d2888ab330.json.
- #305 DONE (codex 267k input): `record-unavailable`; session 268 reports export unavailable, detail
  `no matching supported session data`; repository/history searches found no executed readiness record.
  Evidence: .github/loop/data/session-reports/305/4ff1bcef83153d7bdb139f4873401208fb4d10478ed40774b8ea38b431008ac4.json.
  Do not repeat these searches unless inputs change. Capability-ready does not replace the required independent record review.
- Orders saved and JSON-checked: `relabel-tasks-oracle-304` (benchmark, medium, 40 min/35 turns, main, <=10 calls).
  Changes only preparation-status.json and preparation.json: tasks/oracle reviewed within #304 scope, stale pending-review
  text corrected, status references re-pinned. Expected check: evaluator errors [], missing [], 60 refs, ready/executed false.
- Owner question saved: commit redacted executed #268 record and SHA256 at benchmark/split/store-readiness-268.redacted.json
  and .sha256. No credentials, sentinel markers, private addresses or withheld material. Existing capability scope unchanged.
- Next: verify the label update and preserved limits. If the owner supplies the record, order independent review before store use.
  Other ready work: baseline runner/manifest validation contract from gap map #282; no baseline execution without prerequisites.
  #169 still lacks native readiness; method acceptance and product implementation remain gated. Quality remains unmeasured.

## Iteration 0050 (#311, wake false)
- Considered record 0049 and gap map #282 (baseline rows). Startup ok, 24,039 tokens.
- #309 DONE, merged c0e063f (codex 228k input, 12 turns, owner-accepted). Verified on main: evaluator exit 0, errors [],
  missing [], 60 refs, ready/executed false; status sha eea3c32b…. ALL seven milestones now reviewed-level labels:
  baseline/split design-reviewed, challenges scorer-reviewed, coverage/oracle/sources/tasks reviewed.
- Question #308 (commit redacted #268 record) still pending; do not wait on it. #169 still waiting.
- Order `baseline-run-record-contract` (benchmark, medium, 75/45, main, <=25 calls, <300k): design-only
  benchmark/baseline/run-record.template.json + benchmark/scripts/run_record.py --check (frozen fields, cross-check
  manifest field names, in-memory conversion to score.py claim format, >=4 rejecting mutations), README section;
  no preparation edits. Check: run_record.py --check exit 0 on main; report lists undecided fields.
- Next: if done -> ONE independent review (reviewer from main, Verification run_record.py --check). If partial near
  the input ceiling -> verify the tag and land by script (max_turns >= 25). After accept -> pin under baseline.
  Then: owner presentation of docs/research/0002-delivery.md; tell owner #169 has a cited readiness case; method
  acceptance request only when the remaining items are resource-dependent (#169/#268). Product implementation gated.

## Iteration 0051 (#314) FAILED, rolled back; Iteration 0052 (#316, wake false)
- Considered records 0050/0051, reports #312/#314. #312 (codex 412k, 17 turns) `blocked`: my order #311 made it append
  to the pinned benchmark/baseline/README.md without re-pinning -> evaluator hash mismatch. Work saved at tag
  iter/0050/312 (4fed9eb, on origin): run-record.template.json aa928031…, run_record.py bf57224f…, README 02020a5d….
  run_record.py --check 0, 6 mutations, 8 undecided fields (restricted_storage, provider_usage_mapping, provider_cost,
  infrastructure_cost, interruption_policy, claim_mapping_revision, manifest_binding_evidence, isolation_evidence).
- #314 report listed orders but iteration 0051 failed "ordered no valid tasks" (orders_refused null); cause unconfirmed,
  most likely orders.json missing again. Rollback removed its land_run_record_312.py (execution/scripts empty).
- #316: wrote and parse-checked .session/orders.json FIRST. No script: the landing task runs `git checkout
  iter/0050/312 -- <2 files>` + sha256 gate. Orders (parallel, from main): `land-run-record-312` (benchmark, low,
  20/25) and `review-run-record-312` (reviewer, medium, 60/40, report only, Verification score.py --check).
- Next: verify both files on main (shas above) and evaluator 60 refs. If review accepts: pin script adds the 2 files to
  baseline pins, adds the README link section, re-pins README + status refs (max_turns >= 25). If revise: one narrow
  fix from main. Rule: never order edits to a pinned file unless the same task re-pins.
- LESSON (#316): Finish rejects .session/report.md unless it begins with `<!-- session-report -->` and a ```yaml block
  whose `status` equals Finish.status. Write the report in that format from the start.

## Iteration 0053 (#321, wake false)
- Considered record 0052, report #318. #317 landing DONE, merged (sonnet only, 10 turns, ~66k tokens, owner #319):
  main has run-record.template.json aa928031… and run_record.py bf57224f… (verified), not pinned; README unchanged
  (0adac3b9…). #318 review DONE (codex 461k, 17 turns): ACCEPT, findings 1-5 non-blocking; finding 4: manifest-content
  binding unresolved (run_record.py:134) -> needs actual binding + negative test before runner integration. Same family
  as author #312 (codex). Evidence: .github/loop/data/session-reports/318/11203643….json.
- Wrote execution/scripts/pin_run_record_318.py (hash-gated, idempotent): README = tag #312 bytes with the last
  "Request independent review…" sentence replaced by a #318 sentence; adds the 2 files to baseline pins; appends a
  #318 limitation sentence; re-pins README + status refs. Dry run twice on a worktree of origin/main without env:
  run_record/baseline/evaluator --check 0, 62 refs, README 24c2018f…, status fbdb65ce…, preparation 54c5c701….
- Order `pin-run-record-318` (benchmark, low, 20/25, main, <=8 calls). Orders written and parse-checked before memory.
- Next: verify main 62 refs + status fbdb65ce…, then delete pin_run_record_318.py. Then: owner presentation of
  docs/research/0002-delivery.md (information, no fallback choice), tell owner #169 has a cited readiness case, and
  check whether only resource-dependent items (#169, #268/#308) remain before a method-acceptance request.
  Product implementation stays gated. #308 still pending; do not wait on it.

## Iteration 0054 (#326, wake false)
- Considered record 0053 and git log of origin/main (72e6b0f). #322 pin DONE, owner-accepted #323. Verified on main:
  preparation-status.json fbdb65ce…, preparation.json 54c5c701…, baseline README 24c2018f…; milestones baseline/split
  design-reviewed, challenges scorer-reviewed, coverage/oracle/sources/tasks reviewed. Deleted
  execution/scripts/pin_run_record_318.py (scripts now empty).
- Owner answered #308: commit a43a7b9 added benchmark/split/store-readiness-268.redacted.json (sha 4bed1602…, matches its
  .sha256 file) from workflow .github/workflows/store-readiness.yml; steps a-d pass in run 42283794047; step (e) note: the
  owner deleted the scorer token before the revoked run. Not yet independently reviewed.
- Order `review-store-readiness-308` (reviewer, medium, 40/30, main, report only, <=15 calls): sha check, steps a-e vs
  #268 clause and split templates, redaction scan, limits, verdict accept/revise. A confirmation-only task was dropped (busywork).
- Next: if accept -> design synthetic split allocation using the store (benchmark, design only, no real cases), and pin the
  record + review under split via script (max_turns >= 25). If revise -> owner request with exact action. Still pending:
  owner presentation of docs/research/0002-delivery.md, tell owner #169 has a cited readiness case, method-acceptance
  request once only resource items remain. Product implementation gated.

## Iteration 0055 (#329, wake true)
- Considered record 0054, report #327, .github/workflows/store-readiness.yml, run_record.py, task-graph.md.
- #327 store-readiness review DONE (codex 334k, 16 turns, report only): verdict REVISE. Findings: (1) step (d) blocking:
  workflow masks download/extract/search errors, zero counts unproven -> fail closed, inventories, positive control;
  (2) step (b) push 128 not classified as authorization denial; (3) step (a)/(b) commit creation not gated/recorded.
  (c)/(e) match; redaction clean; sha matches. Repeat (e) after any new scorer-token (b) run. Evidence artifact
  iter-0054/327-store-readiness-review.md. Do not repeat this review.
- Wrote `policy/proposals/store-readiness.yml` (replacement workflow; bash -n 0; yaml parses): mk() gates commit,
  qp() classifies write-denied/other, step (d) fails closed (gh api/run list/log zip/artifact count/download/tar checks,
  per-run inventory, planted positive controls in work/pc), job exits 1 on incomplete, artifact upload if: always().
  Known gap: no positive control for git grep / git log -S. Workflows are owner-only (.github/workflows/**).
- Orders (parallel, wake true): `readiness-gap-delta` (benchmark, medium, 50/35, report only, exports #282): update gap
  map vs main, classify rows, decision line request-acceptance-now | do-first. `review-store-workflow-proposal`
  (reviewer, medium, 45/35, report only, exports #327): verdict on the proposal.
- Next (same iteration, on wake): if workflow review accepts -> owner `question`/request: copy the proposal to
  .github/workflows/store-readiness.yml, rerun initial, then revoke+rerun revoked, commit replacement redacted record +
  sha256; then order independent review. If revise -> fix the proposal file, not another blind review. Read gap-delta
  decision: if request-acceptance-now, draft the method-acceptance request (STE) incl. 0002 estimate presentation and
  #169 readiness-case note; else order the listed now-doable items.

## Iteration 0056 (#340, wake false)
- Considered record 0055 and reports #330-#337 (snapshots .github/loop/data/session-reports/33N/*.json).
- WASTE FOUND: 0055 used wake true; passes 2-4 re-ran the SAME two orders (8 tasks, 2.7M input) with near-identical
  results. Lesson: use wake false unless the next pass orders different work; on a wake pass never re-submit
  finished orders.
- Gap delta (#330/#332/#334/#336): all say do-first. Owner method-acceptance request is premature. Now-doable per #330:
  N1 manifest-content binding (run_record.py:134, #318 finding 4), N2 public lineage adjudication (230 candidate
  groups / 1,244 pairs, lineage.md:10-21), N3 populated-manifest/runner contract. Then #169/#268 evidence.
  Do not re-order the gap delta.
- Workflow reviews #331/#333/#335/#337: all revise. Consolidated F1 git grep/log silent zero; F2 positive controls
  for every search; F3 Actions `bash -e` aborts on grep status 1; F4 local permission -> write-denied; F5 remote
  diagnostic text + literal STORE env; F6 nonzero hits / wrong outcomes still exit 0.
- Revised policy/proposals/store-readiness.yml (rev 2): set +e, trap cleanup, cnt() (status > no-match -> error),
  qp() only GitHub remote denial/403 texts, no `first`, STORE from secret EVAL_STORE_REPO (owner must add it),
  controls for tree/history/issues/logs/artifacts, per-step expected-outcome gates, result line. Measured: bash -n 0;
  helper harness under bash -e -o pipefail: hits 1, misses 0, errors `error`, qp deny/403 write-denied, local
  permission `other`, script reached end.
- Orders (parallel, main): `manifest-binding-n1` (benchmark, medium, 60/45, re-pin) and `review-store-workflow-v2`
  (reviewer, medium, 45/35, exports #331/#337).
- Next: if v2 accept -> owner request: copy proposal to .github/workflows/store-readiness.yml, add secret
  EVAL_STORE_REPO, run initial, revoke scorer, run revoked, commit replacement redacted record + sha256; then order
  independent record review. If revise -> fix the file myself (no blind re-review). Verify N1 on main (evaluator 0,
  new run_record.py sha pinned), then order its review and N2 lineage adjudication (bounded; split by case family).

## Iteration 0057 (#344, wake false)
- Considered record 0056, reports #341/#342, run_record.py on main (bf57224f…), proposal sha 53ac0f9d….
- #341 manifest binding `partial` input_budget (copilot 429k, 26 turns), NO change made (only read files). Do not resume it.
- #342 review of workflow proposal rev 2: ACCEPT, F1-F6 closed (actual models: copilot 308k + sonnet 14 -> GPT family;
  author Policymaker = Claude, so family differs). Non-blocking: (1) issue-control plants raw text, gh JSON escaping may hide
  quote/non-ASCII markers (fix: jq-decoded grep); (2) qp 403 branch and real local-permission failure untested.
- Filed `question` request: owner copies proposal to .github/workflows/store-readiness.yml, adds secret EVAL_STORE_REPO, new
  scorer token, runs initial, revokes, runs revoked, commits replacement redacted record + .sha256 (same path as #308).
- Wrote `execution/scripts/bind_manifest_n1.py` (hash-gated, idempotent): adds bind_manifest() + 3 controls (matching
  accepted, wrong-content hash and one changed byte rejected, output key `manifest_binding`) to run_record.py; replaces
  README finding-4 sentence and status sentence; re-pins. Dry run twice on a copy without env: 4 files change;
  run_record/baseline/score/evaluator --check 0, 62 refs; shas run_record.py 48404c93…, README 9008a808…, status
  e225d24c…, preparation 27542683…; revert (equality always true) -> --check exit 1.
- Orders (parallel, main): `apply-manifest-binding-n1` (benchmark, low, 20/25, <=8 calls) and `review-manifest-binding-n1`
  (reviewer, medium, 45/35, runs the script in a temp copy, probes uppercase hex/appended newline/str input).
- Next: verify main run_record.py 48404c93… + 62 refs, delete bind_manifest_n1.py. If review accepts -> pin script updates the
  "awaits independent review" sentences. If revise -> fix the script myself. Watch the owner's store record; then order one
  independent record review. Then N2 lineage adjudication (bounded, split by case family) and N3 populated-manifest contract.

## Iteration 0058 (#350, wake false)
- Considered record 0057, report #347 (snapshot .github/loop/data/session-reports/347/6310c97e….json), main files.
- #346 DONE, merged 611da6c (sonnet only, 11 turns, ~78k tokens, owner #348). Verified on main: run_record.py 48404c93…,
  README 9008a808…, status e225d24c…, preparation 27542683…; evaluator 0, errors [], missing [], 62 refs.
  Deleted execution/scripts/bind_manifest_n1.py.
- #347 review DONE (sonnet only, 18 turns, 795k cache_read): ACCEPT. Findings: (1) add uppercase-hash and str-input
  controls; (2) "not yet independently reviewed" wording stale. Reviewer and author (Policymaker) are both Claude family.
- Wrote execution/scripts/pin_binding_347.py (hash-gated, idempotent): 2 new controls (5 manifest_binding entries),
  README + status sentences record #347, re-pins. Dry run twice on a copy without env: run_record/baseline/score/
  evaluator --check 0, 62 refs; shas run_record.py b39c3060…, README 75892269…, status bcd2881b…, preparation 315d83a4…;
  revert probes (accept str via encode; .lower() normalization) -> --check exit 1. No __pycache__.
- Orders (parallel, main, wake false): `pin-binding-review-347` (benchmark, low, 20/25) and
  `populated-manifest-contract-n3` (benchmark, medium, 75/45): new run-manifest.synthetic.json, runner_contract.py --check
  (imports run_record.py by path, >=4 mutations), runner-contract.md; no edits to pinned files.
- Owner request #345 (install store-readiness workflow, rerun, commit new record) pending; do not wait on it.
- Next: verify main run_record.py b39c3060… + 62 refs, delete pin_binding_347.py. If N3 done -> one review (reviewer from
  main, Verification runner_contract.py --check), then pin under baseline by script (max_turns >= 25). If partial near the
  input ceiling -> verify the tag and land by script. Then N2 lineage adjudication: 230 candidate groups (183 of size 2,
  one of 38) in benchmark/lineage.json `candidate_variants`, status candidate-unadjudicated; split by group batches.
  When #345 record arrives -> order one independent record review.

## Iteration 0059 (#357, wake false)
- Considered record 0058, report #352 (snapshot .github/loop/data/session-reports/352/5ab8c701….json), main bb83b79.
- #351 pin DONE, merged c91665c (sonnet only, 14 turns, ~124k tokens, owner #353). Verified on main: run_record.py
  b39c3060…, README 75892269…, status bcd2881b…, preparation 315d83a4…; run_record/evaluator --check 0.
  Deleted execution/scripts/pin_binding_347.py (scripts now empty).
- #352 N3 DONE, merged f405d54 (sonnet only, 16 turns, owner #354): run-manifest.synthetic.json 4d4c2b0f…,
  runner_contract.py f5f1b174… (--check 0 on main; 3 cases x 2 arms x 2 reps = 12 runs; 10 mutations),
  runner-contract.md b9e47205…. Not pinned. Author Claude Sonnet.
- Orders written FIRST and parse-checked (parallel, main): `review-runner-contract-352` (reviewer, medium, 45/35,
  report only, 4 temp-copy probes) and `lineage-adjudication-n2-pilot` (benchmark, medium, 60/40, report only):
  rules + decisions JSON for the 13 version-difference groups of 230 `candidate_variants` (all same-basename,
  different-sha256, candidate-unadjudicated), measured per-group cost.
- Next: if review accepts -> pin script adds the 3 N3 files to baseline pins + #-review sentence, re-pins (max_turns
  >= 25). If revise -> fix by script myself. If pilot rules hold -> order an independent review of the rules, then a
  landing script that writes adjudications for all 230 groups (re-pin lineage.json; lineage.py --check needs env).
  #345 store record pending; when it arrives order one independent record review. Product implementation gated.

## Iteration 0061 (#363, wake false)
- Considered record 0059, reports #358/#359/#361, current loop state and startup diagnostics. Startup: ok, 27,967 estimated tokens.
- Iteration 0060 failed because no valid tasks reached the engine. #361 ended partial on input_budget (891,947 input tokens).
  Its report claimed orders existed, but no tasks ran. Do not assume report prose establishes saved orders.
- Wrote .session/orders.json FIRST, wrote the marked report, and checked both structures with python3: three tasks,
  unique ids, valid roles/limits, start_branch null, wake false. No routing change; quota consumption remains unmeasured.
- #358 review REVISE: deleting runner_contract.py's expected-reason comparison leaves --check exit 0.
  Other three failure probes passed; manifest comparison passed (62 fields). Do not repeat that comparison.
  Actual reviewer mainly GPT; #352 author Claude. Keep N3 files unpinned until the fix receives independent acceptance.
- #359 pilot DONE, report only: 7 same-lineage, 6 undecidable, 0 independent across 13 version-difference groups.
  candidate-0124 and candidate-0227 overlap. Rules and decisions need independent review before landing.
  Machine timings exclude substantive adjudication/review; do not project reviewer effort from them.
  Actual author mainly GPT (786,862 input tokens); no changes landed.
- Owner request #345 is completed; replacement public redacted store record exists. Independent review is still required
  before store use. Do not repeat historical searches for the old missing record.
- Orders: fix-runner-reason-control-358 (benchmark, medium, 40 min/35 turns); review-lineage-pilot-359 (reviewer,
  medium, 50/35); review-replacement-store-record-345 (reviewer, medium, 45/35). All start from main and run independently.
  Expected gains: regression-sensitive runner check; reviewed lineage scope; executed-evidence verdict on store readiness.
- Next: read those three results. Independently review the runner fix before pinning. Act on the lineage/store verdicts;
  preserve unresolved relationships and existing synthetic-only access scope. Product implementation remains gated.
- Exact sources: .session/history/records/0059.json;
  .session/history/sessions/358/bb79b91ebd416fa7481a74753d0413fbe8054c8c32789c33254b72df943cbaec.md;
  .session/history/sessions/359/0a041dc81e14594574a34f6e1e9a74df8b142dd9fb4eba432d8bcdc85621d382.md;
  .session/history/sessions/361/159dc30f735b2e540f622e1e9d3a6b316c13e6cdd96caa1672352afeadac91db.md.

## Iteration 0062 (#368, wake false)
- Considered record 0061, reports #364/#365/#366. Startup ok, 28,601 tokens.
- #364 DONE, merged f748718 (codex 266k, 15 turns): runner_contract.py sha 866e9c44…, reason self-test; 4 probes exit 1.
  Author GPT. Still unpinned until independent review.
- #365 lineage review CRASHED at 0 turns (no models, no report). Re-ordered unchanged scope.
- #366 store record review (codex 266k) REVISE: record sha 137cc969… matches sidecar, replaces #308 record; runs
  42375820030 (initial) then 42376072522 (revoked). F1 blocking: issue/comment search uses raw API JSON, control plants
  unescaped text. F2: (c)/(e) accept any nonzero exit. (a)/(b)/(d) otherwise fixed vs #327. Do not repeat.
- Wrote policy/proposals/store-readiness.yml revision 3 (sha 768a447e…, bash -n 0): qr() classifies read denials
  (not-found/auth-failed/401/403 -> access-denied, else other); (c)/(e) fail unless access-denied; dj() jq-decodes all
  strings of issues/comments and of a jq-built issue control before grep.
- Orders (parallel, main, reviewer): review-runner-fix-364, retry-lineage-pilot-review-359, review-store-workflow-v3.
- INCIDENT: .session/orders.json and report.md written early in this session were missing later (transport switch from
  codex to claude mid-session?). Rewrote both. LESSON: re-check both files exist just before Finish.
- Next: v3 accept -> one Owner `question`: install revision 3, add nothing new, run initial, revoke a NEW scorer token,
  run revoked, commit replacement record + .sha256; then independent record review. v3 revise -> fix file myself.
  Runner accept -> pin script adds 3 N3 files + runner_contract.py to baseline pins (max_turns >= 25).
  Lineage accept -> bounded next triage batch per reviewer scope.

## Iteration 0063 (#373, wake false)
- Considered record 0062, reports #369/#370/#371 (snapshots .github/loop/data/session-reports/36N|37N/*.json), main c63ad79.
- #369 review ACCEPT of #364 runner reason fix (sonnet, cross-family to codex author); all probes exit 1 for intended reasons.
  Non-blocking: KeyError diagnostic prints only 'boom'. Main shas: runner_contract.py 866e9c44…, synthetic manifest
  4d4c2b0f…, runner-contract.md b9e47205…, status bcd2881b…, preparation 315d83a4… (all verified).
- #371 review of store workflow v3 (sonnet; author Policymaker also Claude -> same family) REVISE: tokenless git prints
  `fatal: could not read Username for ... terminal prompts disabled` -> qr gave `other`. #366 F1 closed. Fixed in
  policy/proposals/store-readiness.yml revision 4 (sha 27b365ec…): pattern adds `^fatal: could not read (Username|Password) for `.
  Synthetic harness: prompt texts/not-found/auth-failed/403 -> access-denied; DNS/refused/local path -> other; bash -n 0.
- #370 lineage review crashed at 0 turns, like #365. Both staged the 113 KB #359 report export (suspected cause,
  unconfirmed). Copied the JSON block to policy/proposals/lineage-pilot-359.json (sha 3c416ffd…, keys rules/decisions);
  re-ordered with no exports.
- Wrote execution/scripts/pin_runner_369.py (hash-gated, idempotent): pins the 3 N3 files under baseline, appends #369
  limitation sentence, re-pins status refs. Dry run twice on worktree of origin/main without env: 4 checks exit 0,
  65 refs, status 85b0f719…, preparation 403117b5…, only 2 files change, no pyc.
- Orders (parallel, main): review-lineage-pilot-359-noexport (reviewer, 50/35), pin-runner-contract-369 (benchmark,
  low, 20/25), rereview-store-workflow-v4-qr (reviewer, 30/25).
- Next: verify main 65 refs + status 85b0f719…, delete pin_runner_369.py. v4 accept -> one Owner `question`: install
  revision 4, new scorer token, run initial, revoke, run revoked, commit replacement record + .sha256; then independent
  record review. v4 revise -> fix file myself. If lineage review crashes again WITHOUT exports, investigate engine/profile
  (do not order a 4th time). Lineage accept -> bounded next triage batch; delete the proposal copy after landing.

## Iteration 0064 (#378, wake false)
- Considered record 0063, reports #374/#375/#376 (.session/history/sessions/37N/*.md). Startup ok, 29,640 tokens.
- #376 ACCEPT of store workflow revision 4 (sha 27b365ec…), codex GPT reviewer vs Claude author -> cross-family.
  Filed Owner `question` (revision 4): install rev 4, new scorer token, run initial, revoke, run revoked, commit
  replacement record + .sha256 at benchmark/split/store-readiness-268.redacted.json(.sha256).
- #374 lineage review (no exports, no crash -> export staging was the likely crash cause) REVISE: (1) candidate-0124/0227
  XML URLs resolve to absent archive members -> not verified; (2) no inventory pin. All other checks passed (coverage 13
  groups exact, pylavi hashes/LVSR offsets, six R3 groups); do not repeat. Rules R1-R3 may guide MANUAL public triage only.
- Wrote policy/proposals/lineage-pilot-359.json revision 2 (sha 57c558df…): both overlapping decisions R3/undecidable,
  top-level inventory pin lineage.json 52f3d2ea…. Result 5 same-lineage, 8 undecidable, 0 independent.
- #375 pin-runner CRASHED at 0 turns (no models). Main unchanged (status bcd2881b…, preparation 315d83a4…).
- Orders (parallel, main): pin-runner-contract-369-retry (benchmark, low, 20/25), recheck-lineage-pilot-374 (reviewer,
  medium, 30/25, diff rev1 vs rev2 only).
- Next: verify main 65 refs + status 85b0f719…, delete execution/scripts/pin_runner_369.py. If #375 retry crashes at 0
  turns again, investigate profile/runner; no 3rd identical order. Lineage accept -> hash-gated landing script writing
  the 13 adjudications into benchmark/lineage.json (re-pin; lineage.py --check needs env), then delete proposal copy;
  next bounded manual triage batch. Owner record arrives -> one independent record review (cross-family if possible).

## Iteration 0065 (#383, wake false)
- Considered record 0064, reports #380/#381 (.session/history/sessions/38N/*.md). Startup ok, 30,190 tokens.
- #380 ran pin_runner_369.py correctly (tag iter/0064/380 f25a6dd: status 85b0f719…, preparation 403117b5…) but
  ended `blocked`: its own git diff assertions saw an empty diff (my order asked it to confirm the 2-file change).
  Main unchanged (status bcd2881b…, preparation 315d83a4…). LESSON: no git diff/status acceptance in landing tasks;
  compare printed sha256 values only.
- #381 (codex GPT, author Policymaker Claude -> cross-family) ACCEPT of lineage pilot revision 2 (sha 57c558df…,
  inventory lineage.json 52f3d2ea…): 5 same-lineage, 8 undecidable, 0 independent. No blocking findings.
- FOUND: on main `lineage.py --check` exits 1 (stale preparation-status.json). lineage.py:29-37 limitation() still
  generates "(not independently re-reviewed)"; pin script #300 replaced it with the #298/#300 wording. Evaluator does
  not detect generator staleness.
- Wrote execution/scripts/land_runner_lineage_380.py: runs pin_runner_369.py, replaces that phrase in lineage.py
  (pin-gated), regenerates lineage, re-pins. Dry run twice on worktree of origin/main WITH env: exit 0, idempotent,
  evaluator 65 refs missing []; shas lineage.py 9b080b25…, lineage.json 52f3d2ea… (unchanged), lineage.md f3fc0534…,
  status 85b0f719…, preparation ccff5e0e…; only 3 files change; no pyc.
- Orders (parallel, main): land-runner-lineage-380 (benchmark, low, 20/25) and lineage-triage-batch-2 (benchmark,
  medium, 50/35, report only: next 10 two-member groups not in the pilot, R1-R3, JSON block with inventory + rules_source).
- Owner request #379 (install store workflow rev 4, rerun, commit record) pending; do not wait.
- Next: verify main shas above + lineage.py --check 0; delete pin_runner_369.py and land_runner_lineage_380.py.
  Order a cross-family review of batch 2 (author family from its models block). Then a hash-gated landing script
  writing pilot + accepted batches into lineage.json (lineage.py generates candidate status, so the script must
  change lineage.py or add a separate adjudication file pinned under split; decide then). When #379 record arrives,
  order one independent record review.

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
