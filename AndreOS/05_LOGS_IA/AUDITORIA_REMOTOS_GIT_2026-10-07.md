# Auditoria de remotos Git locais — 2026-10-07

## Âmbito

Auditoria pelo Desktop Commander aos repositórios locais em C:\ProgramasGodMode, cruzando os remotos locais com os repositórios disponíveis em GitHub.

## Correções executadas

Foram encontrados remotos locais incorretos com o destino genérico:

https://github.com/AndreVazao/.git

Os remotos foram corrigidos para os repositórios correspondentes em GitHub nos seguintes projetos:

- DGM-Core-Backend
- DGM-Contracts
- DGM-Docs
- VAZAO-EVSE-Platform
- DGM-MAT-Agents
- DGM-MAT-Memory
- DGM-MAT-Media
- DGM-MAT-Marketplace
- DGM-MAT-Cluster
- VocalClaw_11Labs
- TruckFood
- SyntX-26-AI-hackathon
- RuView
- RabbitLLM
- DGM-Experimental
- DGM-Cockpit-Frontend
- n8nworkflows.xyz

## Validação

A pesquisa final aos ficheiros .git/config locais deixou de encontrar o URL genérico https://github.com/AndreVazao/.git.

DGM-Contracts foi ainda configurado para acompanhar explicitamente origin/main.

## Situações que não foram forçadas

- DGM-Core-Backend e DGM-Docs têm repos GitHub existentes mas sem histórico utilizável neste momento; não foi criado um commit artificial apenas para “sincronizar”.
- DGM-Contracts tem ficheiros __pycache__ não versionados; não foram adicionados nem apagados automaticamente.
- Não foi feito push indiscriminado de branches locais à frente ou árvores sujas.
- Não foi feito merge destrutivo.

## Regra operacional

A correção de remotes precede qualquer sincronização automática. Depois de o remote estar correto:

fetch → comparar HEAD/origin → pull --ff-only quando seguro → testar → documentar → commit → push.

## Memória

Este checkpoint é complementar a SYNC_GITHUB_DESKTOP_COMMANDER_2026-10-07.md e deve ser tratado como estado persistente da auditoria local/GitHub.
