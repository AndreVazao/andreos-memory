# AndreOS Memory

Memória persistente canónica do ecossistema AndreOS.

## Regra principal

A memória de desenvolvimento, decisões, arquitetura, contexto e histórico dos projetos vive neste repositório e é sincronizada com:

- Local: `C:\AndreOS-Memory`
- GitHub: `AndreVazao/andreos-memory`

Cada projeto tem a sua própria pasta dentro de `AndreOS/02_PROJETOS/`.

## Estrutura

```text
andreos-memory/
├─ AndreOS/
│  ├─ 00_INBOX/
│  ├─ 01_MEMORIA_NUCLEAR/       # regras e decisões globais
│  ├─ 02_PROJETOS/              # memória separada por projeto
│  │  ├─ DGM-MAT/
│  │  ├─ DGM-MCP/
│  │  ├─ DGM-HUB/
│  │  ├─ OLLAMA/
│  │  ├─ VAZAO-EVSE/
│  │  ├─ BARIBUDOS_STUDIO/
│  │  ├─ BARIBUDOS_STUDIO_WEBSITE/
│  │  ├─ PROVENTIL/
│  │  ├─ N8N/
│  │  └─ outros projetos
│  ├─ 05_LOGS_IA/               # registo de ações e checkpoints
│  ├─ templates/
│  └─ memory.config.json
├─ core/                         # componentes do Memory OS
└─ projects/                     # compatibilidade / projetos auxiliares
```

## Contrato de memória por projeto

Sempre que um projeto tiver trabalho relevante, a sua pasta deve concentrar:

- `MEMORIA_MESTRE.md` — estado consolidado atual.
- `DECISOES.md` — decisões técnicas e de produto.
- `ARQUITETURA.md` — arquitetura quando aplicável.
- `BACKLOG.md` — próximos passos.
- `ULTIMA_SESSAO.md` — último checkpoint operacional.
- `HISTORICO.md` — histórico quando necessário.

Não é obrigatório criar todos os ficheiros; só devem existir quando fizerem sentido.

## Fonte de verdade

A memória persistente do projeto é este repositório Git.

Fluxo normal:

```text
Projeto / sessão
   ↓
Atualizar memória do projeto
   ↓
Validar
   ↓
git commit
   ↓
git push
   ↓
GitHub = cópia persistente
```

Para recuperar contexto:

```text
git pull
→ ler AndreOS/02_PROJETOS/<PROJETO>/
→ continuar trabalho
```

## Separação importante

Este repositório guarda **memória de desenvolvimento e contexto**.

Não deve guardar:

- passwords
- tokens
- API keys
- cookies
- chaves privadas
- credenciais
- dados bancários sensíveis
- ficheiros runtime privados

O estado operacional do PC pode existir localmente, mas a memória necessária para compreender e continuar um projeto deve ser registada aqui.

## DGM-MAT

Todas as repos/componentes do ecossistema DGM-MAT partilham a memória do projeto:

`AndreOS/02_PROJETOS/DGM-MAT/`

Isto inclui Core, Agents, Connectors, Providers, Contracts, Runtime, Orchestrator, Mobile, Plugins, Labs e restantes satélites quando fizerem parte do mesmo produto/ecossistema.

## VAZÃO EVSE

A plataforma VAZÃO EVSE e os seus módulos — carregadores AC, TestStation, CPMS/App, controlo, pagamentos e documentação técnica — usam:

`AndreOS/02_PROJETOS/VAZAO-EVSE/`

## Regra para novos projetos

Antes de iniciar uma nova linha de trabalho relevante:

1. criar a pasta do projeto;
2. criar ou atualizar `MEMORIA_MESTRE.md`;
3. registar decisões importantes;
4. manter a memória sincronizada com GitHub.

## Estado da migração

Em 2026-10-07 a antiga memória local Obsidian foi migrada para este clone Git-sincronizado.

O antigo vault foi preservado em:

`C:\AndreOS-Memory-LEGACY-2026-10-07`

Esse diretório é apenas arquivo de recuperação e não é a fonte principal.
