# Checkpoint — Claude Code Dashboard — 2026-10-09

## Pedido do utilizador
Criar uma interface de chat bonita, fluida e simples para trabalhar com Claude Code sem gerir terminais. Manter documentação atualizada. No final, criar ZIP com documentação completa para reinstalar o setup e sincronizar a memória persistente com GitHub.

## Estado
Primeira versão funcional em C:\ProgramasGodMode\ClaudeCode-Dashboard.

## Verificações executadas
- `node --check server.js`: OK.
- `node --check public/app.js`: OK.
- Launcher oculto arrancou dashboard a frio na validação anterior: OK.
- `/api/status`: `ok=true`, FCC server online, CLI presente, 2 aliases e 7 projetos: OK.
- Browser de teste abriu a interface sem erros de consola observados.
- Smoke test anterior do chat: agente usou a ferramenta de leitura e devolveu nome/versão de `package.json` corretamente.
- API: mensagem vazia e projeto inexistente rejeitados com HTTP 400; ID de cancelamento desconhecido rejeitado com HTTP 404.
- Porta ocupada: segunda instância terminou com `EADDRINUSE`/exit 1, sem derrubar a instância principal.
- Cancelamento por `/api/stop`: devolveu `stopped=true`; entrada ativa removida e chamadas posteriores para o mesmo ID devolveram 404; não foram encontrados processos do teste ativos.
- Adicionado watchdog de tarefa de 15 minutos por defeito e mensagens visíveis para resposta vazia/erro do modelo; syntax checks passaram e o dashboard reiniciou com `/api/status` saudável. O disparo real do watchdog ainda não foi testado com limite acelerado.
- Resposta sem ferramentas pelo alias `sonnet` devolveu `OK` em cerca de 31,6 s; o CLI reportou custo de `$0.100344`, não confirmado como valor efetivamente faturado. Verificar o painel NVIDIA NIM antes de mais testes de consumo elevado.
- Testes reais de criação/edição foram bloqueados pelo Fact-Forcing Gate, que exige apresentação de factos antes da operação. O gate foi mantido ativo; nenhum ficheiro temporário ficou no disco.
- Adicionada UI inline de aprovação/recusa. Playwright confirmou renderização e recusa; um teste de API simulada confirmou que aprovar envia a mensagem explícita na mesma sessão e preserva projeto/modelo.
- Teste real de escrita após aprovação: o Fact-Forcing Gate bloqueou a primeira tentativa e apresentou os factos exigidos; a chamada seguinte com aprovação explícita criou `approval-write-test.txt` com o conteúdo exato `DASHBOARD_APPROVAL_WRITE_TEST_OK`. O harness remoto não devolveu a conclusão do streaming dentro do período de espera e teve de ser terminado; depois disso, `tasklist` confirmou que não havia `fcc-claude.exe` ativo. O ficheiro e os scripts temporários foram removidos. Resultado: a escrita após aprovação passou; a terminação limpa do streaming da sessão retomada permanece por investigar.
- Política CLI passou a usar `acceptEdits`, limitar ferramentas disponíveis e restringir Bash a padrões allowlisted; nunca usar `--dangerously-skip-permissions`.

## Dependências conhecidas
- Windows.
- Node.js >=18; PC atual detetou v24.20.0.
- FCC no perfil do utilizador: fcc-claude.exe e fcc-server.exe.
- FCC Admin: 127.0.0.1:8082.
- CLI Node-compatible: C:\ProgramasGodMode\tools\claude-code-node-2.1.112\package\cli.js.
- Script de arranque FCC: C:\ProgramasGodMode\DGM-MAT-Ensure-FCC-Server.ps1.
- Dashboard: 127.0.0.1:8091.
- Modelos reais: Nemotron 3 Super 120B e Nemotron 3.5 Lightning 30B via aliases FCC.

## Limitações em aberto
- A escrita real após aprovação explícita foi confirmada num ficheiro de teste isolado; ainda não se validou uma edição de código real nem o fecho limpo do streaming após a sessão retomada. Aprovações para comandos Bash fora da allowlist também não estão integradas.
- Pastas autorizadas: configuração global aplicada em `%USERPROFILE%\.claude\settings.json`, backup datado criado, plugins preservados; 32 diretórios existentes confirmados. Dashboard reiniciado e `/api/status` reportou `ok=true`, 32 pastas autorizadas e 7 projetos. A lista inclui OneDrive, Ambiente de Trabalho, Documentos, Imagens, Downloads e pastas de dados adicionais.
- A pasta `C:\Programas (x86)` não existe; foi incluída `C:\Program Files (x86)` (nome real do Windows). `C:\Windows`, `AppData`, perfis de browser e credenciais permanecem fora da lista.
- Cancelamento de tarefas longas precisa de teste dedicado.
- Anexos, visualização de diffs e controlo ADB não estão integrados.
- Não existe instalador autónomo; o ZIP futuro deve documentar dependências sem incluir credenciais.
- O serviço deve permanecer no loopback; não abrir na LAN/Internet sem autenticação.

## Próximos passos
1. Investigar por que a sessão retomada cria o ficheiro aprovado mas o streaming não devolve a conclusão ao harness dentro do tempo esperado; verificar eventos `done`/`exit` e limpeza da árvore de processos.
2. Testar o botão de cancelamento diretamente na UI e confirmar que o estado visual e os processos são limpos.
3. Testar FCC offline, arranque repetido e projetos ausentes sem alterar dados reais.
4. Rever aprovações para comandos Bash fora da allowlist e manter as proteções ativas.
5. Só criar ZIP final depois dos testes essenciais, extração limpa e documentação de setup completa.
6. Confirmar `git diff --check`, commit e push para AndreVazao/andreos-memory.

## 2026-10-09 — autorização permanente de pastas
- Configuração global aplicada em %USERPROFILE%\.claude\settings.json, backup datado criado e plugins existentes preservados.
- 32 diretórios existentes confirmados, incluindo as raízes C: pedidas, OneDrive, Ambiente de Trabalho, Documentos, Imagens, Downloads e pastas pessoais adicionais.
- Dashboard reiniciado e /api/status reportou ok=true, 32 pastas autorizadas e 7 projetos.
- Testes de sintaxe de server.js e public/app.js passaram.
- CLI aceitou 32 caminhos --add-dir e 32 regras de leitura no teste de parsing com --help (exit code 0; sem chamada ao modelo).
- Interface mostra “Pasta base (opcional)” e “FCC · 32 pastas autorizadas”; a mensagem inicial explica que a pasta base não limita a lista autorizada.
- C:\Programas (x86) não existe; foi incluída C:\Program Files (x86). C:\Program Files ficou fora por não ter sido pedida; C:\Windows, AppData, perfis de browser e credenciais ficaram fora da lista.


## 2026-10-09 — preferência de idioma e scroll da interface
- Pedido do utilizador: o assistente do dashboard deve falar por predefinição sempre em português de Portugal (pt-PT), embora possa usar outras línguas quando isso for pedido.
- Pedido do utilizador: a barra lateral esquerda no PC deve ficar fixa; não deve subir/desaparecer com o scroll da conversa. Só a conversa deve ter scroll vertical; cabeçalho e compositor permanecem fixos. No telemóvel, o menu deve continuar a funcionar como painel deslizante.
- Implementado em `server.js`: a instrução de idioma é acrescentada a cada pedido antes de o enviar ao CLI, incluindo sessões retomadas.
- Implementado em `public/style.css`: janela com altura limitada ao viewport, overflow externo oculto e scroll vertical isolado na conversa; menu móvel preservado.
- Estado: alterações de ficheiros aplicadas. Ainda falta executar verificações de sintaxe, reiniciar o dashboard e validar a disposição/idioma no browser; não declarar teste visual concluído antes dessa validação.


## Incidente do pedido cancelado — comandos Bash no Windows
- O utilizador pediu uma melhoria genérica no ProVentil e cancelou após ver uma sequência de erros em tempo real.
- Erros observados no transcript: `Read` aplicado a diretório (`EISDIR`); `dir /b /s` executado sob Bash, interpretando `/b` e `/s` como caminhos; repetição de comandos de listagem incompatíveis; falha de aspas `unexpected EOF`.
- O transcript também mostra texto a sugerir `GATEGUARD_BASH_ROUTINE_DISABLED=1`. Não se deve usar esse bypass. As novas instruções explícitas dizem para nunca enfraquecer o gate; apresentar os factos exigidos (pedido atual e objetivo do comando) e repetir só a operação limitada, ou parar e pedir orientação.
- Alterado `server.js`: removido `Bash(dir *)`; adicionado `Bash(git ls-files *)`; instrução de idioma expandida com regras específicas para shell Bash no PC Windows, leitura de pastas/ficheiros e segurança.
- `node --check server.js` e `node --check public/app.js`: exit code 0. Servidor reiniciado e `/api/status` confirmou `ok=true`, FCC e CLI disponíveis.
- Nenhuma nova chamada ao modelo foi feita durante a correção; não se afirma que o fluxo end-to-end já esteja validado. A alteração evita repetir os erros conhecidos e reforça o comportamento de segurança.
