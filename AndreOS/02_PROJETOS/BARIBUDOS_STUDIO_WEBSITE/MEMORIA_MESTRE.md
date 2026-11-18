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



## Estado operacional — 18-11-2026

### Autoridade e autonomia
- Studio continua a autoridade editorial/comercial e define conteúdo, aprovação, preço, metadados e canais.
- Website deve continuar a vender e servir assets com Studio desligado; reconciliar eventos quando o Studio voltar online.
- Arquitetura confirmada: Vercel para Website; Render conforme serviços realmente existentes. Não presumir configuração Render sem inspeção.

### Website — segurança, catálogo e infraestrutura
- Main observado: `e72c08ffada86aadafe89674c4aa92fa590f4148`; PR #41 integrada; CI #44068506534, Visibility #44068506634 e deployment de produção READY.
- Vercel: SSO ativo com `all_except_custom_domains`; três domínios Vercel, nenhum domínio customizado listado. Acesso público anónimo não foi demonstrado.
- Supabase `ACTIVE_HEALTHY`; `public.system_metadata` continua RLS desativado, 2 linhas, zero políticas e grants excessivos a anon/authenticated. Não executar DDL sem baseline e consumidores reconciliados.
- Catálogo: Product, Publication, PublicationVariant, PublicationAsset, BundleGroup e Checkout com zero registos. Supabase Storage: zero buckets e objects.
- Vercel integration configurations do projeto: lista vazia; inventário completo de Storage stores não exposto. Render sem conector e sem manifest explícito nos repositórios ativos.

### PRs
- #26: 45 commits ahead / 0 behind, CI #170 e preview READY; Draft. Falta unicidade declarativa por variante, baseline de migrations e materialização durável dos assets.
- #27: adicionados helper de sessão ativa e quatro testes; CI #176 e preview READY. Falta teste de integração com cookie JWT + utilizador desativado + biblioteca/checkout; Draft.
- #28 e #29: CI/previews anteriores verdes, mas continuam Draft e sem testes de integração dedicados de pagamento/replay.
- PR #42 atualiza audit e roadmap de distribuição; Draft até CI.

### Distribuição externa
Ebooks, audiobooks e YouTube são fase posterior à autonomia Website. Mapear APIs oficiais, formatos, metadados, direitos, territórios, preços/royalties e contas. YouTube Kids não deve ser tratado como API direta; usar fluxo oficial YouTube/YouTube Studio e validação de elegibilidade. Aprovação por canal continua no Studio.
