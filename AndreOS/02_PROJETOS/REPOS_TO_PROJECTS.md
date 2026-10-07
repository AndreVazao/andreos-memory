# Mapa Canónico — Repositórios → Projetos

**Checkpoint:** 2026-10-07 — auditoria profunda local + GitHub

A memória agrupa repos por **produto/projeto lógico**, não por nome de repo.

## 1. DGM-MAT — `AndreOS/02_PROJETOS/DGM-MAT/`

Repos que formam o ecossistema:
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

Relacionados mas separados:
- DGM-MCP → DGM-MCP/
- DGM-HUB → DGM-HUB/

## 2. Baribudos

### BARIBUDOS_STUDIO/
- baribudos-studio
- baribudos-studio-home-edition
- baribudos-studio-primary

### BARIBUDOS_STUDIO_WEBSITE/
- baribudos-studio-website

Ecossistema/identidade:
- BARIBUDOS/

## 3. Build Control Center — `BUILD_CONTROL_CENTER/`
- build-control-center
- build-control-panel
- universal-build-platform

## 4. AI DevOps Tooling — `AI_DEVOPS_TOOLING/`
Ferramentas relacionadas com organização, governance, agentes e operação DevOps; relacionadas com DGM-MAT mas não absorvidas pelo Core:
- ai-devops-control-center
- Jules-Multi-Agent-Devops
- Project-Organizer-AI
- NeuroStack-OS
- GitHub-auto-builder

## 5. n8n — `N8N/`
- n8n
- awesome-n8n-templates
- n8n-free-templates
- n8n-skills
- n8n-workflows
- n8nworkflows.xyz

## 6. VAZÃO EVSE — `VAZAO-EVSE/`
- VAZAO-EVSE-Platform

Inclui Chargers, TestStation, CPMS/App, controlo, pagamentos e documentação.

## 7. ProVentil — `PROVENTIL/`
- proventil

## 8. ECU Repro — `ECU_REPRO/`
- ecu-pro-tune

## 9. VAZÃO Sovereign Trader — `VAZAO_SOVEREIGN_TRADER/`
- VazaoSovereignTrader

Domínio financeiro independente do VAZÃO EVSE.

## 10. TruckFood — `TRUCKFOOD/`
- TruckFood

Produto independente de inteligência de viagem para camionistas.

## 11. Bot Factory — `BOT_FACTORY/`
- Bot_Factory

Projeto independente de criação/orquestração de bots.

## 12. VORTEXA — `VORTEXA/`
- Vortexa-core

Infraestrutura local para personagens digitais, vozes, áudio e vídeo. Próxima tematicamente de Baribudos, mas separada até decisão de integração.

## 13. VocalClaw — `VOCALCLAW/`
- VocalClaw_11Labs

Projeto independente de Voice AI multi-agent.

## 14. RuView — `RUVIEW/`
- RuView

Projeto independente de sensing WiFi/CSI e spatial intelligence.

## 15. SyntX-26 — `SYNTX_26/`
- SyntX-26-AI-hackathon

Arquivo/projeto de hackathon educacional AI; não tratar como produto ativo sem decisão de continuidade.

## 16. AI / LLM

### Ollama — `OLLAMA/`
- Lab-OllamaConection (Lab)
- material local de Ollama

### AirLLM — `AIRLLM/`
- airllm-plus
- airllm-server

### RabbitLLM — `RABBITLLM/`
- RabbitLLM

### gpt4free — referência AI/LLM
- gpt4free

Estado: software externo/referência de multi-provider; não assumir propriedade arquitetural nem dependência de produção.

## 17. Labs

Repos explicitamente Labs:
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

Política: LAB → AUDIT → VALIDATE → REFACTOR → PROMOTE → TEST → PRODUCTION.

## 18. Upstream / software externo mantido localmente

Estes repositórios não devem ser tratados como projetos de produto próprios apenas por estarem em C:\ProgramasGodMode:

- FreeCAD — upstream FreeCAD
- Ghost — upstream Ghost
- freqtrade — upstream Freqtrade

Podem servir como fonte de código, teste ou referência, mas não entram automaticamente na arquitetura AndreOS.

## 19. Ferramentas/utilitários ainda sem projeto lógico confirmado

- ENV-editor
- script-reviewer-mobile
- SheetProPrivate

Devem permanecer independentes até auditoria funcional suficiente.

## 20. Repositórios ainda insuficientemente identificados

- ProjectFlux

Não criar agrupamento por adivinhação. Auditar conteúdo antes de classificar.

## 21. Regras de classificação

1. Nome da repo não é prova de pertença.
2. Conteúdo + origem + dependências + finalidade determinam o agrupamento.
3. Software externo/upstream fica separado de produto próprio.
4. Ferramentas relacionadas podem ter memória própria sem serem incorporadas ao DGM-MAT.
5. Labs nunca são produção por defeito.
6. Uma fusão física só acontece depois de mapear imports, contratos, testes e histórico.
7. FULL-MIRROR é arquivo de segurança e fica fora deste processo.

Fluxo:
**MAPEAR → AUDITAR CONTEÚDO → IDENTIFICAR PRODUTO → CLASSIFICAR → CRIAR MEMÓRIA → VALIDAR → SÓ DEPOIS MIGRAR/FUNDIR.**

## 22. Fonte de memória

Local canónico:
`C:\AndreOS-Memory`

GitHub:
`AndreVazao/andreos-memory`

`andreos-memory` é infraestrutura de memória, não produto em 02_PROJETOS.
