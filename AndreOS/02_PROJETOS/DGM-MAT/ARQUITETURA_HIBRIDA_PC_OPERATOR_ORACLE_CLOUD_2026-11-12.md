# DGM-MAT — arquitetura híbrida PC Operator + Oracle Cloud Always Free
Data: 2026-11-12

## Decisão arquitetural recomendada

**Adotar arquitetura híbrida, sem migrar já o DGM-MAT inteiro para a cloud e sem provisionar recursos Oracle nesta fase.**

Separar responsabilidades:

1. **Control plane / serviços sempre disponíveis (cloud):** coordenação remota, API autenticada, DGM-HUB, sincronização de estado não sensível, filas e agendamentos leves.
2. **PC Operator / execution plane (PC Windows):** interação com desktop, aplicações instaladas, PowerShell/CMD, processos, serviços, instalação/desinstalação, PATH, diagnóstico e reparação.
3. **DGM-MCP:** interface/porta de ferramentas entre o cérebro e os executores. O DGM-MCP por si só não concede acesso ao PC remoto; é necessário um agente/bridge local no Windows, iniciado pelo operador, autenticado e com política de permissões.
4. **AndreOS Memory/Vault:** evidência persistente, auditoria, provenance e dossiers de projetos; sincronizar apenas dados aprovados e minimizados.

## Oracle Cloud Always Free — capacidade discutida

Em conversas de 2026-11-07, o operador identificou como referência:
- Oracle Ampere A1 ARM64: 2 OCPUs agregadas e 12 GB RAM.
- Block Volume: 200 GB totais, incluindo volume de boot (não vários TB).
- Egress: até 10 TB/mês, sujeito às condições/cotas Oracle.
- Alternativa AMD: até duas E2.1.Micro, cada uma com 1/8 OCPU e 1 GB RAM.
- Apenas Always Free/recursos elegíveis. Zero upgrades pagos, zero custos; confirmar sempre a elegibilidade e limites reais.
- Não provisionar, alterar tenancy, criar VM, rede, volumes ou serviços sem autorização explícita do operador. Nunca pedir nem partilhar credenciais.

Disponibilidade de capacidade Ampere pode variar por região e pode não ser garantida. ARM64 requer verificar compatibilidade das imagens, wheels, containers e binários.

## O que a cloud consegue e não consegue fazer

- A cloud pode executar o backend/coordenação do DGM-MAT, Hub, APIs e serviços leves se a arquitetura e dependências suportarem ARM64.
- A cloud não consegue controlar diretamente o desktop Windows, os programas instalados, os discos locais, CMD/PowerShell ou serviços do PC só por ter DGM-MCP instalado nela.
- Para controlar o PC, é obrigatório um executor local Windows (DGM-MCP local ou bridge/agent), ligado de forma segura ao control plane, com identidade do dispositivo, autenticação mútua, comunicação de saída iniciada pelo PC, allowlists, timeouts, logs e kill switch.
- Nunca expor PowerShell, CMD, RDP ou um MCP executor privilegiado diretamente à Internet.
- A execução deve ser local, visível e governada por policy/approval. Cloud envia uma tarefa tipada; agente local valida policy e executa; recibo com stdout/stderr redigidos, exit code e postconditions regressa ao Vault.
- Quando a cloud perde ligação, o PC mantém controlo local e nenhuma fila remota deve executar operações privilegiadas sem validação fresca.

## Recomendação de colocação

### Agora
- Manter DGM-MAT local como runtime principal de desenvolvimento/testes enquanto o PC está offline ou instável.
- Continuar a evolução GitHub-first: conhecimento de projetos/conversas, Vault, dossier por projeto e PC Operator com testes mockados.
- Desenhar o DGM-MCP como gateway/control plane e definir contrato do executor Windows, mas não ativar acesso remoto privilegiado nem provisionar OCI.
- A Oracle free tier pode ser considerada mais tarde para serviços de coordenação sempre ligados, se os requisitos e quotas reais forem confirmados e o operador autorizar.

### Quando existir PC novo
- Usar o PC novo como execution host principal para desktop automation, aplicações, shell e diagnóstico.
- O runtime local beneficia de CPU/RAM/SSD melhores e mantém baixa latência para GUI e ferramentas instaladas.
- Cloud continua opcional para disponibilidade, coordenação e sincronização; não é requisito para o operador local funcionar.

### VST e outros projetos
- OCI Always Free poderá servir para ambientes de desenvolvimento, APIs leves, dashboard, backtest/simulação ou paper trading do VazaoSovereignTrader, depois de avaliar ARM64, persistência, limites de CPU, disponibilidade, segurança e dados.
- Não assumir que 2 OCPU/12 GB e capacidade Always Free são suficientes para trading real 24/7, execução sensível a latência ou infraestrutura financeira crítica.
- Para VST, começar por workload não crítico e fail-safe; não colocar execução de ordens reais na cloud free sem arquitetura de risco, monitorização, reconciliação, limites e recuperação testados.
- A cloud também pode ser útil para DGM-HUB/serviços de escritório e APIs leves. A decisão por projeto deve ser baseada em workload, não em usar a VM só porque existe.

## Sequência de implementação

1. Inventário read-only do Windows host e software instalado.
2. Contrato tipado DGM-MCP ↔ executor Windows, com identidade de dispositivo e capabilities declaradas.
3. Executor local com operações read-only e recibos duráveis.
4. PowerShell/CMD com timeouts, working directory, captura de resultados e policy.
5. PATH/environment repair backup-first.
6. UI automation visível e interrompível.
7. Software lifecycle planner/executor com approval explícita.
8. Só depois avaliar deployment cloud do control plane, sem mover dados sensíveis sem política de sincronização.

## Guardrails obrigatórios
- Zero custos: não sair de Always Free nem ativar recursos faturáveis.
- Nenhum provisionamento Oracle sem autorização explícita.
- Nenhum segredo, token, cookie, password ou credencial em GitHub/Memory/logs.
- Não expor shell remoto diretamente à Internet.
- Menor privilégio; operações privilegiadas/disruptivas exigem aprovação vinculada ao plano exato.
- Backup antes de alterações; pós-condições verificadas; rollback disponível.
- Evidência e estado real separados de hipóteses.
- PC local continua capaz de operar sem cloud; cloud indisponível não pode bloquear recuperação local.

## Estado de implementação em 2026-11-12
- PR #361 (auditoria estática read-only dos projetos) integrada na main por squash: merge commit `5bd2b77ed6a369e45a215e6b9d89f0b5edcfa506`. Focused Validation #983 e Windows Executable Build #610 SUCCESS.
- Issue #362 criada: https://github.com/AndreVazao/DGM-MAT/issues/362 — operador Windows geral, desktop, shell, software lifecycle, PATH e diagnóstico/reverse engineering defensivo.
- PC do operador desligado na sessão atual; não houve validação real local nem contacto real aos providers.
- Issue #244 já define Intelligent Installer/host capability management e deve ser reutilizada, sem duplicar inventários ou catálogo de ferramentas.
- Nenhum servidor Oracle foi criado/provisionado. Esta documentação é decisão arquitetural, não autorização de provisionamento.


## Primeiro incremento de implementação — inventário de software — 2026-11-12

- Inspeção da main confirmou que já existe um executor governado read-only em `core/operations/command_executor.py`, com catálogo allowlist, `shell=False`, timeout, limite de output, roots autorizadas e rota API auditada antes/depois da execução em `core/api/governance_api.py`.
- PR #363 integrada na main por squash: https://github.com/AndreVazao/DGM-MAT/pull/363.
- Merge commit: `b6c3d08a21f4c0b6bc2f8ceb3cf91698c5a9fda2`; HEAD validado antes do merge: `8f3705a1a355f4e82ce32b96a75627ddeb4c7f29`.
- Focused PR Validation run `43189805712`: regressões afetadas SUCCESS; Windows installer digest gate SUCCESS.
- Windows Executable Build run `43189805683`: build Python 3.12, deep executable validation, assertions e upload de artifacts SUCCESS.
- Adiciona `software.inventory`: leitura read-only das chaves standard de uninstall HKLM 64-bit, HKLM WOW6432Node e HKCU; devolve apenas nome, versão, publisher e data de instalação; limite de 150 entradas; não devolve uninstall commands, install paths ou registry paths; não usa `Win32_Product`.
- Testes e documentação atualizados. A CI valida compilação, regressões afetadas, digest gate e build do executável; não substitui teste no PC Windows real.
- Nenhuma execução real no PC: continua offline. A inventory slice está integrada no código, mas a aceitação operacional Windows aguarda o PC voltar a estar ligado.

## Decisão de colocação atualizada — 2026-11-12

- O PC atual mantém-se como ambiente principal de execução e desenvolvimento enquanto estiver disponível; continuar GitHub-first durante períodos em que esteja desligado.
- O PC novo será a evolução futura do execution host local, mas não é pré-requisito para continuar a desenvolver o DGM-MAT.
- O VazaoSovereignTrader (VST) fica destinado a uma eventual cloud numa fase posterior, até provar valor e existir PC novo. Não antecipar migração nem provisionamento.
- A cloud fica reservada para depois e só será avaliada quando houver necessidade concreta. Nenhum recurso Oracle será provisionado sem autorização explícita; não assumir custos nem upgrades.
- Esta decisão substitui qualquer leitura anterior que sugerisse usar já OCI para VST, DGM-HUB ou serviços de coordenação.


## Segundo incremento do PC Operator — diagnóstico read-only do PATH — 2026-11-12

- PR #364 aberta: https://github.com/AndreVazao/DGM-MAT/pull/364.
- Branch: `feat/read-only-path-diagnostics-v1`.
- HEAD: `f87b2c7db421b6f8da3f8d685a5b12f30e761ea3`.
- Adiciona `environment.path_diagnostics` ao executor existente: leitura de PATH Machine, User e Process; até 120 entradas; scope, índice, texto do caminho, existência da pasta e duplicados.
- Não altera variáveis de ambiente, registo, ficheiros ou permissões. Sem elevação, instalação, remoção ou restart. A reparação continuará separada, com backup, diff e aprovação explícita.
- Focused Validation run `43190881578`: em execução no último check; regressões ainda na instalação de dependências e digest gate em checkout/post-checkout.
- Windows Executable Build run `43190881713`: em execução no último check.
- Snyk reportou limite mensal de testes privados atingido. Ignorado como gate, conforme decisão explícita do operador; não é apresentado como teste aprovado.
- Não fazer merge antes de ambos os workflows relevantes terminarem com sucesso e o HEAD ser novamente confirmado.
- PC continua offline; nenhuma validação real Windows ou alteração de PATH foi efetuada.


## Atualização GitHub-first antes da atualização do PC — 2026-11-12

O operador confirmou que o PC está ligado, mas pediu para preservar a quota mensal limitada do Desktop Commander: concluir o máximo de trabalho possível no GitHub antes de qualquer sessão remota no PC, para depois atualizar a instalação local de uma só vez.

### PRs integradas

- PR #364 — diagnóstico read-only do PATH: merge `dd860f3cd2a85f239e7285c5d51d472ed0002851`. Focused regressions, Windows installer digest gate e Windows Executable Build SUCCESS. Snyk bloqueado pela quota privada mensal; ignorado conforme decisão do operador.
- PR #365 — inventário read-only de serviços Windows: merge `4608af06c9238da9bc9ff42032470b5d5300bddf`. Focused regressions, Windows installer digest gate e Windows Executable Build SUCCESS.
- PR #366 — primeira projeção consultável de dossier por projeto a partir do Vault: merge `0b0316b36f9049bc2dda174d04fda268308f594e`. Inclui identidade do projeto, conversas atribuídas agrupadas por provider/completude, referências de evidência, snapshots de repositório, auditoria estática, referências GitHub extraídas das conversas e fingerprints de artefactos de código. Endpoint `GET /runtime/repository-learning/dossier?project_id=...`, scope operator. Não devolve corpos de conversas nem código extraído. Não infere completude dos providers, decisões do operador, branch/commit atual, runtime ou testes. Focused PR Validation, Windows installer digest gate, Windows Executable Build, Chrome Extension Validation e Mission E2E Regression Gate SUCCESS. O primeiro focused run falhou por teste a esperar `tree_fingerprint` no retorno do método; corrigido para o campo real `fingerprint` e a nova execução passou.

### PR em preparação para a instalação

- PR #367 — https://github.com/AndreVazao/DGM-MAT/pull/367, branch `fix/windows-updater-preserve-vault-v1`.
- Adiciona backup explícito do Vault em `%LOCALAPPDATA%\DGM-MAT\Vault`, sem o mover nem apagar.
- Adiciona lançador de duplo clique `Install-DGM-MAT-Update.bat`, wrapper PowerShell com UAC, leitura do checksum interno do executável, validação de sintaxe PowerShell no workflow, inclusão do launcher e guia PT-PT no ZIP.
- O ZIP continua a ter de ser verificado contra o ficheiro .zip.sha256 independente antes de executar o launcher. O updater existente pede shutdown gracioso, confirma o dono do porto 8181, nunca mata processos, faz backup do executável/launcher/dados e deixa o runtime parado.
- HEAD atual: `9027b82bf697fd5133efff0f95afabcdcd76a7d5`. Windows build em fila/execução no último check; não fazer merge antes de focused validation, parser PowerShell e Windows build passarem.
- Nenhuma desinstalação ou atualização real foi feita no PC.

### Procedimento local quando o pacote estiver pronto

- Não desinstalar manualmente nem apagar a versão atual primeiro. Usar o updater governado de substituição in-place, que mantém o Vault e os dados locais e possui rollback.
- Fechar o cockpit, descarregar o ZIP e checksum do artefacto Windows da execução bem-sucedida, verificar o checksum externo, extrair para pasta separada e executar `Install-DGM-MAT-Update.bat`.
- Após atualização: iniciar o DGM-MAT, validar health, autenticação, cockpit, Vault e fluxos principais. Não declarar aceite apenas com base no build CI.
- O Desktop Commander deve ser usado apenas na sessão local final, minimizando chamadas remotas e agrupando inventário, atualização e E2E.
