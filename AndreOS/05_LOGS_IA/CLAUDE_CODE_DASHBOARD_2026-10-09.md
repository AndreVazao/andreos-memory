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
- Adicionada UI inline de aprovação/recusa. Playwright confirmou renderização e recusa; um teste de API simulada confirmou que aprovar envia a mensagem explícita na mesma sessão e preserva projeto/modelo. Escrita real após aprovação ainda não validada.
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
- Ainda não se verificou uma edição real de código através da interface depois da aprovação explícita do Fact-Forcing Gate; aprovações para comandos Bash fora da allowlist também não estão integradas.
- Pastas autorizadas: configuração global aplicada em `%USERPROFILE%\.claude\settings.json`, backup datado criado, plugins preservados; 33 diretórios existentes confirmados. Dashboard reiniciado e `/api/status` reportou `ok=true`, 33 pastas autorizadas e 7 projetos. A lista inclui OneDrive, Ambiente de Trabalho, Documentos, Imagens, Downloads e pastas de dados adicionais.
- A pasta `C:\Programas (x86)` não existe; foi incluída `C:\Program Files (x86)` (nome real do Windows). `C:\Windows`, `AppData`, perfis de browser e credenciais permanecem fora da lista.
- Cancelamento de tarefas longas precisa de teste dedicado.
- Anexos, visualização de diffs e controlo ADB não estão integrados.
- Não existe instalador autónomo; o ZIP futuro deve documentar dependências sem incluir credenciais.
- O serviço deve permanecer no loopback; não abrir na LAN/Internet sem autenticação.

## Próxima sessão
Testar com ficheiro descartável, cancelamento, arranque repetido, FCC offline, porta ocupada e projetos ausentes. Atualizar este checkpoint e a documentação. Só criar ZIP final quando os testes essenciais estiverem verdes. Confirmar commit e push para AndreVazao/andreos-memory.

## 2026-10-09 — autorização permanente de pastas
- Configuração global aplicada em %USERPROFILE%\.claude\settings.json, backup datado criado e plugins existentes preservados.
- 33 diretórios existentes confirmados, incluindo as raízes C: pedidas, OneDrive, Ambiente de Trabalho, Documentos, Imagens, Downloads e pastas pessoais adicionais.
- Dashboard reiniciado e /api/status reportou ok=true, 33 pastas autorizadas e 7 projetos.
- Testes de sintaxe de server.js e public/app.js passaram.
- CLI aceitou 33 caminhos --add-dir e 33 regras de leitura no teste de parsing com --help (exit code 0; sem chamada ao modelo).
- Interface mostra “Pasta base (opcional)” e “FCC · 33 pastas autorizadas”; a mensagem inicial explica que a pasta base não limita a lista autorizada.
- C:\Programas (x86) não existe; foi incluída C:\Program Files (x86). C:\Windows, AppData, perfis de browser e credenciais ficaram fora da lista.
