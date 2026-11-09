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


### Correção de artefacto/documentação PR #289 — 21:26 UTC
- Head PR #289 atual: `f6a2b425790f42f0cf9dba97d17b341041ec37b9`.
- Run de código #42525073264 SUCCESS; run documental #42525107249 SUCCESS.
- Artefacto mais recente (head documental): ID `13635490035`, 25,511 bytes, ZIP SHA-256 `020848e430ad9d7dbd9f8e821ed36bd776fe92e669f15159f45daca4daa18fcd`, expira 2026-11-22 21:25:28 UTC.
- PR #289 mantém-se aberta, não merged, mergeable=true na última consulta.
- PR #283 Windows Executable Build #42524832858: SUCCESS; Chrome Extension Validation #42524832854: SUCCESS; Focused PR Validation #42524832862 foi CANCELLED (as validações focadas anteriores da PR #283 continuam documentadas como verdes). Nenhum merge.


## PR #289 — ponte durável EGM fresh-review (2026-11-09)

- PR: https://github.com/AndreVazao/DGM-MAT/pull/289
- Branch: `feat/egm-browser-fresh-review-preflight-2026-11-08`
- Head atual após documentação adicional: `3e9dcde3b7da6b424e1dda481ab75d0e142ef4f7`; PR aberta, não merged, mergeable=true na última leitura.
- Implementação adicionada:
  - Migração aditiva da tabela SQLite existente `browser_consultations`: `review_mode`, `review_id`, `evidence_json`; sem segunda fila/base de dados.
  - API `POST /recovery/browser-consult/enqueue` aceita `review_mode=fresh_review`, exige `review_id`, free-capacity attestation e apenas ChatGPT/Gemini.
  - `GET /recovery/browser-consult/peek` não altera estado nem consome claim; só expõe itens já aprovados. Se a privacy UI não está pronta, pedido fica PENDING sem cooldown.
  - Claim continua one-shot e usa o token existente.
  - Resultado fresh só conclui com evidência validada: provider correspondente, privacy mode específico, source ID novo, source ID inicial vazio e zero mensagens iniciais.
  - `GET /recovery/browser-consult/fresh-review/{review_id}` retoma a revisão persistida com respostas e evidência, marcadas não confiáveis.
  - Security inventory classifica peek e resume com scope restrito `browser-capture`.
  - Background extension escolhe o preflight pelo modo da consulta, sem claim antes do preflight.
- Privacy gate exige estado ativo/checked explícito, não apenas labels:
  - ChatGPT: `chatgpt_temporary_unpersonalized`.
  - Gemini: `gemini_temporary_chat`.
  - Grok/DeepSeek/Qwen: bloqueados.
- Testes de extensão, store e API cobrem privacidade ativa/inativa, providers bloqueados, aprovação, peek não-mutável, claim, persistência, evidência e resume.
- Documento de arquitetura: `docs/architecture/EGM_BROWSER_FRESH_REVIEW_DURABLE_BRIDGE_2026-11-09.md`.
- Chrome Extension Validation #42570101916: **SUCCESS**, 15/15 steps; syntax JS, fixtures, manifest, pip-audit, Bandit, regressões API/store e package passaram.
- Artefacto Chrome: `DGM-MAT-Chrome-Conversation-Recovery`, ID `13652128932`, 26,954 bytes, ZIP SHA-256 `bbbc17560d4e04060605da5ccc20c4b916275e9475e7e53c994a36c8d7aaa688`, expira 2026-11-23 05:56:42 UTC.
- Windows Executable Build #42570202406 foi iniciado no head `6037ca152c3b522117bf6d1f724ec4dae2b9f4f7`; resultado ainda pendente na última consulta. O último commit `3e9dcde...` só acrescentou docstring de segurança ao endpoint.
- Limite crítico: UI evidence continua `result_trusted=false` e `independence_attested=false`. Não construir `RuntimeIsolationAttestation` com base nestes dados; falta verifier host-side que liga task/mission/reviewer e persiste recibo através do OrganizationTaskManager.
- Sem aceitação live Windows/Chrome em contas reais; sem flags ligadas; sem merge.


### PR #289 — validação completa Chrome + Focused (2026-11-09 06:00 UTC)
- Head validado: `591a38ab2f679643c8e41d7cd74b101877a5c9f8`; PR aberta, não merged, mergeable=true.
- Chrome Extension Validation #42570380817: **SUCCESS**, 15/15 steps.
- Focused PR Validation #42570380872: **SUCCESS**; compilação Python, regressões afetadas e Windows installer digest gate.
- Artefacto Chrome ID `13653231240`, 27,045 bytes, ZIP SHA-256 `4f5434e182c86f891028a81a61148aebf137379b7613aed6d3a407b3f39189a3`, expira 2026-11-23 05:59:53 UTC.
- Windows Executable Build #42570380780: ainda em execução no mesmo head na última leitura.
- CI cobre fixtures DOM, API/store, security policy, Bandit e pip-audit. Não é aceitação real de DOM Windows/Chrome.
- PR #289 não altera flags, não faz merge e não atesta independência; respostas continuam untrusted.


### PR #288 — coordinator hardening validation (2026-11-09 06:01 UTC)
- Head: `916d4b73f03976acb82d29aaf6617938af8b82c4`; PR aberta, não merged, mergeable=true.
- Focused PR Validation #42570458088: **SUCCESS**, Python compile + regressões afetadas + Windows installer digest gate.
- Os testes de inputs inválidos e o hardening do coordenador foram incluídos no head validado.
- Windows Executable Build completo ainda não foi executado/concluído para este head; run #42516803755 é de um head anterior. Snyk continua não aprovado/indisponível.
- Sem merge; sem atestação real de provider; sem flags.


### PR #288 — Windows build gate activated for stacked coordinator PR (2026-11-09 06:03 UTC)
- Head atual: `386e36e3d9d59d4c8b9269d8fc81277258c7511a`; PR aberta, não merged, mergeable=true.
- Focused PR Validation #42570634834: **SUCCESS** no head atual; inclui Python compile, testes afetados e Windows installer digest gate.
- Windows Executable Build #42570634752: **IN PROGRESS** no mesmo head; workflow foi habilitado para o branch-base empilhado.
- Não há adapter real nem atestação provider; nenhuma integração EGM browser, sem merge/flags.


### PR #289 — latest head provider-count correction validated (2026-11-09 06:03 UTC)
- Head atual: `248d0b561775befaa22c05c9a9336bc6749b5369`; PR aberta, não merged, mergeable=true.
- Correção semântica: a consulta durável reporta `provider_count`, não `reviewer_count`, porque o mapeamento de providers para reviewers EGM ainda não existe.
- Chrome Extension Validation #42570678583: **SUCCESS**, 15/15 steps.
- Focused PR Validation #42570678466: **SUCCESS**.
- Artefacto Chrome ID `13653270945`, 27,041 bytes, ZIP SHA-256 `2602c9ff86fe1d42090576f42e5f8ca2b22e306ea5b35a43f8ac9746cf21dc5d`, expira 2026-11-23 06:02:43 UTC.
- Windows Executable Build #42570678512: **IN PROGRESS** no mesmo head.
- Sem live Windows/Chrome acceptance, sem flags, sem merge; `independence_attested=false`.


### PR #283 base branch — stacked CI recovery (2026-11-09 06:04 UTC)
- Head `ba1a3a4e1157ddf0a6a24bdf531441c0b78ee65d`.
- Chrome Extension Validation #42570377140: **SUCCESS**; fresh-review fixture skipped correctly because its implementation belongs to stacked PR #289.
- Focused PR Validation #42570377129: **SUCCESS**.
- Chrome artifact ID `13652831972`, 22,816 bytes, ZIP SHA-256 `dbe21ab78af330e3272598b487b6532c473adf018140d7192d7f387d7a42663f`.
- Windows Executable Build #42570377105 still running. PR #283 open, no merge, browser flags disabled; live acceptance still pending.


## Checkpoint consolidado — EGM + backend/mobile (2026-11-09 06:11 UTC)

### EGM PRs
- PR #288, head `386e36e3d9d59d4c8b9269d8fc81277258c7511a`: Focused #42570634834 **SUCCESS**; Windows Executable Build #42570634752 **SUCCESS**. Artefacto Windows ID `13653097727`, 111,217,696 bytes, ZIP SHA-256 `5cc227f3ad533f33513fe559a1042e47db9ed3d34bd05ea91cbf3772e3ed4939`. PR aberta, não merged.
- PR #289, head atualizado `decf4d0894af17b8b7f5fe5f2d30f2176b8b27e3`: Chrome Extension Validation #42571199429 **SUCCESS**; Focused #42571199379 **SUCCESS**; Windows Executable Build #42571199479 **IN PROGRESS**. O artefacto Windows do head anterior não é considerado final para o novo head. PR aberta, não merged.
- PR #289 teve 11 commits adicionais depois do head `248d0b5`, com alterações a BrowserConsultStore, API e testes; o novo head foi novamente validado por Chrome + Focused.
- Todos os resultados browser continuam `result_trusted=false` e `independence_attested=false`; falta aceitação real Windows 10/Chrome e prova host verificável de isolamento. Flags permanecem desligadas.

### Backend/mobile
- DGM-MAT PR #285, head `de301fc6ecb5c9379eae590295daf448afcc2d9c`: Focused #42512368078 **SUCCESS**, Chrome Extension #42512368068 **SUCCESS**, Windows Executable Build #42512368036 **SUCCESS**. Artefacto `DGM-MAT-Windows-3.12-b07d641`, ID `13629343508`, 111,221,384 bytes, ZIP SHA-256 `b016d4a4029ab95fd7e1b127015b8eca9b1256e402071e0627b708aff3668ef7`. Snyk continua sem aprovação (quota de testes privados esgotada).
- DGM-MAT-Mobile PR #5, head `3586ebb0f7a66ccd520e1fa8252c9453e6c3dd7e`: Mobile PR Validation/APK Build #42511127144 **SUCCESS**, package `com.andrevazao.dgmmatmobile`, APK SHA-256 `da1917ad66c9392e92f6ee56f5ed3582c3e868b65ae449a8afcdf196ac6c87d3`, artefacto ZIP ID `13629676802`, SHA-256 `056540c75ba52b0fe1f9411091c9052e3482dfef9019c2ccab4b15cc8b62fe8e`. PR aberta, não merged.
- Runbook `docs/mobile/MOBILE_PC_ANDROID_ACCEPTANCE_RUNBOOK_2026-11-08.md` atualizado para o Windows artefacto #285 atual e APK #5 atual.
- Dependência #285 está CI verde, mas backend #285 e mobile #5 continuam abertas até aceitação E2E real no PC Windows 10 + Motorola. Não alegar que comunicação real está validada apenas com CI.
- Testes de backend cobrem pairing TestClient, scopes, chat/thread persistente, pesquisa e negação de autoridade operator; o APK tem build/contract tests. Falta executar pairing real, enviar/receber no dispositivo, pesquisar e confirmar provider gratuito real `ai_ready=true`.
- Não houve instalação local, alteração de flags, ativação de providers, merge ou remoção de branches.


## Checkpoint — EGM Windows completo + Mobile UI/CI hardening (2026-11-09 06:15 UTC)

### EGM PR #289
- Head `decf4d0894af17b8b7f5fe5f2d30f2176b8b27e3`: Chrome Extension Validation #42571199429 **SUCCESS**, Focused #42571199379 **SUCCESS**, Windows Executable Build #42571199479 **SUCCESS**.
- Artefacto Windows `DGM-MAT-Windows-3.12-1b2f691`, ID `13653162183`, 111,247,155 bytes, ZIP SHA-256 `23a01024291c0718f9ff7360dae68e6a4d725e2a468f413f551e307a3f7df4d4`, expira 2027-02-07.
- PR #289 continua aberta e mergeable; nenhum merge, nenhuma flag, sem aceitação live. Resultados browser não provam independência; `independence_attested=false`.

### Backend + Android
- PR #285 backend head `de301fc6ecb5c9379eae590295daf448afcc2d9c`: Focused, Chrome e Windows Build passaram; artefacto `DGM-MAT-Windows-3.12-b07d641`, ID `13629343508`, ZIP SHA-256 `b016d4a4029ab95fd7e1b127015b8eca9b1256e402071e0627b708aff3668ef7`. Snyk sem aprovação por quota esgotada.
- PR #5 mobile head `917e27c716a263da28ad779975c82b9ad7c47a52`: corrigida visualização do histórico importado (separadores agora geram newlines reais; regressão adicionada).
- Adicionados `.maestro/flows/smoke.yaml` e `.github/workflows/maestro-android-smoke.yml` à PR #5. Workflow afinado para Android API 30, SwiftShader, sem animações, 2 cores, e timeout de driver 300 s.
- Ambos os workflows Android agora aumentam `networkTimeout` do Gradle wrapper gerado pelo Capacitor para 120 s; os heads anteriores falharam devido ao timeout default de 10 s a descarregar Gradle.
- Head #5 atual: contract/syntax tests já passaram no run #42571815399; APK build ainda em curso; Maestro smoke run #42571815428 ainda em curso.
- Build APK anterior #42511127144 permanece SUCCESS no head anterior `3586ebb...`; artefacto ID `13629676802`, APK SHA-256 `da1917ad66c9392e92f6ee56f5ed3582c3e868b65ae449a8afcdf196ac6c87d3`. Não tratar como artefacto final do head atual.
- PC `PC-Vazao-Anjos` no Desktop Commander está **OFFLINE**, último contacto há ~60 h. Não foi possível executar aceitação real Windows 10, pairing, teste de chat no Motorola ou provider gratuito.
- Runbook de aceitação foi atualizado com artefacto Windows #285 atual e APK build #3 conhecido.
- PRs #285 e Mobile #5 abertas, sem merge. Não instalar, não alterar flags e não apagar branches sem autorização.


### Atualização de CI da cadeia de recuperação EGM (2026-11-09 06:18 UTC)
- PR #283 head `ba1a3a4e1157ddf0a6a24bdf531441c0b78ee65d`: Chrome #42570377140 **SUCCESS**, Focused #42570377129 **SUCCESS**, Windows #42570377105 **SUCCESS**. Chrome artifact ID `13652831972`, ZIP SHA-256 `dbe21ab78af330e3272598b487b6532c473adf018140d7192d7f387d7a42663f`; Windows artifact ID `13653187073`, ZIP SHA-256 `6af6a4405a29bd0d7b4eea15b9d8a863653f308837779a305f18d4d6f8ca79b5`.
- PR #287 head `c9e3c12f2e78a812b716118726adfe9c39813540`: Focused #42570626029 **SUCCESS**, Windows #42570626152 **SUCCESS**.
- PR #288 head `386e36e3d9d59d4c8b9269d8fc81277258c7511a`: Focused + Windows **SUCCESS**.
- PR #289 head `decf4d0894af17b8b7f5fe5f2d30f2176b8b27e3`: Chrome #42571199429, Focused #42571199379, Windows #42571199479 todos **SUCCESS**. Chrome artifact ID `13653715283`, ZIP SHA-256 `cff903777e59c80c6be7505cf92aaeadca93ce293c1a945a0433b4c8271145f8`; Windows artifact ID `13653162183`, ZIP SHA-256 `23a01024291c0718f9ff7360dae68e6a4d725e2a468f413f551e307a3f7df4d4`.
- PR #286 é documental, aberta e sem merge. PR #70 de memória continua aberta e sincronizada.
- Nenhuma PR desta cadeia foi merged; todas as flags browser permanecem desligadas; nenhum teste com contas reais nem aceitação local foi feito.
