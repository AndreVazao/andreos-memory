# VazaoSovereignTrader — memória técnica persistente

Última atualização: 2026-05-04
Repo principal: `AndreVazao/VazaoSovereignTrader`
Tipo: sistema privado local-first para trading automatizado, PC + APK.
Estado: base inicial criada na repo principal, com PC_ENGINE funcional em PAPER e MOBILE_APP como cockpit.

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
- expõe uma API HTTP local para o APK.

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

### Ativos default confirmados

Modo equilibrado, 5 ativos ativos por defeito:

- `BTC/USDT`
- `ETH/USDT`
- `BNB/USDT`
- `SOL/USDT`
- `DOGE/USDT`

Racional:

- BTC é âncora de mercado e sensor de regime.
- ETH é beta principal e líquido.
- BNB é controlado e líquido.
- SOL dá momentum.
- DOGE é volátil e deve ter limite menor.

### Exchanges pretendidas

- Binance
- BingX

Preparado via CCXT.

Regra obrigatória das APIs:

- Read ligado.
- Spot trading ligado.
- Withdraw desligado.
- Futures/leverage desligado na fase inicial.

---

## 4. Gestão de capital decidida

Foi escolhida a opção:

```text
Pool único inteligente + limites duros por ativo.
```

Não será divisão fixa pura.

O bot deve:

- ler saldo real quando em REAL;
- em PAPER usar saldo simulado;
- alocar capital conforme score dos ativos;
- respeitar exposição máxima global;
- respeitar máximo por ativo;
- reinvestir ganhos automaticamente;
- não retirar ganhos até o André decidir manualmente.

Limites definidos no exemplo atual:

- max open positions: 2
- max total exposure: 35%
- BTC max exposure: 25%
- ETH/BNB/SOL max exposure: 20%
- DOGE max exposure: 10%

---

## 5. Risk engine decidido

Risk engine é a peça central.

Regras atuais da configuração exemplo:

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

Arquivo principal na repo: `PC_ENGINE/core/strategy.py`.

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

Repo: `AndreVazao/VazaoSovereignTrader`

Estrutura criada:

```text
VazaoSovereignTrader/
├── README.md
├── .gitignore
├── requirements-pc.txt
├── requirements-mobile.txt
├── PC_ENGINE/
│   ├── main.py
│   ├── api/server.py
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
│   ├── reports/weekly_report.py
│   ├── learning/champion_challenger.py
│   └── ai_council/
│       ├── decision_mapper.py
│       └── stub.py
├── MOBILE_APP/
│   ├── main.py
│   ├── buildozer.spec
│   └── lang/
│       ├── pt.json
│       ├── en.json
│       └── es.json
├── shared/schemas.py
└── docs/
    ├── BUILD_PC.md
    ├── BUILD_MOBILE.md
    ├── SECURITY.md
    ├── TRADINGAGENTS_INTEGRATION.md
    └── PROFESSIONAL_MODULES.md
```

---

## 8. Segurança GitHub

Já existe `.gitignore` para impedir:

- `.env`
- `config.local.json`
- ficheiros com secrets;
- logs;
- data runtime;
- bases de dados;
- JSONL;
- keystores;
- APKs;
- EXEs;
- artefactos de build.

Nunca subir:

- chaves Binance/BingX;
- token local do PC;
- keystore Android;
- logs reais;
- histórico real com dados sensíveis.

---

## 9. Como arrancar o PC_ENGINE

No Windows 10:

```powershell
git clone https://github.com/AndreVazao/VazaoSovereignTrader.git
cd VazaoSovereignTrader\PC_ENGINE
python -m venv .venv
.venv\Scripts\activate
pip install -r ..\requirements-pc.txt
copy config\config.example.json config\config.local.json
python main.py
```

API local:

```text
http://127.0.0.1:8765/status
```

Exige header:

```text
X-Token: valor de VST_LOCAL_TOKEN
```

---

## 10. Melhorias profissionais implementadas em 2026-05-04

Foram adicionadas e integradas melhorias críticas para preparar o sistema para operação real futura:

### 10.1 Pre-flight checker

Arquivo: `PC_ENGINE/core/preflight.py`

Antes do arranque, verifica:

- exchanges ativas;
- símbolos configurados;
- tickers válidos;
- regras de mercado carregáveis;
- saldo quando aplicável;
- avisos especiais para REAL.

Se `engine.preflight_required = true`, o motor bloqueia o start quando existem erros críticos.

### 10.2 Exchange Rules Engine

Arquivo: `PC_ENGINE/core/exchange_rules.py`

Normaliza e valida ordens com base nas regras reais da exchange:

- `min_qty`;
- `step_size`;
- `tick_size`;
- `min_notional`;
- precision.

Objetivo: evitar ordens rejeitadas ou inválidas.

### 10.3 Paper Broker realista

Arquivo: `PC_ENGINE/core/paper_broker.py`

Simula:

- fees;
- slippage;
- spread;
- rejeições opcionais.

Objetivo: impedir PAPER fantasioso que pareça melhor que REAL.

### 10.4 Order Manager

Arquivo: `PC_ENGINE/core/order_manager.py`

Centraliza execução de ordens:

- valida exchange rules;
- bloqueia duplicados;
- executa paper fills;
- chama exchange real apenas quando `paper=false`.

### 10.5 Recovery Manager

Arquivo: `PC_ENGINE/core/recovery.py`

Guarda posições abertas em runtime local para recuperação após crash/restart.

### 10.6 Watchdog

Arquivo: `PC_ENGINE/services/watchdog.py`

Verifica internet e saúde básica da exchange. Se falhar, o motor entra em `SAFE_MODE`.

### 10.7 Replay Backtester

Arquivo: `PC_ENGINE/backtest/replay.py`

Permite backtest/replay com:

- fees;
- slippage;
- P&L;
- drawdown;
- wins/losses;
- profit factor.

### 10.8 Weekly Reporter

Arquivo: `PC_ENGINE/reports/weekly_report.py`

Gera relatórios JSON/CSV com:

- trades;
- wins/losses;
- winrate;
- P&L;
- melhor/pior trade;
- P&L por ativo.

### 10.9 Champion / Challenger

Arquivo: `PC_ENGINE/learning/champion_challenger.py`

Permite comparar estratégia ativa contra challengers em PAPER. Nunca troca automaticamente; apenas recomenda revisão.

### 10.10 AI Council stub

Arquivos:

- `PC_ENGINE/ai_council/decision_mapper.py`
- `PC_ENGINE/ai_council/stub.py`

Preparado para futura integração com TradingAgents. Desligado por default.

Regra obrigatória:

```text
AI Council só sugere.
Risk Engine decide.
Executor age.
```

---

## 11. Próximos passos recomendados

1. Testar import/path do PC_ENGINE no Windows 10.
2. Corrigir eventuais erros de execução local.
3. Validar pre-flight com Binance pública e depois com API local segura.
4. Rodar PAPER por 14 dias com paper realista.
5. Gerar backtests/replays de 30/90/180 dias antes de REAL.
6. Melhorar dashboard PC local.
7. Empacotar PC com PyInstaller.
8. Testar APK via Buildozer.
9. Criar pairing simples APK ↔ PC.
10. Só depois preparar REAL com confirmação dupla.
11. Futuramente adicionar `ai_council` baseado no TradingAgents.

---

## 12. Binance / conta real

ChatGPT não tem acesso direto à conta privada Binance do André.

O sistema só poderá ler saldo privado quando:

- André criar API key na Binance;
- configurar a key localmente no PC por variáveis de ambiente;
- permissão Read/Spot Trade estiver ativa;
- Withdraw estiver desligado;
- o PC_ENGINE estiver a correr localmente.

Até lá, só é possível consultar dados públicos de mercado, não saldo/conta.

---

## 13. Frase-guia do projeto

```text
O bot é soberano, local e disciplinado.
Não procura magia.
Procura sobreviver, aprender e crescer com risco controlado.
```
