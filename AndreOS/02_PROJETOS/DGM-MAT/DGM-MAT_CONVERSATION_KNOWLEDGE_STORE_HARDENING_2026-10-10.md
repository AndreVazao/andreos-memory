# DGM-MAT — Incremental Conversation Memory Hardening Checkpoint
Date: 2026-10-10

## Current state
- PR #71 remains open and unmerged on `feat/conversation-turn-semantics-v1`.
- Latest synchronized DGM-MAT local/remote commit: `9987ece2328c39bf8ae496e4e429f141a3008f0c`.
- Remote GitHub Actions and combined status queries returned no workflow runs/status checks for the latest checked commit; CI remains unverified.
- No live Core restart, mission mutation or network exposure change occurred.

## Source-cache recovery
- SQLite `source_conversations` index stores ordered source-to-conversation membership and a SHA-256 source fingerprint.
- Unchanged complete exports can return valid cached audit snapshots without reparsing/re-auditing; source bytes are still read to compute SHA-256.
- Changed sources, missing/legacy membership, invalid snapshots and interrupted imports fall back to processing and repair the index before the source is marked complete.
- Regressions cover unchanged-cache reuse, missing index repair, interrupted import retry without reauditing completed items, and changed-source invalidation.

## Reviewed knowledge provenance
- Accepted/rejected AI proposals protect their decision state and provenance.
- Reviewed intents, user-confirmed decisions and reviewed relations now reject any non-identical rewrite, including source message IDs, evidence and confidence. Exact repeats remain idempotent.
- Regression `test_reviewed_knowledge_provenance_and_evidence_cannot_be_silently_rewritten` confirms attempted provenance/evidence substitutions are rejected and original records remain unchanged.

## Validation
- Focused knowledge-store and progress-store tests passed: 26 cases.
- Broader selected regression suite passed with exit code 0: conversation intelligence, contracts, organization, autonomy, security and cockpit.
- `git diff --check` passed.
- Remaining warnings: Starlette TestClient/httpx integration deprecation and FastAPI `on_event` deprecation.

## Synchronization status
- DGM-MAT feature branch: local branch and GitHub match exactly at `9987ece2328c39bf8ae496e4e429f141a3008f0c`; local worktree clean.
- This checkpoint file's content hash matches GitHub main: `e7abcedfd9fa44b6323e668910a4a1e1faf7a7fa`.
- AndreOS memory Git history/refs are not synchronized: local branch remains four commits ahead of cached `origin/main`; `git fetch` fails because Windows Git Credential Manager cannot persist credentials and cannot prompt. Do not reset, force-push or claim full Git synchronization until authentication is repaired safely.

## Core safety gate
- Last known `127.0.0.1:8181/health` returned HTTP 200.
- Unauthenticated runtime status/missions/queue endpoints returned HTTP 401, so active missions could not be verified.
- Do not restart Core or mutate missions until active work is verifiable through an authorized read path or controlled maintenance is explicitly approved.

## Next safe actions
1. Resolve AndreOS memory Git authentication safely.
2. Continue focused transition/provenance tests only when a concrete gap is demonstrated.
3. Keep PR #71 open until remote checks/reviews are explicitly available.


## 2026-10-10 — Source-cache collision guard
- Fixed a correctness gap where two different export files could contain the same provider conversation ID. The global progress row could then belong to the other export, and the first source's cache could have returned a mismatched audit.
- The source-membership index now stores a per-conversation fingerprint. The source-level fast path verifies that the global snapshot's fingerprint matches the indexed source member; missing/legacy fingerprints force a safe parse and index repair.
- Added regression `test_source_cache_rejects_global_snapshot_from_another_export_with_same_conversation_id`.
- Focused progress-store and knowledge-store suites passed, including migration of the existing SQLite membership schema and validation of fingerprint-list lengths. The full selected regression suite passed with exit code 0 (conversation intelligence, contracts, organization, autonomy, security, cockpit); `git diff --check` also passed.
- DGM-MAT PR #71 remains open. No merge or Core restart.


## 2026-10-10 ? Explicit decision supersession
- New local implementation: `ConversationKnowledgeStore.supersede_confirmed_decision`. Ordinary saves still cannot rewrite a user-confirmed decision. A separate explicit transition now allows a confirmed successor to supersede an earlier confirmed decision only when both records exist and non-empty evidence is supplied.
- The prior decision's statement, original source conversation/message, evidence and confirmation flag remain intact; only status becomes `superseded`, with an append-only history event linking the successor and evidence. Same-transition repeats are idempotent; conflicting successors are rejected.
- Added two regression tests for provenance preservation, idempotency, confirmed-successor validation and evidence requirements. Full selected regression suite passed locally with exit code 0; `git diff --check` passed.
- Local commit: `5e49b5a` (`feat: explicitly supersede confirmed conversation decisions`). Standard `git push` failed because Windows Git Credential Manager could not persist credentials or prompt. Exact implementation and test contents were then published sequentially through the GitHub contents API (remote code commit `67ec33c`, test commit `017c5e8`). DGM-MAT local feature branch and GitHub are now synchronized at `9987ece2328c39bf8ae496e4e429f141a3008f0c`, with a clean local worktree. The AndreOS memory file content has been copied from GitHub and its local Git blob matches remote blob `49d849138a677c34e56fcc9451992e74d8213ef3`, but the memory repository history/refs remain divergent: local `main` is four commits ahead of cached `origin/main`, and anonymous fetch is unavailable for this repository. Do not reset, force-push or claim full memory Git synchronization until authenticated fetch/reconciliation is safely available.
- Core not restarted; PR #71 remains open and unmerged. Remote CI for the new commits has not yet been verified.

[executed on device: PC-Vazao-Anjos (982eb058-a42c-4897-9732-547f04cb44f0)]

[executed on device: PC-Vazao-Anjos (982eb058-a42c-4897-9732-547f04cb44f0)]

Note: you've used 90% of this month's Desktop Commander usage. Visit https://mcp.desktopcommander.app/ to learn more about usage and resets.

## 2026-10-10 ? Local-first safety and full-suite verification
- Added local-only changes in DGM-MAT: test suite storage isolation via `tests/conftest.py`; provider execution endpoints now delegate to their own API/operator bearer-token validation instead of requiring an incompatible second local-session token; integration tests now authenticate correctly; storage-default test explicitly tests the real default while restoring temporary environment overrides.
- Full `python -m pytest -q --disable-warnings` passed locally with exit code 0, using disposable temporary storage. `git diff --check` passed. No GitHub push, PR update or Actions workflow was triggered. Changes remain on the PC only pending a workflow-safe sync plan.
- Safety incident: the first full-suite attempt accidentally wrote test actions into the live queue because the test process used the persistent DB. The run was stopped immediately; exact queued test rows 1035 (`contract boundary`) and 1036 (`result boundary`) were rejected through the audited queue API. Completed action 1034 was retained. No bulk cleanup or Core restart. Root test isolation now prevents recurrence.
- Read-only runtime diagnosis: `/health` returns 200, but authenticated runtime status reports `starting`; 495 mission records (491 FAILED, 3 RUNNING, 1 QUEUED); queue health `worker_alive=false`, no heartbeat. Do not automatically retry or delete these records. Diagnose worker/bootstrap and stale mission recovery first.
- Claude Code 2.1.112 is installed but `claude auth status` says `loggedIn=false`; Ollama is not running/reachable. No inference capability should be claimed until verified.
- Next priorities: bootstrap/worker recovery without mission replay; secure PC-local cockpit pairing; deterministic offline work mode for repository inventory, memory retrieval, static checks and tests; continue local-only testing and do not trigger Actions while minutes are constrained.

## 2026-10-10 ? Full-runtime launcher and stale mission recovery
- Confirmed the installed startup shortcut intentionally launched only Uvicorn/API, not `main.py`; therefore `/health` was healthy while runtime status stayed `starting` and the queue worker was dead.
- Local-only service manager now supports `--mode api|full`; full mode launches `main.py --headless`, verifies authenticated `runtime_status=running` plus `worker_alive=true`, refuses to duplicate an API process, and cleans up a child if startup readiness fails. Installer is prepared to select full mode, but the actual Startup shortcut/live process have not yet been switched pending safe mission-state reconciliation.
- Full-runtime service-manager smoke test passed on isolated loopback port 8182 using disposable storage; status confirmed runtime running and queue worker alive, then the isolated service was stopped.
- Added conservative stale mission reconciliation before the queue worker starts: unapproved stale actions return to QUEUED; explicitly approved actions remain eligible; other stale/inconsistent RUNNING missions are marked FAILED with preserved metadata and a no-replay recovery marker. No auto-approval or automatic replay.
- Focused service/auth/recovery tests passed. Full suite was run locally using the test-storage isolation fixture; no GitHub Actions workflow triggered.
- Read-only production queue audit: 1,038 actions (1 APPROVED, 107 COMPLETED, 70 FAILED, 787 QUEUED, 73 REJECTED). Sole APPROVED row is test action 1037, approved by `test_user`; left untouched. Unapproved rows were not bulk changed.

## 2026-10-10 ? Full runtime active; core agent visibility fix
- Live local service on 127.0.0.1:8181 was safely changed from API-only Uvicorn to `backend_service.py start --mode full`. Verified authenticated runtime status `running`, `is_degraded=false`, and durable queue worker alive with heartbeat. Startup shortcut now starts full mode at next Windows login. No GitHub push or Actions workflow triggered.
- Startup recovery reconciled the three stale RUNNING test missions: two with unapproved durable actions returned to QUEUED; one inconsistent/completed-action mission marked FAILED with no-replay provenance. No mission was auto-approved or replayed. The queue retains 787 unapproved QUEUED actions; no bulk cleanup. The only approved row (test action 1037) had no registered handler and was safely marked FAILED by the queue worker.
- Runtime snapshot showed no registered agents even though repo/provider/autonomy agents were constructed. Added explicit `AGENT_STATUS_CHANGED` records with truthful `initialized` status and implementation metadata, plus regression assertions. Full suite rerun follows this change.

## 2026-10-10 ? Runtime startup fixed and full suite verified
- Federation/rendezvous is opt-in through DGM_FEDERATION_ENABLED=1; local-first startup no longer waits on outbound rendezvous.
- Mission restoration now publishes one consolidated state snapshot instead of one event per mission. Regression tests verify the batch behavior.
- Full local pytest suite passed after the latest changes with isolated storage; git diff --check passed. No GitHub Actions or remote push was performed.
- Live runtime is running on loopback 127.0.0.1:8181, non-degraded, with queue worker alive and three core agents visible as initialized. Startup shortcut now selects full mode.
- Low-memory profile is active at 2.96 GB RAM. Claude Code remains logged out and Ollama was not running/reachable. Enabling verified local inference is next.
- Queue remains approval-gated; no bulk execution or deletion.
\n

## 2026-10-10 ? Local Ollama integration and memory guard
- Added a trusted Ollama provider adapter registered first; loopback-only endpoint, installed-model discovery, JSON-mode generation and explicit local_zero_token cost profile. No remote fallback.
- Mission decomposition can request and validate 3?5 proposed subtasks from the local model. Subtasks are only proposals; no automatic execution. Deterministic fallback remains on provider errors, invalid JSON or low memory.
- Hidden Ollama service is running on 127.0.0.1:11434, startup shortcut uses a hidden local service helper, and four installed models are detected.
- Actual inference using llama3.2:1b exceeded 90 seconds and drove free RAM to 0.02 GB. Stopped the model and recovered free RAM to ~0.93 GB. Added a 1.25 GB free-memory guard and keep_alive=0 to prevent PC starvation. Inference is not yet verified as practically usable on this machine.
- Full local pytest suite passed after provider/planner changes, using isolated storage. No GitHub push or Actions workflow was triggered.

## 2026-10-10 ? Provider health persisted as runtime truth
- ProviderBase.broadcast_health now persists the observation through the runtime state store (PROVIDER_UPDATED) as well as the websocket. Includes observation timestamps, installed/loaded, health/availability, freshness and source.
- Bootstrap publishes local Ollama health through the same path, so the cockpit truth can see it after a safe Core restart.
- Added regression test for provider health persistence. Full local pytest suite passed after these changes (exit code 0, 56.82s); git diff --check passed. No Actions workflow was run.
- Did not restart Core because the authenticated safety gate for active missions/approved actions could not be reliably completed. The changes remain local and tested; live runtime adoption is pending a verified safe restart.
- No GitHub push or PR merge.



## 2026-10-10 — Redução de logs repetitivos no ciclo principal
- Removida de `main.py` a chamada `TRACE_LOOP_START:main.py` de dentro do ciclo keep-alive executado a cada segundo. O ciclo mantém o `sleep(1)` e os registos de arranque/ownership.
- Evidência: `.runtime/runtime_activation.log` tinha 52 612 linhas (~1,37 MB), com repetição do marcador no final.
- Validação local: `python -m py_compile main.py` e `git diff --check` passaram. Não foi executada a suite completa para esta alteração de uma linha dedicada apenas a logging.
- O processo ativo já carregou a versão anterior; a correção só entra em vigor após reinício seguro. Não reiniciar enquanto o estado da fila durável/ações aprovadas não estiver confirmado.
- Histórico de logs preservado; nenhuma missão ou ação alterada. Sem push, merge ou GitHub Actions. A memória local ainda precisa de sincronização Git segura, sem force push/reset devido à divergência de histórico já conhecida.


## 2026-10-10 — Core restart verified; provider truth reconciliation

- Authenticated read-only preflight: Core healthy; 555 durable mission JSON checkpoints; three QUEUED missions mapped to unapproved durable actions 1023, 1033 and 1032. Full SQLite action counts were 787 QUEUED, 107 COMPLETED, 71 FAILED, 73 REJECTED; zero APPROVED/RUNNING. No mission/action rows were changed.
- Restarted headless Core hidden (PID 6256). Runtime reports running, non-degraded, low-memory; health endpoint healthy.
- Confirmed TRACE_LOOP_START:main.py spam is gone live: runtime_activation.log size stayed at 1,398,972 bytes during an 8-second observation; startup markers remain. No history truncation.
- New bug: bootstrap persisted Ollama health via PROVIDER_UPDATED, but RealitySnapshotService lazy/low-memory branch emitted deferred/unobserved, then PROVIDERS_RECONCILED replaced the concrete observation. Local fix reuses a previous concrete provider observation in lazy mode without starting another health probe; when no observation exists, it still reports deferred. Regression added: test_lazy_provider_health_preserves_existing_observation_without_new_probe.
- Focused tests tests/runtime/test_reality_snapshot.py, tests/providers/test_ollama_adapter.py, tests/unit/test_provider_api_truth.py passed locally (exit code 0). The latest provider fix is source-only and has not yet been loaded by the live Core.
- Historical mission count: 555 checkpoints, 552 FAILED and 3 QUEUED; sampled failures include timeout errors. Preserve history; no bulk replay/approval/deletion.
- No GitHub push, PR merge, Actions run or queue mutation. AndreOS-Memory file updated locally only; do not claim GitHub synchronization while its local Git refs/history remain divergent.

## 2026-10-10 — Live provider-truth verification
- Committed fix e55eceb; restarted headless Core hidden as PID 2000 after confirming 555 mission checkpoint files and zero durable APPROVED/RUNNING actions. No mission or queue rows were changed.
- Live runtime is running, non-degraded, LOW_MEMORY. Ollama now reports status=ok, available=true, availability_observed=true, freshness=fresh. The lazy-health reconciliation bug is fixed in the running process.
- Missions remain 555 total: 552 historical FAILED and 3 QUEUED. Durable actions: 787 QUEUED, 107 COMPLETED, 71 FAILED, 73 REJECTED; zero APPROVED/RUNNING.
- runtime_activation.log stayed at 1,399,173 bytes across an 8-second check; /health stayed healthy.
- Remaining data-quality issue: Ollama is reported installed=false, loaded=true because the source scanner does not recognize core/providers/local/ollama_adapter.py. Add scanner coverage and a regression test before claiming this field is correct.
- Focused runtime/provider/API tests passed locally; no GitHub push, PR merge or Actions run. This memory update is local-only while AndreOS-Memory Git history remains divergent.

## 2026-10-10 — Provider inventory + mission timeout root cause
- Fixed local provider inventory to detect adapter modules like core/providers/local/ollama_adapter.py while preserving legacy provider package detection; test covers both.
- Read-only audit of all 555 durable mission checkpoints: 552 FAILED, 3 QUEUED; 481 FAILED checkpoints had error “Mission timed out before execution completed.” Sampled timeout records had no execution_started_at; some logs showed only QUEUED or approved-but-not-started work.
- Root cause confirmed in MissionEngine.process_missions(): a generic 60-second guard ran on QUEUED and APPROVAL_PENDING as well as RUNNING, so waiting for a queue worker/operator could incorrectly mark a mission FAILED based on creation time. Changed the guard to apply only to RUNNING. Waiting states retain their status until governed execution/approval transitions them.
- Added regression coverage for old QUEUED and APPROVAL_PENDING missions. Focused runtime/provider/API/mission recovery suite passed: 21 tests, exit code 0; py_compile and git diff --check passed.
- Source/test/docs/memory edits are local-only at this checkpoint; live Core has not yet loaded this timeout fix. No mission/action rows changed; no auto-retry/approval/deletion, GitHub push, or Actions run.

## 2026-10-10 ? Approved execution clock coverage
- Further inspection found non-repository approved missions did not persist execution_started_at before decomposition; after a long approval wait they could still time out against created_at.
- Queue handler now calls _mark_execution_started for every explicitly approved mission before dispatching the selected handler. Added regression for an old queued non-repository mission.
- Focused recovery/mission/provider/runtime/API-truth tests passed (24 tests, exit code 0). This follow-up fix still needs safe live restart; no durable mission/action records were changed.

## 2026-10-10 ? Live adoption verified
- Safely restarted full runtime hidden as PID 3480 after verifying 555 mission checkpoints, no RUNNING mission checkpoints and zero APPROVED/RUNNING durable actions. No mission/action rows changed.
- Runtime healthy, non-degraded, three initialized agents, queue worker alive. Ollama reports installed=true, loaded=true, healthy=true, available=true, status=ok, freshness=fresh.
- Post-restart mission/action counts unchanged (555 missions: 552 FAILED, 3 QUEUED; actions 787 QUEUED, 107 COMPLETED, 71 FAILED, 73 REJECTED; zero APPROVED/RUNNING). runtime_activation.log stable at 1,399,575 bytes over 8 seconds.
- Latest local commits: 37a238c waiting-state timeout fix; 084c0c9 execution clock starts on every approved mission path. No push, PR merge or Actions run.


## 2026-10-10 — Overnight read-only monitoring
- Started hidden process PID 5504 from AndreOS-Memory to sample every 15 minutes until 08:00 local (2026-10-11). Logs health, RAM/CPU, runtime process RSS/CPU, mission checkpoint statuses, SQLite queue counts read-only, and trace size. No queue/mission/service/power mutation.
- First sample: healthy; 928 MB RAM available of 3033 MB; system CPU 57.7% (single sample); runtime RSS 25.9 MB; 555 checkpoints; durable action counts unchanged; trace 1,399,575 bytes.
- Claude Code CLI 2.1.112 exists but was not logged in. Read-only plan invocation failed at authentication; no credentials were accessed or changed. See DGM-MAT_OVERNIGHT_RECOVERY_AUDIT_PRELIMINARY_2026-10-10.md for details and morning follow-up.


## 2026-10-11 — Resultados intermédios do monitor noturno DGM-MAT
- Às 05:49 local, consolidadas 31 amostras entre 22:08:13 e 05:38:32: health 31/31 saudável (HTTP 200), zero erros; monitor PID 5504 e runtime PID 3480 presentes; endpoint `/health` confirmado saudável diretamente.
- RAM total 3033 MB; disponível mínimo 928 MB, máximo 1235 MB, média das amostras 1153,6 MB, última 1112 MB. CPU pontual 0–57,7%, média das amostras 5,9% (não é utilização contínua). RSS runtime 25,5–26,0 MB; PID estável.
- `runtime_activation.log` permaneceu em 1.399.575 bytes em todas as amostras. Missões estáveis em 555 (552 FAILED, 3 QUEUED); ações duráveis estáveis em 107 COMPLETED, 71 FAILED, 787 QUEUED, 73 REJECTED.
- Monitor continua até às 08:00; resultados são intermédios, não a noite completa. Nenhuma mutação, repetição de missão, reinício, push ou Actions.
- Próximo passo após 08:00: recolher últimas amostras e fechar relatório; em seguida classificar falhas com base em evidência e testar recuperação idempotente em ambiente temporário antes de considerar missões reais.
