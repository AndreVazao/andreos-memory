# DGM-MCP: Phase Transition Strategy

**Analysis Date:** 2026-06-19  
**Analyst:** André + Jules  
**Current State:** v0.1.5 (85% production backend / 30% MCP protocol)  
**Next Gate:** Architecture Freeze → 3-document approval → Implementation

---

## The Critical Realization

### What We Thought We Had
```
"DGM-MCP is an MCP server ready for Claude Desktop integration"
HTTP endpoint: POST /mcp/task → Custom JSON protocol
Claims: Production ready
```

### What We Actually Have
```
DGM-MCP = Agent Orchestrator + Task Runtime + Tool Execution Engine

NOT: MCP Protocol Server

Currently: Custom HTTP API bridge
Expected by clients: JSON-RPC 2.0 + STDIO/SSE transport
```

### The Gap

| Aspect | DGM-MCP Today | MCP Standard | Impact |
|--------|---------------|--------------|--------|
| Protocol | HTTP + custom JSON | JSON-RPC 2.0 | 🔴 Incompatible |
| Discovery | Manual tool mapping | `tools/list` method | 🔴 No autodiscover |
| Invocation | POST /mcp/task | `tools/call` method | 🔴 Non-standard |
| Transport | HTTP only | STDIO + SSE | 🔴 Isolated |
| Clients | Hardcoded adapters | Any MCP client | 🔴 Limited adoption |

---

## Strategic Assessment

### Current Readiness
```
Production Backend:  85% ✅
├─ TaskManager, Worker, CognitiveAgent: Solid
├─ Tool execution: 90% correct
├─ Security layer: 92% (audit logging gap only)
└─ Observability: 88%

MCP Protocol:        30% ⚠️
├─ JSON-RPC: 0% (needs Phase 1)
├─ Tool discovery: 0% (needs Phase 2)
├─ Tool invocation: 40% (current HTTP bridges)
├─ Resources: 0% (Phase 4)
├─ Prompts: 0% (Phase 5)
├─ STDIO transport: 0% (CRITICAL, Phase 6)
└─ Integration: 0% (Phase 8)

OVERALL: 65% (backend is solid, protocol layer is missing)
```

### Architecture Safety Assessment

**Components That Can Stay Intact:**
- ✅ TaskManager (task queuing, persistence)
- ✅ Worker Pool (execution threading)
- ✅ CognitiveAgent (reasoning loop)
- ✅ Tool definitions (FS, Git, Shell, Patch, Repo)
- ✅ Security layer (PathGuard, CommandValidator)
- ✅ Observability (metrics, tracing)

**Estimated:** 80% of codebase is stable

**Components That Need Rewriting:**
- ❌ `bridge/` (custom API parser → JSON-RPC handler)
- ❌ `web/` (HTTP routes → MCP-compliant endpoints)
- ❌ `transport/` (doesn't exist → STDIO + SSE)

**Estimated:** 20% of codebase, mostly new layers

### Risk Profile

**Low Risk (Isolation):**
- Phase 1: JSON-RPC core (new module, no imports)
- Phase 2: Tool discovery (additive, no deletions)
- Phase 3: Tool invocation (dual-protocol coexistence)

**Medium Risk (First Runtime Touch):**
- Phase 6: STDIO transport (imports runtime, but clean interface)
- Phase 8: Integration validation (testing only)

**No High Risk Steps** (architecture is sound)

---

## Implementation Philosophy

### What We Will NOT Do

```
❌ Rewrite TaskManager
❌ Redesign Worker pool
❌ Change tool execution logic
❌ Modify security constraints
❌ Remove observability
❌ Break backwards compatibility
```

### What We WILL Do

```
✅ Build JSON-RPC 2.0 layer on top
✅ Expose tools via tools/list
✅ Map tool calls to tools/call method
✅ Add STDIO transport alongside HTTP
✅ Validate with real MCP clients
✅ Keep old API working (dual protocol)
```

---

## The Three-Document Freeze Strategy

Before ANY code is written, Jules generates three specifications:

### 1. ARCHITECTURE_MAP.md (Analysis Document)
**Purpose:** Complete blueprint of what exists  
**Deliverables:**
- Module inventory with stability ratings
- 7 Mermaid diagrams (runtime, task flow, tools, LLM bridge, security, web, bridge)
- Dependency graph
- Main call flow visualization
- Dead code audit confirmation

**Why:** Prevents assumptions; shows exact boundaries for change

### 2. MCP_IMPLEMENTATION_ROADMAP.md (Phased Specification)
**Purpose:** Exact sequence for protocol transformation  
**Deliverables:**
- Gap analysis (current state → MCP state)
- 8 phases with:
  - Files to create / modify
  - Estimated LOC per phase
  - Risk assessment
  - Backwards compatibility strategy
  - Migration notes

**Why:** Makes each PR predictable; shows integration points clearly

### 3. MCP_TOOL_SCHEMAS.md (Tool Catalog)
**Purpose:** JSON Schema for every tool operation  
**Deliverables:**
- FilesystemTool (5 operations)
- GitTool (6 operations)
- ShellTool (1 operation)
- PatchTool (2 operations)
- RepoTool (2 operations)

**Each operation:**
- Input schema (JSON Schema)
- Output schema (JSON Schema)
- Constraints
- Examples (request + response)

**Why:** Generated once, reused for tools/list + validation + docs

---

## Projected PR Sequence

After approval of the three documents:

### PR 1: JSON-RPC 2.0 Core
```
+mcp/request.py
+mcp/response.py
+mcp/errors.py
+tests/test_mcp_jsonrpc.py

Status: New module, no runtime touch
Impact: Low
```

### PR 2: Tool Discovery
```
+bridge/tool_registry.py
+web/routes/mcp_discovery.py

Status: New endpoints, additive
Impact: Low
```

### PR 3: Tool Invocation
```
~web/routes/mcp_discovery.py (add tools/call handler)
+bridge/tool_dispatcher.py

Status: First runtime integration (clean)
Impact: Medium (but tested before merge)
Dual protocol: Old HTTP + new JSON-RPC coexist
```

### PR 4: STDIO Transport (Critical Value Unlock)
```
+transport/stdio_server.py
+transport/protocol.py
+transport/messages.py
~main.py (add STDIO mode)

Status: Native client integration starts here
Impact: Medium
Result: Claude Desktop, Cursor, Windsurf can connect natively
```

### (Optional) PR 5: HTTP SSE Transport
```
+transport/sse_server.py

Status: Browser/HTTP client alternative
Impact: Low
```

### PR 6: Integration Validation
```
+tests/integration/test_claude_desktop.py
+tests/integration/test_cursor.py
+tests/integration/test_windsurf.py

Status: Manual testing with real IDEs
Impact: None (validation only)
```

---

## Success Metrics

### After Architecture Freeze (Documents Approved)
```
✅ Team consensus on scope
✅ Exact LOC estimates per PR
✅ Risk profile visible
✅ No surprises in Phase 1-2
✅ Clear integration boundaries
```

### After Phase 1-3 (Basic MCP Protocol)
```
✅ JSON-RPC core working
✅ tools/list returns correct schemas
✅ tools/call invokes tools correctly
✅ Dual-protocol tests passing
✅ No regression in old HTTP API
```

### After Phase 6 (STDIO Transport)
```
✅ Claude Desktop connects natively
✅ Cursor connects natively
✅ Windsurf connects natively
✅ Any MCP client can connect
✅ No adapters needed
```

### Full Implementation (Phase 8)
```
✅ MCP Protocol: 95%
✅ Production Backend: 85%
✅ Overall: 90% (true production ready)
✅ Ecosystem Integration: ✅
```

---

## Why This Matters

**Current State Problem:**
```
DGM-MCP is a powerful backend that's hard to integrate.
Each IDE (Claude Desktop, Cursor, Windsurf) needs custom adapter.
Adoption barrier is high.
```

**After MCP Implementation:**
```
DGM-MCP is a standard MCP server.
Any IDE that speaks MCP can integrate instantly.
Adoption barrier is zero.
Zero maintenance cost for new integrations.
Opens ecosystem possibilities.
```

---

## Timeline Estimate

| Phase | Time | Blocker |
|-------|------|---------|
| Documents (Jules analysis) | 2-3 hours | None |
| Architecture review | 1 day | Team availability |
| PR 1 (JSON-RPC) | 1-2 days | Clear implementation plan |
| PR 2 (Discovery) | 1 day | Phase 1 merged |
| PR 3 (Invocation) | 2 days | Phase 2 merged, testing |
| PR 4 (STDIO) | 2-3 days | Phase 3 merged, testing |
| PR 5 (SSE) | 1 day | Phase 4 merged |
| PR 6 (Validation) | 2-3 days | All phases merged |
| **Total** | **~2-3 weeks** | Parallel work possible |

---

## Decision Point

### Proceed With Architecture Freeze?

**YES IF:**
- Team agrees DGM-MCP's next value is MCP protocol compatibility
- We're ready to spend 2-3 weeks on protocol layers
- We want to unblock Claude Desktop, Cursor, Windsurf integration
- We value ecosystem adoption over new tool features

**NO IF:**
- We need more tool features before protocol work
- Team is unavailable for protocol engineering
- HTTP adapter is sufficient for current use cases

---

**Recommendation:** YES. Proceed with three-document freeze.

The backend is solid. The inflection point for adoption is the protocol layer.
Once STDIO transport works, integration becomes automatic for any MCP client.

This is the move from "internal tool" to "ecosystem player".
