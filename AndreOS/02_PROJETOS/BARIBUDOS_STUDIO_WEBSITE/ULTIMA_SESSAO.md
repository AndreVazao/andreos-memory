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
- PR #42 integrada em main no commit `fc9bb3c1b3612af6d7239c2fa00ff384687e3cc4`; Website CI #177 e Repository Visibility #171 passaram; Vercel production deployment `dpl_CN8PAoTSUuJvjKYuhcBuGkzctAUi` ficou READY.
- Atualizada issue #30 com estado de storage/Render, issue #39 com revalidação Supabase e issue #40 com SSO/acesso público.

## Bloqueios
- Resolver system_metadata com baseline e consumidores identificados antes de DDL.
- Materializar assets duráveis no Website e provar funcionamento com Studio desligado.
- Configurar e demonstrar acesso público anónimo aprovado.
- Fechar testes de pagamento, sessão, migrações e unicidade comercial.

## Próximo passo
Continuar pela segurança e integridade comercial; depois concluir autonomia de assets e só então iniciar distribuição externa.


## Atualização de branches após os merges documentais — 18 Nov 2026

- Website PR #42 integrada em main no commit `fc9bb3c1b3612af6d7239c2fa00ff384687e3cc4`; CI #177 e Repository Visibility #171 passaram; deployment de produção `dpl_CN8PAoTSUuJvjKYuhcBuGkzctAUi` ficou READY.
- Website PR #26 recebeu merge commit de sincronização `1e014ac29595566ee12d0cdfddb4798de953dc22`: 46 commits ahead / 0 behind. Website CI #179 e Repository Visibility #173 passaram; preview Vercel READY. Continua Draft por unicidade comercial, baseline de migrations e materialização de assets.
- Website PR #27 recebeu merge commit `ef37c4145b9990cc0ae61a14d6ab01875b341911`: 9 ahead / 0 behind. CI #180 ainda executava build na última consulta; typecheck e quatro testes da política ativa passaram. Falta integração real cookie/JWT + utilizador desativado.
- Website PR #28 recebeu merge commit `e3e1093c39a1fc8ea3c7755fcfe27072dcd16621`: 5 ahead / 0 behind; CI #181 em execução.
- Website PR #29 recebeu merge commit `8401ffa590f4ec2fa3d033d38277ced0fe4e0119`: 3 ahead / 0 behind; CI #182 em execução.
- As PRs #27–#29 continuam Draft; não foi feito merge de código de pagamentos/sessões.
- A PR #76 de memória permanece Draft; o repositório não devolveu workflow runs para o head atual, por isso não se declarou CI nem merge.
