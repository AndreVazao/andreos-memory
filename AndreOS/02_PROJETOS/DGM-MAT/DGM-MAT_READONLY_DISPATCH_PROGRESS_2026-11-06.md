# DGM-MAT — read-only specialist dispatch progress 2026-11-06

## Merged work

DGM-MAT PRs #246, #247, #249, #250, #253, #254 and #255 are merged.

- #246: engineering team planner (22 focused tests passed).
- #247: read-only Repository Cartographer (23 focused tests passed).
- #249: safe roster profile reconciliation (5 focused tests passed).
- #250: handler/capability-aware delegation (9 focused tests passed).
- #253: clean mainline integration of Python Source Analyst.
- #254: explicit operator-configured registration in MissionEngine; Focused PR Validation run 42307675986 succeeded.
- #255: Python Test Inventory specialist and bootstrap extension; Focused PR Validation run 42307981234 succeeded.

The 59 tests previously recorded apply to #246/#247/#249/#250 only. #254 and #255 have separate successful focused CI runs. No full-suite or Windows acceptance is claimed.

## New dispatch increment

DGM-MAT PR #256:
https://github.com/AndreVazao/DGM-MAT/pull/256

Adds `ReadOnlyWorkerOrchestrator` and `MissionEngine.run_readonly_repository_worker`, which route fixed, bounded operations to the three registered read-only specialists through the existing durable SQLite InternalMessageBus.

- Fixed agent/operation/capability map.
- Inputs are agent ID, allowlisted repository ID, mission ID and correlation ID; no path or shell command accepted.
- Handler registration and declared capabilities are required.
- Deterministic message IDs support idempotent retries.
- Completed results are returned from durable dispatch receipts.
- If an older inbox message is dispatched first, the current request is accurately reported as QUEUED.
- Adds end-to-end tests for all three workers, receipts, idempotency, unregistered workers and queue ordering.

At this checkpoint PR #256 is open. Focused PR Validation run 42308361804 is in progress; Python compilation and test selection completed, dependency installation is still running. No CI pass or merge is claimed for #256 yet.

## Current safety boundary

Three specialists remain read-only and opt-in through:
- DGM_READ_ONLY_WORKSPACE_ROOT
- DGM_READ_ONLY_REPOSITORIES (JSON stable-ID to relative-path mapping)

They do not execute source, run tests, call shell, modify files, access network or invoke external AI. A durable worker receipt proves that the bounded handler invocation returned; it is not independent verification of its findings.

## Next gates

1. Finish #256 CI; merge only after success.
2. Connect worker dispatch to AgentRegistry/DelegationEngine and durable task contracts without creating a parallel task store.
3. Add task evidence states: configured, handler-registered, smoke-tested, task-validated.
4. On PC reconnect, test DGM-MAT-only allowlist, restart/recovery, permissions and all three real repository tasks.
5. Then add isolated patch proposals using existing worktree and approval infrastructure.
