# Policymaker handoff to the shaper

Written by Policymaker #471 at the start of iteration 0092 (2026-11-12). You cannot read `policy/`; this file
carries what the Policymaker learned while it ordered every task (iterations 0017-0091, no shaper). Your own
`journal/working-memory.md` supersedes this file wherever it is newer. Statements here are evidence to check,
not orders: the direction of the iteration is yours.

## Where the loop stands
- The owner restored the orchestrator as shaper on 2026-11-12 (commit cfaf996). `journal/working-memory.md` is
  still the empty template; you write its first real content.
- Goal priority: deliver the proof of concept (goal section "Proof of concept"). Benchmark work that the POC does
  not need waits until the POC is delivered. The loop does not wait for an owner answer after delivery.
- The POC is the one exception to "method first, then implementation". POC code lives in `docs/research/poc/`
  (the researcher's write path). It is not product code: `src/` stays untouched until the normal route.
- Delivery = files + report + a short instruction for the owner's manual check in LabVIEW. If the POC cannot
  work, deliver the evidence and the possible exits; the loop does not change the goal itself.

## POC thread (records 0090, 0091)
- #465 (step 1, tag `iter/0090/465`): `pylavi/tests/add.vi` (sha256 cf4b1f56...), RSRC container, save version
  21008000, BDHb zlib payload -> 842-byte heap.
- #468 (step 2, merged 0f35a16, codex GPT, 48 turns): `docs/research/poc/inspect_vi.py` + `verify_poc.py`;
  full tag tree of add.vi (162 entries) and three other pylavi fixtures; grammar from pinned pylabview
  `LVheap.py`. README ends `heap-decode: yes`, `poc-feasibility: partial`. Read `docs/research/poc/README.md`
  first; do not re-order container, decompression or framing work.
- Not done yet: (1) no meaning for primitive ids (`primIndex` 103, `primResID` 1050; 103 -> 104 is only a
  syntactic experiment); (2) no edited VI on disk (zlib re-encode, lengths, RSRC offsets); (3) integrity and
  cache rules after an edit; (4) the owner instruction; (5) the "agent that never saw the VI" demonstration: the
  describing session should get only the tool and a VI whose analysis is not already in the README.
- Hypotheses of the Policymaker, none measured:
  - A. A primitive-name table may exist in public sources (pinned pylabview or related projects).
    `docs/research/poc/source-provenance.json` shows how #468 retrieved sources.
  - B. A logic change that needs no primitive identity is cheaper to specify and to check: change a constant
    (numeric, Boolean or string) in a VI that has one. add.vi has no constant; actor-framework (about 800
    LabVIEW files in the prepared environment) probably has many. The owner check is then "the value is X".
  - C. Integrity: the README lists BDPW rules as a gap. My unverified recollection is that pylabview's BDPW
    block recomputes a hash that covers the block-diagram heap; if so, an edit without that hash may not open.
    `docs/research/poc/LVparts-source.txt` is already saved; check it before the edit step.
  - D. Stale compiled code: add.vi stores compiled code in the file. LabVIEW may run old code unless the file
    marks a recompile. A fixture with separated compiled code (`empty_separate_code.vi` is one) may avoid this.
  - E. An owner request for a few labelled fixtures saved in LabVIEW is possible (session protocol, "Requests
    to the owner"). The POC must not wait for it: plan work that is ready without it.
- Prepared public sources: only `actor-framework`, `pylavi`, `readiness.json` under `$LABVIEW_ENVIRONMENT`
  (read-only; sometimes absent in a session, so a task must say what to do then). No LabVIEW runs in the loop.

## Benchmark thread (paused until the POC is delivered)
- Preparation index on main: `benchmark/preparation.json`, 74 pinned references; the policy evaluator check
  reports errors [], missing [], benchmark_ready false, benchmark_executed false, tool_quality null.
  Seven milestones have reviewed-level labels (design or scorer level). Nothing was executed; quality is unmeasured.
- Paused items: re-review of the split allocator completion fix (#446, `benchmark/scripts/split_allocate.py`,
  not pinned); native evidence (capability #169, waiting since 2026-11-04); write-task extension of the method
  (new in the goal); owner method assessment (#430 was declined as not planned when the goal changed).
- Do not repeat: gap maps #282/#330/#400, lineage batches (stopped: no allocation effect), store-record reviews.
- All-version effort estimate exists: `docs/research/0002-delivery.md`. Present it before any LabVIEW 2024
  fallback choice; do not re-order the research. It does not cover writing yet.

## Task-writing lessons (measured, with the session that showed it)
- Never tell a task to `git commit`; the parent commits (#206). No `git diff`/`git status` acceptance checks (#207, #380).
- `## Verification` runs again in an engine job without `LABVIEW_ENVIRONMENT` and without `.session/report.md`
  (#184, #232): one plain `python3` command that needs neither.
- Reviewer tasks start from main (`start_branch` null) and produce a report only; from a task branch they end
  `blocked` (#208, #210). Staging a large report export crashed reviewers at 0 turns (#365, #370).
- Codex sessions often carry most of the work and hit the 800k input ceiling (#228, #258, #465). Put a read
  budget in every task: no whole large JSON reads, at most about 80 lines of output per command, report early.
- Give even small tasks `max_turns` >= 25; 8-15 turn tasks kept ending `partial` (#215, #220, #250).
- A task that edits a file pinned in `benchmark/preparation.json` must re-pin it in the same task (#312).
- Unmerged work of task N is kept as tag `iter/NNNN/N`; `start_branch: task/N` resumes it (#467 -> #468).
- Do not trust model labels for review independence; read the `models` block of the record. Reviewer routes
  often fall to GPT; record a same-family review as a limit instead of repeating it.
- A wake or retry that re-submits finished orders wastes a whole pass (iteration 0055: 8 tasks, 2.7M input).

## Housekeeping found
- `docs/research/poc/__pycache__/inspect_vi.cpython-312.pyc` is tracked although `.gitignore` excludes it;
  let the next researcher task that touches the folder delete it.
