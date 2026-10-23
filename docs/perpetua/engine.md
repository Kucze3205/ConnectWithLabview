# The Perpetua engine

The goal-independent machinery of this loop: workflows, scripts, protected configuration and session contracts. It was copied into this repository by `/perpetua:setup` and belongs to this loop; the setup map may
change it. Terms (loop, owner, iteration, policy, policymaker, evaluator...) are in `CONTEXT.md`.

**Managed definitions** span `execution/` (shaper and work roles) and `policy/` (Policymaker, audit,
evaluator maintenance, verifier, parameters and measurement). Inactive candidates live under protected `templates/`. The **Policymaker** is the agent in the policy layer that creates
and maintains that policy and manages the loop's architecture. The implementation layer applies it to shape,
execute and evaluate work toward the goal. The engine enforces their contracts and the owner's authority.

GitHub Actions, the Claude subscription and GitHub issue owner requests are the shipped architecture defaults. The
owner may replace them during setup; this requires implementing and checking the affected integration, tools and
arming procedure, not selecting a generic backend. Record each decision and the specific guarantee it removes or
replaces in the setup notes and implementing files; preserve that account in `docs/perpetua/setup-decisions.md` before
arming deletes the notes. Losing a guarantee informs the owner's decision and does not automatically veto it. With
no owner change, the shipped behavior remains in force.

Engine version: `ENGINE_VERSION` (`0.3.0`, the engine of plugin 0.4.0, extended here with routed Claude/Codex/Copilot execution). The plugin ships no update path for installed loops; this loop was moved by a manual three-way merge (setup tickets M1-M4) and any later update needs the same care.

When investigating behavior or proposing an engine change, use the [code map](code-map.md)
to find the responsible module, contract and tests.

The agent uses `role:policymaker`, the owner-controlled `policymaker` profile in `engine.yml`,
`policymaker_session_ceilings`, and the editable `policymaker_session` and `policymaker_triggers` parameters.
Its contract is `.github/loop/policymaker.md`; its editable starting prompt is `policy/prompts/policymaker.md`,
staged as `.session/policymaker.md`. `policymaker_only_roles` identifies roles only this agent may order.
Managed definitions span both roots; `policy_rev` and iteration records' `policy` section
refer to their shared revision. `policy_params` holds the common parameters, and
`policymaker_sessions` refers to the agent's session history.

A fresh template has no active roles or shaper. Setup selects complete local skills and
profiles from inactive candidates or project/global/plugin sources, validates the
accepted setup baseline and leaves arming to the owner. This release does not migrate,
update or arm an existing loop. Repeating setup as a review is separate work.

## One iteration

Iterations run one after another. An iteration is an issue labelled `loop:map` + `loop:iteration N`; everything it
does is an issue labelled `loop:iteration N` + `role:<name>`.

```
Policymaker session ──► shaper session ──► task graph ──► task sessions (parallel) ──► record
 (when a trigger is due;    (optional: an      issues and       rebase, check, gate,      iterations/NNNN.json
  always in the first)       orchestrator      blocking edges   merge
                             or a script)

Policymaker orders ──► tasks of the same iteration (the only tasks when `shaper: null`)
```

1. **Start.** The watchdog (or the end of the previous iteration) starts iteration N when none is open, if the
   cadence allows. The triggers of the policy layer are checked now, at the start, never after the previous close.
2. **Policymaker.** When a trigger is due the iteration begins with a `role:policymaker` session and waits for it: the first
   iteration of the loop always (it sets up the execution layer's organization, so it is the larger piece of work), later
   ones on `every_iterations`, `no_progress`, a new audit report or new suggestions. It may change `execution/` and
   `policy/` and write `.session/orders.json`. When it ends, its changes merge and its orders become tasks of this same
   iteration; the iteration record keeps the policy revision before and after, the session and its trigger. A failed
   Policymaker session fails open: the iteration runs on the last organization (`policy/` as it stood); two failed sessions
   in a row roll both managed roots back. With no trigger due the iteration starts at once on the last organization. The
   engine then snapshots the state (`.session/loop-state.json`: goal, parameters, limits, open owner requests, an index line
   per past iteration, `no_progress`) into a comment of the iteration issue.
3. **Shaper (optional).** The role named by `shaper` in `policy/params.yml` (`null`: none; the tasks are then only the
   Policymaker's orders, of any role, and an iteration without a shaper and without valid orders ends `failed` with that reason)
   turns the goal and state into `.session/tasks.json`: an LLM
   orchestrator, or a script role (a deterministic rule: a profile with `agent: false` and a `command`). It has no
   GitHub token; the inactive orchestrator candidate has no shell, while a script shaper executes its configured command.
   The engine validates the graph and creates the issues, blocking edges and consent requests.
   The Policymaker's accepted orders start beside it (the only way to the roles in `policymaker_only_roles`).
   The width of the iteration is the widest layer of the graph, computed, not configured.
4. **Tasks.** Each free task is a `session.yml` run (parallel jobs). When a task closes, what it blocked starts. A
   producer that did not deliver closes its consumers as `blocked`.
5. **Close.** When no session of the iteration is open the engine writes `iterations/NNNN.json` (only the engine writes
   it), closes the iteration, prunes old session streams, raises a notice if there was no progress for too long,
   checks the goal gate, and starts the next iteration.

## Who may change what

These are the shipped boundaries after arming. The owner's ability to change architecture during setup gives the
Policymaker no additional authority. Any owner-chosen change to these boundaries must be explicit, implemented and
documented during setup; otherwise they remain in force.

| Zone | Contents | Changed by |
|---|---|---|
| Workflows | `.github/workflows/` | the owner only (the loop's token cannot write them) |
| Engine scripts and config | `.github/loop/`, `engine.yml`, `ENGINE_VERSION` | the owner only (the loop may ask through a `question` request); sessions cannot write them (`protected`) |
| Managed definitions | `execution/`, `policy/` | the Policymaker, with evaluator changes delegated as below; merged without the change gate, still within the role's `write` paths |
| Audit and journal | `audit/`, `journal/` | the audit role (`audit/`), the orchestrator (`journal/`); merged without the change gate, still within each role's `write` paths |
| Evaluator | `policy/evaluator/` | only a role whose profile has `owns_evaluator`, ordered only by the Policymaker, and only after the evaluator verifier passes |
| Records and goal | `iterations/`, `goal/`, `GOAL_REACHED` | the engine only, except goal files the setup map writes before arming; the owner accepts what goes into `goal/` |
| Work | everything else | task sessions, through the change gate |

The Policymaker never touches the engine, the goal gate, `AUTOPILOT` or a token. `AUTOPILOT` (repository variable) is the
owner's switch; it is the first condition of every workflow and anything but a literal `on` means stop.

## Sessions

**This setup's required architecture:** all loop sessions execute in the cloud. The owner requires Claude, Codex
and GitHub Copilot with model selection by policy and continuation across provider limits. The session path described
below is still the shipped Claude adapter, not the completed multi-provider integration. That integration is tracked in
[Cloud model selection and quota management](https://github.com/Kucze3205/ConnectWithLabview/issues/11).
`provider_pool.py` implements tested selection rules, but adapters, shared availability state, checkpoint continuation
and watchdog integration remain to be implemented. `environment.yml` checks public sources and actual model responses
without arming the loop; it does not run iteration work. See [environment readiness](environment.md) for credentials,
observed limitations and the separate requirement for LabVIEW in the cloud.

A session is one `session.yml` run: `prep` (guard, credential probe, `resolve`) then `session`: two checkouts (the engine
from the default branch, the agent's own working copy), machine preparation (`.github/loop/prepare.sh`, filled in by the
setup), `stage`, the agent, the epilogue.

- **The agent has no GitHub token, no `gh`, no push rights.** Its Claude credential lives only in the `claude`
  process. The engine checkout is removed from the disk while it works. The epilogue re-checks the engine out and fetches
  the agent's commits as plain objects into the trusted checkout; the agent's repository is never used to run git.
- **Input and output are files** in `.session/`: `issue.md` (the issue and trusted comments), `protocol.md`,
  `loop-state.json` (Policymaker, shaper), `inputs/`, `streams/` (audit); `report.md`, `tasks.json`, `orders.json`, `requests.json`,
  `artifacts/` go out. See `.github/loop/session-protocol.md`, the contract every role reads.
- **Kinds.** `agent` (a Claude session, pinned CLI) and `script` (a role with `agent: false`: no model, no credential).
- **Model credential.** By default the engine is wired for a Claude subscription: the repository secret `CLAUDE_CODE_OAUTH_TOKEN`
  (`claude setup-token`), the watchdog's probe and the parking on a subscription limit. Another model provider means
  changing `session.yml`, `watchdog.yml`, `agent.sh`, the probe in `common.py` and `stream_filter.py`; the setup map may
  do it for this loop. Changing provider removes the shipped credential-probe and subscription-limit parking/reset
  guarantees until equivalents have been implemented and checked; document the specific consequences the owner accepts.
- **Limits.** Per-task limits never exceed the ceilings in `policy/params.yml`; the engine enforces time (`timeout`) and
  turns (`--max-turns`) hard. Policymaker session tuning lives in `policymaker_session` in that file and additionally respects
  the owner's `policymaker_session_ceilings` in `engine.yml`; tools and engine safeguards remain owner configuration.
  Tokens are recorded, not budgeted; there is no money limit anywhere in the engine.
- **Statuses.** Agent: `wip`, `done`, `partial`, `blocked`, `rejected`. Engine: `paused` (subscription limit; it
  resumes at the reset time, `resume.yml` keeps the clock), `crashed`. A task can also wait: `awaiting:owner` (the
  change gate is the owner) or `awaiting:verifier` (an evaluator change).
- **Report.** One marked comment with a YAML block. Fields the engine owns (tokens, verdict, merged, times...) cannot be
  forged by the agent. `status`, `commit`, `result` are the agent's.
- **Large outputs** (> `large_file_bytes`, binaries) go in `.session/artifacts/`; the epilogue uploads them as assets of
  the release `iter-NNNN` and lists them in the report. A later task names them in `inputs` and the engine downloads
  them before the agent starts.
- **Streams.** The raw `stream-json` of every session is kept as the artifact `stream-NNNN-<issue>` (for
  `stream_retention_iterations` iterations when set). Nothing interprets it. Declarative `exports` select supported
  data for any role; an audit with no selectors retains the current iteration and three predecessors in
  `.session/streams/`. See [session data exports](session-exports.md) for the catalogue, scopes, manifest and Policymaker
  session tuning contract.

See [session instructions and network access](session-contract.md) for the contract's precedence, editable policy
rules and starting prompts, and enforcement of `internet: false` for tools and script roles.

## The change gate

For this loop's starting role selection, source provenance, prepared tools and the
benchmark-before-product sequence, see [starting roles](roles.md). Profiles and bundled
role folders supply the capabilities; they do not change the owner gate or accepted limits.

Work enters the default branch after a verdict "not worse than what is accepted". After a task ends `done` the
epilogue, in a throwaway worktree: checks the paths (protected, role `write`, file size), rebases on the default branch,
runs `## Verification` and `check`, then asks the gate. Managed definitions and paths in `direct_paths` (`execution/`, `policy/`, `audit/`, `journal/`) are not
work and skip the check and the gate. A rejected push is retried from the new tip, up to three times.

`gate.kind` in `engine.yml`:

- `owner`: the engine opens a `merge-acceptance` request and the task waits (`awaiting:owner`). Completed merges, not
  planned discards (the branch is kept and tagged `iter/NNNN/<issue>`). This is the default until the setup decides.
- `script`: `gate.command` runs from the **accepted tree** (the default branch checkout), never from the candidate, with
  `CANDIDATE_DIR`, `BASELINE_DIR`, `CANDIDATE_SHA`, `BASELINE_SHA`, `CHANGED_FILES_FILE`, `TASK`, `ITERATION`, and no
  secrets except the names in `gate.env_passthrough`. It prints a JSON object as its last line:
  `{"verdict": "accepted|rejected|inconclusive", "improved": true, "detail": "..."}`. No verdict is `inconclusive`, never a
  yes. The engine stores no accepted result: the evaluator compares the candidate with `BASELINE_DIR` itself (and may cache
  its baseline measurement by `BASELINE_SHA`). A judge that calls a model is just a gate command.

`improved` (default: `verdict == accepted`) feeds `no_progress`: the number of trailing iterations without an improving
accepted change.

**Evaluator changes.** A merge that touches `evaluator_paths` does not merge: the engine opens a session of
`verifier_role` (default `evaluator-verifier`, starting from the branch) and merges only if its report says
`result: pass`; until then the old evaluator is the one in force (it lives on the default branch). A failed check goes
back as a rejected task, visible to the Policymaker.

This loop starts with an owner change gate and an evidence-integrity `check`, not a LabVIEW quality score.
See [starting evaluation](evaluation.md) before preparing or reviewing benchmark work. The verifier's skill,
shared role prompt and protocol are protected; `merge_branch` also refuses any change/removal of the
configured verifier's entry in `policy/profiles.yml`. Other profiles remain policy-controlled. Only the owner
may change that reviewer contract; evaluator ownership and pinned independent verification remain in force.

## The goal gate and the end

`goal/goal.md` (the accepted goal text) and `goal/gate.yml` (`command`, `owner_confirms`) exist only when the owner has
accepted them, in the setup or later through an owner request. After every closed iteration, if a gate command exists
and prints `{"reached": true, ...}`: with `owner_confirms` the engine asks the owner to confirm (a `result-confirmation`
request; completed writes `GOAL_REACHED`, not planned lets the loop continue and is not asked again for the same state);
without it the engine writes `GOAL_REACHED` itself. **Without an accepted gate the loop never ends by itself**; only
switching `AUTOPILOT` off stops it.

For this loop the owner accepted the success framework in `goal/goal.md` on 18 October 2026,
while deferring numeric quality thresholds and an executable gate until a credible benchmark
and a separate owner decision. `goal/gate.yml` is intentionally absent. A future accepted
gate must set `owner_confirms: true`; this standing choice does not itself install a command
or enable automatic completion. See [the evaluation contract](evaluation.md).

## Owner requests

Setup topic F's accepted resource, private-data, publication and cost boundaries
are in [accepted limits](accepted-limits.md). `limits.internet: false` requires
owner consent for an online role even when its write list is empty; it does not
disable the trusted model transports. All owner requests have a trusted body
snapshot and verify the closing owner's login. Consent additionally pins the
task identity and profile. Pre-snapshot requests cannot grant authority; replace
them with a newly frozen request.

Optional private-access capability proposals create no iteration/task blocker.
Continue ready work and schedule resource-dependent work after the grant and
readiness check, in a later iteration. A pending request does not pause the loop.

This is the shipped GitHub issue channel. The owner may replace it during setup by implementing its transport,
authority checks and wake-ups. Record which frozen-payload, acceptance/refusal and event-recovery guarantees are
replaced or lost, and update setup topics and arming tools to match. The Policymaker cannot change this channel itself.

The only way the loop asks the owner for a decision, a consent or a confirmation. An issue assigned to the owner (with an
@mention); the answer is closing it: **completed = yes, not planned = no**, with a comment. Only engine scripts create
them. What the owner accepts is the text frozen when the request was opened (a hash in the issue); a change is a new
request. Kinds: `consent`, `merge-acceptance`, `goal-gate`, `goal-change`, `result-confirmation`, `question`, `notice`,
`capability`, `limits-change`, `engine-change`. Sessions propose requests in `.session/requests.json`; the session
protocol defines their fields and the kinds each role may propose.

`capability` asks the owner to supply access, a tool or a named secret and confirm readiness; closing it alone does
not create or verify a secret. `limits-change` automatically replaces only the frozen `limits` block after the owner
accepts it, provided the proposal and its base configuration still match. `engine-change` records a concrete proposal
and base; when the owner closes it as completed, trusted engine code applies the frozen diff to the current `main` and opens
a PR from `engine-change/<proposal_sha12>` (needs "Allow GitHub Actions to create pull requests"). Merging the PR approves,
closing it unmerged declines (the watchdog notices). A diff touching `.github/workflows/**`, or one that does not apply
cleanly, gets no PR: the owner applies it manually and posts `engine-applied`. These requests
keep trusted snapshots and durable decisions so repeated events cannot reapply a proposal.

Closing a request wakes the loop (`owner-request.yml`); the watchdog sweeps requests whose event was lost.

**Consent.** A task whose role's profile is beyond the accepted limits (`limits` in `engine.yml`: tools outside the list,
internet with writes outside `internet_write`) gets a `consent` request that blocks it with a native edge. `resolve`
starts the session only when that request is closed as completed, and then only that one session runs with the profile.
The task can also carry `consent.secrets` (names only); the frozen text of its granted consent decides which pool
secrets of the `Session` step of `session.yml` that one session gets, and a missing one blocks the task with
`secret-missing:NAME` (see [session secrets](session-contract.md#session-secrets)). There is no other path for a secret
to reach an agent; `gate.env_passthrough` is the owner's separate list for the gate command.

## The watchdog

A plain script (`watchdog.yml`, every 30 minutes and on demand), never an agent:

- starts the first iteration after arming, and the next one when a run's end event was lost;
- guards: `AUTOPILOT`, `GOAL_REACHED`, an open `outage` issue (the only quiet state without runs);
- probes the Claude credential: dead or revoked is an outage and a red run (the e-mail to the author of the workflow file is
  the free push channel);
- `idle_resumes` (`engine.yml`, default 3) is the progress breaker: that many consecutive resumes of one parked session
  that used the agent (`agent_s` or tokens) and made no progress (no turns, no new commit) open an outage and the session is not
  resumed again. A routed session reports turns and tokens for its whole life, so for it the breaker counts the growth since the
  previous report, not the totals. Waiting for a limit reset without using the agent does not count; parking does not use up resumes, only the
  breaker and the 30-day age limit end a wait. A parked session commits nothing: reports freeze only in a final state.
- three consecutive `crashed` sessions without a commit is an outage; three fruitless kicks of one issue too; three failed
  iterations in a row too;
- resumes parked sessions that are due; relaunches ready sessions nobody started (kicking before calling);
- `ceilings.iteration_minutes` (the Policymaker's own): fails an iteration that runs past it;
- `params.quiet_minutes` (the setup's): an iteration that does not close in time fails, both managed roots are rolled back to the
  state in which the last iteration closed (at the start: the `setup-baseline` tag), and a `notice` is opened for the owner.
  Time spent waiting for the owner counts only when `params.owner_wait_counts` is true.
  Excluded waits come from frozen blocking consent/merge requests for the active iteration;
  their intervals are combined so simultaneous waits count once, and completed waits remain
  excluded after a restart. Optional capability requests and unrelated issue labels do not pause this clock.
  The policy iteration ceiling also excludes these waits. Provider quota parking is not an owner wait.

This loop's owner-accepted starting thresholds, resource limits and preparation order are
documented in [operating parameters](operating-parameters.md). The no-progress notice
informs the owner without stopping independent work; it measures accepted improvements,
separately from the quiet clock's lack of a closed iteration.

## The iteration record

`iterations/NNNN.json`, written once by the engine, never edited: `schema_version`, `iteration`, `status`
(`closed`/`failed`; the last good state is the last `closed`), `started`, `ended`, `engine_version`, `input_state` (the
snapshot at iteration start, without the index), `policy` (`rev_start`, `rev_end`, `commit_end`, refused orders),
`decided_by` (the shaper role), `tasks` (the frozen graph), `outcome` (sessions with status,
verdict, tokens in/out/cache and by model, turns, agent/gate/total/parked seconds, runner, branch, commit, stream name;
the shaper; the iteration verdict; token sums; wall time; critical path; width; owner requests opened and open at close).
The offline module (not shipped) replays decisions from `input_state` plus the index.

[Change provenance](policy-changes.md) records accepted policy/evaluator changes and verifier outcomes separately,
without modifying closed records. [Reports and suggestions](session-reports.md) describes frozen source evidence,
staged report bodies and the separate suggestion lifecycle.

## Setup outcomes and where they write

Setup clarifies the goal first, then analyses an initial approach, then prepares the environment from that
analysis. The approach is a revisable plan; the loop can adapt it as it learns. Success criteria and evidence
must be verifiable; numerical metrics are optional. Goal criteria do not themselves enable a goal gate.
The rows describe required outcomes, not one issue each. Wayfinder chooses and revises ticket boundaries,
types and dependencies; arming is a separate final ticket after coverage is verified and no in-scope fog remains.

| Outcome | Writes |
|---|---|
| charting (no ticket) | `goal/goal.md`: clear outcome, scope, success criteria and evidence, accepted by the owner |
| Initial approach | `docs/perpetua/approach.md`: steps, dependencies, unknowns, verification needs and the sources, information, tools and access each step requires |
| Environment (derived from the approach) | `.github/loop/prepare.sh`; `engine.yml`: `cli_version`, `owner`, `author`; repository secrets and settings; requirement coverage in `docs/perpetua/approach.md` |
| Evaluator, change gate and goal gate | `engine.yml`: `check`, `gate`, `protected`, `evaluator_paths`; `policy/evaluator/`; owner-accepted `goal/gate.yml` (`command`, `owner_confirms`) |
| Starting roles | selected `execution/roles/<role>/SKILL.md` or `policy/roles/<role>/SKILL.md`, with profiles in that layer; inactive sources under `templates/` |
| Accepted limits | `engine.yml`: `limits`; consent secrets in `session.yml` |
| Parameters | `engine.yml`: `params`, `cadence`; `policy/params.yml`: `criterion`, `ceilings`, `models`, `policymaker_triggers` |
| Arming | delete `docs/perpetua/setup-notes.md`, merge the setup branch into the default branch, tag `setup-baseline`, pass `test_routed_chain.py` on that commit ([validation](validation.md)), set `AUTOPILOT=on`, then run `gh workflow run watchdog.yml` — GitHub's schedule can take 3–6 h to start it. Done by the agent or by the owner, depending on the preflight check of arming permissions |

## Changing the engine after arming

`validate --baseline <tag>` compares the revision of the managed definitions (`execution/`, `policy/`, evaluator paths) at `HEAD` with the one in the tag's commit, and `engine.yml`, `goal/` and `templates/` file by file; it does not compare commit SHAs. Two operations follow:

- **Engine fix after arming**: a commit changing only `.github/loop/` (scripts, tests). The tag stays; validation passes.
- **Definition change**: a change to `execution/`, `policy/`, `engine.yml`, `goal/` or `templates/`. Validation fails until a new `setup-baseline` tag is agreed with the owner.

## Not exercised here

The default test suite runs the engine against an in-memory GitHub and real git repositories. It does not validate
live GitHub workflow execution, release operations, assignment or cancellation. Linux kernel isolation and the real
model/network boundary have separate checks described in [session instructions and network access](session-contract.md);
the provider check requires explicit opt-in and credentials. Exercise the deployed workflows in the trial loop.

## Tests

`python -m unittest discover -s .github/loop/tests` (needs `pyyaml`, `git`, `bash`). `fakes.py` is the fake GitHub and the
git world. In a loop's repository the suites for the template (`test_static.py`) skip themselves.

## Routed cloud execution

`engine.yml.provider_pool` is the owner's provider/model allowlist and backoff
bound. `policy/params.yml.routing.tasks` supplies ordered candidates per task
class. A matching role class is used first, otherwise the explicitly declared
`default`; `route:<class>` selects another declared class. Policymaker sessions
always use `policymaker`. Policy cannot add IDs outside the owner's catalog.
Changes to routing are validated before policy merges and again at session start.
Legacy `model:` aliases and `policymaker_session.model` apply to the old Claude
path; routed selection is controlled by the ordered candidate lists. Effort,
time and action-count ceilings continue to constrain every provider.
The routed `max_turns` is a hard cap on proposed broker actions, rather than a
portable count of provider-internal inference turns. Unexpected native tool
requests terminate the transport; per-request deadlines and the session's outer
process timeout bound internal work. This replaces the Claude-only CLI turn cap
with an action cap plus wall-clock enforcement. Observed token/cache usage is
recorded by provider/model; it is not a provider billing ledger.

The setup enables this path in configuration while AUTOPILOT remains off.
`session.yml` refreshes Codex through a separate serialized trusted workflow,
then starts `runtime_entry.py` from the staged engine directory. The engine
checkout is still removed. The trusted parent receives GitHub write authority;
the model transports and role commands receive separate environment allowlists.
No model sees the workspace, App key, writer token or renewable login bundle.
Codex uses external tokens in memory; Claude has no native tools, and Copilot
sessions have an explicit empty native-tool allowlist. Native tools cannot act
on the role's workspace. Provider model connections remain online.

Models propose one JSON operation. The trusted broker applies the role's tools,
write paths, protected paths and evaluator ownership. Commands have immutable
git metadata, no credential environment, and only permitted writable mounts.
Offline roles additionally deny all socket creation with the existing seccomp
helper. Prepared public sources are read-only under `@environment/` for file
tools and `$LABVIEW_ENVIRONMENT` for commands. Docker daemon access is not granted
to role commands; NI container readiness is a separate trusted environment check.
Skills are staged files read through the broker. Finish requires a marked report
whose fenced YAML terminal status matches the operation.

Shared availability and per-session continuation live on `loop-runtime`, outside
the default branch, through GitHub content-SHA compare-and-swap. Concurrent writers
retry instead of replacing another session's observations. Quota, transport and
service errors use bounded cooldown; a provider's explicit future reset takes
precedence. Time alone never proves availability. New credentials clear an auth
failure/expired-worker observation, while preserving quota and entitlement state.
All unavailable candidates park the issue without the legacy three-resume limit.
A dead Claude credential no longer stops the other providers in the watchdog.

Before an operation, the parent persists its intent. After it, accepted source
changes are committed and pushed only to `task/N`, while reports and artifacts
are snapshotted into immutable-named assets of release `loop-checkpoints`.
The continuation is then saved with that code/output identity. Interrupted
commands are never replayed automatically: recovery tells the next model to
inspect the current files. Extraction accepts only canonical declared outputs;
staged inputs cannot be replaced. Archives have a 2 GB restoration bound.
The normal epilogue, protected-path checks, independent evaluator verification
and change gate still decide what may enter the default branch.
An execution/store failure or a killed worker with a saved continuation parks
the same issue for recovery. Git subprocess errors are sanitized before they
can expose an encoded authorization header in a traceback.

Cloud evidence and remaining checks are in [cloud-authentication.md](cloud-authentication.md).
This setup verification never enables AUTOPILOT and does not implement the product.
