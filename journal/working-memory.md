# Execution working memory

## Considered
- Iteration 0221 / #940: startup documents read once. Iteration 0220 closed, verdict none, not improved; no_progress=1; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #932 done.
- Record 0220: #938 method-review-0220 (reviewer, sonnet, 22 turns) done, verification pass, no repo changes, artifact released as `iter-0220/938-method-review-0220.md` (sha256 eb432303...). Report snapshot `.github/loop/data/session-reports/938/eb8cfeea...json` read whole.
- #938 verdict **NOT-READY**: 25 rows. MET (design only): R1a, R2, R3a, R5b, R6a, R7a, R8, R9, R10. UNMET-FIXABLE: R1b, R4a, R5a, R6b, R7b, R13a, R13b. BLOCKED native: R1c, R3b, R7c. BLOCKED owner material: R1d, R3c, R4b. BLOCKED owner decision: R6c, R11, R12. Hashes at review: evaluation.md d9eb079a..., README.md 8b6dd48d..., method.json 276f2881..., verify_method.py 4ab2552d...; verifier stdout sha dc92ae3e..., rejected_count 44.
- I did not read the artifact itself (only the report summary); counts above are from the report.

## State
- OPEN method corrections from #938, ordered by dependency:
  - UF-0 (root of #935 P1/P2): current pins live in historical integration-0112-provenance.json (verify_method.py ~414-423) + hard-coded HISTORICAL_REPINS / SELF_PRE_REPIN_SHA256. Ordered 0221 with changed-scope review.
  - UF-A (R7b): controls for omitted required ID, duplicate assertion, contradiction (protocol.md:92-110; verify_method.py:16-65, 259-296).
  - UF-B (R1b): WM1/WM2 `save_version: "unavailable"` (method.json:295, 368) vs header 20008000 in benchmark/sources.json; record as unverified header declaration like WP1.
  - UF-C (R4a) writing lineage map; UF-D (R5a) writing coverage matrix rows (rule at method.json:775); UF-E (R6b) hashed baseline addendum.
  - UF-F (R13a): no benchmark/writing/* in benchmark/preparation.json.
  - UF-G (R13b): benchmark/writing/verification.json records old checker da9f45e2 / stdout ae27dd58 (do last, after verifier changes settle).
  - Next after UF-0 CLEAR: UF-A + UF-B (different files? both may touch verify_method.py/method.json and the pin file -> chain with blocked_by or one task), then UF-C/D/E, UF-F, UF-G, each fix+review in one graph.
- After UF corrections: draft owner request for BLOCKED rows (native keys, human C1, restricted split/custodian, model quota/runs, evaluator scorer order, method acceptance). #430 declined a vague assessment request: frame concretely. Not a readiness claim.
- CLOSED (policy #932) frozen dated checkers check_*_01NN.py and reviews-0128/check_integrity_0128.py: pin drift expected. Do not run, survey or re-pin.
- OPEN write-task coverage: protocol.md has no write rows (owner_paths -> owner-gated); WC1/WM1/WM2/WB1 native keys need native capability/owner material.
- OPEN single lineage (Actor Framework only, restricted_evaluation_ready false, method.json:676, 818): BLOCKED owner material (R4b).
- OPEN other gaps (next-gap-0202): dependency/native keys; restricted split (#636); owner acceptance. benchmark_ready=false.
- Reader attempts blocked: reader-integration-0212 blockers 1-4.
- No-environment limit: score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; score_record.py --check and verify_method.py do not.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only.
- Carried minor findings: #935 P1, P2, S1, S2 (targeted by UF-0 task); #920 f1; #916 f2-f4; #809 f2, f4; #763 f6; #898; #873; plan-0189; pin-drift-0218 untraced items.
- Bytecode: `python3 -B -I`; check with pathlib rglob('__pycache__').
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved; #430 declined; #533 source-blocked.

## This iteration
- uf0-pins-0221 (benchmark/default/high, 60 min/45 turns): one current pin file + verifier revision reading it; rejecting wrong-hash control saved to `.session/artifacts/uf0-controls-0221.txt`; fix #935 S1/S2; frozen files unchanged; live pin maps recomputed. Check: `python3 -I -B benchmark/writing/verify_method.py` exit 0.
- uf0-review-0221 (reviewer/default/high, 45 min/35 turns, blocked_by uf0-pins-0221): changed-scope review, reproduces the control, marks #935 P1/P2/S1/S2 resolved or not; artifact uf0-review-0221.md.
- Expected gain: CLEAR -> UF-A/UF-B become one-file re-pin corrections next iteration.

## Tried, do not repeat
- Whole-method review #938 done (NOT-READY); do not re-review the whole method until UF rows are corrected.
- verify_method.py repin (#934) and review (#935 CLEAR) done.
- pin-drift-0218 classification done; protocol-link-0217 map done; rows-0216 done; next-gap-0202 done.
- Scorer-intake thread closed (#920 CLEAR). reader-integration survey done (0212). Citation thread, XML key thread, positive-control thread closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it.
- Pin corrections: verify the WHOLE live map against disk (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Before re-ordering failed work, Glob its expected output on main first (#800).
- Write the graph by ~10th call (0206-0221 at 8-11). Shaper #847 crashed at 21 turns.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- Negative POC 0092/0093 delivered; no fabricated VI, corpus restart or owner wait.
- Closed scopes #581 ... #935 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python one-liners stall; use file helpers.
- 0150/0151 input_budget partials; files-only split worked; fix+review in one graph worked.
- #713/#717 rule pointers in md and json; key `validation_rules`.
- No evaluator, old builders or frozen checker edits. Parent commits.
- Expectations before author applications (#567); not from score.py output (#763 f5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only.
- #617: read-back plus direct Python validation. Read report before Finish.
