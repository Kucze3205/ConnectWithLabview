# Starting roles

Topic E configures the loop's starting capabilities. It creates no reader, benchmark cases,
quality thresholds or new access. The role label selects `<layer>/roles/<name>/SKILL.md`
and the matching entry in that layer's `profiles.yml` (see [managed definitions](managed-resources.md)).
The Policymaker may adapt ordinary roles within the owner's limits; the evaluator verifier's
contract remains owner-controlled. Layer assignment (M2/M3, 20 October 2026): execution roles do
not see the inside of policy, so the reviewer judges the work from pinned evidence without it.

## Responsibilities and separation

| Role | Layer | Responsibility | Repository output |
|---|---|---|---|
| orchestrator (shaper) | execution | Shape one iteration and its dependencies; preserve context | `journal/` |
| researcher | execution | Investigate prepared primary sources, LabVIEW compatibility and delivery options | `docs/research/` |
| benchmark | execution | Prepare verification protocol, development cases and reproducible readiness evidence | `benchmark/` |
| implementation | execution | Implement assigned product behavior after benchmark prerequisites | Product paths declared in its profile |
| reviewer | execution | Independently inspect a pinned product or preparation change against Standards and Spec | Session report/artifacts only |
| evaluator | policy | Implement the measurement under the Policymaker's order | `policy/evaluator/` only |
| evaluator-verifier | policy | Independently check an evaluator change, including transition to real measurement | Session report/artifacts only |
| audit | policy | Measure use of the loop's environment, not product quality | `audit/` |

The Policymaker is a separate engine-selected agent in the policy layer (its skill is `policy/roles/policymaker/SKILL.md`, its permissions come from `engine.yml`), not a task profile.
Keep its existing evaluator and audit orders. The orchestrator can order researcher,
benchmark, implementation and reviewer work, but cannot order evaluator changes.

Independent review means another session with the original evidence and pinned input
trees; different provider/model names alone do not establish independence. A reviewer
reports findings and never edits the work being reviewed. The engine starts the protected
evaluator verifier after evaluator changes and pins approval to the evaluator tree.
Ordinary reviewer recommendations do not bypass the owner change gate.

## Work sequence

1. Research concrete uncertainties using existing source material. Let agents compare
   technical delivery options, including MCP, against the goal rather than choosing a
   delivery form for the owner to organize.
2. Prepare the repeatable verification method and development evidence with the benchmark
   role, following [the evaluation contract](evaluation.md). The first examples are a
   starting corpus, not a scope reduction. Public examples cannot be claimed as private
   or unseen by a model.
3. Give the reviewer a pinned preparation tree, protocol and original-source evidence.
   If executable measurement changes are needed, suggest them to the Policymaker for an
   evaluator order; the engine then requires the separate evaluator verifier's pass.
4. Obtain owner acceptance of the independently checked method and evidence through the
   existing change gate before issuing product implementation. Put links and exact tree
   identities in the implementation task's context. Missing benchmark prerequisites stay
   explicit; role availability does not establish readiness.
5. Implement and independently review product changes against the accepted method. Keep
   evaluation changes in their own sessions. Acceptance thresholds and a goal gate still
   require the owner's separate decision.

Task dependencies sequence sessions. Authoring and reviewing may occur in later iterations
when that gives the reviewer a clearer accepted snapshot. For unmerged input, pass the
candidate branch/tree through the engine's `start_branch` and staged artifacts; list the
baseline SHA, candidate SHA and specification in the task. Report missing input as blocked.
The engine's current owner gate still decides merges; this document does not install an
automatic product-review merge gate.

## Available tools and limits

The four goal-work profiles (researcher, benchmark, implementation, reviewer) are offline. They use the broker's Read/Glob/Grep/Write/Edit tools
and allowlisted git/Python commands. The engine separately permits session reports and
artifacts, so `reviewer.write: []` allows a report while preventing repository edits.
Profiles define filesystem writes, not data confidentiality: readable repository content
is not hidden from implementation sessions.

The existing preparation step pins public pylavi and NI Actor Framework sources. In
routed sessions the broker exposes their read-only cache as `@environment/` to text tools;
commands see `LABVIEW_ENVIRONMENT=/resources/environment`. Begin with `readiness.json`.
Python can inspect binaries, XML and prepared parser sources without downloads. Reuse
only packages actually present; request unavailable dependencies rather than assuming them.

The established NI headless workflow proves a bounded cloud automation path, not access
from role commands. No role receives Docker, the host daemon, desktop automation, model
credentials, GitHub credentials, MCP, subagents or a paid API. A native experiment needs
staged trusted results or an approved capability/engine change with a readiness check.
Likewise, additional web material needs a prepared source or explicitly accepted access;
changing `internet` alone does not add a web tool to the routed broker.

Withheld evaluation cases and answer keys cannot be secured by a folder in this public
repository or its history. Preparation may specify their separation but must request and
verify the needed restricted storage/execution before claiming a withheld evaluation.
The evaluator-only write permission does not itself hide evaluator files from product roles.

The new profiles stay within existing `engine.yml` limits. Missing capabilities use the
engine's owner-request protocol; ordinary role/profile adjustments go to the Policymaker.
No broadening of accepted limits is made here. Topic F decides those boundaries; topic G
decides remaining operating parameters. Existing model routing classes are reused for the
new role names, preserving all three provider candidates and quota fallback.

## Skill reuse

Inventory on 18 October 2026 covered project roles, personal skills under `~/.agents/skills`
and `~/.claude/skills`, and the installed Matt Pocock plugin 1.2.3. Personal research,
implement and code-review workflows provide suitable bases; the plugin equivalents add
no needed capability. Existing project orchestrator, audit, evaluator and evaluator-verifier
skills are retained. Sources and hashes below identify the installed inputs; they are
provenance, not runtime dependencies.

- `researcher/SKILL.md` copies the primary-source investigation and cited Markdown method
  from `research/SKILL.md`; engine task sessions replace its nested background agent.
- `implementation/SKILL.md` adapts `implement/SKILL.md` and `tdd/SKILL.md`: specification,
  focused checks, behavioral vertical slices and review. `tests.md` and `mocking.md` are
  bundled copies from `tdd/`. Staged tasks replace interactive test-seam interviews and
  external skill calls; an independent reviewer replaces nested code-review agents.
- `reviewer/SKILL.md` adapts `code-review/SKILL.md`: pinned comparison and separate Standards
  and Spec assessments. Staged inputs replace tracker fetching; the two assessments run
  inside one independent session without nested agents.
- No installed skill directly prepares a LabVIEW benchmark. `benchmark/SKILL.md` adapts
  actual-output inspection, evidence per assertion, implicit-claim verification and weak
  assertion critique from `skill-creator/agents/grader.md`, combined with the project's
  accepted evaluation contract. It does not reuse that grader's output schema or declare
  numeric scoring rules. Benchmark authors do not approve their own readiness.

Each role is a complete local copy under its layer; only the selected role folder and referenced repository/staged inputs are required on
the runner; personal paths, connector accounts and native skill discovery are unnecessary.

Installed inputs (SHA-256 of the original bytes):

| Source under `~/.agents/skills/` | SHA-256 |
|---|---|
| `research/SKILL.md` | `524b404b1ca373a8b00f63a64667ec4b0a61c3c9cf4e8f246e639be859bb6979` |
| `implement/SKILL.md` | `30cd7bc1ebfb3891e85a1eed3b3b81aea0fa4ad4553a784de7f8e421b2d223e0` |
| `code-review/SKILL.md` | `3abbdfe52540f9242e16589fae2cc423b3d98994c37683944462b29bab89495c` |
| `tdd/SKILL.md` | `193b791c489d1640ccfb58d7cbd60fc9e059ef44632b3c92f208784cfe45ab78` |
| `tdd/tests.md` | `0b401f98bd3684d2fea6440d6946afcf8f5f68ac6a65599dd7a2b90dd9f02eb5` |
| `tdd/mocking.md` | `73a10b6a26b56197c738a764c1e4205af98c74553f4a713795997f6bc35b917d` |
| `skill-creator/agents/grader.md` | `57134da0c1a4eea33fbd74a1c9c44aa814f07d6bc64de303edb586f941e5d21a` |
