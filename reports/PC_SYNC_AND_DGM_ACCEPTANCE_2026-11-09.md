# DGM-MAT PC deployment and day-mission checkpoint — 2026-11-09

## Operator constraints
- PC: `PC-Vazao-Anjos`; Desktop Commander online.
- Last reported monthly remote quota: 17%; preserve remaining quota for VazaoSovereignTrader tests.
- Use grouped remote operations only. No repeated health loops from ChatGPT.
- Protect dirty working trees, user data, credentials, AndreOS Memory and worktrees. No resets or destructive broad cleanup.

## Six GitHub repositories to synchronize
- `AndreVazao/DGM-MAT`
- `AndreVazao/VazaoSovereignTrader`
- `AndreVazao/DGM-HUB`
- `AndreVazao/office-kit`
- `AndreVazao/VAZAO-EVSE-Platform`
- `AndreVazao/TruckFood`

## Merges completed in this operation
- DGM-MAT PR #285 merged: `de56658aafadfb4915eed7902a7b913124a54f14`. Secure mobile scopes, durable chat/history search and API readiness boundaries are now on main.
- DGM-MAT PR #287 merged: `80b7ffa5dc1fea742b9a0f24190b95446ed38d1b`. Read-only EGM review packet contract and tests are on main.
- DGM-MAT PR #288 merged: `b372fb92d54aad19fa0a3a27f71659d12cf51edb`. Host-attested EGM review coordinator and durable task receipt checks are on main. It remains a coordinator contract, not a live provider adapter.
- DGM-Cockpit-Frontend PR #16 merged: `7d5f34be317b5a7b982dc2dd4ccd0abc5068e45f`. Dashboard conversation history search and credential prompt improvements are on main.
- No provider/autonomy flags enabled. No external AI credentials or paid APIs activated.

## Remaining DGM-MAT PRs
- PR #283 remains OPEN and CONFLICTING after main advanced. It must be rebased/reconciled before merge; browser consultation remains disabled by default and requires individual approval.
- PR #289 depends on #283; not merged.
- PR #286 is documentation-only and remains open.
- PR #5 in DGM-MAT-Mobile remains open pending a successful emulator UI smoke test.
- PR #70 in AndreOS Memory remains open.

## CI evidence
- DGM-MAT Windows Executable Build run `42576149537`: SUCCESS on main commit `80b7ffa5dc1fea742b9a0f24190b95446ed38d1b`.
- A further Windows Executable Build run `42576749111` started after PR #288 merge on `b372fb92d54aad19fa0a3a27f71659d12cf51edb`; latest observed status IN_PROGRESS.
- DGM-MAT-Mobile contract/APK run `42575360833`: SUCCESS on commit `bbd21f2f5371fce5c05bc7e6caba275b419794cb`.
- Maestro run `42575360984`: FAILED before the app smoke flow. Emulator booted, then ADB failed during the runner's animation-disable step with `Broken pipe (32)` / exit 224. This is an emulator/ADB infrastructure failure, not an app assertion.
- Maestro workflow hardened again in commit `8104173d94d0027b8db5b415daf093564a4f96ff`: 4 cores, 3 GB RAM, 1 GB heap, runner animation-disabling off, best-effort animation settings after boot. New runs: Maestro `42576654623`, APK/contract `42576654720`, both observed IN_PROGRESS.
- Previous APK artifact from run `42575360984` ID `13655716506`, ZIP SHA-256 `7b35a2d8796b7921eaaa6def05bbc3b7c43f79d67bed9059839b899b791a7b1d`; smoke flow did not pass, so do not treat it as UI-accepted.

## Dashboard deployment design
- DGM-MAT already contains the Qt cockpit in `cockpit/`; `main.py` supports normal cockpit mode, `--headless`, and `--cockpit-only`.
- The separate PC web dashboard package is built by manual workflow `.github/workflows/windows-backoffice-dashboard-build.yml`. It clones DGM-Cockpit-Frontend main, validates Node contracts and focused API security tests, builds a headless `DGM-MAT-BackOffice.exe`, and packages `dashboard/index.html`, `app.js`, `styles.css`, plus `Install-DGM-MAT.ps1`.
- The official installer deploys under `%ProgramFiles%\DGM-MAT`, backs up previous engine files, preserves user data, writes a hidden backend startup launcher and creates a public desktop shortcut to `http://127.0.0.1:8181/app/`.
- The full standalone Windows executable build and the web-dashboard/back-office package are distinct products; use the latter for the requested PC web dashboard.

## PC remote operation
- First grouped script PID `3732` stopped safely before changing files: recursive discovery found a DGM-HUB runtime snapshot worktree without an origin remote. No installation changes were made.
- Corrected grouped operation PID `3196` is running on `PC-Vazao-Anjos`. It excludes runtime snapshots/worktrees, discovers the six repos by GitHub origin, fetches all, fast-forwards only clean `main` branches, and leaves dirty/non-main branches untouched.
- If GitHub CLI is available/authenticated, the same process dispatches `windows-backoffice-dashboard-build.yml`, waits for its run, downloads the dashboard package, checks package commit identity, stops only known DGM-MAT processes, backs up/removes known legacy standalone EXEs, runs the official installer with UAC, starts the hidden backend, verifies `/health`, `/app/`, and `/app/app.js`, opens the dashboard and writes `PC-INSTALL-ACCEPTANCE-2026-11-09.md`.
- No successful PC sync, install or HTTP verification may be claimed until PID 3196's report confirms it. If a UAC prompt or GitHub CLI authentication blocks it, stop and report the exact blocker; do not retry remotely.

## All-day mission: verified limitation
- Main's `MissionEngine` uses `MISSION_EXECUTION_TIMEOUT_SECONDS = 300`.
- Auto-run is restricted to a fixed allowlist of read-only intents; unsupported implementation requests are decomposed as proposals and end FAILED with `NotImplementedError`, not executed.
- `POST /runtime/missions` is operator-protected by local bearer session; dashboard/API readiness does not imply an authenticated operator session.
- Therefore a genuine all-day autonomous engineering mission cannot honestly be started yet. Do not create fake RUNNING records or bypass auth by writing directly to SQLite/checkpoint files.
- Safe immediate work after operator login: launch a supported read-only repository inventory/research mission. For true all-day work, implement and test a durable scheduler/worker with checkpoint/resume, explicit task budgets, cancellation, operator approval for mutations, independent QA, and end-of-day report before claiming it.

## Evidence rule
CI success is not local acceptance. Report local repo paths/branches/SHAs, dirty-state preservation, installed package build SHA, installer backup manifest, API/dashboard HTTP results, and mission ID/status before claiming completion.
