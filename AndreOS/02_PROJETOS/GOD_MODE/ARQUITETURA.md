# Arquitetura - God Mode

## Modelo operacional oficial

```txt
PC de casa = cérebro principal / backend poderoso
Telemóvel = cockpit principal / comandos e aprovações na rua
PC browser/launcher = cockpit secundário quando o operador está em casa
```

A rota canónica do cockpit visual é:

```txt
/app/home
```

Manifestos principais:

```txt
/api/app-entrypoint/manifest
/api/home-control-surface/package
/api/god-mode-global-state/package
```

## Componentes principais implementados

### Core de orquestração

- Goal Planner Core;
- Agent Roles Registry;
- AI Handoff Security Guard;
- AI Provider Router;
- MCP Compatibility Map;
- Real Orchestration Pipeline v1;
- Orchestration Playbooks v1;
- Execution Modes Engine v1;
- Playbook Templates Library.

### Execução e GitHub

- Pipeline Persistence + Low-Risk Executor v1;
- GitHub Approved Actions Executor;
- Repo/File Patch Hub;
- GitHub Actions como gates de validação;
- Android APK Build;
- Windows EXE Build com boot smoke desktop backend.

### Memória e conhecimento

- Memory Sync Runtime;
- GitHub Memory Sync;
- Local Knowledge/RAG Decision v1;
- Provider Outcome Learning;
- AndreOS GitHub memory para memória técnica estável;
- Obsidian/local para oficina viva local.

### Cockpit

- Home/App Control Surface;
- Home Visual Shell;
- Launcher/App Default Home Route;
- `/app/home` para desktop, browser e APK/WebView.

### Estado global

- God Mode Global State Service;
- `/api/god-mode-global-state/package` como snapshot runtime para saber o que existe, como operar e o que falta.

## Fluxo de pedido complexo

```txt
Pedido do André
→ Memory lookup / Global State / Local RAG
→ Goal Planner
→ Agent Roles
→ AI Handoff Security Guard
→ AI Provider Router
→ MCP Compatibility Map
→ Real Orchestration Pipeline
→ Execution Gates
→ Safe Action Queue / Low-Risk Executor / GitHub Approved Actions
→ GitHub Actions validation
→ PR / artifact / cockpit update
→ Memory Sync Runtime
→ AndreOS GitHub memory
```

## Regras de segurança

- Ações destrutivas exigem aprovação explícita do Oner.
- Merge, release, pagamentos, licenças e credenciais exigem gate explícito.
- O God Mode pode preparar PRs, builds e propostas de update, mas não deve fazer merge/release/update final sem aprovação.
- Segredos não entram em GitHub, README, docs ou AndreOS memory.
- Providers externos não recebem segredos no contexto.
- Vault real deve ser local, cifrado e controlado pelo PC com aprovação mobile.

## Memória

### GitHub AndreOS Memory

Guarda:

- decisões técnicas;
- arquitetura;
- histórico;
- backlog;
- última sessão;
- prompts estáveis.

Não guarda:

- tokens;
- passwords;
- cookies;
- API keys;
- chaves privadas;
- dados privados de clientes;
- runtime secrets.

### Obsidian/local

Guarda:

- rascunhos;
- oficina viva;
- notas de trabalho local;
- contexto operacional privado;
- evolução local que ainda não é decisão técnica estável.

## Auto-atualização

Estado atual: roadmap de alta prioridade.

Já existe base para:

- criar branch/ficheiros/PR;
- validar com GitHub Actions;
- gerar artifacts Windows/Android;
- incluir helper de update desktop;
- registar fases merged na memória.

Falta:

- Self-Update Orchestrator;
- update channel manifest;
- staged update no PC;
- rollback;
- aprovação mobile antes de aplicar;
- política de release/update segura.
