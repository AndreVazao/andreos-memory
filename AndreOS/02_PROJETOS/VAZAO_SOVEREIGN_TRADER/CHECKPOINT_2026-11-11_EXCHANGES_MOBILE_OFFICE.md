# VST — checkpoint de continuidade: Exchanges, Mobile e Escritório Digital

**Data:** 2026-11-11  
**Produto:** https://github.com/AndreVazao/VazaoSovereignTrader  
**Main verificada:** `5f73a6d13af42186a2ffade05511fc97d835a8e7`  
**Branch de trabalho VST:** `feat/exchange-readonly-mobile-office-foundation-2026-11-11`

## Estado confirmado nesta sessão

- VST main sem PRs abertas no momento da consulta.
- PC teve VST 2026.11.1 instalado e PAPER iniciado numa sessão anterior; estado atual do processo no PC não foi novamente verificado.
- Market data público não equivale a ligação privada à conta da exchange.
- Não foram introduzidas API keys privadas; não houve ordens reais nem transferências.
- A versão instalada ainda não disponibiliza uma gestão de credenciais de exchange validada.
- O repositório já contém Android APK, pairing/revocation, token Android Keystore e UI de escritório virtual offline. O escritório não deve ser apresentado como cérebro conectado em tempo real.
- A API local e o assistant gateway existem; as capacidades/escopos devem ser auditados endpoint a endpoint antes de expor ações em mobile/office.

## Decisões de produto

1. Um único PC_ENGINE é autoridade. Windows cockpit, Android e Digital Office são clientes, não motores paralelos.
2. Binance e OKX começam por ligação privada read-only.
3. Credenciais só entram num formulário seguro no PC, em ligação local autenticada. Nunca no chat, APK, push, Vercel, logs, config normal, Git ou Learning Vault.
4. Windows DPAPI CurrentUser para armazenamento cifrado; fail-closed sem plaintext fallback. Rejeitar permissões de trade/withdraw no primeiro incremento.
5. Mobile: estado e freshness, Radar/mercados, PAPER/evidência, Learning Vault, alertas/intervenção humana, chat autenticado e IDs de tarefas, estado read-only das exchanges, pairing e revogação.
6. Digital Office: salas alimentadas por snapshots/eventos reais do backend; nenhuma animação pode inventar agentes ativos, lucros, ordens ou atividade. Chat compacto é fallback low-memory.
7. Conectividade remota privada (Tailscale preferencial), API loopback por defeito, sem porta pública. Failover automático apenas GET; timeout de mutação = UNKNOWN/reconcile, nunca retry cego.
8. Sem REAL, ordens, cancelamentos, transferências ou levantamentos nesta fase. Sem cloud paga obrigatória.

## Trabalho documental realizado

Na branch VST acima:
- Criado `docs/EXCHANGE_CONNECTIONS_MOBILE_AND_DIGITAL_OFFICE_ROADMAP_2026-11-11.md` com arquitetura, entregas E1/M1/O1 e gates de aceitação.
- Atualizado o bloco autoritativo no topo de `docs/PROJECT_CONTEXT.md`.
- Ainda não foi implementado vault DPAPI, endpoint de credenciais, formulário de exchanges ou novas vistas mobile. Não alegar implementação concluída.

## Próximas entregas

- E1: inventário de rotas/config/exchanges; vault DPAPI; capability registry Binance/OKX read-only; permission verifier; endpoints owner-only register/verify/status/revoke; formulário PC; testes de redaction, storage, permissões, timeout e falhas.
- M1: modelos tipados de estado e freshness; refresh limitado/offline/stale; chat gateway e task IDs; views PAPER/Radar/Learning/alerts; validar APK, emulator e dispositivo físico separadamente.
- O1: ligar salas do escritório à API/eventos reais, responsividade desktop/Android e renderização adaptativa.
- Só pedir ao utilizador que crie API keys depois de CI exact-head e revisão de segurança. Nunca pedir secrets no chat.

## Regras de continuidade

- Uma branch/PR de implementação de cada vez no repo VST; não editar main diretamente.
- Confirmar SHA/PRs/checks atuais antes de qualquer merge.
- Não usar o checkout local antigo sem backup/inspeção.
- Não gastar quota Desktop Commander sem necessidade; privilegiar inspeção GitHub agrupada.
- Não afirmar teste físico Android, E2E remoto, learning end-to-end ou lucro sem evidência.


## Incremento de 2026-11-11 — observabilidade do mercado e primeira vista mobile

Na branch VST da PR #564:
- `MarketRadar` passou a contar pedidos públicos, observações válidas, erros de rede, rejeições de qualidade, batches de persistência e erros de persistência, incluindo contadores por venue.
- `PaperMarketCollector.snapshot()` expõe estas métricas; endpoint autenticado `GET /paper-collector/resources` inclui `market_data_collection`.
- Android ganhou página Mercado/Radar com pedidos, observações, rejeições, falhas, última observação e contadores por exchange. Atualização só GET, sem credenciais ou comandos financeiros.
- Testes acrescentados a `tests/test_market_radar.py` e `MOBILE_APP/test_startup_contract.py`.
- Documentação do roadmap e PROJECT_CONTEXT atualizada.
- Commit mais recente observado: `1ee6df52f4be1cc061d83329c682b0a5038d66e7`. PR #564 ainda aberta; checks do HEAD mais recente ainda não apareceram na consulta. Não fazer merge até CI exact-head e Windows DPAPI nativo passarem.
- Isto melhora observabilidade; ainda não é prova de recolha live no PC nem de classificação rentável. Não há confirmação de APK em emulador/dispositivo físico nesta sessão.

- Subsequent exact-head changes: Android `MOBILE_APP/ui.py` and `main.py` add a dedicated Mercado/Radar page reading authenticated `GET /paper-collector/resources`, with collector state, counters, per-venue outcomes and last-observation freshness. Static contract test added in `MOBILE_APP/test_startup_contract.py`.
- DPAPI native calls were hardened with explicit ctypes argument/return signatures and pointer-safe `LocalFree` handling. Native Windows execution still needs CI/physical Windows verification.
- Latest VST branch head at checkpoint update: `58e7dc89d4483fc2de3283cd4805eb6436044caf`. PR #564 remains open. Only Vercel Preview Comments had appeared completed at last check; remaining CI was not yet reported complete. Do not merge based on incomplete checks.

- Mobile Radar page now also reads authenticated `GET /evidence-scorecard` and displays evidence requirements met/missing. Copy explicitly states PAPER-only, no submitted orders and no REAL authorization. Static contract test covers this.
- Latest VST PR #564 head: `1afe2df59b59865806048ea2e14a99d0934917e1`; PR remains open and mergeable. Latest checks were queued/pending; prior head PAPER smoke had passed, but rerun for this latest head was queued. Never merge until exact-head tests, Android emulator, APK, Windows build and DPAPI native verification are reviewed.


## Continuidade adicional — 2026-11-11 (revisão exact-head e estratégia PAPER)

- PR VST #564 continua aberta, branch `feat/exchange-readonly-mobile-office-foundation-2026-11-11`, HEAD atual `35217f00d257aaf3851332f9d93c73c41a04058e`, mergeable=true. HEAD anterior `1afe2df59b59865806048ea2e14a99d0934917e1` teve Python tests e PAPER lifecycle smoke PASS; Android APK, Emulator UI e Windows EXE estavam ainda em execução.
- Foi acrescentado `tests/test_credential_vault_windows.py`, que executa round-trip DPAPI CurrentUser nativo em Windows e confirma que o ciphertext e metadata não contêm os valores de teste em plaintext. O workflow `.github/workflows/windows-exe.yml` executa agora este teste e os testes do vault antes do build. A nova execução exact-head está pendente/em progresso; não afirmar PASS até concluir.
- Foi criada branch separada VST `feat/paper-strategy-advisor-2026-11-11`, baseada em main SHA `247f0ebdd62eaafd79510e1ca781e80468704b07`, HEAD atual `3ad6543188744fb769a9f61da0ba52434f59cb8c`. Não foi aberta PR porque #564 ainda está aberta e mantemos uma PR de implementação de cada vez.
- Esta branch adiciona `PC_ENGINE/research/strategy_advisor.py`, CLI `PC_ENGINE/tools/run_strategy_advisor.py`, testes `tests/test_strategy_advisor.py`, documentação `docs/PAPER_STRATEGY_ADVISOR_2026-11-11.md`, e integra o advisor no fim de `run_paper_study.py`.
- O advisor avalia amostra mínima, OOS cronológico, média líquida pós-custos, consistência walk-forward, Monte Carlo e amostra por regime. Resultado é `INSUFFICIENT_EVIDENCE`, `CONTINUE_PAPER_RESEARCH` ou `REJECT_OR_REWORK`. Mesmo quando passa, apenas recomenda continuar investigação PAPER: não altera parâmetros, não promove candidatos, não altera risco, não autoriza REAL nem submete ordens.
- Testes da nova branch ainda não foram executados por CI; não abrir PR nem fazer merge até #564 fechar e validar local/CI. A execução local no PC e o estado atual do engine não foram verificados nesta sessão.
- O objetivo continua a ser produzir evidência de estratégia com dados reais; não afirmar lucro, aprendizagem end-to-end ou prontidão REAL. Preservar baixo consumo e poupar Desktop Commander.


## Incremento de investigação estatística — 2026-11-11

- Branch VST `feat/paper-strategy-advisor-2026-11-11` avançou até HEAD `4fc593cdd5049fe0091281a662aabb0b6073f29c`.
- O estudo agora adiciona `outcome_timestamp_ms` às observações, purga do treino cronológico labels cujo horizonte futuro atravessa o início do teste, e aplica a mesma purga às janelas de treino walk-forward.
- O relatório passa a produzir `monte_carlo_oos` separado. O Strategy Advisor usa apenas este bootstrap OOS para o gate de incerteza; Monte Carlo ausente ou probabilidade inválida falha fechado.
- Testes adicionados/ajustados para purga cronológica, bootstrap OOS e probabilidades inválidas. Ainda sem CI desta branch porque PR #564 continua aberta e mantemos uma PR de implementação de cada vez.
- Atenção: `walk_forward` só relata estatísticas e não ajusta parâmetros de estratégia; ainda não existe ciclo autónomo de geração/seleção de estratégias. Advisor é avaliação de evidência, não prova de rentabilidade.
- PR #564 HEAD `35217f00d257aaf3851332f9d93c73c41a04058e`: Python tests, PAPER smoke, Windows EXE (incluindo teste nativo DPAPI no runner) e Android APK concluídos PASS; Android Emulator UI Smoke ainda em execução. Não fazer merge até o emulador terminar e a revisão final ser concluída.
- Não usar Desktop Commander nesta fase; estado do PC físico e estado atual do engine não foram novamente verificados. Nenhuma chave privada, ordem REAL ou transferência.


## Incremento de descoberta de estratégias — 2026-11-11

- Branch VST `feat/paper-strategy-advisor-2026-11-11` HEAD `430ae4fea6a572c327778466b5bbbb4d5c9ff892`.
- `PC_ENGINE/research/paper_study.py` agora permite restringir timestamps dos sinais sem restringir o conjunto de preços futuros usado para resolver os outcomes.
- Novo `PC_ENGINE/research/strategy_discovery.py`: grelha determinística de filtros de confiança/confluência, escolha exclusiva em treino, purge de sinais de treino cujo horizonte futuro cruza a fronteira, avaliação única OOS do candidato escolhido, baseline OOS e Monte Carlo OOS. Não aplica parâmetros ao runtime nem promove candidato.
- `run_paper_study.py` executa discovery sob AdaptiveJobGate simulation e grava `PC_ENGINE/data/radar/strategy_discovery_report.json`; se recursos insuficientes, grava `DEFERRED_RESOURCE_GUARD` sem bloquear o estudo base.
- Novos testes em `tests/test_strategy_discovery.py`; `tests/test_paper_study.py` reforça o teste de purge e OOS bootstrap. CI ainda não correu nesta branch porque a PR #564 permanece aberta e mantemos uma PR de implementação por vez.
- O algoritmo é uma pesquisa de filtros sobre sinais existentes, não um gerador de modelos/estratégias totalmente novo nem evidência de edge rentável. A avaliação com dados reais e CI é obrigatória.
- PR #564 permanece HEAD `35217f00d257aaf3851332f9d93c73c41a04058e`: Python, PAPER smoke, Windows EXE/DPAPI nativo e Android APK PASS; Android Emulator UI Smoke continua em execução na última consulta. Sem merge ainda.


- Hardening adicional na branch Strategy Advisor: `simulate()` regista agora o timestamp real da observação futura que resolveu cada outcome (pode ser posterior ao horizonte pedido em feeds irregulares); discovery purga treino com base nesse timestamp efetivo e expõe `training_max_outcome_timestamp_ms`. Teste confirma que o último label de treino não ultrapassa a fronteira OOS. Branch VST HEAD atualizado: `cdd3b44ae873299c9046011c439da5ed327fd008`. Ainda sem execução CI nesta branch.
