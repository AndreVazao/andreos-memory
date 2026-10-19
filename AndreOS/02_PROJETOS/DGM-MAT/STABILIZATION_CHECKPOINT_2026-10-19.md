# DGM-MAT — checkpoint de estabilização do cérebro

**Data:** 2026-10-19  
**Estado:** CI de backend verde no HEAD do PR #88; revisão CodeRabbit do HEAD atual pendente; validação Windows/E2E ainda não demonstrada.

## Fonte e autoridade

- Repositório canónico do cérebro: [AndreVazao/DGM-MAT](https://github.com/AndreVazao/DGM-MAT), branch `main`.
- O último commit confirmado em `main` durante esta sessão é `cba0e15fc08470d8d66144e59cb87dad0c789ac4`.
- O cérebro permanece soberano; cockpit é observacional. Não expor a API a LAN/Tailscale/público nem assumir execução real a partir de respostas de criação/planeamento.
- Não alterar `DGM-MAT-FULL-MIRROR`; não fazer merge automático nem eliminar satélites.

## Trabalho efetuado nesta sessão

### PR #88 — correções de CI e política de autenticação

PR: https://github.com/AndreVazao/DGM-MAT/pull/88  
HEAD validado: `6519b591976afa8e938153426b5f7e47cdb48d06`  
Backend Phase Gate run #87: https://github.com/AndreVazao/DGM-MAT/actions/runs/39289078894

Alterações adicionadas ao branch do PR:
- `core/api/security_policy.py`: acrescentada classificação explícita de caminhos concretos contra a lista de rotas autorizadas, respeitando método, número de segmentos e parâmetros de rota completos.
- `core/api/auth_middleware.py`: quando a classificação por rota/template falha, tenta a classificação conservadora do caminho concreto; rotas conhecidas continuam protegidas pela scope declarada.
- `tests/security/test_api_security_policy.py`: teste para caminhos concretos de aprovação/rejeição da fila, ambos operator-only.
- `tests/test_command_executor.py`: corrigida a string do teste para enviar um NUL real, em vez dos caracteres literais `\\x00`.

### Evidência de CI

No HEAD acima, o Backend Phase Gate run #87 terminou com sucesso:
- Mission API, queue and recovery: PASS
- Understanding, help-seeking, research and learning: PASS
- Authentication, permissions and governed execution: PASS
- Research, knowledge fabric and consolidation: PASS
- Minimal PC chat cockpit: PASS
- Python source syntax: PASS
- Durable queue decision safety: PASS
- Required phase-gate summary: PASS

O status Snyk consultado para o mesmo HEAD também reportou sucesso.

Isto valida os gates automatizados do workflow nesse commit; **não** demonstra execução no PC Windows, recuperação real após reinício, integração cockpit/runtime live, build/instalação EXE ou independência do cockpit em execução real.

### Revisão e merge

- Foi publicado um comentário a pedir ao CodeRabbit revisão do HEAD exato `6519b591976afa8e938153426b5f7e47cdb48d06`, em especial o fallback de classificação e o teste de NUL.
- Em 2026-10-19 foi feito novo pedido explícito de revisão no PR #88. CodeRabbit respondeu “Review triggered”, mas avisou que a revisão incremental não volta a rever commits já revistos; ainda não apareceu um novo relatório de findings referente ao HEAD `6519b591...`.
- PR #88 permanece aberto e não foi integrado por esta sessão. Não fazer merge apenas porque a CI ficou verde: verificar a revisão do HEAD atual e manter a aprovação humana para alterações de fronteira de segurança.

## Correção adicional identificada em main

Branch de trabalho: `fix/self-repair-readme-detection-2026-10-19`  
Base: `main` em `cba0e15fc08470d8d66144e59cb87dad0c789ac4`

- Commit `33aa9d0572d23c2ad3ad63f855d1f92bf4be7516`: `core/self_healing/self_repair_engine.py` passa a consultar `audit.readme_present`, campo real de `RepositoryAudit`, em vez de procurar um atributo inexistente `missing_readme`.
- Commit `7d84cfa3d35eb4798863965d7a9c537df5bdbe7a`: criado `tests/self_healing/test_self_repair_engine.py`, cobrindo README ausente/presente e confirmando que a reparação proposta exige aprovação.
- A branch foi aberta como PR #89: https://github.com/AndreVazao/DGM-MAT/pull/89. O PR foi marcado pronto para revisão para permitir CI; continua aberto e não foi integrado.
- Backend Phase Gate run #88 está em curso para o HEAD `7d84cfa3d35eb4798863965d7a9c537df5bdbe7a`: https://github.com/AndreVazao/DGM-MAT/actions/runs/39291621198. A sintaxe Python passou; os outros jobs estavam em curso na última consulta.
- Foi pedido CodeRabbit review no PR #89 para verificar o contrato `readme_present` e confirmar que os testes não habilitam mutação insegura. Ainda não havia revisão publicada na última consulta.
- Os testes não foram executados localmente porque o ambiente não conseguiu resolver `github.com` durante clone. Não declarar os testes como aprovados até o resultado do CI.

## Próximas ações ordenadas

1. Consultar o resultado completo do Backend Phase Gate run #88 do PR #89 e reparar qualquer falha identificada.
2. Obter e verificar a revisão CodeRabbit do PR #89; corrigir apenas findings válidos e voltar a validar.
3. Obter uma revisão CodeRabbit útil do HEAD atual do PR #88; o pedido foi registado, mas a resposta atual apenas diz “Review triggered”.
4. Não fazer merge sem revisão atualizada e decisão explícita; após eventual integração, confirmar o SHA final de `main`.
5. Rebase/recriar a correção de self-repair sobre a base consolidada se PR #88 for integrado primeiro.
6. Continuar a fechar a prova end-to-end: pedido autenticado → missão durável → decisão governada → executor real → resultado verdadeiro → persistência → recuperação após reinício → cockpit a refletir o estado real.
7. Quando o PC estiver acessível, executar e registar os testes Windows/runtime e build; não substituir essa evidência por CI Linux.

## Limitações desta sessão

- Nenhuma validação foi executada no PC Windows local.
- Não foi possível clonar o repositório para executar pytest localmente por falha DNS no ambiente de trabalho desta sessão.
- Nenhum merge foi efetuado.


## Atualização de progresso — 2026-10-19 17:12 UTC

Esta secção prevalece sobre os estados de CI ainda “em curso” descritos acima.

### PR #88 — validação reforçada

- Novo HEAD: `648f148eea71f0db7f00eeedfdc26a5e39e8a246`.
- Backend Phase Gate run #88: https://github.com/AndreVazao/DGM-MAT/actions/runs/39291853775 — **PASS**, os oito jobs concluíram com sucesso.
- Foi acrescentado `tests/security/test_api_security_policy_fallback.py` para verificar que a classificação por caminho concreto rejeita método errado, segmento literal não correspondente, segmento vazio e segmentos extra, mantendo `SecurityScope.OPERATOR` para a rota válida de aprovação.
- Foi novamente solicitado CodeRabbit review ao commit novo. Até à última consulta, o bot só tinha respondido a um pedido anterior com “Review triggered”; não foi publicado um novo relatório de revisão do HEAD atual. A fronteira de segurança continua pendente de revisão humana/CodeRabbit.

### PR #89 — auto-reparação

- HEAD atual: `e8a607a9c90696131890ef6f2f9e52ccaabe90e0`.
- PR: https://github.com/AndreVazao/DGM-MAT/pull/89 — aberto, não integrado, base `main`.
- Além dos testes para README presente/ausente, foi adicionado `tests/self_healing/test_self_repair_approval_gate.py`, que garante que `apply_safe(dry_run=False)` não executa ações com `allowed_automatically=False`.
- O Backend Phase Gate run #88 para o HEAD anterior `7d84cfa3...` falhou em dois jobs durante import/collection porque `main` ainda não contém `core.governance.runtime_capability_profile`, que pertence ao PR #88. Os outros seis jobs passaram, incluindo a compilação Python. Isto não é um teste verde da correção de self-repair.
- Após acrescentar o teste de aprovação, não há ainda um run de CI confirmado para o HEAD `e8a607a9...`. A validação local continua indisponível por falha DNS no clone.
- Foi solicitado CodeRabbit review para o novo teste de aprovação; ainda sem relatório publicado.

### Próximas ações atualizadas

1. Aguardar e inspecionar revisão CodeRabbit do HEAD `648f148...` no PR #88; manter o PR sem merge até a revisão e a decisão humana.
2. Após eventual integração do PR #88, executar o Backend Phase Gate no HEAD atual do PR #89 contra `main` consolidada e corrigir falhas reais.
3. Rever o feedback CodeRabbit do PR #89 e só depois considerar merge.
4. Continuar a validação E2E e Windows; CI verde não substitui esses testes.
