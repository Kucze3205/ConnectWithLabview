# Execution working memory

## Considered
- Iteration 0222 / #945: startup documents read once. Iteration 0221 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #944 done.
- Record 0221: #941 uf0-pins-0221 (benchmark, sonnet, 41 turns) done, merged ab67ce1e, check pass, accepted. #942 uf0-review-0221 (reviewer, 21 turns) done, verification pass; report snapshot `.github/loop/data/session-reports/942/571d0730...json` read whole. Artifact `iter-0221/942-uf0-review-0221.md` (sha256 cdeda81f...) not read by me.
- #942 verdict **CLEAR** for UF-0. Reviewed tree: verify_method.py 1e86831b..., current-pins.json b225ccc2..., README.md 33ea7c05..., input-pins.json 972eb49d...; verifier exit 0, rejected_count 44, status design-consistent. #935 P1/P2/S1/S2 resolved. Two low findings: (1) verifier cannot pin itself inside current-pins.json; reviewers must record printed `inputs_sha256` of current-pins.json (README.md:66); (2) provenance `outputs`/proposal pins for live files skipped by `continue` (verify_method.py:430, :476).
- Record 0220 / #938 whole-method review NOT-READY (25 rows; counts from its report, artifact not read by me).

## State
- OPEN method corrections from #938 (UF-0 CLOSED by #941/#942 CLEAR):
  - UF-B (R1b) and UF-A (R7b): ordered 0222 with one changed-scope review.
  - UF-C (R4a) writing lineage map; UF-D (R5a) writing coverage matrix rows (rule at method.json:775); UF-E (R6b) hashed baseline addendum. Next after UF-A/B CLEAR.
  - UF-F (R13a): no benchmark/writing/* in benchmark/preparation.json; per #942 it needs preparation.json re-pinned in current-pins.json.
  - UF-G (R13b): benchmark/writing/verification.json records old checker da9f45e2 / stdout ae27dd58; do last, after verifier changes settle.
  - Every correction re-pins by editing `benchmark/writing/current-pins.json`; chain tasks that touch it (blocked_by), never parallel.
- After UF corrections: draft owner request for BLOCKED rows (native keys R1c/R3b/R7c; owner material R1d/R3c/R4b; owner decision R6c/R11/R12). #430 declined a vague assessment request: frame concretely. Not a readiness claim.
- Carried low: #942 f1 (self-pin practice, asked of 0222 review), #942 f2 (skipped provenance pins); #920 f1; #916 f2-f4; #809 f2, f4; #763 f6; #898; #873; plan-0189; pin-drift-0218 untraced items.
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
- ufb-saveversion-0222 (benchmark/default/medium, 45 min/35 turns): WM1/WM2 save_version as unverified header declaration (20008000 from benchmark/sources.json) in WP1 shape; re-pin method.json in current-pins.json. Check: verify_method.py exit 0.
- ufa-controls-0222 (benchmark/default/high, 60/45, blocked_by ufb): three rejecting controls (omitted required ID, duplicate, contradiction) quoting protocol.md lines; output `.session/artifacts/ufa-controls-0222.txt`; re-pin; old/new rejected_count (44 before).
- ufab-review-0222 (reviewer/default/high, 45/35, blocked_by ufa): changed-scope review per row; records current-pins.json printed hash; artifact ufab-review-0222.md.
- Expected gain: R1b, R7b -> MET (design). Next shaper reads the review verdict; CLEAR -> order UF-C/D/E chain.

## Tried, do not repeat
- UF-0 fix (#941) and review (#942 CLEAR) done; do not re-review UF-0.
- Whole-method review #938 done (NOT-READY); do not re-review the whole method until UF rows are corrected.
- verify_method.py repin (#934) and review (#935 CLEAR) done.
- pin-drift-0218 classification done; protocol-link-0217 map done; rows-0216 done; next-gap-0202 done.
- Scorer-intake thread closed (#920 CLEAR). reader-integration survey done (0212). Citation thread, XML key thread, positive-control thread closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it.
- Pin corrections: verify the WHOLE live map against disk (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Before re-ordering failed work, Glob its expected output on main first (#800).
- Write the graph by ~10th call (0206-0222 at 8-11). Shaper #847 crashed at 21 turns.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- Negative POC 0092/0093 delivered; no fabricated VI, corpus restart or owner wait.
- Closed scopes #581 ... #942 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python one-liners stall; use file helpers.
- 0150/0151 input_budget partials; files-only split worked; fix+review in one graph worked (0221 again).
- No evaluator, old builders or frozen checker edits. Parent commits.
- Expectations before author applications (#567); not from score.py output (#763 f5).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only.
- #617: read-back plus direct Python validation. Read report before Finish.
