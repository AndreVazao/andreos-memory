# Decisões - God Mode

## 2026-04-30
Decidido que o God Mode usará o AndreOS Memory Core como memória persistente externa, versionada no GitHub e legível no Obsidian.

## 2026-04-30
Decidido que ações perigosas exigem aprovação explícita antes de execução.

## 2026-05-03
Decidido que Ruflo e Praison são laboratórios externos controlados, não dependências centrais do God Mode.

## 2026-05-03
Decidido que o God Mode terá arquitetura nativa própria para:

- Goal Planner;
- Agent Roles;
- AI Handoff Security Guard;
- AI Provider Router;
- MCP Compatibility Map;
- Real Orchestration Pipeline;
- Orchestration Playbooks.

## 2026-05-03
Decidido que todo pedido complexo deve seguir o pipeline:

```txt
Pedido do André
→ Goal Planner
→ Agent Roles
→ AI Handoff Security Guard
→ AI Provider Router
→ MCP Compatibility Map
→ Execution Gates
→ Safe Action Queue
```

## 2026-05-03
Decidido que GitHub memory guarda memória técnica estável e Obsidian local guarda oficina/evolução local. Notas maduras do Obsidian devem ser promovidas para GitHub memory quando virarem decisão técnica.

## 2026-05-03
Decidido que playbooks JSON/YAML-like serão usados como receitas reutilizáveis do God Mode para criar pipelines reais sem depender sempre de chat longo.

## 2026-05-04
Decidido que o GitHub Approved Actions Executor da Phase 168 pode preparar branch, escrever ficheiros aprovados, criar commits e abrir PR, mas nunca pode fazer merge, release, delete, force push, alterações de credenciais, pagamentos ou licenças. Merge continua condicionado a GitHub Actions verdes e aprovação explícita do Oner.

## 2026-05-04
Decidido que o Memory Sync Runtime da Phase 169 separa GitHub memory estável de Obsidian/local: GitHub memory recebe apenas decisões, histórico, arquitetura, backlog e última sessão técnica; Obsidian/local fica como oficina/rascunho/trabalho vivo; programas cloud não dependem do Obsidian; qualquer conteúdo sensível é bloqueado antes de package/sync.

## 2026-05-04
Decidido que a Phase 170 impõe regra `reuse-first`: antes de criar código novo, o God Mode deve pesquisar AndreOS/Obsidian local, docs, backend, desktop, android e materializações locais através do Local Knowledge/RAG Decision v1. O índice v1 é lexical/local-first, não envia contexto para providers externos, sanitiza snippets e mantém `safe_for_external_ai=false` por defeito.

## 2026-05-04
Decidido que a Phase 171 usa aprendizagem de outcomes dos providers apenas em modo advisory: gera scorecards e hints para o AI Provider Router, mas não altera pesos base automaticamente. A aprendizagem não pode recomendar fallback para contornar segurança, política ou aprovação do Oner, e guarda apenas metadados sanitizados.

## 2026-05-04
Decidido que a Phase 172 cria a Home/App Control Surface como agregador backend oficial para PC/APK. O endpoint `/api/home-control-surface/package` passa a ser o contrato principal para renderizar cockpit, módulos e botões reais. A Home/App não executa ações destrutivas diretamente; cada botão mantém risco, confirmação e gate próprio.

## 2026-05-04
Decidido que a Phase 173 cria a Home Visual Shell servida pelo backend em `/app/home`. Esta passa a ser a UI visual real para browser/desktop/APK-WebView, consumindo `/api/home-control-surface/package` em vez de hardcode local. A página renderiza apenas ações vindas do backend e mantém os gates server-side dos módulos originais.

## 2026-05-04
Decidido que a Phase 174 formaliza `/app/home` como rota canónica para desktop launcher, browser e APK/WebView. `/api/app-entrypoint/manifest` passa a ser o contrato oficial de entrypoint. Rotas antigas como `/app/apk-start`, `/app`, `/desktop`, `/mobile`, `/home` e `/app/mobile` ficam como redirects de compatibilidade para `/app/home`.
