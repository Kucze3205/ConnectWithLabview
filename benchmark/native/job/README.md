# Proposed native inspection job for #169

Design only. No native execution, readiness determination or quality measurement is claimed. This draft requires independent cross-family review before the owner considers installation.

The driver uses the two saved-property VIs explicitly named in [readiness-case.json](../readiness-case.json). It copies no source directory or implicit dependencies into the disposable mount. The pinned readiness case still lacks independently established behaviour and controlled I/O. Dependencies, safe loading and native compatibility remain unverified; missing dependencies must remain failures, not trigger fetching or broader mounts.

## Readiness clause map

Line references identify draft mechanisms, not executed evidence.

| #169 clause | Draft implementation or explicit gap |
| --- | --- |
| Dispatch on one public development VI with independently known behaviour from prepared sources | **Gap: known-behaviour dispatch.** The draft selects two saved-property inputs, whose behaviour has not been independently established. It does not satisfy this opening clause. [native_job.py:190](native_job.py#L190) defines the proposed inspection entry point; no native dispatch evidence exists. |
| Original SHA256 identical before and after, using python3 -I | [native_job.py:243](native_job.py#L243) starts source checks; [validate at native_job.py:88](native_job.py#L88) compares original and disposable-copy hashes. Run the driver with python3 -I -B. No actual native preservation evidence exists. |
| Native properties | **Gap.** [native_job.sh:26](native_job.sh#L26) proposes built-in HTML printing, whose property coverage is unverified. [native_job.py:332](native_job.py#L332) retains requested properties as unavailable, with no invented typed values or native locators. A successful HTML export cannot establish saved version, separate compiled code or debugging flags. |
| Diagram capture with output SHA256 manifest | **Partial design; verified diagram content is a gap.** [native_job.sh:26](native_job.sh#L26) proposes HTML output; diagram inclusion and capture regions require confirmation. [native_job.py:347](native_job.py#L347) inventories collected reports/logs for output-sha256.json; [native_job.py:104](native_job.py#L104) verifies their manifest entries and hashes. The manifest excludes itself and record.json to avoid circular hashes; the record includes the manifest hash. |
| Controlled inputs produce recorded outputs | **Gap retained.** [native_job.py:197](native_job.py#L197) requires the existing controlled-I/O gap and rejects changed I/O design. No RunVI call, connector mapping, vectors, reset/stop procedure, expected result or behaviour claim exists. |
| git status --porcelain shows no source mutation | [native_job.py:243](native_job.py#L243) requires a clean source checkout; [native_job.py:287](native_job.py#L287) starts final status and hash checks. These checks detect mutation; they do not establish that loading is free of side effects. |
| Container networking stays disabled | [native_job.py:267](native_job.py#L267) proposes --network none, --rm, --cpus 2, --memory 8g and a disposable /probe bind mount. No repository, source checkout, credentials or Docker socket is mounted. The image digest and LabVIEW path are checked against labview-runtime.json. Image pulling occurs on the host before the network-disabled run. |
| Separate session compares outputs with independently expected values | **Gap.** [native_job.py:223](native_job.py#L223) retains pending independent comparison and unresolved substantive checks. No independent comparison session or controlled-I/O expectations exist. |
| Compile success alone fails | **Explicit exclusion.** Compilation is neither proposed nor accepted as readiness evidence. [native_job.py:332](native_job.py#L332) leaves native property slots unavailable; missing known behaviour, verified diagram content, controlled I/O and independent comparison remain gaps. Compile success cannot close them. |

## Unverified native interface and safety prerequisites

PrintToSingleFileHtml, -VIPath and -HTMLFilePath for LabVIEW 2026 Q1 Linux are **unverified**. Whether the operation emits a self-contained HTML file, creates companion images, includes a block diagram or exposes requested properties is **unverified**. **PNG companion gap:** native_job.py declares no exact PNG output paths. PNG files are excluded from collection and upload; unexpected companions fail the strict output inventory. A reviewed output design is required before supporting them.

Safe loading without automatic execution/hooks, undeclared dependency resolution, no-save behaviour of printing and CloseLabVIEW, and shutdown success are **unverified**. CloseLabVIEW runs in an EXIT trap with file capture; its failure is logged but currently suppressed. Hash checks cannot replace confirmation of these properties. The job must not be installed for execution until independent review resolves or explicitly blocks these prerequisites. No custom VI, VI Scripting operation, edit, save, build or controlled execution is proposed.

The host bounds pull/run/cleanup to 420/300/20 seconds and removes the container after failure or timeout. CLI output goes to files. Collection accepts regular allowlisted files; symlinks and unexpected outputs cause rejection. Logs retain failure reasons and observed output hashes. Hashes establish inventory integrity only, not native content, correctness or absence of undeclared reads.

## Proposed installation and artifact boundary

1. Obtain independent cross-family review and the owner's outstanding #169 licence, operation, spending and provider-output decisions. Resolve safe-loading and CLI interface gaps before running.
2. After review, the owner copies workflow.proposal.yml to .github/workflows/ under an agreed name. This draft writes nothing under .github/.
3. The proposal stages the pinned public pylavi commit, uses contents: read and persist-credentials: false, and supports workflow_dispatch only. The driver checks each named VI hash before invoking Docker.
4. The owner dispatches only within the authorized scope. [workflow.proposal.yml:31](workflow.proposal.yml#L31) uploads record.json, output-sha256.json, logs/*.log, logs/installed-version.txt and reports/*.html from the driver's native-inspection output directory. VI files and PNG companions are excluded; HTML is the only added file kind.
5. Each collected HTML report is listed with its SHA256 in output-sha256.json. The driver validates collected payloads against that manifest. A separate session must inspect the uploaded substantive content; transport and hashes do not establish diagram capture or native agreement.
6. Independently establish and freeze the missing behaviour, connector identities, dependencies, discriminating vectors, reset/stop/timeout and comparison rules in a later reviewed fixture. This draft never upgrades itself to execute revised I/O. Only separate comparison and the owner's capability-ready confirmation can complete #169.

## Local verification

Run `python3 -I -B benchmark/native/job/native_job.py --self-test`. It exercises synthetic integrity checks only: a valid output manifest is accepted, an HTML entry omitted from the manifest is rejected, and the existing five mutations remain (changed source hash, missing output, extra output, networking other than none, changed disposable-copy hash). This does not execute Docker or LabVIEW or establish native readiness. The current session's actual result is recorded in .session/report.md.
