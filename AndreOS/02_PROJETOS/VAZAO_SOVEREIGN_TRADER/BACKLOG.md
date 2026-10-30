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

## 2026-10-27 — CI Android emulador
- [ ] Confirmar resultado do run Android #40484665409 (PR #500) e rever artefactos/logcat/OCR.
- [ ] Validar Maestro após correção do caminho do APK; run #40475487893 falhou antes da instalação, apesar do build e boot do emulador terem passado.
- [ ] Depois do smoke passar, ampliar cobertura de navegação e estados offline, sem depender de seletores de acessibilidade não verificados.
- [ ] Consolidar branding pendente (#489–#493): fundo oficial, logótipo consistente no canto superior esquerdo em cockpit web/PC e arte/ícone Android/Windows. PRs abertos e não integrados em main; rever dependências e testes antes do merge.


## 2026-10-27 — fila GitHub/branding

- [x] Limpar fila antiga a pedido explícito: manter apenas PR #500 aberto.
- [x] Merge PR #498 (identidade nos registos L2 sincronizados).
- [x] Merge PR #489 (imagem de fundo do escritório virtual).
- [x] Criar branch de consolidação de branding sem abrir segundo PR: `feat/vst-brand-consolidation-2026-10-27`.
- [ ] Confirmar resultado do run #40502699078 (Android emulator + Maestro); não mergear #500 se falhar.
- [ ] Rever e validar a branch de branding: Android APK, Windows EXE/installer, arte do cockpit e placa do escritório; criar PR apenas depois de #500 fechar para respeitar um único PR aberto.
- [ ] Reaplicar com cuidado as alterações de fail-closed Coinbase (#488) e os testes de routing L2 (#497) numa branch atualizada; os PRs foram fechados sem merge por conflitos, não assumir que as alterações estão em main.


## Android virtual-office emulator smoke — 2026-10-29 (PR #520)

- [x] Correct test contract to expect supported `orientation = portrait` after `orientation = all` broke APK build.
- [x] Python tests #3260 passed on exact head `fee0ad70ff5ab932606333175986d015504520c0`.
- [ ] Recheck Android APK run #105 (ID `40961763157`), emulator smoke run #62 (ID `40961763144`), Windows EXE run #961 (ID `40961763250`) on exact head.
- [ ] Download and inspect current APK artifact and current emulator screenshot/logcat/OCR artifacts; prior failed runs produced no artifacts and older screenshots must not be reused as current proof.
- [ ] Verify Maestro opens the actual virtual-office page and MARKET RADAR is visible before capture.
- [ ] Inspect actual image dimensions and visual layout in portrait, landscape and tablet. Landscape image dimensions alone do not prove that the portrait-locked Kivy app renders correctly in landscape.
- [ ] Research supported Buildozer/Kivy rotation handling if needed; do not restore unsupported `orientation = all` without evidence.
- [ ] Keep PR #520 open/unmerged until checks and screenshots have been reviewed.


## Atualização de continuidade — 2026-10-29 (depois do handoff)

- Criado no produto `docs/ANDROID_VIRTUAL_OFFICE_VALIDATION_HANDOFF_2026-10-29.md` no commit `d8f9d34c69cb23e69ad1de211906caa3a9bf2f46`, branch `feat/virtual-office-runtime-ux-2026-10-29`, PR #520.
- HEAD confirmado da PR após o documento: `d8f9d34c69cb23e69ad1de211906caa3a9bf2f46`; PR permanece OPEN/unmerged.
- CI do HEAD do documento: Android APK #107 / ID `40963242654` pending; Android Emulator UI Smoke #64 / ID `40963242834` pending; Python tests #3262 / ID `40963242685` in_progress; Windows EXE #963 / ID `40963242833` in_progress.
- Os resultados anteriores de Python/Windows para o HEAD anterior não substituem os checks do novo HEAD. Reconsultar os quatro workflows associados ao HEAD exato.
- O handoff documenta a correção do teste obsoleto, a limitação Buildozer (`orientation = portrait`), o estado offline do escritório e a sequência de inspeção dos artefactos.
- Não há APK/novas capturas confirmados para o HEAD atual nesta atualização. Não reutilizar capturas de runs anteriores como prova.
- Próximo: monitorizar CI exato; corrigir falhas por logs; inspecionar imagens/artefactos do run de smoke; confirmar o escritório real em portrait/landscape/tablet; manter uma única PR/branch ativa e não mergear até checks verdes e inspeção visual.
- Sem validação física no telefone, ADB local, rede doméstica ou Tailscale; sem ligação real ao backend, ordens REAL ou movimentos de capital.



## Backlog atualizado — 2026-10-30

- [x] Consolidar estratégia Windows/Linux e perfis de nó na documentação (PR #521 merged).
- [x] Documentar runtime modular brain-first e escritório remoto como capacidade futura opcional.
- [x] Executar primeiro smoke cloud Obscura vs Chrome: ambos PASS na fixture local; Obscura 23,65 ms mediana vs Chrome headless 728,61 ms, 7 repetições, incluindo cold startup. Evidência preliminar apenas; não declarar ganho geral.
- [ ] Implementar interface comum para browser de investigação/read-only, mantendo Chromium/Playwright como fallback e Obscura isolada até testes de compatibilidade/fallback/circuit breaker.
- [ ] Benchmark Obscura com tarefas variadas, warm/persistent Chromium e medição de recursos; não integrar no caminho crítico sem evidência.
- [ ] Confirmar APK Buildozer com lista explícita de orientações e validar portrait/landscape/tablet; runs #133 e #90 estavam em execução no último checkpoint.
- [ ] Inspecionar artefactos de screenshot atuais; teste físico Android/PC fica BLOCKED até hardware disponível.
- [ ] Auditar o cérebro atual; implementar primeiro diagnóstico read-only (`vst doctor --json`), manifesto de componentes e testes de migração/restore.
- [ ] Manter apenas PR #522 ativa e não fazer merge antes de checks verdes + inspeção visual.


## Estado 2026-10-30 — diagnóstico runtime

- Adicionado na branch da PR #522 o protótipo `PC_ENGINE/tools/doctor.py` e `tests/test_runtime_doctor.py`. É invocável como `python -m PC_ENGINE.tools.doctor --json`; ainda não existe alias/entrypoint instalado `vst doctor`. O diagnóstico não cria diretórios, não inicia serviços, não faz pedidos de rede e não imprime conteúdo/secrets de configuração.
- Commit do código/testes: `ec0de38c3f0cb637eae9d67b401fbe141cfedc92`; documentação de arquitetura foi atualizada depois. PR #522 permanece a única PR de produto aberta; HEAD ao checkpoint atual: `a01bfca0ff35f093a15a6b33d6e3b8363d8a169b`.
- Runs Android APK #137 / ID `41117638456` e Android Emulator UI Smoke #94 / ID `41117638350` estavam em execução; ambos já passaram nos testes de contrato e compilação de fontes Python, Buildozer ainda em progresso. Obscura cloud run #14 / ID `41117638379` concluído com sucesso. Verificar resultados finais e artefactos antes de merge.
- Benchmark Obscura preliminar: run #7 ID `41117040323`, 7/7 para ambos, mediana 23,65 ms Obscura vs 728,61 ms Chrome headless. Inclui processo novo por repetição e fixture local; não provar superioridade sobre browser persistente/exchanges.
