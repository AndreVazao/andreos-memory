# Sovereign Trader — checkpoint autoritativo — 2026-10-30

Este checkpoint substitui handoffs anteriores contraditórios no que respeita ao estado atual de PRs, sistema operativo, instalação adaptativa e Android. O histórico antigo deve ser tratado como histórico, não como estado atual. Confirmar sempre o GitHub live antes de agir.

## Prioridade de produto
1. Cérebro/runtime headless, seguro e independente de UI.
2. APK/Android virtual office: build, smoke, inspeção de artefactos e preparação para instalação física.
3. Portabilidade Windows/Linux e instalação adaptativa.
4. Pesquisa multi-agente, memória central e controlos de risco; não deixar experiências de browser bloquear o cérebro.

## GitHub do produto
Repo: https://github.com/AndreVazao/VazaoSovereignTrader

- PR #520 — correções de safe area e navegação Android — MERGED. Os testes de emulador anteriormente observados passaram e capturas mostraram o escritório offline. Isto não prova teste físico no telefone nem integração com runtime/backend.
- PR #521 — https://github.com/AndreVazao/VazaoSovereignTrader/pull/521 — única PR ativa deste bloco. Branch `docs/cross-platform-runtime-policy-2026-10-30`. Head observado `be51c871e49fe59d5542eb132144c1022e76a44a`. Contém:
  - `docs/CROSS_PLATFORM_RUNTIME_POLICY.md`
  - `docs/ADAPTIVE_INSTALLATION_AND_NODE_ROLES.md`
  - `docs/OBSCURA_EVALUATION_CLAUDE_CODE.md`
  - `.github/workflows/obscura-cloud-smoke.yml`
  - `docs/ACTIVE_HANDOFF_2026-10-30.md`
  Os checks do head final devem ser confirmados antes de merge.
- PR #519 foi fechada sem merge após transferir o plano e o smoke workflow Obscura para a PR #521. O workflow de smoke cloud executou com sucesso no run 41050980461: release oficial descarregada, navegação para fixture local, título, JavaScript e extração de texto passaram, artefacto sanitizado carregado. É apenas teste funcional em runner Linux, não benchmark de desempenho.
- O workflow comparativo Obscura-vs-Chromium não foi transferido porque o protocolo CDP/servidor não está confirmado. Não afirmar que Obscura é mais rápida. Manter opcional e fora do caminho crítico.
- Fechar uma PR não apaga o branch remoto. Não afirmar que branches foram eliminadas sem confirmação do GitHub.

## Decisões técnicas atuais
- Windows e Linux são plataformas suportadas.
- Linux Server LTS mínimo é preferido para futuros servidores dedicados headless e workers dedicados, se hardware/arquitetura/drivers/dependências forem compatíveis. Não migrar já o PC pessoal.
- O mesmo código-base suporta ambos os sistemas. Serviços isolados por adaptadores: systemd em Linux e Windows Service/Task Scheduler no Windows conforme o componente.
- Instalação adaptativa ainda é contrato/documentação, não implementação pronta. Começar por diagnóstico sem alterações (`vst doctor --json`), deteção de OS/arquitetura/CPU/RAM/disco, manifesto de componentes e plano explícito. Instalar apenas componentes autorizados e adequados à função.
- Perfis planeados: brain-server, department-worker, research-worker, memory-node, desktop-cockpit, office-visualizer.
- Deteção da máquina não concede identidade, permissões, autoridade CEO, chaves de exchange ou permissões de execução. Enrollment/approval explícitos.
- Core headless separado do cockpit/escritório virtual. Renderização pode falhar sem parar o cérebro. Em hardware limitado reduzir concorrência e deixar 3D, browser persistente e modelos locais pesados desligados por defeito.
- PAPER/read-only por defeito; sem ordens reais, transferências, secrets em CI, portas públicas automáticas ou alterações automáticas de segurança do sistema.

## APK e testes físicos
- O escritório virtual é atualmente uma superfície de demonstração offline; não declarar que está ligado ao runtime real.
- A correção da PR #520 melhora safe areas/navegação; teste físico Android, ADB local e ligação PC↔telefone/Tailscale continuam BLOCKED/NOT RUN até o PC/dispositivo estarem disponíveis.
- Próximo: confirmar workflows da main após merge de #520; obter o APK do run atual; inspecionar logs e screenshots atuais, confirmar lançamento e navegação; preparar instruções de instalação para o telefone. Não reutilizar artefactos antigos como prova atual.
- O usuário está ansioso por testar o APK no telefone; dar prioridade real a esta frente sem declarar que já está pronto até haver artefactos atuais e teste adequado.

## Regras de continuidade
- Uma PR/branch de implementação ativa por vez; mudanças pequenas.
- Não apagar documentação antiga automaticamente se tiver evidência ou decisões únicas. Consolidar o estado atual num handoff autoritativo e marcar as secções antigas como históricas/obsoletas.
- Só marcar PASS quando o teste foi executado e o resultado confirmado; usar FAIL, BLOCKED ou NOT RUN quando apropriado.
- DGM-MAT é um projeto separado e não deve ser misturado.
- Nenhuma ação de trading REAL ou movimento de capital foi executada neste checkpoint.
