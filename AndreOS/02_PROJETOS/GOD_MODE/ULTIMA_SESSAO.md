# Última Sessão - God Mode

## Data
2026-05-06

## Resumo

A Phase 199 foi implementada, validada e merged. Esta fase adiciona **Controlled Self-Evolution + External Skills Lab Registry** ao core do God Mode.

O God Mode passa a reconhecer oficialmente as external skills labs como fontes de evolução controlada e reutilização de código/padrões. Também passa a avaliar novas repos externas descobertas, decidir se servem ou não, sugerir criação de lab, gerar plano com README/workflow de clone/import upstream e preparar plano de reutilização nativa.

Importante: o God Mode pode decidir que padrões/códigos são úteis e onde devem servir, mas não aplica código, não cria labs, não faz merge, não faz release e não executa ações arriscadas sem gates, PR, validação e aprovação quando aplicável.

## Phase 199 — Controlled Self-Evolution + External Skills Lab Registry

### Implementado

- Serviço: `backend/app/services/external_skills_lab_registry_service.py`
- Rota API: `backend/app/routes/external_skills_lab_registry.py`
- Página: `backend/app/routes/external_skills_lab_registry_frontend.py`
- Docs: `docs/orchestration/controlled-self-evolution-skills-labs.md`
- Smoke workflow atual: `.github/workflows/phase199-controlled-self-evolution-skills-labs-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase198-first-pc-runtime-verification-smoke.yml`

### Endpoints novos

- `/api/external-skills-lab-registry/status`
- `/api/external-skills-lab-registry/policy`
- `/api/external-skills-lab-registry/seed-defaults`
- `/api/external-skills-lab-registry/labs`
- `/api/external-skills-lab-registry/assess-repo`
- `/api/external-skills-lab-registry/catalog-repos`
- `/api/external-skills-lab-registry/decide-reuse`
- `/api/external-skills-lab-registry/create-reuse-plan`
- `/api/external-skills-lab-registry/create-lab-creation-plan`
- `/api/external-skills-lab-registry/dashboard`
- `/api/external-skills-lab-registry/package`

### Rotas visuais

- `/app/external-skills-lab-registry`
- `/app/skills-labs`

### Funcionalidade

- Regista as 10 external skills labs.
- Avalia novas repos externas descobertas.
- Decide se uma repo deve virar lab, referência, quarentena, vertical ou ser ignorada.
- Gera plano de criação de lab com README e workflow de import upstream.
- Decide quais labs/códigos/padrões usar perante um pedido do Oner.
- Cria plano de reutilização nativa.
- Cria cards de revisão para evolução controlada.
- Mantém `can_apply_code_without_gate=false`.
- Mantém `can_create_lab_without_gate=false`.

### Segurança / realidade

- Não faz merge direto.
- Não faz release direta.
- Não guarda segredos.
- Não copia código externo às cegas.
- Não usa automação browser em quarentena sem gate explícito.
- Não executa deploy/cloud/API paga sem aprovação.
- Não cria labs automaticamente sem gate/aprovação.
- O God Mode pode preparar plano, templates e PR; aplicação real continua controlada.

### PR e validação

- PR #342 merged.
- Merge commit: `f2b44a544b413d55fef5eafe0d7ea71f70259b40`.
- Validações verdes antes do merge:
  - Phase 199 Controlled Self Evolution Skills Labs Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend.

## External Skills Labs — inicializadas e reconhecidas

### Labs principais

- `AndreVazao/godmode-openai-skills-lab`
  - Upstream: `openai/skills`
  - Branch upstream: `main`
  - Papel: referência OpenAI/Codex Agent Skills.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.

- `AndreVazao/godmode-anthropic-skills-lab`
  - Upstream: `anthropics/skills`
  - Branch upstream: `main`
  - Papel: referência Claude Skills, Agent Skills spec, templates e document skills.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.

- `AndreVazao/godmode-vercel-skills-cli-lab`
  - Upstream: `vercel-labs/skills`
  - Branch upstream: `main`
  - Papel: CLI/ecossistema multi-agent para instalar/listar/update/remover skills.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.

- `AndreVazao/godmode-android-skills-lab`
  - Upstream: `android/skills`
  - Branch upstream: `main`
  - Papel: referência Android/APK para skills e boas práticas Android.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.

- `AndreVazao/godmode-gemini-skills-lab`
  - Upstream: `google-gemini/gemini-skills`
  - Branch upstream: `main`
  - Papel: referência Gemini API, Live API e Interactions API.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.

- `AndreVazao/godmode-cloudflare-skills-lab`
  - Upstream: `cloudflare/skills`
  - Branch upstream: `main`
  - Papel: referência Cloudflare Workers, Agents SDK, MCP, Durable Objects, R2, D1, KV, Vectorize, tunnels e deploy edge.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.

- `AndreVazao/godmode-awesome-copilot-lab`
  - Upstream: `github/awesome-copilot`
  - Branch upstream: `main`
  - Papel: catálogo de Copilot agents, instructions, skills, hooks, workflows e plugins.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.

- `AndreVazao/godmode-browser-act-skills-lab`
  - Upstream: `browser-act/skills`
  - Branch upstream: `main`
  - Papel: referência para browser task skills e workflows de browser automation.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.
  - Política: lab/quarentena; não usar stealth/captcha/session reuse/private chat automation no core sem gate e aprovação explícita.

### Labs opcionais/verticais

- `AndreVazao/godmode-google-cloud-skills-lab`
  - Upstream: `google/skills`
  - Branch upstream: `main`
  - Papel: referência Google Cloud, Cloud Run, Firebase, Cloud SQL, BigQuery, GKE e WAF.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.

- `AndreVazao/godmode-heygen-skills-lab`
  - Upstream: `heygen-com/skills`
  - Branch upstream: `master`
  - Papel: referência para avatar/video skills, útil sobretudo para VerbaForge e conteúdo.
  - Estado: README contratual + workflow de import upstream + reconhecida pelo God Mode.
  - Política: não chamar API paga nem gerar vídeos sem aprovação explícita do Oner.

## Estado atual do God Mode

O God Mode tem agora:

- PC de casa como cérebro principal;
- telemóvel como cockpit principal;
- PC cockpit secundário;
- `/app/home` como cockpit visual canónico;
- página `/app/first-pc-runtime-verification`;
- página `/app/external-skills-lab-registry`;
- links seguros para providers;
- contratos de launcher/captura de provider;
- mapa real de projetos/repos/conversas;
- scanner de repos com sugestões para Real Work Map;
- inventário de repos GitHub com feed para scanner;
- importador de conversas/fontes com feed para ledger e Work Map;
- verificador runtime de primeiro teste PC;
- Controlled Self-Evolution Registry;
- External Skills Lab Registry;
- capacidade de avaliar novas repos externas e gerar plano de lab/workflow;
- capacidade de decidir que labs/códigos/padrões são úteis para um pedido do Oner;
- capacidade de preparar plano de reutilização nativa sem aplicar diretamente;
- smol-ai GodMode Reference Adapter;
- família de 10 external skills labs reconhecida no core;
- vários módulos manuais de mobile/approval/autopilot/self-update no main.

## Próxima ação recomendada

Próxima fase recomendada: **Phase 200 — External Lab Snapshot Reader + Native Skill Candidate Planner**.

Objetivos:

- ler `docs/UPSTREAM_SNAPSHOT.json` das labs quando existir;
- criar índice local de skills candidatas;
- identificar skills úteis para God Mode, Android, Provider Router, Cloud/Deploy e VerbaForge;
- propor `native_skill_candidate` com risco, origem, uso pretendido e modo de reutilização;
- ligar ao Controlled Self-Evolution Registry;
- manter phase smoke único e apagar o smoke da Phase 199.

## Ação recomendada para labs

Disparar manualmente `Import upstream skills snapshot` em cada lab quando quiser materializar `/upstream/`.

Depois a Phase 200 pode ler os snapshots e propor skills nativas candidatas.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar `docs/project-tree/GOD_MODE_TREE.md`, consultar `/api/module-registry-snapshot/search` antes de criar módulos novos, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
