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
