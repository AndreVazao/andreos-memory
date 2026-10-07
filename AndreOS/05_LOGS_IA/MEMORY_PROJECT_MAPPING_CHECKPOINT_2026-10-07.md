# Memory Project Mapping — 2026-10-07

## Objetivo
Depois de tornar `AndreVazao/andreos-memory` a fonte canónica, foi feito o primeiro inventário de repos GitHub/local contra as pastas de memória.

## Resultado
- Confirmadas as pastas de memória existentes e o conteúdo já migrado.
- Criado `AndreOS/02_PROJETOS/REPOS_TO_PROJECTS.md`.
- Atualizado `AndreOS/02_PROJETOS/INDEX_PROJETOS.md`.
- Identificados agrupamentos lógicos: DGM-MAT, Baribudos, Build Control Center, n8n, VAZÃO EVSE, Labs e outros.
- Criadas as memórias iniciais `AIRLLM/` e `RABBITLLM/` porque foram identificados como projetos lógicos independentes/candidatos claros.
- Repos ainda ambíguas não receberam agrupamento inventado; ficaram explicitamente marcadas para auditoria.

## Regra consolidada
Uma repo GitHub não implica automaticamente uma pasta de memória. A memória representa o projeto/produto lógico.

Processo: MAPEAR → AUDITAR → CLASSIFICAR → AGRUPAR/SEPARAR → CRIAR MEMÓRIA → REGISTAR.

## Próximo trabalho
Auditar os projetos ainda sem classificação e reconciliar repos locais/GitHub com o mapa, sem tocar no `DGM-MAT-FULL-MIRROR`.
