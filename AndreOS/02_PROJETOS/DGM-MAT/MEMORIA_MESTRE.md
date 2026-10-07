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
