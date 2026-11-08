# DGM-MAT — Recuperação e consulta gratuita por browser
**Data de atualização:** 2026-11-08 16:40 UTC  
**Estado:** correção de privilégio mínimo da extensão validada por Focused #722, Chrome Extension #314 e Windows Build #306; artefacto atual `fa98b61`; runbook e auditoria atualizados no head documental `b295662a`; Snyk limitado por quota; aceitação local Windows 10/Chrome pendente; PR #283 aberta e não integrada.

## Repositório e PR
- Repositório: https://github.com/AndreVazao/DGM-MAT
- Branch de consolidação: `recovery/legacy-branch-consolidation-2026-11-07`
- PR: https://github.com/AndreVazao/DGM-MAT/pull/283
- Head de código funcional atual: `739edfc16c05b27429639d142fd85d016189f2b1` (scope dedicado `browser-consult-control` e teste integrado).
- Head de teste atual: `c10d2a3c1e489bb9c6eabe820a9438bd8ff3576d` (corrige expectativa de emparelhamento; sem alterações ao runtime relativamente a `739edfc`).
- Head documental atual da PR: `4cbf2d9ec03ad4ddd2fa197a06dc8a6e253ad2af` (runbook e relatório atualizados com artefacto Build #306, scopes e nomes corretos do ZIP/sidecars).
- Base: `main` em `c009c512593f16ee1bf085012fa700e4352433fe`.
- Estado: aberta, não merged; 86 commits, 19 ficheiros alterados.

## Auditoria de branches antigas
1. `feat/free-tier-browser-ai-consult-2026-11-05` — módulo de consulta SQLite/API preservado; hooks antigos de registo de rotas e segurança arquivados como snapshots.
2. `feat/browser-recovery-deepseek-qwen-2026-11-06` — obsoleta para a recuperação: DeepSeek/Qwen e conteúdo de extensão mais recente já existem no main.
3. `feat/telescope-metadata-only-2026-11-03` — inventário de fontes e Telescope metadata-only já integrados.
4. `feat/external-agent-readiness-probe-2026-11-03` — probe mais recente já integrado.
5. `feat/browser-mission-queue-v1` — fila/operador atuais já substituem o ramo; o popup antigo tinha envio direto que contornava aprovação server-side e foi excluído.

Nenhuma branch antiga foi apagada ou alterada. A branch nova preserva o material único de consulta e snapshots dos hooks antigos.

## Implementação na PR #283
- Store SQLite durável para consultas a ChatGPT, Grok, Gemini, DeepSeek e Qwen.
- Prompts limitados, minimizados e sujeitos a padrões de redacção de segredos; cooldown e deduplicação.
- Estados de aprovação explícita: `PENDING_APPROVAL` antes de o browser poder reclamar a tarefa.
- Rotas com autenticação de sessão local e classificação de scopes: a extensão emparelhada recebe apenas `browser-consult-control` para status/enqueue/approve e `browser-capture` para claim/result/block; nunca recebe o scope geral `operator`.
- Claim token aleatório de utilização única, comparado em tempo constante e invalidado após conclusão/bloqueio.
- Extensão Chrome usa apenas separadores autenticados já abertos e UI visível; polling separado e serializado com o operador de missões.
- Popup para criar pedido, atestar que as contas são gratuitas, aprovar cada envio individualmente e acompanhar estado.
- Opt-in da extensão desligado por defeito. Reinício do service worker bloqueia claims in-flight como interrompidos, sem replay automático.
- Respostas ficam como sugestões externas não verificadas; não executam comandos nem alteram repositórios.
- AutoHelp opcional pode recorrer à fila browser quando o DGM-HUB não tem fornecedor gratuito pronto. Exige três flags explícitas e aguarda aprovação no popup; a resposta concluída é anexada à conversa mobile ligada, marcada como não verificada.

## Flags de ativação
Manter todas desligadas até validação Windows/Chrome:
- `DGM_BROWSER_CONSULT_ENABLED=0`
- `DGM_BROWSER_CONSULT_FREE_CAPACITY_CONFIRMED=0`
- `DGM_AUTONOMY_HELP_BROWSER_CONSULT_ENABLED=0`
- Opt-in de consulta no popup: desligado por defeito.

A lista `DGM_BROWSER_CONSULT_FREE_PROVIDERS` só deve conter fornecedores cujas contas foram confirmadas pelo operador como gratuitas. O sistema não consegue provar o plano da conta.

## Correção de segurança — scope real da extensão (2026-11-08)

A revisão encontrou que a sessão emparelhada recebia apenas `browser-capture`, mas o popup chamava rotas de status/enqueue/approve classificadas como `operator`; essas operações devolveriam HTTP 403. Corrigido com o scope estreito `browser-consult-control`, atribuído pelo servidor à extensão junto com `browser-capture`. O token não inclui `operator`.

- Teste integrado: sessão real da extensão consegue ler status, criar e aprovar consulta; continua a receber HTTP 403 numa rota geral de operador.
- `tests/api/test_extension_pairing_origin.py` atualizado para validar os dois scopes e ausência de `operator`.
- Chrome Extension Validation #313 falhou apenas pela expectativa antiga; corrigido e repetido com #314.

## Validação do código e artefacto Windows

### Head de implementação
Commit validado pelos workflows: `042be2354a82efc3659661f1e85197c9a917692b`.
- Focused PR Validation #713: **SUCCESS** (run `42475479166`).
- Chrome Extension Validation #305: **SUCCESS** (run `42475479119`).
- Windows Executable Build #297: **SUCCESS** (run `42475479161`) — build, deep executable check, final build assertions e upload concluídos.
- Artefacto: `DGM-MAT-Windows-3.12-5f31bf7` (111,238,422 bytes).
- Digest SHA-256 do artefacto GitHub: `8b84cc0a61e36f30d370ca18c285effc7d89dad24cc40293d667003b63b2ca7b`.
- Criado em 2026-11-08 11:26:44 UTC; expira em 2027-02-06 11:22:40 UTC.
- Run Windows: https://github.com/AndreVazao/DGM-MAT/actions/runs/42475479161

### Head funcional com scope corrigido e artefacto atual
- Código: `739edfc16c05b27429639d142fd85d016189f2b1`; teste-only head: `c10d2a3c1e489bb9c6eabe820a9438bd8ff3576d`.
- Focused PR Validation #721: **SUCCESS** (run `42500111864`), 30 testes aprovados.
- Chrome Extension Validation #314: **SUCCESS** (run `42500577041`), 77 regressões browser/API aprovadas; JavaScript fixtures, manifest, Bandit e `pip-audit` passaram; nenhum advisory conhecido nas dependências focadas auditadas.
- Focused PR Validation #722: **SUCCESS** (run `42500577087`), incluindo teste de emparelhamento atualizado e Windows installer digest gate.
- Windows Executable Build #306: **SUCCESS** (run `42500577090`), incluindo deep executable check, final assertions e upload.
- Artefacto atual: `DGM-MAT-Windows-3.12-fa98b61` (111,238,942 bytes).
- Digest SHA-256 do arquivo de artefacto GitHub: `eee9c6a2d890ef23d9aa4dd597914b34b487089dff108b03d95035351fa86a21`.
- Criado em 2026-11-08 16:38:36 UTC; expira em 2027-02-06 16:34:25 UTC.
- URL: https://github.com/AndreVazao/DGM-MAT/actions/runs/42500577090
- Artefacto Chrome: `DGM-MAT-Chrome-Conversation-Recovery` (22,816 bytes; digest `6d02ae8686f9352518906d655a0a78141135c602d17365c1947c4fc2e4a7eac9`; run `42500577041`; expira em 2026-11-22 16:34:45 UTC).
- O digest GitHub identifica o ZIP do artefacto, não o EXE. Para verificar o executável, usar o sidecar `publish/DGM-MAT.exe.sha256` conforme o runbook.
- As alterações `c10d2a3` e os commits documentais seguintes não alteram o runtime compilado.

**Check externo Snyk:** estado `error`, mensagem “You have used your limit of private tests”. É esgotamento de quota; não há análise Snyk aprovada. O `pip-audit` do workflow Chrome terminou sem vulnerabilidades conhecidas no conjunto focado de dependências auditado; não substitui uma análise integral do ambiente.

**Limite importante:** CI e validação automatizada do executável estão verdes. Ainda não foi feita instalação/execução real no Windows 10 do operador, nem E2E com as cinco contas gratuitas. Não declarar aceitação local nem segurança Snyk aprovada.

## Runbook de aceitação Windows 10 + Chrome
- Ficheiro: `docs/recovery/WINDOWS10_CHROME_ACCEPTANCE_RUNBOOK_2026-11-07.md` na branch da PR #283.
- Link: https://github.com/AndreVazao/DGM-MAT/blob/recovery/legacy-branch-consolidation-2026-11-07/docs/recovery/WINDOWS10_CHROME_ACCEPTANCE_RUNBOOK_2026-11-07.md
- Inclui download do artefacto correto, verificação separada do ZIP exterior/ZIP de distribuição/executável, pré-verificações read-only, backup/manifesto através do instalador existente, rollback, primeiro arranque sem consultas, instalação/emparelhamento da extensão e consulta manual individual com aprovação.
- Runbook atualizado para o artefacto Build #306 `DGM-MAT-Windows-3.12-fa98b61` (111,238,942 bytes; digest GitHub `eee9c6a2d890ef23d9aa4dd597914b34b487089dff108b03d95035351fa86a21`; expira 2027-02-06 16:34:25 UTC).
- Inclui verificação dos scopes `browser-capture` e `browser-consult-control`, sem `operator`, e caminhos corretos `package/scripts/...` para instalador, rollback e extensão Chrome.
- O runbook não autoriza instalação, ativação de flags, envio ou merge; as flags ficam desligadas até aprovação explícita.

## Próximos passos
1. Obter aceitação Windows 10 + Chrome: instalar o artefacto atual e testar uma consulta manualmente aprovada, começando por um único fornecedor gratuito.
2. Confirmar login/quota/UI mismatch e interrupção sem replay; depois testar os restantes fornecedores que o operador confirmar como gratuitos.
3. Quando a quota Snyk estiver disponível, repetir o check ou executar uma análise equivalente autorizada.
4. Confirmar que os resultados aparecem como não verificados e que AutoHelp só enfileira com as três flags explicitamente ligadas.
5. Só depois considerar merge da PR #283.
6. As branches antigas auditadas permanecem intactas. Apagá-las apenas após confirmação de que todo o material único está preservado e decisão explícita do proprietário; preservar histórico de commits/PRs.

## Limites
Esta implementação ainda não está ativa por defeito nem foi integrada em main. A integração AutoHelp cobre o fallback do runtime mobile quando o DGM-HUB não tem fornecedor gratuito pronto; a consulta manual pela extensão está disponível através do popup. Não assumir integração automática de consulta em todos os estados de bloqueio do MissionEngine.



## Atualização documental final — head PR #283 `4cbf2d9e` (2026-11-08)
- Runbook Windows 10 + Chrome aponta para o artefacto Windows Build #306 `DGM-MAT-Windows-3.12-fa98b61`, confirma os nomes corretos do ZIP de distribuição e respetivo `.sha256`, e verifica o executável através do sidecar.
- Relatório de consolidação identifica Builds #300 e #305 como históricos/supersedidos pelo #306, evitando usar artefactos antigos.
- Runbook confirma que a extensão deve receber `browser-capture` e `browser-consult-control`, sem `operator`.
- Relatório de recuperação corrige a descrição da integração: router registado em `api_server.py`, rotas classificadas em `security_policy.py`, snapshots antigos apenas como referência histórica.
- Commits documentais posteriores ao head de teste `c10d2a3` não alteram código nem o executável.
- Nenhuma branch antiga foi apagada; PR #283 continua aberta e não integrada.
- Aceitação real no Windows 10/Chrome com contas dos fornecedores continua pendente.


## Atualização de validação — 2026-11-08 16:46 UTC

O head documental da PR #283 avançou para `22755606d8b35ca398e157680fbbeeaee8d1bd1c`. O código/runtime permanece no head de teste `c10d2a3c1e489bb9c6eabe820a9438bd8ff3576d`; os commits posteriores foram apenas documentação.

- Focused PR Validation #726: **SUCCESS**, run `42501213531`; regressões afetadas e Windows installer digest gate passaram.
- Chrome Extension Validation #318: **SUCCESS**, run `42501213530`; sintaxe JS, fixtures, rejeição de envio direto não aprovado, manifest, auditoria focada de dependências, Bandit, regressões browser/API e empacotamento passaram.
- Windows Executable Build #310: **SUCCESS**, run `42501213553`; todos os 15 passos passaram, incluindo validação do instalador, deep executable check, assertions finais e upload.
- Artefacto Windows atual: `DGM-MAT-Windows-3.12-70a7fb7`, 111,237,062 bytes; SHA-256 do ZIP exterior GitHub `03d9a6b6c375ecbb49ce38a3fd4bca00f515b21b2e2a18d481ffd03abe9bc601`; criado 2026-11-08 16:46:11 UTC; expira 2027-02-06 16:42:00 UTC.
- Run: https://github.com/AndreVazao/DGM-MAT/actions/runs/42501213553
- Digest GitHub refere-se ao ZIP exterior, não ao executável. Validar o EXE pelo sidecar `publish/DGM-MAT.exe.sha256` no artefacto extraído.
- Runbook Windows 10 + Chrome e relatório de recuperação foram atualizados na branch da PR com este artefacto e validações. A descrição da PR #283 também foi limpa para remover referências contraditórias a artefactos antigos.
- Snyk continua sem resultado limpo devido à quota privada anteriormente esgotada; Bandit e pip-audit passaram apenas nos respetivos âmbitos configurados.
- PR #283 continua aberta e não integrada. Aceitação local Windows 10/Chrome e E2E real dos fornecedores continuam pendentes. Flags desligadas. Nenhuma branch antiga foi apagada.
- Próximo passo: aceitação local com um fornecedor confirmado gratuito, aprovação manual e testes negativos. Não fazer merge nem apagar branches antes da evidência local e decisão explícita do André.


## Atualização final do checkpoint — 2026-11-08 16:50 UTC

- Head documental PR #283: `4f28754d769b38805ca554d3535a9358eae1cb6f`; código/testes validados permanecem em `c10d2a3c1e489bb9c6eabe820a9438bd8ff3576d`.
- Runbook corrigido para identificar corretamente o head de código/testes, o head documental e os artefactos Build #310 e Chrome Validation #318.
- Artefacto Chrome #318: `DGM-MAT-Chrome-Conversation-Recovery`, 22,820 bytes; digest `8d269c841ed888bc8d2bc0d5e3533ba4d7334a666063db5a70b04c8bb0d1c606`; expira 2026-11-22 16:42:23 UTC.
- Relatório de recuperação e descrição da PR #283 atualizados com os dois artefactos atuais e as três validações verdes (#726, #318, #310).
- PR permanece aberta, não merged; aceitação local Windows 10/Chrome pendente; Snyk sem resultado limpo por quota; flags desligadas; branches antigas intactas.


## Correção final de documentação — 2026-11-08

- O runbook foi revisto novamente para remover uma sequência de escape literal que tinha ficado na introdução e para não declarar incorretamente um head documental anterior como atual.
- Head documental da PR após esta correção: `67374de9f459c412f81028ef6473ca21f29c1116`.
- O conteúdo de código/testes validado continua no head `c10d2a3c1e489bb9c6eabe820a9438bd8ff3576d`; não houve alteração de runtime.
- Artefactos Windows #310 e Chrome #318, hashes, datas de expiração e links estão documentados. A PR permanece aberta e não integrada; aceitação local pendente.
