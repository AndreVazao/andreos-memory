# Script Comparator — Arquitetura do módulo reutilizável

## Princípio

O motor é uma biblioteca Python headless. A GUI é uma camada externa.

    Programa anfitrião
    GUI / API / CLI / agente / mobile
                │
                ▼
          script_comparator
       ┌──────────────────────┐
       │ descoberta           │
       │ agrupamento          │
       │ análise              │
       │ escolha da base      │
       │ merge por formato    │
       │ conflitos            │
       │ validação            │
       │ backup / renomeação  │
       └──────────────────────┘
                │
                ▼
         ficheiros + relatório

## Camadas

### 1. API pública

src/script_comparator/__init__.py expõe o contrato que consumidores devem usar.

### 2. Core

src/script_comparator/core.py contém a implementação sem dependências externas.

### 3. Compatibility shim

MODULO_SCRIPT_COMPARATOR.py mantém imports antigos funcionais durante a migração.

### 4. Testes

tests/test_core.py valida regras críticas de agrupamento, recuperação Python e bloqueio de conflitos.

## Estratégia por linguagem

- Python: AST para símbolos e estrutura top-level; inserção antes do main guard quando apropriado.
- JSON/JSONC: merge de objetos e conflito explícito em valores divergentes.
- Outros textos: SequenceMatcher + âncoras de linhas para inserir blocos no ponto aproximado de origem. Nunca assumir que append ao fim é semanticamente correto.

## Contrato de dados

FileInfo representa a análise de um ficheiro.

Conflict representa uma divergência que não deve ser resolvida automaticamente.

MergeResult é o contrato final consumido pela GUI/aplicação anfitriã.

## Responsabilidade do anfitrião

O núcleo não decide UX. O anfitrião decide seleção de ficheiros, preview, aprovação, logs, permissões, notificações e apresentação de conflitos.

O núcleo também não deve receber credenciais, tokens ou acesso a serviços externos.

## Evolução futura

Adapters por linguagem devem ser adicionados sem quebrar a API pública. A estratégia recomendada é adapter → análise estrutural → merge → validação, com fallback seguro quando não existir parser confiável.
