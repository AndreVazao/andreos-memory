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
