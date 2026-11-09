# DGM-MAT — continuidade e fontes de IA — 2026-11-09

## Ecossistema de IA confirmado pelo utilizador

Fontes de conversas, pela ordem indicada:
1. ChatGPT
2. Grok
3. Gemini
4. Claude
5. DeepSeek
6. Qwen

Agentes locais de execução no PC:
- Codex Free
- Claude Code Free

Ambos são usados através de FCC com NVIDIA NIM. Esta configuração foi reportada pelo utilizador; a disponibilidade, autenticação, modelo efetivo, quotas e execução real devem continuar a ser verificadas em cada ambiente. Não assumir que a indicação de fornecedor equivale a uma chamada funcional comprovada.

Separação obrigatória:
- Os seis fornecedores acima são fontes potenciais de conversas/histórico.
- Codex Free e Claude Code Free são agentes locais para tarefas de execução, sujeitos a sandbox, aprovação, timeout e recibos.
- Não classificar os agentes locais como fornecedores de histórico sem evidência específica.
- “Zia” foi erro de transcrição por voz; não existe fornecedor Zia no roster confirmado. Não criar integração Zia.

## DGM-MAT — estado confirmado nesta sessão

### Memória e contexto
- Repositório canónico de memória: `AndreVazao/andreos-memory`, branch `main`.
- Memória lógica DGM-MAT: `AndreOS/02_PROJETOS/DGM-MAT/`.
- O utilizador pediu atualização desta memória persistente e continuidade do desenvolvimento DGM-MAT.
- O Desktop Commander deve ser poupado para uma instalação consolidada da versão quase pronta e uma única validação inteligente. Não fazer testes repetidos no PC nem contornar limites de quota.

### Código de recuperação de conversas existente
- `ConversationProgressStore` persiste snapshots de conversas e estados de processamento em SQLite, com `list_conversations()`, `get_conversation()`, fingerprints e estado por fonte.
- `ConversationIntelligencePipeline` grava transcrição normalizada, mensagens ordenadas, metadados, artefactos extraídos, findings e proveniência quando disponível.
- A captura real de históricos privados dos seis fornecedores ainda não está demonstrada como completa. Stubs de providers não são coletores de histórico. Não afirmar importação total.
- Arquivos locais e exportações oficiais devem ser preservados antes de indexação; sessão autenticada/browser só pode ser usada por mecanismos suportados, sem ler cookies/tokens/passwords, contornar MFA/CAPTCHA ou rate limits.

### PR #306 — dossiers de contexto por projeto
- PR: https://github.com/AndreVazao/DGM-MAT/pull/306
- Título: `feat: generate evidence-linked project context dossiers`
- Branch e SHA devem ser consultados na PR antes de qualquer merge.
- Ficheiros: `core/conversation_intelligence/project_context.py`, `tests/conversation_intelligence/test_project_context.py`, `docs/operations/PROJECT_CONTEXT_DOSSIERS_V1.md`.
- Implementação V1 gera Markdown por projeto apenas a partir de mapeamento explícito `provider:conversation_id`; não faz associação fuzzy.
- Mensagens user/human são apresentadas como declarações/evidência; mensagens assistant/model ficam numa secção separada de propostas e nunca são promovidas automaticamente a decisões aprovadas.
- Artefactos de código são candidatos, com fingerprint e origem da conversa; não se afirma presença, correção ou recuperação no repositório.
- Escrita é atómica; histórico é content-addressed por SHA-256; manifest JSON regista fontes; snapshots SQLite não são alterados.
- Conversas sem mapeamento e incompletas ficam contabilizadas, sem atribuição presumida.
- Validação focada: run `42643124514`, regressões afetadas SUCCESS e installer digest gate SUCCESS.
- Build Windows: run `42643124184`, concluído SUCCESS; build, deep executable validation, assertions e upload de artefactos concluídos.
- PR #306 permanece OPEN; não fazer merge sem confirmar HEAD/checks/revisão atualizados.
- Revisão técnica submetida (review ID `5828019021`): melhorar paginação/lotes para não carregar todas as transcrições em RAM; preservar timestamps/source_path/metadados por mensagem; manter `provenance.message_id` e `source_fingerprint` nos artefactos sempre que existam. Não ligar ao arranque autónomo antes de resolver/avaliar estas limitações.

### Regras de trabalho
- Evidência antes de afirmações; metadata-only não é recuperação de conteúdo.
- Não confundir sugestão de IA com decisão do utilizador.
- Não marcar código como recuperado sem comparar conteúdo/hash com ficheiro real.
- Não fundir projetos independentes sem aprovação explícita.
- Não alterar main diretamente; usar branches/PRs pequenos, testes e build Windows.
- Não instalar ainda no PC apenas porque o build CI passou; a instalação final deve ser consolidada e seguida de uma única validação inteligente com backup/rollback, runtime full, cockpit/mobile/API e uma missão real.

## Próximos passos

1. Consultar novamente PR #306 e confirmar todos os checks e o HEAD atual.
2. Melhorar o gerador para paginação/batches, proveniência por mensagem e proveniência do artefacto.
3. Acrescentar testes para snapshots grandes, preservação de timestamps/source_path, e ligação artifact→message.
4. Integrar dossiers no ciclo de recuperação apenas após testes; não arrancar captura de provider ainda não validada.
5. Evoluir captura real dos seis fornecedores: ChatGPT, Grok, Gemini, Claude, DeepSeek e Qwen, começando por exportações oficiais/arquivos locais e medindo completude por fonte.
6. Só quando a versão estiver suficientemente madura, preparar instalação Windows consolidada e reservar Desktop Commander para essa operação e validação única.



## Atualização — 2026-11-09: chat de comando, consulta às IAs e pesquisa headless

### Requisito do operador — Issue #313
- Issue: https://github.com/AndreVazao/DGM-MAT/issues/313
- O chat principal do DGM-MAT deve ser o centro de comando persistente, com três ações sempre acessíveis:
  1. **Pesquisar histórico** de conversas/mensagens/missões por texto, projeto, fornecedor/agente, data, ID e estado.
  2. **Nova conversa**, com thread independente e durável, opcionalmente associada a um projeto/dossier, sem apagar ou herdar silenciosamente conversas anteriores.
  3. **Pedir ajuda a uma IA**, usando o contexto técnico exato da missão ativa.
- A pesquisa só pode apresentar conteúdo realmente capturado/indexado. Mostrar completude: complete, partial, metadata-only, unavailable ou unknown; URLs e metadados não provam captura de transcrição.
- O pacote de contexto para outra IA deve ser limitado, determinístico, revisto pelo operador e incluir pedido original, objetivo, missão, repositório/branch/base SHA, excertos relevantes, erros, testes, tentativas e restrições.
- Mostrar o prompt e contexto exatos antes do envio. Exigir confirmação explícita. Permitir editar e excluir elementos do contexto.
- Nunca enviar segredos, tokens, cookies, chaves ou informação não relacionada. Não usar endpoints privados inventados, extração de credenciais, bypass de MFA/CAPTCHA ou evasão de rate limits.
- Fornecedores conversacionais: ChatGPT, Grok, Gemini, Claude, DeepSeek e Qwen. Agentes locais Codex Free e Claude Code Free devem aparecer em categoria separada; não confundir chat provider com CLI executor.
- Respostas externas são propostas atribuídas à sua origem, não decisões aprovadas. Não podem provocar automaticamente escrita de código, aprovações, merges ou deploys.
- Transportes não verificados devem aparecer indisponíveis. Proibido fallback pago silencioso.
- Implementar em fases: (A) pesquisa/histórico e novas conversas; (B) montagem/preview do contexto da missão; (C) consulta governada a fornecedores, um de cada vez e com E2E real; (D) hardening, preempção de tarefas de fundo e recuperação por checkpoint.

### Especificação documentada
- Documento: AndreVazao/DGM-MAT/docs/architecture/COMMAND_CENTRE_CHAT_V1.md
- PR #314: https://github.com/AndreVazao/DGM-MAT/pull/314
- Merge commit: 273c38621304a92a3d2d5c73d440194cc3c540f1
- Issue #313 recebeu comentário com a ligação ao documento e estado.
- A documentação define requisitos e testes de aceitação; não significa que a UI, pesquisa ou consulta a IAs já estejam implementadas.

### Pesquisa headless pública — PR #311 integrada
- PR #311: https://github.com/AndreVazao/DGM-MAT/pull/311
- Branch commit validado: 7bd28808a7ce82a83b17099a673946cb2f60710e
- Merge commit: 9527fda6cdad00fa67e647cd76441440c021e3fd
- CI validada com sucesso:
  - Focused PR Validation run 42649125698 (#847);
  - Mission E2E Regression Gate run 42649125679 (#24), Ubuntu e Windows SUCCESS;
  - Windows Executable Build run 42649125659 (#441), build, deep executable validation, assertions e upload de artefacto SUCCESS.
- A capacidade permite pesquisa web pública em browser Playwright headless efémero, pesquisa de repositórios públicos via invocação fixa read-only de gh search repos, e leitura de URLs HTTPS explicitamente permitidos.
- Pára perante CAPTCHA/desafios; não contorna MFA, CAPTCHA, rate limits nem controlos do fornecedor.
- Não clona, instala, executa ou altera repositórios. Suitability fica not_evaluated até revisão.
- Não implementa captura autenticada de históricos privados, nem execução real de Codex/Claude CLI. O planner de CLI continua dry-run com launch desativado. Issue #310 mantém esses trabalhos bloqueados até verificação e aceitação específicas.

### Regras de continuidade
- Reutilizar Vault, catálogo, RecoveryLedger, Conversation Intelligence, threads e registos de missão existentes; não criar stores concorrentes sem auditoria prévia.
- Prioridade inicial da Issue #313: pesquisa e navegação do histórico + nova conversa independente. Em seguida context package com preview/consentimento, e só depois os transportes para outras IAs.
- Nenhuma integração de fornecedor pode ser marcada funcional sem teste real de envio e resposta.
- Desktop Commander permanece reservado para a instalação final consolidada e uma única validação inteligente; não gastar quota em verificações repetidas no PC.


### Auditoria do chat desktop — 2026-11-09
- Documento de requisitos atualizado com auditoria: AndreVazao/DGM-MAT/docs/architecture/COMMAND_CENTRE_CHAT_V1.md, commit d2e9c8a131d47258af41a158a85155b7e6064860.
- O entry point desktop efetivo é MinimalChatWindow → CommandConsoleWidget.
- CommandConsoleWidget submete uma diretiva como missão e acompanha o resultado. A sua lista history é apenas RAM; não existe ali ID/thread persistente, pesquisa, seletor de conversas ou operação de nova conversa.
- cockpit/workspace/chat_widget.py é um widget separado, não utilizado pelo MinimalChatWindow inspecionado; não assumir que é o chat de produção.
- core/api/conversation_archive_api.py expõe apenas status/import Telescope no router inspecionado; não expõe pesquisa de mensagens nem create/open/resume de threads.
- ConversationProgressStore é registo de progresso de ingestão de fontes/conversas, não o store de threads do chat operacional.
- ConversationKnowledgeStore é a camada de evidência/intenções/propostas/decisões, não deve ser transformado em armazenamento bruto de transcrições.
- Próximo passo técnico: rastrear APIs canónicas de missões/mensagens e verificar se existe um modelo de thread persistente noutra camada antes de propor migração/endpoints. Depois implementar pesquisa paginada e thread lifecycle, com testes de isolamento/restart, e ligar os controlos ao CommandConsoleWidget.
- Esta foi inspeção de código via GitHub; não é validação no PC nem teste runtime. Nenhuma funcionalidade nova de UI foi alegada.


### Correção da auditoria — thread store existente no módulo mobile
- A auditoria alargada encontrou um serviço persistente já implementado: core/mobile_runtime/store.py (ConversationStore), core/mobile_runtime/service.py (MobileConversationService) e rotas em core/api/mobile_bridge.py (/mobile/threads, /mobile/threads/search, detalhe, mensagens e rename).
- ConversationStore guarda threads/mensagens em JSON atómico, carrega o conjunto em memória e reescreve o documento em cada mutação. A pesquisa devolve snippets e limita o número máximo de resultados, mas não suporta offset/cursor pagination.
- A UI desktop MinimalChatWindow → CommandConsoleWidget não utiliza atualmente este serviço.
- Decisão corrigida: reutilizar ou abstrair o serviço/store existente; não criar uma segunda base de conversas. Antes de o partilhar com desktop, testar compatibilidade mobile, autenticação, crescimento do arquivo, custo de escrita/leitura e comportamento com fixtures grandes. Considerar backend SQLite apenas se medições justificarem.
- PR #315 documenta esta descoberta e foi integrada: https://github.com/AndreVazao/DGM-MAT/pull/315 — merge commit b90f56e526930bcc6cb531d20c53ffded084793d.
- Documento canónico atualizado: docs/architecture/COMMAND_CENTRE_CHAT_V1.md.
- A primeira inspeção tinha sido limitada ao chat desktop e ao router de arquivo; esta nota substitui qualquer interpretação de que não existia um modelo de thread persistente em nenhuma outra camada.


### Implementação Phase A — pesquisa paginada — 2026-11-09
- PR #316: https://github.com/AndreVazao/DGM-MAT/pull/316
- Branch: `feat/command-centre-history-pagination-v1`.
- Commit HEAD: `2ca84d928bd670c82e64b1b3cfc1c99d3596a2d2`.
- Alterações: `ConversationStore.search_threads_page()` fornece ordenação determinística, offset/limit, total_count, next_offset e has_more; `search_threads()` mantém a interface antiga de lista para compatibilidade.
- API existente `GET /mobile/threads/search` passa a aceitar `offset` e devolve metadados de paginação mantendo `results` como lista.
- Resultados das conversas nativas locais incluem proveniência `dgm-mat-local-conversation-store` e `capture_completeness=complete`. Isto não se aplica a arquivos importados de fornecedores.
- Testes acrescentados para páginas sem duplicados, metadados de proveniência, limites e compatibilidade.
- CI Focused PR Validation run #848 (ID 42652086835) estava QUEUED na última consulta. PR não foi merged; não declarar testes aprovados até haver conclusão verde.
- Próxima fatia: adicionar cobertura API para paginação e integrar o desktop `CommandConsoleWidget` com o mesmo serviço autenticado, separando gravação passiva de mensagens da rota mobile que interpreta mensagens e pode criar missões. Não submeter uma diretiva duas vezes nem transformar uma simples gravação de histórico numa missão.
- O comentário de progresso foi registado na Issue #313.


### Validação e integração da pesquisa paginada — 2026-11-09
- PR #316 foi integrado em `main` por squash merge: `0982361b37857618dfa05819e6c3a21801c6f5d2`.
- CI Focused PR Validation run #848 / ID `42652086835`: sucesso. Job de compilação e regressões selecionadas passou.
- Windows installer digest gate: sucesso.
- Windows Executable Build run ID `42652086753`: sucesso; build completo do executável concluído.
- Snyk `security/snyk` devolveu estado error por limite mensal de testes privados esgotado. É uma limitação de quota externa já conhecida; não confundir com falha dos testes do código nem reintroduzir Snyk como gate obrigatório enquanto a quota não existir.
- Issue #313 recebeu comentário com este resultado e a fase seguinte.

### Fase de persistência passiva para o cockpit — PR #317
- PR: https://github.com/AndreVazao/DGM-MAT/pull/317
- Branch: `feat/desktop-passive-entry-v1`.
- HEAD: `d628271b19eaf791f1292770a06eff0f6be3cb7d`.
- Implementa `MobileConversationService.append_transcript_entry()`: grava uma entrada já produzida, sem chamar IntentInterpreter, MissionEngine ou criar missão.
- Nova rota `POST /mobile/threads/{thread_id}/entries`, classificada explicitamente como `operator`; não disponível aos clientes mobile emparelhados com scopes limitados.
- Validação: apenas roles user/assistant/system, conteúdo não vazio até 20.000 caracteres, thread existente; metadata de origem `desktop-cockpit-transcript`.
- A rota antiga `POST /mobile/threads/{thread_id}/messages` permanece inalterada e continua a interpretar intenções com governação de missões. Esta separação evita duplicação de submissões quando o cockpit passar a persistir a conversa.
- Foram adicionados testes unitários de persistência, isolamento da interpretação e validação de entradas. CI Focused PR Validation run ID `42653058878` estava em curso na última consulta; PR ainda não integrado.
- Próximo passo após CI: integrar controlos assíncronos de nova conversa/pesquisa/abertura no `CommandConsoleWidget`, ligando o envio da missão à thread ativa e gravando apenas os resultados efetivamente recebidos. Não criar missão ao abrir, pesquisar ou persistir transcript.

- Correção da primeira execução de CI do PR #317: o primeiro run `42653058878` falhou porque o novo teste usava `pytest.raises` sem importar `pytest`. Foi corrigido no commit `b035b26f573e6b44ecfcffdfd2fda890a9eeaa67`.
- Revalidação no commit corrigido: Focused PR Validation run `42653288187` passou; Windows installer digest gate passou; Chrome Extension Validation run `42653288188` passou.
- Windows Executable Build run `42653288191` continuava em curso na última verificação. PR #317 não deve ser merged antes da conclusão desta verificação.

### PR #317 — persistência passiva integrada — 2026-11-09
- PR #317 merged: https://github.com/AndreVazao/DGM-MAT/pull/317
- Merge commit: `dedf88c7c5cad470c7e1d118fae25b96d9bc725d`.
- CI Focused PR Validation run #? / ID `42653288187`: sucesso.
- Windows installer digest gate: sucesso.
- Chrome Extension Validation run `42653288188`: sucesso.
- Windows Executable Build run #446 / ID `42653288191`: sucesso.
- CodeRabbit check ficou `skipped` por exigir revisão manual neste repositório OSS; não houve parecer automatizado nem findings desse bot.
- Issue #313 recebeu comentário com o merge e a validação.
- A nova rota passiva `POST /mobile/threads/{thread_id}/entries` é agora parte de main, classificada como `operator`; grava transcript existente sem interpretação nem dispatch de missão.
- Próxima branch planeada: integração real da UI `CommandConsoleWidget` com GET/POST de threads, pesquisa paginada, abertura de histórico e persistência assíncrona de entradas. Deve manter envio de missão exatamente uma vez e não bloquear GUI.

### PR #318 — UI de histórico no cockpit desktop — em validação
- PR: https://github.com/AndreVazao/DGM-MAT/pull/318
- Branch: `feat/command-centre-thread-history-ui-v2`.
- HEAD na última atualização: `493ab9bb2b8488fafeae8456405f80c190d5670c`.
- `cockpit/widgets/command_console.py`: adiciona controlos para Nova conversa, pesquisa de histórico e Mais resultados (offset paginado), lista de resultados e abertura de thread.
- Usa a API local autenticada já existente, com `_ConversationRequestWorker` fora da thread GUI. Carregamento inicial é iniciado em `showEvent`, não no construtor, para evitar workers de rede em testes/instâncias que nunca são mostradas.
- Cada envio passa a criar/selecionar thread, gravar entrada user na rota passiva `/entries` e só depois chamar o worker de missão. Se a persistência falhar, não envia missão.
- Cada worker de missão guarda o thread_id de origem; respostas posteriores são escritas nessa thread mesmo que o utilizador mude de contexto depois (navegação bloqueada durante missão).
- Escritas transcript serializadas por fila para preservar a ordem. Nova conversa/pesquisa/abertura bloqueadas durante missão e escrita de transcript.
- Testes adicionados em `tests/cockpit/test_minimal_chat_window.py`: controlos UI, chamadas autenticadas fora da GUI, envio apenas após persistência, falha fail-closed, ordem de transcript, paginação e bloqueio de navegação.
- PR #318 ainda não foi integrado. CI para HEAD `493ab9bb2b8488fafeae8456405f80c190d5670c`: Focused PR Validation run `42657210534` e Windows Executable Build run `42657210476` em curso. CodeRabbit é `skipped` por exigir revisão manual no OSS.
- Issue #313 recebeu comentário com a descrição e estado da fase.
- Atenção: build/CI ainda não confirmam comportamento em PC físico. Não afirmar instalação ou teste no Windows local até à validação do utilizador/ambiente local.

### PR #318 — atualização da validação — 2026-11-09
- HEAD atualizado: `ee961e1881aca97f1a158bd38d616e3110500200`.
- A primeira Focused PR Validation falhou apenas no teste do sinal Qt: `QThread.wait()` concluiu o worker, mas a fila de eventos da QApplication ainda não tinha despachado o sinal para o lambda de teste. Corrigido adicionando `qt_app.processEvents()` antes da asserção; o worker e a chamada HTTP já estavam a executar na thread secundária.
- Nova Focused PR Validation run `42657424971`: sucesso.
- Windows installer digest gate: sucesso.
- Windows Executable Build run `42657424958`: ainda em curso na última consulta.
- PR #318 permanece aberto; não integrar até concluir o build Windows e rever os checks finais.
- Issue #313 recebeu comentário atualizado.


### PR #318 — histórico do cockpit integrado — 2026-11-09
- PR #318: https://github.com/AndreVazao/DGM-MAT/pull/318 — merged por squash.
- Merge commit em `main`: `725b8cb3d817c7b2d4faa8999cee6246aaf798f1`; HEAD de `main` confirmado com o mesmo SHA.
- HEAD validado: `ee961e1881aca97f1a158bd38d616e3110500200`.
- Focused PR Validation run `42657424971`: SUCCESS.
- Windows installer digest gate: SUCCESS.
- Windows Executable Build run `42657424958` (#456): SUCCESS. Build, deep executable validation, final assertions e upload de artefactos concluídos.
- Artefacto Windows `DGM-MAT-Windows-3.12-7b7c7ac`, 111,270,824 bytes, SHA-256 `45e4c16d4d5cb7afc09f3e2a15b593b3c2b63e86fe95f7b83d72f9990101c9b7`; expiração indicada: 2027-02-07.
- Revisão final: apenas `cockpit/widgets/command_console.py` e `tests/cockpit/test_minimal_chat_window.py` alterados; nenhum review thread aberto nem reviews submetidos. Contratos de backend confirmados em `main`: criação devolve thread com `id`; pesquisa devolve `thread_id`; detalhe devolve `id/messages`; endpoint passivo aceita roles user/assistant/system e grava sem dispatch.
- Funcionalidade integrada: Nova conversa, pesquisa paginada e abertura de threads; pedidos HTTP fora da GUI; mensagem user persistida antes de submeter missão; falha de persistência bloqueia dispatch; respostas da missão regressam à thread de origem; fila serializa escritas.
- Limite explícito: CI comprova build e testes automatizados, não instalação nem funcionamento no PC físico do utilizador. Instalação local fica reservada à validação consolidada.
- CodeRabbit foi skipped por exigir revisão manual; não houve aprovação automatizada desse bot.
- Próxima fase da Issue #313: pacote de contexto da missão para consulta a outra IA, com seleção de provider, preview/edit/exclusão, redaction, confirmação explícita, provenance e armazenamento da resposta como proposta. Primeiro auditar transportes reais/configurados; não assumir que os seis providers estão acessíveis. Codex Free e Claude Code Free continuam categoria separada de agentes locais.


### PR #319 — pré-visualização exata antes de consultar IA — 2026-11-09
- PR aberta: https://github.com/AndreVazao/DGM-MAT/pull/319
- Branch: `feat/browser-consult-exact-preview-v1`; último HEAD: `3749fba400d1eb6c5d1dc47fc0f28c35d1efe309`.
- Adiciona `POST /recovery/browser-consult/preview` sob scope dedicado `browser-consult-control`; devolve o texto exato gerado pelo redactor, SHA-256 e flag de marcador de segredo, sem criar fila ou contactar provider.
- Enqueue pode receber `preview_sha256`; a API recalcula e recusa com HTTP 409 se goal/context já não corresponderem ao preview. O popup exige preview antes de enfileirar e limpa-o sempre que goal/context mudam. O prompt final fica read-only; edição nesta iteração faz-se nos campos goal/context e nova pré-visualização.
- Testes acrescentados para redaction, ausência de side effect, digest binding e preview com sessão real de extensão de scope estreito.
- UI informa que Claude ainda não está disponível neste canal. O allowlist atual continua ChatGPT, Grok, Gemini, DeepSeek e Qwen. Não foi ativada qualquer flag nem alterado o custo/fallback.
- PR #319 ainda aberta; não integrar antes de checks do HEAD final e revisão.
- Próxima evolução depois deste gate: construtor determinístico de contexto da missão no cockpit, seleção de provider, edição/remoção de excertos e confirmação explícita; preservar provenance e respostas não verificadas. Claude só entra após adapter específico e validação da UI autenticada.


#### Validação intermédia PR #319 — HEAD final 3749fba — 2026-11-09 17:43 UTC
- Focused PR Validation run `42667190982` (#861): SUCCESS, incluindo compilação Python e regressões selecionadas.
- Chrome Extension Validation run `42667190864` (#432): SUCCESS, sintaxe JS, fixtures, regressões de segurança/API e pacote da extensão.
- Windows installer digest gate: SUCCESS.
- Windows Executable Build run `42667190859` (#459): IN_PROGRESS, ainda em instalação de dependências; build/deep check/upload não começaram.
- CodeRabbit skipped por exigir revisão manual; revisão de diff manual efetuada. Não fazer merge enquanto build Windows estiver pendente.


### PR #319 — integrada — 2026-11-09
- PR #319: https://github.com/AndreVazao/DGM-MAT/pull/319 — merged por squash.
- Merge commit: `e09553a591594d80253b572f06059190eea540d5`.
- HEAD validado: `3749fba400d1eb6c5d1dc47fc0f28c35d1efe309`.
- Focused PR Validation, Chrome Extension Validation, Windows installer digest gate e Windows Executable Build concluídos com SUCCESS.
- Artefacto Windows `DGM-MAT-Windows-3.12-139f2c5`, 111,273,743 bytes, SHA-256 `a9d77dce8d27a1bc70c11d70fa8a885f6fe7f3216fdb9a3c0db8131463128ca7`, expira em 2027-02-07.
- PR implementa endpoint autenticado de preview exato redigido e ligação SHA-256 entre preview e enqueue; popup exige preview; conteúdo alterado após preview recebe HTTP 409. Não acrescenta Claude ao allowlist de browser consultation.

### PR #320 — inventário durável de links GitHub nas conversas — 2026-11-09
- PR aberta: https://github.com/AndreVazao/DGM-MAT/pull/320
- Branch `feat/mission-context-and-github-reference-vault-v1`; HEAD atual `56e0bca945351452faa88fd031e417e23e752788`.
- Vault schema v3 adiciona `github_repository_refs` e `github_repository_ref_sources`. `VaultCatalog.archive_conversation()` extrai links canónicos github.com owner/repository de mensagens/título, deduplica e guarda provider, conversa, message_id e URL da conversa; não copia corpos de mensagens para o índice.
- ChatGPT JSON/ZIP import também indexa links. Browser capture e Chrome archive import usam Vault archive path e ficam cobertos.
- API operator-only: GET `/recovery/github-references`; POST `/recovery/github-references/reindex` com cursores independentes Vault/legacy ChatGPT; POST `/recovery/github-references/verify` (máximo 25 por chamada).
- Verificação consulta apenas `api.github.com/repos/{owner}/{repo}`, sem credenciais. Estados: `verified_public`, `not_found_or_private`, `rate_limited`, `unavailable`. HTTP 404 não é tratado como prova de inexistência porque repositórios privados/inacessíveis também devolvem 404.
- Reindex lê arquivos locais imutáveis e não altera nem apaga fontes.
- Testes novos cobrem extração/deduplicação, provenance, backfill, ChatGPT import, classificação de rotas e estados de verificação.
- CI no HEAD final: Focused PR Validation run `42682785157` QUEUED; Windows Executable Build `42682784551` IN_PROGRESS; Chrome Extension Validation `42682784834` IN_PROGRESS. Não integrar antes de todos terminarem.
- Importante: a captura de conversas dos providers continua a exigir import/DOM capture. O arquivo histórico local Chrome é apenas descoberta parcial; não afirmar que todas as conversas foram recuperadas.


### PR #320 — CI feedback and correction — 2026-11-09 19:28 UTC
- Focused validation on earlier HEAD found test expectation mismatches only: canonical repository owner/name is intentionally case-folded. Tests updated to lowercase canonical URL; implementation retained case-insensitive deduplication.
- Latest HEAD after test corrections: 	adf95d202998d106451c3d71711be56c522404f8.
- Windows Executable Build and Chrome Extension Validation are running for latest HEAD. Focused PR Validation latest run is not yet visible; previous run failed only on case-sensitive expected strings. Do not merge before focused green.

### PR #321 — mission-aware consultation — 2026-11-09 19:28 UTC
- PR open: https://github.com/AndreVazao/DGM-MAT/pull/321; branch feat/mission-aware-ai-consultation-v1; latest tested HEAD 22fa07748fa02dec55aba244c9e44735b5a38bbc.
- Adds operator-authenticated POST /recovery/browser-consult/mission-context that reads one durable mission checkpoint, includes bounded goal/status/progress/logs/subtasks/artifact basenames and allowlisted metadata, redacts secrets and removes local filesystem paths. It does not contact a provider.
- Paired Chrome popup can load mission context; operator can edit/remove goal/context and must regenerate exact prompt preview. Mission ID is the consultation task_ref.
- Completed provider responses add consultation ID/provider/status/response SHA-256 to the mission checkpoint and log as unverified; if checkpoint has conversation_thread_id/thread_id, append the unverified response to that thread. No code change or approval is automated.
- Source-file excerpts are not auto-read in this first iteration; manual editable context is supported. A later repo-aware selector must validate paths against the mission repository root.
- Latest HEAD #321: Chrome Extension Validation SUCCESS; focused validation, Windows build in progress. Earlier focused run exposed a test dependency coupling to runtime_api/psutil and an incorrect artifacts/logs line; corrected by injecting _mission_engine() in tests and separating log/artifact collection. Revalidation is pending.


### PR #321 — mission-aware consultation integrada — 2026-11-09
- PR #321 merged por squash: https://github.com/AndreVazao/DGM-MAT/pull/321
- Merge commit main: `cb38db262e14f2374a6346cb009ff89971443772`.
- HEAD validado `22fa07748fa02dec55aba244c9e44735b5a38bbc`: Focused PR Validation SUCCESS, Chrome Extension Validation SUCCESS, Windows Executable Build SUCCESS, Windows installer digest gate SUCCESS.
- Windows artefacto `DGM-MAT-Windows-3.12-afcd410`, 111,279,386 bytes, SHA-256 `e2b9a15d57c9a4e35396f8ef7616cb965fbbdaf9a6ff263a3b422d3e1ebc41c2`, expira 2027-02-07.
- Popup consulta pode carregar checkpoint de missão, editar goal/context, preview SHA256 e enfileirar por mission_id. Contexto inclui apenas estado/progresso/logs recentes/subtarefas/basenames/metadata allowlist; remove caminhos locais e redige segredos. Nenhum provider contactado durante load.
- Resposta externa grava provenance (consultation id, provider, status, response hash) no checkpoint e log como proposta não verificada; se mission checkpoint tem thread_id, append na conversa original. Não altera código nem aprova tarefas.

### PR #322 — Claude no browser recovery — 2026-11-09
- PR aberta: https://github.com/AndreVazao/DGM-MAT/pull/322; branch `feat/claude-browser-conversation-capture-v1`; HEAD `f65abbf5d92fc6806574966647b7f8f3d8b4863e`.
- Adiciona Claude à captura histórica autenticada (API allowlist, validação source ID em /chat/{id} e /project/{project}/chat/{id}, provider rotation, host permission/content script injection, seletores DOM user-message/assistant-message/chat-message).
- Claude continua fora do provider allowlist de consulta externa e fora de fresh independent review; não há privacy-mode adapter verificado. Captura é apenas visible DOM snapshot, não full history.
- Testes API, DOM fixture e manifest atualizados. CI Chrome validation e Windows build ainda em execução/queued no momento desta nota. Live Claude DOM acceptance no Chrome do utilizador continua obrigatória.

### PR #320 — estado de integração após #321
- PR #320 permanece aberta e dirty porque #321 alterou a mesma security_policy.py. Não fazer merge direto. Reaplicar os oito ficheiros/alterações da branch #320 sobre main atualizado em #323 ou rebase controlado; manter testes e docs de #321.
- HEAD #320 `adf95d202998d106451c3d71711be56c522404f8`: focused validation em execução; Chrome validation e Windows build em execução. Primeiro focused run falhou apenas por expectativas de casing, corrigidas.


### PR #322 — Claude capture integrado — 2026-11-09
- PR #322 merged: https://github.com/AndreVazao/DGM-MAT/pull/322
- Merge commit main: c2ab2814165343abb684107a616afdad52b98409.
- HEAD validado 2c341eb617dc08bdaf83279c0a72be4078928e11: Focused PR Validation SUCCESS, Chrome Extension Validation SUCCESS, Windows installer digest gate SUCCESS e Windows Executable Build SUCCESS.
- Artefacto Windows DGM-MAT-Windows-3.12-ff1b213, 111,280,447 bytes, SHA-256 7ffc162f6f0733d4e5ee0bc4ca3a737cbb536ddfcf3b02f547c8e97645d8fecd, expira 2027-02-07.
- Browser capture suporta Claude em claude.ai/chat/{id} e claude.ai/project/{project_id}/chat/{id}. Extensão v0.3.2 / content adapter v0.1.4. Claude incluído na descoberta/rotação de captura; excluído de consulta externa e de polling de envio de missão; fresh-review continua bloqueado sem privacy mode verificado.
- DOM selector fixture cobre user-message/assistant-message/chat-message com deduplicação de containers aninhados. Live Claude UI acceptance ainda falta no PC do utilizador.

### PR #320 supersedida e fechada — 2026-11-09
- PR #320 fechada sem merge por conflito com security_policy.py após #321.
- Todo o conteúdo foi reaplicado sobre main atualizado em PR #323; nenhum código/teste foi descartado.
- PR #323: https://github.com/AndreVazao/DGM-MAT/pull/323; HEAD 0fcca24e27306c4bf428da06821aa996c833e34f; base atual main inclui #321 e #322.
- Focused PR Validation #885 (run 42685551194): SUCCESS.
- Chrome Extension Validation #456 (run 42685550546): SUCCESS.
- Windows Executable Build #485 (run 42685550381): IN_PROGRESS na fase Build Executable, sem resultado final no momento desta nota.
- PR #323 só pode ser integrada depois de Windows deep check e upload concluírem com SUCCESS.


### PR #323 — inventário GitHub integrado — 2026-11-09
- PR #323 merged por squash: https://github.com/AndreVazao/DGM-MAT/pull/323
- Merge commit e HEAD confirmado em main: `e5ab7a27bc2215945c37e57cd0c2a5b8c95e23d7`.
- HEAD testado: `0fcca24e27306c4bf428da06821aa996c833e34f`; Focused PR Validation #885 SUCCESS; Chrome Extension Validation #456 SUCCESS; Windows Executable Build #485 SUCCESS; Windows installer digest gate SUCCESS.
- Artefacto Windows `DGM-MAT-Windows-3.12-06fe206`, 111,288,123 bytes, SHA-256 `755ebddb3c388c1258133d16b2b55eb22c0ea9255c66d1d24ac09d5917f499d8`, expira em 2027-02-07.
- API operador: GET `/recovery/github-references`; POST `/recovery/github-references/reindex?limit=100&offset=0&legacy_offset=0`; POST `/recovery/github-references/verify?limit=10`.
- Vault schema v3 extrai links canónicos em archive_conversation, ChatGPT JSON/ZIP import e reindex de arquivos antigos; indexa provider/conversation/message provenance e não copia corpos das mensagens. Verificação usa apenas api.github.com public REST, sem credenciais. 404 = not_found_or_private; 403/429 rate_limited; falha de rede unavailable.
- PR #320 fechada como supersedida sem perda; #323 reaplicou os mesmos 8 ficheiros sobre main após #321.
- Estado main consolidado: #317, #318, #319, #321, #322 e #323 integradas. #320 fechada supersedida.

### Handoff operacional para recuperação de conversas — manhã 2026-11-10
- Build Windows mais recente contém PR #321 (mission-aware consultation), #322 (Claude historical capture) e #323 (GitHub link inventory).
- Artefacto Chrome Recovery da #322: `DGM-MAT-Chrome-Conversation-Recovery`, artifact ID `13704755395`, SHA-256 `a7d64218b825c3802a34489e9e19d77ec6d8d225e8076156f34ef20a68e781ac`, expira 2026-11-23.
- Artefacto Windows da #323: artifact ID `13705765600`, SHA-256 acima.
- Amanhã no PC: instalar build Windows mais recente; atualizar extensão unpacked v0.3.2; configurar DGM_CHROME_EXTENSION_ID exato no processo API; pair com código de 5 min; abrir tabs autenticadas dos seis providers e ativar unattended recovery. Captura percorre links visíveis e conteúdo DOM visível, não envia mensagens e não prova full history. Claude/DeepSeek/Qwen requerem aceitação live DOM antes de assumir cobertura.
- Após import: chamar reindex com cursores independentes até ambos null; depois verify em lotes até não haver pending/rate_limited/unavailable. Consultar GET list para relatório de URLs e provenance.
- Validação local no PC do utilizador ainda não ocorreu. Não afirmar captura integral até comparar amostras com UI original. Não usar browser consultation Claude ainda; Claude é capture-only.


### Build consolidado de main após #323 — 2026-11-09 19:46 UTC
- Main confirmado em e5ab7a27bc2215945c37e57cd0c2a5b8c95e23d7, contendo #321 + #322 + #323.
- Workflow Windows Executable Build no main: run 42686323637, ainda em instalação de dependências; não existe artefacto consolidado final ainda.
- Run anterior no main após #322 merge: 42685797726 completou build/deep check/upload SUCCESS mas antecede #323, portanto não inclui o índice GitHub.
- Não recomendar o artefacto 42685797726 para o objetivo completo; aguardar run 42686323637 para Windows package com as três features integradas.


### Estado consolidado posterior — 2026-11-09 20:00 UTC
- PR #321 (contexto de missão) merged; PR #322 (Claude como provider de recuperação histórica) merged; PR #323 (GitHub repository reference vault) merged.
- PR #320 fechada sem merge, substituída pela versão limpa #323.
- PR #324 fechada sem merge por conter histórico redundante/divergente; substituída pela PR limpa #325.
- PR #325 aberta: https://github.com/AndreVazao/DGM-MAT/pull/325; branch feat/claude-browser-conversation-capture-v2. Diff final apenas dois ficheiros: browser_extension/content.js e tests/browser_extension/test_content_capture.js. Corrige sourceIdForUrl para reconhecer apenas /chat/{conversation_id} e /project/{project_id}/chat/{conversation_id}, extrair o ID do chat (não do projeto) e rejeitar rotas sem conversa. Testes de regressão para projetos e rotas inválidas.
- HEAD #325 7fb9ebba8a1bdc820ed3857cdad1bec3c72c559e: Focused PR Validation SUCCESS; Chrome Extension Validation SUCCESS; installer digest gate SUCCESS; Windows Executable Build IN_PROGRESS às 20:00 UTC.
- PR #325 é apenas a correção do parser e testes; a integração base Claude veio de #322. Live capture ainda depende de aceitação no Chrome autenticado do PC. O arquivo é visible DOM snapshot, full_history_verified=false; não afirmar recuperação total.


### PR #325 — revisão de fixture e CI final — 2026-11-09 20:01 UTC
- A revisão aprofundada detetou que Claude pode expor um wrapper chat-message e um nó user-message/assistant-message aninhado; o adaptador agora mantém apenas o nó reconhecido mais profundo, evitando arquivar o mesmo turno duas vezes.
- Primeiro teste novo falhou porque a fixture de scroll substituía os nós aninhados por mensagens genéricas (7 em vez de 1); corrigida a fixture para manter o DOM aninhado estável durante o scroll. Não era falha do algoritmo de deduplicação.
- HEAD #325: 51c1cc3a59c96df78dc76986ee01b091b6cd7a1b. Focused PR Validation run 42688849671 SUCCESS; Chrome Extension Validation run 42688848871 SUCCESS. Windows Executable Build run 42688849603 IN_PROGRESS.
- Diff permanece limitado a browser_extension/content.js e tests/browser_extension/test_content_capture.js (2 ficheiros). Aguardar Windows build antes de merge.


### PR #325 — Claude parser e deduplicação integrados — 2026-11-09 20:15 UTC
- PR #325 merged por squash: https://github.com/AndreVazao/DGM-MAT/pull/325
- Merge commit e HEAD de `main` confirmados: `de675c3eff956bf132107e84af059dbd047c4a0a`.
- HEAD validado: `51c1cc3a59c96df78dc76986ee01b091b6cd7a1b`.
- Focused PR Validation run `42688849671`: SUCCESS.
- Chrome Extension Validation run `42688848871`: SUCCESS.
- Windows installer digest gate: SUCCESS.
- Windows Executable Build run `42688849603`: SUCCESS. Build, deep executable validation, final assertions e upload de artefactos concluídos.
- Artefacto Windows `DGM-MAT-Windows-3.12-301fd03`, artifact ID `13706476865`, 111,290,075 bytes, SHA-256 `c1f7a99523fb194a91dae165b690e4c27991055b4fdfea44167be418bec88617`, expira 2027-02-07.
- Correção: sourceIdForUrl Claude reconhece /chat/{conversation_id} e /project/{project_id}/chat/{conversation_id}, usando sempre o ID da conversa e rejeitando rotas sem chat. Seletores eliminam wrappers chat-message quando existe nó role-specific aninhado, evitando duplicação.
- Fixtures determinísticas cobrem rota normal, rota de projeto, rotas inválidas e DOM aninhado. O teste de scroll mantém a fixture aninhada estável.
- PR #318 também confirmado merged (merge commit `725b8cb3d817c7b2d4faa8999cee6246aaf798f1`), integrando histórico durável, pesquisa paginada, nova conversa e persistência passiva no cockpit.
- CodeRabbit foi skipped por exigir revisão manual no repositório OSS; não houve parecer automatizado.
- Limite: build CI não instala no PC nem prova captura live. Claude continua visible-DOM-only, partial snapshot (`full_history_verified=false`) e capture-only; sessão Chrome autenticada emparelhada no PC ainda exige aceitação real.
- Issue #313 atualizada com merge, checks, artefacto e limites. O índice GitHub extrai automaticamente URLs quando conversas são arquivadas/importadas; backfill histórico exige reindex; verificação pública continua manual em lotes bounded (não existe worker periódico).


### PR #326 — opt-in explícito para trabalho de fundo no Chrome — 2026-11-09 20:21 UTC
- PR aberta: https://github.com/AndreVazao/DGM-MAT/pull/326
- Branch `fix/browser-recovery-opt-ins-default-off`; HEAD atual `f52f3b7795b2421b735cc87108b933a1d57d07a2`.
- Auditoria pós-#325 encontrou divergência real: `AUTO_KEY` e `BROWSER_QUEUE_AUTO_KEY` eram inicializados a `true`, apesar do runbook exigir autonomia desligada. Pairing podia iniciar recuperação e polling da fila de tarefas aprovadas sem opt-in explícito.
- Alterações propostas: defaults OFF para recuperação unattended, fila de missões aprovadas e consulta externa; `onInstalled` limpa as três flags e os alarms em install/update; versão da extensão passa de 0.3.2 para 0.3.3; README atualizado; teste estático passa a exigir OFF e reset dos alarms.
- Focused PR Validation run `42691810610`: SUCCESS.
- Chrome Extension Validation run `42691810681`: SUCCESS (inclui JS syntax, fixtures, security/API regressions e pacote instalável).
- Windows installer digest gate: SUCCESS no run focused `42691810610`.
- Windows Executable Build run `42691810700`: IN_PROGRESS na instalação de dependências à última consulta; não integrar até concluir build/deep check/upload.
- Um run Chrome anterior no commit intermédio falhou porque o teste antigo ainda esperava defaults true; teste atualizado no HEAD final e revalidação passou. CodeRabbit skipped por revisão manual obrigatória no repositório OSS.
- Issue #313 atualizada com a divergência, correção, HEAD e CI.
- Pairing sozinho não inicia tarefas. A recuperação manual de um provider permanece disponível. A fila do browser só reclama tarefas já aprovadas no servidor; não cria/aprova tarefas. Após cada atualização Chrome, o operador deve reativar explicitamente os controlos pretendidos.
- Aceitação live em Chrome autenticado no PC continua por executar; CI não equivale a instalação nem a captura real.


### PR #326 merged + PR #327 automatic GitHub reference verification — 2026-11-09 20:39 UTC
- PR #326 merged: `9df4120a91c91fe8206389ad44d67506182144a3`. Extension v0.3.3. Unattended recovery, approved mission queue and external consultation are OFF by default and reset OFF on every install/update; alarms cleared. Manual provider recovery remains available. Tests: Focused PR Validation and Chrome Extension Validation success; Windows Executable Build run `42691810700` success.
- Windows artifact for #326: `DGM-MAT-Windows-3.12-e1abcf4`, ID `13708570151`, 111,290,068 bytes, SHA-256 `da799541842ef1fb27f182964cb0a1646655a7065dd0502f1fcfd5afd4da7a58`, expires 2027-02-07.
- PR #327 opened: https://github.com/AndreVazao/DGM-MAT/pull/327, branch `feat/bounded-github-reference-auto-verifier`, current HEAD `3f72b7cdb054873e108c0eb2a37a30bc49349cd5`.
- Worker starts with API lifecycle, waits 15 seconds then verifies max 5 indexed refs per 30 minutes; config interval 300–86400 seconds, batch 1–10, timeout 5 seconds. Public unauthenticated GitHub REST only; owner/repo sent, never transcript body, credentials, browser cookies or provider sessions. Disable via `DGM_GITHUB_REFERENCE_VERIFIER_ENABLED=0`. Logs bounded cycles/failures and stops on API shutdown.
- Existing verifier query improved to pending-first, then oldest updated retry, preventing repeated unavailable/rate-limited rows starving new references.
- Added tests for default enable/disable, bounded interval/batch, run_once and disabled worker, plus regression ensuring pending refs are processed before retry rows. Added operator docs `docs/recovery/GITHUB_REFERENCE_VERIFIER.md`.
- PR #327 Focused PR Validation run `42694772555`: SUCCESS. Chrome Extension Validation run `42694772667`: SUCCESS. Windows Executable Build run `42694772586`: IN_PROGRESS at dependency installation as of 20:39 UTC. Do not merge until it passes.
- Issue #313 updated. Historical conversations still need bounded paginated reindex; no automatic historical backfill is claimed. Live paired Chrome acceptance and local PC installation remain outstanding.


- Post-merge verification of PR #326 on `main`: Windows Executable Build run `42694352617` SUCCESS; artifact `DGM-MAT-Windows-3.12-9df4120`, ID `13709335882`, 111,290,519 bytes, SHA-256 `b4c201f82379b039a27e9532b0fd824ee23d287d3e8bc363aa634fea00aa02a0`, expires 2027-02-07.


### PR #327 merged — bounded automatic GitHub reference verifier — 2026-11-09 20:42 UTC
- PR #327 merged into `main`: `313e8054e1854a76f99fd23662ae9d29e95a2b22`.
- Final PR HEAD `3f72b7cdb054873e108c0eb2a37a30bc49349cd5`: Focused PR Validation run `42694772555` SUCCESS; Chrome Extension Validation run `42694772667` SUCCESS; Windows installer digest gate SUCCESS; Windows Executable Build run `42694772586` SUCCESS. CodeRabbit skipped because manual review is required for this OSS repository.
- Windows artifact `DGM-MAT-Windows-3.12-2ed3187`, ID `13708423432`, 111,295,465 bytes, SHA-256 `755e5750ab77254c0539667f2f2233c861328a28ffd64c1a66d6eac4d7e77ce0`, expires 2027-02-07.
- API lifecycle now starts a daemon worker 15 seconds after startup and verifies max 5 indexed references every 30 minutes (hard batch cap 10; per-request timeout 5 seconds). Only unauthenticated public GitHub repo metadata is sent; no conversation text, tokens, provider cookies or browser sessions. `DGM_GITHUB_REFERENCE_VERIFIER_ENABLED=0` disables it.
- Selection prioritizes pending refs and rotates retries by oldest update to prevent retry starvation. Failures logged and retried on later cycles; shutdown signals worker. Docs: `docs/recovery/GITHUB_REFERENCE_VERIFIER.md`.
- Existing historical Vault/legacy recovery archives still require paginated reindex; new conversation archive/import automatically extracts links. No automatic historical backfill claim.
- Post-merge Windows build run `42695402137` for main HEAD `313e8054...` is queued; PR artifact above is already fully validated and available.
- Issue #313 updated. Local PC install and live paired/authenticated Chrome acceptance remain outstanding.
