# Path: C:\\AndreOS-Memory\\AndreOS\\02_PROJETOS\\DGM-MAT\\DGM-MAT_GLOBAL_API_AUTH_ENFORCEMENT_2026-10-10.md

# DGM-MAT â€” global API authentication enforcement
Date: 2026-10-10

## Implemented in source
- Added fail-closed ASGI middleware `core/api/auth_middleware.py` for inventoried HTTP and WebSocket routes.
- Only `GET /health` is public. `POST /auth/session` uses the existing loopback-only bootstrap exchange, origin allowlist and rate limiter.
- Private HTTP endpoints require a short-lived in-memory bearer session; missing/invalid/revoked sessions return 401; insufficient scope returns 403.
- `/ws` and `/runtime/ws` require Authorization header; no token in URL/query.
- Removed wildcard CORS and restricted allowed origins/methods/headers to the local desktop origins.
- Added `cockpit/api_client.py` for local bootstrap exchange and in-memory session caching. Token never enters logs, prompts or persistent storage.
- Migrated desktop HTTP calls in main window, provider management, command console and operational dashboard. Realtime WebSocket now authenticates.
- Added `tests/security/test_api_global_auth_enforcement.py` for public/private routes, valid/revoked/insufficient-scope sessions, WebSocket access and CORS rejection.
- Static `/app` shell remains accessible; its API data endpoints remain protected. Browser/mobile pairing is not implemented yet.

## Validation
- Global auth enforcement tests: 7 passed.
- Combined security + cockpit suites passed in the preceding run; a final post-patch run is being verified.
- Broader suites autonomy, organization, contracts, security and cockpit completed with exit code 0.
- `compileall` and `git diff --check` passed.
- Backup before auth edits: `C:\\ProgramasGodMode\\DGM-MAT-OS\\backups\\api-global-auth-2026-10-10`, initial source manifest created. Final source/copy hashes will be refreshed after final edits.

## Critical runtime status
The currently running PC API process was not restarted. In-process TestClient results prove the new source behavior, not that the live server has loaded the middleware. A controlled restart and live HTTP/WebSocket verification are still required before claiming production enforcement. Keep loopback-only binding and do not expose LAN/Tailscale/public access.

## Next gates
1. Verify bootstrap file ACL without printing secret contents.
2. Plan a controlled API restart that preserves independent Core and mission state.
3. Validate live health, 401 without session, success with session, WebSocket 1008 without session and authenticated WebSocket success.
4. Design explicit browser/mobile pairing; never place bootstrap token in static JavaScript or query strings.
5. Review route scopes, sensitive-action rate limits, revocation and audit events.
6. Only after these gates, proceed with private Tailscale access and Android APK.

No paid services, external providers, GitHub Actions or public port changes. Do not touch `C:\\ProgramasGodMode\\DGM-MAT-FULL-MIRROR`.

## Final validation
- Global auth enforcement tests: 7 passed.
- Combined security + cockpit suite after final console patch: exit code 0 (33 tests observed).
- Broader autonomy/organization/contracts/security/cockpit suites: exit code 0.
- compileall and git diff --check passed.
- Live API process was not restarted; source enforcement is not yet confirmed active in production.



## Live maintenance gate check — 2026-10-10
- Live /health returned healthy. Listener is pythonw.exe running uvicorn core.api.api_server:app on 127.0.0.1:8181; this is the pre-change process and has not loaded the new middleware yet.
- Mission queue summary only: 385 total; 380 FAILED, 3 RUNNING and 2 QUEUED. Because five missions are non-terminal, the API/Core process was NOT restarted. No mission goals or outputs were read or printed.
- Bootstrap file exists. ACL shows explicit FullControl only for SYSTEM and the current Windows user; secret contents were not read.
- Next safe step: inspect why the 3 RUNNING/2 QUEUED missions remain non-terminal, allow them to finish or obtain explicit maintenance approval, then perform a controlled API restart and verify live 401/200/WebSocket behavior.
