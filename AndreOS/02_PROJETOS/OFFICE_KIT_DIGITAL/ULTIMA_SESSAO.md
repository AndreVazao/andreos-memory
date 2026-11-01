# Office Kit Digital — último checkpoint

**Data:** 2026-11-01  
**Repo:** AndreVazao/office-kit  
**Branch:** docs/canonical-product-contract  
**PR:** #1 aberta em draft, não fundida.

## Alterações na repo do produto
- Atualizado docs/ROADMAP.md com a ordem explícita de desenvolvimento e a fase futura de descoberta de backends.
- Criado docs/BACKEND_DISCOVERY.md com fontes permitidas, evidência por candidato, consentimento, limites de segurança e testes de aceitação.
- Atualizado docs/README.md e docs/IMPLEMENTATION_STATUS.md.
- Integrado o motor de cena no preview: examples/browser-preview/app.mjs importa calculateSceneLayout, aplica fit scale, trata resize/ResizeObserver e atualiza zoom e orientação.
- Ajustadas dimensões CSS de telhado/pisos/fundação para aproximar as dimensões lógicas do motor.

## Verificação confirmada
- GitHub Actions run #38, ID 41291021736, commit f57330eefbedc4ae53de9083dfca3a401ad4681a: SUCCESS em syntax checks, testes core/scene-engine/perfis gráficos e parsing JSON.
- Alterações de integração visual posteriores estão à espera de nova CI confirmada. A consulta à API ainda não devolveu run associado ao commit mais recente.
- Não foram produzidas screenshots nem executados testes de browser/aparelho físico para a integração atual.

## Memória persistente AndreOS
Pasta AndreOS/02_PROJETOS/OFFICE_KIT_DIGITAL/ com MEMORIA_MESTRE.md, DECISOES.md, BACKLOG.md, ULTIMA_SESSAO.md e README.md. O índice global de projetos também foi atualizado.

## Próximos passos
1. Confirmar nova CI para os commits de integração visual.
2. Inspecionar a cena em browser e capturar 390x844, 844x390 e desktop.
3. Corrigir escala/layout a partir das capturas, sem alegar validação visual antes de as observar.
4. Acrescentar testes automatizados de resize/zoom/orientação.
5. Integrar perfis gráficos reais no renderer e medir desempenho em aparelhos.
6. Manter descoberta de backends como fase futura até os fundamentos visuais/runtime estarem validados.
