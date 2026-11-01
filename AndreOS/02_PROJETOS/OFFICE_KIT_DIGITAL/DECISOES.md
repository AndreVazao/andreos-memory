# Office Kit Digital — decisões canónicas

## 2026-11-01 — Produto genérico e independente
- Office Kit é camada visual/configurável; nunca é o cérebro operacional.
- VST é exemplo de referência, não dependência.
- Renderer, core, adaptadores e configuração devem permanecer separados.
- O produto deve servir múltiplos domínios e tipos de backend sem reescrever o core.

## 2026-11-01 — Qualidade adaptável
- Perfis: Económico, Equilibrado, Detalhado e Cinemático; existe resolução lógica Auto.
- O utilizador pode escolher perfil manualmente.
- Auto deve ser conservador quando os dados do dispositivo faltam.
- Futuro ajuste por frame time usa janelas estáveis e histerese, evitando oscilações.
- A redução de qualidade nunca deve remover informação operacional essencial nem tornar os controlos ilegíveis.
- Alvos FPS são metas, não promessas de desempenho.

## 2026-11-01 — Estado real vs animação social
- Simulação social local não cria tarefas nem envia comandos.
- Só estado/evento confirmado por adaptador pode ser apresentado como trabalho real.
- Perda de comunicação pode originar triagem visual; ações de recuperação exigem capacidade e autorização reais.

## 2026-11-01 — Descoberta futura de backends
- O utilizador pretende uma ferramenta/assistente de pesquisa de pontos de ligação a possíveis backends.
- Esta capacidade deve ser planeada/documentada antes de implementação.
- Começar por fontes explícitas autorizadas; sem scanning indiscriminado.
- Descoberta é só pesquisa/avaliação. Sem comandos de escrita, recolha de segredos ou ativação automática.
- Utilizador escolhe o candidato e autoriza validação/ligação.

## 2026-11-01 — Ordem de desenvolvimento
Consultar docs/ROADMAP.md na repo office-kit. Prioridade imediata: integração do motor de cena no preview, correção de escala/legibilidade, cena determinística, capturas e testes, integração real dos perfis gráficos, animações sociais, contrato/adaptadores, descoberta de backends, editor e distribuição.

## Regra de evidência
Não declarar implementação, teste, build, screenshot, CI, integração, instalação ou merge como concluídos sem resultado observável e verificável.
