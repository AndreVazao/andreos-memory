# Última Sessão - God Mode

## Data
2026-05-07

## Resumo

A Phase 208 foi implementada, validada e merged. Esta fase adiciona **Mobile APK to PC Pairing + Remote Access Contract** ao core do God Mode.

O APK/telemóvel já tem contrato de ligação ao PC:

- dentro de casa tenta primeiro o IP fixo conhecido do PC: `192.168.1.81`;
- depois tenta outros IPs locais detetados;
- fora de casa precisa de canal remoto aprovado: Tailscale, Cloudflare Tunnel, Ngrok ou URL HTTPS manual;
- material remoto fica guardado apenas no Vault local.

## Regra central

- O PC de casa é o cérebro/runtime pesado.
- O telemóvel é cockpit/popup/voz.
- O God Mode pode preparar trabalho, criar packets, pedir permissões, consultar/reutilizar Vault references e importar respostas.
- O God Mode autónomo/runtime não pode fazer merge/release/deploy/update final sozinho sem aprovação explícita do Oner.
- Durante sessão assistida, com checks verdes e ordem do Oner, o assistente pode fazer merge para acelerar.
- Dados sensíveis não vão para repo nem memória normal; entram no Vault local/encriptado do PC e o resto do sistema usa `vault_reference`.

## Phase 208 — Mobile APK to PC Pairing + Remote Access Contract

### Implementado

- Serviço: `backend/app/services/mobile_pc_pairing_remote_access_service.py`
- Rota API: `backend/app/routes/mobile_pc_pairing_remote_access.py`
- Página: `backend/app/routes/mobile_pc_pairing_remote_access_frontend.py`
- Docs: `docs/orchestration/mobile-pc-pairing-remote-access.md`
- Smoke workflow atual: `.github/workflows/phase208-mobile-pc-pairing-remote-access-smoke.yml`
- Atualização: `backend/app/services/god_mode_global_state_service.py`
- Remoção do smoke antigo: `.github/workflows/phase207-first-pc-autopilot-ready-flow-smoke.yml`

### Endpoints

- `/api/mobile-pc-pairing/status`
- `/api/mobile-pc-pairing/create-pairing-session`
- `/api/mobile-pc-pairing/create-remote-access-plan`
- `/api/mobile-pc-pairing/store-remote-material`
- `/api/mobile-pc-pairing/connection-manifest`
- `/api/mobile-pc-pairing/dashboard`
- `/api/mobile-pc-pairing/package`

### Rotas visuais

- `/app/mobile-pc-pairing`
- `/app/connect-phone`

### Funcionalidade

- Cria pairing session entre APK/telemóvel e PC.
- Usa IP prioritário conhecido `192.168.1.81`.
- Gera `home_urls` para LAN.
- Gera `qr_payload` e `pairing_code`.
- Gera `connection_manifest` com ordem de tentativa para o APK.
- Cria planos remotos para Tailscale, Cloudflare Tunnel, Ngrok ou URL HTTPS manual.
- Cria permission request quando o acesso remoto precisa de input do Oner.
- Guarda material remoto no Vault local.

### PR e validação

- PR #351 merged.
- Merge commit: `b0e02c730da2b801aa02993a8a6b8e7f0afa7c36`.
- Validações verdes antes do merge:
  - Phase 208 Mobile PC Pairing Remote Access Smoke;
  - Universal Total Test;
  - Android APK Build;
  - Windows EXE Build com boot smoke desktop backend.

## Recomendação de acesso remoto

Para hoje, a recomendação prática é **Tailscale**:

- requer conta/login;
- instalar Tailscale no PC e no telemóvel;
- aprovar ambos na mesma tailnet;
- não precisa abrir portas no router;
- o APK passa a usar o endereço Tailscale do PC com porta 8000.

Para futuro com domínio/URL estável, usar **Cloudflare Tunnel**:

- requer conta Cloudflare;
- normalmente requer domínio/hostname configurado na Cloudflare;
- não precisa abrir portas no router;
- dá URL HTTPS estável.

Ngrok é útil para teste temporário:

- requer conta/authtoken para uso normal;
- URL pode ser temporária no plano grátis.

## Estado atual do God Mode

O God Mode tem agora:

- PC de casa como cérebro principal;
- telemóvel como cockpit/popup/voz;
- `/app/home` como cockpit visual canónico;
- `/app/first-pc-autopilot-ready` como página única de arranque para hoje;
- `/app/mobile-pc-pairing` para ligar o APK ao PC em casa/rua;
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

1. No PC, abrir `GodModeDesktop.exe`.
2. Confirmar `http://127.0.0.1:8000/app/home`.
3. Abrir `http://127.0.0.1:8000/app/mobile-pc-pairing`.
4. Criar pairing local.
5. No telemóvel/APK, tentar `http://192.168.1.81:8000/app/mobile-permission-relay` dentro de casa.
6. Para rua, instalar/configurar Tailscale no PC e no telemóvel ou criar plano remoto na página `/app/mobile-pc-pairing`.
7. Depois usar `/app/today-ready` e `Start Autopilot`.

## Próxima ação recomendada

Próxima fase recomendada: **Phase 209 — APK Connection Manifest Consumer + Auto Switch Home/Remote**.

Objetivos:

- fazer o APK consumir automaticamente `/api/mobile-pc-pairing/connection-manifest`;
- guardar último endpoint funcional;
- tentar LAN primeiro e remoto depois;
- adicionar ecrã de configuração do endpoint no APK;
- preparar alternância automática casa/rua.

## Regra importante

Antes de continuar o desenvolvimento, consultar sempre a memória AndreOS do projeto GOD_MODE, confirmar o HEAD real de `main`, verificar módulos existentes antes de criar módulo novo, manter esta memória atualizada quando houver fases merged/decisões importantes, e apagar workflows smoke de fases antigas quando uma fase nova avançar.
