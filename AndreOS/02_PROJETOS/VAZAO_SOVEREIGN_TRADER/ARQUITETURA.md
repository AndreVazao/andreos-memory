# VAZÃO Sovereign Trader — Arquitetura

## PC_ENGINE
Cérebro local: estado, risco, estratégia, adapters, reconciliação, recovery e coordenação.

## MOBILE_APP
Cockpit operacional/observabilidade. Nunca ultrapassa os gates do PC Engine.

## shared
Contratos e modelos partilhados.

## Recovery
Primary snapshot + backup snapshot + reconciliation journal + SHA-256 integrity + generation/optimistic concurrency + atomic writes/fsync quando suportado. Journal antes da mutação; limpeza só depois de convergência durável verificável.

## Pending orders
Reconciliação cumulativa de filled quantity, quote/cost e fee. Só remove pending order perante estado terminal autoritativo e remaining qty dentro da tolerância. Fetch errors, estado ambíguo, identity mismatch ou fill inválido permanecem unresolved e fail closed.

## Account reconciliation
Venue autoritativa é a fonte de verdade. Mismatch de posição/base/quote/unexpected asset não é corrigido silenciosamente: bloqueia e entra SAFE_MODE. PR #371 tornou essa condição durável através de restart.

## Capability
market_data_historical, market_data_websocket, market_data_realtime, account_balances, account_positions, paper_order_submit, paper_order_cancel, real_order_submit, real_order_cancel, capital_transfer.
Capability declarada não é autorização REAL; evidence deve ser positiva, fresca e do ambiente correto.

## Capital transfer
PREPARED, SUBMITTED, CONFIRMED, UNKNOWN_OUTCOME, BLOCKED. UNKNOWN_OUTCOME nunca recebe retry cego.

## Superfícies
Browser web, desktop/Windows e Android/APK/emulador. Sem bypass de MFA/CAPTCHA.