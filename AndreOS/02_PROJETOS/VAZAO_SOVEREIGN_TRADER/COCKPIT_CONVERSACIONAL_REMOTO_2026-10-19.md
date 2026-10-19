# Decisão de memória — cockpit conversacional remoto Sovereign Trader
**Data:** 2026-10-19  
**Tipo:** requisito operacional confirmado pelo proprietário.

O proprietário é motorista de camião articulado e pode passar 20–30 dias fora de casa, a viajar pela Europa. O PC doméstico deve continuar a executar o Sovereign Trader e o proprietário precisa de acompanhar o estado e conversar com o Trader através do telemóvel.

Sovereign Trader é exclusivamente uma ferramenta de pesquisa, aprendizagem, análise e operação de trading. O cockpit deve aceitar ordens em linguagem natural, apresentar tarefas/estado/resultados reais, pesquisar com fontes e timestamps, e encaminhar pedidos de autenticação/aprovação para o proprietário remoto. Os pedidos não podem depender de pop-ups locais invisíveis fora de casa.

Passwords, tokens e códigos MFA devem ser introduzidos em canal seguro e não guardados no chat, logs ou notificações. Uma oportunidade identificada não autoriza execução. PAPER/REAL, Risk Engine, RealModeGuard, readiness, autenticação do operador e reconciliação continuam obrigatórios; mensagens do chat não podem ultrapassar esses gates. Ordens, alterações de risco e transferências são ações distintas, sujeitas a autorização apropriada. Resultado desconhecido exige reconciliação, não repetição cega.

PC_ENGINE continua autoridade de risco e execução; cockpit/MOBILE_APP é cliente remoto. Preferir conectividade privada autenticada, não expor API local diretamente à Internet, e testar expiração/revogação, owner/device binding e perda de rede.

**Fronteira de produto:** não fundir este produto com DGM-MAT nem partilhar dados financeiros, credenciais ou permissões entre ambos. Ver também o documento do cockpit no repositório Sovereign Trader.
