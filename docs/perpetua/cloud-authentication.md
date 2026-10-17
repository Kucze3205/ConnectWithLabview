# Cloud authentication: implementation prerequisite

Status: proposed credential architecture, checked 18 October 2026. This is not
an implemented provider adapter or a completed setup decision. The owner must
choose the location and access of private automation before credential persistence
is configured. The product goal and public repository are unchanged.

## Observed cloud evidence

[Environment readiness](https://github.com/Kucze3205/ConnectWithLabview/actions/runs/39073653443)
ran on hosted Ubuntu with the pinned CLIs in `cloud-providers.json`.
The uploaded summaries report Claude subscription exhaustion and actual expected
answers from Codex and Copilot. These observations establish access at the time
of the check, not credential renewal or task execution. The existing Claude
bootstrap access token expires on 18 October 2026 at 04:53 UTC, according to the
previous environment investigation; this session has not read its value.

## Proposed credential layout

| Provider | Subscription credential | Persistence and recovery |
|---|---|---|
| Claude | One-year token from `claude setup-token`, in `CLAUDE_CODE_OAUTH_TOKEN` | Owner authorizes the browser flow, then replaces the secret. Track expiry and request replacement before it; no supported unattended reissuance established. Do not use `--bare` with this auth mode. |
| Codex | Dedicated CI login bundle in `CODEX_AUTH_JSON` | A serialized private worker restores the latest bundle, lets Codex refresh it, then writes the resulting bundle back to a secret manager, including after a failed model call. Desktop and CI must not rotate copies of the same login concurrently. |
| Copilot | Existing `COPILOT_GITHUB_TOKEN` initially | Verify its lifetime and replacement procedure. An alternative is Actions' short-lived `GITHUB_TOKEN` with `copilot-requests: write`; probe the pinned CLI before adopting it. In a personally owned repository it draws from the owner's Copilot seat. |

Claude's documented CI token requires one browser authorization and expires after
one year. Source: [Claude authentication](https://code.claude.com/docs/en/authentication#generate-a-long-lived-token).

OpenAI's account-auth CI guide describes trusted private automation and explicitly
excludes public repositories. It requires retaining Codex's refreshed `auth.json`
and one serialized credential stream. Failed refresh requires login and reseeding;
an original snapshot restored on every run is insufficient. Source:
[Official OpenAI CI authentication guide](https://learn.chatgpt.com/docs/auth/ci-cd-auth).

Copilot's Actions authentication and billing differ between personal and
organization repositories. Keep personal subscription billing; no organization
billing or automatic extra spending has been authorized. Sources:
[Copilot in Actions](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/copilot-cli-in-github-actions),
[workflow configuration](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-in-actions).

## Concrete proposal awaiting the owner

Keep this product repository public and create a separate private control
repository, for example `Kucze3205/ConnectWithLabview-control`, for trusted cloud
workflows and provider credentials. An alternative is changing this repository's
visibility. Neither change has been made. The owner chooses the location and
accepts the necessary access before it is provisioned. Private hosted Actions may
consume the account's included private-repository minutes; no paid overage or
cloud VM purchase is authorized.

For ephemeral workers, use a secret store that can return the latest credential
after acquiring the provider lock. Repository Actions secrets are loaded when a
workflow is queued, so serialization alone must not be assumed to make queued
snapshots current. A protected environment's secrets are read when its job starts;
this is a candidate for serialized Codex jobs, to be verified before adoption.
Source: [When Actions reads secrets](https://docs.github.com/en/actions/reference/security/secrets#when-github-actions-reads-secrets).

Writing refreshed credentials requires separate trusted authority. The normal
job token cannot be given arbitrary repository permissions. A narrowly installed
GitHub App or fine-grained PAT with the required Secrets write permission can
update the store; neither is present yet. The owner must authorize and provision
that authority. Never give it to the model or any tool subprocess. Sources:
[Additional token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token#granting-additional-permissions),
[Secret update API](https://docs.github.com/en/rest/actions/secrets#create-or-update-a-repository-secret).

## Checks required before declaring credentials ready

- Replace Claude's bootstrap snapshot through the supported setup-token flow;
  verify model access independently of subscription capacity.
- Seed a separate CI Codex login. Verify two sequential cloud jobs preserve an
  actual refresh. Exercise overlapping job starts, stale snapshots, cancellation
  during refresh and failure to write back. Such failure must disable that
  credential until repaired, rather than silently reusing the stale bundle.
- Verify Copilot authentication and its model response from the chosen cloud
  workflow, including revoked/expired credentials and seat/model entitlement.
- Keep raw credentials, auth files, provider output and refresh diagnostics out
  of logs and artifacts. Only sanitized status summaries may be published.
- Finish adapter security, model discovery, shared availability, checkpointing
  and scheduler integration for ordinary roles and the Policymaker. Existing
  probe success and routing unit tests do not satisfy those requirements.

`cloud_probe.py` now separates authentication, model entitlement, subscription
quota, transient request throttling, network failures and provider service
failures. An unexplained 403 remains unknown. It preserves only explicit future
numeric provider reset timestamps; absent a reset, the eventual scheduler must
use bounded retry instead of inventing one. These categories are probe evidence;
they are not yet integrated with `provider_pool.py` or the loop.
