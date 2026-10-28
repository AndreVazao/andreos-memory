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


## Follow-up: broadened schema smoke assertions (2026-10-28)
- Expanded the read-only disposable DB smoke script to assert RLS on `trader_departments` as well as the existing registry/provenance/artifact tables.
- Expanded direct-read grant checks to cover anon/authenticated on organizations, memberships, installations, departments, agents, provenance, and shared artifacts.
- This is source-level test coverage only. No disposable Supabase/Postgres database was available in this session, so the script has not been executed and does not prove migration/runtime correctness.
- Before the latest test-only commit, exact-head CI on `0df93d834840297abdf1662d04dd813859b799b0` passed Python, Shared Learning tests/typecheck/build, PAPER smoke, Windows EXE/installer smoke, and Snyk. Vercel still failed with an explicit build-rate-limit response. Latest commit must receive its own exact-head CI check.
- PR #504 remains open/unmerged. Do not deploy, apply migrations to production, activate cloud sync, or enable live trading. Next: verify exact-head CI, then run this script against a disposable Supabase/Postgres instance and add two-session publication/revocation and duplicate/conflict integration tests.


## Follow-up: transactional source-lineage validation (2026-10-28)
- Code review found the publication RPC stored the signed source-artifact ID list without independently checking source eligibility in the transaction.
- Added a transaction-level loop to the RPC. It rejects non-string/empty/duplicate IDs and requires each source to resolve to an eligible, unexpired artifact with verified, non-revoked provenance, active `cross_org_public` organization, approved installation, active agent, and valid department ownership. Relevant rows are locked while publication executes. API maps `source_lineage_not_eligible` to HTTP 409.
- This has not yet been validated in a real disposable Supabase/Postgres database. The current environment has no `psql` executable. Two-session race tests remain mandatory; do not claim the lock behavior is proven.
- Product branch HEAD at this point: `dcb86efd1cedcb15870f6c9b8dcc5d0be47f0125`. Python, Shared Learning, PAPER and Windows workflows pending; Vercel build-rate-limit failure and Snyk pending on this new head. Prior head `49b19ce62c56a49b1244223f1cb2ec539f83c0cc` passed Python, Shared Learning, PAPER, Snyk and Vercel; Windows EXE passed, installer still in progress at last poll.
- PR #504 remains open/unmerged. No production migration, cloud activation, orders, transfers or live trading. Next: exact-head CI, disposable DB smoke and concurrency tests, then trusted enrollment/key lifecycle and local memory persistence/recovery.


## Follow-up: latest head and restarted exact-head CI (2026-10-28, 09:28 UTC)
- Product PR #504 remains open and unmerged. Current HEAD is `2a2e0330a0032652afbe522e01e4f998808ef862` (documentation-only commit atop code changes at `dcb86efd1cedcb15870f6c9b8dcc5d0be47f0125`).
- Added transaction-level source-lineage validation in the publication RPC. It rejects non-string, empty and duplicate source IDs and requires each source artifact to remain eligible, unexpired, verified, non-revoked, owned by an active `cross_org_public` organization, and tied to approved/active registry identities. Source rows are locked during publication. API maps missing/ineligible source lineage to HTTP 409.
- Exact-current-head CI restarted: Python run `40664424298` in progress, PAPER run `40664424265` in progress, Shared Learning run `40664424474` pending, Windows EXE/installer run `40664424230` pending. Vercel currently reports build-rate-limit failure; Snyk pending for this new head.
- Previous code-head PAPER run `40664337403` passed; Python run `40664337419` was cancelled, not passed. Shared Learning and Windows runs `40664337468` and `40664337305` were still in progress at last poll. Do not claim all checks green.
- The read-only schema smoke script and transaction-level source checks have not been executed against a disposable Supabase/Postgres instance. Current runtime has no `psql`; database integration/concurrency remains a hard release gate.
- Product docs updated in `docs/PROJECT_CONTEXT.md` at commit `2a2e0330a0032652afbe522e01e4f998808ef862`. PR body reflects current gate status. No production migration, cloud activation, account provisioning, orders, transfers or live trading.
- Next: poll exact-current-head CI; fix any failure. Then run disposable DB schema smoke and two-session publish/revoke + duplicate/conflict lineage tests. Continue trusted enrollment/key lifecycle and local memory persistence/recovery only after CI stabilizes.


## Follow-up: exact-current-head CI poll (2026-10-28, latest poll)
- Product PR #504 HEAD remains `2a2e0330a0032652afbe522e01e4f998808ef862`, open and unmerged.
- Exact-head Python tests run `40664424298`: SUCCESS (test suite completed).
- Exact-head Shared Learning Service run `40664424474`: SUCCESS (npm test, TypeScript typecheck, production build).
- Exact-head Trading engine PAPER smoke run `40664424265`: SUCCESS.
- Exact-head Windows EXE run `40664424230`: EXE build/smoke passed; installer build completed and silent install/launch/health/uninstall smoke test is still running at latest poll. Do not count Windows workflow as fully green until installer job completes.
- Exact-head Snyk: SUCCESS. Vercel remains FAILURE due to the platform's build-rate-limit response, not an application test result.
- SQL schema smoke and two-session publication/revocation/lineage tests remain unexecuted because no disposable Supabase/Postgres connection or `psql` is available in this session. Source inspection confirms the smoke script is read-only; it does not prove migration correctness.
- Next: poll Windows installer smoke to completion. Keep PR open/unmerged; no production migrations, cloud activation, enrollment, orders, transfers, or live trading.


## Follow-up: deterministic source-lock ordering (2026-10-28, 09:38 UTC)
- Confirmed exact prior HEAD `2a2e0330a0032652afbe522e01e4f998808ef862`: Python tests, Shared Learning test/typecheck/build, PAPER smoke, Snyk, EXE smoke and installer silent install/launch/health/uninstall smoke all passed. Vercel failed due to build-rate-limit.
- Added code commit `1b35777e25c4792a5f7d2611beb869b7a8f4dc69` to sort declared source IDs lexically before acquiring source-row locks in the publication RPC. This reduces avoidable deadlocks when concurrent requests have overlapping source sets supplied in different orders; it does not prove all database locking behavior safe.
- PR #504 body updated to describe the current HEAD and exact outstanding gates. PR remains open/unmerged; the connector reports mergeable=true at this poll.
- New code HEAD has not yet returned its own CI runs/statuses. Do not transfer prior-head pass results to this commit.
- SQL smoke and two-session database tests still need a disposable Supabase/Postgres environment; not executed. No production migration, cloud activation, signing activation, orders, transfers or live trading.
- Next: poll exact-head CI. Then complete disposable DB smoke/concurrency tests and the missing enrollment/key lifecycle and local learning-memory persistence/recovery gates before cockpit work.


## Follow-up: current-head CI after lock-order hardening (2026-10-28, 09:40 UTC)
- Product HEAD remains `1b35777e25c4792a5f7d2611beb869b7a8f4dc69`; PR #504 open/unmerged.
- Exact-head PAPER smoke run `40665707449`: SUCCESS.
- Exact-head Snyk: SUCCESS. Exact-head Vercel: SUCCESS (previous build-rate-limit failure has cleared on this commit).
- Exact-head Shared Learning run `40665707313`: npm test, TypeScript typecheck and production build steps all completed successfully; workflow still finishing post-job cleanup at last poll.
- Exact-head Python run `40665707122`: test suite still in progress at last poll.
- Exact-head Windows EXE run `40665707053`: EXE and installer workflow still in progress; installer build not yet completed at last poll.
- The deterministic source-ID ordering change is not yet fully validated until all exact-head workflows finish.
- Disposable database smoke/concurrency tests remain unavailable in this session. Next: poll Python and Windows final conclusions; then plan integration validation with disposable Supabase/Postgres. No production/cloud/live execution changes.


## Follow-up: durable-memory input validation and latest code head (2026-10-28, 09:53 UTC)
- Exact prior product HEAD `1b35777e25c4792a5f7d2611beb869b7a8f4dc69` is fully green: Python tests, Shared Learning tests/typecheck/build, PAPER smoke, Windows EXE + installer smoke, Snyk and Vercel all reported SUCCESS.
- Updated PR #504 body to reflect those exact-head results and the remaining database/enrollment/memory integration gates.
- Hardened `PC_ENGINE/learning/sqlite_memory.py`: `expected_version` now accepts only a non-negative integer or `None`; explicitly rejects booleans, floats, strings and negative integers before opening a write transaction. Added regression cases in `tests/test_sqlite_learning_memory.py`.
- Latest product branch HEAD: `1cd9c87eb5e4f203e503f7ba48fbb677e6da5ace`. Its exact-head workflow runs/statuses have not appeared yet in the GitHub connector response. Do not transfer prior-head green results to this new commit.
- PR #504 remains open and unmerged. No database smoke/concurrency tests executed; no disposable Supabase/Postgres connection available. No production migrations, cloud activation, key enrollment, orders, transfers or live trading.
- Next: poll exact-head CI for `1cd9c87...`; then continue only with verifiable local-memory multi-connection/recovery tests and disposable database integration when an actual DB is available. Cockpit work remains deferred until brain gates are stronger.


## Follow-up: CI progress after SQLite version-input validation (2026-10-28, 10:00 UTC)
- Current product HEAD `1cd9c87eb5e4f203e503f7ba48fbb677e6da5ace`.
- Current-head Shared Learning Service run `40667653003`: SUCCESS (tests, TypeScript typecheck and production build).
- Current-head Trading engine PAPER smoke run `40667652980`: SUCCESS.
- Current-head Snyk: SUCCESS. Vercel: FAILURE due to platform build-rate-limit response.
- Current-head Python run `40667652911`: IN PROGRESS. Windows EXE/installer run `40667652913`: PENDING at latest poll.
- Updated PR #504 body to match these exact current-head statuses and remaining release gates. PR remains open/unmerged.
- SQLite input validation now rejects bool/float/string/negative `expected_version` values before writes; regression tests were added. This is not fully validated until the exact-head Python suite finishes.
- Disposable Supabase/Postgres schema smoke and two-session concurrency tests remain unexecuted. No production/cloud/live-trading changes.


## Follow-up: brain programming CI confirmed; offline mobile office started (2026-10-28, 10:30 UTC)
- Exact product HEAD for PR #504 is `1cd9c87eb5e4f203e503f7ba48fbb677e6da5ace`. Python tests, Shared Learning Service tests/typecheck/build, PAPER smoke, Windows EXE/installer workflow, and Snyk are SUCCESS. Vercel remains FAILURE with a platform build-rate-limit response.
- Updated PR #504 body to reflect the final exact-head status. It remains open/unmerged due to unexecuted real database smoke/concurrency tests and enrollment/key-lifecycle/integration gates.
- Opened draft PR #506: `https://github.com/AndreVazao/VazaoSovereignTrader/pull/506`, branch `work/mobile-virtual-office-demo-main-2026-10-28`. It adds a Kivy-native **Escritório** page to the Android cockpit, explicitly offline from PC_ENGINE, with 2.5D, Pixel/8-bit, Palitinhos and Compacta modes. Selecting HD 3D is honestly marked future-only and falls back to 2.5D; no real 3D renderer is claimed.
- The office includes CEO, Market Radar, exchange comparison, investigation, analysis, central memory, fast response, risk control and PAPER Lab. It shows no fabricated prices/P&L/orders/agent activity and sends no PC API calls from the office page.
- PR #506 hosted checks: mobile contract tests and Python compile completed successfully in both APK and Android-emulator workflows. APK build and emulator/Maestro startup smoke are still running at last poll. Physical-phone launch/logcat remains a separate required check.
- The existing browser prototype `virtual_office/prototype/index.html` already has adaptive CSS visual modes, but it is a presentation prototype; the Android Kivy page is a separate lightweight offline first pass.
- No production migrations, cloud activation, account provisioning, orders, transfers or live trading enabled.


## Follow-up: mobile office wording correction and CI recheck (2026-10-28, 10:34 UTC)
- PR #506 remains OPEN, DRAFT and unmerged: https://github.com/AndreVazao/VazaoSovereignTrader/pull/506.
- Latest PR #506 HEAD: `4cf320feea03c69c338fde8f74f82cb685141cf2`. A small UI wording fix changes the mode status from “cérebro desligado” to “dados reais desligados”, because this offline visual demo does not determine whether the separate headless brain is running.
- GitHub reports `mergeable=false` at this poll; no merge attempted. Investigate only after the current PR/check processing settles.
- Android APK workflow run `40672181949` (#77) remains IN_PROGRESS at “Build debug APK”; upload is pending. Android Emulator UI Smoke run `40672181950` (#33) remains IN_PROGRESS at “Build emulator-compatible debug APK”; emulator launch/Maestro and evidence upload have not started.
- Both runs were triggered on the earlier PR commit `a4d53488fb676e63e7e62be79dbd24855b13db53`; the new HEAD `4cf320f...` has not yet returned its own workflow run records. Do not count either run as final validation of the latest wording fix.
- Earlier mobile contract tests and Python syntax compile passed on the workflow's checked-out commit. APK is not yet available as an artifact. Physical Android installation, launch and logcat remain required.
- PR #504 is unchanged: HEAD `1cd9c87eb5e4f203e503f7ba48fbb677e6da5ace`, open/unmerged. Python, Shared Learning, PAPER, Windows EXE/installer and Snyk were reported successful on that exact head; Vercel failed due to a build-rate-limit response. Disposable Supabase/Postgres smoke/concurrency, trusted enrollment/key lifecycle and local-memory integration/recovery remain hard gates.
- No production migration, cloud activation, real account provisioning, orders, transfers or live trading.


## Follow-up: Android workflows restarted on latest PR #506 HEAD (2026-10-28, latest poll)
- PR #506 current HEAD remains `4cf320feea03c69c338fde8f74f82cb685141cf2`, open, draft, unmerged; GitHub currently reports mergeable=true.
- The previous APK run `40672181949` and emulator smoke run `40672181950` ended CANCELLED before APK build finished and before emulator launch. No APK artifact was produced by those runs.
- Re-triggered the two Android workflows on the latest PR head. New APK run: `40673079563` (#78). New emulator UI smoke run: `40673079516` (#34).
- In both latest-head runs, mobile contract tests and Python syntax compile passed. APK build is currently IN_PROGRESS in both workflows; upload and emulator/Maestro startup test remain pending.
- Latest workflow records are now associated with `4cf320f...`; do not treat the cancelled earlier runs as evidence of APK success.
- PR #504 remains open/unmerged at `1cd9c87eb5e4f203e503f7ba48fbb677e6da5ace`; the release gates and safety restrictions above remain unchanged.


## Follow-up: emulator APK build succeeded; startup smoke in progress (2026-10-28, latest poll)
- Android APK workflow run `40673079563` (#78) was CANCELLED during the Buildozer debug APK build. Its logs end with GitHub Actions `The operation was canceled` while Kivy/Python modules were being byte-compiled; no APK upload step ran. This is a cancellation, not a reported compiler failure.
- Android Emulator UI Smoke workflow run `40673079516` (#34) has successfully completed its emulator-compatible debug APK build and KVM setup. It is currently installing Maestro CLI. Emulator launch/startup smoke and evidence upload are still pending.
- Both workflows' contract tests and Python syntax compile passed on PR #506 HEAD `4cf320feea03c69c338fde8f74f82cb685141cf2`.
- No downloadable APK artifact is confirmed yet. Keep PR #506 open/draft; physical phone launch/logcat remains required even after hosted emulator smoke passes.


## Follow-up: Android emulator job cancelled and retried (2026-10-28, latest poll)
- Emulator UI Smoke run #34, ID `40673079516`, finished as CANCELLED during the emulator launch/Maestro smoke step, after the emulator-compatible APK build, KVM setup and Maestro installation succeeded. The evidence-upload step completed, but the run has no artifacts; no successful app launch is established.
- APK workflow run #78, ID `40673079563`, also ended CANCELLED during its debug APK build and produced no artifact.
- Mobile contract tests (8 tests) and Python syntax compile passed on merge commit `b7268ca84e0d6639862306aa998023517a340230`, representing PR #506 HEAD `4cf320feea03c69c338fde8f74f82cb685141cf2` merged for CI.
- Retried the cancelled emulator smoke job directly; GitHub accepted the retry. Await the new attempt's result before treating startup as validated.
- PR #506 remains OPEN/DRAFT/unmerged. No APK artifact is currently available. Physical-phone install, launch and logcat remain required.
- PR #504 remains open/unmerged with the brain release gates unchanged: disposable Supabase/Postgres schema and two-session concurrency tests, trusted installation enrollment/key lifecycle, and local-memory integration/recovery remain outstanding. No production/cloud/live-trading changes.


## Follow-up: emulator retry accepted and progressing (2026-10-28, latest poll)
- GitHub accepted a retry of the previously cancelled Android Emulator UI Smoke job. New job attempt ID: `122779920289`, within run `40673079516` (#34).
- Retry has passed setup, checkout, Python setup, the 8 mobile contract tests, Python syntax compile, Java setup and Android build dependency installation. Buildozer installation is currently in progress; APK build, emulator launch/Maestro smoke and evidence upload remain pending.
- No APK artifact or successful startup evidence exists yet. PR #506 stays open/draft/unmerged; physical-phone testing remains required.


## Follow-up: Android emulator UI smoke passed; standalone APK build retried (2026-10-28, 11:21 UTC)
- Android Emulator UI Smoke run #34, ID `40673079516`, is now SUCCESS on PR #506 HEAD `4cf320feea03c69c338fde8f74f82cb685141cf2` (CI checkout merge commit `b7268ca84e0d6639862306aa998023517a340230`).
- All steps passed: 8 mobile contract tests, Python syntax compile, emulator-compatible debug APK build, KVM setup, Maestro installation, emulator launch/UI smoke, and evidence upload.
- Logs contain visible app UI text after launch, including cockpit navigation and the “Escritório” page entry. This is concrete emulator launch evidence; it does not validate installation on the user's physical phone.
- Evidence artifact `vst-android-emulator-smoke` is available from run #34, artifact ID `12812221044`, 351,263 bytes; SHA-256: `26d2787104f3447bc1ecc35b1d3793c51768c2baa15831ab56ac3b13530dd5f8`. It is test evidence, not a standalone APK package.
- Standalone Android APK workflow run #78, ID `40673079563`, was cancelled during Buildozer APK build with upload skipped. Retried that cancelled job; new job attempt ID `122797154539` is in progress. No standalone APK artifact is available at this poll.
- PR #506 remains OPEN/DRAFT/unmerged. Physical-phone installation, launch and logcat are still required before calling the mobile app ready.
- PR #504 brain status and hard release gates unchanged: disposable Supabase/Postgres schema and two-session concurrency tests, trusted installation enrollment/key lifecycle, and local-memory integration/recovery remain outstanding. No production/cloud/live-trading actions.


## Follow-up: standalone APK rebuild now running; brain PR rechecked (2026-10-28, latest poll)
- After the successful emulator UI smoke, retried the cancelled standalone APK job. New attempt `122797154539` (run #78, `40673079563`) has passed mobile contract tests, Python syntax compile, Java verification, system dependency installation and Buildozer installation; the actual debug APK build is now IN_PROGRESS. Upload remains pending; no standalone APK artifact yet.
- PR #504 rechecked: still OPEN/unmerged, mergeable=true, current HEAD `1cd9c87eb5e4f203e503f7ba48fbb677e6da5ace`. Exact-head Python, Shared Learning Service, PAPER smoke and Windows EXE/installer workflows all SUCCESS. PR metadata still records Snyk SUCCESS and Vercel FAILURE due to build-rate-limit.
- Brain release gates remain unchanged: disposable Supabase/Postgres schema smoke, two-session race/RLS/grants tests, trusted installation enrollment and key lifecycle, and local memory multi-connection/restart/recovery/engine integration. Do not merge or declare release-ready based only on unit/CI success.


## Follow-up: standalone Android APK built and adaptive office preferences added (2026-10-28, 12:10 UTC)
- Standalone APK workflow run #78, ID `40673079563`, completed SUCCESS on product branch `work/mobile-virtual-office-demo-main-2026-10-28`, HEAD `4cf320feea03c69c338fde8f74f82cb685141cf2`.
- APK artifact `vazaosovereigntrader-android`, artifact ID `12813478029`, size 19,011,747 bytes, SHA-256 `fc7092a1605c21bc54dc28d520a166b3036e33f61c0572c839780f645dd9ca6e`, expires 2027-01-26. Download from workflow run: https://github.com/AndreVazao/VazaoSovereignTrader/actions/runs/40673079563. This is a standalone debug APK artifact, but physical-device install/launch/logcat remains untested and required.
- Emulator UI smoke run #34, ID `40673079516`, remains SUCCESS on the same PR #506 HEAD. It proves hosted emulator startup and visible UI only, not physical-phone readiness.
- Opened draft PR #507: https://github.com/AndreVazao/VazaoSovereignTrader/pull/507, branch `work/office-mode-preferences-2026-10-28`, initial head `84e035481857b308ffa7e3597f105f9a1b1fbadf`. It persists the office visual preference in app-private storage, defaults to Compacta on narrow screens and 2.5D light on wider screens, and retains the safe fallback for the future-only HD 3D option. Contract tests and README were updated. This is first-run preference selection, not an Android installer wizard.
- Exact-head Android APK run #80 (`40685498423`) and Android Emulator UI Smoke run #36 (`40685498413`) for PR #507 were IN_PROGRESS at checkpoint time. Do not count them as passing until final job conclusions are polled.
- PR #506 remains open/draft/unmerged pending review and final gates. PR #507 also remains open/draft/unmerged. Do not merge before exact-head checks and review.
- Brain PR #504 remains open/unmerged at `1cd9c87eb5e4f203e503f7ba48fbb677e6da5ace`; unit/CI passes do not close the outstanding database integration, two-session concurrency/RLS/grants, trusted installation enrollment/key lifecycle, and local learning-memory persistence/recovery gates.
- No production database migration, cloud sync activation, account provisioning, orders, transfers or live trading were performed.



## Follow-up: persisted office preference separated cleanly; brain concurrency regression added (2026-10-28, 12:15 UTC)
- Standalone debug APK workflow #78, run ID `40673079563`, is SUCCESS. Artifact `vazaosovereigntrader-android`, ID `12813478029`, 19,011,747 bytes, digest `sha256:fc7092a1605c21bc54dc28d520a166b3036e33f61c0572c839780f645dd9ca6e`. It was built from the pre-preference office HEAD `4cf320feea03c69c338fde8f74f82cb685141cf2`; do not treat it as the newest preference build. Physical phone install/launch/logcat still required.
- The persisted visual-mode feature is already being developed in the dedicated draft PR #507 (`work/office-mode-preferences-2026-10-28`, initial HEAD `84e035481857b308ffa7e3597f105f9a1b1fbadf)). It stores the preference locally, defaults to Compacta on narrow screens and 2.5D on wider screens, and keeps HD 3D future-only with a 2.5D fallback. Exact-head APK workflow #80 / run `40685498423` and emulator smoke #36 / run `40685498413` were IN_PROGRESS at last poll.
- An overlapping attempt to add preference persistence to PR #506 was reverted immediately; PR #506 is kept focused on the offline office demo, while PR #507 owns the adaptive preference feature. Revert commit on PR #506 branch: `b4db0a6c99c02d7621a1f2268ede69bd7a9b60d9`.
- Brain PR #504 branch `work/cross-org-learning-provenance-2026-10-27`: added a real SQLite multi-connection regression test `test_two_connections_serialize_competing_versioned_writes`. Two independent store connections race using the same expected version; expected result is exactly one commit, one VersionConflict, durable version/event history after reopen. Commit: `00e71f486760acf78e2adbdfba526f2c8952a11a`. Its exact-head test, PAPER, Windows packaging, Snyk and Vercel statuses were still running/pending at last poll; do not count as passed until confirmed.
- This local SQLite regression improves coverage but does NOT close real Supabase/Postgres two-session race/RLS/grants gates, trusted installation enrollment/key lifecycle, or production-engine wiring/restart/recovery. No production DB or live trading actions.



## Follow-up: local learning-memory concurrency regression passed; release workflows continue (2026-10-28, 12:18 UTC)
- PR #504 new exact-head commit `00e71f486760acf78e2adbdfba526f2c8952a11a` adds `test_two_connections_serialize_competing_versioned_writes`; the Python test-suite workflow completed SUCCESS for this head (run `40685571635`, job `122806934829`). The test covers two independent SQLite connections competing on the same expected version, exactly one winner/one conflict, and durable event/version history after reopen.
- PR #504 PAPER lifecycle/safety-boundaries job completed SUCCESS (run `40685571756`, job `122806935213`). Windows EXE smoke and installer build remained IN_PROGRESS at the latest poll (run `40685571674`). Snyk status SUCCESS; Vercel pending, so the complete PR gate is not green yet.
- PR #507 adaptive office preference feature still has exact-head Android APK workflow `40685498423` and emulator smoke `40685498413` in progress at the latest poll; both were still in the Buildozer APK build step. The earlier standalone APK artifact is not a build of PR #507.
- PR #506 duplicate preference changes have been reverted with commit `b4db0a6c99c02d7621a1f2268ede69bd7a9b60d9`, leaving the office demo and the adaptive preference feature in separate, focused PRs (#506 and #507 respectively).
- Important: SQLite concurrent-writer regression is now covered and passing, but the adapter remains documented as not wired into the production engine. Real Supabase/Postgres schema and race/RLS/grants tests, installation/key lifecycle, and runtime memory integration/startup-shutdown/restart-recovery are still release gates. No production/cloud/live-trading actions.


## Follow-up: PR #507 Android checks green; brain integration audit continued (2026-10-28, 12:22 UTC)
- PR #507 exact HEAD `84e035481857b308ffa7e3597f105f9a1b1fbadf`: Android APK workflow run #80 / ID `40685498423` completed SUCCESS; Android Emulator UI Smoke run #36 / ID `40685498413` completed SUCCESS.
- APK artifact `vazaosovereigntrader-android`, artifact ID `12815436574`, size 19,012,672 bytes, SHA-256 `8a4e3e152a7791867a15af176ca4439afb6d8f253e56a7c01d628523f2582bd4`, expires 2027-01-26. Download from workflow run: https://github.com/AndreVazao/VazaoSovereignTrader/actions/runs/40685498423. This APK includes PR #507 preference persistence and narrow-screen Compacta default. Physical phone ADB install/launch/logcat remains untested.
- Emulator smoke evidence artifact `vst-android-emulator-smoke`, ID `12814779198`, size 392,921 bytes, SHA-256 `9883caab895a559a7701536b38a0a7a0bb0be709d979629e2490b3c0feaee09d`; run link: https://github.com/AndreVazao/VazaoSovereignTrader/actions/runs/40685498413.
- PR #507 is still draft/open/unmerged. Do not merge yet without review of code/tests and final status checks. PR #506 also remains open/draft/unmerged.
- Continued PR #504 audit: reviewed the SQLite durable-memory adapter and tests. The adapter has WAL, busy timeout, BEGIN IMMEDIATE, optimistic version checks, append-only journal, restart persistence tests and two-connection race test. However `docs/DURABLE_LEARNING_MEMORY.md` explicitly says engine startup/shutdown wiring, backup/retention and multi-process deployment are still separate integration work; do not count local adapter tests as production engine wiring.
- Reviewed `verified_publication_schema_smoke.sql`: it checks organization visibility defaults/check constraint, RLS on seven registry/artifact tables, publication RPC execute grants, immutable signing-key trigger, and absence of direct anon/authenticated table SELECT grants. It is read-only but has not been run against a disposable Supabase/Postgres instance in this environment. Real DB two-session concurrency/RLS validation remains open.
- PR #504 exact-head prior CI remains Python tests, shared learning service, PAPER smoke, Windows EXE success; Vercel failure due to rate limit is infrastructure/quota, not a pass.
- No production database migration, cloud sync activation, account provisioning, orders, transfers or live trading were performed.


## Follow-up: first-run interface choice added; exact-head validation pending (2026-10-28, 12:32 UTC)
- Extended PR #507 head to `cd6ba66f718f94a964844a49a04eff09914c4062` and updated title/body: https://github.com/AndreVazao/VazaoSovereignTrader/pull/507.
- First app launch now presents two choices: **Chat simples** (lightweight) or **Escritório virtual**. The selected experience is stored privately, restored on subsequent launches, and can be changed at any time via the new **Modo** navigation entry. The chooser uses a ScrollView and fixed card heights to remain usable on small screens.
- Existing office profile preference remains separate: Compacta default on narrow screens, 2.5D light on wider screens; Pixel/8-bit and Palitinhos remain available, HD 3D remains future-only with 2.5D fallback.
- Updated source-contract tests and mobile README. Latest exact-head CI runs were created and pending at checkpoint time: Android APK run #85 / ID `40688441564`; Android Emulator UI Smoke run #41 / ID `40688441390`. The earlier head's green workflows do NOT validate these new chooser changes; poll the new runs before claiming success.
- APK built for earlier head `84e035481857b308ffa7e3597f105f9a1b1fbadf` remains available as artifact ID `12815436574`, but it does NOT include the new first-run chooser. Do not distribute that earlier artifact as the final chooser build.
- PR #507 remains draft/open/unmerged. Physical phone ADB install/launch/logcat still required.
- Brain status unchanged: PR #504 remains open/unmerged; real disposable Supabase/Postgres smoke, two-session race/RLS/grants, trusted enrollment/key lifecycle, and engine integration of durable local learning memory remain hard gates. SQLite adapter tests pass in CI but do not establish production engine wiring. No production/cloud/live trading actions taken.


## Follow-up: chat-only mode clarified and latest CI queued (2026-10-28, 12:34 UTC)
- Further extended PR #507 to HEAD `ed796b228e9048748b6dc098ebae7b2c06328a53`.
- Chat simples now hides nonessential navigation entries and keeps **Modo** visible so the user can switch back without reinstalling. The experience chooser uses a scrollable layout for small screens. Tests assert the first-run chooser, persisted selection and navigation hiding.
- Updated PR body and README. Latest exact-head workflows:
  - Android APK run #88, ID `40688666026`
  - Android Emulator UI Smoke run #44, ID `40688666349`
  Both were still pending/queued when last polled; no new APK artifact exists yet for HEAD `ed796b2...`. Earlier green runs belong to an older head and must not be treated as validation of this change.
- PR #507 remains draft/open/unmerged. Wait for exact-head checks before review/merge.
- Brain gate status unchanged. Current documented safe scope: SQL smoke has not run against a disposable Supabase/Postgres instance; no trusted registry enrollment/key lifecycle is wired end-to-end; durable SQLite adapter still needs integration into the engine lifecycle/departments. No DB/cloud/live trading action performed.
