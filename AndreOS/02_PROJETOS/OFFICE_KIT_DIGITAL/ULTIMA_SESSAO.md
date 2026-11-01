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

## Próximos passos
1. Capturar/inspecionar preview em 390x844, 844x390 e desktop com browser real; os testes de origem não substituem screenshots.
3. Corrigir escala, enquadramento, corte e legibilidade com base em capturas reais.
4. Acrescentar testes automatizados para resize/zoom/orientação e configurar CI visual.
5. Integrar perfis gráficos ao renderer e medir desempenho em aparelhos reais.
6. Continuar a investigação de módulos Diorama e proveniência/licenças antes de copiar código/assets.
7. Manter descoberta de backends como fase futura até os fundamentos visuais/runtime estarem validados.
