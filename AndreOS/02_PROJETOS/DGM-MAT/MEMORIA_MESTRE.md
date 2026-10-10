# DGM-MAT — Memória Mestre

## Identidade

DGM-MAT é o núcleo “God Mode” / AndreOS destinado a funcionar como cérebro operacional do PC e, futuramente, como cockpit multi-dispositivo.

## Estado arquitetural atual — 2026-10-07

Princípio de reorganização:

**MAPEAR → CLASSIFICAR → COPIAR/MIGRAR → REESCREVER INTERLIGAÇÕES → TESTAR → COMMITAR → VALIDAR → só depois remover a origem.**

Prioridade:

**estabilidade > funcionalidades; realidade > pressupostos; controlo manual > automação destrutiva.**

## Ecossistema

A memória deste projeto abrange o conjunto DGM-MAT, incluindo quando aplicável:

- Core
- Contracts
- Agents
- Connectors
- Providers
- Runtime
- Orchestrator
- Mobile
- Plugins
- Labs
- Assets
- Deploy
- Cluster
- Marketplace
- Media
- Memory
- Studio
- OS

Estas repos podem continuar independentes no GitHub. A pasta de memória é uma unidade lógica do projeto.

## Checkpoints recentes

### Contracts
- DGM-Contracts deixou de ser apenas placeholder e passou a fornecer contratos públicos.
- Event físico foi migrado para DGM-Contracts.
- ToolDescriptor e fronteira de execução/aprovação foram consolidados.
- SafeActionQueue é candidato à autoridade durável de execução/aprovação.
- EventBus permanece process-local; EventStore persiste; RuntimeStateStore é projeção.

### Agents
- DGM-MAT-Agents foi extraído para pacote independente.
- Core consome os agentes através de uma boundary.
- Foram removidos imports diretos de `core.*` do pacote standalone.
- Testes do pacote e suite principal ficaram verdes.

### Connectors
- ObsidianConnector foi extraído para DGM-MAT-Connectors.
- Runtime API consome o connector através de boundary.
- A implementação standalone não importa `core.*`.
- Suite focada e suite completa ficaram verdes.

### Providers
- Providers ainda não foram fisicamente extraídos.
- A área é demasiado acoplada para uma extração cega.
- Próxima fase: contrato mínimo, facade de serviço no Core, remoção do acesso direto do cockpit ao ProviderRegistry e só depois extração dos adapters.

### GitHub Actions
- Workflows normais ficaram manuais por defeito.
- Release continua dependente de tag.
- Testes locais são a validação normal nesta fase.

## Regra de trabalho

Não alterar `DGM-MAT-FULL-MIRROR`. É arquivo de recuperação.

Não fazer commits de ficheiros locais/untracked sem auditoria individual.

## Memória persistente — checkpoint 2026-10-07

A memória canónica do ecossistema AndreOS passou a ser o clone Git-sincronizado `C:\AndreOS-Memory`, repo `AndreVazao/andreos-memory`.

A pasta `AndreOS/02_PROJETOS/DGM-MAT/` é a memória lógica partilhada por todas as repos/componentes DGM-MAT.

Fluxo obrigatório: `git pull → ler memória → trabalhar → atualizar memória → validar → commit → push`.

O registo transversal de contexto da IA está em `AndreOS/01_MEMORIA_NUCLEAR/REGISTO_MEMORIAS_ASSISTENTE.md`.

## Memória legada

Os documentos antigos foram preservados nesta pasta com nomes `CONTEXTO_LEGACY_*` quando necessário.


## Checkpoint 2026-10-09 — Claude Code terminal recovery

No PC-Vazao-Anjos, o Claude Code nativo 2.1.158 falhava antes da autenticação com `0xC000001D` (illegal instruction) num Intel Pentium Dual-Core T3200. Foi isolado o pacote npm oficial 2.1.112, cuja entrada JavaScript `cli.js` corre via Node.js, e confirmada a versão com exit code 0. Os launchers locais e portáteis, mais os shims globais `claude.cmd`/`claude.ps1`, foram encaminhados para esse CLI compatível e definem `DISABLE_AUTOUPDATER=1`; os shims originais foram guardados em backups datados. O atalho antigo `Claude.lnk` sem destino foi reparado e o menu de opções corrigido. O pacote portátil inclui agora o CLI e foi reconstruído. Ainda falta validar uma sessão autenticada/modelo real, a integração Ollama, FCC/NVIDIA NIM e OmniRoute/Ruflo; não assumir que esses fornecedores/agentes estão funcionais. Ver `AndreOS/05_LOGS_IA/DGM-MAT_CLAUDE_CODE_CPU_COMPATIBILITY_2026-10-09.md` para detalhes e testes.


## FOLLOW-UP — FCC/NVIDIA NIM functional test (2026-10-09)

- FCC server was started and is now responding on the local-only port 8082; `/admin` returned HTTP 200.
- FCC status confirms provider `nvidia_nim` is configured, the selected provider is `nvidia_nim`, and the selected model is `nvidia_nim/nvidia/nemotron-3-super-120b-a12b`; the model catalogue contains 80 entries. Only status/model metadata was read; API key values were never read or printed.
- Functional API smoke test: `fcc-claude -p "Responde apenas com NIM_OK." --output-format text --max-turns 1` returned `NIM_OK`, exit code 0. This verifies a real model response through the FCC/NVIDIA NIM route, not merely a local health check.
- `fcc-claude --version` returned `2.1.112 (Claude Code)`, exit code 0.
- OmniRoute returned version `3.8.51` and Ruflo returned `ruflo v3.55.0`, both with exit code 0. Their version commands work; their broader orchestration workflows still require functional tests.
- Added `DGM-MAT-Environment-Discovery.ps1`, a read-only inventory that records hardware, installed tools, local services, configured NIM status, model name/count, browser skills, launcher targets, and versions without collecting secret values. Reports are written to `%LOCALAPPDATA%\DGM-MAT\reports\` and logs to `%LOCALAPPDATA%\DGM-MAT\logs\`.
- Main DGM-MAT menu now exposes normal Claude Code, FCC/NVIDIA NIM, experimental Ollama, NVIDIA NIM admin UI, project folder, and environment inventory. Added `DGM-MAT-Ensure-FCC-Server.ps1`, `DGM-MAT-FCC-Claude.cmd`, `DGM-MAT-NIM-Admin.cmd`, and a desktop shortcut for the local admin UI.
- Ollama API is currently not responding. It remains an opt-in experimental fallback to avoid consuming RAM on the 2.96 GiB machine.
- The portable ZIP contains the Node-compatible Claude CLI, but does not bundle FCC or any credentials; the FCC/NIM route requires FCC to be installed/configured on the destination PC.


## Checkpoint 2026-10-09 — bootstrap de sessão local da API

A fase B foi avançada localmente: `POST /auth/session` está registada no FastAPI, existe um instalador de credencial bootstrap com ACL Windows restrita e a documentação/registo de validação foram atualizados. Os 16 testes focados e a suite completa passaram; o serviço integrado reiniciou oculto e o health está saudável em `127.0.0.1:8181`. O endpoint live está registado e rejeita pedidos sem credencial (401).

**Limite obrigatório:** a sessão local ainda não é enforcement global. As restantes rotas HTTP/WebSocket e os clientes desktop não foram migrados. A API continua loopback-only; não ativar acesso LAN/Tailscale/público. A emissão válida foi coberta por teste automatizado com segredo temporário, mas não confirmada independentemente contra o servidor live nesta passagem. Ver `AndreOS/05_LOGS_IA/DGM-MAT_LOCAL_SESSION_BOOTSTRAP_2026-10-09.md`.
Publicação: o commit DGM-MAT `d4755b7` foi enviado para `origin/main` depois da suite completa passar. A credencial local não está no Git. A emissão live válida e o enforcement global continuam por validar/implementar.


## Checkpoint 2026-10-09 — escritório DGM-MAT e hardening de execução

O DGM-MAT ganhou uma primeira fundação de escritório digital com papéis especializados, encaminhamento determinístico de tarefas e inventário read-only de repositórios. O Bug Hunter corrigiu dois defeitos de veracidade de estado: tarefas não executadas deixaram de aparecer como `VALIDATED`, e a finalização já não transforma ciclos `FAILED` em `COMPLETED`. O shutdown do ResourceMonitor também foi endurecido para parar/juntar a thread antes do encerramento do executor.

Suite completa após as correções: exit code 0. Testes focados: 19 passed. Backend health continua saudável no loopback (PID 6876). Inventário final: 1.601 ficheiros, 221 diretórios, 117 ignorados; ver `reports/repository_inventory/DGM-MAT_TREE_VERIFIED_2026-10-09.txt`.

Claude Code Free/FCC: manter como possível recurso futuro de apoio ao desenvolvimento, sem integração automática no DGM-MAT. A nomenclatura “Cloud Free” usada numa nota anterior foi um erro. Antes de usar, distinguir o caminho real (Claude Code CLI, FCC/NVIDIA NIM, Ollama ou outro), confirmar quotas/custos e permissões; não inferir gratuitidade por uma chamada bem-sucedida. O DGM-MAT continua prioridade principal.

Inventário final sem auto-referência: 1.597 ficheiros, 220 diretórios, 118 ignorados. Os relatórios finais são `reports/repository_inventory/DGM-MAT_INVENTORY_FINAL_VERIFIED_2026-10-09.json` e `DGM-MAT_TREE_FINAL_VERIFIED_2026-10-09.txt`.

Publicação final: DGM-MAT `9296ea0` e memória persistente `6b7ced9` publicados; repositórios limpos e sincronizados.


## Regra central de autonomia — pedir ajuda de forma inteligente (2026-10-09)

O DGM-MAT não tem de saber tudo; tem de reconhecer limites, procurar a fonte de ajuda adequada e pedir ajuda com contexto suficiente. Em cada missão deve compreender objetivo/restrições/critério de aceitação, consultar memória e evidência antes de perguntar, distinguir factos de hipóteses, escolher primeiro o caminho seguro sem custos, e quando bloqueado formular um pedido concreto com objetivo, tentativas, evidências, bloqueio exato e decisão necessária. Nunca inventar resultados nem declarar concluído o que não executou/verificou. Não consumir créditos, contratar serviços, comprar, expor a API externamente ou executar ações irreversíveis sem autorização explícita. Se não existir caminho seguro/gratuito, manter estado honesto `BLOCKED`/`PARTIAL` e explicar a ajuda necessária. Regra curta: **gratuito por defeito; evidência antes de afirmações; pedir ajuda quando bloqueado; nunca gastar sem autorização**.

Implementação inicial em 2026-10-09: `core/organization/help_seeking.py` define HelpContext, HelpDecision, HelpAction, HelpSeekingPolicy e gate de custos `may_spend`; 8 testes focados passaram. A política ainda não está integrada globalmente no Mission Engine/provider execution; ver `AndreOS/05_LOGS_IA/DGM-MAT_HELP_SEEKING_ZERO_COST_2026-10-09.md`.


### Follow-up — HelpSeeking integrado no MissionEngine (2026-10-09)

A falha de uma missão passa agora a gerar uma recomendação de ajuda persistida em `mission.metadata.help_seeking`: ação sugerida, motivo, próximo passo, pedido de ajuda com contexto e `spending_allowed=false`. A missão continua `FAILED` de forma honesta. O handler não despacha mensagens, não faz retries automáticos, não chama providers e não gasta dinheiro. Suite completa após a integração: 100% verde, exit code 0; testes focados de ajuda/lifecycle: 11 passed. Limite: ainda não é enforcement global de todos os providers/caminhos pagos, nem encaminhamento real para workers. Ver `AndreOS/05_LOGS_IA/DGM-MAT_HELP_SEEKING_ZERO_COST_2026-10-09.md`.


## Continuidade oficial — revisão documental e correção de contexto (2026-10-09)

Nome correto do recurso externo referido nas conversas recentes: **Claude Code Free** (incluindo o ecossistema Claude Code/FCC quando o contexto o especificar). A referência anterior a “Cloud Free” foi um erro de transcrição/rotulagem; não existe instrução para integrar um produto chamado Cloud Free. Não iniciar integração automática do Claude Code Free no DGM-MAT: primeiro rever as evidências e limites registados em `AndreOS/05_LOGS_IA/DGM-MAT_CLAUDE_CODE_CPU_COMPATIBILITY_2026-10-09.md`, `DGM-MAT_HELP_SEEKING_ZERO_COST_2026-10-09.md`, `DGM-MAT_GOVERNED_PROVIDER_EXECUTION_2026-10-09.md` e `CLAUDE_CODE_DASHBOARD_2026-10-09.md`. Uma resposta curta `NIM_OK` comprova uma chamada funcional específica através de FCC/NVIDIA NIM, não garante quota gratuita nem custo zero contínuo. O dashboard registou também uma saída CLI que reportou custo de `$0.100344`, sem confirmação de faturação real; verificar limites e métricas antes de novas chamadas de maior consumo.

### Estado verificado na retoma — 2026-10-09

- DGM-MAT local: `C:\ProgramasGodMode\DGM-MAT`, `main` sincronizada com `origin/main`, HEAD `7bcf816` (`feat: record help recommendations on mission failure`); árvore limpa no início da auditoria.
- Memória local: `C:\AndreOS-Memory`, `main` sincronizada com `origin/main`, HEAD `9de7ded` (`docs: record MissionEngine help-seeking integration`); árvore limpa no início da auditoria.
- `core/organization/help_seeking.py` e `tests/organization/test_help_seeking.py` existem; os 8 testes específicos passaram.
- Testes focados de política + MissionEngine e suite completa passaram com exit code 0; a suite completa demorou 68,64 s. `compileall` e `git diff --check` passaram.
- Backend `http://127.0.0.1:8181/health` respondeu `healthy` em loopback.
- O MissionEngine regista recomendação em `mission.metadata.help_seeking` quando uma missão falha; isto não equivale a delegação real, nem a enforcement global de custo/autorizações.
- O roster/delegation continua uma fundação determinística de organização, não prova que todos os especialistas sejam agentes de IA independentes e ativos.
- A API permanece local; não abrir LAN/Tailscale/público sem autenticação e autorização aplicadas globalmente a HTTP/WebSocket e clientes migrados.
- Nenhuma alteração de código ou commit foi feita nesta auditoria. Antes de editar ficheiros existentes, criar backup e verificar SHA-256 em `C:\ProgramasGodMode\DGM-MAT-OS\backups\memory-sync-2026-10-09\` (os três documentos de memória anteriores foram copiados e os hashes original/cópia coincidiram).

### Prioridade técnica seguinte

1. Ler e reconciliar a documentação e memórias de arquitetura, governança, API security, provider registry, provider execution, help-seeking, headless runtime, desktop/mobile boundaries e Claude Code/FCC antes de novas mudanças estruturais.
2. Auditar o custo na fronteira real de execução. `GovernedProviderService` verifica a aprovação duradoura associada à impressão digital do pedido, limites de entrada/saída e timeout, mas o código lido não demonstra uma verificação obrigatória de custo/quota/preço antes de chamar o adaptador. Não declarar proteção financeira global concluída.
3. Verificar os caminhos de chamada e contratos existentes antes de alterar interfaces; preservar providers em safe-off até os gates estarem cobertos por testes de integração.
4. Implementar testes negativos que provem que custo desconhecido, quota não comprovada, aprovação ausente/inválida, falha do armazenamento ou limite excedido impedem qualquer chamada ao adaptador.
5. Só depois atualizar código, executar suite, atualizar documentação/memória e publicar commits verificados.

Proibição permanente: não aceder nem modificar `C:\ProgramasGodMode\DGM-MAT-FULL-MIRROR`.

## 2026-10-09 — Zero-cost provider execution gate

Binding user requirement: **local first; then legitimate browser-based AI free tiers; never spend money or credits; when free limits are reached, wait or use another verified free route. No paid fallback or upgrade without an explicit new policy change.**

Implemented in DGM-MAT:
- Provider execution rejects any external provider unless cost profile is explicitly 'free', billing mode is 'free_tier', cost verification is exactly true, quota usage/limit are known and remaining, and the adapter implements 'reserve_free_quota()' returning exactly true.
- Unknown pricing/quota, paid API mode, exhausted quota, missing reservation, and reservation errors fail closed before provider invocation.
- Base provider cost defaults to 'unknown'.
- ProviderCostOptimizer now chooses 'local-first', a verified free provider with remaining quota, or 'wait-for-free-capacity'; it no longer recommends Claude Sonnet as a paid fallback.
- Focused tests passed for governed provider service, provider request policy, and cost optimizer (results recorded in the 2026-10-09 session).

Important reality check:
- MobileConversationService tries local Ollama first (subject to memory checks) and otherwise returns deterministic fallback text; it does not yet use browser AI sessions.
- AIClient2API and gpt4free adapters are empty skeletons.
- No production external provider adapter with verified free-tier quota reservation exists. The new policy blocks such calls until a real adapter implements the contract. Do not claim browser multi-provider fallback is finished.
- Remote API authentication/session enforcement remains a separate blocker; do not expose the backend remotely.

Policy document: C:\ProgramasGodMode\DGM-MAT\docs\security\ZERO_COST_PROVIDER_POLICY_2026-10-09.md.
Backup: C:\ProgramasGodMode\DGM-MAT-OS\backups\zero-cost-provider-gate-2026-10-09; original files were SHA-256 verified before editing. Never touch C:\ProgramasGodMode\DGM-MAT-FULL-MIRROR.


## 2026-10-09 — Binding architecture clarification: DGM-MAT as a company

The user reaffirmed that DGM-MAT must operate like a digital company, with departments and one clearly owned specialist agent/function wherever justified, internal communication, shared workspace, HQ orchestration, quality/review, and persistent institutional/project/agent learning. It must be as internal/local as practical and never spend by default.

External tools/AI collaborators (including Claude Code Free and ChatGPT) are temporary specialist employees/consultants, not the permanent brain. DGM-MAT assigns them bounded work with context, attempted steps and acceptance tests, reviews the result independently, and stores reusable validated lessons so it does not ask the same question repeatedly. Do not assume unsupported APIs; browser use must be legitimate, authorized and within provider terms.

The organization must have an open Capability Acquisition/Recruitment department that can discover existing local/GitHub/Labs capabilities, sandbox and adapt them, test/review/promote them, or create a new internal agent when a real gap is identified. DGM-MAT must also improve its own code with internal agents and free external help through backups + SHA-256, branch/sandbox, tests, independent review, controlled promotion and persistent learning; never unrestricted self-modification.

Tool availability is not spending authorization. Keep FREE-ONLY / PAID-DENY as default even if paid tools/adapters are configured for future use. Unknown pricing/quota, exhausted free quota, or failed checks must block paid/external invocation and wait or ask for help. No subscription, paid API, credit spend, upgrade or paid fallback without specific explicit authorization.

Normative charter: DGM-MAT/docs/DGM-MAT_ENTERPRISE_AUTONOMY_AND_ZERO_COST_CHARTER_2026-10-09.md.
Reality check: current roster/delegation is not proof of independent active agents; browser-based multi-provider work, durable delegation, capability recruitment and self-improvement loop remain incomplete until end-to-end tested. Never touch DGM-MAT-FULL-MIRROR.


## 2026-10-09 — Specialist collaboration ledger implemented

Added `core/organization/specialist_collaboration.py` and focused tests. It creates durable local task packets for internal or external specialists, includes goal/project/department/role/context/facts/attempts/evidence/constraints/acceptance criteria, exports an explicit FREE_ONLY / no-paid-fallback policy, persists handoff records atomically, can pause on exhausted free capacity, stores returned results as untrusted, and only records a reusable lesson after independent review evidence and a passing-test attestation. It rejects common credential/session-secret patterns and does not invoke browser, network, providers or paid tools.

Focused tests and the complete pytest suite passed (full suite exit code 0; 63.39 seconds). Compileall and git diff --check were also run successfully for the new module and tests. This is now connected to MissionEngine through an explicit handoff-preparation method, but not yet to live browser automation and not automatically triggered by all mission failures. The validation method records review/test evidence but does not execute tests itself; integration must provide evidence. JSON persistence is local/single-process for now.

Specification: `DGM-MAT/docs/DGM-MAT_SPECIALIST_COLLABORATION_LEDGER_2026-10-09.md`.
Backups for existing memory files verified with SHA-256 at `C:\\ProgramasGodMode\\DGM-MAT-OS\\backups\\specialist-collaboration-ledger-2026-10-09`. FULL-MIRROR untouched.


## 2026-10-09 — MissionEngine handoff connection

MissionEngine now exposes `prepare_specialist_collaboration(mission_id, ...)`. It builds a bounded handoff from mission goal/description, existing help request, recent logs, known facts and acceptance criteria; includes strict FREE-ONLY constraints; persists the collaboration record; and links the collaboration ID/status into mission metadata. Default suggested collaborator is Claude Code Free. This method prepares a packet only and does not open a browser, call an AI or spend. Status is explicitly `PACKET_PREPARED_NO_EXTERNAL_CALL`. Focused integration tests and the complete pytest suite passed after this change (full suite exit code 0; 60.01 seconds). Not yet automatically triggered for all mission failures.


## 2026-10-09 — Automatic free-only handoff on mission failure

MissionEngine now automatically prepares a specialist collaboration packet when a mission failure results in `INVESTIGATE_FREE` and no handoff already exists. The packet is local and FREE_ONLY, and its ID/status is attached to mission metadata. Preparation failures fail closed with `PACKET_PREPARATION_BLOCKED` and no sensitive exception text. This does not call Claude/browser or any external provider. Focused tests passed; full suite verification is running after this change.


Verification update — 2026-10-09: after automatic failure handoff integration, focused tests passed and full `python -m pytest -q` completed with exit code 0 in 60.65 seconds. Compileall and git diff check passed. Existing FastAPI/Starlette deprecation warnings remain. Browser automation is still not implemented.


## 2026-10-09 — Specialist department roster expanded

Expanded `core/organization/office.py` with four departments and role records: Browser Automation / `agent:free-browser-operator`; Cost & Quota Governance / `agent:cost-guardian`; Self-Improvement Engineering / `agent:self-improvement-engineer`; Local Runtime & Models / `agent:local-runtime-engineer`. These new agents are explicitly OFFLINE and marked `ROLE_DEFINED_ONLY` until their real execution adapters/workflows are implemented and tested. This is deliberate: a role record is not evidence of an active independent worker. Existing delegation is deterministic assignment, not execution. Focused office/foundation tests passed; full suite is running after this roster change.


Verification update — 2026-10-09: after expanding the office roster, focused office/foundation tests passed and the full `python -m pytest -q` suite completed with exit code 0 in 59.95 seconds. Compileall and diff check passed. The four new specialist roles remain OFFLINE / ROLE_DEFINED_ONLY pending actual worker adapters and independent integration tests.


## 2026-10-09 — Specialist result lifecycle and validated learning

MissionEngine now has local lifecycle methods for listing collaborations, pausing on free-capacity limits, recording specialist results as untrusted, requesting independent review through the in-process bus, rejecting results, validating with independent reviewer/evidence/test attestation, and listing validated lessons. Added `core/organization/validated_learning.py`, an atomic JSON store under the configured runtime `evolution_memory/validated_specialist_lessons`. It refuses packets not marked VALIDATED and preserves project scope, collaborator provenance, reviewer notes, acceptance criteria and timestamp.

Safety boundaries: no browser/provider calls or spending. The QA message is in-process and not durable; it does not prove that a real independent worker executed review. `tests_passed=True` records caller-provided evidence and is not itself a test runner. Browser automation and a durable cross-process dispatcher remain unimplemented. If validated lesson persistence fails, the API reports `PERSISTENCE_FAILED` explicitly instead of claiming memory promotion.

Focused local tests passed for the new lifecycle, previous help-seeking integration and collaboration ledger. Full suite was started after the integration; final verification and synchronization are pending.


### Recovery refinement — validated lesson persistence

Added `MissionEngine.retry_validated_lesson_persistence(collaboration_id)` to recover from a failed local lesson write after a collaboration has already passed independent validation. It refuses non-VALIDATED collaborations and retries only the memory persistence step; it does not re-call the collaborator or repeat validation. A regression test simulates storage failure and successful recovery. Focused lifecycle/help-seeking/ledger tests passed (13 tests) with compileall and diff check. Full suite is running after this final refinement.


Final verification — 2026-10-09: after adding retryable validated-lesson persistence, focused lifecycle/help-seeking/collaboration tests passed (13 tests); complete local `python -m pytest -q` passed with exit code 0 in 63.28 seconds. `compileall` and `git diff --check` passed. Existing FastAPI/Starlette deprecation warnings remain. No GitHub Actions workflow was run.


## Checkpoint 2026-10-10 — Mensagens duráveis e despacho explícito

- Backup SHA-256 verificado antes das alterações: `C:\ProgramasGodMode\DGM-MAT-OS\backups\durable-message-dispatch-2026-10-10_100758\SHA256-MANIFEST.json`; inclui message bus, MissionEngine, testes e documentos anteriores. O teste de lifecycle foi também salvaguardado e o hash da cópia confirmou.
- `core/organization/message_bus.py` passou para SQLite, mantendo API de inbox/outbox e estado de leitura; o caminho de produção é `storage/tasks/organization_messages.sqlite3`. Os dados persistem entre instâncias/reinícios.
- Criado `core/organization/worker_runtime.py`: despacho real para handlers Python explicitamente registados; não interpreta mensagens como código, comandos ou instruções de ferramentas. Sucesso marca leitura; falha fica por reconhecer.
- MissionEngine expõe `register_organization_worker` e `dispatch_organization_message`, além de permitir injeção de bus para testes isolados.
- Semântica: entrega at-least-once. Um handler pode repetir se o processo cair antes do acknowledgement; handlers têm de ser idempotentes. IDs duplicados com conteúdo conflitante são recusados.
- Limite: o mecanismo de despacho está implementado, mas ainda não há Bug Hunter IA automaticamente registado/ativo. Mensagem durável não prova que houve revisão independente. Browser/Claude Code Free, aquisição de capacidades ponta a ponta e autoaperfeiçoamento controlado continuam pendentes.
- FREE-ONLY / PAID-DENY mantido. Sem Actions; testes locais primeiro. `DGM-MAT-FULL-MIRROR` continua intocável.

### Verificação final — 2026-10-10 — durable dispatch
- Testes focados: 23 passaram (bus durável, foundation, specialist ledger/lifecycle e help-seeking).
- Suite completa `python -m pytest -q`: exit code 0; `python -m compileall -q core tests`: exit code 0; `git diff --check` nas duas repos: exit code 0.
- Warnings preexistentes de depreciação FastAPI/Starlette, não bloqueantes.
- Sem GitHub Actions. Commit/push e estado de sincronização devem ser registados após conclusão.


## Publicação confirmada — durable dispatch (2026-10-10)

- DGM-MAT commit `d1e52433fd7848bebd9e7c98e9d5f21b83758cc1` (`feat: persist organization messages and dispatch workers`) foi enviado com sucesso para `AndreVazao/DGM-MAT` `main`.
- Suite completa local passou com exit code 0; 23 testes focados passaram; `compileall` e `git diff --check` nas duas repos passaram. Warnings FastAPI/Starlette preexistentes não bloquearam.
- Memória atualizada neste ciclo e preparada para commit/push em `AndreVazao/andreos-memory`. Nenhum GitHub Actions executado. `DGM-MAT-FULL-MIRROR` intocado.


## Refinement 2026-10-10 — Durable worker result receipts

- Segundo backup SHA-256 verificado antes de alterações: `C:\ProgramasGodMode\DGM-MAT-OS\backups\durable-dispatch-receipts-2026-10-10\SHA256-MANIFEST.json` (6 ficheiros originais e cópias coincidem).
- O bus SQLite passou a persistir `organization_dispatch_receipts`; `WorkerRuntime` guarda resultado JSON-safe e acknowledgement na mesma transação SQLite. `get_dispatch_result(message_id)` permite recuperar o resultado depois de reiniciar.
- Se o handler falhar ou o resultado não puder ser persistido como JSON, a mensagem fica por reconhecer e não há receipt de sucesso. A semântica continua at-least-once: um crash entre o efeito externo do handler e a transação de receipt pode causar repetição, por isso handlers devem ser idempotentes.
- Testes focados após esta refinação: 24 passaram. Suite completa, compileall, diff-check, commit e sincronização serão registados quando terminarem.


## Refinação — isolamento de testes do bus durável (2026-10-10)

- A primeira suite completa após receipts detetou uma falha de teste, não uma falha do runtime: `test_mission_capability_discovery` assumia inbox vazio apesar de mensagens persistidas por execuções anteriores.
- Backups SHA-256 verificados em `C:\ProgramasGodMode\DGM-MAT-OS\backups\message-bus-test-isolation-2026-10-10\SHA256-MANIFEST.json` (3 ficheiros).
- Testes de capability discovery, help-seeking e mission-system agora injetam `InternalMessageBus()` in-memory; o runtime normal continua SQLite durável. A suite focada após isolamento passou (10 testes).
- A suite completa tem de ser repetida após esta correção antes de novo commit/push.


## Verificação final — receipts e isolamento (2026-10-10)

- Testes focados do despacho durável/foundation/lifecycle: 24 passaram; testes capability discovery/help-seeking/mission-system/durable dispatch: 10 passaram.
- A suite completa `python -m pytest -q` voltou a passar com exit code 0 após corrigir o isolamento dos testes que dependem de inbox vazio. `compileall` e `git diff --check` nas duas repos também passaram.
- Avisos FastAPI/Starlette são warnings de depreciação preexistentes, não bloqueantes.
- O código da segunda tranche (receipts duráveis e isolamento de testes) ainda precisa de commit/push; Actions não utilizados.


## Publicação final — durable dispatch receipts (2026-10-10)

- Segunda tranche publicada em `AndreVazao/DGM-MAT` `main`: commit `89cb35c15d05701f8616f446dfc1d773ef7a7929` (`feat: persist worker dispatch receipts`).
- Inclui receipts de resultado persistentes, acknowledgement atómico e isolamento dos testes para que o estado durável de produção não contamine testes não relacionados.
- Suite completa local passou com exit code 0 depois da correção de isolamento; grupos focados passaram (24 e 10 testes). `compileall` e `git diff --check` nas duas repos passaram. Actions não utilizados.
- Publicar agora esta atualização final em `AndreVazao/andreos-memory`; confirmar ambas as repos limpas e sincronizadas.


## QA Intake Worker — 2026-10-10

- Backup SHA-256 verificado antes da alteração; manifesto no diretório de backups `qa-intake-worker-2026-10-10` (7/7 ficheiros).
- Criado `core/organization/qa_intake_worker.py`: handler determinístico que recebe pedidos de revisão, valida campos básicos e emite receipt durável `REVIEW_QUEUED` com próximos passos.
- Ligado ao MissionEngine e ao método `dispatch_pending_review_intake()`. Mantém compatibilidade com o inbox histórico `agent:bug-hunter`, mas não é um Bug Hunter autónomo.
- A resposta declara `independent_review_performed=false`, `tests_executed=false` e `lesson_promotion_allowed=false`; não inspeciona código, não corre testes nem promove lições. Revisão real permanece separada.
- Testes focados: 11 passaram. Suite completa: exit code 0; compileall e diff-check nas duas repos: exit code 0. Warnings FastAPI/Starlette preexistentes não bloquearam. Sem Actions ou chamadas externas de IA.


### Checkpoint 2026-10-10 — Fila persistente de revisão QA

Implementada `core/organization/qa_review_queue.py` com SQLite e estados PENDING/IN_PROGRESS/BLOCKED/COMPLETED/REJECTED. A fila regista correlação, mensagem de origem, missão, prioridade, responsável, tentativas/limite, timestamps, motivo de bloqueio, resultado explícito, verificações executadas e evidências. O `MissionEngine` liga a fila persistente em `tasks/qa_review_queue.sqlite3` ao `QAIntakeWorker`; a entrada da revisão cria item durável antes de confirmar a mensagem. Conclusão exige responsável atual, estado IN_PROGRESS, outcome, pelo menos uma verificação realmente registada e evidência. Receção de mensagem não equivale a revisão concluída. Limite honesto: infraestrutura de fila e intake determinístico; ainda não é um revisor IA independente.


## Checkpoint 2026-10-10 — Coordenador de revisão QA independente

- Integrado `core/organization/qa_review_coordinator.py` no `MissionEngine` através de métodos explícitos para preparar revisão, executar verificações locais, finalizar PASS/FAIL e reconciliar persistência de lições.
- A revisão só aceita colaboração persistida em `RESULT_RECEIVED` e revisor diferente do colaborador original. Resultado e proveniência externos são dados não confiáveis; nunca são executados como comandos.
- Verificações fixas: `git diff --check`, `python -m compileall -q core tests`, `python -m pytest -q`, sempre `shell=False` e timeout limitado. PASS exige correspondência exata com os registos da execução local atual, todos os exit codes a zero, notas de revisão e evidência.
- FAIL pode registar verificações falhadas e rejeita a colaboração sem promover lição. PASS valida a colaboração, persiste a lição e só depois conclui a fila. Se a escrita da lição falhar depois da validação, o item fica IN_PROGRESS e pode ser reconciliado sem repetir colaboração.
- Testes novos em `tests/test_qa_review_coordinator.py`: separação do revisor, fronteira de confiança, execução sem shell, promoção de lição com PASS, rejeição de evidência forjada, bloqueio de PASS com testes falhados e FAIL sem promoção.
- Testes focados iniciais concluídos com exit code 0. A suite completa, compileall, diff-check, backup SHA-256, publicação GitHub e confirmação de sincronização ficam pendentes até terminar a verificação.
- Não ativado Claude Code nem qualquer chamada externa: não era necessário para esta etapa local. FREE-ONLY / PAID-DENY, sem Actions e sem tocar em `DGM-MAT-FULL-MIRROR`.


### Verificação final — coordenador QA independente — 2026-10-10

- Testes focados do coordenador, fila QA e lifecycle de colaboração passaram com exit code 0.
- Suite completa local `python -m pytest -q`: exit code 0, runtime 65,36 s. Warnings FastAPI/Starlette de depreciação continuam não bloqueantes.
- `python -m compileall -q core tests`: passou.
- `git diff --check`: passou em DGM-MAT e AndreOS-Memory.
- Backup e manifesto SHA-256 em `C:\\ProgramasGodMode\\DGM-MAT-OS\\backups\\qa-review-coordinator-2026-10-10\\SHA256-MANIFEST.json`; hashes de origem/cópia coincidiram. O manifesto será atualizado após este registo.
- Commit/push e confirmação final de sincronização continuam pendentes neste ponto. Nenhuma GitHub Action foi executada.


### Publicação — coordenador QA independente — 2026-10-10

- DGM-MAT publicado em `AndreVazao/DGM-MAT` na branch `main`, commit `033c181` (`feat: add independent QA review coordinator`).
- O push foi confirmado pelo Git e o repositório local DGM-MAT ficou limpo/alinhado com `origin/main` após o push.
- A suite completa passou (exit code 0), compileall e diff-check passaram, e o backup SHA-256 teve 6 ficheiros com 0 divergências antes da atualização documental final.
- Falta publicar esta atualização em AndreOS-Memory e fazer a verificação final dos dois repositórios.


### Publicação — coordenador QA independente — 2026-10-10

- DGM-MAT publicado em `AndreVazao/DGM-MAT` na branch `main`, commit `033c181` (`feat: add independent QA review coordinator`).
- Push confirmado pelo Git e repositório local DGM-MAT limpo/alinhado com `origin/main` após o push.
- Suite completa passou (exit code 0); compileall e diff-check passaram; backup SHA-256 teve 6 ficheiros e 0 divergências antes da última atualização documental.
- Falta publicar esta atualização em AndreOS-Memory e confirmar o estado final dos dois repositórios.


### Sincronização final — 2026-10-10

- DGM-MAT: commits `033c181` (coordenador QA) e `c0c7bcd` (registo documental) publicados em `AndreVazao/DGM-MAT` `main`; push confirmado e branch local limpa/alinhada com `origin/main`.
- Verificação local: suite completa exit code 0; compileall e diff-check passaram; backup `C:\\ProgramasGodMode\\DGM-MAT-OS\\backups\\qa-review-coordinator-2026-10-10\\SHA256-MANIFEST.json` contém 6 ficheiros, 0 divergências.
- Esta memória está a ser publicada em `AndreVazao/andreos-memory`; confirmar o estado limpo/alinhado após push.
- Sem GitHub Actions, sem chamadas externas/consumo de créditos e sem acesso a `DGM-MAT-FULL-MIRROR`.


## Checkpoint 2026-10-10 — Browser Automation / Web UIs gratuitas

- Implementado `core/providers/browser/governed_browser_session.py` com Playwright e integrado localmente no MissionEngine: iniciar sessão, navegar, ler texto renderizado, clicar, preencher campos normais, scroll, screenshot, pedir OCR e fechar sessão.
- Sessões Playwright não persistentes/em memória; sem exportação de cookies/storage state. Allowlist explícita de hosts HTTPS, bloqueio de IPs privados/loopback/reservados e URLs com credenciais embutidas. Preenchimento de passwords, tokens, API keys, cartões, OTP e outros campos sensíveis é recusado.
- Limites: máximo de três sessões por MissionEngine, timeouts e tamanhos de input limitados, screenshots restritos a diretório de artefactos e nomes simples. Nenhum CAPTCHA/MFA/paywall/limite de fornecedor é contornado.
- Testes focados `tests/test_governed_browser_session.py` passaram; compileall passou.
- OCR: interface integrada com `pytesseract`/Pillow quando já instalados, mas a inspeção do PC não encontrou pytesseract nem executável Tesseract. Portanto OCR de screenshot está **INDISPONÍVEL e não verificado** nesta máquina; a função reporta isso sem instalar software automaticamente. Leitura de texto DOM funciona sem OCR quando a página expõe HTML acessível.
- A API/cockpit ainda não expõe estas operações; permanece intencionalmente bloqueada até terminar a migração global de autenticação. Não foi feita sessão real de login de IA web, nem foi consumido crédito, nem chamada API paga.
- Próximos passos: obter/validar um motor OCR local gratuito; ligar as ferramentas ao cockpit apenas com auth/scopes e aprovação de ações; construir o liaison de IA web com política FREE-ONLY / PAID-DENY; testar workflow real com utilizador presente, sem bypass de limites.


## Checkpoint 2026-10-10 — Browser Web UIs + OCR local (atualização)

- Serviço de browser governado implementado e integrado localmente no MissionEngine: navegação HTTPS por allowlist, leitura de texto renderizado, click, fill apenas em campos não sensíveis, scroll, screenshot e OCR. Sessões Playwright efémeras, sem persistência/exportação de cookies; máximo três sessões por instância.
- Tesseract instalado via WinGet pacote `UB-Mannheim.TesseractOCR`, versão 5.4.0.20240606. SHA-256 do instalador verificado pelo WinGet: `c885fff6998e0608ba4bb8ab51436e1c6775c2bafc2559a19b423e18678b60c9`.
- Modelo de idioma português obtido de `tesseract-ocr/tessdata` (GitHub oficial): `por.traineddata`, 15.336.931 bytes, SHA-256 `016C6A371BB1E4C48FE521908CF3BA3D751FADE0AB846AD5D4086B563F5C528C`. `tesseract --list-langs` confirmou `eng`, `osd`, `por`.
- OCR invoca Tesseract diretamente com subprocesso sem shell e timeout 30s; evitada dependência Python pytesseract porque a importação de NumPy do ambiente local falhou por DLL. O wrapper pytesseract foi removido depois de detetar esse problema; requirements.txt fica sem essa dependência.
- Prova end-to-end local em imagem sintética: OCR `por+eng` extraiu `DGM MAT OCR TEST 123 - PORTUGUES`. Imagem temporária removida. Nenhuma imagem foi enviada para fora.
- Política: nenhum preenchimento de passwords/tokens/API keys/cartões/OTP, nenhum bypass de CAPTCHA/MFA/paywall/limites/termos. Nenhum crédito ou API paga. Cockpit/API ainda não expõe browser até auth global e scopes estarem prontos.
- Testes focados e suite completa, compileall, diff-check, backup SHA-256, commit/push e sincronização final estão a ser executados/verificados neste checkpoint; só marcar como concluído após saída real das ferramentas.


### Browser security refinement — 2026-10-10

- Added context-level request guard: every request, redirect and subresource must remain HTTPS and inside the explicit host allowlist; unauthorized requests are aborted.
- Added unit coverage for authorized subdomain, cross-domain and non-HTTPS request handling.
- Focused browser suite now passes 14 tests. Live Chrome → HTTPS navigation → page-text extraction → screenshot → local Portuguese/English OCR passed with HTTP 200. Temporary screenshot removed.
- Full test suite is running again after the final request-guard/Chrome launch changes; do not treat publication as complete until it exits successfully.


### Final verification — browser automation + OCR — 2026-10-10

- Browser tests: 14 passed.
- Full DGM-MAT suite after the final request-guard change completed at 100% with process exit code 0 (runtime 68.01 s).
- `python -m compileall -q core tests` passed; `git diff --check` passed.
- Live browser E2E passed: installed Chrome, HTTPS allowlisted navigation to example.com (HTTP 200), rendered text extraction, viewport screenshot, and local `por+eng` OCR. Temporary screenshot deleted.
- Tesseract 5.4.0.20240606 and Portuguese language data installed locally; OCR model hash is recorded in the architecture doc and backup manifest.
- Existing FastAPI/Starlette deprecation warnings are non-blocking.
- Final backups, documentation/memory publication, commits/pushes and clean/synchronized branch verification are now being completed. No GitHub Actions were run, no paid APIs/credits used, no provider login attempted, and no access to DGM-MAT-FULL-MIRROR.


### Publicação e sincronização final — 2026-10-10

- DGM-MAT commit `24c8707` (`feat: add governed browser automation and local OCR`) publicado em `AndreVazao/DGM-MAT`, branch `main`; push confirmado, working tree limpa e HEAD alinhado com origin/main.
- Testes focados browser: 14 passed. Suite completa após a última alteração de segurança: exit code 0, 100% (runtime 68,01 s). `compileall` e `git diff --check` passaram.
- Browser E2E verificado em Chrome instalado: navegação HTTPS autorizada (HTTP 200), extração de texto, screenshot e OCR local `por+eng` aprovados. Sem login real em fornecedores de IA, sem chamadas pagas e sem créditos gastos.
- Tesseract 5.4.0.20240606; modelo português SHA-256 `016C6A371BB1E4C48FE521908CF3BA3D751FADE0AB846AD5D4086B563F5C528C`.
- Backup `C:\\ProgramasGodMode\\DGM-MAT-OS\\backups\\governed-browser-ocr-2026-10-10\\SHA256-MANIFEST.json`: 8 ficheiros, 0 divergências antes desta última atualização da memória; atualizar manifesto/cópia antes de encerrar.
- Próxima fase continua: ligar o browser ao cockpit com auth/scopes e aprovação, e criar o liaison de IA web que usa sessões gratuitas legítimas, sem assumir que a integração end-to-end já existe. Não executar GitHub Actions. `DGM-MAT-FULL-MIRROR` permanece intocado.


## Requisito obrigatório — intervenção humana pelo telefone e retoma segura (2026-10-10)

O DGM-MAT deve agir autonomamente dentro do âmbito autorizado, mas pedir intervenção no cockpit móvel quando um passo exigir o titular da conta (autenticação, CAPTCHA/MFA, consentimento ou confirmação). O pedido identifica a missão/passo, apresenta instruções claras e permite aprovar, rejeitar ou cancelar. Se o telefone estiver offline/dessincronizado, a missão mantém checkpoint durável e espera; após reconexão, valida sessão/dispositivo e sincronização estável antes de aceitar a resposta. Deve confirmar o resultado real e retomar do ponto seguro, sem duplicar missões nem repetir automaticamente ações externas de resultado incerto.

Segurança: CAPTCHA/MFA é resolvido manualmente pelo utilizador, sem bypass. O atual `browser_fill` continua a recusar campos sensíveis. Não colocar valores secretos em prompts, logs, message bus genérico, screenshots, memória ou artefactos. Qualquer canal futuro de input sensível tem de ser autenticado, cifrado, temporário, estritamente ligado a uma única sessão/pedido/campo, sem persistência e com eliminação após uso; preferir input direto do utilizador na sessão viva. Notificações não podem revelar dados sensíveis. Nenhum controlo de browser remoto até auth global HTTP/WebSocket, scopes, emparelhamento/revogação de dispositivos e aprovação estarem implementados e testados.

Documento canónico: `docs/architecture/HUMAN_IN_THE_LOOP_HANDOFF.md`. Maturidade atual: **ESPECIFICADO; NÃO IMPLEMENTADO END-TO-END**. Próxima fase: auditar o bootstrap de sessão e todos os clientes HTTP/WebSocket; desenhar autenticação global e emparelhamento; implementar fila durável/estados anti-replay; só depois pop-up móvel, sincronização e retoma segura. Manter FREE-ONLY / PAID-DENY, sem Actions e sem tocar em `DGM-MAT-FULL-MIRROR`.


### Clarificação obrigatória — intervenção direta do telefone na sessão viva (2026-10-10)

O objetivo não é apenas enviar uma notificação: quando for seguro e possível, o cockpit móvel deve permitir que o utilizador veja/interaja com a sessão ativa do browser e que a sua ação deliberada seja entregue ao separador/campo autorizado no PC. O canal deve ser dedicado, temporário e protegido, ligado ao utilizador/dispositivo/sessão/origem/missão/passo/pedido de uso único. Conteúdo sensível nunca passa pelo modelo de IA, payload genérico, message bus comum ou logs, e deve ser descartado após entrega. CAPTCHA/MFA é resolvido manualmente pelo utilizador; o DGM-MAT só transporta a interação humana, não resolve nem contorna o desafio. Se não for seguro ou compatível com o serviço, explicar a limitação e pedir conclusão na sessão legítima antes de verificar e retomar.


## Checkpoint 2026-10-10 — Fila persistente de intervenção humana (primeira implementação)

- Criado no DGM-MAT: `core/organization/human_intervention_queue.py`; testes em `tests/organization/test_human_intervention_queue.py`; documentação em `docs/architecture/HUMAN_INTERVENTION_QUEUE_IMPLEMENTATION.md`.
- SQLite/WAL, pedidos duráveis e com TTL, índice único parcial por missão/passo ativo, decisões únicas ligadas à missão/passo, expiração e estado `VERIFYING` antes de finalizar. Conexões fechadas explicitamente por operação.
- Validação: 7 testes dedicados e 15 testes focados de regressão passaram; `compileall` e `git diff --check` passaram.
- Estado honesto: componente implementado e testado isoladamente; ainda não integrado ao MissionEngine, não muda estado da missão, não notifica o telefone, não liberta workers e não retoma execução automaticamente. Nenhum endpoint HTTP/WebSocket foi adicionado.
- API permanece loopback-only até auth global HTTP/WebSocket, emparelhamento, scopes, identidade de dispositivo, revogação, anti-replay e migração dos clientes estarem implementados e testados.
- Chamadores não podem colocar segredos em `reason`/`instructions`; sem passwords, OTPs, cookies ou tokens no LLM, bus, logs, DB ou memória. CAPTCHA/MFA manual; verificar o estado real antes de retomar ação externa.
- Próximo passo: integrar checkpoint/estado de espera ao MissionEngine e permitir que delegações independentes continuem, com testes de reinício/concorrência; depois resolver auth global antes do cockpit.
- Restrições: FREE-ONLY / PAID-DENY; sem GitHub Actions; `DGM-MAT-FULL-MIRROR` intocado.


## Checkpoint 2026-10-10 — MissionEngine, checkpoints e intervenção humana

- Integração local: `MissionStatus.WAITING_FOR_USER` e `CANCELLED`; fila SQLite/WAL inicializada pelo MissionEngine; métodos `request_human_intervention()` e `resolve_human_intervention()` com binding de missão/passo/operador.
- Uma missão à espera é ignorada pelo ciclo de scheduler, sem timeout de espera e sem bloquear a iteração das restantes. A aprovação não retoma sem verificação externa explícita e evidência breve não sensível; rejeição/cancelamento fecha a missão; `NEED_CONTEXT` cria novo handoff.
- JSON de missão agora guarda/reconstrói subtarefas e grava atomicamente (temporário, flush/fsync, replace). Arranque reconcilia pedidos SQLite órfãos e recupera retoma verificada interrompida; claims de verificação sem checkpoint verificado voltam a exigir verificação.
- Testes: bateria focada 22/22; suites `autonomy`, `organization`, `contracts`, `security`: 104/104 aprovados, zero falhas. `compileall` e `git diff --check` passaram.
- Docs: `docs/architecture/MISSION_ENGINE_HUMAN_INTERVENTION_CHECKPOINTS.md`; testes em `tests/autonomy/test_mission_human_intervention.py`.
- Limites: não há endpoint remoto, notificação móvel ou verifier real de browser integrado. `verified=True` é exclusivamente para um verifier local de confiança; não expor à API/cockpit remoto. O estado da missão retoma, mas execução automática de subtarefas depende dos workers existentes.
- Próxima ordem: reforço de concorrência/crash; API local read-only para cockpit PC; fechar auth HTTP/WebSocket; cockpit PC; APK Android após pairing/transport security. Tailscale para rede privada; Vercel só rendezvous.
- FREE-ONLY / PAID-DENY; sem portas públicas; `DGM-MAT-FULL-MIRROR` intocado; sem GitHub Actions.


## Checkpoint 2026-10-10 — PC cockpit realtime

- Corrigido arranque do WebSocket do cockpit Qt: asyncio corre em thread dedicado; callbacks e hidratação inicial passam por sinais Qt para atualizar widgets apenas na GUI thread.
- Fecho da janela pede fecho do WebSocket sem parar o Core; stop-before-connect é terminal para evitar corrida.
- `tests/cockpit`: 7 aprovados; compileall e diff-check passaram. É validação do cliente/testes, não E2E com runtime ativo.
- Documento: `docs/architecture/PC_COCKPIT_REALTIME_CONNECTION.md`.
- API default `127.0.0.1`; não expor em LAN/Tailscale, porque auth global HTTP/WebSocket está incompleta e CORS é permissivo. Não adicionar mutações de intervenção remotas ainda.
- Próximos passos: live local E2E; vista de intervenções com API local autenticada; pedidos HTTP não bloqueantes; depois pairing/Tailscale e APK.
