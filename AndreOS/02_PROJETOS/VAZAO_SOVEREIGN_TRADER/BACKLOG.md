# VAZÃO Sovereign Trader — Backlog Vivo

## P0 Recovery/reconciliation
- [x] Auditar crash/restart permutations relevantes já identificadas.
- [x] Cobrir BLOCKED/SAFE_MODE após múltiplos restarts.
- [x] Impedir normalização implícita de SAFE_MODE no startup.
- [x] Definir e testar recovery path explícito para sair de SAFE_MODE.
- [x] Fechar bypass de SAFE_MODE via pause(False)/API /resume.
- [x] Garantir que mismatch autoritativo nunca gera state correction automática.
- [x] Confirmar idempotência de evidence/ledger nos crash windows cobertos.
- [x] Enumerar todos os state-mutating API/control paths e provar que nenhum limpa SAFE_MODE fora de recover_from_safe_mode().
- [x] Garantir que readiness/reconciliation/timing usados no recovery são evidência independente, fresca e verificável, não apenas flags arbitrárias do caller.

## P1 Runtime
- Continuar capability evidence/freshness/readiness audit.
- Expandir observabilidade de UNKNOWN outcomes.
- Manter adapters PAPER/read-only antes de REAL.

## P1 Radar
- Evoluir Market Radar multi-venue.
- Normalizar market data e timestamps.
- Medir vantagem temporal de fontes sem confundir latência com edge económico.
- Evoluir opportunity registry e capital ladder.
- Agents externos permanecem advisory até verificáveis.

## P2 Surfaces
- Browser automation.
- Desktop application.
- Android/emulator.
- Cockpit/sinalética por venue/capability.
- First-install/USB bootstrap dentro das fronteiras de segurança.

## P2 Release
- Manter local validation.
- EXE/installer final via Actions manual/tag.
- APK final via Actions manual/tag.
- Não forçar Android build local.


## 2026-10-07 — PR #376 SAFE_MODE stop closure

- Product main: 953a8bd7db3e26f0d59a01abc41fe6a74a34484a.
- PR #376 closed a fourth SAFE_MODE exit: SovereignEngine.stop() previously forced SAFE_MODE -> OFF.
- stop() now preserves SAFE_MODE while stopping workers; only explicit recover_from_safe_mode() may clear the latch.
- Regression coverage verifies in-memory and persisted SAFE_MODE survive stop.
- Closed exit inventory: startup, pause/resume, autonomous PAPER->REAL promotion, stop.
- Local account-reconciliation suite remains inconclusive/stalled; no green claim.
- No REAL authorization/execution/transfer capability changed.
- Next: exhaustive status-mutation inventory, then independently generated/fresh/verifiable recovery evidence instead of caller-supplied booleans.


## 2026-10-07 — Audit / recovery checkpoint

- [x] Exhaustively inventory production status mutation paths and prove SAFE_MODE cannot be cleared except by explicit recovery.
- [x] Replace caller-supplied readiness/reconciliation/timing booleans in recovery with engine-generated fresh evidence.
- [ ] Complete focused runtime validation of the hardened recovery contract; existing Windows pytest stall remains inconclusive.
- [ ] Complete end-to-end REAL caller/path audit after recovery evidence contract is stable.

## Próximo bloco — REAL side-effect/caller hardening

1. Criar cobertura estática/contratual para impedir novos adapters externos sem authorization boundary.
2. Adicionar testes de crash-window: aceite externo -> falha antes de persistência final -> restart -> resolução por client_order_id.
3. Auditar callers de cancelamento, withdrawal/transfer e execution surfaces browser/Android.
4. Manter REAL totalmente não exercitado e PAPER-first; qualquer ambiguidade permanece UNKNOWN/SAFE_MODE.

- [x] Rejeitar ordens REAL sem `client_order_id` não vazio antes do autorizador e do adapter.
- [x] Criar contrato AST que restringe chamadas diretas de submissão CCXT ao adapter aprovado.
