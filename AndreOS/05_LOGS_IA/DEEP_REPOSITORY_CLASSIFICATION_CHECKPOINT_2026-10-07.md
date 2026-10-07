# Deep Repository Classification Checkpoint — 2026-10-07

## Objetivo

Aprofundar o agrupamento lógico de repos locais e GitHub, deixando de usar apenas nomes e passando a classificar por conteúdo, finalidade, origem e relação arquitetural.

## Fontes auditadas

- `C:\ProgramasGodMode` — inventário local de repositórios Git.
- Repositórios GitHub acessíveis em `AndreVazao`.
- READMEs locais dos repos anteriormente não classificados.
- Remotes Git locais para distinguir repos próprios de clones/upstream.
- Memória canónica `AndreOS/02_PROJETOS/REPOS_TO_PROJECTS.md`.

## Resultado

Novos projetos de memória criados:

- AI_DEVOPS_TOOLING
- BOT_FACTORY
- TRUCKFOOD
- VAZAO_SOVEREIGN_TRADER
- VOCALCLAW
- VORTEXA
- RUVIEW
- SYNTX_26

Também foram identificadas três classes especiais:

### Upstream/reference

- FreeCAD
- Ghost
- freqtrade
- gpt4free

Não devem ser confundidos com produtos próprios apenas por existirem em `C:\ProgramasGodMode`.

### Ferramentas ainda sem classificação suficiente

- ENV-editor
- script-reviewer-mobile
- SheetProPrivate

### Ainda insuficientemente identificado

- ProjectFlux

## Segurança

Foi encontrado um problema nos remotes Git locais: vários repos continham credenciais GitHub embutidas nas URLs de `.git/config`.

Foram normalizados os remotes afetados para URLs GitHub sem credenciais. O conteúdo, histórico e branches dos repos não foram alterados.

Repos afetados: 31.

O `DGM-MAT-FULL-MIRROR` foi explicitamente excluído deste processo.

## Decisão arquitetural

Ferramentas relacionadas com DevOps/AI podem partilhar memória lógica em AI_DEVOPS_TOOLING sem serem automaticamente fundidas no DGM-MAT.

Software upstream permanece separado.

Projetos de produto recebem memória própria.

A regra continua:

**MAPEAR → AUDITAR → CLASSIFICAR → CRIAR MEMÓRIA → VALIDAR → SÓ DEPOIS MIGRAR/FUNDIR.**

## Próximo passo

Auditar os projetos classificados como utilitários, upstream/reference e AI DevOps Tooling com maior profundidade, incluindo dependências, sobreposição funcional e relação GitHub/local, antes de qualquer fusão ou movimento físico.
