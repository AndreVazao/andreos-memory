# ECU Pro Tune — estado persistente — 2026-11-15

## Checkpoint confirmado — Windows CI verde e PR aberto
- Repo: AndreVazao/ecu-pro-tune (público).
- Branch: feature/dashboard-advanced-20261108.
- Commit validado: ff2c609cac0ce0bd1df9b0eab04231ffa8a25671.
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
- Artefacto descarregado para /mnt/data/ECUProTune-Windows-Python311.zip nesta sessão; ZIP contém 2.310 ficheiros e ECUProTune.exe (14,852,596 bytes). Distribuição é onedir: manter o conteúdo da pasta junto do EXE.
- PR #1 aberto para main: https://github.com/AndreVazao/ecu-pro-tune/pull/1.
- PR aberto, não merged; GitHub reporta mergeable=true após atualização dos metadados.
- Diff: 6 commits, 3 ficheiros, 463 adições e 82 remoções.
- Não fazer merge sem autorização explícita.
- Revisão automática CodeRabbit não correu automaticamente porque o repositório tem menos de 10 stars; não confundir isso com CI.
- O CI prova arranque do processo e construção do dashboard, não valida interação visual prolongada, hardware real, ECU física ou funcionamento em todos os PCs.

## Histórico técnico
- Commit do dashboard: 6d28e3c62f9bc15a2f278fd78254bf441cd1125b.
- Workflow: .github/workflows/windows-ci.yml.
- Commit do workflow: 940c7ecd5c26eb9a4ea1e66935b53cba00a44d65.
- Documentação de estado: docs/DEVELOPMENT_STATUS.md.
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
1. Rever o PR #1 e confirmar se queres autorizar o merge em main.
2. Atualizar docs/DEVELOPMENT_STATUS.md com o CI verde e o PR #1, criando novo commit e deixando o CI do PR correr novamente.
3. Teste visual manual no PC Windows quando estiver disponível.
4. Endurecer installer/FFmpeg.
5. Acrescentar testes de integração.
6. Só depois avaliar adapters de hardware, sem escrita física por defeito.
