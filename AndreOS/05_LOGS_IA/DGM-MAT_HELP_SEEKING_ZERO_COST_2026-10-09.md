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


## Follow-up — MissionEngine failure-path integration (2026-10-09)

- Before modifying the existing `core/autonomy/mission_engine.py`, created `C:\ProgramasGodMode\DGM-MAT-OS\archive\DGM-MAT-pre-help-seeking-integration-2026-10-09__core__autonomy__mission_engine.py.bak` and verified source/backup SHA-256 equality (`638502E409C5E59CD7734B28051D6AC0C8353E2AF7D26AC7F660ABEE518FF5A8`).
- Integrated `HelpSeekingPolicy` into `_finish_mission_failure`: failed missions now persist an advisory help recommendation with action, reason, next step, evidence-rich request and `spending_allowed=False` in mission metadata.
- This path does not dispatch messages, invoke providers, retry automatically or spend money. Mission remains honestly `FAILED`; the recommendation is explicitly `RECOMMENDATION_ONLY`.
- Added `tests/autonomy/test_mission_help_seeking.py`. Focused tests across help policy and mission lifecycle passed after correcting one test assertion; `py_compile` and `git diff --check` passed.
- Full suite was started after integration; record final outcome only after checking process completion. Changes have not yet been committed/pushed at the time of this entry.


## Final validation and publication preparation

- Full repository suite after MissionEngine integration: 100% passed, exit code 0 (runtime 56.72s). Existing deprecation warnings remain for Starlette/httpx TestClient and FastAPI `on_event`; no test failures.
- Focused batch: 11 tests passed across help-seeking policy and MissionEngine lifecycle/integration. `py_compile` and `git diff --check` passed.
- Policy design doc updated to describe the actual integration and its remaining global-enforcement limitation.
- The recommendation is persisted inside mission JSON metadata through the existing mission save path, but no live worker dispatch or provider spend enforcement is claimed.
- Ready for a targeted commit/push after checking final diffs and both repository states.
