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


## Browser Operator approval boundary — PR #262 merged

URL: https://github.com/AndreVazao/DGM-MAT/pull/262  
Merge commit: `94923b7822316920400cf66cc3596a36579f1b2f`  
Merged head: `0d21e93042401ee7fafed1c6c5b858b1a7f8f030)

Exact-head CI:
- Focused PR Validation `42356417227`: SUCCESS.
- Chrome Extension Validation `42356417324`: SUCCESS.
- Windows Executable Build `42356491067`: SUCCESS, deep executable validation and artifact upload.

Windows artifact:
- `DGM-MAT-Windows-3.12-94923b7`
- 111,175,585 bytes
- SHA-256 `a6da15990524d8b283dd7d1f63e0d04b8430d5672f14f4f80f1f902a06cd0aa9`
- Artifact ID `13567468532`, expires 2027-02-05.
- Run: https://github.com/AndreVazao/DGM-MAT/actions/runs/42356491067

The direct browser task endpoint no longer accepts client-controlled `approval_required`; explicit per-task approval is mandatory there. Mission-specific automatic sending requires a fresh durable parent checkpoint in RUNNING state. The SQLite queue rechecks the parent immediately before claim, binds approval policy into idempotency, and moves missing/terminal parent tasks to review. Old PR #236 was closed as superseded, not merged.

This is CI/build evidence only. No installation or authenticated provider acceptance on the operator PC is claimed.

## Persistent Vault — PR #263 merged

URL: https://github.com/AndreVazao/DGM-MAT/pull/263  
Merge commit: `f02164ac5df95768b8d7e82e3b4822072ef67489`  
Merged head: `a12758970da3dd7fe6f2702b1e24988b89e7946b`  
Focused CI run: `42357038993` — SUCCESS.  
Chrome Extension Validation: `42357038961` — SUCCESS.

The clean replacement is based on current main and ports the persistent SQLite Vault, raw/normalized conversation archive, Chrome importer, mobile/runtime path alignment, legacy runtime migration, repository snapshots and explicit sync command. Startup bootstrap is opt-in (default OFF) until real Windows performance/persistence acceptance. Provider oldest-boundary evidence remains intentionally empty; hash integrity is not proof of complete history. Explicit zero message counts and actual unknown-role counts are treated as incomplete.

Windows build for the post-Vault main commit: run `42357103463` — **SUCCESS**. Artifact `DGM-MAT-Windows-3.12-f02164a`, 111,211,529 bytes, SHA-256 `1a83a48b83e3453f92f82315cb7f0ee7bc5adb8e08a17cbbe272972728e69380`, artifact ID `13568108257`, expires 2027-02-05. This is the first Windows artifact containing Vault integration; the earlier PR #262 artifact predates Vault. Build success is not local installation acceptance.


## Local coding-agent/operator context architecture — PR #264 merged

URL: https://github.com/AndreVazao/DGM-MAT/pull/264  
Merge commit: `54c3abff83941fcc9162a91a0a4e4b848aa2b09c`.

Added `docs/architecture/LOCAL_AGENTS_AND_OPERATOR_ADAPTIVE_CONTEXT_2026-11-06.md`, including the 2026-11-07 follow-up status. It distinguishes local CLI coding agents (Codex/Claude Code via FCC/NVIDIA NIM) from browser AI consultation (ChatGPT/Grok/Gemini/DeepSeek/Qwen), and defines operator-adaptive context, provenance, isolated worktrees, independent QA and Monday acceptance gates. PR #243 was closed as superseded by #264.

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

1. Back up the current installation/runtime, then install only artifact `DGM-MAT-Windows-3.12-f02164a` after verifying SHA-256.
2. Measure actual CPU/RAM/disk; validate Vault path alignment, legacy runtime migration, startup resource usage (bootstrap disabled by default), and real capture/reopen/restart persistence.
3. Validate the three read-only specialists on real allowlisted repositories and reconcile task/worker receipts after process restart.
4. Verify Codex/Claude Code CLI identity, listener scope, model/provider, free/quota behavior and tool permissions on the actual PC.
5. Validate authenticated visible-UI browser consultation for ChatGPT, Grok, Gemini, DeepSeek and Qwen without cookies/tokens or MFA/CAPTCHA bypass.
6. Add independent review/bug-hunt/QA workflow using separate responsibilities; agents must not approve their own changes as the only reviewer.
7. Only after the read-only lifecycle is proven should the Windows backup-first executor be connected to a bounded patch worker.

## Continuity rule

For future sessions, read this checkpoint together with:
- `DGM-MAT_OFFICE_READINESS_CHECKPOINT_2026-11-06.md`
- `DGM-MAT_SELF_EVOLUTION_CHECKPOINT_2026-11-06.md`
- `DGM-MAT_TASK_PERSISTENCE_AND_SECURITY_CHECKPOINT_2026-11-07.md`
- DGM-MAT issue #245 and the current PR/CI states linked above.

This checkpoint is a project state record, not evidence that unverified work has completed.


## Follow-up checkpoint — post-Vault build and local agent probe (2026-11-07)

### Post-Vault Windows build
- Workflow run `42357103463`: SUCCESS on exact main commit `f02164ac5df95768b8d7e82e3b4822072ef67489`.
- Artifact `DGM-MAT-Windows-3.12-f02164a`, ID `13568108257`, size `111211529` bytes, expires `2027-02-05T08:49:30Z`.
- Build included the persistent Vault integration and passed deep executable validation and artifact upload.
- This is CI/build evidence only; no local installation acceptance is claimed.

### Local coding-agent readiness probe — PR #265 open
- Branch `feat/local-coding-agent-readiness-probe-v1`, head `65013d80f656a04424140c6b597b5b15a7167920`.
- Adds read-only discovery of Codex CLI and Claude Code CLI; only fixed `--version` invocations, bounded timeout, `shell=False`, temporary cwd, minimal environment, bounded output.
- Reports endpoint environment variable names only; never values, credential files, task prompts or source modifications.
- Identity, billing, FCC route and free quota remain unverified; execution stays disabled.
- Focused CI run `42357542481` was cancelled during dependency installation on two attempts; the selected regression tests did not complete. PR remains open/unmerged until a clean exact-head run passes.

### Browser write capability gate
- PR #233 was closed as superseded, not merged. Its extension popup send implementation only used a local browser confirmation and was not bound to the durable server-approved mission/task queue.
- Visible-UI send capability remains required, but must be implemented against the current task approval queue with provider/conversation identity checks, audit evidence and explicit handling of `submitted_unverified`; no automatic retry.
- PR #222 closed as superseded by current main's virtualized capture and Vault integration.
- PR #258 closed as stale documentation because task persistence and MissionEngine wiring were implemented by #259–#261.

### Current host boundary
The operator PC remains offline until 2026-11-09. Do not claim installation, FCC/NVIDIA NIM route identity, Codex/Claude availability, authenticated provider operation, Vault migration, or Windows task crash-recovery until measured and tested on the host.

### Next gates
1. Obtain one clean exact-head CI pass for PR #265; merge only after tests actually execute and pass.
2. Design the browser extension's visible-UI send adapter as a server-approved task operation, not a popup-only local action.
3. Review the old Windows executor PR #220 as a candidate for selective porting; it is 27 commits behind and must not be merged wholesale.
4. On 2026-11-09, back up the current installation/runtime, measure host resources, validate Vault persistence/migration and all read-only specialists, then test task/receipt restart recovery.
5. Keep code mutation disabled until isolated worktrees, exact patch approvals, independent QA and rollback are proven.
