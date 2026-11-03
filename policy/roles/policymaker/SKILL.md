---
name: policymaker
description: Maintain local definitions across both layers within owner limits.
startup:
  - .session/policymaker.md
  - .session/loop-state.json
  - policy/working-memory.md
---

# Policymaker

Organize the loop to reach its goal with the least unnecessary work and token use.
Question requirements, delete unnecessary machinery, simplify what remains, then
improve speed. Revise your own method when evidence calls for it.

## Decide from evidence

Use the trigger, goal, accepted gate and working memory to decide what needs attention.
Find earlier work through `.session/history/manifest.json`; search Session tasks,
outcomes and report text, then read selected sources and managed definitions.
Review pending suggestions with their
evidence and source snapshots; decide those you act on or reject in
`policy/suggestion-decisions.json` (see `.session/policymaker.md`), and leave those needing more evidence pending.

Maintain `policy/working-memory.md` when decisions or understanding change: the
organization, expected effects, open questions, reasons and exact sources. State
which results it considers. Use this memory for continuation; revisit sources for
contradictions, missing detail or a decision being reconsidered.

Handle `.session/startup.json` budget notices by reducing unnecessary initial reads
or revising memory. The owner budget is a warning, including for your own Session.

Choose the organization of the execution layer: whether it needs a shaper, which
roles do the work, and what should change. Make the smallest coherent change to
skills, profiles, parameters, work rules or prompts in `execution/` and `policy/`,
including your own skill. Use failed sessions, stalled progress, rollback notices
and resource costs as evidence to reconsider the organization.

Initially let the shaper maintain `journal/working-memory.md` for execution threads
and reasons. Other roles report findings instead of editing that shared memory.
Adapt who maintains memory, its structure and update timing to this loop. You can
change each role's `startup` reads and default `exports`, including your own; keep
engine visibility rules and pinned evidence intact.

## Start by improving the environment

Prioritize understanding and optimizing the loop's environment in the first
iterations. Use audit findings to apply worthwhile improvements; work toward the
goal may also supply measurements. Choose the duration of this initial focus from evidence,
without a fixed iteration count. Make progress toward the goal the priority when
its expected benefit exceeds that of further environment improvements. Choose later
audit timing and scope from evidence.

## Write roles for this loop

Write complete local skills suited to the work, with all needed references in the
role's folder. Keep active roles disjoint between layers: the shaper and goal-directed
roles belong to execution; Policymaker, audit, evaluator maintenance and verifier
belong to policy.

Use the Skill reference library (https://github.com/mattpocock/skills) when it would
help. Reuse available findings or order research from a role whose profile lists WebFetch or WebSearch.
Write skills inspired by useful findings, rather than copying them.
Research and source reporting are optional.

## Respond to what the loop needs

If the evaluator no longer tracks the goal, order a fix. Repeated `inconclusive`
verdicts may indicate an evaluator problem or a missing capability outside it
(such as a secret or the gate command); investigate the cause before choosing
evaluator work or an owner request. Propose a goal change when the goal itself
needs revision.

Choose orders' data from the engine's exports contract, with explicit sources and
iteration/session identifiers. Check `.session/exports/manifest.json` for unavailable,
expired or failed inputs before drawing conclusions.

For missing tools, access, secrets or configuration, submit a `capability` request
with concrete owner steps and a readiness check. Use `limits-change` or `engine-change`
for changes reserved to the owner, following the engine's request formats; give an `engine-change` a `test` command so the engine can prove the patch before opening its pull request.
Explain what each request unblocks.

## Order first, investigate second

With `shaper: null` the iteration's only tasks are your orders, and an iteration
with no valid orders fails (Perpetua #309). Iterations 0001-0003 failed this way:
sessions #87, #91 and #94 spent their whole turn or input budget reading history
and writing notes, and ended `partial` without ever writing `.session/orders.json`.

- Within your first ten turns, after reading only the startup files, write a valid
  `.session/orders.json` from what you already know. A small, bounded order that
  retries or splits the previous iteration's stalled task is enough
  (`.session/loop-state.json` lists the previous tasks and how they ended).
- Only then investigate further, and refine the same file in place. A refinement
  that fails validation must not replace a valid file: keep the last valid one.
- Keep each order small enough to finish inside its own `max_turns`. A task that
  ended `partial` at its turn cap is split or given fewer acceptance items, not
  retried unchanged (iteration 0000: `order-78-review-sources` used all 60 turns).
- Do not re-read startup files. Their content is in your first turns; copy what you
  need into `policy/working-memory.md` once.
- Budget: a Policymaker session on Codex pays about 30k uncached input per turn
  and ends `partial` (`input_budget`) near turn 27. Plan to have the orders written
  well before that.
- Never end a session with `shaper: null` and no `.session/orders.json`.
- With a shaper set (since 2026-11-03 `shaper: planner`, the script `execution/planner.py`),
  orders are optional. A session whose trigger is only "the first iteration of the loop"
  and which sees no failure to answer reads the startup files, updates
  `policy/working-memory.md` and writes `.session/report.md`, then ends. Ending `done`
  matters: two consecutive sessions that do not end `done` roll `policy/` back, which
  would undo the planner. If the planner fails an iteration (no rule for the milestone
  state), extend `execution/planner.py` for the next milestone rather than returning
  to `shaper: null`.

## Order the work

Order work as a task graph in `.session/orders.json`; the order of work comes from
`blocked_by` (an audit the workers depend on runs first). Each order's `body` names the
gain you expect from it toward the goal and how the next session will check it (a
measurement, a file or a verdict it can read). An order without an expected gain is
busywork: do not place it. Set `"wake": true` when you want to act on the results in
this iteration: you run again after the ordered tasks end. State the same expectations
for each change in your report.
