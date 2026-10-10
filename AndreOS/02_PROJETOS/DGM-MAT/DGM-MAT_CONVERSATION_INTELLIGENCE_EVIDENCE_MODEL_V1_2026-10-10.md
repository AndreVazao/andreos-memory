# DGM-MAT — Conversation intelligence evidence model v1
Date: 2026-10-10
Status: implementation in review; not merged; automated checks not yet confirmed.

## Canonical priority
The primary mission remains authorized conversation-history recovery, project classification/linking, and reconstruction of evolving user intent before non-urgent engineering. Never conflate user requests, AI suggestions, confirmed user decisions, and verified runtime/repository facts.

## Implementation checkpoint
DGM-MAT branch: `feat/conversation-turn-semantics-v1`
Draft PR: https://github.com/AndreVazao/DGM-MAT/pull/71
Feature document: https://github.com/AndreVazao/DGM-MAT/blob/feat/conversation-turn-semantics-v1/docs/architecture/CONVERSATION_INTELLIGENCE_EVIDENCE_MODEL_V1_2026-10-10.md

Changes on the feature branch:
- Added ordered `ConversationMessage` records with role, message ID, timestamp, source and metadata.
- JSON ingestion extracts explicit `messages` arrays and OpenAI-style `mapping` nodes. Missing roles remain `unknown`; attribution is not guessed.
- Added data structures for `UserIntent`, `AIProposal`, `UserDecision`, `ConversationRelation`, `ImportCoverage`, and `ArtifactProvenance`.
- Intent/decision states default to `unverified`; proposals are separate from user decisions.
- Import coverage validation rejects false complete claims when discovered/imported counts disagree.
- Code artifacts include source conversation/provider/path/URL and a code fingerprint.
- Added tests for message separation, unknown roles, mapping order, unverified defaults, and coverage validation.

## Verification truth
- Draft PR is open and not merged.
- The connector reported no PR-triggered workflow runs and no commit statuses for the head commit at the time checked. This is not a passing test result.
- Tests have not been run locally in this tool session.
- No authenticated provider history import, durable checkpointing, persistent relationship graph, or remote rename/regroup has been implemented by this change.
- Existing aggregate content remains for compatibility.

## Next
1. Get a real test run/CI result; repair any regressions before merge.
2. Extend extraction only with fixtures from real, authorized exports and preserve raw-source provenance.
3. Add persistence and idempotent import checkpoints with honest coverage states.
4. Build intent/decision temporal evolution and relationship graph with evidence and human review.
5. Implement authenticated browser session/import only after governed session, user intervention, and security checks.
6. Reconcile this checkpoint with local `C:\AndreOS-Memory` on the PC when remote desktop operations are available. Do not claim local clone sync until confirmed.


## Evolutive office and no-repeat rule — 2026-10-10

The user explicitly confirmed that DGM-MAT is both an office with multiple specialized delegations and an evolutionary system. Once an authorized source/conversation has been completely imported, documented, and validated, the system must move forward rather than re-read the entire old history on every cycle.

The feature branch now adds:
- SQLite/WAL progress ledger at `core/conversation_intelligence/progress_store.py`.
- Optional pipeline integration: `ConversationIntelligencePipeline(progress_store_path=...)`.
- Stable content fingerprints, completed-item skip behavior, source checkpoints and honest statuses.
- Reprocess only if content changes or work is incomplete/failed; a pending review task should be tracked separately from raw history ingestion.
- A database is only created when an explicit local path is supplied; do not store raw history in Git or expose it to the phone.
- The progress ledger now stores derived audit snapshots (code artifacts, findings, project suggestion and provenance), but not the full transcript. Cached audit results are returned on repeat imports, so downstream summaries/consolidation can reuse old work without rereading the source export.
- `load_saved_audits()`, `summarize()` and `consolidate()` can read the persisted derived index; source errors are recorded as `failed` with checkpoint/counts rather than silently remaining `partial`.

Current implementation link: https://github.com/AndreVazao/DGM-MAT/blob/feat/conversation-turn-semantics-v1/core/conversation_intelligence/progress_store.py
Tests added: https://github.com/AndreVazao/DGM-MAT/blob/feat/conversation-turn-semantics-v1/tests/conversation_intelligence/test_progress_store.py

Verification update (2026-10-10): `tests/conversation_intelligence` passed locally (17 tests). The broader regression run across conversation intelligence, contracts, organization, autonomy, security and cockpit also completed with exit code 0. It exposed an existing injected-clock bug in `HumanInterventionQueue.create_request`; the feature branch now uses the supplied creation timestamp for the initial read, and the regression suite passes. GitHub returned no PR-triggered workflow runs for the checked commit, so local tests are verified but CI is absent. The branch remains a draft PR; do not merge or call it production-ready until review/compatibility is complete. Local clone synchronization of this memory repository is still unconfirmed.

## Durable knowledge and review ledger — implementation update

A nova `core/conversation_intelligence/knowledge_store.py` persiste intenções do utilizador, propostas de IA, decisões do utilizador, relações entre conversas e tarefas de revisão numa base SQLite/WAL separada.

- Propostas de IA não são decisões do utilizador e não são aceites automaticamente. Depois de uma aceitação/rejeição explícita, o texto da proposta e a decisão não podem ser alterados silenciosamente.
- Intenções e decisões começam por `unverified`; intenções revistas e decisões confirmadas pelo utilizador não podem ser silenciosamente substituídas por registos não revistos.
- Relações preservam evidência, confiança e estado de revisão; auto-relações e confiança fora do intervalo são rejeitadas.
- Tarefas de revisão têm ciclo de vida próprio e podem ser resolvidas sem reler/importar novamente a conversa de origem.
- O store guarda enunciados e referências de evidência, não uma segunda cópia integral dos transcripts.
- A camada de persistência não prova que a extração automática de intenções, importação autenticada ou UI de revisão estejam concluídas.

Verificação final após a proteção de propostas aceites: a suite focada `tests/conversation_intelligence` passou (24 testes), e a regressão combinada de `conversation_intelligence`, `contracts`, `organization`, `autonomy`, `security` e `cockpit` terminou com exit code 0. GitHub não devolveu workflows PR-triggered para o head verificado; testes locais confirmados, CI ausente. A PR continua em draft até revisão/compatibilidade final.


## Correção de estado e validação — 2026-10-10

Esta secção substitui qualquer formulação anterior que desse como implementadas funcionalidades ainda não verificadas.

**Implementado e validado localmente no checkout Windows** (feature branch `feat/conversation-turn-semantics-v1`, commit sincronizado `dc8c2e3b79a699a78f743942066909d235d8e3c0`, com atualização documental posterior):
- Ledger SQLite/WAL de progresso por conversa e fonte, fingerprints e checkpoints.
- Reutilização de snapshots de auditoria, sem reauditar conteúdo inalterado quando existe snapshot reutilizável; os resultados em cache continuam disponíveis para sumários e consolidação.
- Reprocessamento único de registos antigos que só guardavam contadores e não tinham snapshot reutilizável.
- Store de conhecimento com estado atual e histórico append-only para intents, propostas de IA, decisões e relações; transições de estados confirmados exigem transição explícita.
- Testes locais: `python -m pytest tests/conversation_intelligence -q` terminou com exit code 0; suite combinada `tests/conversation_intelligence tests/contracts tests/organization tests/autonomy tests/security tests/cockpit` terminou com exit code 0; `compileall` e `git diff --check` também terminaram com exit code 0.
- O terminal remoto não apresentou a linha final com o número total exato da suite combinada. Houve avisos de depreciação FastAPI/Starlette/httpx, sem falhas reportadas.
- Não foi confirmado qualquer workflow PR-triggered do GitHub para o commit verificado; CI permanece por confirmar.

**Ainda NÃO implementado/não provado:** ciclo de vida separado de tarefas de revisão (review-task queue), validação de confiança/auto-relações conforme descrito em apontamentos anteriores, extração semântica automática de intenções, importação autenticada de históricos, controlo de sessões dos providers, operações de renomear/agrupar conversas nas plataformas, UI de revisão, integração completa com delegações/cockpit e validação em produção. Não tratar esses itens como concluídos.

**Regra de segurança:** manter a PR em draft e não fazer merge até revisão de compatibilidade e inspeção do diff. A validação local confirma os testes executados no checkout, não a ativação no Core em produção. Não reiniciar o Core live sem resolver a barreira operacional anterior (3 missões RUNNING e 2 QUEUED no último estado observado).


## Checkpoint final — histórico temporal e regressão, 2026-10-10

Correção da avaliação anterior: o código existente inclui tarefas de revisão separadas da importação de conversas. Foi agora acrescentada a tabela `knowledge_history` para snapshots append-only de alterações futuras em intents, propostas, decisões, relações e transições das tarefas de revisão. Escritas idênticas são idempotentes; o histórico novo não consegue reconstruir alterações anteriores à criação da tabela.

Estado confirmado no checkout Windows:
- Código/testes sincronizados até `506c6349a8e82745b85fa51197133e2255952f60`.
- Suite focada `tests\conversation_intelligence`: 27 testes indicados pelo progresso do pytest, exit code 0.
- Suite combinada `tests\conversation_intelligence tests\contracts tests\organization tests\autonomy tests\security tests\cockpit`: exit code 0 depois das últimas alterações.
- `python -m compileall -q core\conversation_intelligence` e `git diff --check`: exit code 0.
- Avisos apenas de depreciação FastAPI/Starlette/httpx; não foram reportadas falhas.
- Sem workflow PR-triggered confirmado para o commit verificado; CI continua por confirmar.
- PR permanece em draft; não foi feito merge nem reiniciado o Core em produção.

Continuam por fazer: revisão final do diff/compatibilidade, ligação da camada de conhecimento ao motor de delegações/cockpit, importação autenticada de históricos e verificação end-to-end. A validação local não significa que estas funções estejam ativas em produção.


## Delegation context API — validação após integração local, 2026-10-10

Foi acrescentado `ConversationIntelligencePipeline.build_delegation_context(provider=None)`: uma chamada reúne o sumário do arquivo histórico, conversas/artifacts em cache com proveniência, intents/propostas/decisões/relações e tarefas de revisão abertas. Usa as bases SQLite locais e não reabre os exports originais. As bases só são criadas quando os respetivos caminhos são configurados explicitamente.

Após esta alteração:
- Suite focada `tests\conversation_intelligence`: exit code 0 (28 marcadores de progresso do pytest).
- Suite combinada `tests\conversation_intelligence tests\contracts tests\organization tests\autonomy tests\security tests\cockpit`: exit code 0.
- `compileall` e `git diff --check`: exit code 0.
- Avisos de depreciação FastAPI/Starlette/httpx, sem falhas reportadas.
- A API de contexto ainda não está ligada ao Core/cockpit live nem exposta pela API HTTP; não houve restart de produção nem importação de contas externas.
