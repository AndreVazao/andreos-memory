# DGM-HUB QUICK AUDIT CHECKLIST
## Use This for Fast Architecture Verification

**Purpose:** Quick review checklist for DGM-HUB codebase changes  
**Time:** 15-30 minutes per review cycle  
**Audience:** Developers, code reviewers

---

## PART 1: SECURITY VERIFICATION (5 min)

### Shell Execution Safety
- [ ] **Check subprocess calls** in execution_engine.py, test_runner.py
  ```bash
  grep -r "shell=True" src/dgm_hub/
  ```
  **Expected:** 0 results (no shell=True)
  **If found:** 🔴 CRITICAL - report immediately

- [ ] **Check for shell command validation**
  ```bash
  grep -r "shell=False\|shlex.split" src/dgm_hub/
  ```
  **Expected:** Present and used consistently
  **If missing:** ⚠️ MEDIUM - could allow injection

### Path Access Control
- [ ] **PowerShell/Cmd tools use PathGuard**
  ```bash
  grep -A5 "class PowerShellTool\|class CmdTool" src/dgm_hub/tools/
  ```
  **Expected:** `self.guard = PathGuard(...)` in constructor
  **If missing:** 🔴 CRITICAL - unrestricted system access

- [ ] **FilesystemTool/GitTool guard enforcement**
  ```bash
  grep "is_allowed\|PathGuard" src/dgm_hub/tools/filesystem_tool.py src/dgm_hub/tools/git_tool.py
  ```
  **Expected:** Guard check before every file operation
  **If missing:** 🔴 CRITICAL - path escape possible

### Exception Safety
- [ ] **Rollback errors are logged (not swallowed)**
  ```bash
  grep -A3 "except.*pass" src/dgm_hub/control/task_executor.py
  ```
  **Expected:** 0 `except: pass` blocks
  **If found:** ⚠️ HIGH - exception info lost

---

## PART 2: CONFIGURATION VERIFICATION (3 min)

### allowed_paths Configuration
- [ ] **allowed_paths is NOT just "."**
  ```bash
  grep "allowed_paths" config/default_config.yaml
  ```
  **Expected:** Explicit paths, not wildcards
  ```yaml
  allowed_paths:
    - "C:\\ProgramasGodMode\\DGM-HUB\\src"
    - "C:\\ProgramasGodMode\\DGM-HUB\\tests"
  ```
  **If ".":** ⚠️ MEDIUM - allows current dir (may be broad)

### Mode and Platform
- [ ] **mode is "headless" (not interactive)**
  ```bash
  grep 'mode.*:' config/default_config.yaml
  ```
  **Expected:** `mode: "headless"`

- [ ] **platform is "windows"**
  ```bash
  grep 'platform.*:' config/default_config.yaml
  ```
  **Expected:** `platform: "windows"`

---

## PART 3: EXECUTION FLOW VERIFICATION (5 min)

### Snapshot Management
- [ ] **Snapshots created before execution**
  ```bash
  grep -n "create_snapshot" src/dgm_hub/control/task_executor.py
  ```
  **Expected:** Line ~50 (before tool execution)

- [ ] **Snapshot creation validated (not None)**
  ```bash
  grep -B2 -A2 "if not snapshot" src/dgm_hub/control/task_executor.py
  ```
  **Expected:** Validation present, raises on failure
  **If missing:** ⚠️ HIGH - could proceed without backup

- [ ] **Snapshot cleanup on old runs**
  ```bash
  ls -la runtime/snapshots/
  ```
  **Expected:** < 10 snapshots, recent modification dates
  **If 100+:** 🔴 CRITICAL - disk space issue

### Tool Execution
- [ ] **Tools dispatched via UnifiedToolManager**
  ```bash
  grep "UnifiedToolManager" src/dgm_hub/control/task_executor.py
  ```
  **Expected:** Present and used

- [ ] **Tool parameters validated before execution**
  ```bash
  grep "validate.*payload\|schema" src/dgm_hub/control/
  ```
  **Expected:** Payload validation layer present
  **If missing:** ⚠️ MEDIUM - no schema enforcement

### Test Execution
- [ ] **Test commands use safe execution (no shell=True)**
  ```bash
  grep -n "shell=True" src/dgm_hub/execution/test_pipeline.py
  ```
  **Expected:** 0 results
  **If found:** 🔴 CRITICAL - shell injection vector

---

## PART 4: DATA INTEGRITY VERIFICATION (5 min)

### Execution Journal
- [ ] **Journal file exists and has recent entries**
  ```bash
  ls -la runtime/journals/
  tail runtime/execution_journal.jsonl
  ```
  **Expected:** JSONL file with recent entries
  **If empty:** ⚠️ MEDIUM - execution tracking broken

- [ ] **Journal entries are valid JSON**
  ```bash
  python -m json.tool runtime/execution_journal.jsonl > /dev/null
  ```
  **Expected:** 0 errors
  **If parsing fails:** 🔴 CRITICAL - journal corrupted

### Rollback Verification
- [ ] **Test successful rollback after execution**
  ```python
  # Create test repo
  mkdir test_repo
  touch test_repo/test.txt
  
  # Create plan that modifies file
  plan = {"actions": [{"type": "edit_file", "payload": {"path": "test.txt", "content": "modified"}}]}
  
  # Execute
  result = executor.execute("test_repo", plan)
  
  # Check file is reverted
  cat test_repo/test.txt
  ```
  **Expected:** File unchanged after execution
  **If modified:** 🔴 CRITICAL - rollback not working

---

## PART 5: DEPENDENCY VERIFICATION (3 min)

### Required Imports
- [ ] **All security modules imported**
  ```bash
  grep -E "from dgm_hub.security|from dgm_hub.control" src/dgm_hub/main.py
  ```
  **Expected:** PathGuard, PolicyEngine, SafeExecutionManager imported

- [ ] **Tool manager initialized with guard**
  ```bash
  grep -A5 "UnifiedToolManager" src/dgm_hub/core/bootstrap.py
  ```
  **Expected:** PathGuard passed to tool manager

### External Dependencies
- [ ] **Python version is 3.12+**
  ```bash
  grep "requires-python" pyproject.toml
  ```
  **Expected:** `>=3.12`

- [ ] **FastAPI version is recent**
  ```bash
  grep "fastapi" pyproject.toml
  ```
  **Expected:** `>=0.111`

---

## PART 6: TEST COVERAGE (3 min)

### Security Tests
- [ ] **Shell injection tests exist**
  ```bash
  grep -r "shell.*inject\|injection" tests/
  ```
  **Expected:** Tests for shell command injection
  **If missing:** ⚠️ HIGH - critical vulnerability untested

- [ ] **Path traversal tests exist**
  ```bash
  grep -r "path.*traversal\|../../../../" tests/
  ```
  **Expected:** Tests for path escape attempts
  **If missing:** ⚠️ HIGH - path guard untested

- [ ] **Tool access control tests exist**
  ```bash
  grep -r "PathGuard\|allowed_path" tests/
  ```
  **Expected:** Tests for tool access restrictions
  **If missing:** ⚠️ MEDIUM - access control untested

### Test Execution
- [ ] **Run test suite**
  ```bash
  pytest tests/ -v
  ```
  **Expected:** All pass (or clear failures explained)
  **If failures:** 🔴 CRITICAL - tests broken

---

## PART 7: PERFORMANCE VERIFICATION (2 min)

### Snapshot Size
- [ ] **Check average snapshot size**
  ```bash
  du -sh runtime/snapshots/*
  ```
  **Expected:** Size reasonable for your repo (~equal to repo size)
  **If >> repo size:** ⚠️ MEDIUM - duplicate copies

### Execution Time
- [ ] **Time a single execution**
  ```python
  import time
  start = time.time()
  result = executor.execute(repo_path, plan)
  elapsed = time.time() - start
  print(f"Execution took {elapsed:.1f}s")
  ```
  **Expected:** < 60s for typical plan
  **If > 60s:** ⚠️ MEDIUM - snapshot overhead (see DGM-HUB_REAL_WORLD_PROBLEMS.md Problem #2)

### Disk Usage Trend
- [ ] **Check snapshots folder size over time**
  ```bash
  du -sh runtime/snapshots/
  # Note this value
  # Wait 1 hour, run 3-4 plans
  du -sh runtime/snapshots/
  ```
  **Expected:** Slow growth (or stable if cleanup working)
  **If fast growth:** 🔴 CRITICAL - snapshots not cleaned (Problem #1)

---

## PART 8: CODE QUALITY (3 min)

### Dead Code Check
- [ ] **Evolution system actively used?**
  ```bash
  grep -r "EvolutionEngine" src/ --include="*.py" | grep -v "import\|class"
  ```
  **Expected:** Used in execution path
  **If only imports:** ⚠️ MEDIUM - dead code cleanup needed

- [ ] **Swarm system actively used?**
  ```bash
  grep -r "SwarmCoordinator\|SwarmLoop" src/ --include="*.py" | grep -v "import\|class"
  ```
  **Expected:** Used in execution path
  **If only imports:** ⚠️ MEDIUM - dead code cleanup needed

### Type Hints
- [ ] **Function signatures have type hints**
  ```bash
  grep -E "def [a-z_]+\([^)]*:[^)]*\)" src/dgm_hub/control/task_executor.py
  ```
  **Expected:** Function parameters typed
  **If missing:** ⚠️ LOW - documentation clarity

---

## PART 9: SEMANTIC VERIFICATION (2 min)

### Rollback Behavior
- [ ] **Confirm rollback semantics documented**
  ```bash
  grep -B5 -A5 "rollback.*always\|always.*rollback" src/dgm_hub/control/task_executor.py
  ```
  **Expected:** Clear comment explaining intent
  **If missing:** ⚠️ MEDIUM - behavior unclear to maintainers

- [ ] **Test that changes DON'T persist after execute()**
  ```python
  # Create test
  plan = {"actions": [{"type": "create_file", "payload": {"path": "test.txt", "content": "data"}}]}
  result = executor.execute(repo_path, plan)
  # After execution, test.txt should NOT exist in repo
  assert not Path(repo_path / "test.txt").exists()
  ```
  **Expected:** File doesn't persist (rollback working)
  **If persists:** ❌ CRITICAL - rollback broken

---

## PART 10: INCIDENT RESPONSE (Only if issues found)

### If Shell Injection Found 🔴
```
1. Disable tool that has shell=True
2. Create bug issue with severity CRITICAL
3. Block merging any PRs with shell=True
4. Patch immediately using shlex.split()
```

### If Path Guard Missing 🔴
```
1. Disable unguarded tool (PowerShell/Cmd)
2. Create bug issue with severity CRITICAL
3. Apply PathGuard to tool constructor
4. Add test requiring path validation
```

### If Silent Exception Swallow Found 🔴
```
1. Add logging to exception handler
2. Re-raise exception (don't swallow)
3. Create test verifying exception is raised
4. Document error handling in code
```

### If Snapshots Accumulating 🔴
```
1. Manually delete old snapshots:
   rm -rf runtime/snapshots/*
2. Implement auto-cleanup in SafeExecutionManager
3. Monitor disk usage after cleanup
4. Set alert if snapshots > 50GB
```

---

## QUICK RESULTS TEMPLATE

Copy this and fill in during review:

```markdown
# DGM-HUB Audit Results
**Date:** [DATE]
**Auditor:** [NAME]
**Time:** [DURATION] minutes

## Security Status
- Shell execution: [✅/⚠️/🔴] - [Finding]
- Path access control: [✅/⚠️/🔴] - [Finding]
- Exception safety: [✅/⚠️/🔴] - [Finding]

## Configuration Status
- allowed_paths: [✅/⚠️/🔴] - [Finding]
- Mode/Platform: [✅/⚠️/🔴] - [Finding]

## Execution Flow Status
- Snapshots: [✅/⚠️/🔴] - [Finding]
- Tools: [✅/⚠️/🔴] - [Finding]
- Tests: [✅/⚠️/🔴] - [Finding]

## Data Integrity Status
- Journal: [✅/⚠️/🔴] - [Finding]
- Rollback: [✅/⚠️/🔴] - [Finding]

## Performance Status
- Snapshot overhead: [✅/⚠️/🔴] - [Finding]
- Disk usage: [✅/⚠️/🔴] - [Finding]

## Critical Issues Found: [NUMBER]
- [ ] Issue #1: [Description]
- [ ] Issue #2: [Description]

## Recommendations
1. [Action]
2. [Action]

## Sign-off
- [ ] All critical issues resolved
- [ ] All P1 issues tracked
- [ ] Documentation updated
```

---

## REFERENCE LINKS

- **Full Architecture Report:** DGM-HUB_ARCHITECTURE_REAL_ANALYSIS.md
- **Real-World Problems:** DGM-HUB_REAL_WORLD_PROBLEMS.md
- **Code Location:** C:\ProgramasGodMode\DGM-HUB\src\dgm_hub\
- **Config Location:** C:\ProgramasGodMode\DGM-HUB\config\

---

**Last Updated:** 2025-06-07  
**Maintenance:** Update whenever critical security issues are fixed