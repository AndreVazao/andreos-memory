# Última Sessão - God Mode

## Data
2026-05-07

## Resumo

A Phase 211 foi implementada, validada e merged. Esta fase adiciona **Temporary Assisted Support Session Connector** ao core do God Mode.

O God Mode fica pronto para primeiro uso real e também passa a ter uma sessão temporária de suporte/teste para debug assistido: diagnóstico redigido, sessão com TTL, ações propostas e aprovadas no telemóvel, audit log local e revogação manual.

## Regra central

- O PC de casa é o cérebro/runtime pesado.
- O telemóvel é cockpit/popup/voz.
- O God Mode pode preparar trabalho, criar packets, pedir permissões, consultar/reutilizar Vault references e importar respostas.
- O God Mode autónomo/runtime não pode fazer merge/release/deploy/update final sozinho sem aprovação explícita do Oner.
- Durante sessão assistida, com checks verdes e ordem do Oner, o assistente pode fazer merge para acelerar.
- Dados sensíveis não vão para repo nem memória normal; entram no Vault local/encriptado do PC e o resto do sistema usa `vault_reference`.
- Suporte temporário é read-only por defeito; qualquer ação assistida exige Mobile Permission Relay.

## Phase 211 — Temporary Assisted Support Session Connector

### Implementado

- Serviço: `backend/app/services/support_session_connector_service.py`
- Rota API: `backend/app/routes/support_session_connector.py`
- Página: `backend/app/routes/support_session_connector_frontend.py`
- Docs: `docs/orchestration/support-session-connector.md`
- Smoke workflow atual: `.github/workflows/phase211-support-session-connector-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase210-final-install-use-pack-smoke.yml`

### Endpoints

- `/api/support-session/status`
- `/api/support-session/policy`
- `/api/support-session/create`
- `/api/support-session/diagnostics`
- `/api/support-session/propose-action`
- `/api/support-session/record-action-result`
- `/api/support-session/revoke`
- `/api/support-session/dashboard`
- `/api/support-session/package`

### Rotas visuais

- `/app/support-session`
- `/app/temporary-support`

### Funcionalidade

- Cria sessão temporária com TTL.
- Gera `support_session_id` e `one_time_approval_code`.
- Gera diagnóstico redigido.
- Não expõe segredos raw, env raw nem Vault raw values.
- Resume ambiente sem valores sensíveis.
- Agrega global state, final install use, pairing, artifacts e support status.
- Permite propor ações assistidas.
- Cada ação segura cria pedido no Mobile Permission Relay.
- Ações bloqueadas ficam `blocked_requires_explicit_design`.
- Regista audit log local.
- Permite revogar sessão manualmente.

### Ações seguras iniciais

- `read_diagnostics`
- `export_redacted_bundle`
- `create_github_issue_plan`
- `prepare_pr_plan`
- `request_screenshot`
- `run_safe_check_request`

### Ações bloqueadas por defeito

- `write_file`
- `apply_patch`
- `run_command`
- `change_vault`
- `deploy`
- `release`
- `merge`
- `browser_automation`
- `read_raw_secret`

### PR e validação

- PR #354 merged.
- Merge commit: `5667f003c1b84fa4c929d9bb117dea5854b10d40`.
- Validações verdes antes do merge:
  - Phase 211 Support Session Connector Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend.

## Estado atual do God Mode

O God Mode tem agora:

- PC de casa como cérebro principal;
- telemóvel como cockpit/popup/voz;
- `/app/home` como cockpit visual canónico;
- `/app/install-use-now` como página final de instalação/uso;
- `/app/final-ready` como alias final;
- `/app/support-session` para suporte/teste temporário assistido;
- `/app/temporary-support` como alias de suporte;
- `/app/mobile-pc-pairing` para ligar APK ao PC em casa/rua;
- LAN sweep robusto `192.168.1.61-101`;
- `/app/mobile-permission-relay` para popups/permissões/sync/voz;
- `/app/god-mode-vault` para vault/intake de segredos;
- `/app/ia-operator-bridge` para primeiro loop autónomo;
- `GodModeDesktop.exe` como runtime PC;
- APK Android WebView;
- Final Install & Use Pack;
- Support Session Connector;
- Mobile Permission Relay;
- Driver Voice Mode;
- Offline Resend Queue;
- Local encrypted Vault;
- Secret Intake Classifier.

## Caminho de uso imediato

### PC

1. Abrir GitHub Actions → Windows EXE Build → última run verde.
2. Fazer download de `godmode-windows-exe`.
3. Extrair ZIP.
4. Abrir `GodModeDesktop.exe`.
5. Abrir `http://127.0.0.1:8000/app/install-use-now`.
6. Confirmar readiness.
7. Abrir `/app/connect-phone` para ligar o telemóvel.
8. Se necessário, abrir `/app/god-mode-vault` e colar `.env`, URLs e material aprovado.
9. Carregar `Start Now`.

### Telemóvel/APK

1. Abrir GitHub Actions → Android APK Build → última run verde.
2. Fazer download de `godmode-android-webview-apk`.
3. Instalar APK.
4. Dentro de casa, tentar `http://192.168.1.81:8000/app/mobile-permission-relay`.
5. Se falhar, usar sweep `192.168.1.61-101` conforme manifest.
6. Para rua, configurar Tailscale/Cloudflare/Ngrok/URL HTTPS remoto.
7. Usar `/app/mobile-permission-relay` para aprovações e `/app/driver-voice-permissions` para voz.

### Suporte temporário

1. Abrir `/app/support-session`.
2. Criar sessão temporária.
3. Copiar diagnóstico redigido ou partilhar resultado.
4. Qualquer ação assistida passa por aprovação no telemóvel.
5. Revogar sessão quando terminar.

## Estado final

Com a Phase 211 merged e builds verdes, o God Mode está pronto para primeiro uso real no PC/telemóvel e tem conector de suporte temporário seguro para debug pós-instalação.

## Próxima ação recomendada futura

Depois do primeiro teste real: **Real First Run Bugfix Pack**, apenas se aparecerem falhas reais no PC/APK.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar módulos existentes antes de criar módulo novo, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
