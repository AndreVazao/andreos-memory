# Última Sessão - God Mode

## Data
2026-05-07

## Resumo

A Phase 204 foi implementada, validada e merged. Esta fase adiciona **Autonomous IA Work Session Operator + Provider Work Pack Queue** ao core do God Mode.

A intenção operacional ficou ainda mais clara: o cérebro do God Mode corre no PC de casa e continua trabalho com IAs e projetos enquanto o Oner está na rua. O telemóvel é cockpit/popup de autorização e voz, não centro de trabalho manual constante.

## Clarificação importante da regra de operação

A regra correta é:

- O God Mode autónomo/runtime não pode fazer merge/release/deploy/update final sozinho sem aprovação explícita do Oner.
- Durante uma sessão de trabalho assistida, quando o Oner manda continuar/mergear depois de GitHub Actions verdes, o assistente pode fazer o merge para acelerar o desenvolvimento.
- O God Mode pode preparar missões, prompts, pacotes de trabalho, imports de resposta, diagnósticos e planos de PR.
- O God Mode deve operar em modo seguro quando o Oner está ausente/na rua: cria trabalho, fala com IAs por pacotes controlados e só pede aprovação para decisões bloqueantes/riscadas.
- O God Mode precisa de um relay móvel de permissões semelhante às aprovações do ChatGPT/GitHub: envia popup, espera, reenvia/sincroniza se não houver rede, e continua quando receber autorização.
- Para credenciais ou dados sensíveis, o popup deve pedir preenchimento/voz/ação manual pelo Oner; o God Mode não deve guardar tokens/passwords/cookies em memória normal.
- O modo condução deve aceitar voz, falar respostas curtas e evitar exigir toque no ecrã enquanto o Oner conduz.

## Phase 204 — Autonomous IA Work Session Operator + Provider Work Pack Queue

### Implementado

- Serviço: `backend/app/services/autonomous_ia_work_session_operator_service.py`
- Rota API: `backend/app/routes/autonomous_ia_work_session_operator.py`
- Página: `backend/app/routes/autonomous_ia_work_session_operator_frontend.py`
- Docs: `docs/orchestration/autonomous-ia-work-session-operator.md`
- Smoke workflow atual: `.github/workflows/phase204-autonomous-ia-work-session-operator-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase203-self-diagnosis-mission-control-smoke.yml`

### Endpoints novos

- `/api/autonomous-ia-work-session/status`
- `/api/autonomous-ia-work-session/policy`
- `/api/autonomous-ia-work-session/create-session`
- `/api/autonomous-ia-work-session/create-work-packet`
- `/api/autonomous-ia-work-session/create-packets-from-self-diagnosis`
- `/api/autonomous-ia-work-session/mark-packet-status`
- `/api/autonomous-ia-work-session/import-response`
- `/api/autonomous-ia-work-session/convert-response-to-tasks`
- `/api/autonomous-ia-work-session/create-provider-launcher-contract`
- `/api/autonomous-ia-work-session/packets`
- `/api/autonomous-ia-work-session/dashboard`
- `/api/autonomous-ia-work-session/package`

### Rotas visuais

- `/app/autonomous-ia-work-session`
- `/app/ia-work-operator`

### Funcionalidade

- Cria `ia_work_session`.
- Cria `ia_work_packet` por provider.
- Gera prompt controlado e sanitizado.
- Cria packets a partir do self-diagnosis queue.
- Permite importar resposta IA para Conversation Source Import Feed.
- Converte resposta importada em tarefas de revisão.
- Cria contrato de provider launcher sem login automático.
- Separa trabalho seguro de decisões que exigem Oner.

### Segurança / realidade

- `can_operate_while_oner_busy=true`.
- `can_send_without_manual_provider_gate=false`.
- `can_login_or_scrape_private_chats=false`.
- `can_merge_without_oner_approval=false`.
- Não guarda tokens, passwords, cookies, API keys ou segredos.
- Não automatiza login privado.
- Não faz scrape de conversas privadas.
- Não chama APIs pagas sem aprovação.
- Não faz merge/release/deploy autónomo.

### PR e validação

- PR #347 merged.
- Merge commit: `f099f15d9421c89120183f6b7b2defe765d59301`.
- Validações verdes antes do merge:
  - Phase 204 Autonomous IA Work Session Operator Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend.

## Estado atual do God Mode

O God Mode tem agora:

- PC de casa como cérebro principal;
- telemóvel como cockpit principal;
- PC cockpit secundário;
- `/app/home` como cockpit visual canónico;
- `/app/autonomous-ia-work-session` para sessões IA/work packets;
- `/app/god-mode-self-diagnosis` para self-diagnosis;
- `/app/first-pc-install-ready-pack` para instalação PC;
- contrato local para `GodModeDesktop.exe`;
- URL local canónico `http://127.0.0.1:8000/app/home`;
- readiness pack de primeira instalação PC;
- self-diagnosis mission control;
- self-fix queue;
- PR planning brief para lacunas do próprio God Mode;
- Autonomous IA Work Session Operator;
- Provider Work Pack Queue;
- importação de respostas IA para Conversation Source Import Feed;
- External Skills Lab Registry;
- External Lab Snapshot Reader;
- Native Skills Adoption Queue;
- cards de revisão mobile;
- mapa real de projetos/repos/conversas;
- scanner de repos com sugestões para Real Work Map;
- inventário de repos GitHub com feed para scanner;
- provider launcher/capture contract;
- runtime verification para PC;
- Controlled Self-Evolution Registry.

## Próxima ação recomendada

Próxima fase recomendada: **Phase 205 — Mobile Permission Relay + Driver Voice Mode + Offline Resend Queue**.

Objetivos:

- ligar o operador IA/mobile approval a um relay de permissões real;
- criar `permission_request` para aprovações, login manual, preenchimento sensível, pausa/continuação e decisões bloqueantes;
- suportar estados: `queued`, `sent`, `delivered`, `acknowledged`, `approved`, `rejected`, `expired`, `resend_pending`, `offline_wait`;
- suportar reenvio quando o telemóvel está sem rede/túnel;
- suportar wait mode no PC até chegar resposta;
- criar contrato de popup com formulário preenchível e ações simples OK/rejeitar/alterar;
- criar modo condução/voz: comando por fala, leitura curta por voz, sem exigir toque enquanto conduz;
- reutilizar `mobile_approval_cockpit_v2_service.py` em vez de duplicar approvals;
- manter segredos fora da memória normal e preparar binding futuro com vault;
- manter phase smoke único e apagar o smoke da Phase 204.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar `docs/project-tree/GOD_MODE_TREE.md` quando disponível, consultar módulos existentes antes de criar módulo novo, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
