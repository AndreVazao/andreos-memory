# SwapMaster AI — memória mestre

**Última atualização:** 2026-11-13  
**Repositório de produto:** https://github.com/AndreVazao/SwapMaster-AI  
**Repositório:** público durante desenvolvimento, por decisão explícita do André. Reavaliar passagem a privado apenas quando o produto estiver pronto e após revisão de dados, segredos, dependências e histórico Git.  
**Memória persistente:** este documento vive no AndreOS Memory; o código e documentação técnica do produto vivem no repositório SwapMaster-AI.

## Objetivo

Aplicação desktop Windows, modular e extensível, para apoiar o planeamento de swaps de motores de combustão, elétricos e híbridos e conversões EV. Deve cruzar dimensões, interfaces, pontos de fixação, transmissão, requisitos auxiliares e dados com proveniência; apoiar medições e importação de digitalizações 3D; e produzir documentação e CAD preliminar com revisão humana.

Idioma inicial: Português (Portugal), com arquitetura preparada para localização.

## Regras de engenharia e segurança

- Nunca declarar compatibilidade física apenas por dimensões externas.
- Distinguir sempre dados confirmados, documentados, estimados e desconhecidos.
- Preservar fonte, método de medição, unidades, incerteza e revisão de cada dado.
- Bloquear conclusões positivas quando faltam dados críticos.
- Apoios, adaptadores, caixas de bateria e interfaces estruturais são safety-critical.
- CAD futuro deve estar marcado **PRELIMINAR — NÃO FABRICAR — REQUER VALIDAÇÃO DE ENGENHARIA** até existir revisão técnica independente.
- IA pode propor alterações, mas não pode aplicá-las sem diff legível e aprovação explícita do André.
- Não prometer homologação, segurança estrutural ou prontidão de fabrico sem evidência e validação profissional.

## Estado real verificado

### GitHub
- Repositório AndreVazao/SwapMaster-AI confirmado.
- Visibilidade observada: public, autorizada explicitamente pelo André em 2026-11-13 para facilitar Actions durante desenvolvimento.
- Branch main: README inicial.
- Branch develop: implementação de fundação.
- PR draft #1: https://github.com/AndreVazao/SwapMaster-AI/pull/1

### Implementado em develop (primeiro incremento)
- Projeto Python configurado em pyproject.toml (Python 3.11+).
- Modelo de proveniência Evidence com níveis confirmed/documented/estimated/unknown.
- Modelo Envelope3D com validação de dimensões e comparação com folga.
- Avaliação conservadora de envelope, sem confundir bounding-box pass com fitment real.
- Testes pytest para proveniência, dimensões e resultados preliminares.
- Workflow GitHub Actions .github/workflows/ci.yml: matriz Windows/Ubuntu e Python 3.11/3.12, com pytest, Ruff e mypy.
- Documentação: arquitetura, segurança de engenharia, roadmap e contribuição.

### CI
- Workflow foi acionado nos pushes para develop.
- Como cada ficheiro foi commitado separadamente, vários runs intermédios foram cancelados pela política concurrency (cancel-in-progress).
- O run final observado: https://github.com/AndreVazao/SwapMaster-AI/actions/runs/43429400303
- Na última consulta ainda estava em execução/queued; **não registar como aprovado até verificar conclusão verde de todos os jobs**.

## Próximas prioridades

1. Verificar e corrigir CI até todos os jobs Windows/Linux e Python 3.11/3.12 passarem.
2. Corrigir a cadência de commits (agrupar alterações em commits menores, evitar disparar workflow em cada ficheiro).
3. Expandir domínio: veículo, motor, caixa, interfaces, pontos de montagem, massa, centro de gravidade, requisitos auxiliares e unidades.
4. Base de dados local versionada, importação validada e catálogo com fontes verificáveis.
5. Motor de regras multidimensional com resultados explicáveis e bloqueios por dados em falta.
6. UI desktop e fluxos Simples/Técnico/Oficina.
7. Planeamento de conversão EV e checklist de alta tensão.
8. Importação de malhas 3D, calibração e pontos de referência.
9. CAD paramétrico preliminar e documentação de revisão.
10. ONER com aprovação humana obrigatória.
11. Empacotamento Windows, instalador e testes em máquina limpa.

## Governança Git

- main é a base estável.
- develop recebe desenvolvimento ativo.
- PRs focados, pequenos e revistos.
- Não fazer merge do PR #1 até CI ficar verde e conteúdo ser revisto.
- Não publicar segredos, credenciais, dados pessoais ou dados proprietários no repositório público.
- Reavaliar visibilidade pública/privada antes de qualquer release.

## Nota de continuidade

O projeto está em fundação técnica inicial; não está completo, não tem catálogo real de motores/veículos, UI desktop, scanner 3D funcional, CAD de fabrico, análise FEA, instalador nem validação de engenharia. Comunicar sempre o estado real.
