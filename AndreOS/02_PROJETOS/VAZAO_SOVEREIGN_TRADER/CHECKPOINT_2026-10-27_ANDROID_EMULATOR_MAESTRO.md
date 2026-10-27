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

## Atualização 2026-10-27 — falha CI e correção #500

- Run #40475487893 terminou FAILURE, mas não devido à compilação: o passo Buildozer concluiu sucesso e o emulador Android iniciou. A falha foi a pesquisa relativa do APK devolver vazio no contexto de trabalho do action antes da instalação; não houve teste Maestro nem artefacto de evidência.
- PR #500 corrige a localização com GITHUB_WORKSPACE e prepara recolha de evidência: https://github.com/AndreVazao/VazaoSovereignTrader/pull/500.
- Novo run #40484665409 estava queued na última consulta: https://github.com/AndreVazao/VazaoSovereignTrader/actions/runs/40484665409. Estado pendente; não declarar verde até inspecionar resultado e artefactos.
- Próximo: seguir o run #40484665409; se passar, ampliar cobertura UI. Se falhar, usar logs/evidência para corrigir. Não alterar o APK release ARM64.


## Atualização 2026-10-27 12:20 UTC — limpeza da fila

- Produto main: `a109a2d0c7be18364cbfeee38f89aded327037cf`.
- PR #498 merged: `087144e668769ab6e51c2e524597703b61ae2240`.
- PR #489 merged: `a109a2d0c7be18364cbfeee38f89aded327037cf`.
- Só PR aberto: #500, https://github.com/AndreVazao/VazaoSovereignTrader/pull/500. Base main, HEAD `5c1b96f0b99a42408769fc04757926074cc0beff`.
- Run #40484665409 falhou na recolha de evidências por variável shell não persistente entre linhas do action runner; build do APK, boot do emulador e instalação do Maestro tinham passado. Novo run #40502699078 em progresso, build APK ainda em curso na última consulta.
- Corrigido o workflow para usar caminhos absolutos em cada linha; aguardar resultado final antes de merge.
- PRs #485, #486, #488, #490–#493, #497 e #499 fechados sem merge por conflitos/dependências empilhadas. Não os contar como integrados.
- Nova branch sem PR para trabalho seguinte: `feat/vst-brand-consolidation-2026-10-27`, commit `edcd4ed4cdd6bb9b82e659333fa0fb88a3d8c136`. Consolida assets e scripts de branding de office/Android/Windows; ainda por validar com CI.
- Nunca mergear #500 até o workflow passar e a revisão do diff estar concluída.


## Atualização 2026-10-27 13:12 UTC — consolidação de PRs e branch única

- Estado verificado no GitHub: o único PR aberto é #501, https://github.com/AndreVazao/VazaoSovereignTrader/pull/501.
- PR #500 foi fechado sem merge e substituído por #501 porque o head antigo estava divergido de main; o seu trabalho de Android smoke test foi transportado para a nova branch, não descartado.
- Branch ativa única: `work/trader-consolidation-2026-10-27`.
- Head atual: `c2dc321c79d34b5feee16df5c7e6b71b36ff4e31`; a comparação GitHub reportou 9 commits à frente e 0 atrás de main.
- #501 agrega o workflow Android x86_64 + Maestro e artefactos de evidência, correção fail-closed para eventos Coinbase rejeitados, normalização do heartbeat OKX, testes de regressão e documentação L2.
- A revisão confirmou que parte da persistência L2/identidade de venue e símbolo já está em main; foi adicionado teste compatível com a implementação atual, sem reintroduzir a implementação antiga do PR #497.
- Checks disparados no head #501: Python tests run #3117, Windows EXE run #818 e Android Emulator UI Smoke run #8. Estavam queued na última consulta; não fazer merge antes de concluírem e serem inspecionados.
- PRs #488 e #497, bem como os PRs empilhados #485/#486/#490–#493/#496/#499, permanecem fechados sem merge. As correções técnicas relevantes de #488/#497 foram reaplicadas/adaptadas em #501. A cadeia de branding raster/ícones Windows/Android continua fora do #501 porque a cópia segura do asset binário e validação de packaging não foram concluídas; não declarar esse trabalho integrado.
- Política de higiene: manter apenas #501 aberto e uma branch de trabalho ativa; fechar o PR atual anterior quando substituído. Não apagar branches históricas enquanto houver trabalho exclusivo não recuperado.
- Segurança: PAPER/read-only; sem credenciais, chamadas de conta privada, ordens ou permissões REAL.
