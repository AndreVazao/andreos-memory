# VAZÃO Sovereign Trader — Histórico Consolidado

Capability/readiness: #338-#343.
Capital transfer: #344-#346.
Actions/local-first: #355-#361.
Recovery/reconciliation: #359, #362-#370.
Authoritative mismatch -> SAFE_MODE audit: #366.
Engine startup recovery replay: #367.
Corrupt backup recovery: #369.
Invalid primary / valid backup recovery: #370.
SAFE_MODE persistente através de restart: #371.
Documentação do checkpoint: #372.
Explicit SAFE_MODE recovery / startup hardening: #373.
SAFE_MODE resume bypass closure: #374.
SAFE_MODE autonomous promotion closure: #375.

## PR #375
- `_maybe_autonomous_real_promotion()` bloqueia imediatamente em SAFE_MODE.
- Regression: 10 testes focados passaram no .venv.
- Main: 9e05e8121911a6bbb69765cec746098f3477624a.

Baseline: PAPER/read-only default. Nenhuma autorização REAL ativa.


## 2026-10-07 — PR #376 SAFE_MODE stop closure

- Product main: 953a8bd7db3e26f0d59a01abc41fe6a74a34484a.
- PR #376 closed a fourth SAFE_MODE exit: SovereignEngine.stop() previously forced SAFE_MODE -> OFF.
- stop() now preserves SAFE_MODE while stopping workers; only explicit recover_from_safe_mode() may clear the latch.
- Regression coverage verifies in-memory and persisted SAFE_MODE survive stop.
- Closed exit inventory: startup, pause/resume, autonomous PAPER->REAL promotion, stop.
- Local account-reconciliation suite remains inconclusive/stalled; no green claim.
- No REAL authorization/execution/transfer capability changed.
- Next: exhaustive status-mutation inventory, then independently generated/fresh/verifiable recovery evidence instead of caller-supplied booleans.
