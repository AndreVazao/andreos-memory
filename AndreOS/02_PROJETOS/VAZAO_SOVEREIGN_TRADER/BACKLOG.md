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

- [ ] Implementar supervisor de serviços opcionais (Ollama/Tailscale) com health-check, leases/refcount, ownership, timeout e stop seguro; falhas nunca bloqueiam o motor.
- [ ] Implementar provider de IA opcional para contexto/links, zero-paid por defeito, sem chamadas no hot path e fallback determinístico.
- [ ] Confirmar deployment Vercel/Supabase e fechar endpoint lease autenticado + descoberta PC/Android por Tailscale sem introdução manual de IP.

- [x] Implementar supervisor opcional Ollama com ownership, leases, idle grace, timeout e cleanup; 6 testes de supervisor passam.
- [x] Implementar provider local-only e interpretação advisory de páginas públicas na fila de investigação; sem inferência cloud e com fallback determinístico.
- [ ] Validar inferência real com modelo local já instalado, com limite de tempo/recursos e sem descarregar modelos.
- [ ] Confirmar plano/custos de Supabase antes de provisionar backend partilhado; Vercel não tem environment variables configuradas.
- [ ] Ligar cliente PC e Android ao endpoint lease assinado e testar reconexão/offline com Tailscale sem IP manual.

## Android/remote cockpit — 2026-10-20

- [x] Adicionar campos Android separados para endereço LAN e endereço Tailscale; manter configuração local.
- [x] Compatibilidade de leitura com o antigo `pc_url`, migrando para LAN sem inferir que é Tailscale.
- [x] Permitir failover LAN→Tailscale só para GET em falha de rede/timeout; nunca repetir automaticamente POST/uploads/comandos; não contornar 401/403.
- [x] Executar testes puros de endpoint selection no workflow Android antes do build; run #45 passou.
- [ ] Adicionar testes mockados para migração e comportamento real de `_request` (LAN OK, fallback, ambos offline, 401/403, POST sem replay).
- [ ] Usar endpoint privado autenticado para confirmar autorização; `/health` não é prova de autenticação.
- [ ] Validar arranque do APK no Redmi Android 16 com logcat e testar rede Wi-Fi de casa / Tailscale fora de casa.
- [ ] Preservar PR #388 como única PR ativa deste bloco; não fazer merge até revisão do diff e confirmação dos checks.

## L2 market data — 2026-10-27
- [x] PR #495 adiciona callback OKX ao collector runner e separa JSONL sincronizado por venue (PR aberto; testes Python e Windows build observados com sucesso nos runs #40472713932 / #40472713919).
- [x] PR #496 adiciona teste do contrato de persistência e fail-closed para venue desconhecida (CI em execução quando anotado; não declarar green sem rever run).
- [ ] Confirmar CI #496.
- [ ] Rever estado/merge de PR #488 Coinbase fail-closed e stack de branding (#489–#493); não assumir merge automático.
- [ ] Integrar telemetry persistida no depth-edge PAPER só depois de mapping canónico explícito, equivalência de instrumento, clock domain comum, freshness/skew, custos por venue e replay validados.
- [ ] Fazer validação visual em browser/Android/Windows; CI de packaging não substitui teste visual em dispositivo.
- [ ] PR #497 substitui a tentativa #496 fechada; confirmar Python tests run #40473392788 e Windows EXE run #40473392950 antes de marcar como validado.
## Android emulator smoke — 2026-10-27
- [x] PR #499 adds hosted Android API 35 emulator + Maestro CLI startup smoke (PR open; run #40475487893 in progress at checkpoint).
- [ ] Verify run #40475487893 result, screenshot/OCR/logcat artifacts; fix failures before treating emulator validation as green.
- [ ] After smoke passes, add a small number of robust Maestro flows for cockpit navigation and offline states; don't assume Kivy widgets are accessible to Maestro without checking screenshot/accessibility evidence.
- [ ] Keep physical Android device validation separate from emulator CI.
- [x] Windows EXE/installer workflows use Windows-hosted runner; package smoke passed on run #40473392950. Physical user PC remains unverified.