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

