# Backlog - God Mode

## Prioridade Alta

### Phase 177 — Main Tree Reconciliation + Module Registry Snapshot

- Ler/registrar a árvore real atual do `main`.
- Criar snapshot técnico de módulos existentes por categoria.
- Evitar duplicar serviços já existentes.
- Atualizar README/docs se necessário com a árvore real.
- Melhorar `/api/god-mode-global-state/package` para reconhecer módulos manuais existentes.
- Confirmar HEAD real de `main` antes de criar branch.

### Phase 178 — Local Encrypted Vault Contract

- Definir storage local cifrado no PC.
- Guardar apenas referências/labels no GitHub/AndreOS.
- Aprovação mobile para unlock/uso de segredo.
- Logs redigidos com secret IDs, nunca valores.
- Política de rotação/revogação.

### Phase 179 — Self-Update Orchestrator

- Detectar mudanças aceites para o próprio God Mode.
- Preparar branch/PR via GitHub Approved Actions.
- Validar GitHub Actions.
- Gerar update manifest.
- Staged update no PC.
- Rollback local obrigatório.
- Aprovação mobile antes de aplicar.

### Phase 180 — Mobile Operator Flow

- Cockpit pensado para uso real na rua/trabalho/condução.
- Aprovações grandes, rápidas e seguras.
- Resumo curto do que o PC está a fazer.
- Próxima ação recomendada.
- Modo voice-first futuro.

## Concluído recentemente

### Phase 176 — Cockpit Runtime UX + Execution Logs

- Polling package em `/api/cockpit-runtime-ux/package`.
- Logs por botão via `/api/cockpit-runtime-ux/log-button-event`.
- Histórico visível via `/api/cockpit-runtime-ux/history`.
- Cards compactos via `/api/cockpit-runtime-ux/quick-history-cards`.
- Reaproveitamento do `OperatorActionJournalService`.
- Não executa ações privilegiadas diretamente.

## Prioridade Média

- RAG local avançado com embeddings/vector DB.
- Provider/browser/platform control registry.
- Melhorar playbooks de automação.
- Modo multi-provider com aprendizagem mais robusta.
- Painel de agentes com estado operacional.
- Integração MCP real quando fizer sentido.

## Prioridade Baixa

- Voice-first completo.
- Agentes autónomos especializados mais profundos.
- UI avançada com preferências visuais.
- Otimização mobile/APK.

## Sempre obrigatório

- Consultar AndreOS memory antes de continuar GOD_MODE.
- Confirmar HEAD real de `main` antes de criar branch, especialmente se houver commits manuais.
- Atualizar AndreOS memory após fases merged, commits manuais relevantes ou decisões técnicas importantes.
- Manter README alinhado com arquitetura real.
- Validar com GitHub Actions antes de merge.
- Não guardar tokens, passwords, cookies, API keys ou segredos em GitHub/README/docs/memória.
- Não fazer merge/release/update final/pagamentos/licenças/credenciais sem aprovação explícita do Oner.
