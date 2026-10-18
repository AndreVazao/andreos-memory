# Avaliação cruzada dos relatórios Grok e Qwen — Família DGM-MAT

**Data da revisão:** 2026-10-18  
**Estado:** triagem documental e técnica; não equivale a auditoria completa das árvores Git, nem a execução de testes locais.  
**Fontes:** relatórios Grok e Qwen fornecidos pelo proprietário nesta conversa.

## Resumo executivo

Os relatórios apontam corretamente para a prioridade de reduzir dispersão e provar o cérebro DGM-MAT ponta a ponta antes de aumentar a arquitetura. Porém, algumas afirmações precisam de verificação factual e a proposta de sincronização não é segura para adoção direta.

Decisões que prevalecem:
- DGM-MAT é o cérebro soberano; o Headquarters é observacional.
- andreos-memory é a memória canónica de governação/continuidade.
- DGM-MAT-Memory é mantido como repositório seletivo de recuperação/sincronização operacional. Não é duplicado substituível por andreos-memory.
- Não clonar automaticamente satélites, repositórios privados ou terceiros para o workspace local.
- A distribuição por vários PCs é a direção arquitetural futura; a prioridade atual é estabilizar e provar o cérebro headless com cockpit simples.
- Não apagar, fundir, renomear ou mover conteúdo antes de inventariar dependências, consumidores, histórico e alterações não integradas.

## Verificação das alegações Qwen

### canonical_local_root

A alegação de que AndreOS/memory.config.json contém C:AndreOS-Memory está desatualizada ou incorreta relativamente ao ficheiro consultado no branch main em 2026-10-18. O valor publicado é:

    "canonical_local_root": "C:\\AndreOS-Memory"

A representação JSON com duas barras invertidas corresponde ao caminho Windows C:\AndreOS-Memory. Não alterar este valor sem nova evidência.

### Motor safe_sync.py

O script proposto não deve ser integrado nem executado tal como foi apresentado. Riscos identificados:

1. Usa git add ., podendo incluir ficheiros não revistos e não limitados à lista verificada.
2. Analisa apenas linhas de git status --porcelain que começam com dois padrões específicos; trata incorretamente renomes, cópias, conflitos, ficheiros staged e outros estados.
3. A análise por regex tem falsos negativos e falsos positivos; ignorar extensões como PDF/DB/SQLite não prova ausência de segredos.
4. Faz commit e push diretamente para main sem confirmar raiz Git, repositório, branch, remote, estado de merge, diff staged ou aprovação humana.
5. O caminho da configuração é relativo ao diretório corrente, não ao caminho do próprio script.
6. Falhas de leitura são ignoradas, podendo converter um erro de auditoria num falso sinal de segurança.
7. Não verifica se os ficheiros staged coincidem exatamente com os ficheiros examinados, nem volta a inspecionar o conteúdo final staged.
8. A mensagem de sucesso afirma que não foram expostos segredos, conclusão que regex simples não consegue garantir.

Se for construído um motor de sincronização, deverá começar em modo dry-run, trabalhar apenas numa allowlist explícita, verificar a raiz/repositório/branch esperados, examinar todos os ficheiros staged após staging explícito, bloquear estados ambíguos, nunca ignorar falhas de leitura, evitar push automático para main, exigir confirmação antes de mutações e documentar os limites de deteção. Preferir ferramentas maduras de secret scanning como defesa adicional, sem alegar garantia absoluta.

### Pastas core/sync, core/injector e core/agents

A existência de pastas não demonstra por si só que estão vazias ou que falta todo o motor. É necessária inspeção da árvore completa, conteúdo, histórico e consumidores. Não criar uma segunda implementação antes de verificar scripts, workflows e integração local existentes.

## Avaliação das tarefas Grok

| Tarefa | Avaliação | Decisão recomendada |
|---|---|---|
| T01 — congelar novos satélites e conceptualização | Reduzir scope é sensato, mas não deve impedir documentação de segurança, arquitetura vinculativa, correções e checkpoints necessários. | Moratória a novos satélites e features não essenciais até à auditoria; documentação apenas quando necessária para decisões, correções ou preservação. |
| T02 — remover artefactos de runtime do tracking | Importante, mas os caminhos concretos não foram confirmados nesta revisão. | Auditar .runtime/, estado persistido, ignore rules e consumidores; preservar artefactos úteis antes de remover tracking. |
| T03 — nomes enganadores/ficheiros vazios | Higiene de baixo risco apenas após confirmar caminhos e referências. | Verificar existência, histórico, links e consumidores; renomear/arquivar com alterações rastreáveis. Não presumir que ClaudeWorkTodayLog,txt ou architecture.md existem na branch atual sem inventário da árvore. |
| T04 — inventário canónico de satélites | Essencial e consistente com governação já existente. | Expandir/atualizar o inventário com presença, conteúdo real, testes, dependências, histórico, status e decisão; indicar data e evidência. |
| T05 — duplicação core/satélites | Importante, mas remoção de duplicados antes da análise pode perder funcionalidade ou trabalho local. | Mapear importações, chamadas, workflows, testes e histórico; decidir caso a caso entre migração validada, compatibilidade temporária ou arquivo. |
| T06 — memória canónica única | A formulação é enganadora e conflita com decisões explícitas anteriores. | Manter separação: andreos-memory = governação/continuidade; DGM-MAT-Memory = recuperação operacional seletiva. Auditar core/memory/ para determinar se é memória ativa do runtime, sem fundir papéis diferentes. |
| T07 — provar core headless | Prioridade P1 real e condição de base. | Validar arranque sem UI, persistência de missão, desconexão de cliente, erros de worker/satélite, reinício e resultado observável. Testes locais primeiro quando possível; CI apenas para gates necessários. |
| T08 — publicar/pinificar contratos | Necessário se o runtime realmente depende de instalar contratos externos. | Primeiro resolver dependência atual de DGM-Contracts, acesso privado e versões. Preferir referência imutável por tag/commit ou pacote versionado; não publicar código privado sem decisão explícita. |
| T09 — classificar documentação | Útil depois do inventário. | Aplicar estados normativos/atuais/históricos/superados com ligações para sucessores; preservar documentos históricos até compreender dependências. |
| T10 — departamento piloto | Útil depois de core e contratos comprovados. | Escolher um piloto após T07/T08 com contrato e critérios reais; não criar satélite novo apenas para cumprir a tabela. |
| T11 — reduzir workflows | Útil para custo e fiabilidade, mas desativar cegamente pode remover gates importantes. | Inventariar triggers, funções, consumo de minutos e gates cobertos; manter apenas workflows necessários e não iniciar execuções sem necessidade. |
| T12 — registar decisões | Obrigatório como processo contínuo. | Registar decisão, evidência, alternativas, impacto, data, estado e supersessão em andreos-memory. |

## Sequência ajustada

1. Preservar alterações não integradas e evitar criar novos satélites/features não essenciais.
2. Inventariar a árvore real e o estado Git, incluindo artefactos de runtime, ficheiros suspeitos, diretórios DGM-MAT-*, workflows e consumidores.
3. Atualizar a matriz canónica de satélites com evidência e decisão individual.
4. Auditar a duplicação core/satélites e o subsistema de memória sem confundir memória de governação, arquivo de recuperação e memória ativa do runtime.
5. Resolver o acesso/versionamento de DGM-Contracts e a divergência do PR de estabilização sem o integrar enquanto os gates end-to-end falharem.
6. Provar o ciclo headless de missão até resultado persistido, desconexão/reinício e recuperação.
7. Só então escolher o departamento piloto, ajustar CI e criar a próxima branch limpa a partir de uma base verificada.

## Limites da revisão

Nesta revisão foi confirmado o conteúdo atual de AndreOS/memory.config.json e consultados os documentos principais de governação/README no GitHub. Não foi feita uma inspeção completa do clone local, de todos os branches, de todos os ficheiros e consumidores, nem execução de testes Windows. Os itens T02/T03 e o estado das pastas de código continuam por verificar. Não declarar o core estabilizado com base apenas nestes relatórios.
