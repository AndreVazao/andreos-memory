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
