# Execution working memory

## Considered
- Iteration 0225 / #962: startup documents read once. Iteration 0224 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #961 done.
- Record 0224: #957 uff-preparation (benchmark, 40 turns) done, merged f3e6a2f7, verification pass. #958 verifier-sections partial at 45/45 turns (cause session_budget, branch task/958, commit 27030059); report snapshot `.github/loop/data/session-reports/958/7f02825c...json` holds only the status block, no description. #959 uff-review blocked (dependency not done, 0 turns).
- I did not inspect the task/958 tree; the finishing task's first step is to list done/missing.
- Record 0223 / #954 CLEAR for R4a, R5a, R6b. Reviewed tree: verify_method.py 5066235c..., method.json 5a7fb194..., current-pins.json 38f5e9ff..., README.md 6652f6f0...; rejected_count 47.
- #954 findings: f1 verifier lacks lineage_map / matrix / addendum checks (in progress, #958); f2 README, f4 WM2 candidate-0033 (fixed by #957, unreviewed); f3, f5, f6, f7 carried low.
- Record 0220 / #938 whole-method review NOT-READY (25 rows).

## State
- OPEN method corrections from #938: UF-0, UF-A..UF-E CLOSED (#942, #948, #954 CLEAR).
  - UF-F (R13a): done by #957 (merged f3e6a2f7), awaiting review uff-review-0225.
  - #954 f1 verifier sections: #958 partial; finishing task ordered 0225 on start_branch task/958.
  - UF-G (R13b): benchmark/writing/verification.json records old checker da9f45e2 / stdout ae27dd58; order after uff-review-0225 CLEAR.
  - Every correction re-pins `benchmark/writing/current-pins.json`; chain tasks touching it (blocked_by), never parallel.
- Carried low: #954 f3, f5, f6, f7; #948 f2 (header_declaration control), f3, f4 (ledger outcome validation, per-dimension contradiction; quote protocol.md before adding a rule). Candidates to ride with UF-G.
- After UF corrections: whole-method re-review of #938 rows (changed rows only plus summary), then draft owner request for BLOCKED rows (native keys R1c/R3b/R7c; owner material R1d/R3c/R4b; owner decision R6c/R11/R12). #430 declined a vague request: frame concretely. Not a readiness claim.
- Carried low: #942 f2 (verify_method.py:430, :476); #920 f1; #916 f2-f4; #809 f2, f4; #763 f6; #898; #873; plan-0189; pin-drift-0218 untraced.
- CLOSED (policy #932) frozen dated checkers check_*_01NN.py and reviews-0128/check_integrity_0128.py: pin drift expected. Do not run, survey or re-pin. Historical maps drift by design.
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
- verifier-sections-finish-0225 (benchmark/default/high, 60 min/40 turns, start_branch task/958): list done/missing first, then finish #954 f1 checks, mutations (rejected_count > 47), README count, re-pin. Check: verify_method.py exit 0, build_addendum --check.
- uff-review-0225 (reviewer/default/high, 50/40, blocked_by finish): changed-scope review of #957 + #958/finish; artifact uff-review-0225.md.
- Expected gain: #954 f1/f2/f4 and R13a closed by review. CLEAR -> order UF-G (R13b) with carried lows; NOT-CLEAR -> correct named findings plus changed-scope review.
- If the finishing task goes partial again: do not resume a third time; inspect task branch with git show, split by file (verifier checks vs mutations/README/pins).

## Tried, do not repeat
- #958 full verifier-sections task ran 45 turns, partial; resumed once in 0225. Never resume the same full task a third time.
- UF-F done (#957); do not redo.
- UF-C/D/E fixes (#951-#953) and review (#954 CLEAR) done; do not re-review.
- UF-A/UF-B (#946, #947, #948 CLEAR); UF-0 (#941, #942 CLEAR) done.
- Whole-method review #938 done (NOT-READY); re-review only after UF-F/UF-G.
- verify_method.py repin (#934) and review (#935 CLEAR) done.
- pin-drift-0218 classification done; protocol-link-0217 map done; rows-0216 done; next-gap-0202 done.
- Scorer-intake thread closed (#920 CLEAR). reader-integration survey done (0212). Citation, XML key, positive-control threads closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it.
- Pin corrections: verify the WHOLE live map against disk (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Before re-ordering failed work, Glob its expected output on main first (#800).
- Write the graph by ~10th call (0206-0225 at 8-11). Shaper #847 crashed at 21 turns.
- 0223 shaper: a Write with empty text blanked this file; always put the content in `text`.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- Negative POC 0092/0093 delivered; no fabricated VI, corpus restart or owner wait.
- Closed scopes #581 ... #954 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python one-liners stall; use file helpers.
- 0150/0151 input_budget partials; files-only split worked; fix+review in one graph worked (0221-0223).
- No evaluator, old builders or frozen checker edits. Parent commits.
- Expectations before author applications (#567); not from score.py output (#763 f5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only.
- #617: read-back plus direct Python validation. Read report before Finish.
