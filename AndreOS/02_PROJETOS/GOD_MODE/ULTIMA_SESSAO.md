# Última Sessão - God Mode

## Data
2026-05-07

## Resumo

A Phase 203 foi implementada, validada e merged. Esta fase adiciona **God Mode Self-Diagnosis Mission Control + Fix-What-Is-Missing Queue** ao core do God Mode.

A intenção ficou clarificada: o God Mode deve continuar o trabalho quando o Oner está na rua/ocupado, criando pacotes de trabalho para IAs, recolhendo/importando respostas, diagnosticando o que falta nele mesmo e preparando correções por PR/gates. O Oner não deve ter de conduzir o trabalho manualmente no telemóvel enquanto está a conduzir.

## Clarificação importante da regra de operação

A regra correta é:

- O God Mode autónomo/runtime não pode fazer merge/release/deploy/update final sozinho sem aprovação explícita do Oner.
- Durante uma sessão de trabalho assistida, quando o Oner manda continuar/mergear depois de GitHub Actions verdes, o assistente pode fazer o merge para acelerar o desenvolvimento.
- O God Mode pode preparar missões, prompts, pacotes de trabalho, imports de resposta, diagnósticos e planos de PR.
- O God Mode deve operar em modo seguro quando o Oner está ausente/na rua: cria trabalho, fala com IAs por pacotes controlados e só pede aprovação para decisões bloqueantes/riscadas.
- O objetivo é evitar merges antes dos checks e antes de validação humana, não travar o desenvolvimento quando o Oner já deu autorização no chat.

## Phase 203 — God Mode Self-Diagnosis Mission Control + Fix-What-Is-Missing Queue

### Implementado

- Serviço: `backend/app/services/god_mode_self_diagnosis_mission_control_service.py`
- Rota API: `backend/app/routes/god_mode_self_diagnosis_mission_control.py`
- Página: `backend/app/routes/god_mode_self_diagnosis_mission_control_frontend.py`
- Docs: `docs/orchestration/god-mode-self-diagnosis-mission-control.md`
- Smoke workflow atual: `.github/workflows/phase203-self-diagnosis-mission-control-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase202-first-pc-install-ready-pack-smoke.yml`

### Endpoints novos

- `/api/god-mode-self-diagnosis/status`
- `/api/god-mode-self-diagnosis/policy`
- `/api/god-mode-self-diagnosis/run`
- `/api/god-mode-self-diagnosis/queue`
- `/api/god-mode-self-diagnosis/update-queue-item`
- `/api/god-mode-self-diagnosis/create-pr-planning-brief`
- `/api/god-mode-self-diagnosis/dashboard`
- `/api/god-mode-self-diagnosis/package`

### Rotas visuais

- `/app/god-mode-self-diagnosis`
- `/app/self-fix-mission-control`

### Funcionalidade

- Agrega First PC Install Ready Pack, Runtime Verification, Artifacts Center, Global State, Module Registry e Native Skills Adoption Queue.
- Gera `diagnostic_run`.
- Gera lacunas reais priorizadas.
- Cria `self_fix_queue_item`.
- Separa bloqueantes de instalação de melhorias futuras.
- Cria PR planning brief sem aplicar código.
- Cria cards mobile de revisão.

### Segurança / realidade

- Não aplica fixes diretamente.
- Não cria patch/código sozinho nesta fase.
- Não faz merge/release/deploy autónomo.
- Não guarda segredos.
- Não executa browser automation.
- Mantém `can_apply_fix_without_gate=false`.
- Mantém `can_merge_without_oner_approval=false` no runtime autónomo.

### PR e validação

- PR #346 merged.
- Merge commit: `a8d31cf1022a4862619aa3a15fe8e25d1267f472`.
- Validações verdes antes do merge:
  - Phase 203 Self Diagnosis Mission Control Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend.

## Estado atual do God Mode

O God Mode tem agora:

- PC de casa como cérebro principal;
- telemóvel como cockpit principal;
- PC cockpit secundário;
- `/app/home` como cockpit visual canónico;
- página `/app/first-pc-runtime-verification`;
- página `/app/first-pc-install-ready-pack`;
- página `/app/god-mode-self-diagnosis`;
- página `/app/external-skills-lab-registry`;
- página `/app/external-lab-snapshot-reader`;
- página `/app/native-skills-adoption-queue`;
- contrato local para `GodModeDesktop.exe`;
- URL local canónico `http://127.0.0.1:8000/app/home`;
- readiness pack de primeira instalação PC;
- self-diagnosis mission control;
- self-fix queue;
- PR planning brief para lacunas do próprio God Mode;
- External Skills Lab Registry;
- External Lab Snapshot Reader;
- Native Skills Adoption Queue;
- leitura de snapshots sanitizados das labs;
- geração de `native_skill_candidate`;
- promoção para `adoption_queue_item`;
- criação de candidate plans e implementation plans gated;
- cards de revisão mobile;
- mapa real de projetos/repos/conversas;
- scanner de repos com sugestões para Real Work Map;
- inventário de repos GitHub com feed para scanner;
- importador de conversas/fontes com feed para ledger e Work Map;
- provider launcher/capture contract;
- runtime verification para PC;
- Controlled Self-Evolution Registry;
- capacidade de avaliar novas repos externas e gerar plano de lab/workflow;
- capacidade de decidir que labs/códigos/padrões são úteis para um pedido do Oner;
- capacidade de preparar plano de reutilização nativa sem aplicar diretamente;
- smol-ai GodMode Reference Adapter;
- família de 10 external skills labs reconhecida no core.

## Próxima ação recomendada

Próxima fase recomendada: **Phase 204 — Autonomous IA Work Session Operator + Provider Work Pack Queue**.

Objetivos:

- permitir que o God Mode crie missões de trabalho para IAs enquanto o Oner está ausente/na rua;
- gerar work packets por provider/projeto/módulo;
- criar prompts controlados para ChatGPT/Claude/Gemini/etc.;
- manter modo manual-safe: abrir provider/captura manual quando necessário, sem automatizar login privado;
- importar respostas para Conversation Source Import Feed;
- ligar respostas ao self-fix queue, real work map e candidate/PR planning;
- gerir estados: `drafted`, `ready_to_send`, `waiting_response`, `response_imported`, `converted_to_tasks`, `blocked_needs_oner`;
- separar decisões bloqueantes que exigem Oner de trabalho que pode continuar sem risco;
- manter phase smoke único e apagar o smoke da Phase 203.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar `docs/project-tree/GOD_MODE_TREE.md` quando disponível, consultar módulos existentes antes de criar módulo novo, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
