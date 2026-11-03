# Registo de decisões — catálogo mestre e escritório virtual DGM-MAT
**Data:** 2026-10-14  
**Branch:** `docs/tooling-capability-audit-2026-10-14`  
**Estado:** decisão documental registada; implementação futura, não executada.

## 1. Catálogo mestre de capacidades
Consolidar a lista inicial de plugins/MCPs/ferramentas e a lista complementar de plugins e skills Claude Code num catálogo mestre com IDs únicos, aliases e níveis de validação V0–V4. Todos os candidatos começam como **por identificar/não verificados**; não assumir que estão instalados, são gratuitos, seguros, mantidos ou compatíveis. Manter as listas detalhadas e a auditoria como referências cruzadas.

Documento DGM-MAT: `docs/architecture/DGM-MAT_MASTER_CAPABILITY_CATALOG_2026-10-14.md`.

Princípios: estabilidade antes de funcionalidades; evidência antes de conclusões; local-first; sem API paga obrigatória nem fallback pago silencioso; medir recursos no PC de 2 núcleos/~3 GB RAM; aprovar manualmente permissões, efeitos externos e alterações persistentes. Clones de terceiros e Labs não devem ser alterados nem sincronizados por esta tarefa.

## 2. Conceito do escritório empresarial virtual
O escritório DGM-MAT será uma visualização operacional isométrica/3D ligada ao estado real do Orchestrator/Runtime. Cada departamento ocupa um piso lógico; a Direção/Boss fica no último piso; os pisos comunicam através de elevadores e telefone/mensagens. Os agentes podem levantar-se, caminhar, usar o elevador, recolher uma encomenda no departamento de origem e regressar ao trabalho, quando a política do pedido exige recolha presencial.

O fluxo logístico deve ser real e rastreável: pedido com ID → aceite/rejeitado → preparação → pronto → transporte → entregue → reconhecido. O telefone é um evento visual e não substitui o registo persistente. Encomendas digitais podem ser entregues diretamente; recolha presencial só ocorre quando faz sentido. Nenhuma animação pode marcar uma tarefa concluída sem evento confirmado no backend.

Piso 0 proposto: receção, armazém, fila e expedição. Pisos intermédios: departamentos reais existentes (engenharia, investigação, QA, segurança, memória/documentação, conectores/operações, ajustáveis após auditoria). Último piso: boss, prioridades, escalamentos e relatórios. Salas comuns incluem reunião, arquivo/biblioteca, laboratório isolado e enfermaria/sala de recuperação.

Manter conceitos já definidos:
- Enfermaria para agentes realmente bloqueados/à espera de recuperação, mostrando causa e ação seguinte.
- Armazém com contagens derivadas de pedidos pendentes, em preparação, prontos e expedidos.
- Entregas externas com embalagem/viatura apenas quando a expedição real é confirmada.
- Separar estado de domínio e animação; a vista 3D nunca é fonte da verdade e o backend deve continuar a funcionar sem a vista aberta.
- Implementação por MVPs: planta estática, presença real, rotas, chamadas/pedidos, elevadores/encomendas, depois logística e reuniões.
- Manter uma vista compacta 2D/lista, acessibilidade, movimentos reduzidos e consumo baixo de RAM/CPU.

Referência de investigação: `docs/architecture/DGM-MAT_VIRTUAL_OFFICE_RESEARCH_2026-10-14.md` no DGM-MAT. Foram identificados projetos públicos para estudar padrões, não aprovados para instalação ou clonagem. A análise inicial favorece a comparação de arquitetura e separação de responsabilidades, não a adoção direta de um projeto externo.

## 3. Segurança e âmbito
- Não instalar nem executar os projetos de referência nesta fase.
- Não fazer merge na main, não sincronizar a cópia local nesta ação e não alterar clones de terceiros/Labs.
- Antes de adoção, verificar URL oficial, licença, commit, dependências, permissões, rede, autenticação, armazenamento e recursos.
- Qualquer ação com efeito externo exige contrato, registo de auditoria e aprovação humana apropriada.
