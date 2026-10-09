# DGM-MAT — Startup + API Security Audit (2026-10-09)
<!-- Path: C:\AndreOS-Memory\AndreOS\05_LOGS_IA\DGM-MAT_STARTUP_SECURITY_FOLLOWUP_2026-10-09.md -->

## Startup
- Installed reversible Startup-folder launcher at %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\DGM-MAT Headless.lnk.
- It points to pythonw.exe and scripts/autostart/backend_service.py start, not the cockpit.
- Original shortcut was backed up to %LOCALAPPDATA%\DGM-MAT\startup-backup\DGM-MAT Headless.original.lnk.
- Rollback: scripts/autostart/uninstall_backend_startup.ps1 restores the original shortcut.
- Simulated stop -> hidden shortcut launch -> health check. Passed; current API PID at validation was 4800 (pythonw.exe).
- Actual reboot/logon cycle is not yet verified.

## Security
- Wildcard CORS found.
- /ws and /runtime/ws have no authentication.
- Several runtime/governance/mobile routes do not consistently enforce authentication.
- Do not expose via LAN/Tailscale/public tunnel yet. Keep loopback 127.0.0.1:8181 until global HTTP/WebSocket auth policy and denial tests are complete.

## Files
- scripts/autostart/install_backend_startup.ps1
- scripts/autostart/uninstall_backend_startup.ps1
- docs/security/API_SECURITY_BOUNDARY_AUDIT_2026-10-09.md
- reports/DGM-MAT_STARTUP_SECURITY_FOLLOWUP_2026-10-09.md
