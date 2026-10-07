# VAZÃO Sovereign Trader — Memória Mestre

Fonte canónica: AndreOS/02_PROJETOS/VAZAO_SOVEREIGN_TRADER/ no repositório andreos-memory.
Produto: AndreVazao/VazaoSovereignTrader.
Último main confirmado do produto: 42362843672d979371e4b0a16aedd91fc32ab9d4.

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
- PR #371 tornou SAFE_MODE causado por mismatch autoritativo persistente através de restart.
- PR #373 impede que start() normalize SAFE_MODE para RUNNING e cria recovery explícito.
- PR #374 fecha o segundo bypass: pause(False)/resume já não podem limpar SAFE_MODE.

## Últimos checkpoints
- PR #371 merged: 984271a76c33595131183ec6fe271b686e9521a2.
- PR #372 documentation checkpoint merged: 607466a24c9fea7798b5a2e7a9f817ef614f3550.
- PR #373 merged: 91c8a08ea79bb292b79050f06aab47674ca07350.
- PR #374 merged: 42362843672d979371e4b0a16aedd91fc32ab9d4.
- Documentation checkpoint after #374: b19181d97dc4ffc4528ba3d98ca82f042da18cec.
- Nenhuma autorização REAL de ordem, cancelamento ou transferência está ativa.

## Validação
GitHub Actions incluído está esgotado para o ciclo atual; rotina pesada é local-first. No #373, 3 testes SAFE_MODE passaram no .venv. No #374, 4 testes SAFE_MODE passaram no .venv. O módulo completo de account reconciliation continua sujeito ao stall ambiental conhecido e não é classificado como green. Global Python não tem ccxt; .venv é o ambiente de validação correto.

## Próximo foco
1. Enumerar todos os state-mutating API/control paths.
2. Garantir que nenhum deles limpa SAFE_MODE fora de recover_from_safe_mode().
3. Tornar readiness/reconciliation/timing do recovery evidência independente e fresca, não apenas flags arbitrárias do caller.
4. Reauditar REAL caller/path end-to-end antes de qualquer autorização REAL.
5. Depois avançar para a próxima lacuna real sem inventar trabalho redundante.

## Organização
VazaoSovereignTrader continua repo independente. A memória comum é organizada por projeto em andreos-memory; não criar nested Git repositories.