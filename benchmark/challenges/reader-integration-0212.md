# Reader / probes / scorer integration gap (reader-integration-0212)

Measurement only. No file other than this one was changed. No LabVIEW behaviour is claimed. `benchmark_executed` stays false and benchmark readiness stays false. Not re-surveyed, cited: `next-gap-0202.md`, `gap-0160.md`, `scorer-probe-0164.md`.
Reading limits: `benchmark/README.md` does not exist; the README cited as `README.md:N` in next-gap-0202 is `benchmark/challenges/README.md`. I read score.py, run_record.py, runner_contract.py and the other scripts only at the signature/docstring/`main` ranges named below, not whole.

## Requirements

Line numbers: `EV` = `docs/perpetua/evaluation.md` (line numbers taken from `next-gap-0202.md`, not recounted), `P` = `benchmark/protocol.md`.
- Reader attempts: paired runs of each task without and with the reader (P:79). The reader is a pinned tool with commit, configuration and tool schema in a run manifest (P:80).
- Fresh-session runs: every repetition runs in a fresh session with no prior answers, key access or shared memory; requests, responses, tool calls, model ids, timestamps, token usage, errors and scorer records are preserved (P:83). Repetition count, order and stopping rule are frozen before comparison (P:82).
- Separate scoring: answer correctness and source grounding are measured separately on frozen ID denominators (P:84). Reader fidelity is measured through the frozen observation contract in a separate recorded reader-probe session, isolated from the answer sessions, with raw requests/responses and a full alignment ledger (P:85). The three dimensions are never merged into one score (EV:78).
- Counts: planned, attempted, executed, scored and complete-pair counts are reported, with unavailable cases kept in coverage (P:86).
- Controls must be positive as well as negative (P:108), and keys come from independent native evidence, not from the reader (EV:65).

## Existing

- Scorer: `benchmark/scripts/score.py`. Entry point `main()` at :618-631 takes only `--check`. It calls `generate()` (:575), which loops over the three fixed fixtures (`FIXTURES`, :21) and writes `benchmark/results/challenges.json`. There is no argument that accepts an external answer record or reader response.
- Scoring function: `compute(source, denominators, inventory, submitted, probe, alignment, load_bytes)` (:234). Input format: `submitted` has `answer_record` (`status`, `claims[]` with `claim_id`, `answer`, `conditions`, `citations`; :240, :268), `raw_answer_record` (:243), `reader_response` with `observations[]` (:241, :251) and `raw_reader_response` (:244); `probe` has `raw_request`, `raw_request_sha256`, `request`, `simulated_operation`, `actual_execution` (:242, :246-248, :261); `alignment` entries carry `observation_id`, `aligned_claim_id`, `native_reference`, `reference_scope`, `xml_expected` (:253-254). Dimensions: correctness, grounding, fidelity (`DIMS`, :22).
- Record bridge: `benchmark/scripts/run_record.py:95` `score_answer(record)` converts a run record into `answer_record` and `raw_answer_record` only. Its docstring (:96-100) says it manufactures no keys, fidelity probes or denominators. It has no reader-response side.
- Runner contract: `benchmark/scripts/runner_contract.py:2` is "Synthetic runner-contract check only: no runner, model calls, real cases or scoring". `main` (:287-300) offers `--check` and `--write-manifest` only. `run_record.py:2` is likewise synthetic. `baseline.py:2`, `precision_plan.py:2` and `native_jobs.py:2` validate or generate designs and never execute.
- Reader adapter or runner that calls a model or reader: none under `benchmark/scripts/` (Glob listed 16 files: baseline, challenges, change_cases, two check_* scripts, coverage, dev_cases, lineage, native_jobs, precision_plan, run_record, runner_contract, score, sources, split_allocate, split_boundary). `benchmark/challenges/README.md:6`: "The concrete reader adapter is unavailable"; zero reader attempts.
- Probe definitions: only inside fixture JSON (`benchmark/challenges/{library-icon-tests,library-specialty,vi-actor-core-native-gap}.json`) as synthetic raw request/response text and `simulated_operation`. They were not opened whole. The probe-suite revision pinned to a native reference required by P:85 does not exist (`challenges/README.md:6`, `:8`).
- Keys: `challenges/README.md` last paragraph says both library inventories are confirmed 10/10 against independent XML keys (XML text agreement only). The native N-claims stay unverified, so no positive control can earn `correct` (`challenges/README.md:8`).
- Scorer behaviour on synthetic controls: 33 of 33 match author expectations, zero executed (`scorer-probe-0164.md:3,5`); no fixture shows credit awarded (`scorer-probe-0164.md:54`).

## Blockers

Blockers to one recorded reader attempt on a public dev fixture (library-specialty is the natural target).
1. No reader adapter or reader invocation path; the reader is the product. Class: needs-product-code. Evidence: `challenges/README.md:6`; no such script in `benchmark/scripts/` (Glob); `runner_contract.py:2`.
2. No native references for reader-fidelity alignment or for the native N-claims; fidelity and correctness cannot reach `correct`. Class: needs-LabVIEW. Evidence: `challenges/README.md:8`; `protocol.md:120`; `next-gap-0202.md` dependency/native keys row.
3. No chosen model/provider, pinned snapshot, quota or repetition count; manifest fields stay null. Class: needs-owner. Evidence: `protocol.md:80,82,124`; `runner_contract.py:7`.
4. No fresh-session runner that preserves real requests/responses/usage. Needs a model and reader to run, so it is not buildable as a working runner now. Class: needs-owner (model access and quota) plus needs-product-code (reader). Evidence: `protocol.md:83,124`; `runner_contract.py:2`; `run_record.py:5` (not a validator for populated records).
5. No scorer entry that takes a real answer record or reader response; `main` only regenerates the fixed synthetic fixtures. Class: doable-now-as-preparation (a `benchmark/scripts/` intake script composing `run_record.score_answer` with `score.compute`). Caveat: whether `compute` accepts an absent reader response was not checked. Evidence: `score.py:618-631`, `score.py:234`, `run_record.py:95-108`.
6. The reader-side bridge is missing: `score_answer` returns answer fields only (`run_record.py:96-100`), and no probe-suite record format exists for a real reader session. Class: doable-now-as-preparation (specify the format) and needs-product-code (to produce it). Evidence: `run_record.py:95-108`; `protocol.md:85`.
7. The scorer's citation check against the XML artifact: next-gap-0202 states the scorer never checks it (#831). `score.py` now has `citation_resolves` (:146), `citations_resolve` (:169) and `environment_loader` (:121), so that statement looks stale. I did not read those functions, so the status is unverified. Class: doable-now-as-preparation (re-measure it). Evidence: `score.py:121,146,169`; `next-gap-0202.md` reader row.
8. The dev attempt scored by this scorer is development evidence only; withheld evaluation needs the restricted store, custodian and tested boundary. Class: needs-owner. Evidence: `protocol.md:75,119`. This does not block a dev attempt.
9. Scorer and any change to it are reviewed independently; the benchmark scripts are unreviewed (`score.py:7`). Class: needs-owner (Policymaker orders review and evaluator work). Evidence: `protocol.md:111,125`.

## Recommendation

No attempt can be recorded now: blockers 1-4 need the product, native evidence or owner decisions. One preparation task is ready.

**Task: `benchmark/scripts/score_record.py`, a record-intake scorer for the `library-specialty` dev fixture.** It reads one run-record JSON (the `run_record.py` format), builds `submitted` with `run_record.score_answer`, scores correctness and grounding with `score.compute`, and prints outcome counts per frozen ID. Fidelity is reported `not-applicable/unexecuted` when no reader response exists. It must not write `benchmark/results/` and must not import `src/`. First step: read `score.compute` lines 234-367 to confirm an absent reader response is accepted; if it is not, report that as the blocker instead.
- Expected gain: when any real answer record exists, scoring needs no new glue. The synthetic round trip also shows whether scorer and record formats compose, which blocker 5 and 6 leave unmeasured. Limit: native slots keep correctness `unverified` (`challenges/README.md:8`), so this gives no quality result.
- Verification: `python3 -B -I benchmark/scripts/score_record.py --check`. It runs the synthetic record from `runner_contract.py` through the path and exits 0. It must exit 1 when a claim answer is altered. Afterwards, `git status --porcelain` must show no `__pycache__`.
