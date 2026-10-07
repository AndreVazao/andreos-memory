# DGM-MAT — Registo de checkpoints persistentes

Atualizado em 2026-10-07.

Este ficheiro consolida o histórico técnico recente que estava disperso entre memória conversacional, Mem e notas locais.

## Arquitetura e reorganização

- Arquitetura real mapeada: API → MissionEngine → mission JSON + SafeActionQueue → SQLite → approval → consumer → MissionEngine handler → persistence → RuntimeStateStore → API/WebSocket.
- Event flow: EventBus → governance/validation → EventStore SQLite → stream → realtime → WebSocket.
- Autonomous flow: daemon → CognitionLoop → MissionEngine → repository observation → StrategicPlanner → ObjectiveEngine → ExecutionDirector → validation → LearningLoop.
- Reorganização segue: MAPEAR → CLASSIFICAR → COPIAR/MIGRAR → REESCREVER INTERLIGAÇÕES → TESTAR → COMMITAR → VALIDAR → só depois remover origem.
- FULL-MIRROR é arquivo de recuperação e não deve ser alterado.

## DGM-Contracts

- `93ee591` — pyproject inicial.
- `0253df5` — exports.
- `98c5bf6` — schemas.
- `cf94d49` — reconciliação.
- Contratos incluem ExecutionRequest/Result, ToolDescriptor, ApprovalRequest/Decision, EventEnvelope, MissionReference/State e ports de Agents.
- Event canónico aceita alias legado `id` e expõe `Event.id`.
- Migração física de Event concluída.
- Checkpoint DGM-MAT: `8528575`.

## Execução e approvals

- SafeActionQueue é a fronteira durável candidata a autoridade de execução/aprovação.
- ApprovalManager passou a facade de compatibilidade.
- Teste cross-process confirma missão persistida pode ser encontrada por outro processo e concluída.
- Checkpoint: `86ad0c8d8a0d368182f00fd074abfec104a4ad25`.

## Event boundary

- EventRecord passou a guardar envelope completo.
- EventStore persiste/reproduz EventEnvelope.
- EventStream transmite envelope completo.
- Checkpoint: `56019e4`.

## Regression

- Suite DGM-MAT chegou a 100% verde.
- Correções incluíram imports, cockpit dispatch, proteção de workflows, knowledge engine, paths configuráveis, runtime smoke e compatibilidade TaskGenerator.
- Checkpoint: `df097bd`.

## GitHub Actions

- Workflows normais passaram a `workflow_dispatch`.
- Release continua tag-driven.
- Política: testes locais primeiro; não iniciar Actions desnecessariamente.
- Commits: `dff165c`, `4e3ecaa`.

## Agents

- DGM-MAT-Agents extraído como pacote independente.
- DGM-Contracts fornece AgentLogger, ProviderService e TaskService.
- Core usa boundary/adapters.
- Commits: `3bf14d6` em Contracts; `cade249`, `527fece` no pacote; `3518bd8` no DGM-MAT.
- Testes standalone e suite principal verdes.

## Connectors

- ObsidianConnector extraído para DGM-MAT-Connectors.
- Core consome via boundary.
- Commits: `f4df495`, `0c86139`, `47e38ff`.
- Testes standalone, focados e suite principal verdes.

## Providers

Providers ainda não foram extraídos fisicamente.

Razão: acoplamento significativo entre ProviderBase, realtime, credential vault, ProviderRegistry, StorageManager, dynamic discovery, ProviderRuntime e cockpit.

Gate definido:
1. inventariar API real do Registry;
2. inventariar request/response usados;
3. criar contratos mínimos em DGM-Contracts;
4. criar facade de serviço no Core;
5. retirar acesso direto do cockpit ao Registry;
6. adaptar Agent ProviderService;
7. só então extrair adapters para DGM-MAT-Providers.

Checkpoint documental: `b62abeb`.

## DGM-HUB / DGM-MCP

- DGM-HUB permanece sistema legado/research/reuse source.
- TruthLayer, AgentLoop e PatchApplyEngine são referências; não devem ser importados wholesale.
- DGM-MCP fornece referência para MCP transport, ToolDescriptor, PathGuard, AuditLogger e tool registry.
- MCP é transporte/interface, não autoridade do DGM-MAT.
- Papel documentado: `5662518`.
- Auditoria integrada: `9ec5693161b7ebce588994d1c9f67fdae2d03543`.

## Memória

A partir de 2026-10-07, a memória persistente de DGM-MAT deve ser lida/escrita em:

`C:\AndreOS-Memory\AndreOS\02_PROJETOS\DGM-MAT\`

O GitHub `AndreVazao/andreos-memory` é a persistência partilhada entre sessões e ferramentas.
