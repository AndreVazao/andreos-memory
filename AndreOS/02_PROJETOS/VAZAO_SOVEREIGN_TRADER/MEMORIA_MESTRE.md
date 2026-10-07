# VAZÃO Sovereign Trader — Memória Mestre

Fonte canónica: AndreOS/02_PROJETOS/VAZAO_SOVEREIGN_TRADER/ no repositório andreos-memory.
Produto: AndreVazao/VazaoSovereignTrader.
Último main confirmado do produto: 5910c641211d8fe7c7ef5c107515e9cbf028204a.

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
- PR #374 fecha pause(False)/resume como bypass de SAFE_MODE.
- PR #375 fecha o terceiro bypass: autonomous PAPER→REAL promotion já não pode ocorrer enquanto SAFE_MODE estiver ativo.

## Últimos checkpoints
- PR #371 merged: 984271a76c33595131183ec6fe271b686e9521a2.
- PR #372 documentation checkpoint merged: 607466a24c9fea7798b5a2e7a9f817ef614f3550.
- PR #373 merged: 91c8a08ea79bb292b79050f06aab47674ca07350.
- PR #374 merged: 42362843672d979371e4b0a16aedd91fc32ab9d4.
- PR #375 merged: 9e05e8121911a6bbb69765cec746098f3477624a.
- Documentation checkpoint after #375: 126416932deb5e3f816dadfada155c6f7fe98ce1.
- Nenhuma autorização REAL de ordem, cancelamento ou transferência está ativa.

## Validação
GitHub Actions incluído está esgotado para o ciclo atual; rotina pesada é local-first. No #373, 3 testes SAFE_MODE passaram no .venv. No #374, 4 testes SAFE_MODE passaram no .venv. No #375, 10 testes focados de autonomous promotion/SAFE_MODE passaram no .venv. O módulo completo de account reconciliation continua sujeito ao stall ambiental conhecido e não é classificado como green. Global Python não tem ccxt; .venv é o ambiente de validação correto.

## Próximo foco
1. Enumerar qualquer state-mutating API/control path ainda não coberto.
2. Tornar readiness/reconciliation/timing do recovery evidência independente e fresca, não apenas flags arbitrárias do caller.
3. Reauditar REAL caller/path end-to-end antes de qualquer autorização REAL.
4. Depois avançar para a próxima lacuna real sem inventar trabalho redundante.

## Organização
VazaoSovereignTrader continua repo independente. A memória comum é organizada por projeto em andreos-memory; não criar nested Git repositories.

## 2026-10-07 — PR #376 SAFE_MODE stop closure

- Product main: 953a8bd7db3e26f0d59a01abc41fe6a74a34484a.
- PR #376 closed a fourth SAFE_MODE exit: SovereignEngine.stop() previously forced SAFE_MODE -> OFF.
- stop() now preserves SAFE_MODE while stopping workers; only explicit recover_from_safe_mode() may clear the latch.
- Regression coverage verifies in-memory and persisted SAFE_MODE survive stop.
- Closed exit inventory: startup, pause/resume, autonomous PAPER->REAL promotion, stop.
- Local account-reconciliation suite remains inconclusive/stalled; no green claim.
- No REAL authorization/execution/transfer capability changed.
- Next: exhaustive status-mutation inventory, then independently generated/fresh/verifiable recovery evidence instead of caller-supplied booleans.


## Checkpoint 2026-10-07 — Exhaustive SAFE_MODE mutation audit + recovery evidence hardening

- Product main at audit start: `8a20e6ca099d0ec0917e9f38b399e2f24032cd49`.
- The two commits after #376 were documentation-only; product code was unchanged from the #376 code baseline.
- Exhaustive production mutation inventory found no additional SAFE_MODE exit path. Only `recover_from_safe_mode()` can write SAFE_MODE -> OFF.
- Closed exits remain: startup, pause/resume, autonomous PAPER->REAL promotion, stop.
- Added product audit document: `docs/SAFE_MODE_STATE_MUTATION_AUDIT_2026-10-07.md`.
- `recover_from_safe_mode()` now generates preflight/readiness/reconciliation/timing evidence internally, verifies freshness, persists the evidence actually used, and rejects caller-supplied boolean evidence claims.
- REAL recovery requires a fresh REAL authorization window; no REAL execution or capital operation was enabled.
- Added authenticated `POST /safe-mode/recover` for explicit operator confirmation.
- Local compile and diff-check passed. Pytest remains inconclusive/stalled; no green claim.
- Next: focused recovery validation, then complete REAL caller/path audit.


## Checkpoint 2026-10-07 — Focused recovery validation + REAL caller-path audit

- Product checkpoint after the prior recovery hardening is now followed by a focused validation increment.
- 7 focused recovery tests passed in .venv: stale readiness, failed preflight, required/stale timing, missing fresh REAL authorization, explicit PAPER recovery, and preservation of SAFE_MODE on failures.
- Full account-reconciliation pytest still stalls in the Windows environment; no green claim for the full suite.
- Audited production REAL callers: POST /real/arm, POST /real/disarm, POST /start, POST /mode, autonomous PAPER→REAL promotion, and recover_from_safe_mode().
- Found and fixed /mode REAL authorization sequencing: it now consumes the one-shot RealModeGuard authorization before SovereignEngine.set_mode("REAL"), which explicitly requires freshly consumed authorization.
- Added product audit: docs/REAL_AUTHORIZATION_CALLER_PATH_AUDIT_2026-10-07.md.
- Added/updated product roadmap and handoff documentation.
- No REAL execution, order, cancellation, transfer, or capital authorization was enabled.
- Next: audit the complete REAL_ACTIVE execution chain through order gate, adapter, authoritative outcome, persistence, ledger and recovery; add API-level regression coverage for /mode without live services.
