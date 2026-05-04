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
Decidido que o Memory Sync Runtime da Phase 169 separa GitHub memory estável de Obsidian/local: GitHub memory recebe apenas decisões, histórico, arquitetura, backlog e última sessão técnica; Obsidian/local fica como oficina/rascunho/trabalho vivo; programas cloud não dependem do Obsidian; qualquer conteúdo com tokens, passwords, cookies, API keys, private keys, access/refresh tokens ou dumps locais é bloqueado antes de package/sync.
