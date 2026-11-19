# Última Sessão — Baribudos Website

## Data
19-11-2026

## Progresso confirmado
- Website PR #43 consolidou o trabalho útil das antigas PRs #26–#29 e foi integrada: `d5dc761671496b91b0360a5bd43d2679b121fba3`. PR #26 ficou closed/superseded, não merged individualmente.
- Website CI #187 e Repository Visibility #178 SUCCESS; Vercel status SUCCESS no head #43.
- Main contém ingestão Studio transacional/Serializable com checksum SHA-256, proteção de versões, preço, assets snapshot (URLs ainda não bytes) e fulfillment Stripe/PayPal.
- PR #44 Draft: sanitização dos erros públicos de checkout Stripe, PayPal create/capture e webhook Stripe; JSON inválido tratado 400, falhas processamento genéricas 500. Head `8f0067d954aedacb439d3f43a4b53fd7552a5b72`; Repository Visibility #181 SUCCESS, Website CI #190 in progress, Vercel pending.

## Bloqueios
- Catálogo vazio (consulta read-only de 18-11): produtos, publicações, variantes, assets, bundles e checkouts = 0; Supabase Storage buckets/objects = 0.
- Supabase system_metadata RLS disabled e grants anon/authenticated excessivos (issue #39). Não alterar produção até baseline migration e consumidores identificados.
- Unicidade declarativa variante/product ativa ainda falta; migration baseline não reconciliada.
- Assets não materializados em storage durável: Website ainda depende de URLs; autonomia com Studio desligado não provada.
- Vercel public access, secret visibility e Render service/disks ainda por confirmar.

## Próxima frente
Completar CI/review PR #44; corrigir segurança Supabase apenas após baseline; estabelecer storage durável existente sem contratar recursos; reconciliar recibos reais Studio→Website; testes de checkout/webhooks/replay; manter Studio como autoridade editorial/comercial.
