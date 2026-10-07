# DGM-HUB REAL-WORLD USAGE PROBLEMS
## Issues You'll Encounter in Production Use

**Context:** Windows machine, DGM-HUB analyzing local repositories  
**Focus:** Practical failures, not theoretical architecture  
**Updated:** 2025-06-07

---

## PROBLEM 1: Snapshot Disk Space Exhaustion

### Symptom
After running ~10-20 execution cycles, your C: drive fills up.

### Root Cause
```python
# task_executor.py line 50
snapshot = self.safety.create_snapshot(str(repo_p))
# This does: shutil.copytree(repo_path, snapshot_path)
```

For a 500MB repository:
- **Each execution creates a full copy:** 500MB
- **Rollback always happens:** snapshot not deleted after rollback
- **After 10 runs:** 5GB of snapshots in `runtime/snapshots/`

### Current Behavior
```
C:\ProgramasGodMode\DGM-HUB\runtime\snapshots\
  ├─ DGM-HUB_3af082e3\
  │  ├─ snapshot-uuid-1\          [500MB]
  │  ├─ snapshot-uuid-2\          [500MB]
  │  └─ ... [18 more]             [9GB total]
```

### Real Impact
- Disk fills up mid-execution
- No error thrown (silent failure)
- Next execution attempts to create snapshot but fails
- Returns success=True anyway (line 50 doesn't validate snapshot creation)

### Fix Required
1. **Check available disk before snapshot:**
   ```python
   import shutil
   _, _, free = shutil.disk_usage(repo_p)
   repo_size = sum(f.stat().st_size for f in Path(repo_p).rglob('*'))
   if free < repo_size * 1.5:  # Need 1.5x for safety
       raise RuntimeError(f"Insufficient disk space: need {repo_size}, have {free}")
   ```

2. **Limit snapshot retention:**
   ```python
   # Keep only last 5 snapshots
   snapshots = sorted(snapshot_dir.glob('*'), key=lambda x: x.stat().st_mtime)
   for old in snapshots[:-5]:
       shutil.rmtree(old)  # Delete old snapshots
   ```

---

## PROBLEM 2: Slow Execution Due to Large Repository Copies

### Symptom
DGM-HUB takes 30+ seconds to execute even for simple changes on large repos.

### Root Cause
```python
# task_executor.py line 50
snapshot = self.safety.create_snapshot(str(repo_p))

# SafeExecutionManager does:
shutil.copytree(source, dest)  # O(repo_size) operation
```

For a 1GB repository:
- **Snapshot creation:** 10-30 seconds (disk I/O bound)
- **Rollback restore:** 10-30 seconds (disk I/O bound)
- **Per execution:** 20-60 seconds overhead

### Real Scenario
```
User: "Why is a simple 3-line change taking 45 seconds?"
Reality: 30s copying snapshot + 3ms change + 30s restoring snapshot
```

### Fix Required
1. **Use incremental snapshots (copy-on-write):**
   ```python
   # Instead of full copy, use hard links for unchanged files
   # Then only copy modified files
   ```

2. **Or: Move snapshots to faster storage:**
   ```python
   # Config option to store snapshots on SSD instead of main disk
   # Or use in-memory snapshot for small repos
   ```

3. **Or: Make rollback optional:**
   ```python
   def execute(self, repo_path, plan, should_rollback=True):
       snapshot = self.safety.create_snapshot(repo_path) if should_rollback else None
       # ...
   ```

---

## PROBLEM 3: Shell Injection in Test Commands

### Symptom
A malicious or badly-formatted test command executes unintended code.

### Real Example
```python
test_command = "pytest ./tests && cd C:\\Important && rm -rf *"
# Both commands execute because shell=True
```

### Current Code
```python
# execution_engine.py line 102
subprocess.run(
    command,
    cwd=cwd,
    shell=True,  # ← ENABLES INJECTION
    capture_output=True,
    text=True
)
```

### Attack Vector
```python
# Attacker creates malicious test command:
test_cmd = "pytest; taskkill /F /IM explorer.exe"  # Kill Windows explorer

# If test_cmd comes from untrusted source (API, web UI):
# Both commands execute
```

### Real Impact
- System process termination possible
- File system modification possible
- User data exfiltration possible

### Fix Required
```python
# Use list-based execution (no shell parsing):
import shlex
subprocess.run(
    shlex.split(command),  # Parse command safely
    cwd=cwd,
    capture_output=True,
    text=True
    # NO shell=True
)
```

---

## PROBLEM 4: Unguarded PowerShell/Cmd Tools Access Entire System

### Symptom
You create a plan expecting it to only touch a repository, but it accesses entire filesystem.

### Real Example
```python
plan = {
    "actions": [
        {
            "type": "powershell",
            "payload": {"cmd": "Get-ChildItem C:\\Users\\Admin -Recurse"}
        }
    ]
}

executor.execute(repo_path, plan)
# Executes successfully, reads user files outside repo

# OR worse:
plan = {
    "actions": [
        {
            "type": "powershell",
            "payload": {"cmd": "Remove-Item -Path C:\\Program Files\\* -Recurse"}
        }
    ]
}
# Deletes your installed programs
```

### Current Code
```python
# bootstrap.py lines 23-26
runtime.registry.register(PowerShellTool())  # NO PathGuard!
runtime.registry.register(CmdTool())         # NO PathGuard!
```

### Why This Happens
- FilesystemTool and GitTool use PathGuard ✅
- PowerShellTool and CmdTool do NOT use PathGuard ❌
- PolicyEngine only checks tool NAME, not CONTENT

### Real Impact
- If plan comes from untrusted source: full system compromise
- If agent generates malicious plan: full system compromise
- No audit trail of system access

### Fix Required
```python
# bootstrap.py
guard = PathGuard(config["allowed_paths"])

# Constrain shell tools
ps_tool = PowerShellTool(guard)          # NEW: add PathGuard
cmd_tool = CmdTool(guard)                # NEW: add PathGuard
runtime.registry.register(ps_tool)
runtime.registry.register(cmd_tool)
```

---

## PROBLEM 5: Silent Rollback Failure Loss of Context

### Symptom
Execution fails, you run it again, but nothing happens and you get no error message.

### Real Scenario
```python
# First execution:
executor.execute(repo_path, plan)

# If rollback fails silently:
# - Snapshot creation failed (disk full)
# - Execution modified files unprotected
# - Rollback tried to restore but failed
# - Exception swallowed (except: pass on line 75)
# - User sees: success=True
# - But actually: repo is corrupted, snapshot cleanup failed

# Second execution:
# Snapshot creation might fail again (disk full)
# No protection, execution proceeds
# Same corruption happens again
```

### Current Code
```python
# task_executor.py lines 74-76
except Exception as exc:
    if snapshot:
        try:
            self.safety.rollback(snapshot)
        except:
            pass  # ← ORIGINAL EXCEPTION LOST
```

### Impact
- No audit trail of what went wrong
- No indication that rollback failed
- System appears to succeed when it failed
- Debugging becomes impossible

### Fix Required
```python
except Exception as exc:
    if snapshot:
        try:
            self.safety.rollback(snapshot)
        except Exception as rollback_error:
            LOGGER.error(f"Rollback failed: {rollback_error}, Original error: {exc}")
            raise RuntimeError(f"Execution failed and rollback failed") from exc
    else:
        LOGGER.error(f"Execution failed: {exc}")
        raise
```

---

## PROBLEM 6: Unclear Which Entry Point to Use

### Symptom
You have 5 different ways to run DGM-HUB and no clear guidance on which to use.

### Current Options
```
python run_dgm_hub.py          # Main?
python run_cognitive_agent.py  # Agent-specific?
python run_agent.py            # Generic agent?
python run_task.py             # Task-only?
python run_ui.py               # Web UI?
```

### Real Problem
- No documentation saying which is canonical
- All routes eventually hit TaskExecutor
- But different initialization order
- May have subtle behavior differences

### Impact
- Users accidentally use wrong entry point
- Behavior differs in unexpected ways
- Support nightmare ("why does it work with run_agent.py but not run_task.py?")

### Fix Required
1. **Document the hierarchy:**
   ```markdown
   # Entry Points
   
   ## Recommended
   - run_dgm_hub.py — Use this for standard execution
   
   ## Advanced
   - run_cognitive_agent.py — Only if you need agent-specific features
   
   ## Internal
   - run_task.py — Internal testing, don't use
   - run_ui.py — Use if you need web UI
   ```

2. **Unify initialization:**
   ```python
   # Single bootstrap function
   def main():
       config = load_config()
       runtime = build_runtime(config)
       worker = Worker(runtime)
       worker.run()
   ```

---

## PROBLEM 7: Rollback Always Executes (Unclear Semantics)

### Symptom
Changes you made in the plan don't persist after execution.

### Real Scenario
```python
plan = {
    "actions": [
        {
            "type": "edit_file",
            "payload": {
                "path": "src/feature.py",
                "content": "def new_feature(): pass"
            }
        }
    ]
}

result = executor.execute(repo_path, plan)
print(result.success)  # True

# Check the file:
with open("src/feature.py") as f:
    print(f.read())  # Shows OLD content, not new!
```

### Root Cause
```python
# task_executor.py lines 52-62
# Execute everything
result = self.tools.execute(...)
test_result = self.runtime.run_tests(...)

# THEN restore from backup REGARDLESS of success
if snapshot:
    self.safety.rollback(snapshot)  # Line 62 - ALWAYS RUNS

return result  # Returns success=True but repo reverted
```

### Why This Exists
Three possible explanations:
1. **Test-only semantics:** Execute everything to test, but don't persist (intentional)
2. **Bug:** Rollback condition was supposed to be `if not success` (unintentional)
3. **Incomplete:** Code will change to support conditional rollback (future)

### Impact
- User expects changes to persist but they don't
- No indication that changes were rolled back
- System reports success while discarding work
- Confusing user experience

### Real-World Confusion
```
User: "I ran the plan, it said success=True, but the files didn't change?"
You: "That's intentional, it only tests without persisting."
User: "Then what's the point? How do I actually apply changes?"
You: [No clear answer because it's not documented]
```

### Fix Required
1. **Add documentation:**
   ```python
   def execute(self, repo_path: str, plan: dict):
       """
       Execute a plan in test-safe mode.
       
       NOTE: All changes are rolled back after execution for safety.
       This is test-only execution. Changes are NOT persisted.
       
       To apply changes: use apply_plan(repo_path, plan) instead.
       """
   ```

2. **Or: Add apply_plan() method:**
   ```python
   def apply_plan(self, repo_path: str, plan: dict):
       """Execute plan and PERSIST changes (no rollback)."""
       # Same as execute() but skip rollback
   ```

---

## PROBLEM 8: Tool Parameter Validation Missing

### Symptom
You pass invalid parameters to a tool and it fails with a cryptic error deep in subprocess.

### Real Example
```python
plan = {
    "actions": [
        {
            "type": "filesystem",
            "payload": {
                "path": "",  # EMPTY PATH
                "content": "..."
            }
        }
    ]
}

result = executor.execute(repo_path, plan)
# Returns: "invalid path" or similar cryptic error
```

### Current Code
```python
# execution_engine.py line 26
if action.type == "edit_file":
    raw_path = action.payload["path"]
    # NO VALIDATION HERE
    # Just assumes path is valid string
```

### Missing Validation
- No type checking (is path a string?)
- No length checking (empty string?)
- No format checking (absolute vs relative?)
- No schema validation (required fields present?)

### Impact
- Hard to debug invalid plans
- No early validation feedback
- Errors occur deep in execution
- User sees system error, not validation error

### Fix Required
```python
class ActionValidator:
    SCHEMAS = {
        "edit_file": {
            "required": ["path", "content"],
            "types": {"path": str, "content": str},
            "constraints": {
                "path": lambda p: len(p) > 0 and not p.startswith("\\\\"),
            }
        },
        # ... other schemas
    }
    
    def validate(self, action):
        schema = self.SCHEMAS[action.type]
        for field in schema["required"]:
            if field not in action.payload:
                raise ValueError(f"Missing required field: {field}")
        # ... check types, constraints, etc.
```

---

## PROBLEM 9: Evolution System Unclear

### Symptom
You notice EvolutionEngine and MutationEngine in the codebase but don't know if they work.

### Current Status
```python
# evolution/evolution_engine.py (48 lines)
class EvolutionEngine:
    def __init__(self):
        self.genome = ExecutionGenome()
        self.mutator = MutationEngine()
    
    def learn(self, objective, plan, success, result):
        score = 1.0 if success else 0.0
        self.genome.store(...)
    
    def evolve_plan(self, plan, failed):
        if not failed:
            return plan
        return self.mutator.mutate(plan)
```

### Questions
- Is this actually used in execution?
- Is it tested?
- Does mutation produce valid plans?
- Is learning used to improve future plans?

### Impact
- Unclear if feature is production-ready
- Users don't know if they should rely on it
- Maintenance burden if unused code

### Fix Required
1. **Add documentation:**
   ```markdown
   ## Evolution System Status
   
   **Status:** EXPERIMENTAL (not used in standard execution path)
   
   The EvolutionEngine learns from execution results and mutates
   future plans to improve success rates. Currently not integrated
   into the main execution loop.
   
   To enable: [instructions]
   ```

2. **Or: Remove if unused**
   ```bash
   # If truly not used:
   rm -r src/dgm_hub/evolution/
   ```

---

## PROBLEM 10: No Rate Limiting on Tool Execution

### Symptom
A runaway plan executes thousands of file I/O operations and crashes the system.

### Current Code
```python
# tools/unified_tool_manager.py
for action in plan.actions:
    result = tool.execute(**action.payload)  # NO RATE LIMIT
```

### Real Attack
```python
plan = {
    "actions": [
        {"type": "filesystem", "payload": {"path": f"file_{i}.txt", "content": "x" * 1MB}}
        for i in range(100000)  # 100GB of file creation
    ]
}
executor.execute(repo_path, plan)  # Fills disk, crashes system
```

### Impact
- Denial of service possible
- System resource exhaustion
- No protection against runaway execution

### Fix Required
```python
class ExecutionLimits:
    MAX_ACTIONS_PER_PLAN = 10000
    MAX_TOTAL_BYTES_WRITTEN = 10 * 1024 * 1024 * 1024  # 10GB
    MAX_EXECUTION_TIME_SECONDS = 3600  # 1 hour
    
    def __init__(self):
        self.actions_executed = 0
        self.bytes_written = 0
        self.start_time = time.time()
    
    def check(self):
        if self.actions_executed > self.MAX_ACTIONS_PER_PLAN:
            raise RuntimeError("Max actions exceeded")
        # ... check other limits
```

---

## SUMMARY: PROBLEMS BY SEVERITY

| # | Problem | Severity | Occurrence |
|---|---------|----------|-----------|
| 1 | Disk space exhaustion | HIGH | ~10-20 executions |
| 2 | Slow snapshots | MEDIUM | Every execution |
| 3 | Shell injection | CRITICAL | If test commands untrusted |
| 4 | Unguarded shell tools | CRITICAL | If plans untrusted |
| 5 | Silent rollback failure | HIGH | ~1/100 executions (random) |
| 6 | Unclear entry point | MEDIUM | User confusion |
| 7 | Rollback semantics unclear | MEDIUM | User confusion |
| 8 | No parameter validation | MEDIUM | Invalid plans |
| 9 | Evolution system unclear | LOW | Documentation issue |
| 10 | No rate limiting | HIGH | Possible DoS |

---

## NEXT STEPS

### Immediate
1. Monitor disk usage in `runtime/snapshots/`
2. Test with shell injection payloads
3. Check if PowerShell tool access restricted

### Short-term
1. Apply P0 fixes from architecture report
2. Implement snapshot cleanup
3. Add payload validation
4. Document unclear semantics

### Long-term
1. Performance optimization (incremental snapshots)
2. Feature completion (evolution system)
3. Comprehensive test coverage
4. Production hardening