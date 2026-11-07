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


## PR #276 — independent security review and remediation checkpoint (2026-11-07)

CodeRabbit completed a substantive review against code head `d348c164a50493a229e95749ea1bbe631bcb9173`. It identified seven actionable security findings, two test-coverage findings and a docstring-coverage warning. This is not an approval.

Follow-up commits on branch `fix/backup-first-staged-create-recovery-2026-11-07`:
- `e8b5e02`: multi-digit 8.3 alias syntax, rollback state validation before missing-target cleanup, and automatic replacement restoration only after mutation starts.
- `674da67`: reject UTF-16 native names exceeding the 16-bit `UNICODE_STRING` length bounds.
- `98b8e8a`, `06d38a9`: Windows regressions for missing/mismatched replacement hashes and multi-digit aliases.
- `7ca94f5`: add native final-path component inspection through `GetFinalPathNameByHandleW`.
- `7c9c14e`: verify native long-name identity for each opened repository directory and rollback target; constrain missing-identity create cleanup to `prepared`.
- `0d8248d`: correct native path separator handling.
- `ce9fa0e`: test pinned-handle native long-name resolution.
- Diagnostic report updated in DGM-MAT commit `63c1afa`; PR comment records the addressed and outstanding findings.

Latest code/test commit: `ce9fa0ebc9266b35fa2ad6c02cef2882e756033e`. Latest PR head after diagnostic sync: `63c1afacee92da84f3288b234bd7a4ff7e0708bd`.

The exact-code-head Windows Guard run `42366006820` was cancelled when the report commit advanced the PR head; the latest report-head Windows Guard `42366022221` and Focused PR Validation `42366022180` were running at checkpoint time. Do not claim either passed yet. Snyk remains `error`.

Still open from CodeRabbit:
1. prove backup_root is a dedicated directory before changing its DACL; preserve ACLs of shared directories;
2. ensure staged created files inherit destination directory security policy before promotion;
3. persist and recover rollback intent/outcome across interruption;
4. native long-name verification (implemented in this follow-up, still requires Windows CI confirmation);
5. adversarial ACL tests for broad SIDs, null/absent DACLs, unprotected roots and invalid inheritance;
6. docstring coverage (reported 11.32% vs 80% threshold);
7. fresh independent re-review of the corrected head.

PR #276 remains draft and unmerged. PC acceptance is still pending until 2026-11-09. NTFS/storage abrupt-power-loss acceptance and Snyk remain open. No MissionEngine integration, no real-project mutation, no auto-merge. SAFE default and explicit approval remain mandatory.


### CI correction after review remediation — 2026-11-07

The first rerun against report-head commit `63c1afacee92da84f3288b234bd7a4ff7e0708bd` failed in test collection, not in executor behavior: a pre-existing `@pytest.mark.parametrize("path", ...)` decorator was inadvertently left attached to the newly inserted Windows alias test, producing duplicate parametrization. Both Windows Guard `42366022221` and Focused PR Validation `42366022180` exposed the same collection error. The issue was corrected in commit `f37c8da187c550d73717ade6761380b9e246b3fc` by separating the two parametrized test functions. New exact-head runs are Windows Guard `42366097061` and Focused PR Validation `42366096817`; both were still running at this update. No success is claimed. Keep PR #276 draft and unmerged.


### Exact-code CI passed after test correction — 2026-11-07

The duplicate parametrization collection failure was corrected in `f37c8da187c550d73717ade6761380b9e246b3fc`. Exact code/test head CI completed successfully:
- Windows Guard [42366097061](https://github.com/AndreVazao/DGM-MAT/actions/runs/42366097061): SUCCESS.
- Focused PR Validation [42366096817](https://github.com/AndreVazao/DGM-MAT/actions/runs/42366096817): SUCCESS.
- Python compilation and selected regression tests passed. The Windows Guard exercised both `test_backup_first_patch_executor.py` and `test_windows_handle_fs.py`.
- This is hosted Windows CI, not operator Windows 10 acceptance.

DGM-MAT diagnostic report synced in commit `2bf99e0bef79988ae52f1c75e5b23e70f509564b`; exact code/test head remains `f37c8da187c550d73717ade6761380b9e246b3fc`. The report sync advances PR head without changing source/test code. PR #276 remains draft. Open CodeRabbit findings: dedicated backup-root scope before ACL changes; destination ACL policy for staged creates; durable rollback intent/restart recovery; adversarial ACL tests; docstring coverage (11.32% vs 80%); fresh independent re-review. Snyk remains `error`; Windows 10 host/storage acceptance remains open. No merge, MissionEngine integration or real-project mutation.



### Installer provenance gate and UpdateEngine correction — 2026-11-07 16:12 UTC

- PR #277 `fix/update-engine-fail-closed-2026-11-07` remains OPEN/DRAFT. Focused PR Validation #645 / run `42384614731` completed SUCCESS, including Python compilation and selected regression tests. Snyk status is still ERROR; do not claim a clean security scan. The facade now fails closed, but release discovery and self-update remain unimplemented.
- PR #279 `fix/installer-independent-exe-digest-2026-11-07` adds mandatory `ExpectedExeSha256` to `scripts/install_windows_update.ps1`. The digest comparison occurs before creating backup/target directories, stopping the runtime, or replacing files. The Windows build publishes `DGM-MAT.exe.sha256` as a separate Actions artifact file and includes it in the ZIP. The install manifest records the expected digest and pre-mutation verification.
- PR #279 Focused PR Validation run `42389920969` was still running at checkpoint time. No pass is claimed until the workflow completes. Windows 10 operator acceptance remains unavailable while the PC is offline.
- Security boundary: a separately supplied SHA-256 digest improves integrity checking against accidental corruption/substitution but is not a publisher signature or cryptographic build attestation. No self-update, download, installation or PC mutation was performed.
- Daily report PR #278 received an addendum and remains draft. Issue #244 was updated with the PR #279 link.
- Current PR inventory at checkpoint: #276, #277, #278, #279 open/draft. No merge, direct main write, branch deletion, worktree change or installation occurred.
