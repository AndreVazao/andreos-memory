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
- A revisão CodeRabbit disponível antes desse comentário era anterior a este HEAD; aguardar a revisão mais recente e inspecionar os findings.
- PR #88 permanece aberto e não foi integrado por esta sessão. Não fazer merge apenas porque a CI ficou verde: verificar a revisão do HEAD atual e manter a aprovação humana para alterações de fronteira de segurança.

## Correção adicional identificada em main

Branch de trabalho: `fix/self-repair-readme-detection-2026-10-19`  
Base: `main` em `cba0e15fc08470d8d66144e59cb87dad0c789ac4`  
Estado: 2 commits à frente, sem PR criado.

- Commit `33aa9d0572d23c2ad3ad63f855d1f92bf4be7516`: `core/self_healing/self_repair_engine.py` passa a consultar `audit.readme_present`, campo real de `RepositoryAudit`, em vez de procurar um atributo inexistente `missing_readme`.
- Commit `7d84cfa3d35eb4798863965d7a9c537df5bdbe7a`: criado `tests/self_healing/test_self_repair_engine.py`, cobrindo README ausente/presente e confirmando que a reparação proposta exige aprovação.
- Estes testes ainda **não foram executados**. A tentativa de clonar o repositório público no ambiente de validação falhou por indisponibilidade de resolução DNS para `github.com`. Não declarar o teste como aprovado.
- Não abrir ainda um PR isolado contra a base antiga enquanto PR #88 não for resolvido: a CI da base `main` ainda não inclui as correções de autenticação/path que passaram no PR #88.

## Próximas ações ordenadas

1. Obter e verificar a revisão CodeRabbit referente ao HEAD atual do PR #88; inspecionar todos os findings.
2. Não fazer merge sem revisão atualizada e decisão explícita; após eventual integração, confirmar o SHA final de `main`.
3. Rebase/recriar a pequena correção de self-repair sobre a base consolidada e executar o teste dedicado, sem misturar responsabilidades.
4. Continuar a fechar a prova end-to-end: pedido autenticado → missão durável → decisão governada → executor real → resultado verdadeiro → persistência → recuperação após reinício → cockpit a refletir o estado real.
5. Quando o PC estiver acessível, executar e registar os testes Windows/runtime e build; não substituir essa evidência por CI Linux.

## Limitações desta sessão

- Nenhuma validação foi executada no PC Windows local.
- Não foi possível clonar o repositório para executar pytest localmente por falha DNS no ambiente de trabalho desta sessão.
- Nenhum merge foi efetuado.
