# VazaoSovereignTrader — checkpoint 2026-10-22 (auditoria e prontidão)

## Estado verificado
- Main checkpoint conhecido após PR #431: `7a33a0177fdc7e370ea6a2bc1a5f84214d1cc71f`.
- Auditoria estática: `docs/TRADING_INTEGRATION_AUDIT_2026-10-22.md`. Não é certificação de produção, runtime, PC Windows, Android ou rentabilidade.
- PR #432: https://github.com/AndreVazao/VazaoSovereignTrader/pull/432 — state machine inicial de Binance Spot diff-depth; continua aberta. O run Python #3033 / `39735346490` passou no head inicial `12dbb8da2db98ad9835c90da8b2fb9bf592e616d`.
- Depois do run inicial, foram feitos dois commits de hardening na branch da PR: `258474745e962798535f3f06fc26b09b8e2a099e` e `b7f4f41a6179dd1ef189423266f7f8c7d76f47b5`. O código rejeita sequências negativas/invertidas, configuração max_age_ms não finita e books cruzados não elegíveis; foram acrescentados testes de regressão.
- Atenção: não foi encontrado ainda um workflow Python associado ao novo head `b7f4f41a6179dd1ef189423266f7f8c7d76f47b5`. Portanto o código adicional ainda não está validado por CI no head exato e PR #432 não deve ser merged até existir validação equivalente e revisão final.
- A state machine #432 continua isolada: ainda não liga snapshot REST, buffer bounded, replay, reconnect/resync ou telemetria ao coletor live; não ligar ao cálculo de edge nem tratar o JSONL L2 como livro sincronizado.

## Escritório digital
- Existe `virtual_office/prototype/full_cockpit_shell.html`, servido por `GET /virtual-office`, e testes em `tests/test_virtual_office_route.py`.
- A shell tem layout responsivo, mapa de departamentos selecionáveis, modos office/compact/chat, painel de ligação autenticada e resumo via endpoints de observação. O HTML ainda se identifica como protótipo e vários elementos/salas são demonstrativos.
- O contrato de integração documenta leitura autenticada, token apenas em memória de página e gateway determinístico para `POST /assistant/message`, com limites de segurança. Ainda faltam browser end-to-end tests, rendering tipado completo, streaming/reconnect e comprovar que todas as conversas/departamentos estão ligadas ao runtime real. Não alegar escritório plenamente funcional.
- O runtime deve continuar a ser o único cérebro/autoridade; o escritório é cliente observador/controlador, não segundo motor.

## Mobile / instalação
- `MOBILE_APP/ui.py` contém cockpit Kivy com chat, PC/LAN/Tailscale, ficheiros, intervenção humana e readiness; a página PC usa ScrollView.
- `MOBILE_APP/README.md` diz que o token não é persistido e tem de ser introduzido após reiniciar a app. A documentação de pairing e o código atual têm de ser reconciliados: o projeto-context anterior assinala que one-time cryptographic pairing/device revocation e Android Keystore-backed token persistence não estavam completos. Não afirmar Keystore/revogação seguras sem verificar o código atual.
- Build Windows/APK e smoke físico no PC/Android não foram verificados no SHA atual desta auditoria. O histórico de um build anterior não valida o release atual.
- Não instalar ainda. Manter PAPER/read-only; não inspecionar nem imprimir segredos da configuração local sem acesso e consentimento apropriados.

## Estimativas atuais de prontidão (heurísticas, não métricas automáticas)
- Engine + recolha de dados: 70%.
- Radar / edge temporal cross-exchange: 45%.
- Segurança / execução / reconciliação integrada: 60%.
- Cockpit + escritório digital: 40%.
- APK Android: 30%.
- Instalação Windows/autostart no PC atual: 35%.
Estas percentagens representam proporção aproximada de trabalho/evidência concluída por área, não probabilidade de sucesso, qualidade de trading nem autorização REAL.

## Próxima sequência
1. Obter CI no head exato atual de #432 e rever os diffs; não mergear sem isso.
2. Depois de #432 validada/merged, implementar integração Binance separadamente: WS bounded buffer + REST snapshot + replay da sequência + reconnect/resync + métricas; testes para buffer overflow, gap, restart, stale e fail-closed.
3. Implementar contratos de book independentes para OKX e Coinbase; não generalizar o protocolo Binance.
4. Fazer inventário e testes negativos dos caminhos de ordens/cancelamentos/transferências/retiradas e da reconciliação no SHA atual; confirmar PAPER por defeito.
5. Testar API/cockpit/office: autorização, dados stale/offline, mensagens, departamento direto, não duplicação do Runtime, desconexão e saturação.
6. Gerar builds Windows e Android a partir do SHA release; depois smoke no PC e no telefone, reboot/restart e LAN/Tailscale. Até então, marcar dispositivos/builds como não verificados.
7. Atualizar a auditoria e percentagens só com evidência nova. Nenhuma instalação ou execução REAL até os blockers correspondentes estarem fechados.


## Atualização — 2026-10-22, pesquisa de conectores e edge L2

- Main observado depois do PR #465: `c727c388294ff08b82f2c77d10e222a17c5811f8`.
- PR #465 merged: https://github.com/AndreVazao/VazaoSovereignTrader/pull/465. Introduz `PC_ENGINE/radar/depth_edge.py`, uma avaliação PAPER-only e fail-closed de top-of-book entre duas views já sincronizadas: exige identidade canónica exatamente igual, venues diferentes, estado SYNCED/eligible, idades limitadas, preços válidos/não cruzados, timestamps monotónicos comparáveis com skew limitado e custos explícitos por venue + penalização de latência. O resultado mantém `execution_allowed=false`. CI Python e Windows EXE/installer passaram no head `ef25ee760ef685d00932e3f5082105b2c609f20c`. Isto **não** sincroniza dados, normaliza mercados, calcula VWAP/profundidade, mede fill probability nem liga o sinal à execução.
- Pesquisa técnica: Hummingbot recomenda separar Connector, OrderBookTracker, fonte de dados e tracking privado de ordens; os dados de book exigem timestamps/sequência e fallback de snapshot quando a continuidade não pode ser garantida. CCXT Pro usa loops async e caches limitadas, e documenta a diferença entre consumir cada update em tempo real e processamento throttled. Adotar os padrões como arquitetura e testes, não copiar código sem revisão de licença.
- PR #466 aberto: https://github.com/AndreVazao/VazaoSovereignTrader/pull/466. Corrige um caso no parser Coinbase Advanced Trade: `sequence_num` pertence ao envelope e não a cada item interno; múltiplos itens do mesmo envelope passam a produzir um evento atómico para que o reconstrutor não veja o mesmo sequence ID repetido. Testes novos cobrem agregação, mistura snapshot/update e aplicação contígua ao `OrderBookBuilder`. O Python suite passou no head intermédio `f64e3a4940c41a214c99ea10be35ab69f530fe63`; após o commit de teste `da337352a80f7a3083dd61df7876dafb7b1bfe8f`, Python passou e o Windows EXE/installer ainda estava em curso na última verificação. Não mergear até Windows terminar e diff ser revisto contra o head atual.
- Vercel continua a devolver rate-limit de deployment gratuito. Isto não é falha dos testes Python/Windows nem prova de que a versão web foi publicada.
- Os resultados de pesquisa não autorizam afirmar edge lucrativo: o avaliador atual é top-of-book, com views fornecidas externamente, e continua desligado dos coletores/sincronizadores e da execução. Próxima evolução depois do PR #466: sincronização Coinbase própria com snapshot/continuidade/recovery/freshness; depois OKX incremental; então comparar VWAP para tamanho fixo e custos realistas, sempre em replay/PAPER e com out-of-sample.
- Postura operacional permanece PAPER/read-only. Não houve ordens REAL, transferências, levantamentos nem ativação REAL. Windows CI não substitui verificação do PC físico; APK/Android físico, auth e failover LAN/Tailscale continuam por testar.
