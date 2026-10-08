# DGM-MAT — Governance Bootstrap / Self-Audit Foundation
Date: 2026-10-08

## Decision

The portfolio audit must be performed by DGM-MAT itself. External manual auditing by the assistant is now limited to bootstrapping and validating DGM-MAT; the long-term authority for repository discovery, classification, grouping proposals, repair planning and controlled execution is DGM-MAT.

## Implemented in DGM-MAT

Commit: 07a5a3f — feat(governance): add DGM self-audit and controlled self-repair

Added:
- core/repository_intelligence/portfolio_auditor.py
- core/self_healing/self_repair_engine.py
- core/api/governance_api.py
- tests/repository_intelligence/test_portfolio_auditor.py

Integrated:
- governance router into the DGM-MAT API
- README updated with the operating model and boundaries

## Capabilities now exposed

Read-only:
- GET /governance/audit/self
- GET /governance/audit/workspace
- GET /governance/repair/self/plan

Controlled:
- POST /governance/repair/self/apply
- explicit confirm=true required
- safe self-test may run automatically
- structural repository changes remain approval-gated

The auditor currently observes:
- local existence and Git repository state
- origin
- branch
- commit count
- dirty state
- file count
- languages and manifests
- README/purpose
- classification
- logical project group
- relationships
- protected paths
- risks
- recommended action
- confidence
- optional read-only GitHub metadata

## Safety boundary

DGM-MAT-FULL-MIRROR remains frozen/protected.

The audit layer is read-only and never:
- moves repositories
- deletes repositories
- renames repositories
- changes remotes
- commits/pushes
- triggers external workflows

Those operations belong to a later governed execution layer with explicit approval and validation.

## Validation

- repository-auditor unit tests: 2 passed
- DGM-MAT headless runtime: reached bootstrap complete / all systems nominal
- API /health: healthy
- /governance/audit/self: operational
- /governance/audit/workspace?limit=3: operational
- self-repair plan: operational

## Next architecture step

Do not continue the manual portfolio audit as the primary mechanism.

Next work should make DGM-MAT's own governance/execution layer capable of:
1. full bounded portfolio audit
2. evidence-backed relationship/lineage analysis
3. project-family grouping proposals
4. repair plans
5. approval-gated structural operations
6. validation after every mutation
7. persistent audit/decision records in andreos-memory

External/clone/lab repositories follow:
UPSTREAM/CLONE -> STUDY -> AUDIT -> EXTRACT CONCEPT -> REIMPLEMENT/ADAPT -> VALIDATE -> PRODUCT

DGM-MAT is the current authority for the God Mode / AI-DevOps / multi-agent engineering family.
