# ECU Pro Tune — estado persistente — 2026-11-13

## Estado confirmado
- Repo: AndreVazao/ecu-pro-tune.
- Branch de trabalho: feature/dashboard-advanced-20261108.
- Commit do dashboard: 6d28e3c62f9bc15a2f278fd78254bf441cd1125b.
- Workflow GitHub Actions: .github/workflows/windows-ci.yml.
- Commit do workflow: 940c7ecd5c26eb9a4ea1e66935b53cba00a44d65.
- Documentação atualizada na branch após o workflow.
- Workflow ainda não teve o resultado do primeiro run confirmado.
- A implementação ainda não foi integrada em main.
- PC-Vazao-Anjos está offline/indisponível; CI corre em runner Windows hospedado pelo GitHub.
- Local ECU: C:\\ProgramasGodMode\\ecu-pro-tune.
- Local memory: C:\\ProgramasGodMode\\andreos-memory.
- O diretório local não versionado andreos-memory deve continuar preservado.

## Windows CI
- Ficheiro: .github/workflows/windows-ci.yml.
- Runner: windows-latest, Python 3.11.
- Triggers: push em main e feature/**; pull_request para main; workflow_dispatch.
- Steps: instalar requirements, pip check, compileall, pytest, import smoke test, construção Tk dashboard smoke test e build PyInstaller Windows.
- Publica artefacto ECUProTune-Windows-Python311 por 14 dias.
- Considerar pendente até o primeiro run ficar verde; criar o workflow não significa testes aprovados.

## Implementado
- GUI ttkbootstrap com Performance/Showcase.
- ProfileManager, ECUManager, Scheduler, RollbackManager, SoundManager, Logger.
- MapEditor, validators e live graph.
- Stage 1 profile/map.
- SoundManager fail-safe: MP3 quando disponível, WAV fallback no Windows e backend ausente não bloqueia a GUI.
- Gerador stdlib de 12 cues WAV fallback, 6 por modo, sem dependência de FFmpeg.
- Testes do checkpoint anterior: 4 passed.
- compileall do checkpoint anterior: PASS.
- .venv com NumPy 1.26.4 e Matplotlib 3.9.4.
- Novo dashboard na branch: seis métricas, RPM/boost gauges, gráfico rolling, monitor de sistema, navegação para Perfis/Mapas e retorno ao dashboard.
- Atualização do dashboard em intervalo de 400 ms e histórico limitado a 90 amostras.
- Identidade visual azul/ciano/preto/cinza, sem novas dependências.

## Segurança
- Nenhuma escrita física de ECU.
- Nenhum driver de flash.
- Toda a telemetria do dashboard é simulada.
- Futura integração de hardware deve ser isolada e fail-closed por defeito.

## Próximos passos
1. Inspecionar o primeiro run do workflow e resolver qualquer falha.
2. Descarregar/validar o EXE gerado pelo runner.
3. Criar PR da branch para main apenas com CI verde.
4. Endurecer installer/FFmpeg.
5. Acrescentar testes de integração.
6. Só depois avaliar adapters de hardware, sem escrita física por defeito.
