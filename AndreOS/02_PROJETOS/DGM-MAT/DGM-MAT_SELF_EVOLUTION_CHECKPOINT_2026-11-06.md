# DGM-MAT — Self-Evolution Implementation Checkpoint

Date: 2026-11-06
Project repository: AndreVazao/DGM-MAT
North-star specification: Issue #245
Related foundations: Issues #242 and #244

## Operator decision

DGM-MAT is to evolve into an internally capable software engineering organization. Its long-term normal engineering lifecycle must work without depending on Codex or Claude Code. Codex and Claude remain optional external consultants, independent reviewers and fallback specialists; they are not the permanent core.

The internal organization is expected to develop specialist engineering capabilities based on actual repository languages and ecosystems, plus independent teams for architecture/review, bug investigation, testing, research, security, release and recovery. It must create and improve its own modules, agents and tools, propose changes to its own GitHub repository, and support controlled self-updates.

Self-improvement is governed engineering, not unrestricted self-modification. Changes must be isolated, versioned, tested, independently reviewed, evidence-backed and reversible. Protected merges, releases, migrations, destructive actions, permission changes and other high-impact operations remain subject to explicit operator approval.

## Repository findings before implementation

The default-branch source inventory found an existing organizational foundation. It must be reused rather than duplicated:

- core/organization/models.py — AgentProfile, Department, Task, Message, Evidence and EvolutionProposal.
- core/organization/registry.py — in-memory AgentRegistry.
- core/organization/bootstrap.py and office.py — initial and expanded role/department rosters.
- core/organization/delegation.py — deterministic skill/permission/department/dependency matching; assignment only, not execution.
- core/organization/task_manager.py — in-memory task lifecycle and dependency checks.
- core/organization/message_bus.py and worker_runtime.py — durable SQLite message transport and explicitly registered local Python handler dispatch.
- core/organization/qa_review_queue.py and qa_review_coordinator.py — persisted QA intake/review workflow and fixed local checks.
- core/organization/capability_models.py, capability_registry.py, capability_scout.py, recruitment.py and skill_forge.py — capability discovery/acquisition and recruitment primitives.
- core/development/language_catalog.py — deterministic language/format catalogue; planning metadata only, no toolchain detection or code execution.
- core/execution/worktree_manager.py and execution-related contracts — isolated workspace primitives, not yet a complete MissionEngine coding lifecycle.

Important limitations confirmed from source/documentation:
- A role in a roster is not proof of an active AI worker.
- Delegation and message dispatch are not a generic code-writing pipeline.
- The organization registry and task manager are in-memory; they are not the durable mission/task authority.
- WorkerRuntime invokes only explicitly registered local Python handlers; it does not interpret message text as code.
- The language catalogue does not prove compiler/runtime availability.
- Legacy DevelopmentEngine/ImplementationEngine/ExecutionFabric paths must not be treated as real code execution; the readiness audit documents no-op or unsafe placeholder behavior.
- A queued QA request is not proof that independent review or tests occurred.
- No PC-local or Windows acceptance was performed in this GitHub-only checkpoint.

## First implementation increment

DGM-MAT PR #246:
https://github.com/AndreVazao/DGM-MAT/pull/246

Branch: feat/internal-engineering-team-planner-v1

Adds:
- core/organization/engineering_team_planner.py
- tests/organization/test_engineering_team_planner.py
- docs/architecture/ENGINEERING_TEAM_PLANNER_V1_2026-11-06.md
- public exports from core/organization/__init__.py

The planner reuses the canonical language catalogue and Task model. It groups changed paths by language and creates a deterministic proposed task graph:
- optional research;
- one implementation proposal per detected language;
- cross-language integration review;
- independent bug-hunt;
- independent QA;
- security review for high/critical risk.

It rejects unsafe paths, unknown extensions and ambiguous C/C++ headers from implementation assignment. Task IDs use stable SHA-256 derivation.

Hard safety invariants on every generated task:
- planning_only=true;
- execution_authorized=false;
- toolchain_status=not_probed;
- no worker assignment;
- no code execution, patch application, provider call or verification claim.

Implementation tasks declare sandbox-write permission requirements and require a later approval bound to the exact proposed diff. The planner is intentionally not wired into MissionEngine or an executor yet.

PR #246 latest head 4a58737b79b0e64fa20a0c8b91535eceb11cf935 passed Focused PR Validation run 42302213926: repository Python compilation and all 17 selected planner tests passed. The first run on the earlier head also passed. The PR is now ready for independent review; it is not merged. PC/Windows acceptance is still pending.

## Next implementation gates

1. Verify PR #246 CI and review any failures without weakening tests.
2. Compare the task graph's required skills/permissions with the actual registered office roster. Report missing specialists/capabilities honestly; do not auto-assign a role-defined-only worker.
3. Build one deterministic, non-mutating internal worker adapter through the existing explicit WorkerRuntime registration boundary.
4. Persist task/run lifecycle using an existing durable authority; do not create a parallel mission database.
5. Prove restart recovery, idempotent dispatch and trusted evidence provenance.
6. Only then add one real language-specific patch worker, isolated by WorktreeManager and guarded by exact path/diff approval.
7. Require independent QA/bug-hunt evidence before a task can become verified or a PR can be marked ready.
8. Add self-improvement proposal generation and GitHub PR creation only after the internal implementation lifecycle is proven.
9. Add staged self-update, health verification and rollback as a later release-management phase.

## Permanent operating rules

- Stability and recoverability before fleet size or speed.
- Evidence before claims; AI consensus is not proof.
- Do not create one worker per language until repository inventory and workload justify it.
- Resource-aware execution must support slow sequential operation on constrained hardware and scale on stronger hardware.
- No paid APIs/subscriptions by default; local LLM inference is optional.
- Never collect credentials, cookies, MFA codes or raw tokens.
- Never bypass MFA, CAPTCHA, provider limits or free-tier restrictions.
- No unrestricted shell, uncontrolled agent spawning, recursive self-modification loops or unbounded retries.
- No self-merge to protected branches, history rewrite, destructive cleanup or risky deployment without approval.
- Keep the PC offline constraint until Monday 2026-11-09; do not claim local tests during this period.

## Status vocabulary

- Implemented in source: code exists on a branch.
- CI passed: only when the exact PR head has successful workflow evidence.
- Locally accepted: only after the real target PC has executed the relevant checks.
- Operational: only after an end-to-end task has run, been independently validated and recovered from interruption.

Memory review PR: https://github.com/AndreVazao/andreos-memory/pull/29

This checkpoint is a durable project memory record, not a claim that DGM-MAT is already self-evolving or independent of external coding agents.
