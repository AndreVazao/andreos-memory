# DEVOPS / BUILD / ORCHESTRATION — AUDITORIA FASE 1
Data: 2026-10-08

## Conclusão
Não existe evidência suficiente para tratar todos os repos como um único projeto. Existem pelo menos duas famílias distintas: BUILD CONTROL e AUTONOMOUS ENGINEERING. Há ainda repos fora dessas famílias.

## Matriz
| REPO | TIPO | FINALIDADE | RELAÇÃO | DECISÃO |
|---|---|---|---|---|
| ai-devops-control-center | CORE-PRODUCT candidato | Control plane PWA: discovery, governance, GitHub sync, health, workflow planning | Forte overlap com Build Control e DGM-MAT | Manter separado; candidato atual da família Build Control |
| build-control-center | LEGACY / PRODUCT | Dashboard: repos, builds, workflow trigger, artefactos | Mesma família funcional do panel | Manter como geração histórica |
| build-control-panel | LEGACY / TOOL | Next.js: needs-build, status, build, webhook | Família Build Control | Manter como geração anterior |
| GitHub-auto-builder | TOOL | Android: clipboard de IA → FILE → validação → commit GitHub | Satélite mobile DevOps | Manter separado |
| Jules-Multi-Agent-Devops | LEGACY / EXPERIMENT | Multi-agent engineering center, FastAPI, cockpit, missions, cluster, autonomy | Forte overlap DGM-MAT/ProjectFlux | Congelar como reuse source |
| universal-build-platform | UNKNOWN / SUBPROJECT | Builders + PersonaForge + project2 | Conteúdo não corresponde a control plane | Separar; auditar PersonaForge |
| Project-Organizer-AI | EXPERIMENT / TOOL | Frontend estático para APIs, credenciais, conversas e projetos | Conceito de organização | Manter separado |
| ProjectFlux | LEGACY / EXPERIMENT | PyQt6 + FastAPI, watchdog, agents, swarm, GitHub, sync, memory, self-evolution | Forte overlap DGM-MAT/Jules | Congelar como reuse source |

## Genealogia funcional Build Control
build-control-panel começou em fevereiro de 2026. build-control-center surgiu em março e ampliou o painel para builds, workflows e artefactos. ai-devops-control-center também surgiu em março e acrescentou discovery, policy, governance, GitHub sync, health scoring, workflow planning e PWA/Android.

Hipótese funcional:
BUILD CONTROL PANEL → BUILD CONTROL CENTER → AI DEVOPS CONTROL CENTER

Isto é genealogia funcional, não ancestry Git comprovada.

## Autonomous Engineering
Jules-Multi-Agent-Devops tem root em 2026-05-08; ProjectFlux em 2026-05-16. Ambos possuem agentes, orquestração, cluster, Git/GitHub, memória, execução e automação, mas os roots são diferentes. Classificar como arquiteturas paralelas/gerações sobrepostas, não como clone confirmado.

## DGM-HUB / DGM-MCP / DGM-MAT
DGM-HUB é um runtime autónomo de execução/debugging com Task → RuntimeSession → TaskExecutor → WorkflowRuntime → UnifiedToolManager → TestPipeline → History, além de segurança, approvals e MCP bridge.

DGM-MCP especializa o transporte/protocolo e tooling MCP: STDIO/SSE/HTTP, registry, Git/FS/shell/patch/repo tools, PathGuard e AuditLogger.

DGM-MAT é a autoridade atual, com Contracts, Agents/Connectors boundaries, Providers extraction gate, Event Bus, Execution Fabric, Mission Engine, Cognition, Runtime, Cockpit e Governance.

Decisão:
DGM-MAT = CURRENT AUTHORITY
DGM-HUB = LEGACY / RESEARCH / REUSE SOURCE
DGM-MCP = SPECIALIZED PROTOCOL / TOOL SATELLITE

Não importar sistemas em bloco.

## NeuroStack-OS
Iniciado em 2026-05-18. Ollama, multi-agent, plugins, RAM scheduler, dashboard, systemd e Tailscale. O código real é simples e orientado a Linux. Há referências a ollama, jules, godmode e mad. Classificação: EXPERIMENT / LEGACY / REUSE SOURCE. Forte overlap conceptual com DGM-MAT, sem ancestry comprovada.

## Universal Build Platform
O conteúdo real contém builders e um projeto grande PersonaForge, com animation/audio/characters/render/lipsync/storytelling/YouTube/SEO/monetization. Não corresponde a um universal DevOps control plane. Manter separado e comparar depois com Vortexa-core e Baribudos Studio.

## Project-Organizer-AI
É essencialmente frontend estático com tabs para APIs, credenciais, conversas, projetos e explorer. EXPERIMENT / TOOL.

## Regras de integridade
Nenhum código de produto foi alterado. Nenhum repo foi movido, apagado ou renomeado. Nenhum workflow foi disparado. DGM-MAT-FULL-MIRROR não foi tocado. A memória LEGACY não foi usada.

## Próximo lote
universal-build-platform + PersonaForge → Vortexa-core → Baribudos Studio/Baribudos → restantes UNKNOWN.

Antes de qualquer migração: comparar código, dependências, imports e histórico.
