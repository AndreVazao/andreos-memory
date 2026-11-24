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


## 2026-11-24 — Isolamento das edições e fronteira read-only
- Universal é um produto independente de DGM-MAT e VST. As três edições podem partilhar apenas o core genérico; adapters, credenciais, identidade e dados específicos permanecem na edição/instalação respetiva.
- Todo o backend começa desconectado e read-only. Descoberta não equivale a autenticação, compatibilidade, sincronização ou autorização. Não inventar atividade operacional nem permitir controlos PAPER/REAL sem enforcement autoritativo do backend.
- VST remoto continua desativado até validação completa do transporte privado Tailscale e pairing; DGM-MAT/VST live E2E ainda são gates de produção.

## 2026-11-24 — Windows publisher policy: autenticidade não é freshness
- WinVerifyTrust deve validar a assinatura primária e obter o signer do mesmo provider state; comparar SHA-256 SPKI e aplicar revogação explícita fail-closed.
- Um envelope assinado não prova que é o mais recente. A política exige high-water mark protegido fora do perfil gravável, hash canónico por versão e atualização crash-recoverable.
- Caminhos absolutos derivados de SystemRoot/WINDIR herdados não são uma raiz de confiança. O installer/launcher deve estabelecer o root por boundary OS confiável e testar executáveis decoy.
- Sem installer/update autenticado, âncora anti-replay e matriz nativa completa, manter o host fail-closed e não distribuir comercialmente.

## 2026-11-24 — Classes de evidência
- Fakes/unit tests não provam drivers nativos. SQLite/WAL e processos reais em CI provam apenas os cenários exercitados. WinTrust/CNG em runners Windows não prova cadeia comercial nem instalação física. TPM, power-loss, restore e live adapters exigem hardware/instâncias reais e evidência específica.
