# DGM-MAT — Recuperação e consulta gratuita por browser
**Data:** 2026-11-07  
**Estado:** três workflows essenciais verdes no commit de código/artefacto `a83f3a4`; runbook Windows 10/Chrome corrigido; check externo Snyk continua limitado por quota; aceitação local pendente; PR #283 aberta e não integrada.

## Repositório e PR
- Repositório: https://github.com/AndreVazao/DGM-MAT
- Branch de consolidação: `recovery/legacy-branch-consolidation-2026-11-07`
- PR: https://github.com/AndreVazao/DGM-MAT/pull/283
- Head de código/artefacto Windows validado: `a83f3a4148ad7226e42240734fcfba13d844b16b`.
- Head documental mais recente da branch da PR: `042be2354a82efc3659661f1e85197c9a917692b` (runbook Windows/Chrome e correção final dos caminhos de extração).
- Base: `main` em `c009c512593f16ee1bf085012fa700e4352433fe`
- Estado: aberta, não merged; 64 commits, 16 ficheiros alterados.

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
Commit validado pelos workflows: `a83f3a4148ad7226e42240734fcfba13d844b16b`.
- Focused PR Validation #707: **SUCCESS** (run `42424345722`).
- Chrome Extension Validation #299: **SUCCESS** (run `42424345700`).
- Windows Executable Build #291: **SUCCESS** (run `42424345706`) — build, deep executable check, final build assertions e upload concluídos.
- Artefacto: `DGM-MAT-Windows-3.12-145f01e` (111,239,092 bytes).
- Digest SHA-256 do artefacto GitHub: `5a66ca634fd5e71a0b825e79a78eb18b1845a0849ad0b9bfd981e74448508ef8`.
- Criado em 2026-11-07 23:18:13 UTC; expira em 2027-02-05 23:14:39 UTC.
- Run Windows: https://github.com/AndreVazao/DGM-MAT/actions/runs/42424345706
- **Check externo Snyk:** estado `error`, mensagem “You have used your limit of private tests”. É esgotamento de quota do serviço Snyk; não há análise Snyk aprovada.

**Limite importante:** os três workflows essenciais estão verdes para o commit de código/artefacto `a83f3a4`. O status externo Snyk continua em `error` por quota. Os commits posteriores na branch da PR apenas corrigem documentação/runbook; não alteram o código do executável. Ainda não foi feita instalação/execução real no Windows 10 do operador, nem E2E com as cinco contas gratuitas. Não declarar aceitação local nem segurança Snyk aprovada.

## Runbook de aceitação Windows 10 + Chrome
- Ficheiro: `docs/recovery/WINDOWS10_CHROME_ACCEPTANCE_RUNBOOK_2026-11-07.md` na branch da PR #283.
- Link: https://github.com/AndreVazao/DGM-MAT/blob/recovery/legacy-branch-consolidation-2026-11-07/docs/recovery/WINDOWS10_CHROME_ACCEPTANCE_RUNBOOK_2026-11-07.md
- Inclui download do artefacto correto, verificação separada do ZIP exterior/ZIP de distribuição/executável, pré-verificações read-only, backup/manifesto através do instalador existente, rollback, primeiro arranque sem consultas, instalação/emparelhamento da extensão e consulta manual individual com aprovação.
- Artefacto atualizado: `DGM-MAT-Windows-3.12-145f01e`, run `42424345706`; o digest `5a66...` é do arquivo GitHub, não deve ser usado como SHA do executável. O SHA do EXE é lido do sidecar `publish/DGM-MAT.exe.sha256` e comparado com o ficheiro extraído.
- O runbook esclarece agora a extração do ZIP interno para `package/` e usa os caminhos corretos `package/scripts/...` para instalador, rollback e extensão Chrome, com separadores Windows normalizados no documento final.
- O runbook não autoriza instalação, ativação de flags, envio ou merge; as flags ficam desligadas até aprovação explícita.
- As validações CI essenciais concluíram SUCCESS no commit `a83f3a4`; as últimas alterações de documentação não alteram o binário.

## Próximos passos
1. Obter aceitação Windows 10 + Chrome: instalar o artefacto e testar uma consulta manualmente aprovada, começando por um único fornecedor gratuito.
2. Confirmar login/quota/UI mismatch e interrupção sem replay; depois testar os restantes fornecedores que o operador confirmar como gratuitos.
3. Quando a quota Snyk estiver disponível, repetir o check ou executar uma análise equivalente autorizada.
4. Confirmar que os resultados aparecem como não verificados e que AutoHelp só enfileira com as três flags explicitamente ligadas.
5. Só depois considerar merge da PR #283.
6. As cinco branches antigas auditadas permanecem intactas. Apagá-las apenas após confirmação de que todo o material único está preservado e decisão explícita do proprietário; preservar histórico de commits/PRs.

## Limites
Esta implementação ainda não está ativa por defeito nem foi integrada em main. A integração AutoHelp cobre o fallback do runtime mobile quando o DGM-HUB não tem fornecedor gratuito pronto; a consulta manual pela extensão está disponível através do popup. Não assumir integração automática de consulta em todos os estados de bloqueio do MissionEngine.
