# DGM-MAT — Checkpoint: fila persistente de intervenção humana
Data: 2026-10-10

## Implementado nesta etapa
- Criado `core/organization/human_intervention_queue.py` no repo `AndreVazao/DGM-MAT`.
- Criado `tests/organization/test_human_intervention_queue.py`.
- SQLite WAL, conexões por operação, pedidos duráveis, expiração, índice único parcial para missão+passo ativos, decisões ligadas a missão/passo e de uso único, transição de verificação antes de fechar como RESUMED/CANCELLED/BLOCKED.
- O componente guarda metadados operacionais delimitados e não oferece campos dedicados para segredos nem notas livres na decisão. Não tem endpoint HTTP/WebSocket; quem cria pedidos continua responsável por não inserir segredos em `reason`/`instructions`.
- Teste dedicado da fila: 7/7 passou. Bateria focada final após revisão do código: 15/15 passou, incluindo autenticação local, sistema de missões e contrato entre processos. `compileall` e `git diff --check` passaram.

## Estado honesto
**Componente local implementado; integração end-to-end pendente.** Não está ligado ao MissionEngine, não altera estado da missão, não notifica o telefone, não liberta workers e não retoma automaticamente. Não afirmar que o cockpit ou a autenticação global já estão seguros/implementados.

## Segurança obrigatória
- Manter API loopback-only até enforcement global de auth HTTP/WebSocket, emparelhamento, scopes, identidade, revogação, anti-replay e migração de clientes.
- CAPTCHA/MFA manual. Nunca colocar passwords, OTPs, cookies ou tokens no LLM, bus, logs, base de dados ou memória.
- Aprovação humana não implica repetição automática de ação externa incerta; verificar estado real.
- FREE-ONLY / PAID-DENY. Não modificar `C:\\ProgramasGodMode\\DGM-MAT-FULL-MIRROR`.

## Próximos passos
1. Confirmar resultado de `tests/organization/test_human_intervention_queue.py`, `tests/security/test_local_auth_api.py`, `tests/autonomy/test_mission_system.py` e `tests/contracts/test_cross_process_mission.py`.
2. Corrigir regressões antes de integrar.
3. Integrar checkpoint/estado WAITING_FOR_USER no MissionEngine e libertar workers enquanto tarefas independentes prosseguem.
4. Fazer testes de concorrência e recuperação após reinício.
5. Só depois tratar auth global HTTP/WebSocket e cockpit móvel.
6. Manter descoberta Tailscale/Vercel e dashboard multi-PC como fases posteriores; Vercel é rendezvous, não túnel.
