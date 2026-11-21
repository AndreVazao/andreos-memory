# ECU Pro Tune — Última Sessão / Handoff

**Checkpoint:** 2026-11-21  
**Repo:** AndreVazao/ecu-pro-tune  
**Branch de documentação:** docs/persistent-checkpoint-20261121

## Estado real confirmado pela documentação da main
- PR #12: validador de relatório de aceitação estruturado — integrado.
- PR #13: testes de integração reais PowerShell — integrado.
- PR #14: installer smoke test Windows clean runner — integrado.
- PR #15: gate combinado de release readiness — integrado.
- Main CI #155 SUCCESS; 53 testes Python.
- PowerShell parser/validator integration, instalador, ambiente venv, Tk, PyInstaller, metadados do EXE, startup smoke, ZIP, verificação independente e upload — PASS.
- Não há aceitação manual real: 14 testes ainda pendentes devido ao PC de teste estar offline.

## Continuação imediata
A próxima sessão deve começar pela expansão de testes GUI/recuperação de ficheiros sem hardware, ou preparar o processo de aceitação manual para quando Windows real estiver disponível. Evitar repetir trabalho já integrado nos PR #12–15.

## Segurança
Sem ECU física, flash, driver ou programação hardware. Relatórios synthetic fixtures são temporários e não são evidência manual. Release/tag pública continua condicionada à aceitação real.
