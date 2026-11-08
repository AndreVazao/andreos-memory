# DGM-MAT — Recuperação e consulta gratuita por browser
**Data de atualização:** 2026-11-08 16:27 UTC  
**Estado:** CI Focused/Chrome/Windows Build #716/#308/#300 verdes no head documental validado `75b6fa0`; artefacto `54e344e`; runbook e auditoria de branches atualizados no head atual `86974c5`; Snyk limitado por quota; aceitação local Windows 10/Chrome pendente; PR #283 aberta e não integrada.

## Repositório e PR
- Repositório: https://github.com/AndreVazao/DGM-MAT
- Branch de consolidação: `recovery/legacy-branch-consolidation-2026-11-07`
- PR: https://github.com/AndreVazao/DGM-MAT/pull/283
- Head de código/artefacto Windows validado: `042be2354a82efc3659661f1e85197c9a917692b`.
- Head documental com CI validado: `75b6fa0a7a09af645aa8ee80e39384a4858550b0`. Head documental atual da PR: `86974c54f26e7f6c81e9e46712f018dc69709fdb` (runbook e relatório de recuperação corrigidos; sem alterações de código após o build).
- Base: `main` em `c009c512593f16ee1bf085012fa700e4352433fe`
- Estado: aberta, não merged; 75 commits, 16 ficheiros alterados.

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
- Rotas com autenticação de sessão local e classificação de scopes: operador para criar/aprovar/consultar estado; extensão emparelhada para claim/result/block.
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

### Head documental atualizado
- Commit: `75b6fa0a7a09af645aa8ee80e39384a4858550b0`.
- Focused PR Validation #716: **SUCCESS** (run `42475905963`).
- Chrome Extension Validation #308: **SUCCESS** (run `42475905965`).
- Windows Executable Build #300: **SUCCESS** (run `42475905948`); job `build (3.12)` e todos os passos principais concluídos com sucesso, incluindo Build Executable, Validate Executable (Deep Check), Prepare Artifacts, Final Build Assertions e Upload Build Artifacts.
- Artefacto atual: `DGM-MAT-Windows-3.12-54e344e` (111,238,946 bytes).
- Digest SHA-256 do arquivo de artefacto GitHub: `f5d5abefe05dd14c40043484f4601eb90cdcad45ae034d31d71fd2eb7eee97d2`.
- Criado em 2026-11-08 11:32:45 UTC; expira em 2027-02-06 11:28:39 UTC.
- URL: https://github.com/AndreVazao/DGM-MAT/actions/runs/42475905948
- O digest acima identifica o ZIP de artefacto GitHub, não o executável. Para verificar o EXE, usar o sidecar `publish/DGM-MAT.exe.sha256` conforme o runbook.
- As alterações entre o head de implementação e o head documental validado são apenas documentação/runbook; os commits seguintes até `86974c5` também só alteram documentação e não mudam o código executável.

**Check externo Snyk:** estado `error`, mensagem “You have used your limit of private tests”. É esgotamento de quota; não há análise Snyk aprovada.

**Limite importante:** CI e validação automatizada do executável estão verdes. Ainda não foi feita instalação/execução real no Windows 10 do operador, nem E2E com as cinco contas gratuitas. Não declarar aceitação local nem segurança Snyk aprovada.

## Runbook de aceitação Windows 10 + Chrome
- Ficheiro: `docs/recovery/WINDOWS10_CHROME_ACCEPTANCE_RUNBOOK_2026-11-07.md` na branch da PR #283.
- Link: https://github.com/AndreVazao/DGM-MAT/blob/recovery/legacy-branch-consolidation-2026-11-07/docs/recovery/WINDOWS10_CHROME_ACCEPTANCE_RUNBOOK_2026-11-07.md
- Inclui download do artefacto correto, verificação separada do ZIP exterior/ZIP de distribuição/executável, pré-verificações read-only, backup/manifesto através do instalador existente, rollback, primeiro arranque sem consultas, instalação/emparelhamento da extensão e consulta manual individual com aprovação.
- Runbook atualizado com o artefacto `DGM-MAT-Windows-3.12-54e344e` e caminhos corretos `package/scripts/...` para instalador, rollback e extensão Chrome.
- O runbook aponta agora para o artefacto Build #300 `DGM-MAT-Windows-3.12-54e344e` (111,238,946 bytes; digest GitHub `f5d5abefe05dd14c40043484f4601eb90cdcad45ae034d31d71fd2eb7eee97d2`; expira 2027-02-06 11:28:39 UTC). O runbook não autoriza instalação, ativação de flags, envio ou merge; as flags ficam desligadas até aprovação explícita.

## Próximos passos
1. Obter aceitação Windows 10 + Chrome: instalar o artefacto atual e testar uma consulta manualmente aprovada, começando por um único fornecedor gratuito.
2. Confirmar login/quota/UI mismatch e interrupção sem replay; depois testar os restantes fornecedores que o operador confirmar como gratuitos.
3. Quando a quota Snyk estiver disponível, repetir o check ou executar uma análise equivalente autorizada.
4. Confirmar que os resultados aparecem como não verificados e que AutoHelp só enfileira com as três flags explicitamente ligadas.
5. Só depois considerar merge da PR #283.
6. As branches antigas auditadas permanecem intactas. Apagá-las apenas após confirmação de que todo o material único está preservado e decisão explícita do proprietário; preservar histórico de commits/PRs.

## Limites
Esta implementação ainda não está ativa por defeito nem foi integrada em main. A integração AutoHelp cobre o fallback do runtime mobile quando o DGM-HUB não tem fornecedor gratuito pronto; a consulta manual pela extensão está disponível através do popup. Não assumir integração automática de consulta em todos os estados de bloqueio do MissionEngine.


## Atualização de documentação — head PR #283 `86974c54` (2026-11-08)
- Runbook Windows 10 + Chrome atualizado para o artefacto exato do Windows Build #300 (`54e344e`), incluindo nome do ZIP interno, tamanho, digest do arquivo GitHub, commit e expiração.
- Relatório de consolidação corrigido: a API de consulta está agora registada em `api_server.py` e as rotas estão classificadas em `security_policy.py`; os snapshots antigos são apenas referência histórica, não integração pendente.
- As alterações `ba28b513` e `86974c54` são documentação; não alteram código nem invalidam o binário produzido no head `75b6fa0`.
- Não foram acionados novos workflows por estes commits documentais; os três workflows verdes permanecem associados ao head documental `75b6fa0`.
