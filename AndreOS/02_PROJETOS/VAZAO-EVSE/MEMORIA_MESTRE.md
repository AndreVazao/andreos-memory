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


### ADS131M06 anti-alias and THP210 simulation — 2026-11-15

PR #8 design study now includes TI's ADS131M06 Rev A §9.1.2 reference anti-alias network (1 kΩ series in each input leg, 10 nF differential capacitor), stated by TI for CLKIN 2–8.2 MHz. Approximate differential pole is 7.96 kHz; do not freeze without actual CLKIN/OSR, measurement bandwidth, source impedance, THP210 stability and six-channel phase checks. TI lists THP210 PSpice and TINA-TI models. The latest product PR #8 head is `fd29ebb82394d72c929210d26c9d697ce3ce2e64`; exact-head workflows were queued at last check. All changes remain review-only and PR #8 Draft/unmerged.


### 2026-11-15 — ADC configuration and sensor supply HOLD

PR #8 exact-head CI passed on `fd29ebb82394d72c929210d26c9d697ce3ce2e64`: verified-symbol workflow #43707363902 and physical migration workflow #43707363906 both SUCCESS, including AFE arithmetic validation and native KiCad checks. This is CI/static evidence only, not analog/safety approval.

A source audit found no verified ADS131M06 firmware register/clock configuration in the indexed repo snapshot; M2.9-J explicitly leaves CLKIN/XTAL implementation on HOLD. Actual fCLKIN/fMOD, OSR, data rate, digital filter, PGA, reference mode and SPI/SYNC timing remain OPEN.

Blocking discrepancy: M2.9-J says TMCS1123 VS → 3V3_MEAS, while the A1/THP210 ±70 A study assumes 5 V and computes sensor VOUT up to 4.25 V nominal (4.2675 V with sensitivity-only +0.4% screening). Do not assume this is compatible with 3.3 V sensor supply, and do not change the rail without reviewing exact sensor variant, power tree and domains. A second discrepancy exists between M2.2 internal ADC reference baseline and M2.9-J/M2.9-L dedicated REFIN network.

Product PR #8 received review-only note `M2.9-K-ADC-CONFIGURATION-AND-SENSOR-RAIL-HOLD-2026-11-15.md`, commit `652eda7ca3624f81a225e09f15be32539b3b94ee`. No schematic, BOM, firmware, net mapping, PCB, fabrication or energization approval. Full details in TESTSTATION-V1-CAD-ENGINEERING-STATE-2026-11-13.md.