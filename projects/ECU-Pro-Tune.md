# ECU Pro Tune — estado persistente — 2026-11-08

## Estado confirmado
- Repo: AndreVazao/ecu-pro-tune.
- Branch de trabalho atual: feature/dashboard-advanced-20261108.
- Commit do dashboard: 6d28e3c62f9bc15a2f278fd78254bf441cd1125b.
- Commit da documentação na branch: 9eb0a3709a8fa9c68ddb018edcd6f58772317b56.
- A implementação ainda não foi integrada em main.
- PC-Vazao-Anjos estava offline durante a sessão; validação local e GUI pendentes.
- Local ECU: C:\ProgramasGodMode\ecu-pro-tune.
- Local memory: C:\ProgramasGodMode\andreos-memory.
- O diretório local não versionado andreos-memory deve continuar preservado.

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

## Ambiente
- Python global apresentou falha DLL no NumPy 2.4.6.
- Usar o ambiente .venv e NumPy 1.26.4.
- FFmpeg não estava no PATH no último checkpoint; GUI e WAV fallbacks não dependem dele.

## Próximos passos obrigatórios
1. Reconectar PC-Vazao-Anjos e validar compileall, pytest e abertura da GUI.
2. Corrigir qualquer problema encontrado e integrar a branch em main via PR.
3. Endurecer installer/FFmpeg.
4. Empacotar EXE.
5. Acrescentar testes de integração.
6. Só depois avaliar adapters de hardware, sem escrita física por defeito.
