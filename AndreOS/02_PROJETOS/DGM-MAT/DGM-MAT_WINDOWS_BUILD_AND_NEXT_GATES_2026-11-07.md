# DGM-MAT — Windows build and next engineering gates

**Date:** 2026-11-07  
**Repository:** https://github.com/AndreVazao/DGM-MAT  
**Main:** `c448bc5a28776b395e0dafc1c1fc5aed009af9df`

## Verified Windows build

The current-main Windows 3.12 executable build completed successfully:

- Workflow run: [42359050528](https://github.com/AndreVazao/DGM-MAT/actions/runs/42359050528)
- Job: `build (3.12)` — completed / success.
- All 31 job steps completed successfully, including dependency installation, browser extension installer validation, executable build, deep executable validation, final assertions and artifact upload.
- Artifact: `DGM-MAT-Windows-3.12-c448bc5`
- Artifact ID: `13568827964`
- Size: `111216164` bytes
- Created: `2026-11-07T09:21:10Z`
- Expires: `2027-02-05T09:16:42Z`
- SHA-256: `b148c16809cae271696953e7872f9d8136c942fe434ca131664b3b243b2b27c2`

This artifact includes merged PR #275 (legacy Claude auth probe hardening). It supersedes the previous #274 artifact for current-main testing. Build/CI success is not local Windows installation or runtime acceptance.

## Mainline changes included

The current mainline includes the durable Vault, durable organization task lifecycle, read-only repository/Python/test specialists, browser server-approved task queue, browser direct-send bypass removal and regression fixtures, Codex/Claude readiness probes, Windows CLI shim handling, and the cross-platform legacy Claude probe wrapper rejection.

## Current mutation boundary

Issue #212 remains the acceptance specification for connecting backup-first patch execution to MissionEngine. PR #220 is now the stale predecessor to replacement PR #276. Neither is to be merged/connected to MissionEngine until ACL inheritance, abrupt-power-loss durability, independent review and Windows 10 operator acceptance are resolved.

SAFE remains the default; explicit approval is required; auto-merge remains disabled. No source mutation or local coding-agent task execution is enabled by this build.

## Next host acceptance — 2026-11-09

The operator PC is currently offline. On return:

1. Preserve the existing installation, runtime, configuration and Vault with a verified backup before changing anything.
2. Measure actual CPU, RAM, disk and available resources; do not rely on historical hardware estimates.
3. Verify the new artifact digest and inspect installer/runtime paths before installation; retain rollback to the previous version.
4. Validate Vault path alignment, migration, reopen/restart persistence and resource use.
5. Configure a narrow allowlist for a disposable or explicitly approved repository and run one repository inventory, one Python source analysis and one test inventory.
6. Compare worker outputs with manual inspection and test durable task/receipt recovery after process restart.
7. Probe Codex/Claude CLI and FCC status without exposing credentials; distinguish CLI presence, authentication, provider/model identity and free-tier/quota evidence.
8. Keep mutation disabled until the native Windows executor passes its host gates and a bounded isolated-worktree integration is independently reviewed.

## Evidence boundary

This document records GitHub CI/build evidence and pending host acceptance. It does not claim that the artifact has been downloaded, installed, or run on the operator PC.


## Additional PR #220 recovery finding — 2026-11-07

A source review of PR #220 head `db18012f3d2d094a8dc3ed14b7b680b8025b93d1` identified a create-operation crash window in `BackupFirstPatchExecutor._apply_text_windows()`:

1. A durable `prepared` manifest is written with `target_identity: null`.
2. The new destination is created using `FILE_CREATE`.
3. Only afterwards is its file identity written into the manifest.

A process/power interruption between steps 2 and 3 can leave an empty created destination while the manifest has no identity. Recovery correctly refuses to delete an unverified target, but automatic prepared-state recovery is incomplete for this window. A deterministic fault-injection test and a handle-bound recovery design are required; do not weaken identity checks or use path-based cleanup.

The finding was recorded on PR #220 in comment https://github.com/AndreVazao/DGM-MAT/pull/220#issuecomment-6705102905. PR #220 remains draft/open/unmerged. Existing independent review, backup-root ACL, abrupt-power-loss durability and real Windows 10 acceptance gates remain open.

No local host test or source mutation is claimed.


## Replacement executor PR #276 — staged-create recovery correction (2026-11-07)

Replacement PR: https://github.com/AndreVazao/DGM-MAT/pull/276  
Branch: `fix/backup-first-staged-create-recovery-2026-11-07`  
Exact validated head: `a4133c666b036ebf5c98d6d9b8c64f3b8740e935`  
Base: current main `c448bc5a28776b395e0dafc1c1fc5aed009af9df`.

### Correction

The create path no longer creates the final repository target before persisting its identity. It writes the new content to a staging file inside the transaction/backup directory, obtains the NTFS file identity, persists identity/hash in the `prepared` manifest, then promotes the staged file by handle-relative atomic rename with overwrite disabled.

Recovery behavior:
- Crash immediately after staging FILE_CREATE but before identity persistence: the repository target is never created. The unverified staging file is retained; recovery refuses to delete it by name alone.
- Crash after identity persistence but before promotion: recovery verifies staged file identity and result hash before deletion.
- Crash after promotion but before the `applied` manifest: recovery verifies target identity and hash before rollback.
- A prepared created target whose content has changed since promotion is preserved; rollback refuses to delete newer content.

Fault-injection tests cover these boundaries and the newer-content conflict.

### Exact-head CI

- Windows Guard run [42361201247](https://github.com/AndreVazao/DGM-MAT/actions/runs/42361201247): **SUCCESS** on exact head `a4133c666b036ebf5c98d6d9b8c64f3b8740e935`. The native Windows test suite passed; 8 POSIX-only tests were skipped by policy.
- Focused PR Validation run [42361201259](https://github.com/AndreVazao/DGM-MAT/actions/runs/42361201259): **SUCCESS** on the same exact head; Python compilation and selected regressions passed.
- The first Windows Guard attempt failed because the PR omitted `tests/execution/test_windows_handle_fs.py` while the workflow invoked it. The missing file was added; a subsequent exact-head Windows Guard passed. This initial failure was not ignored.
- Snyk status remains `error`; no clean Snyk scan is claimed. The previously observed private-test quota limit is a coverage gap, not a vulnerability finding or approval.

### Gates still open

1. Backup-root ACL: directories inherit parent ACLs; the implementation does not yet verify that the configured backup root is private. Verify and enforce/accept ACL on the real Windows host.
2. Abrupt-power-loss durability: file flush/write-through does not prove absolute durability of directory-entry metadata. Do not claim stronger guarantees without Windows/NTFS-specific evidence.
3. Independent security review of the current replacement.
4. Windows 10 operator-PC acceptance: create/replace, verified backup, rollback, restart/recovery and concurrent-writer rejection.
5. Only after the above, implement task-specific MissionEngine integration using existing MissionEngine/TaskManager and WorktreeManager, allowlisted validators, exact diff approval, durable checkpoints and rollback.

PR #276 remains draft. PR #220 remains open/draft as the stale predecessor. SAFE remains default, explicit approval required, auto-merge disabled, and no source mutation is enabled. The operator PC remains offline until 2026-11-09; no host acceptance is claimed.
