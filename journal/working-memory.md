# Execution working memory

## Considered
- Iteration 0223 / #950: startup documents read once. Iteration 0222 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #944 done.
- Record 0222: #946 ufb-saveversion-0222 (benchmark, 22 turns) merged f4ec2667, accepted. #947 ufa-controls-0222 (benchmark, 27 turns) merged 8fba029b, accepted. #948 ufab-review-0222 (reviewer, 23 turns) done, verification pass; report snapshot `.github/loop/data/session-reports/948/3a2b2ab8...json` read whole. Artifact `iter-0222/948-ufab-review-0222.md` (sha256 3b64066e...) not read by me.
- #948 verdict **CLEAR** for R1b (UF-B) and R7b (UF-A). Reviewed tree: verify_method.py 5066235c..., method.json 985ad3b5..., current-pins.json e693909d... (printed inputs_sha256 equal), input-pins.json 972eb49d..., protocol.md 1aeb8322...; verifier exit 0, rejected_count 47, design-consistent; 33 current-pins entries 0 mismatches.
- #948 low findings: f1 README.md:42 says "Forty-four", no ledger controls / header_declaration mention (ordered in UF-E task 0223); f2 header_declaration guarded only by tasks[:4] hash, no named control vs sources.json; f3 WM1/WM2 nested declaration vs WP1 flat fields; f4 check_answer_ledger does not validate outcome values or tie them to credited assertions; contradiction checked per item, not per dimension (protocol.md:102).
- Record 0220 / #938 whole-method review NOT-READY (25 rows; counts from its report, artifact not read by me).

## State
- OPEN method corrections from #938 (UF-0, UF-A, UF-B CLOSED by #942, #948 CLEAR):
  - UF-C (R4a) lineage map, UF-D (R5a) writing coverage rows (rule near method.json:775), UF-E (R6b) hashed baseline addendum: ordered 0223 as a chain plus one review.
  - UF-F (R13a): no benchmark/writing/* in benchmark/preparation.json; needs preparation.json re-pinned in current-pins.json. Next after UF-C/D/E CLEAR.
  - UF-G (R13b): benchmark/writing/verification.json records old checker da9f45e2 / stdout ae27dd58; do last, after verifier changes settle.
  - Every correction re-pins by editing `benchmark/writing/current-pins.json`; chain tasks that touch it (blocked_by), never parallel.
- Carried low from #948: f2 (header_declaration control), f4 (ledger outcome validation, per-dimension contradiction). Candidate small correction with UF-F or UF-G; quote protocol.md before adding a rule.
- After UF corrections: draft owner request for BLOCKED rows (native keys R1c/R3b/R7c; owner material R1d/R3c/R4b; owner decision R6c/R11/R12). #430 declined a vague assessment request: frame concretely. Not a readiness claim.
- Carried low: #942 f2 (skipped provenance pins for live files, verify_method.py:430, :476); #920 f1; #916 f2-f4; #809 f2, f4; #763 f6; #898; #873; plan-0189; pin-drift-0218 untraced items.
- CLOSED (policy #932) frozen dated checkers check_*_01NN.py and reviews-0128/check_integrity_0128.py: pin drift expected. Do not run, survey or re-pin.
- OPEN write-task coverage: protocol.md has no write rows (owner_paths -> owner-gated); WC1/WM1/WM2/WB1 native keys need native capability/owner material.
- OPEN single lineage (Actor Framework only, restricted_evaluation_ready false): BLOCKED owner material (R4b).
- OPEN other gaps (next-gap-0202): dependency/native keys; restricted split (#636); owner acceptance. benchmark_ready=false.
- Reader attempts blocked: reader-integration-0212 blockers 1-4.
- No-environment limit: score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; score_record.py --check and verify_method.py do not.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only. Bytecode: `python3 -B -I`; check with pathlib rglob('__pycache__').
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved; #430 declined; #533 source-blocked.

## This iteration
- ufc-lineage-0223 (benchmark/default/high, 60 min/45 turns): R4a lineage map; missing lineages marked as gaps (R4b); re-pin current-pins.json. Check: verify_method.py exit 0.
- ufd-coverage-0223 (benchmark/default/high, 60/45, blocked_by ufc): R5a writing coverage rows by kind/version, gaps visible; re-pin.
- ufe-baseline-0223 (benchmark/default/high, 60/45, blocked_by ufd): R6b hashed baseline addendum plus #948 f1 README count fix; re-pin.
- ufcde-review-0223 (reviewer/default/high, 50/40, blocked_by ufe): changed-scope review per row; artifact ufcde-review-0223.md; records current-pins.json printed hash.
- Expected gain: R4a, R5a, R6b -> MET (design). Next shaper reads the review verdict; CLEAR -> order UF-F (then UF-G); NOT-CLEAR -> correct the named findings plus changed-scope review.
- Risk: three chained writers on one file; if one goes partial, resume it with start_branch, do not redo merged siblings.

## Tried, do not repeat
- UF-A/UF-B fixes (#946, #947) and review (#948 CLEAR) done; do not re-review.
- UF-0 fix (#941) and review (#942 CLEAR) done; do not re-review UF-0.
- Whole-method review #938 done (NOT-READY); do not re-review the whole method until UF rows are corrected.
- verify_method.py repin (#934) and review (#935 CLEAR) done.
- pin-drift-0218 classification done; protocol-link-0217 map done; rows-0216 done; next-gap-0202 done.
- Scorer-intake thread closed (#920 CLEAR). reader-integration survey done (0212). Citation thread, XML key thread, positive-control thread closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it.
- Pin corrections: verify the WHOLE live map against disk (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Before re-ordering failed work, Glob its expected output on main first (#800).
- Write the graph by ~10th call (0206-0223 at 8-11). Shaper #847 crashed at 21 turns.
- 0223 shaper: a Write with empty text blanked this file; always put the content in `text`.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- Negative POC 0092/0093 delivered; no fabricated VI, corpus restart or owner wait.
- Closed scopes #581 ... #948 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python one-liners stall; use file helpers.
- 0150/0151 input_budget partials; files-only split worked; fix+review in one graph worked (0221, 0222).
- No evaluator, old builders or frozen checker edits. Parent commits.
- Expectations before author applications (#567); not from score.py output (#763 f5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only.
- #617: read-back plus direct Python validation. Read report before Finish.
