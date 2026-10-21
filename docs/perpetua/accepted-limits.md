# Accepted limits and owner decisions

Accepted in setup topic F on 18 October 2026. These boundaries apply to the
Policymaker, ordinary roles and trusted preparation jobs.

## Technical autonomy

Agents choose technical solutions, organize ordinary roles, prepare verification
and implement assigned work within granted tools and paths. The product is the
tool enabling AI agents to read LabVIEW code, projects and all artifacts like
ordinary code; its delivery form is open. Product implementation follows the
independently checked, owner-accepted verification method in [evaluation.md](evaluation.md).
Preparing the environment, examples and verification method can precede that.

`engine.yml.limits` retains git/Python and file tools and explicitly requires
consent for any online role, including one with no repository write paths.
Existing model transports stay online through trusted adapters; this does not
grant role commands network access. Prepared sources are read-only for roles.
The Policymaker may adjust ordinary profiles within these limits. The owner
retains engine, verifier contract, goal, success criteria and AUTOPILOT authority.

## Sources, access and publication

Agents may propose public sources and free dependencies. Trusted preparation
pins sources, checks provenance/license and supplies them to offline roles.
Adding preparation capabilities or external services requires an owner request;
changing a role's internet flag does not install a transport or a web tool.

Private projects require a concrete grant specifying the materials, permitted
processing location, model providers and publishable outputs. Permission to read
does not authorize uploading material to model providers or publishing it.
New categories of published data require owner approval. The existing public
repository continues to hold reports and accepted code; redact secrets, private
source material and withheld evaluation content from issues, logs and artifacts.

The owner prefers granting concrete private access during setup. No specific
private project or restricted evaluation store has been identified in topics
B/E/F; no blanket private-data grant is inferred. Once a concrete proposal exists,
specify resource, least required access, recipient providers, publication limits,
revocation and a readiness check before asking. Do not put secret values in issues.

Evaluation cases withheld from development and answer keys need restricted
storage/execution and a tested separation from product-development sessions.
A path in this public repository, its history or public release assets provides
no secrecy. The existing public-control-repository decision remains in force;
it does not rule out a future restricted evaluation data store.

## Costs and native LabVIEW

Use existing subscriptions and available resources within their existing limits.
No paid API, purchased quota, paid runner/storage or other additional spending is
authorized. A spending proposal names the service, purpose and explicit ceiling;
technical autonomy supplies no budget. Provider/model catalogs and quotas retain
their current controls; remaining operating parameters belong to topic G.

Native LabVIEW work runs in separate trusted cloud jobs with declared inputs,
bounded operations and staged results. Roles receive no Docker daemon access.
The established NI container readiness path remains available; extending it to
new experiments needs a concrete capability/engine proposal and readiness check.
This acceptance does not establish native 2024 execution or all-version coverage.

## Access requests do not stop independent work

Request optional private access using `capability` in `.session/requests.json`.
It creates an owner issue without a task/iteration dependency. Finish available
work and schedule other ready research, public examples, verification preparation
or implementation permitted by its prerequisites. Defer work requiring the
ungranted resource instead of creating a session waiting on its consent.
An open capability request is not an outage or a global pause and does not
prevent closing an iteration or starting another. Read the request's later
decision from loop state and schedule newly enabled work in a later iteration.
Do not claim unavailable evaluation evidence or silently reduce the goal.
If all useful work truly needs missing access, report that fact without bypassing
access controls or manufacturing repeated busywork.

## GitHub decisions and recovery

Only `Kucze3205` may decide owner requests. The engine stores the original body
in trusted state; editing the issue or displayed hash cannot change a grant.
Completed accepts that exact proposal; Not planned refuses it. Silence grants
nothing. Consent is tied to one task and its exact permission profile; a changed
profile or copied consent label cannot authorize another session.

Capability acceptance also requires manual provisioning and the proposal-specific
`capability-ready` confirmation after the readiness check. Closing alone creates
no credential or access. Limits-change applies only its frozen limits mapping
against the recorded base. Engine-change requires manual application, checking
and the printed `engine-applied` confirmation. Refusal supplies no access; a
materially revised proposal is a new request rather than repeatedly reopening it.

Closing triggers `owner-request.yml`; the watchdog recovers missed close events
and readiness confirmations posted after closure. Work resumes only while
AUTOPILOT is on. Access decisions do not turn it on. Ordinary merge acceptance
and the benchmark-before-product prerequisites remain as previously accepted.
