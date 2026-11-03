# Memória DGM-MAT — Auditoria de aplicações Web e automação visual
Data: 2026-10-10

Foi feita uma inspeção somente leitura ao PC para avaliar o uso das aplicações de IA já instaladas como ferramentas gratuitas do DGM-MAT.

## Evidências
- ChatGPT, Grok e Gemini são aplicações Web do Chrome abertas com `chrome_proxy.exe` e o perfil `Default`.
- Claude tem um atalho para `C:\\ProgramasGodMode\\DGM-MAT-Claude-Agent.cmd`; Perplexity é uma aplicação própria.
- Tesseract 5.4.0 está instalado com idiomas português (`por`) e inglês (`eng`).
- Python 3.12 tem Playwright e pywinauto.
- O serviço `GovernedBrowserSession` já suporta sessões Playwright efémeras, navegação, leitura de página, cliques, preenchimento limitado, screenshots e OCR local.
- Os métodos são chamados pelo MissionEngine, mas não foram encontrados endpoints de API que exponham essas operações ao cockpit.
- A sessão Playwright é isolada e não reutiliza a autenticação do perfil Chrome pessoal. Não se deve copiar cookies/tokens nem ler credenciais do perfil pessoal.

## Decisão arquitetural
É viável desenvolver automação governada para usar interfaces Web gratuitas, mas não declarar a capacidade concluída. Implementar primeiro uma instância de browser dedicada ao DGM-MAT, login manual, API autenticada e permissões por missão; exigir aprovação humana para enviar mensagens na fase inicial. Usar pywinauto/OCR como alternativa quando o DOM não estiver acessível. Não contornar CAPTCHA/MFA nem automatizar ações financeiras ou irreversíveis.

Documento de evidência no repositório DGM-MAT:
`docs/architecture/WEB_AI_APPS_AND_VISUAL_AUTOMATION_AUDIT_2026-10-10.md`
