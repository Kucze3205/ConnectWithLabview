# Execution working memory

## Considered
- Iteration 0218 / #929: startup documents read once. Iteration 0217 closed, verdict accepted, improved; no_progress=0; rollback streak 1; outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #922 done.
- `benchmark/writing/protocol-link-0217.md` (0217 output) read whole: 0 of 10 writing checkers pass; every readable failure is pin/hash drift (preparation.json, input-pins.json, c1-artifact-manifest-0126.json); 0115/0117 causes not inspected. Write contracts WC1/WM1/WM2/WB1 have no independent key (native/owner blocked); WP1 text key exists (wp1-key-0123). Protocol has no write row; writing split absent; baseline design only.
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- OPEN writing-checker health (goal: write implementation waits for a method covering write tasks). Reason open: 0/10 checkers pass on current tree (protocol-link-0217 `## Checker runs`). Ordered 0218: pin-drift-0218 -> `benchmark/writing/pin-drift-0218.md`. Next: read its `## Recommendation`. If all pin-drift-only, send a Policymaker suggestion (or order a permitted writer) to decide a re-pin of live maps vs frozen snapshots (README.md:60 says #544 checker is frozen by design); if content-drift, order a narrow correction + changed-scope review in one graph.
- OPEN write-task coverage of the method: protocol.md has no write rows; writing split absent; WC1/WM1/WM2/WB1 keys need native capability/owner material (protocol-link-0217 `## Write contracts`). After checker health, candidate: add a writing row/addendum to the protocol map (owner_paths include benchmark/protocol.md -> owner-gated).
- CLOSED rows measurement (0216, rows-0216.md). Do not re-measure EV:63-68.
- CLOSED scorer-intake scope: score_record.py (#913, #916, #919, CLEAR #920). Carry low: #920 f1, #916 f2-f4.
- CLOSED citation thread (#897/#898, #905/#906); XML key-agreement (#881/#882); citation-resolution (#889/#893/#894).
- OPEN challenges row (EV:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only.
- OPEN other gaps (next-gap-0202): dependency/native keys (needs LabVIEW); restricted split/allocation/isolation (#636 blockers); whole-method review + owner acceptance. benchmark_ready=false.
- Reader attempts blocked: no reader (product), no native refs, no model/quota/repetition decisions (owner) - reader-integration-0212 blockers 1-4.
- No-environment limit: score.py generation, --check, self-test need LABVIEW_ENVIRONMENT; score_record.py --check and the writing checkers do not.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #920 f1; #916 f2-f4; #809 f2, f4; #763 f6; #898 hash-only re-pin check; #873 N/M count approximate; plan-0189 limit.
- Bytecode: run benchmark python with `python3 -B -I`; check with pathlib rglob('__pycache__'), not git status.
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- pin-drift-0218 (benchmark/default/medium, 60 min/40 turns): measurement only; classifies each of the 10 failures as pin-drift-only / content-drift / unknown, reads full 0115/0117 output via `.session/artifacts/`, drift table with pinned vs current sha256 and changing commit/issue. No re-pin, no checker edits.
- Expected gain: know whether any writing checker could pass after a re-pin; check: verification command (headings + checker names) and `## Recommendation`.

## Tried, do not repeat
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
- Write the graph by ~10th call (0206-0218 at 8-11). Shaper #847 crashed at 21 turns: stay short.
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
