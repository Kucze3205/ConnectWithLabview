# Cloud authentication and routed execution

Status: credential work in progress, checked 18 October 2026. The owner explicitly
retained this public repository for GitHub Actions capabilities and rejected a
private control repository. That is the accepted location; do not reopen the
visibility question. Provider adapters, shared availability and durable role
execution are implemented on the setup branch. Cloud verification is described
below; the integration issue remains open until its remaining checks pass. The
product goal is unchanged and AUTOPILOT remains off.

## Observed cloud evidence

[Environment readiness](https://github.com/Kucze3205/ConnectWithLabview/actions/runs/39073653443)
ran on hosted Ubuntu with the pinned CLIs in `cloud-providers.json`.
The uploaded summaries report Claude subscription exhaustion and actual expected
answers from Codex and Copilot. A [later hosted check](https://github.com/Kucze3205/ConnectWithLabview/actions/runs/39074979503)
also passed the mount/PID boundary checks, Codex's access-only credential format
and Copilot's short-lived job token. Claude still reported subscription exhaustion.
The engine suite passed 282 tests, with 11 skips (template-only checks and the
opt-in live Claude tool-network check), in the same
[cloud run](https://github.com/Kucze3205/ConnectWithLabview/actions/runs/39074979503).
These early observations establish access at the time of the check. Later
renewal and task-execution evidence below supersedes their narrower coverage.
The owner replaced Claude's bootstrap credential with a one-year setup-token.

## Provisioned credential layout

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
The cloud jobs exercise the filesystem/process boundary and role tools. No paid API, overage or
cloud VM purchase is authorized.

For ephemeral workers, use a secret store that can return the latest credential
after acquiring the provider lock. Repository Actions secrets are loaded when a
workflow is queued, so serialization alone must not be assumed to make queued
snapshots current. A protected environment's secrets are read when its job starts;
this is the implemented store for serialized Codex maintenance jobs. Sequential
cloud jobs restored and renewed the previous job's saved bundle successfully.
Source: [When Actions reads secrets](https://docs.github.com/en/actions/reference/security/secrets#when-github-actions-reads-secrets).

Writing refreshed credentials requires separate trusted authority. The normal
job token cannot be given arbitrary repository permissions. A narrowly installed
GitHub App with repository Environments write permission can update this
environment-secret store; the owner provisioned it for this repository. Repository-secret updates
would instead require Secrets write. Never give storage-write authority to the
model or any tool subprocess. Sources:
[Additional token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token#granting-additional-permissions),
[Environment secret update API](https://docs.github.com/en/rest/actions/secrets#create-or-update-an-environment-secret).

## Implemented and exercised round trip

`credential_store.py` and the Codex readiness job implement a restore/lease/run/
persist sequence. Its tests cover refreshed tokens on the next runner,
interruption, failed write-back, invalid bundles, symlinks, file permissions and
store-authority isolation. The owner completed the dedicated CI login and App
setup. Two successive cloud runners completed restore, lease, forced renewal,
model response and write-back in
[run 39074979503](https://github.com/Kucze3205/ConnectWithLabview/actions/runs/39074979503).
The second Codex job completed on 18 October at 08:51 UTC.

Renewal invokes Codex App Server's `account/read` with `refreshToken: true`,
without a model prompt or a custom OAuth implementation. A successful response
must change the auth file before write-back is allowed. Failure or an ambiguous
response keeps the lease marker. The subsequent model probe receives only an
external-token projection, with an empty refresh token, in a separate scratch
home. It cannot rotate the maintenance credential. This file format is an
internal contract of the pinned Codex CLI and needs revalidation before upgrading;
the task adapter instead supplies external access tokens over App Server stdin
and keeps them in memory, with no auth file visible to native tools. Sources:
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
directory is outside the workspace, has private permissions and is never uploaded;
the auth file is removed in the final cleanup step. Writer errors publish only fixed
summaries. The model process receives neither the App key nor its writer token.
`probe_isolation.py` additionally runs each model CLI in a mount/PID namespace
containing system runtimes and that probe's scratch directory. Other runner
files and parent process environments are absent. Each provider job checks this
boundary before making its request. This prevents native tools in a probe from
reading the maintainer's full bundle or Actions token-output files. Task-workspace
permissions and offline command networking are enforced separately by
`tool_broker.py` and checked on the cloud kernel.

Without that opt-in, Codex readiness still tests the existing bootstrap snapshot;
it projects that snapshot to access-only credentials and cannot refresh it.
Its success does not establish renewal. Maintenance now publishes only
`CODEX_WORKER_AUTH_JSON` to `provider-claude`, the execution environment that also
holds Claude's setup-token. Neither the renewable bundle nor the App key leaves
`provider-codex`. `session.yml` calls the serialized credential-maintenance
workflow before starting a routed worker. A maintenance failure does not prevent
Claude or Copilot from executing; the failed transaction still requires repair.

## Execution and model discovery evidence

The [structured transport check](https://github.com/Kucze3205/ConnectWithLabview/actions/runs/39114968592)
obtained Claude's catalog through its control protocol, Codex's catalog through
`model/list`, and real schema-validated actions from Codex `gpt-6.1-sol` and
explicitly selected Copilot `gpt-5.6-luna`. Claude's model request correctly
reported subscription exhaustion. These catalogs populate the owner's allowed
IDs in `engine.yml`; only executed IDs have positive inference evidence.

With the job token, Copilot's `models.list` is empty despite working inference.
Its runtime default reported `gpt-5.6-luna`, then an explicit request for that
ID succeeded. Do not invent more selectable Copilot IDs from an empty catalog.
The pinned runtime's `--no-auto-login` blocks this installation-token path;
use environment authentication in an empty scratch HOME without that flag.
The App/Actions token must not use the SDK's user-token option. See
[GitHub's server-to-server authentication instructions](https://docs.github.com/en/copilot/how-tos/copilot-sdk/auth/server-to-server-tokens).

[Run 39114566066](https://github.com/Kucze3205/ConnectWithLabview/actions/runs/39114566066)
executed the actual role runtime: Claude hit its real limit, policy selected
Codex, six accepted role operations completed the file task, source was pushed
to `task/900039114566066`, and a deleted report was restored from a remote
checkpoint release asset. This was setup verification, without merging to main
or arming the loop.

[Run 39136473067](https://github.com/Kucze3205/ConnectWithLabview/actions/runs/39136473067)
passed 322 engine tests (11 skipped), credential renewal and both interruption/
recovery pairs. The ordinary role used Codex `gpt-6.1-sol`; the Policymaker used
`gpt-6-astra`. Each test stopped after pushing its first source change but before
saving the continuation, leaving a pending Write intent. Separate fresh runners
then used Copilot `gpt-5.6-luna` to inspect the accepted file, create/verify the
report and finish. Both tests confirmed the source commit on the remote task
branch and restored the report from its release checkpoint. Concurrent updates
to one state document also survived the real content-SHA race. No pending action
was blindly replayed. The source refs are `task/900039136473067` and
`task/900139136473067`; neither enters main.

The complete run remains red solely because Claude's independent readiness call
reports quota. During an earlier run Codex also reported quota; no capacity was
invented or spending enabled. A later actual request again proved Codex available.

## Remaining verification

- Verify a successful structured Claude task after subscription capacity returns.
- Review a successful Claude task before resolving the integration issue.
  Revocation, entitlement, transient errors,
  all-provider exhaustion and ambiguous command replay are fault-injection tests;
  the owner's live credentials are not deliberately revoked.
- Cancellation during credential rotation cannot recover a lost rotated bundle.
  Tests verify rejection of the lease/stale seed and write-back failure; repair
  requires a new dedicated login. Do not claim unattended recovery from that case.
- Keep raw credentials, auth files, provider output and refresh diagnostics out
  of logs and artifacts. Only sanitized status summaries may be published.
- Preserve the catalog, policy/Policymaker bounds, kernel isolation and scheduler
  checks on upgrades; probe success alone does not establish task execution.

`cloud_probe.py` now separates authentication, model entitlement, subscription
quota, transient request throttling, network failures and provider service
failures. An unexplained 403 remains unknown. It preserves only explicit future
numeric provider reset timestamps; absent a reset, the scheduler uses bounded
retry instead of inventing one. `role_runtime.py` persists these observations
through the content-SHA state store and uses them for subsequent selections.
