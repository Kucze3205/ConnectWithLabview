# Execution working memory

## Considered
- Iteration 0208 / #892: startup documents read once. Iteration 0207 closed, verdict none, not improved (record 0207.json); no_progress=1; rollback streak 1 (0190, quiet time); outboxes 787, 837, 851; no open requests; goal gate unaccepted; Policymaker #887 done.
- #889 (citation-check-0207) report snapshot `.github/loop/data/session-reports/889/b6dde20d...json` read whole: partial on 60-turn cap (cause session_budget), branch task/889 commit 7d62165a, not merged. #890 review blocked (never ran, producer partial).
- Final .session/tasks.json validated by the direct Python JSON/heading check, exit 0.

## State
- CLOSED XML key-agreement scope for library inventories (#881, CLEAR #882 at abd491f9). Do not reopen.
- OPEN #831 citation gap: design citation-gap-0206.md (#885). Implementation saved on task/889 (7d62165a): citation_resolves/citations_resolve/combine_grounding/environment_loader in score.py; controls 1-7 all match expectations (control 4 now `incorrect`); challenges.json 35/35; input-pins 62 and preparation.json 80 entries match disk; inventory_sha256 in library-icon-tests.json and library-specialty.json refreshed (stale since #881). Open item: preparation-status.json mirror not ruled out. 0208 finishes on the branch and reviews. Next: read review verdict; NOT-CLEAR -> correct named findings + changed-scope review; CLEAR -> close scope, then decide `answer_record_contract` string-vs-dict shape (fixture pinned in three places) and extension to library-icon-tests / vi-actor-core-native-gap (no citations there).
- New limit from #889: score.py generation, --check and self-test now need LABVIEW_ENVIRONMENT; without it citation_controls raises. Consider whether a no-environment mode is needed (engine verification cannot see the environment).
- OPEN challenges row (evaluation.md:69). gap-0160 (#725): all five kinds `partial`, synthetic fixtures only; challenges.json self-comparison (quality_measured false).
- Other method gaps (next-gap-0202 `## Gaps`): dependency/native keys OPEN (N0001/N0002 native-unverified; needs LabVIEW); restricted split/allocation/isolation OPEN (#636 blockers); reader/probes/scorer integration PARTIAL (zero reader attempts); whole-method review + owner acceptance OPEN; sources/tasks/oracle/coverage/baseline rows not re-measured. benchmark_ready=false.
- #873 minor: failure N/M count counts distinct mismatching IDs (approximate); MISMATCH lines authoritative.
- Tool-disable message: native-tool refusal, not broker failure (#854); keep the pointer in task bodies.
- Grep is literal-substring only; empty match on existing file -> Read in ranges.
- Carried minor findings: #809 f2, #809 f4; #763 f6; plan-0189 limit: vi-actor-core-native-gap.json not counted.
- Bytecode trap: tasks running benchmark python use `python3 -B -I`, check `git status --porcelain` (#785).
- POC unsuccessful bounded delivery accepted 0093, docs/research/poc/delivery.md. No session can run LabVIEW.
- Owner #618 declined human C1; #532 approved metadata only; #430 declined. #533 source-blocked.

## This iteration
- citation-check-finish-0208 (benchmark/default/medium, start_branch task/889, 45 min/20 turns): no rewrite; confirm checks on branch, scan preparation-status.json for OLD hashes of #889-changed files via helper script, fix with Edit and re-verify full pin maps, report.
- citation-check-review-0208 (reviewer/default/medium, 60 min/40 turns, blocked_by finish): expectations artifact first; rule check incl. environment_loader None cases; fixture inventory_sha256 check; --check with env; byte-for-byte regeneration; full pin recomputation; checker unchanged.
- Expected gain: #831 grounding check merged with a CLEAR/NOT-CLEAR verdict. Check = finish report (merged, pins OK) + reviewer verdict.

## Tried, do not repeat
- citation-check-0207 (#889) full implementation ran 60 turns at high effort; do not re-order the full task — finish only (third full attempt banned).
- Citation gap measurement + design done (#885, citation-gap-0206.md); do not re-measure.
- XML key thread: cold keys 0191, 0203 (#872), 0204 (#877); checker + 10/10 specialty (#873); 10/10 icon-tests (#878); agreement recorded (#881), CLEAR (#882). Closed.
- next-gap survey done (0202, next-gap-0202.md); do not re-survey the gaps table.
- Positive-control thread (#820, 0191, #828, #831, #852, #856, #857, #860/#861, #865, CLEAR #866). Closed.
- Step 4 attempts #834, #838, #848, #852 stopped on the native-tool message; pointer in task body fixed it (0199).
- Pin corrections: verify the WHOLE live map against disk, not one hash (#857 f4, #861 f1); #881, #889 did it right.
- Regeneration of challenges.json done (#812/#816, CLEAR #817). Keyed-literal probe (0183), control (#808, CLEAR #809), constant-export probe #791/#797, mutation check #785, #779, #766/#778 re-pin: done.
- Before re-ordering failed work, Glob its expected output on main first (#800, 0190). Partial with recorded branch is resumable (#812 -> #816).
- Write the graph by ~10th call (0206 at 10, 0207 at 8, 0208 at 8). Shaper #847 crashed at 21 turns: stay short.
- #754: report `commit:` fields may name an empty commit; verify by hash. #882: HEAD may be an epilogue commit; diff against the task commit's parent.
- #465/#468 framing/mutations do not establish semantics; negative POC 0092/0093 delivered. No fabricated changed VI, corpus restart, duplicate delivery or owner wait.
- Closed scopes #581/#587/#594/#612/#626/#633/#639/#656/#678/#685/#703/#722/#809/#817/#866/#882 stay closed. gap-0160, scorer-probe-0164, #739, #751: do not re-survey.
- #743: long inline python3 one-liners stall; use file-based helpers.
- 0150/0151 partial input_budget; files-only split worked; fix+review in one graph worked (0154-0205 several).
- #713: corrections touching md and json list every rule pointer in both. #717: json key is `validation_rules`.
- #643 prohibited evaluator call earns no credit. No evaluator, old builders or frozen #544/0125 checker. Parent commits.
- Deriving positive expectations from score.py output is not independent (#763 f5). Expectations before author applications (#567).
- evaluation.md is Polish; Read whole. Inputs stage flat; counts from bytes (#518).
- Reviewers write report/artifacts only. Engine verification: repository-only checks, no environment.
- #617 invalid quoting: read-back plus direct Python validation. Empty Write erases files. Read report before Finish.
