# DGM-MAT — cérebro primeiro: checkpoint persistente de missões e intervenção humana
Data: 2026-10-10

## Implementação local desta fase
- `MissionStatus` inclui `WAITING_FOR_USER` e `CANCELLED`.
- `MissionEngine` usa `HumanInterventionQueue` SQLite durável no armazenamento de tarefas.
- `request_human_intervention()` persiste pedido, missão, passo, validade e estado de checkpoint; coloca só a missão dependente em espera. `process_missions()` ignora a missão em espera sem bloquear a iteração das restantes missões nem aplicar-lhe timeout.
- A serialização da missão agora guarda subtarefas e os respetivos estados, agentes/IDs de tarefa e timestamps; o carregamento reconstrói as subtarefas após reinício.
- Gravação do JSON da missão é atómica via temporário, flush/fsync e replace.
- Reconciliação no arranque recupera pedido ativo criado antes de um crash entre a gravação SQLite e o checkpoint JSON.
- `resolve_human_intervention()` valida missão/pedido/passo e identidade do operador; rejeição/cancelamento termina como `CANCELLED`; `NEED_CONTEXT` abre pedido novo; aprovação só retoma se um chamador local de confiança confirmar o estado externo e fornecer evidência breve não sensível.
- A transição de retoma verificada grava primeiro um checkpoint `RESUME_VERIFIED_PENDING_FINALIZE`, finaliza a fila e depois muda a missão para `RUNNING`. O arranque recupera a transição se o processo cair entre estas gravações. Um claim `VERIFYING` interrompido sem checkpoint verificado volta a `RESPONSE_RECEIVED` e exige nova verificação.
- Nenhum endpoint HTTP/WebSocket, notificação móvel ou controlo remoto foi adicionado.

## Testes e estado
- Teste dedicado novo: `tests/autonomy/test_mission_human_intervention.py` cobre espera sem timeout, outras missões continuam scheduláveis, subtarefas sobrevivem a recriação do motor, decisão ligada ao operador, verificação obrigatória, cancelamento sem replay, recuperação de pedido órfão e recuperação de retoma/claim interrompidos.
- Bateria focada final após recuperação de crash: **22 testes aprovados**. Bateria alargada das suites `autonomy`, `organization`, `contracts` e `security`: **104 testes aprovados, 0 falhas**. `compileall` e `git diff --check` passaram.
- Documentação: `docs/architecture/MISSION_ENGINE_HUMAN_INTERVENTION_CHECKPOINTS.md`.

## Limites explícitos
- A fila e o motor são locais; ainda não há verifier de browser/serviço real integrado. O parâmetro `verified=True` só pode ser fornecido por um verificador local de confiança após confirmar o estado real. Não ligar isso a um endpoint público nem permitir que um cliente remoto o declare arbitrariamente.
- A missão retomada preserva o checkpoint, mas isso não significa que qualquer subtarefa pendente seja executada automaticamente; os workers/scheduler existentes continuam responsáveis pela execução real.
- CAPTCHA/MFA é sempre manual. Não colocar passwords, OTPs, cookies ou tokens no LLM, logs, memória, SQLite ou message bus.
- API loopback-only até autenticação global HTTP/WebSocket, pairing/scopes, revogação, anti-replay e migração dos clientes.
- FREE-ONLY / PAID-DENY; não alterar `C:\\ProgramasGodMode\\DGM-MAT-FULL-MIRROR`; sem GitHub Actions.

## Sequência pedida pelo utilizador
1. Cérebro: durabilidade, checkpoints, scheduler e intervenções humanas.
2. Cockpit PC: cliente local avançado, Core permanece independente e invisível em background.
3. APK Android: depois de auth/pairing/transport security, ligação privada por Tailscale e descoberta; Vercel só rendezvous, nunca túnel mágico.
