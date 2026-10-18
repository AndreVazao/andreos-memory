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
| `DGM-MAT-Memory` | DELETE CANDIDATE | Generic stub and duplicate concept; canonical persistent memory is `andreos-memory`. Replace README with explicit delete notice after checking branch history/consumers. |
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
- Delete-review notices committed to `DGM-MAT-Cluster`, `DGM-MAT-Media`, `DGM-MAT-Studio`, `DGM-MAT-Memory`, `DGM-MAT-Marketplace`, `DGM-Core-Backend`, and `DGM-Docs`. These repositories were not deleted. The owner should manually verify branches/issues/consumers/history and then delete them.
- Keep `DGM-MAT-OS`, `DGM-Experimental`, `DGM-MAT-Runtime`, `DGM-MAT-Orchestrator`, `DGM-MAT-Assets`, `DGM-MAT-Plugins`, `DGM-MAT-Providers`, and `DGM-MAT-Connectors` in REVIEW until their full trees, histories and consumers are audited. Do not call them safe to delete based on size alone.
