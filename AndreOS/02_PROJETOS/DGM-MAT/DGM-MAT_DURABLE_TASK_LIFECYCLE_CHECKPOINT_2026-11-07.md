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


## Local coding agents and browser send hardening — 2026-11-07

### Local Codex / Claude Code CLI readiness

- PR #265 merged: `07e4487db34d9dc1f290ea1cfc5727a9351e694c`. Adds a read-only fixed CLI probe and OFFLINE/read-only office roles `agent:codex-cli` and `agent:claude-code-cli`.
- PR #267 merged: `fba69c7152dd57a4ebbb5f3f2b3981b2c251bb3c`. Existing operator-only `/governance/agents/readiness` now reports Codex CLI version presence, Claude Code auth status and FCC free inference status in separate fields. `fcc_inference_ready` is explicitly inference-only; local coding-agent execution remains false.
- PR #272 merged: `7140c6f79bee358d9567bb073788fb828c0aaa64`. The local probe supports Windows `%APPDATA%/npm/*.ps1` and `.cmd` wrappers with fixed `--version`, noninteractive/no-profile PowerShell, `cmd.exe /d /c`, bounded timeout and fail-closed interpreter checks.
- Exact-head focused CI: PR #265 run `42357604402` SUCCESS; PR #267 run `42357853427` SUCCESS; PR #272 run `42358160440` SUCCESS.
- No CLI task execution is enabled. Codex authentication/provider/model identity/free billing remain unverified. Claude auth status is reported separately; no secrets are returned.

### Browser send boundary

- PR #268 merged: `b4267a8dc47f077fd24499a0533be48704304073`. Adds actual content-script task E2E fixtures.
- PR #271 merged: `b60a8e42a131da4d3c558b5c01b9227356db7c41`. Removes the popup direct-send composer and `DGM_SEND_MESSAGE` listener. A local `window.confirm()` is not a durable approval. Only server-claimed `DGM_EXECUTE_BROWSER_TASK` can send.
- PR #273 merged: `688e057361f02f894f959138a55aeceb192e5b8a`. Restores both complementary CI fixtures after #271: reject direct send and validate the approved task path.
- PR #273 Chrome Extension Validation `42358330665`: SUCCESS, including both tests, Bandit, browser/API regressions and extension packaging.
- PR #270 was closed as superseded by #272.

### Latest Windows build after local CLI wrapper merge

- Run `42358240899`, head `7140c6f79bee358d9567bb073788fb828c0aaa64`, was in progress when this checkpoint was written.
- This build includes Vault (#263), local CLI probe (#265/#267/#272), browser direct-send removal (#271) and the five-provider browser operator.
- Do not use the older PR #263 artifact as the final latest build once this run completes; update the checkpoint with the new artifact SHA-256 and artifact ID.

### Mutation executor status

PR #220 remains a draft by design. It has exact-head Windows Guard evidence (38 passed, 8 POSIX-only skipped) and focused CI success, but local Windows acceptance is still open: backup-root ACL, namespace durability after abrupt power loss, create/replace, rollback, prepared-state recovery and concurrent-writer rejection. Do not merge or connect it to MissionEngine until these gates pass on the actual Windows host.


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


## Follow-up checkpoint — local probe merged and browser task coverage (2026-11-07)

### Local Codex/Claude Code probe merged
- PR #265 merged as `07e4487db34d9dc1f290ea1cfc5727a9351e694c` (head `56d17556b3f68ac75ff659863d9a595049d6f8b3`).
- Exact-head Focused PR Validation run `42357604402`: SUCCESS. The affected regression selection, dependency installation and selected pytest step all completed successfully.
- Probe is read-only: fixed Codex/Claude CLI IDs, `--version` only, bounded timeout, `shell=False`, temporary cwd, minimal environment, endpoint variable names only. No task execution, credential reads, identity/billing/free-tier assertions, or source mutation.
- Codex and Claude profiles remain OFFLINE / ROLE_DEFINED_ONLY until the real Windows host and FCC/NVIDIA NIM route are verified.

### Focused CI efficiency fix merged
- PR #266 merged as `c1747880255881571090bab2441e6b5a8ad7232a`.
- Qt system packages are now installed only when selected regression files actually contain GUI markers (`PySide6`, `PyQt`, `QApplication`, `qtbot`, `pytestqt`).
- Exact workflow validation run `42357790832`: SUCCESS; because the PR changed only the workflow, no Python regressions were selected, and source compilation passed.
- This removes unnecessary apt/Qt installation from non-GUI PRs such as the local coding-agent probe.

### Browser task content-script coverage — PR #268 open
- Branch `test/browser-operator-content-task-e2e`, head `f80b0eb59e2999d3e3cf89780f3f8ae18209ce44`.
- Adds deterministic Node tests that execute the real `DGM_EXECUTE_BROWSER_TASK` content-script handler.
- Scenarios: successful send + stable assistant response; provider mismatch; conversation mismatch; rate-limit block; unverified user send; assistant timeout. Failure/unverified scenarios assert no automatic resend.
- Chrome Extension Validation run `42357937274` and Focused PR Validation run `42357937221` were queued at checkpoint creation; do not merge until exact-head validations finish successfully.

### Housekeeping
- PR #258 stale task-persistence gap documentation closed (not merged) after #259–#261 implemented durable task lifecycle.
- PR #222 and #233 closed as superseded (not merged). The current main already has the server-approved browser task queue and visible-UI content-script task handler. The old popup-only sending path was not carried forward because it lacked the durable server mission/task approval contract.
- PR #40 and PR #42 in AndreOS Memory are merged; this checkpoint is the next continuity update.

### Next gates
1. Validate and merge PR #268 only after its exact-head browser-extension and focused CI pass.
2. Continue integrating browser action evidence with the durable task lifecycle; distinguish completed, blocked, failed and unverified, never retry an unverified send automatically.
3. Review PR #220's native Windows backup-first executor as a separate candidate; it remains 27 commits behind and must not be merged wholesale while Windows acceptance is pending.
4. On 2026-11-09, back up current installation/runtime, measure host resources, validate Vault migration/restart persistence, test all three read-only specialists and durable task receipts, and run the local Codex/Claude/FCC readiness probe.
5. Keep code mutation disabled until task-specific approval, isolated worktrees, exact patch digest, independent QA and rollback are proven.


## Follow-up checkpoint — browser approval hardening and local CLI probe (2026-11-07)

### Merged
- PR #265 `07e4487db34d9dc1f290ea1cfc5727a9351e694c`: read-only Codex/Claude Code CLI readiness probe. Exact-head Focused PR Validation `42357604402` SUCCESS, including selected regression execution. Execution disabled; identity/billing/FCC route remain unverified.
- PR #266 `c1747880255881571090bab2441e6b5a8ad7232a`: focused CI installs Qt only for selected GUI tests. Workflow run `42357790832` SUCCESS; no Python regressions were selected because only workflow logic changed.
- PR #268 `b4267a8dc47f077fd24499a0533be48704304073`: end-to-end deterministic tests for actual browser task content-script execution. Chrome Extension Validation `42358015160` SUCCESS; Focused PR Validation `42358015196` SUCCESS.
- PR #271 `b60a8e42a131da4d3c558b5c01b9227356db7c41`: removed unaudited direct popup send route. Content script now sends only via `DGM_EXECUTE_BROWSER_TASK` from the server-claimed task queue. Chrome Extension Validation `42358142300` SUCCESS; direct-send bypass fixture passed; Focused PR Validation `42358142142` SUCCESS.

### Browser task execution contract
The content script now has deterministic coverage for provider mismatch, conversation mismatch, quota/rate-limit block, visible user-message confirmation, stable assistant response, unverified send and assistant timeout. Unverified sends are never automatically replayed. Popup direct sending has been removed; all sends must enter through the durable server-side mission/task approval and audit path.

### Local Windows CLI wrappers — PR #272 open
The read-only probe is being extended to detect npm `.ps1`/`.cmd` shims under `%APPDATA%\\npm`. A review comment requires safe `cmd.exe /s /c` quoting and a regression with a path containing spaces and `&`; do not merge until this is fixed and exact-head CI passes. No prompts, credentials or model requests; coding-agent task execution remains disabled.

### Windows patch executor
PR #220 remains open and 27 commits behind. Native Windows handle-based backup-first mutation still requires review of backup-root ACL inheritance, power-loss durability guarantees, and real Windows 10 create/replace/rollback/concurrent-writer tests. It is not wired into MissionEngine and must remain disabled until host acceptance.

### Host boundary
The operator PC remains offline until 2026-11-09. No local install, FCC/NVIDIA NIM route identity, free quota, authenticated browser provider, Vault migration or Windows task/receipt crash recovery is claimed.

### Next gates
1. Review/fix PR #272's `.cmd` command-line quoting and merge only after exact-head tests pass.
2. Keep browser sends on the server-approved queue; continue audit evidence and visible response validation.
3. Review PR #220 separately; do not merge wholesale while the Windows acceptance gates are open.
4. On 2026-11-09, back up current installation/runtime, measure actual CPU/RAM/disk, validate Vault migration and restart persistence, test all read-only specialists and task receipts, and inspect FCC/Codex/Claude readiness without exposing secrets.
5. Keep source mutation disabled until isolated worktrees, exact patch approvals, independent QA and rollback are proven.


## Follow-up checkpoint — Windows CLI wrapper hardening (2026-11-07)

### PR #272 merged, PR #274 corrective hardening merged
- PR #272 merged as `7140c6f79bee358d9567bb073788fb828c0aaa64`; Focused CI `42358160440` SUCCESS. It added detection for Windows npm `.ps1`/`.cmd` shims.
- Post-merge review identified that `.cmd` invocation via `cmd.exe /d /c` with an unquoted path could expose command-tail parsing despite `shell=False`.
- PR #274 merged as `9b8c61cca942bedfc2112ac7033875f536a52af1`; Focused PR Validation `42358445492` SUCCESS, including selected Python regression execution.
- Corrected policy: `.cmd`/`.bat` wrappers are detected but never launched. Prefer `.ps1` (fixed PowerShell `-File`, no profile/noninteractive) or `.exe`. If only `.cmd` exists, report `version_probe_unavailable` / `cmd_wrapper_not_executed_for_safety` and do not start a process. Regression uses an APPDATA path containing `&` and asserts no subprocess launch.
- Local CLI task execution remains disabled; this is version discovery only. No prompt, credentials, identity, FCC route or billing claim.

### Windows artifacts
- PR #271 mainline build `42358215841`: SUCCESS, commit `b60a8e42a131da4d3c558b5c01b9227356db7c41`; artifact `DGM-MAT-Windows-3.12-b60a8e4`, ID `13568906155`, 111,214,099 bytes, expires 2027-02-05. Contains browser direct-send approval hardening; predates PR #274.
- Fresh build for current main after PR #274: run `42358509993`, queued at checkpoint update. Do not claim the prior artifact contains the latest CLI wrapper correction.

### Remaining gates
1. Verify the current-main post-PR-274 Windows build and artifact.
2. Keep PR #220 unmerged; native Windows backup-first mutation still needs independent security review and real Windows 10 acceptance.
3. On 2026-11-09, back up existing install/runtime, measure host, validate Vault migration/reopen/restart, read-only specialist dispatch, task/receipt recovery and FCC/Codex/Claude readiness.
4. Keep local coding-agent task execution and source mutation disabled until route/free-tier identity, isolated worktrees, task-specific approvals, independent QA and rollback are proven.
