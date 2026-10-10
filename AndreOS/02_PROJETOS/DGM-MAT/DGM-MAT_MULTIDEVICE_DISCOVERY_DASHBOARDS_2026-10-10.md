# DGM-MAT — Acesso multi-dispositivo, descoberta e dashboards

Data: 2026-10-10
Tipo: decisão arquitetural vinculativa

## Contexto real de utilização

O utilizador trabalha em rotas de camião pela Europa e precisa de usar o DGM-MAT pelo telefone sem introduzir IPs. Em casa, quer um dashboard completo no PC e quer poder instalar apenas o dashboard noutros PCs/portáteis para comunicar pela rede local com uma torre que executa o Core como servidor em background.

## Arquitetura decidida

- **PC servidor = cérebro:** runtime, memória operacional, scheduler, agentes, delegações, missões, checkpoints, ferramentas e fonte de verdade.
- **Cockpit móvel = comunicação simples:** chat contínuo, conversas, seleção de projeto e provedor, pedidos, notificações e pop-ups de intervenção humana.
- **Dashboard desktop = gestão avançada:** missões/delegações, projetos, repositórios, ferramentas, ficheiros, diagnósticos, saúde, aprovações, políticas, auditoria e configuração.
- **Dashboard noutro PC = cliente remoto**, não outro cérebro. Fechar o cliente nunca pode parar o Core.

O Core deve correr em background supervisionado, sem depender de janelas de terminal ou dashboard aberto. O servidor continua trabalho independente quando os clientes estão offline.

## Descoberta sem IP manual

Em casa, procurar um Core emparelhado através de descoberta local (ex. mDNS/DNS-SD) e/ou registo conhecido, sempre com autenticação e validação de identidade.

Fora de casa, usar Tailscale como conectividade privada e um serviço de rendezvous/descoberta (potencialmente no Vercel). O Core inicia uma ligação de saída autenticada e publica apenas presença/metadados mínimos. O cliente autenticado encontra o servidor emparelhado e estabelece ligação privada através do tailnet. Vercel não é um túnel mágico nem torna um PC atrás de NAT diretamente acessível; se Tailscale não estiver disponível, a app deve mostrar offline e nunca abrir portas públicas automaticamente. Qualquer relay futuro exige desenho de segurança e validação próprios.

Tailscale, IPs, CORS ou pertença à rede não substituem autenticação da aplicação. ACLs/grants devem limitar o acesso ao servidor e às portas necessárias. Não usar Funnel/publicação pública como atalho.

## Segurança antes de acesso remoto

Auditoria preliminar encontrou rotas HTTP/WebSocket sem proteção global aparente e cliente móvel sem sessão autenticada. A API deve continuar limitada a loopback até autenticação HTTP/WebSocket, pairing, identidade por dispositivo, scopes mínimos, expiração/revogação, proteção anti-replay e migração dos clientes estarem concluídos e testados. Não guardar credenciais, OTP, tokens ou passwords em prompts, logs, memória persistente ou metadados do rendezvous.

## Continuidade e intervenção humana

Pedidos de intervenção persistem no Core quando o telefone está offline. A delegação dependente fica pendente e outras delegações continuam trabalho independente seguro. Ao reconectar, o cliente autentica, sincroniza e deduplica antes de permitir ações. Cada resposta fica limitada ao utilizador/dispositivo/pedido/missão/etapa/prazo e é processada uma vez. Verificar o estado real antes de retomar; não repetir automaticamente ações externas não idempotentes de resultado incerto.

## Fases

1. Inventário e especificação do runtime/APIs/portas.
2. Separar e validar Core em background e dashboard independente.
3. Autenticação global HTTP/WebSocket, pairing e migração segura dos clientes.
4. Cockpit móvel com chat, projetos, provedores, notificações e intervenções.
5. Descoberta LAN sem IP manual.
6. Tailscale privado validado fora da LAN.
7. Rendezvous Vercel com heartbeat de saída e descoberta autenticada, sem segredos.
8. Dashboard avançado instalável noutros PCs.
9. Teste end-to-end de viagem: telefone fora da rede, Core em background, perda/reconexão, pedidos pendentes e retomada.

## Critérios de aceitação

- Na Europa, o telefone encontra o servidor emparelhado sem escrever IPs.
- Torre sem monitor/dashboard aberto mantém o Core a trabalhar.
- Portátil pode executar só o dashboard e ligar-se ao Core autorizado.
- Perder ligação não para o cérebro e nunca expõe automaticamente a API.
- Descoberta, autenticação, sincronização e intervenções são testadas end-to-end.
- Política FREE-ONLY / PAID-DENY; sem custos/créditos sem autorização.

## Estado real

É uma decisão arquitetural/documentação, não prova de implementação. Tailscale, rendezvous Vercel, autenticação global, cockpit móvel e dashboard multi-PC só serão considerados concluídos após implementação e testes reais.

Documento no repo DGM-MAT: `docs/architecture/MULTI_DEVICE_ACCESS_DISCOVERY_AND_DASHBOARDS.md`.
Relacionado: `PC_BRAIN_MOBILE_COCKPIT_PARALLEL_DELEGATIONS.md`, `HUMAN_IN_THE_LOOP_HANDOFF.md`.
