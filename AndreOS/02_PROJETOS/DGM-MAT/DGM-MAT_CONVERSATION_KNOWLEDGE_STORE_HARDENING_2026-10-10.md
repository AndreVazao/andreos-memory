# DGM-MAT — Incremental Conversation Memory Hardening Checkpoint
Date: 2026-10-10

## Current state
- PR #71 remains open and unmerged on `feat/conversation-turn-semantics-v1`.
- Latest synchronized DGM-MAT local/remote commit: `a6ddbade1f2ec915e99d1902aa9005922043a577`.
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
- DGM-MAT feature branch: local branch and GitHub match exactly at `a6ddbade1f2ec915e99d1902aa9005922043a577`; local worktree clean.
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
- Local commit: `5e49b5a` (`feat: explicitly supersede confirmed conversation decisions`). Standard `git push` failed because Windows Git Credential Manager could not persist credentials or prompt. Exact implementation and test contents were then published sequentially through the GitHub contents API (remote code commit `67ec33c`, test commit `017c5e8`). The local feature branch and GitHub branch now have different commit histories and still require verified ref/content reconciliation; do not claim exact Git sync yet.
- Core not restarted; PR #71 remains open and unmerged. Remote CI for the new commits has not yet been verified.

[executed on device: PC-Vazao-Anjos (982eb058-a42c-4897-9732-547f04cb44f0)]