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


## Follow-up: opt-in Python signer/adapter added (2026-10-28)
- Product branch HEAD at the time: `a67439eea7d0e9050a387e03ef18059cf4dc1212`; a documentation-only commit will advance the head again.
- Added `PC_ENGINE/core/shared_learning_provenance.py` with an injected-key Ed25519 signer using the shared RFC 8785/JCS canonical message and payload digest helpers.
- Added explicit `VercelSharedIntelligenceProvider.push_verified(..., signer=...)` posting the signed `{artifact, provenance}` wrapper to `POST /api/v1/artifacts`. Existing legacy `push()` is unchanged. Verified push requires explicit lineage IDs and fails closed unless server confirms verified provenance; no automatic runtime activation.
- Added tests for signature verification, digest binding, public allow-list privacy, explicit lineage, and no fallback to legacy acceptance.
- At last poll, exact-head PAPER smoke and Snyk passed; Python tests and Shared Learning CI were queued/in progress, Windows EXE pending, and Vercel failed due build-rate-limit. Do not claim the new signer tests passed until GitHub Actions reports success for the relevant code commit.
- Product docs updated at `docs/PROJECT_CONTEXT.md`; commit `dbfc982e2d67eaf693f37b8de2b31e492b9b2ca2`.
- Still blocked: trusted key provisioning/enrollment/approval/revocation/rotation, explicit cross-org visibility policy, disposable Supabase migration/RLS/RPC/lineage tests, and local-memory concurrency/recovery. Python signing remains opt-in only; no production sync or live trading.


## Follow-up: explicit cross-organization visibility gate (2026-10-28)
- Sovereign Trader PR #504 added migration `202610280001_cross_org_visibility_policy.sql`. All organizations default to `organization_only`; public cross-org discovery requires the exact `cross_org_public` opt-in. No organization is made public by migration.
- Verified provenance reads now require active public-opt-in status for the contributor organization and all lineage-source organizations, with a second fail-closed check before returning data.
- Legacy `GET /api/v1/artifacts` is scoped to the authenticated user's own rows so it cannot bypass verified provenance policy for cross-org reads.
- Added a unit test for the policy helper; current-head CI must pass before this change is considered validated.
- Product docs updated at commit `642533a31b7cc2935980e164dae086c20080f299`. Branch remains `work/cross-org-learning-provenance-2026-10-27`, PR #504 remains open/unmerged. No production migration, cloud sync activation, trading, orders, or transfers.
- Next gates: disposable Supabase tests for migrations/RLS/grants/RPC concurrency and revocation races; trusted owner/admin visibility controls; enrollment/approval/revocation/rotation of installation keys; local learning memory persistence/concurrency/recovery.


## Follow-up: publication/revocation race hardening (2026-10-28)
- Updated the verified publication RPC in PR #504 to lock active organization + publisher membership, approved installation, active agent and department rows with `FOR UPDATE` while publishing. This is designed to serialize concurrent revocation/suspension with publication.
- This remains an unverified database-level hardening until tested against disposable Supabase/Postgres, including concurrent revocation, duplicate publication, lineage, RLS and grants. Do not claim the race is eliminated yet.
- Product documentation checkpoint: `9bebf49442ff366785a0ca010eb44e9207ce235b`. PR #504 remains open/unmerged. Current-head CI must be checked after the latest source and docs changes; Vercel build-rate-limit remains unresolved.


## Follow-up: exact-head CI and disposable database smoke harness (2026-10-28)
- Confirmed exact-head workflows at `9bebf49442ff366785a0ca010eb44e9207ce235b`: Python tests, Shared Learning tests/typecheck/build, PAPER safety smoke, and Windows EXE workflow completed successfully; Snyk passed. Vercel remains failed due to build-rate-limit.
- Added `cloud/shared-learning/supabase/tests/verified_publication_schema_smoke.sql` as a read-only assertion script for a disposable Supabase/Postgres instance. It checks default-private visibility, visibility constraint, RLS, RPC grants, immutable installation key trigger, and no direct table read for anon/authenticated. It has not been executed against a live disposable database.
- Product docs checkpoint commit `0df93d834840297abdf1662d04dd813859b799b0`; this is a newer head and its CI must be rechecked. PR #504 stays open/unmerged.
- Next: run SQL smoke in disposable Supabase, add two-session concurrency tests for publish-vs-revoke and duplicate/conflicting publication, then complete trusted key enrollment/approval/revocation/rotation and local memory persistence/recovery tests. No production migration, cloud activation, or live trading.
