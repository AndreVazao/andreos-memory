# Script Comparator — Backlog

## Concluído
- [x] Separação do motor da GUI.
- [x] Pacote src/script_comparator.
- [x] API pública através de __init__.py.
- [x] pyproject.toml para empacotamento.
- [x] Shim de compatibilidade para imports antigos.
- [x] Testes de regressão iniciais.
- [x] Agrupamento por nome base + extensão.
- [x] Score de completude e escolha de base.
- [x] Backup e preservação das versões.
- [x] Conflitos bloqueiam escrita por defeito.
- [x] Inserção Python antes do main guard.
- [x] Fallback genérico com âncoras em vez de append cego.
- [x] Dry-run/preview formal sem escrita.
- [x] Relatório JSON estável para consumidores.
- [x] Merge estruturado de JSON com chaves aninhadas.
- [x] Parsing seguro de JSONC para validação e merge.
- [x] Adapter estrutural inicial para JavaScript/TypeScript/JSX/TSX.
- [x] Testes de recuperação e conflito JS/TS.
- [x] Testes de merge JSON aninhado e JSONC com comentários/URLs.

## Próximas fases
- [ ] Preservação de comentários durante serialização JSONC.
- [ ] Adapter Kotlin/Java/C#.
- [ ] Merge estrutural HTML/CSS.
- [ ] Suite de famílias reais de ficheiros.
- [ ] Empacotamento/release interna versionada.
- [ ] Primeiro consumidor externo real.
- [ ] Teste de atualização do módulo sem quebra do consumidor.
- [ ] GUI PyQt construída como cliente do core.
- [ ] Integração com script-reviewer-mobile.
- [ ] Integração futura no DGM-MAT quando houver benefício comprovado.
