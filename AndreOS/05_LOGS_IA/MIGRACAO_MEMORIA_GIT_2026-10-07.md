# Migração da memória persistente para GitHub — 2026-10-07

## Objetivo

Transformar `C:\AndreOS-Memory` na cópia local sincronizada da repo privada `AndreVazao/andreos-memory`.

## Trabalho realizado

1. Preservado o antigo vault em `C:\AndreOS-Memory-LEGACY-2026-10-07`.
2. Clonada a repo GitHub para `C:\AndreOS-Memory`.
3. Mantida a estrutura existente do AndreOS Memory OS.
4. Migrada a memória antiga para as respetivas áreas de projeto.
5. Criadas áreas explícitas para DGM-MAT, DGM-MCP, DGM-HUB, OLLAMA, VAZÃO EVSE e n8n.
6. Criado contrato de persistência por projeto.
7. Atualizado o README para declarar o clone local e GitHub como fonte de memória persistente.
8. Mantidos os segredos fora do repositório.

## Regra daqui para a frente

Memória relevante → projeto → commit → push.

A sincronização GitHub/local deve ser verificada antes e depois de operações importantes.
