# DGM-MAT — Governed Provider Execution Service — 2026-10-09

A bounded, chat-only governed provider execution service was added locally for the next DGM-MAT phase.

Files:
- `DGM-MAT/core/provider_sync/governed_provider_service.py`
- `DGM-MAT/core/provider_sync/durable_provider_approval_store.py`
- `DGM-MAT/tests/provider_sync/test_governed_provider_service.py`
- `DGM-MAT/docs/architecture/GOVERNED_PROVIDER_EXECUTION_SERVICE.md`
- `DGM-MAT/reports/DGM-MAT_GOVERNED_PROVIDER_EXECUTION_2026-10-09.md`

Security contract:
- No HTTP/cockpit/orchestrator wiring; provider registration remains safe-off.
- Only chat is supported. No tools, browser, file writing or shell execution.
- Input and response sizes are bounded; one async adapter call under timeout; no retries; exceptions become generic codes; common bearer/API-key patterns are redacted from returned text.
- Optional durable approval is bound to a SHA-256 fingerprint of provider ID, request ID and canonical messages. Approval must include an approved state, operator and timestamp; it is claimed through a conditional DB update, with the approval record moved to RUNNING and is_approved=False.
- The approval store helper can create a provider-specific approval request with that fingerprint.
- No credentials were retrieved; no live provider activated; immutable mirror untouched.
- Rate limiter is still process-local. SQLite tests verify single-use claims, but the configured production database still needs environment-specific validation before high-impact use; timeout cancellation remains adapter-dependent.
- Focused service and SQLite approval-store tests passed (exit code 0). Full pytest suite passed after final code changes (exit code 0). `git diff --check` and `py_compile` passed.
- Published to `AndreVazao/DGM-MAT`, branch `main`, commit `086ca1f8781d66594ffd4d0e20d99ef43c23b017`; local HEAD matched origin/main after push. Persistent-memory commit/push remains to be completed.
