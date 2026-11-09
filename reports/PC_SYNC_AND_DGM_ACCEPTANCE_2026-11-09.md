# Operação PC + DGM-MAT — 2026-11-09

## Objetivo e restrições
- Utilizador confirmou que o PC `PC-Vazao-Anjos` está ligado.
- O Desktop Commander reportou apenas **17% de chamadas remotas restantes** no mês.
- Instrução: não esgotar a quota; reservar margem para testes do VazaoSovereignTrader.
- Não executar testes remotos repetidos nem fazer operações destrutivas sem inventário.
- Não declarar sincronização, instalação ou aceitação local concluídas sem evidência do PC.

## Repositórios confirmados no GitHub
- `AndreVazao/DGM-MAT`
- `AndreVazao/VazaoSovereignTrader`
- `AndreVazao/DGM-HUB`
- `AndreVazao/office-kit`
- `AndreVazao/VAZAO-EVSE-Platform`
- `AndreVazao/TruckFood`

## Estado verificado DGM-MAT
- `main` aponta para `c009c512593f16ee1bf085012fa700e4352433fe`, commit de 2026-11-07: `ci(windows): scope executable builds to application changes (#281)`.
- Windows Executable Build run `42393147249` terminou SUCCESS.
- Artefacto `DGM-MAT-Windows-3.12-c009c51`, ID `13582621027`, SHA-256 do ZIP `95290e958fdf3d992b7538d89355219bd3cb6092ced631a5f1bfb92ee6776b84`.
- O artefacto é da main atual, mas antecede as PRs de desenvolvimento recentes; não contém as alterações ainda abertas.
- PRs DGM-MAT abertas verificadas: #283 (recuperação legacy/browser), #285 (mobile scopes/history), #286 (documentação EGM), #287 (review packet), #288 (review coordinator), #289 (fresh review browser), além de #282 e #284. Todas permanecem por integrar; não houve merge nesta operação.
- PR #285 declara explicitamente que não deve ser integrada antes da aceitação E2E Windows/Android e confirmação de provider gratuito real.
- Flags de consulta browser e autonomia continuam desligadas. Não ativar providers nem credenciais.

## Estado Android / Maestro
- Run Maestro anterior `42572168935` falhou depois de o emulador arrancar, o APK ser compilado e carregado como artefacto.
- Diagnóstico dos logs: erro de parsing shell no ciclo `for attempt ...; do` no script entregue ao android-emulator-runner; não foi falha de compilação do APK.
- Corrigido o workflow `.github/workflows/maestro-android-smoke.yml` no PR #5, commit `bbd21f2f5371fce5c05bc7e6caba275b419794cb`, removendo o loop redundante de boot e usando o boot gate do próprio runner mais uma verificação única.
- Novas execuções iniciadas em `2026-11-09T06:48:49Z`: Maestro `42575360984`; Mobile PR Validation/APK Build `42575360833`. Estado observado: IN_PROGRESS. Não declarar sucesso até conclusão.
- Artefacto APK da execução anterior falhada existe e foi carregado, mas a falha UI significa que o smoke test não passou.

## Estado do PC e operações não executadas
- Desktop Commander listou `PC-Vazao-Anjos` como Online.
- Não foi consumida uma sequência de chamadas remotas para sincronizar, compilar, instalar ou testar, para preservar a cota de 17% para o Sovereign Trader.
- Não houve git pull, alteração de working tree, desinstalação de versões, instalação de EXE, teste de health local ou teste E2E no PC nesta operação.
- Nenhuma versão anterior foi desinstalada; nenhum dado local foi apagado.
- O inventário local ainda é necessário para identificar paths, alterações não commitadas e versões instaladas antes de executar uma única operação agrupada.

## Próxima execução local planeada
1. Quando a quota reservada permitir, executar um único inventário de seis working trees, branches, remotes e dirty state.
2. Fast-forward apenas working trees limpas; working trees modificadas devem ser preservadas e reportadas, sem reset/stash automático.
3. Construir/obter artefacto DGM-MAT correspondente ao conjunto de PRs aprovado e integrado; não instalar artefacto antigo como se incluísse código ainda em PR.
4. Antes da substituição, identificar entradas de desinstalação e caminhos de dados; preservar configurações, credenciais e memória. Remover apenas versões antigas confirmadas do DGM-MAT, nunca outras aplicações.
5. Instalar, executar uma única ronda de health/API/chat/history e guardar relatório local.
6. Reservar quota para validação separada do VazaoSovereignTrader.
7. Sincronizar também os outros cinco repositórios, com proteção contra alterações locais.

## Regra de evidência
CI verde não equivale a instalação nem E2E real. Não declarar sincronização PC/GitHub concluída até obter branches/SHAs locais alinhados e relatório de validação do PC.
