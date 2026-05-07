# Última Sessão - God Mode

## Data
2026-05-07

## Resumo

A Phase 201 foi implementada, validada e merged. Esta fase adiciona **Native Skills Runtime + Candidate Adoption Queue** ao core do God Mode.

O God Mode passa a transformar `native_skill_candidate` em `adoption_queue_item`, com estados controlados, plano de implementação nativa e cards de revisão mobile. Isto prepara a próxima camada prática: transformar candidatos aprovados em planos de PR/code patch, mantendo gates.

## Clarificação importante da regra de merge

A regra correta é:

- O God Mode autónomo/runtime não pode fazer merge/release/deploy/update final sozinho sem aprovação explícita do Oner.
- Durante uma sessão de trabalho assistida, quando o Oner manda continuar/mergear depois de GitHub Actions verdes, o assistente pode fazer o merge para acelerar o desenvolvimento.
- O objetivo é evitar merges antes dos checks e antes de validação humana, não travar o desenvolvimento quando o Oner já deu autorização no chat.

## Phase 201 — Native Skills Runtime + Candidate Adoption Queue

### Implementado

- Serviço: `backend/app/services/native_skills_adoption_queue_service.py`
- Rota API: `backend/app/routes/native_skills_adoption_queue.py`
- Página: `backend/app/routes/native_skills_adoption_queue_frontend.py`
- Docs: `docs/orchestration/native-skills-adoption-queue.md`
- Smoke workflow atual: `.github/workflows/phase201-native-skills-adoption-queue-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase200-external-lab-snapshot-reader-smoke.yml`

### Endpoints novos

- `/api/native-skills-adoption-queue/status`
- `/api/native-skills-adoption-queue/policy`
- `/api/native-skills-adoption-queue/promote-candidate`
- `/api/native-skills-adoption-queue/promote-candidates-by-filter`
- `/api/native-skills-adoption-queue/queue`
- `/api/native-skills-adoption-queue/update-status`
- `/api/native-skills-adoption-queue/create-implementation-plan`
- `/api/native-skills-adoption-queue/dashboard`
- `/api/native-skills-adoption-queue/package`

### Rotas visuais

- `/app/native-skills-adoption-queue`
- `/app/native-skills-runtime`

### Funcionalidade

- Promove `native_skill_candidate` para `adoption_queue_item`.
- Promove candidatos por filtro de domínio/risco.
- Mantém status controlado com transições permitidas.
- Cria planos de implementação nativa sem aplicar código.
- Consulta `module_registry_snapshot_service` antes de recomendar módulo novo.
- Cria cards mobile para revisão.
- Gera decision log sanitizado.

### Estados da fila

- `proposed`
- `needs_review`
- `approved_for_planning`
- `planned`
- `rejected`
- `quarantined`

### Segurança / realidade

- Não faz merge autónomo.
- Não faz release direta.
- Não faz deploy direto.
- Não cria PR sozinho nesta fase.
- Não guarda segredos.
- Não copia código externo às cegas.
- Não torna labs dependências centrais.
- Não usa automação browser em quarentena sem gate explícito.
- Não executa deploy/cloud/API paga sem aprovação.
- Mantém `can_apply_code_without_gate=false`.
- Mantém `can_merge_without_oner_approval=false` no runtime autónomo.

### PR e validação

- PR #344 merged.
- Merge commit: `9e438581ca3f20271a3b0765959591d88336af8c`.
- Validações verdes antes do merge:
  - Phase 201 Native Skills Adoption Queue Smoke;
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
- página `/app/external-skills-lab-registry`;
- página `/app/external-lab-snapshot-reader`;
- página `/app/native-skills-adoption-queue`;
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

Próxima fase recomendada: **Phase 202 — First PC Install Ready Pack + One-Click Local Start Contract**.

Objetivos:

- aproximar o God Mode de instalação real no PC;
- criar pacote/checklist de arranque local focado no `GodModeDesktop.exe` e backend;
- expor cockpit para verificar artefactos Windows/Android, rotas essenciais e readiness;
- criar contrato de first-run sem segredos no repo;
- preparar o caminho para autoevolução assistida pelo PC, sempre com gates;
- manter phase smoke único e apagar o smoke da Phase 201.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar `docs/project-tree/GOD_MODE_TREE.md` quando disponível, consultar módulos existentes antes de criar módulo novo, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
