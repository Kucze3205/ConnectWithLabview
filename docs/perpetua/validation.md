# Validating the layered engine

Run from the repository root:

```sh
python3 -m unittest discover -s .github/loop/tests
```

The suite never arms a real loop. The evidence for this loop's migration is the Linux Actions run recorded in
ticket M4 (#15): 415 tests, 18 skipped (3 environmental provider/network checks, tracked in #24, and 15 that apply
only to the plugin template). Skips are missing checks, not passes. `environment.yml` runs `test_executor_boundary`
under `sudo` and the other modules unprivileged.
`test_template_flow.py` is written for the plugin's inactive template; in this loop it is skipped. It copies the inactive template, explicitly installs
roles, validates the committed setup baseline, stages the selected shaper, accepts
a work product through the accepted-tree gate, delivers a suggestion to the
Policymaker, activates changes to both layers and checks receipts and rollback.
Git and engine behavior are real; GitHub and provider session outputs are simulated.
`test_activation.py` additionally checks pending, rejected, incomplete and stale
independent evaluator verification and atomic activation of dependent definitions.

Run the full suite on supported Linux hosts with bubblewrap and namespace/seccomp
support. Windows checks do not prove kernel isolation. The script and model boundary
tests must execute on Linux; an environment skip is an outstanding check, not proof.
Use the prerequisites and opt-in live provider procedure in
[session contracts](session-contract.md). A passing fake CLI or a live API error
does not establish the real provider guarantee: the pinned CLI must successfully
call its model while subprocess probes demonstrate denied policy/history/host
reads and the appropriate network restrictions.

`test_agent_chain.py` runs the real `agent.sh` with a stand-in CLI. `PlainPromptTest` needs a
POSIX shell and checks that a prompt over 128 KiB reaches the CLI whole, through stdin. `ExecutorChainTest`
needs Linux, bubblewrap and a C compiler (the boundary runs only a native CLI, so the stand-in is built
from C). It walks stage, executor admission, the isolated CLI, checkpoint and epilogue for an
execution-layer role and requires a completed session (`turns` of at least 1), an admitted work product and
no `origin` remote in the executor repository. Without its requirements it is skipped with the reason
printed; a skip is an outstanding check, never a pass.

`test_routed_chain.py` is the same chain for the routed runtime that this loop actually runs: stage, executor
admission, `runtime_entry.py` (real broker, git checkpoint and `provider_adapter.request`), epilogue. The stand-in is a
`claude` executable that answers `Read`, `Write` and `Finish`; GitHub's state API and release assets are plain files and
the bubblewrap wrapper is removed (`test_model_boundary.py` covers the namespace). It requires `turns` of at least 1,
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
triggers. Validation supplies no migration or reconfiguration procedure. Repeating setup as a review is separate work.
Before arming, also run `python3 .github/loop/setup_roles.py validate --baseline setup-baseline` against the tagged commit (see [setup decisions](setup-decisions.md)).
