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


## Further hardening — NTFS capability and same-volume enforcement (2026-11-07)

PR #276 advanced beyond the staged-create correction:

- Uses `GetVolumeInformationByHandleW` against already-pinned volume handles.
- Mutation fails closed unless the filesystem is NTFS and advertises `FILE_PERSISTENT_ACLS`.
- Backup root must be on the same NTFS volume as the repository, because handle-relative staged promotion cannot cross volumes.
- Create failures after promotion preserve the `prepared` target/manifest for explicit verified rollback instead of deleting the target and leaving an unrecoverable manifest.
- A prepared create rollback verifies the expected result hash and preserves content modified by a later writer.

Microsoft documents that `FILE_FLAG_WRITE_THROUGH` causes NTFS to flush metadata changes such as rename operations; it also notes that not all storage hardware supports write-through. See:
- https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea
- https://learn.microsoft.com/en-us/windows/win32/fileio/file-caching

The implementation now rejects non-NTFS filesystems and volumes without persistent ACL support. This does **not** verify that the actual inherited backup-root ACL is sufficiently private, nor does cloud CI establish the operator PC's storage-controller behavior.

Latest exact head: `edcc28007e98c78bf799ce32e6aada520ff74409`
- Windows Guard [42361470426](https://github.com/AndreVazao/DGM-MAT/actions/runs/42361470426): SUCCESS — 47 passed, 8 POSIX-only skipped.
- Focused PR Validation [42361470561](https://github.com/AndreVazao/DGM-MAT/actions/runs/42361470561): SUCCESS.
- Snyk status remains `error`; no clean scan is claimed.

PR #276 remains draft. Remaining gates: inspect/verify inherited backup-root ACL; validate actual Windows 10 operator host create/replace/recovery/concurrency; verify storage write-through behavior; obtain independent review. PR #220 remains open/draft as predecessor. No MissionEngine mutation integration or local acceptance is claimed.


## Prepared replacement recovery guard — 2026-11-07

A further independent source review found that a `replace` operation in state `prepared` could restore the original backup even if the target had been changed by an independent writer after process death. The exclusive handle only protects while the process is alive; after a crash it no longer excludes writers.

Correction on PR #276:
- For a prepared replacement, rollback now accepts only a current SHA-256 equal to either `original_sha256` or `result_sha256`.
- If current bytes match neither value (partial interrupted write or later writer), rollback refuses to overwrite them and preserves the backup for manual recovery.
- Added native Windows fault-injection tests for partial-write crash and independent newer content; added a positive recovery test for the complete expected result.
- Replaced an older test that manually edited the manifest via path-based writes; real crash boundaries are now simulated through the executor's own failure points.

Validation history:
- Windows Guard on `d96bac1` failed because the old partial-write recovery test still expected automatic restoration. This exposed an obsolete test expectation.
- Windows Guard on `d3549a9` still failed because that obsolete test rewrote the manifest by path and produced a JSONDecodeError; focused validation passed.
- The obsolete fixture has been removed; current branch head is `588b9d8a38f21185240ae9e4726eb784cb2b829b`. Exact-head Windows Guard and Focused PR Validation are running; do not claim them passed yet.
- A further diagnostic improvement on `a10b0be` includes the underlying exception type/message in unexpected rollback errors.

PR #276 remains draft. ACL effective-permission inspection, independent external review, Windows 10 operator-host acceptance and storage durability acceptance remain open. PR #220 remains stale predecessor. No MissionEngine integration or real-project mutation is enabled.


CodeRabbit manual review was triggered on PR #276 via `@coderabbitai review`; the bot acknowledged the invocation, but no substantive review result has been received yet. Do not count the acknowledgement as a review.


### Final checkpoint after diagnostic report sync

- PR #276 current head: `6a81e235e5f28ad06fa53f1d15338a0eccbc82d3`.
- Diagnostic report updated in DGM-MAT commit `6a81e235e5f28ad06fa53f1d15338a0eccbc82d3`: `reports/diagnostics/RELATORIO_BACKUP_FIRST_EXECUTOR_2026-11-07.md`.
- Both workflows rerun on the exact current PR head: Windows Guard [42363128805] SUCCESS (49 passed, 8 skipped); Focused PR Validation [42363128778] SUCCESS.
- PR #220 closed as superseded by #276; not merged, branch/history retained.
- CodeRabbit's first manual review trigger was not completed because the head changed while queued. A new trigger was sent for the current head; no substantive independent review yet.
- PR #276 remains draft; effective backup-root ACL inspection, independent review, Windows 10 operator/storage acceptance and Snyk remain open. No MissionEngine integration or source mutation.
