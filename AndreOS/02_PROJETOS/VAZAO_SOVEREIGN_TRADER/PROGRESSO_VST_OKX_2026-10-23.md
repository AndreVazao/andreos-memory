# VST — progresso e próximos bloqueios
Data: 2026-10-23

## Identidade visual oficial
- Sigla curta oficial: **VST**.
- Nome completo: **Vazão Sovereign Trader**.
- Lockup visual: **V** sobre **Vazão**, **S** sobre **Sovereign**, **T** sobre **Trader**.
- O lockup foi integrado no escritório virtual e no protótipo standalone via PR #482, merged em `287aae28f5aeaabe27117dc3061f861ec46a8948`.
- Padrão de marca: `AndreOS/02_PROJETOS/VAZAO_SOVEREIGN_TRADER/VST_BRAND_STANDARD_2026-10-23.md` e `docs/VST_BRAND_STANDARD.md` no produto.
- Não renomear diretórios, pacotes ou identificadores internos automaticamente só para fazer a sigla coincidir.

## Estado de mercado — OKX L2
- PR #481 foi fechado sem merge para evitar conflito após a integração da marca VST em `main`.
- Substituto: PR #483, draft, branch `feat/okx-books-sync-rebased-2026-10-23`.
- PR #483 contém sincronizador fail-closed para o canal incremental `books`, validação de instrumento, continuidade de sequência, invalidamento em desconexão/erro de parsing, telemetria de frescura e testes de regressão.
- Corrigido no branch: heartbeat vazio com `seqId == prevSeqId` é preservado como evento de controlo interno; só renova frescura se a sequência coincide com o livro sincronizado; não é encaminhado para o armazenamento normalizado de eventos de livro.
- `data: []` é rejeitado e invalida imediatamente um livro previamente elegível.
- Snapshot com sequência inferior à sincronizada invalida a vista e exige recuperação explícita.
- Cabeça atual conhecida de #483 no momento do registo: `bfec5247867751c8445205e67be73878eb88df1a`.
- Os checks Vercel e Snyk estavam pendentes nesta cabeça; consulta de GitHub Actions devolveu zero workflow runs. **Não declarar os testes Python executados ou aprovados.** Executar testes focados e a suite Python necessária na cabeça final, guardar os resultados e rever os checks após os últimos commits.

## Gate de segurança
- OKX continua **inelegível para sinais de edge cross-venue baseados em profundidade** até testes Python exatos da cabeça final, revisão do protocolo com fixtures e observação ao vivo não executora.
- Parser válido não prova livro sincronizado; livro sincronizado não prova equivalência de instrumentos; diferença de preços não prova lucro executável.
- Manter observação/PAPER. Não ativar REAL, enviar ordens, transferir ou levantar fundos sem autorização explícita do utilizador.
- Sem afirmar que sincronização com PC, runtime Windows, Android ou E2E físico foi validada sem evidência real.

## Próximas ações
1. Esperar Vercel/Snyk no PR #483 e confirmar estados terminais.
2. Executar localmente testes focados de `tests/test_l2_collectors.py` e `tests/test_okx_book_sync.py`, mais a suite Python requerida, na cabeça final.
3. Corrigir quaisquer falhas, repetir os checks na nova cabeça e só então pedir revisão/merge.
4. Depois validar casos de sequência/recovery de Coinbase e telemetria Binance; só mais tarde trabalhar em normalização cross-venue, custos, latência e evidência PAPER.
