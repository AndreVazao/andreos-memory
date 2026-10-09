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

Cloud Free: manter apenas como possibilidade futura de agente/provider; utilizador informou mudanças estruturais significativas. Não integrar nem alterar sem revisão read-only posterior. O DGM-MAT continua prioridade principal.

Inventário final sem auto-referência: 1.597 ficheiros, 220 diretórios, 118 ignorados. Os relatórios finais são `reports/repository_inventory/DGM-MAT_INVENTORY_FINAL_VERIFIED_2026-10-09.json` e `DGM-MAT_TREE_FINAL_VERIFIED_2026-10-09.txt`.

Publicação final: DGM-MAT `9296ea0` e memória persistente `6b7ced9` publicados; repositórios limpos e sincronizados.


## Regra central de autonomia — pedir ajuda de forma inteligente (2026-10-09)

O DGM-MAT não tem de saber tudo; tem de reconhecer limites, procurar a fonte de ajuda adequada e pedir ajuda com contexto suficiente. Em cada missão deve compreender objetivo/restrições/critério de aceitação, consultar memória e evidência antes de perguntar, distinguir factos de hipóteses, escolher primeiro o caminho seguro sem custos, e quando bloqueado formular um pedido concreto com objetivo, tentativas, evidências, bloqueio exato e decisão necessária. Nunca inventar resultados nem declarar concluído o que não executou/verificou. Não consumir créditos, contratar serviços, comprar, expor a API externamente ou executar ações irreversíveis sem autorização explícita. Se não existir caminho seguro/gratuito, manter estado honesto `BLOCKED`/`PARTIAL` e explicar a ajuda necessária. Regra curta: **gratuito por defeito; evidência antes de afirmações; pedir ajuda quando bloqueado; nunca gastar sem autorização**.

Implementação inicial em 2026-10-09: `core/organization/help_seeking.py` define HelpContext, HelpDecision, HelpAction, HelpSeekingPolicy e gate de custos `may_spend`; 8 testes focados passaram. A política ainda não está integrada globalmente no Mission Engine/provider execution; ver `AndreOS/05_LOGS_IA/DGM-MAT_HELP_SEEKING_ZERO_COST_2026-10-09.md`.


### Follow-up — HelpSeeking integrado no MissionEngine (2026-10-09)

A falha de uma missão passa agora a gerar uma recomendação de ajuda persistida em `mission.metadata.help_seeking`: ação sugerida, motivo, próximo passo, pedido de ajuda com contexto e `spending_allowed=false`. A missão continua `FAILED` de forma honesta. O handler não despacha mensagens, não faz retries automáticos, não chama providers e não gasta dinheiro. Suite completa após a integração: 100% verde, exit code 0; testes focados de ajuda/lifecycle: 11 passed. Limite: ainda não é enforcement global de todos os providers/caminhos pagos, nem encaminhamento real para workers. Ver `AndreOS/05_LOGS_IA/DGM-MAT_HELP_SEEKING_ZERO_COST_2026-10-09.md`.
