# DGM-MAT — Recuperação e consulta gratuita por browser
**Data:** 2026-11-07  
**Estado:** CI e artefacto Windows concluídos no head atual; aceitação local Windows 10/Chrome pendente; PR #283 aberta e não integrada.

## Repositório e PR
- Repositório: https://github.com/AndreVazao/DGM-MAT
- Branch de consolidação: `recovery/legacy-branch-consolidation-2026-11-07`
- PR: https://github.com/AndreVazao/DGM-MAT/pull/283
- Head atual: `43e0befc9fbe493d591f92bcb0c985f9c8f83993`
- Base: `main` em `c009c512593f16ee1bf085012fa700e4352433fe`
- Estado: aberta, não merged; 61 commits, 15 ficheiros alterados; mergeability reportada como true, mas sem aceitação local.

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

## Validação do head atual
Head validado: `43e0befc9fbe493d591f92bcb0c985f9c8f83993`.
- Focused PR Validation #704: **SUCCESS**.
- Chrome Extension Validation #296: **SUCCESS**.
- Windows Executable Build #288: **SUCCESS** — build, deep executable check, final build assertions e upload concluídos.
- Artefacto: `DGM-MAT-Windows-3.12-2078d11` (111,235,672 bytes).
- SHA-256: `8edb2d56d6e6886fc2b8a9d09af41620825dd9217c0d273d7f4c0c3ddd6c3edb`.
- Criado em 2026-11-07 22:05:41 UTC; expira em 2027-02-05 22:01:16 UTC.
- Run: https://github.com/AndreVazao/DGM-MAT/actions/runs/42418598505

**Limite importante:** CI e criação do executável estão validados. Ainda não foi feita instalação/execução real no Windows 10 do operador, nem E2E com as cinco contas gratuitas. Não declarar aceitação local.

## Próximos passos
1. Obter aceitação Windows 10 + Chrome: instalar o artefacto e testar uma consulta manualmente aprovada, começando por um único fornecedor gratuito.
2. Confirmar login/quota/UI mismatch e interrupção sem replay; depois testar os restantes fornecedores que o operador confirmar como gratuitos.
3. Confirmar que os resultados aparecem como não verificados e que AutoHelp só enfileira com as três flags explicitamente ligadas.
4. Só depois considerar merge da PR #283.
5. As cinco branches antigas auditadas permanecem intactas. Apagá-las apenas após confirmação de que todo o material único está preservado e decisão explícita do proprietário; preservar histórico de commits/PRs.

## Limites
Esta implementação ainda não está ativa por defeito nem foi integrada em main. A integração AutoHelp cobre o fallback do runtime mobile quando o DGM-HUB não tem fornecedor gratuito pronto; a consulta manual pela extensão está disponível através do popup. Não assumir integração automática de consulta em todos os estados de bloqueio do MissionEngine.
