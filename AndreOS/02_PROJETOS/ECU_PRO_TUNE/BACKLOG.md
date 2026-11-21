# ECU Pro Tune — Backlog

## P0 — Aceitação e release
- [ ] Disponibilizar Windows real de utilizador final para executar os 14 casos de aceitação.
- [ ] Registar todos os 14 como PASS/FAIL/SKIP com notas/evidência.
- [ ] Validar relatório com -RequirePass.
- [ ] Executar gate check_release_readiness.ps1 e confirmar hash/manifest/version.
- [ ] Rever os resultados antes de qualquer tag/release.

## P1 — Qualidade de produto (sem hardware)
- [ ] Expandir testes de GUI por fluxo e regressão, mantendo ambiente headless-friendly no CI.
- [ ] Testar recuperação/rollback quando ficheiros JSON/config/map estão incompletos, truncados ou corrompidos.
- [ ] Melhorar observabilidade de erros sem expor paths/segredos desnecessários.
- [ ] Rever accessibility, teclado, resize, persistência de estado e estabilidade de scheduler.

## P2 — Evolução
- [ ] Planeamento de adapters de hardware apenas como interfaces isoladas, sem write/flash implementado.
- [ ] Avaliar política de privatização do repo depois da maturidade e release.
- [ ] Preparar release notes e processo manual de publicação; CI não publica releases/tags automaticamente.

## Restrições
- Nunca contar CI sintética como aceitação manual.
- Não habilitar escrita física/flash de ECU neste estágio.
