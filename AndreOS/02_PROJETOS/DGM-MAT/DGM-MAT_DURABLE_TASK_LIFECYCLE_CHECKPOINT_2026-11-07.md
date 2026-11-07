# DGM-MAT — Durable Organization Task Lifecycle Checkpoint

**Date:** 2026-11-07  
**Project:** AndreVazao/DGM-MAT  
**Primary continuity issue:** https://github.com/AndreVazao/DGM-MAT/issues/245

## Strategic direction

DGM-MAT is being advanced toward a governed internal engineering organization. It must eventually take bounded engineering tasks, recover project context, select internal specialists, work in isolation, test, obtain independent review, create traceable PRs and recover after interruption. Codex Free and Claude Code Free remain optional consultants/fallbacks, not mandatory runtime dependencies.

Safety invariants remain:
- evidence before assumptions; inspect before changing;
- stability over feature count;
- preserve existing code/data before migration or cleanup;
- no unrestricted self-modification, silent merge, destructive cleanup or hidden credential access;
- free/local-first by default;
- model/agent output is untrusted until independently validated;
- no local acceptance claim without a real PC test.

## Completed in this increment

### PR #259 — merged

URL: https://github.com/AndreVazao/DGM-MAT/pull/259  
Merge commit: `42be7164a99e79b2a3fddac3cae5d341c38a8bb7`  
Focused CI run: `42355370414` — SUCCESS on exact PR head.

Added durable task records to the existing `InternalMessageBus` SQLite database:
- versioned `organization_tasks` table; no parallel task database;
- complete task envelope persistence (mission, title/description, ownership, assignee, status, priority, dependencies, inputs/outputs, evidence, approval fields, retry policy, metadata, timestamps);
- create, assignment and lifecycle transition persistence;
- optimistic revisions reject stale concurrent writers;
- duplicate task IDs cannot overwrite records; identical insert retries are idempotent;
- malformed and unsupported schema records fail closed and remain stored for inspection;
- no-bus mode remains in-memory for isolated tests;
- returned tasks are detached copies.

New tests cover restart/reopen, dependency and assignment recovery, transition recovery, duplicate IDs, stale-writer conflict, malformed-record retention, unsupported schema retention and detached-copy isolation.

### PR #260 — MissionEngine integration under review

URL: https://github.com/AndreVazao/DGM-MAT/pull/260  
Head at creation: `e6e6dfa5291d45dd8581dad8f90a0fb031cc89e9`  
Focused CI run: `42355510679` — running on the latest exact PR head `e4e37f9455dd221e86e47c6a0693897ece1f92c0`; an earlier run `42355488150` was cancelled when the documentation commit updated the PR head.

Proposed integration:
- MissionEngine constructs exactly one `OrganizationTaskManager` using its existing `organization_bus`.
- One `DelegationEngine` uses the existing office registry and `WorkerRuntime`.
- bounded create/get/delegate methods are exposed;
- delegation only assigns to a registered worker whose declared capabilities, skills, department and permissions match;
- task descriptions are never interpreted as executable instructions;
- readiness distinguishes durable SQLite from memory-only injected test mode and continues to report `task_validated=false`.

Added integration tests for MissionEngine restart/reopen and capability-gated delegation. Added architecture document:
`docs/architecture/ORGANIZATION_TASK_LIFECYCLE_V1.md`.

Do not claim this integration is merged until PR #260 is reviewed and its exact-head CI succeeds.

### PR #261 — typed read-only task dispatch merged

URL: https://github.com/AndreVazao/DGM-MAT/pull/261  
Merge commit: `36ed349a9444b3d55cc115d0fc5200879d52b751`  
Merged head: `8d6cb91d1db9cde414b2c1f10c3b899ece3d5206`  
Focused CI run: `42355811617` — **SUCCESS** on exact PR head.

Implemented the fixed task-kind map for repository inventory, Python source analysis and Python test inventory. The dispatcher checks ASSIGNED state, exact agent mapping, current DelegationEngine eligibility and handler capabilities. Worker messages carry task_id. A task is completed only after a durable receipt is confirmed; receipt ID and result are persisted. A retry after a crash between receipt and task update receives ALREADY_COMPLETED and finalizes without rerunning the worker. Unknown task kinds, mismatched agents, unassigned tasks and unverified results fail closed.

Added `docs/architecture/ORGANIZATION_TYPED_TASK_DISPATCH_V1.md`. This is still read-only work; it does not enable shell, imports, test execution, network or code mutation.

## Existing specialist workforce status

The three read-only specialists remain:
1. `agent:repository-cartographer`
2. `agent:python-source-analyst`
3. `agent:python-test-inventory`

They are only activated when the host explicitly configures the workspace root and repository allowlist. Their work remains metadata/AST/test-inventory only; no repository code execution, shell, network, or mutation. They have not yet been accepted on the operator PC.

## Security blocker — PR #236

URL: https://github.com/AndreVazao/DGM-MAT/pull/236

Keep unmerged. The direct `POST /browser-operator/tasks` route still accepts client-controlled `approval_required=false` and forwards it to the queue without a fresh server-side parent-mission state check. This can bypass the intended explicit approval gate. Required fix:
- enforce approval in a shared service/queue boundary, not just a route;
- validate parent mission state server-side;
- test pending, running, completed, cancelled, failed and missing missions through both route entry points;
- prevent idempotent resubmission from changing approval state.
No live-runtime exploit test is claimed; this is a code-level review finding.

## PC acceptance

The operator PC is offline until 2026-11-09. Do not configure allowlists, execute local workers or claim Windows acceptance before then.

When online:
1. profile actual CPU/RAM/disk and inspect the active installation;
2. verify the persistent SQLite path and permissions;
3. create/reopen/assign/transition a test task and restart DGM-MAT;
4. run one allowlisted repository inventory, one Python source analysis and one test inventory;
5. compare results to manual inspection;
6. test stale-process recovery, task/receipt reconciliation and database backup;
7. keep all code mutation disabled until isolated worktree, exact-digest approval, test and rollback gates are accepted.

## Next engineering sequence

1. Add independent review/bug-hunt/QA workflow using separate responsibilities; agents must not approve their own changes as the only reviewer.
2. Fix the server-side approval bypass in browser-operator PR #236 before merging/enabling browser sends.
3. Review PR #238 Vault carefully before any merge; its history-boundary and startup/bootstrap concurrency questions remain separate from organization task persistence.
4. On 2026-11-09, run PC acceptance and record exact commands, results, environment and limitations.
5. Reconcile task/worker receipts under real process restart and concurrent manager tests on Windows.
6. Only after the read-only lifecycle is proven should the Windows backup-first executor be connected to a bounded patch worker.

## Continuity rule

For future sessions, read this checkpoint together with:
- `DGM-MAT_OFFICE_READINESS_CHECKPOINT_2026-11-06.md`
- `DGM-MAT_SELF_EVOLUTION_CHECKPOINT_2026-11-06.md`
- `DGM-MAT_TASK_PERSISTENCE_AND_SECURITY_CHECKPOINT_2026-11-07.md`
- DGM-MAT issue #245 and the current PR/CI states linked above.

This checkpoint is a project state record, not evidence that unverified work has completed.
