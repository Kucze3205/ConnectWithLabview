# Shaper reference: task-writing lessons and paused threads

Updated by Policymaker #475 for iteration 0093. Read only when needed; `journal/working-memory.md` carries the
execution state and supersedes this reference. Earlier handoff: accepted change #471, record 0092, commit 5268784.

## Latest result to carry into memory
- Record 0092: shaper #472 finished in 19 turns, created one task and saved all four memory sections.
- Accepted researcher #473: `docs/research/poc/edit-readiness.md` and `.json`, verdict **partial**. Eight VIs were
  inspected. No supported semantic edit was established. Do not order a disk edit from this evidence.
- Exact blockers: primitive identity/replacement contract; DTHP/VCTP type resolution and ConstValue encoding;
  unexplained BDPW chunks; compiled-cache invalidation. No edited VI or runtime result exists.
- Read the result and its two exits before choosing the next task: a bounded missing-source investigation or
  documented unsuccessful POC delivery. Controlled fixtures require verified availability; do not create a waiting task.
  Avoid another broad corpus search. The cold-agent demonstration remains outstanding.
- POC delivery, including unsuccessful delivery with evidence and possible exits, precedes unrelated benchmark work.
  No session can run LabVIEW. Owner silence does not accept a method or establish POC success.

## Paused-thread pointers
- `benchmark/preparation.json`: 74 references, not executed; quality unmeasured. See policy-era findings in record 0091
  if reconsidering details. Split fix #446 (`benchmark/scripts/split_allocate.py`) needs re-review before pinning.
- Capability #169 availability is unknown; check current readiness before ordering native-dependent work.
- Method assessment #430 was declined as not planned. The goal now requires write tasks in the method before writing
  implementation. Read `docs/perpetua/evaluation.md` before resuming benchmark/product planning.
- `docs/research/0002-delivery.md` estimates version effort but omits writing. Reconcile before any 2024 fallback choice.
- Do not repeat gap maps #282/#330/#400, lineage batches without allocation effect, or store-record reviews.

## Task-writing lessons
- Never ask a task to `git commit`; the parent commits (#206). No git diff/status acceptance checks (#207, #380).
- Verification runs again without `LABVIEW_ENVIRONMENT` or `.session/report.md` (#184, #232): one plain python3 command.
- Reviewers start from main (`start_branch: null`) and report only (#208, #210). Large report exports caused
  zero-turn failures (#365, #370).
- Give tasks a bounded read budget, short command output and early saved findings. Codex input-limit failures:
  #228, #258, #465. Even small tasks need at least 25 turns (#215, #220, #250).
- Editing a file pinned in `benchmark/preparation.json` requires re-pinning it in the same task (#312).
- Unmerged task N is saved at `iter/NNNN/N`; `start_branch: task/N` resumes it (#467 -> #468).
- Use record `models` blocks to assess review independence. Record same-family review as a limit; do not repeat it.
- A wake/retry must not resubmit finished work (iteration 0055: eight tasks, 2.7M input).
