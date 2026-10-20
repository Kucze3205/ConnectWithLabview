# Model selection: quality per quota

Owner preference (20 October 2026): the best ratio of result quality to subscription quota consumed
("tokens"), in every available case. Wall-clock time only breaks ties. No paid API or extra spending
is implied; see [accepted-limits.md](accepted-limits.md).

This file is evidence and a starting prior, not a routing rule. The Policymaker decides during the loop
which provider and model each task class uses, from actual availability and measured usage, within the
catalog in `engine.yml` `provider_pool`. Limits can be exhausted or unavailable at any time (for example Codex
until its reset, a small Copilot allowance, Claude subscription exhaustion in every cloud run so far), so no
fixed order is assumed. The engine already probes availability and falls back along the declared candidates.

## What the evidence is and is not

Collected 20 October 2026 from provider pricing pages and the Artificial Analysis (AA) Intelligence Index
v4.3.2. API-equivalent cost stands in for subscription quota: no provider publishes per-model quota weights
for the owner's plans, so the ranking is a hypothesis with medium or low confidence. The index measures
general task solving, not defect finding or LabVIEW reading. The repo records availability only, not
per-model quota use or task success.

| Model | Price in/out per Mtok | AA index / cost per task (high effort unless noted) |
|---|---|---|
| gpt-6.1-sol | $2 / $10 | 50 / $0.32 (52 / $0.72 at max) |
| claude-opus-5-5 | $4 / $20 | 54 / $1.82 (58 / $5.98 at max) |
| claude-sonnet-5-5 | $2 / $10 | 47 / $0.88 (56 / $5.46 at max; the most verbose model AA measured) |
| gpt-6-astra | $10 / $50 | 51 / $1.73 (reserve for hardest science tasks) |
| claude-fable-5-1 | $10 / $50 | 51 / $3.91 (dominated by Opus 5.5) |
| gpt-6-luna | $0.10 / $0.50 | 33 / $0.03 (untested here; candidate for mechanical edits) |
| gpt-5.6-luna (Copilot) | $0.20 / $1.20 | 37 at max / $0.18; AA marks it deprecated; has run successfully here |
| claude-haiku-5-5 | not in the evidence | AA: 43 / $0.21 at max; added to the catalog on 20 October 2026, unverified here |
| claude-haiku-4-5-20251001 | $1 / $5 | about 15, estimated; deprecated |

Other catalog entries (`gpt-6-sol`, `gpt-5.6-sol`, `gpt-5.6-terra`) have weaker or unconfirmed evidence and are
fallbacks at most.

## Starting prior (not a rule)

- Planning, research, benchmark: `gpt-6.1-sol` gives about 5 times less cost than Astra for 1-2 index points less;
  Opus 5.5 leads the index and Terminal-Bench but uses far more output tokens at high effort.
- Implementation: `gpt-6.1-sol` over `claude-sonnet-5-5` on cost; Sonnet's effort curve is steep
  (high to max: six times the cost for nine points).
- Independent review: another model family than the implementer. Do not let a model review its own code.
  Luna is a cheap first-pass filter, not a sole reviewer.
- Never request Codex fast or ultrafast modes (2.5 and 8 times the allowance).
- Effort scales cost steeply for Claude; `efforts: [low, medium, high]` already caps the worst case.

## What the loop should measure itself

The adapters keep per-session token counts. To rank models by accepted outcome per quota, the audit role should
join these with the quota percentage before and after a session, the gate verdict, rework iterations and
reviewer defect counts, and log quota exhaustion per provider per day. Useful experiments: matched A/B runs of
the same task class on two models; seeded defects in a diff to calibrate reviewers; one task class at low, medium
and high effort to find the knee of the curve. Record the date of any figure used, because limits and prices
change.

Sources: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing),
[Codex pricing](https://learn.chatgpt.com/docs/pricing),
[GitHub Copilot usage-based billing](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals),
[AA leaderboard](https://artificialanalysis.ai/leaderboards/models).
