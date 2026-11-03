# VazaoSovereignTrader — checkpoint de continuidade
Data: 2026-10-11
Branch GitHub: `continuity/pc-setup-2026-10-11`

## Objetivo deste registo
Preservar o estado conhecido do projeto e impedir que a sincronização do DGM-MAT altere inadvertidamente o ambiente de trading. Este checkpoint é documental; não valida a estratégia nem o estado live do motor.

## Evidência do PC recolhida antes de o Desktop Commander esgotar as chamadas
- Workspace/repositorio observado em `C:\\ProgramasGodMode\\VazaoSovereignTrader`.
- Ambiente virtual observado em `C:\\ProgramasGodMode\\VazaoSovereignTrader\\PC_ENGINE\\.venv`.
- Snapshot do PC: Windows 10 Home x64, build 19045; 2 cores; cerca de 2,96 GiB RAM.
- Python global 3.12.6 em `%LOCALAPPDATA%\\Programs\\Python\\Python312\\python.exe`; falta verificar qual interpretador o venv usa.
- O Desktop Commander está agora a 0% de chamadas remotas. Estado Git local, divergência local/remoto, dependências do venv e saúde atual do motor não foram revalidados.

## Limites de segurança
- Não publicar `.env`, credenciais de exchange, API keys, tokens, dados de conta, logs privados ou material de carteira.
- Não executar operações de trading, ordens, alterações de estratégia, limites de risco ou configurações como parte da sincronização.
- Não fazer reset forçado nem sobrescrever alterações locais não revistas.
- Sem GitHub Actions/builds automáticos por defeito; preservar os minutos.
- Dependências e credenciais do Sovereign Trader continuam isoladas do DGM-MAT, mesmo quando ferramentas comuns são inventariadas centralmente.

## Próximos passos quando o PC voltar a estar acessível
1. Recolher read-only: `git status`, branch, remotes, commits recentes e diff local.
2. Inspecionar o interpretador e as dependências do venv sem imprimir segredos.
3. Comparar as histórias local e GitHub, preservando ambos os lados antes de reconciliar.
4. Registar caminhos absolutos, versões, origem dos pacotes, hashes/assinaturas e probes de saúde inofensivas.
5. Só executar testes offline aprovados; não contactar exchanges nem iniciar trading para validar a instalação.

Referência técnica publicada no repositório `AndreVazao/VazaoSovereignTrader`: `docs/continuity/PC_AND_GITHUB_CONTINUITY_2026-10-11.md`.
