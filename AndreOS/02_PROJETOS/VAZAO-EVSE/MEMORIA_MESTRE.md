# VAZÃO EVSE — Memória Mestre

## Identidade

VAZÃO EVSE é a plataforma modular de carregamento elétrico AC.

A memória desta pasta cobre a plataforma como um todo, não apenas um carregador isolado.

## Escopo

- carregador AC simples
- carregador dual
- carregador quad
- wallbox
- futuras multistations
- hardware e quadros elétricos
- BOM e custos
- controlo local
- CPMS
- aplicação do cliente
- pagamentos
- gestão de parques
- TestStation Mini / PRO / Factory
- diagnóstico, validação e assistência

## Arquitetura funcional

Papéis principais:

- Oner / proprietário do sistema
- cliente / investidor / proprietário do parque
- utilizador final

O sistema de carregamento deve suportar controlo local e gestão remota conforme o tipo de instalação.

## TestStation

A VAZÃO EVSE TestStation é um módulo da mesma plataforma.

Variantes:

- Mini
- PRO
- Factory

Objetivos:

- desenvolvimento
- validação
- diagnóstico
- assistência
- produção

Inclui testes elétricos e funcionais, diagnóstico antes da máquina e dentro da máquina, análise de fases e orientação de correção.

## Fonte de verdade técnica

O GitHub da plataforma VAZÃO EVSE continua a ser a fonte de verdade do código/documentação técnica.

Esta pasta é a memória persistente transversal usada para recuperar decisões e contexto entre sessões e repos.


## TestStation current-channel design checkpoint — 2026-11-13

Current engineering proposal is 32 A RMS continuous and ±70 A instantaneous measurement target. 40 A RMS/10 s and 48 A RMS/1 s are analysis scenarios only, not verified thermal withstand or fault ratings. TMCS1123A1 at 5 V is the preferred analogue-front-end study candidate (±96 A linear range), not a BOM selection. A3 remains the existing BOM item and fails the 32 A RMS sinusoidal measurement range. A-family VREF is 2.5 V including A3; pin 5 is a reference output, not current return. A1 requires a designed conditioning/attenuation/common-mode stage before ADS131M06. Source of truth and detailed gates are in TESTSTATION-V1-CAD-ENGINEERING-STATE-2026-11-13.md and product repo PR #7. PR #7 remains Draft/unmerged; no schematic, BOM, PCB, fabrication or energization approval.


### A1 / ADS131M06 analogue-front-end study — 2026-11-13

A separate review-only engineering study is now in product PR #8, stacked on PR #7:
https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/8

TMCS1123A1 at 5 V remains a study candidate, not a BOM selection. The prior 0.60 attenuation suggestion is superseded; the study uses 0.50 or lower as a preliminary target to preserve more ADC differential headroom. No amplifier, resistor, capacitor, filter or clock setting is selected. VOUT/VREF must be sensed with suitable high impedance; A1 VOUT spans nominal 0.75–4.25 V at ±70 A, so its input stage cannot be assumed compatible with 3.3 V. Detailed arithmetic, architecture and remaining validation gates are recorded in TESTSTATION-V1-CAD-ENGINEERING-STATE-2026-11-13.md. PR #8 remains Draft/unmerged; no BOM or schematic change, fabrication or energization approval.


### 2026-11-15 — THP210 candidate for the TestStation AFE

The A1/ADS131M06 design study in product PR #8 now screens TI THP210 as the first fully differential amplifier candidate. It is not a BOM selection. The provisional output common-mode target is updated from 1.65 V to 2.25 V, following TI's documented 5 V THP210 application. At ±70 A, sensitivity-only +0.4% screening and gain 0.50, ideal ADC outputs are 1.81075–2.68925 V with ±0.8785 V differential, leaving 0.3215 V to nominal ±1.2 V PGA=1 FSR. The TMCS1123A1 VOUT/VREF pair common-mode is 1.625–3.375 V, inside THP210's 1–4 V input common-mode screening interval on 5 V supply.

Important gate: THP210 absolute maximum differential voltage between IN+ and IN− is ±0.5 V. Full sensor differential must not be connected directly across those pins; the closed-loop FDA resistor network, input-pin differential, start-up and powered-off fault cases require simulation. ADS131M06 delta-sigma settling and source-impedance interaction also require verification. PR #8 remains Draft/unmerged; no BOM, schematic, wiring, fabrication or energization approval. Full details in TESTSTATION-V1-CAD-ENGINEERING-STATE-2026-11-13.md.
