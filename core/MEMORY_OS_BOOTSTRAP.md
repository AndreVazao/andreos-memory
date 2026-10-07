# ANDREOS MEMORY OS — BOOTSTRAP CORE

## 1. Sistema

Este repositório é a camada canónica de memória persistente do ecossistema AndreOS.

**Local canónico:** `C:\AndreOS-Memory`
**GitHub:** `AndreVazao/andreos-memory`

## 2. Arquitetura

```text
C:\AndreOS-Memory
│
├─ AndreOS/
│  ├─ 01_MEMORIA_NUCLEAR/       regras globais
│  ├─ 02_PROJETOS/              memória por projeto
│  └─ 05_LOGS_IA/               checkpoints
│
├─ core/                         Memory OS
└─ projects/                     compatibilidade
```

## 3. Regra de projeto

Cada projeto possui uma pasta própria em:

`AndreOS/02_PROJETOS/<PROJETO>/`

Várias repos que formem um único produto/ecossistema podem partilhar a mesma pasta de memória.

## 4. Sincronização

Fluxo recomendado:

1. `git pull`
2. ler a memória do projeto
3. trabalhar
4. atualizar `MEMORIA_MESTRE.md` / decisões / sessão
5. validar
6. `git commit`
7. `git push`

## 5. Obsidian

O Obsidian pode ser usado como interface de consulta/edição sobre esta memória, mas a persistência de projeto é o Git.

## 6. Segurança

Nunca guardar neste repositório:

- passwords
- tokens
- API keys
- cookies
- chaves privadas
- credenciais
- dados sensíveis de clientes

## 7. Recuperação

A migração de 2026-10-07 deixou o vault anterior em:

`C:\AndreOS-Memory-LEGACY-2026-10-07`

Esse diretório é somente recuperação e não é a fonte principal.
