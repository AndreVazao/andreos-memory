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
- Seleção entre sete caminhos de projeto fixos, incluindo o próprio dashboard.
- Dois aliases de modelo configurados via FCC.
- Botão de paragem e terminação de árvore de processos no Windows.
- Política CLI explícita: `acceptEdits`, ferramentas limitadas a Read/Write/Edit/Glob/Grep/Bash e comandos Bash autorizados por padrões restritos; nunca usar `--dangerously-skip-permissions`.
- Deteta bloqueios do Fact-Forcing Gate, apresenta aprovação/recusa inline e mostra falhas de ferramenta no feed de atividade.
- Pastas autorizadas permanentemente: configuração global `permissions.additionalDirectories`, 32 diretórios existentes neste PC; dashboard passa-os ao CLI com `--add-dir` e limita as regras de leitura às raízes autorizadas.
- Pastas pessoais reais incluem OneDrive, Ambiente de Trabalho, Documentos, Imagens, Downloads, Música, Vídeos e outras pastas de dados existentes. A pasta base selecionada no painel não limita as pastas autorizadas.
- Script de configuração com backup: `Configure-ClaudeCode-AuthorizedDirectories.ps1`; lista e limites: `AUTHORIZED_DIRECTORIES.md`.
- Watchdog de tarefa de 15 minutos por defeito; mensagem de erro visível se o processo terminar sem texto ou o modelo sinalizar erro. O timeout foi validado por sintaxe/reinício, mas o disparo ainda não foi testado com limite acelerado.
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
3. `/api/status` confirmou `ok=true`, FCC servidor disponível, CLI disponível, 2 aliases, 7 projetos e 32 pastas autorizadas.
4. Browser de teste abriu a interface sem erros de consola observados.
5. Smoke test anterior do chat usou a ferramenta de leitura e devolveu nome/versão de `package.json`.
6. API rejeitou mensagem vazia e projeto inexistente com HTTP 400, e ID de cancelamento desconhecido com HTTP 404.
7. Segunda instância com porta 8091 ocupada terminou com `EADDRINUSE`/exit 1; a instância existente continuou saudável.
8. Cancelamento via endpoint devolveu `stopped=true`; a entrada ativa foi limpa e o ID passou a devolver 404. Não foram encontrados processos do teste ainda ativos.
9. Resposta sem ferramentas pelo alias `sonnet` devolveu `OK` em cerca de 31,6 s; o CLI reportou custo de `$0.100344`, ainda não confirmado como valor efetivamente faturado. Verificar o painel NVIDIA NIM antes de mais testes de consumo elevado.
10. Nas primeiras tentativas de criação/edição, o Fact-Forcing Gate bloqueou `Write` e `Edit` até serem apresentados os factos exigidos; a proteção permaneceu ativa. Um teste posterior isolado confirmou a criação do ficheiro depois da aprovação explícita; o fecho do streaming dessa sessão continua por investigar.
11. UI de aprovação: Playwright confirmou que aparecem **Aprovar e continuar** e **Recusar**; recusar atualiza o estado sem enviar autorização. Com API simulada, aprovar enviou a mensagem de aprovação na mesma sessão e preservou projeto/modelo. Num teste real isolado, a primeira escrita foi bloqueada pelo Fact-Forcing Gate e, após aprovação explícita na sessão retomada, o ficheiro foi criado com o conteúdo exato esperado. O harness não recebeu o fim do streaming no período de espera e teve de ser terminado; não ficou `fcc-claude.exe` ativo. A escrita passou, mas o fecho limpo do streaming continua por investigar.
12. Pastas autorizadas: script executado com sucesso, backup datado de `settings.json` criado, plugins preservados e 32 pastas existentes adicionadas a `permissions.additionalDirectories`. O dashboard reiniciado reporta 32 caminhos autorizados e 7 projetos.

Não afirmar que todas as funcionalidades estão prontas. A escrita real após aprovação foi confirmada num ficheiro descartável, mas a conclusão/fecho do streaming na sessão retomada continua por investigar. A aprovação de comandos Bash não allowlisted, anexos, diffs e integração Android continuam por implementar/testar.

## Pastas autorizadas permanentemente
A lista completa e o script estão na aplicação e também nesta pasta de memória: `AUTHORIZED_DIRECTORIES.md` e `Configure-ClaudeCode-AuthorizedDirectories.ps1`. A cópia de execução principal está em `C:\ProgramasGodMode\ClaudeCode-Dashboard`. Inclui as raízes C: indicadas pelo utilizador, `Program Files (x86)` real e 18+ diretórios de dados pessoais existentes, incluindo OneDrive Desktop/Documentos/Imagens. O perfil `.claude\settings.json` tem `permissions.additionalDirectories`; o dashboard também passa as pastas existentes por `--add-dir`. O backup automático de settings foi criado. `C:\Windows`, `AppData`, browser profiles e credential stores continuam fora da lista; não se ativou bypass de permissões.

## Decisões e limites
- Manter o servidor apenas em 127.0.0.1. Não expor a rede sem autenticação e revisão de segurança.
- Não usar --dangerously-skip-permissions nem desativar proteções do Windows.
- Cada tarefa tem limite de 15 minutos por defeito (`CLAUDE_DASHBOARD_TASK_TIMEOUT_MS` para ajustar); timeout tenta terminar a árvore de processos, sem reverter alterações já realizadas.
- sonnet e haiku são aliases FCC; os modelos reais são Nemotron Super e Nemotron Lightning, não Claude Sonnet/Haiku.
- Não há fallback automático confirmado.
- Histórico fica no browser e não está sincronizado entre dispositivos.
- Não incluir segredos, credenciais, logs pessoais nem tokens em GitHub ou ZIP.
- Preferência do utilizador: documentação atualizada durante o trabalho; no final, criar ZIP com setup, dependências, configuração, serviços/portas, ligações necessárias e diagnóstico.
- Não gerar ZIP final até a aplicação estar pronta e os testes essenciais concluídos.

## Próximos passos
1. Investigar por que a sessão retomada cria o ficheiro aprovado mas o streaming não devolve a conclusão ao harness no período esperado; verificar eventos `done`/`exit` e limpeza da árvore de processos.
2. Validar uma edição de código num ficheiro descartável e testar o botão de cancelamento diretamente na UI.
3. Forçar o watchdog com limite acelerado e testar FCC offline, arranque repetido, porta ocupada e projetos ausentes.
4. Implementar fluxo de aprovação para comandos Bash fora da allowlist.
5. Implementar anexos e visualização de alterações com validação de segurança.
6. Atualizar documentação/changelog a cada marco.
7. Criar ZIP sem segredos nem caches; testar extração e instalação a partir do ZIP.
8. Confirmar commit e push para AndreVazao/andreos-memory.

## Referência
O guia completo da aplicação está em C:\ProgramasGodMode\ClaudeCode-Dashboard\README.md.
