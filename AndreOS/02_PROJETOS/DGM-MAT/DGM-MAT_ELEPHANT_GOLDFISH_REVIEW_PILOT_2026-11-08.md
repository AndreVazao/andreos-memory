# DGM-MAT — adoção seletiva Elephant-Goldfish Model (EGM)

**Data:** 2026-11-08  
**Estado:** contrato read-only implementado em PR; Focused PR Validation verde; Windows build em curso; revisão independente ainda não operacional.

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
- Head: `58f77409f3af697a4091e6d512d87a7d06e0dac2`
- Estado observado: aberta, não merged; mergeable=true na última consulta.
- Compare: 6 commits ahead, 0 behind; 3 ficheiros novos.
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

- Focused PR Validation run `42516345669`: **SUCCESS**. Compilação Python, seleção e execução das regressões afetadas e Windows installer digest gate passaram.
- Windows Executable Build run `42516345831`: **IN PROGRESS** na última consulta, em instalação de dependências.
- Um smoke test isolado da lógica de contrato executado num ambiente Python temporário produziu 8 testes aprovados; não equivale à suite do repositório nem substitui CI.
- Não foi observado resultado Snyk limpo nesta PR.
- Nenhum merge executado.

## Próxima fase

1. Aguardar Windows build e confirmar artefacto/resultado.
2. Confirmar se existem outros checks exigidos para PR #287.
3. Validar a suite exata do repositório, não apenas o smoke test.
4. Só depois desenhar adapter de sessões novas/isoladas para especialistas reais.
5. O adapter deve provar isolamento no runtime, limitar permissões a read-only e nunca entregar credenciais.
6. Guardar brief, findings e resultados como recibos duráveis ligados a task_id/mission_id existentes.
7. Fazer piloto em mudança de baixo risco; dashboard apenas apresenta estado verificado.
8. Não chamar uma revisão de independente sem atestação real do runtime.
9. Não ativar flags, não criar motor paralelo, não interferir com prioridade backend/APK/dashboard e não fazer merge sem validação.

## Princípios

Estabilidade > funcionalidades; evidência > suposição; revisão independente verdadeira > simulação de independência; autoridade humana para alterações estruturais; preservar proveniência e histórico.
