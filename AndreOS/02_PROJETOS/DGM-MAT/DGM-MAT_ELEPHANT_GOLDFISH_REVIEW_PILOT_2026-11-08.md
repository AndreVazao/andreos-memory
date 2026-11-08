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
- Head: `73c32159ff777b88a65fecc3f16f9fb80cb7397e`
- Estado observado: aberta, não merged; mergeable=true na última consulta.
- Ficheiros adicionais:
  - `core/organization/design_review_coordinator.py`
  - `core/organization/task_manager.py` — propriedade `durable_persistence_enabled`
  - `tests/organization/test_design_review_coordinator.py`
  - `docs/architecture/EGM_HOST_RUNTIME_COORDINATOR_PILOT_2_2026-11-08.md`
- O coordenador exige tarefa RUNNING atribuída a `agent:design-review-coordinator`, `task_kind=independent_design_review`, brief ligado ao task_id/mission_id e persistência SQLite.
- A documentação da PR #288 foi complementada com auditoria concreta do browser adapter: o código da PR #283 exige `source_id` existente e opera em conversas já abertas; não cria contexto novo. Além disso, a aprovação manual e conclusão assíncrona da fila não encaixam diretamente no coordenador síncrono. É necessário protocolo fresh-review e workflow durável start/resume.
- Cria todas as sessões antes de chamar qualquer revisor; cada sessão recebe apenas o seu próprio pacote; outputs não são partilhados.
- Exige atestação do host runtime: sessão fresca, histórico anterior excluído, sem partilha entre revisores, tools e escrita desativadas, credenciais excluídas, context IDs distintos.
- Resultados e atestações são gravados no recibo existente através de `OrganizationTaskManager.complete_with_result`. Sem nova DB/fila.
- Falhas não produzem recibo de sucesso; a tarefa fica RUNNING para inspeção.
- Não aprova nem executa alterações.

## Validação observada em 2026-11-08

- PR #287 Focused PR Validation run `42516345669`: **SUCCESS**.
- PR #287 Windows Executable Build run `42516345831`: **IN PROGRESS** na última consulta.
- PR #288 Focused PR Validation run `42516803853`: **SUCCESS**; compilação Python, seleção e execução das regressões afetadas e Windows installer digest gate passaram.
- PR #288 Windows Executable Build run `42516803755`: **SUCCESS**; executável e artefactos publicados. Um commit documental posterior atualizou a auditoria do adapter browser e vai disparar nova validação.
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



## Auditoria complementar da consulta por browser — 2026-11-08 21:15 UTC

- Windows Executable Build da PR #287, run `42516345831`: **SUCCESS**.
- Windows Executable Build da PR #288, run `42516803755`: **SUCCESS**. A PR #288 mantém-se aberta, não merged e mergeable=true.
- Os corpos das PRs #287 e #288 foram atualizados com os resultados finais. Focused CI e Windows build estão verdes; Snyk não está confirmado como aprovado.

### Bloqueio encontrado antes do adapter EGM real

Inspeção do código da PR #283, branch `recovery/legacy-branch-consolidation-2026-11-07`:

- `browser_extension/background.js` faz polling das consultas por browser usando tabs de fornecedor já abertas e o estado atual do separador.
- O content script `browser_extension/content.js` implementa `DGM_EXECUTE_BROWSER_TASK` exigindo `source_id` de uma conversa existente e confirma que o separador continua nessa conversa antes de enviar.
- `sendMessageThroughVisibleUi` recusa páginas sem um identificador de conversa reconhecido: “Open an existing conversation before sending.”
- Portanto, o fluxo atual consulta conversas existentes. **Não cria nem comprova uma conversa nova/fresca**, pelo que não pode servir como adapter Goldfish independente sem alteração.
- O README da extensão descreve principalmente recuperação de conversas; o comportamento real de consulta foi acrescentado posteriormente. A extensão usa UI visível, aprovação manual e não usa API paga, mas isso não prova isolamento de contexto.
- Não reutilizar o endpoint atual como prova de fresh-session. Não aceitar context IDs fabricados a partir de IDs de provider sem verificação do estado inicial.
- Próximo desenvolvimento correto: protocolo separado de fresh-review, com pré-condição verificável de página nova sem mensagens/histórico visível, contexto por separador/revisor, envio apenas após aprovação individual e confirmação de que o provider criou um novo ID de conversa; rejeitar páginas que já estejam numa conversa existente. Criar testes DOM para os cinco providers e validação real Windows/Chrome antes de atestar.
- Até esse trabalho estar concluído, o coordenador EGM fica sem adapter real; não ativar flags nem marcar Goldfish operacional.

## Princípios

Estabilidade > funcionalidades; evidência > suposição; revisão independente verdadeira > simulação de independência; autoridade humana para alterações estruturais; preservar proveniência e histórico.
