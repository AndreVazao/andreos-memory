# Changelog — Claude Code Dashboard

## 2026-10-09 — v0.1.0 inicial
- Criada interface de chat local com histórico e streaming.
- Adicionados seletor de projeto e seletor de aliases do FCC.
- Criado endpoint de estado e endpoint de paragem.
- Adicionado watchdog de 15 minutos por defeito para evitar tarefas presas indefinidamente e melhorado o feedback quando o processo termina sem texto/assinala erro.
- Adicionada deteção de bloqueios do Fact-Forcing Gate, painel inline Aprovar/Recusar e apresentação de falhas de ferramentas no feed de atividade.
- Adicionado o próprio dashboard à allowlist de projetos (total: 7) e política CLI explícita `acceptEdits` com ferramentas limitadas e padrões Bash autorizados.
- UI de aprovação testada em browser isolado com API simulada. Teste real isolado confirmou que a primeira escrita foi bloqueada pelo Fact-Forcing Gate e que, após aprovação explícita na mesma sessão, o ficheiro de teste foi criado com o conteúdo exato. O harness remoto não devolveu o fim do streaming dentro do período de espera e foi terminado; não ficou `fcc-claude.exe` ativo. A terminação limpa do streaming da sessão retomada continua por investigar.
- Criado launcher VBS/PowerShell para arranque oculto e atalho no Ambiente de Trabalho.
- Documentados pré-requisitos, setup, modelos, serviços/portas, diagnóstico e limites.
- Validados syntax checks, endpoint de estado, validação de entrada, projeto inexistente, ID de paragem inválido e conflito de porta.
- Cancelamento via endpoint confirmou limpeza da tarefa ativa e ausência de processo do teste ainda ativo.
- Resposta sem ferramentas via alias `sonnet` devolveu `OK` em cerca de 31,6 s; CLI reportou custo de `$0.100344`, não confirmado como valor faturado.
- Histórico de testes: `haiku` expirou aos 180 s e `sonnet` aos 90 s em tentativas anteriores sem escrita. Teste posterior isolado confirmou criação real após aprovação explícita; permanece por diagnosticar a demora/falta de fecho do streaming na sessão retomada.
- Em aberto: diagnosticar o timeout de execução/fornecedor, testar o botão de cancelamento na UI, FCC offline, arranque repetido, anexos, diffs e empacotamento.

## 2026-10-09 — autorização persistente de pastas
- Adicionada autorização persistente para 32 diretórios existentes em C:, projetos e pastas pessoais, incluindo OneDrive, Ambiente de Trabalho, Documentos, Imagens e Downloads.
- Criado Configure-ClaudeCode-AuthorizedDirectories.ps1, que faz backup de settings.json e atualiza permissions.additionalDirectories sem ativar bypass de permissões.
- Dashboard passa as pastas autorizadas ao CLI via --add-dir, restringe regras de leitura às raízes autorizadas e mostra a contagem de pastas no estado da ligação.
- Interface esclarece que a pasta base é opcional e que a lista autorizada permanece disponível em todas as conversas.
- Validado: settings.json atualizado, plugins preservados, backup criado, CLI aceitou os 32 caminhos e 32 regras de leitura em teste de parsing com --help; dashboard saudável, 7 projetos e 32 diretórios no endpoint.
- C:\Programas (x86) não existe neste PC; C:\Program Files (x86) foi incluída como pasta real equivalente. C:\Program Files ficou fora por não ter sido pedida. C:\Windows, AppData, perfis de browser e credenciais permanecem fora da lista.


## 2026-10-09 — idioma predefinido e painel fixo
- O servidor acrescenta a cada pedido uma instrução permanente para responder em português de Portugal (pt-PT), permitindo outra língua quando o utilizador a pede explicitamente.
- Ajustado o layout para manter a barra lateral fixa no PC e limitar o scroll vertical à área da conversa; cabeçalho e compositor mantêm-se no lugar. Em ecrãs móveis, o menu continua a ser um painel deslizante.
- Verificação de sintaxe e validação visual/end-to-end ainda pendentes após reiniciar o servidor.


## 2026-10-09 — corrigir comandos Bash no Windows e reforçar proteções
- Instruções permanentes ao agente clarificam que Bash não é CMD/PowerShell, recomendam `ls`/`git ls-files` e proíbem ler diretórios como ficheiros.
- Removido `Bash(dir *)` da allowlist e adicionado `Bash(git ls-files *)`.
- Reforçada a instrução para nunca desativar o Fact-Forcing Gate ou usar `GATEGUARD_BASH_ROUTINE_DISABLED` para contornar bloqueios.
- Sintaxe validada e dashboard reiniciado; validação end-to-end ainda pendente.


## 2026-10-10 — Skills reutilizáveis e diagnóstico
- Criado catálogo local com seis Skills para auditoria, correção segura, automação Windows, saúde Git, consolidação de scripts e testes/build.
- A raiz do dashboard é agora adicionada a cada sessão via --add-dir, disponibilizando o catálogo nos projetos selecionados.
- Allowlist ampliada com comandos específicos de diagnóstico Git, versões de ferramentas, lint/typecheck/check e unittest; sem comandos shell genéricos nem instalação de dependências.
- Instruções reforçam logs, dry-run, backups e confirmação explícita para tarefas agendadas, serviços, arranque automático, instalações e operações destrutivas.
- Sintaxe de server.js e public/app.js passou. Reinício e teste end-to-end de descoberta das Skills continuam pendentes.


### Validação operacional final — 2026-10-10
- Dashboard iniciado em background após as alterações. GET /api/status confirmou ok=true, FCC disponível, CLI disponível e os sete projetos esperados.
- Pedido direto a http://127.0.0.1:8082/admin devolveu HTTP 200. O script de verificação do FCC teve um timeout transitório no seu próprio pedido HTTP durante o arranque; a verificação posterior confirmou que o endpoint estava saudável.
- node --check server.js e node --check public/app.js terminaram com exit code 0.
- O catálogo de seis Skills e o índice estão presentes. Não foi feita chamada ao modelo; por isso, a descoberta automática das Skills dentro de uma conversa continua por validar e não é declarada como confirmada.


## Centro de Ferramentas, launcher e automações — 2026-10-10
- Adicionado botão Ferramentas no cabeçalho e uma janela de controlo com pesquisa de aplicações, ações de janela e automações reutilizáveis.
- GET /api/apps lista atalhos .lnk/.url nas pastas conhecidas do Menu Iniciar, Ambiente de Trabalho e respetiva pasta OneDrive. A lista é limitada a 500 atalhos e profundidade 5; não pesquisa o registo nem executa programas automaticamente.
- POST /api/apps/launch aceita apenas o ID de um atalho atual da lista e pede ao Windows para o abrir; a interface pede confirmação antes de enviar.
- POST /api/desktop/control expõe apenas windows, inspect e click; desktop-control.ps1 exige uma única janela correspondente e, para clicar, um botão acessível, visível, ativo e com nome exato único.
- A interface bloqueia botões com nomes claramente associados a compras/pagamentos, eliminação de conta, reposição de fábrica e operações semelhantes; todos os outros cliques também exigem confirmação.
- Criadas duas Skills adicionais: reusable-automations e windows-app-control. O catálogo passa de seis para oito competências.
- Automações incluídas: diagnóstico do projeto, atualização segura, testes/relatório, plano de cópia de segurança e comparação apenas de problemas novos.
- Testado desktop-control.ps1 windows: devolveu as janelas visíveis; inspect devolveu controlos acessíveis da janela Chrome. O endpoint de aplicações encontrou 159 atalhos após corrigir a expressão regular e incluir a pasta OneDrive Ambiente de Trabalho.
- Limitação: abertura de programas pelo painel e controlo manual de botões acessíveis estão implementados; não está confirmada a capacidade de o modelo Claude invocar diretamente estas ações a partir do chat. Jogos com UI não acessível podem exigir cliques manuais.
- Pendente: reinício final, validação de sintaxe e teste dos endpoints do Centro de Ferramentas. Nenhuma aplicação/jogo foi aberto durante os testes e nenhuma chamada adicional ao modelo foi executada.


## Experiência de conversa e scroll independente — 2026-10-10
- Ajustado o layout para que a barra lateral tenha a sua própria lista de conversas com scroll vertical independente, sem scroll propagado para o histórico principal.
- A lista de conversas ocupa o espaço vertical disponível entre os controlos fixos da barra; deixou de estar limitada a 40vh, o que evita áreas vazias e melhora a navegação quando existem muitas conversas.
- Aumentada a área clicável dos itens de conversa para 42px de altura mínima, com foco de teclado visível e nome da conversa alinhado de forma consistente.
- A conversa usa scroll vertical isolado (`overscroll-behavior-y: contain`) e mantém cabeçalho/compositor fixos. O menu móvel continua a ser um painel sobreposto.
- Corrigido o auto-scroll: o código tentava definir `scrollTop` em `#messages`, que não é a área scrollável; agora desloca `.conversation` para o fim ao renderizar novas mensagens.
- Verificações: `node --check` em `public/app.js` e `server.js` terminou com código 0; CSS servido em `http://127.0.0.1:8091/style.css` contém as regras novas; `/api/status` respondeu `ok:true`; `/api/apps` respondeu 200 com 159 atalhos; `/api/automations` respondeu 200 com 5 automações; `/api/desktop/control` aceitou a consulta de janelas com HTTP 200.
- O dashboard não tem pasta `.git` em `C:\ProgramasGodMode\ClaudeCode-Dashboard`, pelo que as alterações de UI estão aplicadas localmente, mas não foram versionadas num repositório próprio.
