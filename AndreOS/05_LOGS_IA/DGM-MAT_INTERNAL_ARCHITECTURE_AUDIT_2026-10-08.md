# DGM-MAT Internal Architecture Reuse Audit — 2026-10-08

Auditoria comparativa entre DGM-MAT e os repos independentes DGM-HUB/DGM-MCP.

Resultado:
- DGM-HUB TruthLayer não deve ser copiado: DGM-MAT já possui RealitySnapshotService, RuntimeStateStore, runtime path validation, health/degradation/recovery e governance.
- DGM-HUB AgentLoop/ToolReasoner/patch orchestration são referências algorítmicas apenas; DGM-MAT já possui agents/autonomy/development/execution_fabric/governance/self_evolution/recovery.
- DGM-HUB/DGM-MCP ToolRegistry/PathGuard/BaseTool demonstram padrões úteis, mas não devem introduzir dependências nem execução não governada no DGM-MAT.
- Foram encontrados dois placeholders potencialmente mortos no DGM-MAT: core/development/test_orchestrator.py e core/execution_fabric/validation_pipeline.py. Ambos retornam True sem executar validação real e não foram encontrados como referências no core. Devem ser removidos/quarentenados ou transformados em adapters reais apenas depois de definir contrato e testes.
- Decisão: estabilidade > funcionalidades; não importar código só por duplicação aparente; preferir consolidação, remoção de dead code ou adapters estreitos testados.
