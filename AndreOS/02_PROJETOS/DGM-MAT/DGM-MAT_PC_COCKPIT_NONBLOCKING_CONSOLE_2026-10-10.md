# Path: C:\\AndreOS-Memory\\AndreOS\\02_PROJETOS\\DGM-MAT\\DGM-MAT_PC_COCKPIT_NONBLOCKING_CONSOLE_2026-10-10.md

# DGM-MAT — PC cockpit non-blocking console
Date: 2026-10-10

## Implemented
- `cockpit/widgets/command_console.py` now runs mission/status HTTP requests in a dedicated Qt worker thread.
- Controls disable while a request is active and preserve the last runtime-online/offline state after completion.
- Timeouts are treated as an unknown outcome; operator is instructed to inspect Missions before retrying.
- Mission creation is reported only when a success response and mission ID are both present.
- This widget no longer writes raw user directives to the general observability log.
- User/provider text is HTML-escaped before display.
- API URL explicitly uses `127.0.0.1:8181`.
- Tests added at `tests/cockpit/test_command_console_worker.py`.

## Validation
- Cockpit suite: 10 tests passed.
- Wider suites `autonomy`, `organization`, `contracts`, `security`, and `cockpit` completed with exit code 0.
- Syntax compilation and `git diff --check` passed.
- Backup before editing: `C:\\ProgramasGodMode\\DGM-MAT-OS\\backups\\pc-cockpit-nonblocking-console-2026-10-10\\command_console.py.before`, SHA-256 `6D39A4CF9F3E4A4DE50AA8A27ACBE99EBD66DD35654641F00EAD3479EE9ECD5A`.

## Security blockers remain
- `core/api/api_server.py` still has wildcard CORS (`allow_origins=["*"]`).
- Legacy runtime/mobile/governance/provider routes are not globally enforced by the local session manager. `POST /auth/session` issues sessions, but issuance is not route enforcement.
- API remains bound to loopback by default. Do not expose via LAN/Tailscale/reverse proxy/public internet until global HTTP/WebSocket auth, origin policy, scopes, revocation, anti-replay and client migration are complete and tested.
- Do not expose the human-intervention queue over HTTP/WebSocket yet. No remote caller may assert verification to resume a mission.
- CAPTCHA/MFA remains manual; secrets never enter prompts, general logs, SQLite handoff metadata, memory or rendezvous metadata.

## Next gate
1. Inventory every HTTP and WebSocket route and define a fail-closed auth contract.
2. Migrate desktop and realtime clients to short-lived scoped sessions.
3. Add negative tests for every protected HTTP route and WebSocket.
4. Only then add a read-only pending-interventions endpoint/view.
5. Complete the PC cockpit and end-to-end tests before pairing/Tailscale and Android APK.

## Links
- DGM-MAT implementation note: https://github.com/AndreVazao/DGM-MAT/blob/main/docs/architecture/PC_COCKPIT_NONBLOCKING_COMMAND_CONSOLE.md
- Previous realtime connection note: https://github.com/AndreVazao/DGM-MAT/blob/main/docs/architecture/PC_COCKPIT_REALTIME_CONNECTION.md

Policy remains stability > features, reality > assumptions, FREE-ONLY / PAID-DENY. No GitHub Actions. Never touch `C:\\ProgramasGodMode\\DGM-MAT-FULL-MIRROR`.
