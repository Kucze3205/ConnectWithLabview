# Delivery options and version-scope effort

Initial partial report for issue #49; source inspection and verification are still in progress. This report makes no delivery choice and no fallback choice for the owner.

## Evidence and scope

The goal is agent reading across every LabVIEW artifact family and save version. A 2024-only fallback remains the owner's decision after reviewing effort and compatibility limits ([journal/0001.md](../../journal/0001.md), State; [roles.md](../perpetua/roles.md), Work sequence).

Prepared evidence is pylavi commit `35d2a0318f71dcb87bb9c431dc00700ee6b9fb75` (Unlicense) and NI Actor Framework commit `371c631c16155d88f02be11a953e4964d7452fd8` (MIT). `@environment/readiness.json` records resource-table access for `Core/ActorFramework/Actor/Actor Core.vi`, SHA256 `135d50e68f002aea9c6a08d0265cc6178b326f1af99353755064c953eaec063c`, and XML parsing of a project with LVVersion `20008000`. Semantic reading is explicitly `not_measured`; this is not all-version or native-2024 evidence.

## CLI export

Proposed use: an agent runs a command on an artifact or directory and reads deterministic text/JSON with original-source locations. Runtime would need the chosen parser and Python for a pylavi-based implementation; native extraction would additionally need a compatible NI runtime and permitted automation. A pure-parser path could operate offline on local inputs after dependencies are staged. Native licensing and cloud availability require separate checks. Potential families include binary resource artifacts supported by the parser plus XML project/library manifests through additional readers. Resource-table access alone does not establish diagram semantics.

## Python library

Proposed use: an agent runs Python to inspect structured objects and request selected details. Runtime would need compatible Python, the library and its dependencies; native calls would inherit NI requirements. A pure-parser library could operate offline. Family coverage depends on reader implementation, not packaging; XML manifests require a separate reader if the parser only handles binary resource containers. A stable public API, bounded resource consumption and explicit unsupported-result reporting remain engineering work.

## MCP server

Proposed use: an MCP-capable agent discovers tools/resources and requests artifact summaries, graph neighborhoods and source locations. Runtime would add a protocol implementation, an agent client supporting it and a running server around the same reader. A local transport could avoid external service access; a remotely hosted deployment would introduce authentication, data handling and operation costs. MCP does not itself decode any additional artifact family. Neither an MCP runtime nor MCP access is currently available to this research role ([roles.md](../perpetua/roles.md), Available tools and limits). Protocol and client details remain unverified against staged primary sources.

## Committed text mirror

Proposed use: an agent reads/searches generated text alongside source artifacts in git. Consumers need only text access; producers need an exporter and regeneration checks. Reading existing text could be offline without NI; refreshing it inherits exporter dependencies and licensing. Every family would require a faithful exporter, original-artifact identifiers and a stale-output check. Binary originals must remain authoritative. Text generation and committing are proposals, not an implemented product or an authorization to publish private inputs.

## Effort: all versions vs 2024-only

Estimates will be extended after inspecting the prepared parser's actual version handling. They will be planning ranges, not measured implementation durations. Both variants must cover all artifact families; restricting the save-version target cannot silently remove families or substitute resource enumeration for semantic reading.

## Compatibility limits of the 2024 fallback

A 2024-only save-format reader would offer no promise for artifacts saved by later releases. Older save formats would also remain outside its promise unless explicitly tested and supported. Native LabVIEW 2024 loading older files and direct parsing of 2024-saved files are different contracts. Neither is established by a 2026 runtime processing a 2014 VI ([environment.md](../perpetua/environment.md), LabVIEW cloud runtime and version coverage). Password protection, missing dependencies, platform/toolkit features and compiled-only inputs need separate evidence before claiming coverage.

## Open measurements

- Inspect the pinned pylavi tree for format revisions, version predicates, unsupported resource blocks and actual XML support; record source locations before estimating scope differences.
- Establish separately the readability of original binary artifacts, parsed resource structures and exported program meaning against independent expected answers.
- Obtain provenance-pinned 2024 and historical fixtures and measure each artifact family/save-version pair; no native 2024 execution is ready in the role environment.
- Validate proposed MCP client/transport behavior against a staged primary specification and an available client before estimating integration as measured work.
- Measure regeneration, stale-mirror detection, offline operation and consumer workflow costs for each proposed delivery form after the prerequisite reading method is independently checked.
