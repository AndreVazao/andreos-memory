# CodeRabbit — política de revisão GitHub para projetos públicos

**Criado:** 2026-10-18  
**Âmbito:** transversal aos projetos públicos de AndreVazao; aplicação inicial em DGM-MAT.

## Objetivo

Usar CodeRabbit como revisor automático adicional nos Pull Requests dos projetos públicos, para encontrar regressões, riscos de segurança, inconsistências, problemas de testes, documentação e oportunidades de simplificação antes do merge.

## Fluxo obrigatório

1. Abrir PR pequeno e com propósito claro; não misturar refatorações sem relação.
2. Deixar a CI/testes relevantes executar. CodeRabbit é uma camada adicional, não substitui testes, análise humana, validação local nem prova do comportamento em Windows.
3. Pedir/reconfirmar revisão após a última alteração relevante do PR. CodeRabbit é incremental e pode não rever novamente commits já analisados; verificar que a revisão corresponde ao HEAD atual.
4. Classificar cada finding como bloqueador, importante, menor ou falso positivo, guardando a justificação.
5. Confirmar cada finding no código, contratos, chamadores, histórico e testes antes de alterar.
6. Corrigir os findings válidos com alterações pequenas e reversíveis; acrescentar testes de regressão quando adequado.
7. Reexecutar os testes e a CI após as correções. Não fazer merge enquanto houver falhas obrigatórias sem explicação e decisão explícita.
8. Registar o resultado no PR e na memória do projeto quando a decisão afetar arquitetura, segurança ou procedimento futuro.

## Limites e segurança

- CodeRabbit é assessor, não autoridade: não aceitar sugestões automaticamente nem ativar autofix em lote sem inspeção.
- Nunca confiar num resumo como prova de que os testes passaram; consultar os jobs/logs reais do GitHub Actions.
- Nunca expor tokens, segredos, dados privados, ficheiros locais sensíveis ou contexto de utilizadores nos comentários/prompts.
- Não reduzir requisitos de segurança ou remover testes para obter CI verde.
- A revisão automática pode falhar, estar incompleta, desatualizada ou não cobrir todos os ficheiros. Verificar o commit/HEAD revisto e pedir nova revisão quando necessário.
- Não assumir que a disponibilidade/preço do CodeRabbit é permanente; confirmar as condições atuais para cada tipo de repositório/plano quando isso for relevante.
- Projetos privados: não presumir que a cobertura/condições de uso são iguais às dos projetos públicos.

## Regra para o DGM-MAT

Ordem de evidência: **CI/testes reproduzíveis + revisão do diff e contratos + CodeRabbit + validação Windows/runtime**. Todas as camadas devem ser relatadas separadamente. CI verde não prova arranque real, persistência após reinício, processamento de missões, independência do cockpit nem funcionamento do EXE.

## Estado inicial

- CodeRabbit foi instalado/ativado pelo proprietário no GitHub e foi usado no PR #88 de DGM-MAT em 2026-10-18.
- O bot publicou um walkthrough/pre-merge checks e uma revisão foi acionada novamente depois de alterações no HEAD. A revisão deve ser confirmada contra o commit atual antes de tratar findings como finais.
- PR #88 permanece aberto e draft enquanto as falhas obrigatórias da fase-gate são investigadas.
