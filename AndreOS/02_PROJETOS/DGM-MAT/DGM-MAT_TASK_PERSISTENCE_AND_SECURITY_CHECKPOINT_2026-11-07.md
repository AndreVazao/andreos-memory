# DGM-MAT — task persistence and browser approval checkpoint 2026-11-07

## Session constraints

- GitHub-only work because the operator PC is offline until Monday 2026-11-09.
- No local Windows runtime, browser session, authenticated provider UI, workspace allowlist or real worker execution was tested or changed.

## Verified current main state

- `OrganizationTaskManager` (`core/organization/task_manager.py`) is process-local: Python dictionary + RLock, with no persistence or reload contract.
- `InternalMessageBus` (`core/organization/message_bus.py`) already provides SQLite persistence for organization messages and dispatch receipts.
- `WorkerRuntime` persists handler result receipts and message acknowledgement atomically through the bus.
- `ReadOnlyWorkerOrchestrator` sends bounded fixed-operation requests with deterministic IDs through the bus.
- `DelegationEngine` checks handler registration and declared capabilities, but task assignment is only stored in the in-memory manager.
- No production MissionEngine construction/use of `OrganizationTaskManager` was found by default-branch search.
- Therefore message/receipt durability does not imply task lifecycle durability. A restart may preserve a dispatch receipt while losing the task object, assignment and task status.

## DGM-MAT PR #258

- PR: https://github.com/AndreVazao/DGM-MAT/pull/258
- Branch: `docs/organization-task-persistence-gate-2026-11-07`
- Commit: `3e38ef43e1a726d75a3be3853b922046b3a2eb06`
- Adds `docs/architecture/ORGANIZATION_TASK_PERSISTENCE_GATE_2026-11-07.md`.
- Documentation only, 53 lines added; compare confirms exactly one file and branch is 1 commit ahead, 0 behind main.
- At checkpoint creation, no PR-triggered workflow run was returned; combined status contained only Snyk error due quota/unavailability. PR metadata reports mergeable=true. Do not call this green CI and do not claim it is merged.

## Blocking security finding on DGM-MAT PR #236

- `BrowserOperatorTaskCreate.approval_required` is client-controlled and forwarded directly to `BrowserOperatorQueue.enqueue()`.
- An authenticated local operator can send `approval_required=false`, causing immediate queue status instead of `pending_approval`.
- The endpoint does not enforce the PR's claimed RUNNING-parent-mission condition server-side.
- Blocking comment added to PR #236, requiring server-side approval enforcement and negative tests for false, missing, non-running and terminal missions.
- PR #236 remains open and must not be merged until fixed and tested on exact head.

## Other open PRs checked

- #220 — backup-first Windows executor, draft; Windows acceptance and independent review pending.
- #235 — virtualized browser history capture; authenticated UI acceptance pending.
- #236 — browser mission queue; approval bypass finding above.
- #238 — persistent Vault catalogue and project trees; bootstrap concurrency/history completeness review pending.
- #239 — DeepSeek/Qwen adapters; dependent on #235 and manual UI acceptance pending.
- #243 — local coding agents/adaptive context docs; PC acceptance pending.
- #258 — organization task persistence gate docs; no green workflow evidence at checkpoint.
- PRs #246/#247/#249/#250/#253/#254/#255/#256/#257 were previously recorded as merged; re-check current state when needed.

## Next implementation sequence

1. Extend the existing InternalMessageBus SQLite database/API with versioned task records; do not create a parallel task DB.
2. Persist complete Task envelopes and create/assign/transition operations transactionally.
3. Reload and validate tasks on manager reconstruction; malformed/unknown schema records fail closed and remain inspectable.
4. Add restart/reopen, conflicting ID, dependency, assignment, transition and malformed-record tests.
5. Wire one MissionEngine-owned task manager and DelegationEngine, then add fixed task-to-worker dispatch through existing worker handlers.
6. Keep read-only specialists read-only. Code changes require isolated worktrees, backup-first execution, approval bound to exact patch digest, independent QA and rollback.
7. On 2026-11-09, profile the actual PC and validate one task per read-only worker with DGM-MAT-only allowlist, restart recovery and manual output comparison.

## Operator direction

Continue GitHub work while PC is offline. Update this memory and the DGM-MAT repository checkpoint after material milestones so a new conversation can resume without losing completed work, evidence, blockers or next steps.