# AndreOS Memory

Memória persistente canónica do ecossistema AndreOS.

## Fonte de verdade

- Local: `C:\AndreOS-Memory`
- GitHub: `AndreVazao/andreos-memory`
- Branch: `main`

A memória local e a memória GitHub são a mesma fonte lógica. O clone local é a cópia operacional; GitHub é a cópia persistente e sincronizável.

## Regra operacional

```text
git pull
  ↓
ler a memória do projeto
  ↓
trabalhar
  ↓
atualizar a memória
  ↓
validar
  ↓
git commit
  ↓
git push
```

A memória relevante não deve ficar apenas na conversa.

## Estrutura

```text
AndreOS/
├── 00_INBOX/                 # informação ainda não classificada
├── 01_MEMORIA_NUCLEAR/       # regras e contexto global
├── 02_PROJETOS/              # uma pasta de memória por projeto
├── 05_LOGS_IA/               # ações e checkpoints da IA
├── templates/                # modelos
└── memory.config.json        # contrato de operação
```

## Uma pasta por projeto

Cada projeto independente possui uma pasta própria em `AndreOS/02_PROJETOS/<PROJETO>/`.

Quando várias repos pertencem ao mesmo produto/ecossistema, a memória pode ser partilhada pela pasta do produto. Isto é intencional no DGM-MAT e no VAZÃO EVSE.

Contrato recomendado:

- `MEMORIA_MESTRE.md` — estado atual consolidado.
- `DECISOES.md` — decisões relevantes.
- `ARQUITETURA.md` — arquitetura e fronteiras.
- `BACKLOG.md` — próximos passos.
- `ULTIMA_SESSAO.md` — último checkpoint.
- `HISTORICO.md` — histórico quando necessário.

Não é obrigatório criar ficheiros vazios.

## Mapa de projetos

Consultar `AndreOS/02_PROJETOS/INDEX_PROJETOS.md`.

## Registo transversal da IA

O contexto persistente de trabalho consolidado encontra-se em:

`AndreOS/01_MEMORIA_NUCLEAR/REGISTO_MEMORIAS_ASSISTENTE.md`

Esse registo não substitui a memória específica de cada projeto.

## Segurança

Nunca guardar aqui passwords, tokens, API keys, cookies, chaves privadas, credenciais, dados bancários sensíveis ou dumps de runtime privados.

## Obsidian

O antigo vault Obsidian foi preservado apenas para recuperação em:

`C:\AndreOS-Memory-LEGACY-2026-10-07`

O vault legado não é a fonte principal.

## DGM-MAT

Todas as repos/componentes do ecossistema DGM-MAT podem continuar independentes no GitHub, mas partilham a memória lógica:

`AndreOS/02_PROJETOS/DGM-MAT/`

## VAZÃO EVSE

A plataforma VAZÃO EVSE e os seus módulos — carregadores AC, TestStation, CPMS/App, controlo, pagamentos e documentação técnica — usam:

`AndreOS/02_PROJETOS/VAZAO-EVSE/`

## Novos projetos

Antes de iniciar trabalho relevante:

1. `git pull`;
2. localizar/criar a pasta do projeto;
3. ler a memória;
4. trabalhar;
5. atualizar a memória;
6. validar;
7. commit;
8. push.
