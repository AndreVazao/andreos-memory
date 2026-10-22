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


## 2026-10-20 — correção de resolução da venue no PR #389

- Logs completos confirmaram que a suite Python falhava com 10 falhas (951 passed, 44 subtests) e PAPER smoke com 5 falhas (74 passed).
- Identificadas duas causas compatíveis com o código:
  1. Testes financeiros e de recuperação têm apenas `_main_exchange()` configurado, sem mapa `self.exchanges`; a resolução anterior recusava uma venue registada mesmo quando a exchange principal declarava o mesmo nome.
  2. `tests/test_pending_order_reconciliation.py::make_engine` omitia a exchange nas ordens legadas e não configurava `_main_exchange()`, tornando o fixture incompleto.
- Alteração no motor, commit `e6552ab0a5787c7b9cf72039f70f539da5c2fea1`: quando a venue está registada mas não existe no mapa, a exchange principal só é aceite se `main_exchange.name` corresponder exatamente ao identificador registado. Não há fallback para venue arbitrária.
- Alteração de teste, commit `db1e12e0c8097adea526fc715457b8bfeb89ea79`: o helper de reconciliação declara explicitamente a exchange principal fake para os fixtures legados que não contêm campo de venue.
- Verificação CI: consulta imediata de workflows para o commit devolveu lista vazia; ainda não existe confirmação de execução. Não declarar testes corrigidos até analisar o novo run.
- Próximo passo: aguardar/consultar CI do PR #389, rever traceback se alguma falha persistir e só então adicionar mais alterações. PR continua aberto, sem merge, sem ordens reais e sem alteração de gate REAL.

## 2026-10-20 — primeiro fio real entre escritório virtual e API do motor

- No branch feat/pc-cockpit-full-office-shell-2026-10-20, mantido dentro do único PR #389, foi adicionada a rota GET /virtual-office em PC_ENGINE/api/server.py. Serve o HTML do escritório no mesmo origin do backend, com Cache-Control: no-store, X-Content-Type-Options: nosniff e resposta 404 clara se o asset não estiver instalado.
- O HTML do escritório ganhou um painel de ligação read-only: pede token ao operador, valida primeiro GET /status com X-Token e depois tenta /venue-health, /diagnostics, /human-interaction/pending e /research. Não usa POSTs, não guarda o token em localStorage nem em URL, não executa ordens. O token fica apenas na memória da página e o botão Desligar limpa o campo e a referência.
- Atualizado docs/PC_COCKPIT_API_INTEGRATION_MAP.md para documentar o fio inicial, as limitações e a necessidade de incluir o asset na futura embalagem EXE/APK. A primeira integração não é ainda paridade total: a conversa permanece demonstração local, não existe stream de eventos nem modelo detalhado completo de cada endpoint, e o HTML precisa de ser servido pelo backend (não aberto como ficheiro local nem servido por Vercel).
- PR #389 continua aberto e sem merge; head observado após estas alterações: 8132a2ab5f82bfb00002424d629dba358b5985b2.
- CI mais recente observado: PAPER smoke run 39472825937 passou; Python suite run 39472825929 falhou com 3 falhas, 958 passed e 44 subtests: test_reconcile_pending_buy_applies_only_unseen_fill_delta, test_reconcile_pending_sell_reduces_position_by_unseen_fill_delta e test_reconcile_partial_fill_sequence_is_cumulative_and_exactly_once. As três deixam a posição inalterada; a causa ainda não está confirmada.
- Adicionado um assert diagnóstico ao primeiro teste para revelar PENDING_ORDER_RECONCILE_ERROR nos logs do motor. Commit 9f617cc6e18b331b8a5eab24d305d4eab9903b66. A consulta aos runs para este commit devolveu lista vazia; não há ainda novo resultado para esse assert.
- O commit de documentação 8132a2ab5f82bfb00002424d629dba358b5985b2 está no head do PR segundo a consulta mais recente, mas ainda não apareceu run CI associado. Reconsultar PR/checks antes de assumir execução.
- Segurança mantida: sem ordens reais, sem transferência, sem mudança do gate REAL, sem credenciais de exchange no cliente, sem proxy Vercel. Próxima prioridade: obter a causa exata do erro de reconciliação, reparar e validar CI; depois expandir a ligação read-only com testes de contrato e só então ligar a conversa ao gateway autenticado.

## 2026-10-20 — conversa do escritório ligada ao gateway autenticado

- PR #389 segue único PR de implementação, aberto e sem merge. Branch: feat/pc-cockpit-full-office-shell-2026-10-20. Head observado: 51aa08fc97fa82f29297f4313c453cd63a47f331.
- A correção confirmada pelo traceback das três falhas Python foi no fixture FakeRecovery: a implementação de teste aceitava só seis argumentos de estado, mas _persist_recovery já passa um campo de estado adicional. Isto gerava PENDING_ORDER_RECONCILE_ERROR e deixava fills parciais sem aplicar. Atualizei FakeRecovery.save_positions para aceitar os campos de estado expandidos; produção não foi alterada para mascarar o erro.
- CI para o commit eb799a3ff957901a234d6f08a919694fe076486f terminou com Python suite 961 passed, 44 subtests passed e PAPER smoke passou. O run Python 39474300604 foi visto a concluir com sucesso. Como depois houve mais alterações no HTML, documentação e cabeçalhos da rota, há uma nova execução para o head atual.
- Escritório virtual: o formulário de chat agora encaminha mensagens para POST /assistant/message após autenticação e mostra a resposta do OperatorAssistantGateway. O gateway atual é um router determinístico: consulta estado, coloca investigação na fila se houver scope submit_research, permite controlos PAPER existentes se houver trade_paper, recusa linguagem REAL/live e não cria autorização REAL. Não é ainda um LLM livre nem conversa em streaming. Erros de transporte avisam que o resultado é desconhecido e não repetem automaticamente a ação.
- A leitura do escritório usa /status, /venue-health, /diagnostics, /human-interaction/pending e /research, todos autenticados. Token permanece em memória de página, no header X-Token; não é guardado em localStorage nem URL. Botão Desligar limpa token e campo.
- A rota GET /virtual-office agora define Cache-Control no-store, X-Content-Type-Options nosniff, Referrer-Policy no-referrer, X-Frame-Options DENY e CSP limitada ao mesmo origin com inline script/style necessário para o protótipo.
- Últimos runs do head 51aa08fc97fa82f29297f4313c453cd63a47f331 observados: Python run 39474481355 em progresso (dependências a instalar) e PAPER smoke run 39474481346 pendente/sem jobs ainda. Não declarar validação final do head até estes resultados terminarem.
- Sem ordens reais, sem chamadas a exchanges, sem alterações ao gate REAL. Não abrir PR paralelo, não fazer merge antes de CI final e revisão do código de integração. Ainda falta teste end-to-end de browser, tipagem visual completa dos endpoints, reconexão/stream e validação de empacotamento EXE/APK. Para uso remoto, preferir Tailscale; não expor a API publicamente.



## 2026-10-20 — PR #389 merged; smaller API contract PR opened

- PR #389 (PC cockpit / Virtual Office shell and authenticated gateway) foi merged por squash depois de os checks ficarem verdes. Merge commit: `504d894c8e7ad0f98bc7bcafde65907d6649aa68`. Head validado: `51aa08fc97fa82f29297f4313c453cd63a47f331`.
- No head do PR #389, Python tests run `39474481355` e PAPER lifecycle/safety run `39474481346` concluíram com sucesso. Checks de CodeRabbit, Snyk e Vercel também estavam verdes. Não houve revisão humana registada; merge foi feito após checks verdes conforme instrução do utilizador.
- Criada branch nova `test/virtual-office-api-contract-2026-10-20` a partir do merge commit, para evitar PR gigante.
- Aberto PR #390: https://github.com/AndreVazao/VazaoSovereignTrader/pull/390 — teste focado para `GET /virtual-office`, conteúdo HTML e cabeçalhos Cache-Control, nosniff, Referrer-Policy, X-Frame-Options e CSP.
- Commit atual do #390: `df225531ad1d081a06a39ea0d4d36fec08b66a1a`. Run Python `39474967625` está em progresso; Vercel e Snyk ainda pending na última consulta. Não declarar verde nem fazer merge até terminar.
- Escopo do #390 é test-only. Sem ordens de exchange, sem credenciais, sem alterações a permissões ou ao gate REAL. Manter apenas este PR aberto e, quando CI ficar verde, fazer merge e seguir para outro PR pequeno.
- O teste usa a configuração exemplo e instancia SovereignEngine para exercitar a rota Flask; confirmar CI antes de confiar que o fixture é robusto.

## 2026-10-20 — foco no cérebro e memória de aprendizagem durável

- O utilizador está longe do PC e pediu explicitamente para adiar sincronismo PC–telemóvel, testes locais/físicos e validação no equipamento para uma fase posterior. Continuar desenvolvimento por GitHub/CI; não bloquear tarefas de código por falta de acesso físico.
- Objetivo de preparação pré-instalação: áreas do produto (cockpit, escritório virtual, mobile) perto/acima de 85% por implementação e integração testável; cérebro perto de 90% de preparação técnica. Estes números são metas de planeamento, não certificação de segurança, prova de edge ou promessa de lucro. Recolha real e fine-tuning dependem de o PC estar a correr e obter dados reais de qualidade.
- PR #390 foi merged por squash após checks confirmados verdes. Merge commit: 5143cd441dac5b1c6dbd8d348a1d60ffe2ce36dd. Teste cobre GET /virtual-office e cabeçalhos de segurança.
- Aberto PR #391: https://github.com/AndreVazao/VazaoSovereignTrader/pull/391 — branch `feat/durable-learning-memory-sqlite-2026-10-20`, head `89fa16e892e8208242dcdf010fa122710571bb90`.
- PR #391 adiciona `PC_ENGINE/learning/sqlite_memory.py`: memória de aprendizagem SQLite com transações, optimistic version checks, valores JSON estritos (rejeita NaN/Infinity e objetos não serializáveis), TTL/frescura, timestamps de parede para persistência após restart, journal append-only e callbacks locais best-effort. Testes em `tests/test_sqlite_learning_memory.py`; contrato em `docs/DURABLE_LEARNING_MEMORY.md`.
- Importante: o adapter ainda não está ligado ao arranque do motor; o PR preserva a memória em-processo existente e não muda silenciosamente o backend de produção. Migração, backup/retention, lifecycle e event bus entre processos ficam para follow-up separado.
- Estado de CI consultado: CodeRabbit success, Snyk success; Python suite run `39477862535` ainda em progresso no passo de testes; Vercel pending. Não fazer merge até todos os checks requeridos ficarem verdes. Manter apenas um PR de implementação aberto.
- Próxima prioridade depois do #391: corrigir os riscos de qualidade do Radar antes de chamar sinais de oportunidades. Atualmente a latência calcula diferença entre relógio local e timestamp da exchange (sem garantia de relógios/semântica equivalentes) e o lead/lag deriva de timestamps de polling sequencial; estes valores podem ser confundidos com latência/lead-lag executável. Criar PR pequeno com semântica explícita de tempos, instrumentação monotónica de duração da requisição e classificação de observações inconclusivas; sem ordens reais.
- Limites invariáveis: nenhuma ordem real, nenhuma mudança do gate REAL, nenhum segredo de exchange no cliente. Só promover hipóteses com proveniência, frescura, replay sem look-ahead, custos/latência realistas, evidência fora da amostra e revisão de risco.

## 2026-10-20 — PR #391 merged; Radar timing/data-quality hardening opened

- PR #391 foi merged por squash após todos os checks ficarem verdes. Merge commit: `ea02f4ab2b3491021aa2430e15ea9cf3c1ee7ba6`. Python suite run `39477862535` passou; CodeRabbit, Snyk e Vercel estavam success. PR #391 adiciona adapter SQLite de memória durável e testes, mas ainda não liga esse adapter ao startup de produção.
- Aberto PR #392: https://github.com/AndreVazao/VazaoSovereignTrader/pull/392 — branch `fix/radar-timing-quality-2026-10-20`, head `7bfea457f03f1eb8d31e7ea45c958909ed4d1f88`.
- Alterações #392: `latency_ms` legado agora é null (não calcular diferença entre relógio local e timestamp da exchange como latência); medição separada `request_duration_ms` usa relógio monotónico; timestamps de fonte duplicados/não crescentes para mesmo venue/símbolo são rejeitados e incrementam `quality_rejections`; eventos de lead/lag recebem `evidence_status=polling_order_unconfirmed`; JSONL documenta semântica candidate-only; testes cobrem os novos contratos; documento `docs/RADAR_TIMING_AND_DATA_QUALITY.md`.
- O radar continua read-only, sem ordem, sem mudança de REAL. O PR reduz inferências enganadoras mas não prova edge. WebSocket event-time, alinhamento de relógios, replay, custos de execução e validação out-of-sample continuam por fazer.
- Estado inicial de checks no head do #392: Vercel pending; workflows ainda não devolvidos pelo wrapper na primeira consulta. Não fazer merge até Python suite, Vercel, Snyk e restantes checks exigidos estarem verdes. PR #392 é o único PR de implementação aberto.
- Prioridade seguinte após #392: integração testada do SQLiteLearningMemory no lifecycle do engine, em PR pequeno, com caminho configurável, migração/backup documentados e fallback seguro. Depois construir pipeline de replay/avaliação de evidência do Radar. Não iniciar integração física PC–mobile até o utilizador estar junto do PC.


## Checkpoint 2026-10-20 — Radar timing and Freqtrade capability study

- PR #391 merged: SQLite durable learning-memory adapter added, but it is not yet wired into engine lifecycle/startup.
- PR #392 merged as `7a07ae47d473a96c771ca56a3b2bbb6ae18eca64`: Radar no longer reports wall-clock minus exchange timestamp as latency; REST lead/lag is explicitly candidate-only. Python test workflow, CodeRabbit, Snyk and Vercel were green at merge. No PC/mobile physical tests were performed.
- Reviewed the user's private `AndreVazao/freqtrade` fork and its exchange architecture: common exchange class/resolver, venue capability overrides, CCXT feature validation, retry/backoff, WebSocket lifecycle, and explicit BingX behavior.
- Licensing caution: fork root LICENSE says “Bot copiado para experiência.” while pyproject.toml declares GPLv3. Treat this as ambiguous; no Freqtrade code or tests copied. Current work is a clean-room conceptual study.
- Created documentation-only PR #393: https://github.com/AndreVazao/VazaoSovereignTrader/pull/393. It is open and Snyk/Vercel are still pending; do not merge until required checks are green.
- Source audit found a concrete follow-up issue in `PC_ENGINE/radar/websocket_radar.py`: `_make_event()` calculates `local_receive_latency_ms = receive_ts - exchange_ts`, which subtracts a venue timestamp from local wall-clock time and may falsely represent latency when clocks/timestamp semantics are not aligned. The REST PR did not fix this WebSocket path. After #393 is green/merged, make this the next small implementation PR: use a monotonic receive measurement for collector-local elapsed time, keep venue event time separate, name semantics explicitly, and ensure any lead/lag evidence remains unconfirmed until replay validation.
- Other next priorities: our own declarative exchange capability registry; public-data conformance tests; add BingX public WebSocket only after adapter lifecycle/quality contracts; event-time replay and cost-aware PAPER validation.
- Keep only one implementation PR open at a time. No REAL-mode gate or live order behavior changes; PC/mobile integration tests wait until the user is back near the PC.


## Checkpoint 2026-10-21 — Freqtrade study merged; WebSocket timing fix in CI

- PR #393 (Freqtrade exchange-capability and clean-room adaptation study) merged as `7aedeba72757d52b9b622834bb7894e49384359a`. The study covers common exchange contracts, venue-specific capabilities, WebSocket lifecycle/feed health, read-only conformance tests, event replay and the licensing ambiguity in the user's fork. No Freqtrade code or tests were copied.
- Opened PR #394: https://github.com/AndreVazao/VazaoSovereignTrader/pull/394 — `fix/websocket-timing-semantics-2026-10-21`. It changes `local_receive_latency_ms` to `None` in `_make_event()` because local wall clock minus exchange event timestamp is not a trustworthy latency measurement without a validated clock-offset model. Added regression tests for the parser and event factory.
- Latest CI observation for PR #394 head `0d3fc5c1d34059a8be541d0f58911c3e354592af`: Python workflow run `39604732075` is in progress at dependency installation; test suite pending. CodeRabbit and Snyk success; Vercel pending. Do not merge until Python tests and all required checks are green.
- No orders, exchange credentials, REAL-mode gates, or execution authorization changed. No PC/mobile physical tests; user is away from the PC.
- After #394 merges: next priority is a minimal, tested exchange capability registry / public-data conformance contract, starting with Binance and BingX public market data. Keep one implementation PR open at a time. SQLite learning-memory adapter is still not wired into production engine startup; plan its lifecycle integration separately.


## 2026-10-21 — Virtual Office runtime summary PR #395

- PR #394 merged as 3281bca0f353ad8ea96a4bfba957b974e594394b; WebSocket radar no longer infers latency from local wall-clock minus venue event timestamp. This only fixes timing semantics; it does not establish a market edge.
- Started the digital-office/runtime integration while the owner is away from the PC. Opened PR #395: https://github.com/AndreVazao/VazaoSovereignTrader/pull/395 — branch feat/virtual-office-live-runtime-summary-2026-10-21.
- PR #395 removes misleading hard-coded office metrics (including the example PAPER label) and renders engine status, mode, market-data health and refresh time only after authenticated GET /status and GET /diagnostics responses. Unknown values stay unknown; no polling or mutation controls added. Added a shell contract regression test.
- CI for head ec59b5c796e4341d6fa9381131e8baef45493580: Python workflow run 39605570778 queued; Snyk and Vercel pending at initial check. Do not merge until all required checks are green.
- Token remains in page memory and X-Token header; no localStorage, URL token, separate engine, live order, or REAL gate changes. Physical PC/mobile test remains pending.
- Next: after #395 checks pass and merge, add bounded/cancellable refresh and freshness/error states, then expand read-only diagnostics/venue/evidence panels. Only then integrate protected research conversation and human-intervention displays with route-scope tests. Keep one implementation PR open at a time.


## 2026-10-21 — Virtual Office non-blocking observer PR #396

- PR #395 merged after Python tests, CodeRabbit, Snyk and Vercel checks reported success. Merge commit: 43be0ba456ff18d39274bbd8a24dfffaa9a88b1d.
- Owner clarified the non-negotiable architecture: the trading Runtime must never be held up by virtual-office rendering/animation. The office is optional visualization only; if observer load threatens response/reaction latency, degrade or disable visuals while the engine continues.
- Opened PR #396: https://github.com/AndreVazao/VazaoSovereignTrader/pull/396 — `fix(office): keep observer requests bounded and cancellable`, branch `feat/office-nonblocking-observer-2026-10-21`.
- PR #396 adds a 2.5-second AbortController deadline to office GET/chat fetches, aborts outstanding browser requests on explicit disconnect, clears the in-memory token, and adds shell regression assertions. No background polling was added; refresh remains manual.
- Added `docs/VIRTUAL_OFFICE_NON_BLOCKING_OBSERVER.md` defining the required boundary: one engine, publish-not-wait snapshots/events, no critical locks over network I/O, bounded/coalescing visual queues, drop visual updates under pressure, and degrade/disable visualization without affecting engine risk policy.
- Explicit limitation: browser-side request cancellation is not proof of engine/process isolation. Runtime-side circuit breaker, observer worker/queue, performance budgets, load tests, and PC/mobile validation are not yet implemented or proven. Do not claim full non-blocking isolation until those tests pass.
- Latest PR #396 head `0d503820becb4c8b8f17e296dc30bec2eccae9e6`: Python workflow run `39607030840` is in progress in test suite; CodeRabbit and Snyk success, Vercel pending. Do not merge until all required checks are green.
- No trading authority, REAL-mode gates, exchange credentials or live-order behavior changed. Physical PC/mobile tests wait until owner returns to PC. Keep one implementation PR open at a time.

- PR #396 merged after the Python test suite, CodeRabbit, Snyk and Vercel all reported success. Merge commit: ab5e6429856c82b408e378b7f9293125bca0ad11. Browser requests are bounded/cancellable; this does not yet prove runtime CPU/process isolation.


## 2026-10-21 — Lightweight Runtime observer PR #397

- PR #396 merged as `ab5e6429856c82b408e378b7f9293125bca0ad11`; browser-side office requests have a deadline and can be cancelled on disconnect. This remains client-side protection, not proof of Runtime isolation.
- Opened PR #397: https://github.com/AndreVazao/VazaoSovereignTrader/pull/397 — `perf(runtime): keep virtual office on a lightweight observer path`, branch `feat/runtime-observer-snapshot-isolation-2026-10-21`.
- Added authenticated `GET /observer/summary` that copies only primitive Runtime fields under the engine lock, avoiding full `asdict()`/nested snapshot work on this observer route.
- Changed routine office refresh to use `/observer/summary` and `/market-data-health` instead of the heavier `/diagnostics` endpoint each time. Full diagnostics remain available for deliberate inspection.
- Added regression coverage for the new route being protected by authentication and office shell using the lightweight endpoints. Added `docs/RUNTIME_OBSERVER_ISOLATION.md` with explicit limits and acceptance tests.
- This is reduced request-path work, not zero contention: the endpoint still briefly acquires the engine lock. A bounded/coalescing observer queue or cached publication, measured latency budgets, saturation tests and a Runtime-side visual circuit breaker remain future work. No REAL-mode gates, strategies, orders or execution authority changed.
- PR #397 head `e147448e0559b916ac21474c6462e70625a7b7af`: Python workflow run `39608675218` is still in progress at dependency installation; Vercel and Snyk pending at last check. Do not merge until all required checks are green.
- No PC/mobile physical tests performed; those wait until owner is home at the PC. Keep only one implementation PR open at a time.


## 2026-10-21 — Observer fast-path regression guards PR #398

- PR #397 merged after Python tests, CodeRabbit, Snyk and Vercel reported success. Merge commit: `b1dbdd63a19aa07687c0f4466936bd7e211d5e11`.
- PR #397 now keeps routine virtual-office refresh on authenticated `/observer/summary` plus `/market-data-health`; it avoids the full `engine.snapshot()` and diagnostics aggregation on the normal office refresh path. The observer summary still briefly takes `engine.lock`, so this is not zero contention or process/CPU isolation.
- Opened PR #398: https://github.com/AndreVazao/VazaoSovereignTrader/pull/398 — `test(observer): enforce lightweight Runtime summary contract`, branch `test/observer-summary-fast-path-guards-2026-10-21`.
- PR #398 adds regression tests asserting the authenticated observer endpoint does not call `SovereignEngine.snapshot()`, constrains the response to primitive status/count/timestamp fields, and preserves the unauthenticated 401 response.
- Latest head: `d3b7302c14227b55d201271b4c0d57d090509e95`. Python workflow run `39609658035` was in progress at dependency installation; Snyk and Vercel pending at last check. Do not merge until Python tests, CodeRabbit, Snyk, Vercel and all required checks are green.
- No engine trade policy, credentials, REAL-mode gate or live-order behavior changed. No PC/mobile tests performed because owner is away from PC.
- Next engineering milestone after #398: implement a measured, bounded/coalescing observer publication path that does not put serialization/network work under engine locks, then test observer saturation and Runtime cycle latency. Do not claim isolation until tests/measurements demonstrate it. Keep one implementation PR open at a time.


- PR #398 merged after Python tests, CodeRabbit, Snyk and Vercel reported success. Merge commit: `f07c4f1e64113bb9751f82f7c0714af5125bed22`. Regression tests now guard the observer summary's primitive-only response and ensure the full engine snapshot is not called.
- Opened PR #399: https://github.com/AndreVazao/VazaoSovereignTrader/pull/399 — `perf(runtime): publish cached observer snapshots outside HTTP path`, branch `perf/runtime-cached-observer-publication-2026-10-21`.
- PR #399 adds `RuntimeObserverSnapshot`, a bounded latest-value mailbox with no queue/subscriber callbacks; the engine publishes at initialization, lifecycle transitions and in a `finally` around each cycle. The authenticated HTTP endpoint reads a detached cached copy without acquiring `engine.lock`.
- Tests cover latest-value replacement, detached copies, fixed primitive schema, and a request-level assertion that the observer route does not acquire the engine lock. Docs state that publication still takes a brief engine lock after cycle/transition; eventual consistency and absence of measured latency/load proof are explicit.
- PR #399 head `8c501ba1a2ba7cd15184faa0b9a9209fc6554008`; CI status pending at initial PR opening. Do not merge until all required checks pass and any failures are inspected.
- Next after #399: measure observer publication lock hold/wait and engine-cycle duration, stress repeated/slow reads, and compare engine latency with observer absent/normal/saturated. Only then design a visual circuit breaker. Do not claim CPU/process isolation or zero latency without evidence.

- PR #399 CI update: Python tests run `39610257663` completed successfully; CodeRabbit, Snyk and Vercel report success. PAPER smoke run `39610257559` has its job steps completed successfully, but GitHub still reports the workflow itself as `in_progress` at the latest poll. Keep #399 open until that workflow is terminal and every required check is green.


## 2026-10-21 — Cached observer merged; receptionist / distributed-office architecture clarified

- PR #399 merged successfully by squash as `f6b47e0f5960cb8f8647997f4429c4bd33b997f0`. Head validated: `8c501ba1a2ba7cd15184faa0b9a9209fc6554008`.
- Confirmed terminal success for Python tests run `39610257663` and PAPER smoke run `39610257559`; CodeRabbit, Snyk and Vercel status checks were success. The PAPER job steps all completed successfully.
- #399 provides a bounded latest-value observer mailbox; authenticated `/observer/summary` reads the cached primitive-only snapshot without taking the engine lock in the HTTP route. This is not yet proof of zero Runtime impact or CPU/process isolation; publication still briefly copies fields under the engine lock after cycles/transitions, and latency/saturation benchmarks remain outstanding.
- Owner clarified the product topology: the Runtime/brain and dashboard/virtual office happen to be on the same PC initially, but the brain may later run on another host. Architecture must therefore treat Runtime as an independent service and the dashboard/office as clients from the start.
- The office chat area should behave like a real company: the owner submits a natural-language request at a Reception/dispatcher, which clarifies ambiguity, classifies and routes a task to the appropriate department, tracks status/ownership, and returns a consolidated answer in the same conversation. Departments include research, analysis, exchange comparison, shared learning/memory, and fast reaction/execution subject to existing risk and human-authorization gates.
- Reception/office is an orchestration and observation surface, not a second brain or trading executor. One authoritative Runtime; no duplicate engine/state. Department responses must cite freshness/provenance and distinguish findings from hypotheses. Mutations and any live trading action remain subject to existing server-side permissions/guards and explicit authorization.
- Future distributed topology: local IPC/network when co-located; authenticated remote transport when separated, with Tailscale preferred for private connectivity and discovery/rendezvous not treated as the trust boundary. No public unauthenticated Runtime API. Keep credentials out of URLs/logs/client persistence.
- Non-negotiable: office rendering, chat UI, avatars and department animations must never block Runtime. Under pressure, visual fidelity/update frequency degrades and then visuals disable; Runtime's own risk policy remains authoritative.
- Next: open one small documentation/contract PR specifying Reception dispatch, task lifecycle, department capability/permission boundaries, Runtime-independent topology, and acceptance tests. Then implement routing incrementally with tests. Physical PC/mobile integration remains pending until owner is back at the PC.


- Documentation branch created from merged main: `docs/reception-dispatch-distributed-office-2026-10-21`, commit `6d311992abb2207f5207df8396e9c6b48551bdc7`. New doc: `docs/RECEPTION_DISPATCH_AND_DISTRIBUTED_OFFICE.md`, defining the Reception dispatcher, task contract, department boundaries, same-host/future remote topology, security boundaries and acceptance tests.
- Attempt to open the documentation PR through the GitHub action was blocked by a tool safety check; no PR was created by that attempt. Branch/doc exist, but must verify branch contents and open the PR through an allowed route before treating it as reviewable. Do not start another implementation PR meanwhile.


## 2026-10-21 — Office conversation modes clarified

- Owner clarified desired interaction model: most communication should be directly with the CEO as the primary/default chat; Reception is for ordinary requests the owner chooses to route; the owner must also be able to click any department and speak with that department in a separate direct conversation.
- Opened documentation PR #400: https://github.com/AndreVazao/VazaoSovereignTrader/pull/400 — `docs: define Reception dispatch and distributed office contract`. Branch `docs/reception-dispatch-distributed-office-2026-10-21`, initial commit `6d311992abb2207f5207df8396e9c6b48551bdc7`.
- Added `docs/VIRTUAL_OFFICE_CONVERSATION_MODES.md` on the PR branch, commit `b16394b9a4e8e41bcecc0b73bebfba3d3c38a92d`, explicitly specifying CEO as default, direct department chats, and Reception as optional routing.
- Required UI: visible active interlocutor, distinct conversation/task correlation, direct department requests do not pass through Reception unless requested, and switching rooms never creates another Runtime or changes authorization.
- PR #400 is open and unmerged; review/checks pending. Documentation only; no Runtime code or trading permissions changed.


## 2026-10-21 — PR #400 clarified conversation modes

- Re-reviewed PR #400: https://github.com/AndreVazao/VazaoSovereignTrader/pull/400.
- Found and corrected wording conflict in `docs/RECEPTION_DISPATCH_AND_DISTRIBUTED_OFFICE.md`: Reception is explicitly optional; CEO is the default conversation; direct department chats are supported without mandatory Reception/CEO routing. Each path keeps its own conversation/task correlation.
- Latest docs commit: `d5d35d73b628569a3713e829d1770633a400392b`.
- Latest PR head is mergeable/clean and docs-only, but checks for the updated head had not yet appeared at last poll (zero check runs/statuses). Do not merge until the latest head's applicable checks are verified.
- CodeRabbit skipped automated review because the public repository has fewer than 10 stars; manual content review found and fixed the Reception-only wording conflict.
- No runtime code, execution gates, or trading permissions changed.
- Next: verify checks for PR #400 latest head; after merge, open one focused test/metrics PR for observer publication lock/cycle latency and saturated-consumer behavior. No PC/mobile physical validation until owner returns to the PC.


## 2026-10-21 — PR #400 merged; observer stress coverage opened

- PR #400 merged by squash as `259519ffa01ab8268976cd4d67304c409e407615`. Latest head checked was `d5d35d73b628569a3713e829d1770633a400392b`; Snyk, CodeRabbit status and Vercel were green. There were no formal review submissions; CodeRabbit explicitly skipped automated review due to the repository's star-count policy. The docs were manually inspected before merge.
- The merged contract explicitly defines CEO as default/primary chat, direct department conversations as a separate supported path, and Reception as optional. These are specifications, not claims that all flows are already implemented.
- Opened PR #401: https://github.com/AndreVazao/VazaoSovereignTrader/pull/401 — `test: stress observer mailbox and add microbenchmark`.
- PR #401 adds `tests/test_observer_snapshot_concurrency.py`, stressing four concurrent readers against 5,000 publications and checking fixed schema, normalized counts, latest-value semantics and thread termination.
- PR #401 also adds `scripts/benchmark_observer_snapshot.py`, which reports p50/p95/p99/max/mean publish/read timings for the isolated in-process mailbox. Its output explicitly warns that this does not measure engine-cycle latency, engine-lock contention, HTTP serialization, or process/CPU isolation.
- PR #401 head: `c637ccf7a912c3a365c49e6c9860bd78bc95fc70`. Python tests workflow run `39618650736` was queued at last check; no combined status checks had appeared yet. PR is open and mergeable according to PR metadata, but must remain unmerged until CI is terminal and green.
- No Runtime behavior, trading permissions, or REAL-mode controls changed in #401. The benchmark is a useful narrow measurement tool, not proof that the office cannot affect engine latency.
- Next after #401: once checks are green, integrate it; then create a separate focused increment to instrument engine cycle duration and observer publication lock wait/hold, and build a controlled comparison for office absent/normal/saturated. Do not claim the visual circuit breaker is implemented until measured thresholds and tests exist. Physical PC/mobile validation still waits until owner is home.


## 2026-10-21 — Observer timing instrumentation and diagnostics

- PR #401 merged successfully as `f02f4879a6821edd5ec59baf21fbf9b951f9c6ae`; Python tests passed.
- PR #402 merged successfully as `8a8bc116c0488575afb8d27e77b4554b50702b25`. It adds bounded in-memory timing samples for Runtime cycle duration and observer lock wait/hold. Python tests and PAPER lifecycle/safety workflow both passed.
- PR #403 is open: https://github.com/AndreVazao/VazaoSovereignTrader/pull/403 — authenticated read-only `/observer/timing` diagnostics endpoint, with auth and response tests. Head `4577a71f11c83f1f50a78214619ebff92aa0441f`; Python workflow `39620306126` was queued at last poll. Do not merge until checks finish green.
- No live-trading or risk-policy changes. Full absent/normal/saturated office benchmarks and PC/mobile validation remain outstanding.


## 2026-10-21 — Authenticated Runtime timing endpoint merged; observer-load benchmark opened

- PR #403 merged by squash as `f2255302a9425aa4c2759645f68bd7e331bacccc`: https://github.com/AndreVazao/VazaoSovereignTrader/pull/403.
- The PR exposes authenticated read-only `GET /observer/timing` with bounded Runtime cycle and observer lock wait/hold metrics. A failing percentile assertion exposed a nearest-rank bug; corrected percentile calculation and a test that incorrectly assumed no lock measurements existed before synthetic values were recorded. Final Python tests passed on head `446477e5df50f9b3bcbfcee9cd4a7ff8cd67ad9e`; PAPER lifecycle/safety workflow also passed.
- Open PR #404: https://github.com/AndreVazao/VazaoSovereignTrader/pull/404 — `test(perf): compare observer load against Runtime cycle wrapper`.
- PR #404 adds `scripts/benchmark_runtime_observer_load.py`, comparing office absent, normal authenticated polling and saturated authenticated polling, reporting cycle-wrapper and endpoint latency percentiles, request errors and reader leaks. It deliberately replaces `_cycle_once` with a no-op: no strategy, exchange requests or orders are executed. Therefore it measures observer-path contention only and must not be presented as full trading-cycle performance or CPU/process isolation.
- Added smoke/unit tests in `tests/test_runtime_observer_load_benchmark.py`. Head `5a2c315b64f1d357887c6d4e9f6e074d50663620`; Python workflow run `39621804246` was queued at last poll. Do not merge until the latest head's applicable checks are green.
- Next: use the benchmark to collect reproducible observer-path measurements; then design a separate harness that can measure the real cycle with controlled/fake exchange adapters and no live orders. Continue to keep Runtime authoritative, keep UI load off critical engine locks, and never claim visual degradation/circuit breaker is implemented until it is measured and tested. PC/mobile tests remain pending until owner returns home; no REAL trading enabled.


## 2026-10-21 — Observer load benchmark merged

- PR #404 merged by squash as `cd938cfbccd9127897228aabea98a3a13baf480a`: https://github.com/AndreVazao/VazaoSovereignTrader/pull/404.
- The Python test workflow on latest head `f41050d74a0d8e15e04401850826395208986700` passed. One initial failure was a case-sensitive assertion on a scope note (`No-op` vs `no-op`); fixed the assertion to normalize case and re-ran CI successfully. The smoke test confirms requests succeed and reader threads terminate.
- `scripts/benchmark_runtime_observer_load.py` compares three scenarios: office absent, normal authenticated polling and saturated authenticated polling. It reports p50/p95/p99/max/mean for Runtime cycle-wrapper and HTTP observer-summary latency, request/error counts, thread leaks and bounded timing metrics.
- Critical limitation: this harness intentionally replaces `_cycle_once` with a no-op. It performs no strategy calculations, exchange requests or orders. It is only a reproducible observer-path/API contention benchmark, not full trading-cycle performance, real market timing or CPU/process isolation.
- Next: build a separate safe test harness for a representative full Runtime cycle using deterministic fake exchange adapters and PAPER-only fixtures, with no network and no live orders. Then compare p50/p95/p99 with observer absent/normal/saturated. Keep one implementation PR open at a time; physical PC/mobile integration tests wait until owner is home.


## 2026-10-21 — Correctness fix: unknown WebSocket latency was shown as zero

- During source audit after PR #404, found `PC_ENGINE/diagnostics/operational.py` converted missing/null `local_receive_latency_ms` to integer `0` using `int(value or 0)`. This falsely presents unknown/unvalidated timing as zero-millisecond latency, undermining temporal-edge analysis.
- Opened PR #405: https://github.com/AndreVazao/VazaoSovereignTrader/pull/405 — `fix(diagnostics): preserve unknown websocket latency`.
- Changed diagnostics to emit JSON null for missing, null or malformed latency while preserving a genuine explicit zero and valid positive values. Added regression tests for all cases.
- PR #405 head `33bdafa637db7211dbbafbee2eb113e50fec14e9`; Python workflow `39622462500` was queued at last poll. Keep it open until the latest-head tests are green.
- This does not change execution logic or enable live trading; it prevents diagnostics from inventing a timing value. Continue checking downstream reports for other places where missing timing is coerced to zero.


## 2026-10-21 — WebSocket timing integrity and reconnect resilience

- PR #405 merged as `4231af440de06a22eb67d15f0355740b3135a23b`: operational diagnostics preserve missing/null/malformed `local_receive_latency_ms` as unknown rather than coercing it to zero; explicit zero remains valid.
- PR #406 merged as `fcb2437387dba10f9ad860aeecabbeba6b7be2ff`: WebSocket event construction no longer subtracts exchange event time from local wall clock and labels the difference as one-way network latency. The value remains unknown until a calibrated clock-offset model exists, and the fast-path bridge fails closed when it is unknown. Regression tests passed in Python workflow run `39624742839` on PR head `19c4f9592939a3ea3a822afd8936ecd10145d3cc`.
- Open PR #407: https://github.com/AndreVazao/VazaoSovereignTrader/pull/407 — bounded exponential reconnect backoff with jitter now covers both normal WebSocket disconnect returns and exceptions; delay resets only after actual socket uptime reaches the stable interval (not while DNS/connect is stalled). Deterministic tests cover backoff growth, cap and stable-connection reset.
- PR #407 latest head: `825468482bbd59bb053d29a756007578fc7f8176`; Python workflow run `39625620537` was still running the test suite at checkpoint time. Do not merge until this exact head's CI completes successfully.
- Clean-room study continues to use Freqtrade, CCXT and Hummingbot as design references, not copied code. Research priorities: per-exchange capability/quality matrix, WebSocket freshness/recovery, order-book consistency, rate-limit/retry policy and a read-only BingX public Spot feed candidate. BingX public Spot stream uses `wss://open-api-ws.bingx.com/market`; official integration notes identify GZIP-compressed messages and heartbeat requirements, which must be tested explicitly before declaring support.
- No private API keys, live orders, transfers, withdrawals or REAL-mode changes. Physical PC/Android validation still waits until owner returns to PC. Keep one implementation PR open at a time.


## 2026-10-21 — Reconnect resilience merged; source-timestamp fabrication audit

- PR #407 merged successfully as `ad8a66e7707f1c5c6dccbf2509f78f815f691f2b`: https://github.com/AndreVazao/VazaoSovereignTrader/pull/407. Python test workflow run `39625641048` passed on exact PR head `825468482bbd59bb053d29a756007578fc7f8176`. Reconnect backoff now handles normal disconnect returns and exceptions, applies jitter, caps the delay and resets only after a genuinely stable connection.
- Source audit found a second timestamp-integrity problem in `PC_ENGINE/radar/websocket_radar.py`: Binance and OKX parser paths substituted local receive wall time when venue trade timestamp was missing, while Coinbase's ISO parser did the same for missing/malformed time. This can fabricate exchange-time evidence and create false cross-venue lag.
- Open PR #408: https://github.com/AndreVazao/VazaoSovereignTrader/pull/408 — reject native Binance/Coinbase/OKX public-trade messages when the venue timestamp is missing, malformed or non-positive; do not substitute receive time. Added parser regression tests and documented the policy.
- PR #408 head `5c0c12a5d148ad69cff3ef7c208d6c739664c684`; Python workflow run `39627161341` was still executing the test suite at last poll. Do not merge until CI passes on the exact latest head; inspect failure logs if it fails.
- Important distinction: `local_ts_ms` is local receive wall time; `exchange_ts_ms` is source-provided venue event time; `local_receive_latency_ms` remains unknown without a validated clock-offset model. Never fill one field from another. Cross-venue temporal candidates remain research evidence, not proof of executable profit.
- Continue audit for consumers that assume timestamps are always present, improve normalized event schema and timestamp-quality reporting, then implement deterministic representative Runtime-cycle benchmark using fake exchange adapters and PAPER fixtures. No live orders or REAL-mode changes. Physical PC/Android tests remain pending until owner is home; one implementation PR at a time.


## 2026-10-21 — Reject fabricated source timestamps; timing validation semantics under review

- PR #408 merged successfully as `2c40ecc864519a5b606a104673ef117144a38ecc`: https://github.com/AndreVazao/VazaoSovereignTrader/pull/408. Python workflow run `39627161341` passed on exact head `5c0c12a5d148ad69cff3ef7c208d6c739664c684`.
- Binance, Coinbase and OKX public trade parsers now reject missing/malformed/non-positive venue trade timestamps rather than substituting local receive time. Added regression tests and a documented timestamp policy. This removes a path that could fabricate exchange-time lead/lag evidence.
- Open PR #409: https://github.com/AndreVazao/VazaoSovereignTrader/pull/409 — source audit found `PC_ENGINE/research/websocket_timing_validation.py` compared local receive wall time against exchange event time and called that a negative latency. It also treated missing latency as an invalid timestamp, obscuring the actual evidence gap.
- PR #409 separates timestamp quality from receive-latency quality, counts unknown/malformed latency explicitly, never subtracts different clock domains to infer one-way latency, and keeps economic interpretation blocked until required latency evidence is available. Added tests for unknown latency and clock-domain separation.
- PR #409 head `363b58f4ed8d320b4c7f33b25f2ef11de0036c09`; Python workflow run `39627582204` was in progress at last poll. Do not merge until CI passes on this exact latest head.
- The readiness gate remains fail-closed: no inference of profit, no private API changes, no live orders, no REAL-mode authorization. Continue next with deterministic full-cycle PAPER benchmark using fake adapters, and then connector conformance/health contracts. PC/mobile validation remains pending until owner is back at PC; one implementation PR at a time.


## 2026-10-21 — Escritório virtual: renderização adaptativa por dispositivo

- Proprietário confirmou o requisito: **a planta, os departamentos e as ligações são sempre os mesmos; a representação visual adapta-se ao aparelho e aos recursos disponíveis**.
- Atualizado o PR #411: https://github.com/AndreVazao/VazaoSovereignTrader/pull/411 — `docs(office): apply approved departments to exploded mockup`.
- Head atual confirmado depois das atualizações: `acfd8072baf5622581af55a5ea7986ed6dcb67dc`; PR aberto, não merged, base `main`, 4 ficheiros alterados. A consulta de workflow runs associadas a este commit não devolveu runs; não afirmar CI verde. Manter sem merge até confirmar a política/checks aplicáveis ao head atual.
- Atualizados `docs/SOVEREIGN_TRADER_VIRTUAL_OFFICE_3D_MOCKUP.md` e `docs/SOVEREIGN_TRADER_VIRTUAL_OFFICE_DEPARTMENTS.md` com perfis de renderização: chat/acessibilidade; 2D económico com palitos para PC antigo; pixel-art; 2.5D; 3D detalhado; cinemático/alta definição.
- Definida separação explícita entre modelo canónico (planta, IDs estáveis, relações e estado semântico) e renderizadores substituíveis. O telefone pode usar 3D se tiver capacidade; PC antigo começa leve. Há seleção manual, deteção conservadora, descida automática sob pressão, carregamento/libertação de assets sob procura, animações limitadas e fallback 2D/chat.
- Invariante de arquitetura: a qualidade visual não muda departamentos, memória central, permissões, autorização, gates de risco nem o ciclo de trading. A UI pode degradar; o Runtime continua headless e independente.
- Critérios de aceitação documentados; ainda é necessário medir CPU/RAM/frame time/tráfego no PC real e no telefone real. Não declarar os perfis validados nem afirmar que renderização adaptativa já está implementada no produto.
- Sem execução REAL, ordens, transferências ou alteração de permissões. Próximo passo após integrar a documentação: mapear IDs/estados das salas para fontes reais autenticadas do Runtime e implementar o seletor de renderizador em incremento isolado, mantendo um PR de implementação de cada vez.


## 2026-10-21 — Escritório adaptativo integrado; correção de métricas temporais em revisão

- PR #411 foi integrado por squash como `69ba0fd967b15c3610dc9fd2ce5c84ef940e1c1d`. Checks no head exato `acfd8072baf5622581af55a5ea7986ed6dcb67dc`: Snyk, CodeRabbit e Vercel reportaram success. A especificação de renderização adaptativa e as decisões de departamentos estão agora integradas em `main`.
- PR #412 aberto: https://github.com/AndreVazao/VazaoSovereignTrader/pull/412 — `fix(research): preserve unknown empty timing statistics`.
- O validator `PC_ENGINE/research/websocket_timing_validation.py` ainda emitia zero para média/p50/p95/p99/máximo quando não havia amostras válidas de latência, e zero para estatísticas vazias de diferença de lag. Isso confunde “não medido” com “zero medido”, contrariando o requisito de integridade temporal.
- PR #412 altera essas estatísticas vazias para `None`/JSON null e acrescenta testes de regressão em `tests/test_websocket_timing_validation.py`. Head `fd61ce834ea6afe6f88353b5daf406652e98412b`; estado combinado consultado: Vercel pending, ainda sem evidência de CI verde. Não fazer merge antes de verificar os checks aplicáveis no head atual.
- A recolha de dados públicos já tem código documentado no README (Market Radar por polling e collector WebSocket público para Binance/Coinbase/OKX), mas isto **não prova que esteja ativo no PC do proprietário neste momento**. A recolha contínua e a saúde dos dados têm de ser verificadas na máquina real quando o proprietário estiver junto do PC. Não afirmar que o processo foi iniciado remotamente ou que existem dados novos sem evidência.
- Próxima prioridade: confirmar CI e integrar #412 se passar; depois fazer auditoria operacional do collector (arranque automático, ciclo de vida, heartbeat/freshness, reconexão, persistência JSONL, limites de disco e relatório de saúde), acrescentar teste controlado com feeds simulados e PAPER-only, e só depois orientar o proprietário a validar no PC real. Sem ordens reais, credenciais privadas ou alterações de permissões.


## 2026-10-21 — Hierarquia de chefes e subagentes aprovada

- PR #412 foi integrado por squash como `409f93e3e12d84ab2be58a634b007a1921b3693b`. No head exato `fd61ce834ea6afe6f88353b5daf406652e98412b`, CodeRabbit, Snyk, Vercel e o workflow Python tests terminaram com sucesso.
- A pedido do proprietário, criada a proposta formal de hierarquia para o Sovereign Trader no PR #413: https://github.com/AndreVazao/VazaoSovereignTrader/pull/413 — `docs(agents): define department chiefs and reporting hierarchy`.
- Head atual do #413: `c5d209a2d77c4f27445804a2d026c77f173aa491`. CodeRabbit e Snyk estão success; Vercel estava pending na última consulta. Workflow runs ainda não apareciam. **Não fazer merge enquanto os checks aplicáveis ao head atual não estiverem concluídos e aprovados.**
- Hierarquia proposta: Operador → CEO → chefe de departamento → subchefe/coordenador opcional → agentes especializados. CEO comunica operacionalmente com os chefes; utilizador pode falar com CEO por omissão ou selecionar um departamento para falar com o respetivo chefe.
- Chefes lógicos: Atlas (Market Radar), Delta (Comparação entre Exchanges), Bridge (Integrações), Sherlock (Investigação), Athena (Análise), Flash (Resposta Rápida/PAPER), Turing (Laboratório PAPER/Replay), Sentinel (Controlo de Risco), Mnemosyne (Memória Central), Scribe (Auditoria), Phoenix (Saúde/Recuperação), Guardian (Intervenção Humana/Aprovações).
- Documentação acrescenta subagentes/frentes de trabalho, formato mínimo das mensagens, correlação por task/message ID, proveniência, confiança, incertezas, relatório consolidado, escalada de conflitos e prevenção de trabalho duplicado/perda de informação.
- Estado explicitamente documental: os nomes identificam papéis planeados, não provam que 12 agentes autónomos já estejam implementados ou ativos. Implementação futura deve começar pelo contrato de mensagens/supervisão e relatórios auditáveis. Resposta Rápida continua PAPER/observacional; Sentinel e os gates de risco não podem ser contornados.
- Sem ativação de ordens reais ou alteração de permissões. Manter a regra de um PR de implementação de cada vez.


## 2026-10-21 — Modelo distribuído e nomes próprios para todos os agentes

- O proprietário clarificou que a instalação futura será distribuída: CEO, departamentos e Memória Central podem residir em PCs/servidores diferentes. A identidade e a hierarquia devem manter-se independentemente da localização física.
- Atualizado o PR #413 no branch `docs/department-chief-hierarchy`; novo head `fe7870e43bac433a0a65b4ee3997927671151eb9`. O commit amplia `docs/SOVEREIGN_TRADER_VIRTUAL_OFFICE_DEPARTMENTS.md` com identidade estável por agente, IDs imutáveis, node_id mutável, supervisor, permissões mínimas, leases/heartbeats, protocolo remoto, idempotência, recuperação de tarefas e auditoria ponta a ponta.
- O documento agora contém nomes próprios propostos para 48 subagentes, além dos 12 chefes anteriormente definidos. “Feed Watcher”, “Cost Analyst”, etc. são descrições funcionais; os nomes próprios individuais passam a identificar cada agente lógico.
- Exemplos de chefes: Atlas (Market Radar), Delta (Comparação entre Exchanges), Bridge (Integrações), Sherlock (Investigação), Athena (Análise), Flash (Resposta Rápida), Turing (PAPER), Sentinel (Risco), Mnemosyne (Memória Central), Scribe (Auditoria), Phoenix (Recuperação), Guardian (Aprovações).
- Regra de deployment: mover um agente de PC/servidor não altera o seu `agent_id`; estado offline não significa tarefa concluída; mensagens repetidas são idempotentes; relatórios sobem pela hierarquia; Memória Central guarda conhecimento/proveniência, mas não substitui a autoridade do Runtime nem os gates de risco.
- Checks consultados para o novo head `fe7870e...`: ainda não havia statuses nem workflow runs publicados. PR #413 permanece aberto; não fazer merge até os checks aplicáveis ao head atualizado estarem concluídos e verdes.
- Esta alteração é documental e proposta para implementação; não significa que os 60 agentes já estejam ativos. Próximas fases: contrato de identidade/mensagens, supervisão e fila durável, heartbeat/leases, auditoria e testes de vários nós simulados; só depois conectar máquinas reais. PAPER/observação continua obrigatório; nenhuma ordem REAL autorizada.


## 2026-10-21 — Registo Vercel, nomes globais únicos e proveniência de aprendizagem entre instalações

- Novo requisito do proprietário: quando computadores partilham aprendizagem, cada instalação consumidora deve ver quem originou a descoberta, em que instalação/PC, em que condições, quais evidências foram recolhidas, quem verificou/validou e qual o estado atual. Exemplo conceptual: “Joana, agente da instalação ANDRE-PC-01, descobriu X sob condições Y; validado por Z”. Importar conhecimento não altera a autoria original; reprodução, validação ou contestação noutro PC acrescenta eventos separados.
- Cada instalação, departamento e agente provisionado deve ter IDs estáveis únicos (installation_id, node_id, department_id, agent_id) e nomes legíveis globalmente exclusivos no registo do Sovereign Trader. Nomes de funções genéricas podem repetir-se como categorias; identidades e nomes próprios de agentes/departamentos não. Nome não é autenticação: IDs e credenciais são a identidade técnica.
- Vercel é um registo mínimo de bootstrap/rendezvous e descoberta entre telefone e PCs/servidores, evitando digitar IPs manualmente. No primeiro registo, reservar nomes de forma atómica, publicar só metadados mínimos, gerir presença por heartbeat/lease e suportar revogação. Colisões devem ser rejeitadas, não aceites silenciosamente. A recuperação de instalação existente deve ser distinta de criar uma instalação nova.
- Após descoberta/autenticação, comunicação privada deve preferir LAN em casa e Tailscale quando remoto. Vercel não deve ser proxy obrigatório para o tráfego contínuo nem fonte de autoridade do Runtime. A perda do registo não pode autorizar bypass de segurança nem parar automaticamente Runtime local já autorizado.
- Separar três planos: (1) registo/descoberta Vercel; (2) mensagens/tarefas operacionais autenticadas via LAN/Tailscale; (3) memória de aprendizagem partilhável com evidência, condições, versões, validade e proveniência. Memória não concede permissões nem dispara ordens. Nunca partilhar chaves, tokens, credenciais, saldos ou dados privados de conta.
- A documentação foi acrescentada ao PR #413, branch docs/department-chief-hierarchy, novo head 30d1da52dda8ebff462119c92025c3d503a9a17d: secção “Registo global de instalações, nomes únicos e proveniência de aprendizagem”. O PR permanece aberto. Na consulta imediatamente após o commit, CodeRabbit estava success, mas Snyk e Vercel estavam pending; workflow runs retornou vazio. Não fazer merge até verificar que os checks aplicáveis ao head exato terminaram com sucesso.
- Critérios futuros: testes de colisão concorrente, nomes/IDs duplicados, reinstalação e recuperação, revogação, presença expirada, telefone sem IP manual, importação sem perda de autoria, validações independentes e divergentes, mensagens duplicadas e nó offline. Fase atual apenas documental/simulada e PAPER/observacional; não ativar ordens reais.


- Atualização final de PR #413: depois do commit documental sobre registo Vercel, nomes globais únicos e proveniência, os checks para o head exato 30d1da52dda8ebff462119c92025c3d503a9a17d ficaram verdes (CodeRabbit, Snyk e Vercel). PR #413 foi integrado por squash em 2026-10-21; merge SHA: edf0dbf88a5478af4c7433e3927d7683116f435e. Isto integra documentação, não implementa ainda o serviço Vercel nem ativa agentes autónomos.


## 2026-10-21 — PR #414: validação estrita dos trades públicos do Market Radar

- Nova PR: https://github.com/AndreVazao/VazaoSovereignTrader/pull/414 — branch fix/radar-reject-invalid-trade-values.
- Alterações em PC_ENGINE/radar/websocket_radar.py: os adapters públicos Binance, Coinbase e OKX passam a rejeitar preços e quantidades ausentes, malformados, não finitos (NaN/Inf), negativos ou zero. Valores inválidos não devem entrar em eventos, movimentos nem candidatos lead/lag.
- Foram acrescentados testes determinísticos em tests/test_websocket_radar.py para preços inválidos e quantidades inválidas nos três adapters, incluindo rejeição de quantidade zero.
- Estado ao último check: PR #414 aberto, head 853bab2b316b93afdc04f8d367b2130c2d0045aa. Para este head, combined status devolveu statuses vazios e workflow runs vazio; não afirmar que os testes passaram nem fazer merge sem checks verdes aplicáveis. A PR é uma alteração pequena de qualidade de dados, observacional/PAPER, sem ordens ou credenciais privadas.
- Próxima sequência após resolver #414: auditoria da persistência JSONL (falhas de disco, limites/rotação e integridade), lifecycle/reconexão/health do coletor e testes determinísticos com feeds falsos; só depois recolha real verificada no PC do proprietário. Não afirmar que o coletor está a correr no PC local.


## 2026-10-21 — Market Radar: validação numérica, persistência e freshness/worker health

- PR #414 foi integrado por squash; merge SHA `4be9e43934c167766a5c201156cff2cf161ba07f`. Os parsers públicos Binance, Coinbase e OKX rejeitam agora preços/quantidades inválidos, não finitos ou não positivos, evitando contaminar eventos e candidatos lead/lag.
- PR #415 foi integrado por squash; merge SHA `488684cc33373a5f565486735dc3f0c109d545c6`. A persistência JSONL foi centralizada num helper que serializa com `allow_nan=False`, contabiliza falhas de persistência no health snapshot e impede que uma falha de disco/serialização mate o feed público ou o callback. Teste determinístico cobre `OSError` de disco.
- PR #416 foi integrado por squash em 2026-10-21; merge SHA `ab68f119897d77093c54582fe6fdbd773bdcda1d`. No head exato `70ddd2933324a1c411e9931c0bb6ba9051047ad5`, CodeRabbit, Snyk, Vercel e o workflow Python tests (run `39668440581`) terminaram com sucesso.
- O snapshot do WebSocket Market Radar agora expõe `trade_freshness` por exchange (`no_trade_yet`, `recent_trade`, `no_recent_trade`, limiar inicial de 30 segundos) e `worker_alive` baseado no estado real das threads. Silêncio de trades é sinal de frescura dos dados, não prova de socket desligado; mercados/símbolos podem estar quietos.
- Estes incrementos são de qualidade de dados, observabilidade e resiliência, em modo público/observacional. Não ativam ordens REAL, não usam credenciais privadas e não provam que o coletor esteja efetivamente em execução no PC do proprietário.
- Próximo trabalho: auditar lifecycle do coletor (arranque/paragem controlados, recuperação após restart, reconexão, heartbeat, persistência/rotação e limites de disco) com testes determinísticos/fake feeds, mantendo PAPER/observação e um PR de implementação de cada vez. Só depois orientar validação física no PC quando o proprietário estiver disponível.


## 2026-10-21 — PR #417: lifecycle control do WebSocket Market Radar

- Aberta PR #417: https://github.com/AndreVazao/VazaoSovereignTrader/pull/417 — `fix/radar-controlled-lifecycle`, head `88a7864b905a013a9be4f61e126264902db12db7`.
- Corrige quatro riscos de ciclo de vida: chamadas repetidas a `start()) podiam criar workers duplicados; `stop()) não fechava explicitamente sockets ativos; referências de threads eram apagadas mesmo quando a thread podia sobreviver ao timeout; `snapshot().running` podia confundir uma lista não vazia com workers realmente vivos.
- A implementação torna `start()` idempotente enquanto houver workers vivos, fecha sockets registados durante `stop()`, trata a corrida entre stop e criação de socket e conserva referências a threads que não terminem no timeout.
- Acrescentados testes determinísticos com worker bloqueado e fake WebSocket, sem ligação real a exchanges.
- Checks no head exato: CodeRabbit e Snyk success; Vercel ainda pending; workflow Python tests run `39669146924` ainda in progress na última consulta. PR permanece aberta; não fazer merge até todos os checks aplicáveis terminarem com sucesso.
- Não foram executados testes localmente nesta sessão; não há confirmação de que o coletor esteja ativo no PC do proprietário. Escopo exclusivamente observacional/PAPER, sem credenciais privadas nem ordens.


## 2026-10-21 — PR #417: proteção contra corrida entre start/stop

- PR #417 continua aberta: https://github.com/AndreVazao/VazaoSovereignTrader/pull/417. Durante revisão manual do ciclo de vida, identifiquei uma corrida adicional: `stop()` podia libertar o lock antes de terminar o join; um `start()` concorrente podia limpar o evento de paragem e reabrir workers durante o shutdown.
- No branch `fix/radar-controlled-lifecycle`, novo head `6b715b6b8ab1c1dc950503de29d31c9cc7b681f9`: introduz `_stop_lock` para serializar pedidos de paragem e `_stopping` sob `_lifecycle_lock`; `start()` não reinicia workers enquanto a paragem está em curso.
- Acrescentado teste determinístico com fake WebSocket cujo `close()` fica bloqueado até o teste permitir a continuação. O teste chama `start()` durante o shutdown e verifica que não nasce um segundo worker e que o estado final fica parado.
- Depois das alterações, o estado consultado no novo head mostrava Snyk pending e nenhum workflow Python publicado ainda; CodeRabbit foi novamente solicitado. **Não afirmar testes/checks verdes nem fazer merge** até verificar o head exato e aguardar todos os checks aplicáveis.
- Não foram executados testes localmente nesta sessão; alterações exclusivamente de lifecycle do coletor público/observacional, sem credenciais privadas, ordens ou ativação REAL. Não há prova de que o coletor esteja ativo no PC do proprietário.


## 2026-10-21 — PR #417: retry de fecho para corrida no arranque do WebSocket

- A revisão CodeRabbit de #417 identificou um segundo caso de corrida: o primeiro `app.close()` pode acontecer depois do teste de `_stop` mas antes de `run_forever()`; em `websocket-client`, o arranque do loop pode repor o estado interno e ignorar esse fecho antecipado.
- Corrigido no branch `fix/radar-controlled-lifecycle`: novo head `b7613321a3b0e511059162e8a5bb45e7a94cade9`. Durante até 3 segundos de shutdown, `stop()` volta a tentar fechar os sockets enquanto faz joins curtos às threads vivas; conserva referências se alguma thread sobreviver ao limite.
- Adicionado teste determinístico com evento de paragem instrumentado e fake WebSocket que pausa precisamente entre o check de `_stop` e a entrada em `run_forever()`, simulando o primeiro close antecipado e verificando que um close posterior termina o worker.
- A revisão manual também levou à proteção `_stop_lock` + `_stopping`, que impede `start()` de limpar o pedido de paragem enquanto `stop()` ainda está a fechar/aguardar workers.
- Checks para o novo head: Vercel e Snyk pending; workflow Python tests ainda não publicado na última consulta; CodeRabbit recebeu novo pedido de revisão. PR aberta e sem merge até CI/revisão do head exato ficarem verdes.
- Não foram executados testes localmente; sem confirmação de execução no PC do proprietário. Alterações apenas de lifecycle do collector público/observacional, sem credenciais privadas, ordens ou permissões REAL.


## 2026-10-21 — Diretriz permanente: transferir conhecimento de projetos de trading estabelecidos

- O utilizador reforçou que devemos continuamente estudar bots/plataformas de trading conhecidos e integrar técnicas comprovadas no VazaoSovereignTrader, não deixar esse trabalho para uma fase indefinida.
- Referências prioritárias já definidas: Freqtrade (multi-exchange, protocolos, WebSockets, frescura e normalização dos dados, precisão, limites/erros e execução) e Cabin Freight Trade (maturidade funcional e preparação multi-exchange); estudar também outros projetos relevantes quando acrescentem valor concreto.
- Método obrigatório: distinguir princípios/técnicas gerais de código e componentes específicos; não copiar código, não depender de licenças ambíguas/incompatíveis, preservar a identidade e arquitetura próprias do Sovereign Trader. Usar laboratório/simuladores quando necessário e contratos/testes próprios antes de integrar.
- Prioridade estratégica continua a ser detetar diferenças temporais reais entre exchanges e provar se são executáveis após frescura, sequência/timestamps, instrumentos equivalentes, liquidez, taxas, slippage, inventário e latência. PAPER/replay/sintético antes de qualquer consideração de execução real; nenhuma técnica de outro bot constitui autorização para ordens.
- Aplicação prática: cada auditoria de componente deve identificar (1) padrão comprovado que vale aprender, (2) evidência/documentação pública, (3) adaptação própria proposta, (4) riscos/licença/dependências, (5) testes de aceitação, (6) resultado da validação. Manter um registo de aprendizagens e ligar cada aprendizagem a uma mudança de código ou decisão explícita de não integrar.
- Esta diretriz deve acompanhar a fila de trabalho após resolver a PR #417; não abrir uma segunda PR de implementação concorrente antes de a #417 ser concluída.


## 2026-10-21 — PR #417 merged; PR #418 temporal causality gate

- PR #417 merged by squash: https://github.com/AndreVazao/VazaoSovereignTrader/pull/417, merge commit `b124a1e139a2ae4e402740498e4e02fae3c293f8`. At the verified head `b7613321a3b0e511059162e8a5bb45e7a94cade9`, Snyk, Vercel, CodeRabbit status and Python tests all reported success. This integrates lifecycle serialization, retry-close during shutdown, and deterministic race tests. No local test run and no evidence that collector is running on the user's PC.
- Opened PR #418: https://github.com/AndreVazao/VazaoSovereignTrader/pull/418, branch `fix/radar-reject-noncausal-lead-lag`, head `7decf7515b08969769a27b136b4b61964191baf8`.
- #418 adapts a core market-data quality principle common to robust temporal systems: exchange timestamps alone are insufficient to claim a leader/follower edge; local receive order and delivery freshness must also be consistent. `_match_candidate` now rejects negative local receive lag (causality inversion) and local receive lag exceeding `lead_window_ms`, before writing candidate/edge statistics.
- Added deterministic tests for inverted receive order and stale local delivery, and documented the gate in `docs/SOVEREIGN_MARKET_RADAR.md`. Observation/PAPER only; public data, no credentials, no orders, no REAL changes.
- #418 CI/review still needs to validate exact head; no tests run locally. Continue one PR at a time. Learning policy remains: study established projects (especially Freqtrade multi-exchange/data protocols and Cabin Freight Trade maturity), adapt concepts rather than copying code, record evidence/tests/licence considerations, and validate before integrating.


## 2026-10-21 — PR #418 merged; temporal lead/lag causality gate

- PR #418 merged by squash: https://github.com/AndreVazao/VazaoSovereignTrader/pull/418, merge commit `f83755cf376f085b9ed7631815596adf47d7f967`.
- Exact validated head: `7decf7515b08969769a27b136b4b61964191baf8`. Python tests succeeded, Snyk and Vercel succeeded, and CodeRabbit status was green but its manual review command was rate-limited; a manual diff review was performed before merge.
- Radar rejects lead/lag candidates when local receive order is inverted or local receive lag exceeds `lead_window_ms`, in addition to the exchange timestamp window. Tests cover inverted receive order and stale local delivery. This reduces false temporal-edge candidates but does not establish profitability.
- Observation/PAPER only; no credentials, orders or REAL-mode changes. Continue one implementation PR at a time, and record reference-project lessons with evidence, own adaptation, tests and validation.


## 2026-10-21 — PR #419: deduplicate replayed public trades (open)

- Opened https://github.com/AndreVazao/VazaoSovereignTrader/pull/419, branch `fix/radar-deduplicate-public-trades`; latest head `2884fa2e19d0d5694aa2b765837e7ef45d8194ff`.
- Public venue trade identity is preserved where supplied: Binance `t`, Coinbase `trade_id`, OKX `tradeId`. A bounded 10,000-entry in-memory ordered set of identities (exchange, symbol, trade ID) rejects replay duplicates before counters, movement matching, callbacks and persistence. Blank IDs normalize to unknown; feeds without IDs remain accepted without a dedupe guarantee.
- Added tests for extracting native trade IDs and ensuring a replayed ID does not increment counters, call the callback or write another JSONL event. Updated Radar docs. Changes are public-feed/observation only, no credentials or orders.
- Latest CI snapshot for exact head: Snyk pending; Vercel failed due account deployment quota `api-deployments-free-per-day` (more than 100 deployments; retry in 24 hours), an infrastructure/quota failure, not a code-test result. No GitHub Actions Python test run was returned yet. CodeRabbit review was requested, but review capacity may be rate-limited. Do not merge until code checks/review are sufficiently validated; manually review diff and recheck exact head.
- This change adapts a general exchange-integration reliability principle rather than copying third-party code. Learning notes: venue-native IDs allow replay protection after reconnect, but IDs are optional and the bounded cache is not a durable exactly-once guarantee; eviction means a very old replay may be counted again.


## 2026-10-21 — Freqtrade research note while PR #419 CI runs

- Public Freqtrade docs currently describe WebSocket consumption through CCXT Pro with REST fallback if WebSocket fails or is disabled, plus per-stream configuration (for example OHLCV vs order book): https://github.com/freqtrade/freqtrade/blob/develop/docs/configuration.md
- Freqtrade exchange implementation tracks supported WebSocket capabilities per stream and caches market data/refresh times: https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/exchange/exchange.py
- Freqtrade maintainers' public discussion notes that WebSocket latency benefits depend on endpoint and safe clock-drift assumptions, and that order-book stream volume/subscription lifecycle can become a resource issue: https://github.com/freqtrade/freqtrade/issues/10094
- Adaptation decisions for Sovereign Trader (not copied code): keep feed health/freshness per exchange and per stream; explicit REST fallback policy should be observable, not silent; compare data age and completeness before treating WS as superior; bound subscriptions/buffers and instrument recovery. Before implementation, add replay tests for reconnect gaps, duplicate IDs, and stale snapshots. No new implementation PR opened while #419 is awaiting checks.
- PR #419 exact head `2884fa2e19d0d5694aa2b765837e7ef45d8194ff` remains open. Latest check: Python tests in progress, Snyk success, CodeRabbit status green but its manual review was rate-limited, Vercel failed on account daily deployment quota. No merge until Python tests finish and relevant code review is satisfactory.


## 2026-10-21 — PR #419 merged; next recovery-observability step

- PR #419 merged by squash: https://github.com/AndreVazao/VazaoSovereignTrader/pull/419, merge commit `399be9189b1d050c6f1f9b92c1c44e868af05837`; exact head validated was `2884fa2e19d0d5694aa2b765837e7ef45d8194ff`.
- Python tests completed successfully and Snyk succeeded. CodeRabbit status was green, but a manual review command was rate-limited; I manually reviewed the diff. Vercel failed due the account's daily deployment quota, unrelated to the Python backend tests. No claim of local test execution.
- Market Radar now preserves venue-native trade IDs where supplied (Binance `t`, Coinbase `trade_id`, OKX `tradeId`) and suppresses duplicate IDs within a bounded 10,000-entry in-memory window before updating stats, callbacks and persistence. Blank IDs normalize to unknown; feeds without IDs remain supported. This is bounded replay protection, not durable exactly-once delivery.
- Next single implementation scope: audit reconnect/data-gap observability. Add explicit connection lifecycle signals and last-message timestamps per exchange, distinguish connected/reconnecting/never-connected states, and test normal close, error close, stale feed and recovery. Do not infer a trade-feed sequence gap when the venue's trade stream provides no reliable sequence; document the limit. No orders or REAL execution changes.


## 2026-10-21 — PR #420: WebSocket connection/recovery health (open)

- Opened https://github.com/AndreVazao/VazaoSovereignTrader/pull/420, branch `feat/radar-connection-recovery-health`, head `5dc8f2f1c8af15b06557ea40a051e9aa98c445fc`.
- Exposes per-exchange connection states (`never_connected`, `connecting`, `connected`, `reconnecting`, `stopping`, `stopped`), timestamps for last connected/disconnected/message, and only the exception class for the last connection error (not raw exception text or URLs).
- Added fake-WebSocket test coverage for connected/message/stopped state and initial never-connected state; documented the limitation that silence of trades is not proof of disconnection and trade streams without reliable sequence numbers cannot establish gap-free delivery.
- This is observability only, public feeds/PAPER; no credentials or order changes. PR checks have not yet published Python/Snyk results at the time of this note. Vercel reports the account daily deployment quota limit, so it is not evidence of a Python code failure. CodeRabbit review requested; do not merge until exact-head Python tests and applicable review/checks complete.
- Next after this PR: consider per-stream recovery-gap validation only where the venue protocol provides a trustworthy sequence/checksum/snapshot contract; do not invent gap detection for plain trade feeds.


### PR #420 latest-head update — 2026-10-21

- PR #420 now includes a regression fix distinguishing failed connection attempts from real disconnections: `last_disconnected_ts_ms` is set only when the socket reached the open callback. Added deterministic test asserting a failed connection records the exception class but not a false disconnect timestamp.
- Latest exact head: `de7342d703bf6116976bf66213c38e0a510ad4c4`. Snyk success; CodeRabbit status green but manual review request rate-limited; Python tests pending at last poll; Vercel failure remains account daily deployment quota, not backend test evidence. PR is open and must not merge until Python tests complete and manual review is satisfactory.


### PR #420 — correção do teste de lifecycle (2026-10-22)

- O workflow Python da PR #420 terminou com **1 falha, 1.012 testes aprovados e 77 subtests aprovados**. A falha era `test_stop_closes_active_websocket_and_reports_worker_stopped`: o fake WebSocket chamava `json.dumps`, mas `tests/test_websocket_radar.py` não importava `json`; a exceção dentro do worker impedia o evento de teste `opened` e fazia o teste falhar por timeout.
- Corrigido no mesmo branch da PR #420, commit `01eb90d9e2333481a783705b5ca783af95ba2fc4`: acrescentado o import em falta. Isto corrige a causa observada no log; **não significa que o novo CI já tenha passado**.
- No primeiro check após o push, ainda não havia status nem workflow run publicados para o novo commit. Aguardar e verificar o CI no head atualizado; não fazer merge antes de o workflow terminar com sucesso e da revisão do diff. Vercel continua a reportar limite diário de deploy, independente do teste Python.
- Continua observacional/PAPER, sem credenciais privadas, ordens ou ativação REAL. Uma PR de implementação de cada vez.


### PR #420 — merged (2026-10-22)

- PR #420 `feat(radar): expose websocket connection recovery health` foi merged por squash no commit `85becfa5a58b75e1f072dbb715569d5e38d9bdb2`; head validado `01eb90d9e2333481a783705b5ca783af95ba2fc4`.
- O workflow Python no head corrigido concluiu com sucesso; Snyk, CodeRabbit status e Vercel também estavam verdes. A revisão manual do diff confirmou que `last_disconnected_ts_ms` só é registado após a conexão atingir `on_open`, evitando chamar uma falha inicial de ligação uma desconexão. CodeRabbit não forneceu revisão manual independente devido a rate limit; a revisão do diff foi manual.
- A correção do teste adicionou `import json` em `tests/test_websocket_radar.py`. O snapshot agora expõe estado por exchange, timestamps de ligação/desligação/mensagem e apenas a classe de erro; os streams sem sequência nativa continuam sem alegação de deteção de lacunas.
- Próximo passo: antes de implementar deteção de gaps, estudar por exchange a semântica documentada de sequência/IDs/snapshot; não inferir lacunas de IDs que não sejam garantidamente sequenciais. Continuar investigação de Freqtrade e Cabin Freight Trade com fonte, adaptação própria, risco de licença e testes de aceitação. Nenhuma ordem REAL; PAPER/observação.


### PR #421 — Market Data health heartbeat (2026-10-22)

- Aberta PR #421: `https://github.com/AndreVazao/VazaoSovereignTrader/pull/421`, branch `fix/market-data-health-heartbeat`, head `983f9130ca1e791454944844902cc8860e5a1b4b`.
- Diagnóstico: o collector escrevia `market_data_health.json` no arranque e em ciclos de aprendizagem/estudo, que por defeito são de minutos; o endpoint operacional considera o heartbeat stale após 30 segundos por defeito. Assim, um collector ativo podia aparecer stale entre ciclos.
- Alteração proposta: heartbeat independente do ciclo de aprendizagem, intervalo configurável e limitado em função de `health_stale_seconds`; falhas de escrita do heartbeat são registadas apenas pela classe da exceção e não devem parar a recolha pública. Testes cobrem default, valores inválidos e limites de intervalo.
- Estado na última consulta: Snyk success; Python workflow `39729305426` pendente/ainda sem jobs reportados; Vercel em build. A PR indicou `mergeable=false` temporariamente, por confirmar após atualização de metadata; não fazer merge até confirmar mergeability, workflow Python e status final. Alteração só de telemetria, PAPER/observação.
- Próxima investigação depois de #421: continuar análise técnica de Freqtrade; a pesquisa pública por “Cabin Freight Trade” não identificou um repositório inequívoco, pelo que não afirmar que foi revisto até obter URL exata ou fonte identificável.


### PR #421 — merged (2026-10-22)

- PR #421 `fix(radar): keep market-data health heartbeat fresh` merged by squash: https://github.com/AndreVazao/VazaoSovereignTrader/pull/421.
- Exact validated head: `983f9130ca1e791454944844902cc8860e5a1b4b`; merge commit: `5edfd513f09af18bc9bfbe11200cbdf6735734b4`.
- Python workflow run `39729305426` and job `119660545461` completed successfully. Combined commit statuses for the exact head: Snyk success, CodeRabbit status success, Vercel success. PR metadata confirmed mergeable and the diff was manually reviewed; no formal submitted review was present.
- Collector health telemetry now refreshes `market_data_health.json` on a bounded heartbeat independent of slower learning/study cycles. Interval defaults to 10 seconds and is bounded using `health_stale_seconds`; invalid/non-finite settings fall back safely. An `OSError` writing heartbeat health logs only the exception class and does not stop public market-data collection.
- Added tests for default interval, bounds, stale-window clamping and invalid values. This is observability only: public data/PAPER, no credentials, orders or REAL-mode changes. No claim of local PC testing or of the collector running on the owner's PC.
- Next: continue one scoped implementation PR at a time. Study Freqtrade's public exchange/WebSocket/recovery patterns more deeply, and identify a reliable source/repository for “Cabin Freight Trade” before claiming to review it. For recovery gaps, only implement protocol-specific sequence/checksum/snapshot guarantees; never infer a gap from non-sequential or undocumented trade IDs. Keep learned patterns documented with source evidence, own adaptation, license/dependency risks, acceptance tests and validation. Keep all execution in observation/PAPER; no live orders.


### PR #422 — validação conservadora do lado agressor (aberta, 2026-10-22)

- Aberta https://github.com/AndreVazao/VazaoSovereignTrader/pull/422, branch `fix/radar-reject-invalid-trade-side`, head atual `a364384a441bf64055395cc56cfdacf107f113ee`, base main no merge #421 `5edfd513f09af18bc9bfbe11200cbdf6735734b4`.
- A revisão do diff encontrou um caso de qualidade de dados: Binance interpretava ausência/tipo inválido do campo booleano `m` como BUY por causa de `bool(...)`; Coinbase/OKX podiam aceitar lado vazio/desconhecido. A PR rejeita estes eventos antes de contadores/matching/callback/persistência.
- Inclui testes determinísticos para flag Binance ausente/string, lado Coinbase vazio e lado OKX desconhecido, e atualiza `docs/SOVEREIGN_MARKET_RADAR.md`.
- Estado inicial no head exato: Vercel pending; Python workflow ainda não publicado; sem reviews submetidas. PR não mergeada. Aguardar e validar os checks finais no head exato, rever qualquer comentário e só fazer merge se os checks aplicáveis terminarem com sucesso.
- Escopo observacional/PAPER, apenas dados públicos; nenhuma credencial, ordem ou alteração REAL. Não foram executados testes localmente nem feita ligação a exchanges.


### PR #422 — atualização de CI (2026-10-22)

- Confirmado novamente o head da PR #422: `a364384a441bf64055395cc56cfdacf107f113ee`; PR aberta e mergeable.
- Python workflow `39729766621`, job `119661875892`: em execução, atualmente a instalar dependências; a suite ainda não começou. Snyk success e CodeRabbit status success; Vercel ainda pending. Nenhum review submetido. Não fazer merge até a suite Python e os checks aplicáveis terminarem com sucesso e o diff continuar válido.


### PR #422 — merged (2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/422 `fix(radar): reject invalid trade aggressor sides` merged by squash. Merge commit: `71e4aeda848e5baba2d52e51b33556784c47a027`; validated head: `a364384a441bf64055395cc56cfdacf107f113ee`.
- Exact head CI: Python workflow `39729766621` run #3026 succeeded; job `119661875892` and full test-suite step succeeded. Combined statuses: Snyk success, CodeRabbit success status, Vercel success. No submitted formal reviews or inline review threads were returned.
- Parser now rejects Binance trade payloads missing/non-boolean `m`; Coinbase/OKX side values must normalize to BUY or SELL. Regression tests cover missing/string Binance flag, empty Coinbase side, and unknown OKX side. Docs updated.
- Data-quality/observability only, public market-data/PAPER; no credentials or REAL order path. No local PC tests or live exchange connection claimed.
- Next focus: protocol-grounded exchange-data recovery and Freqtrade reference study. Do not infer sequence gaps from trade IDs; only implement recovery where documented sequence/checksum/snapshot semantics exist. For each reference, record source evidence, adaptation, licensing/dependency risks and tests. Continue one PR at a time and keep real execution disabled.


### PR #423 — erros de processamento WebSocket (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/423, branch `fix/radar-surface-message-errors`, head `f31c6afddf5990eff4fc049b0216f7bbd57727b8`, base main `71e4aeda848e5baba2d52e51b33556784c47a027` (merge #422).
- Adds `message_errors` per exchange and `last_message_error` exception-class-only telemetry to distinguish JSON/parser/dispatch failures from connection errors. Does not persist raw payload or raw exception message; documented that parser rejections of valid but irrelevant/invalid messages are not counted as exceptions. Includes regression test and snapshot test fixture updates.
- Initial CI state on exact head: Vercel pending; Python workflow not yet visible; no submitted reviews. Diff manually inspected. Do not merge until Python suite and applicable checks pass on exact head.
- Safety: public-feed diagnostics only, no private/authenticated streams or orders; no local PC testing or live exchange run claimed.

### PR #423 — telemetria de erros WebSocket (merged, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/423 foi integrada por squash. Commit de merge: `1c83dd9d70cbf030d03fdd3c252a2286e945554a`; head validado: `f31c6afddf5990eff4fc049b0216f7bbd57727b8`.
- Workflow Python run `39730122312` / #3027 concluiu com sucesso; job `119662992512`, incluindo a suite completa, passou no head exato. Checks combinados: Snyk success, CodeRabbit status success e Vercel success/deployment Ready.
- Diff revisto em `PC_ENGINE/radar/websocket_radar.py`, `tests/test_websocket_radar.py` e `docs/SOVEREIGN_MARKET_RADAR.md`.
- O snapshot expõe `message_errors` por exchange e `last_message_error` apenas como classe da exceção para distinguir erros de JSON/parser/dispatch de erros de ligação. Payload bruto e texto da exceção não são persistidos; rejeições deliberadas de payloads não relevantes não são contabilizadas como exceções.
- Não houve reviews formais nem threads inline de revisão. O comentário do CodeRabbit indicou que a revisão automática não ocorre neste repositório sem acionamento explícito; o status de check verde não foi tratado como revisão de código. Diff foi inspecionado manualmente.
- Escopo de observabilidade de feeds públicos/PAPER; sem credenciais, streams privados, ordens ou alteração de modo REAL. Não foram alegados testes locais no PC nem ligação real às exchanges.
- Próximo: continuar a pesquisa fundamentada em protocolos para recuperação de dados, começando por referências públicas como Freqtrade. Só implementar sequência/snapshot/checksum quando documentados pela exchange; nunca inferir lacunas a partir de IDs de trades. Registar evidência da fonte, adaptação própria, risco de licença/dependências e testes de aceitação. Uma PR de cada vez; manter execução REAL desativada.

### PR #424 — testes integrados do callback WebSocket (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/424, branch `test/radar-message-error-callbacks`, head `714985866b58311dfda68ef9f326f0f64ac5e86e`, base main `1c83dd9d70cbf030d03fdd3c252a2286e945554a` (merge #423).
- Acrescenta teste determinístico através do callback real de WebSocket para dois casos: JSON malformado e exceção do parser. Confirma incremento de `message_errors`, classe da exceção e ausência de texto bruto sensível no snapshot.
- Diff manualmente revisto; apenas `tests/test_websocket_radar.py` foi alterado. Sem reviews formais ou threads inline neste checkpoint.
- CI exato: Python workflow `39730475427` / #3028 ainda em execução, job `119664114132` a instalar dependências; suite pendente. Snyk success e CodeRabbit status success; Vercel pending. **Não fazer merge** até a suite e checks aplicáveis terminarem verdes no head exato e a alteração continuar correta.
- Testes apenas; sem ligação real a exchanges, credenciais, ordens ou alterações ao modo REAL. Nenhum teste local no PC foi alegado.

### PR #424 — testes integrados do callback WebSocket (merged, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/424 foi integrada por squash. Commit de merge: `996cc5486036a74ad9fdbb07678203077d7957b9`; head validado: `714985866b58311dfda68ef9f326f0f64ac5e86e`.
- Workflow Python run `39730475427` / #3028 concluiu com sucesso; job `119664114132`, incluindo a suite completa, passou no head exato. Statuses finais combinados: Snyk success, CodeRabbit status success e Vercel success.
- Diff de um único ficheiro `tests/test_websocket_radar.py`, revisto manualmente. Adiciona testes através do callback WebSocket real para JSON malformado e exceção do parser; verifica incremento de `message_errors`, classe de exceção e não exposição de texto sensível.
- Não foram encontrados reviews formais nem threads inline. O status verde de CodeRabbit não foi interpretado como review humano/formal.
- Testes de CI apenas; sem ligação real às exchanges, credenciais, ordens ou ativação de modo REAL. Não foram alegados testes locais no PC.
- Próximo: documentar padrões técnicos próprios a partir de leitura de referência Freqtrade, mantendo separação entre conhecimento geral e código de terceiros. Fontes lidas: https://github.com/AndreVazao/freqtrade/blob/main/freqtrade/exchange/exchange_ws.py e https://github.com/AndreVazao/freqtrade/blob/main/tests/exchange/test_exchange_ws.py. Padrões observados: loop asyncio dedicado e encerramento ordenado, lock para estado partilhado, tarefas por par/timeframe, timestamps distintos de pedido/refresh, cópia defensiva de caches, limpeza de cache após expiração/religação, verificação explícita de capacidade do exchange, fallback de unwatch e testes determinísticos com mocks. Estes são padrões arquiteturais observados, não autorização para copiar implementação. Adaptar apenas requisitos que façam sentido ao nosso feed de trades, com testes próprios, auditoria de licença/dependências e nenhum pressuposto de garantia de sequência sem documentação oficial da exchange.

### PR #425 — estudo documentado de padrões Freqtrade (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/425, branch `docs/radar-freqtrade-pattern-study`, head `fe3f4dddcd66ad99c8ea761365eaba36165fc9a1`, base main `996cc5486036a74ad9fdbb07678203077d7957b9` (merge #424).
- Alteração apenas documental em `docs/SOVEREIGN_MARKET_RADAR.md`: padrões observados em `freqtrade/exchange/exchange_ws.py` e `tests/exchange/test_exchange_ws.py`; adaptação arquitetural própria; limites de evidência para sequência/replay/recuperação; critérios de aceitação e nota de licença não confirmada no ficheiro LICENSE consultado. Sem código copiado ou dependências novas.
- Diff manualmente revisto. Sem reviews formais/threads inline no checkpoint. Não há workflow Python reportado para este commit; Vercel pending. **Não fazer merge enquanto checks aplicáveis estiverem pendentes**; voltar a verificar estado final e rever novamente antes de integrar.
- Nenhuma alteração de runtime, credenciais, ligação a exchanges, ordens ou modo REAL.

### PR #425 — estudo Freqtrade (merged, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/425 foi integrada por squash. Commit de merge: `136bebf837761fed108e6ee21bb46deacf20f8de`; head validado: `fe3f4dddcd66ad99c8ea761365eaba36165fc9a1`.
- Diff documental em `docs/SOVEREIGN_MARKET_RADAR.md`, revisto manualmente. Statuses finais do head: Snyk success, CodeRabbit status success, Vercel success. Não foi reportado workflow Python para este commit e não houve reviews formais/threads inline.
- Regista padrões observados na referência Freqtrade sem copiar código nem adicionar dependências, limites de evidência para recuperação de order book/trades e estado de licença não confirmado para reutilização direta.

### PR #426 — migração urgente do endpoint WebSocket OKX (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/426, branch `fix/okx-websocket-port-sunset`, head `e49b297e260680da23cc6bacfef43648a03c86d3`, base main `136bebf837761fed108e6ee21bb46deacf20f8de`.
- Fonte oficial OKX: https://my.okx.com/docs-v5/log_en/ (secção “WebSocket port 8443 discontinuation”, atualizada em 2026-10-16). Ligações WebSocket pela Internet pública à porta 8443 deixam de ser aceites em 2026-10-31; a documentação manda remover `:8443`, mantendo host/path e usando a porta TLS 443 por omissão. O SMR usava `wss://ws.okx.com:8443/ws/v5/public`; PR troca para `wss://ws.okx.com/ws/v5/public`.
- PR altera apenas o endpoint público, teste de regressão que fixa o endpoint, e documentação com a fonte oficial. Diff revisto manualmente. Sem reviews formais/threads inline.
- Estado CI no head exato: nenhum workflow Python reportado ainda; Snyk pending e Vercel pending. **Não fazer merge** até os checks aplicáveis concluírem e a suite Python passar no head exato. Não houve teste local no PC nem ligação real a OKX.
- Escopo público/observacional: sem credenciais, canais privados, ordens ou modo REAL. Próxima prioridade após esta PR: validar a mudança de endpoint e só depois investigar sincronização de order book com sequências oficiais (não usar IDs de trades como sequência).

### PR #426 — atualização de CI (2026-10-22)

- Head confirmado sem alterações: `e49b297e260680da23cc6bacfef43648a03c86d3`.
- Python workflow `39730964019` / #3029 em execução; job `119665657081` já concluiu instalação de dependências e está a executar a suite. Snyk success e CodeRabbit status success; Vercel pending.
- PR continua aberta e mergeable, mas não fazer merge até a suite Python e checks aplicáveis concluírem com sucesso no head exato.


### PR #426 — migração OKX para WebSocket TLS 443 (merged, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/426 foi integrada por squash no commit `6c30c89f5beda5333bf5d3ae06cbc16306779b24`; head validado: `e49b297e260680da23cc6bacfef43648a03c86d3`.
- Fonte oficial: https://my.okx.com/docs-v5/log_en/, aviso “WebSocket port 8443 discontinuation” atualizado em 2026-10-16: ligações públicas à porta 8443 deixam de ser aceites em 2026-10-31. O endpoint foi mudado de `wss://ws.okx.com:8443/ws/v5/public` para `wss://ws.okx.com/ws/v5/public`; teste de regressão fixa o endpoint e a documentação regista a justificação.
- Python workflow `39730964019` / #3029 e job `119665657081`: suite completa passou no head exato. Statuses combinados: Snyk success, CodeRabbit status success e Vercel success. Não houve reviews formais nem threads inline; o diff foi revisto manualmente. O status CodeRabbit não foi tratado como revisão manual independente.
- Só endpoint de feed público, teste e documentação. Não foram alegados testes no PC do proprietário nem ligação live a OKX; sem credenciais, canais privados, ordens ou execução REAL.
- Próximo: investigar sincronização e recuperação de order book com base nas regras oficiais de sequência/snapshot/checksum de cada exchange; nunca inferir gaps de IDs de trades. Continuar uma PR de cada vez e manter PAPER/observação.


### PR #427 — continuidade protocolar de order book (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/427, branch `docs/order-book-continuity-protocols`, head atual `e1bb9f9f651229efa98457f47de2ce73030f95bc`, base `main` em `6c30c89f5beda5333bf5d3ae06cbc16306779b24`. Compare confirma branch 2 commits ahead, 0 behind, só um ficheiro alterado: `docs/SOVEREIGN_MARKET_RADAR.md`.
- Documenta as regras oficiais de Binance Spot diff-depth + snapshot (`U/u`, `lastUpdateId`, sincronização inicial e gap/resync) e as notas oficiais OKX sobre `seqId/prevSeqId` e checksum descontinuado em canais específicos. Fontes incluídas na PR: https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#how-to-manage-a-local-order-book-correctly e https://app.okx.com/docs-v5/log_en/#2026-06-23.
- A documentação deixa explícito que o SMR atual continua a recolher trades públicos e ainda não tem order book local sincronizado. Define critérios de aceitação para futuro adapter: estados UNINITIALIZED/SYNCED/INVALID, freshness, buffer limitado, métricas, testes determinísticos e invalidar/resync em lacuna; sem orders/REAL.
- Diff documental revisto; corrigida formatação de inline code. Head final no checkpoint: Snyk success, CodeRabbit status success, Vercel pending; não existe workflow Python reportado para o commit documental. PR aberta, sem reviews formais nem threads inline. Aguardar Vercel terminar e confirmar metadata/checks antes de merge.
- Próximo passo após esta documentação: implementar camada de continuidade isolada e testável apenas depois de verificar os schemas atuais de cada canal. Não conectar ao cálculo de edge enquanto não estiver sincronizada/fresca; manter PAPER/observação.


### PR #427 — continuidade protocolar do order book (merged, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/427 integrada por squash no commit fd308be1c76825f20e34ca2db2a661362bfc9ae7; head validado e1bb9f9f651229efa98457f47de2ce73030f95bc.
- Documenta contratos de sequência/snapshot Binance Spot e notas OKX de sequência/checksum com critérios fail-closed. Vercel e Snyk success; CodeRabbit indicou que a revisão automática não corre neste repo sem acionamento. Não houve reviews formais; diff documental revisto manualmente.
- Não implementa order book local sincronizado. O SMR continua a recolher trades públicos; nenhum book pode alimentar edge até haver adapter, sincronização/freshness e testes.
- Revisão transversal encontrou endpoint OKX :8443 ainda presente no coletor secundário PC_ENGINE/market_events/websocket_collectors.py, usado por run_top_of_book_collector.py, apesar da migração do radar principal.

### PR #428 — migrar o coletor secundário OKX (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/428, branch fix/top-of-book-okx-port-443, head 17210a4523710818072426f6e016e146f8e35899, base main fd308be1c76825f20e34ca2db2a661362bfc9ae7.
- Atualiza PC_ENGINE/market_events/websocket_collectors.py para wss://ws.okx.com/ws/v5/public, adiciona teste test_default_okx_public_endpoint_uses_tls_443 em tests/test_websocket_collectors.py e documenta que a correção cobre a segunda via. Só feed público; sem credenciais/ordens/REAL.
- Workflow Python run 39732477590 / #3030, job 119670439529: instalação de dependências em curso e suite pendente no último checkpoint; Snyk e Vercel pendentes. CodeRabbit avisou que a revisão automática não corre sem trigger explícito. Não fazer merge até CI/checks aplicáveis passarem no head exato e diff ser revisto.
- Depois de #428, executar nova auditoria de integração com evidência por caminho: entrypoints/endpoints por exchange; market data → normalização/freshness → lead/lag → sinais → risk/authorization → order manager; persistência/restart/UNKNOWN_OUTCOME; transferências/accounting; health; cockpit/API/Android/remote; builds Windows/Android; CI e gaps. Classificar provado/parcial/falhado/não verificado, sempre com ficheiro, teste/workflow, SHA e ação seguinte. Manter PAPER/read-only e não certificar REAL sem provas completas.


### PR #428 — endpoint OKX corrigido nos dois coletores (merged, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/428 integrada por squash no commit 9cbf3bba6b234464578671ad0097ab401223e0f4; head validado 17210a4523710818072426f6e016e146f8e35899.
- Python workflow run 39732477590 / #3030 e job 119670439529 passaram, incluindo a suite completa, no head exato. Checks combinados finais: Snyk success, CodeRabbit status success e Vercel success. CodeRabbit comentou que revisão automática não é executada neste repositório sem trigger explícito; o check verde não foi tratado como review independente. Diff manualmente revisto; sem reviews formais.
- Corrigido o endpoint OKX na função default_public_configs de PC_ENGINE/market_events/websocket_collectors.py, consumida pelo run_top_of_book_collector.py. Teste novo test_default_okx_public_endpoint_uses_tls_443 em tests/test_websocket_collectors.py. A documentação regista a segunda via. Com #426 e #428, ambos os consumidores identificados usam wss://ws.okx.com/ws/v5/public; não foi provada conectividade live nem testado no PC.
- Próxima fase solicitada: nova auditoria de integração abrangente do Sovereign Trader, não só inventário de módulos. Cobrir caminhos de dados e execução, gates, persistência/restart, capital/transferências, ownership, APIs/cockpit/mobile/remote, endpoints duplicados por exchange, builds e CI. Para cada item classificar PROVADO/PARCIAL/FALHADO/NÃO VERIFICADO com ficheiro, teste/workflow e SHA. Reconfirmar o SHA atual de main antes da auditoria; manter PAPER/read-only e não certificar REAL sem provas completas.


### PR #429 — endpoint OKX do coletor L2 (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/429, branch fix/l2-okx-port-443, head 96df885caa2bcca6916e3c2883c3eab394740898, base main 9cbf3bba6b234464578671ad0097ab401223e0f4.
- Corrige o terceiro consumidor encontrado pela busca transversal: PC_ENGINE/market_events/l2_collectors.py, chamado por PC_ENGINE/tools/run_l2_market_data_collector.py. Acrescenta teste test_default_okx_l2_endpoint_uses_tls_443 em tests/test_l2_collectors.py e nota documental que separa migração de endpoint de sincronização do book.
- Workflow Python run 39732769193 / #3031, job 119671371199: instalação de dependências concluída; suite completa em execução no último checkpoint. Snyk success e CodeRabbit status success; Vercel ainda pending no status agregado (comentário do Vercel mais recente mostrava deployment Ready para outro status/deployment, verificar status agregado final). CodeRabbit declara que não faz review automático sem trigger explícito. Não fazer merge até suite/checks aplicáveis verdes no head exato e diff revisto.
- A auditoria de integração fica para depois de concluir esta PR. Escopo público, sem credenciais/ordens/REAL; nenhuma ligação live ou teste no PC alegado.


### PR #429 — migração OKX L2 para TLS 443 (merged, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/429 integrada por squash no commit 93b2559ef300bc1c0700eb9bca2c20fcb6d9af40; head validado 96df885caa2bcca6916e3c2883c3eab394740898.
- Python workflow run 39732769193 / #3031, job 119671371199, passou com sucesso, incluindo a suite completa no head exato. Statuses finais: Snyk success, CodeRabbit status success, Vercel success. CodeRabbit declarou que não executa review automático sem trigger explícito; o status verde não foi tratado como review independente. Diff manualmente revisto.
- Atualiza endpoint gerado por default_l2_configs em PC_ENGINE/market_events/l2_collectors.py e adiciona test_default_okx_l2_endpoint_uses_tls_443 em tests/test_l2_collectors.py. Em conjunto com #426 e #428, os três consumidores identificados (trade radar, top-of-book, L2) usam wss://ws.okx.com/ws/v5/public. Não foi validada conectividade live nem PC físico.
- Começar agora a auditoria de integração do main pós-#429, SHA 93b2559ef300bc1c0700eb9bca2c20fcb6d9af40. Resultado deve distinguir código existente de ligação real entre módulos e de validação operacional; documentar blockers e evidência exata. Manter PAPER/read-only e não certificar REAL.


### PR #430 — auditoria de integração de trading (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/430, branch audit/trading-integration-2026-10-22b, head be84db244a22312eb045c87486e4b42dc0141784, base main 93b2559ef300bc1c0700eb9bca2c20fcb6d9af40. Documento novo: docs/TRADING_INTEGRATION_AUDIT_2026-10-22.md.
- Auditoria estática abrange engine, market data/3 endpoints OKX, L2 continuity, exchange coverage, symbol equivalence, lead-lag, strategy/OOS, shared learning/Vercel, risk/execution, effective REAL config, order recovery, transfer/accounting, owner isolation, API/mobile/Tailscale, Windows EXE/APK, virtual office e CI evidence. Classifica cada área e enumera provas necessárias.
- Achados principais: as três configurações de WebSocket OKX verificadas usam agora wss://ws.okx.com/ws/v5/public após #426/#428/#429; coletor L2 ainda não equivale a livro local sincronizado; config.example.json inclui autonomous_execution enabled=true, allow_real=true, auto_promote_real=true e a configuração efetiva no PC deve ser inspecionada antes de qualquer uso real; shared_intelligence.sync_enabled está false no exemplo; PC/Android físico não foi validado.
- O documento é explícito: auditoria estática, não certificação de produção/REAL. Python full suite passou no head de #429 (run 39732769193, job 119671371199); não foi alegada ligação real a exchanges nem teste local.
- PR #430 é documental; Vercel está pendente no último checkpoint, nenhum workflow Python reportado. Sem reviews formais/threads; aguardar checks aplicáveis, rever diff e confirmar estado final antes de integrar.


### PR #430 — auditoria de integração integrada (2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/430 foi integrada por squash no commit dfa2ce2a5e2f4b1cc5cb855f37b7d8ccb2700926; head validado be84db244a22312eb045c87486e4b42dc0141784. Documento: docs/TRADING_INTEGRATION_AUDIT_2026-10-22.md.
- Checks finais no head: Snyk success, Vercel success, CodeRabbit status success. Não houve workflow Python (alteração documental); não houve reviews formais/threads inline. Diff de documento foi revisto manualmente. CodeRabbit informou que revisão automática não corre sem trigger explícito.
- A auditoria estática conclui: manter PAPER/read-only; não é certificação REAL. Principais blockers/parciais: order book L2 ainda não sincronizado/reconstruído (só parsing de eventos), cobertura nativa WebSocket de trades centrada em Binance/Coinbase/OKX, equivalência de instrumentos e edge OOS não demonstrados, config.example.json contém autonomous_execution enabled=true/allow_real=true/auto_promote_real=true e exige inspeção da configuração efetiva no PC, shared_intelligence.sync_enabled=false no exemplo, recuperação/side-effect paths precisam de prova end-to-end no SHA atual, Windows/Android físico não verificados.
- Migração OKX: após #426/#428/#429, os três consumidores identificados (PC_ENGINE/radar/websocket_radar.py, PC_ENGINE/market_events/websocket_collectors.py, PC_ENGINE/market_events/l2_collectors.py) usam wss://ws.okx.com/ws/v5/public e têm testes de endpoint em cada caminho. #428 full Python suite passed run 39732477590 / #3030; #429 full Python suite passed run 39732769193 / #3031; ambos com Snyk/Vercel success. Isto não prova conectividade live nem execução no PC.
- Próxima etapa recomendada: fechar primeiro P0 do relatório com uma auditoria técnica de caller paths e configuração efetiva, depois implementar state machine L2 de um canal/exchange com snapshots, sequência, gap/resync e testes, sem ligar depth a edge até sincronização/freshness provadas. Depois validar builds Windows/APK e smoke no PC/Android quando o utilizador estiver junto dos dispositivos. Não ativar REAL nem transferências sem autorização separada.


### Follow-up #431 — defaults REAL mais seguros (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/431, branch `safety/disable-real-promotion-example-defaults`, head `1e7b30b1bf076006cedc24e2d3d2192deaebe016`, base main `dfa2ce2a5e2f4b1cc5cb855f37b7d8ccb2700926`.
- A auditoria #430 identificou `autonomous_execution.allow_real=true` e `auto_promote_real=true` no config.example.json. PR #431 mantém `autonomous_execution.enabled=true` para continuar a investigação/autonomia PAPER, mas muda as duas flags REAL para false; acrescenta teste em `tests/test_fast_path_config.py` e atualiza a auditoria para distinguir exemplo de configuração privada efetiva.
- Snyk success. Vercel falhou apenas por limite diário de deploys da conta (não é falha de build/teste). CodeRabbit publicou aviso de que revisão automática não corre sem trigger explícito; estado verde não é review independente. Python workflow run `39735137739` / #3032, job `119678946482`: instalação terminou e suite ainda em execução no último checkpoint. Não fazer merge antes de a suite passar no head exato e revisão manual do diff.
- A alteração não toca em `config.local.json`, não prova a configuração efetiva do PC e não autoriza REAL. Depois, retomar a implementação de state machine L2 específica por protocolo; não ligar depth a sinais até snapshot/continuidade/freshness e resync serem comprovados.


### PR #431 — defaults REAL desativados no exemplo (merged, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/431 foi integrada por squash no commit `7a33a0177fdc7e370ea6a2bc1a5f84214d1cc71f`; head validado `1e7b30b1bf076006cedc24e2d3d2192deaebe016`.
- `PC_ENGINE/config/config.example.json`: mantém `autonomous_execution.enabled=true` para pesquisa/autonomia PAPER, mas muda `allow_real=false` e `auto_promote_real=false`. `tests/test_fast_path_config.py` acrescenta regressão. Auditoria `docs/TRADING_INTEGRATION_AUDIT_2026-10-22.md` atualizada para clarificar que config.local efetiva continua por verificar.
- Workflow Python #3032 / run `39735137739`, job `119678946482`: suite completa passou no head exato. Snyk success. Vercel falhou apenas por quota diária `api-deployments-free-per-day` (>100 deployments), sem indicação de falha de build/teste; CodeRabbit status success mas bot informou que não há revisão automática sem trigger explícito. Diff manualmente revisto; sem reviews formais.
- Limite: isto só melhora defaults para instalações que copiem o exemplo. Não altera config.local no PC e não é autorização nem certificação REAL.
- Próxima frente técnica: state machine L2 protocolar para um canal/exchange, com snapshot, sequência, invalidar/resync e freshness; não usar a saída atual do coletor L2 como livro sincronizado nem ligar a edge até os testes provarem continuidade. Depois fazer auditoria de integração pós-correções no SHA atual, incluindo caller graph de side effects, config efetiva (quando houver acesso ao PC), builds Windows/APK e testes de restart/reconciliation.


### PR #432 — state machine inicial para Binance Spot L2 (aberta, 2026-10-22)

- PR https://github.com/AndreVazao/VazaoSovereignTrader/pull/432, branch `feat/binance-spot-book-state-machine`, head `12dbb8da2db98ad9835c90da8b2fb9bf592e616d`, base main `7a33a0177fdc7e370ea6a2bc1a5f84214d1cc71f`.
- Acrescenta `PC_ENGINE/market_events/binance_book_state.py` e `tests/test_binance_book_state.py`: estados UNINITIALIZED/SYNCED/INVALID, instalação de snapshot fornecido pelo caller, validação de continuidade Binance `U/u`, ignora updates antigos/duplicados, remove níveis com quantidade zero, invalida/limpa livro em gap/níveis inválidos e expõe view elegível só quando recente.
- Documentação deixa explícito que não está ligado ao coletor/sinais: ainda faltam snapshot REST + buffering bounded/replay + reconnect/resync + telemetria; OKX books5 e Coinbase precisam de contratos próprios. Não usar JSONL L2 como livro sincronizado.
- CI Python run `39735346490` / #3033, job `119679614904`: dependências instaladas e suite completa em execução no último checkpoint. Snyk success. Vercel falhou por limite diário de deployments, não por teste/build; CodeRabbit status success mas avisou que review automático requer trigger. PR aberta, sem reviews formais/threads. Não fazer merge até suite passar no head exato e diff revisto manualmente.


### Update 2026-10-22 — auditoria e sincronização Binance

- PR #432 foi fechada sem merge porque a branch estava atrás de main; trabalho preservado numa branch nova.
- PR #433 https://github.com/AndreVazao/VazaoSovereignTrader/pull/433 foi merged como `c7dbb1dcceb48ea2a2546312ec3bf0b2fcedc622`. A state machine Binance Spot com estados UNINITIALIZED/SYNCED/INVALID, continuidade U/u, freshness e testes está em main.
- PR #434 https://github.com/AndreVazao/VazaoSovereignTrader/pull/434 em aberto, branch `feat/binance-spot-book-snapshot-replay`, head `e548c8d4131a13e774afdbef706c88a8437e0769`. Integra REST snapshot público, buffer bounded, replay, gap/overflow/disconnect invalidation, reconnect com backoff, rejeição de payloads inválidos, health JSON e saída sincronizada separada. O output sincronizado não alimenta sinais/ordens; OKX/Coinbase ainda são eventos brutos.
- Workflow Python #3043 / run `39739624702` está em execução no head exato acima. O run #3042 anterior teve suite completa a passar, mas não valida o último commit de backoff. Snyk e CodeRabbit verdes; Vercel falha por quota diária de deployments. Não mergear #434 até a suite do head atual passar e haver revisão manual.
- Atenção a follow-up: a health telemetry do sincronizador deve expor a frescura atual (age/eligible) para que consumidores não tratem o último JSONL histórico como sempre fresco.
- Escritório digital ainda protótipo: banner de ligação contraditório, mensagens demonstrativas, clicar em sala não inicia conversa isolada de departamento e não há E2E em browser/dispositivos. APK/Windows installer e smoke físico não verificados. Não instalar ainda; manter PAPER/read-only.


### Update 2026-10-22 — PR #434 merged; PR #435 office in validation

- PR #434 `feat(market-data): synchronize Binance Spot depth snapshots` foi merged por squash no commit `640a95ab2602b3d15862514bd0b84024b2d2d756`. Head validado `210cf2621f9db5ce3a9249845a0f81adb66d9186`; Python workflow #3047 / run `39739970324` passou suite completa no head exato, incluindo stale health. Snyk/CodeRabbit verdes; Vercel quota diária falhou. Output sincronizado continua desligado de sinais/execução.
- PR #435 https://github.com/AndreVazao/VazaoSovereignTrader/pull/435 em aberto, head `5fc3dcc79b24812663f6dbc304b21ad9109abb1d`, workflow Python #3048 / run `39740811008` em execução no último checkpoint. Corrige badge de ligação, estado desconhecido do motor, histórico por departamento na sessão do browser, contexto validado no `POST /assistant/message`, contexto de departamento na fila de investigação e resposta explícita `DEPARTMENT_NOT_CONNECTED` se não existe agente independente. Tests de gateway/API e docs adicionados.
- Não alegar que nove agentes estão prontos: esta PR só estabelece contexto e histórico em memória por sessão. Faltam agentes/worker independentes, histórico persistente no servidor e browser E2E. APK Windows/Android físicos continuam não verificados. Não instalar ainda; manter PAPER/read-only.


### Update 2026-10-22 — escritório: estado de ligação e contexto por departamento

- PR #435 https://github.com/AndreVazao/VazaoSovereignTrader/pull/435 foi merged por squash no commit `5e9c046a048757df79ab94639c13fa17792fdd83`. Python workflow #3048 / run `39740811008` passou suite completa no head exato `5fc3dcc79b24812663f6dbc304b21ad9109abb1d`; Snyk/CodeRabbit status success; Vercel quota diária falhou. Diff revisto manualmente, sem reviews formais/threads.
- Escritório: badge dinâmico de demonstração/autenticado/recusado/desligado; estado de motor desconhecido deixa de aparecer como OFF; mensagens de demonstração são limpas após autenticação; contexto de departamento é validado e enviado no POST autenticado; histórico separado por departamento é só em memória da sessão do browser; pedido de investigação carrega rótulo do departamento na fila comum.
- Limite explicitado no código e docs: ainda não existem nove agentes independentes; departamentos sem worker devolvem `DEPARTMENT_NOT_CONNECTED`. Próxima etapa é ligar handlers de leitura reais aos serviços existentes, depois histórico durável e browser E2E. Não declarar escritório pronto nem instalar ainda.


### Update 2026-10-22 — handlers de departamentos e diagnóstico mobile

- PR #436 `feat(office): connect departments to read-only runtime services` foi merged depois da suite Python passar no head exato `a1ec49b67b7de684bae575d628587721fc689668` (workflow #3053/run `39741857947`). Os departamentos agora têm handlers de leitura reais para venues, radar, pesquisa, PAPER, readiness, recuperação, ledger e intervenção humana. Continuam ferramentas determinísticas, não agentes autónomos.
- PR #437 https://github.com/AndreVazao/VazaoSovereignTrader/pull/437 em aberto, branch `fix/mobile-startup-diagnostics`, head `beb813dbbb8a2d865a8d7c7b5a956bba50fb9f7d`. Corrige o reparenting do status Label entre páginas Kivy, guarda a ScrollView de chat, adiciona fallback com diagnóstico local e retry para erros de construção do cockpit, e inclui testes de sintaxe/estrutura. O workflow Android #52/run `39742635169` passou os testes de startup e compileall; Buildozer continua a compilar APK no último checkpoint. Não mergear até concluir build; mesmo com APK compilado, falta launch físico/logcat no Android.
- Próxima prioridade após PR #437: testar o APK sem instalar como release; depois rever configuração local/escopos REAL e automatizar o smoke real do instalador Windows em PR. Não instalar no PC nem telefone até esses gates serem fechados. Manter PAPER/read-only.


### Update 2026-10-22 — PR #437 merged; Android APK build green, physical launch still blocked

- PR #437 foi merged por squash no commit `e6392ab9fec47ce51a7f2f029a15bc5b6990fe0a`. Workflow Android #52 / run `39742635169` passou no head `beb813dbbb8a2d865a8d7c7b5a956bba50fb9f7d`: startup contract tests, `compileall`, Buildozer debug APK build e upload do artifact passaram.
- Artifact GitHub Actions: `vazaosovereigntrader-android`, ID `12410422468`, 19,008,308 bytes, SHA-256 `d1f26069c00c6514a12735b84e590dc5500b85a362a17a4ef98cdc656fa62706`. É debug APK. Não houve launch físico nem logcat; a causa exata do crash reportado continua por confirmar. Fix concreto: status widget não é reparented entre headers; `app._chat_scroll` é mantido; falhas de construção do cockpit mostram ecrã de diagnóstico local/retry.
- PR #394 fechada como superseded, pois a semântica de latência desconhecida já está em main e coberta por testes. Neste checkpoint não há PRs abertas.
- Próximo: branch de release Windows para adicionar smoke real do instalador no PR workflow (install silencioso, arranque/health, uninstall) e retirar `trade_real` dos scopes de owner no config.example para novas instalações. Não assumir que isso altera `config.local.json` existente; a configuração efetiva do PC do utilizador ainda tem de ser revista localmente. Não instalar nem habilitar REAL até completar esses gates.


### Update 2026-10-22 — defaults PAPER-only and Windows installer smoke

- PR #439 https://github.com/AndreVazao/VazaoSovereignTrader/pull/439 merged: `trade_real` removed from `DEFAULT_OWNER_SCOPES`, because the example-profile hardening alone left a fallback that could grant REAL if an owner omitted `scopes` or supplied an empty list. Added tests for missing scopes, empty scopes, and explicit REAL scope. Exact-head Python workflow #3056 / run `39745332939` passed; focused PAPER lifecycle/safety workflow #22 / run `39745332867` passed. Snyk/CodeRabbit green; Vercel daily quota failure only. This still does not alter the existing PC `config.local.json`; explicit scopes may still grant REAL and must be inspected locally.
- PR #438 https://github.com/AndreVazao/VazaoSovereignTrader/pull/438 remains open: Windows EXE/installer CI now includes silent install, launch/health on loopback PAPER, stop/uninstall and scheduled-task cleanup checks. Manual diff review found a likely test blocker: the installer output name includes `-2026.10.1`, while the smoke test expected an unversioned filename. Fixed the smoke to require exactly one `VazaoSovereignTrader-Setup-*.exe` in commit `77ef30ce6e10324dad160e34123aff752aa951e7`. Python run #3057 / `39745494853` is in progress; Windows EXE run #751 / `39745494861` is pending at latest check. Do not merge #438 until both exact-head workflows pass.
- Current release blockers unchanged: actual effective PC config and Windows launch/firewall/token verification; Android physical launch/logcat; OKX/Coinbase protocol-specific synchronized books; edge-after-costs and order/reconciliation proof; office browser E2E and install packaging. Keep PAPER/read-only.


## Checkpoint 2026-10-22 — PR #438 Windows smoke merged; audit refreshed

- VazaoSovereignTrader main advanced to `5cd14a69d707e2cb935e7d9da621aa6888901068` via PR #438: https://github.com/AndreVazao/VazaoSovereignTrader/pull/438.
- Exact-head Python workflow run `39745494853` passed; Windows EXE workflow run `39745494861` passed both `build-exe` and `build-installer` jobs. Installer smoke includes silent install, installed files/config, both scheduled tasks, PAPER launch with loopback `/health`, process stop, silent uninstall and scheduled-task cleanup.
- This is hosted CI evidence only. It does not validate the user's actual Windows PC, effective private config, environment tokens, firewall, scheduled tasks or installed runtime.
- PR #439's identity defaults fix removes `trade_real` from `DEFAULT_OWNER_SCOPES`; PR #438 also removes the REAL scope from example owner profiles. Existing local configs/tokens were not changed or inspected.
- Integration audit update merged in PR #440: https://github.com/AndreVazao/VazaoSovereignTrader/pull/440. It records the current evidence and remaining acceptance gates.
- Binance Spot depth has snapshot + buffered diff replay, gap/overflow/disconnect invalidation, reconnect backoff and a separate synchronized-view artifact/health record. It remains observational and is not proven wired into edge scoring/execution. OKX/Coinbase synchronized L2, normalized cross-venue instrument equivalence and edge-after-cost proof remain incomplete.
- Physical Android launch/logcat, real PC validation, office browser E2E, independent department workers and LAN/Tailscale failover remain unverified.
- Posture remains PAPER/read-only; no REAL activation, live order, transfer or withdrawal performed.
- Next: inspect current Binance collector/state/tests and add deterministic contract coverage for failure/recovery; keep depth-based signals ineligible until the synchronized output is explicitly validated and wired.


## Update 2026-10-22 — Windows release smoke passed; Coinbase L2 parser hardened

- Product PR #438 merged: https://github.com/AndreVazao/VazaoSovereignTrader/pull/438. Exact-head Python workflow `39745494853` passed; Windows workflow `39745494861` passed for both EXE and installer, including silent install, loopback PAPER health check, process stop, silent uninstall and scheduled-task cleanup. This is hosted CI evidence only; actual PC config/runtime remains unverified.
- Installer smoke now discovers the versioned Inno Setup artifact and requires exactly one match. Example owner scopes are least privilege and example config keeps `allow_real=false`, `auto_promote_real=false`; PR #439 removes `trade_real` from `DEFAULT_OWNER_SCOPES`. Existing local config/tokens have not been inspected or changed.
- PR #442 merged: https://github.com/AndreVazao/VazaoSovereignTrader/pull/442. Coinbase Advanced Trade parser accepts `l2_data`, preserves/validates `sequence_num`, checks `product_id`, uses envelope timestamp fallback and rejects unknown event types. Exact-head Python run `39748485048` passed; Windows EXE/installer run `39748484977` passed; Snyk no manifest changes. Vercel deployment was blocked by daily quota, not test failure.
- PR #445 merged: https://github.com/AndreVazao/VazaoSovereignTrader/pull/445. Integration audit records latest Coinbase parser validation and explicit remaining blockers.
- Product main checkpoint at time of audit update: `918f94a7f911edba65e93cab00a02f400e992885`.
- Binance synchronized Spot book remains observational; invalidation state notifications are published, but live continuity and wiring to edge scoring/execution are not proven. Coinbase parser is not a synchronized Coinbase book. OKX/Coinbase synchronized depth, cross-venue instrument equivalence and net edge-after-cost proof remain incomplete.
- Virtual office: read-only department handlers exist, not independent autonomous chiefs; browser E2E, persistent per-department history, physical Android launch/logcat and Tailscale/LAN failover remain unverified.
- Posture remains PAPER/read-only. No live order, transfer, withdrawal, REAL activation or profitability claim.
- Next: review the live Binance collector/state/recovery path and deterministic tests; keep unsynchronized venues ineligible for depth signals; update the audit only with evidence. Device checks require access to the user's actual PC/phone.


## Update 2026-10-22 — PR #446 OKX books5 snapshot semantics (in progress)

- PR #446: https://github.com/AndreVazao/VazaoSovereignTrader/pull/446, branch `fix/okx-books5-snapshot-semantics`.
- Manual review found that the collector subscribes to OKX `books5` (full top-five snapshots) but classified payload action `update` as an incremental delta. Corrected `books5` and `bbo-tbt` to emit snapshot events on every push; incremental `books` remains action-based and unknown actions now fail closed.
- Added deterministic tests for a `books5` update being treated as a snapshot and for unknown OKX action rejection.
- Exact-head Python workflow #3060 / run `39753632745` passed. Windows EXE workflow #754 / run `39753632452`: EXE build/smoke passed; installer build still in progress at checkpoint, so PR must not merge until installer smoke finishes successfully.
- Official OKX documentation reference used: https://tr.okx.com/docs-v5/ — `books5` publishes full five-level snapshots on changes, unlike `books` incremental depth.
- This fixes event semantics only. It does not implement OKX synchronized-book continuity/recovery or enable depth signals. Keep PAPER/read-only.


## Update 2026-10-22 — Coinbase/OKX parsing and audit consolidation

- PR #442 merged: Coinbase Advanced Trade l2_data envelope parser preserves sequence_num, validates product_id, uses event/envelope timestamp fallback, and rejects unknown event types. This is parser hardening, not a synchronized Coinbase book.
- PR #446 merged as 38614b7573941166826e6249adc167883b8c9aa6: OKX books5 and bbo-tbt are treated as full snapshots even on action=update; incremental books retains action-based semantics. Python and Windows EXE workflows passed on exact head ead9c38e662daf42f647e765f077e139a3e600a8. Vercel deployment remained blocked by its 24-hour deployment quota; this is not a Python/Windows test failure.
- PR #438 Windows EXE/installer smoke passed on exact head 77ef30ce6e10324dad160e34123aff752aa951e7, including silent install, PAPER launch/loopback health, stop, uninstall and scheduled-task cleanup. This proves hosted Windows runner behavior only; the user's actual PC config and runtime remain unverified.
- PR #439 least-privilege default-scope fix merged; missing/empty owner scopes no longer default to trade_real. Existing local config and previously issued tokens were not inspected/revoked.
- Audit documentation PR #443 and subsequent #447 were closed unmerged after base/file conflicts. Replacement PR #448 is open: https://github.com/AndreVazao/VazaoSovereignTrader/pull/448. It consolidates current release/order-book evidence and acceptance gates; documentation only. Vercel deployment status is rate-limited, Snyk was pending at last check.
- Current main checkpoint after #446: 38614b7573941166826e6249adc167883b8c9aa6.
- Remaining blockers: prove synchronized Binance view is actually consumed by temporal-edge scoring; complete protocol-specific OKX/Coinbase synchronization and recovery; prove normalized instrument equivalence and net edge after all costs via chronological out-of-sample PAPER/shadow; verify actual PC config/runtime, physical Android APK and LAN/Tailscale transitions.
- Virtual-office department handlers are read-only service adapters, not independent autonomous LLM chiefs; browser E2E and persistent per-department conversations remain incomplete.
- PAPER/read-only only. No live orders, transfers, withdrawals, REAL activation, device smoke test, or profitability claim.


## Continuação — 2026-10-22 (PR #449 integrado; PR #450 em validação)

- Sovereign Trader main após PR #449: `52a0343872ce24873059ef508603b699089e57e7`.
- PR #449 merged: https://github.com/AndreVazao/VazaoSovereignTrader/pull/449. Corrigiu a ordenação do replay L2: reconstrução por ordem de chegada monotónica local, em vez de ordenar primeiro pelos relógios das exchanges; timestamps de exchange podem divergir e fabricar uma sequência causal falsa.
- O mesmo PR endureceu `OrderBookBuilder`: snapshots/deltas com níveis não finitos ou inválidos são rejeitados; deltas sem sequência deixam o livro inválido; o estado é limpo quando a continuidade não pode ser provada. Testes de regressão para skew temporal, níveis não finitos e sequência ausente foram adicionados.
- Python workflow #3069 / run `39755437777` passou no head exato `e213a387abc8b42b36ac7b7a48ec9c8b1c06acc1`. O status Vercel continuou rate-limited e não representa falha dos testes Python.
- PR #450 está aberto: https://github.com/AndreVazao/VazaoSovereignTrader/pull/450. Corrige mapeamento implícito de Coinbase: não tratar `BTC/USDT` como `BTC/USD`; pares Coinbase só são criados automaticamente quando a cotação é USD, e pares sem mapeamento seguro são reportados como não configurados.
- No head de PR #450 `00c2a0b98568b89997c194dc805cde78a9eaacd7`, Python passou (run `39755348462`); Windows EXE passou e o trabalho de construção/smoke do instalador ainda estava em execução na última verificação. Não fazer merge até confirmar o resultado final do instalador e rever a mergeabilidade contra main atualizada por #449.
- A análise L2 continua PAPER/read-only. Não há prova ainda de que os livros sincronizados estejam ligados ao cálculo de edge temporal nem de rentabilidade após custos; OKX/Coinbase não devem ser elegíveis para decisões baseadas em profundidade até terem sincronização/recuperação protocolar testada.
- PC real, configuração privada, APK físico e transições LAN/Tailscale continuam por validar. Nenhuma ordem real ou ativação REAL foi executada.


## Update 2026-10-22 — PR #450 Coinbase quote mapping guard (CI in progress)

- PR #450: https://github.com/AndreVazao/VazaoSovereignTrader/pull/450. Scope expanded to cover both the L2 collector and the trade WebSocket radar, because both previously built Coinbase product IDs from arbitrary configured quote assets.
- Default Coinbase subscription now applies only to USD-quoted symbols; BTC/USDT is not silently treated as BTC/USD. L2 startup/health output reports unconfigured symbol/venue pairs, and radar snapshots report unconfigured symbols by exchange.
- Exact latest-head Python workflow run 39755348462 passed on 00c2a0b98568b89997c194dc805cde78a9eaacd7. Windows EXE build/smoke job passed in run 39755348449; installer build was still in progress at last check, so PR #450 has NOT been merged.
- Snyk reported no manifest changes; Vercel deployment is blocked by the external daily deployment quota. Do not treat Vercel quota failure as a Python/Windows source-test failure.
- PR #448 audit consolidation merged as f271fcc077f148a28350f52e6f45d53942cdd55b. Audit now documents #438 Windows hosted smoke evidence, #439 least-privilege defaults, #442 Coinbase parser hardening, #446 OKX snapshot semantics and remaining blockers.
- Current main next priority after #450: correct the temporal-edge detector's gross-edge calculation so it measures the remaining leader/follower move gap rather than treating the leader's entire move as profit; add tests for current same-direction persistence and all-in costs. Keep it PAPER/shadow-only and separate from any order path.


## Update 2026-10-22 — PR #452 temporal edge correction (CI running)

- PR #452: https://github.com/AndreVazao/VazaoSovereignTrader/pull/452, branch `fix/radar-residual-temporal-edge`, head `49f569170f2fb17e8953f3e50116b15eb5b29ad4`.
- Found a substantive overstatement in `PC_ENGINE/radar/latency_edge.py`: `gross_edge_bps` used the leader's entire move even when the follower had already reflected most of it. It now computes only the unmatched same-direction movement: `max(0, abs(leader_move_bps) - abs(follower_move_bps))`; if directions differ, gross edge is zero.
- Removed duplicate receive-lag conditions and explicitly rejects negative leader lag. Added regression coverage for the overstatement example, a residual gap that remains positive after configured costs, and negative lead time.
- Exact-head GitHub Actions run `39756888433` had Windows EXE and installer jobs still in progress at last poll. Do not merge until Python suite and required build/smoke jobs are confirmed green; Vercel's deployment quota status is unrelated to Python correctness.
- This change is research/PAPER only. Net edge remains a cost-assumption heuristic, not evidence of realized profitability and not an order authorization. No REAL trading was enabled.


## Update 2026-10-22 — PR #452 merged; integration audit refreshed

- PR #452 merged as `072a2e67bc772f73ccc4f6aa4fe14a1f15d1b92c`. Exact-head Python run `39756888443` and Windows EXE workflow passed on head `49f569170f2fb17e8953f3e50116b15eb5b29ad4`.
- The residual temporal-edge correction prevents counting the leader's entire move as an opportunity after the follower has already caught up part-way. This is still a heuristic; no profitable edge or execution readiness is established.
- PR #438 Windows EXE/installer hosted smoke passed and was merged. It checks silent install, PAPER startup/loopback health, stop/uninstall and scheduled-task cleanup; actual home-PC configuration and runtime remain unverified.
- PR #439 removed `trade_real` from default owner scopes. Existing local configuration and already-issued tokens have not been inspected/revoked; don't infer they are safe from repository defaults alone.
- PR #442 merged Coinbase Advanced Trade `l2_data` envelope parsing, sequence preservation, product matching, timestamp fallback and parser regressions. Coinbase does not yet have a proven synchronized-book state machine.
- Binance has bounded buffering, REST snapshot/replay, gap/overflow/disconnect invalidation and stale-health tests. The production temporal-edge consumer wiring and decision-time freshness enforcement remain unproven. OKX/Coinbase depth synchronization and cross-venue normalized-cost edge validation remain blockers.
- Audit refresh is in PR #453: https://github.com/AndreVazao/VazaoSovereignTrader/pull/453. Documentation-only, open at checkpoint; Vercel is rate-limited by its daily deployment quota, and manual CodeRabbit review is not automatic. Do not treat either as a Python failure or as successful deployment/review.
- Readiness estimates in the audit are engineering judgments only: Windows EXE/installer 75% (hosted CI, not local PC); Binance synchronized L2 65% (consumer wiring remains a blocker); Coinbase L2 30%; OKX L2 25%; temporal edge after full costs 30%; virtual office 60%; Android APK 45%; remote LAN/Tailscale 50%; cross-PC learned knowledge 40%.
- Safety posture remains PAPER/read-only. No REAL orders, transfers, withdrawals, or REAL activation. Next work: confirm #453 checks and merge only after safe review; then trace Binance synchronized-book callback through production consumers and add explicit wiring/freshness tests before depth signals are eligible.
