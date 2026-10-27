# Checkpoint VST — Android Emulator + Maestro — 2026-10-27

## Checkpoint 2026-10-27 — Android emulator + Maestro

- Produto main observado: 011efeb26db80291a96032d1de042c2c3fed6389.
- PR #497 permanece aberto: https://github.com/AndreVazao/VazaoSovereignTrader/pull/497. Python tests run 40473392788 e Windows EXE run 40473392950 concluíram success. Não fazer merge automaticamente.
- PR #499 aberto: https://github.com/AndreVazao/VazaoSovereignTrader/pull/499; branch feat/android-emulator-maestro-smoke-2026-10-27, HEAD 826b6a8a10cc58a39cfe28cb4c993da39ba2d4f2.
- PR #499 adiciona workflow `.github/workflows/android-emulator-maestro.yml`, flow `.maestro/android-startup-smoke.yaml` e docs `docs/ANDROID_EMULATOR_TESTING.md`.
- O workflow constrói APK de teste x86_64 temporário, inicia Android API 35 no runner Linux via KVM, instala APK, corre Maestro CLI, confirma processo vivo, captura screenshot/logcat e usa OCR para verificar texto inicial. O APK x86_64 não é release; o workflow APK de produção ARM64 fica separado.
- Run #40475487893 estava `in_progress` na última consulta; não afirmar sucesso até terminar e inspecionar logs/artifact. Link: https://github.com/AndreVazao/VazaoSovereignTrader/actions/runs/40475487893.
- Maestro CLI open-source sem Maestro Cloud/token; sem custos de serviço extra previstos além dos limites normais de GitHub Actions. Confirmar limites/consumo se necessário.
- Windows já é testado em runner Windows nativo, com build/smoke do EXE e instalador. Não se implementou nested Windows VM; não é necessário para o smoke de pacote. Máquina Windows física do utilizador ainda não foi testada.
- Não há ligação à PC API/exchanges, credenciais ou ordens. Teste é apenas smoke de arranque e renderização, não cobertura completa de funcionalidades ou dispositivo físico.
- Próximo passo: verificar run #40475487893, corrigir falhas se houver; depois ampliar Maestro para navegação do cockpit se os seletores de Kivy forem verificáveis. Manter PAPER/read-only.