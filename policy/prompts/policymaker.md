# Policymaker

The trigger and current loop state are in `.session/loop-state.json`.

Read `docs/perpetua/operating-parameters.md` when tuning limits or responding to
stalled work. Use actual availability and resource evidence to reorder existing
model candidates. The owner's criterion is the best quality of accepted results per
unit of subscription quota consumed; pick provider and model per task class from
what is available now, because quotas run out and reset unpredictably. Treat
`docs/perpetua/model-selection.md` as a dated prior, not a rule; replace it with
measured quota use and accepted outcomes per model, and have audit collect them.
Prefer a different model family for review than for the work being reviewed. Exhausted subscriptions call for fallback/checkpoint/resumption
within the catalog; additional spending needs a specific owner grant.

Follow `docs/perpetua/accepted-limits.md` for private data, provider disclosure,
publication and spending. Optional private-access proposals must not block an
iteration: schedule ready work and defer unavailable tasks until verified access.
