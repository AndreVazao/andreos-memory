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


### 2026-11-21 — PR #13 regulated alternative screening

Continued the sole work PR #13 without opening another PR. Added M2.9-AB section 12 after manufacturer-source screening. RECOM REC3A-2405SW/H2 is documented only as a regulated/no-minimum-load electrical comparator: 18–36V input, 5V/600mA, 3W, DIP24, 2kV isolation figure, UL60950-1 listing. The manufacturer page confirms regulated output and no minimum load, but the available evidence does not establish IEC 61010-1 approval, reinforced insulation, or an adequate continuous working-voltage/impulse rating for the TestStation. It is therefore not accepted as a safety barrier and is not selected. RECOM RSE-2405S/H2 was also checked: although regulated with 0% minimum load, its datasheet explicitly says insulation grade is functional, so it is rejected for barrier use. This establishes that regulation/no-minimum-load and safety insulation are separate acceptance gates.

Clarified that AMC1311B 7.1–9.7mA is IC-only current: the actual MASTER still has U3–U8 disconnected and the full high-side divider/filter/protection network is not implemented as a connected circuit. No divider current may be inferred without a defined circuit and component values. Complete per-channel rail budget remains open.

PR #13 head now cc23b6f16314906708ee961380ec5616d5daa693; 5 commits, 1 changed file, 156 additions, 0 deletions; Draft, Open, sole work PR. Document section 12 fetched back and verified. No workflow runs returned; documentation-only, no executable tests or CI pass claimed. API currently reports mergeable=true, but PR remains Draft and must not merge until safety/evidence review is closed. No BOM/MASTER/netlist/footprint/PCB/firmware/test procedure or safety classification changes; no fabrication or energization.


### 2026-11-21 — PR #13 RHV2 high-isolation IEC 61010 candidate

Further manufacturer datasheet review found RECOM RHV2-2405S/R20 (RHV2 Rev. 1/2022), a 2W 24V-to-5V unregulated module. Unlike prior regulated REC3A comparator, RHV2 datasheet lists reinforced insulation, rated working voltage 1400Vrms, 20kVDC/1s and 12.5kVAC/1min test values, isolation capacitance 3.5pF typical/4pF max, >30mm pin separation, PD2, altitude 5000m, and IEC/EN 61010-1:2010 plus IEC/EN 62368-1:2014 2nd edition. Exact manufacturer datasheet and product page links recorded in M2.9-AB section 13.

Critical limitations: unregulated output; minimum load listed 0%, but manufacturer explicitly warns specs may not be met below 10%. For 2W/5V/400mA, this is 40mA. AMC1311B IC alone is 7.1mA typical/9.7mA max at 4.5–5.5V; complete high-side load unknown because U3–U8 and ancillary circuits remain disconnected in MASTER. Datasheet says explicit RECOM written consent is required for safety-critical use. 1400Vrms is a component working-voltage rating, not system approval. Current IEC 61010 edition/amendments, report/certificate scope, input/transient, measurement category, system insulation coordination, low-load rail tolerance, thermal/EMI, footprint and exact MPN still open. RHV2 is the strongest documentary candidate found so far, but not selected or approved.

PR #13 remains sole open Draft PR, 6 commits, 1 file, 193 additions, 0 deletions; head 92c250bd88f71ad0914b9c7b59f426c99f7e1d39. Section 13 fetched back and verified. No workflows returned; no CI/test pass claimed. No BOM/MASTER/netlist/PCB/firmware/test procedure changes, fabrication or energization. Memory checkpoint is separate from EVSE product PR.


### 2026-11-21 — PR #13 RHV2 low-load mitigation analysis

Continued the single VAZÃO EVSE work PR #13; no parallel PR opened. Added section 14 to M2.9-AB, analysing RHV2-2405S/R20 with a post-regulator and hypothetical preload. Core finding: a downstream LDO does not cure RHV2's <10% load specification concern; the converter sees the LDO input current plus its quiescent current, which may remain below the 40mA threshold. A preload could force a higher operating load but introduces real per-channel dissipation and does not improve regulation accuracy. Illustrative 100Ω preload arithmetic only: 42.5mA / 0.181W at 4.25V; 50mA / 0.25W at 5V; 57.5mA / 0.331W at 5.75V. Across six channels this is about 1.09W / 1.50W / 1.99W respectively, before converter losses and AMC loads. These are examples, not a selected resistor or verified RHV2 output range.

RHV2 + preload + LDO remains unproven because output headroom, output tolerance/load regulation, LDO dropout, stability, startup, fault and thermal behaviour are unresolved. Further manufacturer-oriented search did not return an exact low-power regulated/no-minimum-load candidate with adequate IEC 61010-1/reinforced-insulation evidence; a Vicor Micro family surfaced but insufficient evidence for exact 5V low-power model and IEC 61010 scope, so it was not shortlisted. This does not prove no suitable product exists.

Updated engineering direction: prefer a regulated isolated converter with exact IEC 61010-1 certificate scope, reinforced insulation, sufficient rated working voltage and documented no-minimum-load operation. Complete channel load budget still blocked by disconnected U3–U8 and unimplemented/unknown divider/filter/protection network in MASTER. No converter selected; no preload selected; no post-regulator topology approved. No MASTER/BOM/netlist/footprint/PCB/firmware/test procedure or safety classification changes; no fabrication/energization.

EVSE PR #13 head: 4a39f854d482fdc5bec2d4028f928c0ef41d0947; 7 commits, 1 file, 240 additions, 0 deletions; Open, Draft, sole work PR. Latest metadata reports mergeable=false (earlier true); this is not interpreted as a confirmed conflict without further refresh/compare. No workflow runs returned for this head; no CI pass claimed. Documentation-only update was fetched back and verified. PR remains unmerged pending technical/safety gates.

### 2026-11-21 — PR #13 regulated TRACO comparator screen

Continued the single VAZÃO EVSE work PR #13. Added section 15 to M2.9-AB after reviewing official TRACO manufacturer datasheets. New evidence:
- TRACO TCL-024-105 DC: 18–75 VDC input, regulated 5 V/5 A, 0–100% load regulation 0.5% max, ripple <50 mVpp, and IEC/EN 61010-1 plus IEC/EN 61010-2-201 listed. However the reviewed datasheet states only 1500 VDC input/output isolation test for 60 s and does not establish reinforced insulation or rated continuous working voltage. It is one common DIN-rail output and cannot by itself supply six independent floating domains. Not accepted as a barrier candidate.
- TRACO TMDC 06-2411: 9–36 VDC input (24 V nominal), regulated 5.1 V/1.2 A, no minimum load, 0.5% max load regulation over 0–100%, 75 mVpp typical ripple. The manufacturer datasheet explicitly classifies its insulation system as functional and lists IEC/EN/UL 62368-1 approvals; 3000 VDC/60 s is only a test voltage and does not override the functional-insulation classification. Rejected for safety barrier role.
- These examples reinforce that no-minimum-load regulation and an IEC standard listing do not prove reinforced insulation or an adequate working-voltage rating. No exact small-power 24V-to-5V candidate yet meets all required gates: regulated, guaranteed no-minimum-load, IEC 61010-1 certificate scope, reinforced insulation, adequate rated working voltage and manufacturer approval for intended safety-critical use. This is not proof that none exists.

PR #13 latest head 1740facc9b063993e17282e875e7ced8979cb9b5; 8 commits, one documentation file, 274 additions, zero deletions. Compare main to branch: ahead 8, behind 0, one added file. PR remains Open/Draft/unmerged. PR metadata reports mergeable=false despite clean compare and zero behind; treat as unresolved metadata/conflict signal and do not merge. Combined commit status has no status checks; no PR-triggered workflow runs returned. No CI pass claimed. Latest file fetched back and verified (blob 44f201808daa0b59b7de4ad2e32c3f1a9347abc5). No MASTER/BOM/netlist/PCB/firmware/test procedure changes, no converter selection, no fabrication or energization.


### 2026-11-22 — recuperação de divergência Git da PR #13

Foi detetado que o commit documental `be2c70f8dfa9294f2dba6d0e890b68c3b3bc3b36` (mensagem `docs(teststation): compare isolated power architecture paths`) foi publicado em `main`, quando o destino pretendido era a branch da PR #13. O commit contém o documento M2.9-AB completo, incluindo a secção 16 de alternativas de arquitetura; não alterou MASTER, BOM, netlist, PCB, firmware ou procedimentos.

Auditoria comparativa confirmou que o ficheiro na branch antiga da PR #13 (275 linhas) é um prefixo exato, linha a linha, do ficheiro em `main` (309 linhas). Logo, todo o conteúdo da PR estava já presente em `main`; não existia conteúdo exclusivo para integrar. A PR #13 foi fechada como redundante, sem merge, sem reescrita de histórico e sem force-push. O commit em `main` foi preservado.

Foi criada a branch limpa `work/teststation-isolated-power-requirements-gate` diretamente a partir de `main` para o próximo ciclo. No checkpoint, não foi aberta nova PR nem alegada validação CI. Estado correto: zero PRs de trabalho abertas; branch nova preparada. A regra mantém-se: uma PR de cada vez, alterações pequenas, revisão e verificações reais antes de merge. A ocorrência deve permanecer registada; não ocultar nem classificar o commit acidental como merge aprovado.


### 2026-11-22 — M2.9-AC matriz de requisitos das seis alimentações isoladas

Na branch limpa work/teststation-isolated-power-requirements-gate, criada a partir de main, foi acrescentado o documento hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-AC-SIX-CHANNEL-ISOLATED-POWER-REQUIREMENTS-MATRIX-2026-11-22.md (152 linhas, documentação apenas). Commit: a0f946c8ad5e5c5fb9adda6ff369fac99c823321. Ficheiro recuperado do GitHub e conteúdo verificado (blob e497428b95692259b0a05e45081ff4b775ef19c2). Compare confirmado: branch 1 commit à frente de main, 0 atrás, apenas um ficheiro novo.

A matriz separa requisitos sistémicos ainda OPEN (uso previsto, normas/edições, categoria de medição/OVC, tensão de trabalho, transitórios/impulso, isolamento, poluição/altitude, interfaces e falhas) dos requisitos de circuito e fornecedor. Mantém U3–U8 individualizados e sem inventar cargas, porque o MASTER/netlist conhecido não demonstrou ainda as redes completas ligadas. Define gates de MPN exato, comportamento a carga leve, tensão de trabalho, impulso, isolamento/certificados, creepage/clearance, parasitas, EMC, térmica, falhas e restrições do fabricante; inclui revisão de todos os caminhos galvânicos e sequência de fecho.

Aberta PR #14: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/14 — TestStation V1: define six-channel isolated power requirements matrix. É a única PR de trabalho aberta neste ciclo, com um commit, um ficheiro e 152 adições. A verificação de conteúdo e compare passou. O combined status não devolveu checks e não foram devolvidos workflow runs para o commit; portanto não declarar CI verde. A metadata inicial da PR reportou mergeable=false; não fazer merge enquanto esse estado não for reavaliado e não houver evidência suficiente. PR aberta, não merged.

Próxima ação técnica indicada no próprio documento: recuperar/auditar os ficheiros nativos KiCad MASTER, símbolos, footprints, projeto e netlist para estabelecer o estado real dos seis canais e respetivas redes high-side. Não fabricar esquemas em texto nem inferir cargas. Nenhuma alteração a MASTER, BOM, netlist, footprint, PCB, firmware, procedimento de teste ou classificação de segurança; sem seleção de conversor, fabrico ou energização.


### 2026-11-22 — Merge M2.9-AC e descoberta do MASTER nativo; PR #15

PR #14 (M2.9-AC) foi reavaliada: GitHub REST confirmou `mergeable=true`, `mergeable_state=clean`, sem reviews nem workflow runs. Sendo documentação focada, sem alterações de hardware e com conteúdo verificado, foi merged por squash. Merge commit: `4b22e2a0b2af3a59c7f2d82cc63ec0dcfea9c2e8`. Não se declara CI verde.

Auditoria seguinte confirmou que o esquema nativo existe: `hardware/teststation/V1/CAD/schematics/TS-V1-M2.9-K-MASTER.kicad_sch`, blob `3a75a000077a5acd208b5905a345a5e44aa78720`, 79,604 bytes, 4,708 linhas raw, KiCad schema 20260306 / eeschema 10.0, title-block revision M2.9-L.2, ERC/DRC pendentes. Foram confirmadas seis instâncias AMC1311BDWVR U3–U8 e coordenadas na fonte. A presença das instâncias não valida conectividade, nomes de nets, independência das ilhas, cargas nem isolamento. Não foi executado KiCad CLI, ERC, DRC ou exportação de netlist nesta sessão.

Nova branch `work/teststation-native-master-audit`, commit `1f82f2fab341551b9b7c58c0431eefe39c665c26`, documento M2.9-AD (60 linhas), recuperado do GitHub e verificado. Compare: 1 commit à frente, 0 atrás, apenas um ficheiro adicionado. PR #15 aberta: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/15 — “TestStation V1: audit native MASTER schematic evidence”. PR criada; mergeability inicial false (requer refresh/reavaliação); não há CI claim.

Próximo passo: obter ambiente KiCad 10 ou exportação verificada de netlist/ERC, mapear pin-to-net U3–U8, identificar circuitos high-side exatos e cargas com evidência; manter decisões de arquitetura, BOM, PCB, energização e certificação bloqueadas até auditoria.


### 2026-11-22 — PR #15 merged; M2.9-AE histórico de netlist e risco do workflow

PR #15 (M2.9-AD native MASTER discovery) foi merged por squash após reavaliação de `mergeable=true`. Merge commit: `015c6a24d89818107fddd97def38750139658078`. PR #15: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/15.

A auditoria aprofundada encontrou artefactos KiCad históricos já versionados: XML `M2.9-K-MASTER.net`, CSV `M2.9-K-PIN-TO-NET-MATRIX.csv`, ERC report e relatórios associados. O XML identifica Eeschema 10.0.6 e data 2026-10-16 13:49:15; não está demonstrado que corresponda exatamente ao blob atual do MASTER, portanto é evidência histórica, não validação do HEAD atual.

No CSV histórico, todas as oito pins de cada AMC1311BDWVR U3–U8 aparecem como nets individuais unconnected. Os seis MEE1S2405SC U9–U14 também não têm circuitos completos: apenas VIN+ de U10 (/ISO5_A1), U11 (/ISO5_A2), U13 (/ISO5_B1) e U14 (/ISO5_B2) surgem como labels single-node; U9/U12 VIN+ e os pins 2/3/4 de todos os seis estão unconnected. Logo, estes artefactos não demonstram seis alimentações isoladas funcionais. O mesmo export histórico regista 24 componentes, 165 nets, três nets multi-node suspeitas U19/U2 e ERC com 353 mensagens (300 errors, 53 warnings). O relatório M2.9-AE documenta os resultados e exige regeneração atual antes de qualquer conclusão sobre HEAD.

A inspeção do workflow `.github/workflows/teststation-m2.9-k-kicad-native.yml` revelou um risco importante: o job remove o MASTER nativo e recria-o importando o esquema legacy, depois corre ERC/netlist e tem permissões de escrita/commit. Não o executar por dispatch/trigger sem primeiro rever o seu comportamento, pois pode substituir o MASTER nativo atual por uma conversão legacy. A validação atual-head tem de ser desenhada de forma não destrutiva (checkout/branch isolada, cópia temporária, sem push automático para main) e referenciar o SHA exato.

Nova branch `work/teststation-isolated-netlist-evidence`, commit `30de64ce51f0c090068af90f3b285dc33ea4f064`; documento M2.9-AE (79 linhas) recuperado e verificado. Compare: 1 commit ahead, 0 behind, um ficheiro novo. PR #16 aberta: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/16 — “TestStation V1: document historical isolated-channel netlist evidence”. Mergeability inicial false; manter aberta até refresh/review. Nenhum current-head KiCad/ERC/netlist/DRC ou CI verde alegado.

### 2026-11-22 — PR #16 merged; first fresh KiCad audit of current MASTER; PR #17

PR #16 (M2.9-AE historical netlist evidence) foi merged por squash após atualização do estado GitHub: mergeable=true, branch 1 commit ahead / 0 behind, CodeRabbit concluiu a revisão sem comentários acionáveis. Merge commit em main: d79a421c9c722c6e4f28cfc27cffd248233b1bfe. A regra de uma PR TestStation ativa foi preservada.

Foi executada uma validação KiCad 10.0.8 sobre o conteúdo do MASTER atualmente integrado, através do workflow existente .github/workflows/validate-evse-symbol-library.yml, run #45066094391:
https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/45066094391

O run fez checkout do commit 015c6a24d89818107fddd97def38750139658078 (main imediatamente antes do merge documental da PR #16). O MASTER foi novamente obtido de main já no commit d79a421c9c722c6e4f28cfc27cffd248233b1bfe; o blob permaneceu idêntico em ambos: 3a75a000077a5acd208b5905a345a5e44aa78720. Assim, a execução representa exatamente os mesmos bytes do MASTER atual, embora o SHA do commit de checkout seja o pai do merge documental.

A execução confirmou:
- KiCad CLI 10.0.8.
- Static symbol regression checks SUCCESS (62 linhas únicas de pinos; mapas esperados validados para ADS131M06IPBSR, AMC1311BDWVR, TMCS1123A3AQDVGR, MEE1S2405SC e ISO1044BDWR).
- KiCad SVG export/load SUCCESS para os cinco símbolos.
- ERC report e XML netlist exportados; auditoria de netlist e triagem ERC concluídas.
- Artifact evse-master-erc-netlist-45066094391, ID 14771257730, SHA-256 6a44e9158c045f6553fb05e8f798fb317ee9663c4011e056a68ae7ab7f9f56d2, retenção até 2026-12-22.

Resultado elétrico atual reproduzido:
- ERC: 353 mensagens, 300 erros, 53 avisos; erros: 32 label_dangling, 151 pin_not_connected, 50 pin_not_driven, 1 pin_to_pin, 66 power_pin_not_driven; avisos: 11 isolated_pin_label, 24 lib_symbol_issues, 18 unconnected_wire_endpoint.
- Netlist: 24 componentes, 165 nets, 3 nets multi-node; as três ligações suspeitas U19/U2 permanecem (U19.3↔U2.17, U19.2↔U2.20, U19.8↔U2.19); estado BLOCKED_KNOWN_SUSPICIOUS_CONNECTIONS.
- U3–U8 AMC1311BDWVR: todas as oito pins de cada instância aparecem como nets individuais unconnected no export atual.
- U9–U14 MEE1S2405SC: U9 e U12 têm os quatro pins unconnected; U10/U11/U13/U14 têm VIN+ em labels single-node /ISO5_A1, /ISO5_A2, /ISO5_B1, /ISO5_B2, enquanto VIN−/VOUT−/VOUT+ continuam unconnected em todos os seis conversores.

O pipeline terminou SUCCESS, mas isso significa que a análise foi executada; não significa ERC limpo nem aprovação elétrica. Nenhum MASTER, BOM, PCB, firmware ou safety classification foi alterado.

A análise identificou que o workflow existente tem contents: read e issues: write (a permissão de issues serve para publicar resultado na issue de controlo #3); não possui contents: write. O workflow perigoso teststation-m2.9-k-kicad-native.yml continua proibido de executar porque remove/substitui o MASTER nativo a partir do esquema legacy e faz push.

Nova branch limpa work/teststation-readonly-master-audit criada a partir de main d79a421c9c722c6e4f28cfc27cffd248233b1bfe. PR #17 aberta:
https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/17
Commit head: fc45db18de5796df0e928230148a1f5c767f46f9. Dois ficheiros adicionados:
- .github/workflows/teststation-master-readonly-audit.yml: workflow manual com SHA de commit obrigatório, checkout exato, Git blob SHA e SHA-256, cópia temporária do MASTER, ERC/netlist/auditorias, confirmação de integridade da origem, artefactos e permissões contents: read exclusivamente; sem comments, commit, push ou mutação do esquema.
- M2.9-AF-FRESH-MASTER-KICAD-AUDIT-2026-11-22.md: regista a execução fresca e os resultados elétricos acima, com a limitação exata de proveniência do commit.

PR #17 é a única PR TestStation aberta, 2 commits / 2 ficheiros, compare 2 ahead / 0 behind. GitHub reporta mergeable=true após refresh, mas ainda não há workflows/checks associados ao head porque o workflow novo é workflow_dispatch e só poderá ser executado depois de integrado. CodeRabbit não fez revisão: respondeu que o repositório tem menos de 10 estrelas e exige acionar manualmente Trigger review; o comando @coderabbitai review sozinho foi ignorado. PR #17 não merged. Próximo gate: revisão manual/CodeRabbit quando acionável, revisão da lógica do workflow, merge seguro e primeira execução manual com o SHA exato de main. Não afirmar CI verde para o workflow novo.

Nenhuma aprovação de ligação elétrica, isolamento, seleção de conversor, footprint, fabrico, certificação ou energização. Continuar a exigir revisão de manufacturer pin maps e intenção de circuito antes de resolver as ligações suspeitas U19/U2.


### 2026-11-22 — revisão técnica adicional da PR #17 e correção de SHA

Foi revista integralmente a PR #17 e os quatro scripts/workflows relacionados. O novo workflow read-only reutiliza os mesmos comandos de instalação do KiCad 10, exportação SVG e execução das ferramentas de validação da pipeline existente já executada com sucesso em Ubuntu 24.04. O workflow novo mantém `permissions: contents: read`, trabalha sobre cópia temporária do MASTER, verifica SHA/blob e SHA-256 e não contém permissões nem comandos de commit/push.

A revisão detetou uma inconsistência de normalização: a validação aceitava SHA hexadecimal em maiúsculas, mas a comparação posterior era sensível a maiúsculas/minúsculas. Corrigido na branch da PR #17 com `TARGET_SHA="${TARGET_SHA,,}"` imediatamente após a validação do formato. Commit: `779dded87f786006e36df829c396bb64294d3751`; blob do workflow confirmado: `c4271b864fe35beb1bd89ec1975d9bba78ef2e72`.

Estado após atualização: PR #17 continua Open e é a única PR TestStation ativa; head `779dded87f786006e36df829c396bb64294d3751`; compare `main...work/teststation-readonly-master-audit` = 3 commits ahead / 0 behind, dois ficheiros adicionados. Combined status vazio, sem workflow runs no head e sem reviews formais. GitHub reportou temporariamente `mergeable=false`, apesar do compare limpo; não assumir conflito nem mergeabilidade até novo refresh. A PR não foi aprovada nem merged. O workflow manual só pode ser testado depois de integrado na branch default; por isso não declarar CI verde nem execução do novo workflow. Próximo gate: resolver estado de mergeabilidade, obter validação/revisão suficiente e só então integrar; depois executar workflow manual no SHA exato de main e verificar artefactos.

Sem alterações ao MASTER, BOM, PCB, firmware ou classificação de segurança. O risco do workflow legacy que substitui o MASTER continua registado e a sua execução permanece proibida. Nenhuma aprovação de fabrico, certificação ou energização.


**Atualização de estado após refresh (2026-11-22):** a metadata da PR #17 voltou a `mergeable=true`; compare continua 3 ahead / 0 behind. Esta confirmação resolve apenas a dúvida de mergeabilidade Git, não substitui checks ou revisão. Combined status continua vazio, não existem workflow runs associados ao head e a lista de reviews formais permanece vazia. Manter a PR aberta até haver validação suficiente do workflow; não fazer merge nem declarar testes verdes nesta fase.


### 2026-11-23 — PR #17 merged; manual dispatch blocked by browser access

PR #17 was reviewed against its exact head and merged by squash with expected-head protection. Merge commit: `66354cd67556d5563779d02ec27f6fe0e60a8835`. The workflow is now on main and remains read-only (`contents: read`), exact-SHA checked, stages the MASTER copy in runner temp and uploads evidence. No MASTER/BOM/PCB/firmware change.

A manual dispatch was attempted for the new workflow on `main` with target SHA `66354cd67556d5563779d02ec27f6fe0e60a8835`, but the connected browser execution failed before interacting with GitHub because Browser Use reports insufficient credits. No workflow run was launched; this is a tooling limitation, not a workflow failure. GitHub MCP in this session has no workflow-dispatch operation. Next available dispatch method is GitHub Actions UI: Actions → “TestStation V1 read-only MASTER audit” → Run workflow → branch main → target_sha exact merge commit above. Do not use the dangerous legacy conversion workflow.

After merge, a fresh clean branch was created from main for the next review-only task: `work/teststation-u19-u2-cross-domain-review`. No new PR opened yet; preserve one-open-PR rule.


### 2026-11-23 — PR #19 M2.9-AG review of U19/U2 suspicious cross-domain nets

After PR #17 was merged, branch `work/teststation-u19-u2-cross-domain-review` was created from main. Review-only document M2.9-AG was committed as `9be4439d4f23e380d5e9367b8b68e4270e5b5a60` and PR #19 opened: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/19. Compare is 1 ahead / 0 behind, one file, 49 additions. PR #19 is sole open TestStation PR. Initial GitHub metadata says mergeable=false; refresh/compare before deciding, do not merge without sufficient review.

M2.9-AG records the native symbol functions for the three current netlist connections: U19 TMCS1123 pin 3 GND ↔ U2 ADS131M06 pin17 CS; U19 pin2 IN− ↔ U2 pin20 DOUT; U19 pin8 VS ↔ U2 pin19 SCLK. This documents the suspicious function pairs but is not a diagnosis or repair. Manufacturer pin maps, exact footprint/package, intended topology, native geometry endpoints and current netlist need independent cross-check before any schematic change. No MASTER/BOM/PCB/firmware/footprint or safety classification change.

PR #17 merge was verified at `66354cd67556d5563779d02ec27f6fe0e60a8835`. Manual dispatch of the new read-only workflow remains blocked: Browser Use cloud has insufficient credits; GitHub MCP lacks workflow dispatch. No run was launched. The exact target SHA is the merge commit; dispatch only through the workflow UI on main and never run the dangerous legacy conversion workflow.


### 2026-11-23 — PR #19 merged; manufacturer pin functions verified; footprint mapping blocked

PR #19 (`https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/19`) was expanded with official Texas Instruments datasheet evidence and a read-only audit of native MASTER/PCB placeholder artifacts. Latest GitHub REST refresh confirmed state open, `mergeable=true`, `mergeable_state=clean`, exact head `efd0de99f7380e3c4856622f7c53aea5d2cab3a1`, base `66354cd67556d5563779d02ec27f6fe0e60a8835`. PR merged by squash with expected-head protection: merge commit `33b1078fef36204b3a0493943dbfb20ad12c0508`.

Official TI sources confirm exact manufacturer pin functions: TMCS1123A3AQDVGR (DVG 10-pin SOIC): pin 2 IN−, pin 3 GND, pin 8 VS; ADS131M06IPBSR (PBS 32-pin TQFP): pin 17 CS, pin 19 SCLK, pin 20 DOUT. Thus all three netlist pairs join unlike named functions and remain suspicious; this is not by itself a diagnosis of wiring intent. Sources: https://www.ti.com/product/TMCS1123/part-details/TMCS1123A3AQDVGR ; https://www.ti.com/lit/ds/symlink/tmcs1123.pdf ; https://www.ti.com/product/ADS131M06/part-details/ADS131M06IPBSR ; https://www.ti.com/lit/ds/symlink/ads131m06.pdf.

Read-only MASTER inspection shows U2 and U19 both have empty Footprint properties. The PCB-A M2.9-C artifact is explicitly a COMPONENT FOOTPRINT PLACEHOLDERS file; its U2 project footprint has only pads 1 and 2, while its TMCS1123 placeholder refs are U13/U14 (not U19) and also only have pads 1 and 2. These are not valid production package footprints or independent symbol-to-pad mapping. Physical footprint/package and PCB connectivity therefore remain BLOCKED. No MASTER, BOM, PCB, firmware, footprint, safety classification, fabrication or energization change/approval.

PR #19 was merged because it is a reviewed documentation-only evidence record, not a circuit correction. New clean branch created from the merge commit: `work/teststation-u19-u2-topology-endpoint-audit`. It is the next work branch; no new PR opened yet. Next gate: inspect native KiCad geometry/wire/label endpoints and approved requirements/topology, determine whether U19/U2 nets are an intentional fixture or schematic mistake, and only then prepare a separate review patch if justified. Preserve one open TestStation PR at a time.


### 2026-11-23 — Native KiCad geometry confirms direct U19/U2 pin endpoint overlap; PR #20

Read-only parse of MASTER `hardware/teststation/V1/CAD/schematics/TS-V1-M2.9-K-MASTER.kicad_sch`, exact blob `3a75a000077a5acd208b5905a345a5e44aa78720`, confirmed three pairs of symbol pin endpoints occupy identical coordinates:
- U2.17 CS and U19.3 GND: `(190.50, 63.50)`
- U2.20 DOUT and U19.2 IN−: `(190.50, 55.88)`
- U2.19 SCLK and U19.8 VS: `(190.50, 60.96)`
U2 origin `(177.80,60.96)`, U19 origin `(203.20,58.42)`, both rotation 0. No wire segment endpoint or label anchor exists at the three coincident coordinates. Direct pin-endpoint contact explains netlist joins; it remains unresolved whether this was intentional direct pin-to-pin wiring or accidental symbol placement. No change to MASTER or electrical files.

Documented in PR #20: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/20. Branch `work/teststation-u19-u2-topology-endpoint-audit`, head `79aa2d1cbbaabd4ada3cda61dfcaaef3f9e83ba4`, base/main `33b1078fef36204b3a0493943dbfb20ad12c0508`, compare 1 ahead / 0 behind, one file, 23 additions, 0 deletions. REST refresh reports PR open, not merged, `mergeable=true`, `mergeable_state=clean`. Sole open TestStation PR; separate PR #18 is charger workstream and not part of this TestStation PR sequence.

Next gates: confirm intended measurement/control topology from approved design requirements and obtain production footprints/consistent PCB revision. Do not infer design intent from the coincident geometry; do not modify circuit until justified. PR #20 is documentation-only and has no CI/review evidence asserted. No fabrication, certification or energization approval.


### 2026-11-23 — PR #20 aprofundada: divergência entre MASTER e contrato elétrico U19-B2/ADC-B

A investigação prosseguiu na branch `work/teststation-u19-u2-topology-endpoint-audit`, mantendo a PR #20 como única PR ativa da TestStation. Foram consultados diretamente no `main` os contratos M2.9-J, M2.9-H, M2.9-E e o pacote de arquitetura M2.4.

A evidência documental confirma a intenção funcional:
- U2 = ADS131M06 ADC-B.
- U19 = TMCS1123-B2, corrente da fase L2 da Zona B.
- U19 deve alimentar ADC-B CH4/AIN4 através da saída VOUT e da rede analógica de entrada.
- M2.9-J atribui U19 a ADC-B CH4; M2.9-H descreve B_L2_I -> TMCS1123-B2 -> ADC-B AIN4; M2.4 descreve TMCS1123 OUT -> filtro analógico -> entrada diferencial ADS131M06.
- O MASTER tem, em simultâneo, três contactos diretos entre U19 e pinos SPI/terra/alimentação de U2: U19.3 GND ↔ U2.17 CS; U19.2 IN− ↔ U2.20 DOUT; U19.8 VS ↔ U2.19 SCLK. Isto contradiz a topologia funcional documentada. O mismatch de topologia está estabelecido relativamente ao contrato; não está estabelecida uma correção segura ou completa.

A secção 9 do relatório M2.9-AG foi acrescentada com esta comparação. Também se registou uma divergência adicional que necessita resolução: M2.9-J identifica TMCS1123 VS como 3V3_MEAS; M2.9-E usa SENSOR_5V_x; M2.4 indica faixa 3,0–5,5 V e baseline 3,3 V. Não escolher a alimentação por suposição.

Commit de atualização do relatório: `b23821fd4b0de2d268a6d740c590af575de7d663`; commit de alinhamento da disposição textual: `386e5ce1f4035379e53b4fb2f679edda0401af5b`. Relatório: `hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-AG-U19-U2-CROSS-DOMAIN-NET-REVIEW-2026-11-23.md`.

PR #20: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/20. Head `386e5ce1f4035379e53b4fb2f679edda0401af5b`; base/main `33b1078fef36204b3a0493943dbfb20ad12c0508`; compare 3 ahead / 0 behind; um ficheiro, 51 adições, zero remoções. PR continua aberta. REST refresh após update indicou mergeable=false/mergeable_state unknown; não interpretar como conflito confirmado. Não há reviews formais nem check runs (0). Não fazer merge enquanto a mergeability não for novamente confirmada e não houver revisão suficiente. O trabalho permanece documental e não modifica MASTER, esquemático, BOM, PCB, firmware, footprints ou classificação de segurança.

Gates ainda abertos: obter footprints reais e revisão PCB consistente para U2/U19; reconciliar filtro diferencial, polaridade, bias/referência, headroom e erro de fase; resolver alimentação oficial do TMCS1123; confirmar qual revisão de contrato é autoritativa. Sem aprovação de fabrico, certificação ou energização. Preservar a regra de uma PR TestStation ativa.


### 2026-11-23 — qualificação de evidência M2.9-L no relatório U19/U2

A leitura integral de `M2.9-L-INTENDED-INTERFACE-REGISTER.md` mostrou que as atribuições funcionais extraídas do legado são explicitamente classificadas como **source-declared functional intent — not yet pin-level approved**. O documento M2.9-L-REAL-ELECTRICAL-CONNECTIVITY-IMPLEMENTATION é um contrato de implementação, não uma aprovação final do esquema atual. Por rigor, o relatório e o texto da PR #20 foram corrigidos: o resultado é um mismatch confirmado entre MASTER e intenção funcional documentada, mas ainda requer confirmação/aprovação explícita de pin-level design antes de qualquer correção. Não chamar esta intenção de arquitetura aprovada.

A mesma leitura identificou M2.9-I como baseline adicional: TMCS1123 opera na faixa 3–5,5 V e especifica desacoplamento local de 100 nF + 1 µF, mas não resolve o rail nominal; M2.9-J e M2.4 apontam 3V3_MEAS, enquanto M2.9-E nomeia SENSOR_5V_x. A divergência permanece aberta.

Último commit da branch/PR #20: `325d340b3987e5ac42b0918d847d82422f3f251b`. PR continua aberta, documentação apenas, 4 commits na branch, um ficheiro alterado (52 adições, zero remoções). REST continua a devolver mergeable=false/estado desconhecido; sem reviews formais e sem check runs. Não fazer merge até refresh fiável de mergeability e revisão suficiente. MASTER, esquemático, BOM, PCB, firmware, footprints e segurança continuam inalterados.


### 2026-11-23 — PR #20 merged; PR #21 opened for six current-sensor paths

PR #20 `TestStation V1: audit direct U19/U2 pin endpoint overlap` was merged by squash after the latest GitHub refresh confirmed `mergeable=true`, `mergeable_state=clean`, and compare 5 ahead / 0 behind. CodeRabbit check was completed with conclusion `skipped` because manual review is required for this OSS repository; no formal reviews. This was a documentation-only change, self-reviewed; no electrical design or source CAD files changed. Merge commit: `847bf54ef7560dff29573a11323b7a84fca43133`.

Created clean branch `work/teststation-u19-u2-followup-interface-reconciliation` from that merge commit; initial compare to main was identical.

Further read-only parsing of the exact main netlist `hardware/teststation/V1/CAD/verification/netlist/M2.9-K-MASTER.net` (blob `99627d6676a53b69af2a9b8d3e6f23104c423a2f`) mapped all six TMCS1123 instances:
- U15/U16/U17/U18/U20: pins 1–4 and 6–8 unconnected in the exported model; pin 5 VREF connected to the corresponding `/A_L1_I_RET`, `/A_L2_I_RET`, `/A_L3_I_RET`, `/B_L1_I_RET`, `/B_L3_I_RET` nets.
- U19: pin 5 VREF to `/B_L2_I_RET`; pin 2 IN− to U2.20 DOUT; pin 3 GND to U2.17 CS; pin 8 VS to U2.19 SCLK; pins 1,4,6,7 unconnected.
- All six modeled VOUT pin 6 nets are unconnected. Therefore current exported netlist proves no TMCS1123 VOUT-to-ADC path for any channel.
- Existing cached MASTER TMCS1123 symbol models pins 1–8 only and omits physical pins 9 VOC and 10 NC. The physical cross-check already documents this. The cached ADC symbol also has a known physical pins 1–6 mapping defect. Do not trust its current channel assignments.
- VREF pin 5 mapped to I_RET nets may be intentional for differential measurement; do not call it wrong without approved interface matrix. M2.9-E names pin 5 CURRENT_VREF_x while J describes controlled reference net.
- M2.9-E names sensor VS SENSOR_5V_x; M2.9-J/M2.4 name 3V3_MEAS. TI 3–5.5 V operating range permits 3.3 V but does not resolve canonical project rail. Existing netlist has VS unconnected for five sensors and incorrectly joined for U19.
- Review-only footprint candidates for U2 and U19 were confirmed on separate branch `review/teststation-physical-symbol-migration`; they are not on main and are not assigned to MASTER/PCB-A. They remain non-production candidates. U2 has a KiCad API/CSV consistency check; U19 still requires independent drawing/CAD/render/physical review and system insulation coordination.

Created report `hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-AH-SIX-CHANNEL-TMCS1123-NETLIST-AUDIT-2026-11-23.md`, commit `808b7986e2ead0f0fc9c6f81f6bbd1491509a0be`. Opened PR #21: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/21. Branch `work/teststation-u19-u2-followup-interface-reconciliation`, head `808b7986e2ead0f0fc9c6f81f6bbd1491509a0be`, base `847bf54ef7560dff29573a11323b7a84fca43133`, 1 commit, 1 file, 83 additions, 0 deletions. PR open; no review/check evidence yet. Do not merge until fresh mergeability and review. No MASTER, schematic, BOM, PCB, firmware, footprint assignment or safety classification changed. No fabrication/certification/energization approval.


### 2026-11-23 — PR #21 ampliada: reconciliação de seis sensores e pinout TI

A PR #21 foi ampliada sem tocar no MASTER. O relatório inicial M2.9-AH recebeu a secção 9, cruzando a netlist com M2.9-E/H/I/J/L e datasheet TI TMCS1123 Rev. D (May 2026). Foi criado o documento de matriz `hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-AI-SIX-CHANNEL-TMCS1123-ADC-INTENT-RECONCILIATION-2026-11-23.md`.

Evidência documental adicional:
- M2.9-H/J recuperam as associações funcionais: U15/U16/U17 → ADC-A CH3/4/5; U18/U19/U20 → ADC-B CH3/4/5. M2.9-L mantém expressamente estas associações como intenção de fonte, ainda não aprovadas ao nível dos pinos.
- M2.9-E usa `SENSOR_5V_x` para VS do TMCS1123; M2.9-J usa `3V3_MEAS`. A faixa TI de 3–5,5 V não decide a escolha. Rail canónico permanece OPEN.
- Datasheet TMCS1123 Rev. D confirma: pin 4 ALERT e pin 7 OC são open-drain active-low; pin 5 VREF é saída analógica de referência zero-corrente (flutua se não usada); pin 9 VOC liga a VS se não usada; pin 10 NC pode ligar a GND ou ficar flutuante. Não confundir VREF com GND.
- Datasheet ADS131M06 Rev. A confirma: CH3 pins 3=N / 4=P; CH4 pins 5=P / 6=N; CH5 pins 7=N / 8=P. Comparando com M2.9-E, labels `_IP`/`_IN` de L1 e L3 estão invertidos relativamente aos nomes físicos P/N; L2 está alinhado. Isto prova uma inconsistência de nomenclatura/polaridade na fonte, não determina sozinho a correção elétrica. Significado de IP/IN e convenção de sinal devem ser aprovados.
- A matriz M2.9-AI mantém todas as decisões elétricas por U15–U20 em OPEN: direção de corrente, VOUT/filtro/ADC P, VREF/ADC N, rail VS, ALERT/OC, VOC e NC.

PR #21: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/21. Branch `work/teststation-u19-u2-followup-interface-reconciliation`; head atual `dfbec23e1f7f614e5b5ec7eac94504d3858b9799`; base `847bf54ef7560dff29573a11323b7a84fca43133`; compare 4 ahead / 0 behind; 2 ficheiros, 238 adições, zero remoções. PR continua aberta. CodeRabbit foi explicitamente solicitado para revisão independente via comentário `@coderabbitai review`; ainda não existe review formal. A leitura REST devolveu `mergeable=null`, `mergeable_state=unknown` enquanto o GitHub recalcula; não interpretar como conflito nem como aprovação. CI/status checks vazios. Não fazer merge até confirmar novamente mergeability e revisão suficiente. Relatórios são documentais; sem alterações ao MASTER, netlist, BOM, PCB, firmware, footprints ou segurança. Sem aprovação de fabrico, certificação ou energização.


Adenda 2026-11-23 — variante exata TMCS1123A3 e supply: leitura da secção 9.2.2 da revisão D do datasheet TI confirmou que variantes AxA (incluindo MPN A3) usam referência zero-corrente de 2,5 V e são destinadas a medição bidirecional com alimentação de 5 V; variantes BxA usam 1,65 V e são destinadas a 3,3 V. A família aceita 3–5,5 V, pelo que 3,3 V não está automaticamente proibido, mas exige cálculo de headroom, range de saída, limites diferenciais/common-mode do ADS131M06 e calibração. Isto torna M2.9-E SENSOR_5V_x coerente com a intenção AxA e reforça a contradição com M2.9-J 3V3_MEAS. Não mudar MPN nem rail sem análise quantitativa e aprovação. PR #21 atualizada para head `0550a9c46d954404729a6383101f0b361d892e7d` (5 commits, 2 ficheiros, 252 adições, zero remoções, compare 5 ahead/0 behind). Nova revisão CodeRabbit solicitada para incluir este commit; aguardar resultado. Nenhuma alteração elétrica.


Adenda crítica 2026-11-23 — TMCS1123A3 saturação provável no requisito 32 A RMS: o datasheet TI Rev. D confirma que o MPN `TMCS1123A3AQDVGR` corresponde ao grau x3A, 75 mV/A, VOUT zero-corrente típico 2,5 V; faixa válida de sensibilidade 0,05 V a VS−0,2 V. Para 32 A RMS sinusoidais, Ipeak=45,25 A e excursão necessária=3,394 V em torno de 2,5 V, exigindo aproximadamente −0,894 V a 5,894 V, fora do intervalo. Mesmo com VS=5,5 V, A3 só permite cerca de +37,3 A / −32,7 A de pico; com VS=5 V, positivo cerca de +30,7 A. O rating térmico de 80 A_RMS não equivale à faixa linear de medição. A2 (50 mV/A) a 5 V dá aproximadamente +46 A de pico, margem quase nula; A1 (25 mV/A) tem mais headroom, mas precisa avaliação de resolução/ruído. Isto é screening, não escolha de substituição. A3 fica HOLD crítico contra 32 A_RMS bidirecional; verificar requisito real, crest factor, sobrecarga, temperatura, PGA/ADC, ruído e margem antes de qualquer alteração de BOM. PR #21 atualizada para head `86dd94225a9e83aaeb330b561b9eb4be5a3e4017`; 6 commits, 2 ficheiros, 273 adições, zero remoções, base `847bf54ef7560dff29573a11323b7a84fca43133`, compare 6 ahead/0 behind. CodeRabbit review solicitada para este commit, ainda pendente. Sem alterações ao MASTER/BOM/PCB/firmware.


### Correção crítica 2026-11-23 — limites exatos TI TMCS1123A3 e FSR ADS131M06

A análise anterior de headroom baseada apenas em VS−0,2 V foi substituída pelos limites explícitos de faixa linear da tabela 4-1 do datasheet TI TMCS1123 Rev. D (SBOSA24D, maio 2026): A3A 75 mV/A = ±32 A com VS=5 V e −32 A a +9,3 A com VS=3,3 V. A1A 25 mV/A = ±96 A com 5 V e −96 A a +28 A com 3,3 V. A2A 50 mV/A = ±48 A com 5 V e −48 A a +14 A com 3,3 V. Os limites são de excursão linear, separados do rating térmico 80 A_RMS. 32 A_RMS sinusoidais = 45,25 A de pico; A3 não suporta sem clipping em nenhuma das duas alimentações. A2 a 5 V só tem 2,75 A de margem nominal de pico; A1 a 5 V tem margem de sensor, mas cria exigência adicional no ADC.

ADS131M06 Rev. A, secção 8.3.3 / tabela 8-1: FSR diferencial ±1,2 V / PGA gain. Com A1 25 mV/A e 45,25 A pico, o diferencial nominal é 1,131 V, restando apenas 69 mV (5,75%) de margem a PGA=1; ganhos superiores saturam. A2 gera 2,263 V e excede ±1,2 V mesmo em gain 1 sem atenuação/level shift; A3 teórico 3,394 V mas o sensor já satura primeiro. Common-mode, tensão absoluta por pino, topologia VREF, filtro, tolerâncias, crest factor, sobrecarga e calibração continuam OPEN. Isto é screening e não recomenda alteração de MPN.

M2.4 contém uma justificação A3 incorreta: assume 32 A como pico (32×75mV/A=2,4V) e diz suportar bidirecional 32 A, sem converter 32 A_RMS para 45,25 A pico. Deve ser formalmente reaberto/corrigido pelo responsável de design; não foi alterado nesta PR. A secção anterior que estimava A2 ≈46 A e A3 por cálculo simplificado de headroom fica supersedida pelos limites de Table 4-1.

CodeRabbit reviu PR #21 e apontou dois ajustes documentais: explicitar A3 HOLD na lista de provas obrigatórias e explicitar inversão L1/L3 P/N relativamente a pinos ADS (M2.9-E pins 3/7 são AIN3N/AIN5N com label _IP; pins 4/8 são AIN3P/AIN5P com _IN; CH4 pins 5/6 estão alinhados). Ambos foram corrigidos em AH. Também foi acrescentado FSR ADC em AI. Head PR #21 `92d94a8bf4e94db5db90faca5b812c2baeca0ff0`; 9 commits, 2 ficheiros, 328 adições, zero remoções; base `847bf54ef7560dff29573a11323b7a84fca43133`; PR mergeable=true no último refresh, sem merge até nova revisão/validação. Nova revisão incremental CodeRabbit solicitada após correções, ainda pendente. Nenhuma alteração elétrica.


Adenda 2026-11-23 — limite absoluto de pinos ADS131M06: datasheet TI Rev. A, tabela 6-3, AINxP/AINxN em PGA 1/2/4 devem ficar entre AGND−1,3 V e AVDD; em ganhos 8..128 o limite superior é AVDD−1,8 V. AVDD permitido 2,7..3,6 V. Logo FSR diferencial ±1,2 V não basta: cada pino tem de cumprir também o limite absoluto. Na hipótese A1/5 V direta, VREF=2,5 V e 32 A_RMS (45,25 A pico), VOUT pico ≈3,631 V; ultrapassa AVDD nominal 3,3 V e até o máximo AVDD 3,6 V. O RC M2.4 47Ω/4,7nF não é atenuador/level shifter; portanto nem A1 pode ser assumido diretamente compatível. É necessária interface analógica dimensionada (atenuação/level shift/buffer conforme análise), com provas de FSR, pin voltage, common-mode, tolerâncias, filtros, fase e calibração. PR #21 atualizada com secção 12 do relatório AI e descrição atualizada; head `3f73a13c81da5acd5d8e8d21267bc1be7aeb6a1a`. Nenhuma alteração elétrica.
