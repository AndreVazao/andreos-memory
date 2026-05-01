# AndreOS Memory

Repositório privado de memória persistente de programação, decisões técnicas e contexto das repos do ecossistema AndréOS.

## Papel deste repo

Este repo NÃO é a memória operacional diária dos programas instalados no PC.

Este repo serve para guardar contexto de desenvolvimento, auditoria e programação, por exemplo:

- O que foi alterado nas repos.
- Porque uma decisão técnica foi tomada.
- Como uma arquitetura ficou definida.
- Que endpoints, scripts, builds, deploys e integrações foram criados.
- Que problemas foram encontrados e como foram resolvidos.
- Contexto para ChatGPT, God Mode e futuras sessões de programação.

## Separação obrigatória

```text
Programas instalados no PC
└── Memória operacional local
    ├── Obsidian local
    ├── storage local
    └── ficheiros/runtime privados do computador

GitHub / andreos-memory
└── Memória de programação e contexto técnico das repos
    ├── decisões de arquitetura
    ├── histórico de alterações
    ├── auditorias
    └── instruções para futuras alterações de código
```

## Ponte com ferramentas

Este repo pode funcionar como ponte de contexto entre:

- Obsidian
- ChatGPT
- God Mode
- GitHub
- Repos públicas e privadas
- Projetos pessoais e empresariais

Mas a regra é clara: aqui fica memória técnica e contexto de desenvolvimento. A execução real dos programas e o progresso de trabalho local ficam no PC.

## Vault principal

O vault Obsidian local fica em:

```text
AndreOS/
```

O Obsidian pode sincronizar ou consultar notas equivalentes, mas não deve transformar este repo num depósito de segredos ou dados privados de clientes.

## Projetos iniciais

- GOD_MODE
- PROVENTIL
- VERBAFORGE
- BOT_LORDS_MOBILE
- ECU_REPRO
- BUILD_CONTROL_CENTER
- BARIBUDOS_STUDIO
- BARIBUDOS_STUDIO_WEBSITE

## Regra crítica de segurança

Não guardar aqui passwords, tokens, chaves API, cookies, chaves privadas, credenciais de clientes, dados bancários sensíveis ou ficheiros runtime privados dos programas.

## Como usar comigo

Quando quiseres que eu use esta memória para programação, escreve:

```text
Usa a memória AndreOS no repo AndreVazao/andreos-memory antes de mexer na repo.
Projeto: BARIBUDOS_STUDIO.
Pedido: ...
```

Quando o assunto for uso diário do programa no PC, a fonte principal deve ser o Obsidian/local runtime do computador, não este repo.
