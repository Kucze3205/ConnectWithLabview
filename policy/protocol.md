# Work rules

These work rules are part of policy: the rules and artifacts in `policy/` maintained
by the Policymaker to govern the implementation layer. The engine's session contract
takes precedence.

Read the whole task and the files named in its context budget. Start from named evidence;
expand the investigation when the task needs it. When measuring or researching, report the
finding before proposing a fix. Keep commits small and commit progress before the session ends.

Keep the report concise; link detailed evidence and explain what should happen next.

Before planning or implementing the LabVIEW reader, follow `docs/perpetua/evaluation.md`.
Prepare the repeatable verification method first. Product implementation waits until an independent review
has checked that method and the owner has accepted the pinned protocol and evidence through the existing change gate.
An evidence index, a green engine test suite or a functioning export does not establish benchmark readiness.
Keep missing coverage and unmeasured quality explicit in every evaluation report.

Aim for about 15 lines of report prose: what changed and why, or exactly what failed.
Use `## Discoveries` for findings outside the task, one sentence and evidence link each.
For unfinished work include `## What next`: committed SHA, the next step, and what
the next cold session should avoid repeating. Put lengthy evidence in linked files.
