# Policy working memory

Considered: iteration records 0000-0091 and the owner commit cfaf996. Rewritten and compressed by Policymaker #471 at
the start of iteration 0092 (2026-11-12). The earlier per-iteration notes (0024-0091, 110 KB) are in git:
`git show 2b6f6870:policy/working-memory.md` (sha256 68d353d1...). Read a section there only when a decision is reconsidered.
History: `.session/history/manifest.json`; records `.session/history/records/<nnnn>.json`; session documents
`.session/history/sessions/<issue>/` (list with python glob, not Glob).

## Organization (changed 2026-11-12)
- Owner commit cfaf996 set `shaper: orchestrator` (routes: Fable 5.2, Opus 5.5, codex) and put Fable 5.2 first for the
  Policymaker. Reason in params.yml: iterations 0087-0089 failed with no shaper and no orders after input_budget exhaustion.
  The owner comment says: keep this order. `every_iterations: 1` stays while task creation is restored.
- With a shaper the Policymaker orders ONLY `evaluator` and `audit` (task-graph.md:36); other orders are refused whole.
  An iteration no longer fails when the Policymaker writes no orders. It fails when the shaper writes no valid
  `.session/tasks.json` (engine.md:84-85), and then `execution/` and `policy/` roll back.
- The shaper cannot read `policy/`. Its inputs: loop state, `.session/capabilities.json`, `journal/working-memory.md`,
  its skill folder, `.session/history/`.
- #471 changes (iteration 0092):
  - `execution/roles/orchestrator/SKILL.md` rewritten: `startup` list (state, capabilities, journal memory, handoff);
    section "Write the graph first" (valid tasks.json by about the 12th tool call; iterations 0003-0005 failed at the turn cap
    with no graph, reset-2026-10-28.md:56); section "Current priority: the proof of concept"; one memory file
    `journal/working-memory.md` with four sections replaces per-iteration `journal/NNNN.md`; stale paths fixed
    (`iterations/NNNN.json` -> `.session/history/records/`).
  - `execution/roles/orchestrator/references/handoff.md` (new, 6.4 KB): loop state, POC thread with five open items and
    hypotheses A-E, paused benchmark thread, task-writing lessons with session numbers. Staged as
    `.session/role/references/handoff.md`.
  - `execution/profiles.yml`: orchestrator `max_turns` 30 -> 45 (60 min, medium unchanged). Reason: 30 turns ended with no
    graph three times; the graph-first rule is the main fix, the extra turns are margin for memory and report.
  - `policy/layer-rules.py` on the new definitions: `{"errors": []}`.
- Expected effects, to check in record 0092: shaper session `done`; `tasks` >= 1; `journal/working-memory.md` has the four
  sections; shaper `startup.tokens` shows the handoff was read (about 12k tokens of documents); the ordered task
  advances the POC and does not repeat #465/#468.
- If the shaper fails: `rollbacks` in the loop state changes and this skill and handoff vanish. Read the shaper's
  record first (turns, models, whether tasks.json existed). One failure -> re-apply with a tighter graph-first rule. Two
  failures -> propose `shaper: null` with small Policymaker orders, or a script shaper, and tell the owner why.

## Open questions
- Cost of a Policymaker session at every iteration with a shaper (#467: 957k cache read, 19 turns). After two shaper
  iterations in a row that close with tasks, consider `every_iterations` 3 and tell the owner (the owner set 1).
- Is the `startup` list of an execution skill honoured for the shaper? Check record 0092 startup tokens.
- Can the orchestrator write `.session/report.md` and `.session/requests.json`? (reset lesson 6 said its profile allowed
  only `journal/**`; tool_broker.py:22 lists both as session outputs.) Check its report in 0092.
- Loop state `owner_requests.open` is now []. Capability #169 (native jobs, waiting since 2026-11-04) is not listed; its
  state is unknown. Do not assume it is ready or closed.
- No audit report exists (`audit_report: null`); audits #43/#55 crashed. Order an audit only with a concrete question, for
  example quota per accepted result of the shaper organization after 3 iterations.

## Goal state
- Goal changed about iteration 0087: adds writing ("Pisanie") and a POC before further benchmark preparation.
  Owner request #430 (method assessment) was DECLINED as not planned. A new method request needs write tasks in the
  method first. `policy/proposals/method-acceptance-draft.md` is the old text; reuse only as a base.
- POC thread: #465 (step 1, tag iter/0090/465) container + save version 21008000 of pylavi add.vi; #468 (step 2,
  merged 0f35a16, codex 48 turns, accepted) `docs/research/poc/inspect_vi.py`, `verify_poc.py`, full BDHb tag tree
  (162 entries / 842 bytes), README lines `heap-decode: yes`, `poc-feasibility: partial`. Open: primitive meaning
  (primIndex 103, primResID 1050), no edited file on disk, integrity/cache rules, owner instruction, unseen-VI
  demonstration. Details and hypotheses: the handoff file. The shaper owns the next step.
- Benchmark thread (paused until POC delivery). Main: preparation.json 99069d8d..., preparation-status.json 8f64e982...,
  evaluator `python3 policy/evaluator/evaluate.py --check` -> errors [], missing [], 74 refs, ready/executed false.
  Milestones: baseline/split design-reviewed, challenges scorer-reviewed, coverage/oracle/sources/tasks reviewed.
  Store record #379 reviewed (#431) and pinned. Unpinned, review pending: `benchmark/split/allocation.synthetic.json`
  70d94d28... and `benchmark/scripts/split_allocate.py` 55c236ad... (fix #446 of review #443 finding 1; fix round 1 used).
  Nothing was executed; quality is unmeasured; reader implementation is gated on method acceptance.
- All-version estimate: docs/research/0002-delivery.md (89-264 d all versions vs 33-99 d 2024-only; strict 2024 excludes
  413 of 415 RSRC files). Present before any fallback choice; it does not cover writing yet. Do not re-order it.
- Do not repeat: gap maps #282/#330/#400; reviews #403/#408/#409/#415/#421/#427/#431/#443; lineage batches (stopped
  in 0066: no allocation effect; rules kept in policy/proposals/lineage-pilot-359.json); old store-record searches.
- `policy/proposals/store-readiness.yml` equals the installed workflow revision 4 (27b365ec...); it can be deleted.

## Session mechanics (lessons, each cost at least one failed session)
- Finish rejects `.session/report.md` unless it begins with `<!-- session-report -->` and a yaml block whose `status`
  equals Finish.status (#316).
- Files under `.session/` vanished mid-session several times (provider switch; #368, #402, #429). Re-check that the
  report (and orders, if any) exist immediately before Finish.
- In this harness `git status` and `git diff` show nothing for files written in the session (#471). Verify written files
  by reading them (bytes, sha256), not by git.
- A Write with empty `text` truncates the file (#471 did this once to the orchestrator skill and rewrote it). Check the
  byte count after each Write of a managed file.
- Two Policymaker sessions in a row that do not end `done` roll back both managed roots (0041, 0051, 0086-0089).
  Keep sessions short: decide, write, verify, report. Large reads caused the input_budget partials.
- `wake: true` only when the next pass orders different work (0055 wasted 8 tasks, 2.7M input).
- If the Policymaker orders goal work again (shaper null): write orders.json first and parse-check it; never ask a task
  to `git commit`; no git diff/status acceptance; Verification is one plain python3 command that needs neither
  LABVIEW_ENVIRONMENT nor `.session/report.md`; reviewers start from main and report only; max_turns >= 25; a task that
  edits a pinned file re-pins it; unmerged work is tag `iter/NNNN/N` and `start_branch: task/N` resumes it; for
  mechanical landings write a hash-gated idempotent script in `execution/scripts/`, dry-run it twice on a copy, order
  one low-effort run, delete it afterwards. The same lessons are in the shaper handoff.
- Both preparation JSON files are `json.dumps(indent=2, sort_keys=True)` + newline; a changed pinned file needs every
  reference to preparation-status.json re-pinned. `lineage.py --check` needs LABVIEW_ENVIRONMENT.

## Model and resource evidence
- Do not trust report/startup model labels; read each record's `models` block. Sessions that start on Sonnet often run
  mostly on codex gpt-6.1-sol or copilot gpt-5.6-luna. Reviewer routes fell to GPT in most reviews; the `opus` alias did
  not hold (#221, #232, #241, #247). A same-family review is recorded as a limit, not repeated.
- Codex sessions hit the 800k unique-input ceiling often (#228, #258, #287, #465). #468 used 4.38M input with 4.24M
  cache read in 48 turns and finished: long codex sessions are possible when cache reads are high.
- No measured subscription-quota figure exists. Cache and input-budget accounting are not quota use. No routing change
  without measurements; the owner's Fable-first order for Policymaker and orchestrator stays.

## Rules to preserve
- Read docs/perpetua/evaluation.md before reader planning or implementation; accepted-limits.md before private data,
  disclosure, publication or spending. Optional access never blocks an iteration.
- The POC is not the product and not quality evidence. No readiness, threshold, gate or fallback choice is implied by
  any preparation result. Missing coverage and native answers stay explicit in every report.
- Requests: `.github/loop/session-protocol.md` ("Requests to the owner"); owner texts in Simplified Technical English.
- Evaluator path is `policy/evaluator/evaluate.py`; change it only through an `evaluator` order plus verifier.

## Next Policymaker
1. Read record 0092: shaper status, tasks, tokens, `rollbacks`. Check the expected effects above.
2. Read `journal/working-memory.md` (the shaper's memory) instead of re-deriving the execution state.
3. Decide pending shaper suggestions (`suggestions` in the loop state) in `policy/suggestion-decisions.json`.
4. Change the skill, handoff or limits only from evidence in that record. When the journal memory covers the handoff,
   shrink the handoff to the task-writing lessons and remove it from the shaper's `startup`.
