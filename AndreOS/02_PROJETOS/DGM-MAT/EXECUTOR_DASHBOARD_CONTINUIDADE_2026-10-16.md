# DGM-MAT — Continuidade do executor governado e cockpit
**Checkpoint:** 2026-10-16  
**Estado:** alterações de código/documentação em branches remotas; integração de runtime ainda não validada no PC.

## Fonte de verdade e branches
- DGM-MAT: `AndreVazao/DGM-MAT`, branch `feat/governed-command-executor-v1`, PR #74 (draft, não integrado).
- Cockpit PC: `AndreVazao/DGM-Cockpit-Frontend`, branch `feat/pc-only-chat-cockpit-v1`, PR #1.
- Memória persistente: `AndreVazao/andreos-memory`, branch de documentação `docs/dgm-mat-dashboard-executor-continuity-2026-10-16`.
- Não declarar nenhuma destas alterações instalada/ativa no computador até executar validação no PC real.

## O que existe no backend DGM-MAT
- `core/operations/command_executor.py`: catálogo explícito de diagnósticos read-only; IDs conhecidos: `system.summary`, `process.top`, `engines.inventory`, `git.status`, `ollama.status`, `claude.status`.
- Não aceita texto shell arbitrário; usa `subprocess.run(..., shell=False)`, timeout e limite de saída.
- `core/api/governance_api.py`: `GET /governance/commands/catalog` e `POST /governance/commands/run`.
- `core/api/security_policy.py`: rotas classificadas como operator-only. A sessão autenticada tem de ser autorizada pelo middleware existente.
- `core/operations/operation_audit.py`: eventos JSONL redigidos, com intenção persistida antes da execução; falha de armazenamento bloqueia a execução.
- O inventário devolve nomes/PIDs, não linhas de comando completas, e não prova ownership dos processos.

## Ligação ao cockpit acrescentada
Ficheiros no branch `feat/pc-only-chat-cockpit-v1`:
- `index.html`: botão “Consultar motores” e área de resultados no painel de motores.
- `app.js`: consulta catálogo governado com a sessão atual; verifica explicitamente `mode=read-only-allowlist` e `arbitrary_shell=false`; preenche um seletor com IDs/descrições recebidos; executa apenas o ID selecionado após clique. O campo de pasta só aparece para comandos com `requires_target=true`, e a validação do caminho continua no backend.
- Para `engines.inventory`, mostra nomes/PIDs com `textContent`; não executa inventário a cada polling.
- `styles.css`: estilos do seletor, campo de pasta e saída limitada.

Falhas de sessão, permissões, auditoria ou API devem permanecer visíveis como falhas. O frontend não pode inferir sucesso a partir do clique.

## Limitações e segurança
- O executor é apenas de leitura. Não instalar software, não elevar privilégios, não iniciar/parar processos e não manipular credenciais.
- Não parar/reiniciar Ollama, Claude Code ou processos Node só porque o nome corresponde. Uma futura ação de lifecycle exige registo de ownership criado pelo DGM-MAT, PID + hora de início verificados contra reutilização de PID, timeout, confirmação explícita e verificação do estado final.
- A autenticação web tem de continuar ligada ao middleware local existente; nunca guardar token bootstrap em localStorage nem mostrar segredos.
- O controlo web/browser ainda não está implementado/confirmado; login/MFA/CAPTCHA continuam sob controlo direto do utilizador.

## Validação pendente (obrigatória antes de merge/ativação)
1. Recuperar/atualizar branches no PC sem reset/clean nem descartar alterações locais.
2. Correr os testes focados do DGM-MAT para executor, audit trail, security policy e autenticação; corrigir falhas reais.
3. Validar que a API inclui o router e que as rotas devolvem 401/403 a sessões sem autorização.
4. Testar frontend com backend executado localmente: sem sessão, sessão read-only, sessão operator, catálogo disponível, inventário bem-sucedido, erro de PowerShell e falha de audit storage.
5. Confirmar que a saída é limitada e não contém command lines, tokens ou caminhos privados.
6. Só depois avaliar merge dos PRs; não fazer merge cego nem ativar start/stop.
7. Quando o PC estiver acessível, registar resultados, versões/commits efetivos, testes executados e logs sem segredos nesta memória e no registo de checkpoints.

## Próximo passo de engenharia
Construir um registo de lifecycle apenas para processos que o DGM-MAT tenha criado explicitamente. Antes de qualquer ação start/stop, implementar e testar o modelo de ownership (PID + creation/start time + identificador de instância) sem efetuar ações reais. Depois ligar os estados do ciclo de vida ao cockpit. Manter a implementação read-only até os testes e a política de aprovação estarem demonstrados.


## Follow-up audit — 2026-10-16 (static review)
- Static review found the catalog UI previously accepted an empty/malformed command list as healthy and retained stale command entries after a failed refresh. The cockpit now validates command IDs, READ risk and `requires_target`, and clears/disables execution on catalog failure.
- Backend target path normalization now denies malformed paths predictably; regression test added for an embedded NUL.
- Manual-only test workflows are being added (no push/PR triggers) to avoid unplanned GitHub Actions usage. They still need to be explicitly dispatched and their results recorded.
- Static JavaScript parse and HTML ID consistency checks are possible in this session; backend pytest and browser/E2E tests have not been run here.


## Test workflows and mergeability clarification — 2026-10-16
- Added `DGM-Cockpit-Frontend/.github/workflows/cockpit-contract.yml` and `tests/cockpit-contract.test.cjs`. It is manual-only (`workflow_dispatch`) and checks JS syntax plus static DOM/API/security contracts.
- Added `DGM-MAT/.github/workflows/governed-executor-tests.yml`, also manual-only, to run focused Python executor, audit and API security tests.
- These workflows were added to their respective PR branches but have not been dispatched. The static contract checks were independently evaluated in this session and all 12 checks passed; that is not the same as running Node's test runner or Python pytest.
- GitHub's raw PR API for cockpit #1 reports `mergeable=null` and `mergeable_state=unknown`; a connector snapshot mapped this to `false`. This is **not proof of a merge conflict**. Compare API showed 24 commits ahead, 0 behind at the earlier checkpoint; re-check mergeability once GitHub recalculates.
- No merges, installations, or runtime activation were performed.


## Latest verified checkpoint — 2026-10-16 19:32 UTC

Branches compared with `main`:
- Cockpit PR #1: 28 commits ahead, 0 behind; raw PR API `mergeable_state=clean`; head `695cea4149ad19b15c653a9405ab8bee534822ab`.
- DGM-MAT PR #74: 33 commits ahead, 0 behind; raw PR API `mergeable_state=clean`; head `3394d20d579edcc9d315a6d26b7293a170d4650c`; still draft.
- AndreOS Memory PR #7: 7 commits ahead, 0 behind; raw PR API `mergeable_state=clean`; head `f588712184f4e604f9f7cfa6d7b3559b22ec93dd`; still draft.

Latest static checks evaluated against fetched branch source:
- JavaScript parse: PASS.
- Literal DOM lookup IDs: all found in HTML.
- Catalog mode, no-shell flag and READ-only risk validation: present.
- Stale catalog clearing on failed refresh: present.
- Execution is explicit POST only; no execution route in periodic polling: PASS.
- Node contract tests: 5 tests authored.
- Both workflows are manual-only; neither has been dispatched.
- Invalid path normalization maps to a controlled denial; audit fail-closed regression now asserts the executor cannot run.

Important: these are static checks, not a Node test-runner result, pytest result, browser/E2E result, or PC runtime validation. The available GitHub integration in this session has no workflow-dispatch operation, so the manual workflows could not be started here. Do not claim tests passed until an actual workflow run reports success.


## Test workflow launch path — 2026-10-16 19:34 UTC
The DGM-MAT feature branch now extends the pre-existing `.github/workflows/autonomy-smoke.yml` (which already exists on `main`) with:
- focused executor, operation-audit, and API auth/security pytest suites;
- checkout of public cockpit branch `feat/pc-only-chat-cockpit-v1`;
- `node --check app.js` and `node --test tests/cockpit-contract.test.cjs`.

It remains `workflow_dispatch` only, with no push/PR trigger. It can be launched in GitHub Actions by selecting workflow **Autonomy Validation** and branch `feat/governed-command-executor-v1`. I could not dispatch it from this chat session; no workflow-dispatch action is exposed in the available GitHub integration. Therefore no CI result is claimed.
