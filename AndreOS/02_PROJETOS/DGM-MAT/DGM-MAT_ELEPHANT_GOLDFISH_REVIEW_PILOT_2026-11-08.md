# DGM-MAT — adoção seletiva Elephant-Goldfish Model (EGM)

**Data:** 2026-11-08  
**Estado:** método estudado; primeiro contrato read-only proposto em PR; nenhuma revisão independente operacional ainda.

## Referência upstream

- Projeto: https://github.com/google/elephant-goldfish-model
- Modelo: Elephant mantém contexto e prepara a especificação; Goldfish recebe a especificação/fontes sem a conversa anterior e procura pressupostos omitidos, riscos e falhas; o proprietário decide.
- Licença declarada pelo upstream: Apache-2.0.
- Decisão: aproveitar metodologia e conceitos seletivamente, sem importar o plugin completo nem criar segundo motor de tarefas.

## PRs DGM-MAT

### PR #286 — documentação da adoção
- https://github.com/AndreVazao/DGM-MAT/pull/286
- Branch: `feat/egm-independent-design-review-2026-11-08`
- Commit documental: `de2d57ef8c35d6a2dd20d2ffab558352c025f656`
- Estado observado: aberta, não merged; mergeable=true na última consulta.
- Documento: `docs/architecture/DGM-MAT-SELECTIVE-ADOPTION-ELEPHANT-GOLDFISH-MODEL-2026-11-08.md`.
- Decisão arquitetural: reutilizar MissionEngine/OrganizationTaskManager/recibos existentes; aplicar revisão completa a mudanças arquiteturais/de alto risco; tarefas triviais mantêm fluxo leve.

### PR #287 — contrato read-only piloto 1
- https://github.com/AndreVazao/DGM-MAT/pull/287
- Branch: `feat/egm-review-packet-contract-2026-11-08`
- Último head observado: `58f77409f3af697a4091e6d512d87a7d06e0dac2`
- Estado observado: aberta, não merged; GitHub reportou mergeable=false temporariamente; compare com main indicou 6 commits ahead, 0 behind e três ficheiros novos.
- Ficheiros:
  - `core/organization/design_review.py`
  - `tests/organization/test_design_review.py`
  - `docs/architecture/EGM_REVIEW_PACKET_PILOT_1_2026-11-08.md`
- Contrato inclui DesignBrief limitado, ReviewerPacket específico, ReviewFinding tipificado, ReviewerResult com context ID, criação de 2–5 revisores únicos e verificação de resultados.
- Segurança: contexto do autor, cadeia de pensamento, recomendações do autor, resultados de outros revisores e segredos estão excluídos do pacote.
- Independência é fail-closed: distinct context IDs sem atestação explícita do runtime resultam em `independent=false`; IDs repetidos nunca passam.
- Não instancia sessões, chama fornecedores, despacha tarefas, persiste resultados, altera API/APK/dashboard ou autoriza execução.
- Não cria nova fila/base de dados; futura integração deve usar MissionEngine, OrganizationTaskManager e recibos existentes.

## Validação observada

- O código e os testes foram revistos via GitHub.
- Um smoke test isolado da lógica de contrato executado num ambiente Python temporário produziu 8 testes aprovados; não equivale a execução da suite do repositório nem a CI GitHub.
- No último estado consultado, os status checks do commit #287 estavam vazios e o workflow-run lookup não devolveu execuções. Não declarar CI verde.
- Snyk não foi confirmado como aprovado nesta PR.
- Nenhum merge executado.

## Próxima fase

1. Resolver/confirmar estado mergeable e obter execução CI real para PR #287.
2. Validar a suite exata do repositório, não apenas o smoke test.
3. Só depois desenhar adapter de sessões novas/isoladas para especialistas reais.
4. O adapter deve provar isolamento no runtime, limitar permissões a read-only e nunca entregar credenciais.
5. Guardar brief, findings e resultados como recibos duráveis ligados a task_id/mission_id existentes.
6. Fazer piloto em mudança de baixo risco; dashboard apenas apresenta estado verificado.
7. Não chamar uma revisão de independente sem atestação real do runtime.
8. Não ativar flags, não criar motor paralelo, não interferir com prioridade backend/APK/dashboard e não fazer merge sem validação.

## Princípios

Estabilidade > funcionalidades; evidência > suposição; revisão independente verdadeira > simulação de independência; autoridade humana para alterações estruturais; preservar proveniência e histórico.
