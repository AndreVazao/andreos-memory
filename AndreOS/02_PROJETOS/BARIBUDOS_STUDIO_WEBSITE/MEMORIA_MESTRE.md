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


## Checkpoint operacional — 19-11-2026

### Integração de publicação e pagamentos
- Website PR #43 consolidou o trabalho útil de PRs #26–#29 e foi integrada em main no commit `d5dc761671496b91b0360a5bd43d2679b121fba3`. PR #26 ficou fechada como supersedida/consolidada, não merged individualmente.
- Website CI #187 e Repository Visibility #178 passaram no head #43; Vercel status success.
- Implementado: checksum SHA-256 real, ingestão Serializable/idempotente, snapshot completo de assets (ainda URLs, não bytes), preços transacionais, conflitos retryable, sessão de utilizador desativado rejeitada e fulfillment Stripe/PayPal validado/transacional.
- Gates: baseline migration ausente/incompleta, unicidade declarativa de produto ativo por variante não aplicada, assets ainda não materializados em storage durável. Não há catálogo comercial (última consulta de 18-11: produtos/publicações/variantes/assets/bundles/checkouts = 0; buckets/objects = 0).

### Segurança e infraestrutura
- Supabase `public.system_metadata`: RLS disabled, zero policies, grants anon/authenticated excessivos (issue #39). Não aplicar DDL até recuperar baseline, identificar consumidores e rever privileges.
- Vercel SSO/domínio público, flags de secret visibility e acesso anónimo continuam por validação. Valores de secrets não foram lidos. Render account/services/disks continua não verificado.
- Website PR #44 Draft: sanitiza erros públicos de checkout/capture/webhook Stripe/PayPal; separa JSON inválido (400) de falha de processamento (500), adiciona helper/testes. Head `8f0067d954aedacb439d3f43a4b53fd7552a5b72`; Repository Visibility #181 success, Website CI #190 ainda in progress na última verificação e Vercel pending.
- Não houve produção, migrations, credentials, storage ou infraestrutura alterados.

### Roadmap
Website deve materializar bytes de assets no storage durável já disponível (primeiro verificar Render/Vercel e recursos contratados; não criar custos), vender com Studio offline, reconciliar eventos quando Studio regressa e só depois integrar canais externos (ebook, audiobook e YouTube Studio) com aprovação por canal no Studio.


### Follow-up security issue — 19-11-2026
- Website issue #45: PayPal capture endpoint currently uses submitted provider order ID as lookup and capture capability without signed-in ownership or a separate one-time/expiring guest capability. Guest checkout is supported, so auth must be designed without breaking guest flows; tests for wrong-user/expiry/replay/success required. No fix or production change yet.
