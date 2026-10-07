# Script Comparator — Memória Mestre

**Estado:** módulo reutilizável refatorado e preparado para integração externa — 2026-10-07.

## Decisão principal

O Script Comparator/Consolidator passa a ser tratado como **biblioteca independente**. O programa visual futuro será apenas um consumidor dessa biblioteca.

O core não depende de PyQt, FastAPI, React, Android, DGM-MAT ou serviços externos.

## Fonte técnica

    AndreOS/02_PROJETOS/SCRIPT_COMPARATOR/
    ├── src/script_comparator/__init__.py
    ├── src/script_comparator/core.py
    ├── tests/test_core.py
    ├── pyproject.toml
    └── MODULO_SCRIPT_COMPARATOR.py  # compatibility shim

## Como outro projeto deve consumir

Preferência:

1. importar script_comparator como dependência versionada quando existir uma release;
2. enquanto isso, incorporar src/script_comparator/ como componente Git/vendor controlado;
3. usar o shim apenas para compatibilidade de código antigo.

O consumidor deve tratar MergeResult como contrato e nunca ignorar validated=False ou conflicts.

## Funcionalidade

- agrupa versões por base + extensão;
- escolhe base por evidência de completude;
- recupera funções/classes/chaves quando seguro;
- preserva versões originais;
- cria backup;
- bloqueia conflitos por defeito;
- valida resultado;
- suporta processamento de múltiplos grupos.

## Limitação

Merge semântico universal não existe. A biblioteca deve preferir conflito explícito a uma alteração potencialmente destrutiva.

## Regra de evolução

Mudanças na API pública devem ser documentadas e testadas antes de qualquer consumidor externo ser atualizado.
