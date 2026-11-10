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

