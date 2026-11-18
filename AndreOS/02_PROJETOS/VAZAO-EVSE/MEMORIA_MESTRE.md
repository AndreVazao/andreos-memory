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

### 2026-11-17 — TMCS1123 Rev D variant and ADC-rate screening

Product PR #8 head is now `5ed914ccd34c9db08025b6de3583a76e4b7c23dd`; PR #8 remains Draft/open/unmerged and stacked cleanly 8 commits ahead / 0 behind PR #7 base. The new review-only document `M2.9-M-TMCS1123-VARIANT-AND-ADC-RATE-SCREENING-2026-11-17.md` was published and fetched back for verification.

TI TMCS1123 datasheet Rev D (May 2026), Table 4-1:
- A1A at 5 V: ±96 A linear; at 3.3 V: −96 A to +28 A (not symmetric ±70 A).
- B1A at 3.3 V: ±62 A; at 5 V: −62 A to +130 A (not symmetric ±70 A).
- A3A at 5 V: ±32 A; at 3.3 V: −32 A to +9.3 A.
Therefore A1A at 5 V is the only symmetric ±70 A candidate among the compared A/B variants. It is not BOM-approved.
- Linear output range is separate from thermal SOA. TI Rev D SOA depends on ambient, PCB, airflow, pulse duration and duty cycle. 32 A_RMS continuous and provisional ±70 A peak must be validated independently; 70 A peak as a continuous sine is 49.5 A_RMS and cannot be presumed thermally safe at high ambient.
- M2.9-I's six isolated 5 V supplies are for six AMC1311B voltage channels, not a defined shared sensor/FDA rail. No approved 5V_MEAS source, regulator, load budget or sequencing was found. No rail changes made.

TI ADS131M06 Rev A gives HR mode options at 8.192 MHz CLKIN: OSR 1024/512/256/128 -> 4/8/16/32 kSPS. These are comparison values only; project CLKIN, OSR, filter, PGA and SPI timing remain open. No ADC settings or firmware changed.

Exact-head CI on previous code head `652eda7ca3624f81a225e09f15be32539b3b94ee` completed SUCCESS:
- verified-symbol run #43746490496;
- physical migration run #43746490537.
The new commit is documentation-only and triggered no workflows (no runs returned for new head); do not imply CI was rerun on it. PR #8 is 8 commits ahead / 0 behind its base per compare endpoint. GitHub's PR detail temporarily returned mergeable=false, so keep Draft and do not merge; comparison shows no behind commits.

No MASTER/BOM/netlist/pin-to-net/firmware/PCB changes, fabrication or energization approval. Full evidence in product PR #8 and the M2.9-M document.


## TestStation V1 — 2026-11-18 power-domain audit

PR #8 advanced with documentation-only commit `d7648844012224a68c023712da033a36fedadcf0`; branch compare is 9 commits ahead / 0 behind PR #7 base. PR #7 and #8 remain open Draft, unmerged, mergeable=true at latest check. New product document: `hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-N-5V-SENSOR-RAIL-AND-POWER-DOMAIN-AUDIT-2026-11-18.md`.

Direct read-only inspection of native `TS-V1-M2.9-K-MASTER.kicad_sch` (title-block M2.9-L.2) confirms six U15–U20 still use TMCS1123A3AQDVGR; six MEE1S2405SC U9–U14 and ISO5_A1..B3 labels exist; one 3V3_MEAS label exists; no 5V_MEAS label and no TLV70033 instance are present. Coordinate checks find no wire endpoint at pin 8 VS or pin 3 GND for any of U15–U20. This is source-text inspection only, not KiCad netlist/ERC validation. Therefore the native schematic snapshot does not yet implement a connected current-sensor supply/return tree; do not treat M2.9-J's 3V3_MEAS line as verified physical connectivity.

The M2.6/M2.9-I source discrepancy is now explicit: M2.6 §17 describes each AMC1311B domain as isolated 5 V followed by TLV70033 3.3 V; M2.9-I §4 describes the isolated 5 V as the AMC1311B supply. Actual pin-level source must be reconciled before rail design. Six isolated converter outputs remain reserved for independent AMC1311B voltage channels and must not be borrowed or paralleled.

TI TMCS1123 product data lists 14 mA maximum quiescent supply current; six sensors imply 84 mA / 0.42 W at 5 V sensor-only planning allowance. Six THP210 at 0.95 mA typical imply 5.7 mA typical only, not worst-case. No complete rail budget or regulator selection. A dedicated 5V_MEAS is an architecture option to evaluate, not an approved rail. No MASTER/BOM/net/pin/firmware/PCB change, fabrication, mains energization or safety approval.


**Further native-source finding (2026-11-18):** pin-coordinate inspection of MEE1S2405SC U9–U14 in the same M2.9-L.2 native schematic shows no explicit wire endpoint at any converter output pin (VOUT−/VOUT+) or VIN−. VIN+ has a wire endpoint only for U10/U11/U13/U14; not U9/U12. Thus the six independent ISO5 domains are architectural documentation intent, not fully implemented/verified connectivity in this native file. No native netlist/ERC run has been claimed. M2.9-N records the pin table.

A 36-row machine-readable observation register was added to product PR #8 at `hardware/teststation/V1/CAD/verification/netlist/M2.9-N-POWER-PIN-CONNECTIVITY-AUDIT.csv`; all `resolved_net` fields are deliberately blank. It is an observation record only, not a pin-to-net contract. Latest related product documentation commit at this point: `d5157af05e2aa118821ced2c8366ce9e6584dadc`.

**Latest 2026-11-18 checkpoint:** PR #8 head is `d5157af05e2aa118821ced2c8366ce9e6584dadc`; compare to PR #7 base is 14 ahead / 0 behind. PR #7 and #8 are both open Draft, unmerged, mergeable=true. Exact-head workflows #44269948933 (verified symbol library) and #44269949087 (physical symbol migration) are still IN_PROGRESS; completed static pin-map, six-sensor migration, range arithmetic, A1/ADS study arithmetic, footprint CSV and U19 coordinate checks are SUCCESS. KiCad 10 install/native parser/ERC/netlist stages have not completed, so no exact-head KiCad/ERC success is claimed.

### Correction to 2026-11-18 coordinate-only audit — KiCad evidence

The earlier manual coordinate observations in M2.9-N were not reliable because the full symbol orientation/transform was not accounted for. They are superseded for the review-migration schematic by KiCad 10.0.8 generated netlist evidence from physical migration workflow #44269949087. The exported source was the review-only `TS-V1-M2.9-K-MASTER-SYMBOL-MIGRATION.kicad_sch`, NOT the production MASTER.

KiCad netlist shows U15–U20: pin 8 VS connected to each `*_I` label; pin 9 VOC connected to each `*_I_RET` label; pins 1 IN+, 2 IN−, 3 GND, 5 VREF and 6 VOUT unconnected. This is a critical symbol/wiring mapping defect in the review migration export. U9–U14: `ISO5_A1/A2/B1/B2` labels on VIN+ pin 1 of U10/U11/U13/U14; all VIN− and VOUT−/VOUT+ pins unconnected; U9/U12 all four pins unconnected. U1/U2 ADS131M06 key power/reference pins unconnected in this review export.

KiCad ERC review-baseline: 300 errors / 53 warnings. Migrated review: 383 errors / 53 warnings (+83 errors). Native export success does not mean electrical correctness. Full report: product repo M2.9-O, plus corrected 98-row CSV `M2.9-N-POWER-PIN-CONNECTIVITY-AUDIT.csv`. The separate workflow #44269948933 is tasked with MASTER ERC/netlist and must finish before the MASTER power tree is described. No production design changes or approval.


### TestStation V1 — actual MASTER netlist completed 2026-11-18

KiCad 10.0.8 workflow #44269948933 completed SUCCESS and exported the actual production MASTER `TS-V1-M2.9-K-MASTER.kicad_sch`; blob SHA `3a75a000077a5acd208b5905a345a5e44aa78720` (same at workflow commit and later PR #8 docs-only head). Artifact ID 14412079410, SHA256 `0f2d963ec3d3081bd42a20955057deae57523112945c76672f0638356430026e`.

MASTER netlist: 24 components, 165 nets, 3 multi-node nets; automated triage `BLOCKED_KNOWN_SUSPICIOUS_CONNECTIONS`, all three U19/U2 cross-domain nets present:
- U19 GND pin3 ↔ U2 CS pin17
- U19 IN− pin2 ↔ U2 DOUT pin20
- U19 VS pin8 ↔ U2 SCLK pin19

Power tree is not implemented in the current MASTER:
- U9–U14 MEE1S2405SC: every VOUT pin unconnected; ISO5_A1/A2/B1/B2 labels on VIN+ pins of U10/U11/U13/U14; U9/U12 all pins unconnected.
- U3–U8 AMC1311B: all 8 pins unconnected.
- U15–U20 TMCS1123A3: IN+/IN−, GND and VOUT unconnected; each VREF pin5 carries *_I_RET label; VS pin8 unconnected except U19 suspicious cross-net.
- Dangling labels include 24V_SELV, 3V3_MEAS, AGND_B, ISO5_A3/B3 and current/voltage channel labels. REF1 VDD/VREF open; GND pin2 alone on AGND_A.
- ERC 353 messages: 300 errors, 53 warnings. Categories: 151 pin_not_connected, 66 power_pin_not_driven, 50 pin_not_driven, 32 label_dangling, 1 pin_to_pin; warnings 24 lib_symbol_issues, 18 unconnected_wire_endpoint, 11 isolated_pin_label.
Full product report M2.9-P and 145-row register `M2.9-P-MASTER-POWER-CONNECTIVITY-2026-11-18.csv`. Earlier coordinate-only claims withdrawn; these findings are from KiCad native netlist. No production design change or approval.


**Power-tree reconstruction backlog:** product PR #8 added M2.9-Q `M2.9-Q-POWER-TREE-INTENT-VS-MASTER-GAP-MATRIX-2026-11-18.md`. It compares M2.6/M2.9-I/M2.9-J/M2.9-M intended architecture against actual KiCad MASTER netlist and defines a controlled rebuild sequence. Key conflicts: M2.6 5V_ISO -> TLV70033 -> 3V3_ISO versus M2.9-I 5V isolated directly to AMC1311B; M2.9-J TMCS VS -> 3V3_MEAS versus M2.9-M A1A 5V requirement for symmetric ±70 A; converter references in M2.9-J do not match actual ISO labels on VIN+ pins. No pin-to-net or rail change approved.

**M2.9-R — dual-domain power study (2026-11-18):** product PR #8 now contains `M2.9-R-DUAL-DOMAIN-SUPPLY-ARCHITECTURE-STUDY-2026-11-18.md`. It records the AMC1311B high-side VDD1/GND1 and low-side VDD2/GND2 separation (TI typical 5 V/3.3 V), warns that an LDO on one isolated return cannot feed the opposite side without bypassing isolation, and flags MEE1S2405SC's 1000 V isolation rating for full working-voltage/surge/insulation coordination review. Candidate topology only: independent high-side supply domains, low-side ADC supply domain(s), separate 5V_MEAS for TMCS A1A/THP210. No rails or components approved.


### 2026-11-18 — TestStation isolated-supply requirements M2.9-S

Product PR #8 head at checkpoint: `baf8608aa548191528cd501eb3703c8c26f59cf9`. Exact-head workflows #44272428820 (physical migration) and #44272428736 (verified symbols) both completed SUCCESS. PR #8 remains Draft/open/unmerged, stacked on PR #7. These are CI validations, not electrical approval.

Product PR #8 added review-only M2.9-S:
`hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-S-ISOLATED-SUPPLY-REQUIREMENTS-AND-CONVERTER-SCREEN-2026-11-18.md`
Commit: `6941b6f3fcfbdfff59b17a18779fe208aed0b988`.

M2.9-S formalizes the candidate six independent floating AMC1311B high-side supply domains, low-side 3V3_MEAS candidate, and separate low-side 5V_MEAS candidate for TMCS1123A1A/THP210. MEE1S2405SC is NOT approved for mains-referenced high-side use: its published 1000 V isolation figure alone does not establish continuous working voltage, surge, reinforced insulation, certification or system insulation coordination. The 24V_SELV source/protection is not established in MASTER. No replacement DC/DC MPN selected.

No MASTER, BOM, netlist, pin-to-net, PCB, firmware or test procedure changed. No fabrication, energization, overload testing or safety approval.

### Checkpoint after M2.9-S — 2026-11-18 10:56 UTC

PR #8 now points to `6941b6f3fcfbdfff59b17a18779fe208aed0b988`, with 30 commits ahead / 0 behind PR #7 base. New M2.9-S file was fetched back and verified. Exact-head workflows #44289899964 (physical migration) and #44289899967 (verified symbol library) were still IN_PROGRESS at the latest check. Previous exact-head runs on predecessor `baf8608aa548191528cd501eb3703c8c26f59cf9` both succeeded (#44272428820 and #44272428736). PR #7/#8 remain open, Draft and unmerged. No production electrical changes.
