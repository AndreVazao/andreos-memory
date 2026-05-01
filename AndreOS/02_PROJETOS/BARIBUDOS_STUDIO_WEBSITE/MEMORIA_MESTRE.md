# BARIBUDOS STUDIO WEBSITE - MEMORIA MESTRE

## Objetivo
Website publico, comercial e de catalogo do ecossistema Baribudos Studio.

## Relacao com o Studio
O website e controlado pelo Baribudos Studio atraves de endpoints administrativos. O Studio e o cerebro operacional; o website e a camada publica/comercial.

## Repo
`AndreVazao/baribudos-studio-website`

## Stack confirmado
- Next.js 14
- React 18
- TypeScript
- Prisma
- PostgreSQL

## Estado implementado em 2026-05-01
Foi adicionada documentacao no website para clarificar a ligacao com a memoria persistente do Studio:

- `docs/STUDIO_MEMORY_LINK.md`

## Regras obrigatorias
- O website nao deve guardar memoria operacional sensivel.
- Segredos devem ficar apenas em variaveis de ambiente ou gestor seguro.
- Estado publico, catalogo, produtos e publicacoes vivem no website.
- Decisoes, historico operacional e contexto de IA vivem no Studio e no `andreos-memory`.

## Proximo foco
Integrar o dashboard do Studio com uma UI de memoria que tambem mostre o estado do website, divergencias e publicacoes sincronizadas.
