# VazaoSovereignTrader — aprendizagem de candlesticks

Atualização: 2026-09-06

## Validação das imagens fornecidas

As duas imagens mostram padrões reais e conhecidos de price action/candlesticks, mas os rótulos BUY/SELL não devem ser tratados como verdade universal.

Correções importantes:
- Hammer: normalmente bullish/reversal warning após queda, não SELL automático.
- Hanging Man: normalmente bearish warning após subida, não BUY automático.
- Dragonfly Doji: tendência bullish/reversal apenas em contexto adequado.
- Gravestone Doji: tendência bearish/reversal apenas em contexto adequado.
- Doji: indecisão, não é BUY/SELL por si só.
- Morning Star e Bullish Engulfing: setups bullish contextuais.
- Three White Soldiers: bullish.
- Three Black Crows: bearish.

A validação foi confrontada com material técnico da Fidelity e com literatura de candlesticks; a conclusão é que os padrões são conceitos reais, mas são sinais suplementares e dependentes de contexto/confirmação.

## Implementação no repo principal

Commits realizados em `AndreVazao/VazaoSovereignTrader`:

- `509e6a39df891b62309340ae3978927a0dd5b835` — novo `PC_ENGINE/core/candlestick_patterns.py`.
- `ebd3c8b4a33614e52d6c7c53fb48f99e152a6413` — integração do viés de candlesticks na `TrendEmaAtrStrategy`.
- `696e356222fcda9da1644ae1028c5f1185671abb` — documentação `docs/CANDLESTICK_LEARNING.md`.
- `ab79f824fcfbefb92cba568a88ec295e2c5009b3` — testes `tests/test_candlestick_patterns.py`.

## Regra de aprendizagem

O bot não copia cegamente a imagem. A camada de candlesticks apenas refina um sinal de tendência já existente.

Pipeline:

`padrão -> contexto -> tendência EMA/ATR/VWAP -> confirmação -> risk engine -> PAPER -> resultado -> aprendizagem`

Nenhum candlestick sozinho pode abrir uma posição.

## Próxima melhoria

Usar o ledger PAPER para medir por ativo/timeframe:
- frequência de cada padrão;
- win rate;
- P&L médio;
- drawdown associado;
- desempenho por regime;
- desempenho com/sem volume e confirmação de breakout.

Só depois de amostra estatística suficiente os pesos dos padrões devem ser ajustados automaticamente. Até lá, o peso é conservador.
