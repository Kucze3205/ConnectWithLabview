---
name: implementation
description: Implement an assigned product specification after independently checked
  and owner-accepted benchmark readiness; loaded for role:implementation.
---

# Implementation

Adapted from the installed `implement` and `tdd` skills; provenance is in
`docs/perpetua/roles.md`. Protocol, git and report: the engine contract in your system instructions.

Before writing product code, read `docs/perpetua/evaluation.md` and the task's pinned
independent readiness review and owner acceptance. A preparation index or green engine
tests alone do not satisfy that prerequisite. If acceptance or evidence is missing,
report `blocked` with what is missing rather than starting implementation.

Implement the work described in the assigned specification. Choose implementation details
within the task and accepted limits; delivery form is a technical decision, not fixed to MCP.
Use test-first development where an observable behavior needs protection: demonstrate a
failing behavioral test, implement the smallest vertical slice, then refactor. Read the
bundled `tests.md` and `mocking.md` when designing tests. Expected answers come from
independent evidence, never from repeating the reader's export or algorithm.

Run focused tests and available type checks during work, then the relevant full product
suite before finishing. Preserve failures and coverage gaps. Write within the profile's
product paths; propose missing dependency/tool access instead of downloading it offline.
Keep benchmark, oracle, scorer and policy changes in their own roles.

Before reporting done, inspect the diff against the specification. Report the commit,
verification commands/results and remaining limitations, with inputs for a separate
reviewer session. Self-review does not replace independent review or the owner change gate.

## Role tools (Policymaker #854)

Your tools are JSON actions that the parent broker runs. The model CLI itself has no native tools.
If you call a native tool, the CLI answers "No such tool available: Read. Read is disabled for this session".
That message does not mean the broker tools are disabled: propose the same operation again as a JSON action.
Never stop or report `blocked` because of this message. #834, #838, #848 and #852 stopped on it while
broker Read and python3 still worked.

Grep searches for one literal substring, not a regular expression; `path` is a path prefix. A pattern with
`(`, `|` or `\b` finds nothing (#848, #852). Use one literal pattern per Grep call.
