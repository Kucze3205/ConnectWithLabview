# Policy working memory

Considered: iteration records 0000–0009; reports #110/#112/#117/#123/#124; commits 0285248,
ef9db89 and 8156cad; evaluator check at 984a992. Updated by Policymaker #131, iteration 0010.
Historical inputs: `.session/history/manifest.json`; iteration 0009: `.session/history/records/0009.json`.

## Current organization and state
- `shaper: null`: always write `.session/orders.json`; it supplies the iteration's work.
- Routing remains benchmark Claude-first, reviewer/audit Codex-first. Actual iteration 0009 execution
  mostly fell back to Copilot gpt-5.6-luna. No measured subscription-quota comparison justifies a routing change.
- #122 coverage landed with owner acceptance #129; duplicate #125 was rejected through #128.
  Iteration 0009 was accepted/improved; `no_progress` reset to 0. Earlier stall concern is obsolete.
- At 984a992, `python3 -I policy/evaluator/evaluate.py --check` exited 0: errors [], 8 evidence refs;
  missing tasks, oracle, split, baseline, challenges. Sources and coverage remain prepared-not-reviewed.
  Benchmark readiness is false, benchmark has not executed, tool quality is unmeasured.
  Independent method review and owner acceptance remain required before product implementation.

## Iteration 0009 findings
- #123 stopped partial/input_budget. Its reusable result is ef9db89; parent 2e74e02 is on main.
  Two repositories have dependency objects. Changed files: sources.py, sources.json, sources.md,
  coverage.json. Contrary to its report, preparation.json was NOT updated: all four hashes would mismatch.
- ef9db89 incorrectly counts project virtual folders (`Dependencies`, `vi.lib`) as dependency identities;
  repeated items also need consolidation with source provenance preserved. Binary linkage/native checks remain unknown.
- #124 stopped partial/session_budget; report contains only an artifact reference, no recommendation.
  Artifact review-coverage.md (2777 bytes, sha256 6810a571202993e70416fa3ea07e8bde79058a812d6cae00109ad21b2faa0254)
  is not staged locally. Do not infer its findings. Commit 8156cad contains no tracked review output.
- Duplicate task issuance recurred in 0009 (#122–#124 and #125–#127); cause is unverified.

## Saved orders for iteration 0010
- `bench-sources-deps-land`: restore ef9db89's four files, exclude folder items, consolidate dependencies,
  regenerate sources then coverage, re-pin every changed evidence hash, quote actual check exit codes.
  Expected result: sources reviewable on main, evaluator errors [], explicit unknowns retained.
- `review-coverage2`: independent coverage review, recommendation tied to the inspected commit.
- `review-sources2`, blocked by dependency landing: sample at least five declarations against pinned sources,
  recheck prior passing source properties, recommend accept/revise/reject at the inspected commit.
- Both reviews write findings directly into `.session/report.md` from the start; budget exhaustion must
  leave readable findings. Coverage review may inspect the pre-dependency-change commit; check its pin later.
- Next Policymaker: run the evaluator check on main, read landing check outputs and both review reports;
  do not mark milestones reviewed or readiness established solely from hashes or engine acceptance.

## Mechanisms to preserve
- Input ceiling is 800k unique input; #123 consumed 419934 input plus 385555 cache-write tokens.
  Never read large sources.json/coverage.json directly; use bounded Python summaries and reuse saved work.
- Task Verification runs in-session and again without LABVIEW_ENVIRONMENT in the engine epilogue;
  keep it offline over committed files. Environment checks belong in Acceptance. Report-only reviews use no command.
- After rebase the engine runs evaluator --check; changed pinned files require preparation.json re-pinning.
- Missing git identity: leave changes staged; parent engine commits. Partial predecessors block dependants.
- Exports contract: `docs/perpetua/session-exports.md`; explicit records/reports/streams/actions selectors only.
  Current `.session/exports/manifest.json` has results []; it supplies no artifact or stream evidence.
  Avoid repeating unsuccessful Grep/Glob searches for #124's unavailable artifact.

## Open questions
- How a recommendation becomes milestone `reviewed` remains undecided; follow the existing owner change gate.
- Duplicate issuance and quota use warrant a targeted audit if recurrence threatens useful work; no cause inferred yet.
- Notices #92/#100 remain pending for the owner. Do not reinstate the crashed script shaper without contract review.
