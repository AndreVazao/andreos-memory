# VAZÃO Sovereign Trader — Última Sessão

Data: 2026-10-07

## Trabalho desta sessão
- PR #373: SAFE_MODE persistente deixou de poder ser normalizado para RUNNING por start() após restart.
- PR #374: pause(False)/API /resume deixam de limpar SAFE_MODE.
- Auditoria seguinte encontrou bypass em `_maybe_autonomous_real_promotion()`.
- PR #375 bloqueia autonomous PAPER→REAL promotion enquanto SAFE_MODE estiver ativo.
- PR #375 merged como `9e05e8121911a6bbb69765cec746098f3477624a`.
- `.venv`: 10 testes focados de autonomous promotion/SAFE_MODE passaram.
- Handoff do produto atualizado em `126416932deb5e3f816dadfada155c6f7fe98ce1`.
- Nenhuma autorização REAL foi criada ou relaxada.

## SAFE_MODE exit audit atual
Os caminhos identificados de saída para RUNNING foram fechados em #373, #374 e #375: startup/start(); pause(False) e API /resume; autonomous PAPER→REAL promotion.

## Próximo passo
Auditar restantes control paths mutáveis e fortalecer a evidência independente/fresh do recovery explícito.


## 2026-10-07 — PR #376 SAFE_MODE stop closure

- Product main: 953a8bd7db3e26f0d59a01abc41fe6a74a34484a.
- PR #376 closed a fourth SAFE_MODE exit: SovereignEngine.stop() previously forced SAFE_MODE -> OFF.
- stop() now preserves SAFE_MODE while stopping workers; only explicit recover_from_safe_mode() may clear the latch.
- Regression coverage verifies in-memory and persisted SAFE_MODE survive stop.
- Closed exit inventory: startup, pause/resume, autonomous PAPER->REAL promotion, stop.
- Local account-reconciliation suite remains inconclusive/stalled; no green claim.
- No REAL authorization/execution/transfer capability changed.
- Next: exhaustive status-mutation inventory, then independently generated/fresh/verifiable recovery evidence instead of caller-supplied booleans.


## 2026-10-07 — Exhaustive mutation audit + recovery evidence increment

- PC and GitHub product main confirmed synchronized at `8a20e6ca099d0ec0917e9f38b399e2f24032cd49` before the current product commit.
- Exhaustive production status mutation inventory found no new SAFE_MODE bypass after #376.
- Added formal source inventory document in the product repo.
- Hardened `recover_from_safe_mode()`: caller booleans removed; engine now generates preflight/readiness/reconciliation/timing evidence and checks freshness.
- Added authenticated `POST /safe-mode/recover` with explicit human confirmation only.
- REAL recovery requires fresh REAL authorization; no REAL execution/capital action changed.
- `py_compile` and `git diff --check` passed. Pytest remains inconclusive/stalled and is not green.
- Next: focused recovery validation, then end-to-end REAL caller audit.


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


## Checkpoint 2026-10-07 — final external side-effect audit

- Product documentation advanced with `docs/FINAL_EXTERNAL_SIDE_EFFECT_AUDIT_2026-10-07.md`, committed on product main as `1261c97ea8a0b0d4cd62cc49fbbdbd7211865941`.
- Audited exchange submission/cancellation capability, capital transfer execution, Browser and Android execution surfaces.
- Capital transfer path is fail-closed: owner isolation, explicit REAL authorization, dedicated transfer authorizer, SUBMITTED-before-adapter durability, UNKNOWN_OUTCOME for ambiguous results, and reconciliation before retry/accounting.
- Cross-owner transfers are structurally forbidden; transfer planning does not execute transfers.
- Browser live execution remains explicitly gated by enabled + live_enabled + confirmation and does not bypass CAPTCHA/2FA; Android trade/withdrawal permissions default false and are owner-bound.
- REAL capability verification does not treat method presence as sufficient evidence; runtime promotion remains required.
- Focused external-side-effect suite: **56 passed in 10.37s**.
- No REAL order, cancellation, withdrawal, transfer, capital movement, or paid service was executed.
- Remaining release blocker: deterministic end-to-end runtime verification against controlled adapters and final human-controlled REAL release checklist.


## Checkpoint 2026-10-07 — deterministic controlled runtime + REAL release gate

- Product main advanced to `62eda13d7b6c639fa5cca4952003bf86d255702` with deterministic controlled REAL runtime E2E coverage.
- Added `tests/test_real_controlled_runtime_e2e.py`: controlled BUY+SELL chain exercises ExecutionGate -> engine -> OrderManager -> controlled adapter without any real venue; a second test proves the adapter is unreachable unless `REAL_ACTIVE`.
- Current controlled E2E: **2 passed in 4.23s**.
- Combined local regression checkpoint on PC: **12 passed in 9.07s**; production modules compiled and `git diff --check` passed.
- Added `docs/REAL_RELEASE_GATE_2026-10-07.md`, explicitly separating software validation from REAL authorization.
- Release gate's final blocker is explicit human authorization through the protected control path; green tests never authorize REAL trading.
- PC `C:\\ProgramasGodMode\\VazaoSovereignTrader` was hard-reset/synchronized to `origin/main`; working tree is clean.
- No REAL order, cancellation, withdrawal, transfer, capital movement, or paid service was executed.
- Next: continue only with release-gate strengthening, controlled recovery/restart coverage, and documentation. Do not activate REAL without explicit human authorization.


## Checkpoint 2026-10-07 — controlled restart/recovery E2E + release gate strengthening

- Product main advanced to `63df8d9` (`Add controlled restart recovery E2E`) and was pushed to `origin/main`.
- Added `tests/test_controlled_restart_recovery_e2e.py`: deterministic simulated process death/restart, durable `execution_intent`, exact venue/client identity lookup, authoritative closed fill, reconciliation, safe intent cleanup and restart replay without a second external submission.
- Added `docs/CONTROLLED_RESTART_RECOVERY_E2E_2026-10-07.md` documenting the evidence and fail-closed guarantees.
- Controlled restart/runtime/recovery checkpoint: **12 passed in 6.67s**.
- Additional focused authorization/execution/recovery checkpoint: **23 passed in 12.22s**; py_compile and `git diff --check` passed.
- The broader `test_account_reconciliation.py` invocation was observed to stall again on Windows and was terminated; it is explicitly **not** claimed green.
- Strengthened `docs/REAL_RELEASE_GATE_2026-10-07.md` with the new restart/recovery evidence and the known Windows-suite limitation; product doc commit `29a0ca12f1f108bbb5e1a056cbd2bad537146753`.
- PC `C:\\ProgramasGodMode\\VazaoSovereignTrader` was subsequently hard-reset/synchronized to `origin/main` at `29a0ca1` after the release-gate documentation update; working tree is clean.
- No REAL order, cancellation, withdrawal, transfer, capital movement, or paid service was executed.
- REAL remains disabled; explicit final human authorization through the protected control path is still the release blocker.
\n## Checkpoint 2026-10-07 — build/install readiness PC + Android\n\n- Product main advanced to \\51e2ed5\\ (\\Prepare PC and Android installation tooling\\) and was pushed to \\origin/main\\.\n- Added \\scripts/release_preflight.ps1\\: checks Git/Python/Inno Setup/ADB, Android/Windows build definitions, mobile compilation and focused release tests.\n- Added \\scripts/install_apk.ps1\\: installs a downloaded APK only when exactly one authorized ADB device is present by default.\n- Hardened \\scripts/build_windows_installer.ps1\\: installer artifact discovery is now limited to \\installer-output\\, avoiding an expensive recursive scan of the entire repository after Inno Setup.\n- Added \\docs/BUILD_INSTALL_READINESS_2026-10-07.md\\.\n- Installed/validated local Windows toolchain: Inno Setup 6.7.1 and ADB 37.0.0; PowerShell syntax checks passed.\n- Release preflight checkpoint: **14 passed in 18.95s**.\n- Local Windows installer build completed through PyInstaller + Inno Setup. Generated installer: \\installer-output/VazaoSovereignTrader-Setup-2026.10.1.exe\\ and normalized \\installer-output/VazaoSovereignTrader-Setup.exe\\, both 126,002,180 bytes. SHA-256 normalized installer: \\72FEA062A18E9F19DBDE2AC06B63824A8BD1DB8B2E0F30BD8B089D89D8C2439A\\.\n- The build exposed non-fatal PyInstaller warnings around NumPy hook discovery and missing optional hidden imports; the PC build itself completed successfully.\n- Android APK build remains intentionally delegated to GitHub Actions on Ubuntu because native Windows Buildozer is not the supported path. The existing \\.github/workflows/android-apk.yml\\ is ready to produce the debug APK artifact.\n- Android install path is now ready through ADB + \\scripts/install_apk.ps1\\; physical device pairing/Keystore validation still requires the actual Android device.\n- No REAL order, cancellation, withdrawal, transfer, capital movement, or paid service was executed. Build/install readiness does not authorize REAL.\n


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


## Checkpoint 2026-10-09 — REAL client identity boundary

- Criado incremento local na branch `hardening/require-client-order-id-at-real-boundary`.
- `OrderManager` agora rejeita `client_order_id` ausente, vazio ou só com espaços antes de chamar o autorizador e o adapter; PAPER continua compatível.
- Adicionado contrato AST para impedir novas chamadas diretas de submissão CCXT fora de `PC_ENGINE/exchanges/ccxt_client.py` e dos wrappers revistos.
- Atualizados README e `docs/REAL_CLIENT_ORDER_ID_BOUNDARY_2026-10-09.md`.
- Validação focal alargada: **25 passed in 10.76s**; `py_compile` e `git diff --check` passaram.
- Commit local criado. O branch de produto ainda não foi publicado porque Actions está sob contenção de quota; `artifacts/` permanece untracked e não foi incluído.
- Nenhuma exchange foi contactada; nenhum order/cancel/transfer/withdrawal foi executado. REAL continua bloqueado.

## Claude Code / NVIDIA NIM — decisão de integração

- Memória transversal de 2026-10-09 confirma Claude Code Node-compatible v2.1.112 e smoke funcional curto FCC/NVIDIA NIM (`NIM_OK`), modelo Nemotron-3-Super-120B-A12B.
- O smoke não prova gratuitidade contínua nem capacidade robusta de tool-use. Ollama continua não validado.
- Usar Claude Code/NIM apenas como segunda opinião curta e advisory, depois de confirmar custo/limites; não permitir que decida/autorize execução, altere risco ou desbloqueie REAL.


## Checkpoint 2026-10-09 — política zero-custo, IA opcional e descoberta PC/mobile

- Pedido do proprietário confirmado: não autoriza gastos com inferência/API. NIM/FCC/Claude Code não devem ser chamados automaticamente pelo Trader. O output anterior `$0.100344` não prova cobrança, mas exige contenção: nenhuma chamada adicional de consumo foi feita.
- Inspeção do PC: Ollama CLI 0.23.0 instalado, daemon parado; lista de modelos não foi confirmada porque o daemon não estava a correr. Claude CLI, Node/npm e Tailscale CLI existem. `vercel` não foi encontrado em PATH (não prova ausência de deploy). `tailscale status`: PC `100.69.225.47` online; Redmi `100.101.25.85` offline/última presença ~33 min. Não foi iniciado/parado nenhum serviço.
- Criado `docs/OPTIONAL_LOCAL_AI_AND_SERVICE_LIFECYCLE.md`, com contrato de supervisor lease-based, zero-paid inference por defeito, AI advisory/fail-open para a operação, sem LLM no hot path, fallback determinístico, discovery via Vercel com lease curta e ligação direta autenticada via Tailscale.
- README atualizado com a arquitetura pretendida. Commit local `dae435a` (`Document optional local AI and service lifecycle`) na branch `hardening/require-client-order-id-at-real-boundary`, após `68a0f56` (client identity boundary). `git diff --check` passou. `artifacts/` continua untracked e não incluído.
- A automação de lifecycle ainda não está implementada; o documento declara isso explicitamente. A descoberta Vercel/Android também não está confirmada em produção; serviço e cliente precisam de integração e testes. Não afirmar que já existe auto-start/stop automático.
- Próximos passos: inventariar modelos Ollama sem manter o daemon ligado por mais tempo do que o necessário, implementar supervisor local com ownership/leases/timeouts e testes, criar provider interface opcional para interpretação de contexto/links sem bloquear research, confirmar estado de deployment Vercel/Supabase e fechar endpoint lease + cliente Android/PC.


### Vercel coordination status verified read-only (2026-10-09)

- Connected Vercel account shows Hobby team and linked `vazao-sovereign-trader` project for `AndreVazao/VazaoSovereignTrader`.
- Latest production deployment is `READY`, commit `7ea1a897` (`Add conversational mobile cockpit`), but project metadata says `live: false`; SSO protection is enabled except custom domains. This is not proof the shared-learning endpoints are publicly reachable.
- Supabase provisioning, env config, root directory and live endpoint-lease flow remain unverified. Do not connect PC/Android clients to a guessed URL. Verify the actual project root, deployment routes and Supabase health read-only first.
- Product docs commit `720ca29` records this finding. No deployment, environment changes, billing changes or secrets were accessed.


## Checkpoint 2026-10-09 — continuação full-force

- Criado supervisor opcional Ollama com allow-list, deteção health, ownership do processo, leases concorrentes, idle grace e fail-open; implementado contexto local advisory para páginas públicas no `ResearchWorker`.
- Modelos locais encontrados sem arrancar o serviço: `deepseek-r1:1.5b`, `llama3.2:1b`, `qwen2.5:1.5b`, `qwen2.5-coder:1.5b`. Inferência real ainda não foi testada.
- Commits locais Trader: `d7d6a05` (supervisor + provider local) e `97048dd` (docs/verificação). 25 testes focados passaram, incluindo testes research e REAL-boundary; compile e `git diff --check` passaram. Nenhum teste arrancou Ollama.
- Vercel API: health 200, GET endpoint lease 405, POST anónimo 401. Rotas implantadas; Vercel não tem env vars e Supabase só mostra um projeto website inativo. A sincronização PC/Android não está funcional em produção até existir backend configurado. Não criar recursos sem validar custo.
- Próximo foco: teste local controlado com um dos modelos instalados; confirmar plano/custos Supabase antes de provisionar; fechar cliente PC/Android com endpoint lease e ligação direta Tailscale.

## Sessão 2026-10-20 — Android LAN/Tailscale e CI

- Na branch de PR #388, adicionados helpers de seleção e testes; workflow Android agora executa `python -m unittest MOBILE_APP.test_endpoint_selection -v` antes de Buildozer.
- Run #45 (ID 39419467665) terminou SUCCESS: testes do seletor, build APK debug e upload artifact passaram. Ainda não há confirmação de arranque num dispositivo real.
- Implementada configuração Android com `lan_url` + `tailscale_url`; a configuração legada `pc_url` migra para LAN, sem adivinhar o tipo de endereço.
- Failover automático permitido apenas em GET após erro de rede/timeout. POST/PUT/PATCH/DELETE/uploads não são repetidos; 401/403 não são contornados via outra rota. `/health` continua sendo apenas teste público de reachability, não autenticação.
- Atualizados docs do produto. Pendências: testes de integração mockados da função HTTP/configuração legada; endpoint de estado privado autenticado; testar app no Redmi Android 16 e recolher logcat; confirmar alternância Wi-Fi casa/Tailscale.
- Sem merge, sem PR adicional, sem chamadas a exchanges, ordens, transfers, mudança de REAL, nem exposição de endpoints privados em Vercel.


## 2026-10-20 — PR #388 merged; PC cockpit / virtual office shell started

- PR #388 merged successfully as `9c942e8fdde41b839d8c18297af83a8c741b878d`.
- Exact-head GitHub Actions run `39421760944` completed successfully: endpoint-selection unit tests, Android debug APK build, and artifact upload all succeeded.
- APK artifact: `vazaosovereigntrader-android`, artifact ID `12264317144`, SHA-256 `33b0a728f958155b97e8f3bf1018f8180ec61fc2600334e65a5919df92e8880c`. Successful CI build does NOT prove startup on the physical Android 16 device; the previously documented Kivy/HWUI SIGABRT remains unverified until logcat/device retest.
- New branch: `feat/pc-cockpit-full-office-shell-2026-10-20`, based on the merge commit above.
- New PR #389: https://github.com/AndreVazao/VazaoSovereignTrader/pull/389 — adds `virtual_office/prototype/full_cockpit_shell.html` and `docs/PC_COCKPIT_VIRTUAL_OFFICE_PARITY_CONTRACT.md`.
- Prototype layout: left navigation, central interactive office, persistent right conversation panel, office/compact/chat modes, narrow-screen overlays, request/alert tabs. It is standalone and clearly demo-only; chat does not call the backend. No live trading or cloud behavior was added.
- Contract explicitly requires functional parity with PC cockpit, one authoritative backend, authenticated/authorized commands, real server-confirmed status/events, no fake office activity, no client exchange secrets, LAN at home / Tailscale away, and Vercel as rendezvous only (never traffic/order proxy).
- PR #389 is open and not merged; its mergeability was reported false immediately after opening and must be rechecked after GitHub recalculates status and CI/review.
- Next: map existing PC cockpit controls to current API routes; implement authenticated read-only status/events adapter and tests before commands; preserve single open implementation PR. Physical Android startup validation remains pending.


## 2026-10-20 — Freqtrade reference reviewed (clean-room boundary)

- Inspected `AndreVazao/freqtrade` `README.md` and `LICENSE`. The repository LICENSE currently contains only `Bot copiado para experiência.`; this is not a clear licence grant or proof that the repository owner can relicense all upstream material.
- Freqtrade upstream is GPL-3.0; do not assume the fork's one-line note overrides upstream rights. No Freqtrade source, strategy, tests, documentation, or assets were copied into Sovereign Trader.
- Added `docs/FREQTRADE_INDEPENDENT_REVIEW_AND_CLEAN_ROOM_PLAN.md` on branch `feat/pc-cockpit-full-office-shell-2026-10-20`, commit `de796e63704ebd02c52beed27d7272f81ac639f9`.
- Review identifies product-level capabilities to independently evaluate: venue capability matrix, PAPER/dry-run separation, reproducible historical replay/backtesting, OOS/walk-forward, look-ahead/recursive-bias checks, cost-aware reporting and exchange-specific operational semantics.
- Existing PC cockpit inventory source: `PC_ENGINE/api/cockpit.py` (aliased by `PC_ENGINE/api/dashboard.py`). It already exposes operator controls, REAL readiness/auth guard, human-interaction bridge, research inbox, venue health, execution-surface status, PAPER evidence/ongoing study, diagnostics, assets, positions, models, logs and preflight. Next is exact route/auth/guard/test mapping before wiring the office.
- PR #389 remains the only active implementation PR; no source-code import, live trading, credential changes or REAL gate changes.

- Continued route-level inspection of `PC_ENGINE/api/server.py` and current `PC_ENGINE/api/cockpit.py`; added `docs/PC_COCKPIT_API_INTEGRATION_MAP.md` on PR #389 branch (commit `44f3c7fab85ae98b5450b5ef1acb6182a144ac4e`). It maps status, diagnostics, venue health, PAPER evidence, human intervention, pairing, operator files and execution-surface routes with auth scopes and safety distinctions.
- Key findings: public `GET /health` proves reachability only; private read endpoints use `read_private_state`; execution-surface lifecycle uses `trade_paper`. Existing cockpit has state-changing controls that must not be copied into the new office before route-specific method/scope/guard/confirmation contracts are tested.


## 2026-10-20 — Shortlist de reutilização legal e laboratório independente

- O utilizador clarificou a estratégia: estudar projetos semelhantes, reutilizar componentes apenas quando a licença/proveniência permitir, e desenvolver a identidade técnica do Sovereign Trader de forma independente; avaliar experiências úteis num repo-laboratório satélite, sem misturar código experimental com o núcleo.
- Criado em PR #389: `docs/INDEPENDENT_TRADING_PROJECT_REUSE_SHORTLIST.md` (commit `89eceed4c1667162137e420d0df6ccff16bac2d6`).
- Triagem inicial das licenças nos repositórios oficiais: Hummingbot declara Apache-2.0; Jesse declara MIT; Erfaniaa/LLM-Auto-Trader declara MIT; NautilusTrader declara LGPL-3.0; Freqtrade upstream é GPL-3.0. Estas licenças não significam ausência de condições: preservar notices e rever dependências/proveniência e distribuição por componente.
- Hummingbot é candidato prioritário para estudar arquitetura de conectores multi-venue; Jesse para fluxo de investigação/backtesting; LLM-Auto-Trader para a separação entre proposta de LLM e camada determinística de risco; NautilusTrader apenas como estudo de arquitetura nesta fase devido às implicações LGPL.
- CCXT é referência para cobertura de exchanges, mas esta passagem não confirmou a licença exata do pacote no repositório; não assumir permissão até a verificar.
- Plano de laboratório proposto: primeiro harness sintético de contratos/capacidades de venue; depois replay PAPER reproduzível e avaliação sem enviesamento; depois adaptador LLM-proposta→plano validado sem side effects. Não importar frameworks inteiros nem enviar ordens reais.
- Nenhum código externo foi copiado. Nenhuma chave/API token, ação real, transferência ou alteração dos gates REAL foi feita.
- PR #389 continua o único PR de implementação ativo; o novo shortlist está no mesmo branch.


## 2026-10-20 — Foco central: vantagem temporal entre exchanges

- O utilizador clarificou que o objetivo fundamental do Sovereign Trader é investigar diferenças temporais de atualização entre exchanges e avaliar se representam atraso de feed/amostragem ou oportunidade executável e líquida, depois de custos e risco.
- Fiz leitura adicional do README do fork AndreVazao/freqtrade e de fontes upstream Freqtrade: `freqtrade/exchange/exchange.py`, `exchange_ws.py`, `exchange_utils.py`. O README do fork declara suporte Spot a Binance, BingX, Bitget, Bitmart, Bybit, Gate.io, HTX, Hyperliquid, Kraken, OKX/MyOKX; Futures para Binance, Bitget, Gate.io, Hyperliquid, OKX, Bybit e Kraken; Bitvavo e Kucoin como comunitariamente testados. O README indica que a base de integração usa CCXT e que as notas específicas por exchange são importantes.
- Padrões técnicos a estudar e reimplementar de forma própria: capacidades/semântica por venue, normalização de dados, deduplicação e ordenação de trades, tratamento de candles parciais, websocket e idade de atualização do order book, reconexão/timeouts/rate limits, precisão de preço/quantidade/contratos. Não foi copiado código.
- Criado `docs/TEMPORAL_MARKET_EDGE_RESEARCH_PLAN.md` em PR #389, commit `cab183f056669565f29daa467cbbd1189c07cc59`.
- Plano exige timestamps separados (evento da exchange, receção local wall-clock e monotónica, sequência, incerteza de relógio), coleta read-only de dados públicos, classificação de artefactos de UI/amostragem/transporte/relógio versus atraso potencialmente executável, replay sem look-ahead, custos de spread/fees/slippage/latência, e PAPER shadow mode antes de qualquer avaliação de execução.
- Nenhuma ordem real, transferência, levantamento, chave de API ou alteração de gate REAL foi usada. O trabalho permanece no único PR de implementação #389; laboratório temporal deverá começar sintético/read-only e isolado.


## 2026-10-20 — primeira implementação da memória interna partilhada

- O utilizador confirmou o modelo de empresa modular: CEO/orquestrador, investigação, análise, comparação entre exchanges, risco/validação e departamento especial de Aposta Rápida; todos partilham a memória interna de aprendizagem dentro do mesmo Sovereign Trader/PC. Isto é separado da futura partilha de conhecimento entre instalações/computadores via Vercel.
- Criado docs/MODULAR_DEPARTMENT_ARCHITECTURE.md em PR #389, commit 0d2915d3a92affcbb08d603fc417613f6c06be81. Define fronteiras dos departamentos, fluxo de oportunidade, memória versionada, requisitos de latência, evolução de um PC para processos/máquinas separadas e limites de segurança.
- Implementado primeiro módulo process-local PC_ENGINE/learning/shared_memory.py, commit 074765f144541453de899a7f981184ebcf9be956: registos partilhados thread-safe, versões, conflito otimista, provenance, confidence, status de validação, TTL/frescura e notificações de atualização. A memória não é ainda distribuída nem persistente em disco; não deve ser usada como armazenamento de ticks nem como autorização de execução.
- Adicionados testes tests/test_shared_learning_memory.py, commit 225bbea3f4b2a14b00bda408598e512303d896c1, para leitura comum entre departamentos, conflito de versão, frescura/TTL, validação, isolamento de callbacks e unsubscribe.
- A execução dos testes não foi feita nesta sessão através do ambiente local; não declarar os testes verdes até serem executados no PC/CI. Não foi enviada ordem real, não houve conexão a exchanges, e nenhum gate REAL foi alterado.
- PR #389 continua o único PR de implementação ativo e não foi mergeado. Próximo passo: validação local/CI; corrigir qualquer falha; depois integrar os departamentos consumidores através de interfaces pequenas, mantendo hot market data separado da memória duradoura.


## Continuação — memória interna e validação (2026-10-20)

- PR #389 continua aberto e não foi mergeado: https://github.com/AndreVazao/VazaoSovereignTrader/pull/389
- Commits de reforço da memória interna:
  - `d6143e50bc2cbc2bfa9ed5a0a00cb381edfbc961`: TTL e max_age agora exigem milissegundos inteiros válidos; `list_records` apresenta registos expirados como `stale`, sem alterar silenciosamente o registo armazenado.
  - `82ad2c7f394a5c98e63a79772e0c6b53c1620760`: testes adicionais para listagem de evidência expirada e rejeição de janelas de frescura fracionárias.
- Verificação remota: não foram encontrados workflow runs associados ao commit atual através da consulta de runs de PR. Portanto, **os testes ainda não estão confirmados como executados**; não declarar sucesso até existir CI verificável ou execução local.
- A memória continua apenas em processo Python, sem persistência em disco, distribuição entre processos ou computadores. Não foi ligada ao caminho quente de ticks nem a execução de ordens.
- Próximo passo: validar a suíte no CI/ambiente do projeto e, em seguida, integrar a memória somente no fluxo de investigação/análise com evidência e frescura explícitas; manter a recolha de mercado sem bloqueios e sem efeitos de execução.


## Continuação — CI Python ativado no PR (2026-10-20)

- No PR #389, identifiquei a razão para não aparecerem testes Python automáticos: `.github/workflows/python-tests.yml` estava configurado apenas com `workflow_dispatch`.
- Atualizei o workflow no branch `feat/pc-cockpit-full-office-shell-2026-10-20` para correr em pull requests que alterem `PC_ENGINE/**`, `tests/**`, `requirements-pc.txt` ou o próprio workflow, mantendo também o acionamento manual.
- Commit: `b5ec09e1b92ec8f1ed7161c359b5d8e6edd0a5f9`.
- A consulta imediatamente após o push ainda não mostrava workflow run; os checks Snyk e Vercel estavam pendentes. É necessário voltar a consultar e confirmar se o workflow dispara e se termina com sucesso; não declarar testes passados sem resultado verificável.
- PR #389 permanece aberto, não mergeado. Sem ordens reais, sem alterações a permissões REAL.


## 2026-10-20 — falha CI identificada e correção de compatibilidade de venue

- O workflow Python passou a correr no PR #389 e falhou: **3 failed, 958 passed, 44 subtests passed** (run ID 39461273045; job 118761062388).
- As falhas ocorreram em tests/test_pending_order_reconciliation.py: reconciliação de compra, venda e sequência de fills parciais.
- Causa encontrada na resolução da exchange de uma ordem pendente: _exchange_for_pending_order() só consultava venue_id; registos de compatibilidade mais antigos guardam o identificador em exchange. Sem venue_id, o método podia cair para a exchange principal e não consultar a venue registada no próprio registo.
- Corrigido PC_ENGINE/core/engine.py para resolver a venue por venue_id ou, na ausência deste, por exchange, antes do fallback legado. Commit no branch do PR #389: 940cc513fb1cae71badfb4c62a6b360dc6b2e4a2.
- Após o push, a consulta aos runs associados ao commit ainda não mostrou uma execução; a correção ainda não está validada por CI. Próximo passo obrigatório: confirmar novo run, analisar qualquer falha remanescente e só então continuar.
- PR #389 permanece aberto e sem merge. Nenhuma ordem real, chamada de exchange, alteração de autorização REAL ou transferência foi executada.


## 2026-10-20 — follow-up CI reconciliação (não resolvido)

- Reconsultados os workflows para commit 940cc513fb1cae71badfb4c62a6b360dc6b2e4a2. Ambos terminaram em failure: Python tests run 39470886084/job 118794335082 e Trading engine PAPER smoke run 39470886020/job 118794335885. Os checks CodeRabbit, Snyk e Vercel estavam verdes; isso não substitui os testes Python/PAPER.
- Acesso aos logs detalhados de jobs devolveu 404 através do conector; os metadados confirmam que o passo de execução de testes falhou, mas não expõem os nomes/tracebacks individuais. Não alterar a lógica de reconciliação com base em suposições.
- Revisão estática revelou que os fixtures de `tests/test_pending_order_reconciliation.py` omitem `exchange` em várias ordens pendentes, apesar de o helper só configurar `engine.exchanges` e não criar uma exchange principal. Isto é uma hipótese concreta para investigar, não uma causa confirmada dos failures; confirmar pelos logs completos ou reproduzir localmente antes de corrigir.
- `PC_ENGINE/core/engine.py` agora tenta `venue_id` e depois `exchange`; se ambos faltarem, mantém o fallback legado `_main_exchange()`. Não introduzir fallback silencioso para a única exchange configurada: isso pode encaminhar uma ordem pendente para a venue errada.
- Estado: PR #389 aberto, sem merge. Próximo passo: obter traceback detalhado/reproduzir os dois comandos de teste, corrigir causa confirmada, adicionar teste de regressão e revalidar ambos os workflows. Sem ordens reais nem alteração de gate REAL.


## 2026-10-20 — logs completos CI e novo diagnóstico (VazaoSovereignTrader 2)

- Recuperados os logs completos de Python tests run 39470886084/job 118794335082 e PAPER smoke run 39470886020/job 118794335885.
- Python: 10 falhas, 951 passed, 44 subtests passed. Falhas em:
  - `test_idempotent_reconciliation.py` (2) e `test_lost_position_recovery.py` (1): `KeyError: 'BTC/USDT'`.
  - `test_pending_order_financial_recovery.py`: compra parcial com `KeyError: 'BTC/USDT'`, venda parcial mantém qty 1.0 em vez de 0.6, recuperação após restart deixa ordem `o1` pendente em dois testes.
  - `test_pending_order_reconciliation.py`: compra parcial resulta qty 0.2 em vez de 0.5; venda parcial resulta qty 0.8 em vez de 0.5; sequência cumulativa resulta qty 0.0 em vez de 0.4.
- PAPER smoke: 5 falhas, 74 passed, em `test_lost_position_recovery.py` e `test_pending_order_financial_recovery.py` (mesmas categorias).
- A correção de venue em `940cc513...` não resolveu a suíte. Não fazer merge.
- A leitura estática de `_exchange_for_pending_order` e `test_pending_order_reconciliation.py` mostra um possível defeito nos fixtures: algumas ordens não incluem `exchange`/ `venue_id`, enquanto o helper cria `engine.exchanges` mas não configura `_main_exchange`. Como a resolução de exchange ocorre antes do bloco `try`, a falha pode abortar a reconciliação nesses testes. Isto explica plausivelmente os três asserts de fills parciais, mas não explica por si só as falhas financeiras/KeyError; tratar como hipótese a confirmar, não como correção definitiva.
- O caminho financeiro usa `state.financial_account` e deve preservar a invariância de quantidade/notional/fees, atualização exatamente uma vez e remoção da ordem terminal só após commit durável. Não introduzir fallback silencioso para uma exchange arbitrária nem alterar gates REAL.
- Próximo passo: inspecionar tracebacks completos e as funções de reconstrução/commit para os KeyError e a recuperação financeira; reproduzir os testes afetados num checkout executável; criar correções mínimas com testes de regressão; voltar a executar os dois workflows.
- PR #389 continua o único PR de implementação ativo, aberto e sem merge. Não houve ordens reais nem chamadas de exchange.
