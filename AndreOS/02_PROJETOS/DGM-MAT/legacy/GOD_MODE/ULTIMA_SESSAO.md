# Última Sessão - God Mode

## Data
2026-05-07

## Resumo

A Phase 212 foi implementada, validada e merged. Esta fase adiciona **Guided Provider Setup Wizard + Browser Assist Contract + Hard Stop Resume Flow** ao core do God Mode.

O God Mode está pronto para primeiro uso real no PC/telemóvel e também tem agora um assistente de configuração de providers externos para acesso remoto. O assistente pode abrir a página oficial do provider, mostrar um popup limpo com só os campos necessários, guardar campos sensíveis no Vault local, criar contrato de browser assist, pedir gate no telemóvel, preencher/avançar localmente, mostrar página original em hard stops e retomar quando o Oner clicar “Já resolvi / continuar”.

## Regra central

- O PC de casa é o cérebro/runtime pesado.
- O telemóvel é cockpit/popup/voz.
- O God Mode pode preparar trabalho, criar packets, pedir permissões, consultar/reutilizar Vault references e importar respostas.
- O God Mode autónomo/runtime não pode fazer merge/release/deploy/update final sozinho sem aprovação explícita do Oner.
- Durante sessão assistida, com checks verdes e ordem do Oner, o assistente pode fazer merge para acelerar.
- Dados sensíveis não vão para repo nem memória normal; entram no Vault local/encriptado do PC e o resto do sistema usa `vault_reference`.
- Suporte temporário é read-only por defeito; qualquer ação assistida exige Mobile Permission Relay.
- Browser Assist é local, gated e auditável: mostra popup limpo, guarda campos sensíveis no Vault, preenche página oficial depois do gate e pausa em hard stops.

## Phase 212 — Guided Provider Setup Wizard + Browser Assist Contract

### Implementado

- Serviço: `backend/app/services/guided_provider_setup_wizard_service.py`
- Rota API: `backend/app/routes/guided_provider_setup_wizard.py`
- Página: `backend/app/routes/guided_provider_setup_wizard_frontend.py`
- Docs: `docs/orchestration/guided-provider-setup-wizard.md`
- Smoke workflow atual: `.github/workflows/phase212-guided-provider-setup-wizard-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase211-support-session-connector-smoke.yml`

### Endpoints

- `/api/guided-provider-setup/status`
- `/api/guided-provider-setup/providers`
- `/api/guided-provider-setup/start`
- `/api/guided-provider-setup/browser-assist-contract`
- `/api/guided-provider-setup/resume-after-human-step`
- `/api/guided-provider-setup/capture-result`
- `/api/guided-provider-setup/dashboard`
- `/api/guided-provider-setup/package`

### Rotas visuais

- `/app/guided-provider-setup`
- `/app/setup-remote-access`

### Funcionalidade

- Suporta Tailscale, Cloudflare Tunnel, Ngrok e Manual HTTPS.
- Abre/guia página oficial do provider.
- Mostra popup limpo com campos necessários.
- Guarda campos sensíveis no Vault local.
- Cria Browser Assist Contract.
- Pede aprovação no Mobile Permission Relay antes de preencher/avançar.
- Preenche/avança localmente dentro do fluxo do provider após gate.
- Em hard stop, mostra página original.
- Depois do Oner resolver, usa “Já resolvi / continuar”.
- Regista resume event.
- Pede novo gate para continuar.
- Captura endpoint final: IP Tailscale/MagicDNS/URL HTTPS.
- Cria remote profile para o APK/PC.

### Hard stops

- MFA;
- captcha;
- device approval;
- billing/plano pago;
- provider terms/consentimento;
- página inesperada;
- security warning.

### PR e validação

- PR #355 merged.
- Merge commit: `ead0008c14f06ca4d66990560d7d098bb7dafac3`.
- Validações verdes antes do merge:
  - Phase 212 Guided Provider Setup Wizard Smoke;
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
- `/app/guided-provider-setup` para setup de Tailscale/Cloudflare/Ngrok/HTTPS;
- `/app/setup-remote-access` como alias do setup remoto;
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
- Guided Provider Setup Wizard;
- Browser Assist Contract;
- Hard Stop Resume Flow;
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
8. Se necessário, abrir `/app/setup-remote-access` para configurar Tailscale/Cloudflare/Ngrok.
9. Se necessário, abrir `/app/god-mode-vault` e colar `.env`, URLs e material aprovado.
10. Carregar `Start Now`.

### Telemóvel/APK

1. Abrir GitHub Actions → Android APK Build → última run verde.
2. Fazer download de `godmode-android-webview-apk`.
3. Instalar APK.
4. Dentro de casa, tentar `http://192.168.1.81:8000/app/mobile-permission-relay`.
5. Se falhar, usar sweep `192.168.1.61-101` conforme manifest.
6. Para rua, usar endpoint criado por Tailscale/Cloudflare/Ngrok/URL HTTPS remoto.
7. Usar `/app/mobile-permission-relay` para aprovações e `/app/driver-voice-permissions` para voz.

### Suporte temporário

1. Abrir `/app/support-session`.
2. Criar sessão temporária.
3. Copiar diagnóstico redigido ou partilhar resultado.
4. Qualquer ação assistida passa por aprovação no telemóvel.
5. Revogar sessão quando terminar.

## Veredicto

Com a Phase 212 merged e builds verdes, o God Mode está pronto para primeiro uso real no PC/telemóvel.

Ele já consegue “auto-arranjar-se” de forma controlada:

- diagnostica o próprio estado;
- cria filas de correção;
- cria work packets para IAs;
- usa provider bridge;
- usa Vault local;
- pede permissões no telemóvel;
- gera suporte temporário e diagnóstico redigido;
- permite browser assist para setup de providers;
- pode preparar PRs/planos/correções;
- valida com GitHub Actions.

Limite atual: não deve aplicar patches locais, executar comandos perigosos, fazer merge/release/deploy ou mexer em segredos sem gate explícito. O primeiro teste real deve decidir a próxima fase: bugfix pack ou executor local mais forte.

## Próxima ação recomendada futura

Depois do primeiro teste real: **Real First Run Bugfix Pack**, apenas se aparecerem falhas reais no PC/APK.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar módulos existentes antes de criar módulo novo, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
