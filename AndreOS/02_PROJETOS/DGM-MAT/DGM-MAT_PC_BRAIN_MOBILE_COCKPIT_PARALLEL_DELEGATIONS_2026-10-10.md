# DGM-MAT — Cérebro no PC, cockpit móvel e delegações paralelas

Data: 2026-10-10
Tipo: decisão arquitetural vinculativa

## Regra central do utilizador

**O PC é o cérebro do DGM-MAT. O telefone é apenas o cockpit de comunicação e intervenção humana. O cérebro não pode depender do telefone.**

O PC mantém runtime, memória operacional, estado das missões, checkpoints, filas, ferramentas e orquestração. O telefone pode ficar offline ou desligar sem parar o processo principal nem invalidar o trabalho autónomo.

## Função do telefone

O cockpit permite ao utilizador enviar pedidos, conversar, acompanhar progresso, receber notificações e responder quando a atenção humana é necessária. Pode ser usado para fornecer instruções, orientar pesquisas, pedir investigação sobre sites, e completar manualmente passos legítimos como login, CAPTCHA/MFA, consentimento ou introdução segura de password. Não é o cérebro, não é a fonte de verdade e não deve hospedar o runtime.

## Delegações paralelas

O DGM-MAT deve operar como escritório/empresa digital com delegações independentes. Se uma delegação encontrar um passo que exige o utilizador, apenas a tarefa dependente fica em `WAITING_FOR_USER`/`BLOCKED`. A missão guarda checkpoint durável, evidência, dependências e política de retry; liberta recursos desnecessários e envia um pedido específico ao cockpit.

Enquanto espera, o orquestrador do PC procura e executa outras tarefas independentes e seguras: investigação, pesquisa, comparação, análise, testes, documentação, classificação/organização de ficheiros, identificação de duplicados e renomeações previamente autorizadas. **Uma delegação em espera não significa que a empresa inteira fica parada.**

O scheduler deve separar tarefas prontas, em execução, pendentes de intervenção e concluídas; evitar bloquear workers; respeitar prioridades e recursos; persistir estado através de reinícios; evitar ciclos de espera, duplicação de pedidos e retries cegos. Se não existir qualquer trabalho independente elegível, deve esperar honestamente, sem simular progresso.

## Continuidade após intervenção

Se o telefone estiver offline, o pedido permanece persistido no PC. Na reconexão, o cockpit autentica-se, sincroniza e obtém pedidos pendentes sem duplicação. Respostas são limitadas ao pedido, missão, etapa, dispositivo e prazo. Após intervenção, o DGM-MAT verifica o estado real do browser/serviço antes de retomar. Ações externas não idempotentes de resultado incerto não são repetidas automaticamente.

## Segurança e limites

- Segredos não entram em prompts, logs, memória persistente ou bus genérico.
- CAPTCHA/MFA é resolvido manualmente; nunca contornar.
- Não expor API a LAN/Tailscale/público até autenticação global HTTP/WebSocket, emparelhamento, scopes, revogação e migração de clientes serem concluídos e testados.
- FREE-ONLY / PAID-DENY: sem gastar dinheiro/créditos sem autorização explícita.
- Estabilidade > funcionalidades; evidência > pressupostos; controlo manual > automação destrutiva.

## Estado real

Este registo formaliza o requisito e o comportamento-alvo. Não prova que a delegação paralela, fila durável, pop-up móvel, autenticação global ou retoma end-to-end estejam já implementados. Esses componentes só podem ser marcados concluídos após implementação e testes reais.

Documento no repo DGM-MAT: `docs/architecture/PC_BRAIN_MOBILE_COCKPIT_PARALLEL_DELEGATIONS.md`.
Relacionados: `docs/architecture/HUMAN_IN_THE_LOOP_HANDOFF.md`, `docs/architecture/GOVERNED_BROWSER_AUTOMATION.md`.
