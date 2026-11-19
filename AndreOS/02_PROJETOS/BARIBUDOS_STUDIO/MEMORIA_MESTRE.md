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


## Checkpoint operacional — 19-11-2026

### Repositório e integrações
- Main confirmado: merge commit Studio PR #60 `3596b655daa1d9efb6466a62b12d6926a7986207` e PR #61 `cc7067695573792690e2321dffcfe8ca2f7743f8`.
- PR #60 separa audiobook da minissérie: factory, pipeline manual e export route não passam audiobook para o renderer; o resolver falha fechado até existir ledger de aprovação imutável server-owned.
- Todos os MP4 atuais são `animatic_only`, `finalizable=false`, bloqueados pela ausência de animação real. Testes cloud são fixtures sintéticas, zero aprovações editoriais.
- PR #60: Distribution Hub V6 Smoke #76, Studio CI #616 e Story Production Cloud Validation #39 passaram no head antes do merge. Não foram encontrados workflows pós-merge para os merge commits.
- PR #61 versionou `docs/security/STUDIO_HTTP_SECURITY_SURFACE_2026-11-19.md`; Studio CI #622 (backend-validate e frontend-build) passou antes do merge.

### Segurança P0 — evidência de runtime
- Artifact CI #616: 78 módulos route; 233 handlers AST; 233 sem sinal auth local heurístico; 29 referências a campos de identidade cliente; 97 sinais sensíveis/operacionais.
- Manifest runtime: 219 APIRoute entries + 6 HTTP non-APIRoute; 2 mounts StaticFiles; zero global FastAPI dependencies e zero top-level dependency edges reportados.
- CORS: wildcard origins, credentials=true, wildcard methods/headers. Mounts `/public` e `/storage` com autorização não verificada pelo manifest.
- Os números são evidência de inventário, não prova dinâmica de exposição. A matriz manual handler→dependency→service continua incompleta (issue #43). Não foi alterada auth, CORS, storage, dados ou credenciais.

### Próxima frente
Completar a matriz manual e desenhar rollout compatível de hash credentials, signed/expiring sessions, RBAC, CORS restrito e serving público/privado; não aplicar remendos parciais. Continuar a animação real, ledger editorial e approvals sem declarar minisséries finais a partir de animatics.
