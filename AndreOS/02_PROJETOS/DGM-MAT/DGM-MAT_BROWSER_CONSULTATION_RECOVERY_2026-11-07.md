# DGM-MAT — Recuperação e consulta gratuita por browser
**Data:** 2026-11-07  
**Estado:** implementação em revisão; não integrada no main.

## Repositório e PR
- Repositório: https://github.com/AndreVazao/DGM-MAT
- Branch de consolidação: `recovery/legacy-branch-consolidation-2026-11-07`
- PR: https://github.com/AndreVazao/DGM-MAT/pull/283
- Head registado neste checkpoint: `9386a1b12417392dc906223dab4aedf610176f6a`
- Base: `main` em `c009c512593f16ee1bf085012fa700e4352433fe`
- A PR está aberta e pronta para revisão; não foi feito merge.

## Auditoria de branches antigas
Branches analisadas:
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

## Validação conhecida
- Uma revisão anterior da PR teve Chrome Extension Validation verde e Focused PR Validation verde depois de corrigir problemas de prompt/deduplicação.
- Uma revisão intermédia revelou falhas reais: lookup sem `task_ref` e expectativa antiga de estado `FAILED_NO_RETRY`; foram corrigidas.
- No head deste checkpoint:
  - Focused PR Validation #702: **IN PROGRESS** — inclui os testes fail-closed de auditoria acrescentados na última revisão.
  - Chrome Extension Validation #294: **PENDING**.
  - Windows Executable Build #286: **IN PROGRESS**.
  - A revisão anterior #699 passou nos testes afetados; Chrome #291 também passou.
- Não declarar a revisão totalmente validada até o build Windows terminar e até existir aceitação E2E real em Windows 10 + Chrome.
- Não houve testes locais no PC Windows 10, nem aceitação E2E real com contas dos cinco fornecedores.

## Próximos passos
1. Confirmar CI verde no head mais recente da PR #283; corrigir regressões até ficar verde.
2. Validar Windows 10 + Chrome com uma consulta manualmente aprovada por fornecedor, confirmar login/quota/UI mismatch e interrupção sem replay.
3. Confirmar que os resultados aparecem como não verificados na conversa local e que o AutoHelp só enfileira quando as três flags estão explicitamente ligadas.
4. Só depois considerar merge da PR #283.
5. Após confirmar que a PR preserva todos os ficheiros únicos e snapshots, as cinco branches antigas auditadas podem ser apagadas pelo proprietário; preservar histórico de commits/PRs.

## Limites
Esta implementação ainda não está ativa por defeito nem foi integrada em main. A integração AutoHelp cobre o fallback do runtime mobile quando o DGM-HUB não tem fornecedor gratuito pronto; a consulta manual pela extensão está disponível através do popup. Não assumir ainda integração automática de consulta em todos os estados de bloqueio do MissionEngine.
