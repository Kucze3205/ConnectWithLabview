# Method-acceptance owner request draft (Policymaker #426, iteration 0078)

Source: corrected draft of review #403 at main dacb5fba604f3686d85f548a787b3a6aa9f5912f
(snapshot .github/loop/data/session-reports/403/f2f9617058d208b792b09030f37e745cbc161705de5cc442eb61470642fb805a.json).
Changes vs #403: new commit and index hash; step 3 records the pinned change-case specifications
(reviews #408, #415, #421); step 4 records the pinned precision plan (reviews #409, #415, #421).
Status: unfiled. Independent fact-check ordered as review-method-request-draft-426.

---

**title:** Assess the verification method and its documented design limits

**what:** Please assess the verification method and its preparation evidence. Accept the documented design scope, or identify the changes you require.
Use main commit `0222240d1bd71d88c2bcec8c9084d739b3023aad`.
Use preparation index SHA256 `25cf0059164b7ec7d3be88f0bca00dbb16ccac85a82c0f8b28d5b6a7a31c1d35`.
Read `benchmark/protocol.md` at that commit and the evidence files that the index identifies.
The commit identifies the protocol because the index does not include it.
Exclude the unindexed native job draft `benchmark/native/job/` from the pinned acceptance evidence.

**why:** The method defines separate checks for reading fidelity, answer correctness and source grounding.
Existing reviews cover public XML keys, design contracts, change-case specifications, the precision plan and synthetic scoring tests.
The preparation status records their limits.
Missing evidence remains a requirement before implementation acceptance.
This decision establishes no benchmark readiness, quality threshold, goal gate or product claim.
It selects no fallback and reduces no goal scope.

**unblocks:** Your decision can settle acceptance of the documented design scope through the existing owner gate.
The loop then completes the remaining preparation and evidence requirements before implementation acceptance.
Each work change still requires the applicable owner decision.

1. Check the commit and the index hash above. Read the protocol and the limitations in `benchmark/preparation-status.json`. Keep the substantive evidence requirements of the protocol open.
2. Keep every execution gap. Native executions remain zero. All 23 native slots remain unresolved. No split allocation exists. Store readiness evidence remains pending #379 under capability #268. Native capability #169 remains not ready. No native key, native challenge result or matched model comparison exists.
3. Assess the two change-case specifications in `benchmark/change-cases/`: typedef-impact and diagram-difference. They are public specifications only. Their native answers are unavailable until #169 is ready. No edit or build grant exists. Edits and builds need your explicit grant before the loop does them.
4. Assess the precision plan in `benchmark/precision/`. It predeclares a 95% paired bootstrap at lineage level with seed 40502 and 10,000 resamples. The model and provider quota remains your decision. No paired run exists.
5. Keep the remaining oracle and comparison requirements. Semantic documentation is not pinned by version, location and content hash. Disputed expected claims need resolution before key use. The scorer keeps `independently_reviewed: false`.
6. Assess the recorded review limits. GPT-family authors and reviewers did the split, baseline-template, native-design and synthetic-scorer reviews. Review #347 used the same Anthropic family as its author. Reviews #369 and #421 checked fixes across model families. Review #421 found that a coordinated edit of two checker lines can bypass the reason controls. These reviews establish their recorded scopes only.
7. Read `docs/research/0002-delivery.md:105–109,123,143,153–163`. That report estimates 89–264 engineer-days for all versions and 33–99 for the 2024-only core. The difference of the corresponding endpoints is 56–165 engineer-days. These figures are uncertain planning estimates. The strict 2024 option of that report excludes 413 of its 415 versioned RSRC files. This information selects no fallback.
8. Record an explicit decision through the existing owner change gate. Identify the commit, the index hash, the accepted design scope and the remaining requirements. Accept that scope, or reject it and state the required changes. This decision approves no benchmark readiness, quality threshold, goal gate, product claim or fallback.
