# VST — identidade oficial e continuidade do escritório virtual

Data: 2026-10-23

## Decisão oficial

- A sigla curta oficial é **VST**.
- O nome completo é **Vazão Sovereign Trader**.
- Em interfaces, títulos e mensagens curtas, preferir VST.
- Na primeira referência técnica, escrever VST (Vazão Sovereign Trader); depois, VST.
- Não renomear repositórios, módulos, caminhos ou identificadores técnicos só por causa da sigla.

## Regra visual obrigatória do escritório virtual

O lockup deve apresentar a sigla em grande e alinhar cada palavra por baixo da inicial correspondente:

- **V** com **Vazão** por baixo.
- **S** com **Sovereign** por baixo.
- **T** com **Trader** por baixo.

A sigla VST deve ser imediatamente reconhecível; as palavras completas devem estar visualmente associadas à letra correta, em três colunas, e não aparecer apenas como tagline corrida. O pequeno sigilo VST pode permanecer junto ao lockup.

## Implementação iniciada

Branch do produto: https://github.com/AndreVazao/VazaoSovereignTrader/tree/feat/vst-office-brand-lockup-2026-10-23

Alterações preparadas na branch:
- virtual_office/prototype/full_cockpit_shell.html — lockup alinhado no cockpit/escritório integrado, com tamanhos menores para mobile.
- virtual_office/prototype/index.html — lockup correspondente no protótipo visual standalone.
- README.md — regra oficial de nomenclatura.
- docs/VST_BRAND_STANDARD.md — norma de identidade e limites da mudança.

Esta alteração é branding/documentação apenas. Não altera o motor, feeds, estado de agentes, permissões, risco ou execução. A interface continua obrigada a mostrar demo/ligação de acordo com o estado real do backend.

PR do produto será aberto em draft para revisão e CI; não fazer merge até os checks aplicáveis estarem verdes e a diff ser revista.

## Continuidade técnica paralela

A prioridade funcional permanece a revisão do PR #481 de sincronização de order book OKX. Os bloqueios registados no checkpoint de revisão continuam válidos: heartbeat e freshness, mensagens data vazias, snapshots antigos e evidência de testes no head exato. OKX depth permanece inelegível para edge cross-venue até a máquina de estados e a CI serem comprovadas.

Segurança: PAPER/read-only, sem ordens reais, transferências, levantamentos ou ativação REAL.
