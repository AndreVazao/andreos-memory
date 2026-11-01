# Office Kit Digital — memória mestre

**Estado do registo:** 2026-11-01  
**Repo do produto:** AndreVazao/office-kit  
**Branch ativa conhecida:** docs/canonical-product-contract  
**PR de trabalho:** #1 — feat: establish Office Kit contract and first runnable core  
**Estado da PR:** aberta, draft; não fundida no último estado verificado. Confirmar novamente antes de operações futuras.

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
