# Registo de referência externa — Moli

**Data:** 2026-10-17  
**Projeto:** DGM-MAT / AndreOS  
**Estado:** candidato para investigação; adoção não aprovada.

## Referência

- Projeto: Moli, navegador headless open source para agentes de IA, implementado em Rust.
- URL: https://github.com/lexmount/moli
- README: https://github.com/lexmount/moli/blob/main/README.md

## Porque interessa

Pode servir de backend opcional de navegação web para agentes DGM-MAT: extração de páginas para Markdown/HTML/JSON/árvore semântica, execução de JavaScript e automação por CLI, CDP, WebDriver Classic e WebDriver BiDi. O desenho de layout/renderização sob pedido pode ser interessante para tarefas que normalmente só precisam do DOM e do conteúdo estruturado.

## Reserva importante

Não é um browser gráfico completo e não promete paridade visual total com Chrome. Existem limites documentados para GUI persistente, Canvas/WebGL e certos modos de renderização. A compatibilidade, consumo de recursos no PC-alvo, segurança de rede e licenças têm de ser verificadas antes de qualquer adoção.

## Próxima ação

Criar uma prova de conceito isolada e comparar com a automação web já existente no DGM-MAT. Medir consumo de RAM/CPU, velocidade, qualidade da extração, compatibilidade com sites dinâmicos, estabilidade e comportamento perante falhas. Testar políticas contra SSRF/acesso a localhost e redes privadas. Não usar credenciais pessoais.

## Decisão atual

**Não integrar diretamente, não substituir ferramentas existentes e não tornar obrigatório.** Considerar um adaptador opcional apenas se os testes demonstrarem vantagem concreta. Manter o DGM-MAT funcional sem Moli.

## Documento técnico detalhado

Ver `docs/future/EXTERNAL_REPOSITORY_MOLI_REVIEW_2026-10-17.md` no repositório DGM-MAT.
