# DGM-MAT — Provider API and Human Approval Integration
<!-- Path: C:\AndreOS-Memory\AndreOS\05_LOGS_IA\DGM-MAT_PROVIDER_API_APPROVAL_INTEGRATION_2026-10-09.md -->

Date: 2026-10-09
Project: AndreVazao/DGM-MAT
State: implementation validated, committed, and pushed; providers remain safe-off.
Main commit: 8498e688e09bbad6a475da80143b2ab765415301
Original-source archive commit: 2c17436e72413803aa492f5522ffdb980cb46ec9

## Changes

- Added authenticated API router core/api/provider_execution_api.py and included it in core/api/api_server.py.
- Added request creation, operator-only approval queue, operator-only approve/reject, and execution of only the exact stored/approved message envelope.
- API and operator bearer secrets must be different and configured via DGM_PROVIDER_API_TOKEN and DGM_PROVIDER_OPERATOR_TOKEN; absent/equal secrets fail closed. Optional audit label: DGM_PROVIDER_OPERATOR_ID.
- Extended durable approval storage to retain the exact messages and SHA-256 request fingerprint, claim the approval once, and append a non-sensitive execution outcome without storing provider response text.
- The generic queue consumer remains unable to execute these approvals (is_approved=False).
- Providers remain safe-off; no live provider or credential was activated or accessed.

## Validation status

- py_compile succeeded for changed Python modules.
- Focused provider service + durable approval store + API integration tests passed: 30 tests, exit code 0, including durable envelope persistence and outcome audit tests.
- git diff --check passed.
- Full repository suite passed with exit code 0 using python -m pytest -q --disable-warnings; pytest progress output did not include a numeric test summary.
- Production runtime database was not modified for a smoke test; approval persistence/outcome audit are covered by isolated SQLite tests.
- Main implementation: https://github.com/AndreVazao/DGM-MAT/commit/8498e688e09bbad6a475da80143b2ab765415301.
- Original-source archive: https://github.com/AndreVazao/DGM-MAT-OS/commit/2c17436e72413803aa492f5522ffdb980cb46ec9.
- Final validation report commit pushed: https://github.com/AndreVazao/DGM-MAT/commit/5ae3ef4c2e7fa2e0dcb03afc6fe0f2ea5a345521.
- Persistent memory record was committed and pushed to AndreVazao/andreos-memory (initial record commit: de3613ac579c2eaa1d4169f530e9413c6d64fce1).
- Existing API TestClient/httpx and startup event deprecation warnings remain unrelated; Pydantic deprecation warnings were removed.

## Safety limits

- This does not globally authenticate legacy API routes.
- Rate limiting is process-local (10 requests per provider per minute).
- The operator token is a shared bearer credential, not individual user identity.
- Production database validation, private deployment of distinct bearer secrets, and an explicit operator decision are required before considering provider activation.
- Immutable mirror C:\ProgramasGodMode\DGM-MAT-FULL-MIRROR remains untouched.
