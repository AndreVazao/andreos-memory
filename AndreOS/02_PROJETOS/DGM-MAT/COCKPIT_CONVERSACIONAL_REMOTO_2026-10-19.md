# Decisão de memória — cockpit conversacional remoto DGM-MAT
**Data:** 2026-10-19  
**Tipo:** requisito operacional confirmado pelo proprietário.

O proprietário é motorista de camião articulado e pode passar 20–30 dias fora de casa, a viajar pela Europa. O PC de casa deve continuar a executar o DGM-MAT e o proprietário precisa de acompanhar o trabalho e conversar com o sistema a partir do telemóvel.

DGM-MAT é uma ferramenta para construir e reparar ferramentas: engenharia, DevOps, scripts, auditoria, pesquisa técnica e integração de conversas/respostas de várias IAs. O cockpit deve aceitar linguagem natural, expor o estado real das missões, preservar contexto após desconexões e encaminhar pedidos de aprovação/autenticação até ao proprietário remoto. Não basta um pop-up local no PC.

Credenciais e códigos MFA devem ser introduzidos por um canal seguro, nunca no histórico de chat, logs ou notificações. Aprovações devem estar autenticadas, vinculadas à ação e dispositivo, ser expiradas/revogáveis e falhar em modo fechado. O PC/cérebro continua a autoridade de execução; o cockpit é uma interface remota de observabilidade e comando autenticado. Não expor APIs locais diretamente à Internet.

**Fronteira de produto:** este requisito de experiência não transforma DGM-MAT no Sovereign Trader nem autoriza partilha de credenciais, dados ou permissões entre os produtos. Ver também o documento de arquitetura no repositório DGM-MAT.
