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


### 2026-11-18 — M2.9-T standards applicability

PR #8 added review-only M2.9-T at `hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-T-STANDARDS-APPLICABILITY-AND-INSULATION-COORDINATION-BASIS-2026-11-18.md`, commit `b338f5f529fb37b2868c9af4918cfbad5b33c8e4`.

M2.9-T distinguishes a standalone electrical measurement/test instrument from EVSE product equipment. IEC 61010-1 and IEC 61010-2-030 are primary applicability candidates if the TestStation is a standalone measurement/test instrument; IEC 60664-1 is a candidate insulation-coordination basis; IEC 61851-1 applies to EVSE equipment and is not automatically the TestStation's own product safety standard. No formal standard applicability or edition is approved. Product boundary, measurement category, voltage/transient/impulse environment, pollution degree, altitude, insulation objective and protective-earth/operator access must be defined first.

Exact-head CI on M2.9-S: #44289899964 physical migration SUCCESS; #44289899967 verified symbol library CANCELLED. Predecessor exact-head checks both succeeded on `baf8608aa548191528cd501eb3703c8c26f59cf9`. M2.9-T adds documentation only. No MASTER/BOM/netlist/pin mapping/PCB/firmware changes.


### 2026-11-18 — M2.9-U: definitive MEE1 exclusion

Official Murata MEE1 datasheet and exact MEE1S2405SC product entry reviewed. M2.9-U published in EVSE Platform PR #8 at `hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-U-MEE1S2405SC-MANUFACTURER-INSULATION-CLASSIFICATION-DECISION-2026-11-18.md`, commit `b4eeab3a35cb211d0e258e87cde85505e34f9ccb`.

Murata states MEE1 is UL60950-recognized for functional insulation, both sides normally remain SELV, 1kVDC is a 1-second production hi-pot test, and the part must never be used as an element of a safety-isolation system. Exact part is therefore excluded from a mains-referenced-to-accessible safety barrier. This supersedes the earlier evidence-only HOLD for that specific role. No replacement MPN selected; no MASTER/BOM/netlist/PCB change.


### 2026-11-18 — M2.9-V: IEC 61010-2-030 edition verified

PR #8 document `M2.9-V-IEC-61010-2-030-EDITION-AND-MEASURING-CIRCUIT-SCOPE-2026-11-18.md`, commit `5669534c9efc31611832155e46fb130cf58c7f15`. IEC catalogue verifies IEC 61010-2-030:2023 and scope for measurement circuits connected to external circuits. Strong applicability candidate with IEC 61010-1 if TestStation is standalone test/measurement equipment. IEC 61010-1:2010+AMD1:2016 consolidated and IEC 60664-1:2020+AMD1:2025 consolidated identified as candidate texts. Product boundary, EN/national adoption and CAT/transient/installation assumptions remain open; no standards compliance claim.


### 2026-11-18 — M2.9-W: AMC1311B supply path must preserve barrier

Official TI AMC1311 Rev C (June 2022) datasheet reviewed; PR #8 document `M2.9-W-AMC1311B-REINFORCED-BARRIER-AND-HIGH-SIDE-SUPPLY-REQUIREMENTS-2026-11-18.md`, commit `b22b56ea2a09e6cd8d9aadb6fa1e3cd5ea89c57d`. AMC1311B reinforced barrier ratings include VIORM 2120 VPK, VIOWM 1500 VRMS AC / 2120 VDC, VIOTM 7000 VPK, VIMP 9800 VPK, VIOSM 12800 VPK, UL1577 5 kVRMS; DIN EN IEC 60747-17 certificate 40040142 and UL file E181974. Device ratings do not confer system ratings. Its floating VDD1/GND1 power path is another galvanic crossing and must preserve the final required protection level. MEE1 functional-insulation converter excluded. No converter MPN or system safety rating selected.


### 2026-11-18 — PR workflow reset and M2.9-X

The VAZÃO EVSE Platform PR process was reset to enforce one open work PR at a time. Product PR #2 (Charger Hardware V1), #7 (TestStation physical-symbol/footprint review) and #8 (TMCS1123 AFE study stacked on #7) are now **closed without merge**. Their branches and commits remain preserved; no branch deletion or production-main merge was performed. PR #7's latest known head `9b5775d8c83e9852377f92e12b09011a7fec281e` had both workflows complete successfully: physical symbol migration run #43440733631 and verified symbol library run #43440733694. Despite CI success, PR #7 was not suitable for merge because the documented pin-to-net/connectivity and safety review gates remain open, and its scope was too broad (91 commits / 30 files). PR #8 remains a preserved stacked study branch, not integrated.

A new single-scope Draft PR #9 is now the only open PR:
https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/9
Branch: `review/teststation-amc1311b-isolation-crossing-matrix`
Head: `cb74a6d57d10cf0afd2be842d1f90c6a1734ec4a`
Base: `main`
One file, documentation-only, 91 additions:
`hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-X-AMC1311B-ISOLATION-CROSSING-INVENTORY-AND-REVIEW-MATRIX-2026-11-18.md`

M2.9-X records the six AMC1311B U3–U8 signal barriers and the corresponding floating high-side supply crossings, marks exact nets and converter assignments as not established by the actual MASTER netlist, and lists possible bypass paths through USB/debug, Ethernet, sensor returns, service connectors, PE/chassis and auxiliary supplies. It defines evidence required before any converter selection or insulation approval. It does not choose independent vs grouped high-side domains, assign nets, select an MPN, or claim a system insulation rating. No production MASTER, BOM, netlist, pin-to-net mapping, PCB, firmware or test procedure changed.

PR #9 was fetched back and verified. GitHub reports it open, Draft, mergeable=true, with one commit and one changed file. No workflow runs were returned for its documentation-only head; therefore no CI pass is claimed. Current PR states verified individually: #2 closed/unmerged, #7 closed/unmerged, #8 closed/unmerged, #9 open/unmerged. This restores exactly one open work PR. Continue with small, focused PRs; do not merge until the scope-specific review and required checks are satisfied.


### 2026-11-19 — M2.9-Y high-side power-domain architecture comparison

PR #9 remains the single open Draft work PR. Added M2.9-Y, documentation-only, on branch `review/teststation-amc1311b-isolation-crossing-matrix`, commit `382e95f1b587f90bfbdaa5eeb8e2eb28dddde4fa`, file `hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-Y-AMC1311B-HIGH-SIDE-POWER-DOMAIN-ARCHITECTURE-COMPARISON-2026-11-19.md`. The comparison evaluates (A) six independent floating supplies, (B) grouped domains (two groups of three only as illustrative example), and (C) one common high-side domain. It distinguishes six measurement channels, six signal barriers, power-island count, and all galvanic crossings. A is the conservative reference for evaluating independent fault containment, not an approved architecture. Grouping/common supply remain conditional on measurement references, sensor wiring, common-mode conditions, channel coupling, fault containment and standard-derived protection requirements. No architecture, MPN, CAT/insulation rating, clearance, creepage or safety claim approved. Production MASTER/BOM/netlist/pin map/PCB/firmware/test procedures untouched. Fetch-back confirmed doc content (blob `743b903e0a72cc0bff36655b00921651e27c1d59`). No PR-triggered workflow runs were returned for commit; no CI pass claimed. PR #9 metadata currently open, Draft, two commits, two files, 190 additions; GitHub's mergeable field is currently false, so do not attempt merge. Review pending.


### 2026-11-19 — PR #9 merged; single-PR cycle continued with #11

PR #9 was reviewed as a documentation-only change (M2.9-X isolation crossing inventory and M2.9-Y high-side domain architecture comparison). GitHub initially refused merge because the PR was Draft; it was marked Ready after review and then successfully squash-merged. Merge commit: `8f7e8964d0252132eac0be8c9ed60e37c98c5c71`. No executable tests apply to these docs; no workflow runs were returned, and CI is not claimed. Production electrical files remain unchanged.

Immediately after merge, created branch `review/teststation-amc1311b-channel-measurement-intent-matrix` from main and opened PR #11 as the sole open Draft PR: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/11. Head `1ea4fa9980b46d3cd941f104074e3b7a5a5694ac`; one commit, one file, 84 additions. M2.9-Z captures the required measurement intent, exact nodes/polarity, references/returns, voltage/transient environment, common-mode, isolation/fault containment, accuracy/bandwidth and interface data for U3–U8. All channel functions and assignments remain explicitly OPEN because actual MASTER netlist does not establish them. File fetched back and inspected (blob `af03819bcca7ec7ad5bda4f99b359a1af74f04aa`). No workflow runs returned for the commit. PR #11 is Draft, mergeable currently false, and review/checks pending. No production MASTER/BOM/netlist/PCB/firmware/test procedure changes; no fabrication/energization. Rule continues: exactly one open work PR; merge only reviewed scope with required checks; if blocked preserve branch and close without merge; then create the next focused branch/PR.


### 2026-11-19 — M2.9-Z source-intent recovery inside PR #11

Repository search recovered explicit source-declared legacy intent that was missing from the initial matrix: U3/U4/U5 = Zone A L1/L2/L3 voltage to ADC-A CH0/1/2; U6/U7/U8 = Zone B L1/L2/L3 voltage to ADC-B CH0/1/2. Legacy intended dedicated supply pairings U9→U3, U10→U4, U11→U5, U12→U6, U13→U7, U14→U8 are documented. This is **source intent only**; current native MASTER netlist still shows AMC pins disconnected. MEE1S2405SC is already excluded by M2.9-U from safety-isolation role; old supply pairing must not be implemented for that role. PR #11 document M2.9-Z was updated to distinguish source-intent from actual connectivity and safety approval, with file fetch-back verified (blob `b880549aae9176ca0e93409c349c64794b13c32a`). PR #11 head now `97dd97da9c66fd6eed883a7b1e5e8c93f584b612`, 2 commits, 1 file, 98 additions, still sole open Draft PR; mergeable currently false and no workflow runs returned. No CI pass claimed. No production electrical changes.


### 2026-11-20 — PR #11 merged and isolated-supply selection gate opened as PR #12

PR #11 M2.9-Z was reviewed and squash-merged documentation-only. Merge commit `e71bee3b9334267311d50a6b85bfda92ba7ce16e`. Source-declared functional intent recovered: U3/U4/U5 Zone A L1/L2/L3 voltage → ADC-A CH0/1/2; U6/U7/U8 Zone B L1/L2/L3 → ADC-B CH0/1/2. Intended old converter pairings U9–U14 one per channel remain source intent only; current MASTER netlist has no actual AMC pin connections. MEE1S2405SC excluded from safety-isolation use.

After merge, opened PR #12 as sole open Draft work PR, branch `review/teststation-isolated-supply-requirements-gate`, head `6170701ef290d5314f61beb626badb39e55309cc`, base main `e71bee3b9334267311d50a6b85bfda92ba7ce16e`. File M2.9-AA defines mandatory isolated DC/DC selection evidence: input envelope, output/load budget, continuous working voltage, impulse/transient, exact certification/scope/MPN, insulation conditions, creepage/clearance, capacitance/EMI, thermal derating, startup/fault behaviour, reliability/lifecycle. It explicitly selects no converter and makes no system safety claims. Document fetched back (blob `5878ecd602e82d259139d89fa285e1a5dc86f191`). PR #12 open Draft, 1 commit, 1 file, 96 additions, mergeable=true at last check; no workflow runs returned and no CI pass claimed. PRs #2/#7/#8 remain closed unmerged, branches preserved; #9 and #11 merged. Exactly one open work PR (#12). No production electrical files changed, no fabrication or energization.


### 2026-11-20 — PR #12 merged; preliminary converter screen in sole-open PR #13

PR #12 M2.9-AA isolated power selection requirements gate was reviewed and squash-merged. Merge commit `0c4450d508dbfd03ca22d16598befe37013a8686`. Documentation only; no executable tests applicable and no workflows returned.

Opened PR #13, branch `review/teststation-isolated-dcdc-candidate-screening`, head `1c80737dfcba8fd5bb4205ead4e5c0ca7d81d45c`, base main `0c4450d508dbfd03ca22d16598befe37013a8686`. Document M2.9-AB preliminarily screens manufacturer sources for 24V-input/5V-output converters, explicitly search assumptions only. RECOM R24P05S/P/X2/R6.4 retained as a candidate for exact datasheet/certificate review, not approved; it is 1W/200mA nominal, with reinforced-series EN/IEC61010 listing, /P short-circuit protection and /X2 clearance option per manufacturer. Crucial caveat: 6.4kVDC/1s is test voltage, not continuous working voltage. Functional-isolation RTC2, lower-evidence ROE/NME examples and legacy MEE1 are screened out from safety barrier role. Source URLs recorded in doc. Document fetched back (blob `fc643fe812f5e6ddadd04cc8c7b2a88978a6f09f`). PR #13 sole open Draft, 1 commit, 1 file, 78 additions; mergeability false at last check, no workflow runs claimed. Exact system working voltage, transient/impulse, source range, AMC variant/load and certification scope remain unresolved. No electrical production files changed, no fabrication/energization.


### 2026-11-20 — PR #13 datasheet-level review added

Continued work in existing sole-open PR #13 (no second work PR). Retrieved exact current RECOM manufacturer product pages and linked RxxPxx/R datasheet, Rev. 6/2020, and updated M2.9-AB with exact evidence and cautions. New document commit 9da1ca379548db56ee4d4abbefc1dd18ad0a876e; head now 2 commits, 1 file, 101 additions. Fetch-back verified.

Datasheet review recorded: input nominal ±10% (24V case 21.6–26.4V); 5V/200mA/1W; ±5% output accuracy; 15% typical load regulation (10–100% for 5V); 200mVp-p ripple/noise; specifications may not be met below 10% load despite minimum load 0%; 6.4kVDC/1s and 3.2kVAC/60s tests; reinforced grade, 2MOPP at 34Vrms; >4.8mm internal/external creepage/clearance in datasheet, product page claims >9mm input-output for /X2; isolation capacitance 4–10pF, leakage <0.01µA, 65kV/µs common-mode dv/dt claim; PD2, altitude 3000m, temperature/derating limits. Exact /X2 pinout differs: pin 1 +Vin, 2 -Vin, 5 NC, 6 -Vout, 7 +Vout. Ordering-code sequence in datasheet examples (R24P05S/R6.4/P/X2) differs from product-page naming (R24P05S/P/X2/R6.4), must resolve exact order code with manufacturer/distributor before any BOM/footprint work. EN/IEC61010-1 listing/report cited as 2010 edition; applicability/current edition requires review. Mandatory new gate: datasheet states product not authorized for safety-critical applications without explicit written RECOM consent; written manufacturer confirmation for intended TestStation use is required. Still no continuous rated working voltage evidence adequate for this system, and exact standards/system insulation requirements remain OPEN. No converter selected/approved. No BOM, MASTER, netlist, PCB, firmware, procedure or safety classification changes; no fabrication/energization.

PR #13 updated body with these boundaries; refreshed GitHub metadata reports mergeable=true, still Draft and sole open PR. 2 commits, 1 file, 101 additions. No workflow runs returned; no CI pass claimed. PR #13 must not merge until technical scope reviewed and unresolved mandatory gates appropriately documented; current status remains candidate screening only. Manufacturer sources: RECOM product pages and linked datasheet. These component values are not system approval.


### 2026-11-20 — PR #13 secondary 2 W candidate screened

Within the same PR #13 and existing M2.9-AB document, added a secondary RECOM RxxP2xx 2 W family candidate: R24P205S/P/X2/R6.4 (product-page code sequence), manufacturer published 24 V input, 5 V output, 400 mA/2 W, /P continuous SCP, /X2 >9 mm input-output clearance and 6.4 kVDC test option. Exact order code and datasheet conditions require confirmation. This candidate could offer power-budget headroom versus the 1 W example but remains unregulated and not selected. Same mandatory gates apply, including written RECOM authorization for safety-critical use, continuous working voltage, system insulation requirements, transient/input, actual AMC/load, certificate scope, pinout, layout/thermal/EMC. Added manufacturer product and family datasheet links. Document commit 4c936842e6e2b484eb783930c036771ca37de293; fetched back and verified. PR #13 now 3 commits, 1 file, 114 additions, Draft, sole open work PR. Latest metadata says mergeable=true after refresh; no workflows found/no tests claimed. No production circuit changes or fabrication/energization.


### 2026-11-20 — PR #13 AMC1311B supply load-budget finding

Added TI AMC1311B Rev C high-side supply-current data to M2.9-AB and performed arithmetic estimate. AMC1311B VDD1 is 3.0–5.5V; at 4.5–5.5V, IDD1 7.1mA typical / 9.7mA max. Nominal 5V rail power estimate 35.5mW typical / 48.5mW max per device; six channels 213mW / 291mW before ancillary loads. Important RECOM RxxPxx/R 1W unregulated datasheet states specs may not be met below 10% load; 1W 5V module 10% threshold is 20mA. AMC1311B alone draws below this. 2W candidate 10% threshold is 40mA, also above AMC-only consumption. Therefore neither candidate is assumed to regulate/specify correctly at actual load; validated minimum-load strategy or regulated alternative may be needed. No dummy load proposed or circuit changes authorized. Document commit fd4ee06520b3d7253cdcc1c44cd55a2f2d8d337a; fetched back verified. PR #13 now 4 commits, 1 file, 127 additions, Draft, sole open PR. Latest metadata mergeable=true after refresh; this can fluctuate and does not equal approval. No workflow runs found; no CI claim. No BOM/MASTER/netlist/PCB/firmware/test procedure changes, fabrication or energization.
