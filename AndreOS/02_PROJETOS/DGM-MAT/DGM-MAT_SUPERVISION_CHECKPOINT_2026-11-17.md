# DGM-MAT — Supervisão e reconciliação operacional
**Data:** 2026-11-17  
**Estado:** checkpoint de acompanhamento; validação do PC ainda incompleta.

## 1. Estado do PC comunicado na supervisão de 16/11

Os pontos seguintes foram comunicados pelo operador na supervisão de 2026-11-16, às 14:47 UTC; não foram reexecutados nesta sessão:

- `GET /health` devolveu HTTP 200; endpoints operacionais devolveram HTTP 401.
- Instalação e executável DGM-MAT presentes.
- Dois processos `DGM-MAT.exe` em relação pai-filho; ainda não classificados como supervisor/runtime ou duplicação.
- Checkout local na branch `recovery/local-worktree-consolidation-2026-11-09`, HEAD `e06d894`.
- Working tree com alterações e ficheiros/pastas não versionados; não limpar, resetar, rebasear ou substituir.
- Configuração em ficheiro indica SAFE, `approval_required=true`, `auto_merge_enabled=false`; configuração efetivamente carregada pelo runtime ainda não confirmada.
- Codex CLI 0.130.0-alpha.5: `.fcc/codex-model-catalog.json`, linha 29, contém `reasoning_effort=max`; o esquema aceita `none`, `minimal`, `low`, `medium`, `high`, `xhigh`.
- Claude Code 2.1.112 instalado sem autenticação; FCC não encontrado como comando; Ollama 0.23.0 cliente presente, servidor indisponível.
- Nenhuma resposta real de agente foi obtida; nenhum destes componentes deve ser contado como agente funcional.
- Nenhuma autenticação foi forçada, nenhum processo interrompido e nenhuma instalação alterada.

## 2. Contrato de autenticação encontrado no código GitHub main

Leitura do código da branch `main` em 2026-11-17:

- `core/api/local_auth_api.py` expõe `POST /auth/session`, com bootstrap bearer local e restrição a loopback.
- O bootstrap token é lido de `%LOCALAPPDATA%\DGM-MAT\security\bootstrap.token`, salvo override `DGM_LOCAL_BOOTSTRAP_FILE`; não foi lido nem copiado qualquer segredo.
- O endpoint aplica validação de origem, limite de tentativas e comparação constante do segredo. O cliente não escolhe scopes.
- Para o cliente desktop normal, o servidor atribui `local-client` e `operator`; a sessão normal tem TTL de 30 minutos e é process-local.
- O middleware `core/api/auth_middleware.py` exige bearer session nos endpoints privados. `GET /health` é público.
- Isto descreve o contrato da branch main; não prova que a instalação local na branch/HEAD comunicada contenha exatamente o mesmo código ou que o ficheiro bootstrap exista.
- Próximo passo autorizado deve ser diagnóstico sem revelar segredo: confirmar versão/rotas efetivamente carregadas, existência/permissões do ficheiro bootstrap e se o Cockpit/API client está a enviar o bearer. Só depois, se o mecanismo local estiver presente, emitir uma sessão curta através do endpoint oficial e testar uma leitura operacional. Não extrair cookies, tokens de browser ou credenciais de providers.

## 3. Reconciliação de PRs DGM-MAT

Base observada para as PRs: `main` em `2cf91c5b36a9f7360cf142dc2c60be6ac2f6f18e`.

### PR #385 — teste de alegações de completude multi-provider
- URL: https://github.com/AndreVazao/DGM-MAT/pull/385
- Branch: `test/browser-capture-boundary-claims-all-providers`
- Commit de acompanhamento: `50e140f2c5307aa3ec53e0ec57351876daf99040`.
- Clarificado o âmbito do teste: alegações client-side não podem promover o histórico a completo; o teste não fixa o valor do campo efetivo `oldest_boundary`, porque esse contrato de servidor pertence à PR #386.
- Título atualizado para `test(recovery): reject invented full-history claims across providers`.
- No HEAD `50e140f`, o workflow de digest do instalador passou e os jobs de validação/compilação ainda estavam em execução no momento deste checkpoint. Não declarar CI completa até nova leitura dos check-runs.
- CodeRabbit foi automaticamente skipped; Snyk não é critério de aceitação e permanece excluído por decisão do operador.

### PR #386 — fronteira histórica derivada no servidor
- URL: https://github.com/AndreVazao/DGM-MAT/pull/386
- Branch: `fix/recovery-server-derived-oldest-boundary`
- HEAD previamente verificado: `29eb10712210096804b32bfc34dcf2d0fb039340`.
- Altera API e testes para só aceitar `confirmed` com evidência allowlisted e todos os gates de completude; alegações do cliente são preservadas separadamente como `client_reported_*`.
- CI anteriormente confirmada como success: Focused PR Validation #1037, Chrome Extension Validation #524 e Windows Executable Build #678.
- A lista allowlisted de evidências em produção continua vazia; não inventar marcadores por provider.

### PRs #379 e #382 — dossier GitHub
- Ambas abertas e não integradas; ambas alteram os mesmos três ficheiros: `core/repository_intelligence/github_live_evidence.py`, respetivo documento operacional e testes.
- #379 (HEAD `e4e22b8b961165dc199979426f0da78b75c47377`) acrescenta snapshot limitado dos PRs/issues abertos, com até quatro pedidos GET por dossier sem SHA/checks.
- #382 (HEAD `16cff2fb5090395c1c3d054bd024d999c5ec6048`) acrescenta histórico recente bounded e snapshot separado de itens abertos, com até seis GET por dossier quando inclui checks.
- #382 é a opção mais abrangente; #379 é mais leve e limitado a trabalho aberto. Não são equivalentes: o snapshot aberto separado em #382 evita perder trabalho aberto mais antigo por causa da janela histórica.
- Recomendação para revisão: usar #382 como candidata de consolidação e comparar custo/latência dos pedidos; manter #379 aberta até decisão explícita. Não fechar nem fazer merge automaticamente.

### PR #387 — freshness do dossier
- URL: https://github.com/AndreVazao/DGM-MAT/pull/387
- HEAD `f66ab7eb4c37aab101f1c450bbb2b04317307bfa`.
- CI previamente confirmada success; artefacto Windows gerado, não descarregado nem instalado.
- Dossier expõe timestamps e estados por fonte sem inferir currentness.

## 4. Estado operacional e regras

- O acesso ao PC foi reportado como recuperado, mas a sessão API continua sem autenticação.
- Nenhuma missão read-only foi submetida nesta sessão; nenhuma resposta real de agente, recuperação nova de conversas ou ligação DGM-MAT ↔ DGM-HUB foi confirmada.
- Não tocar no working tree local até criar cópia verificável e inventariar alterações/untracked.
- Não matar processos DGM-MAT antes de identificar pai/filho, argumentos, executáveis e portas.
- Não alterar o catálogo Codex antes de backup e validação do esquema; o valor `max` deve ser substituído apenas após confirmar a intenção semântica (provável `xhigh`, não assumir silenciosamente).
- Não instalar por cima da versão existente até backup de dados/executável, manifesto de hashes, rollback e autorização.
- Nenhuma alteração em `main`, nenhum merge, fecho de PR, reset, rebase, force-push ou eliminação de branches.
- DGM-MAT continua em estado **não validado operacionalmente** até uma missão autenticada terminar e ser verificada, com respostas reais dos agentes e prova de persistência/recuperação.

## 5. Próxima sequência segura

1. Confirmar a build/código efetivamente carregado no PC e o caminho legítimo de emissão de sessão.
2. Diagnosticar o cliente Cockpit/API para localizar a ausência de bearer; não contornar a autenticação.
3. Com cópia/backup e aprovação operacional, emitir uma sessão curta através do bootstrap local oficial e executar apenas leitura.
4. Corrigir `reasoning_effort` no catálogo Codex com backup, validação de schema e teste de invocação real; não contabilizar como funcional sem resposta.
5. Investigar Claude auth, FCC/NIM e Ollama server separadamente; não imprimir tokens nem automatizar login.
6. Identificar os dois processos DGM-MAT sem terminar nenhum.
7. Executar uma missão read-only com receipt/checkpoint e confirmar estado terminal.
8. Consolidar dossiers (#382/#379) e recuperação (#385/#386) em PRs pequenas, com CI verde e sem merge sem autorização.
9. Preservar o working tree e preparar atualização segura apenas depois das provas acima.

---
**Este checkpoint distingue factos comunicados pelo operador, código lido em GitHub e verificações CI. Não representa prova de execução funcional no PC.**
