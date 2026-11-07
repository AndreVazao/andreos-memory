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

### Latest Windows build after local CLI wrapper merge — SUCCESS

- Run `42358240899`, head `7140c6f79bee358d9567bb073788fb828c0aaa64`: SUCCESS through Build Executable, Deep Check, artifact preparation, final assertions and upload.
- Artifact `DGM-MAT-Windows-3.12-7140c6f`, 111,214,741 bytes, SHA-256 `015e08b97bbdf2952d9dfcda5cc9cfe1871090729745c0337973ab3724fcab26`, artifact ID `13568377573`, expires 2027-02-05.
- This build includes Vault (#263), local CLI probe and Windows npm wrappers (#265/#267/#272), browser direct-send removal (#271) and five-provider browser operator. PR #273 is test/docs-only and does not change the executable runtime.
- Build success is not installation or authenticated provider acceptance. Preserve the existing installation/runtime and verify the SHA-256 before replacement.


## Browser send regression coverage restored — PR #273 merged

URL: https://github.com/AndreVazao/DGM-MAT/pull/273  
Merge commit: `688e057361f02f894f959138a55aeceb192e5b8a`  
Chrome Extension Validation run `42358330665`: SUCCESS.

The extension CI now runs both:
- `test_message_send.js`: rejects the removed direct `DGM_SEND_MESSAGE` path without a callback or UI action.
- `test_browser_operator_task.js`: verifies the approved `DGM_EXECUTE_BROWSER_TASK` path, provider/conversation binding, visible send and blocked/unverified/timeout no-replay behavior.

PR #271 removed the popup composer and direct content-script listener; a local confirm is not a durable approval record. Only the server-claimed task path can send.

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


## Follow-up checkpoint — browser task tests and dual CLI wrapper hardening (2026-11-07)

### Browser task coverage restored
- PR #273 merged: `7c53f4eb0ea2aa824f8157dc11b5a1ef57250003`.
- Exact-head Chrome Extension Validation `42358330665`: SUCCESS.
- Exact-head Focused PR Validation `42358330658`: SUCCESS.
- The workflow now runs both complementary fixtures: `test_message_send.js` rejects the removed unapproved `DGM_SEND_MESSAGE` path; `test_browser_operator_task.js` exercises the approved `DGM_EXECUTE_BROWSER_TASK` path and validates identity, blocked, unverified and timeout outcomes.

### Windows coding-agent wrapper corrections
- PR #272 merged (PowerShell and npm shim detection), followed by corrective PR #274 merged as `9b8c61cca942bedfc2112ac7033875f536a52af1`.
- Exact-head Focused PR Validation `42358445492`: SUCCESS; selected regression tests executed.
- `.cmd`/`.bat` wrappers are detected but never launched, even with `shell=False`; `.ps1` uses fixed PowerShell `-NoLogo -NoProfile -NonInteractive -File`; `.exe` is invoked directly. If only a `.cmd` exists, readiness reports a detected-but-not-probed state and does not start a process.
- Current-main Windows executable build run `42358509993`: SUCCESS on commit `9b8c61cca942bedfc2112ac7033875f536a52af1`. Artifact `DGM-MAT-Windows-3.12-9b8c61c`, ID `13569096106`, 111,216,617 bytes, expires `2027-02-05T09:09:23Z`. This is a CI-built artifact; no local installation acceptance is claimed.

### Additional legacy Claude probe path — PR #275 open
- Audit found `core/development/external_agent_probe.py` still launched `claude.cmd` via `cmd.exe /d /c`, bypassing the safer shared local CLI probe policy.
- PR #275 changes the legacy auth-status probe to reject `.cmd`/`.bat` wrappers, run from the temporary directory with a minimal environment (process plumbing and user-profile paths only), and exclude inherited API-key/secret environment variables.
- First exact-head run `42358904900` failed because the regression exposed that the wrapper guard was Windows-only while the test ran on Linux. This was a genuine test finding, not ignored.
- Corrective commit `0a7808b40ff5eff263470ed84523b028e9dcdb5d` makes `.cmd`/`.bat` rejection host-independent. New exact-head Focused PR Validation run `42358986108` was in progress at checkpoint time. Do not merge PR #275 until that exact-head run completes successfully.
- No model prompts/requests or local coding-agent task execution are enabled by these readiness probes.

### Current mainline and host boundary
- Mainline at checkpoint: `9b8c61cca942bedfc2112ac7033875f536a52af1`.
- PR #220 remains open and must not be merged wholesale: native Windows backup-first mutation still needs independent review of backup-root ACL inheritance and power-loss durability, plus real Windows 10 create/replace/rollback/concurrent-writer acceptance. It is not integrated into MissionEngine.
- Operator PC remains offline until 2026-11-09. Do not claim local install, actual Codex/Claude CLI presence, FCC route identity, free quota, Vault migration/restart acceptance, browser-provider authentication or real task recovery until measured on host.

### Next actions
1. Wait for exact-head CI `42358986108`; fix any regression and merge #275 only after success.
2. Update this checkpoint again with #275 final state and exact CI evidence.
3. Keep PR #220 unmerged; continue only with isolated review and explicit host acceptance.
4. On 2026-11-09, back up existing install/runtime, measure host resources, validate Vault migration/restart, read-only specialists, durable task receipts and local CLI/FCC readiness. Do not expose secrets.
5. Keep coding-agent execution and source mutation disabled until free-route identity, isolated worktrees, task-specific approvals, independent QA and rollback are verified.

## Follow-up checkpoint — legacy Claude auth probe secured (2026-11-07)

- PR #275 merged as `c448bc5a28776b395e0dafc1c1fc5aed009af9df`.
- Exact-head Focused PR Validation `42358986108` on `0a7808b40ff5eff263470ed84523b028e9dcdb5d`: SUCCESS. Python compilation and selected regression tests completed; wrapper rejection and environment-isolation tests passed.
- The legacy `probe_claude_code()` path now rejects `.cmd`/`.bat` wrappers on every host rather than trying `cmd.exe /d /c`; it preserves PowerShell and direct executable paths.
- Auth-status inspection now runs from the temporary directory with a deliberately minimal environment: process plumbing and user-profile path variables only; inherited API-key/secret variables are not passed to the CLI.
- The first exact-head CI run `42358904900` failed on the newly added Linux regression because the `.cmd` guard was Windows-only. This was fixed in commit `0a7808b40ff5eff263470ed84523b028e9dcdb5d`; subsequent exact-head run passed. No failed CI was ignored.

### Mainline / build status
- Mainline is now `c448bc5a28776b395e0dafc1c1fc5aed009af9df`.
- New Windows executable build `42359050528` is queued for this exact mainline. The latest completed build remains `42358509993` on `9b8c61c`, before #275; do not describe that older artifact as containing #275.
- Previous artifact `DGM-MAT-Windows-3.12-9b8c61c` (ID `13569096106`, 111,216,617 bytes) remains available until `2027-02-05T09:09:23Z`, but predates the legacy Claude probe hardening.

### Current acceptance boundary
- PRs #271, #272, #273, #274 and #275 are merged; the direct browser-send bypass is removed and both approved-task and bypass-rejection fixtures run in CI.
- Local Codex/Claude coding-agent execution remains disabled. These are readiness probes only; no local Windows installation, FCC route identity, free quota, authentication, or provider model request is claimed.
- PR #220 remains open and unmerged. Native Windows mutation still needs independent review and real Windows 10 acceptance before MissionEngine integration.
- Operator PC remains offline until 2026-11-09. Monday plan remains backup first, measure actual hardware, validate Vault migration/restart, read-only specialists, durable task receipts, and local CLI/FCC readiness.

### Next steps
1. Verify Windows build `42359050528` and capture its artifact ID/size/expiry when complete.
2. Keep #220 unmerged; do not enable source mutation or coding-agent task execution from CI-only evidence.
3. On host return, validate current installer and runtime against backup/rollback plan, then exercise the exact probe and task recovery paths locally.


## Follow-up checkpoint — staged executor recovery correction (2026-11-07)

Replacement PR #276: https://github.com/AndreVazao/DGM-MAT/pull/276  
Exact head `a4133c666b036ebf5c98d6d9b8c64f3b8740e935`, based directly on current main.

- New files are staged in the transaction/backup directory. NTFS identity and result hash are persisted before atomic no-overwrite promotion to the repository target.
- Fault injection covers interruption immediately after FILE_CREATE, after identity persistence/before promotion, after promotion/before applied-manifest update, and a newer-content conflict.
- Prepared create rollback now verifies the expected result hash; it will not delete content changed after promotion.
- Windows Guard [42361201247](https://github.com/AndreVazao/DGM-MAT/actions/runs/42361201247): SUCCESS on exact head.
- Focused PR Validation [42361201259](https://github.com/AndreVazao/DGM-MAT/actions/runs/42361201259): SUCCESS on exact head.
- An initial Windows Guard failure was caused by the PR missing a native test file referenced by its workflow. The file was added and the later exact-head run passed.
- Snyk status remains `error`; no clean scan is claimed.

**Do not merge or integrate yet.** PR #276 remains draft; PR #220 is its stale predecessor. Open gates: inherited backup-root ACL verification/enforcement, power-loss directory-entry durability, independent security review, and real Windows 10 operator-PC acceptance. PC remains offline until 2026-11-09. SAFE default, explicit approval, no auto-merge and no real-project mutation remain in force.


### Further executor hardening — NTFS and same-volume requirements

Replacement PR #276 now also queries volume capabilities by pinned handle:
- only NTFS volumes with `FILE_PERSISTENT_ACLS` are accepted;
- the backup root must be on the same NTFS volume as the repository for staged handle-relative promotion;
- create-apply errors preserve the recoverable prepared object for explicit rollback;
- prepared-create rollback checks the expected content hash and refuses to delete newer content.

Exact current head `edcc28007e98c78bf799ce32e6aada520ff74409`:
- Windows Guard [42361470426](https://github.com/AndreVazao/DGM-MAT/actions/runs/42361470426): SUCCESS — 47 passed, 8 POSIX-only skipped.
- Focused PR Validation [42361470561](https://github.com/AndreVazao/DGM-MAT/actions/runs/42361470561): SUCCESS.

Microsoft documents NTFS metadata flushing for write-through operations including rename, while noting that not all storage hardware supports write-through: https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea and https://learn.microsoft.com/en-us/windows/win32/fileio/file-caching.

Still open: effective backup-root ACL verification, operator-PC Windows 10 and storage acceptance, independent review, and Snyk scan (status `error`, no clean result). PR #276 remains draft; PR #220 is stale predecessor. No MissionEngine integration or source mutation is enabled.


### Prepared replacement crash-recovery guard — 2026-11-07

Review found a data-loss risk in rollback of an existing-file replacement while the manifest is `prepared`: after process death the exclusive handle is gone, so a later writer could change the file before rollback. The old code could overwrite those bytes with the original backup.

PR #276 now requires a prepared replacement's current hash to equal either the original hash or the intended result hash. Any third hash (partial interrupted write or independent writer) is preserved; rollback stops for manual recovery. Native Windows tests cover both rejected cases and the positive case where the full expected result was written before the crash.

Exact code head `588b9d8a38f21185240ae9e4726eb784cb2b829b` passed Windows Guard [42362955666] (49 passed, 8 POSIX-only skipped) and Focused PR Validation [42362955616] (SUCCESS). Earlier attempts failed because the old test still expected unsafe auto-restore and then because it edited the manifest through path-based writes; the obsolete fixture was removed and real fault injection retained.

Memory follow-up commit: `a56e1cf0595bcfdd82a86fe140c94552faa8c63d`.


CodeRabbit review was manually triggered on PR #276; bot acknowledged the trigger but has not supplied substantive findings/review yet. The acknowledgement is not an approval.
Memory update commit: `ad16f007098f58194a73bae6153d45fb2b9fa789`.


Final PR #276 checkpoint:
- Current PR head `6a81e235e5f28ad06fa53f1d15338a0eccbc82d3`; report `reports/diagnostics/RELATORIO_BACKUP_FIRST_EXECUTOR_2026-11-07.md` updated in that commit.
- Exact-current-head Windows Guard [42363128805] SUCCESS (49 passed, 8 skipped); Focused PR Validation [42363128778] SUCCESS.
- PR #220 closed as superseded, not merged; branch/history retained.
- CodeRabbit manual review retriggered for current head; no substantive review result yet.
- PR #276 remains draft pending effective backup-root ACL validation, independent review, Windows 10 operator/storage acceptance and Snyk. No MissionEngine integration or source mutation.
Memory commit: `52cf3e00398081925b9a37b2d2b457f5ecea5507`.


## Protected backup-root ACL — current executor checkpoint (2026-11-07)

Active candidate: DGM-MAT PR #276  
Code head with ACL hardening: `c9662b8ff73b30024ffd96711b290add44e2bc02`  
Latest diagnostic report commit: `d348c164a50493a229e95749ea1bbe631bcb9173`  
Report: `reports/diagnostics/RELATORIO_BACKUP_FIRST_EXECUTOR_2026-11-07.md`

### ACL implementation
- Dedicated backup root DACL is explicitly protected from parent inheritance with `SetSecurityInfo` + `PROTECTED_DACL_SECURITY_INFORMATION`.
- Only current process user, Local SYSTEM and Built-in Administrators are granted full control, inheritable by files and child directories.
- Root owner and DACL are audited through `GetSecurityInfo` on the pinned handle; protected state is requested and checked.
- Rejects null/absent DACL, unapproved SIDs, deny/unsupported ACEs, non-inheritable/inherit-only/no-propagate ACEs and insufficient rights.
- Each transaction directory is audited separately against the inherited restricted DACL; it is not required to have its own protected flag.
- `READ_CONTROL` is used for inspection. `WRITE_DAC` is requested only for the final backup-root handle, never for the drive root or ancestor directories.
- Rollback reopens and verifies both backup root and transaction directory before reading or changing anything.

### Exact-head CI for code head c9662b8
- Windows Guard [42364111315](https://github.com/AndreVazao/DGM-MAT/actions/runs/42364111315): SUCCESS — 50 passed, 8 skipped (POSIX mutation tests intentionally fail-closed).
- Focused PR Validation [42364111361](https://github.com/AndreVazao/DGM-MAT/actions/runs/42364111361): SUCCESS.
- Intermediate failures exposed missing READ_CONTROL, path traversal variable propagation, fixture forwarding and transaction/root DACL distinctions; each was fixed and retested.
- Snyk remains `error`; no clean scan or security approval is claimed.

### Still blocked
- Independent substantive security review of the current code.
- Actual Windows 10 operator-PC acceptance: ACL, create/replace, verified backup, rollback, restart/recovery and concurrency.
- Real storage/controller write-through and abrupt-power-loss acceptance.
- Snyk clean result or formally documented scanner limitation.

PR #276 remains draft. PR #220 is closed as superseded, without merge and with branch/history retained. No MissionEngine integration, no real-project mutation and no auto-merge. SAFE default and explicit approval remain mandatory.


### Final exact-head revalidation — PR #276

The diagnostic report was committed to the PR branch as `d348c164a50493a229e95749ea1bbe631bcb9173`. Both workflows were rerun on this exact head:
- Windows Guard [42364253899](https://github.com/AndreVazao/DGM-MAT/actions/runs/42364253899): SUCCESS — 50 passed, 8 POSIX-only skipped.
- Focused PR Validation [42364253897](https://github.com/AndreVazao/DGM-MAT/actions/runs/42364253897): SUCCESS.

PR #276 remains draft. A security-focused CodeRabbit review was requested for the exact head; no substantive review result is available yet. Windows 10 operator-PC/storage acceptance and Snyk remain open. No MissionEngine integration or source mutation.


## Continuity update — PR #276 CodeRabbit findings and remediation (2026-11-07)

The latest backup-first executor is still isolated from MissionEngine. CodeRabbit's substantive review of head `d348c164a50493a229e95749ea1bbe631bcb9173` identified seven security findings, two test gaps and docstring coverage below its threshold.

Changes now committed to the PR branch:
- fixed multi-digit Windows 8.3 alias matching;
- verified native long-name components through pinned handles using `GetFinalPathNameByHandleW` during repository traversal and rollback;
- validated manifest state before missing-target create cleanup;
- limited automatic replacement restoration to cases where mutation actually began;
- bounded UTF-16 native names before constructing `UNICODE_STRING`;
- added Windows tests for missing/mismatched hashes, multi-digit aliases and native long-name resolution.

Code/test head: `ce9fa0ebc9266b35fa2ad6c02cef2882e756033e`. Diagnostic report commit: `63c1afacee92da84f3288b234bd7a4ff7e0708bd`. PR #276 remains draft.

The latest report-head CI runs at checkpoint time were Windows Guard `42366022221` and Focused PR Validation `42366022180`; they were still running. An earlier Windows Guard attempt was cancelled when the diagnostic report advanced the PR head. Do not report CI success until both latest runs complete successfully. Snyk is still `error`.

Open blockers: backup-root dedicated-directory validation before ACL changes; destination ACL policy for staged creates; durable rollback-intent/restart recovery; adversarial ACL tests; CodeRabbit docstring coverage (11.32% vs 80%); fresh independent re-review; Windows 10 host and real storage acceptance. No merge, no MissionEngine integration, no real-project mutation, no auto-merge. POSIX mutation remains disabled and SAFE/explicit approval remain mandatory.


### CI regression and correction — PR #276 (2026-11-07)

Review follow-up CI on report-head `63c1afacee92da84f3288b234bd7a4ff7e0708bd` failed because the protected-path parametrization decorator was accidentally applied to the new Windows short-name parametrized test as well, causing duplicate `path` parametrization during pytest collection. The failure was inspected in the actual Windows Guard and Focused PR Validation logs; it was not hidden. Commit `f37c8da187c550d73717ade6761380b9e246b3fc` moves the protected-path decorator back to its original test and keeps the Windows alias test separately parametrized. Exact-head runs `42366097061` (Windows Guard) and `42366096817` (Focused PR Validation) were running at checkpoint time. Do not claim either passed until completed. PR #276 remains draft; no merge or MissionEngine integration.


### Exact-code validation recovered — PR #276 (2026-11-07)

The pytest collection error from duplicate `path` parametrization was corrected in commit `f37c8da187c550d73717ade6761380b9e246b3fc`. Both exact-code workflows passed:
- Windows Guard `42366097061`: SUCCESS.
- Focused PR Validation `42366096817`: SUCCESS.

Python compilation and selected regressions passed; native Windows Guard completed the executor and handle test modules. This does not count as operator Windows 10 acceptance. Diagnostic report update: DGM-MAT commit `2bf99e0bef79988ae52f1c75e5b23e70f509564b`. PR #276 remains draft. Remaining gates: backup-root dedication/ACL preservation, destination ACL on staged files, durable rollback intent, adversarial ACL tests, docstring coverage and fresh independent review. Snyk remains `error`; PC/storage acceptance pending. No merge, MissionEngine integration, source mutation or auto-merge.



### UpdateEngine and installer integrity checkpoint — 2026-11-07 16:12 UTC

**PR #277:** Focused PR Validation run `42384614731` is SUCCESS (compile + selected regression suite). The `security/snyk` check remains ERROR. Keep the PR draft; the fail-closed facade does not implement self-update.

**PR #279:** New isolated branch `fix/installer-independent-exe-digest-2026-11-07` and draft PR require `ExpectedExeSha256` for the Windows installer. The supplied digest is compared to the received executable before directory creation, backup creation, runtime stop, or destination mutation. The Windows build emits a standalone `DGM-MAT.exe.sha256` artifact and includes it in the ZIP; the installer records the digest in its manifest. The regression file checks ordering and workflow publication. Focused validation run `42389920969` was still running at this checkpoint; do not report success until completed.

This SHA-256 sidecar is an integrity check, not a publisher signature or cryptographic provenance attestation. No self-update is implemented and no local PC operation was performed.

PR #276 remains unmerged because backup-root/ACL scope, destination ACL inheritance, durable rollback recovery, adversarial ACL tests, docstring coverage, fresh review, Snyk and real Windows 10 acceptance remain unresolved. PR #278 remains draft with the daily report addendum. Current open PRs: #276–#279. No direct main changes, merges, branch deletions, worktree changes or PC installation.



### CI finalizado para PR #279 — 2026-11-07 16:13 UTC

Focused PR Validation run `42389920969` concluiu **SUCCESS**: checkout das dependências, compilação Python, seleção e execução dos testes afetados passaram. O check `security/snyk` no head da PR #279 está em **ERROR**. O workflow Windows de build não foi executado na branch (configurado para push em main ou workflow_dispatch); não existe ainda validação de sintaxe PowerShell em runner Windows nem execução do instalador. A PR #279 permanece draft. A aceitação no Windows 10 do operador continua pendente.



### Windows runner verification — 2026-11-07 16:15 UTC

PR #279's Windows-specific job in Focused PR Validation run `42390097774` completed **SUCCESS**. The Windows runner parsed `scripts/install_windows_update.ps1` and executed the negative-digest test, confirming rejection before target/backup directory creation. The Linux focused job in the same run was still installing dependencies at last observation; do not claim its final result yet. Snyk remains ERROR. The PR stays draft and the operator's Windows 10 acceptance is still required.



### PR #279 full CI result — 2026-11-07 16:16 UTC

Both jobs in Focused PR Validation `42390097774` completed **SUCCESS**:
- Windows installer digest gate: PowerShell parse and mismatch rejection before target/backup directory creation.
- Compile and run only affected regressions: Python compile and selected regressions passed.

Snyk remains **ERROR**. The full Windows executable build workflow was not run, and the operator's Windows 10 acceptance remains outstanding. PR #279 remains draft and unmerged. No local installation or mutation occurred.


### Snyk quota diagnosis and review boundary — 2026-11-07 16:20 UTC

For PR #279 head `2456cc7eac6893ed82499e1aea4b041ae4774559`, GitHub commit status API returned `security/snyk (andrevazao)` = `error`, with exact description **“You have used your limit of private tests”**. This is an external Snyk status, not a GitHub Actions job, and it contains no vulnerability findings. Classify it as Snyk private-test quota exhaustion / scan unavailable. It is neither evidence of a vulnerability nor a clean scan/security approval.

The repository's `.github/workflows/security-scan.yml` is manual-only (`workflow_dispatch`) and runs Bandit, pip-audit and Safety. It does not generate or repair the external Snyk status and is not a replacement for a clean Snyk scan.

The exact-head Focused PR Validation run `42390097774` has both jobs SUCCESS. CodeRabbit check was skipped with **“Review skipped: draft pull request”**; no independent review exists for this PR head. Current Windows test validates PowerShell parsing and rejection of a wrong digest before target/backup directory creation. It does not validate successful installation, interruption rollback, real launcher replacement or operator Windows 10 acceptance. Full Windows executable build on this PR branch was not run. Keep PR #279 draft/unmerged.
