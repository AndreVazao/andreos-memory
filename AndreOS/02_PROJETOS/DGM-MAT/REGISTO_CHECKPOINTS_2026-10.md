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

- Claude Code Free/FCC: preservar como possível recurso futuro de apoio ao desenvolvimento; não integrar automaticamente no DGM-MAT. A designação “Cloud Free” foi um erro de nomenclatura. Antes de usar, identificar a rota concreta e verificar custo/quota/permissões. Não inferir que o uso é gratuito só porque uma inferência funcionou.
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


## Follow-up — HelpSeeking integrado no caminho de falha das missões (2026-10-09)

- Backup SHA-256 verificado antes de alterar `core/autonomy/mission_engine.py`, guardado em `C:\ProgramasGodMode\DGM-MAT-OS\archive\DGM-MAT-pre-help-seeking-integration-2026-10-09__core__autonomy__mission_engine.py.bak`.
- `_finish_mission_failure` gera e persiste recomendação `RECOMMENDATION_ONLY` com contexto/evidência e `spending_allowed=false`; não altera o estado `FAILED`, não executa retries, não chama providers nem envia mensagens.
- Teste novo: `tests/autonomy/test_mission_help_seeking.py`.
- Testes focados: 11 passed. Suite completa após integração: 100%, exit code 0. `py_compile` e `git diff --check` passaram. Avisos de depreciação Starlette/httpx e FastAPI continuam warning-only.
- Limite: a política ainda não está aplicada globalmente em todos os adapters/caminhos de consumo de créditos; ainda falta encaminhamento durável para especialistas e testes end-to-end na fronteira de providers.


## Retoma oficial e revisão de contexto — 2026-10-09

- Correção de nomenclatura: onde notas anteriores dizem “Cloud Free” para o recurso que o utilizador queria preservar, ler **Claude Code Free**. Foi uma rotulagem errada, não um pedido para integrar outro produto. Consultar o log corrigido `DGM-MAT_HELP_SEEKING_ZERO_COST_2026-10-09.md` e os logs Claude Code/FCC antes de qualquer integração.
- DGM-MAT `main` e `origin/main` estavam sincronizados em `7bcf816`; memória `main` e `origin/main` em `9de7ded`. Ambas as árvores estavam limpas no início da retoma.
- Help-seeking: 8 testes próprios aprovados; testes focados política + MissionEngine aprovados; suite completa aprovada (exit code 0, 68,64 s); `compileall` e `git diff --check` aprovados. Backend local `/health` respondeu `healthy`.
- A integração MissionEngine apenas persiste recomendação contextual quando a missão falha. Não representa delegação real a workers nem bloqueio global de fornecedores pagos.
- Lacuna a investigar: o `GovernedProviderService` verifica aprovação duradoura ligada ao pedido e faz uma única chamada limitada, mas a inspeção atual não encontrou verificação obrigatória de custo exato/quota gratuita antes da invocação do adapter. Manter providers safe-off até esta fronteira e os testes negativos serem verificados.
- Foram criadas cópias de segurança dos três ficheiros de memória alterados em `C:\ProgramasGodMode\DGM-MAT-OS\backups\memory-sync-2026-10-09\`; SHA-256 original e cópia coincidem. O espelho imutável `DGM-MAT-FULL-MIRROR` não foi consultado nem alterado.

## Checkpoint 2026-10-09 — Zero-cost provider gate
- Implemented fail-closed provider preflight for explicitly verified free-tier billing and known remaining quota.
- Requires adapter quota reservation before invocation; missing/failed reservations block.
- Cost optimizer now local-first, then verified free provider, otherwise waits; no paid provider fallback.
- Focused tests: governed provider service + request policy + cost optimizer passed.
- Browser AI free-tier fallback remains NOT IMPLEMENTED. Ollama local-first exists in MobileConversationService; external provider adapters reviewed were empty skeletons.
- Policy: DGM-MAT/docs/security/ZERO_COST_PROVIDER_POLICY_2026-10-09.md
- Backups SHA-256 verified at DGM-MAT-OS/backups/zero-cost-provider-gate-2026-10-09. FULL-MIRROR untouched.

- Final verification 2026-10-09: full pytest suite passed after updating the API integration fake to explicitly represent a verified free-tier provider; compileall passed; git diff --check passed. Commit published to DGM-MAT main: 94043c29a4b0dd587be7a8c6938e2baca6e796a0.


## Checkpoint 2026-10-09 — Empresa digital, colaboradores gratuitos e autoevolução
- Clarificação vinculativa do utilizador: DGM-MAT deve funcionar como empresa digital com HQ, departamentos, agentes especialistas por função, memória e aprendizagem persistentes.
- Local/interno primeiro. Claude Code Free, ChatGPT e outras IAs em free mode são colaboradores externos temporários para tarefas delimitadas; rever independentemente e guardar lições validadas.
- Departamento permanente de aquisição/recrutamento: descobrir, avaliar, sandbox, adaptar, testar, rever, promover e registar ferramentas/agentes gratuitos ou criar especialistas internos quando justificado.
- DGM-MAT deve melhorar o próprio código de forma controlada: backup SHA-256, branch/sandbox, testes, revisão independente, promoção e memória; sem auto-modificação irrestrita.
- Ferramentas pagas podem existir para futuro uso autorizado, mas default continua FREE-ONLY / PAID-DENY; sem custo desconhecido, sem fallback pago e sem gastar sem autorização específica.
- Charter: DGM-MAT/docs/DGM-MAT_ENTERPRISE_AUTONOMY_AND_ZERO_COST_CHARTER_2026-10-09.md.
- Limite de realidade: roster não significa agentes independentes ativos; browser multi-IA, delegação durável, recrutamento e autoevolução ponta a ponta ainda exigem implementação e testes.
- Backup dos 7 documentos anteriores verificado por SHA-256 em DGM-MAT-OS/backups/enterprise-architecture-clarification-2026-10-09. FULL-MIRROR intocado.


## Checkpoint 2026-10-09 — Specialist Collaboration Ledger
- Criados `core/organization/specialist_collaboration.py` e `tests/organization/test_specialist_collaboration.py`.
- Pacotes de trabalho persistentes com contexto delimitado, tentativas, evidências, critérios de aceitação e política FREE_ONLY sem fallback pago.
- Registo local atómico, estado de espera por quota gratuita, resultado não confiável até revisão, aprendizagem reutilizável apenas após evidência/revisão independente/testes declarados aprovados.
- Testes focados passaram. A suite completa está em execução neste checkpoint e ainda não deve ser declarada aprovada.
- Ainda não integrado no MissionEngine, dispatcher de departamentos ou browser real de Claude Code/ChatGPT. O ledger não executa os testes por si; a integração tem de fornecer a evidência.
- Documento: `DGM-MAT/docs/DGM-MAT_SPECIALIST_COLLABORATION_LEDGER_2026-10-09.md`.
- Backups SHA-256 dos ficheiros de memória verificados em DGM-MAT-OS/backups/specialist-collaboration-ledger-2026-10-09. FULL-MIRROR intocado.


## Checkpoint 2026-10-09 — MissionEngine handoff connection
- Integrado método explícito `MissionEngine.prepare_specialist_collaboration`.
- Cria e persiste pacote free-only a partir da missão e da recomendação de ajuda; guarda ID/estado no metadata da missão.
- O método não abre browser, não chama fornecedor e não gasta. Estado explícito: `PACKET_PREPARED_NO_EXTERNAL_CALL`.
- Testes focados e suite completa passaram após esta alteração (pytest exit code 0; 60.01 segundos).
- Ainda não é automaticamente disparado por todas as falhas de missão nem está ligado a automação browser real.


## Checkpoint 2026-10-09 — Automatic free-only handoff on failure
- Falha de missão com recomendação `INVESTIGATE_FREE` prepara agora automaticamente um pacote de colaboração, se ainda não existir.
- O ID/estado fica no metadata da missão; sem browser, chamada externa ou gasto.
- Se a preparação falhar, regista `PACKET_PREPARATION_BLOCKED` sem guardar texto potencialmente sensível da exceção.
- Testes focados passaram; suite completa está a ser repetida após esta alteração.


## Verification checkpoint 2026-10-09 — Automatic handoff
- Após integração do handoff automático em falhas `INVESTIGATE_FREE`, testes focados passaram e a suite completa `python -m pytest -q` terminou com exit code 0 em 60.65 segundos.
- Compileall e git diff check passaram.
- Permanecem avisos de depreciação FastAPI/Starlette preexistentes. Browser automation continua por implementar.


## Checkpoint 2026-10-09 — Specialist roster expansion
- Adicionados departamentos browser-automation, cost-governance, self-improvement e local-runtime.
- Adicionados agentes `agent:free-browser-operator`, `agent:cost-guardian`, `agent:self-improvement-engineer` e `agent:local-runtime-engineer`.
- Os quatro estão OFFLINE / ROLE_DEFINED_ONLY até haver execução real testada; não os apresentar como agentes ativos.
- Testes focados de office/foundation passaram; suite completa está a ser repetida após a alteração.


## Verification checkpoint 2026-10-09 — Specialist roster
- Após expansão do roster, testes focados de office/foundation passaram e suite completa `python -m pytest -q` terminou com exit code 0 em 59.95 segundos.
- Compileall e diff check passaram.
- Agentes novos continuam OFFLINE / ROLE_DEFINED_ONLY até integração real testada.


## Checkpoint 2026-10-09 — Specialist result lifecycle
- Adicionados métodos MissionEngine para listar handoffs, pausar por limite gratuito, receber resultados como não confiáveis, pedir revisão independente via message bus interno, rejeitar e validar resultados, e consultar lições validadas.
- Criado `core/organization/validated_learning.py`: persistência atómica local de lições com proveniência e âmbito de projeto; só aceita colaboração VALIDATED.
- Testes focados passaram: `test_mission_specialist_lifecycle.py`, `test_mission_help_seeking.py`, `test_specialist_collaboration.py`.
- Limites: message bus de revisão ainda é process-local/não durável; pedido não prova execução por worker independente; a evidência de testes é uma atestação fornecida pelo chamador, não um runner automático. Browser automation e dispatcher durável continuam pendentes.
- Suite completa foi iniciada; atualizar este checkpoint com resultado final antes do commit.


### Refinement — recovery of lesson persistence
- Adicionado `retry_validated_lesson_persistence`, restrito a colaborações já VALIDATED.
- Teste de regressão simula falha de escrita, confirma que a lição não aparece e depois verifica a recuperação sem repetir a validação nem chamar colaborador.
- Testes focados passaram (13); compileall e diff check passaram. Suite completa a correr após a última alteração.


## Verificação final — 2026-10-09 — Specialist lifecycle
- Testes focados de lifecycle/help-seeking/ledger: 13 passaram.
- Suite completa local `python -m pytest -q`: exit code 0 em 63.28 segundos.
- `compileall` e `git diff --check` passaram para os módulos/testes alterados.
- Avisos de depreciação FastAPI/Starlette permanecem; não bloquearam os testes.
- Nenhum workflow GitHub Actions foi executado.


## Checkpoint 2026-10-10 — Durable message bus / worker dispatch

- Adicionado SQLite persistente a `core/organization/message_bus.py`; MissionEngine aponta para `storage/tasks/organization_messages.sqlite3`.
- Criado `core/organization/worker_runtime.py` com handlers explícitos por agente, despacho de uma mensagem por chamada, acknowledgement apenas após sucesso e falha explícita sem marcar lida.
- API MissionEngine: `register_organization_worker`, `dispatch_organization_message`.
- Novos testes: persistência/reload, estado lido após reinício, proteção contra colisão de IDs, dispatch bem-sucedido, falha não reconhecida e bloqueio de worker não registado.
- O bus de testes de lifecycle é in-memory para não contaminar testes com mensagens antigas do runtime real.
- Limites: at-least-once, handlers precisam ser idempotentes; nenhum agente IA foi automaticamente registado; não chamar esta fase de autonomia multiagente end-to-end. Browser provider, capability pipeline end-to-end e self-improvement continuam por ligar.
- Backup verificado: `C:\ProgramasGodMode\DGM-MAT-OS\backups\durable-message-dispatch-2026-10-10_100758\SHA256-MANIFEST.json`.
- A completar após execução: resultados finais pytest, compileall, diff-check, commit e sincronização PC/GitHub; Actions não devem ser usados.

### Verificação final — durable dispatch (2026-10-10)
- Focados: 23 passed. Suite completa: exit code 0. Compileall e diff-check nas duas repos: exit code 0.
- Warnings FastAPI/Starlette existentes não bloquearam. Actions não utilizados.
- A atualizar este checkpoint após commit e sincronização remota.


## Publicação confirmada — durable dispatch (2026-10-10)

- DGM-MAT `d1e52433fd7848bebd9e7c98e9d5f21b83758cc1` está publicado em `origin/main`.
- Suite completa: exit code 0; focados: 23 passed; compileall e diff-check em DGM-MAT e memória: exit code 0.
- Esta alteração de memória é a atualização associada e será publicada em `AndreVazao/andreos-memory`. Actions não utilizados; FULL-MIRROR intocado.


## Refinement — Durable dispatch receipts (2026-10-10)

- Novo ledger SQLite de receipts: resultado do handler e acknowledgement persistidos atomicamente.
- API `get_dispatch_result(message_id)` para recuperar receipt após reinício.
- Falha do handler ou serialização/persistência do resultado deixa a mensagem unread; sem receipt falso de sucesso.
- Backup SHA-256 verificado em `C:\ProgramasGodMode\DGM-MAT-OS\backups\durable-dispatch-receipts-2026-10-10\SHA256-MANIFEST.json`.
- Testes focados: 24 passed. Suite completa pendente nesta linha de checkpoint.


### Test isolation — durable message bus (2026-10-10)

- Full suite revelou um teste com pressuposto de inbox vazio incompatível com o bus SQLite partilhado entre instâncias. Os testes que não validam persistência agora injetam bus in-memory.
- Backups SHA-256 verificados em `C:\ProgramasGodMode\DGM-MAT-OS\backups\message-bus-test-isolation-2026-10-10\SHA256-MANIFEST.json`.
- Focados capability discovery/help-seeking/mission-system/durable dispatch: 10 passed. Suite completa pendente.


### Verificação final — receipts e isolamento (2026-10-10)

- Focados: 24 + 10 passaram nos grupos de testes relevantes.
- Suite completa: exit code 0. Compileall e diff-check em ambas as repos: exit code 0.
- O bus de produção continua durável; testes que não testam persistência injetam bus in-memory para evitar estado cruzado entre execuções.
- Próximo passo: commit/push da segunda tranche e confirmação final da sincronização.


## Publicação final — durable dispatch receipts (2026-10-10)

- DGM-MAT commit `89cb35c15d05701f8616f446dfc1d773ef7a7929` publicado em `origin/main`.
- Testes focados: 24 e 10 passaram nos grupos relevantes; suite completa exit code 0; compileall e diff-check nas duas repos exit code 0.
- Esta atualização final será publicada em AndreOS-Memory; depois confirmar estado limpo/sincronizado das duas repos. Sem GitHub Actions.
