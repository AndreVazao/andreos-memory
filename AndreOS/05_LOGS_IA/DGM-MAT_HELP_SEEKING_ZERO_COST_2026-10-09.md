# Path: C:\\AndreOS-Memory\\AndreOS\\05_LOGS_IA\\DGM-MAT_HELP_SEEKING_ZERO_COST_2026-10-09.md
# DGM-MAT — Help-seeking and zero-cost-by-default

Date: 2026-10-09

## User requirement
DGM-MAT must understand the task, recognize when it does not know or cannot proceed, know where and how to ask for help, and avoid spending money by default.

## Implementation started
- Added `core/organization/help_seeking.py`: deterministic HelpContext/HelpDecision/HelpAction and HelpSeekingPolicy.
- The policy prioritizes user decisions, bounded retry stop, available internal specialist, free/local options and only then blocks on a potentially paid-only path.
- `may_spend` fails closed unless explicit approval, exact cost known and within-approved-limit are all true.
- Help request builder includes goal, facts, unknowns, attempts, evidence, free options, paid option disclosure and specific ask.
- Added `tests/organization/test_help_seeking.py` with eight tests covering free-first routing, specialist routing, stop-after-retries, user decision, no-spend gate and evidence-rich requests.
- Added design doc `docs/architecture/HELP_SEEKING_ZERO_COST_POLICY.md`.
- Targeted tests passed: 8 passed. py_compile and git diff --check passed.

## Limitation
This is a new policy primitive and tests only. It is not yet connected to Mission Engine/provider execution, does not persist decisions, and is not a global spend-enforcement boundary. Do not claim the entire system is protected until integration and end-to-end tests prove it.

## Next steps
1. Review task lifecycle and provider call boundaries.
2. Back up and hash-verify any existing source before modification in DGM-MAT-OS.
3. Integrate help decision into mission exception/blocker handling and provider preflight without changing unrelated behavior.
4. Add end-to-end tests verifying paid providers are never invoked unless explicit approval, known cost and approved limit are all validated.
5. Run focused and full tests, inspect diffs, update canonical project memory/checkpoint and push only after validation.
