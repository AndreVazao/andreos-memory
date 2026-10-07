# Script Comparator — Decisões

## D01 — biblioteca primeiro
O motor é tratado como componente reutilizável, não como código interno de uma GUI.

## D02 — API pública estável
Consumidores importam de script_comparator; detalhes internos podem evoluir sem obrigar todos os anfitriões a conhecer a implementação.

## D03 — zero dependências externas no core
O núcleo usa apenas a biblioteca standard Python para facilitar integração em programas diferentes.

## D04 — compatibilidade durante migração
MODULO_SCRIPT_COMPARATOR.py continua como shim para integrações antigas.

## D05 — extensão faz parte da identidade
main.py e main.js nunca são tratados como versões do mesmo ficheiro.

## D06 — conflito bloqueia por defeito
Um conflito não é licença para escolher arbitrariamente uma implementação.

## D07 — backup antes de mutação
Nenhuma consolidação destrutiva deve ocorrer sem backup.

## D08 — sem append cego
Funcionalidade recuperada deve ser inserida no contexto aproximado da origem; para linguagens suportadas estruturalmente, usar AST/parser.

## D09 — GUI fora do core
PyQt, web UI, mobile UI, FastAPI e integrações com DGM-MAT são consumidores, não dependências do motor.

## D10 — versionamento futuro
Quando o primeiro consumidor externo estiver validado, publicar uma release versionada e definir política de compatibilidade da API.
