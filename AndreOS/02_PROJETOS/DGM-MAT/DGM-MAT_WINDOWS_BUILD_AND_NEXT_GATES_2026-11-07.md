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

Issue #212 remains the acceptance specification for connecting backup-first patch execution to MissionEngine. PR #220 remains open and must not be merged wholesale. The Windows-native executor still requires independent review of backup-root ACL inheritance and abrupt-power-loss durability guarantees, followed by actual Windows 10 tests for create/replace, backup verification, rollback, prepared-state recovery and concurrent-writer rejection.

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
