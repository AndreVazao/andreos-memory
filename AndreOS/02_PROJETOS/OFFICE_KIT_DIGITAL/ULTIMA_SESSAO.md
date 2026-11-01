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
- A alteração do seletor de qualidade e o ajuste final do HTML ainda não têm resultado CI confirmado; o endpoint de runs consultado não devolveu execução associada ao commit mais recente.

## Memória persistente AndreOS
Pasta AndreOS/02_PROJETOS/OFFICE_KIT_DIGITAL/ com MEMORIA_MESTRE.md, DECISOES.md, BACKLOG.md, ULTIMA_SESSAO.md e README.md. O índice global de projetos também foi atualizado.

## Próximos passos
1. Confirmar CI/sintaxe/testes para os commits recentes do seletor de qualidade.
2. Capturar/inspecionar preview em 390x844, 844x390 e desktop.
3. Corrigir escala, enquadramento, corte e legibilidade com base em capturas reais.
4. Acrescentar testes automatizados para resize/zoom/orientação e configurar CI visual.
5. Integrar perfis gráficos ao renderer e medir desempenho em aparelhos reais.
6. Continuar a investigação de módulos Diorama e proveniência/licenças antes de copiar código/assets.
7. Manter descoberta de backends como fase futura até os fundamentos visuais/runtime estarem validados.
