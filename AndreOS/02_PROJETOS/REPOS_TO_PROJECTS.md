# Mapa Canónico — Repositórios → Projetos

**Checkpoint:** 2026-10-07

Esta tabela define o agrupamento lógico das repos GitHub na memória persistente AndreOS.

A regra é: **uma pasta de memória por projeto lógico**, não necessariamente uma pasta por repo.

## 1. DGM-MAT — AndreOS/02_PROJETOS/DGM-MAT/

Repos que formam o ecossistema DGM-MAT:

- DGM-MAT
- DGM-MAT-Agents
- DGM-MAT-Assets
- DGM-MAT-Cluster
- DGM-MAT-Connectors
- DGM-MAT-Deploy
- DGM-MAT-Labs
- DGM-MAT-Marketplace
- DGM-MAT-Media
- DGM-MAT-Memory
- DGM-MAT-Mobile
- DGM-MAT-Orchestrator
- DGM-MAT-OS
- DGM-MAT-Plugins
- DGM-MAT-Providers
- DGM-MAT-Runtime
- DGM-MAT-Studio
- DGM-Cockpit-Frontend
- DGM-Contracts
- DGM-Core-Backend
- DGM-Docs
- DGM-Experimental

Sistemas relacionados, mas com memória própria:
- DGM-MCP → DGM-MCP/
- DGM-HUB → DGM-HUB/

DGM-MCP e DGM-HUB são projetos independentes/referenciais, embora possam integrar ou influenciar a arquitetura DGM-MAT.

## 2. Baribudos

- baribudos-studio → BARIBUDOS_STUDIO/
- baribudos-studio-home-edition → BARIBUDOS_STUDIO/
- baribudos-studio-primary → BARIBUDOS_STUDIO/
- baribudos-studio-website → BARIBUDOS_STUDIO_WEBSITE/

A memória de marca/ecossistema permanece em BARIBUDOS/.

## 3. Build Control Center — BUILD_CONTROL_CENTER/

- build-control-center
- build-control-panel

## 4. n8n — N8N/

- n8n
- awesome-n8n-templates
- n8n-free-templates
- n8n-skills
- n8n-workflows
- n8nworkflows.xyz

## 5. VAZÃO EVSE — VAZAO-EVSE/

- VAZAO-EVSE-Platform

A memória abrange toda a plataforma, incluindo Chargers, TestStation, CPMS/App, controlo, pagamentos e documentação.

## 6. ProVentil — PROVENTIL/

- proventil

## 7. ECU Repro — ECU_REPRO/

- ecu-pro-tune

## 8. God Mode / DevOps legacy — GOD_MODE/

- devops-god-mode

Manter separado do DGM-MAT moderno até a arquitetura determinar uma integração real.

## 9. AI / LLM

### Ollama — OLLAMA/
- Lab-OllamaConection (Lab)
- material local de Ollama já arquivado na memória

### AirLLM
Repos:
- airllm-plus
- airllm-server

Estado: candidato a novo projeto lógico AIRLLM, a consolidar depois de auditoria de conteúdo.

### RabbitLLM
- RabbitLLM

Estado: projeto independente; memória própria deve ser criada quando o conteúdo for auditado.

## 10. Labs

Repos explicitamente classificadas como Labs:
- godmode-android-skills-lab
- godmode-anthropic-skills-lab
- godmode-awesome-copilot-lab
- godmode-browser-act-skills-lab
- godmode-cloudflare-skills-lab
- godmode-gemini-skills-lab
- godmode-google-cloud-skills-lab
- godmode-heygen-skills-lab
- godmode-lords-mobile-lab
- godmode-openai-skills-lab
- godmode-praison-lab
- godmode-ruflo-lab
- godmode-smol-ai-lab
- godmode-vercel-skills-cli-lab
- Lab-forge-icons
- Lab-ionicons.designerpack
- Lab-OllamaConection

Labs não devem ser tratados como produção apenas por existirem no GitHub.

## 11. Projetos independentes ainda por classificar

Não receberão agrupamento inventado antes de auditoria:
- ai-devops-control-center
- Bot_Factory
- ENV-editor
- FreeCAD
- freqtrade
- Ghost
- GitHub-auto-builder
- Jules-Multi-Agent-Devops
- NeuroStack-OS
- ProjectFlux
- Project-Organizer-AI
- RuView
- script-reviewer-mobile
- SheetProPrivate
- SyntX-26-AI-hackathon
- TruckFood
- universal-build-platform
- VazaoSovereignTrader
- VocalClaw_11Labs
- Vortexa-core

## 12. Regra de classificação futura

Não criar uma pasta de memória só porque existe uma repo.

Primeiro:

MAPEAR → AUDITAR CONTEÚDO → IDENTIFICAR PRODUTO/PROJETO → AGRUPAR OU SEPARAR → CRIAR MEMÓRIA → REGISTAR NO MAPA.

Assim evitamos transformar a memória num espelho caótico do GitHub.

## 13. Repositório de memória

A repo andreos-memory é infraestrutura de memória, não um projeto de produto em 02_PROJETOS.

Fonte canónica local:
C:\AndreOS-Memory

Fonte GitHub:
AndreVazao/andreos-memory
