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
