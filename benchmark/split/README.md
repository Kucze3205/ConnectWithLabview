# Split boundary design

This is a public, design-only contract. No partition is allocated here: no case or key is withheld, and nothing public (including repository history, obscure paths, release assets, or evaluator directories) provides secrecy. The restricted store has an executed readiness record (benchmark/split/store-readiness-268.redacted.json, accepted by review #431) with synthetic sentinels only; it holds no case. The isolated runner is not ready.

## Lineage allocation

Before allocation, whole projects, shared dependencies, copied components, and related revisions are grouped into connected lineage groups. Exact copies are checked by original/member hashes; renamed, resaved, archived, and edited variants require provenance, native structural comparison, and manual adjudication. Hash inequality alone does not establish independence. A connected group must remain in one partition.

The manifest template defines the future custodian record without allocating anything. Its allowed partitions are `development`, `eval-unseen-lineage`, and `eval-held-out-family`. It must not contain real keys, credentials, or withheld case content.

The two evaluation strata are:

* unseen lineages within families represented in development; and
* whole held-out families, with all related projects and components excluded from development.

Mixed-family projects remain whole groups. If whole-group allocation makes a family holdout infeasible, the infeasible stratum is reported rather than leaking components across partitions.

## Isolation readiness

The isolation record describes required pre-measurement checks: custodian clone and push; scorer clone with push rejected; tokenless `ls-remote` denied; zero synthetic-sentinel hits in logs, artifacts, and the public repository; and revoked scorer-token clone denied. Actual results and evidence remain null until a real store, identities, custodian, and independent review exist. Synthetic sentinels must be used for boundary testing; real keys and cases are not placed here.

Split remains blocked by new/private cases, variant analysis, and native structural comparison. Public sources can support development specifications and duplicate-method preparation only.
