# Issue #287 readiness search

Result: none of the three inspected candidate VIs qualifies. No native execution occurred. No controlled I/O expectations were derived from a VI, its filename, or reader output; no readiness-case.json is proposed.

Prepared sources: pylavi commit `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75` and actor-framework commit `371c631c16155d88f02be11a953e4964d7452fd8`, accessed read-only through LABVIEW_ENVIRONMENT. SHA256 values below were measured with `python3 -I -B` and hashlib over original bytes.

| Candidate path relative to LABVIEW_ENVIRONMENT | SHA256 | Independent source | Complete controlled I/O expectation? |
| --- | --- | --- | --- |
| pylavi/tests/add.vi | cf4b1f56c8e42a7a353101ba1322aa3d64207bb19df5dc791cb3eedf2bb2f7e8 | pylavi/tests/test_validate.py:93-94 asserts zero validation problems for the breakpoint check. | No: metadata validation supplies neither connector identities nor arithmetic input/output values. |
| pylavi/tests/add_breakpoints.vi | 510a227bb02cca8238654261761f95ba422c7e7be9631996e41769f73a80feb6 | pylavi/tests/test_validate.py:95-96 asserts one validation problem for the breakpoint check. | No: a validation problem count does not specify native execution behavior. |
| pylavi/tests/empty.vi | d58fe28f21ad9ac1623009f290a1d7cd4f34a514f236f61867cbcb854772f173 | pylavi/tests/test_validate.py:85-90 asserts validation results for embedded-code checks. | No: these assertions specify file metadata, not discriminating controlled I/O. |

The independent test source `pylavi/tests/test_validate.py` has SHA256 `eb787e7e4a0dbd7d901a1c8e0cff77e8e94b258e59c60e2f29ab0a96298c972c`.

Search scope: pylavi README, tests/args.yaml and all 21 test*.py files; actor-framework README and Documentation/**/*.md. Searches used bounded printed matches for VI references, addition, native-call APIs, expected values, assertions, calculations, inputs and outputs. The initial @environment Grep/Glob returned truncated or incorrectly scoped results; subsequent searches used the explicit LABVIEW_ENVIRONMENT root. Those initial results were not treated as evidence of absence.

Two documentation leads describe generated applications rather than an identified, hashed prepared VI with complete controlled vectors. `actor-framework/Documentation/Test Plan/1713431.md:18-22` describes a cooler application, approximate temperature evolution, thresholds and stopping; SHA256 `ae7e17698edef322b54ba30ea47593630af663efb52951e4b9c408f181170b5f`. `actor-framework/Documentation/Test Plan/1713432.md:23-29` describes splash/UI behavior, message logging and exit; SHA256 `539ed50ba902555c7129e40d4fa6f06286ee847077e211fc8fcbfd82afd5e234`. Neither establishes a complete fixture for an original prepared VI. These leads were not promoted to additional candidates.

This is a bounded negative finding, not proof that no suitable public VI exists. Per issue #287's none-qualifies branch, stop selection here. #169 remains unready. Next work needs a prepared public VI paired with independent test code or documentation specifying exact controls, outputs and at least two discriminating vectors; provision and pin that source before a new readiness preparation session. Do not repeat metadata-only assertions as an I/O oracle.
