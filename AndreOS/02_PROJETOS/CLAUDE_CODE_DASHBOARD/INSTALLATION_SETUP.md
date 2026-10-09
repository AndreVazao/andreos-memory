# Installation & Setup — Claude Code Dashboard

**Estado:** guia de setup do protótipo v0.1.0, Windows. Rever este guia durante estabilização e antes do ZIP final.

## A. Instalações necessárias

### 1. Windows e Node.js
- Sistema alvo: Windows 10/11.
- Instalar Node.js LTS >=18.
- Confirmar em PowerShell: node --version e npm --version.
- Ambiente observado em 2026-10-09: Node v24.20.0, npm 11.16.0.

### 2. Free Claude Code (FCC)
- Instalar FCC seguindo o procedimento oficial/provider aprovado para o ambiente.
- O perfil do utilizador deve conter:
  - %USERPROFILE%\.local\bin\fcc-server.exe
  - %USERPROFILE%\.local\bin\fcc-claude.exe
- O dashboard não inclui FCC nem redistribui binários.
- Confirmar o painel local em http://127.0.0.1:8082/admin.
- Confirmar que o fornecedor está configurado e autenticado no FCC. Não colocar chaves no repositório ou nos logs.
- Neste PC o fornecedor configurado é NVIDIA NIM; quotas, disponibilidade e eventuais custos devem ser confirmados no respetivo painel.

### 3. CLI Node-compatible
- A instalação atual usa C:\ProgramasGodMode\tools\claude-code-node-2.1.112\package\cli.js.
- O caminho é fixo no server.js nesta versão.
- Ao reinstalar noutro caminho, atualizar CLAUDE_CLI em server.js e voltar a testar.
- Não assumir que a versão nativa mais recente é compatível com o CPU antigo deste PC.

### 4. Script de arranque do FCC
- A instalação atual depende de C:\ProgramasGodMode\DGM-MAT-Ensure-FCC-Server.ps1.
- O script arranca/verifica o FCC na porta 8082 e regista stdout/stderr em %LOCALAPPDATA%\DGM-MAT\logs.
- Numa instalação limpa, fornecer este script como dependência validada ou substituir por um launcher próprio documentado. Não copiar ficheiros DGM-MAT sem rever as dependências.

## B. Instalar os ficheiros do dashboard

1. Extrair a pasta ClaudeCode-Dashboard para C:\ProgramasGodMode\ClaudeCode-Dashboard.
2. Confirmar que existem server.js, package.json, public\index.html, public\style.css, public\app.js e os launchers.
3. A versão atual não usa dependências npm externas; o servidor utiliza módulos built-in do Node.js. Não executar npm install por rotina sem confirmar alterações ao package.json.
4. Confirmar e ajustar os caminhos de projeto no objeto PROJECTS de server.js:
   - C:\ProgramasGodMode
   - C:\ProgramasGodMode\DGM-MAT
   - C:\ProgramasGodMode\VAZAO-EVSE-Platform
   - C:\ProgramasGodMode\proventil
   - C:\ProgramasGodMode\baribudos-studio
   - C:\ProgramasGodMode\ai-devops-control-center
5. Confirmar que os projetos que devem aparecer existem realmente. Projetos inexistentes ficam indisponíveis.
6. Criar/confirmar o atalho do Ambiente de Trabalho apontando para Launch-ClaudeCode-Dashboard.vbs através de wscript.exe.
7. Manter os ficheiros de configuração e credenciais do FCC fora do pacote e do Git.

## C. Arranque

1. Clicar em Claude Code Dashboard no Ambiente de Trabalho.
2. O launcher executa Launch-ClaudeCode-Dashboard.vbs, que chama Launch-ClaudeCode-Dashboard.ps1 sem janela de consola.
3. O PowerShell chama DGM-MAT-Ensure-FCC-Server.ps1; se o FCC estiver pronto, inicia o servidor Node em background se a porta 8091 estiver livre.
4. O browser abre http://127.0.0.1:8091.
5. O uso diário é feito pela interface; não é necessário abrir terminal manualmente.

Alternativa de diagnóstico: C:\ProgramasGodMode\Start-ClaudeCode-Dashboard.cmd.

## D. Modelos e aliases

Configuração observada:
- Alias sonnet -> nvidia_nim/nvidia/nemotron-3-super-120b-a12b.
- Alias haiku -> nvidia_nim/nvidia/nemotron-3.5-lightning-30b-a3b.

Os aliases são usados por compatibilidade do CLI. Não são os modelos Claude originais. O modelo leve funcionou num teste mas não se confirmou mais rápido. Não há fallback automático validado. Verificar a configuração atual no FCC após reinstalação e não assumir que o acesso ao fornecedor é gratuito.

## E. Endereços e logs

- Dashboard: http://127.0.0.1:8091
- Estado do dashboard: http://127.0.0.1:8091/api/status
- FCC admin: http://127.0.0.1:8082/admin
- Logs FCC: %LOCALAPPDATA%\DGM-MAT\logs\fcc-server.stdout.log e fcc-server.stderr.log

O serviço está limitado a loopback. Não mudar para 0.0.0.0 nem expor a rede sem autenticação, proteção CSRF, firewall e revisão de segurança.

## F. Checklist pós-instalação

- [ ] node --version confirma Node >=18.
- [ ] fcc-server.exe e fcc-claude.exe existem.
- [ ] FCC admin responde em 127.0.0.1:8082.
- [ ] O fornecedor/modelo está autenticado e autorizado.
- [ ] O CLI Node-compatible existe no caminho configurado.
- [ ] O launcher oculto arranca o FCC/dashboard sem janela de terminal persistente.
- [ ] /api/status devolve ok=true e cliAvailable=true.
- [ ] Os projetos pretendidos aparecem disponíveis.
- [ ] Uma pergunta simples recebe resposta no chat.
- [ ] Um teste seguro de leitura de ficheiro funciona.
- [ ] Um teste de edição é feito apenas em ficheiro descartável.
- [ ] A paragem de uma tarefa de teste termina o processo esperado.
- [ ] Nenhum segredo, token, cookie ou log pessoal é incluído no pacote.

## G. Problemas comuns

**FCC indisponível:** abrir o painel FCC, confirmar os binários, verificar logs em %LOCALAPPDATA%\DGM-MAT\logs e validar configuração do fornecedor.

**CLI não encontrado:** verificar CLAUDE_CLI em server.js e instalar/copiar a versão compatível para o caminho previsto.

**Projeto indisponível:** confirmar a pasta e o objeto PROJECTS; não permitir caminhos arbitrários recebidos do browser.

**Porta 8091 ocupada:** identificar o processo que está a escutar antes de o terminar; não matar processos por nome indiscriminadamente.

**Dashboard abre mas chat falha:** consultar o estado da API, FCC admin e stderr; nunca imprimir credenciais nos logs.

## H. Segurança e limites

- A interface não remove as permissões do Claude Code.
- Não ativar bypass de permissões nem desativar proteções Windows.
- O botão de parar não reverte alterações já realizadas.
- Histórico local é guardado no browser; não está cifrado nem sincronizado.
- ADB, anexos e diffs ainda não estão integrados nesta versão.
- O ZIP final deve ser testado numa extração limpa e não pode ser anunciado como autónomo enquanto depender do FCC/fornecedor/CLI externo.
