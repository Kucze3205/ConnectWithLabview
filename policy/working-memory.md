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
