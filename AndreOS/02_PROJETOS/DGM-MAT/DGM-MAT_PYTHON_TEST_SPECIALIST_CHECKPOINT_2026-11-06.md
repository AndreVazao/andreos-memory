# DGM-MAT — Python test specialist checkpoint 2026-11-06

## Verified merged increments

- DGM-MAT #246 — deterministic engineering team planner; 22 focused tests passed.
- DGM-MAT #247 — bounded read-only Repository Cartographer; 23 focused tests passed.
- DGM-MAT #249 — safe additive roster reconciliation; 5 focused tests passed.
- DGM-MAT #250 — handler/capability-aware delegation; 9 focused tests passed.
- DGM-MAT #253 — clean mainline integration of the Python Source Analyst.
- DGM-MAT #254 — MissionEngine explicit registration of read-only repository specialists; Focused PR Validation run 42307675986 succeeded.
- DGM-MAT #255 — Python Test Inventory Worker; Focused PR Validation run 42307981234 succeeded and the PR was merged.

## Current read-only workforce

The operator-configured bootstrap now registers three specialists against one host-owned repository allowlist:

1. `agent:repository-cartographer`: metadata-only project tree and file inventory.
2. `agent:python-source-analyst`: bounded Python AST syntax/import/definition analysis.
3. `agent:python-test-inventory`: AST-only test suite structure inventory (test functions, async tests, test classes, fixture/parametrize decorators, pytest/unittest imports).

The allowlist is provided through `DGM_READ_ONLY_WORKSPACE_ROOT` and `DGM_READ_ONLY_REPOSITORIES`, a JSON mapping of stable repository IDs to relative paths. Missing/invalid configuration leaves the workers disabled. Message payloads cannot add paths.

## Safety and maturity

All three workers are read-only. They do not execute Python, import project modules, run tests, invoke shell commands, write source files, access networks or call external AI providers. The Python Test Inventory is not test execution, coverage measurement or test quality proof.

A registered handler is only a configured capability. A successful real-repository task, independent review and Windows restart/recovery tests are still required to establish task-level readiness.

## Operator PC acceptance

The PC remains offline until Monday 2026-11-09. No local configuration or installation is to be attempted before reconnect. First acceptance should use only the DGM-MAT repository in the allowlist, then run one Cartographer, one Python AST and one test-inventory request. Capture exact outputs and compare them with manual inspection.

## Next work

- Integrate worker task assignment with the existing AgentRegistry/DelegationEngine and durable message bus without creating a parallel task store.
- Add task-level evidence states (configured, handler-registered, smoke-tested, task-validated).
- Add an independent Python quality/review specialist after task dispatch is proven.
- Then introduce isolated patch proposals through existing WorktreeManager and approval infrastructure.
- Continue audits of browser-operator approval gates and Vault bootstrap before further structural changes.

No secrets, credentials, private conversations or Vault payloads are included.
