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


### Verificação adicional do commit local comunicado

O commit `e06d894` é acessível no histórico GitHub e contém:
- `cockpit/api_client.py`, que lê o bootstrap file, troca-o por uma sessão em memória via `POST /auth/session`, e envia `Authorization: Bearer` nos pedidos HTTP;
- `cockpit/streaming/realtime_client.py`, que obtém uma sessão e envia bearer no handshake WebSocket;
- `core/api/api_server.py`, que instala `LocalSessionAuthMiddleware`.

Consequência: um teste manual direto a endpoint privado sem bearer pode devolver 401 de forma correta e não prova, por si só, que o Cockpit está sem sessão. A hipótese a testar no PC passa a ser mais precisa: existência/permissões do bootstrap file, sucesso do exchange `/auth/session`, versão efetivamente executada e eventual divergência entre o processo do Cockpit e o runtime. Não se deve classificar a autenticação como defeito confirmado até observar o fluxo autenticado do próprio cliente.


## 6. Supervisão de 17/11/2026 — relatório das 14:22 UTC

Factos comunicados no relatório diário do operador:
- PC `PC-Vazao-Anjos` offline, última ligação Desktop Commander aproximadamente 17 horas antes; API/runtime, autenticação, scheduler, fila e agentes não foram verificados nesta ronda.
- Não houve missão read-only, respostas reais de agentes, novas conversas recuperadas, validação DGM-HUB nem teste local do atualizador.
- GitHub antes do relatório: 55 branches, 18 PRs abertas, 22 issues abertas (excluindo PRs), 3.870 Actions runs, 25 workflows, main em `2cf91c5`, última integração reportada em 13/11, zero releases. Após o relatório: 56 branches e 19 PRs abertas.
- Artefacto oficial de main reportado: `DGM-MAT-Windows-3.12-2cf91c5`, ID `14075509514`, SHA-256 `40707c10a44971bbf3ae2deaf3bed2d494ff327660eff72bc7e39e592ed5120a`; não descarregado nem instalado.
- PR documental #389: https://github.com/AndreVazao/DGM-MAT/pull/389, draft aberta, ficheiro `reports/DAILY_SUPERVISION_2026-11-17.md`, branch `reports/daily-supervision-2026-11-17`, commit comunicado `45847a7`. Relatório contém 209 linhas segundo o operador.

## 7. Revalidação GitHub posterior ao relatório (17/11)

### PR #385
- HEAD `50e140f2c5307aa3ec53e0ec57351876daf99040`.
- Três validações concluídas com sucesso: Focused Validation #1043 / run `44027120141`; Chrome Extension #527 / run `44027109546`; Windows Build #684 / run `44027109473`.
- CodeRabbit skipped automaticamente. Nenhuma revisão independente foi afirmada.

### PR #386
- HEAD `29eb10712210096804b32bfc34dcf2d0fb039340`.
- Checks confirmados: validate-and-package, Windows installer digest gate, regressões focadas e build Windows, todos success.

### PR #387
- HEAD `f66ab7eb4c37aab101f1c450bbb2b04317307bfa`.
- Checks confirmados: Windows installer digest gate, regressões focadas e build Windows, todos success.

### Reconciliação #385/#386
- Comparação GitHub entre os heads: divergentes, quatro commits exclusivos em cada branch; ambas alteram `tests/api/test_browser_capture_api.py`.
- #386 contém teste multi-provider mais forte: fronteira efetiva desconhecida perante prova inventada, evidência efetiva vazia, preservação dos campos `client_reported_*`, classificação parcial e validação do arquivo persistido.
- #385 mantém teste mais estreito de `history_completeness=partial_or_unknown` e `full_history_verified=false`.
- Recomendação registada nas conversas das duas PRs: tratar #386 como candidata mais completa para fix + regressão; decidir explicitamente se a cobertura adicional da #385 é necessária. Ambas permanecem abertas; sem merge/rebase/fecho.

### Reconciliação #379/#382
- Comparação GitHub entre heads: divergentes, #382 tem 22 commits exclusivos e #379 tem quatro; ambas alteram os mesmos três ficheiros (collector, documento operacional e testes).
- #379: snapshot bounded de trabalho aberto, até dez itens por coleção, duas consultas adicionais.
- #382: histórico recente separado e snapshot open separado; filtra PRs duplicadas da API issues; mede truncation por coleção; inclui testes para casos de fronteira e para trabalho aberto fora da janela histórica.
- #382 é a candidata mais completa, mas tem orçamento de até seis GET sem cache quando checks são consultados. Deve validar custo/latência e degradação parcial. #379 permanece aberta até decisão explícita.
- Comentários de reconciliação adicionados às PRs #379, #382, #385 e #386; nenhum merge, rebase, force-push ou fecho.

### Proteção de main
- API GitHub consultada em 17/11: `main` em `2cf91c5b36a9f7360cf142dc2c60be6ac2f6f18e`, campo `protected=false`; o relatório do operador refere também lista de rulesets vazia.
- Nenhuma alteração à proteção foi efetuada. Requer decisão explícita do operador e definição de checks/regras adequadas antes de configurar.

## 8. Estado e prioridades atualizados

- DGM-MAT permanece **não validado operacionalmente**. O PC offline impede provar API, sessão, fila, execução de missão, providers, captura real, self-update e ligação DGM-HUB.
- Não inferir que os problemas de Codex/Claude/FCC/Ollama continuam iguais hoje; são apenas último estado local conhecido em 16/11, não re-testado em 17/11.
- Ao regressar o PC: preservar working tree e ficheiros untracked; confirmar processos sem os terminar; verificar o bootstrap e fluxo de sessão oficial sem revelar segredos; validar Cockpit autenticado; depois missão read-only com receipt/checkpoint e estado terminal.
- Reconciliar #386/#385 e #382/#379 conforme análise acima, mantendo branches e PRs preservadas até autorização.
- Decidir explicitamente se pretende ativar proteção/rulesets para main; não fazer alterações automáticas.
- Só testar self-update em ambiente controlado, com backup, SHA-256, rollback e aceitação local.
- Não instalar, limpar working tree, matar processos, extrair credenciais, alterar permissões, fazer merge ou fechar PRs sem autorização.


## 9. Integração GitHub — 17/11/2026, 21:56 UTC

Após autorização explícita do operador para executar os merges, foram integradas cinco PRs DGM-MAT por squash merge, cada uma com SHA esperado fixo e confirmação posterior no GitHub:

- #345 — classificação least-privilege de archive/restore mobile; merge `ebdf83141bc4deab97a26b1823d6905b17544605`.
- #386 — fronteira histórica efetiva derivada no servidor; merge `23567e816c2045bc07d1ea73f33d522829851991`.
- #382 — histórico bounded de PRs/issues GitHub e snapshot separado de trabalho aberto; merge `755de4622b9314754447d4a09bef4644e5fee283`.
- #387 — freshness por fonte nos dossiers; merge `018fd78907ab19949e358eaed4b9c458a1b4bf27`.
- #376 — consulta read-only de dossiers do projeto a partir do chat Cockpit; merge `e0247e0039f8fd9976de86e89cb4859d70764b36`.

A branch `main` foi consultada depois da sequência e aponta para `e0247e0039f8fd9976de86e89cb4859d70764b36`. Os cinco PRs foram confirmados como `closed` e `merged=true`.

### PRs preservadas sem merge

- #385 não foi integrada por sobreposição com a cobertura mais abrangente de #386; branch preservada.
- #379 não foi integrada por sobreposição com a versão mais abrangente de #382; branch preservada.
- #347 permanece aberta e não mergeable, com 16 ficheiros numa área sensível de shutdown, autenticação, atualização e rollback; não foi forçada.
- PRs documentais antigas, planos e auditorias permanecem abertas, algumas com base antiga e `mergeable=false`; não foram fechadas nem apagadas.

Foi criada uma única PR documental nova para registar esta consolidação:
- DGM-MAT PR #390: https://github.com/AndreVazao/DGM-MAT/pull/390
- Branch `reports/consolidation-2026-11-17`
- Commit `424faedcd54024f59104b75b5caaf435ee037b52`
- Ficheiro `reports/CONSOLIDATION_2026-11-17.md`
- Base main observada: `e0247e0039f8fd9976de86e89cb4859d70764b36`.

### Limites após integração

- Os checks focados/build Windows dos heads das PRs integradas estavam verdes antes dos merges.
- Não foi feita validação pós-merge no PC; PC-Vazao-Anjos continua offline.
- Não houve missão read-only local, resposta de agentes, recuperação de conversas, teste de sessão autenticada, self-update ou DGM-HUB.
- A integração GitHub não permite declarar DGM-MAT operacionalmente pronto.
- Main protection permanece inalterada; última leitura indicava `protected=false`.

**Estado atualizado:** cinco PRs de código integradas; uma PR documental nova #390 aberta; validação operacional local continua pendente.


## 10. Integração documental adicional — 17/11/2026, 22:05 UTC

Depois dos cinco merges de código/funcionalidade, foram integradas mais onze PRs documentais, após revalidar head SHA, estado e mergeability em cada passo:

- #389 — relatório diário 17/11; merge `b0364c068a12ed61b5d47b9e9b59fc6f2c6557a8`.
- #388 — relatório diário 16/11; merge `c38c17331b85168d31a52b1f41b94084207e2d21`.
- #384 — relatório diário 15/11; merge `d0b8a78aa718538581b19aff583133cc88261018`.
- #383 — relatório diário 14/11; merge `89a67673a3d4c6d328e7ec8faa48761daa35d2ec`.
- #377 — relatório diário 13/11; merge `82aeec4e6bdb219d23601413da22f4b1aefaa312`.
- #368 — relatório diário 12/11; merge `b3d3197d2808d7618a1920f1a7f798847b9ef4e6`.
- #359 — auditoria de recuperação de conhecimento/dossiers; merge `2e1586f9b31ef8fe8e5ca21d1d566adf70abaa4b`.
- #349 — plano de consulta AI em linguagem natural; merge `41d61fcabc4ef800cf5f4efa05d64dbddc5953c5`.
- #346 — relatório diário 11/11; merge `df96918da178df88bcfc83f8c66aaaa3b41ef36d`.
- #344 — registo de readiness do mission executor; merge `c7fade48b613a8a1aaad717f2758ab9dc9bb9fbb`.
- #343 — relatório diário 10/11; merge `4bbbcf462561bbb60b66c570146eeb2cc22d4451`.

Total de integrações nesta ronda: **16 PRs** — cinco de código/funcionalidade e onze documentais.

Continuam abertas/preservadas sem merge:
- #347 — shutdown seguro de update/rollback, 16 ficheiros, mergeability false; requer resolução técnica/revisão antes de integração.
- #379 — sobreposta com #382, que já foi integrada.
- #385 — cobertura de teste sobreposta com #386, que já foi integrada.
- #390 — única PR nova criada para consolidar esta ronda: https://github.com/AndreVazao/DGM-MAT/pull/390, branch `reports/consolidation-2026-11-17`, ficheiro `reports/CONSOLIDATION_2026-11-17.md`. Continua aberta para revisão.
- A branch main foi confirmada após os merges iniciais em `e0247e0039f8fd9976de86e89cb4859d70764b36`; depois houve mais merges documentais, pelo que o HEAD final deve ser novamente consultado e não inferido.

Os merges documentais não alteram a classificação operacional: PC offline, sem prova de runtime, missão real, providers, recuperação de conversas, self-update ou DGM-HUB. Main protection não foi alterada.


## 11. Fecho das PRs redundantes — 17/11/2026, 22:08 UTC

Após os merges de #382 e #386:
- PR #379 foi encerrada como substituída por #382; comentário publicado. Branch `feat/dossier-live-github-work-items` preservada.
- PR #385 foi encerrada como redundante face a #386; comentário publicado. Branch `test/browser-capture-boundary-claims-all-providers` preservada.
- Não foram apagadas branches.
- Permanecem abertas no DGM-MAT: #390 (única PR nova ativa desta ronda) e #347 (draft antiga, não mergeable, shutdown/update/rollback).

Main HEAD observado: `4bbbcf462561bbb60b66c570146eeb2cc22d4451`.


## 12. Reconciliação final e PR única — 18/11/2026, 10:45 UTC

Revisão da antiga PR DGM-MAT #347:
- A funcionalidade de shutdown autenticado está já na main atual: endpoint `POST /runtime/shutdown`, classificação operator-only, sinalização do runtime owner, shutdown Uvicorn, instalador e rollback fail-closed.
- O EventBus atual tem `stop(timeout)`, aguarda o worker e drena a fila; Runtime espera os workers relevantes e o API thread.
- Os testes atuais incluem `tests/api/test_runtime_shutdown.py`, `tests/runtime/test_runtime_shutdown_lifecycle.py` e `tests/operational/test_installer_graceful_shutdown.py`.
- A branch #347 tinha 36 commits exclusivos e 43 commits em falta face à main na comparação observada. O CI focado falhou por colisão de módulos pytest entre dois ficheiros com o mesmo basename. A main já usa `test_runtime_shutdown_lifecycle.py`.
- A PR #347 foi encerrada como supersedida, sem merge/rebase/force-push e sem apagar a branch.

PR documental:
- A PR #390 foi encerrada por ter base histórica antiga.
- A PR #391 é a única PR aberta nova: https://github.com/AndreVazao/DGM-MAT/pull/391
- Branch `reports/consolidation-clean-main-2026-11-18`, criada diretamente do main HEAD `4bbbcf462561bbb60b66c570146eeb2cc22d4451`.
- Commit `4e402f9377dbeff6fbb699b3efdc4e8fc838b6df`.
- Só altera `reports/CONSOLIDATION_2026-11-17.md` (90 linhas adicionadas).
- A PR #391 foi confirmada aberta e mergeable no GitHub.

Estado final de PRs novas: #391 é a única PR aberta. As branches antigas #347, #379, #385 e #390 foram preservadas; PRs #347/#379/#385/#390 encerradas sem merge. Nenhuma branch foi apagada.

A revisão de GitHub não substitui execução local. O PC ainda não foi validado nesta ronda; não há prova nova de runtime, missão read-only, agentes, recuperação de conversas, instalação/rollback ou DGM-HUB.
