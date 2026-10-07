# Script Comparator

Módulo reutilizável para comparação, análise e consolidação segura de várias versões do mesmo script.

## Estrutura

- `MEMORIA_MESTRE.md` — objetivo e contrato.
- `ARQUITETURA.md` — desenho técnico e API.
- `DECISOES.md` — decisões de arquitetura.
- `BACKLOG.md` — evolução planeada.
- `MODULO_SCRIPT_COMPARATOR.py` — implementação core sem GUI.

## Integração

O anfitrião pode importar o módulo e chamar:

```python
from MODULO_SCRIPT_COMPARATOR import analyze_files, consolidate_group

infos = analyze_files(paths)
result = consolidate_group(paths)
```

O núcleo não cria janelas nem depende de PyQt. Uma aplicação pode construir a sua própria GUI sobre a API.

## Regra operacional

Nunca usar o módulo como "copiador de linhas". O objetivo é recuperar funcionalidades com contexto, preservar versões, criar backup e expor conflitos.

## Fonte de verdade

A documentação persistente deste componente está na repo `AndreVazao/andreos-memory`, dentro de `AndreOS/02_PROJETOS/SCRIPT_COMPARATOR/`.
