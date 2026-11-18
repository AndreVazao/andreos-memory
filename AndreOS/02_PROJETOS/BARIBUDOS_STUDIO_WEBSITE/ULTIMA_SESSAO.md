# Ultima Sessao - Baribudos Studio Website

## Data
2026-11-18

## O que foi feito
- Revalidados os repositórios ativos, PRs, CI, branches e deployments.
- PR #41 já está integrada; produção Vercel READY no commit main `e72c08ffada86aadafe89674c4aa92fa590f4148`.
- PR #26: 45 commits ahead / 0 behind; CI #170 e preview READY. Mantida Draft por falta de unicidade declarativa, baseline de migrations e storage durável.
- PR #27 recebeu helper puro para política de sessão ativa, declaração TypeScript e quatro testes Node; Website CI #176, Repository Visibility #170 e preview Vercel READY. Falta teste de integração cookie/JWT + desativação + endpoints reais.
- PRs #28 e #29 continuam Draft; precisam testes de integração para captura/webhook e replay.
- Supabase Security Advisor confirmou novamente RLS desativado em `public.system_metadata`; 2 linhas, zero policies e grants excessivos. Nenhum DDL executado.
- Contagens read-only: Product/Publication/Variant/Asset/Bundle/Checkout = 0; Supabase Storage buckets/objects = 0.
- Vercel SSO ativo em todos os domínios Vercel listados; sem domínio customizado. Acesso anónimo não demonstrado.
- Vercel project integrations list vazia; inventário completo de stores não disponível. Render sem conector nesta sessão e sem manifest nos repos.
- Criada PR #42 para atualizar o audit de produção e roadmap de distribuição externa; Draft até CI/revisão.
- Atualizada issue #30 com estado de storage/Render, issue #39 com revalidação Supabase e issue #40 com SSO/acesso público.

## Bloqueios
- Resolver system_metadata com baseline e consumidores identificados antes de DDL.
- Materializar assets duráveis no Website e provar funcionamento com Studio desligado.
- Configurar e demonstrar acesso público anónimo aprovado.
- Fechar testes de pagamento, sessão, migrações e unicidade comercial.

## Próximo passo
Continuar pela segurança e integridade comercial; depois concluir autonomia de assets e só então iniciar distribuição externa.
