# VazaoSovereignTrader — memória técnica persistente

Última atualização: 2026-05-04
Repo principal: `AndreVazao/VazaoSovereignTrader`
Tipo: sistema privado local-first para trading automatizado, PC + APK.
Estado: PC_ENGINE com módulos profissionais, dashboard local e scripts Windows; MOBILE_APP como cockpit.

---

## 1. Objetivo do projeto

Construir um sistema privado para o André usar pessoalmente, não para vender nem alugar.

Objetivo operacional:

- O PC fica como motor principal 24/7.
- O APK Android fica como cockpit simples.
- O utilizador deve apenas iniciar, pausar ou parar.
- O bot deve analisar o mercado, decidir onde alocar capital, executar em modo PAPER inicialmente, e só depois permitir REAL com cautela.
- Tudo deve correr localmente, sem cloud obrigatória.
- Sem automação de missões, quizzes, cupões, scraping, cliques ou ações internas de Binance/BingX que violem Termos de Uso.

Filosofia do projeto:

```text
Sobrevivência primeiro.
Risco controlado sempre.
Bot pensa, risk engine decide, executor age.
André controla START / PAUSE / PANIC.
```

---

## 2. Decisões de arquitetura já tomadas

### 2.1 PC como cérebro

O PC_ENGINE é o motor principal:

- roda 24/7;
- lê mercado via CCXT;
- calcula indicadores;
- decide sinais;
- faz alocação dinâmica;
- aplica risk engine;
- mantém ledger local;
- expõe uma API HTTP local para o APK e dashboard.

### 2.2 Mobile como cockpit

O APK não deve guardar chaves das exchanges.

O APK deve:

- mostrar estado;
- mostrar saldo/equity;
- mostrar P&L semanal e drawdown;
- mostrar scores dos ativos;
- enviar comandos locais ao PC: start, pause, stop;
- default em Português, com EN e ES preparados.

### 2.3 Tudo local-first

- PC e APK comunicam por rede local.
- Nada deve depender de servidor externo próprio.
- Internet é usada apenas para APIs oficiais de exchanges e dados de mercado.

### 2.4 TradingAgents

Foi analisado o ZIP `TradingAgents-main.zip`.

Conclusão:

- Tem interesse como futuro módulo de análise/aconselhamento no PC.
- Não deve ir para o APK por ser pesado.
- Não deve executar ordens.
- Deve entrar futuramente como `ai_council`, opcional e desligado por default.

Regra final:

```text
TradingAgents pensa.
Risk Engine decide.
Executor age.
```

---

## 3. Ativos e exchanges

Ativos default:

- `BTC/USDT`
- `ETH/USDT`
- `BNB/USDT`
- `SOL/USDT`
- `DOGE/USDT`

Exchanges pretendidas:

- Binance
- BingX

Regra APIs:

- Read ligado.
- Spot trading ligado.
- Withdraw desligado.
- Futures/leverage desligado na fase inicial.

---

## 4. Gestão de capital decidida

Opção escolhida:

```text
Pool único inteligente + limites duros por ativo.
```

O bot deve:

- ler saldo real quando em REAL;
- em PAPER usar saldo simulado;
- alocar capital conforme score dos ativos;
- respeitar exposição máxima global;
- respeitar máximo por ativo;
- reinvestir ganhos automaticamente;
- não retirar ganhos até o André decidir manualmente.

Limites exemplo:

- max open positions: 2
- max total exposure: 35%
- BTC max exposure: 25%
- ETH/BNB/SOL max exposure: 20%
- DOGE max exposure: 10%

---

## 5. Risk engine decidido

Regras atuais:

- Modo default: PAPER.
- Risco por trade: 0.5% (`0.005`).
- Drawdown diário máximo: -2%.
- Drawdown semanal máximo: -6%.
- Máximo de perdas seguidas por símbolo: 3.
- Cooldown após loss: 3600 segundos.
- Kill cooldown: 86400 segundos.

Regra de operação:

- Se o risk engine bloqueia, o bot não deve executar.
- Nenhum módulo de IA pode contornar o risk engine.
- O modo REAL não deve ser ativado com o motor a correr.

---

## 6. Estratégia base implementada

Arquivo principal: `PC_ENGINE/core/strategy.py`.

Estratégia: `TrendEmaAtrStrategy`.

Indicadores:

- EMA curta;
- EMA longa;
- ATR;
- VWAP;
- slope da EMA longa;
- spread guard.

Regimes:

- `TREND_UP`
- `TREND_DOWN`
- `RANGE`
- `CHAOS`
- `WARMUP`

Entrada BUY quando:

- EMA curta acima da longa;
- slope positivo suficiente;
- ATR percentual mínimo;
- preço acima da VWAP;
- spread aceitável.

Saída SELL quando:

- tendência enfraquece;
- EMA curta abaixo da longa;
- stop/take-profit do motor é atingido.

---

## 7. Estado atual da repo principal

Estrutura relevante:

```text
VazaoSovereignTrader/
├── PC_ENGINE/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── server.py
│   │   └── dashboard.py
│   ├── config/config.example.json
│   ├── core/
│   │   ├── allocator.py
│   │   ├── config.py
│   │   ├── engine.py
│   │   ├── indicators.py
│   │   ├── risk.py
│   │   ├── strategy.py
│   │   ├── exchange_rules.py
│   │   ├── paper_broker.py
│   │   ├── order_manager.py
│   │   ├── preflight.py
│   │   └── recovery.py
│   ├── exchanges/
│   │   ├── base.py
│   │   └── ccxt_client.py
│   ├── storage/ledger.py
│   ├── services/watchdog.py
│   ├── backtest/replay.py
│   ├── tools/run_backtest.py
│   ├── reports/weekly_report.py
│   ├── learning/champion_challenger.py
│   └── ai_council/
│       ├── decision_mapper.py
│       └── stub.py
├── MOBILE_APP/
│   ├── main.py
│   ├── buildozer.spec
│   └── lang/
├── scripts/
│   ├── windows_setup.bat
│   ├── windows_run_pc_engine.bat
│   └── windows_backtest_btc.bat
├── shared/schemas.py
└── docs/
    ├── BUILD_PC.md
    ├── BUILD_MOBILE.md
    ├── SECURITY.md
    ├── TRADINGAGENTS_INTEGRATION.md
    ├── PROFESSIONAL_MODULES.md
    └── QUICKSTART_WINDOWS.md
```

---

## 8. Melhorias profissionais implementadas em 2026-05-04

Foram adicionadas e integradas melhorias críticas:

- Pre-flight checker.
- Exchange Rules Engine.
- Paper Broker realista.
- Order Manager.
- Recovery Manager.
- Watchdog.
- Replay Backtester.
- Weekly Reporter.
- Champion / Challenger.
- AI Council stub.

Documentação: `docs/PROFESSIONAL_MODULES.md`.

---

## 9. Melhorias adicionais implementadas na ronda seguinte

Foram adicionadas melhorias para usabilidade e teste local em Windows:

### 9.1 Arranque Windows mais robusto

`PC_ENGINE/main.py` agora corrige `sys.path` para permitir correr:

```text
python PC_ENGINE/main.py
```

ou:

```text
cd PC_ENGINE
python main.py
```

Também foi criado `PC_ENGINE/__init__.py`.

### 9.2 Dashboard local no browser

Arquivos:

- `PC_ENGINE/api/dashboard.py`
- `PC_ENGINE/api/server.py`

Endpoint:

```text
http://127.0.0.1:8765/dashboard
```

O dashboard mostra:

- status;
- modo PAPER/REAL;
- saldo/equity;
- P&L diário/semanal;
- drawdown;
- watchdog;
- champion/challenger;
- scores por ativo;
- posições abertas;
- logs.

Botões:

- INICIAR;
- PAUSAR;
- PARAR;
- PAPER;
- REAL;
- PREFLIGHT.

### 9.3 Endpoint de preflight

Foi adicionado:

```text
POST /preflight
```

### 9.4 Scripts Windows

Foram criados:

```text
scripts/windows_setup.bat
scripts/windows_run_pc_engine.bat
scripts/windows_backtest_btc.bat
```

### 9.5 Backtest CLI

Arquivo:

```text
PC_ENGINE/tools/run_backtest.py
```

Permite correr replay/backtest com candles públicos da Binance:

```powershell
python PC_ENGINE\tools\run_backtest.py --exchange binance --symbol BTC/USDT --limit 500
```

### 9.6 Quickstart Windows

Arquivo criado:

```text
docs/QUICKSTART_WINDOWS.md
```

---

## 10. Segurança GitHub

Nunca subir:

- chaves Binance/BingX;
- token local do PC;
- keystore Android;
- logs reais;
- histórico real com dados sensíveis.

---

## 11. Como arrancar agora no Windows 10

Na raiz da repo:

```text
scripts/windows_setup.bat
scripts/windows_run_pc_engine.bat
```

Depois abrir:

```text
http://127.0.0.1:8765/dashboard
```

Backtest rápido BTC:

```text
scripts/windows_backtest_btc.bat
```

---

## 12. Próximos passos recomendados

1. Fazer `git pull` no PC.
2. Correr `scripts/windows_setup.bat`.
3. Correr `scripts/windows_run_pc_engine.bat`.
4. Abrir dashboard local.
5. Executar PREFLIGHT.
6. Testar backtest BTC.
7. Corrigir eventuais erros locais.
8. Rodar PAPER por 14 dias.
9. Só depois preparar confirmação dupla para REAL.
10. Futuramente melhorar pairing APK-PC com QR Code.
11. Futuramente adicionar `ai_council` real baseado no TradingAgents.

---

## 13. Binance / conta real

ChatGPT não tem acesso direto à conta privada Binance do André.

O sistema só poderá ler saldo privado quando:

- André criar API key na Binance;
- configurar a key localmente no PC por variáveis de ambiente;
- permissão Read/Spot Trade estiver ativa;
- Withdraw estiver desligado;
- o PC_ENGINE estiver a correr localmente.

Até lá, só é possível consultar dados públicos de mercado, não saldo/conta.

---

## 14. Frase-guia do projeto

```text
O bot é soberano, local e disciplinado.
Não procura magia.
Procura sobreviver, aprender e crescer com risco controlado.
```


## Current engineering checkpoint — 2026-10-23

Latest reviewed product main: `d1a84642b0f503252e6d0df967d8cda2ba06ad0c`. Coinbase parser contract was corrected (#442), monotonic clock regression now fails closed (#477), and malformed depth messages immediately invalidate synchronized book state (#475). Integration audit was updated in #478. Exact-head Python suites for #475 and #477 passed. These changes improve fail-closed behavior but do not prove live-feed correctness or a tradeable temporal edge. Keep cross-venue depth-based signals PAPER/observation-only until protocol-specific gap/reconnect recovery, normalized instrument identity, and edge-after-costs are validated. Actual PC and physical Android tests remain pending.


---

## Checkpoint de continuidade — 2026-10-28 08:00 UTC — PR #504

### Estado GitHub verificado

- Repositório: `AndreVazao/VazaoSovereignTrader`.
- PR #504: https://github.com/AndreVazao/VazaoSovereignTrader/pull/504 — permanece OPEN, não fazer merge enquanto os gates de segurança estiverem incompletos.
- Branch única ativa: `work/cross-org-learning-provenance-2026-10-27`.
- HEAD verificado: `434f37e05721311b3ad4f9a01072403f7778ad03`.
- Commit mais recente observado: `test(security): exercise actual unpaired Unicode surrogates`.
- GitHub Actions do HEAD: os checks `Python tests` e `Shared Learning validate` aparecem como SUCCESS. Snyk reportou “4 security tests have passed”; Vercel reportou deployment concluído. Não há confirmação neste checkpoint de Windows EXE, Windows installer e PAPER smoke no SHA exato; não declarar todos os workflows verdes sem os verificar.
- O corpo da PR foi atualizado para documentar canonicalização compatível com RFC 8785/JCS, vetores partilhados TypeScript/Python e um vetor fixo Ed25519 verificado nos dois runtimes. Isto é o que o estado remoto declara; confirmar o conteúdo e os resultados exatos antes de ativar assinatura Python.

### Progresso recente da canonicalização

A branch recebeu trabalho adicional após o SHA antigo `639fc441...`. A descrição atual da PR informa:
- canonicalização de payload compatível com RFC 8785/JCS em TypeScript e Python;
- vetores de canonicalização partilhados;
- cobertura da ordenação de chaves por unidades UTF-16;
- vetor fixo de mensagem/assinatura Ed25519;
- correções após testes detetarem PEM mal formatado, representação de `1e20` no fixture e teste de surrogate Unicode que inicialmente não criava o caractere inválido real.

**Não assumir que isto está pronto para produção.** Os testes do HEAD exato e a cobertura completa precisam de ser revistos; assinatura Python e integração do adaptador continuam explicitamente desativadas/não integradas.

### Bloqueios e sequência seguinte

1. Obter o conteúdo do HEAD `434f37e05721311b3ad4f9a01072403f7778ad03` para `cloud/shared-learning/lib/provenance.ts`, testes TypeScript, canonicalização Python, fixtures partilhados e workflow. Rever se os vetores correspondem realmente ao RFC 8785/JCS e se os digests foram calculados de forma independente.
2. Confirmar no SHA exato os resultados de Python tests, Shared Learning tests/TypeScript/build, Windows EXE, Windows installer, PAPER smoke, Snyk e Vercel. Resolver falhas antes de qualquer merge.
3. Manter Python signing e consumo do endpoint de proveniência verificada desligados até os testes cruzados de assinatura passarem no HEAD final.
4. Construir testes com base de dados descartável para migrações Supabase, RLS, chaves imutáveis, RPC atómica e linhagem. Não aplicar migrações experimentais à produção.
5. Definir o processo confiável de enrollment/aprovação/revogação/rotação de instalações e chaves.
6. Confirmar explicitamente a política de visibilidade cross-organization e manter testes DB de linhagem.
7. Integrar a memória local no runtime; testar concorrência, reinício, persistência e recuperação.
8. Atualizar `docs/PROJECT_CONTEXT.md` no repositório principal e esta memória após avanços comprovados.

### Regras invariáveis

- Manter foco no cérebro do Sovereign Trader; não desviar para DGM-MAT ou UI/3D/APK enquanto os gates do cérebro estiverem abertos.
- PAPER/read-only apenas. Sem ordens reais, transferências, levantamentos, provisionamento pago, migrações de produção ou ativação de sincronização produtiva.
- Cérebro independente da UI e da cloud; memória local interdepartamental não depende de Vercel.
- Aprendizagem partilhada não pode transmitir credenciais, saldos, memória privada, ordens nem autoridade de execução.
- Uma só branch de trabalho ativa; PR pequena e sem merge antes de verificações obrigatórias verdes e bloqueios resolvidos.


---

## Checkpoint de continuidade — 2026-11-08 15:28 UTC — VST PR #549 integrada

### Estado GitHub verificado
- PR #549: https://github.com/AndreVazao/VazaoSovereignTrader/pull/549 — CLOSED e MERGED.
- HEAD validado por CI: `c27c666eee4b4edd51d57183b616ec7f485b88fa`.
- Merge squash e novo `main`: `8a339f8029fba3824c963664dc8dd3654aa9c0d6`.
- Estado da PR e SHA de `main` confirmados após o merge.

### Validação no SHA exato
- Python tests: SUCCESS.
- PAPER lifecycle and safety boundaries: SUCCESS.
- Windows EXE: SUCCESS, incluindo amostragem adaptativa Windows, build e smoke test.
- Windows installer: SUCCESS, incluindo instalação, atualização, lançamento, health check, desinstalação e preservação do Learning Vault.
- CodeRabbit foi SKIPPED por exigir revisão manual; não é teste funcional.
- Snyk free quota esgotada e explicitamente excluída dos bloqueios pelo utilizador.
- Vercel Preview não é considerado teste de código.

### Alterações integradas
PR #549 adicionou orçamento adaptativo independente para análise offline PAPER, através de `max_analysis_workers` e `run_adaptive_analysis`, nos entry points:
- `PC_ENGINE/tools/run_lead_lag_validation.py`
- `PC_ENGINE/tools/run_regime_validation.py`
- `PC_ENGINE/tools/run_readiness_pipeline.py`

Os testes confirmam que hosts COMPACT/sem orçamento adiam análise antes de construir validadores ou carregar histórico pesado; o readiness pipeline preserva relatórios anteriores; falhas de amostragem/configuração são fail-closed. Não altera risco, modo PAPER/REAL, permissões REAL, ordens, recolha contínua de Market Data, Radar ou persistência PAPER.

### Branches VST observadas após merge
- `main`: `8a339f8029fba3824c963664dc8dd3654aa9c0d6`.
- `docs/recover-historical-work-2026-11-08`: documentação integrada via PR #548; candidata a eliminação pelo utilizador.
- `fix/adaptive-analysis-entrypoints-2026-11-08`: integrada via PR #549; candidata a eliminação pelo utilizador.
- `work/mobile-virtual-office-demo-2026-10-28`: antiga, divergente e obsoleta; não fazer merge integral. Confirmar commits isolados antes de o utilizador a eliminar.
- Nenhuma branch foi apagada.

### Próxima prioridade
1. Reduzir pressão de memória em PCs COMPACT preservando Market Data público, Radar observacional, PAPER bookkeeping, persistência e health telemetry.
2. Auditar leituras históricas restantes que possam carregar datasets inteiros antes da admissão adaptativa; preferir streaming/chunking e limites explícitos.
3. Melhorar diagnósticos de adiamento sem interromper trabalhos em curso.
4. Preparar teste físico focado no PC antigo: instalação, health/status, bootstrap público Market Data e Radar; medir memória e validar artefactos READY.
5. Não declarar a cadeia Market Data → validação → Radar → estratégias → risk → PAPER → telemetry certificada sem evidência end-to-end.
6. Manter backend/cérebro como prioridade; UI/3D/APK secundária.

### Regras invariáveis
- PAPER/read-only apenas; sem ordens reais, transferências, levantamentos, credenciais REAL ou auto-promoção REAL.
- Adaptação de recursos altera apenas orçamento computacional, nunca permissões, limites de risco ou modo.
- Não terminar processos nem fechar aplicações no PC sem autorização explícita.
- Uma branch ativa e uma PR de avanço de cada vez; não editar `main` diretamente.
- Não fazer merge sem workflows aplicáveis verdes no SHA exato.
- Não bloquear progresso por Snyk free quota ou Vercel preview.


## 2026-11-09 — PR #551 merged and physical Windows reinstall audit

- PR #551 was merged to VST main; validated main SHA: `59436c47ed3fdfb79e5de184f11596a0e8b48a8b`.
- CI evidence: Python 1,379 passed + 96 subtests; PAPER safety workflow PASS; Windows EXE build PASS; installer lifecycle (install/upgrade/health/uninstall and Vault marker preservation) PASS.
- Physical PC: Windows 10 build 19045, Python 3.12.6, approximately 3 GB RAM; disk C had 722.67 GB free at final sample.
- Fresh installation: installer `2026.11.1` installed. No prior registered Inno Setup installation was found, so this was a fresh app install; source checkout and pre-existing untracked files were preserved. Artifact ZIP SHA-256: `a6201768565141dab7bb7596b00c6437af0b83696a59a802f73db3f5dc2b01f1`; installer EXE SHA-256: `602AAEEE2C68E2408636BB61B05AF5CC3A54921A81C77CB453EDD8086DF58C64`.
- Windows verification: `verify_pc_install.ps1` PASS; 249 first-party Python modules compiled; `pip check` PASS; 22 focused local tests PASS (identity/auth, compile, installer safety, Desktop PAPER surface).
- Runtime security remained PAPER; API bound to `127.0.0.1:8765`; `allow_real=false`; `auto_promote_real=false`; REAL scope removed; no private exchange keys, private balance probes, orders, transfers, scheduled tasks or auto-start.
- API: `/health`, authenticated `/status`, and `/learning-memory/health` returned HTTP 200/HEALTHY.
- Learning Vault correction: actual Vault is under per-user LOCALAPPDATA, not `PC_ENGINE/data`. Separate backup at `C:\\VST_Backups\\pre-reinstall-20261109\\default-vault`, 13 files, SHA-256 manifest verified. SQLite `integrity_check=ok`; current `learning_records=0`, `learning_events=0`; isolated-copy write/read/reopen PASS. Original Vault was not overwritten.
- Public bootstrap: READY under configured minimum-venue policy, 4/5 venues and 22 symbols. Binance, BingX and OKX 5/5; Bybit OHLCV passed but ticker `timestamp_ms` missing for 5/5 symbols; Coinbase 2/5 (BNB/USDT unsupported; DOGE 2 candles; SOL 14). Do not call all-exchange Radar ready.
- Live collector proof: installed WebSocket collector ran in PAPER/public-only mode; Binance and OKX connected for BTC/USDT and ETH/USDT. Integrated PAPER smoke saw 3,662 Binance events and 117 OKX events, zero message errors, `market_data.ok=true`, health RUNNING/non-stale.
- Runtime PC profile: WebSocket collector uses Binance + OKX; REST/bootstrap profile includes Binance + BingX + OKX. Bybit and Coinbase remain excluded until data-quality fixes.
- Shutdown limitation: API stop returned success, but engine status remained STOPPING after 30 seconds even though the paper collector reported `running=false` and no active workers were reported. Collector Ctrl+C did not terminate its PyInstaller child. Only audit-owned process trees were cleaned; final verification showed zero VST processes and zero listeners on port 8765.
- Final report status: PARTIAL, not 24/7 ready. Full Python suite, endurance, 24/7/autostart and complete strategy-to-risk-to-learning pipeline were intentionally skipped on the low-RAM PC.
- Local audit branch: `audit/windows-reinstall-2026-11-09`; no tracked source changes committed. Temporary audit scripts removed. Existing untracked `artifacts/` and `bash.exe.stackdump` preserved.
- Next fixes: (1) engine stop lifecycle must settle STOPPING→OFF after producers exit; (2) Market Data collector PyInstaller child must shut down cleanly on Ctrl+C; (3) Bybit ticker timestamp quality gate; (4) Coinbase symbol mapping and bounded OHLCV backfill; (5) integrated Windows test for backend+collector start/stop/restart. Keep REAL and 24/7 disabled.


---

## Checkpoint de continuidade — 2026-11-11 — PR #562 integrada

### Estado GitHub verificado
- PR #562: https://github.com/AndreVazao/VazaoSovereignTrader/pull/562 — CLOSED e MERGED.
- HEAD validado por CI: `15b6c5474c4a967cec349568162b0d4f02e36cda`.
- Merge squash SHA e novo `main`: `67d4d6a8943be984980c68aa2dfc137de2d4535c`.
- PR marcada ready antes do merge; merge executado com expected_head_sha para impedir integração se a branch tivesse mudado.
- Após merge, PR e ref `main` foram consultadas novamente e confirmadas.

### CI no HEAD exato
- Python tests: SUCCESS — run 43063754581.
- Trading engine PAPER smoke: SUCCESS — run 43063754596.
- Windows EXE: SUCCESS — run 43063754701; build e smoke, validação PowerShell 5.1 e constrained-memory resource policy passaram.
- Windows installer: SUCCESS no mesmo run; build previous-version, upgrade e lifecycle smoke (install, upgrade, launch, health, uninstall, Learning Vault preservation) passaram.
- Nenhum review ou review thread pendente.

### Alterações integradas
- `PaperMarketCollector` partilha o `AdaptiveResourceManager` do motor e atualiza a política por ciclos.
- Perfil COMPACT preserva recolha pública, bookkeeping PAPER e persistência durável, adiando tarefas opcionais pesadas e ajustando cadência.
- Falha/degradação da sondagem de recursos usa fallback conservador COMPACT.
- Diagnóstico autenticado `GET /paper-collector/resources`, protegido por `read_private_state`, expõe snapshot/política/cadência/estado de shutdown sem divulgar learning paths.
- Testes cobrem recursos degradados, adiamento de tarefas pesadas, API autenticada e invariantes PAPER-only.
- Safety: sem alteração de permissões, risco, modo, autoridade de ordens ou execução REAL; sem force-kill ou fecho prematuro do store.

### Estado de Issue #560
- Continua OPEN deliberadamente.
- O reteste de ciclo de vida no PC físico continua pendente. CI Windows não substitui o teste no PC antigo.
- Não houve acesso nem alteração ao PC físico nesta ronda.
- Próximo passo operacional: obter autorização explícita para inventário read-only + backup verificável SHA-256 de checkout/config/Learning Vault/artifacts/untracked; só depois executar instalação e lifecycle retest no PC.

### Estado do repositório após integração
- Main: `67d4d6a8943be984980c68aa2dfc137de2d4535c`.
- Pesquisa de PRs abertas devolveu zero PRs abertas nesse momento.
- Manter PAPER/read-only, uma branch/PR ativa de cada vez, sem trabalho visual do cockpit até backend validado localmente.
- Snyk continua excluído por limite do plano free; Vercel previews não são testes de código.


## 2026-11-11 — PR #563 merged: local Windows validation prompt refreshed

- PR #563: https://github.com/AndreVazao/VazaoSovereignTrader/pull/563 — CLOSED/MERGED.
- Merge SHA and VST `main` after verification: `5f73a6d13af42186a2ffade05511fc97d835a8e7`.
- Documentation-only change; no CI workflows were triggered for the docs path. PR was mergeable and merged with expected head SHA `86ebe520d2fd7fa5605fda2404827cad5cd129b8`.
- Updated `prompts/PROMPT_MASTER_LOCAL_WINDOWS_BACKEND_E2E.md`: removed stale PR #522/branch pin; local validation now targets exact current main SHA and matching CI/artifacts; requires verified SHA-256 backup of checkout + untracked state, sanitized config, active/legacy Learning Vault, artifacts and runtime evidence before any state-changing PC test; added guidance for authenticated `GET /paper-collector/resources` and PAPER-only invariants.
- This does not validate the physical PC. No PC access or state changes occurred.
- Current VST main: `5f73a6d13af42186a2ffade05511fc97d835a8e7`. No open VST PR was present immediately before PR #563; PR #563 is now merged.
- Next blocker remains physical target-PC lifecycle retest. Obtain explicit owner authorization for read-only inventory and verified backup before installing/upgrading or starting/stopping anything. Keep Issue #560 open until that evidence is complete.


## 2026-11-12 — VST PR #564 merged and Android emulator UI smoke recovered

- PR #564 https://github.com/AndreVazao/VazaoSovereignTrader/pull/564 CLOSED/MERGED; tested HEAD d7c3d4c38eadb746555c84ca4e5731d1f856e383; squash merge and verified main SHA 8414091f475c726b8cde720b7e9efcc9573141a1.
- Exact HEAD CI all PASS: Python run 43181588502; PAPER smoke 43181588435; Android Emulator UI Smoke 43181588546; Windows EXE + installer lifecycle 43181588446; Android APK 43181588492.
- Windows EXE job ran Validate native DPAPI CurrentUser credential vault successfully. Installer lifecycle passed previous-version, upgrade, install, launch, health, uninstall and Learning Vault preservation.
- Android artifact vst-android-emulator-smoke ID 13927602112 inspected. OCR confirmed first-run chooser and office screen; orientation evidence PASS for portrait, landscape and tablet landscape. The UI explicitly labels the office DEMO OFFLINE — ESCRITÓRIO SEM MOTOR; CI proves offline visual launch/orientation only, not live backend connection or physical-device behavior.
- PR adds initial Windows DPAPI CurrentUser vault foundation (Binance/OKX; not yet wired into runtime/API), public Radar collection metrics and authenticated /paper-collector/resources, Android Radar + PAPER evidence scorecard, and roadmap. No exchange account registration/permission-verification/revocation API, no PC form, no live private account reads, no REAL authority.
- No PC physical runtime actions, installation, upgrade, engine start/stop or exchange credentials. Remain PAPER-only and public-data-only.
- Next engineering increment: inspect existing CCXT construction and API scopes, then implement explicit read-only Binance/OKX capability boundary and owner-only credential registration/verification/status/revocation with DPAPI storage, no-store/redaction, bounded requests and negative permission tests. Never request secrets in chat/mobile. Keep PC lifecycle test gated by read-only inventory + verified SHA256 backup and separate authorization for state changes.


## 2026-11-12 — Universal platform coverage and Android virtualization requirement

- PR #565 merged into VST main as `09b803a2ce0bba10de895b800fd8950a60e739a1`. Its exact HEAD `bb9792b252bdd10396560b046edcc4f64c3b8fcd` passed Python tests (run 43205252171), PAPER lifecycle/safety (43205226035), Windows EXE and installer jobs (43205252789). Duplicate earlier runs were cancelled; final reruns passed.
- PR #566 opened: https://github.com/AndreVazao/VazaoSovereignTrader/pull/566; branch `feat/universal-platform-android-virtualization-2026-11-12`. Documentation architecture defines provider-neutral integrations and Android virtualization; check live PR state/head before claiming merge.
- User clarified VST must not be limited to Binance/OKX. Treat them as first examples only. Build universal connector catalogue for exchanges, brokers, fintech/banking (including U-Hodler as candidate), wallets, payments, portfolio apps, Android apps, web/desktop apps and cloud services. Each adapter declares explicit capabilities, access method, permissions, health/freshness, limits and evidence; unknown operations fail closed.
- Android virtualisation must support local emulators, self-hosted farms and optional cloud providers behind one orchestrator. No mandatory provider or paid cloud. Cloud sessions need isolation, encrypted streaming, short-lived auth, private device control (no public ADB), cost/runtime caps, region/retention controls, revocation and evidence redaction.
- Prefer official APIs/OAuth/SDK. UI automation only as authorized fallback; stop on uncertainty and require owner handoff for MFA/OTP/CAPTCHA/biometrics/consent/payment/security prompts. Never bypass safeguards or perform unattended financial mutations.
- U-Hodler and other named apps are candidates, not implemented connectors. No cloud provider provisioned, no cost incurred, no app credentials used, no PC physical runtime changes. Continue PAPER-only and no REAL authority.
- Next: inventory connector construction and Android automation contracts; define typed provider-neutral manifest/capability registry and fake adapter tests; prototype local Android session provider; compare cloud providers before any provisioning.
