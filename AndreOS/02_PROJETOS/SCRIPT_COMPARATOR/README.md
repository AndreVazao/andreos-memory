# AndreOS Script Comparator & Consolidator

**Estado:** núcleo reutilizável / biblioteca, sem GUI e sem dependências externas.

> **IMPORTANTE:** este projeto não é apenas um programa com uma janela. O motor foi separado deliberadamente como **módulo reutilizável**. Qualquer outro programa AndreOS pode consumi-lo sem importar PyQt, sem abrir janelas e sem conhecer a implementação interna.

## O que resolve

Durante desenvolvimento iterativo é comum existirem várias versões do mesmo ficheiro:

    main.py
    main01.py
    main002.py
    main_final.py

O motor agrupa essas versões por nome lógico + extensão, analisa estrutura/completude, escolhe uma base, recupera funcionalidades ausentes quando a evidência é suficiente, deteta conflitos, valida o resultado, cria backup e preserva as versões originais com nomes numerados.

**Nunca** é objetivo simplesmente copiar todas as linhas adicionadas de um diff para o fim do ficheiro.

## Arquitetura atual

    SCRIPT_COMPARATOR/
    ├── src/
    │   └── script_comparator/
    │       ├── __init__.py       <- API pública
    │       └── core.py           <- motor reutilizável
    ├── tests/
    │   └── test_core.py          <- regressão do núcleo
    ├── MODULO_SCRIPT_COMPARATOR.py <- compatibilidade com integrações antigas
    ├── pyproject.toml            <- empacotamento Python
    ├── README.md
    ├── ARQUITETURA.md
    ├── DECISOES.md
    ├── BACKLOG.md
    └── MEMORIA_MESTRE.md

## API pública

    from script_comparator import (
        analyze_file,
        analyze_files,
        group_files,
        choose_base,
        validate_text,
        backup_files,
        plan_version_names,
        preview_group,
        consolidate_group,
        consolidate_all,
    )

O resultado principal é MergeResult, contendo base escolhida, ficheiro de saída, validação, alterações recuperadas, conflitos, backup e avisos. Para operação segura antes de qualquer escrita existe PreviewResult através de preview_group(), que calcula o plano completo sem criar backup, renomear ou modificar ficheiros.

## Como usar noutro projeto

### Opção A — integração direta por código-fonte

Indicada enquanto a biblioteca ainda está em evolução.

1. Copiar a pasta src/script_comparator/ para o projeto anfitrião.
2. O programa anfitrião passa a importar de script_comparator.
3. Manter os testes do componente ou executar a suíte original antes de atualizar a cópia.

### Opção B — Git como componente partilhado

Quando vários repositórios precisarem da mesma versão, manter este projeto como fonte de verdade e integrá-lo como submodule/vendor controlado ou outro mecanismo de dependência Git aprovado pelo projeto anfitrião.

O contrato é a pasta src/script_comparator/. Documentação e GUI não fazem parte da dependência runtime.

### Opção C — pacote Python

O pyproject.toml já prepara o projeto para empacotamento. Quando houver uma release estável, o pacote poderá ser instalado a partir de um índice privado, Git ou outro registry adotado pelo ecossistema AndreOS.

Não é necessário PyQt, FastAPI, React, Ollama ou qualquer serviço externo.

## Contrato de integração

O programa anfitrião deve:

1. fornecer caminhos de ficheiros válidos;
2. separar ou permitir que o motor agrupe automaticamente por extensão;
3. apresentar MergeResult ao utilizador;
4. tratar conflicts como decisão pendente;
5. não ignorar validated=False;
6. preservar o diretório de backup;
7. decidir quando executar uma consolidação destrutiva/renomeação;
8. manter a responsabilidade da GUI, permissões, logs e UX fora do núcleo.

### Fluxo recomendado

    Selecionar ficheiros
          ↓
    analyze_files / group_files
          ↓
    preview_group (zero escrita)
          ↓
    aprovação do utilizador
          ↓
    consolidate_group / consolidate_all
          ↓
    backup automático
          ↓
    merge estrutural
          ↓
    validação
          ↓
    válido + sem conflito → resultado consolidado
    conflito              → decisão humana
    inválido               → nenhuma escrita final

## Segurança e limites

- Extensões diferentes nunca são misturadas.
- Backup é criado antes da alteração.
- Conflitos bloqueiam escrita por defeito.
- Python usa AST.
- JSON usa parsing estruturado.
- Outros formatos usam fallback textual conservador com âncoras, não append cego.
- Não existe promessa de merge semântico perfeito para todas as linguagens.
- O motor prefere deixar um conflito para decisão humana a inventar uma solução destrutiva.

## Compatibilidade

MODULO_SCRIPT_COMPARATOR.py permanece como ponto de compatibilidade. Integrações antigas podem continuar a fazer import a partir desse ficheiro enquanto migram para src/script_comparator/.

## Próximo passo para reutilização em escala

Antes de declarar uma release estável para múltiplos projetos:

- aumentar cobertura de testes por linguagem;
- adicionar adapters específicos para JS/TS, Kotlin/Java/C#, HTML/CSS;
- melhorar merge semântico por AST onde houver parser seguro;
- criar relatório JSON/HTML estável;
- definir versionamento semântico;
- publicar uma primeira release interna;
- migrar um consumidor real, começando por script-reviewer-mobile ou outro projeto adequado;
- validar atualização do componente sem quebrar consumidores.

**Fonte de verdade:** AndreVazao/andreos-memory, em AndreOS/02_PROJETOS/SCRIPT_COMPARATOR/.
