# Checkpoint — VazaoSovereignTrader PR #504
Data: 2026-10-28 (UTC)

## Estado GitHub verificado
- Repositório do produto: AndreVazao/VazaoSovereignTrader.
- PR #504 continua OPEN e não mergeada: https://github.com/AndreVazao/VazaoSovereignTrader/pull/504
- Branch única desta tarefa: `work/cross-org-learning-provenance-2026-10-27`.
- HEAD atual observado após a extensão dos vetores: `ada068facdbc46e63fe89e96ab2198cb53e0a8fd`.
- O commit anterior `434f37e05721311b3ad4f9a01072403f7778ad03` teve sucesso nos workflows Python tests, Shared Learning Service, Windows EXE/installer e Trading engine PAPER smoke. Esses resultados não validam o novo HEAD.
- Para `ada068facdbc46e63fe89e96ab2198cb53e0a8fd`, o endpoint de workflows ainda não devolveu runs; Snyk está PENDING e o check Vercel falhou com indicação de build rate limit. Não declarar CI final verde. GitHub reportou temporariamente `mergeable=false`; investigar/confirmar antes de qualquer decisão.

## Canonicalização TypeScript/Python
- O branch já usa `PC_ENGINE/core/canonical_json.py` com a biblioteca `rfc8785`, e TypeScript implementa serialização ECMAScript, ordenação de chaves por unidades UTF-16, escaping JSON e rejeição de surrogates inválidos.
- Os dois runtimes leem o fixture partilhado `cloud/shared-learning/tests/fixtures/canonical-json-vectors.json`.
- Nesta sessão foi corrigido um erro de escaping no fixture que tinha sido gravado inicialmente de forma inválida. O conteúdo foi validado com JSON.parse antes da segunda gravação.
- HEAD do fixture: blob SHA `a77637e04339e58a4f6752e9bd5370a33ff03c68`.
- Foram acrescentados vetores para zero negativo (entrada literal `-0.0`, bytes canónicos `{"value":0}`) e escapes de caracteres de controlo/aspas.
- Os sete digests declarados foram recalculados independentemente com SHA-256 sobre as strings canónicas UTF-8 e coincidiram:
  - property-order: `6f8e07a68fb3342735f01b788af3e724a7056b40e2aad3d4321d38f7de49f905`
  - number-format: `b04cff7ab24fc44e872971bc226145e0e463d3419039d12d4cd678a7183fe443`
  - unicode/escaping: `1d121f17fdfccad1823ead75968568570fc4ba4bc544bf1e5819b48892324ab2`
  - nested array: `890892ec384db5b85e7e42a8ed4e631892f2af6e32d2f8c99fd8b8c75e24cd86`
  - UTF-16 key ordering: `28c95d1bbb2209223307e62f489020e8f9e0cfa16adf2daf6d88127a1e8dd22a`
  - negative zero: `23d7b286bd429460b92a2a1c21b6afc34110446c5034c17363fda363aa0a7c5d`
  - control/quote escaping: `45c0045e372e453176acb8bde77a2b90fe30adba79a7d821e94c95443658edc2`
- Independent hashing validates the stored digest values against the declared canonical byte strings; it does not replace executing both runtimes on the exact HEAD.
- Python signing remains disabled. No production synchronization or deployment enabled.

## Bloqueios / próximo passo
1. Confirmar os checks exatos de `ada068f...`, incluindo o resultado Snyk e a limitação Vercel; repetir/verificar o estado após a conclusão do processamento GitHub.
2. Confirmar que os testes TypeScript e Python aceitam todos os sete vetores e o vetor Ed25519 partilhado no mesmo HEAD.
3. Se um check não correr por causa do rate limit, documentar isso como não validado; não declarar sucesso por inferência.
4. Depois continuar com adaptador Python + endpoint de proveniência verificada, inscrição/aprovação/revogação/rotação de instalações, testes de integração Supabase descartável, política de visibilidade entre organizações e integração da memória local.
5. Manter PAPER/read-only. Não aplicar migrações em produção, não habilitar assinatura Python, não executar ordens ou transferências e não fazer merge enquanto houver checks/bloqueios pendentes.

## Segurança e arquitetura
Cérebro independente da UI; aprendizagem local não depende da rede/Vercel; partilha cross-org apenas de artefactos aprovados e metadados públicos permitidos; partilha consultiva sem autoridade de negociação; sem credenciais, saldos, ordens ou memória privada.


## Follow-up: numeric fixture token correction (2026-10-28)
- Sovereign Trader branch HEAD at the time of this note: `59b7c93bdbb12aebd5969d1e90692456b1508de2`.
- Corrected shared fixture input token `100000000000000000000` to `1e20` so Python JSON parsing yields a binary64 float compatible with RFC 8785's number domain. Canonical expected output remains `100000000000000000000`.
- JSON syntax passed validation. All seven declared canonical UTF-8 strings' SHA-256 values were recalculated independently and matched expected digests.
- Exact-head GitHub Actions were not final at last poll: Python tests, Shared Learning Service and PAPER smoke in progress; Windows EXE pending. Snyk pending; Vercel failed due build-rate-limit indication.
- Product documentation also updated in `docs/PROJECT_CONTEXT.md`; its commit is `d298e8726b480174d589610424a2b0cae4d9d7cb`, which advances the product branch HEAD and triggers fresh checks.
- Keep PR #504 open; Python signing disabled; no production sync or migration. Next action is to inspect checks on the new exact HEAD and resolve any failing test.
