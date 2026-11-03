# DGM-MAT — PC cockpit realtime bootstrap checkpoint
Data: 2026-10-10

## Implementado
- Corrigido `cockpit/main_window.py`: o cliente WebSocket agora arranca num thread dedicado com `asyncio.run()`; o bootstrap anterior tentava obter um loop asyncio na thread Qt e ficava silenciosamente sem iniciar quando não existia loop ativo.
- Mensagens e estados de conexão atravessam `Signal`/`Slot` para atualizar widgets na thread GUI; a hidratação HTTP inicial também emite sinal, evitando chamadas diretas a widgets desde thread de trabalho.
- Fechar a janela pede paragem/fecho do WebSocket sem parar o Core; flag de stop evita corrida em que a janela fecha antes do cliente começar.
- Testes em `tests/cockpit/test_realtime_integration.py` cobrem passagem de estado por sinal e stop antes de conectar.
- Testes cockpit: 7 aprovados; compileall e `git diff --check` passaram.
- Verificação live contra o Core já em execução: `/health` HTTP 200, `/runtime/truth` HTTP 200 e handshake WebSocket `ws://127.0.0.1:8181/ws` OK. Ainda falta verificar a janela Qt real a receber evento de estado end-to-end.

## Limites e segurança
- Isto valida os testes do cliente Qt, não é ainda uma verificação E2E contra um runtime ativo.
- API mantém host default `127.0.0.1`. Não expor em LAN/Tailscale: há rotas legadas sem autenticação global e CORS permissivo. Nenhum endpoint móvel/intervenção remota foi adicionado.
- Não expor decisões de intervenção até autenticação HTTP/WebSocket global, identidade do operador/dispositivo, scopes, revogação, anti-replay e auditoria.

## Próximos passos
1. Verificar conexão real com API local sem reiniciar nem parar o Core.
2. Criar vista de intervenções humanas com contrato local autenticado e sem segredos.
3. Remover pedidos HTTP síncronos da thread Qt.
4. Só depois de cockpit PC + auth estáveis: pairing multi-device/Tailscale e APK Android.
