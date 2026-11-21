# ECU Pro Tune — Memória Mestre

**Repositório:** AndreVazao/ecu-pro-tune  
**Branch principal:** main  
**Visibilidade:** public durante desenvolvimento/CI, decisão de tornar privado após fase de desenvolvimento  
**Última atualização:** 2026-11-21

## Produto
Aplicação desktop Python para gestão visual de perfis de calibração automóvel, edição de mapas, curvas, backups, rollback, scheduler e dashboard. Estado funcional 0.1.0.

## Segurança e âmbito
- Atualmente gestão, visualização e simulação; não existe escrita física ECU, driver flash nem programação de ECU.
- Qualquer futura integração de hardware deverá ficar isolada, explícita, fail-closed e bloqueada por defeito.
- Testes sintéticos do CI nunca são aceitação manual real.
- Não publicar tag/release definitiva antes dos 14 testes manuais em Windows real estarem concluídos e revistos.

## Estado consolidado (2026-11-21)
- PR #12 integrado: validador de relatórios estruturados de aceitação.
- PR #13 integrado: harness PowerShell executa o validador contra relatórios sintéticos temporários; verifica 14/14 PASS, bloqueio de INCOMPLETE por -RequirePass, IDs duplicados e totais inconsistentes.
- PR #14 integrado: smoke test end-to-end do instalador num runner Windows limpo, com ECU_PRO_TUNE_CI=1, .venv, pip check e imports Python 3.11.
- PR #15 integrado: gate combinado de prontidão de release (manifesto, ZIP, SHA-256, versão e 14/14 PASS), sem publicar release automaticamente.
- Última CI de main documentada: run #155, SUCCESS; 53 testes Python; PowerShell parser/integration, installer, venv, Tk, PyInstaller, metadata EXE, startup smoke, ZIP, independent verification e artifact upload PASS.
- Artefacto main #14674238646; digest do artefacto e SHA do ZIP constam de docs/DEVELOPMENT_STATUS.md. Artefactos Actions são temporários e têm retenção limitada.

## Bloqueio operacional
O PC de utilizador PC-Vazao-Anjos estava offline na última verificação. Os 14 casos de aceitação manual continuam pendentes. Não confundir CI/fixtures sintéticos com aceitação real.

## Próximos passos
1. Executar os 14 casos em Windows de utilizador final e guardar relatório estruturado.
2. Validar relatório com scripts/validate_windows_acceptance.ps1 -RequirePass.
3. Executar scripts/check_release_readiness.ps1 e confirmar integridade/versão.
4. Rever resultados, defeitos e evidência visual antes de release.
5. Expandir testes GUI e recuperação de ficheiros sem hardware.
6. Manter a fronteira de segurança sem flash/write físico.
7. Após maturidade/release, avaliar privatização do repositório conforme decisão do proprietário.

## Documentação de referência
- README.md
- docs/DEVELOPMENT_STATUS.md
- docs/ACCEPTANCE_TEST_WINDOWS.md
- docs/RELEASE_PACKAGING.md
- scripts/record_windows_acceptance.ps1
- scripts/validate_windows_acceptance.ps1
- scripts/check_release_readiness.ps1
- scripts/verify_release.ps1
- tests/test_windows_acceptance_validator.ps1
- .github/workflows/windows-ci.yml
