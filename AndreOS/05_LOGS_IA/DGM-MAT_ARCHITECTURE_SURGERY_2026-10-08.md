# DGM-MAT â€” Architecture Surgery Memory â€” 2026-10-08

## Canonical state

DGM-MAT canonical repository: C:/ProgramasGodMode/DGM-MAT.
Runtime: C:/DevopGodMode.
Persistent memory repository: C:/AndreOS-Memory.
Historical quarantine: C:/ProgramasGodMode/DGM-MAT-OS.
Immutable archaeology backup: C:/ProgramasGodMode/DGM-MAT-FULL-MIRROR â€” never modify.

Principles:
- stability > features
- reality > assumptions
- manual control > destructive automation
- discovered source is evidence, not executable authority
- preserve recoverable history when removing canonical residue
- human approval remains required for secrets, destructive actions, releases/publication and consequential ambiguity

## October surgery history

Removed/quarantined stale development subsystem:
- core/development/*
- archived in DGM-MAT-OS/archive/DGM-MAT-stale-development-subsystem-2026-10-08
- commit aed57a3

Removed dead validation placeholders:
- core/development/test_orchestrator.py
- core/execution_fabric/validation_pipeline.py
- archived in DGM-MAT-OS/archive/DGM-MAT-dead-placeholders-2026-10-08
- commit 1df132d

Removed fake/ungrounded provider adapters previously identified:
- core/model_router/local_provider_adapter.py
- core/providers/ollama/ollama_provider.py
- archived in DGM-MAT-OS/archive/DGM-MAT-fake-provider-adapters-2026-10-08
- commit 7c03d3e

Quarantined obsolete Phase 15-17 execution generation:
- execution_engine.py
- worktree_manager.py
- branch_manager.py
- repair_loop.py
- rollback_engine.py
- merge_guard.py
- execution_context.py
- execution_models.py
- archived in DGM-MAT-OS/archive/DGM-MAT-legacy-execution-engine-2026-10-08
- commit 8e3470a

Reason: no production callers; historical import/logic tests only; ExecutionEngine calls WorktreeManager with obsolete signature. GitUtils retained because it has real callers.

## EventStore correction

EventStore is historical from persistent engine/cockpit lineage (4e7f8a4), later adapted to EventEnvelope at 56019e4.

The failing replay contract test was caused by accumulated local SQLite records of the same event type. Replay is intentionally chronological. The test now uses a unique event type so it is isolated from historical local state.

Result: full suite green before provider quarantine.

## Historical archaeology

New report:
reports/DGM-MAT_HISTORICAL_CREATION_ORDER_2026-10-08.md

New complete Git first-add index:
reports/DGM-MAT_FILE_CREATION_INDEX_2026-10-08.md

Important discovery: a very large amount of DGM-MAT architecture was created in rapid succession on 2026-05-22/23/24. Future audits must compare current structural reality with historical lineage.

## Provider archaeology â€” major finding

The provider connector lineage begins at dbb0e69. Phase 42.2-LITE commit 55afee0 later introduced dynamic provider discovery/orchestration.

Current provider adapters were not trustworthy runtime implementations:
- ChatGPT chat returned placeholder output and browser authentication declared success without verifying a session.
- Claude, DeepSeek, Gemini, Grok and OpenAI returned placeholder output.
- several health checks treated credential/configuration presence as ok rather than performing an observed service check.
- Open WebUI was placeholder-only.
- provider mesh had no production callers and tests encoded placeholder/capability-score assumptions.
- local AI fabric contained a real Ollama HTTP adapter but no production callers; Open WebUI was placeholder-only.
- browser provider/recovery components had no canonical production callers.

Quarantined to:
DGM-MAT-OS/archive/DGM-MAT-unproven-provider-stack-2026-10-08

ProviderBase and provider registry contract remain canonical. No unproven provider is automatically considered available.

The tests that existed only to prove the fake provider stack were removed. Full regression suite remains green at 178 tests.

## Current execution truth

The assumed path Mission -> SafeActionQueue -> ExecutionFabric is not the current proven runtime path.

Actual proven path:
MissionEngine -> SafeActionQueue -> registered MISSION_EXECUTION handler in MissionEngine -> mission execution/decomposition logic.

ExecutionFabric itself is not yet deleted because WorktreeRuntime is still imported by core/sandbox/isolated_runtime.py. This requires a separate ownership audit.

## Next work

1. Audit Storage/Event/EventBus lineage.
2. Audit ExecutionFabric -> WorktreeRuntime -> sandbox ownership and actual callers.
3. Audit ProviderBase health semantics and provider registry now that unproven adapters are gone.
4. Audit runtime/bootstrap lineage.
5. Audit MissionEngine/SafeActionQueue/approval lineage.
6. Audit Conversation Intelligence and memory lineage.
7. Audit October 2026 contract consolidation.

Every removal must preserve recoverable history in DGM-MAT-OS and remain green under regression tests.

## ExecutionFabric / sandbox quarantine — 2026-10-08

Deep structural audit proved that `core/execution_fabric` is not a production runtime dependency of current DGM-MAT. The fabric is internally self-contained, has no current production callers, contains placeholder/no-op behavior, and has an inconsistent AutonomousExecutor -> WorktreeRuntime interface (`create_sandbox` / `cleanup_sandbox` versus `create_worktree` / `remove_worktree`).

`core/sandbox` likewise has no production callers. Its only code dependency was the orphaned WorktreeRuntime import from the execution fabric. The dedicated sandbox/worktree tests therefore represented historical behavior, not a live contract.

Canonical DGM-MAT quarantined the execution fabric, sandbox, and dedicated tests. DGM-MAT-OS preserves the exact tracked state under `archive/DGM-MAT-unproven-execution-sandbox-2026-10-08/`, including a Git recovery payload and provenance README. FULL-MIRROR was not touched.

Canonical commit: `4c00b3f` — refactor: quarantine unproven execution fabric and sandbox.
Archive commit: `d95a370` — archive: preserve unproven execution fabric and sandbox.
Regression suite after surgery: **178 passed, 0 failed**, warnings only. CPU/memory degradation warning appeared during the run, consistent with the old 3 GB workstation profile; no test failure resulted.

Next deep audit target: ProviderBase health semantics and provider registry contract, followed by Runtime/bootstrap, MissionEngine/SafeActionQueue/approval, Storage/Event/EventBus, and Conversation Intelligence/memory lineage.
