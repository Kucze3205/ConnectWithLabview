# Resource proposals for the protocol's resources table

Proposal material for the Policymaker to turn into `capability` requests. It grants no access, spending or publication rights and claims no readiness. It sets no thresholds, does not choose the LabVIEW 2024 fallback and does not narrow scope. Rules come from `docs/perpetua/accepted-limits.md`: reading permission is not permission to upload to model providers or publish; no spending is authorized, so anything new is marked "needs specific owner grant (service, purpose, ceiling)". Items marked **OQ** are owner questions; nothing in them is assumed. Do not put secrets or private material in any request.

Common readiness conventions: checks run with `git` and `python3 -I`, write raw outputs to a manifest with sha256 hashes, and are reviewed by a session other than the author. A check passing for one row says nothing about another.

## Row 1. Restricted evidence store with isolated execution
- **Unblocks:** protocol `split` (withheld cases/keys, tested isolation), restricted parts of `oracle`, `baseline`, `challenges`.
- **Public work can satisfy it?** No. A path in the public repo or its history gives no secrecy.
- **Resource options:** (a) a private repository in the owner's existing GitHub account, with separate access identities for custodian, scorer/checker, evaluated-session runner and development sessions; (b) a private store already held by the owner (e.g. existing cloud storage) reached from a trusted job. Option (a) at no cost only if the owner's plan already includes private repos (**OQ**). Paid storage/runner needs a specific owner grant.
- **OQ:** which store/service exists? who is custodian? can development sessions be technically denied access (separate token, not shared checkout)? does the trusted job path support a separate evaluated-session identity?
- **Providers/data:** the store operator sees everything stored. Model providers see only the assigned question and permitted artifact views of an evaluated session; never keys, other cases or oracle evidence. Which provider receives which category must be named in the grant.
- **Access:** custodian write; scorer/checker read keys; evaluated session read assigned input only; development none.
- **Publication:** only redacted aggregate split descriptions. Keys, cases, transcripts and revealing scores stay restricted.
- **Revocation:** remove tokens/identities and collaborator access, rotate credentials, delete clones, caches and backups on the grant's schedule; a leak retires the affected holdout.
- **Owner steps:** name the store and custodian; approve data categories and recipient providers; provision least-privilege identities manually; post the `capability-ready` confirmation after the check.
- **Readiness check:** with synthetic sentinel files only, from each identity run `git ls-remote`/`git clone` and a `python3 -I` read script; record allowed vs denied results; grep logs and artifacts for the sentinel; remove one token and re-run to show revocation. Independent review of the record.

## Row 2. Bounded native LabVIEW cloud inspection and experiment jobs
- **Unblocks:** `tasks`, `oracle`, reader-observation probes and `challenges` evidence.
- **Public work can satisfy it?** Partly: job recipes, input hashes and output schemas can be drafted now from public prepared sources. Execution needs the capability.
- **Resource options:** extend the established NI container readiness path (NI 2026 Q1 image, currently proven only for compiling a 2014 VI) as a trusted cloud job on the existing GitHub-hosted runner; or a self-hosted runner if the owner holds a licensed LabVIEW (**OQ**: version, licence type — development, volume, evaluation — and whether it may run unattended in a container or VM).
- **OQ:** does the NI image permit VI Scripting/property inspection and diagram capture? Is the licence terms-compatible with automated jobs? Any new hosted minutes or runner is spending needing a specific grant.
- **Providers/data:** GitHub (and NI image source) see job inputs; for public development sources that is already public. Model providers see only job outputs approved for the case category; private/withheld material is excluded until a Row 4/5 grant.
- **Access:** job receives only declared artifact hashes and licence; roles get staged results, no Docker daemon or runner credentials.
- **Publication:** development outputs where the source licence permits; otherwise restricted.
- **Revocation:** disable dispatch workflow/runner registration, delete runner secrets and mounts, expire working copies and staged outputs.
- **Owner steps:** confirm the environment and licence answers; approve operations list (read properties, capture diagrams, controlled I/O; edits/builds separately); approve and provision; confirm `capability-ready`.
- **Readiness check:** on one public development VI whose behaviour is independently known, the job must preserve the original (sha256 before/after via `python3 -I`), emit native properties and a capture, run controlled inputs, and write output hashes; `git status --porcelain` shows no source mutation; an independent session compares outputs with the expected values. Compile success alone fails.

## Row 3. Native versions, modules, targets, dependencies and licences
- **Unblocks:** `oracle` and `coverage` per environment stratum, including whether 2024 can be read at all.
- **Public work can satisfy it?** Partly: a table of required versions/modules from public sources can be drafted. Verifying anything needs access.
- **Resource options:** use only entitlements the owner already holds. Candidates per stratum: NI 2026 Q1 container (existing), a 2024 image/installer if the owner holds it, extra modules (Real-Time, FPGA, toolkits) if licensed.
- **OQ:** which LabVIEW versions and bitness does the owner hold? which modules/toolkits? licence type and activation limits? any hardware targets? may dependencies be redistributed to a runner? Any purchase needs service, purpose and ceiling in a specific grant. This proposal does not pick a fallback.
- **Providers/data:** licence/hosting vendors see activation data; model providers see only redacted environment metadata, never licence secrets.
- **Access:** runner reads installer/licence secret only during a job.
- **Publication:** permitted environment metadata and redacted results; never licence keys or proprietary binaries.
- **Revocation:** remove licence secret and installers from the runner, delete temporary installations.
- **Owner steps:** answer the OQs; nominate named strata to request one by one; provision; confirm.
- **Readiness check (per stratum):** job records version/build, OS, modules; loads a public VI saved in a known version; resolves a dependency; invokes the inspection API; outputs are hashed by `python3 -I`; failures recorded as such. Hardware claims need the actual target.

## Row 4. Owner-authorized private projects
- **Unblocks:** realistic `tasks`/`oracle` and project/family holdouts in `split`.
- **Public work can satisfy it?** No. No private project is identified and no blanket grant is inferred.
- **Resource options:** specific projects the owner owns or may license, named by repository/path; processed inside Row 1's store and Row 2's jobs.
- **OQ:** which projects exist, who holds rights, may any be natively opened, may any model provider see any part, what may be published?
- **Providers/data:** each permitted provider named per material category; default none. Reading permission does not authorize upload.
- **Access:** minimum read for custodian and checker; none for development roles.
- **Publication:** categories pre-approved; default restricted.
- **Revocation:** remove access, delete copies and backups, ask provider deletion per its terms, replace affected cases.
- **Owner steps:** list materials and rights; name providers, location, retention; provision; confirm.
- **Readiness check:** before ingestion, confirm the grant text against provisioned identities; sentinel test of denied development access (Row 1 procedure); provenance and licence record hashed with `python3 -I`; independent native check before any key is used.

## Row 5. Newly authored restricted cases, including missing families/versions
- **Unblocks:** independent `oracle`, whole-lineage `split`, discriminating `challenges`, coverage of families absent from public sources.
- **Public work can satisfy it?** Partly: authoring recipes and specs can be drafted now. Withheld cases cannot be public.
- **Resource options:** the owner (or a named author) builds new VIs/projects in a licensed native LabVIEW (**OQ**: version, who authors, owned/licensed inputs), stored in Row 1's store; checked in Row 2's jobs.
- **Providers/data:** model providers see case content only if the grant names them for authoring; evaluated sessions see assigned inputs only.
- **Access:** author write to own cases; checker read; evaluated session assigned input; development none.
- **Publication:** aggregates only; nothing that reveals a case.
- **Revocation:** remove author/runner access; retire leaked or withdrawn cases and keep lineage record.
- **Owner steps:** name missing families/versions to target (no scope change implied); name author/custodian/checker; confirm ownership; provision.
- **Readiness check:** provenance and ownership record; sha256 of originals; `python3 -I` duplicate check against public sources; whole-group allocation recorded; native discriminating evidence; independent claim/key review.

## Row 6. Existing model access, reproducible runner and quota
- **Unblocks:** paired `baseline` runs, uncertainty, cost and time reports.
- **Public work can satisfy it?** Mostly: runner design, manifest schema and development pilots on public cases use existing subscriptions. Evaluation runs need Rows 1 and 3-5.
- **Resource options:** existing subscription providers/models listed in the engine's catalog; pin exact snapshot where the provider allows, else disclose and bound the run window.
- **OQ:** remaining quota, whether image input is available, provider retention/training settings, whether a runner may run repeated fresh sessions within limits. Extra quota or paid API needs a specific grant with ceiling.
- **Providers/data:** the chosen provider sees prompts and assigned artifacts of that run; scorer alone reads keys.
- **Access:** runner reads assigned cases only.
- **Publication:** configuration and aggregates only; revealing prompts/responses restricted.
- **Revocation:** remove session credentials, clear caches/memory, follow provider deletion terms; disclose unpriced resources.
- **Owner steps:** name provider/model and retention settings; confirm quota; approve a repetition and precision plan (not set here).
- **Readiness check:** one complete development pair on a public case, same prompt, inputs and budgets; manifest with model id, tokens, time, errors, cost written and hashed with `python3 -I`; confirm fresh sessions; `git status --porcelain` clean for inputs. Does not show benchmark quality.

## Row 7. Independent method reviewer, key checker and authorized executable scorer work
- **Unblocks:** reviewed `tasks`, `oracle`, `split`, `baseline`, `challenges`; executable scoring later.
- **Public work can satisfy it?** Yes for public development material: the Policymaker can order separate review and evaluator sessions with no new access. Private evidence needs a Row 4 grant.
- **Resource options:** separate reviewer sessions; evaluator role for `policy/evaluator/` changes with its independent verifier.
- **OQ:** none for public review; for private evidence, which providers may the reviewer use?
- **Providers/data:** the reviewing model provider sees the reviewed public files; private evidence only if granted.
- **Access:** minimum evidence per grant; the author cannot approve their own work.
- **Publication:** redacted findings only.
- **Revocation:** end reviewer/scorer access after assignment; keep approved audit records.
- **Owner steps:** none for public review; later owner acceptance of the pinned protocol and evidence remains separate.
- **Readiness check:** reviewer records claim-level findings; evaluator verifier passes the exact changed tree; `python3 -I policy/evaluator/evaluate.py --check` exits 0 (index integrity only); a pass is never inferred from filenames, hashes or exit status alone.

## Filing checklist
Before a `capability` request: actual service and operator; exact materials; least access; every recipient provider; processing location; publication categories; retention, deletion, backups; revocation; existing entitlement vs new spending with ceiling; the readiness command. Approval provisions nothing; wait for manual provisioning and `capability-ready`. Suggested order: rows 1 and 2.
