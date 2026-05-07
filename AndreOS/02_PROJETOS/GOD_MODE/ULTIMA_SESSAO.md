# Última Sessão - God Mode

## Data
2026-05-07

## Resumo

A Phase 210 foi implementada, validada e merged. Esta fase adiciona **Final Install & Use Pack + APK Auto Endpoint Contract** ao core do God Mode.

O God Mode fica no estado mínimo prático para primeiro uso real: instalar Windows EXE, instalar APK, ligar telemóvel ao PC por LAN sweep ou remoto, abrir cockpit final, confirmar readiness e iniciar Autopilot.

## Regra central

- O PC de casa é o cérebro/runtime pesado.
- O telemóvel é cockpit/popup/voz.
- O God Mode pode preparar trabalho, criar packets, pedir permissões, consultar/reutilizar Vault references e importar respostas.
- O God Mode autónomo/runtime não pode fazer merge/release/deploy/update final sozinho sem aprovação explícita do Oner.
- Durante sessão assistida, com checks verdes e ordem do Oner, o assistente pode fazer merge para acelerar.
- Dados sensíveis não vão para repo nem memória normal; entram no Vault local/encriptado do PC e o resto do sistema usa `vault_reference`.

## Phase 210 — Final Install & Use Pack + APK Auto Endpoint Contract

### Implementado

- Serviço: `backend/app/services/final_install_use_pack_service.py`
- Rota API: `backend/app/routes/final_install_use_pack.py`
- Página: `backend/app/routes/final_install_use_pack_frontend.py`
- Docs: `docs/orchestration/final-install-use-pack.md`
- Smoke workflow atual: `.github/workflows/phase210-final-install-use-pack-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase209-connection-discovery-smoke.yml`

### Endpoints

- `/api/final-install-use/status`
- `/api/final-install-use/readiness`
- `/api/final-install-use/apk-endpoint-contract`
- `/api/final-install-use/install-steps`
- `/api/final-install-use/start-now`
- `/api/final-install-use/package`

### Rotas visuais

- `/app/install-use-now`
- `/app/final-ready`

### Funcionalidade

- Agrega readiness final de global state, artifacts, today-ready, mobile/PC pairing e IA bridge.
- Dá passos finais para PC e telemóvel.
- Expõe contrato final do APK:
  - tentar `last_working_endpoint`;
  - usar `connection_manifest`;
  - tentar LAN sweep `192.168.1.61-101` com prioridade em `192.168.1.81`;
  - tentar endpoint remoto se LAN falhar;
  - guardar primeiro endpoint funcional;
  - abrir `/app/mobile-permission-relay` por defeito.
- Dá endpoint `Start Now` para iniciar o primeiro Autopilot quando readiness está OK.

### PR e validação

- PR #353 merged.
- Merge commit: `9b5e6a53e0ae3e2798dc7821e01132e45d3036ba`.
- Validações verdes antes do merge:
  - Phase 210 Final Install Use Pack Smoke;
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
- `/app/first-pc-autopilot-ready` como página única de arranque;
- `/app/mobile-pc-pairing` para ligar APK ao PC em casa/rua;
- LAN sweep robusto `192.168.1.61-101`;
- `/app/first-pc-install-ready-pack` para instalação PC;
- `/app/god-mode-self-diagnosis` para self-diagnosis;
- `/app/autonomous-ia-work-session` para sessões IA/work packets;
- `/app/mobile-permission-relay` para popups/permissões/sync/voz;
- `/app/god-mode-vault` para vault/intake de segredos;
- `/app/ia-operator-bridge` para primeiro loop autónomo;
- contrato local para `GodModeDesktop.exe`;
- readiness pack de primeira instalação PC;
- Autonomous IA Work Session Operator;
- IA Operator Permission/Vault Bridge;
- First PC Autopilot Ready Flow;
- Mobile APK to PC Pairing;
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

## Estado final

Com a Phase 210 merged e builds verdes, o God Mode está pronto para primeiro uso real no PC/telemóvel.

## Próxima ação recomendada futura

Depois do primeiro teste real: **Phase 211 — Real First Run Bugfix Pack**, apenas se aparecerem falhas reais no PC/APK.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar módulos existentes antes de criar módulo novo, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
