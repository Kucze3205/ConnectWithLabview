# Setup notes

The standing rules of the setup map of this loop. Every session working the map reads this file first. Written by the Perpetua setup skill in Claude Code or Codex; topic H deletes it.

**What this map is.** Its main job is to prepare the environment: the loop can reach every source, piece of information and tool it needs. Its second job is to propose reformulations of the goal that make it easier for the loop to reach. Only the owner accepts a reformulation. Unlike plain wayfinding, this map carries execution: each topic writes its piece of configuration on the setup branch `perpetua/setup` when its ticket closes (the decision lives in the file, the ticket points at it). The map does no work toward the goal itself. The default branch is untouched until topic H.

**Branch.** Work on `perpetua/setup` (`git switch perpetua/setup`, `git pull`); commit and push when the ticket closes. Research and prototype findings go in the ticket's resolution comment: no branch, no file.

## Owner context and questions

- **Architecture:** Owner requires cloud-only execution (confirmed 18 October 2026). Do not register the owner's computer as a runner. Retain GitHub Actions and GitHub issue owner requests; the loop must support Claude, Codex and GitHub Copilot accounts. Product delivery form remains open; MCP is not a fixed requirement.
- **Requested engine changes:** The Policymaker must choose suitable models per task across all three providers and manage exhausted limits, checkpoints and resumption. The owner accepted the goal and steps in [Cloud model selection and quota management](https://github.com/Kucze3205/ConnectWithLabview/issues/11). The setup branch now contains provider adapters, policy routing, serialized renewal, shared availability, role-tool isolation and remote checkpoints. Positive Codex tasks, real Claude-limit fallback, interrupted Policymaker checkpoints and Copilot continuation on new runners have cloud evidence. On 18 October 2026 the owner accepted proceeding on the assumption that Claude works and explicitly removed its successful task test as a blocker for closing the integration topic. That task remains unverified because Sonnet, Opus and Haiku reported subscription exhaustion; runtime availability checks and fallback remain mandatory. Continue subsequent setup topics; AUTOPILOT remains off until the final arming decision. See [cloud authentication](cloud-authentication.md) and [environment readiness](environment.md).
- **Confirmed license, use and cloud baseline (18 October 2026):** The owner's expanded NI License Manager screenshot shows LabVIEW 2026 Q1 Community Edition Licensed until 27 June 2027. The owner confirmed a private, non-commercial project; do not ask those questions again. A digest-pinned official NI 2026 Q1 headless container passed hosted Ubuntu processing of an existing LV2014 VI with no desktop activation, NI login or outgoing container network. Use it for permitted analysis/build automation, not source authoring. This is an environment baseline, not proof of all-version compatibility, VI Scripting or native 2024 execution. See environment.md for evidence and the published license interpretation. Evaluation Available entries are not active licenses for the other editions.
- **Credential decision (18 October 2026):** The owner explicitly retained this public repository for GitHub Actions capabilities and rejected a private control repository. Keep all automation here; do not ask the visibility question again. OpenAI's managed account-auth CI guidance describes private automation, so its deployment recommendation does not cover the chosen layout. Preserve credential confidentiality with trusted workflows, isolated model processes, serialized refresh and a secret-manager round trip; verify these replacements. See [cloud authentication](cloud-authentication.md). No paid API or extra spending is authorized, and probe evidence alone does not complete the multi-provider task.
- **Other context:** The owner has intermediate LabVIEW knowledge. Explain consequential choices in plain Polish with concrete examples. Agents should decide implementation details independently. Establish a credible benchmark or another repeatable verification method before implementing the tool. The desired scope includes LabVIEW code, projects and all artifacts; any proposed narrowing or staged definition of success requires the owner's acceptance. Repository was empty: an empty initial commit established main before creating the setup branch.
- **Version compatibility (18 October 2026):** The owner prioritizes all LabVIEW versions. If investigation shows this takes substantially more time than supporting one version, LabVIEW 2024 is the accepted fallback (the owner explicitly corrected the typo "20214" to 2024). Present the estimated additional effort and compatibility limitations before choosing the fallback; no numeric time threshold was accepted. This condition concerns versions, not artifact families. Do not silently substitute the locally discovered LabVIEW 2026 or treat a single-version test as proof of universal compatibility.
- **Question preference:** key topics. Skip breadth-first grilling and detailed technical interviews. Reserve the most important decisions for the owner, especially meaningful scope/success changes, access to private resources, spending and accepted authority. The goal includes the owner's conditional version fallback above; no new numeric success threshold or budget has been accepted.
- **Starting evaluation (topic C):** Retain the shipped owner change gate until a trustworthy repeatable benchmark and an owner-accepted gate replacement exist. `policy/evaluator/` checks evidence integrity and reports both trees with quality unmeasured; it cannot accept a change or claim improvement. Missing benchmark evidence is explicit, not a passed product test. Follow [the evaluation contract](evaluation.md) before product implementation. The verifier skill, shared role prompt/protocol and the verifier's profile entry are owner-controlled to preserve independent review; other profiles remain policy-controlled.
- **Success framework (topic D, accepted 18 October 2026):** The owner accepted separate reading-fidelity and grounded-answer checks, independent expected answers, withheld evaluation cases and matched baselines, with explicit coverage and gaps across the full goal. See `goal/goal.md`. Numeric quality thresholds and an executable goal gate are deliberately deferred until a credible benchmark exists and the owner accepts them. A future gate must use `owner_confirms: true`; no command is accepted and `goal/gate.yml` remains absent. This does not establish benchmark readiness or authorize product implementation before the accepted verification prerequisites. Do not reopen the full-scope decision or interpret D's closure as acceptance of success thresholds.

These separate fields carry the owner's architecture choices or constraints, requested engine changes, other background and question preference through charting and every map continuation. Read them before choosing topics or asking questions. Explicit owner choices take precedence over Defaults; keep requests distinct from accepted decisions and implemented changes. Write only the accepted outcome to `goal/goal.md`.

- `none`: proceed from the supplied context and defaults, with no optional interview or breadth-first grilling.
- `key topics`: skip breadth-first grilling; discuss consequential or unclear topics, using grilling where it helps resolve them. This is the default when the owner supplied no preference.
- `all`: run breadth-first grilling and discuss every applicable topic in depth; use supplied answers rather than asking them again.

Every mode still requires a precise question when a necessary owner decision remains unresolved, including acceptance of a goal reformulation or a change outside existing authority. `none` reduces optional questions; it does not supply that decision. Update these fields and the map's Notes when the owner changes context or preference, and record resulting decisions in configuration and ticket resolutions. Continuations apply the latest recorded choices rather than resetting to Defaults. At topic H, preserve this context and the resulting decisions in `docs/perpetua/setup-decisions.md` before deleting these notes.

## Map rules

**Starting parameters (topic G, 18 October 2026):** The owner accepted a 24-hour
clock without a closed iteration, excluding cumulative blocking owner waits,
with policy rollback and retry; ten consecutive iterations without accepted
improvement produce a notice and independent work continues. Existing
subscription-only spending limits remain. See
[operating-parameters.md](operating-parameters.md) for session ceilings,
model availability, Policymaker triggers and the benchmark-before-product order.

**Accepted limits (topic F, 18 October 2026):** See [accepted-limits.md](accepted-limits.md).
The owner accepted technical autonomy within the existing tools, offline roles,
controlled source preparation and trusted native LabVIEW jobs. Private material,
provider disclosure, new publication categories and additional spending require
specific grants. Prefer granting concrete private access during setup; none has
yet been identified. Optional capability requests must leave independent work
and later iterations running; defer unavailable work instead of creating waiting
sessions. Existing goal, benchmark, verifier, public repository and owner gate
decisions remain. GitHub requests are frozen and only the owner may decide them.

**Starting roles (topic E, 18 October 2026):** `policy/profiles.yml` adds offline researcher,
benchmark, implementation and report-only reviewer roles using copied/adapted installed
skills. Existing orchestrator, audit, evaluator and protected evaluator verifier remain.
Read `docs/perpetua/roles.md` for responsibilities, staged tools, provenance and the route
from preparation through independent review and owner acceptance to product work. No new
access or limits are accepted here; withheld evaluation isolation and direct native LabVIEW
execution from roles are not claimed. Carry these facts into topics F/G and the final setup
decisions. Product implementation remains blocked on the evaluation contract's prerequisites.

**Client skill calls.** In Claude Code use the Skill tool. In Codex, where wayfinder or its dependencies say to call that tool, read and follow the named skill's `SKILL.md` with the same input in the current conversation. Resolve installed skills by their available paths and plugin-qualified names; filesystem-backed skills also work. Give research subagents the research skill path and the applicable map notes. Continue the map with `/wayfinder <URL>` in Claude Code or `$wayfinder <URL>` / `Use wayfinder for <URL>` in Codex. The setup client does not select the loop's provider; retain the Defaults unless the owner changes them.

**Tracker.** By default the tracker is GitHub issues of `Kucze3205/ConnectWithLabview`, driven with `gh`. The commands below describe that integration; if the owner changes the tracker or substrate, replace them with the implemented equivalents before using them. Do not run `/setup-matt-pocock-skills`.
- map: the issue labelled `wayfinder:map`; ticket: an issue labelled `wayfinder:<type>`
- child ticket: `gh api repos/Kucze3205/ConnectWithLabview/issues/<map>/sub_issues -F sub_issue_id=<id>`, where `<id>` is the ticket's database id (`gh api repos/Kucze3205/ConnectWithLabview/issues/<n> --jq .id`), not its number
- blocking: `gh api repos/Kucze3205/ConnectWithLabview/issues/<blocked>/dependencies/blocked_by -F issue_id=<id>` with the blocker's database id
- claim: assign `@me`; frontier: open, unassigned child issues with no open blocker

**Glossary.** One glossary: `CONTEXT.md` at the repo root. Add terms of the goal's domain there. When an owner decision changes a Perpetua concept, update its definition and its uses in the setup, configuration and engine documentation together; keep owner, policy (rules and artifacts), Policymaker (the agent), engine, goal gate and owner request distinct.

**Topics.** The goal was settled when the map was charted (`goal/goal.md`). Every topic below has a ticket. For each, investigate what the goal and this repo need, using the owner context and question mode above to guide discussion and grilling. A topic that does not apply to this goal is recorded as "not applicable" with the reason, never skipped silently. The Policymaker maintains the evaluator, roles and parameters in separate triggered sessions beside iterations, so this map sets their **starting state**. Adapt the topics and dependencies to the architecture the owner chooses. Every key and file is described in `docs/perpetua/engine.md`.

| # | Topic | Content |
|---|---|---|
| B | Environment | Sources, information and tools; access from the chosen substrate; provider, credential handling and readiness checks; tools' secrets and machine preparation (by default repository secrets and `.github/loop/prepare.sh`). Implement any changed provider or substrate integration. |
| C | Starting evaluator and change gate | A script (it may call a model with a rubric), or "owner only"; the check command; protected paths. |
| D | Goal reformulation and goal gate | Proposed reformulations (realistic only after B and C); whether a goal gate exists and the `owner_confirms` field. |
| E | Starting roles | Propose existing skills first (plugins, personal, project); a role built on one gets a copy of it in `policy/roles/<role>/`, since only that folder reaches the runner. Write a new skill only when nothing fits. |
| F | Accepted limits and owner interaction | The boundary within which the Policymaker may widen roles and profiles on its own (`limits` in `engine.yml`); the owner-request channel and its acceptance, refusal and wake-up semantics. Implement any changed channel and its authority checks. |
| G | Starting parameters | The watchdog's "time without an iteration" and whether time spent waiting for the owner counts toward it; ceilings and models; the shaper's starting instructions and Policymaker triggers in `policy/params.yml`. |
| H | Arming | A `task` ticket, last. Preserve owner decisions, specific lost guarantees and replacement checks in `docs/perpetua/setup-decisions.md`, with links to the implementing files, then delete `docs/perpetua/setup-notes.md`. By default merge `perpetua/setup` into the default branch, tag the merge commit `setup-baseline`, switch on `AUTOPILOT`, then `gh workflow run watchdog.yml` to start iteration 0 now. For a changed substrate, use the implemented equivalents for accepting the setup, recording the baseline, enabling the owner's switch and starting work; verify its credentials and controls before enabling it. No trial run: the first iteration is the trial. |

Dependencies: B → C → D; E needs B and C; F needs B and E; G needs C, E and F; H needs all.

**Defaults.** These are the shipped starting choices, all open to change by the owner during setup. With no owner change, retain the existing behavior. The charting session establishes which defaults hold; later topics may revise them with the owner.

| Topic | Default |
|---|---|
| G: cadence, criterion | cadence "iteration after iteration"; design criterion "shortest wall-clock time to the goal" |
| Orchestrator | the generic LLM role from the engine; the owner may choose a different starting shaper during setup, and the Policymaker may later choose an orchestrator or rule within its authority |
| F | the engine's limits (`limits` in `engine.yml`) |
| E | existing skills first, a new skill only when nothing fits |
| C | the Policymaker owns the evaluator; it changes only through the evaluator verifier |
| D | **none** for the goal gate; without an accepted gate the loop never declares its own end |
| G: watchdog | **none** for "time without an iteration" and for the waiting-time question; they follow from the goal |

**Architecture decisions.** The shipped defaults are GitHub Actions, a Claude subscription, and GitHub issue owner requests. The engine is a copy owned by this repo; the owner may change any starting architecture choice during setup. Record the decision in this file while the map is active and in the implementing configuration, code and `docs/perpetua/engine.md`. For each change, name the specific guarantee lost and any replacement, rather than a generic warning. For example:

- A different provider removes the shipped Claude credential probe and subscription-limit parking/reset guarantees until equivalent behavior is implemented and checked.
- A different owner-request channel removes the issue-close acceptance/refusal, frozen-payload checks and close-event/watchdog wake-ups unless replacements implement them.
- A different execution substrate removes reliance on GitHub Actions workflow permissions, runner isolation and watchdog scheduling; identify which controls the replacement supplies.

These consequences inform the owner's choice; they do not automatically block it. The setup now adds routed Claude/Codex/Copilot execution to the shipped engine. Choosing another substrate or channel still means changing and checking the relevant engine integration, topic instructions, tools and arming procedure. An unimplemented integration is unfinished setup, not a reason to reject the choice.

**Authority after arming.** The owner's power to change setup does not pass to the Policymaker. Under the shipped boundaries only the owner accepts a goal gate or changes the engine, accepted limits and `AUTOPILOT`; the Policymaker changes only its permitted artifacts and proposes other changes through owner requests. A setup decision changes those boundaries only when the owner explicitly chooses it and the map implements and documents it. See `docs/perpetua/engine.md`, "Who may change what".

**Where things are.** Glossary: `CONTEXT.md`. Engine documentation: `docs/perpetua/engine.md`. Engine version: `0.2.0`, stamped in `ENGINE_VERSION`. For provider integration points see `docs/perpetua/engine.md`, "Sessions".

**Language.** These notes stay in English. Write tickets, comments and the conversation in the language the owner used to state the goal.
