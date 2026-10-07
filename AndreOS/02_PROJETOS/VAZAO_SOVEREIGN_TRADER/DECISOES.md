# VAZÃO Sovereign Trader — Decisões

- Local-first: PC é centro de controlo.
- PAPER-first: evolução validada em PAPER/read-only antes de REAL.
- Fail closed: UNKNOWN/ambiguidade bloqueia.
- Venue é autoridade sobre resultado executado.
- Recovery é problema de consistência: journal + primary + backup + integrity + idempotency.
- UNKNOWN é estado próprio; não reenviar cegamente.
- REAL exige autorização humana independente.
- Repositórios de produto permanecem independentes; memória comum fica em andreos-memory.
- GitHub Actions é manual/deliberado devido ao orçamento consumido.
- A experiência de locking OS-level do PR #350 foi fechada após hangs de concorrência; não ressuscitar sem evidência forte.