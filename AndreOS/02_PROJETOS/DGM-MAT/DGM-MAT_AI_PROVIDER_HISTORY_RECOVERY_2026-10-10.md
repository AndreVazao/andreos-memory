# DGM-MAT — Plano para recuperar históricos de IAs e organizar scripts
Data: 2026-10-10

Objetivo prioritário: o DGM-MAT deve recuperar contextos históricos de ChatGPT, Gemini, Grok e outras ferramentas autorizadas, encontrar scripts acima no histórico, organizar conversas por projeto, comparar versões e encaminhar artefactos para repositórios e memória.

Decisões:
- Preferir exportações oficiais quando disponíveis; usar browser autenticado e governado como segunda opção; OCR/pywinauto como fallback.
- Criar perfil de browser dedicado ao DGM-MAT. Login inicial manual num browser visível; headless apenas após teste de estabilidade. Não extrair cookies/tokens do Chrome pessoal Default.
- Não criar vault com passwords reutilizadas em texto simples nem pedir ao utilizador que as partilhe no chat. Preferir sessão persistente dedicada; credenciais necessárias para integrações suportadas devem ficar em Windows Credential Manager/DPAPI ou vault cifrada protegida pelo SO, nunca em Git, logs, prompts ou memória geral.
- Mobile recebe pedidos de intervenção, nunca passwords/cookies/tokens/MFA. O login é concluído diretamente no PC/browser oficial.
- Importação incremental com checkpoints, estado parcial explícito, pesquisa DOM, scroll verificado, deduplicação e proveniência. Nunca afirmar completude se só foi lida parte visível.
- Scripts recuperados ficam em quarentena/revisão, não são executados nem aplicados automaticamente. Comparar com os repositórios atuais, testar e pedir aprovação.
- Perfil leve: um browser por vez, pequenos lotes, OCR só quando necessário. Headless é otimização posterior, não ponto de partida.
- Cockpit deve ter área “Fontes de IA”, cartões por fornecedor, estado da sessão, ligar/reautenticar, testar, importar, pausar e terminar sessão.
- CAPTCHA/MFA manual; sem contornar limites de fornecedores; API permanece local até auth live e pairing validados.

Estado atual: GovernedBrowserSession existe mas é efémera, não herda a sessão Chrome pessoal e ainda não foi encontrado endpoint API para cockpit. Esta é uma arquitetura planeada, não uma capacidade entregue.

Documento técnico: `docs/architecture/AI_PROVIDER_HISTORY_RECOVERY_AND_SCRIPT_ARCHIVE_2026-10-10.md`.
