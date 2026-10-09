# DGM-MAT — Clarificação de arquitetura: backend, dashboard desktop e cockpit móvel
<!-- Path: C:\AndreOS-Memory\AndreOS\05_LOGS_IA\DGM-MAT_BACKEND_DESKTOP_MOBILE_BOUNDARIES_2026-10-09.md -->

Data: 2026-10-09
Estado: decisão de arquitetura confirmada pelo utilizador; orientação vinculativa para as próximas fases.

## Decisão principal

O DGM-MAT tem três superfícies distintas, com responsabilidades claras:

1. **Backend/runtime no PC** — prioridade de desenvolvimento atual. Deve correr continuamente em background, sem janela de terminal ou consola visível, com arranque e paragem controlados, logs/diagnóstico e recuperação de falhas. O backend é o motor operacional; não é a interface de trabalho.
2. **Dashboard desktop** — interface de trabalho para quando o utilizador está sentado ao PC. Será desenvolvida depois de o backend estar estável e operacional. Deve ser intuitiva, prática, agradável e organizada, inspirada no fluxo conversacional do ChatGPT sem necessidade de design extravagante. Deve permitir trabalhar confortavelmente, ver estado, conversar com o sistema e gerir operações/aprovações.
3. **Cockpit móvel** — experiência separada, otimizada para telefone, com controlos compactos e adaptação ao ecrã. Deve sincronizar automaticamente com o PC e evitar obrigar o utilizador a introduzir endereços IP manualmente.

## Prioridades

- Agora: concentrar esforço no backend, segurança, estabilidade, contratos de API, runtime, logs, recuperação, aprovações e testes reais controlados.
- Depois: construir o dashboard desktop sobre APIs estáveis, com uma experiência de trabalho tipo ChatGPT.
- Em paralelo, apenas quando não desviar o foco do backend: documentar a arquitetura de sincronização móvel/PC.
- Mais tarde: implementar descoberta/conexão automática segura entre PC e telefone, usando a solução de rede privada já existente no projeto (Tailscale como contexto atual), autenticação e identificação de dispositivo; não assumir que IPs fixos escritos à mão são a solução final.
- A referência do utilizador a “Pell scale” foi interpretada como referência à parte móvel/escala responsiva e à sincronização; confirmar o termo técnico quando se for desenhar essa componente, sem bloquear o trabalho atual do backend.

## Requisitos não negociáveis

- O backend não deve depender de uma janela de dashboard aberta.
- Fechar o dashboard não deve parar o backend.
- O dashboard desktop e o cockpit móvel são clientes do mesmo backend/API, com permissões apropriadas; não devem implementar motores de execução independentes.
- Não iniciar já uma reformulação visual do dashboard enquanto a estabilidade do backend estiver por concluir.
- Não expor a API do backend indiscriminadamente à rede; ligação móvel deve usar rede privada/confiável e autenticação.
- Não afirmar sincronização automática concluída antes de implementar e testar descoberta, autenticação, reconexão e comportamento quando um dispositivo está offline.

## Contexto existente

- O utilizador quer um cockpit móvel via Tailscale; referências de dispositivos previamente registadas: PC 100.69.225.48 e telefone 100.109.173.115. Tratar estes endereços como contexto histórico, não como valores hardcoded obrigatórios.
- A API governada de providers e o fluxo de aprovação humana são a base em desenvolvimento; os providers permanecem safe-off até às validações e decisões de ativação necessárias.
- Manter a regra de estabilidade > funcionalidades, realidade > suposições, controlo manual > automação destrutiva.
- Preservar originais em DGM-MAT-OS antes de alterar ficheiros existentes; nunca aceder ou modificar C:\ProgramasGodMode\DGM-MAT-FULL-MIRROR.
