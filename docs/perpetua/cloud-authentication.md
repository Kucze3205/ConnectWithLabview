# Cloud authentication: implementation prerequisite

Status: credential work in progress, checked 18 October 2026. The owner explicitly
retained this public repository for GitHub Actions capabilities and rejected a
private control repository. That is the accepted location; do not reopen the
visibility question. Provider adapters and the complete credential lifecycle are
not implemented yet. The product goal is unchanged.

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
| Codex | Dedicated CI login bundle in environment secret `CODEX_CI_AUTH_JSON` | A serialized trusted worker restores the latest bundle, lets Codex refresh it, then writes the resulting bundle back to a secret manager, including after a failed model call. Desktop and CI must not rotate copies of the same login concurrently. |
| Copilot | Actions' short-lived `GITHUB_TOKEN`, passed as `COPILOT_GITHUB_TOKEN` | The readiness job requests `copilot-requests: write` and tests compatibility with the pinned CLI. In this personally owned repository it draws from the owner's Copilot seat. No copied personal token is used by this job. |

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

## Accepted deployment and replacement checks

Keep product and control workflows in this public repository, as the owner
decided. OpenAI's private-automation deployment recommendation therefore does not
cover this layout; do not describe the topology as officially recommended.
Replace the private-repository assumption with owner-controlled workflow refs,
no credentialed PR jobs, branch-restricted credential environments, a serialized
refresh stream and isolation of model/tools from storage-write authority.
These replacements still need adversarial cloud checks. No paid API, overage or
cloud VM purchase is authorized.

For ephemeral workers, use a secret store that can return the latest credential
after acquiring the provider lock. Repository Actions secrets are loaded when a
workflow is queued, so serialization alone must not be assumed to make queued
snapshots current. A protected environment's secrets are read when its job starts;
this is a candidate for serialized Codex jobs, to be verified before adoption.
Source: [When Actions reads secrets](https://docs.github.com/en/actions/reference/security/secrets#when-github-actions-reads-secrets).

Writing refreshed credentials requires separate trusted authority. The normal
job token cannot be given arbitrary repository permissions. A narrowly installed
GitHub App with repository Environments write permission can update this
environment-secret store; it is not provisioned yet. Repository-secret updates
would instead require Secrets write. Never give storage-write authority to the
model or any tool subprocess. Sources:
[Additional token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token#granting-additional-permissions),
[Environment secret update API](https://docs.github.com/en/rest/actions/secrets#create-or-update-an-environment-secret).

## Implemented round trip, awaiting real credential provisioning

`credential_store.py` and the Codex readiness job implement a restore/lease/run/
persist sequence. Its tests cover refreshed tokens on the next runner,
interruption, failed write-back, invalid bundles, symlinks, file permissions and
store-authority isolation. This is not yet a live proof of renewal, or an
integration with ordinary task sessions.

Renewal invokes Codex App Server's `account/read` with `refreshToken: true`,
without a model prompt or a custom OAuth implementation. A successful response
must change the auth file before write-back is allowed. Failure or an ambiguous
response keeps the lease marker. The subsequent model probe receives only an
external-token projection, with an empty refresh token, in a separate scratch
home. It cannot rotate the maintenance credential. This file format is an
internal contract of the pinned Codex CLI and needs revalidation before upgrading;
the future task adapter must preserve this separation. Sources:
[App Server authentication](https://learn.chatgpt.com/docs/app-server),
[pinned authentication implementation](https://github.com/openai/codex/blob/rust-v0.162.0-alpha.17.2/codex-rs/login/src/auth/manager.rs).

All three `provider-*` environments are restricted to `main` and
`perpetua/setup`. The readiness provider jobs additionally require this exact
repository, its owner as actor, and one of those refs. The Codex job's shared
`provider-credential-codex` concurrency group must also be used by any future
workflow that receives a managed refresh credential.

The Codex path is opt-in through environment variable
`CODEX_CREDENTIAL_STORE_READY=on`. It requires, in environment `provider-codex`:

- `CREDENTIAL_STORE_APP_CLIENT_ID` (variable), identifying an App installed only
  on this repository with Environments write permission.
- `CREDENTIAL_STORE_APP_PRIVATE_KEY` (secret), used by the token action only.
- `CODEX_CI_AUTH_JSON` (secret), from a dedicated CI login, not the desktop copy.

Before invoking Codex, the trusted writer replaces the secret with a non-secret
lease marker. After successful renewal, even on model failure, it writes the resulting
bundle back. Cancellation, ambiguous renewal or storage failure leaves the marker; the next job
rejects it and requires a fresh dedicated login. This trades automatic recovery
after an interrupted credential transaction for rejection of stale refresh
tokens. It does not preserve a lost rotated bundle magically. The credentials
directory is outside the workspace, has private permissions, is never uploaded,
and is removed in the final cleanup step. Writer errors publish only fixed
summaries. The model process receives neither the App key nor its writer token.
`probe_isolation.py` additionally runs each model CLI in a mount/PID namespace
containing system runtimes and that probe's scratch directory. Other runner
files and parent process environments are absent. Each provider job checks this
boundary before making its request. This prevents native tools in a probe from
reading the maintainer's full bundle or Actions token-output files. Task-workspace
permissions and offline tool networking still require the separate adapter work.

Without that opt-in, Codex readiness still tests the existing bootstrap snapshot;
it projects that snapshot to access-only credentials and cannot refresh it.
Its success does not establish renewal. Parallel task workers must eventually
receive access-only credentials or use the same serialized stream; the current
task workflow still uses Claude. These integrations remain part of the open task.

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
