# Ultima Sessao - Baribudos Studio

## Data
2026-05-01

## O que foi feito
- Analisado o repo `AndreVazao/baribudos-studio`.
- Confirmado backend FastAPI.
- Criado servico de memoria persistente.
- Criado router `/api/persistent-memory`.
- Ligado router e inicializacao no `main.py`.
- Adicionado `storage/memory/` ao `.gitignore`.
- Criada documentacao `docs/PERSISTENT_MEMORY.md`.
- Atualizada memoria privada `andreos-memory`.

## Proximo passo
Criar interface visual no dashboard do Studio para operar a memoria sem usar chamadas manuais de API.



## 2026-11-18 — Checkpoint operacional

- Consultados os repositórios ativos, PRs, issues, CI e deployments relevantes.
- PR Studio #52: 2 commits à frente de main, 0 atrás; CI #529 success; permanece Draft por ser apenas política-alvo documental.
- PR Studio #56: 8 commits à frente, 0 atrás; CI #577 e Distribution Hub Smoke #65 success; comentário de revisão aberto sobre validação real de assets e tipo `age`.
- PR Studio #58 integrada em main no commit `30eb91ae09c1a284f8a2743fbe282d6dbadd1c66`; Studio CI #578 passou. A roadmap atualizada está em main.
- P0 de segurança continua sem alteração de runtime: CORS wildcard+credentials, /storage estático e falta de auth global. Issue #43 continua a exigir matriz handler-to-service.
- Repositórios históricos primary/home-edition verificados e preservados (`archived=false`).
- Nenhuma migração de autenticação, alteração de CORS, storage, dados ou credenciais foi feita.
