# Public lineage preparation

- repositories: 2
- artifacts: 829
- originals: 530
- archive members: 299
- exact hash groups including singletons: 803
- exact duplicate groups: 24
- exact duplicate members: 50
- candidate groups: 230
- distinct different hash candidate pairs: 1244
- candidate groups with version difference: 13
- conservative lineage groups: 2
- development cases: 11
- development lineage ids: 1
- static membership declarations: 647
- static name gaps: 151

Counts describe the [public inventory](lineage.json); candidate groups overlap and remain unadjudicated. This summary contains no case keys. Hash inequality does not establish independence.

Split remains **not-started**. Public inventory preparation is unreviewed; no evaluation partitions are allocated. Missing: restricted store, custodian, private/new cases, native structural comparison and tested isolation. Independent method review and owner acceptance are still required; no readiness or product claim.

Generate: `python3 -I benchmark/scripts/lineage.py`. Verify: `python3 -I benchmark/scripts/lineage.py --check` and `python3 -I policy/evaluator/evaluate.py --check`.
