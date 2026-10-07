# Contexto Persistente — DGM-MAT

## Identidade
DGM-MAT = Devops God Mode — Multi Agent Tool.

## Canonical
- Trabalho: C:\ProgramasGodMode\DGM-MAT
- FULL-MIRROR: C:\ProgramasGodMode\DGM-MAT-FULL-MIRROR — read-only
- OS-Memory: C:\AndreOS-Memory

## Arquitetura — checkpoint 2026-10-06

A decisão estrutural foi tomada: antes de qualquer movimento físico, mapear todas as interligações reais.

Mapa automático atual:
- 774 ficheiros Python
- 774 módulos
- 1.015 imports internos
- 15 diretórios DGM-MAT-* embutidos no repositório

Artefactos versionados no commit 46ed522:
- reports/DGM-MAT_INTERCONNECTION_MAP.md
- reports/dgm_mat_dependency_graph.json
- reports/DGM-MAT_REORGANIZATION_PLAN.md
- tools/generate_dependency_map.py

## Arquitetura-alvo preliminar

- DGM-Core-Backend: núcleo Python/backend; por princípio todo o core/ deve acabar aqui, salvo fronteira funcional comprovada.
- DGM-Cockpit-Frontend: cockpit e UI.
- DGM-Contracts: contratos, eventos, DTOs, schemas e modelos realmente partilhados.
- DGM-Docs: documentação permanente.
- DGM-MAT-Agents: agentes concretos/especializações.
- DGM-MAT-Runtime: runtime independente apenas se o mapa comprovar essa fronteira.
- DGM-MAT-Connectors: integrações externas.
- DGM-MAT-Providers: providers/adapters.
- DGM-MAT-Memory: integração de memória do produto; memória global permanece AndreOS/OS-Memory.
- DGM-MAT-Orchestrator: coordenação independente se comprovada.
- DGM-MAT-OS: integração/lifecycle do sistema operativo.
- restantes satélites serão classificados pelo conteúdo real.

## Regra de migração

MAPEAR -> CLASSIFICAR -> COPIAR/MIGRAR -> REESCREVER INTERLIGAÇÕES -> TESTAR -> COMMITAR -> VALIDAR -> só depois remover origem.

Nunca mover e apagar simultaneamente.

O nome de uma pasta/repo não decide o destino sozinho.

## Fronteiras desejadas

O Cockpit não deve importar ficheiros privados do Core.
Agentes não devem depender de caminhos físicos de outros repos.
Repos não devem usar caminhos absolutos para C:\ProgramasGodMode\DGM-MAT.
Comunicação cross-process deve usar contratos, APIs, eventos/queues ou storage como fonte de verdade.
Singletons em memória não podem ser a fonte de verdade entre processos.

## FULL-MIRROR

Intocável. É recuperação histórica e fonte de arqueologia, não um segundo projeto concorrente.

## Próximo trabalho

Fase M1: completar o mapa semântico:
- quem manda
- quem obedece
- quem cria
- quem aprova
- quem executa
- quem responde
- quem escreve
- quem lê
- quem persiste
- quem observa
- quem expõe API
- quem depende de quem

Depois classificar individualmente os ficheiros e construir uma matriz FILE -> REPO DESTINO -> DEPENDÊNCIAS -> REESCRITAS NECESSÁRIAS.

Só então começar a extração de core para DGM-Core-Backend, cockpit para DGM-Cockpit-Frontend e demais domínios.

## Sincronização

GitHub/local confirmado no commit 46ed522.
OS-Memory atualizado neste checkpoint.
Mem atualizado neste checkpoint.


## Auditoria de repositórios e file-level — checkpoint 2026-10-06

Concluída a auditoria factual dos repositórios locais sem qualquer migração física.

Artefacto novo:
- C:\\ProgramasGodMode\\DGM-MAT\\reports\\DGM-MAT_REPOSITORY_AUDIT_MATRIX.md
- GitHub commit: 3b3db7e6b17b1f99d34ec4dc7bcc4e53013dd690

Classificações confirmadas:
- DGM-MAT = host funcional atual / origem da migração.
- DGM-Core-Backend, DGM-Contracts, DGM-Cockpit-Frontend = shells/destinos.
- DGM-HUB = sistema real independente para arqueologia/reutilização, não cópia cega.
- DGM-MCP = servidor MCP real independente; integração futura por contrato.
- DGM-MAT-Labs e Lab-* = camada de experimentação/reutilização, sem autoridade de produção.
- DGM-MAT-FULL-MIRROR = arquivo de segurança intocável.

Auditoria file-level executada em core/shared/cockpit/scripts/tools/tests/legacy:
- 808 ficheiros Python analisados no conjunto auditado.
- core: 587; shared: 4; cockpit: 55; scripts: 29; tools: 7; tests: 78; legacy: 48.
- Artefactos: reports/DGM-MAT_FILE_LEVEL_OWNERSHIP_AUDIT.md e reports/dgm_mat_file_level_audit.json.
- Ferramenta: tools/audit_file_level.py.

Achados críticos:
1. shared.models.event.Event é consumido por Core, Cockpit e testes e é forte candidato a DGM-Contracts.
2. shared.config.settings depende diretamente de core.storage.storage_manager; shared não pode ser movido inteiro para Contracts sem separar schema/config pública da resolução de storage do Core.
3. Cockpit tem 13 importações diretas de Core; todas são rewrite obrigatório antes da extração.
4. MissionEngine regista callback privado no SafeActionQueue, mantendo acoplamento process-local; este continua a ser o principal risco cross-process já identificado.
5. runtime_api.py funciona atualmente como camada de orquestração e depende diretamente de múltiplos domínios Core; não deve ser tratado como API fina durante a migração.
6. EventBus mistura contrato/evento, persistência e streaming no mesmo fluxo; requer separação de fronteiras antes da extração.
7. Permanecem caminhos Windows hardcoded e defaults localhost no Cockpit; devem ser centralizados.
8. start_daemon.py é lifecycle/deployment e não deve ficar como responsabilidade de domínio do Core.

Próxima fase: aprofundar DGM-HUB/src e DGM-MCP/src, comparar símbolos/autoridades com DGM-MAT e transformar a auditoria file-level numa matriz final FILE -> DESTINATION -> REWRITE -> OWNER/AUTHORITY -> READ/WRITE -> API/QUEUE/PROCESS -> TEST. Nenhum movimento físico ainda.


## CHECKPOINT 2026-10-06 — clarification DGM-HUB / DGM-MCP
- User clarified that the original purpose of DGM-HUB is no longer remembered; treat DGM-HUB strictly as LEGACY/RESEARCH/REUSE SOURCE until evidence proves otherwise. Do not make it a DGM-MAT dependency or authority.
- User clearly remembers DGM-MCP as the system created to let an AI/tool operate on the PC. Audit confirms this role: MCP protocol + ToolAdapter/ToolRegistry + guarded filesystem, command, PowerShell, Git/repository and test tools.
- New architecture decision: DGM-MCP is the historical/specialized PC-control + MCP integration boundary; public tool contracts belong in DGM-Contracts; execution/security belong behind DGM-MAT controlled boundaries; MCP must not own mission/autonomy/memory/orchestration state.
- New document: reports/DGM-HUB_DGM-MCP_ROLE_DECISION.md
- GitHub commit: 5662518 — docs(architecture): clarify HUB and MCP roles
- No physical migration performed. DGM-MAT-FULL-MIRROR remains untouched.
