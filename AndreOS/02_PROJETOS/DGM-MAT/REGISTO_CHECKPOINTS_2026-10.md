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


## Segurança API — bootstrap de sessão local (2026-10-09)

- Integrada localmente a rota `POST /auth/session` e classificada como `OPERATOR`.
- Instalador `scripts/autostart/install_local_bootstrap_credential.ps1` criou credencial aleatória de 128 caracteres hexadecimais em `%LOCALAPPDATA%\DGM-MAT\security\bootstrap.token`; segredo não foi mostrado nem registado.
- ACLs do ficheiro e diretório de segurança têm herança desativada e acesso limitado à conta Windows atual e SYSTEM.
- Testes focados: 16 passaram. Suite completa: exit code 0. Parser PowerShell, py_compile e `git diff --check` passaram.
- Backend reiniciado de forma controlada: PID 4800 parado; versão integrada PID 6876, health saudável, rota presente no OpenAPI e pedido sem credencial rejeitado com HTTP 401.
- Limite: emissão válida foi verificada com credencial temporária nos testes automatizados, mas não validada independentemente contra o servidor live nesta passagem. Não contornar bloqueios de ferramenta.
- A API continua loopback-only. A nova rota não protege globalmente rotas HTTP/WebSocket existentes e os clientes ainda não foram migrados. Não ativar LAN/Tailscale/público.
- Relatório: `AndreOS/05_LOGS_IA/DGM-MAT_LOCAL_SESSION_BOOTSTRAP_2026-10-09.md`.
- Publicação confirmada depois do relatório: commit DGM-MAT `d4755b7` (`feat: add local bootstrap session endpoint`) enviado para `origin/main`; a credencial bootstrap não foi adicionada ao Git.


## DGM-MAT — escritório digital, Bug Hunter e inventário (2026-10-09)

- Cloud Free: utilizador informou alterações estruturais substanciais. Manter em memória como potencial agente/provider futuro do DGM-MAT; não mexer nem integrar agora. Antes de qualquer trabalho futuro, inventariar o estado atual em modo read-only.
- Implementados localmente: `core/organization/office.py` (roster expandido), `core/organization/delegation.py` (delegação determinística por skills/permissões/dependências), `core/repository_intelligence/snapshot.py` (inventário/tree limitado, sem ler conteúdo e sem seguir symlinks).
- Bug Hunter detetou e corrigiu falso `VALIDATED` em tarefas que nunca eram executadas; placeholders agora dizem `NOT_EXECUTED` e ciclos ficam `PARTIAL`. Corrigido também bug em que `AutonomyCycle.complete()` sobrescrevia `FAILED` com `COMPLETED`.
- Corrigido shutdown do ResourceMonitor: stop event, wait interruptível, join limitado e integração no shutdown do GovernanceEngine. A primeira suite completa passou mas produziu erro Loguru de thread tardia; após correção a suite completa voltou a passar com exit code 0 e sem esse erro.
- Testes focados finais: 19 passaram; py_compile e diff check passaram.
- Backend vivo: health saudável em `127.0.0.1:8181`, PID 6876.
- Inventário verificado: 1.601 ficheiros, 221 diretórios, 117 itens/diretórios ignorados. Artefactos `reports/repository_inventory/DGM-MAT_INVENTORY_VERIFIED_2026-10-09.json` e `DGM-MAT_TREE_VERIFIED_2026-10-09.txt`.
- Relatório: `reports/DGM-MAT_BUG_HUNTER_AUDIT_2026-10-09.md`.
- Limite: o roster ainda não representa processos IA independentes ativos; delegação ainda não está ligada à execução durável. A API continua loopback-only até auth global e migração de clientes.

- Correção do inventário final para evitar auto-referência: 1.597 ficheiros, 220 diretórios, 118 ignorados; diretório de saída excluído do snapshot. Ficheiros finais `DGM-MAT_INVENTORY_FINAL_VERIFIED_2026-10-09.json` e `DGM-MAT_TREE_FINAL_VERIFIED_2026-10-09.txt` em `reports/repository_inventory/`.

Publicação confirmada: DGM-MAT `9296ea0` e memória `6b7ced9` enviados para `origin/main`; ambas as repos foram verificadas limpas e sincronizadas após integrar commits remotos concorrentes.


## Princípio operacional pedido pelo utilizador — ajuda e custos (2026-10-09)

- O DGM-MAT deve perceber o que a missão exige e reconhecer explicitamente quando não sabe ou não consegue avançar.
- Antes de perguntar, deve consultar memória persistente, código/documentação, evidências e ferramentas já disponíveis.
- Quando precisa de ajuda, encaminhar o pedido ao especialista ou recurso certo e incluir objetivo, contexto, passos tentados, evidência, bloqueio e pergunta/ação concreta.
- Preferência: capacidades locais gratuitas → quotas gratuitas verificadas → documentação oficial/pesquisa → especialista adequado → pergunta ao utilizador para decisões/autorização.
- Não fingir conclusão, repetir tentativas cegas ou gastar créditos/ativar serviços pagos sem autorização explícita e custo/limite conhecido.
- Sem caminho seguro/gratuito, registar `BLOCKED` ou `PARTIAL` e indicar a ajuda necessária.
- Implementação inicial: `core/organization/help_seeking.py`, `tests/organization/test_help_seeking.py` e `docs/architecture/HELP_SEEKING_ZERO_COST_POLICY.md`. Testes focados: 8 passed; compilação e diff check passaram.
- Limite: ainda não integrado globalmente no Mission Engine/provider execution; não afirmar que a plataforma inteira já está protegida. Ver `AndreOS/05_LOGS_IA/DGM-MAT_HELP_SEEKING_ZERO_COST_2026-10-09.md`.
