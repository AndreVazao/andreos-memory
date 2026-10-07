# CONTEXTO DGM-MCP: Phase Transition (v0.1.5 → MCP Core)

**Date:** 2026-06-19  
**Status:** Pre-Architecture-Freeze  
**Readiness:** 85% (Production Backend) / 30% (MCP Protocol)

---

## Critical Insight: DGM-MCP ≠ MCP

**The Finding:**
DGM-MCP é um **Agent Orchestrator + Task Runtime + Tool Execution Engine**.
NÃO é um servidor MCP compatível.

**Current State (Wrong Path):**
```
POST /mcp/task → Custom HTTP API
Claims: "Pronto para integração real com Claude Desktop"
Reality: Bridge adapter, não protocolo MCP
```

**What Claude Desktop / Cursor / Windsurf Expect:**
```
JSON-RPC 2.0
├─ tools/list
├─ tools/call
├─ resources/*
├─ prompts/*
└─ STDIO Transport (ou HTTP SSE)
```

---

## Architecture Status

| Component | Status | Notes |
|-----------|--------|-------|
| TaskManager | 95% ✅ | Solid, no changes needed |
| Worker Pool | 95% ✅ | Stable runtime |
| CognitiveAgent | 90% ✅ | Minor observability tweaks |
| Tools (FS/Git/Shell) | 90% ✅ | Semantic logic sound |
| Security Layer | 92% ✅ | PathGuard audit logging gap only |
| Observability | 88% ✅ | Good trace/metric collection |
| **bridge/** | 40% ⚠️ | Needs protocol rewrite |
| **web/** | 40% ⚠️ | Needs JSON-RPC layer |
| **transport/** | 0% ❌ | STDIO + HTTP SSE missing |

---

## Phase 1: Architecture Freeze (Next 2 PRs)

### Action 1: ARCHITECTURE_MAP.md

**Prompt to Jules:**

```
Generate ARCHITECTURE_MAP.md

Requirements:

1. Map every module (no code changes)
2. Generate Mermaid diagrams:
   - Runtime bootstrap
   - Task flow (enqueue → execute → result)
   - Tool execution (invoke → validate → run → serialize)
   - LLM provider integration
   - Security layer (PathGuard + CommandValidator)
   - Web layer (current HTTP shape)
   - Bridge layer (current design)

3. Dependency graph (module imports)
4. Call flow: User → API → Runtime → Agent → Tool → Result
5. Dead code audit (confirm shadow modules)

Output: ARCHITECTURE_MAP.md (no code changes)
```

**Why:**
- Antes de mexer na fundação, precisamos de blueprint completo
- Vai confirmar o que pode ficar intacto (80% runtime)
- Vai identificar exatamente quem mexe no quê

---

## Phase 2: MCP Implementation Roadmap (After MAP)

### Action 2: MCP_IMPLEMENTATION_ROADMAP.md

**Prompt to Jules:**

```
Create MCP_IMPLEMENTATION_ROADMAP.md

Based on ARCHITECTURE_MAP.md and MCP specification.

Split implementation into 8 phases:

Phase 1: JSON-RPC 2.0 Core
Phase 2: Tool Discovery (tools/list)
Phase 3: Tool Invocation (tools/call)
Phase 4: Resources (resources/*)
Phase 5: Prompts (prompts/*)
Phase 6: STDIO Transport
Phase 7: HTTP SSE Transport
Phase 8: Claude Desktop Validation

For each phase provide:
- Files to create
- Files to modify
- Estimated LOC
- Runtime impact analysis
- Backwards compatibility strategy
- Risk assessment

Output: MCP_IMPLEMENTATION_ROADMAP.md (specification only)
```

**Why:**
- Vai revelar que 80% do runtime fica intacto
- Apenas `bridge/`, `web/`, `transport/` mudam
- Mostra que TaskManager, Worker, Agent, Tools, Security continuam

---

### Action 3: MCP_TOOL_SCHEMAS.md (Early Generation)

**Prompt to Jules:**

```
Generate MCP_TOOL_SCHEMAS.md

Create JSON Schema definitions for all DGM-MCP tools:

1. FilesystemTool
   - read_file
   - write_file
   - delete_file
   - list_directory

2. GitTool
   - clone
   - commit
   - push
   - branch

3. ShellTool
   - execute_command

4. PatchTool
   - apply_patch
   - generate_patch

5. RepoTool
   - analyze
   - extract

Each schema:
- name
- description
- inputSchema (JSON Schema)
- constraints
- examples

Output: MCP_TOOL_SCHEMAS.md (no code)
```

**Why:**
- Vai poupar semanas de trabalho later
- Necessário para `tools/list` response
- Define contract que todos os tools precisam cumprir

---

## Phase 3: PR Sequence (After Roadmap Approved)

### PR 1: JSON-RPC Core
```
mcp/request.py        (new)
mcp/response.py       (new)
mcp/errors.py         (new)
tests/test_jsonrpc.py (new)

Creates JSON-RPC 2.0 request/response marshalling
Does NOT touch runtime yet
```

### PR 2: Tool Discovery
```
bridge/tool_registry.py (new)
web/routes/mcp.py      (new)

Exposes tools/list endpoint
Returns schemas from MCP_TOOL_SCHEMAS
Still uses current HTTP API internally
```

### PR 3: Tool Call
```
web/routes/mcp.py      (modify)

Transforms POST /mcp/task
Into JSON-RPC method: tools/call
Maps request → tool execution → response

First dual-protocol moment:
Old API still works + new JSON-RPC works side-by-side
```

### PR 4: STDIO Transport (Most Critical)
```
transport/stdio.py     (new)
transport/protocol.py  (new)

STDIO server opens Unix socket / named pipe
Claude Desktop fala direto com DGM-MCP
Sem HTTP, sem bridge adapters

This is where value explodes:
- Claude Desktop integration ✅
- Cursor integration ✅
- Windsurf integration ✅
```

---

## Readiness Assessment

### Before Last PRs
```
65% production ready
```

### Now (v0.1.5)
```
Production Backend:  85% ✅
MCP Protocol:        30% ⚠️
Overall:             65% → 85% (backend only)
```

### After MCP Implementation
```
Production Backend:  85% ✅
MCP Protocol:        95% ✅
Overall:             90% (true production ready)
```

---

## Key Insight

**The Next Value Leap is NOT:**
- More security checks
- More observability
- More features on tools

**The Next Value Leap IS:**
Transform `bridge/` from custom HTTP API → True MCP Protocol

**Impact:**
- Claude Desktop can natively connect
- Cursor can natively connect
- Windsurf can natively connect
- Any MCP client can natively connect
- No adapters, no workarounds, no custom integrations

**This is the inflection point that moves DGM-MCP from "internal tool" to "ecosystem player"**

---

## Immediate Next Steps

1. ✋ FREEZE architecture (don't touch runtime yet)
2. 📋 Generate ARCHITECTURE_MAP.md
3. 🗺️ Generate MCP_IMPLEMENTATION_ROADMAP.md
4. 📝 Generate MCP_TOOL_SCHEMAS.md
5. ✅ Review with core team
6. 🔨 Start PR 1: JSON-RPC Core
