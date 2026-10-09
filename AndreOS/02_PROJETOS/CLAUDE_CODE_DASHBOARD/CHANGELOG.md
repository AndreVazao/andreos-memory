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
