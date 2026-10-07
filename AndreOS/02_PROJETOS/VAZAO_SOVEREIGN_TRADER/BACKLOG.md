# VAZÃO Sovereign Trader — Backlog Vivo

## P0 Recovery/reconciliation
- Auditar restantes crash/restart permutations.
- Cobrir BLOCKED/SAFE_MODE após múltiplos restarts.
- Impedir normalização implícita de SAFE_MODE no startup.
- Definir recovery path explícito para sair de SAFE_MODE.
- Garantir que mismatch autoritativo nunca gera state correction automática.
- Confirmar idempotência de evidence/ledger em todos os crash windows.

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