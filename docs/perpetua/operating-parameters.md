# Starting operating parameters

The owner accepted the two intervention thresholds in setup topic G on
18 October 2026. Configuration is in `engine.yml` and `policy/params.yml`;
ordinary role limits are in `execution/profiles.yml` and `policy/profiles.yml`.

## Costs and model selection

Existing subscriptions and resources only, within the accepted limits in
[accepted-limits.md](accepted-limits.md). No additional spending was granted.
Time, turns and routing are operating controls, not a monetary budget or billing
ledger. Paid APIs, purchased quota and paid runners/storage still need a concrete
owner grant with an explicit ceiling.

Retain the cloud-only Claude/Codex/Copilot routing established in topic B2.
The Policymaker may reorder/subset the owner's model catalog by task using
actual availability, suitability and resource evidence. A model listed in
configuration does not establish entitlement or remaining quota. The adapters
probe availability, checkpoint, fall back and resume after limits; they do not
create a spending grant.

The owner wants the best quality per quota consumed in every available case.
Availability changes constantly (a provider may be exhausted until a reset or
have a small allowance), so the Policymaker chooses and reorders candidates by
task class during the loop from current availability and measured usage; no
fixed order is assumed. Evidence and its limits: [model-selection.md](model-selection.md).
The Policymaker's own session stays on `claude-opus-5-5`: it runs only when the
core loop is not making enough progress. Claude's successful task test remains owner-deferred,
as recorded in [cloud-authentication.md](cloud-authentication.md).

## Sessions and cadence

Retain the supplied outer ordinary-session cap of 240 minutes and 150 turns.
Starting role profiles use at most 120 minutes; research, benchmark and evaluator
roles use 120 turns, independent reviewers 100, and implementation and the
orchestrator 150. Smaller task limits apply before larger role/policy ceilings.
The Policymaker starts at 90 minutes and 150 turns, bounded by the owner's
separate ceiling. The routed runtime bounds model requests/tool actions per
invocation; resumed invocations have their own caps. These are not cumulative
token or financial caps over the lifetime of an issue.

Continue iteration after iteration. The design criterion is the best quality of
accepted results per unit of subscription quota consumed (owner decision of
20 October 2026, replacing "shortest wall-clock time to the goal"); wall-clock
time only breaks ties. No daily iteration cap, cadence delay or separate
policy iteration timeout is introduced. The Policymaker may tune its permitted
parameters from evidence without changing owner-controlled engine safeguards.

## Two distinct interventions

- **No closed iteration for 24 hours:** the watchdog fails the active iteration,
  restores the managed definitions (`execution/` and `policy/`) to the last closed iteration's state (or `setup-baseline`
  before the first close), notifies the owner and retries. Unaccepted policy
  changes since that state can be discarded. The watchdog checks every
  30 minutes, so intervention occurs at the next check after the threshold.
- **Ten consecutive iterations without an accepted improvement:** open a notice
  for the owner and keep useful independent work running. This is not a stop or
  a new success criterion. Preparation reports remain distinct from evidence
  of product quality.

Blocking owner-decision waits are excluded from the 24-hour clock, including
the completed portion after the owner's answer. Overlapping waits count once.
An optional access proposal does not pause this clock or independent work.
Provider quota parking remains subject to the ordinary watchdog rule; it is not
an owner-decision wait. Existing repeated-failure outage controls still apply.

A Policymaker session opens the iteration when a trigger is due, and the
iteration waits for it: the first iteration always, then every fifth iteration,
each additional three iterations without improvement, a new audit report or
new session suggestions. Only one Policymaker session runs at a time. The first
session orders an audit unless already ordered, running or complete; later
audits follow evidence.

## Starting order of work

Investigate prepared sources and coverage, prepare the repeatable verification
method with independent expected answers and evaluation separation, obtain a
separate review and owner acceptance, then implement the product. Use the
readiness contract in [evaluation.md](evaluation.md) and responsibilities in
[roles.md](roles.md). Numeric product quality thresholds and the executable
goal gate still await credible benchmark evidence and the owner's acceptance.
