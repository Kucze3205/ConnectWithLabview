# Execution working memory

## Considered
- Iteration 0220 / #937: startup documents read once. Iteration 0219 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #932 done.
- Record 0219: #934 verifier-repin-0219 done/merged (commit 81973732); #935 verifier-review-0219 done, report snapshot `.github/loop/data/session-reports/935/75e358b4...json` read whole: **CLEAR** at b88d3ff9, verify_method.py sha256 4ab2552d..., exit 0, stdout ends `"status": "design-consistent"`, rejected_count 44.
- #935 findings (non-blocking): P1 medium (outputs pin of verify_method.py compared only to old hash da9f45e2..., not tamper detection); P2 low (hard-coded HISTORICAL_REPINS break on next challenge/score.py re-pin; no rejecting control for that branch); S1 low (comment chain lists 83a4c7a8 wrongly for input-pins.json); S2 low (README.md:66 not updated for re-pins); P3 info (frozen records pin old verifier hash, intended).
- `benchmark/writing/protocol-link-0217.md` read whole (protocol map, write contracts, recommendation).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- CLOSED verify_method.py health: #934 repin + #935 CLEAR. Carry P1, P2 as stated limits; S1, S2 optional cleanup (could be one small benchmark correction later; not worth a review chain alone).
- OPEN whole-method review of the writing extension (goal: write implementation waits for an accepted method covering write tasks). Ordered 0220: method-review-0220 (reviewer). Next: read its requirement table (`.session/artifacts/method-review-0220.md`, report). UNMET-FIXABLE rows -> order corrections (one graph with changed-scope review); if only BLOCKED rows remain -> draft owner request (`.session/requests.json`) for method acceptance with blockers stated; NOT a readiness claim.
- CLOSED (policy #932) frozen dated checkers check_*_01NN.py and reviews-0128/check_integrity_0128.py: pin drift expected. Do not run, survey or re-pin.
- OPEN write-task coverage: protocol.md has no write rows (owner_paths -> owner-gated); writing split absent; WC1/WM1/WM2/WB1 native keys need native capability/owner material (protocol-link-0217 `## Write contracts`).
- OPEN challenges row (EV:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only.
- OPEN other gaps (next-gap-0202): dependency/native keys (needs LabVIEW); restricted split/allocation/isolation (#636 blockers); owner acceptance. benchmark_ready=false.
- Reader attempts blocked: no reader (product), no native refs, no model/quota/repetition decisions (owner) - reader-integration-0212 blockers 1-4.
- No-environment limit: score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; score_record.py --check and verify_method.py do not.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #935 P1, P2, S1, S2; #920 f1; #916 f2-f4; #809 f2, f4; #763 f6; #898 hash-only re-pin check; #873 N/M count approximate; plan-0189 limit; pin-drift-0218: 0117 `predecessor_package_unchanged: false` untraced; 0121 PRE `649b7138` and 0123 PIN_MANIFEST `cab26fce` match no blob.
- Bytecode: run benchmark python with `python3 -B -I`; check with pathlib rglob('__pycache__'), not git status.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined (method assessment request declined: a new acceptance request needs a different, concrete framing). #533 source-blocked.

## This iteration
- method-review-0220 (reviewer/default/high, 60 min/45 turns): whole-method review of the writing extension against docs/perpetua/evaluation.md; per-requirement verdict MET / UNMET-FIXABLE / BLOCKED with file:line; overall READY-FOR-OWNER-ACCEPTANCE or NOT-READY. Carries #935 P1/P2/S1/S2 and the write-contract gaps without re-measuring. Check: `python3 -I -B benchmark/writing/verify_method.py` exit 0; artifact method-review-0220.md.
- Expected gain: a requirement table that decides between corrections and an owner method-acceptance request.

## Tried, do not repeat
- verify_method.py repin (#934) and its review (#935 CLEAR) done; do not re-review that scope without changed evidence.
- pin-drift-0218 classification done; do not re-classify the 10 checkers or replay them on the current tree.
- protocol-link-0217 coverage map and checker runs done; do not re-run the map.
- rows-0216 measurement done; do not re-measure rows or re-survey next-gap-0202.
- Scorer-intake thread done (#913, #916, #919, #920 CLEAR); do not re-review score_record.py.
- reader-integration survey done (0212); do not re-survey.
- Citation thread done end-to-end (#885 ... #906). XML key thread closed (#872 ... #882).
- Positive-control thread (#820 ... CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Probes/controls 0183, #808/#809, #791/#797, #785, #779, #766/#778: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190).
- Write the graph by ~10th call (0206-0220 at 8-11). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866/#882/#894/#898/#906/#920/#935 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked.
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker edits. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
