# Execution working memory

## Considered
- Iteration 0226 / #966: startup documents read once. Iteration 0225 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #961 done.
- Record 0225: #963 verifier-sections-finish (benchmark, 17 turns) done, merged 78ecbc3d, verification pass, accepted. #964 uff-review (reviewer, 29 turns) done; report snapshot `.github/loop/data/session-reports/964/0c9220b7...json`; artifact uff-review-0225.md (release iter-0225/964-uff-review-0225.md).
- #964 verdicts: R13a CLEAR; #954 f2 CLEAR; #954 f4 CLEAR (candidate-0033) with residual; new verifier checks CLEAR. Reviewed tree: verify_method.py 67b934d6..., method.json 195697bf..., current-pins.json 63cfe6da..., input-pins.json 3979779e..., README.md 95ac1605..., preparation.json c5cf2ff5..., baseline-addendum.json b46e7fb6...; rejected_count 64 (README.md:44).
- #964 findings (non-blocking): f1 consumer completeness (verify_method.py:789 complete=False; artifact-0087 omits candidate-0043); f2 variant_member_artifacts and source line anchor (method.json:943) unenforced; f3 no mutation for lineage-map-group / lineage-map-tasks; f4 observation (current-pins 36 vs 37 entries).
- #964 discovery: preparation.json does not register current-pins.json, input-pins.json, integration-0112 provenance, review-corrections.json, review-0110* (judgement, not demanded by R13a).
- Record 0220 / #938 whole-method review NOT-READY (25 rows).

## State
- OPEN method corrections from #938: UF-0, UF-A..UF-F CLOSED (#942, #948, #954, #964 CLEAR). #954 f1 closed by #963 + #964.
  - #964 f1-f3: correction ordered 0226 (lineage-complete-0226).
  - UF-G (R13b): verification.json records old checker da9f45e2 / stdout ae27dd58; ordered 0226 (ufg-0226) after the correction. Possible circularity if the verifier pins verification.json; the task asks the worker to re-run and report.
  - Every correction re-pins `benchmark/writing/current-pins.json`; chain tasks touching it (blocked_by), never parallel.
- Carried low: #954 f3, f5, f6, f7; #948 f2 (header_declaration control), f3, f4 (ledger outcome validation, per-dimension contradiction; quote protocol.md before adding a rule); #964 f4 and discovery (preparation.json registrations).
- After ufg-review-0226 CLEAR: whole-method re-review of #938 rows (changed rows only plus summary), then draft owner request for BLOCKED rows (native keys R1c/R3b/R7c; owner material R1d/R3c/R4b; owner decision R6c/R11/R12). #430 declined a vague request: frame concretely. Not a readiness claim.
- Carried low: #942 f2 (verify_method.py:430, :476); #920 f1; #916 f2-f4; #809 f2, f4; #763 f6; #898; #873; plan-0189; pin-drift-0218 untraced.
- CLOSED (policy #932) frozen dated checkers check_*_01NN.py and reviews-0128/check_integrity_0128.py: pin drift expected. Do not run, survey or re-pin.
- OPEN write-task coverage: protocol.md has no write rows (owner_paths -> owner-gated); WC1/WB1 have no original.
- OPEN single lineage (Actor Framework only): BLOCKED owner material (R4b).
- OPEN other gaps (next-gap-0202): dependency/native keys; restricted split (#636); owner acceptance. benchmark_ready=false.
- Reader attempts blocked: reader-integration-0212 blockers 1-4.
- No-environment limit: score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; score_record.py --check, verify_method.py, build_addendum.py --check do not.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only. Bytecode: `python3 -B -I`; check with pathlib rglob('__pycache__').
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved; #430 declined; #533 source-blocked.

## This iteration
- lineage-complete-0226 (benchmark/default/high, 60 min/40 turns): fix #964 f1-f3 in verify_method.py + method.json (candidate-0043), mutations, README count (>64), re-pin. Check: verify_method.py exit 0.
- ufg-0226 (benchmark/default/high, 50/35, blocked_by lineage-complete): R13b, verification.json records current verifier sha256 and real stdout hash; re-pin maps listing it.
- ufg-review-0226 (reviewer/default/high, 50/40, blocked_by ufg): changed-scope review; artifact ufg-review-0226.md; verdict per f1, f2, f3, R13b.
- Expected gain: all UF rows and #954/#964 residuals closed. CLEAR -> order whole-method re-review of #938 changed rows. NOT-CLEAR -> correct named findings plus changed-scope review in one graph.
- If a task goes partial: inspect its branch with git show, finish on start_branch with <=20 turns; do not resume a third time.

## Tried, do not repeat
- #958 partial (45 turns), finished by #963 on task/958 in 17 turns; do not redo.
- UF-F (#957) and #954 f1 (#963) reviewed CLEAR by #964; do not re-review.
- UF-C/D/E fixes (#951-#953) and review (#954 CLEAR) done; do not re-review.
- UF-A/UF-B (#946, #947, #948 CLEAR); UF-0 (#941, #942 CLEAR) done.
- Whole-method review #938 done (NOT-READY); re-review only after UF-G review.
- verify_method.py repin (#934) and review (#935 CLEAR) done.
- pin-drift-0218 classification done; protocol-link-0217 map done; rows-0216 done; next-gap-0202 done.
- Scorer-intake thread closed (#920 CLEAR). reader-integration survey done (0212). Citation, XML key, positive-control threads closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it.
- Pin corrections: verify the WHOLE live map against disk (#857 f4, #861 f1).
- Finishing a partial on its branch with few turns worked (#889 -> #893; #958 -> #963).
- Before re-ordering failed work, Glob its expected output on main first (#800).
- Write the graph by ~10th call (0206-0226 at 8-11). Shaper #847 crashed at 21 turns.
- 0223 shaper: a Write with empty text blanked this file; always put the content in `text`.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- Negative POC 0092/0093 delivered; no fabricated VI, corpus restart or owner wait.
- Closed scopes #581 ... #964 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python one-liners stall; use file helpers.
- 0150/0151 input_budget partials; files-only split worked; fix+review in one graph worked (0221-0225).
- No evaluator, old builders or frozen checker edits. Parent commits.
- Expectations before author applications (#567); not from score.py output (#763 f5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only.
- #617: read-back plus direct Python validation. Read report before Finish.
