# Policy working memory

Considered: iteration records 0000–0018; reviews #146/#147; #150 and acceptance #151; #157 and acceptance #161;
re-review #166; reports #170/#172/#175; acceptance #176.
Updated by Policymaker #178, iteration 0019.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`;
selected reports `.session/history/sessions/<issue>/`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; without valid orders the iteration fails (0017 failed so).
- Protocol re-review #166 (codex) closed F1/F2 at 2669ec4, overall accept; design review lacked model-family diversity.
- Iteration 0018 (#175, codex/gpt-6.1-sol, 20 turns, ~300k input, 292 s) restored d0e14f6 and landed it (owner #176
  approved). `dev_cases.py --check` exit 0, `evaluate.py --check` exit 0 (35 evidence refs, benchmark_ready=false).
  11 public dev cases: 3 .lvproj, 3 .lvclass, 4 .lvlib, 1 .vi native-gap; 1,053 XML slots + 23 native-required slots
  (README, author-reported). All share-or-use lineage group `public-ni-actor-framework-all-projects-copies-variants`.
- Milestones: sources/coverage/tasks/oracle prepared-not-reviewed; split/baseline/challenges not-started.
  Evaluator schema only checks the seven milestone names + evidence refs (policy/evaluator/evaluate.py:10,45-53);
  status words live in benchmark/preparation-status.json.
- Owner acceptance of the method NOT requested: needs reviewed tasks/oracle/split/baseline/challenge evidence first.

## Iteration 0019 orders (#178, no wake)
- `review-dev-cases` (reviewer, default alias → routing claude-sonnet first, so likely cross-family vs codex author):
  independent re-extraction script, sha256 checks, per-family agree/disagree/unresolvable counts, Standards/Spec
  findings, recommendation accept/revise/reject. Expected gain: first independent claim-level agreement for dev keys.
- `lineage-exact-duplicates` (benchmark): `benchmark/scripts/lineage.py` + `benchmark/lineage.json`/`lineage.md`,
  exact-copy groups and unadjudicated candidate variants of public sources; split stays `not-started`.
  Expected gain: reproducible public lineage inventory as first split preparation, no private data.
- Both independent (width 2). Limits 90 min / 60 turns each.

## Next Policymaker
- Read both reports. Check reviewer's actual model (if codex, no diversity — say so). If review says revise, order a
  benchmark fix of named findings only; if accept, record as review evidence for tasks/oracle (still not readiness).
- Check lineage exit codes, group/candidate counts, consistency with dev-case lineage ids; then order its review.
- Ready later preparation: challenge fixtures on dev cases (protocol `## challenges` table), baseline design,
  native-job input/output schema. Restricted-store proposal needs owner answers on store/custodian.
- Capability #169 (native jobs) and engine-change #165 remain waiting; do not duplicate or block on them.
- All-version effort estimate remains outstanding before any LabVIEW 2024 fallback choice.

## Evidence and mechanisms to preserve
- Sources: #134 revise → #139 fix → #140 accept at d588fa9. Coverage: #133 accept at 6933e17 as limited inventory.
- Input ceiling 800k: codex counts all non-cached input. Bounded orders (explicit "never print whole JSON", report
  early) worked in #175 (~300k). Keep that budget text in orders touching case/sources/coverage JSON.
- Task Verification runs in-session and offline; rebase runs evaluator --check. Changed pinned evidence requires
  preparation.json re-pinning. Parent commits accepted changes.
- Orders: `.github/loop/task-graph.md`; ids unique within an iteration. Requests: `.github/loop/session-protocol.md`.
  Export availability from `.session/exports/manifest.json`.
- `.session/history/sessions/<n>/` holds .md reports (not JSON); Glob on it returns whole-repo listings — use python glob.
- Read evaluation.md before reader planning/implementation; accepted-limits.md before private data, disclosure,
  publication or new spending. Optional access must not block ready work.
- Do not reinstate the crashed script shaper without contract review. Notices #92/#100/#158 approved.
