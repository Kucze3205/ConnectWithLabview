# Proposed native inspection job for #169

Design only. Author model family: OpenAI GPT-6.1 (Codex, gpt-6.1-sol). No Docker or LabVIEW execution, readiness determination or quality measurement was performed. This draft requires independent cross-family review before the owner considers installation. The startup diagnostic names another model; it is not the identity of this drafting candidate.

The driver uses the two saved-property VIs explicitly named in [readiness-case.json](../readiness-case.json), not the older add.vi candidate in recipes.json. It copies no source directory or implicit dependencies into the disposable mount. The pinned readiness case still lacks independently established behaviour and controlled I/O. Dependencies, safe loading and native compatibility remain unverified; missing dependencies must remain failures, not trigger fetching or broader mounts.

## Readiness clause map

Line references below refer to the proposed files in this directory. They identify draft mechanisms, not executed evidence.

| #169 clause | Draft implementation or explicit gap |
| --- | --- |
| Original SHA256 identical before and after, using python3 -I | [native_job.py:219](native_job.py#L219) starts source checks; lines 222–233 hash declared originals and copies; lines 263–276 rehash and validate; line 88 defines rejecting comparisons. Run the driver with python3 -I -B. No actual native preservation evidence exists. |
| Native properties | **Gap.** [native_job.sh:26](native_job.sh#L26) proposes built-in HTML printing, whose property coverage is unverified. [native_job.py:308](native_job.py#L308) retains every requested property as unavailable, with no invented typed values or native locators. A successful HTML export cannot establish saved version, separate compiled code or debugging flags. |
| Diagram capture with output SHA256 manifest | **Partial design; capture content is a gap.** [native_job.sh:26](native_job.sh#L26) proposes HTML output; actual diagram inclusion and capture regions require confirmation. [native_job.py:324](native_job.py#L324) hashes collected reports and logs. The manifest excludes itself and record.json to avoid circular hashes; the record includes the manifest hash. |
| Controlled inputs produce recorded outputs | **Gap retained.** readiness-case.json declares vectors null and status gap. [native_job.py:173](native_job.py#L173) rejects changed I/O design rather than executing it. The template's controlled_io fields remain unpopulated. There is no RunVI call, invented connector map, expected result or behaviour claim. |
| git status --porcelain shows no source mutation | [native_job.py:219](native_job.py#L219) requires a clean source checkout; lines 263–276 compare the final status and hashes; line 296 records both statuses. Disposable-copy hashes are also compared. These checks detect mutation; they do not establish that loading is free of side effects. |
| Container networking disabled | [native_job.py:243](native_job.py#L243) uses --network none, --rm, --cpus 2, --memory 8g and a disposable /probe bind mount, matching the named runtime pattern. No repository, source checkout, credentials or Docker socket is mounted. The image digest and LabVIEW path are checked against labview-runtime.json. Image pulling occurs on the host before the network-disabled run. |
| Separate session compares outputs with independently expected values | **Gap.** [native_job.py:199](native_job.py#L199) retains pending independent comparison and unresolved substantive checks. The author cannot supply independent approval. No comparison session or controlled-I/O expectations exist. |

## Unverified native interface and safety prerequisites

Repository evidence confirms only the existing runtime pattern: LabVIEWCLI, CloseLabVIEW, -LabVIEWPath, -Headless, -LogToConsole TRUE and -LogFilePath were used by labview_runtime.sh. It does not confirm the proposed PrintToSingleFileHtml operation, -VIPath or -HTMLFilePath for LabVIEW 2026 Q1 Linux: all are **unverified**. Whether that operation emits one self-contained HTML file, creates companion image files, includes a block diagram or exposes any requested property is **unverified**. Unexpected companion files currently fail the strict output inventory; the allowlist must be reviewed before supporting them.

Safe loading without automatic execution/hooks, undeclared dependency resolution, no-save behaviour of printing and CloseLabVIEW, and shutdown success are **unverified**. CloseLabVIEW runs in an EXIT trap with file capture; its failure is logged but currently suppressed, following the existing runtime pattern. Hash checks cannot replace confirmation of those safety properties. The job must not be installed for execution until the independent review resolves or explicitly blocks these prerequisites. No custom VI, VI Scripting operation, edit, save, build or controlled execution is proposed.

The host bounds pull/run/cleanup to 420/300/20 seconds and removes the container after failure or timeout. Captured CLI output goes to files, never pipes. Collection accepts only regular allowlisted files; symlinks and unexpected outputs cause rejection. Logs record failure reasons and observed output hashes. Hashes establish inventory integrity only; they cannot establish native content, correctness or absence of undeclared reads.

## Proposed installation and artifact boundary

1. Obtain the independent review and the owner's outstanding #169 licence, operation, spending and provider-output decisions. Resolve safe-loading and CLI interface gaps before running.
2. After review, the owner copies workflow.proposal.yml to .github/workflows/ under an agreed name. This draft writes nothing under .github/.
3. The proposal stages the pinned public pylavi commit, uses contents: read and persist-credentials: false, and supports workflow_dispatch only. The driver verifies each named VI hash before invoking Docker. No source provenance is inferred from a filename.
4. The owner dispatches the installed workflow only within the authorized scope and reviews the record, manifest and logs. The workflow uploads exactly those categories and no VI files.
5. **Artifact-transfer gap:** native HTML reports are collected and hashed on the disposable runner but deliberately excluded from the proposed upload allowlist. A separate session cannot substantively inspect those reports through this artifact. The owner/reviewer must resolve an authorized report-transfer design before claiming diagram capture or native comparison; a hash in record.json is insufficient.
6. Independently establish and freeze the missing behaviour, connector identities, dependencies, discriminating vectors, reset/stop/timeout and comparison rules in a later reviewed fixture. This draft never upgrades itself to execute revised I/O. Only a separate comparison and the owner's capability-ready confirmation can complete #169.

## Local verification

`python3 -I -B benchmark/native/job/native_job.py --self-test` completed with exit 0: a synthetic baseline was accepted and changed source hash, missing output, extra output, networking other than none, and changed disposable-copy hash were rejected. These are integrity checks on synthetic files, not native tests. `bash -n benchmark/native/job/native_job.sh` and `python3 -I -B policy/evaluator/evaluate.py --check` also completed with exit 0. The evaluator reported benchmark_executed false, benchmark_ready false and tool_quality null. No pinned design or evidence index was changed.
