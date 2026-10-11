# DGM-MAT — continuity and synchronization checkpoint
Date: 2026-10-11
Branch: `continuity/pc-setup-2026-10-11`
Status: documentation checkpoint committed to a separate branch; local PC checkout not reconciled because Desktop Commander has 0% remote calls remaining.

## Immediate user priorities
1. Preserve continuity so project decisions and next actions are not lost.
2. Keep GitHub as a usable fallback if local remote access is unavailable.
3. Get the PC cockpit working before mobile pairing.
4. Inventory all installed programs, runtimes, models, skills, provider integrations, exact executable paths and project dependencies.
5. Let DGM-MAT discover missing tools, explain why each is needed, and request explicit approval before installing or changing anything.
6. Later provide a Windows installer EXE with preflight, adaptive hardware profile, resumable installs, verified health checks and rollback. Do not claim the EXE exists until a real artifact is verified.

## Evidence and path anchors
See `AndreVazao/DGM-MAT` document `docs/architecture/PC_SETUP_AND_REPROVISIONING_INVENTORY_2026-10-11.md` on branch `continuity/pc-setup-2026-10-11`.
- Workstation: PC-Vazao-Anjos; Windows 10 Home x64 build 19045; Pentium T3200 2 cores; ~2.96 GiB RAM.
- Workspace `C:\\ProgramasGodMode`; DGM-MAT local repo `C:\\ProgramasGodMode\\DGM-MAT`; observed local branch `feat/conversation-turn-semantics-v1`.
- Runtime `C:\\DevopGodMode`.
- Active local memory `C:\\AndreOS-Memory`; canonical remote `AndreVazao/andreos-memory`, main.
- Preserve legacy archive `C:\\AndreOS-Memory-LEGACY-2026-10-07` and never modify `DGM-MAT-FULL-MIRROR`.
- Python 3.12.6, Node 24.20.0/npm 11.19.0, Git 2.45.1, Ollama 0.23.0 and four small local models were observed; full inventory/version/signature and all provider health checks remain incomplete.
- FCC executable/workspace and Sovereign Trader virtual environment were observed; details and end-to-end health remain to be verified.
- Desktop Commander usage is now 0%. Do not claim a fresh local sync, live dashboard verification or a full machine scan.

## Safety and operating rules
- Investigate -> compare -> document -> test -> decide -> change.
- Preserve uncommitted local work, logs, stack dumps and old files until reviewed. No force-push, no blind reset, no cleanup of historical queues.
- No automatic GitHub Actions workflows/builds/reruns; conserve minutes.
- No Vercel/mobile exposure until local cockpit auth is proven and user explicitly approves.
- No secrets in Git or memory. Future Vault integration must use an approved credential manager/DPAPI-backed mechanism and scoped credentials.
- Path repair must use process/package/registry/PATH/repository evidence, report confidence and affected callers, back up configuration, test and provide rollback. Never silently rewrite paths.
- Hardware profile must adapt to the current host; the present low-resource PC is not an architectural limit.

## Next sequence when local access returns
1. Read-only Git status, branch, remote refs, stash list, recent commits and dirty diff for DGM-MAT, AndreOS-Memory and VazaoSovereignTrader. Do not discard or force-reset anything.
2. Compare local commits/files against GitHub and publish only reviewed changes. This branch is a continuity documentation branch, not proof of full synchronization.
3. Audit Core process PID, current auth middleware loaded status, queue state and local cockpit launch command; avoid restart while non-terminal missions exist unless maintenance is explicitly approved.
4. Validate loopback dashboard E2E and auth negative/positive cases; then correct launch paths and add a user-friendly startup entry only after evidence.
5. Build a versioned path/tool catalogue and project dependency manifests; then implement the approved EXE bootstrap and test on clean Windows.

## Related Sovereign Trader continuity
A separate documentation-only checkpoint was added to the `AndreVazao/VazaoSovereignTrader` repository on the same branch name. It records the observed virtual-environment path and explicitly does not change trading code, configuration, keys, orders or runtime behavior.
