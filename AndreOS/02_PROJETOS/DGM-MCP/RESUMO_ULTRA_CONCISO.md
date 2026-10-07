# v0.2.0 Estratégia: Ultra-Conciso

**Decision Made:** Certification-First (não straight to v0.3.0)  
**Why:** Testar com clientes REAIS antes de release  
**Cost:** +5-7 dias  
**Gain:** Meses de estabilidade (evita hotfixes)

---

## 3 Ações Concretas

### 1. PR 1: Repo Hygiene
- **O quê:** Remove audit.log e logs/ do git
- **Tempo:** ~2 horas
- **Guide:** `PR1_REPO_HYGIENE.md` (passo-a-passo)

### 2. PR 2: Framework
- **O quê:** Templates de certificação + test skeletons
- **Tempo:** ~1-2 dias
- **Guide:** `PR2_CERTIFICATION_FRAMEWORK.md` (passo-a-passo)

### 3. Phase 2.5: Real Testing
- **O quê:** Jules testa com Claude Desktop, Cursor, Windsurf, MCP Inspector
- **Tempo:** ~3-4 dias testing + reports
- **Prompt:** Embed em `PR_SEQUENCE_v0.2.0_CLOSE.md`

---

## Timeline

```
Today:     Aprovação estratégia
Day 1-2:   PR 1 + PR 2 merge
Days 3-7:  Phase 2.5 testing
Day 7:     v0.2.0 release (se tudo passar)
```

---

## Success = When This Happens

```
✅ PR 1 merged (logs não são tracked)
✅ PR 2 merged (framework pronto)
✅ Jules testa 4 clientes
✅ Relatórios mostram "CERTIFIED"
✅ v0.2.0 release com confiança
```

---

## Documentos (Todos no Vault)

```
Estratégia:
  1. DECISAO_FINAL_v0.2.0_STRATEGY.md (contexto completo)
  2. PR_SEQUENCE_v0.2.0_CLOSE.md (sequência detalhada)

Operacional:
  3. PR1_REPO_HYGIENE.md (step-by-step)
  4. PR2_CERTIFICATION_FRAMEWORK.md (step-by-step)
  5. NEXT_ACTIONS_QUICK_START.md (o que fazer agora)
```

---

**READY? Start with PR1_REPO_HYGIENE.md**
