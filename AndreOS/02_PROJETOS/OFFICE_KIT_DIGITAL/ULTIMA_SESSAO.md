# Office Kit Digital — último checkpoint

**Data:** 2026-11-01  
**Repo:** AndreVazao/office-kit  
**Branch:** docs/canonical-product-contract  
**PR:** #1 aberta em draft, não fundida; última verificação mergeable.

## Alterações na repo do produto
- Atualizado docs/ROADMAP.md com ordem explícita de desenvolvimento e fase futura de descoberta de backends.
- Criado docs/BACKEND_DISCOVERY.md com fontes permitidas, evidência por candidato, consentimento, limites de segurança e testes de aceitação.
- Atualizado docs/README.md e docs/IMPLEMENTATION_STATUS.md.
- Integrado o motor de cena no preview: examples/browser-preview/app.mjs importa calculateSceneLayout, aplica fit scale e trata zoom/resize/ResizeObserver.
- Ajustadas dimensões CSS de telhado/pisos/fundação para aproximar as dimensões lógicas do motor.
- Adicionado seletor visível de qualidade no preview (Automático, Económico, Equilibrado, Detalhado, Cinemático); nesta fase, os perfis aplicam apenas efeitos/animações CSS simples. Não controlam DPR, texturas, GPU nem FPS real.
- Atualizado docs/IMPLEMENTATION_STATUS.md para declarar claramente o âmbito limitado do seletor.
- A demonstração continua a ser um protótipo CSS; não é ainda o renderer final.

## Verificação confirmada
- GitHub Actions run #50, ID 41291148536, SUCCESS. O job core-tests passou syntax checks, testes do core/motor de cena/perfis gráficos e parsing JSON.
- Run #50 verificou o código de integração visual nos commits incluídos no HEAD 5a96970246aebc3abcb2d8203a64b8a1c2983afc. Foi depois feito um commit documental para atualizar o estado da implementação; não alterou código.
- Não foram produzidas screenshots nem executados testes de browser/aparelho físico. CI verde não prova correção visual.
- GitHub Actions run #62, ID 41291442920, SUCCESS para o commit 55031c9456533a579de459cdc7ead87a92b5edd3, cobrindo a alteração do seletor e o ajuste final do HTML.
- Corrigido o enquadramento do edifício: passou a ser ancorado no centro do viewport com translate + scale e o viewport corta overflow, evitando que a caixa lógica de 1200px desloque o edifício para fora do ecrã estreito.
- Criado packages/scene-engine/test/preview-layout.test.mjs com testes de regressão de origem para centralização, clipping, ResizeObserver e regras CSS retrato/paisagem.
- GitHub Actions run #70, ID 41292191794, SUCCESS no commit f13f8233348134fc741e032ae5d170349d3d28ba, incluindo o fix de enquadramento e os testes novos. O commit documental posterior não alterou código.

## Memória persistente AndreOS
Pasta AndreOS/02_PROJETOS/OFFICE_KIT_DIGITAL/ com MEMORIA_MESTRE.md, DECISOES.md, BACKLOG.md, ULTIMA_SESSAO.md e README.md. O índice global de projetos também foi atualizado.

## Nova decisão canónica — vista geral e interação espacial (2026-11-01)
- A vista inicial do modo edifício deve mostrar o edifício inteiro em perspetiva superior angular com corte frontal, permitindo compreender pisos, departamentos e divisões.
- Clicar/tocar num departamento ou divisão foca essa zona por zoom; deve existir regresso simples à vista geral.
- Todos os avatares devem ser selecionáveis e permitir conversa contextual. Chefias servem como pontos de entrada para pedidos dirigidos ao departamento.
- O CEO é uma personagem central selecionável, configurável com imagem do utilizador, para este se representar dentro do escritório e comandar/consultar o sistema.
- Interações reais só são confirmadas por adaptador/backend ligado e autorizado; sem ligação, a UI não pode fingir que a ordem foi enviada ou executada.
- Requisito já registado em `docs/PRODUCT_CONTRACT.md`, `docs/ROADMAP.md` e `docs/IMPLEMENTATION_STATUS.md` na branch `docs/canonical-product-contract`. Ainda não implementado nem validado visualmente.

## Próximos passos
1. Capturar/inspecionar preview em 390x844, 844x390 e desktop com browser real; os testes de origem não substituem screenshots.
3. Corrigir escala, enquadramento, corte e legibilidade com base em capturas reais.
4. Acrescentar testes automatizados para resize/zoom/orientação e configurar CI visual.
5. Integrar perfis gráficos ao renderer e medir desempenho em aparelhos reais.
6. Continuar a investigação de módulos Diorama e proveniência/licenças antes de copiar código/assets.
7. Manter descoberta de backends como fase futura até os fundamentos visuais/runtime estarem validados.

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



## Checkpoint global — 2026-11-24 13:31 UTC

### Office Kit main e PRs
- Main/base da PR #139: `027851c04ff1b23d239b90a06bfc4ef84aecf425` (commit #138 removeu da main um teste WinTrust que ainda não estava revisto).
- PR #139 Draft, branch `feat/authenticode-wintrust-primary-mainline-2026-11-23`, HEAD depois da atualização documental `13b190de4c4a0e18cb1ba33c9ad2d8e9344629fb`. Visual #45405580584 PASS. CI #45405580412 estava em execução: Linux Node 22/26 PASS; Windows Node 22/26 ainda em Publish Windows CNG host. Não há merge.
- HEAD de código anterior `bb457884444d14eae7e8d51cd162338c84291c56`: CI #45403375515 PASS nos quatro jobs Linux/Windows Node 22/26.13.1; visual #45403375437 PASS. Os jobs Windows passaram CNG bootstrap, WinTrust nativo, journal/identity e bundles E2E das três edições.
- PR #108 Avatar Studio permanece Draft, isolada em `avatar-studio/`; HEAD `3749ba5fbfc8b7cd184b7af37ad74f0fb3a9829c`; CI #45379629961 e visual #45379629909 PASS. O harness de GLB/rig ainda não foi executado num browser real nesta execução.
- Auditados 94 branches, 2 PRs abertas e 9 issues abertas.

### Alterações nesta execução
- Atualizados na branch #139 os documentos `docs/IMPLEMENTATION_STATUS.md`, `docs/ROADMAP.md`, `docs/ARCHITECTURE.md` e `docs/security/WINDOWS_AUTHENTICODE_POLICY.md` com os blockers #140 e #141 e limites da evidência.
- Atualizada a descrição da PR #139 e adicionado checkpoint de evidência à issue #110.
- Não foram alterados backends VST/DGM-MAT, credenciais, trust stores ou infraestrutura externa.

### Novos blockers confirmados
- #140: paths absolutos System32 continuam derivados de `SystemRoot`/`WINDIR` herdados; falta root OS confiável e testes decoy nativos.
- #141: envelope assinado pode sofrer replay de versão antiga porque não existe high-water mark protegido fora do perfil do utilizador.
- #104/#110: installer/update ainda não verifica o pacote nem provisiona política/chave CNG atomicamente; matriz nativa completa e PC físico pendentes.
- #109 licensing, #58 TPM/anti-rollback, #57 DGM-MAT live, #121 PAPER backend enforcement e #124 Tailscale VST continuam gates abertos.

### Próximo passo
Concluir CI no HEAD documental atual #139; depois resolver #140 e #141 dentro da única PR runtime ativa, ou manter o host fail-closed se a solução exigir uma fase de installer separada. Não fazer merge enquanto a política de confiança não for completa. Manter Universal independente de DGM-MAT/VST, core genérico partilhado e backend inicial read-only/desconectado.
