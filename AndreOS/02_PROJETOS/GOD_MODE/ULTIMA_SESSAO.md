# Última Sessão - God Mode

## Data
2026-05-05

## Resumo

A Phase 187 foi implementada, validada e merged. Esta fase adiciona o Conversation Requirement Ledger, uma camada para o God Mode distinguir pedidos do Oner, respostas/propostas das IAs, decisões aceites, scripts extraídos, migrações de arquitetura e evidência real de implementação.

Esta fase responde diretamente à necessidade crítica do Oner: o God Mode tem de ler conversas de várias IAs, diferenciar pedidos do Oner das respostas das IAs, sacar scripts, entender contexto, preservar pedidos antigos e comparar o que foi pedido com o que foi decidido/implementado. Se o projeto mudou de direção, por exemplo de cloud/Supabase/Render/Vercel para PC brain + mobile cockpit, a migração fica registada sem apagar pedidos antigos.

## Phase 187 — Conversation Requirement Ledger + Request/Decision Reconciliation

### Implementado

- Serviço: `backend/app/services/conversation_requirement_ledger_service.py`
- Rota: `backend/app/routes/conversation_requirement_ledger.py`
- Docs: `docs/orchestration/conversation-requirement-ledger.md`
- Smoke workflow atual: `.github/workflows/phase187-conversation-requirement-ledger-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase186-provider-env-writers-dry-run-smoke.yml`

### Endpoints novos

- `/api/conversation-requirement-ledger/status`
- `/api/conversation-requirement-ledger/policy`
- `/api/conversation-requirement-ledger/analyze-text`
- `/api/conversation-requirement-ledger/analyze-messages`
- `/api/conversation-requirement-ledger/compare-project`
- `/api/conversation-requirement-ledger/open-requirements`
- `/api/conversation-requirement-ledger/realness-scorecard`
- `/api/conversation-requirement-ledger/package`

### Funcionalidade

- Analisa texto/transcrições de conversas.
- Separa `operator_request` vs `ai_response`.
- Extrai pedidos, decisões, scripts/code blocks e migrações.
- Detecta direção cloud → PC/local.
- Compara pedidos com decisões/evidência.
- Lista requisitos em aberto.
- Gera realness scorecard.
- Regra: resposta da IA é proposta até ser confirmada/implementada/validada.

### Regras críticas registadas

- Pedido do Oner é a fonte da intenção.
- Resposta de IA é proposta até ser confirmada, implementada e validada.
- Mudança de direção não apaga pedidos antigos.
- Migrações ficam registadas, por exemplo cloud/Supabase/Render/Vercel para PC brain + mobile cockpit.
- Feature só é marcada como real quando há evidência:
  - endpoint;
  - código;
  - PR;
  - merge;
  - GitHub Actions;
  - smoke/build;
  - proof local.

### Segurança / realidade

- Não guarda segredos crus.
- Scripts extraídos exigem reconciliation antes de aplicar.
- Feature só é marcada como real com endpoint/código/PR/merge/CI/build/proof local.
- Pedidos antigos não são apagados silenciosamente quando a arquitetura muda.

### PR e validação

- PR #330 merged.
- Merge commit: `065f9c92531932ca94626f4c18eae9a0de2a9ff4`.
- Validações verdes antes do merge:
  - Phase 187 Conversation Requirement Ledger Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend.

## Workflows atuais após limpeza

Ficam esperados:

- `.github/workflows/phase187-conversation-requirement-ledger-smoke.yml`
- `.github/workflows/universal-total-test.yml`
- `.github/workflows/android-real-build-progressive.yml`
- `.github/workflows/windows-exe-real-build.yml`
- `.github/workflows/prune-old-artifacts-all-repos.yml`
- `.github/workflows/project-tree-autorefresh.yml`

## Estado atual

O God Mode tem agora:

- PC de casa como cérebro principal;
- telemóvel como cockpit principal;
- PC cockpit secundário;
- `/app/home` como cockpit visual canónico;
- Home/App Control Surface;
- Home Visual Shell;
- Cockpit Runtime UX;
- Operator Action Journal;
- GitHub Approved Actions Executor;
- Memory Sync Runtime;
- Local Knowledge/RAG Decision;
- Provider Outcome Learning;
- God Mode Global State;
- Project Tree Autorefresh com `GOD_MODE_TREE.md`;
- Module Registry Snapshot;
- Reality Audit + First Real Install Mission;
- PC Provider Conversation Proof;
- First Install PC Proof Center;
- Local Encrypted Vault Contract;
- Lab Best-Of Work Ally;
- Real Local Encrypted Vault;
- Vault Deployment Binding;
- Provider Env Writers Dry-Run;
- Conversation Requirement Ledger;
- vários módulos manuais de mobile/approval/autopilot/self-update no main.

## Próxima ação recomendada

Próxima fase recomendada: **Phase 188 — Conversation Ledger Cockpit Cards + Open Requirements Review**.

Objetivos:

- adicionar cards no cockpit para requisitos abertos;
- mostrar pedido original, resposta IA ligada, decisão ligada e evidência real;
- permitir marcar requisito como confirmado, obsoleto, migrado ou ainda em aberto;
- ligar provider proof imports ao ledger;
- manter phase smoke único e apagar o smoke da Phase 187.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar `docs/project-tree/GOD_MODE_TREE.md`, consultar `/api/module-registry-snapshot/search` antes de criar módulos novos, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
