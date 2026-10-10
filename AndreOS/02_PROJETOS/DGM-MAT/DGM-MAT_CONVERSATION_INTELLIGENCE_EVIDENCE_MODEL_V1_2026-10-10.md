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
