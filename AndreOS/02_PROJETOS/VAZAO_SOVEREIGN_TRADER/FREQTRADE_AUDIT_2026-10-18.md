# Sovereign Trader — memória da auditoria Freqtrade
Data: 2026-10-18

## Resultado
O repositório privado `AndreVazao/freqtrade` foi inspecionado por GitHub connector. É um bot Python baseado em CCXT, licenciado GPL-3.0, com suporte a várias exchanges, backtesting, dry-run, estratégias candle-based, WebUI/API e mecanismos de proteção/rate limiting.

## Decisão
Não incorporar Freqtrade inteiro no processo central do VazaoSovereignTrader. Reutilizar padrões de arquitetura e validar lacunas reais do nosso conector CCXT. Não copiar código GPL para o core sem revisão de licenciamento. Se necessário, considerar Freqtrade como processo externo isolado para tarefas de backtesting/candle strategies, nunca como autoridade de risco ou execução.

## Componentes de interesse
- `freqtrade/exchange/exchange.py` — normalização CCXT, capacidades de venue, precisão, limites, order book e integração assíncrona.
- `freqtrade/resolvers/exchange_resolver.py` — resolução de subclasses específicas e fallback genérico.
- `docs/exchanges.md` e `docs/configuration.md` — rate limits, configurações específicas, REST/WebSocket.
- Backtesting/dry-run e análise de lookahead/recursive bias — bons princípios de validação, mas não substituem o motor de arbitragem cross-venue e latência do Sovereign Trader.
- A API local do Freqtrade não deve ser exposta publicamente nem ter autoridade sobre REAL.

## Segurança e limites
- O PC de desenvolvimento `PC-Vazao-Anjos` estava offline durante esta sessão. Não foi possível validar a working tree local, correr testes nem alterar código local.
- Foi criado PR documental draft #379 no Trader: https://github.com/AndreVazao/VazaoSovereignTrader/pull/379
- Commit da documentação no branch PR: `2e5f383d4505374e9e6c4f5188a9380997656de4`.
- Nenhuma exchange contactada, nenhuma API key usada, nenhuma ordem, depósito ou transferência. PAPER-first inalterado.

## Próximos passos
1. Quando o PC voltar online, verificar status/log Git e alterações locais antes de qualquer sync.
2. Rever PR #379 e integrar documentação depois da revisão.
3. Auditar os adaptadores CCXT que já existem no core e construir mapa de capacidades sem duplicar clientes.
4. Implementar/read-testar um conector de dados públicos de cada vez, com timestamps de exchange e receção, bid/ask/depth, rate limits, freshness e fixtures offline.
5. Garantir NO_EDGE para dados stale/desconhecidos/não comparáveis.
6. Manter a fronteira de execução desativada e independente de Freqtrade.

Fontes:
- https://github.com/AndreVazao/freqtrade
- https://github.com/AndreVazao/freqtrade/blob/main/freqtrade/exchange/exchange.py
- https://github.com/AndreVazao/freqtrade/blob/main/freqtrade/resolvers/exchange_resolver.py
- https://github.com/AndreVazao/freqtrade/blob/main/docs/exchanges.md
- https://docs.freqtrade.io/en/latest/
- https://docs.freqtrade.io/en/latest/backtesting/
- https://docs.ccxt.com/docs/comparisons/ccxt-vs-freqtrade
