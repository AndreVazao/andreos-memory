# Office Kit Digital — backlog e ordem de execução

## P0 — próximo trabalho
- [ ] Inspecionar estado atual da branch/PR e CI antes de escrever mais.
- [ ] Integrar packages/scene-engine no examples/browser-preview em vez de manter layout duplicado.
- [ ] Rever escalas e rótulos para ecrãs estreitos; garantir rotação retrato/paisagem.
- [ ] Fazer a demonstração carregar toda a cena a partir de configuração.
- [ ] Acrescentar testes para resize, zoom e orientação.
- [ ] Disparar/confirmar CI após as alterações recentes.

## P1 — renderer e QA visual
- [ ] Escolher e implementar primeira cena determinística pequena inspirada no Diorama após auditoria suficiente.
- [ ] Capturas repetíveis em 390x844, 844x390 e desktop, ajustando os tamanhos de referência conforme a infraestrutura.
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
