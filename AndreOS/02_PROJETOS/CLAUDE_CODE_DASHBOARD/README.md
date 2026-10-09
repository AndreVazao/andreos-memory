# Claude Code Dashboard — memória do projeto

**Última atualização:** 2026-10-09  
**Estado:** v0.1.0 funcional inicial; estabilização em curso  
**Instalação de desenvolvimento:** C:\ProgramasGodMode\ClaudeCode-Dashboard  
**Memória persistente:** C:\ProgramasGodMode\andreos-memory\AndreOS\02_PROJETOS\CLAUDE_CODE_DASHBOARD

## Objetivo
Criar uma interface simples, fluida e visualmente limpa para pedir trabalho ao Claude Code sem gerir terminais manualmente. Prioridades: fiabilidade, simplicidade e transparência sobre o que foi realmente testado.

## Implementado
- Aplicação web local com Node.js e interface HTML/CSS/JavaScript.
- Streaming de respostas por Server-Sent Events.
- Histórico local no browser e sessões retomáveis por ID.
- Seleção entre seis caminhos de projeto fixos.
- Dois aliases de modelo configurados via FCC.
- Botão de paragem e terminação de árvore de processos no Windows.
- Launcher VBS/PowerShell oculto, atalho de ambiente de trabalho e verificação de estado.
- FCC iniciado/verificado pelo script existente C:\ProgramasGodMode\DGM-MAT-Ensure-FCC-Server.ps1.
- Documentação de instalação e diagnóstico no README da aplicação.

## Ambiente conhecido
- PC Windows: PC-Vazao-Anjos.
- Node.js detetado: v24.20.0; requisito declarado: Node >=18.
- CLI Node-compatible: C:\ProgramasGodMode\tools\claude-code-node-2.1.112\package\cli.js.
- FCC: %USERPROFILE%\.local\bin\fcc-claude.exe e fcc-server.exe.
- FCC local: http://127.0.0.1:8082/admin.
- Dashboard: http://127.0.0.1:8091.
- Modelo principal: nvidia_nim/nvidia/nemotron-3-super-120b-a12b.
- Alias leve: nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b.
- RAM limitada (~2.96 GiB observados anteriormente); evitar concorrência excessiva.
- Instruções globais: C:\ProgramasGodMode\ClaudeCode-Global-Instructions.md e %USERPROFILE%\.claude\CLAUDE.md.

## Resultados confirmados em 2026-10-09
1. node --check server.js e node --check public/app.js passaram.
2. Launcher oculto conseguiu iniciar a frio o dashboard.
3. /api/status confirmou ok=true, FCC servidor disponível, CLI disponível, 2 aliases e 6 projetos.
4. Browser de teste abriu a interface sem erros de consola observados.
5. Smoke test anterior do chat usou a ferramenta de leitura e devolveu nome/versão de `package.json`.
6. API rejeitou mensagem vazia e projeto inexistente com HTTP 400, e ID de cancelamento desconhecido com HTTP 404.
7. Segunda instância com porta 8091 ocupada terminou com `EADDRINUSE`/exit 1; a instância existente continuou saudável.
8. Cancelamento via endpoint devolveu `stopped=true`; a entrada ativa foi limpa e o ID passou a devolver 404. Não foram encontrados processos do teste ainda ativos.
9. Resposta sem ferramentas pelo alias `sonnet` devolveu `OK` em cerca de 31,6 s; o CLI reportou custo de `$0.100344`, ainda não confirmado como valor efetivamente faturado. Verificar o painel NVIDIA NIM antes de mais testes de consumo elevado.
10. Teste de edição real: pedido com `haiku` expirou após 180 s sem criar o ficheiro descartável; repetição com `sonnet` expirou após 90 s e chamou `Glob`, `Bash` e `Read`, mas não `Write`. Em ambos os casos o dashboard permaneceu saudável e não ficou ficheiro de teste. Tool-use/latência do fornecedor é a hipótese atual, ainda não confirmada. Edição real continua NÃO VALIDADA.

Não afirmar que todas as funcionalidades estão prontas. A execução de edição tem um timeout por investigar; o cancelamento foi validado ao nível da API, mas falta teste direto do botão na UI. Anexos, diffs, aprovações granulares e integração Android continuam por implementar/testar.

## Decisões e limites
- Manter o servidor apenas em 127.0.0.1. Não expor a rede sem autenticação e revisão de segurança.
- Não usar --dangerously-skip-permissions nem desativar proteções do Windows.
- sonnet e haiku são aliases FCC; os modelos reais são Nemotron Super e Nemotron Lightning, não Claude Sonnet/Haiku.
- Não há fallback automático confirmado.
- Histórico fica no browser e não está sincronizado entre dispositivos.
- Não incluir segredos, credenciais, logs pessoais nem tokens em GitHub ou ZIP.
- Preferência do utilizador: documentação atualizada durante o trabalho; no final, criar ZIP com setup, dependências, configuração, serviços/portas, ligações necessárias e diagnóstico.
- Não gerar ZIP final até a aplicação estar pronta e os testes essenciais concluídos.

## Próximos passos
1. Testar edição de um ficheiro descartável num projeto de teste.
2. Testar cancelamento de tarefa demorada e confirmar que termina a árvore de processos.
3. Melhorar o tratamento de erros/estados do streaming.
4. Implementar anexos e visualização de alterações com validação de segurança.
5. Testar arranque repetido, porta ocupada, FCC offline e projetos ausentes.
6. Atualizar documentação/changelog a cada marco.
7. Criar ZIP sem segredos nem caches; testar extração e instalação a partir do ZIP.
8. Confirmar commit e push para AndreVazao/andreos-memory.

## Referência
O guia completo da aplicação está em C:\ProgramasGodMode\ClaudeCode-Dashboard\README.md.
