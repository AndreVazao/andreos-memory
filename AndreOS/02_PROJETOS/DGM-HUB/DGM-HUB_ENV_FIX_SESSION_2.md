# DGM-HUB Environment Consistency Fix — Session 2025-06-10

## Problem Identified
**API Mismatch between WorkflowRuntime and TestPipeline**

The code was failing with:
```
TestPipeline.run() got an unexpected keyword argument 'cwd'
```

This was caused by version mismatch in the environment Python import paths.

## Root Cause Analysis

### Initial State
1. Local `test_pipeline.py` had old signature: `run(repo_path, command=None)`
2. Local `workflow_runtime.py` was calling with: `.run(command, cwd=cwd)` ❌
3. This caused: `TypeError: got an unexpected keyword argument 'cwd'`

### The Pull Updated Everything
After `git pull origin main`, the repository was updated with:
- **New `test_pipeline.py` signature**: `run(command=None, cwd=None)` ✓
- This new signature is correct and matches the call pattern

### What Was Wrong in Local Environment
Before the pull, the environment had:
- Old code being imported from repo (`C:\ProgramasGodMode\DGM-HUB\src\`)
- Older API contract that wasn't being respected

## Solutions Applied

### Step 1: Clean Repository State
```bash
git restore --staged .    # Unstage all changes
git restore .             # Discard working directory changes
git pull origin main      # Pull latest (4 commits behind)
```
✓ **Status**: Clean pull completed, 19 files updated

### Step 2: Fresh Package Installation
```bash
pip install -e . --force-reinstall --no-cache-dir
```
✓ **Status**: Reinstalled all dependencies (dgm-hub + 25 transitive deps)

### Step 3: Verify Import Paths
Created `test_imports.py` to verify:
- `TestPipeline` imported from correct file
- API signatures match actual code
- No stale site-packages versions interfering

Results:
```
[OK] TestPipeline.run signature: (command: str | None = None, cwd: str | Path | None = None)
[OK] WorkflowRuntime.run_tests signature: (command: str, cwd: str | None = None)
```

### Step 4: Update WorkflowRuntime
Fixed `workflow_runtime.py` line 36-39:
```python
return self.tests.run(
    command=command,
    cwd=cwd
)
```
✓ Maps `cwd` parameter correctly to TestPipeline's signature

## Test Results

Ran full test suite:
```
29 PASSED
1 SKIPPED
121.90s total runtime
```

All critical tests passing:
- Chaos tests (subprocess timeout, git failure, permissions, etc.)
- Integration tests (real repositories, large repos, forbidden paths)
- Real-world tests (truth layer)
- End-to-end tests (security, execution, approval UI, engineering loop)

## Key Learnings

### Why Environment Consistency Failed Initially
1. GitHub had newer code than local repo
2. Local `pip install -e .` was cached
3. Python was importing from old code
4. Mismatch between file content and runtime behavior

### Prevention
- Always verify import paths before running tests:
  ```python
  import dgm_hub.execution.test_pipeline as t
  print(t.__file__)  # Should point to repo location
  ```
- Use `pip install -e . --force-reinstall` when pulling major changes
- Don't rely on `git status` alone — verify imports at Python level

## Remaining Known Issues (From Previous Audit)

### CRITICAL
- [PROBLEM #3] Shell injection in test commands (`shell=True`)
- [PROBLEM #4] Unguarded PowerShell/Cmd tools access

### HIGH
- [PROBLEM #1] Snapshot disk space exhaustion (every 10-20 executions)
- [PROBLEM #5] Silent rollback failures lose context
- [PROBLEM #10] No rate limiting on tool execution

### MEDIUM
- [PROBLEM #2] Slow execution due to large repository copies (30+ seconds)
- [PROBLEM #6] Unclear which entry point to use
- [PROBLEM #7] Rollback always executes (semantics unclear)
- [PROBLEM #8] Tool parameter validation missing

### LOW
- [PROBLEM #9] Evolution system unclear (documentation needed)

## Session Summary

**Status**: ✅ **INFRASTRUCTURE ISSUE RESOLVED**

The real problem wasn't missing features—it was environment consistency. Code on GitHub was correct; local environment was stale. After cleaning up and reinstalling, all 29 tests pass.

**Next Phase**: Security hardening (fix CRITICAL issues #3, #4) before moving to Ollama integration or autonomous agents.
