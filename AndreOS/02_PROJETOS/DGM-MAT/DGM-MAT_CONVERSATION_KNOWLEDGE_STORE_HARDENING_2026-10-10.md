# DGM-MAT — Conversation Knowledge Store Hardening Checkpoint
Date: 2026-10-10

- PR #71 remains open on `feat/conversation-turn-semantics-v1`; no merge.
- Local DGM-MAT branch pre-change HEAD was `5afe452ae78f26e3f0db43c7a6bc3085e9dc4f42`, matching `origin/feat/conversation-turn-semantics-v1` before this checkpoint's changes.
- Reviewed the incremental progress ledger and pipeline: snapshots are persisted and loaded back for unchanged conversations, cached artifacts remain available for consolidation, and legacy counter-only records are rebuilt once. Current ingest still parses the source export each invocation; source-level fingerprint short-circuiting and a source-to-conversation membership index remain future work.
- Fixed a concrete provenance gap in `ConversationKnowledgeStore.save_proposal`: after a proposal has explicit accepted/rejected state, changes to `source_message_id` or `decision_id` are now rejected alongside changes to its decision state, statement, or source conversation. Added regression test `test_accepted_proposal_preserves_message_and_decision_provenance`.
- Local focused suite passed: 29 tests across `test_knowledge_store.py`, `test_progress_store.py`, `test_evidence_aware_models.py`, and `test_pipeline.py`; exit code 0. `git diff --check` passed (one CRLF normalization warning only).
- Live Core: `/health` returned HTTP 200. Unauthenticated reads of `/runtime/status`, `/runtime/missions`, and `/runtime/queue` returned HTTP 401, so active missions were not verified. No restart or mission mutation occurred.
- GitHub integration returned no PR-triggered workflow runs or combined status checks for the pre-change SHA; this is not a passing CI result. The code, regression test, and checkpoint were subsequently published to the feature branch through the GitHub integration as commits `20b94be`, `632552b`, and `b6968f0`.
- Next: verify the latest PR head and CI, then continue the pipeline/source-level incremental review. Do not merge prematurely or restart the Core without verifying active missions.
