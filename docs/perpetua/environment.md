# Environment readiness

The owner requires the entire loop to execute in the cloud. Their Windows machine
is not a runner. Public source preparation and model access checks run on GitHub
hosted Ubuntu; using a full LabVIEW IDE in the cloud remains an explicit access gap.
The product goal is unchanged and no artifact family has been excluded.

Version requirement clarified by the owner on 18 October 2026: prioritize all
LabVIEW versions; LabVIEW 2024 is the accepted fallback if investigation shows
substantially greater time is needed for all versions. Estimate that difference
before choosing a version scope. No numeric time threshold was agreed. The local
LabVIEW 2026 observation does not verify LabVIEW 2024 or cross-version compatibility.

## Reproducible public sources

`.github/loop/prepare.sh` calls `prepare_environment.py`. It needs Python 3.10+
and git, no secrets, pip installations or NI activation. Sources and exact commits
are in `.github/loop/environment-sources.json`:

- NI Actor Framework, MIT, commit `371c631c16155d88f02be11a953e4964d7452fd8`.
- pylavi, Unlicense, commit `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75`.

The check fetches these commits, rejects tracked modifications in its cache,
checks license markers and the SHA256 of one real NI VI, loads its resource table
with the pinned parser, and parses a real LabVIEW project as XML. It writes
`readiness.json` and exposes the cache as `LABVIEW_ENVIRONMENT` to subsequent job
steps. Default cache: `$RUNNER_TEMP/connectwithlabview-environment`.
Public copies stay outside git. No NI installation files or personal projects are
redistributed. Downloads require outbound HTTPS to GitHub.

Preparation passed twice in a clean Linux Python 3.12 container and on Windows
Python 3.14. The checked VI contains 30 resource types; this is evidence of resource
access, not correctness of diagram interpretation. The public project reports
LVVersion `20008000`. Broader coverage and independent expected answers belong to
the evaluator/benchmark work; do not use parser output as its own sole oracle.

Hosted confirmation: [Environment readiness, run 39073653443](https://github.com/Kucze3205/ConnectWithLabview/actions/runs/39073653443)
on 18 October 2026 (Europe/Warsaw) passed public source preparation and its second
invocation on GitHub-hosted Ubuntu 24.04.

The engine test suite passed on Linux/Python 3.12: 263 tests, 11 skipped
(template-only and opt-in live checks). This includes the routing and probe
classification tests. It does not validate unfinished adapter integration.

## Cloud provider access checks

`.github/workflows/environment.yml` runs on setup-branch changes to environment
code, and can be dispatched after GitHub registers the workflow. It does not call
the loop, merge work, or enable `AUTOPILOT`. Repository Actions are enabled; the
workflow needs only `contents: read` plus the selected provider's secret. No custom
runner is registered. `AUTOPILOT=off` is explicit during setup.

Pinned CLI packages are recorded in `.github/loop/cloud-providers.json`. Each
provider job installs just its CLI, calls a fixed probe in an isolated temporary
home, and uploads a summary, never credentials or raw model streams. A missing
secret, exhausted quota or failed response fails that readiness check. Generic
429/network failures remain unknown; they do not prove a depleted subscription.

| Provider | Repository secret | Access semantics |
|---|---|---|
| Claude | `CLAUDE_CODE_OAUTH_TOKEN` | Bootstrap access token from the existing Claude subscription. Current snapshot expires 18 October 2026, 04:53 UTC; a durable token from `claude setup-token` is still needed. |
| Codex | Bootstrap `CODEX_AUTH_JSON`; opt-in environment `CODEX_CI_AUTH_JSON` | The existing snapshot proves model access only. The new guarded secret round trip requires a dedicated CI login and the App described in cloud-authentication.md; it is not yet enabled or live-verified. |
| Copilot | Job `GITHUB_TOKEN`, passed as `COPILOT_GITHUB_TOKEN` | The readiness job now requests `copilot-requests: write` and checks the pinned CLI. Current GitHub documentation supports this in personally owned repositories against the owner's seat. The earlier copied OAuth token remains stored but is no longer passed by this readiness job. |

The owner requested access to these accounts for cloud execution. Bootstrap values
were transferred directly to encrypted repository secrets without printing them.
They are not a complete unattended credential-renewal system. No API billing mode,
automatic credit purchase or provider substitution has been enabled.

The [credential requirements and accepted public repository](cloud-authentication.md)
record verified renewal requirements and cloud evidence. The owner explicitly
retained this public repository on 18 October 2026 and rejected a private control
repository. OpenAI's account-auth CI deployment recommendation covers private
automation; that recommendation does not cover the chosen layout. Trusted workflow
and credential-isolation checks must replace that assumption. No visibility or
billing change has been made.

Local diagnostic observations before adopting the cloud-only constraint: Claude
2.1.292 was authenticated but its real call reported a weekly subscription limit,
reset 20 October 2026 at 21:00 Europe/Warsaw. Codex 0.162.0-alpha.17.2 and Copilot
1.0.98 returned their expected probe answers. Those local observations do not by
themselves prove cloud access. The hosted workflow's summaries are the cloud evidence.

That hosted run returned `available` with an actual model answer for Codex and
Copilot, and `quota` for Claude. The overall run therefore correctly failed
readiness. Claude's cloud call reached the service and reported a subscription
limit; it did not produce a usable model answer. These observations are point-in-time
checks, not promises of availability or durable token renewal.

## Required multi-provider execution

The owner accepted [Cloud model selection and quota management](https://github.com/Kucze3205/ConnectWithLabview/issues/11).
The existing engine still launches Claude. Installing the other CLIs does not
integrate task execution, stream accounting, permissions or the watchdog.

`provider_pool.py` is a deterministic building block, with tests. Owner configuration
defines the allowed provider/model catalog and bounded retry delays; policy supplies
an ordered list of candidates for each task class. Selection distinguishes model
and provider limits, requires a probe after reset, never invents fallback models,
and waits when all candidates are limited. Authentication failures remain blocked
until explicitly updated. The caller must persist state and implement probes,
provider adapters and checkpoint continuation. No live model catalog is accepted
or inferred by this module.

The integration must replace specific Claude guarantees for both other providers:
secret isolation from tool subprocesses, offline command networking, write scopes,
ignored task-branch configuration/hooks, time/turn limits, usage accounting and
limit/reset parsing. Copilot output redaction alone is not credential isolation.
Do not arm the loop until these checks and the other setup topics are resolved.

## LabVIEW cloud access remains unverified

The local diagnostic found only one actual LabVIEW executable: 32-bit LabVIEW 2026
26.1.1f1, plus NI LabVIEW CLI. The CLI connected to LabVIEW and completed an operation
help request. A direct COM probe did not open an example successfully. Neither
finding proves scripting, activation rights or operation on a cloud machine.
Directories named for older releases were not counted as installed editors.

The owner's expanded NI License Manager screenshot, supplied on 18 October 2026,
confirms LabVIEW 2026 Q1 Community Edition is Licensed until 27 June 2027.
Professional Development System is Unlicensed; Base, Full, Continuous Integration
and Debug Deployment show Evaluation Available, not active licenses. This screenshot
supersedes the earlier uncertainty from package metadata. It establishes local
Community activation, not activation of LabVIEW 2024 or a cloud machine. No
activation was changed and no private project, serial number or NI license file
was uploaded.

NI's Community usage guidance permits personal, non-commercial, non-industrial
projects and lists free open-source projects as an example. The owner explicitly
confirmed a private, non-commercial project on 18 October 2026. The public download page does not confirm authenticated
access to the 2024 installer. Cloud deployment, account activation and unattended
operation remain to be checked separately.

## Official NI cloud automation path

[NI's official container project](https://github.com/ni/labview-for-containers)
and [headless guide](https://github.com/ni/labview-for-containers/blob/2afb30b23bdb144368ee36d5f5ca33c06f800a98/docs/headless-labview.md)
provide a cloud automation path that does not need desktop activation for supported
non-development operations. The setup uses the owner's active Community development
license and confirmed personal use for a bounded analysis/build check. Applying
the development-license container terms to that combination is an interpretation
of the published terms, not a specific NI statement about this project. No paid-only
condition or explicit Community exclusion was found. See the
[NI agreement](https://www.ni.com/content/dam/web/pdfs/legal/software_license_agreement_en.pdf),
Addendum F, and [Community guidance](https://www.ni.com/en/support/documentation/supplemental/20/labview-community-edition-usage-details.html).

The container is for automation/analysis/testing; it must not be used to author or
edit LabVIEW source. No public LabVIEW service or redistributed container image is
created. The readiness workflow mounts only a disposable fixture directory, has
no model/account secrets, and disables container networking. It mass-compiles an
existing public MIT fixture and collects operation logs and package versions.
Compilation is an environment check, not product development or the benchmark.

Pins and input provenance live in `.github/loop/labview-runtime.json`; the public
workflow is `.github/workflows/labview-runtime.yml`. The image is NI's LabVIEW
2026 Q1 Linux release, pinned by digest. Its fixture comes from the pinned pylabview
LV2014 example and is SHA256-checked before use. Successful processing would prove
that this runtime can load/compile that input; it would not prove semantic reading,
all-version compatibility, VI Scripting availability, or native LabVIEW 2024.

The official registry lists no LabVIEW 2024 image as of 18 October 2026. A separate
2024 installer/activation path remains to be investigated if native 2024 execution
is needed. Using the newer runtime for this setup check does not select the fallback
or change the owner's goal of all versions.

NI's published [software license agreement](https://www.ni.com/content/dam/web/pdfs/legal/software_license_agreement_en.pdf)
and [Community usage guidance](https://www.ni.com/en/support/documentation/supplemental/20/labview-community-edition-usage-details.html)
must be checked against the owner's actual entitlement and intended cloud use.
The account/license documents and cloud hosting choice are unresolved. No license
purchase, cloud VM purchase or license acceptance has been made.

To complete the environment topic: verify a permitted LabVIEW cloud installation,
its activation and unattended read/automation operation; verify durable account
renewal and real responses from all three cloud providers; then link those results
in the issue resolution. Until then the environment topic remains open, and the
public parser checks must not be presented as full LabVIEW readiness.
