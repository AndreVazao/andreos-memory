# Migração da memória persistente para Git — 2026-10-07

## Estado

A partir deste checkpoint, `C:\AndreOS-Memory` é o clone local canónico da repo privada:

`AndreVazao/andreos-memory`

Branch: `main`

## Alterações consolidadas

1. Confirmado que o clone local está ligado ao GitHub e sincronizado.
2. Mantida a estrutura `AndreOS/00_INBOX`, `01_MEMORIA_NUCLEAR`, `02_PROJETOS`, `05_LOGS_IA` e `templates`.
3. Reforçada a regra de uma pasta de memória por projeto em `AndreOS/02_PROJETOS/`.
4. Criado `AndreOS/02_PROJETOS/INDEX_PROJETOS.md`.
5. Criado `AndreOS/01_MEMORIA_NUCLEAR/REGISTO_MEMORIAS_ASSISTENTE.md` para consolidar o contexto transversal de trabalho.
6. README reescrito para declarar Git/local como fonte canónica.
7. `memory.config.json` atualizado para declarar a repo Git como memória persistente e desativar Obsidian como mecanismo de persistência principal.
8. O antigo vault continua preservado em `C:\AndreOS-Memory-LEGACY-2026-10-07` apenas como arquivo de recuperação.
9. DGM-MAT continua a usar uma pasta de memória lógica única porque é um ecossistema composto por várias repos.
10. VAZÃO EVSE continua a usar uma pasta de memória lógica única para toda a plataforma e módulos.

## Regra operacional definitiva

`git pull → ler memória do projeto → trabalhar → atualizar memória → validar → commit → push`

Nenhuma memória importante deve depender apenas do histórico da conversa.

## Segurança

O repositório não deve receber passwords, tokens, API keys, cookies, chaves privadas, credenciais ou outros segredos.

O arquivo `C:\AndreOS-Memory-LEGACY-2026-10-07` não é fonte ativa e não deve ser usado para sincronização automática.
