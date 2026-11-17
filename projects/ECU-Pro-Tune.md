# ECU Pro Tune — estado persistente — 2026-11-15

## Checkpoint confirmado — Windows CI verde e PR aberto
- Repo: AndreVazao/ecu-pro-tune (público).
- Branch: feature/dashboard-advanced-20261108.
- Commit funcional validado: ff2c609cac0ce0bd1df9b0eab04231ffa8a25671.
- GitHub Actions run #4: 43427809165 — SUCCESS.
- Run URL: https://github.com/AndreVazao/ecu-pro-tune/actions/runs/43427809165.
- Job: Windows / Python 3.11 — todos os 16 passos concluídos com sucesso.
- Testes unitários: 4 passed in 0.02s.
- Compileall, pip check, import smoke test e construção Tk dashboard: PASS.
- PyInstaller: build Windows concluído.
- Smoke test do executável: processo iniciou e permaneceu ativo durante os 8 segundos de verificação.
- Artefacto: ECUProTune-Windows-Python311, ID 14036984205, 53,394,215 bytes.
- SHA-256 do ZIP: d535beb11fb51fb0bd59c5210d902a8d6aff84e03501f181a4bd6ba9abcb19dc.
- Retenção do artefacto: até 2026-11-27T12:46:48Z.
- ZIP contém 2.310 ficheiros e ECUProTune.exe (14,852,596 bytes). Distribuição onedir: manter o conteúdo da pasta junto do EXE.
- PR #1 aberto para main: https://github.com/AndreVazao/ecu-pro-tune/pull/1.
- PR aberto, não merged; GitHub reporta mergeable=true.
- Diff original: 6 commits, 3 ficheiros, 463 adições e 82 remoções; documentação de estado atualizada posteriormente.
- Commit da documentação de estado: 2775fb9929f090f7d446a0e015ab3cd5dc7a0e1e.
- Novo run #6 para esse commit: 43749616835, em execução no último check. Run #5 (PR event) foi cancelado automaticamente pelo concurrency ao ser substituído pelo push do commit seguinte; run #6 é o que deve ser acompanhado.
- Não fazer merge sem autorização explícita.
- CodeRabbit não corre automaticamente neste repo com menos de 10 stars; isso não afeta o CI.
- CI valida build/testes e arranque breve, não valida interação visual prolongada, hardware real, ECU física ou funcionamento em todos os PCs.

## Histórico técnico
- Commit do dashboard: 6d28e3c62f9bc15a2f278fd78254bf441cd1125b.
- Workflow: .github/workflows/windows-ci.yml.
- Commit do workflow: 940c7ecd5c26eb9a4ea1e66935b53cba00a44d65.
- Documentação: docs/DEVELOPMENT_STATUS.md.
- AndreOS Memory checkpoint: 5248d4b41cde1ae749beb0e37eca7834296dd02c (checkpoint inicial CI verde); atualização posterior em curso.
- PC-Vazao-Anjos está offline/indisponível; CI corre em runner Windows hospedado pelo GitHub.
- Local ECU: C:\\ProgramasGodMode\\ecu-pro-tune.
- Local memory: C:\\ProgramasGodMode\\andreos-memory.
- O diretório local não versionado andreos-memory deve continuar preservado.

## Implementado
- GUI ttkbootstrap com Performance/Showcase.
- ProfileManager, ECUManager, Scheduler, RollbackManager, SoundManager, Logger.
- MapEditor, validators e live graph.
- Stage 1 profile/map.
- SoundManager fail-safe: MP3 quando disponível, WAV fallback no Windows e backend ausente não bloqueia a GUI.
- Gerador stdlib de 12 cues WAV fallback, 6 por modo, sem dependência de FFmpeg.
- Novo dashboard na branch: seis métricas, RPM/boost gauges, gráfico rolling, monitor de sistema, navegação para Perfis/Mapas e retorno ao dashboard.
- Atualização do dashboard em intervalo de 400 ms e histórico limitado a 90 amostras.
- Identidade visual azul/ciano/preto/cinza, sem novas dependências.

## Segurança
- Nenhuma escrita física de ECU.
- Nenhum driver de flash.
- Toda a telemetria do dashboard é simulada.
- Futura integração de hardware deve ser isolada e fail-closed por defeito.

## Próximos passos
1. Confirmar run #6 verde e validar os checks associados ao PR #1.
2. Rever PR #1 e aguardar autorização explícita antes do merge em main.
3. Teste visual manual no PC Windows quando estiver disponível.
4. Endurecer installer/FFmpeg.
5. Acrescentar testes de integração.
6. Só depois avaliar adapters de hardware, sem escrita física por defeito.


## Checkpoint adicional — 2026-11-17 — run #6 confirmado verde
- Run #6: 43749616835 — SUCCESS, concluído em 2026-11-15T18:58:29Z.
- Commit validado: 2775fb9929f090f7d446a0e015ab3cd5dc7a0e1e.
- URL: https://github.com/AndreVazao/ecu-pro-tune/actions/runs/43749616835.
- Job Windows / Python 3.11: os 16 passos concluídos com sucesso, incluindo pytest (4 passed), imports, construção Tk, PyInstaller, verificação do EXE, smoke test de arranque e upload do artefacto.
- PR #1 permanece open, merged=false, mergeable=true, mergeable_state=clean; branch feature/dashboard-advanced-20261108 para main.
- PR URL: https://github.com/AndreVazao/ecu-pro-tune/pull/1.
- Não foi feito merge. Exigir autorização explícita do utilizador antes de integrar.
- Run #5 continua classificado como cancelamento automático por concurrency, não falha funcional.
- Próximo gate: revisão final do PR e autorização de merge. Depois avançar para teste visual manual em Windows, robustez do instalador e testes de integração.


## Checkpoint 2026-11-17 — PR #1 merged / fase de integração iniciada
- PR #1 (dashboard avançado + Windows CI) foi integrado na main do ECU Pro Tune.
- Merge commit: aa388679e1ea0510c66ed588d4d313e2cbe7e1ba.
- PR #1 URL: https://github.com/AndreVazao/ecu-pro-tune/pull/1.
- Branch main confirmada nesse merge commit.
- Nova branch criada a partir de main: feature/integration-tests-20261117.
- Hardening implementado em validators, ProfileManager, ECUManager e RollbackManager.
- Novos testes em tests/test_integration_managers.py: round-trip de perfil, proteção path traversal, validação de mapas, extração de arrays, backup/restauro, rejeição NaN/inf/bool e nomes inválidos.
- CI run #18: 44035159971 — SUCCESS; commit 7f1b53e0743f049d5b3929db84ed265d062f782d.
- 20 testes passaram em 0.10s.
- pip check, compileall, imports, construção Tk, PyInstaller, verificação do EXE, smoke test de arranque e upload de artefacto: PASS.
- Artefacto: ECUProTune-Windows-Python311, ID 14306118545, 53,396,254 bytes, SHA-256 2787bc15238657ec9446f691521b03d66438178e976812a553a2e321d1cce510, expira em 2026-12-01T07:00:26Z.
- Commit de documentação na branch: 21b976f2ea67fc48a24b5b05471208574e7e5fab.
- CI push #18 validou o commit de código anterior; o commit de documentação vai disparar nova execução.
- PR #2 ainda não criado neste checkpoint; aguardar CI da atualização documental e abrir PR para main.
- Segurança permanece: sem escrita física ECU, sem driver de flash; qualquer futura integração deve ser isolada e fail-closed.
- Próximos passos: confirmar CI do commit docs, criar PR #2, expandir testes scheduler/logging/ficheiros corrompidos/GUI, endurecer installer e validar visualmente em Windows.


## Checkpoint 2026-11-17 — PR #2 merged / scheduler and logger phase
- PR #2 merged successfully into ECU Pro Tune main.
- PR URL: https://github.com/AndreVazao/ecu-pro-tune/pull/2.
- Merge commit: 0980530a17368c919f07867953e51da3dea649da.
- Main CI after merge: run #21, 44035795100 — SUCCESS.
- New branch: feature/scheduler-logging-tests-20261117.
- Scheduler hardened: validates schedule data, profile references and ISO dates; rejects corrupt JSON without overwriting; writes atomically; isolates callback errors; uses cancelable Event.wait instead of fixed sleep.
- New tests cover schedule append/validation, corrupt file preservation, due/future entries, callback retry behavior, and UTF-8 logging.
- CI run #25: 44035973794 — SUCCESS; commit d699874850daf5de3c290e77384ab65d631ec2b8.
- 29 tests passed in 0.12s.
- Full Windows pipeline PASS: dependency check, compileall, imports, Tk dashboard construction, PyInstaller build, EXE verification, packaged startup, artifact upload.
- Artifact ECUProTune-Windows-Python311 ID 14306798921, 53,398,443 bytes.
- SHA-256 adc45d75bb8930a77fe25fffb083dd999c45b6ae4f1606396807bb46d0b78796; expires 2026-12-01T07:06:49Z.
- Documentation commit in branch: 778521ba9f31872ba9c66d7b2002730b8dbc2590.
- PR #3 to be opened after branch documentation commit CI completes.
- No physical ECU write or flash capability; hardware integration remains out of scope until explicitly designed, isolated, and fail-closed.
