# Task 27 — orchestrator journal

## Status: blocked on the runner, no work done yet

### What happened
The runner stopped 14 times in a row while a read-only action was pending. No result came back for any of them:
- Read `.session/protocol.md`: 9 attempts
- Read `.session/issue.md`: 2 attempts
- Read `.session/loop-state.json`: 2 attempts
- Glob `.session/**`: 1 attempt
- Grep `.session/protocol.md` (pattern `.`): 1 attempt

So far I have not read the protocol, the issue, the role skill, capabilities or loop state. I have made no plan and run no verification. I have not changed anything outside `journal/`.

### Permission conflict to resolve
The task says to write `.session/report.md`. My role profile only allows writes under `journal/**`. The parent or protocol needs to say whether `.session/report.md` is an exempt output path. Until then the report lives here in the journal.

### How to resume
1. Check that the runner returns results. Start with a small read: Glob `.session/**`.
2. Read these in order: `.session/protocol.md`, `.session/issue.md`, `.session/role/SKILL.md` and its references, `.session/capabilities.json`, `.session/loop-state.json`.
3. Plan the work on branch `task/27` from the issue's acceptance criteria. Delegate any work outside `journal/**` according to the protocol.
4. Run the issue's verification command. Keep its output as evidence whether it passes or fails.
5. Write `.session/report.md` if that is allowed. Otherwise write the report here. Then Finish.
