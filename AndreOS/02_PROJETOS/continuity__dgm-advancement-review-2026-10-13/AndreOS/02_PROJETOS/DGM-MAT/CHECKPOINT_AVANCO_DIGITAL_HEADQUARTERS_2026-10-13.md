# Checkpoint de continuidade — avanço DGM-MAT Digital Headquarters
**Data:** 2026-10-13  
**Estado:** investigação remota concluída; documentação preservada numa branch GitHub; não implementado nem integrado localmente.  
**Repositório analisado:** `AndreVazao/DGM-MAT`  
**Branch principal de documentação:** `docs/digital-headquarters-concept-2026-10-12`  
**Commit base de main observado na comparação:** `abeb8c593d298662e62a4aed98965a05283855c4`

## Instrução de continuidade
O utilizador pediu para suspender o trabalho no PC, investigar este avanço, guardar o conhecimento e, quando voltar ao PC, incorporar as evoluções no código local antes de qualquer merge e sincronização PC↔GitHub. Não iniciar merges, resets, rebases, pulls/pushes ou implementação com base apenas nesta documentação. Primeiro auditar branches, working trees e commits locais/remotos, preservar o trabalho local e mapear as propostas aos contratos/código reais.

## Estado observado no GitHub
A comparação de `main` com `docs/digital-headquarters-concept-2026-10-12` devolveu **13 commits à frente, 0 atrás** (`ahead`, `behind`), com oito ficheiros adicionados nesta comparação:
- `docs/future/README-DIGITAL-HEADQUARTERS-RESEARCH-PACKAGE.md`
- `docs/future/DGM-MAT-DIGITAL-HEADQUARTERS-CONCEPT-2026-10-12.md`
- `docs/future/DGM-MAT-EXTERNAL-AGENTS-AND-SELF-IMPROVEMENT-RESEARCH-2026-10-12.md`
- `docs/future/DGM-MAT-VIRTUAL-OFFICE-TECHNOLOGY-RESEARCH-2026-10-12.md`
- `docs/future/DGM-MAT-ADAPTIVE-RUNTIME-AND-DISTRIBUTED-WORKERS-2026-10-12.md`
- `docs/future/DGM-MAT-ADAPTIVE-TOOLS-SKILLS-AND-AUTONOMY-ROADMAP-2026-10-13.md`
- `docs/future/DGM-MAT-DEPARTMENT-SOVEREIGNTY-AND-AGENT-GOVERNANCE-2026-10-13.md`
- `docs/future/assets/dgm-mat-digital-headquarters-wireframe.svg`

A comparação não é uma validação de runtime nem uma confirmação de que o PC local contém estes documentos. São propostas documentais; não assumir funcionalidades já implementadas.

## Conteúdo a preservar
1. **Digital Headquarters / escritório vivo:** navegação fixa à esquerda, escritório isométrico ao centro e chat/pedidos à direita; departamentos, agentes, formação, recrutamento, remodelação, enfermaria/recuperação, armazém, produção, QA e expedições. A visualização tem de ser uma projeção do estado real do backend, nunca uma fonte de verdade paralela.
2. **Semântica fiel:** agente bloqueado pode ser encaminhado para diagnóstico/recuperação; espera por dependência não é doença; reativação só após health checks/testes. Armazém e viaturas refletem pedidos, produção, validação, expedição e entregas realmente registados. Não inventar progresso, atividade, respostas externas nem entregas.
3. **Renderização adaptável:** mesma aplicação e estado canónico com modos 3D, 2D/isométrico, 2D leve, personagem mínima/chat e sem animação. Escolha por medições reais, fallback, escolha manual e preservação de estado; o hardware antigo conhecido (~2 cores, ~3 GB RAM) exige começar leve.
4. **Cérebro independente:** DGM-MAT conserva política, memória, orquestração, contratos, validação, auditoria e estado canónico. Harnesses, modelos, ferramentas MCP e outros computadores são workers/adaptadores substituíveis; nenhum recebe autoridade central nem acesso ilimitado.
5. **Workers distribuídos:** futura arquitetura com control plane central, gateway por nó, catálogo de capacidades verificadas, dispatcher, canal autenticado/cifrado, artefactos e auditoria. Inscrição explícita de cada máquina; LAN não implica confiança; começar por read-only/workspace isolado; revogação, timeout, cancelamento, quotas e permissões mínimas.
6. **Política free/local-first:** preferir capacidades locais gratuitas adequadas e ferramentas gratuitas já autorizadas; considerar qualidade, privacidade, latência e disponibilidade; APIs pagas só após configuração e autorização explícitas, com limites de despesa. Nunca criar custos silenciosamente nem presumir quotas ilimitadas.
7. **Skills e autoevolução:** skills versionadas, auditáveis e portáveis por adaptadores; melhoria baseada em evidência, memória/histórico, hipótese, sandbox, testes independentes, aprovação proporcional ao risco, publicação controlada e rollback. Evitar repetir leituras/trabalho já documentados; consultar a memória antes de recomeçar.
8. **Governação de departamentos/agentes:** mandato, identidade/versão, responsável, ferramentas, permissões, limites, proveniência, critérios de qualidade e ciclo de vida. Distinguir agente temporário, permanente e externo; contratação/expansão limitada, sem loops de delegação ou autoaprovação; capacidades e competências demonstradas por testes, não por tempo decorrido.
9. **Licenças e adoção de terceiros:** My Virtual Office tem licença AGPL-3.0-or-later segundo a pesquisa registada; My Virtual World indica PolyForm Noncommercial para código e CC BY-NC-SA para assets; confirmar licenças/commits atuais antes de qualquer reutilização. Claude Office/Pixel Agent Office são referências de arquitetura de eventos e visualização; DeepSeek Harness é candidato a worker experimental isolado, não o cérebro. Não copiar código/ativos sem revisão.
10. **Plano de fases:** (A) auditoria/reconciliação local-remota; (B) mapear APIs, contratos, eventos, providers, persistência, governação, filas e frontend existentes; (C) medir baseline do PC; (D) protótipo visual com mock data; (E) projeção read-only; (F) um worker isolado e medido; (G) só depois ações, departamentos e rede distribuída, com autorização e rollback.

## Branches que não se devem confundir
A pesquisa encontrou também `feature/digital-organization-foundation`, comparada com `main` como **divergente**: 11 commits à frente e 118 atrás, com ficheiros de código de organização, message bus, registry, task manager, workspace, configuração, documentação e testes. Não fazer merge automático nem misturar com a branch documental: precisa de auditoria independente de histórico, conteúdo e compatibilidade com o estado local.
A branch `fix/digital-organization-foundation-complete` foi devolvida como 107 commits atrás e 0 à frente na comparação com `main`; não a tratar como avanço atual sem nova evidência.
Não concluir que a branch documental ou a feature branch já está presente no PC.

## Links
- [Pacote e índice da investigação](https://github.com/AndreVazao/DGM-MAT/blob/docs/digital-headquarters-concept-2026-10-12/docs/future/README-DIGITAL-HEADQUARTERS-RESEARCH-PACKAGE.md)
- [Conceito Digital Headquarters](https://github.com/AndreVazao/DGM-MAT/blob/docs/digital-headquarters-concept-2026-10-12/docs/future/DGM-MAT-DIGITAL-HEADQUARTERS-CONCEPT-2026-10-12.md)
- [Runtime adaptável e workers distribuídos](https://github.com/AndreVazao/DGM-MAT/blob/docs/digital-headquarters-concept-2026-10-12/docs/future/DGM-MAT-ADAPTIVE-RUNTIME-AND-DISTRIBUTED-WORKERS-2026-10-12.md)
- [Roadmap de ferramentas, skills e autonomia](https://github.com/AndreVazao/DGM-MAT/blob/docs/digital-headquarters-concept-2026-10-12/docs/future/DGM-MAT-ADAPTIVE-TOOLS-SKILLS-AND-AUTONOMY-ROADMAP-2026-10-13.md)
- [Soberania departamental e governação de agentes](https://github.com/AndreVazao/DGM-MAT/blob/docs/digital-headquarters-concept-2026-10-12/docs/future/DGM-MAT-DEPARTMENT-SOVEREIGNTY-AND-AGENT-GOVERNANCE-2026-10-13.md)
- [Pesquisa comparativa de escritórios virtuais](https://github.com/AndreVazao/DGM-MAT/blob/docs/digital-headquarters-concept-2026-10-12/docs/future/DGM-MAT-VIRTUAL-OFFICE-TECHNOLOGY-RESEARCH-2026-10-12.md)

## Próximas ações ao regressar ao PC
1. Read-only: inventariar remotos/branches, HEAD, working tree, commits não publicados e diferenças locais.
2. Preservar working trees e backups; não descartar ficheiros desconhecidos nem usar force-push.
3. Comparar cada ficheiro documental com o estado local e cruzar as propostas com contratos/APIs/testes atuais.
4. Auditar separadamente `feature/digital-organization-foundation` e os commits locais ainda não publicados; não assumir que são equivalentes.
5. Adaptar primeiro o código/documentação no PC, testar localmente e atualizar a memória central.
6. Só depois preparar merges locais explícitos e validar a reconciliação.
7. Publicar apenas depois de confirmar a relação local/remota; não disparar GitHub Actions desnecessariamente.

**Limites da investigação de 2026-10-13:** análise remota da branch/documentação via GitHub; sem acesso atual ao filesystem do PC, sem testes locais, sem instalação, sem merge e sem sincronização.
