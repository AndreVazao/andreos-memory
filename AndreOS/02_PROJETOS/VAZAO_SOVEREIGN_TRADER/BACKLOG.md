# VAZÃO Sovereign Trader — Backlog Vivo

## P0 Recovery/reconciliation
- [x] Auditar restantes crash/restart permutations relevantes.
- [x] Cobrir BLOCKED/SAFE_MODE após múltiplos restarts.
- [x] Impedir normalização implícita de SAFE_MODE no startup.
- [x] Definir e testar recovery path explícito para sair de SAFE_MODE.
- [x] Garantir que mismatch autoritativo nunca gera state correction automática.
- [x] Confirmar idempotência de evidence/ledger nos crash windows cobertos.
- [ ] Auditar todos os callers/API que possam limpar SAFE_MODE fora de recover_from_safe_mode().
- [ ] Garantir que readiness/reconciliation/timing usados no recovery são evidência independente e fresca, não apenas flags arbitrárias do caller.

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
