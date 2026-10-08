# Registo de Memórias do Assistente

**Consolidação:** 2026-10-07  
**Fonte:** contexto persistente de trabalho + memória Git local + decisões registadas no ecossistema AndreOS.

Este documento é operacional e não contém credenciais ou segredos.

## 1. Preferências de trabalho

- Entregáveis completos e funcionais; evitar esqueletos, placeholders e instruções genéricas.
- Quando houver código, indicar o caminho exato do ficheiro.
- Decisões técnicas devem partir do estado real dos repositórios e dos testes.
- No DGM-MAT: **estabilidade > funcionalidades; realidade > pressupostos; controlo manual > automação destrutiva**.
- Testes locais são a validação normal; GitHub Actions só quando necessário ou explicitamente pedido.
- Alterações destrutivas exigem controlo e validação antes de remover a origem.
- `C:\ProgramasGodMode\DGM-MAT-FULL-MIRROR` é arquivo de segurança e **não deve ser alterado**.

## 2. Memória persistente

Fonte canónica:

- local: `C:\AndreOS-Memory`
- GitHub: `AndreVazao/andreos-memory`
- branch: `main`

Fluxo:

`git pull → ler memória → trabalhar → atualizar memória → validar → commit → push`

A antiga memória Obsidian foi preservada em `C:\AndreOS-Memory-LEGACY-2026-10-07` apenas para recuperação.

## 3. DGM-MAT

### Objetivo

DGM-MAT é o núcleo operacional/God Mode do ecossistema AndreOS. A visão é um sistema estilo cockpit/Jarvis:

- cérebro executado no PC;
- cockpit no PC e futuramente no telemóvel;
- pesquisa, programação, testes, Git/GitHub, configuração, reparação e organização de projetos;
- arquitetura multi-agente;
- controlo de permissões;
- memória persistente;
- sincronização multi-dispositivo.

### Ecossistema

As repos podem continuar independentes no GitHub, mas partilham a memória lógica:

`AndreOS/02_PROJETOS/DGM-MAT/`

Abrange Core, Contracts, Agents, Connectors, Providers, Runtime, Orchestrator, Mobile, Plugins, Labs, Assets, Deploy, Cluster, Marketplace, Media, Memory, Studio, OS e componentes relacionados.

### Regra de reorganização

`MAPEAR → CLASSIFICAR → COPIAR/MIGRAR → REESCREVER INTERLIGAÇÕES → TESTAR → COMMITAR → VALIDAR → só depois remover a origem.`

### Estado arquitetural — 2026-10-07

- DGM-Contracts é um pacote real de contratos públicos.
- Event foi fisicamente encaminhado para DGM-Contracts.
- ToolDescriptor e fronteira de execução/aprovação foram consolidados.
- SafeActionQueue é candidato à autoridade durável de execução/aprovação.
- EventBus continua process-local; EventStore persiste; RuntimeStateStore é projeção.
- DGM-MAT-Agents foi extraído para pacote independente e consumido por boundary.
- DGM-MAT-Connectors foi extraído para pacote independente; ObsidianConnector é consumido por boundary.
- Providers ainda **não** foram fisicamente extraídos. Próxima fase: contrato mínimo, facade no Core, remoção do acesso direto do cockpit ao ProviderRegistry e só depois extração dos adapters.
- Workflows GitHub normais estão manuais por defeito; release continua dependente de tag.
- Suite local DGM-MAT foi validada a 100% no checkpoint de 2026-10-07.

### Segurança operacional

Não alterar `DGM-MAT-FULL-MIRROR`.

Não fazer commits de ficheiros locais/untracked sem auditoria individual.

## 4. DGM-HUB e DGM-MCP

### DGM-HUB

Projeto independente tratado como legacy/research/reuse source. Não deve ser importado integralmente para DGM-MAT.

### DGM-MCP

Sistema especializado de transporte/interface MCP e controlo de PC.

Fronteira preferida:

`Cockpit / Agent / cliente externo → contratos DGM-MAT → execução/ferramentas controladas → PC`

DGM-MAT não deve depender de classes privadas do runtime DGM-MCP.

## 5. VAZÃO EVSE

VAZÃO EVSE é uma plataforma modular de carregamento AC.

Abrange:

- carregadores simples, duplos e quádruplos;
- wallboxes;
- futuras multistations;
- hardware e quadros elétricos;
- BOM e produção;
- controlo local;
- CPMS;
- aplicação de cliente;
- RFID;
- pagamentos;
- smart charging;
- arquitetura master/slaves;
- TestStation Mini, PRO e Factory;
- diagnóstico, assistência e produção.

Toda a plataforma usa:

`AndreOS/02_PROJETOS/VAZAO-EVSE/`

## 6. ProVentil

Projeto empresarial em Portugal para serviços técnicos, com foco inicial em motores de extração de restaurantes e videoporteiro.

As regras de negócio detalhadas devem permanecer na memória própria do projeto.

## 7. Baribudos

Ecossistema de conteúdo infantil:

- canal: ViralVazao;
- produção: Baribudos Studio;
- marca: Os Baribudos;
- selo: As Histórias que Protegem.

As várias frentes devem manter memória própria quando forem projetos independentes, preservando a ligação ao ecossistema.

## 8. Ferramentas e ambiente

- Desenvolvimento principal em Windows.
- GitHub CLI autenticado no PC.
- Remote Desktop Commander usado para operações autorizadas no PC.
- Tailscale usado no ecossistema DGM-MAT para acesso entre PC e telemóvel.
- Fluxos mobile-friendly são importantes quando o trabalho puder ser feito a partir do telemóvel.

## 9. Regra para a IA

A IA deve tratar `C:\AndreOS-Memory` como memória persistente central.

Antes de continuar um projeto:

1. sincronizar a repo;
2. identificar a pasta de memória correta;
3. ler o contexto relevante;
4. executar o trabalho;
5. atualizar o registo do projeto;
6. atualizar o registo transversal se a decisão afetar vários projetos;
7. sincronizar para GitHub.

Uma decisão relevante não deve ficar apenas no histórico da conversa.


## 10. Script Comparator / Consolidador de Scripts

Foi definido um módulo reutilizável para resolver famílias de scripts geradas durante desenvolvimento iterativo.

Local canónico da memória:
`AndreOS/02_PROJETOS/SCRIPT_COMPARATOR/`

Funções principais:

- comparar várias versões do mesmo ficheiro;
- agrupar por nome base + extensão;
- escolher uma versão-base por completude estrutural;
- recuperar funcionalidades ausentes;
- detetar conflitos;
- validar o resultado;
- criar backup;
- renomear versões para `base001.ext`, `base002.ext`, etc.;
- reservar `base.ext` para o resultado consolidado.

Regra importante: não fazer merge cego por número de linhas nem anexar indiscriminadamente linhas de diff ao fim do ficheiro.

O núcleo foi desenhado sem GUI para poder ser integrado em DGM-MAT, Build Control Center, script-reviewer-mobile ou outras aplicações AndreOS.


## 11. Sincronização GitHub + Desktop Commander — checkpoint 2026-10-07

A memória persistente `C:\AndreOS-Memory` foi sincronizada com `AndreVazao/andreos-memory` através de fast-forward de `origin/main`. O clone local ficou em `b232848` e sem alterações pendentes.

O Desktop Commander está autorizado no PC Windows para continuar a auditoria dos projetos locais. A regra operacional passa a ser:

`sync → ler memória → inspecionar estado real → trabalhar → validar → documentar → commit → push → confirmar sync`

A sincronização de projetos locais deve ser conservadora: alterações locais não auditadas, branches divergentes e repositórios com risco de perda não devem ser sobrescritos automaticamente.

Detalhes do checkpoint: `AndreOS/05_LOGS_IA/SYNC_GITHUB_DESKTOP_COMMANDER_2026-10-07.md`.


## 12. Auditoria de remotos locais — checkpoint 2026-10-07

A auditoria pelo Desktop Commander encontrou 17 clones locais com o remote genérico https://github.com/AndreVazao/.git. Os remotos foram corrigidos para os repositórios correspondentes do GitHub e a pesquisa final deixou de encontrar esse URL genérico.

Foram preservadas as regras de não forçar merges, não publicar branches locais sem auditoria e não criar commits artificiais em repos GitHub vazias. DGM-Contracts ficou explicitamente a seguir origin/main; mantém apenas __pycache__ não versionado, sem alteração destrutiva.

Detalhes: AndreOS/05_LOGS_IA/AUDITORIA_REMOTOS_GIT_2026-10-07.md.


## 13. DGM-MAT — Conversation recovery and program assembly protocol — checkpoint 2026-10-08

The DGM-MAT operating procedure is now explicitly ordered as:

LIST conversations → CREATE per-conversation context vaults → RELATE conversations across providers → CLUSTER project threads → RENAME/GROUP → RECOVER scripts by browser scrolling when necessary → STAGE artifacts by project → DISCOVER/VERIFY local and GitHub repository → GENERATE <PROJECT>_TREE.txt → ASSEMBLE code into correct files/modules → CONSOLIDATE competing AI implementations → MAP the real program → AUDIT → TEST/REPAIR → VALIDATE → PERSIST MEMORY → SYNCHRONIZE → RESUME from idempotent checkpoint.

Initial browser/local provider scope: ChatGPT, Grok, Claude/Claude Code, Gemini and DeepSeek. Paid provider APIs are not required for the primary acquisition path.

The key invariant is **context travels with code**: provenance, surrounding reasoning, cross-provider corrections, project identity and later decisions must remain attached to recovered artifacts.

Detailed protocol: AndreOS/05_LOGS_IA/DGM-MAT_CONVERSATION_RECOVERY_PROTOCOL_2026-10-08.md and DGM-MAT/docs/DGM-MAT_CONVERSATION_RECOVERY_AND_PROJECT_ASSEMBLY.md.

DGM-MAT-FULL-MIRROR remains immutable. Consequential/destructive operations remain approval-gated.
