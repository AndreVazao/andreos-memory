# DGM-MAT Architecture Surgery — continuation — 2026-10-08

## Execution architecture

Reference tracing confirms the current high-level canonical path is:
`Mission/Autonomy -> SafeActionQueue -> Execution Fabric -> Worktree/SafePatch/Supervisor -> validation/reality -> memory`.

`core/execution_fabric` is the active autonomous orchestration layer. `core/runtime/safe_action_queue.py` is the durable governance/control boundary. `core/execution` remains lower-level Git/worktree infrastructure; `core/execution/execution_engine.py` currently has no production/test callers and is retained pending a separate deletion decision.

The old `core/development` subsystem was already quarantined and removed from Runtime in commit `aed57a3`.

## Reality-grounding cleanup

Reference tracing found no callers for two fake provider modules:
- `core/model_router/local_provider_adapter.py`
- `core/providers/ollama/ollama_provider.py`

They were removed from canonical DGM-MAT and archived in DGM-MAT-OS under `archive/DGM-MAT-fake-provider-adapters-2026-10-08`.

These modules were unsafe as architecture because they could report capability/health without observing reality: one always returned `True`; the other forced Ollama to `ok` and returned a placeholder chat response.

Canonical rule: provider availability and capability must be based on an actual observable check or an explicit unknown/unavailable state. Simulation must never masquerade as health.

## Regression finding

The previous canonical baseline had 183 passing tests. During this continuation, the suite exposed a separate EventStore contract failure in `tests/contracts/test_event_boundary.py`: `EventStore.replay(limit=20, event_type=...)` orders ascending and can omit the newly persisted event when the local SQLite store already contains more than 20 matching records. `EventStore.get()` still succeeds.

The product replay semantics were deliberately left chronological. The contract test was corrected to use a unique event type per test instance so it cannot depend on accumulated local SQLite state. The targeted EventStore tests pass and the full suite returned 100% green (183 tests).

## Historical creation-order audit

A new DGM-MAT report reconstructs component lineage from Git history rather than filesystem creation timestamps: reports/DGM-MAT_HISTORICAL_CREATION_ORDER_2026-10-08.md.

Key findings: the core architecture was created very rapidly on 2026-05-22/23/24; EventStore lineage starts at 4e7f8a4 and later receives the EventEnvelope boundary at 56019e4; ExecutionEngine originates in 8135a73 while ExecutionFabric originates later in a396bef; provider lineage begins in dbb0e69 and later receives orchestration/reality layers; MissionEngine is heavily evolved through Phase 41/42 stabilization commits.

New surgery rule: every future audit must use both structural reality (current callers, data flow and tests) and historical reality (first introduction, evolution, replacement, migration and rename lineage). Old does not mean canonical; late does not mean disposable.

## Synchronization

DGM-MAT documentation updated and pushed:
- `7c03d3e` — `refactor: remove ungrounded provider adapters`

DGM-MAT-OS contains the preserved historical modules.

Next: audit the unreferenced `core/execution/execution_engine.py`, followed by ProviderBase default-health semantics. Each step requires regression proof before removal/consolidation.
