# Execution working memory

## Considered
- Iteration 0219 / #933: startup documents read once. Iteration 0218 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #932 done (frozen dated checkers stay frozen; repair verify_method.py as a normal correction + changed-scope review in one graph).
- `benchmark/writing/pin-drift-0218.md` (0218 output) read whole: 4 pin-drift-only (0115, 0117, 0119, 0121), 6 unknown (fail-fast), 0 content-drift. Drifted: preparation.json, input-pins.json, c1-challenges-0125-pins.json, reviews-0128/c1-artifact-manifest-0126.json; changed by #758 ... #905 re-pins of challenge fixtures and score.py.
- verify_method.py read at lines 1-40, 321-350 (614 lines): fails at :338/:341 (EXTRA_HISTORICAL and historical loops). input-pins.json `protected_inputs_sha256`: 62 entries, 0 mismatches against disk (checked 0219).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN verify_method.py health (goal: write implementation waits for a method covering write tasks; the whole-method review needs a passing verifier). Ordered 0219: verifier-repin-0219 -> verifier-review-0219. Next: read the review verdict. CLEAR -> closes this scope; reassess the write-task coverage thread. NOT-CLEAR -> narrow correction of named findings + changed-scope review in one graph.
- CLOSED (by policy #932) frozen dated checkers check_*_01NN.py and reviews-0128/check_integrity_0128.py: pin drift on current tree is expected, 0 content-drift (#927, #930, pin-drift-0218). Do not run, survey or re-pin them. Replay at pinned commit only if a named review needs it.
- OPEN write-task coverage of the method: protocol.md has no write rows; writing split absent; WC1/WM1/WM2/WB1 keys need native capability/owner material (protocol-link-0217 `## Write contracts`). After verifier health: candidate writing row/addendum to the protocol map (benchmark/protocol.md is in owner_paths -> owner-gated).
- CLOSED rows measurement (0216, rows-0216.md). Do not re-measure EV:63-68.
- CLOSED scorer-intake scope: score_record.py (#913, #916, #919, CLEAR #920). Carry low: #920 f1, #916 f2-f4.
- CLOSED citation thread (#897/#898, #905/#906); XML key-agreement (#881/#882); citation-resolution (#889/#893/#894).
- OPEN challenges row (EV:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only.
- OPEN other gaps (next-gap-0202): dependency/native keys (needs LabVIEW); restricted split/allocation/isolation (#636 blockers); whole-method review + owner acceptance. benchmark_ready=false.
- Reader attempts blocked: no reader (product), no native refs, no model/quota/repetition decisions (owner) - reader-integration-0212 blockers 1-4.
- No-environment limit: score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; score_record.py --check and verify_method.py do not.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #920 f1; #916 f2-f4; #809 f2, f4; #763 f6; #898 hash-only re-pin check; #873 N/M count approximate; plan-0189 limit; pin-drift-0218: 0117 `predecessor_package_unchanged: false` cause untraced; 0121 PRE `649b7138` and 0123 PIN_MANIFEST `cab26fce` match no blob.
- Bytecode: run benchmark python with `python3 -B -I`; check with pathlib rglob('__pycache__'), not git status.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- verifier-repin-0219 (benchmark/default/high, 60 min/50 turns): new verify_method.py revision pinning current drifted inputs with old/new hash + commit chain; frozen checker hashes listed in body; live pin maps recomputed. Check: `python3 -I -B benchmark/writing/verify_method.py` exits 0; artifacts verify_method-before/after.out.
- verifier-review-0219 (reviewer/default/high, 45 min/40 turns, blocked_by repin): changed-scope review, pins merged commit and hashes itself, inputs the two .out artifacts. Expected gain: CLEAR verdict lets the whole-method review rely on the verifier.
- Frozen checker sha256 at 0219 start are in the repin task body (e.g. check_wp1_key_0115.py e7d22309...).

## Tried, do not repeat
- pin-drift-0218 classification done; do not re-classify the 10 checkers or replay them on the current tree.
- protocol-link-0217 coverage map and checker runs done; do not re-run the map.
- rows-0216 measurement done; do not re-measure rows or re-survey next-gap-0202.
- Scorer-intake thread done (#913, #916, #919, #920 CLEAR); do not re-review score_record.py.
- reader-integration survey done (0212); do not re-survey.
- Citation thread done end-to-end (#885 ... #906). XML key thread closed (#872, #873, #877, #878, #881, #882).
- Positive-control thread (#820 ... CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1).
- Finishing a partial on its branch with 20 turns worked (#889 -> #893).
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Probes/controls 0183, #808/#809, #791/#797, #785, #779, #766/#778: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190).
- Write the graph by ~10th call (0206-0219 at 8-11). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866/#882/#894/#898/#906/#920 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked.
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker edits. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
