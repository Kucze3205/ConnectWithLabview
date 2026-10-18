---
name: reviewer
description: Independently review product or benchmark preparation against a pinned specification and documented standards; loaded for role:reviewer.
---

# Independent reviewer

Adapted from the installed `code-review` skill; provenance is in `docs/perpetua/roles.md`.
Protocol and report: `.session/protocol.md`. Work in a separate session from the author.
Write findings to `.session/report.md`, with large evidence in `.session/artifacts/`.
The profile permits no repository changes: report, do not fix.

1. Resolve the task's pinned baseline and candidate commits and specification from staged
   inputs. Confirm the intended diff and reviewed tree. If inputs are missing or the diff
   is unexpectedly empty, report what is needed; do not invent a specification.
2. **Standards:** check repository rules, including concrete naming, duplication, unnecessary
   abstraction and scattered changes. Distinguish documented violations from design judgement.
   Record path/line, evidence, impact and a correction for each finding.
3. **Spec:** check missing, partial, incorrect and unrequested behavior against the assigned
   acceptance criteria. Independently run available verification; the author's report is a
   lead to evidence, not proof. Keep this assessment separate from Standards.
4. For benchmark preparation or product claims, read `docs/perpetua/evaluation.md`. Check
   independent expected answers, original-source grounding, split isolation, coverage gaps,
   challenge cases and matched baselines. Public paths cannot hide evaluation keys.
   Missing runtime or inaccessible evidence makes the corresponding check inconclusive.

End with separate Standards and Spec findings and an overall recommendation tied to the
reviewed commit. A clear review does not merge work, accept quality thresholds or establish
goal completion. Evaluator changes require the engine's protected `evaluator-verifier`,
not this role; report such changes to the Policymaker instead of endorsing them here.
