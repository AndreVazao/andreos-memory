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
