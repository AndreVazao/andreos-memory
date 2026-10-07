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

## PR #373
- start() deixa de converter implicitamente SAFE_MODE em RUNNING.
- Recovery explícito requer confirmação humana e evidência de readiness/reconciliation/timing.
- REAL recovery continua condicionado ao ExecutionGate.
- Cobertura: múltiplos restarts + bloqueio de start + recovery explícito persistindo OFF.
- Main: 91c8a08ea79bb292b79050f06aab47674ca07350.
- 3 testes focados SAFE_MODE passaram no .venv local.
- Full account-reconciliation permaneceu inconclusive por stall ambiental conhecido.

Baseline: PAPER/read-only default. Nenhuma autorização REAL ativa.
