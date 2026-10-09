# DGM-MAT — Continuidade oficial, auditoria documental e sincronização

Data: 2026-10-09
Projeto: DGM-MAT — DevOps God Mode Multi-Agent Tool
Repositórios: `AndreVazao/DGM-MAT`, `AndreVazao/andreos-memory`

## Correção de contexto

O recurso referido pelo utilizador é **Claude Code Free**, não “Cloud Free”. A menção antiga foi um erro de nomenclatura. Não integrar automaticamente; manter o custo zero como preferência, mas verificar sempre quota/custo e permissões concretas do caminho de execução.

## Estado inicial observado no PC

- DGM-MAT: `C:\ProgramasGodMode\DGM-MAT`, branch `main`, `HEAD 7bcf816`, igual a `origin/main`; `git status` sem alterações.
- Memória: `C:\AndreOS-Memory`, branch `main`, `HEAD 9de7ded`, igual a `origin/main`; `git status` sem alterações.
- `core/organization/help_seeking.py` e `tests/organization/test_help_seeking.py` presentes.
- Testes específicos de help-seeking: 8 aprovados.
- Testes de help-seeking + MissionEngine: aprovados, exit code 0.
- `python -m compileall -q ...`: exit code 0.
- `git diff --check`: exit code 0.
- Suite completa `python -m pytest -q`: 100% concluída, exit code 0, runtime reportado 68,64 s. Permanecem avisos de depreciação Starlette/httpx e FastAPI startup events.
- `http://127.0.0.1:8181/health`: `{"status":"healthy","service":"dgm-mat"}`.

## Leitura arquitetural e limites

A documentação consultada cobre o modelo operacional, contrato de agentes, arquitetura/build order da organização digital, política de help-seeking, execução governada de providers, auditorias de provider registry, Bug Hunter, backend headless, limites desktop/mobile, segurança da API e registos de memória. A organização/roster e delegação são ainda uma base de encaminhamento determinístico; não significam que todos os especialistas sejam agentes de IA independentes ativos. A integração do MissionEngine guarda `mission.metadata.help_seeking` em caso de falha, mantendo o estado honesto, mas não faz despacho real nem retries automáticos.

## Risco prioritário identificado

`GovernedProviderService` exige aprovação duradoura associada ao fingerprint do pedido quando `approval_task_id` é fornecido, valida mensagens e limita timeout/tamanho/execução a uma chamada. Porém, o código inspecionado não demonstra que todas as chamadas exigem aprovação, nem que o custo/quota/preço é verificado antes de cada invocação. A ausência de `approval_task_id` atualmente não equivale, por si só, a bloqueio; a política de request é invocada com `approval_required=False` nesse caminho. Isto precisa de revisão de arquitetura e testes antes de declarar proteção global contra despesa.

## Segurança

- Backend health saudável apenas em `127.0.0.1:8181`.
- Não abrir API à LAN/Tailscale/Internet até autenticação HTTP/WebSocket, scopes, sessões e migração de clientes estarem aplicados e testados globalmente.
- Não ativar providers nem ler/expor credenciais durante auditorias.
- Nunca modificar `C:\ProgramasGodMode\DGM-MAT-FULL-MIRROR`.

## Backups

Antes de atualizar esta memória foram copiadas para `C:\ProgramasGodMode\DGM-MAT-OS\backups\memory-sync-2026-10-09\`:
- `MEMORIA_MESTRE.md`
- `REGISTO_CHECKPOINTS_2026-10.md`
- `DGM-MAT_OFFICE_AND_CLOUDFREE_CONTEXT_2026-10-09.md`

O comando `Get-FileHash -Algorithm SHA256` mostrou hashes correspondentes entre cada original e a cópia. As versões originais estão preservadas.

## Próximos passos

1. Rever o conjunto documental completo antes de mudanças de arquitetura, com foco nos contratos e call-sites de provider execution e na segurança API.
2. Criar uma fronteira financeira fail-closed: custo desconhecido, quota gratuita não comprovada, autorização ausente/inválida, armazenamento indisponível ou limite excedido devem negar a chamada antes de chegar ao adapter.
3. Adicionar testes de integração com contador de chamadas para provar que nenhuma execução externa ocorre em caminhos negados.
4. Verificar compatibilidade, suite completa e health; atualizar documentação/memória e sincronizar ambos os repositórios só após validação.
5. Manter o cockpit PC/móvel sem redesenho enquanto o backend e a segurança não estiverem estabilizados.

## Estado de publicação

Este registo documenta a retoma e não afirma por si só que a memória foi publicada. O commit/push deve ser confirmado separadamente após edição, testes de integridade e comparação com `origin/main`.


## 2026-10-09 — Zero-cost provider execution gate

Binding user requirement: **local first; then legitimate browser-based AI free tiers; never spend money or credits; when free limits are reached, wait or use another verified free route. No paid fallback or upgrade without an explicit new policy change.**

Implemented in DGM-MAT:
- Provider execution rejects any external provider unless cost profile is explicitly 'free', billing mode is 'free_tier', cost verification is exactly true, quota usage/limit are known and remaining, and the adapter implements 'reserve_free_quota()' returning exactly true.
- Unknown pricing/quota, paid API mode, exhausted quota, missing reservation, and reservation errors fail closed before provider invocation.
- Base provider cost defaults to 'unknown'.
- ProviderCostOptimizer now chooses 'local-first', a verified free provider with remaining quota, or 'wait-for-free-capacity'; it no longer recommends Claude Sonnet as a paid fallback.
- Focused tests passed for governed provider service, provider request policy, and cost optimizer (results recorded in the 2026-10-09 session).

Important reality check:
- MobileConversationService tries local Ollama first (subject to memory checks) and otherwise returns deterministic fallback text; it does not yet use browser AI sessions.
- AIClient2API and gpt4free adapters are empty skeletons.
- No production external provider adapter with verified free-tier quota reservation exists. The new policy blocks such calls until a real adapter implements the contract. Do not claim browser multi-provider fallback is finished.
- Remote API authentication/session enforcement remains a separate blocker; do not expose the backend remotely.

Policy document: C:\ProgramasGodMode\DGM-MAT\docs\security\ZERO_COST_PROVIDER_POLICY_2026-10-09.md.
Backup: C:\ProgramasGodMode\DGM-MAT-OS\backups\zero-cost-provider-gate-2026-10-09; original files were SHA-256 verified before editing. Never touch C:\ProgramasGodMode\DGM-MAT-FULL-MIRROR.
