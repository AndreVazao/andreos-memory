# BARIBUDOS STUDIO - MEMORIA MESTRE

## Objetivo
Dashboard e cerebro operacional para criar, organizar, produzir, publicar e controlar conteudos do ecossistema Baribudos: ebooks, audiobooks, videos, personagens, vozes, sagas, campanhas, produtos, bundles e publicacoes.

## Relação com o website
O Baribudos Studio controla o repo/site `AndreVazao/baribudos-studio-website` atraves de endpoints administrativos e servicos de publicacao, controlo, reconciliacao e estado.

## Repos envolvidos
- Studio: `AndreVazao/baribudos-studio`
- Website: `AndreVazao/baribudos-studio-website`
- Memoria privada: `AndreVazao/andreos-memory`

## Estado implementado em 2026-05-01
Foi adicionada ao repo `baribudos-studio` uma camada de memoria persistente local em Markdown:

- `studio_core/services/persistent_memory_service.py`
- `studio_core/api/routes/persistent_memory.py`
- Router ligado em `studio_core/api/main.py`
- Inicializacao automatica no lifespan do FastAPI
- `storage/memory/` adicionado ao `.gitignore`
- Documentacao criada em `docs/PERSISTENT_MEMORY.md`

## Endpoints de memoria no Studio
- `POST /api/persistent-memory/initialize`
- `GET /api/persistent-memory/projects`
- `POST /api/persistent-memory/projects`
- `GET /api/persistent-memory/projects/{project_name}`
- `POST /api/persistent-memory/decisions`
- `POST /api/persistent-memory/history`
- `POST /api/persistent-memory/backlog`
- `POST /api/persistent-memory/last-session`
- `POST /api/persistent-memory/context`
- `GET /api/persistent-memory/obsidian-uri/{project_name}/{file_name}`

## Projetos criados automaticamente na memoria runtime
- `BARIBUDOS_STUDIO`
- `BARIBUDOS_STUDIO_WEBSITE`

## Regras obrigatorias
- O Studio deve consultar memoria antes de agir sobre conteudo, website ou publicacoes.
- Decisoes importantes devem ser guardadas em `DECISOES.md`.
- Historico de acoes deve ser guardado em `HISTORICO.md`.
- `ULTIMA_SESSAO.md` deve ser atualizado no fim de sessoes relevantes.
- Segredos nunca devem ser guardados na memoria.
- O repo `andreos-memory` e a memoria longa privada para IA/Obsidian.
- A pasta runtime `storage/memory/` do Studio nao deve ir para Git.

## Proximo foco
Criar no dashboard uma zona visual para consultar memoria, gerar contexto para IA e registar decisoes/historico sem mexer diretamente em ficheiros.



## Estado operacional — 18-11-2026

### Repositórios e arquitetura
- Repositórios ativos: `AndreVazao/baribudos-studio` (FastAPI) e `AndreVazao/baribudos-studio-website` (Next.js/Prisma/PostgreSQL).
- Studio é a autoridade editorial/comercial; Website é a montra pública e canal de venda, independente do computador doméstico.
- Sincronização desejada: outbound, autenticada, versionada, checksum, auditável; o Website materializa os bytes antes de publicar.
- Render + Vercel são a arquitetura confirmada; Vercel está ligado ao Website. A conta Render não foi inspecionada nesta execução.
- Repositórios históricos `baribudos-studio-primary` e `baribudos-studio-home-edition` existem, `archived=false`, e permanecem preservados.

### Studio — estado e segurança
- Main observado: `0bf7157cf9c976ed84acb53a965051f944f06f35`.
- P0 ainda aberto: CORS wildcard com credenciais, mount estático da raiz `/storage`, ausência de autenticação global verificada e handlers que confiam em identidade enviada pelo cliente.
- Inventário: 219 rotas ASGI; 233 handlers AST, 29 com referências a identidade do cliente e 97 superfícies sensíveis/operacionais (heurísticas, não prova dinâmica).
- Issue #43 exige matriz manual handler → dependências → serviços → side effects → principal server-side → permissão.
- PR #52 (policy register) continua Draft; CI #529 success, mas não implementa proteção runtime nem completa a matriz handler-to-service.
- PR #56 (canon de personagens) continua Draft; Studio CI #577 e Distribution Hub V6 Smoke #65 success. Revisão identificou que o gate verifica paths não vazios, não existência/confinamento/checksum dos bytes; confirmar também o contrato do tipo `age`.

### Próximo foco
Completar matriz e migração coordenada de credenciais hash, sessões server-side assinadas/expiradas, RBAC, CORS restrito e serving separado de assets públicos/privados. Não aplicar middleware parcial antes da migração dos clientes desktop/mobile.
