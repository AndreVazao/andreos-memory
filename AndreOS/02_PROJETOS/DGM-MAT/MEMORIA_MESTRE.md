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
