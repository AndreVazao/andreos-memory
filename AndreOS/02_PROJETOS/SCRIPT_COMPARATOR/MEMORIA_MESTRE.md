# Script Comparator — Memória Mestre

**Estado:** módulo reutilizável definido e registado em 2026-10-07.

## Objetivo

Criar um componente reutilizável para integrar em outros programas AndreOS e resolver o problema de múltiplas versões do mesmo script criadas durante desenvolvimento iterativo.

Exemplo:

```text
main.py
main01.py
main002.py
main_final.py
```

O componente deve agrupar ficheiros pela base lógica do nome + extensão, preservar a extensão original, analisar conteúdo e estrutura, escolher uma versão-base por critérios de completude, recuperar funcionalidades presentes noutras versões, detetar conflitos, validar o resultado, criar backup e reservar o nome canónico para o resultado final.

## Regra de nomes

Para uma família `main.py`, `main01.py`, `main002.py`:

- resultado consolidado: `main.py`;
- versões preservadas: `main001.py`, `main002.py`, etc.;
- extensão sempre preservada.

O mesmo contrato aplica-se a `.json`, `.kt`, `.css`, `.html`, `.js` e outras extensões de texto suportadas.

## Regra de segurança

O módulo nunca deve interpretar "mais linhas" como sinónimo de "melhor código".

Não deve simplesmente copiar linhas de um diff para o fim do ficheiro.

Merges ambíguos devem ser reportados como conflitos e não aplicados silenciosamente.

## Separação por linguagem

Extensões diferentes pertencem a grupos diferentes. `main.py` + `main01.py` pode ser consolidado; `main.py` + `main.js` não deve ser misturado.

## Implementação

A referência sem GUI ficará em:

`AndreOS/02_PROJETOS/SCRIPT_COMPARATOR/MODULO_SCRIPT_COMPARATOR.py`

A API é independente de PyQt e pode ser integrada em DGM-MAT, Build Control Center, script-reviewer-mobile ou outros programas AndreOS.

## Validação

Python usa AST quando possível. JSON usa parsing JSON. Outras linguagens usam análise textual conservadora.

## Backup

Princípio obrigatório:

`analisar → backup → preparar resultado → validar → alterar nomes/escrever final`.

## Limitação assumida

Não existe merge semântico 100% seguro para todas as linguagens através de heurísticas genéricas. O objetivo é maximizar automação segura e nunca esconder conflitos.
