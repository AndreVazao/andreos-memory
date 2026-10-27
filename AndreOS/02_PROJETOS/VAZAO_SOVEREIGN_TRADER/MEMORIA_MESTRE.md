# VAZÃO Sovereign Trader — Memória Mestre

Fonte canónica: AndreOS/02_PROJETOS/VAZAO_SOVEREIGN_TRADER/ no repositório andreos-memory.
Produto: AndreVazao/VazaoSovereignTrader.
Último main observado do produto: 7d680ebafe65cab7842ff690617804238c46b18c (2026-10-27; confirmar novamente antes de qualquer merge).

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

## Checkpoint 2026-10-07 — REAL_ACTIVE execution-path audit

- Product main advanced to `c679e80a5c6f45a1bfd4ef1284fb4ec1198cb1e9` and is pushed/synchronized.
- Audited REAL_ACTIVE from guarded activation through `start()` -> execution gate -> OrderManager -> exchange adapter -> outcome normalization -> pending/reconciliation -> ledger/recovery.
- No production REAL side-effect bypass was found. No live order, cancellation, transfer, or capital operation was executed.
- `start()` in REAL requires preflight, unresolved execution-intent recovery, and authoritative account reconciliation before `RUNNING`/`real_operational=True`.
- `_open_position()` / `_close_position()` require `ExecutionGate.REAL_ACTIVE` plus opportunity/risk/exchange/freshness checks; the final OrderManager authorizer re-checks REAL_ACTIVE and `real_operational` immediately before adapter side effect.
- Engine persists execution intent before external order submission and assigns deterministic client-order identity. Restart recovery resolves only against the recorded venue and exact identity; ambiguity remains fail-closed.
- Pending order reconciliation is cumulative/idempotent and does not treat submitted as filled.
- Direct production `ccxt.create_order()` reachability is confined to `CcxtExchangeClient`, called through `OrderManager`; no second production order submission path was found.
- Capital-transfer execution independently requires explicit authorization, journaled SUBMITTED-before-adapter state, idempotency key, and UNKNOWN_OUTCOME for ambiguous post-submission results; UNKNOWN is not retryable.
- `ExecutionFabric` is independently fail-closed with per-intent authorization and mandatory idempotency, though the primary engine exchange path currently uses OrderManager.
- Focused validation: **8 passed, 7 deselected in 7.60s**; audited modules compile and `git diff --check` passes.
- Full account-reconciliation suite remains known to stall on Windows and is not green.
- Product audit document: `docs/REAL_ACTIVE_EXECUTION_PATH_AUDIT_2026-10-07.md`.
- Residual backlog: static/contract proof for all future external side-effect adapters; crash-window tests between external acceptance and persistence; complete caller audit for cancellation/withdrawal/transfer and browser/Android surfaces.

## Checkpoint 2026-10-07 — PR #354 reconciliation

- Investigated the only open GitHub PR in `AndreVazao/VazaoSovereignTrader`: **#354 `fix: preserve observed partial fills across pending-order recovery`**.
- PR #354 was stale: head `8b338b9...` was 32 commits behind current `main` and 4 commits ahead, so it was not safe to merge directly.
- Its substantive change was still relevant: pending/partial **sell** recovery was discarding venue-observed cumulative fill quantity, fee, quote notional, and client-order identity.
- Reapplied that useful hardening directly on current main in commit `ee9f0d7c2d3573c2ffdd440aa7613ada4e4498ec`.
- Updated regression coverage accordingly; focused validation: **8 passed in 5.49s**, compile and diff-check passed.
- GitHub PR #354 was then **closed without merging**, because its useful content is now incorporated into current main and its branch was stale.
- No REAL order/capital operation was executed. PAPER-first and fail-closed constraints remain unchanged.
- Product main and persistent memory must remain synchronized after this checkpoint.


## Checkpoint 2026-10-07 — crash-window / UNKNOWN_OUTCOME hardening

- Product main advanced to `1246531` (`Harden ambiguous external order recovery`) and was pushed to `origin/main`.
- Closed a critical crash window: OrderManager exceptions during/after the external adapter call now become `UNKNOWN_OUTCOME`, not a normal rejection.
- REAL engine buy/sell paths retain the durable `execution_intent` and enter SAFE_MODE on UNKNOWN_OUTCOME; they never blindly retry.
- Adapter response contract violations after an external call are also treated as UNKNOWN_OUTCOME.
- Immediate returned `clientOrderId` mismatches are rejected as unsafe adapter identity mismatches.
- Removed duplicate/dead execution method implementations from `SovereignEngine`; AST audit now reports no duplicate methods.
- Added regression coverage for ambiguous external outcomes, intent retention, adapter identity mismatch and restart-safe recovery.
- Focused validation: **26 passed in 12.44s**; py_compile and git diff --check passed.
- Added product document: `docs/REAL_EXECUTION_CRASH_WINDOW_HARDENING_2026-10-07.md`.
- No REAL order, transfer, withdrawal, capital movement or paid service was executed. PAPER-first/fail-closed remains unchanged.
- Next: static/contract proof for every external side-effect adapter; complete cancellation/transfer/withdrawal and Browser/Android caller audit; deterministic restart/reconciliation integration tests.


## Checkpoint 2026-10-08 — Conversational Mobile Cockpit

- Product main advanced to `7ea1a89` (`Add conversational mobile cockpit`) and was pushed to `origin/main`.
- Android UI was redesigned as a compact ChatGPT-like cockpit: sidebar, central conversation, message composer, voice/transcription entry, and dedicated PC/Ficheiros/Humano/Readiness views.
- Added `PC_ENGINE/api/assistant_gateway.py`: deterministic conversational routing for STATUS, PAPER start/pause/resume/stop, research requests, generic chat and explicit REAL blocking.
- The gateway is an operator UX boundary, not a second trading executor. It never creates REAL authorization and continues to rely on existing engine gates/scopes.
- Mobile pairing scope set now includes `submit_research`, while `trade_real` and exchange-account management remain unavailable to device tokens.
- Added Android Speech Recognizer integration using `pt-PT` and `RECORD_AUDIO`; speech is transcribed locally into the composer before sending.
- Added `tests/test_operator_assistant_gateway.py`; focused gateway + mobile pairing + API validation: **14 passed in 5.34s** after the final UI cache patch.
- Production/mobile modules compile and `git diff --check` passes.
- Added product doc: `docs/MOBILE_CHAT_COCKPIT_2026-10-08.md`.
- Android build workflow #32: run `37780479751`, triggered from `7ea1a89`; build was in progress at checkpoint time. Physical Redmi installation remains pending because the phone is away/offline from ADB.
- No REAL order, cancellation, withdrawal, transfer, capital movement, or paid service was executed. PAPER-first/fail-closed remains unchanged.
- Deliberate limitation: current gateway is deterministic, not a general LLM. Future LLM integration must sit behind the same gateway and security gates.


## Checkpoint 2026-10-09 — client-order identity boundary

- `OrderManager` exige agora `client_order_id` REAL não vazio antes do callback de autorização ou de qualquer adapter; valores ausentes/vazios/brancos são rejeitados sem side effect. PAPER permanece compatível.
- `tests/test_external_side_effect_adapter_contract.py` impõe um contrato AST para confinar chamadas diretas de submissão CCXT ao adapter aprovado.
- Validação focal alargada: 25 testes passaram; `py_compile` e `git diff --check` passaram. A suíte completa não foi declarada verde.
- Código commitado apenas na branch local `hardening/require-client-order-id-at-real-boundary`; publicação adiada para preservar a quota de GitHub Actions. Artefactos APK não foram incluídos.
- Não houve chamadas a exchanges nem operações de capital. REAL continua bloqueado.

## Política Claude Code / NVIDIA NIM para o Trader

Claude Code v2.1.112 e o smoke FCC/NVIDIA NIM foram encontrados na memória transversal; o smoke devolveu `NIM_OK`, mas não demonstra gratuitidade contínua ou fiabilidade de tool-use. A integração no Trader fica adiada até confirmar limites/custos e um contrato isolado. Qualquer LLM é advisory para pesquisa/análise; não pode autorizar ordens, mudar limites de risco, contornar gates ou desbloquear REAL. Ollama permanece não validado.


## Política zero-custo / IA local / ciclo de serviços (2026-10-09)

- O proprietário não autoriza gastos com inferência/API. Cloud NIM/FCC/Claude Code não podem ser invocados automaticamente pelo Trader; a inferência paga fica desativada por defeito. O output `$0.100344` do CLI é custo reportado, não cobrança confirmada; não gastar mais quota para investigar sem ordem explícita.
- Trader continua funcional sem IA. Nenhum LLM no hot path de market data, risco ou execução. AI opcional serve apenas para interpretar intenção/contexto, resumir links e propor hipóteses de pesquisa, com output não confiável e validação determinística/PAPER/OOS. Falha, timeout, ausência de modelo ou falta de RAM não bloqueiam o Trader.
- Ollama CLI 0.23.0 está instalado, daemon desligado; inventário de modelos ainda não confirmado. Claude CLI/Node e Tailscale CLI encontrados. Vercel CLI ausente do PATH não prova ausência de deploy. Tailscale PC online, Redmi offline no último status. Nenhum serviço foi arrancado/parado durante a inspeção.
- Novo documento: `docs/OPTIONAL_LOCAL_AI_AND_SERVICE_LIFECYCLE.md`. Define supervisor futuro com health checks, leases/refcount, ownership de processos, idle timeout, sem matar processos preexistentes, fallback determinístico e sem start no hot path. Isto é uma decisão arquitetural, não funcionalidade já implementada.
- Discovery PC/Android pretendida: Vercel autentica owner/device e distribui lease curta de endereço Tailscale; depois ligação direta autenticada PC↔Android. Sem introdução de IP no uso normal; cloud nunca transporta ordens nem se torna dependência local. USB pode continuar necessário para bootstrap/approval.
- Código local na branch `hardening/require-client-order-id-at-real-boundary`: `68a0f56` hardens client identity REAL; `dae435a` documents zero-cost optional AI/service lifecycle. `artifacts/` não versionado. Não houve chamadas a exchange ou ações de capital.


## Checkpoint 2026-10-09 — supervisor Ollama e contexto local

- Inventário sem arrancar serviços: Ollama 0.23.0 instalado e daemon desligado; manifests locais `deepseek-r1:1.5b`, `llama3.2:1b`, `qwen2.5:1.5b`, `qwen2.5-coder:1.5b`; cache aproximada 4.11 GB. Runtime/inferência real ainda não validado.
- Commit local `d7d6a05` adiciona `PC_ENGINE/services/optional_service_supervisor.py`: allow-list exclusiva para Ollama, health-check localhost, ownership do processo exato, leases/refcount, idle grace, timeout e cleanup. Nunca gere Tailscale.
- `PC_ENGINE/research/local_context_assistant.py` usa exclusivamente localhost/Ollama, deteta modelo em cache sem iniciar daemon, não descarrega modelos, limita entradas/respostas, usa `keep_alive=0` e falha sem bloquear. `VST_LOCAL_CONTEXT_AI=off` desativa a capacidade.
- `ResearchWorker` só pede interpretação ao modelo quando pelo menos uma página pública foi obtida. Texto do modelo é marcado como advisory não validado; não altera categoria, avaliação, risco nem execução. Não há inferência cloud implementada.
- Commit local seguinte `97048dd` atualiza documentação com verificação Vercel. `git diff --check` e `py_compile` passaram; 17 testes supervisor/context/research + 8 testes de fronteira REAL passaram (25 total). Testes executados com `VST_LOCAL_CONTEXT_AI=off` para não arrancar daemon durante a suíte.
- API Vercel: health `200`, GET endpoint lease `405`, POST anónimo `{}` `401 unauthorized`. Rotas estão implantadas. Inventário de environment variables Vercel vazio (`envs=[]`, `hiddenProductionEnvCount=0`). Supabase lista apenas `baribudos-studio-website` INACTIVE; nenhum projeto ativo de shared-learning/trader. Descoberta autenticada PC/mobile ainda não funciona ponta-a-ponta; falta backend/env. Nenhuma chave/valor de segredo foi lido; nenhum projeto criado ou deployment alterado por política de custo zero.
- Branch de produto continua local `hardening/require-client-order-id-at-real-boundary`; commits desta sessão `d7d6a05`, `97048dd`. `artifacts/` segue untracked e não foi commitado. Sem chamadas a exchange, operações de capital ou REAL.

## Continuidade Android/LAN/Tailscale — 2026-10-20

- Produto repo: `AndreVazao/VazaoSovereignTrader`; trabalho ativo na única PR #388: https://github.com/AndreVazao/VazaoSovereignTrader/pull/388, branch `feat/headless-clients-office-apk-2026-10-20`. Não abrir PR paralela para este bloco e não fazer merge sem decisão/validação.
- Android agora tem campos separados `lan_url` e `tailscale_url`, guardados localmente em `connection.json`. Configuração antiga `pc_url` é migrada para LAN por compatibilidade; não inferir que é Tailscale.
- `GET` pode passar de LAN para Tailscale apenas após falha de rede/timeout; pedidos não-GET, uploads e comandos nunca são repetidos automaticamente. Respostas HTTP 401/403 são definitivas e não desencadeiam failover.
- `/health` é público e só prova reachability; a validação de autenticação exige uma futura leitura privada protegida. Nenhum endereço LAN/token é publicado em Vercel.
- Actions run #45 / ID 39419467665 passou os testes atuais do seletor e construiu/uploadou APK debug. Isto não prova que o APK arranca no telefone. A validação física Android 16/logcat continua pendente.
- Documentação do produto atualizada em `docs/ANDROID_LAN_TAILSCALE_IMPLEMENTATION_CONTRACT.md` e `docs/PROJECT_CONTEXT.md`. Próximos passos: testes mockados de `_request`/migração, autenticação via endpoint privado, confirmar layout e validar no aparelho. Não tocar em REAL/trading engine.

## Checkpoint 2026-10-27 — recuperação de avanços externos e novo teste L2

- Produto main observado em 7d680ebafe65cab7842ff690617804238c46b18c (docs/audit refresh).
- PR #495 aberto: sincronizador OKX ligado ao runner L2; persistência por venue (Binance/Coinbase/OKX), Python tests green, Windows EXE workflow success com artefacto. Não demonstra edge executável.
- PR #496 criado como extensão de #495: helper de persistência testável, routing dedicado por venue e rejeição fail-closed para venue desconhecida. Python/Windows CI estava em progresso na última verificação; não declarar green sem rever run.
- Branding: PR #491 Android APK CI success; PR #492 Windows EXE/installer CI success e artefacto publicado. Device/browser visual validation ainda pendente.
- PR #488 fail-closed Coinbase continua aberto; não confundir com código já merged.
- Regra: não fazer merge automaticamente. PAPER/read-only, sem live orders, sem credenciais privadas. Persistência de livro sincronizado != edge económico; ainda faltam mapping canónico validado, custos/fill assumptions, frescura/skew, integração/replay e evidência.
## Correção/atualização — 2026-10-27 08:26 UTC
- PR #495 foi merged por outra sessão/conta em 08:23 UTC, merge commit 011efeb26db80291a96032d1de042c2c3fed6389. O código OKX -> runner e JSONL separado por venue está agora em main.
- PR #496 foi criado com base no commit pré-merge e depois fechado para evitar PR divergente; não usar como referência ativa.
- PR #497 é a versão limpa do teste de persistência sobre main: https://github.com/AndreVazao/VazaoSovereignTrader/pull/497, branch test/l2-persistence-contract-main-2026-10-27.
- PR #497 acrescenta helper de persistência testável, teste de routing Binance/Coinbase/OKX e fail-closed para venue desconhecida, e clarifica documentação.
- CI #497 ainda em execução: Python tests run 40473392788 e Windows EXE run 40473392950. Não afirmar green até conclusão.
- A branch temporária #496 está fechada; não fazer merge dela.
## Checkpoint 2026-10-27 — Android emulator + Maestro

- Produto main observado: 011efeb26db80291a96032d1de042c2c3fed6389.
- PR #497 permanece aberto: https://github.com/AndreVazao/VazaoSovereignTrader/pull/497. Python tests run 40473392788 e Windows EXE run 40473392950 concluíram success. Não fazer merge automaticamente.
- PR #499 aberto: https://github.com/AndreVazao/VazaoSovereignTrader/pull/499; branch feat/android-emulator-maestro-smoke-2026-10-27, HEAD 826b6a8a10cc58a39cfe28cb4c993da39ba2d4f2.
- PR #499 adiciona workflow `.github/workflows/android-emulator-maestro.yml`, flow `.maestro/android-startup-smoke.yaml` e docs `docs/ANDROID_EMULATOR_TESTING.md`.
- O workflow constrói APK de teste x86_64 temporário, inicia Android API 35 no runner Linux via KVM, instala APK, corre Maestro CLI, confirma processo vivo, captura screenshot/logcat e usa OCR para verificar texto inicial. O APK x86_64 não é release; o workflow APK de produção ARM64 fica separado.
- Run #40475487893 estava `in_progress` na última consulta; não afirmar sucesso até terminar e inspecionar logs/artifact. Link: https://github.com/AndreVazao/VazaoSovereignTrader/actions/runs/40475487893.
- Maestro CLI open-source sem Maestro Cloud/token; sem custos de serviço extra previstos além dos limites normais de GitHub Actions. Confirmar limites/consumo se necessário.
- Windows já é testado em runner Windows nativo, com build/smoke do EXE e instalador. Não se implementou nested Windows VM; não é necessário para o smoke de pacote. Máquina Windows física do utilizador ainda não foi testada.
- Não há ligação à PC API/exchanges, credenciais ou ordens. Teste é apenas smoke de arranque e renderização, não cobertura completa de funcionalidades ou dispositivo físico.
- Próximo passo: verificar run #40475487893, corrigir falhas se houver; depois ampliar Maestro para navegação do cockpit se os seletores de Kivy forem verificáveis. Manter PAPER/read-only.

## Atualização operacional 2026-10-27 — Android UI smoke
- PR #499 cria workflow Android emulator + Maestro, mas o run #40475487893 falhou depois de build APK e boot do emulador passarem: o script não encontrou o APK por usar caminho relativo incompatível com o diretório de trabalho do action.
- PR #500 (https://github.com/AndreVazao/VazaoSovereignTrader/pull/500) corrige pesquisa do APK via GITHUB_WORKSPACE e reforça recolha de evidência; run #40484665409 estava queued na última verificação.
- Branding: PRs #489–#493 estão abertos, não integrados em main. #489 fundo do escritório virtual; #490 arte no APK; #491 ícone launcher Android; #492 ícones Windows EXE/instalador; #493 placa do CEO. A presença de ficheiros/PRs não significa aplicação em todas as interfaces. O shell web tem SVG no topo; MOBILE_APP ainda mostra VST textual e PC_ENGINE/api/cockpit.py usa cabeçalho textual. Falta consolidação visual transversal e validação de build/renderização.
- Estado base observado: main 011efeb26db80291a96032d1de042c2c3fed6389. Não fazer merge automático; utilizador faz merge. PAPER/read-only permanece obrigatório.


## GitHub hygiene — 2026-10-27

- Main do produto confirmado: `a109a2d0c7be18364cbfeee38f89aded327037cf`.
- PRs merged nesta limpeza: #498 (`087144e668769ab6e51c2e524597703b61ae2240)) e #489 (`a109a2d0c7be18364cbfeee38f89aded327037cf)).
- Apenas PR aberto no produto: #500 (Android emulator/Maestro smoke + correção de paths), HEAD `5c1b96f0b99a42408769fc04757926074cc0beff`; run #40502699078 ainda em progresso na última consulta.
- PRs #485, #486, #488, #490–#493, #497 e #499 fechados sem merge devido a conflitos/dependências. Os respetivos branches continuam no repositório; alterações pendentes têm de ser reintroduzidas e testadas antes de serem consideradas integradas.
- Branch de trabalho sem PR: `feat/vst-brand-consolidation-2026-10-27`, commit `edcd4ed4cdd6bb9b82e659333fa0fb88a3d8c136`. Não está validada nem merged.
- Política continua PAPER/read-only, fail-closed e sem merge de #500 antes do CI verde.
