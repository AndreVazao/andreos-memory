# Script Comparator — Arquitetura

## Camadas

```text
Programa anfitrião
      │
      ▼
Script Comparator API
      ├── descoberta e agrupamento
      ├── análise de completude
      ├── análise estrutural
      ├── consolidação por linguagem
      ├── deteção de conflitos
      ├── validação
      ├── backup
      └── normalização de nomes
```

## API

- `analyze_file(path)`
- `analyze_files(paths)`
- `group_files(paths)`
- `choose_base(infos)`
- `validate_text(text, extension)`
- `backup_files(paths)`
- `plan_version_names(base, extension, count)`
- `consolidate_group(paths, ...)`
- `consolidate_all(paths, ...)`

## Modelo

### FileInfo
Caminho, nome/base, extensão, grupo canónico, encoding, validade sintática, linhas, símbolos e score.

### Conflict
Tipo, símbolo/chave, ficheiro-base, origem e detalhe.

### MergeResult
Grupo, base, resultado, alterações, validação, conteúdo recuperado, conflitos, backup e avisos.

## Estratégia

**Python:** AST para funções/classes e validação. Símbolos ausentes podem ser recuperados. Divergências do mesmo símbolo ficam em conflito, salvo quando uma versão é claramente uma extensão da outra.

**JSON:** merge de chaves em objetos. Chaves novas podem ser recuperadas; valores divergentes são conflito.

**Outras linguagens:** fallback textual conservador com SequenceMatcher.

## GUI futura

A GUI fica fora do núcleo e pode fornecer seleção, score, preview, conflitos, aprovação e histórico.
