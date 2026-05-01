# Arquitetura - Baribudos Studio

## Backend
Repo `AndreVazao/baribudos-studio` usa FastAPI.

## Memoria persistente implementada
- Servico: `studio_core/services/persistent_memory_service.py`
- Router: `studio_core/api/routes/persistent_memory.py`
- Integracao: `studio_core/api/main.py`
- Runtime path: `storage/memory/AndreOS`

## Filosofia
- Markdown e a fonte humana legivel.
- `storage/memory/` e runtime local e fica fora do Git.
- `AndreVazao/andreos-memory` e memoria longa privada.
- Website continua como camada publica/comercial, sem guardar memoria operacional sensivel.

## Fluxo
1. Studio arranca.
2. `initialize_memory_core()` cria estrutura local.
3. Dashboard chama endpoints de memoria.
4. IA usa `/context` para receber contexto compacto.
5. Decisoes e historico sao gravados.
6. Resumos importantes sao enviados para AndreOS Memory privado.
