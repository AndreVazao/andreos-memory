# Changelog — Claude Code Dashboard

## 2026-10-09 — v0.1.0 inicial
- Criada interface de chat local com histórico e streaming.
- Adicionados seletor de projeto e seletor de aliases do FCC.
- Criado endpoint de estado e endpoint de paragem.
- Adicionado watchdog de 15 minutos por defeito para evitar tarefas presas indefinidamente e melhorado o feedback quando o processo termina sem texto/assinala erro.
- Criado launcher VBS/PowerShell para arranque oculto e atalho no Ambiente de Trabalho.
- Documentados pré-requisitos, setup, modelos, serviços/portas, diagnóstico e limites.
- Validados syntax checks, endpoint de estado, validação de entrada, projeto inexistente, ID de paragem inválido e conflito de porta.
- Cancelamento via endpoint confirmou limpeza da tarefa ativa e ausência de processo do teste ainda ativo.
- Resposta sem ferramentas via alias `sonnet` devolveu `OK` em cerca de 31,6 s; CLI reportou custo de `$0.100344`, não confirmado como valor faturado.
- Edição real não validada: `haiku` expirou aos 180 s; `sonnet` expirou aos 90 s após chamadas `Glob`, `Bash` e `Read`, sem `Write`. Tool-use/latência ainda por diagnosticar.
- Em aberto: diagnosticar o timeout de execução/fornecedor, testar o botão de cancelamento na UI, FCC offline, arranque repetido, anexos, diffs e empacotamento.
