# Office Kit Digital — backlog e ordem de execução

## P0 — estabilizar integração visual
- [x] Inspecionar estado da branch/PR e CI antes de alterar.
- [x] Integrar packages/scene-engine no examples/browser-preview.
- [x] Fazer a cena recalcular fit scale no resize/ResizeObserver e no zoom.
- [ ] Confirmar CI após os commits de integração visual.
- [ ] Inspecionar preview no browser e gerar capturas 390x844, 844x390 e desktop.
- [ ] Corrigir sobreposições, corte, enquadramento e escala com base nas capturas reais.
- [ ] Acrescentar testes automatizados para resize, zoom e orientação.
- [ ] Confirmar que toda a cena continua a ser gerada a partir do JSON genérico.

## P1 — renderer e QA visual
- [ ] Escolher e implementar primeira cena determinística pequena inspirada no Diorama após auditoria suficiente.
- [ ] Capturas repetíveis em retrato, paisagem e desktop.
- [ ] Testar consola, sobreposição, corte, deformação, foco/seleção e legibilidade.
- [ ] Registar proveniência/licença de cada asset e código reutilizado.

## P2 — perfis gráficos
- [ ] Ligar os perfis a parâmetros reais do renderer.
- [ ] Criar UI manual Auto/Económico/Equilibrado/Detalhado/Cinemático.
- [ ] Medir frame time e aplicar ajuste adaptativo com histerese.
- [ ] Testar movimento reduzido e limites de personagens.
- [ ] Benchmark em aparelhos reais; não inferir a partir de uma única máquina.

## P3 — core e backend
- [ ] Contrato de configuração versionado e migrações.
- [ ] Backend fictício com snapshot, eventos, heartbeat, stale e reconexão.
- [ ] Testar modo sem backend e garantir que simulação social não faz chamadas operacionais.
- [ ] Adaptador VST de referência depois do contrato neutro estabilizado.

## P4 — descoberta de backends (futuro)
- [ ] Implementar contrato de candidato/fonte/evidência/resultado.
- [ ] Pesquisa manual de endpoint/documentação fornecidos pelo utilizador.
- [ ] Catálogo versionado de adaptadores e compatibilidade.
- [ ] Health-check de leitura com consentimento, timeout e scope.
- [ ] Fontes de conectores/plugins autorizados.
- [ ] Só considerar descoberta local com opt-in e limites explícitos.
- [ ] Sem varredura indiscriminada, credenciais guardadas ou comandos de escrita.
- [ ] Nenhuma integração ativa sem escolha explícita.

## P5 — produto e distribuição
- [ ] Editor visual intuitivo.
- [ ] Triagem/enfermaria configurável com distinção de ações reais.
- [ ] Acessibilidade, segurança, import/export e migrações.
- [ ] Escolher e validar distribuição mobile/desktop a partir de evidência.


## P0 — segurança do host Windows e cadeia de confiança (2026-11-24)
- [ ] #140: deixar de confiar em `SystemRoot`/`WINDIR` herdados; estabelecer o root por boundary OS/installer confiável e provar que executáveis decoy em CWD/PATH não são chamados.
- [ ] #141: ancorar versão máxima e hash canónico da política fora do perfil gravável; suportar atualização atómica ou protocolo de duas fases com recovery; testar replay, backup restore, anchor ausente e interrupção.
- [ ] #104/#110: implementar installer/update assinado que verifica o próprio pacote, provisiona a chave CNG e política de forma atómica, com ACLs restritas e recovery; executar matriz nativa completa e validar em PC físico.
- [ ] Manter o host fail-closed e a PR #139 em Draft até todos os gates de confiança e freshness passarem.

## P1 — produção nas três edições
- [ ] #109: integrar licenciamento assinado e ativação durável nos hosts Universal, DGM-MAT e VST; keyring comercial/rotação, identidade por plataforma, seat enforcement, backup/restore e recuperação.
- [ ] #58: provider TPM monotónico real, sem inferir proteção a partir de fakes; testar power-loss, clear/reprovision e backup/restore em hardware físico.
- [ ] Implementar hosts e instaladores MSI/MSIX isolados; validar clean install, upgrade, rollback, repair e uninstall por edição.
- [ ] Providers de armazenamento seguro e identidade persistente para Linux/macOS/Android.

## P2 — integrações e operação segura
- [ ] #57: live E2E DGM-MAT read-only, com sessão real e testes de expiração/revogação.
- [ ] #121: manter comandos PAPER ocultos/bloqueados até o backend garantir atomicamente que cada operação é PAPER e rejeitar REAL/UNKNOWN/SAFE_MODE.
- [ ] #124: manter VST remoto desativado até Tailscale Serve HTTPS, pairing/token, identidade de dispositivo, scopes, revogação, redirect/DNS e reconciliação de POST desconhecido serem validados.
- [ ] Completar descoberta assistida Universal sem ligação automática, credenciais no core ou scanning indiscriminado.

## P3 — produto, UX e distribuição
- [ ] Onboarding, UX adaptativa, acessibilidade, observabilidade, atualização, backup/recuperação, assinatura e distribuição.
- [ ] Validar compatibilidade e instalação/desinstalação em Windows, Linux, macOS e Android físicos.
- [ ] Avatar Studio (#108): executar harness no browser real, stress de deformação/animações, inspeção visual dos quatro perfis e aceitação externa de GLB; manter isolado do runtime genérico.
