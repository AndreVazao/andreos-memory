# ANDREOS MEMORY OS — BOOTSTRAP CORE

## 1. SYSTEM OVERVIEW
This repository is the canonical persistent memory layer for the Andreos ecosystem.

It centralizes:
- Long-term memory storage
- Agent context synchronization (Cloud Desktop, Antigravity, Obsidian)
- Cross-device state persistence
- DevOps orchestration memory layer

## 2. MEMORY ARCHITECTURE

C:\ProgramasGodmode\andreos-memory
        │
        ├── Obsidian Vault (UI layer)
        ├── Cloud Desktop (execution + debugging layer)
        ├── Antigravity (agent orchestration layer)
        ├── GitHub (persistent sync layer)
        └── Windows Environment Variables (system binding layer)

## 3. SINGLE SOURCE OF TRUTH

All tools should reference:

ANDREOS_MEMORY = C:\ProgramasGodmode\andreos-memory

This repository represents the canonical state of system memory.

## 4. WINDOWS ENVIRONMENT SETUP

### CMD
```cmd
setx ANDREOS_MEMORY "C:\ProgramasGodmode\andreos-memory" /M
setx OBSIDIAN_VAULT "C:\ProgramasGodmode\andreos-memory" /M
setx ANTIGRAVITY_MEMORY "C:\ProgramasGodmode\andreos-memory" /M
setx CLOUD_DESKTOP_MEMORY "C:\ProgramasGodmode\andreos-memory" /M
setx GODMODE_MEMORY "C:\ProgramasGodmode\andreos-memory" /M
```

### PowerShell
```powershell
[Environment]::SetEnvironmentVariable("ANDREOS_MEMORY","C:\ProgramasGodmode\andreos-memory","Machine")
[Environment]::SetEnvironmentVariable("OBSIDIAN_VAULT","C:\ProgramasGodmode\andreos-memory","Machine")
[Environment]::SetEnvironmentVariable("ANTIGRAVITY_MEMORY","C:\ProgramasGodmode\andreos-memory","Machine")
[Environment]::SetEnvironmentVariable("CLOUD_DESKTOP_MEMORY","C:\ProgramasGodmode\andreos-memory","Machine")
```

## 5. SYMLINK STANDARDIZATION

```cmd
mklink /D "C:\DevopsGodmode\memory" "C:\ProgramasGodmode\andreos-memory"
mklink /D "C:\DevopsGodmode\vault" "C:\ProgramasGodmode\andreos-memory"
mklink /D "C:\DevopsGodmode\obsidian" "C:\ProgramasGodmode\andreos-memory"
```

## 6. MEMORY RULES

- This repository is the primary memory source
- Agents should sync state changes here
- Obsidian acts as visualization layer
- GitHub is the persistence layer of record

## 7. FUTURE EXTENSIONS
- Vector-based memory indexing
- Multi-agent context routing
- Automated memory compression
- Event-driven synchronization hooks

## 8. BOOT SEQUENCE
1. Load ANDREOS_MEMORY environment variable
2. Sync Obsidian vault
3. Pull latest GitHub state
4. Initialize agent contexts

---
This system defines the foundation for a persistent distributed memory substrate.