# DGM-MAT — adoção seletiva Elephant-Goldfish Model (EGM)

**Data:** 2026-11-08  
**Estado:** contrato e coordenador host-runtime implementados em PRs empilhadas; CI do piloto 2 em execução; nenhum adapter real de fornecedor ainda.

## Referência upstream

- Projeto: https://github.com/google/elephant-goldfish-model
- Modelo: Elephant mantém contexto e prepara a especificação; Goldfish recebe a especificação/fontes sem a conversa anterior e procura pressupostos omitidos, riscos e falhas; o proprietário decide.
- Licença declarada pelo upstream: Apache-2.0.
- Decisão: aproveitar metodologia e conceitos seletivamente, sem importar o plugin completo nem criar segundo motor de tarefas.

## PRs DGM-MAT

### PR #286 — documentação da adoção
- https://github.com/AndreVazao/DGM-MAT/pull/286
- Branch: `feat/egm-independent-design-review-2026-11-08`
- Documento: `docs/architecture/DGM-MAT-SELECTIVE-ADOPTION-ELEPHANT-GOLDFISH-MODEL-2026-11-08.md`.
- Decisão arquitetural: reutilizar MissionEngine/OrganizationTaskManager/recibos existentes; aplicar revisão completa a mudanças arquiteturais/de alto risco; tarefas triviais mantêm fluxo leve.

### PR #287 — contrato read-only piloto 1
- https://github.com/AndreVazao/DGM-MAT/pull/287
- Branch: `feat/egm-review-packet-contract-2026-11-08`
- Head: `58f77409f3af697a4091e6d512d87a7d06e0dac2`
- Estado observado: aberta, não merged.
- Ficheiros: `core/organization/design_review.py`, `tests/organization/test_design_review.py`, `docs/architecture/EGM_REVIEW_PACKET_PILOT_1_2026-11-08.md`.
- Contrato inclui DesignBrief limitado, ReviewerPacket específico, ReviewFinding tipificado, ReviewerResult com context ID, criação de 2–5 revisores únicos e verificação de resultados.
- Independência é fail-closed: distinct context IDs sem atestação explícita do runtime resultam em `independent=false`; IDs repetidos nunca passam.
- Não instancia sessões nem chama fornecedores.

### PR #288 — coordenador host-runtime piloto 2
- https://github.com/AndreVazao/DGM-MAT/pull/288
- Branch: `feat/egm-runtime-review-coordinator-2026-11-08`
- Base: branch da PR #287 (PR empilhada para manter o diff isolado).
- Head: `7d2d12b020efa2ea74068baa3564a37238b74652`
- Estado observado: aberta, não merged; mergeable=false temporariamente enquanto CI calcula.
- Ficheiros adicionais:
  - `core/organization/design_review_coordinator.py`
  - `core/organization/task_manager.py` — propriedade `durable_persistence_enabled`
  - `tests/organization/test_design_review_coordinator.py`
  - `docs/architecture/EGM_HOST_RUNTIME_COORDINATOR_PILOT_2_2026-11-08.md`
- O coordenador exige tarefa RUNNING atribuída a `agent:design-review-coordinator`, `task_kind=independent_design_review`, brief ligado ao task_id/mission_id e persistência SQLite.
- Cria todas as sessões antes de chamar qualquer revisor; cada sessão recebe apenas o seu próprio pacote; outputs não são partilhados.
- Exige atestação do host runtime: sessão fresca, histórico anterior excluído, sem partilha entre revisores, tools e escrita desativadas, credenciais excluídas, context IDs distintos.
- Resultados e atestações são gravados no recibo existente através de `OrganizationTaskManager.complete_with_result`. Sem nova DB/fila.
- Falhas não produzem recibo de sucesso; a tarefa fica RUNNING para inspeção.
- Não aprova nem executa alterações.

## Validação observada em 2026-11-08

- PR #287 Focused PR Validation run `42516345669`: **SUCCESS**.
- PR #287 Windows Executable Build run `42516345831`: **IN PROGRESS** na última consulta.
- PR #288 Focused PR Validation run `42516803853`: **IN PROGRESS**; compilação Python passou, regressões selecionadas ainda em instalação de dependências.
- PR #288 Windows Executable Build run `42516803755`: **IN PROGRESS**.
- Smoke test isolado anterior: 8 testes da lógica de contrato aprovados; não substitui CI nem a suite exata.
- Não foi observado resultado Snyk limpo.
- Nenhum merge executado.

## Limitações e gates seguintes

1. A PR #288 fornece protocolo e coordenador, não um adapter concreto ChatGPT/Claude/Gemini/browser.
2. A atestação é contrato para código host-owned; não é prova criptográfica contra adapter malicioso e nunca pode vir do texto gerado pelo modelo.
3. O próximo passo exige implementar adapter num runtime real que crie conversas novas, sem histórico e sem ferramentas, e validar o comportamento com testes de integração.
4. Ligar o adapter apenas após confirmação de fornecedor gratuito/permitido, sem quota paga nem fallback de cobrança.
5. Fazer primeiro um piloto read-only de baixo risco; depois registar findings e recibos no dashboard.
6. Não ativar flags, não criar motor paralelo, não interferir com backend/APK/dashboard e não fazer merge sem validação e autorização aplicável.

## Princípios

Estabilidade > funcionalidades; evidência > suposição; revisão independente verdadeira > simulação de independência; autoridade humana para alterações estruturais; preservar proveniência e histórico.
