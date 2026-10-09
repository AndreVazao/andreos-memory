# DGM-MAT API Security Phase A — Inventory Enforcement
**Date:** 2026-10-09

Added `core/api/security_policy.py` and `tests/security/test_api_security_policy.py` in DGM-MAT. The policy inventories current HTTP routes, both WebSockets, docs endpoints and the optional mobile static mount. A test fails when a route is added without explicit classification; only `GET /health` is classified public. Added a constant-time strict bearer comparison helper that fails closed on missing credentials/configuration.

Focused security/API tests: 11 passed. Full repository suite `python -m pytest -q --disable-warnings` completed with exit code 0 in 55.44 seconds. DGM-MAT commit: `3ffc079` (route inventory and auth primitives).

This is inventory plus reusable primitives only, not global authentication. Existing clients are unchanged. API remains loopback-only; no Tailscale/LAN/public access. Next: PC-local session bootstrap, migrate desktop clients, then enforce HTTP/WebSocket authentication with compatibility tests.
