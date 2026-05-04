# Histórico - God Mode

## 2026-04-30
Criada a memória inicial do projeto God Mode dentro do repo privado `AndreVazao/andreos-memory`.

## 2026-05-03 — Fases 155–164
Bloco grande de evolução do God Mode para passar de dashboard/automações soltas para orquestrador real com memória, planeamento, segurança, providers e playbooks.

### Fases implementadas

- Phase 155 — `Ecosystem Map Operationalization`
  - Documento do ecossistema passou a camada operacional.
  - Criados endpoints `/api/ecosystem-map/*`.
  - God Mode classifica projetos/repos por grupo, execução, licenciamento, memória e reusable code.

- Phase 156 — `Ruflo Research Lab Adapter`
  - Criado/adaptado laboratório `AndreVazao/godmode-ruflo-lab`.
  - Ruflo fica como pesquisa controlada, não dependência central.
  - Criados endpoints `/api/ruflo-research-lab/*`.

- Phase 157 — `Goal Planner Core`
  - Criado `goal_planner_service`.
  - Pedido do André vira plano com tarefas, riscos, memória, reusable code e validação.
  - Endpoints `/api/goal-planner/*`.

- Phase 158 — `AI Handoff Security Guard`
  - Criado filtro antes de enviar contexto para IA.
  - Deteta dados sensíveis e prompt injection antes de handoff externo.
  - Endpoints `/api/ai-handoff-security-guard/*`.

- Phase 159 — `Agent Roles Registry`
  - Criados papéis internos: architect, builder, tester, security, memory, reusable_code, github, obsidian, release, mobile, desktop, ai_research.
  - Endpoints `/api/agent-roles/*`.

- Phase 160 — `AI Provider Router`
  - Criado router com scoring/fallback para ChatGPT, Gemini, DeepSeek, Grok, Ollama e coding assistant local.
  - Endpoints `/api/ai-provider-router/*`.

- Phase 161 — `MCP Compatibility Map`
  - Mapeia endpoints do God Mode como futuras tools MCP/agents.
  - Ainda não cria servidor MCP real.
  - Endpoints `/api/mcp-compatibility/*`.

- Phase 162 — `Real Orchestration Pipeline v1`
  - Liga Goal Planner → Agent Roles → Security Guard → Provider Router → MCP Compatibility → Execution Gates → Safe Action Queue.
  - Endpoints `/api/real-orchestration/*`.

- Phase 163 — `Praison Research Adapter`
  - Praison registado como fonte de pesquisa para playbooks, workflows, RAG/memória, Ollama e agentes.
  - Endpoints `/api/praison-research/*`.

- Phase 164 — `Orchestration Playbooks v1`
  - Criado motor de playbooks JSON/YAML-like.
  - Playbook → validação → pipeline request → Real Orchestration Pipeline → safe action queue.
  - Modos v1: sequential, hierarchical, workflow, prompt_chain, evaluator_optimizer, parallel_safe.
  - Endpoints `/api/orchestration-playbooks/*`.

### Validação
As fases principais foram validadas por GitHub Actions com:

- Universal Total Test;
- Android APK Build;
- Windows EXE Build;
- Boot smoke test desktop backend;
- Upload artifact.

## 2026-05-04 — Phase 168

### Phase 168 — `GitHub Approved Actions Executor`

Implementado no repo `AndreVazao/devops-god-mode`.

- Serviço: `backend/app/services/github_approved_actions_executor_service.py`
- Rota: `backend/app/routes/github_approved_actions_executor.py`
- Docs: `docs/orchestration/github-approved-actions-executor.md`
- Smoke workflow: `.github/workflows/phase168-github-approved-actions-smoke.yml`
- Endpoints: `/api/github-approved-actions/*`

### Funcionalidade

- Liga ao playbook/template `approved_github_patch`.
- Executa apenas planos aprovados do `Repo/File Patch Hub`.
- Exige frase exata `APPLY REPO PATCH`.
- Faz `dry_run=true` por defeito.
- Em execução real pode garantir/criar branch, escrever ficheiros aprovados e abrir PR.
- Regista execução local e run no Patch Hub.

### Segurança

- Não faz merge automático.
- Não faz release.
- Não faz delete.
- Não faz force push.
- Não altera credenciais, pagamentos ou licenças.
- Merge continua dependente de GitHub Actions verdes e aprovação explícita do Oner.

### PR e validação

- PR #310 merged.
- Merge commit: `2ba51432b8f9353b06ae4473443429ce18f2f6a0`.
- Validações verdes antes do merge:
  - Phase 168 GitHub Approved Actions Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend;
  - Artifact Download Shortcuts Validation.

## 2026-05-04 — Phase 169

### Phase 169 — `Memory Sync Runtime`

Implementado no repo `AndreVazao/devops-god-mode`.

- Serviço: `backend/app/services/memory_sync_runtime_service.py`
- Rota: `backend/app/routes/memory_sync_runtime.py`
- Docs: `docs/orchestration/memory-sync-runtime.md`
- Smoke workflow: `.github/workflows/phase169-memory-sync-runtime-smoke.yml`
- Endpoints: `/api/memory-sync-runtime/*`

### Funcionalidade

- Regista eventos técnicos maduros do tipo `merged_phase`.
- Constrói pacote estável para AndreOS GitHub memory.
- Prepara nota Obsidian/local opcional.
- Separa GitHub memory estável de rascunho/local.
- Executa sync em `dry_run=true` por defeito.
- Liga por cima do `github_memory_sync_service` existente.

### Segurança

- Bloqueia conteúdo sensível antes de package/sync.
- GitHub memory recebe apenas memória técnica estável.
- Obsidian/local fica como oficina e continuidade local.
- Programas cloud não dependem do Obsidian local.

### PR e validação

- PR #311 merged.
- Merge commit: `b024a37ee798ef0664178204424f9c74d81eb8a2`.
- Houve uma falha inicial no smoke por serialização de dicts no package; corrigida no commit `6a525edb09698ccece1aa7dfeb1ea9366c1c0c70`.
- Validações verdes antes do merge:
  - Phase 169 Memory Sync Runtime Smoke;
  - Phase 168 GitHub Approved Actions Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend;
  - Artifact Download Shortcuts Validation.

## 2026-05-04 — Phase 170

### Phase 170 — `Local Knowledge/RAG Decision v1`

Implementado no repo `AndreVazao/devops-god-mode`.

- Serviço: `backend/app/services/local_knowledge_rag_decision_service.py`
- Rota: `backend/app/routes/local_knowledge_rag_decision.py`
- Docs: `docs/orchestration/local-knowledge-rag-decision-v1.md`
- Smoke workflow: `.github/workflows/phase170-local-knowledge-rag-smoke.yml`
- Endpoints: `/api/local-knowledge-rag/*`

### Funcionalidade

- Índice lexical local-first para memória, docs e código.
- Pesquisa segura em AndreOS/Obsidian local, docs, backend, desktop, android e materializações locais.
- Decisão `reuse-first` antes de criar código novo.
- Integra `CapabilityReuseService`, `MemoryContextRouterService` e `MemoryCoreService`.
- Sanitiza snippets e evita caminhos sensíveis.
- V1 não requer embeddings/vector DB; preparado para upgrade futuro.

### Segurança

- Não indexa ficheiros/paths sensíveis, dependências, builds ou caches.
- Snippets são redigidos quando há padrões sensíveis.
- `safe_for_external_ai=false` por defeito.
- V1 é local-first e não envia contexto para providers externos.

### PR e validação

- PR #312 merged.
- Merge commit: `18afcdfba8a0c4cd581288c291765cc31280371c`.
- Validações verdes antes do merge:
  - Phase 170 Local Knowledge RAG Smoke;
  - Phase 169 Memory Sync Runtime Smoke;
  - Phase 168 GitHub Approved Actions Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend;
  - Artifact Download Shortcuts Validation.

## 2026-05-04 — Phase 171

### Phase 171 — `Provider Outcome Learning`

Implementado no repo `AndreVazao/devops-god-mode`.

- Serviço: `backend/app/services/provider_outcome_learning_service.py`
- Rota: `backend/app/routes/provider_outcome_learning.py`
- Docs: `docs/orchestration/provider-outcome-learning.md`
- Smoke workflow: `.github/workflows/phase171-provider-outcome-learning-smoke.yml`
- Endpoints: `/api/provider-outcome-learning/*`

### Funcionalidade

- Regista outcomes sanitizados por provider IA.
- Cria scorecards por provider/task tag.
- Gera hints em modo `advisory_v1` para o AI Provider Router.
- Simula rota com ajustes aprendidos sem alterar pesos base automaticamente.
- Aprende sucesso/falha por tarefa, qualidade, latência, custo e rating do operador.

### Segurança

- Guarda apenas metadados sanitizados, nunca conteúdo bruto sensível.
- Bloqueia conteúdo sensível antes de gravar outcome.
- Não recomenda fallback para contornar safety/policy/operator gate.
- Providers externos continuam dependentes do AI Handoff Security Guard.

### PR e validação

- PR #313 merged.
- Merge commit: `1b555bd39343af54ed0e6077bc242f11808c365a`.
- Validações verdes antes do merge:
  - Phase 171 Provider Outcome Learning Smoke;
  - Phase 170 Local Knowledge RAG Smoke;
  - Phase 169 Memory Sync Runtime Smoke;
  - Phase 168 GitHub Approved Actions Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend;
  - Artifact Download Shortcuts Validation.

## 2026-05-04 — Phase 172

### Phase 172 — `Home/App Control Surface`

Implementado no repo `AndreVazao/devops-god-mode`.

- Serviço: `backend/app/services/home_app_control_surface_service.py`
- Rota: `backend/app/routes/home_app_control_surface.py`
- Docs: `docs/orchestration/home-app-control-surface.md`
- Smoke workflow: `.github/workflows/phase172-home-app-control-surface-smoke.yml`
- Endpoints: `/api/home-control-surface/*`

### Funcionalidade

- Cria uma superfície única para PC/APK renderizarem o cockpit do God Mode.
- Agrega módulos reais: Playbook Templates, Pipeline Store/Low-Risk Executor, Memory Sync Runtime, GitHub Approved Actions, Local RAG, Provider Outcome Learning e Histórico/Auditoria.
- Expõe manifesto de botões, módulos, mobile shell e desktop shell.
- Define contrato de botão com endpoint, método, risco, confirmação e payload padrão.
- PC/APK podem consumir `/api/home-control-surface/package` para renderizar o cockpit sem hardcode.

### Segurança

- Não expõe ações destrutivas diretas pela Home/App.
- Ações de maior risco continuam atrás dos gates próprios.
- Approved GitHub Actions mantém frase de aprovação e PR/checks.
- Memory Sync mantém dry-run por defeito.
- Provider Learning continua advisory.

### PR e validação

- PR #314 merged.
- Merge commit: `33cf9c5ab8caaed145327cfbcb8a7ef2e6e22461`.
- Validações verdes antes do merge:
  - Phase 172 Home App Control Surface Smoke;
  - Phase 171 Provider Outcome Learning Smoke;
  - Phase 170 Local Knowledge RAG Smoke;
  - Phase 169 Memory Sync Runtime Smoke;
  - Phase 168 GitHub Approved Actions Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend;
  - Artifact Download Shortcuts Validation.

## 2026-05-04 — Phase 173

### Phase 173 — `Home Visual Shell`

Implementado no repo `AndreVazao/devops-god-mode`.

- Serviço: `backend/app/services/home_visual_shell_service.py`
- Rota: `backend/app/routes/home_visual_shell.py`
- Docs: `docs/orchestration/home-visual-shell.md`
- Smoke workflow: `.github/workflows/phase173-home-visual-shell-smoke.yml`
- Endpoints: `/app/home`, `/api/home-visual-shell/*`

### Funcionalidade

- Cria UI visual real servida pelo backend em `/app/home`.
- A página consome `/api/home-control-surface/package`.
- Renderiza cards por módulo com semáforo.
- Renderiza botões reais vindos do backend.
- Suporta editor de payload para ações POST.
- Exige confirmação visual quando `requires_confirmation=true`.
- Layout responsivo para desktop, browser e APK/WebView.

### Segurança

- A página não inventa ações; renderiza apenas o manifesto do backend.
- Não expõe merge/release/delete direto.
- Gates server-side continuam nos módulos originais.
- Ações de maior risco continuam dependentes de confirmação/payload/frase/gate próprio.

### PR e validação

- PR #315 merged.
- Merge commit: `79d328d6481c60d97640728c1087309c59e94ff5`.
- Validações verdes antes do merge:
  - Phase 173 Home Visual Shell Smoke;
  - Phase 172 Home App Control Surface Smoke;
  - Phase 171 Provider Outcome Learning Smoke;
  - Phase 170 Local Knowledge RAG Smoke;
  - Phase 169 Memory Sync Runtime Smoke;
  - Phase 168 GitHub Approved Actions Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend;
  - Artifact Download Shortcuts Validation.

## 2026-05-04 — Phase 174

### Phase 174 — `Launcher/App Default Home Route`

Implementado no repo `AndreVazao/devops-god-mode`.

- Serviço: `backend/app/services/app_entrypoint_manifest_service.py`
- Rota: `backend/app/routes/app_entrypoint_manifest.py`
- Docs: `docs/orchestration/app-entrypoint-manifest.md`
- Smoke workflow: `.github/workflows/phase174-launcher-app-entrypoint-smoke.yml`
- Atualização de `backend/main.py` para expor a rota canónica.
- Endpoints: `/api/app-entrypoint/*`.

### Funcionalidade

- Formaliza `/app/home` como rota canónica para desktop/browser/APK-WebView.
- Expõe manifesto em `/api/app-entrypoint/manifest`.
- Adiciona redirects de compatibilidade para `/app`, `/desktop`, `/mobile`, `/home`, `/app/mobile` e `/app/apk-start`.
- Mantém compatibilidade com metadata antiga do Android que apontava para `/app/apk-start`.
- Confirma que desktop launcher e Android WebView usam `/app/home` internamente.

### Segurança

- Não adiciona ações destrutivas.
- Não altera gates de módulos.
- Home visual continua a renderizar ações vindas do backend.

### PR e validação

- PR #316 merged.
- Merge commit: `277d4c36023a34ea9ce1132df8fa29e1608526ef`.
- Validações verdes antes do merge:
  - Phase 174 Launcher App Entrypoint Smoke;
  - Phase 173 Home Visual Shell Smoke;
  - Phase 172 Home App Control Surface Smoke;
  - Phase 171 Provider Outcome Learning Smoke;
  - Phase 170 Local Knowledge RAG Smoke;
  - Phase 169 Memory Sync Runtime Smoke;
  - Phase 168 GitHub Approved Actions Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend;
  - Artifact Download Shortcuts Validation.
