# DGM-MAT — Integração autorizada e limpeza de PRs — 23/11/2026

## Merges concluídos

### PR #393 — integridade do histórico de conversas
- Squash merge: `5cbf90d607ee3846bbbeb25421a6744811736a13`.
- HEAD integrado: `975f16ec2f75033ffef54a10885aaebbf2b5d742`.
- Focused Validation #1048 e Windows Build #694: success.
- CodeRabbit reportou sem findings acionáveis; a ferramenta avisou que a revisão incremental não reanalisa commits previamente revistos. O patch final foi manualmente inspecionado antes do merge.
- Implementa fail-closed em erro de load, valida schema/registos, IDs duplicados, guarda pré-mutação e testes de bytes+memória.

### PR #396 — recuperação documental limpa
- Squash merge: `a0b6fc1477d648c5888c1dc0492c26b5325c06b1`.
- Recuperação seletiva dos relatórios 18–23/11 e consolidação 17/11, sete ficheiros exclusivamente documentais.
- Branch criada a partir da main atual após #393; 7 commits ahead, 0 behind.
- #391 e #392 foram fechadas como superseded por #396. Branches originais preservadas, sem eliminação.

## Estado final observado
- PR #393 merged.
- PR #396 merged.
- PR #391/#392 closed sem merge, conteúdo recuperado em #396.
- Não foi observada validação pós-merge por workflow-run associada ao commit #396 (fetch retornou runs vazias).
- PC local offline; runtime/API/missão/providers/agents/Vault/DGM-HUB não validados.

## Próxima funcionalidade
Issue #394 (diagnóstico de saúde do ConversationStore/API/Cockpit) é a próxima funcionalidade. Começar branch limpa a partir da main atual, manter PR única e executar CI. Issue #395 recuperação Vault seletiva depois.
