# Public change-case designs

These are design only: zero native executions, no key established, no edit performed.
The two public development specifications cover [typedef impact](typedef-impact.spec.json) and [diagram differences](diagram-difference.spec.json). All native answers remain `unavailable` under #169; neither specification establishes semantic correctness or benchmark readiness.

Each design pins a prepared NI Actor Framework original, freezes four required claim IDs and four reader-observation IDs, and describes derived-copy edits, native observations and independent checking. Static consumer candidates remain unconfirmed. The prepared actor-framework checkout has one commit, so no paired public revisions exist; proposed variants are future derived copies.

Run from the repository root:

```sh
python3 -I -B benchmark/scripts/change_cases.py --check
```

The stdlib checker validates required fields, fixed IDs, unavailable answers, grant flags and ten in-memory rejecting mutations with asserted reasons. When `LABVIEW_ENVIRONMENT` is set it verifies the original and candidate source SHA256 pins; otherwise it explicitly reports that source verification was skipped. It writes no files and executes no prepared source. A checker pass validates the design structure, not the proposed native effects.

Edits and builds require an explicit owner grant before execution under [the protocol](../protocol.md#resources-and-owner-decisions), plus a permitted licensed authoring environment. The current official headless container cannot author/edit source. Semantic documentation still needs version, section/location and content-hash pins; each specification lists those gaps. Native fixtures and object locators must be frozen and independently checked before reader exposure.

Next, the Policymaker should run the checker on main and order one independent review. Native execution remains blocked on #169 and the stated grants/capabilities. Preserve originals, retain unavailable claims in all denominators, and keep these public sources and derivatives in the same development lineage group. No preparation index, milestone status or pinned evidence is changed by these new files.
