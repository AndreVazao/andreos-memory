# Última Sessão - God Mode

## Data
2026-05-06

## Resumo

A Phase 200 foi implementada, validada e merged. Esta fase adiciona **External Lab Snapshot Reader + Native Skill Candidate Planner** ao core do God Mode.

O God Mode passa a conseguir ler snapshots sanitizados das external skills labs, especialmente `docs/UPSTREAM_SNAPSHOT.json`, transformar paths `SKILL.md` em `native_skill_candidate`, classificar domínio/risco/modo de reutilização e criar planos gated por candidato.

Importante: a Phase 200 não importa código bruto das labs, não torna labs dependências centrais e não aplica candidatos sem PR, gates, GitHub Actions e aprovação do Oner quando aplicável.

## Phase 200 — External Lab Snapshot Reader + Native Skill Candidate Planner

### Implementado

- Serviço: `backend/app/services/external_lab_snapshot_reader_service.py`
- Rota API: `backend/app/routes/external_lab_snapshot_reader.py`
- Página: `backend/app/routes/external_lab_snapshot_reader_frontend.py`
- Docs: `docs/orchestration/external-lab-snapshot-reader.md`
- Smoke workflow atual: `.github/workflows/phase200-external-lab-snapshot-reader-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase199-controlled-self-evolution-skills-labs-smoke.yml`

### Endpoints novos

- `/api/external-lab-snapshot-reader/status`
- `/api/external-lab-snapshot-reader/policy`
- `/api/external-lab-snapshot-reader/ingest-snapshot-text`
- `/api/external-lab-snapshot-reader/ingest-snapshot`
- `/api/external-lab-snapshot-reader/generate-candidates-from-registry`
- `/api/external-lab-snapshot-reader/candidates`
- `/api/external-lab-snapshot-reader/create-candidate-plan`
- `/api/external-lab-snapshot-reader/dashboard`
- `/api/external-lab-snapshot-reader/package`

### Rotas visuais

- `/app/external-lab-snapshot-reader`
- `/app/lab-snapshot-reader`

### Funcionalidade

- Lê JSON colado no telemóvel a partir de `docs/UPSTREAM_SNAPSHOT.json`.
- Lê payload estruturado de snapshot.
- Extrai paths `SKILL.md` e metadados equivalentes.
- Cria `native_skill_candidate` com origem, lab, upstream, path, domínio alvo, confiança, risco, modo de reutilização e aprovações exigidas.
- Gera fallback de candidatos a partir do External Skills Lab Registry quando os snapshots reais ainda não foram importados.
- Cria plano gated para candidato específico.
- Cria card de revisão no cockpit mobile.

### Domínios de candidato

- `god_mode_core`
- `android_mobile`
- `provider_router`
- `cloud_deploy`
- `verbaforge_content`
- `github_workflow`
- `browser_quarantine`

### Segurança / realidade

- Não faz merge direto.
- Não faz release direta.
- Não faz deploy direto.
- Não guarda segredos.
- Não copia código externo às cegas.
- Não torna labs dependências centrais.
- Rejeita texto de snapshot com padrões óbvios de segredo.
- Não usa automação browser em quarentena sem gate explícito.
- Não executa deploy/cloud/API paga sem aprovação.
- Mantém `can_apply_candidate_without_gate=false`.
- Mantém `can_import_raw_lab_code_without_review=false`.

### PR e validação

- PR #343 merged.
- Merge commit: `a8814fa9d13c7f8c71640a6c32b9f9a7c2c479f6`.
- Validações verdes antes do merge:
  - Phase 200 External Lab Snapshot Reader Smoke;
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
- External Skills Lab Registry;
- External Lab Snapshot Reader;
- leitura de snapshots sanitizados das labs;
- geração de `native_skill_candidate`;
- criação de candidate plans gated;
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

Próxima fase recomendada: **Phase 201 — Native Skills Runtime + Candidate Adoption Queue**.

Objetivos:

- transformar `native_skill_candidate` em fila real de adoção controlada;
- permitir promover candidatos para `adoption_queue_item` sem aplicar código;
- criar estados: `proposed`, `needs_review`, `approved_for_planning`, `planned`, `rejected`, `quarantined`;
- gerar plano de implementação nativa por candidato;
- ligar ao External Lab Snapshot Reader e ao Mobile Approval Cockpit;
- manter `can_apply_code_without_gate=false`;
- manter phase smoke único e apagar o smoke da Phase 200.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar `docs/project-tree/GOD_MODE_TREE.md` quando disponível, consultar módulos existentes antes de criar módulo novo, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
