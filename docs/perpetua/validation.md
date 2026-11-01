# Validating the layered engine

Run from the repository root:

```sh
python3 -m unittest discover -s .github/loop/tests
```

In a copied loop use `-s .github/loop/tests`. The suite never arms a real loop.
`test_template_flow.py` copies the actual shipped template, writes and registers the execution
roles, validates the committed setup baseline, stages the selected shaper, accepts
a work product through the accepted-tree gate, delivers a suggestion to the
Policymaker, activates changes to both layers and checks the change records and rollback.
Git and engine behavior are real; GitHub and provider session outputs are simulated.
`test_activation.py` additionally checks pending, rejected, incomplete and stale
independent evaluator verification and atomic activation of dependent definitions.
In this loop `test_template_flow.py` and the template-only checks are skipped: it is a configured instance,
not the shipped template. Skips are missing checks, not passes.

Use `python3` on Linux if that is the interpreter name. The host requirements of the
Linux tests (packages, kernel settings, the pinned CLI) are the install step of
[`engine-tests.yml`](https://github.com/Kucze3205/Perpetua/blob/main/.github/workflows/engine-tests.yml); nothing else lists them.
Windows skips the tests that need a POSIX shell, the symlink cases and the kernel-isolation tests, so a Windows run
does not prove isolation. The script boundary tests must execute on Linux; an environment skip is an outstanding check, not proof.
The opt-in live provider procedure is below. A passing fake CLI or a live API error
does not establish the real provider guarantee: the pinned CLI must successfully
call its model while subprocess probes demonstrate the network restrictions.

`test_agent_chain.py` runs the real `agent.sh` with a stand-in CLI. `PlainPromptTest` needs a
POSIX shell and checks that a prompt over 128 KiB reaches the CLI whole, through stdin.

`test_routed_chain.py` is the same chain for the routed runtime that this loop actually runs: stage, executor
admission, `runtime_entry.py` (real broker, git checkpoint and `provider_adapter.request`), epilogue. The stand-in is a
`claude` executable that answers `Read`, `Write` and `Finish`; GitHub's state API and release assets are plain files. It requires `turns` of at least 1,
the written file on `task/N`, a prompt over 128 KiB reaching the CLI through stdin, no `origin` in the executor
repository and a frozen `done` report. It needs a POSIX shell and runs unprivileged in `environment.yml`. Both iteration 0
failures (a checkpoint that pushed to a missing `origin`, a prompt in argv) make it fail. **Its result on the commit to be
armed is a precondition of `AUTOPILOT=on`**, next to the full Linux suite.

Record the commit, command, platform, test count and skips for each validation run.
Report provider quota/authentication or missing kernel support separately from
test failures. Require both the full Linux regressions and the opted-in live
provider boundary check before claiming all ADR-0004 validation is complete.

The regression suite also covers engine ownership and local versioning (ADR-0001),
credential-free agent sessions (ADR-0002), the accepted-tree change gate without
an engine-owned accepted measurement (ADR-0003), limits, owner requests and rollback
triggers. Validation supplies no migration or reconfiguration procedure. Repeating
setup as a review is separate work.
Before arming, also run `python3 .github/loop/setup_roles.py validate --baseline setup-baseline` against the tagged
commit (see [setup decisions](setup-decisions.md)).

## Session boundary checks

The [session boundary](session-boundary.md) defines what these checks exercise. In the commands below use
`engine/.github/loop/tests` in the plugin repository or `.github/loop/tests` in a copied loop.

Run `python3 -m unittest discover -s .github/loop/tests -p test_security.py -v` for the tool allowlist and
`-p test_static.py` for the workflow properties: the session job has `permissions: {}` and nothing mentions the removed
sandbox. No provider, native CLI or actual GitHub credential is needed; the engine tests workflow installs only
`python3-yaml`.

## Deployment checks

The default suite uses an in-memory GitHub and real temporary Git repositories.
It does not validate live GitHub workflow execution, release operations,
assignment or cancellation. Exercise those in a trial loop when a change needs
that evidence; documentation edits do not require arming a real loop.

`E2E_CAPTURE=on` (repository variable, off by default) makes `session.yml` upload
each whole `.session/`, staged contract, raw stream and checkout listing as
`capture-<iteration>-<issue>.tgz` on release `e2e-capture`. These include session
inputs; real loops leave capture off. Template-only tests in `test_static.py`
skip in a copied loop.
