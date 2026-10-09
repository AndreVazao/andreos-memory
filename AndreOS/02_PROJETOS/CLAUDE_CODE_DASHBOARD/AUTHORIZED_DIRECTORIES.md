# Path: C:\ProgramasGodMode\ClaudeCode-Dashboard\AUTHORIZED_DIRECTORIES.md
# Claude Code — autorização permanente de diretórios (Windows)

**Estado:** configurado em 2026-10-09. Fonte persistente no PC: %USERPROFILE%\.claude\settings.json, propriedade permissions.additionalDirectories. O dashboard aplica a mesma lista por sessão através de --add-dir e gera regras de leitura específicas.

## Pastas autorizadas no C:

- C:\AI
- C:\AndreOS-Memory
- C:\AndreOS-Memory-LEGACY-2026-10-07
- C:\CloneZIP
- C:\DevopGodMode
- C:\DevopsGodMode
- C:\Lords Mobile PC
- C:\Programas
- C:\ProgramasGodMode
- C:\ProgramData
- C:\ProjectFlux
- C:\ProjectMind
- C:\Projects
- C:\WinClean
- C:\Program Files (x86) — pasta real equivalente ao nome referido como Programas (x86).

## Pastas pessoais autorizadas que existem neste PC

O script verifica a existência das pastas antes de as adicionar; caminhos ausentes não são criados automaticamente.

- C:\Users\<perfil>\OneDrive (inclui pastas sincronizadas)
- C:\Users\<perfil>\Documents
- C:\Users\<perfil>\Os Meus Documentos
- C:\Users\<perfil>\Downloads
- C:\Users\<perfil>\Music
- C:\Users\<perfil>\Videos
- C:\Users\<perfil>\3D Objects
- C:\Users\<perfil>\Contacts
- C:\Users\<perfil>\Favorites
- C:\Users\<perfil>\Links
- C:\Users\<perfil>\Saved Games
- C:\Users\<perfil>\Searches
- C:\Users\<perfil>\Modelos
- Ambiente de Trabalho real: OneDrive\Ambiente de Trabalho
- Documentos reais redirecionados: OneDrive\Documentos
- Imagens reais redirecionadas: OneDrive\Imagens
- OneDrive\Anexos
- Pastas especiais do Windows devolvidas por [Environment]::GetFolderPath (Desktop, MyDocuments, MyPictures, MyMusic, MyVideos), quando existem.

## Como funciona

- permissions.additionalDirectories torna estes diretórios conhecidos/acessíveis ao Claude Code entre sessões; não é necessário voltar a indicar cada caminho.
- O dashboard passa a lista existente ao CLI em --add-dir e permite leitura com regras Read(//caminho/**).
- O diretório selecionado no painel continua a ser a pasta de trabalho/base da tarefa; não limita a lista de pastas autorizadas.
- O script Configure-ClaudeCode-AuthorizedDirectories.ps1 aplica a configuração persistente, junta-se às pastas já configuradas, cria uma cópia de segurança de settings.json e não ativa bypassPermissions.
- Depois de uma atualização ao CLI/settings, reiniciar sessões Claude Code para recarregar a configuração.
- O dashboard está limitado a 127.0.0.1:8091; FCC usa 127.0.0.1:8082.

## Limites de segurança mantidos

- Não foi autorizado o disco C:\ inteiro.
- C:\Program Files ficou fora por não ter sido pedido. C:\Windows, pastas de recuperação, AppData, perfis de browser, diretórios ocultos de credenciais e tokens também ficaram fora por defeito.
- C:\ProgramData foi pedido explicitamente; C:\Program Files (x86) foi incluído como equivalente real de Programas (x86). Alterações a programas instalados, definições de segurança ou serviços continuam a ser operações sensíveis.
- A autorização de caminho não é autorização para apagar dados, remover backups, desinstalar programas, fazer commit/push ou alterar segurança sem revisão quando a ação for destrutiva ou irreversível.
- Esta configuração elimina a necessidade de escolher/indicar os caminhos autorizados; não promete eliminar todas as confirmações de segurança internas do Claude Code.

## Manutenção

Executar quando forem adicionadas pastas novas ou após reinstalar:

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\ProgramasGodMode\ClaudeCode-Dashboard\Configure-ClaudeCode-AuthorizedDirectories.ps1"

O script adiciona apenas pastas que existem, conserva as definições existentes e cria backup datado. Não colocar tokens, cookies ou segredos no ficheiro.
