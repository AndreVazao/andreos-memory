# DGM-MAT Repository Governance and Consolidation
**Updated:** 2026-10-18  
**Status:** active consolidation plan; do not delete repositories automatically.

## Non-negotiable architecture
- `AndreVazao/DGM-MAT` is the sovereign brain and the primary execution authority.
- HQ/cockpit is an observational projection of real runtime events. It must not orchestrate, authorize, or control the brain; visual agents/animations reflect actual runtime state.
- No automatic cloning of satellite, private, or third-party repositories into the DGM-MAT workspace. Third-party source code is admitted to the lab only by an explicit, approved import.
- Preserve `DGM-MAT-FULL-MIRROR`, legacy AndreOS memory, and unrelated Labs/clones unchanged.
- Do not delete source code before dependencies, consumers, tests, and history are audited.

## Canonical memory and documentation
- Canonical memory repository: `AndreVazao/andreos-memory`, branch `main`.
- Local operational copy: `C:\\AndreOS-Memory`.
- This file is the central repository inventory and governance record. Update it whenever repository roles/status change.
- DGM-MAT's own README must summarize architecture boundaries and link back to this inventory.

## Repository inventory (GitHub metadata/readme inspected 2026-10-18)
Status meanings: **KEEP** = established purpose; **KEEP / STRICT BOUNDARY** = retain but narrow responsibility; **REVIEW** = meaningful code exists or purpose/dependencies need audit; **DELETE CANDIDATE** = currently empty or generic stub, owner should delete manually after final confirmation; **DO NOT TOUCH** = explicit exclusion.

| Repository | Decision | Purpose / action |
|---|---|---|
| `DGM-MAT` | KEEP — canonical brain | Core intelligence, runtime, tools, orchestration, tests, governance. No automatic satellite clones. |
| `andreos-memory` | KEEP — canonical memory | Cross-project persistent memory and authoritative repository inventory. |
| `DGM-Cockpit-Frontend` | KEEP / STRICT BOUNDARY | Read-only visual cockpit; presentation only, never brain control. |
| `DGM-Contracts` | KEEP / STRICT BOUNDARY | Shared public contracts; preserve while `DGM-MAT-Agents` depends on it. |
| `DGM-MAT-Mobile` | KEEP / STRICT BOUNDARY | Lightweight remote chat/cockpit; PC DGM-MAT remains execution authority. |
| `DGM-MAT-Labs` | KEEP — external code laboratory | Explicitly imported third-party repos/code for study, security/license review, tests, and selective reuse. Never auto-clone. Never execute untrusted code by default. |
| `DGM-MAT-Connectors` | REVIEW / likely KEEP | External integration adapters; confirm imports and deployment boundary before migration. |
| `DGM-MAT-Providers` | REVIEW / likely KEEP | AI/browser provider adapters; confirm no duplicate core logic and no uncontrolled browser automation. |
| `DGM-MAT-Plugins` | REVIEW / likely KEEP | Optional extensions, isolated from core; confirm real consumers. |
| `DGM-MAT-Assets` | REVIEW | Shared assets/data only if there is a real consumer and access-control contract. Do not use as an arbitrary code dump. |
| `DGM-MAT-Deploy` | KEEP / STRICT BOUNDARY | Vercel rendezvous/discovery only; never execution plane or conversation-content store. |
| `DGM-MAT-Agents` | KEEP / REVIEW integration | Standalone agent package; preserve source in core until consumers and full regression suite validate migration. |
| `DGM-MAT-OS` | REVIEW — do not delete | Substantial repository; audit overlaps/dependencies before deciding. |
| `DGM-MAT-Runtime` | REVIEW | Tiny repository; determine whether it contains unique runtime assets or is an empty stub. |
| `DGM-MAT-Orchestrator` | REVIEW / likely redundant | Do not split orchestration out of the sovereign brain unless a tested architectural contract proves the need. |
| `DGM-MAT-Memory` | KEEP — recovery synchronizer | Selective, versioned, secret-scrubbed backup of approved DGM-MAT documents, verified learning, recovery manifests and environment reconstruction instructions. It is not the same as `andreos-memory`; the prior delete notice was incorrect and its README has been corrected. |
| `DGM-MAT-Cluster` | DELETE CANDIDATE | Reported size 0, generic stub. Confirm no active consumer before deletion. |
| `DGM-MAT-Media` | DELETE CANDIDATE | Reported size 0, generic stub. Confirm no active consumer before deletion. |
| `DGM-MAT-Studio` | DELETE CANDIDATE | Reported size 0, generic stub. Confirm no active consumer before deletion. |
| `DGM-MAT-Marketplace` | DELETE CANDIDATE | Generic stub; no concrete role established. Confirm no active consumer before deletion. |
| `DGM-Core-Backend` | DELETE CANDIDATE | Reported size 0. The backend/core authority belongs to `DGM-MAT`; confirm no consumer before deletion. |
| `DGM-Docs` | DELETE CANDIDATE | Reported size 0. Central documentation belongs in `andreos-memory` and relevant product docs in `DGM-MAT`. |
| `DGM-Experimental` | REVIEW — do not delete yet | Substantial content; inspect history, code and dependencies. Candidate to merge useful material into the core/lab or archive only after audit. |
| `DGM-HUB` | KEEP SEPARATE / REVIEW | Independent DGM repository, not a DGM-MAT satellite dependency. Evaluate as a possible integration only with evidence. |
| `DGM-MCP` | KEEP SEPARATE | Local MCP bridge with its own security boundary. Do not silently merge it into the DGM-MAT core. |
| `DGM-MAT-FULL-MIRROR` | DO NOT TOUCH | Explicitly excluded from modifications/deletion. |
| Legacy AndreOS memory | DO NOT TOUCH | Explicitly excluded from modifications/deletion. |
| Unrelated Labs/clones | DO NOT TOUCH | Not to be imported, changed, or removed by this consolidation. |

Repository sizes are GitHub-reported size metadata, not proof that a repository is safe to delete. A delete-candidate label is a manual recommendation, not authorization for automatic deletion.

## AI conversation archive design
Use a structured, searchable archive with source provenance instead of one giant text file:
1. Preserve the original export/import file unchanged under a source archive path.
2. Normalize each conversation and message/turn into records with stable IDs, source provider, source conversation ID, timestamps, role, content, attachments/references, and import timestamp.
3. Store durable records in a local database (SQLite is the default candidate for the current Windows/local-first runtime), with full-text search (FTS5 where available); keep original raw exports for traceability.
4. Store derived summaries, topics, project links, decisions and supersession relationships separately from original messages.
5. Index incrementally; retrieve relevant local records first. Contact external AI websites only when the archive lacks the answer or a fresh lookup is explicitly needed.
6. Avoid one folder per conversation as the primary index. Optional per-conversation Markdown/JSON exports may be generated for portability, but the database and source archive are authoritative.
7. Do not implement a second archive until the current DGM-MAT storage/session/event persistence has been audited.

## Merge/consolidation gate before starting a clean branch
1. Inventory all relevant branches, unmerged commits, open PRs, local changes, tests and consumers in DGM-MAT and its retained satellites.
2. Compare branch diffs and identify duplicate, superseded, conflicting, or unrelated work.
3. Preserve all unmerged work before any branch cleanup. Do not overwrite user changes.
4. Integrate selected work into the appropriate canonical repository; do not merge unrelated products or entire satellite repositories into DGM-MAT.
5. Run available local tests and CI evidence; record known failures without claiming green status.
6. Update READMEs and this inventory; only then create the next clean feature branch from the verified canonical base.
7. No GitHub Actions workflows should be newly added or triggered without explicit need/approval; prefer local validation.

## Required README boundaries for retained satellites
Each retained satellite README must specify: purpose, what belongs here, what must remain in DGM-MAT, dependency/API contract, test/validation procedure, current status, and prohibited responsibilities. Keep READMEs concise but operational.


## Live consolidation checkpoint — 2026-10-18
- DGM-MAT `main` now includes the updated README authority boundary (commit `0ffa2565a1ccdd51f02a3242469d5e544855fd7c`).
- This governance record was committed to `andreos-memory/main` (`25e07996061c9966ab7cf5b30b7787ad52b9c579`).
- DGM-MAT currently exposes many historical/feature branches. Comparison against `main` found `feat/conversation-turn-semantics-v1`, `integration/all-branches-recovery-2026-10-17`, `recovery/missing-feature-modules-2026-10-17`, `audit/self-repair-web-control-gaps-2026-10-16`, `feat/capability-acquisition-recruitment`, and `fix/digital-organization-foundation-complete` are behind `main` with no unique commits ahead; do not merge these stale branches into main.
- `docs/digital-headquarters-integration-index-2026-10-17` is diverged by 1 commit ahead / 8 behind; inspect its unique commit before deciding whether the content is already present or needs cherry-picking.
- `fix/backend-end-to-end-stabilization-final-2026-10-18` is diverged by 93 commits ahead / 1 behind and is the head of open draft PR #86. Its own PR description says end-to-end sign-off is incomplete: GitHub Actions lacks `DGM_CONTRACTS_READ_TOKEN`; Windows runtime startup, queue consumption, full cockpit-to-result flow, restart recovery and EXE build are not validated. **Do not merge PR #86 yet.** First inspect the diff, resolve the one-behind base, validate the code and required gates; do not create a new feature branch until this consolidation decision is recorded.
- PR #86: https://github.com/AndreVazao/DGM-MAT/pull/86
- The branch `ci/backend-phase-gate-workflow-2026-10-17` and related CI branches exist. The user's standing preference is to avoid Actions usage unless necessary; inspect and decide whether the workflow is actually needed before merging it.
- README boundary updates committed: `DGM-MAT-Labs`, `DGM-MAT-Mobile`, `DGM-MAT-Plugins`, `DGM-MAT-Connectors`, `DGM-MAT-Providers`, `DGM-MAT-Deploy`, `DGM-Cockpit-Frontend`, `DGM-MAT-Agents`, and `DGM-Contracts`.
- Delete-review notices committed to `DGM-MAT-Cluster`, `DGM-MAT-Media`, `DGM-MAT-Studio`, `DGM-MAT-Marketplace`, `DGM-Core-Backend`, and `DGM-Docs`. These repositories were not deleted. `DGM-MAT-Memory` was incorrectly classified and is now explicitly retained; its README was corrected in commit `c4e87f652cce2126ef2d57f50910a101f8b4ac59`. The owner should manually verify the remaining candidates' branches/issues/consumers/history before deleting them.
- Keep `DGM-MAT-OS`, `DGM-Experimental`, `DGM-MAT-Runtime`, `DGM-MAT-Orchestrator`, `DGM-MAT-Assets`, `DGM-MAT-Plugins`, `DGM-MAT-Providers`, and `DGM-MAT-Connectors` in REVIEW until their full trees, histories and consumers are audited. Do not call them safe to delete based on size alone.


## Architectural priorities and hardware adaptation — confirmed by owner 2026-10-18

### DGM-MAT-Memory is a required satellite
- Keep `AndreVazao/DGM-MAT-Memory`; do not delete it or treat it as a duplicate of `andreos-memory`.
- Its purpose is the DGM-MAT's **selective recovery/synchronization repository**: keep approved and recoverable documents, validated learning, architecture and recovery manifests in GitHub so a replacement PC can reconstruct the environment after hardware failure.
- `andreos-memory` remains the authoritative governance/continuity memory for decisions and project tracking. `DGM-MAT-Memory` is the operational recovery archive. Their responsibilities are related but distinct.
- Sync must be explicit/selective, versioned, traceable and secret-scrubbed. No credentials, tokens, cookies, private keys, unreviewed conversation dumps, caches, or indiscriminate workspace mirrors.
- A local-first brain must continue working if GitHub or the network is unavailable; the remote repository is a recovery copy, not a runtime dependency.
- Recovery to a new PC must include a reproducible environment manifest (OS, CPU/RAM/GPU/storage capability, installed tools and versions, dependencies, configuration templates without secrets, and restore/validation steps).

### Adaptive runtime
- Detect the real environment at startup and on meaningful changes: OS, CPU, RAM pressure, storage, GPU/VRAM where applicable, connectivity, available tools, local models and versions.
- Adapt concurrency, model choice, memory limits, test scope, and department scheduling to measured resources. Do not assume that the older current PC and future stronger PC have the same capacity.
- If a required tool is missing, research viable alternatives and explain purpose, license, cost, provenance and impact; request approval before installing. If no appropriate tool exists, the Virtual Factory may propose a purpose-built component, isolated and tested before production use.
- Never introduce a paid dependency or paid fallback silently. Prefer local/free capabilities where adequate and disclose limitations.

### Highest-priority departments: Programming and Research
All departments remain important, but the owner explicitly identifies these two as especially critical and expects meticulous, evidence-backed operation.

**Programming and Code Review department**
- Requirements and acceptance criteria before implementation; inspect callers, imports, contracts, tests, runtime behavior, persistence and Git history before edits.
- Small, reversible changes; preserve user work; no silent deletion or broad refactors to mask a failing test.
- Review diffs independently; test syntax, focused behavior, regression, security, integration and runtime where feasible.
- Report precisely what passed, failed, was blocked or remains unverified. No false claims of completion.
- Proposed self-modification must be isolated, reproducible, tested and reviewed; human approval is required for high-impact, destructive, permission-changing or authority-changing actions.

**Research and Innovation department**
- Prefer primary/official sources and cross-check important claims; record source URLs, retrieval date, version and license.
- Search the local conversation/document/code archive before repeating external research; revisit external sources only when freshness or missing evidence requires it.
- Compare alternatives with explicit criteria: correctness, maintenance, compatibility, security, licensing, performance on the current PC, resource requirements and future portability.
- Third-party code enters only the designated lab through explicit import; inspect license, provenance, security and tests, then extract/adapt only justified components.
- Distinguish verified fact, hypothesis, recommendation and untested claim. Provide reproducible evidence and a clear confidence/limitation statement.

### Headquarters is strictly observational
- The DGM-MAT brain owns mission state, decisions, scheduling, authorization and execution.
- The Headquarters/cockpit visualizes actual runtime events and state; it cannot control or orchestrate the brain and must not be a dependency for brain operation.
- Characters, departments, laboratories, research activity and warehouse/archive visuals must derive from real entities/events. No simulated agent activity or fabricated progress.

### Consolidation checkpoint amendment
- The owner has explicitly confirmed that `DGM-MAT-Memory` is required for recovery synchronization; prior delete-candidate classification is superseded.
- Do not merge PR #86 while GitHub reports it non-mergeable and its required end-to-end gates are incomplete. Continue by resolving the base divergence, checking workflow side effects and dependencies, and obtaining honest CI evidence. Create the clean next feature branch only from the verified consolidated base.


## Distributed brain and virtual city vision — owner confirmation 2026-10-18

The owner has explicitly confirmed the long-term architecture: the brain remains sovereign and headless; departments must be modular enough to run first on one PC and later on separate satellite PCs on the same network; the Headquarters/cockpit may run on a different PC, browser or phone. The virtual office should grow from one multi-floor building into a city of department buildings as real machines and services are added.

- Canonical detailed design: DGM-MAT document `docs/architecture/DGM-MAT-DISTRIBUTED-BRAIN-AND-VIRTUAL-CITY-ROADMAP-2026-10-18.md` (commit `02bfe2a97a0efcb98b663f9049ce5f5401b5a226`).
- This is a binding architectural direction, not a claim that multi-PC execution or the virtual city is already implemented.
- Current phase stays focused on repairing and proving the brain end-to-end with a simple cockpit. Do not start 2D/3D city work ahead of runtime stability and regression gates.
- Design modules around explicit/versioned contracts, node identity and trust, capability/health reports, durable tasks, result envelopes, real observability events, resource-aware scheduling, security boundaries, and offline/recovery behavior. First inspect and reuse existing contracts, queues, persistence and event systems; avoid duplicating working infrastructure.
- Brain and departments must continue running if the cockpit/browser/phone/rendering layer is closed or disconnected. The cockpit only projects actual authenticated runtime state and never becomes an authority or an execution dependency.
- The design must support hardware adaptation and migration to a stronger/replacement PC, and avoid assuming all departments share a process, filesystem or database.
- No automatic cloning of satellite/private/third-party repositories into the local DGM-MAT workspace. External source is studied in DGM-MAT-Labs only through explicit, approved import.
- Non-regression is mandatory: inspect history, callers, contracts, persistence and local changes before editing; make small reversible changes; validate the complete user-order → durable task → execution → result → persistence → cockpit path, restart/recovery and relevant Windows behavior; accurately report every failed, blocked and untested gate.


## Verified CI / PR state amendment — 2026-10-18

This section supersedes the earlier statement above that PR #86 must not be merged: the GitHub record now confirms PR #86 was merged into `main`.

- PR #86: https://github.com/AndreVazao/DGM-MAT/pull/86 — merged; merge commit `cba0e15fc08470d8d66144e59cb87dad0c789ac4`. This does **not** constitute end-to-end sign-off.
- Backend Phase Gate run for the PR head: https://github.com/AndreVazao/DGM-MAT/actions/runs/39107658582 — **failed**. Three dependency-dependent jobs failed at `Restore modular runtime dependencies` because `AndreVazao/DGM-Contracts` is verified **private** and the workflow's anonymous-clone fallback cannot access it.
- The same run passed: understanding/help/research/learning; minimal PC chat cockpit tests; Python source compilation; durable queue safety. The required phase-gate summary failed because the mission/API, security/governed-execution, and research/knowledge-fabric jobs failed before their test suites could run.
- A corrective draft PR #87 is open: https://github.com/AndreVazao/DGM-MAT/pull/87. It makes the missing private-repository credential failure explicit in all three workflow dependency-restore steps. It does not bypass tests or claim to solve the credential requirement.
- Remaining owner-side prerequisite: configure the GitHub Actions repository secret `DGM_CONTRACTS_READ_TOKEN` with least-privilege Contents: Read-only access to `AndreVazao/DGM-Contracts`. Never paste the token into chat, a commit, workflow logs or source files. After the secret is configured, rerun the phase gate and require all jobs to pass before claiming end-to-end readiness.
- PR #86's code has merged despite its own body accurately warning that Windows startup, real queue consumption, cockpit-to-result flow, restart recovery and EXE build were not validated locally. Those checks remain unproven until separately demonstrated.
- Current branch discovery via the GitHub branch-search endpoint returned only `main` for an empty query; this is not a complete inventory of all PR heads or all satellite repositories. Do not infer that the entire consolidation inventory is complete from that result.


## Correction: DGM-Contracts is public; CI no longer requires a token — 2026-10-18

The owner confirmed that `AndreVazao/DGM-Contracts` was made public to avoid token requirements. A fresh GitHub repository metadata check confirms `visibility: public`.

- Superseded and closed draft PR #87 (it incorrectly retained a private-repository token requirement): https://github.com/AndreVazao/DGM-MAT/pull/87
- Opened draft PR #88: https://github.com/AndreVazao/DGM-MAT/pull/88
- PR #88 changes all three restore steps in `.github/workflows/backend-phase-gate.yml` to a direct shallow HTTPS clone of the public `DGM-Contracts` repository. No token is needed for this dependency.
- Workflow commit: `5d33a24d9a8f24285fc237490e8c3cec2afd52be`.
- Backend Phase Gate run: https://github.com/AndreVazao/DGM-MAT/actions/runs/39125135429 — queued at last check. Do not mark CI passed until the run completes and all required jobs are green.
- PR #88 remains draft/unmerged until the workflow results are inspected. Even with green CI, Windows startup, real mission consumption, persisted results, restart/recovery, cockpit independence and EXE packaging remain separate checks.


## CodeRabbit + CI follow-up — 2026-10-18

- Owner enabled CodeRabbit on GitHub; use it as an additional reviewer for public projects, initially DGM-MAT, with the procedure in `AndreOS/02_PROJETOS/DGM-MAT/CODERABBIT_GITHUB_REVIEW_POLICY.md`.
- CodeRabbit is advisory, not a replacement for CI, code/diff inspection, Windows validation, or explicit merge approval. Verify that its review covers the current PR HEAD; incremental review may not revisit prior commits.
- PR #88 head advanced to `0d7d68d18fb1356d7acc714873d87000e2149129` when the runtime capability module was added. Backend Phase Gate run #75: https://github.com/AndreVazao/DGM-MAT/actions/runs/39125327911 — **failed** after dependency restore and compilation succeeded.
- Run #75 findings: mission API/queue/recovery had four 403 responses where authenticated cockpit requests expected 200, plus a mission-recovery test expected a `status` key absent from failure results; auth/governed-execution had several 403 responses where missing/valid sessions should respectively yield 401/200 and an invalid target path returned the wrong denial reason. These are being corrected on the PR branch; do not merge until the next full gate is green.
- Corrections committed to PR #88 branch: auth classification fallback (commit `61cfa32`), explicit control-character path rejection (`b8ade22`), explicit `status: failed` in failed mission results (`8954b94`), regression expectation for truthful planning-only failure (`f4cb9e6`), removal of an unused import (`635ce22`), and a runtime capability profile test (`dceec02`). These commits are not yet considered validated until the CI for the latest HEAD completes.
- The module-missing failures in run #74 were from the earlier head before the module was added; the next run reached tests, proving dependency restoration and module import progressed. The current blocking failures are the functional regressions listed above.
- Keep PR #88 draft/unmerged until all required gate jobs pass and CodeRabbit review of the latest HEAD is checked. Windows startup, durable mission execution, restart recovery, cockpit independence and EXE packaging remain separate, unproven checks.


## Latest CodeRabbit findings and CI dispatch limitation — 2026-10-18

- CodeRabbit findings were checked against the branch and both valid findings were fixed: removed all three unused `DGM_CONTRACTS_READ_TOKEN` env entries from `.github/workflows/backend-phase-gate.yml`; added `GET /governance/runtime-capabilities` to `ROUTE_CLASSIFICATIONS` with `SecurityScope.OPERATOR`. Both review threads were replied to and resolved after the changes.
- Other PR branch fixes currently include: explicit control-character rejection for target paths; explicit `status: failed` in mission failure results; updating the recovery regression expectation to reflect that planning without a generic executor is not successful execution; adding a unit test for the runtime capability profile; removing an unused import; and hardening auth classification fallback.
- Latest observed PR #88 HEAD: `fd23dbb75ee696208ec0a6bd55234f03ec78ca6c`. PR remains draft/open/unmerged.
- The last full Backend Phase Gate run observed was run #79 (`39125697595`), which started before the latest auth classification change and failed its mission/API and auth/governed-execution jobs. Other jobs shown in that run passed, but this is not validation of the latest HEAD.
- Attempted to dispatch the Backend Phase Gate through the browser, but the browser session was not authenticated (GitHub displayed Sign in); no workflow was dispatched and no repository changes were made by that attempt. The GitHub integration also did not report a workflow run for the latest HEAD at the time of this checkpoint. Owner-side authenticated dispatch/recheck is needed.
- CodeRabbit's valid findings are fixed, but its re-review requests were rate-limited / incremental after several rapid commits. Do not claim a final CodeRabbit review of the latest HEAD until the bot posts one for that revision.
- **Do not merge PR #88 yet.** Next gate: run the full Backend Phase Gate on the exact latest HEAD, inspect all jobs/logs, address any remaining failures, then recheck CodeRabbit. Windows startup, real durable mission consumption, restart recovery, cockpit independence and EXE packaging still require separate evidence.
