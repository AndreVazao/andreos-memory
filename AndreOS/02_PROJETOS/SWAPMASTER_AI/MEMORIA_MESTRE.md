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


## Checkpoint 2026-11-15 — persistência SQLite

Commit em develop: `76010303e74b099cf3fc69e0ec698a10ecc86dee`

Implementado:
- `infrastructure/persistence/sqlite.py`: adaptador SQLite sem dependências externas.
- Migração v1 com `PRAGMA user_version`, tabela `schema_migrations`, tabela `measurement_revisions` e índice por field_path.
- Repositório append-only: gravação em transação `BEGIN IMMEDIATE`; rejeita sobrescrita, saltos de revisão, mudança silenciosa de unidade e timestamps fora de ordem.
- Restrições SQL para unidades suportadas, evidência UNKNOWN e dados CONFIRMED com fonte/método.
- Leitura de histórico completo, última revisão e lista determinística de campos.
- Testes de migração idempotente, round-trip, histórico, conflitos, desconhecidos e constraints SQL.
- Atualizados Architecture e Roadmap.

Limites:
- SQLite local de processo único; não existe sincronização multiutilizador.
- Não existe ainda interface de backup/restauro, encriptação em repouso, import/export validado, camada de serviços de aplicação ou audit trail completo.
- O adaptador expõe a ligação SQLite a repositórios no processo; a UI ainda não está ligada à persistência.

CI inicial do commit `76010303e74b099cf3fc69e0ec698a10ecc86dee`: os 41 testes passaram com 95% de cobertura, mas Ruff detetou uso de `timezone.utc` em vez de `datetime.UTC`. Corrigido nos commits `60177486b4b5702e88c81df9a9628d8eeb168527` e `1046e2dc5c9341ef7fa55294942b50b2b11545e7`. CI do commit `1046e2dc5c9341ef7fa55294942b50b2b11545e7` revelou uma referência `timezone.utc` remanescente num teste, que causou NameError após o import ser removido. Corrigida no commit `a86d5e199c0e60e0cfdcb376b88e3c3d7968f9d2`. Run `43749077284` passou nos testes mas falhou no Ruff por ordem dos imports padrão; corrigido no commit `2a802d5cce6877d4e3bd8af1345ef4638dfdd57f`. CI atual: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43749119836 — pendente/em execução na última consulta.


- Correção Ruff no adaptador SQLite e testes: substituir `timezone.utc` por `datetime.UTC` (Python 3.11+). Commits: `60177486b4b5702e88c81df9a9628d8eeb168527`, `1046e2dc5c9341ef7fa55294942b50b2b11545e7`. Run atual: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43749013709.


- Correção adicional do teste SQLite: uma ocorrência residual de `timezone.utc` provocou NameError. Substituída por `UTC` no commit `a86d5e199c0e60e0cfdcb376b88e3c3d7968f9d2`. CI: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43749077284.


- Correção final de ordenação dos imports em `tests/test_sqlite_repository.py`: commit `2a802d5cce6877d4e3bd8af1345ef4638dfdd57f`. CI: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43749119836.


### Resultado final — persistência SQLite — 2026-11-15
- Commit final de CI: `2a802d5cce6877d4e3bd8af1345ef4638dfdd57f`.
- Run: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43749119836 — success.
- Quatro jobs passaram: Windows 3.11, Windows 3.12, Ubuntu 3.11, Ubuntu 3.12.
- Em todos passaram pytest, Ruff e mypy.
- Relatório verificado em Ubuntu/Python 3.12: 41 testes passaram; 95% de cobertura global.
- PR #1 continua em draft, atualizado com o novo incremento. Sem merge automático.



## Checkpoint 2026-11-17 — backup e restauro SQLite

Commit em develop: `755024ef372e9b69897c88b614a4fa9aab5265b9`

Implementado:
- `SQLiteDatabase.backup_to(destination)`: backup consistente através da API online `Connection.backup`, incluindo bases em ficheiro e em memória.
- Validação `PRAGMA integrity_check`, versão `PRAGMA user_version` e sequência da tabela `schema_migrations`.
- Backup escrito num ficheiro temporário no diretório de destino e publicado por `os.replace`, evitando substituir um backup válido com uma operação incompleta.
- `SQLiteDatabase.restore_from(backup_path, destination)`: abre a origem em modo read-only, valida-a, restaura para staging temporário, volta a validar e só depois substitui atomicamente o destino.
- Bloqueio de backup/restauro sobre destinos com sidecars WAL (`-wal` ou `-shm`), que são tratados como sinal de que a base poderá estar em utilização. O chamador tem de fechar todos os utilizadores do destino antes de restaurar.
- Testes para round-trip de histórico com várias revisões, backup de base em memória, destino igual à origem, sidecars WAL, ficheiro corrompido, versão futura e preservação do destino em falhas.
- Architecture e Roadmap atualizados.

Limites:
- Isto não oferece encriptação em repouso, agendamento, retenção, cópia off-site ou objetivos garantidos de recuperação.
- A deteção de sidecars WAL não consegue detetar todos os casos de handles externos quando a base usa outro modo de journal; a aplicação tem de impor exclusão/encerramento de utilizadores durante o restauro.
- Ainda não existe import/export JSON versionado, camada de serviços de aplicação, UI nem sincronização multiutilizador.

CI do commit `755024ef372e9b69897c88b614a4fa9aab5265b9`: run PR https://github.com/AndreVazao/SwapMaster-AI/actions/runs/44032001047 e run push https://github.com/AndreVazao/SwapMaster-AI/actions/runs/44031995337. Ubuntu/Python 3.12 já passou: 47 testes, 94% cobertura global, Ruff e mypy sem erros. Os restantes três jobs estavam em execução na última verificação; não declarar matriz completa até todos terminarem success.

Próximo passo:
1. Fechar validação dos quatro ambientes.
2. Implementar formato JSON versionado para export/import de MeasurementHistory, com parsing estrito, validação de domínio, deteção de duplicados/conflitos e importação all-or-nothing.
3. Atualizar documentação e memória após validação.


Validação final confirmada em 2026-11-17: run PR https://github.com/AndreVazao/SwapMaster-AI/actions/runs/44032001047 terminou success nos quatro jobs (Ubuntu/Windows × Python 3.11/3.12). Em Ubuntu/Python 3.12: 47 testes passaram, 94% de cobertura global, Ruff e mypy passaram. PR #1 permanece draft e sem merge.



## Checkpoint 2026-11-17 — import/export JSON versionado

Commits em develop:
- `7093c7d53e578a936fabaf0eedb3eac4427475d2`
- `56ee93eae458ee747c34c61b63f6e6bc9e9eafc8`
- `114b96b143efc1da5e88c3f1e27d724ef1408667`
- `08c4bab40b953873b7fa6e33864970f7b43420ca`
- `7d1658d9f16dcd77d545238718641cf3679d7071`
- `a38aa0d46b279de4dfd461cd76468ce7b3250aee`
- `f5f3781aadbda0590ed40a0a4cb33b5ca7747cfd`
- `663368bbb59f8eccf19fb6b0bb446393d66342c3`
- `f86194ddbe2f9a4157819986a7006a809ffec7a2`
- `9a2e6aa8bee110631b94dee6bbe154c08577c227`

Implementado:
- Novo módulo `infrastructure/persistence/measurement_json.py`.
- Formato `swapmaster.measurement-histories`, schema_version 1.
- Exportação determinística, ordenada por field_path, preservando revisões, unidades, evidência, fonte, método, notas, incerteza, timestamp, autor e referência.
- Parser estrito: rejeita chaves JSON repetidas, versões desconhecidas, chaves extra/em falta, valores não numéricos/não finitos, booleanos como números, unidades/evidências desconhecidas, timestamps inválidos ou sem timezone, revisões inválidas e field_paths duplicados.
- `SQLiteMeasurementRepository.import_histories`: importação completa numa transação `BEGIN IMMEDIATE`; rejeita campos existentes e duplicados; rollback integral em conflito.
- Exports públicos e testes de round-trip, ordenação, desconhecidos explícitos, corrupção semântica e atomicidade.
- Architecture e Roadmap atualizados.

Validação final do commit `9a2e6aa8bee110631b94dee6bbe154c08577c227`: run PR https://github.com/AndreVazao/SwapMaster-AI/actions/runs/44033275006 terminou success nos quatro jobs (Ubuntu/Windows × Python 3.11/3.12). No relatório Ubuntu/Python 3.11: 60 testes passaram, 92% cobertura global, Ruff e mypy sem erros.
- Houve falhas intermédias no desenvolvimento (tipagem mypy, fixtures JSON e formatação Ruff); corrigidas e cobertas pelo run final verde.
- PR #1 continua aberto em draft; sem merge automático.

Estado atual da persistência:
- SQLite local com migração v1, repositório append-only, backup online e restauro validado/atómico.
- Import/export JSON v1 para históricos de medições.
- Ainda não existe encriptação at-rest, agendamento/retenção de backups, sincronização multiutilizador, audit trail completo ou resolução de conflitos por origem.

Próximo incremento recomendado:
1. Camada de serviços de aplicação para encapsular repositórios, casos de uso, validação e eventos.
2. Serviços de criação/edição versionada de medições e gestão de backup/import/export.
3. Fluxos de criação de veículo e powertrain, com aprovação humana para alterações propostas pela IA.
4. Depois, começar shell desktop Windows com UI a chamar serviços sem expor consola.



## Checkpoint 2026-11-17 — camada de serviços de aplicação

Commit em develop: `7c75a92c49f0367a88cb9eb96cd74e992baa4801`

Implementado:
- Novo pacote `application` com `MeasurementRepository` Protocol, desacoplando os casos de uso do adaptador SQLite.
- `MeasurementService.record`: valida a sequência através do histórico de domínio antes de pedir ao repositório que grave a revisão; exige revisão 1 no primeiro registo.
- `get_history`: consulta validada por field_path.
- `export_json` e `import_json`: delegam no formato versionado v1 e preservam a regra de não sobrescrever; importação vazia é inócua.
- `assess_readiness`: aplica o gate de completude/evidência sem o apresentar como aprovação de fitment ou segurança.
- Testes dedicados para append imutável, rejeição de saltos de revisão, import/export, conflito e readiness.
- Architecture e Roadmap atualizados: a UI deverá falar com serviços de aplicação e não diretamente com SQLite.

Validação final do commit `7c75a92c49f0367a88cb9eb96cd74e992baa4801`: run PR https://github.com/AndreVazao/SwapMaster-AI/actions/runs/44033672734 terminou success nos quatro jobs Windows/Ubuntu × Python 3.11/3.12. Em Ubuntu/Python 3.11: 66 testes passaram, 93% cobertura global, Ruff e mypy sem erros.

Estado atualizado:
- Backup/restauro SQLite local e validado.
- JSON versionado v1 com importação transacional sem sobrescrita.
- Primeira camada de serviços de aplicação pronta para ser consumida pela futura UI.
- Ainda sem shell desktop, catálogo OEM real, scanner 3D, CAD, FEA, encriptação, sync multiutilizador, audit trail completo ou validação/homologação de engenharia.

Próximo incremento:
1. Criar serviços/casos de uso para veículos e powertrains, com IDs e proveniência por campo.
2. Definir repositórios e persistência para catálogo local.
3. Introduzir eventos/audit trail e fluxo explícito de aprovação humana para alterações propostas pela IA.
4. Só depois ligar o shell desktop Windows aos serviços de aplicação.
