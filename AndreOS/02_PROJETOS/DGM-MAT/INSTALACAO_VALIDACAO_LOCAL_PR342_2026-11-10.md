# DGM-MAT — instalação e validação local pós-PR #342 — 2026-11-10

## Código e artefacto oficial

- Repositório: `AndreVazao/DGM-MAT`.
- Main validada: `fdae0ce102c35d15ff3c4564039bdd4396aa139a`.
- PR #342 integrada; Issue #341 resolvida.
- Windows Executable Build pós-merge: run `42806219347`, SUCCESS.
- Mission E2E Regression Gate pós-merge: run `42806219343`, SUCCESS em Ubuntu e Windows.
- Artefacto: `DGM-MAT-Windows-3.12-fdae0ce`, ID `13757993868`, 115,278,337 bytes.
- SHA-256 do ZIP do artefacto: `c12ec6c6cb01e37f862101063ed420e5e8a3f1f9ea0c39c248710d71f757c3e2`.
- SHA-256 do ZIP interno do pacote: `E0D18FD4683B80374F84E13A698B345DA5921A3544E0399BB5680CCF3AC23887`.
- SHA-256 do executável: `97C4B1FCA805E884C3AFEF54902D047F700254F96989632502C65849DD44D675`.

## Instalação no PC-Vazao-Anjos

- Destino: `C:\\ProgramasGodMode\\DGM-MAT\\installed\\DGM-MAT.exe`.
- O artefacto foi descarregado para staging local; os hashes externo, interno e do EXE foram verificados antes da instalação.
- O instalador oficial `scripts/install_windows_update.ps1` executou com sucesso. Atualizou EXE e launcher de serviço.
- SHA-256 final do EXE instalado, verificado novamente após instalação: `97C4B1FCA805E884C3AFEF54902D047F700254F96989632502C65849DD44D675`.
- Launcher: `C:\\ProgramasGodMode\\DGM-MAT\\scripts\\autostart\\backend_service.py`; SHA-256 `34BA311953BA9CD0CA55FE74E4098C535B6A71F83AE1331040A7C73201D9883A`.
- Backup/manifesto: `C:\\ProgramasGodMode\\DGM-MAT\\update-backups\\20261110-125511\\INSTALL-MANIFEST.json`.
- O instalador preservou runtime, recovery inbox, diagnostics, reports, recovery ledger SQLite, DGM-MAT-Memory, memory_sync, storage/runtime, .runtime, logs e launcher anterior. Security/bootstrap e worktrees foram deliberadamente mantidos intactos.
- Os processos antigos do executável foram parados pelo instalador seguro, que verificou o listener/API antes da substituição. Novo runtime arrancado com `--headless`.

## Validação local pós-instalação

- `GET http://127.0.0.1:8181/health`: `{"status":"healthy","service":"dgm-mat"}`.
- Listener 8181: loopback `127.0.0.1`, PID observado `2364`.
- `POST /auth/session` com bootstrap local: sessão autenticada obtida com sucesso.
- `GET /runtime/status`: `status=running`, `is_degraded=false`, `missions_active=0`; agentes repo/provider/autonomy inicializados.
- `GET /runtime/queue`: `worker_alive=true`, thread_count 1, handler `MISSION_EXECUTION`.
- Processos do EXE verificados: PID 6052 e processo filho 2364, ambos a executar o executável instalado e argumento `--headless`.
- A atualização terminou com exit code 0 e mensagem `INSTALL_AND_HEALTH_CHECK_COMPLETE`.

## Ressalva sobre a fila histórica

- A fila persistente foi preservada, não limpa nem reexecutada.
- Foram observadas ações históricas #6 e #7, marcadas COMPLETED no nível da fila, mas cujo resultado interno da missão é `failed` / `NotImplementedError`: o plano tinha sido criado sem executor genérico registado. A mensagem de resultado confirma que subtarefas eram propostas e não foram executadas.
- As ações antigas #1–#5 permanecem QUEUED e sem aprovação; não foram reexecutadas.
- Isto é histórico anterior à instalação e não invalida o health/runtime/worker atual. A PR #342 introduz readiness `WAITING_FOR_CAPABILITY` para evitar criar nova ação aprovável sem executor real. A validação desta sessão não submeteu uma missão nova nem testou um executor de missão real.

## Limites de aceitação

- Confirmados: instalação oficial, hashes, backup/manifesto, preservação dos dados, API, autenticação, runtime full, estado não degradado e worker durável ativo.
- Não confirmados nesta sessão: aceitação visual/interativa do cockpit, E2E Chrome/extensão, consulta real a providers, captura integral dos históricos de seis IAs ou execução de uma missão de escrita real.
- Não alterar nem apagar as ações históricas sem revisão explícita. Manter o backup para rollback.
- Snyk continua fora do gate por quota mensal gratuita esgotada, conforme instrução explícita do operador.

## Próximos passos

1. Aceitação do cockpit desktop após abrir o atalho atualizado, sem alterar dados.
2. Testar nova conversa e pesquisa do histórico local com uma operação read-only e confirmar persistência/restart.
3. Investigar separadamente as ações históricas pendentes e o resultado de missões sem executor; não reexecutar automaticamente.
4. Atualizar o dossier principal de continuidade com referência a este relatório.



## Seguimento — cockpit e runtime autenticado — 2026-11-10 19:20 UTC

### PC e cockpit

- PC-Vazao-Anjos online; `GET /health` continua HTTP 200.
- Checkout local observado em `C:\\ProgramasGodMode\\DGM-MAT`: branch `recovery/local-worktree-consolidation-2026-11-09`, HEAD `e06d89402d9e3cd6e36a189daa3f13bee8c4d413`.
- Working tree não limpo: `scripts/autostart/backend_service.py` modificado e ficheiros não rastreados, incluindo `installed/`, backups, vários diretórios update-staging e artefactos de recuperação. Nenhuma operação Git foi executada; preservar integralmente.
- Dois processos DGM-MAT.exe observados: PID 6052 (pai) e PID 2364 (filho); o listener 8181 pertence ao processo filho. A relação pai/filho foi confirmada, mas a função arquitetural do segundo processo ainda não foi explicada por logs/telemetria.
- Não foi encontrado atalho `DGM-MAT Chat` nos locais Desktop e Start Menu pesquisados.
- Cockpit nativo iniciado como processo Python GUI PID 4416; janela `DGM-MAT - Chat`, handle não nulo e `Responding=True`.
- Python 3.12.6 e PySide6 6.11.1; importação de `cockpit.app` aprovada.
- Teste do próprio `CommandConsoleWidget` com `runtime status` terminou com sucesso: autenticação local, consulta HTTP 200, runtime RUNNING, não degradado, zero missões ativas.
- A implementação instalada ainda não corresponde ao cockpit ChatGPT-like completo: o widget mantém histórico apenas na lista em memória da instância; não apresenta sidebar de conversas, pesquisa integrada ou persistência demonstrada. A janela abre e consulta o backend, mas a experiência completa continua pendente.

### API autenticada e limites

- Cliente `cockpit.api_client` conseguiu obter sessão normal via bootstrap local; nenhum token foi impresso, copiado ou persistido por estes testes.
- `GET /runtime/status`: HTTP 200, `status=running`, `is_degraded=false`, `missions_active=0`.
- `GET /runtime/queue`: HTTP 200, worker vivo, um thread e handler `MISSION_EXECUTION`.
- A ação histórica #7 surge como COMPLETED na fila, mas o seu resultado interno da missão é `failed` / `NotImplementedError`, indicando ausência de executor genérico. Não foi reexecutada nem alterada.
- `GET /runtime/missions` excedeu timeout de leitura de 5 segundos; não foi repetido em ciclo.
- Não foi criada missão nova, aprovada/rejeitada ação, alterada fila, testado provider, nem contactado DGM-HUB.

### Conclusão

A instalação do build oficial e a autenticação normal do cockpit/runtime estão confirmadas. A consulta read-only ao estado e à fila passou. A missão read-only com recibo durável continua por testar devido ao timeout na listagem de missões; o cockpit completo, pesquisa/persistência de conversas, atalho, papel arquitetural do processo filho, rollback, providers e DGM-HUB permanecem pendentes. A classificação correta mantém-se **VERIFICAÇÃO INCOMPLETA**.


## Correção de evidência — cockpit oficial validado — 2026-11-10 19:27 UTC

Esta correção prevalece sobre qualquer formulação anterior neste relatório que pudesse confundir o teste Python do checkout local com o executável oficial instalado.

### Separação entre código local e executável instalado

- O primeiro processo GUI Python (PID 4416) foi iniciado a partir do checkout local `recovery/local-worktree-consolidation-2026-11-09`, cujo código de cockpit está desatualizado. Esse processo foi fechado e o seu teste visual/widget não é aceite como prova do cockpit oficial.
- O executável instalado foi iniciado separadamente com `DGM-MAT.exe --cockpit-only`, sem iniciar um segundo backend.
- A janela Qt do executável oficial foi confirmada visível, com título `DGM-MAT - Assistente`, processo GUI PID 2816 e `Responding=True`.
- Os processos backend originais PID 6052/2364 mantiveram-se ativos; não foram reiniciados.
- O código da main observada em `fdae0ce` contém sidebar com Nova conversa, pesquisa, histórico, paginação, arquivo/restauro, consulta governada a IA e estado do sistema. A inspeção da fonte confirmou os handlers e endpoints correspondentes.

### Conversas — criação, pesquisa e persistência

- `GET /mobile/threads`: HTTP 200; 24 conversas listadas antes do teste.
- `GET /mobile/threads/search?q=DGM&limit=5&offset=0`: HTTP 200; cinco resultados e `has_more=true`.
- Foi criada uma conversa de teste local, sem mensagem: título `Validação técnica cockpit — 2026-11-10`, ID `thread-14375e4504ee4365`; `POST /mobile/threads` devolveu HTTP 200.
- `GET /mobile/threads` confirmou o ID e o título exatos (25 conversas na listagem).
- A janela oficial foi fechada graciosamente e o cockpit foi iniciado novamente com `--cockpit-only`. Após o fecho/reabertura, a consulta autenticada à lista voltou a devolver HTTP 200 e confirmou que a conversa de teste continuava presente com estado `active`.
- Esta prova cobre persistência da conversa através do fecho/reabertura do cockpit enquanto o backend permaneceu ativo; não prova persistência após reinício do backend/PC.
- A conversa de teste foi mantida para inspeção no cockpit. Não contém mensagens de teste.
- Não foi submetida missão, nem executada ação de aprovação, arquivo ou restauro.

### Estado final desta validação

**Confirmado:** executável oficial abre uma janela Qt visível e responsiva; API autenticada; lista e pesquisa de conversas; criação e persistência de uma conversa após fechar/reabrir o cockpit.  
**Ainda por confirmar:** interação manual completa no ecrã, conteúdo visual de cada componente, envio de mensagem, pesquisa pela interface, arquivo/restauro pela interface, atalho Desktop e persistência após reinício do backend.  
**Classificação global:** VERIFICAÇÃO INCOMPLETA.


## Correção adicional — atalho Desktop localizado — 2026-11-10 19:29 UTC

A pesquisa inicial de atalhos não incluiu a localização Desktop redirecionada para OneDrive. A consulta correta a `[Environment]::GetFolderPath('Desktop')` encontrou o atalho existente:

- Ficheiro: `DGM-MAT Chat.lnk` no Desktop OneDrive.
- Target: `C:\\ProgramasGodMode\\DGM-MAT\\installed\\DGM-MAT.exe`.
- Argumentos: `--cockpit-only`.
- Working directory: `C:\\ProgramasGodMode\\DGM-MAT`.
- Descrição: abrir o cockpit de chat ligado ao backend local.

O atalho já estava corretamente configurado; não foi criado nem alterado. O teste anterior do executável com o mesmo argumento confirmou uma janela oficial `DGM-MAT - Assistente` visível e responsiva.


## Novo bloqueio confirmado — archive/restore e classificação da rota — 2026-11-10 21:44 UTC

- Foi tentado arquivar exclusivamente a conversa de teste `thread-14375e4504ee4365`.
- O endpoint `POST /mobile/threads/{id}/archive` devolveu HTTP 403: `Route has no security classification.`
- O teste parou imediatamente; o endpoint restore não foi chamado e a conversa de teste não foi alterada.
- Não se deve contornar nem enfraquecer a middleware. É necessário inspecionar o registo/classificador de segurança das rotas e acrescentar a classificação explícita correta, com testes de autorização para arquivo/restauro.
- O achado foi registado na issue #313. A quota Desktop Commander está a 13% disponível; o próximo ciclo deve privilegiar inspeção do código e testes determinísticos no GitHub/CI, reservando nova execução remota para uma verificação agrupada depois da correção.

## Documentação da readiness

- PR #344 criada: [docs: record mission executor readiness validation](https://github.com/AndreVazao/DGM-MAT/pull/344).
- Corrige o estado obsoleto `awaiting CI validation` do documento de readiness, regista os runs Windows build #42806219347 e Mission E2E Regression Gate #42806219343 e distingue esses resultados de uma missão read-only real ainda não concluída.
- PR #344 está aberta, não mergeada. O combined status mostra apenas `security/snyk` pendente; não o usaremos como bloqueio porque a quota mensal gratuita do Snyk está esgotada. Nenhuma alteração de código/runtime foi feita nesta PR.


## Correção preparada — classificação archive/restore — 2026-11-10 21:48 UTC

A inspeção da fonte na main confirmou a causa exata do HTTP 403:

- `core/api/mobile_bridge.py` regista `POST /threads/{thread_id}/archive` e `POST /threads/{thread_id}/restore`.
- `core/api/auth_middleware.py` aplica classificação fail-closed e devolve 403 quando não existe entrada explícita.
- `core/api/security_policy.py` classificava create, messages e rename, mas omitia archive e restore.

Foi preparada a PR #345: [fix(security): classify mobile conversation archive and restore routes](https://github.com/AndreVazao/DGM-MAT/pull/345).

Alterações na branch `fix/classify-mobile-thread-archive-restore`:
- Classificar os dois endpoints como `MOBILE_CHAT`, exigindo o scope `mobile-chat`.
- Testar a classificação por template e por caminho concreto.
- Testar a autorização de sessão mobile-chat para arquivar/restaurar.
- Testar que uma sessão apenas `local-client` recebe 403 e não altera o estado da conversa.

A PR está aberta e mergeável. O único check reportado neste momento é `security/snyk` pendente; não será usado como bloqueio devido à quota mensal gratuita esgotada. Não foi feito bypass à middleware, merge ou instalação. A correção ainda aguarda CI de testes e validação real no PC.


## CI parcial da correção archive/restore — 2026-11-10 21:50 UTC

PR #345 / commit `246f08b55101fa599e29c37e87c2d2d216cbe28f`:

- Focused PR Validation run `42908115013`: **SUCCESS** — regressões afetadas passaram; Windows installer digest gate também passou.
- Chrome Extension Validation run `42908115162`: **SUCCESS**.
- Windows Executable Build run `42908115116`: ainda **IN_PROGRESS** no último polling.
- `security/snyk`: permanece pendente e é ignorado por quota gratuita esgotada; não é apresentado como aprovação.
- PR #345 continua aberta e mergeável. Não foi feito merge nem instalação.
- Falta esperar o build Windows terminar e, depois da integração autorizada, repetir archive/restore no PC com o executável atualizado e confirmar 200/estado archived/active.


## Continuidade — PR #348 integrada e artefacto final verificado — 2026-11-11

### Integração na main
- PR #348: https://github.com/AndreVazao/DGM-MAT/pull/348
- Branch limpa criada sobre a main atual; comparação final antes do merge: 0 commits behind.
- André aprovou explicitamente integração e instalação.
- PR #348 convertida de draft para ready e integrada por squash.
- Merge commit: `291091123fc5493dc236ed40d5a6fc3affc25b9f`.
- Main foi comparada com esse commit e devolveu `identical`.
- Branch de recuperação original `fix/graceful-runtime-shutdown-windows-update-2026-11-10` e PR #347 foram preservadas, sem merge nem alteração.

### Alterações funcionais integradas
- Uvicorn gerido explicitamente; `POST /runtime/shutdown` é loopback-only e exige sessão autenticada com scope `operator`.
- O pedido HTTP responde e o Uvicorn drena o pedido antes de sinalizar o runtime owner.
- `Runtime.shutdown()` também pede shutdown da API no caminho de KeyboardInterrupt.
- Cancela startup timers e aguarda API, repository-learning, auto-help, SafeActionQueue, kernel, governance, knowledge e EventBus.
- RepositoryLearningService e AutoHelpWorker devolvem confirmação de conclusão; runtime owner espera sem limite após timeout inicial se o worker continuar ativo.
- Todos os produtores param antes do drain final do EventBus.
- EventBus mantém referência da thread, drena a fila e aguarda o worker.
- Installer identifica o PID real do listener 8181 e confirma o caminho do executável; falha fechado se não provar propriedade.
- Installer e rollback não usam `Stop-Process -Force`.
- Rollback valida hashes de manifesto e prepara/verifica backups do EXE e launcher antes de substituir os destinos.
- Workflow Mission E2E instala DGM-Contracts, corre regressões novas em Windows/Linux e valida a sintaxe dos scripts PowerShell no Windows.

### CI do HEAD final
HEAD validado: `1e132728d540c52412f75e9556b6ba684f179b0e`.
- Mission E2E #82: SUCCESS em Windows e Ubuntu.
- Focused PR Validation #959: SUCCESS, incluindo installer digest gate.
- Chrome Extension Validation #506: SUCCESS.
- Windows Executable Build #580: build, deep executable check, final assertions e upload concluídos com sucesso.

### Artefacto oficial e hashes independentes
- Artefacto GitHub Actions ID: `13872750190`.
- Nome: `DGM-MAT-Windows-3.12-5a3282a`.
- Tamanho: 115,289,278 bytes.
- Expira em 2027-02-09.
- SHA-256 ZIP exterior (verificado localmente e igual ao digest GitHub): `d0edb7065c4035fa4ec2b9c57a1cb90cd99381878db160cb9692964bf8d53d08`.
- SHA-256 ZIP interno (igual ao sidecar incluído): `1f575a5333974b239fd80a373933287c7605f4bcd64196ec9a9c0ec8ce97f858`.
- SHA-256 EXE (igual ao sidecar incluído): `68481CF150E15C70DE703211CECFBC55C8DFCD86D22CA41FED4A2E18F2A870EF`.

### Estado da instalação local
- O artefacto foi descarregado para o ambiente de trabalho desta sessão e os três hashes foram verificados.
- **Ainda não foi transferido nem instalado no PC.**
- Não foi feito shutdown remoto, alteração de ficheiros locais, merge da branch de recuperação nem limpeza de filas/dados.
- Próximo passo autorizado: staging do artefacto no PC, fechar cockpit de forma graciosa se estiver aberto, executar installer oficial com SHA-256 independente, confirmar manifesto/backup e hash instalado, arrancar `backend_service.py start --mode full`, validar `/health`, `/runtime/status`, `/runtime/queue` (worker vivo), e abrir cockpit.
- Se o processo local não encerrar graciosamente, se a propriedade do listener não for provada ou se qualquer hash divergir, abortar sem matar processos nem substituir ficheiros.

### Classificação de aceitação
**CI e artefacto: VALIDADO. Instalação e operacionalidade no PC: PENDENTE.** Não declarar DGM-MAT operacional no PC até o serviço full e cockpit passarem a validação local autenticada.
