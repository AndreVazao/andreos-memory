# SwapMaster AI — memória mestre

**Última atualização:** 2026-11-13  
**Repositório de produto:** https://github.com/AndreVazao/SwapMaster-AI  
**Repositório:** público durante desenvolvimento, por decisão explícita do André. Reavaliar passagem a privado apenas quando o produto estiver pronto e após revisão de dados, segredos, dependências e histórico Git.  
**Memória persistente:** este documento vive no AndreOS Memory; o código e documentação técnica do produto vivem no repositório SwapMaster-AI.

## Objetivo

Aplicação desktop Windows, modular e extensível, para apoiar o planeamento de swaps de motores de combustão, elétricos e híbridos e conversões EV. Deve cruzar dimensões, interfaces, pontos de fixação, transmissão, requisitos auxiliares e dados com proveniência; apoiar medições e importação de digitalizações 3D; e produzir documentação e CAD preliminar com revisão humana.

Idioma inicial: Português (Portugal), com arquitetura preparada para localização.

## Regras de engenharia e segurança

- Nunca declarar compatibilidade física apenas por dimensões externas.
- Distinguir sempre dados confirmados, documentados, estimados e desconhecidos.
- Preservar fonte, método de medição, unidades, incerteza e revisão de cada dado.
- Bloquear conclusões positivas quando faltam dados críticos.
- Apoios, adaptadores, caixas de bateria e interfaces estruturais são safety-critical.
- CAD futuro deve estar marcado **PRELIMINAR — NÃO FABRICAR — REQUER VALIDAÇÃO DE ENGENHARIA** até existir revisão técnica independente.
- IA pode propor alterações, mas não pode aplicá-las sem diff legível e aprovação explícita do André.
- Não prometer homologação, segurança estrutural ou prontidão de fabrico sem evidência e validação profissional.

## Estado real verificado

### GitHub
- Repositório AndreVazao/SwapMaster-AI confirmado.
- Visibilidade observada: public, autorizada explicitamente pelo André em 2026-11-13 para facilitar Actions durante desenvolvimento.
- Branch main: README inicial.
- Branch develop: implementação de fundação.
- PR draft #1: https://github.com/AndreVazao/SwapMaster-AI/pull/1

### Implementado em develop (primeiro incremento)
- Projeto Python configurado em pyproject.toml (Python 3.11+).
- Modelo de proveniência Evidence com níveis confirmed/documented/estimated/unknown.
- Modelo Envelope3D com validação de dimensões e comparação com folga.
- Avaliação conservadora de envelope, sem confundir bounding-box pass com fitment real.
- Testes pytest para proveniência, dimensões e resultados preliminares.
- Workflow GitHub Actions .github/workflows/ci.yml: matriz Windows/Ubuntu e Python 3.11/3.12, com pytest, Ruff e mypy.
- Documentação: arquitetura, segurança de engenharia, roadmap e contribuição.

### CI
- Workflow foi acionado nos pushes para develop.
- Como cada ficheiro foi commitado separadamente, vários runs intermédios foram cancelados pela política concurrency (cancel-in-progress).
- O run final do incremento inicial: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43429400303 — concluído com success. Matriz Windows/Ubuntu e Python 3.11/3.12 aprovada.
- O incremento de catálogo e a correção da configuração Ruff passaram na matriz completa Windows/Ubuntu + Python 3.11/3.12 no run https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43748398224.
- O incremento seguinte de proveniência por campo foi enviado no commit `500094773b54e4c691ec6a0711dc6b3c9e166643`; CI correspondente em execução na última verificação: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43748502483. Não declarar este incremento aprovado até todos os jobs terminarem verdes.

## Próximas prioridades

1. Verificar e corrigir CI até todos os jobs Windows/Linux e Python 3.11/3.12 passarem.
2. Corrigir a cadência de commits (agrupar alterações em commits menores, evitar disparar workflow em cada ficheiro).
3. Expandir domínio: veículo, motor, caixa, interfaces, pontos de montagem, massa, centro de gravidade, requisitos auxiliares e unidades.
4. Base de dados local versionada, importação validada e catálogo com fontes verificáveis.
5. Motor de regras multidimensional com resultados explicáveis e bloqueios por dados em falta.
6. UI desktop e fluxos Simples/Técnico/Oficina.
7. Planeamento de conversão EV e checklist de alta tensão.
8. Importação de malhas 3D, calibração e pontos de referência.
9. CAD paramétrico preliminar e documentação de revisão.
10. ONER com aprovação humana obrigatória.
11. Empacotamento Windows, instalador e testes em máquina limpa.

## Governança Git

- main é a base estável.
- develop recebe desenvolvimento ativo.
- PRs focados, pequenos e revistos.
- Não fazer merge do PR #1 até CI ficar verde e conteúdo ser revisto.
- Não publicar segredos, credenciais, dados pessoais ou dados proprietários no repositório público.
- Reavaliar visibilidade pública/privada antes de qualquer release.

## Nota de continuidade

O projeto está em fundação técnica inicial; não está completo, não tem catálogo real de motores/veículos, UI desktop, scanner 3D funcional, CAD de fabrico, análise FEA, instalador nem validação de engenharia. Comunicar sempre o estado real.


## Checkpoint 2026-11-13 — catálogo de domínio

Commit em develop: `d9805d0fe711722e28c0065c36dd8a463c574638`

Implementado no incremento:
- `domain/catalog.py`: modelos imutáveis para `VehiclePlatform`, `PowerUnit`, `Transmission`, `MountingPoint` e `MechanicalInterface`.
- Tipos de propulsão: combustão, elétrico, híbrido e outros.
- Unidades explícitas: mm, kg, kW e Nm; pontos de montagem exigem referencial de coordenadas.
- Validação de campos essenciais, valores físicos finitos/positivos e unicidade de identificadores.
- Avaliação de interfaces por família e identificador. Mesmo uma correspondência confirmada é apenas preliminar; geometria, tolerâncias, fixadores, cargas e alinhamento continuam por validar.
- Testes em `tests/test_catalog.py`; exports públicos no pacote domain.
- Atualizados Architecture e Roadmap para declarar limites reais e estado.

Limitações conhecidas:
- Proveniência está ao nível do registo, ainda não ao nível de cada campo.
- Ainda não existem transformações de coordenadas, catálogo OEM, importação de dados, validação dimensional de padrões de interface ou análise de cargas.
- Não existe ainda UI, base de dados, CAD ou recomendação real de swaps.

Próximo passo técnico:
1. Verificar CI do commit de catálogo nos quatro ambientes.
2. Adicionar proveniência por campo, incerteza, unidade tipada e revisão/versionamento.
3. Implementar requisitos auxiliares e matriz de verificações, mantendo bloqueio quando dados críticos faltam.


### Atualização de execução — 2026-11-13

- Commit de catálogo: `d9805d0fe711722e28c0065c36dd8a463c574638`.
- Correção de lint em dois commits incrementais; commit mais recente: `354fba61653e40aceb40bb2e0961b324679e38ed`.
- Run intermédio confirmou 20/20 testes; Ruff falhou apenas por ordenação de imports, já corrigida.
- Novo run de validação para o commit final: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43430980821 (queued no último check).
- PR #1 continua aberto e em draft; descrição atualizada para refletir catálogo e limites de segurança. Não fazer merge antes de CI verde e revisão.


## Checkpoint 2026-11-15 — medições com proveniência por campo

### Catálogo de domínio e qualidade
- Commit validado em develop: `62c90e27e05e3b73794059ee07f2c68ba6839264`.
- Corrigida a classificação de imports do Ruff em `pyproject.toml`, com `known-first-party = ["swapmaster"]` e `known-third-party = ["pytest"]`.
- Run CI https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43748398224 terminou success nos quatro jobs: Windows/Python 3.11, Windows/Python 3.12, Ubuntu/Python 3.11 e Ubuntu/Python 3.12. Em todos passaram pytest, Ruff e mypy.

### Novo incremento em develop
Commit enviado: `500094773b54e4c691ec6a0711dc6b3c9e166643`

Implementação:
- `domain/measurement.py`: `EngineeringDatum` com caminho do campo, valor ou desconhecido explícito, unidade, evidência, incerteza absoluta, revisão, timestamp timezone-aware, autor e referência da fonte.
- Unidades explícitas: mm, kg, kW, Nm, V, A, rpm e °C. Não há conversão silenciosa.
- Intervalo de incerteza calculado como valor ± incerteza absoluta.
- `MeasurementHistory`: histórico imutável, revisions sequenciais desde 1, unidade constante e append que devolve novo histórico.
- `assess_required_measurements`: bloqueia se falta qualquer campo obrigatório; exige revisão quando evidência não é confirmada ou incerteza não está declarada; estado READY_FOR_ENGINEERING_REVIEW significa apenas dados prontos para revisão humana, nunca aprovação de fitment/segurança.
- Testes dedicados em `tests/test_measurement.py`; exports no pacote domain; arquitetura e roadmap atualizados.

Limites:
- Não existe ainda persistência real de histórico em base de dados.
- Não existe resolução de conflitos entre fontes, audit trail transacional, importação, UI, catálogo OEM, transformação de coordenadas ou análise estrutural.
- A incerteza é registada como valor absoluto na unidade do campo; a sua qualidade depende da fonte/método e deve ser validada pelo utilizador.

CI inicial do commit `500094773b54e4c691ec6a0711dc6b3c9e166643` falhou por um teste que esperava incorretamente um campo UNKNOWN como existente; a lógica de bloqueio identificou corretamente os dois campos em falta. O teste foi corrigido para usar um campo medido e deixar apenas o segundo ausente. Commit de correção: `92157e61f3df092c095cdc44352426c4c4e44ee7`. Depois da correção do cenário, os testes passaram e Ruff passou, mas mypy detetou inferência demasiado estreita do tipo da variável `reasons`; foi adicionada anotação explícita `tuple[str, ...]`. Commit de tipagem: `43bdec630400df94bda32e4bd098558e8213621b`. CI final do commit `43bdec630400df94bda32e4bd098558e8213621b`: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43748644996 — concluído com success nos quatro jobs Windows/Ubuntu e Python 3.11/3.12; pytest, Ruff e mypy passaram.

Próximo passo: confirmar CI verde; depois desenhar persistência SQLite versionada e camada de repositórios/migrações, com testes de integridade e exportação/importação.


### Nota de validação — 2026-11-15
- O run de medições teve 32 testes passados e 1 falhado. A falha estava no cenário de teste, não na função: o teste marcava o campo length como UNKNOWN e esperava que não fosse reportado como ausente.
- Corrigido o cenário para medir length e deixar width em falta; agora a expectativa corresponde à regra de domínio.
- Commit: `92157e61f3df092c095cdc44352426c4c4e44ee7`.
- CI deste commit ainda em execução: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43748582779.


- Segunda correção de validação: mypy exigiu tipo explícito `tuple[str, ...]` para as razões do gate de medições, porque os ramos devolvem tuplos com comprimentos diferentes. Corrigido no commit `43bdec630400df94bda32e4bd098558e8213621b`; CI: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43748644996.


### Resultado final da validação — 2026-11-15
- Commit validado: `43bdec630400df94bda32e4bd098558e8213621b`.
- Run: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43748644996
- Resultado: success nos quatro jobs da matriz (Windows/Ubuntu × Python 3.11/3.12).
- Em todos os jobs passaram pytest, Ruff e mypy.
- A implementação de medições por campo está validada na matriz; 33 testes no total e 94% de cobertura global, segundo o relatório pytest-cov.
