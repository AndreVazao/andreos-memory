# Arquitetura - God Mode

## Componentes principais
- Android overlay com botões flutuantes.
- Memory Core para ler e escrever memória persistente.
- GitHub Connector para repos, ficheiros, commits e PRs.
- AI Router para encaminhar pedidos para IAs.
- Approval Gate para bloquear ações perigosas sem confirmação.
- Action Logger para registar histórico.

## Fluxo base
1. Capturar pedido ou contexto.
2. Identificar projeto.
3. Ler memória relevante.
4. Montar contexto compacto.
5. Enviar para IA.
6. Apresentar plano/resposta.
7. Pedir aprovação quando necessário.
8. Executar.
9. Atualizar histórico e última sessão.
