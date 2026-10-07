# VAZÃO Sovereign Trader — Memória Mestre

Fonte canónica: AndreOS/02_PROJETOS/VAZAO_SOVEREIGN_TRADER/ no repositório andreos-memory.
Produto: AndreVazao/VazaoSovereignTrader.
Último main confirmado do produto: 91c8a08ea79bb292b79050f06aab47674ca07350.

## Missão
Trader soberano, local-first, auditável e PAPER-first. O PC é o centro de controlo; browser, Windows e Android/emulador são superfícies operacionais. Cloud/Vercel coordena/sincroniza/aprende, mas não concede autorização autónoma para trading REAL.

## Regras inegociáveis
- PAPER é o padrão; REAL permanece bloqueado por defeito.
- REAL exige autorização humana explícita e gates independentes.
- Fail closed perante UNKNOWN, dados ambíguos, capability não verificada, freshness expirada, venue indisponível ou reconciliação falhada.
- UNKNOWN nunca recebe retry cego.
- Nunca duplicar uma ordem/transferência potencialmente executada.
- submitted != filled; filled != reconciled; reconciled != authorized.
- Nunca contornar MFA/CAPTCHA.
- Nunca guardar secrets, API keys, tokens, cookies ou credenciais nesta memória.
- Saúde operacional não é promessa de rentabilidade.

## Cadeia REAL
human authorization -> readiness freshness -> capability verification -> preflight -> reconciliation/recovery -> risk -> venue health/freshness -> execution gate -> adapter -> authoritative outcome -> persistence -> ledger -> recovery.

## Estado técnico consolidado
- Capability contracts/verifier/evidence/readiness fail-closed.
- Probes read-only para market data e account state.
- Pending-order reconciliation cumulativa com filled/cost/fee e tratamento de UNKNOWN.
- Recovery com primary, backup, journal, SHA-256 integrity, generation, atomic writes e replay idempotente.
- Crash windows relevantes já cobertos, incluindo primary/backup corruptos e journal pending.
- Capital transfer contract/journal fail-closed: PREPARED, SUBMITTED, CONFIRMED, UNKNOWN_OUTCOME, BLOCKED.
- Account reconciliation usa a venue como autoridade e nunca corrige silenciosamente o estado local.
- PR #371 tornou SAFE_MODE causado por mismatch autoritativo persistente através de restart, usando runtime_status opcional sem migração de schema.
- PR #373 impede que start() normalize SAFE_MODE para RUNNING depois de restart; SAFE_MODE agora exige recovery explícito.
- PR #373 adiciona recover_from_safe_mode() com confirmação humana e evidência explícita de readiness/reconciliation/timing; REAL continua dependente do ExecutionGate.

## Últimos checkpoints
- PR #371 merged: 984271a76c33595131183ec6fe271b686e9521a2.
- PR #372 documentation checkpoint merged: 607466a24c9fea7798b5a2e7a9f817ef614f3550.
- PR #373 merged: 91c8a08ea79bb292b79050f06aab47674ca07350.
- Nenhuma autorização REAL de ordem, cancelamento ou transferência está ativa.

## Validação
GitHub Actions incluído está esgotado para o ciclo atual; rotina pesada é local-first. No PR #373, os 3 testes focados de SAFE_MODE passaram no .venv local. O módulo completo de account reconciliation voltou a stall ambiental; foi tratado como inconclusive, nunca como green. O Python global também confirmou ausência de ccxt, pelo que a validação correta foi feita no .venv.
Actions só devem ser gastas deliberadamente para clean environment, packaging/release ou necessidade que o PC não consiga reproduzir.

## Próximo foco
1. Considerar fechado o gap de SAFE_MODE implícito no startup.
2. Auditar qualquer caller/API que possa limpar SAFE_MODE sem passar pelo recovery explícito.
3. Confirmar que evidência de recovery é produzida por fontes independentes, e não apenas flags arbitrárias de caller.
4. Reauditar REAL caller/path end-to-end antes de qualquer autorização REAL.
5. Depois avançar para a próxima lacuna real sem inventar trabalho redundante.

## Organização
VazaoSovereignTrader continua repo independente. A memória comum é organizada por projeto em andreos-memory; não criar nested Git repositories.