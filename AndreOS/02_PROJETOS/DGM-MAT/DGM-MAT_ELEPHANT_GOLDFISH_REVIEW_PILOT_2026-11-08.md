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


## PR #289 — fresh browser review preflight (2026-11-08 21:22 UTC)

- PR: https://github.com/AndreVazao/DGM-MAT/pull/289
- Branch: `feat/egm-browser-fresh-review-preflight-2026-11-08`
- Head: `f60713fc90158cf5658f3721cd9a8762bdc62f3f`
- Base: `recovery/legacy-branch-consolidation-2026-11-07` (PR #283 branch); PR open, not merged, mergeable=true.
- Changes:
  - `browser_extension/content.js`: extension-only `DGM_FRESH_REVIEW_PING` and `DGM_EXECUTE_FRESH_REVIEW`.
  - Preflight requires allowlisted provider, non-blocked page, no recognized conversation ID, no visible prior user/assistant messages and visible composer.
  - A one-shot nonce binds execution to same provider and exact tab URL; checks repeat immediately before sending.
  - Prompt limited to 8,000 chars; success requires a newly observed provider conversation ID and stable assistant response.
  - Test `tests/browser_extension/test_fresh_review_context.js` covers ChatGPT, Gemini, Grok, DeepSeek, Qwen and rejection cases.
  - Chrome Extension Validation workflow includes the new test; README states scope/limits.
- CI Chrome Extension Validation run `42524840946`: **SUCCESS**, all 15 steps, including JS syntax, existing browser fixtures, fresh-review fixture, API/security regressions, Bandit, pip-audit and extension packaging.
- Artifact `DGM-MAT-Chrome-Conversation-Recovery`, ID `13634832357`, 24,304 bytes; ZIP SHA-256 `511b19eb51912256b9b0b3426bdc76b24856d9a6b002a889fa81adccdada3878`; expires 2026-11-22 21:22:18 UTC.
- A workflow update on the PR #283 base branch added its recovery branch to the pull_request base filter, so stacked PR #289 can run Chrome Extension Validation. PR #283 focused/windows/extension workflows also started again on branch head `9201a9a560b3099d6a46bd02cab44c98356f9609`; results pending at last check.

### Limitações ainda abertas

- PR #289 is only a browser content-script protocol. It is **not** wired to BrowserConsultStore, the popup approval queue, or DesignReviewCoordinator.
- The response deliberately keeps `independence_attested=false`: visible blank page → new conversation ID is UI-observed evidence, not cryptographic proof that the provider has no hidden account-side context.
- It does not yet implement durable asynchronous start/resume or persist the review evidence in the DGM task receipt.
- No live Windows/Chrome acceptance on the five providers yet. Do not merge or enable it as operational EGM.
- Next: design a durable start/resume bridge that reuses BrowserConsultStore's approval lifecycle, records each provider's preflight/new conversation evidence and response, then validates/persists the final reviewer results via the existing OrganizationTaskManager receipt. Do not block a synchronous worker while waiting for manual approval.


## Atualização privacy-mode e CI final do código PR #289 — 2026-11-08 21:25 UTC

- Head documental atual: `f6a2b425790f42f0cf9dba97d17b341041ec37b9`.
- Head de código validado: `359f0e4389c14f9f1905dcd44145d146934f346d`.
- Chrome Extension Validation run `42525073264`: **SUCCESS**, 15/15 steps. O teste fresh-review passa apenas para ChatGPT e Gemini com o modo temporário adequado; Grok, DeepSeek e Qwen falham fechados. Sintaxe, fixtures de histórico, segurança de envio, browser operator, manifest, regressões API, Bandit, pip-audit e empacotamento passaram.
- Artifact atualizado: `DGM-MAT-Chrome-Conversation-Recovery`, ID `13634792968`, 24,847 bytes, ZIP SHA-256 `7836922c04a7b9e226d7a8787dcfb85a6333a431e5ea4fcc9d0c82286b439355`, expira 2026-11-22 21:25:04 UTC.
- Commit posterior `f6a2b425790f42f0cf9dba97d17b341041ec37b9` acrescenta fontes oficiais no README; run documental `42525107249` estava queued.
- Fontes oficiais usadas para política de privacidade:
  - OpenAI Help Center: Temporary Chat Unpersonalized não usa Memory, custom instructions ou plugins; contexto de segurança limitado pode continuar a ser usado: https://help.openai.com/en/articles/8914046-temporary-chat-in-chatgpt
  - Google: Gemini Temporary Chat não aparece no histórico/Activity e não é usado para personalização nem treino: https://blog.google/products-and-platforms/products/gemini/temporary-chats-privacy-controls/
  - xAI: Grok Private Chat esconde do histórico e remove em até 30 dias, mas o controlo separado `Personalize Grok using X` não é verificado pelo adapter: https://x.ai/legal/faq
  - DeepSeek privacy policy não define modo temporary/isolated: https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html
  - Qwen API stateless não prova comportamento da UI web; sem modo temporary UI oficialmente verificado.
- A implementação só aceita ChatGPT Temporary Chat + Unpersonalized e Gemini Temporary Chat. Grok/DeepSeek/Qwen não são elegíveis para este adapter enquanto não existir prova UI verificável.
- Ainda mantém `independence_attested=false`; protocolo não está ligado à fila, aprovação popup ou coordinator. Sem aceitação real Windows/Chrome. Sem merge.
