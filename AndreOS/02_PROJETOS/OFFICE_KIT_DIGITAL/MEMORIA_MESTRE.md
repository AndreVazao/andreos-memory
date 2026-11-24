# Office Kit Digital — memória mestre

**Estado do registo:** 2026-11-24 13:31 UTC  
**Repo do produto:** AndreVazao/office-kit  
**Memória canónica:** AndreVazao/andreos-memory — `AndreOS/02_PROJETOS/OFFICE_KIT_DIGITAL/`  
**Main verificada:** `027851c04ff1b23d239b90a06bfc4ef84aecf425`  
**PR runtime ativa:** #139 — Draft; HEAD `13b190de4c4a0e18cb1ba33c9ad2d8e9344629fb`; CI em execução após atualização documental; visual PASS.  
**PR separada:** #108 — Avatar Studio Draft; browser/GLB acceptance pendente.

## Estado global verificado — 2026-11-24 13:31 UTC

### Repositório e PRs
- Produto: [AndreVazao/office-kit](https://github.com/AndreVazao/office-kit).
- Main HEAD verificada pelo base SHA da PR #139: `027851c04ff1b23d239b90a06bfc4ef84aecf425` (commit #138: remoção do teste WinTrust que ainda não estava revisto na main).
- 94 branches listadas; 2 PRs abertas; 9 issues técnicas abertas.
- PR #139 — Authenticode/WinTrust — branch `feat/authenticode-wintrust-primary-mainline-2026-11-23`, HEAD atual após documentação: `13b190de4c4a0e18cb1ba33c9ad2d8e9344629fb`, Draft, aberta e mergeable. Regressão visual #45405580584 passou nesse HEAD. CI #45405580412 ainda estava em execução: Linux Node 22/26 passou; Windows Node 22/26 estava a publicar o CNG host, sem falhas observadas até ao checkpoint. Não transportar resultados de SHA anterior para este HEAD.
- O HEAD de código imediatamente anterior, `bb457884444d14eae7e8d51cd162338c84291c56`, passou CI #45403375515 nos quatro jobs Linux/Windows Node 22/26.13.1 e visual #45403375437. Ambos os Windows jobs executaram CNG policy bootstrap, WinTrust nativo, persistência CNG, identidade/journal e bundles E2E Universal/DGM-MAT/VST.
- PR #108 — Avatar Studio — HEAD `3749ba5fbfc8b7cd184b7af37ad74f0fb3a9829c`, Draft e isolada em `avatar-studio/`; CI #45379629961 e visual #45379629909 passaram nesse SHA. O harness GLB/rig continua a precisar de execução no browser real e aceitação externa de GLB; a regressão visual do Office Kit não substitui esses testes.

### Capacidades integradas
- PR #127: contrato neutro Universal de descoberta de backends, sem varrimento, autenticação, ativação ou ligação automática.
- PR #132: VST `GET /health` público e sem token; rotas privadas continuam autenticadas. Falhas públicas não invalidam a sessão privada.
- PR #133: validação null-safe do CNG AlgorithmGroup; avisos CS8602 corrigidos sem supressão.
- PRs #135–#137: chave CNG machine-scoped RSA-3072, envelope de política assinado e leitura da chave pública diretamente do CNG.
- PR #139: WinVerifyTrust nativo, assinatura primária índice 0, certificado extraído do mesmo provider state, pin SHA-256 SPKI, revogação online para install/update e cache-only para startup; ambos fail-closed. Teste nativo Windows usa runtime Node assinado pela Microsoft e rejeita cópia adulterada.

### Bloqueios de produção identificados
- #140: resolver de executáveis usa caminhos absolutos e sanitiza PATH/PSModulePath, mas ainda confia em `SystemRoot`/`WINDIR` herdados. Um root local forjado e internamente consistente não é autenticado; faltam boundary confiável installer/launcher e testes nativos com executáveis decoy.
- #141: envelope assinado em `publisher-policy.json` sob data root do utilizador pode ser substituído por envelope antigo autêntico. Falta high-water mark monotónico protegido fora do perfil gravável, atualização atómica/crash-recoverable e testes de restore/replay.
- #110: gate pai Authenticode; matriz nativa completa para expirado/revogado/untrusted/unknown revocation/múltiplas assinaturas/ACL/timeout e validação física pendentes.
- #104: instaladores MSI/MSIX e fluxo real de install/update ainda não verificam o pacote nem provisionam chave CNG/política assinada atomicamente.
- #109: licenciamento ainda precisa de integração nos três hosts, keyring comercial, ativação durável e recuperação.
- #58: TPM/anti-rollback real e testes físicos de power-loss/backup/restore pendentes.
- #57: live E2E DGM-MAT pendente. #121: PAPER controls bloqueados até enforcement atómico no backend. #124: transporte VST remoto Tailscale permanece desativado até validação integral.

### Fronteiras obrigatórias
- Universal é produto independente; DGM-MAT e VST são edições/instalações isoladas e partilham apenas o core genérico.
- Adaptadores e credenciais específicas permanecem nas respetivas edições.
- Qualquer backend começa desconectado e read-only. Não inferir trabalho operacional, não inventar atividade e não ativar comandos PAPER/REAL por UI.
- Testes com fakes, SQLite/processos reais em CI, integração com drivers nativos e validação física são classes de evidência distintas.
- Nenhuma edição está pronta para distribuição comercial; não alegar instalação física, TPM real ou integração live sem evidência.

## Próxima ordem de execução
1. Fechar #140 com raiz Windows obtida por boundary confiável e testes decoy nativos.
2. Fechar #141 com anchor de versão/hash protegido e protocolo de update crash-recoverable.
3. Integrar provisioning no instalador/update #104 e completar a matriz nativa #110.
4. Integrar licenciamento #109 e providers seguros/identidade durável por plataforma.
5. Continuar SQLite/TPM #58, integração read-only DGM-MAT/VST, PAPER #121 e Tailscale #124.
6. Hosts/instaladores Linux/macOS/Android, onboarding, acessibilidade, observabilidade, backup/recuperação, assinatura e distribuição.

## Missão

Criar um escritório digital visual, leve, intuitivo e totalmente configurável que represente equipas, departamentos e agentes de qualquer projeto. Tem de funcionar em diferentes backends e aparelhos, com modos de visualização e qualidade gráfica adaptáveis. VST é apenas um caso de referência, não uma dependência.

## Requisitos não negociáveis do utilizador

- O backend/cérebro deve funcionar independentemente do Office Kit. Fechar, bloquear, atualizar ou remover o frontend não pode parar nem corromper o backend.
- O Office Kit deve ser adaptável a qualquer tipo de projeto/backend, usando contratos neutros e adaptadores, sem dependências específicas do projeto no renderer.
- Deve funcionar em telemóvel, tablet e computador; suportar retrato e paisagem sem deformação, sobreposição crítica ou texto ilegível.
- Deve oferecer vários modos de visualização, desde chat/painel simples e 2D leve até pixel diorama, 2.5D/isométrico e eventualmente 3D, conforme implementação real.
- Deve permitir níveis de qualidade selecionáveis e adaptação automática às capacidades/desempenho do dispositivo.
- A composição deve ser configurável: edifícios, pisos, departamentos, salas, personagens/agentes, avatares, mobiliário, temas, nomes, posições e regras visuais.
- A configuração deve ser intuitiva; um utilizador comum não deve precisar de editar código.
- Sem backend válido, os personagens podem realizar animações sociais locais (café, conversa, caminhar, pausa, relógio, varanda etc.), mas nunca podem dar a entender que executam trabalho real.
- Trabalho e estado operacional só são representados como reais quando confirmados pelo backend; distinguir ligado, sincronizado, desatualizado, desconectado e desconhecido.
- Uma enfermaria/triagem pode representar perda de comunicação, mas não pode fingir diagnóstico, reinício ou recuperação.
- O renderer deve ser isolado, resiliente e leve; reduzir efeitos/densidade antes de sacrificar informação operacional ou legibilidade.
- Estudar e adaptar de forma seletiva sloemo01/diorama como referência visual; não copiar uma cena fixa nem importar assets/código sem verificar proveniência e licença.
- Não alegar testes, builds, screenshots, integração, instalação ou merge sem evidência concreta.
- Documentar decisões canónicas e a ordem de desenvolvimento na repo do produto e nesta memória persistente.

## Implementação registada em 2026-11-01

- Repo pública AndreVazao/office-kit; branch de trabalho docs/canonical-product-contract; PR #1 aberta em draft.
- Core JavaScript sem dependências para validar/normalizar configuração e separar simulação social local de estado operacional confirmado.
- Preset genérico JSON e preview browser responsivo inicial; o preview ainda é protótipo CSS, não renderer final. O preview agora importa o motor de cena e aplica escala calculada no resize/zoom.
- Motor de cena renderer-neutral com layout determinístico, ordem de pisos, posições lógicas, validação de viewport, escala e zoom.
- Perfis gráficos definidos em packages/scene-engine/src/quality.mjs: economy, balanced, detailed, cinematic, e resolução automática conservadora por pistas do dispositivo.
- GitHub Actions run #50 (ID 41291148536) passou em commit 5a96970246aebc3abcb2d8203a64b8a1c2983afc: syntax checks, testes core/scene-engine/perfis gráficos e parsing JSON após integração do motor de cena no preview.
- GitHub Actions run #62 (ID 41291442920) passou no commit 55031c9456533a579de459cdc7ead87a92b5edd3 após adição do seletor de qualidade e ajuste do HTML.
- Corrigido o posicionamento do edifício escalado para o centro do viewport e o overflow horizontal; adicionados testes de regressão de origem para layout responsivo.
- GitHub Actions run #70 (ID 41292191794) passou no commit f13f8233348134fc741e032ae5d170349d3d28ba com o fix de enquadramento e os novos testes. Isto não valida renderização visual nem dispositivos físicos.
- Foi adicionado um seletor de qualidade no preview (automático/económico/equilibrado/detalhado/cinemático) com efeitos CSS leves. Não controla ainda DPR, texturas, GPU, metas reais de FPS ou autoajuste por frame time.
- A integração dos perfis num renderer real, métricas de frame time, autoajuste em runtime e benchmarks em aparelhos físicos não estão implementados.
- O renderer final estilo diorama, assets/rigs, editor visual, adaptadores reais e embalagem APK/desktop não estão implementados.

## Decisão canónica adicional — edifício e personagens interativos

- Vista inicial do modo edifício: edifício inteiro numa perspetiva superior angular com corte frontal.
- Selecionar departamento/divisão aproxima a visualização à área; deve ser possível regressar à vista geral.
- Todos os avatares são selecionáveis e podem abrir conversa contextual; chefias recebem pedidos dirigidos aos respetivos departamentos.
- CEO selecionável com avatar configurável a partir da imagem do utilizador, como representação do utilizador no escritório para comandar/consultar.
- Nenhuma conversa/ordem pode ser apresentada como entregue ou executada sem confirmação real do adaptador/backend.
- Canonizado em `docs/PRODUCT_CONTRACT.md`; ainda não implementado nem validado visualmente.

## Decisões e próximos passos

A ordem canónica encontra-se em docs/ROADMAP.md. Prioridade imediata:
1. Capturar e inspecionar o preview integrado em retrato, paisagem e desktop; corrigir escala/legibilidade com evidência.
3. Corrigir enquadramento, escala, rotação, legibilidade e sobreposição em telemóvel/tablet/PC.
3. Criar cena determinística pequena, carregada por configuração, usando a referência Diorama após auditoria suficiente.
4. Implementar capturas automatizadas em retrato/paisagem e verificar erros visuais.
5. Integrar perfis gráficos no renderer e medir desempenho real.
6. Implementar animação social local sem qualquer autoridade operacional.
7. Definir/validar o contrato de backend e reconexão com backend fictício.
8. Implementar futuramente descoberta assistida e segura de pontos de ligação a possíveis backends.
9. Construir adaptador de referência VST sem dependência VST no core.
10. Editor plug-and-play, triagem/enfermaria e distribuição após os fundamentos.



## Avanço: harness de validação visual real (2026-11-01)
- Confirmado novamente: PR #1 em AndreVazao/office-kit continua aberta, draft, não fundida; branch `docs/canonical-product-contract`.
- Criado `scripts/visual-check.mjs`: serve o preview localmente, abre Chromium via Playwright e testa 390×844 retrato, 844×390 paisagem e 1366×768 desktop; verifica carregamento, ausência de overflow horizontal, limites horizontais do edifício dentro do viewport, departamentos renderizados, seletor de qualidade, seleção de departamento e erros de browser; guarda uma screenshot por viewport.
- Criado `.github/workflows/visual-regression.yml`: instala temporariamente Playwright/Chromium, executa as verificações e publica screenshots como artifact do GitHub Actions.
- Atualizados `docs/ROADMAP.md` e `docs/IMPLEMENTATION_STATUS.md` para refletir que o harness está criado, mas a execução/inspeção das capturas ainda está pendente. Não afirmar que o visual passou até existir run bem-sucedido e screenshots inspecionadas.
- A vista inicial em corte angular, zoom real por departamento e conversa por avatar/CEO continuam requisitos canónicos ainda não implementados.



## Resultado visual e interação de foco (2026-11-01)
- Visual regression run #2, ID 41293249440, concluiu SUCCESS; screenshots artifact ID 13077921682 (390×844 portrait, 844×390 landscape, 1366×768 desktop) foram descarregadas e inspecionadas.
- Observado: o edifício cabe nos três viewports e não há overflow horizontal; a versão atual é ainda um placeholder CSS. Em retrato, rótulos/personagens ficam pequenos; em paisagem, os detalhes também são reduzidos; não existe ainda perspetiva angular/corte frontal real.
- Implementado no preview CSS um foco/zoom provisório ao selecionar um departamento, com botão “Vista geral” e seleção de departamento também por clique/teclado no piso.
- Ampliado `scripts/visual-check.mjs` para verificar que o foco aumenta a cena e que o botão regressa à vista geral.
- CI normal #95 e visual #15 estão em curso após estas últimas alterações; não assumir sucesso até verificar ambos.
- Documentação de roteiro/estado atualizada. PR #1 continua draft, aberta e não fundida.



## Resultado confirmado — zoom de departamento e CI visual (2026-11-01)
- Corrigidos os handlers do preview: selecionar departamento/piso aplica zoom de foco, destaca a zona e revela “Vista geral”; o piso é também selecionável por teclado (Enter/Espaço).
- O teste Playwright aguarda o fim da transição antes de comparar geometria. CI normal #108 passou.
- Visual regression run #28, ID 41293713424, passou; artifact screenshots ID 13077699039 para 390×844, 844×390 e 1366×768. O script verifica também o zoom de foco e o reset para a vista geral.
- A vista geral atual ainda é uma caixa CSS simples, não a perspetiva superior angular com corte frontal pretendida. Os avatares ainda não abrem conversas; CEO configurável e comandos reais continuam pendentes.
- PR #1 segue aberta em draft, não fundida. Último HEAD antes das atualizações documentais: 17b93542fd582a6fb9fac19b59a0921d1e775f90; atualizar HEAD/CI depois dos commits documentais antes de declarar estado final.

## Requisito futuro: procurar pontos de ligação a backends

O utilizador antecipa uma espécie de motor de busca/assistente para procurar pontos de conexão a possíveis backends. Está documentado em docs/BACKEND_DISCOVERY.md, ainda não implementado. Deve:
- começar por endpoints/documentação/catálogos que o utilizador forneça ou autorize;
- mostrar evidência, origem, compatibilidade estimada, capacidades e requisitos;
- separar endpoint encontrado de autenticação válida, adaptador compatível e estado sincronizado;
- nunca fazer varredura indiscriminada, contornar autenticação, procurar/guardar segredos ou enviar comandos de escrita;
- exigir escolha e consentimento explícitos antes de validar/ativar integração;
- manter Office Kit funcional sem qualquer backend ou serviço de descoberta.

## Referências canónicas

- Repo: https://github.com/AndreVazao/office-kit
- PR: https://github.com/AndreVazao/office-kit/pull/1
- Roteiro: docs/ROADMAP.md
- Contrato: docs/PRODUCT_CONTRACT.md
- Perfis gráficos: docs/QUALITY_PROFILES.md
- Descoberta de backends: docs/BACKEND_DISCOVERY.md
- Diorama: https://github.com/sloemo01/diorama

Não assumir que o estado remoto permanece igual ao deste checkpoint. Verificar PR, branch, CI e commits antes de continuar.
