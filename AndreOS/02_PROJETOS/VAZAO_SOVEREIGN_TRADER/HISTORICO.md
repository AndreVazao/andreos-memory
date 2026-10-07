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

## PR #374
- pause(False) deixa de converter SAFE_MODE em RUNNING.
- API /resume devolve 409 enquanto SAFE_MODE estiver ativo.
- Cobertura focada: 4 testes SAFE_MODE passaram no .venv.
- Main: 42362843672d979371e4b0a16aedd91fc32ab9d4.

Baseline: PAPER/read-only default. Nenhuma autorização REAL ativa.
