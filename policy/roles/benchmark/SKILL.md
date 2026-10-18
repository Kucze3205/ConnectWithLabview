---
name: benchmark
description: Prepare the LabVIEW verification protocol, development fixtures and readiness evidence before product implementation; loaded for role:benchmark.
---

# Benchmark preparation

This project-specific skill adapts the installed skill-creator grader's evidence and
assertion-critique method; provenance is in `docs/perpetua/roles.md`.
It follows `docs/perpetua/evaluation.md`; read that contract and
`goal/goal.md` before designing cases. Protocol and report: `.session/protocol.md`.
The existing evaluator verifier supplies the independent readiness checks, in another session.

Write only `benchmark/`: protocol, provenance and coverage records, development cases,
repeatable preparation scripts and the optional preparation evidence index. Keep large
originals in `.session/artifacts/` with hashes and source records. Preserve originals before
conversion. Reuse the prepared read-only sources as described in `docs/perpetua/environment.md`.

For the assigned part of the protocol:

1. State the question, expected observable behavior and verifiable location in the original
   artifact. Establish expected answers independently of the reader being tested. Record
   the method, evidence and uncertainties; unavailable native evidence stays unavailable.
2. Account for artifact families, versions, dependencies and inaccessible diagrams. Keep
   unsupported or unexecuted cases visible. The first corpus does not redefine the goal.
3. Specify project/family splits, duplicate checks and how evaluation cases and answer keys
   will be withheld from the evaluated agent. The repository and its history are public:
   do not commit withheld cases or keys here, including under `policy/evaluator/`.
   Design an access boundary and request missing capability before claiming isolation.
4. Specify matched no-tool and tool baselines, pinned model/prompt/budget, repeats,
   uncertainty and separate reading-fidelity, answer-correctness and source-grounding checks.
5. Exercise the method with wrong answers, wrong source locations, a constant exporter and
   an unsupported case. Link executed evidence and explicit failures. Independently derived
   expectations must distinguish correct and deliberately wrong outputs.

Inspect actual outputs, rather than relying on the execution report. For each expectation,
cite evidence of the substantive result; correct filenames and valid hashes alone do not
pass. Extract and verify implicit factual, process and quality claims. Flag unverifiable
claims and assertions that would also pass a clearly wrong output, or important outcomes
that no assertion checks. These checks adapt the grader instructions; they do not grant
this author independent approval of their own method.

Completion means the assigned evidence is reproducible, not that the benchmark is ready.
Report which prerequisites remain missing. Request a separate reviewer session for the
preparation evidence and a Policymaker-ordered evaluator change when executable scoring is
needed. Only the evaluator role changes `policy/evaluator/`; its independent verifier must
pass before that change takes effect. Product implementation waits for independent method
review and owner acceptance of the pinned protocol and evidence. Numeric thresholds,
scope changes and the goal gate remain owner decisions.
