# AndreOS Memory — VAZÃO EVSE Charger Hardware V1

**Checkpoint:** 2026-11-13 UTC  
**Product repo:** AndreVazao/VAZAO-EVSE-Platform  
**Active branch:** feat/charger-hardware-v1-component-selection  
**Active PR:** https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/2  
**Policy:** PR #2 remains Draft/open; do not merge without André's explicit instruction and closure of engineering gates.

## Product and safety principles

VAZÃO EVSE includes modular AC chargers, TestStation, CPMS/App, control, payments and documentation. Product family: Wallbox 1/2 outputs; pedestal 1/2/4 outputs; cross-shaped four-face quad pedestal; future MultiStation.

Every output must have its own local EVSE safety/control function. Shared master/load management never replaces per-output safety. Local safe operation cannot depend on cloud/network. RFID, communications, HMI, payment and telemetry are optional modules with safe blanking/provisions. RFID identifies the user; mutable monetary balance is not stored on card. Payment/commercial services remain outside local safety. Evidence before assumptions; no invented terminal schedules, component ratings, dimensions or test results. No mains energisation, production fabrication, installation or commercial deployment without qualified review and applicable compliance validation.

## Verified GitHub state

PR #2: Draft/open/not merged. The verified head before M1.23 was `e404bf5d1201f84b8b048679dac277ab0c4aa294`; after M1.23 product-document and index commits, re-fetch PR metadata for the current head and counts. PR remains Draft/open/not merged; do not merge without André's explicit instruction. M1.22 and M1.23 PR-body summaries must be present and verified.

Engineering index: `docs/00-index/CHARGER-HARDWARE-V1-INDEX.md`.

## Milestone history

M1.1–M1.5A: component-selection gates, controller candidate/interface reviews, Phoenix CHARX modular architecture and manual extraction.

M1.6–M1.8: modular product/quad architecture, optional-module profiles and four-point CHARX study topology 1 × SEC-3xxx + 3 × SEC-1000. Manufacturer describes up to 11 SEC-1000 attached to one SEC-3xxx via supplied DIN-rail connector; nominal backplane current limit 6 A. Exact terminals/accessories remain open.

M1.9: point-level metering, RFID-reader absence/failure behaviour and shared server/backplane dependencies. Quad = four locally controlled outputs in shared cluster, not four proven autonomous units.

M1.10: lifecycle correction: ISKRA WM3M4C 1429603 no longer in product range; block new procurement. RFID/NFC-PCB 1391227, EV-RCM-6DC-WAT 1309697 and cable 1360462 are candidates. No 12 V PSU approved; STEP3-PS/1AC/12DC/2.5/PT 1170953 not approved for quad.

M1.11: separated controller/backplane, auxiliary 12 V, coil and safety power domains; 6 A backplane ceiling is hard and not an auxiliary distribution rating. No PSU selected.

M1.12: EEM-XM375 1674510 is a MID CT meter candidate, not production approved. EEM-EM355 2908578 discontinued; EEM-XM355 1674509 listed as replacement.

M1.13: CHARX firmware 1.9.1 lists EEM-XM355 as selectable point-meter profile, but separate legal-metrology/OCMF list does not include XM models. Per-point meter required for load management; optional grid meter is separate. XM355 is not evidenced as OCMF billing meter.

M1.14: EMH iML e-moc leading OCMF prototype candidate (CHARX firmware 1.09 / OCMF 1.4.1; manufacturer publishes MID/national approval, direct 0.1–5(40) A and RS-485 Modbus/OCMF). BAUER BSM-WS36A-Y held pending exact variant evidence; do not transpose H01 manual.

M1.15: Portugal legal-metrology/AFIR/payment boundary. IPQ is National Metrology Institution under DL 29/2022 Article 13. Public ad-hoc access and transparent pricing/payment obligations apply; payment stays outside local safety. No Portuguese billing approval.

M1.16: two-track meter bench evaluation: EMH iML e-moc for OCMF, EEM-XM355 point-meter/load-management alternative. One attributable meter per output plus optional separate grid meter. Bench tests not started.

M1.17: controlled supplier/adviser RFI package prepared for Phoenix Contact, EMH, Portugal metrology and operator/fiscal review. RFI has NOT been sent unless later evidence says otherwise.

M1.18: independent validation matrix separates manufacturer evidence, design evidence, test evidence and competent approval. Physical tests NOT STARTED absent retained records.

M1.19: conceptual modular electrical architecture and interface boundaries for Single/Dual/Quad/Wallbox; per-output local safety/control, switching/feedback, CP/PP and attributable metering; separate mains, backplane, auxiliary, coil and safety domains. No terminal-level wiring, final ratings, cable sizing or production release.

M1.20: 12 physical panel zones, repeated output-cell/shared assemblies, segregation, service access, optional-module blanking and mechanical inputs for dimensioned CAD. No dimensions, drilling, terminal layout or production assembly instructions.

M1.21 document:
`docs/03-engineering/CHARGER-HARDWARE-V1-M1-21-ENCLOSURE-ENGINEERING-THERMAL-AND-ENVIRONMENTAL-REQUIREMENTS.md`
SHA: `79b0777cd58ce6233bc46a99117f60b6eac13292`.
Defines enclosure framework for Wallbox/pedestal/quad/cross-quad/MultiStation; thermal-loss methodology, cooling trade-offs, environmental exposure, materials, corrosion, condensation, structural inputs, security/serviceability, risks and ten gates. No final dimensions/material/IP/IK/cooling/structural solution. Tests NOT STARTED.

M1.22 document:
`docs/03-engineering/CHARGER-HARDWARE-V1-M1-22-DIMENSIONING-CAPACITY-AND-CAD-INPUT-MATRIX.md`
Commit: `97bb669088c9edef7da499fc526f7a9123e47e5e`.
Index update commit: `e404bf5d1201f84b8b048679dac277ab0c4aa294`.
Defines source-controlled component envelopes, usable-space accounting, variant capacity model, zone schedule, cable/service envelopes, wallbox/pedestal/cross-quad interfaces, option configurations, native CAD deliverables, review checklist and ten CAD gates D1–D10. No numerical dimensions, coordinates, clearances, cable radii, structural loads, SKUs or manufacturing drawings invented/frozen. Conceptual CAD only until evidence gates close.


M1.23 document:
`docs/03-engineering/CHARGER-HARDWARE-V1-M1-23-NATIVE-CAD-ARCHITECTURE-AND-MODEL-CONTROL.md`
Product document commit: `89fb517b8e0792778f995d7c24f5e235c14e1afd`.
Defines native-source-first CAD control; provisional FreeCAD evaluation (not verified installed); STEP/DXF exchange; proposed repository structure; naming, units, datums and revision rules; parametric variant decomposition; optional configurations; manufacturer-model provenance; CAD validation; Git/large-file policy; controlled non-electrical pilot; ten C1–C10 gates. Actual workstation CAD inventory and native-format pilot remain NOT PERFORMED/OPEN. No product dimensions, component placement, clearances, manufacturing geometry or fabrication release.


**M1.23 verification checkpoint (2026-11-13):** product document commit `89fb517b8e0792778f995d7c24f5e235c14e1afd`; index update commit `c95efe30506c7efe10bd1b7ed9dc7820820e79b1`; index blob SHA `fc3d5136391bf312056135b0c6e0cb3f7093a626`. Document was fetched back and verified (14,641 characters; C1–C10 gates present). AndreOS Memory updated in commit `9a9af294f1711b8b0a5ffaebb2692906ca712285` (current file blob SHA before this checkpoint update: `6eaf876582cde14868429e52bc89be9b738abc1b`). PR #2 re-verified open/Draft/not merged/mergeable; 55 commits, 27 changed files, 4,847 additions, 2 deletions; HEAD `c95efe30506c7efe10bd1b7ed9dc7820820e79b1`. PR body includes M1.22 and M1.23; comment ID `6851812855`. Desktop Commander device `PC-Vazao-Anjos` was checked and is OFFLINE (last seen 9 hours before the check), so the actual CAD application/version inventory and native-format pilot could not be performed. Do not claim FreeCAD or any CAD application is installed. M1.23 C1/C2/C3 remain OPEN pending workstation access.

**Repository correction note:** M1.24 procedure file was initially created on default branch due an omitted branch argument. It was immediately copied to `feat/charger-hardware-v1-component-selection` (commit `197da5526169b75e4b590c4910b942eec8ab0eb6`) and the accidental default-branch copy was removed (commit `8a3e64164b0c2beb5b9415f768780754e7a381fa`). The intended working-branch copy is the authoritative version. Verify the default branch no longer contains the file and the feature branch does before further changes.

## Core files

- `docs/03-engineering/CHARGER-HARDWARE-V1-ELECTRICAL-SCHEMATIC.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-SAFETY-CHAIN.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-INTERNAL-PANEL-LAYOUT.md`
- `docs/03-engineering/CHARGER-HARDWARE-V1-TERMINAL-WIRING.md`
- `docs/04-bom/CHARGER-HARDWARE-V1-BOM.md`
- `docs/05-decisions/ADR-002-LOCAL-SAFETY-CONTROL-BOUNDARY.md`
- Full milestone catalogue in `docs/00-index/CHARGER-HARDWARE-V1-INDEX.md`.

## Open gates — do not silently close

Exact CHARX terminal schedule/topology/fault behaviour; complete 6 A backplane budget and approved supply; contactor coil/inrush/feedback; RCM and RCD coordination; per-output meter, MID scope, OCMF integration and four-session behaviour; RS-485 wiring/EMC; offline authorisation and signed transaction recovery; Portuguese metrology/fiscal/privacy review; supplier lifecycle/quotations/warranty/security; protection coordination/cable sizes/clearances; enclosure environmental targets and thermal data; exact component envelopes/cables/glands/structural loads/native CAD. Supplier RFI not sent. Physical/bench/environmental/thermal/structural tests NOT STARTED until evidence exists.


**M1.24 preparation checkpoint (2026-11-13):** prepared but NOT executed because Desktop Commander workstation `PC-Vazao-Anjos` was offline at the last check. Added read-only Windows inventory utility `tools/cad/Invoke-VazaoCadInventory.ps1` and procedure `docs/03-engineering/CHARGER-HARDWARE-V1-M1-24-CAD-WORKSTATION-INVENTORY-PILOT-PREP.md`. Utility collects Windows/host/PowerShell details, installed-app registry records and known CAD executable evidence; writes timestamped JSON and Markdown reports; performs no installation, removal, application launch or CAD file test. Its recursive known-path scan is limited to Program Files roots and LocalAppData\\Programs (not all LocalAppData) to reduce unnecessary scanning. Product commits: script initial `5cd2ffc47945bb884d8ad231fc5b50efd6954a47`, M1.24 prep doc `57468ac4601ee95a4e364fbedc225e16c9e65363`, index update `6257dc453e8c5c32949bb4abc07be58b25490d0e`, scan-scope refinement `14a9f98f1bf537b9ee50debfebbfc6c28048dbea`. Script has NOT been executed or runtime-tested; inventory and CAD app presence remain unknown. W1–W10 all OPEN. Review workstation report for sensitive identifiers/software before public commit. Next: execute inventory when PC online, reconcile actual CAD candidates, then test native save/reopen and verified STEP/DXF exchange. Do not claim CAD application installed or tests passed.

## Next milestone

**M1.24 execution — evidence-backed CAD toolchain pilot and first non-electrical model.** Run the committed read-only inventory utility on the actual workstation, reconcile exact application/version/path, then test native save/reopen and verified STEP/DXF exchange as applicable. Only after that, create a non-electrical workflow pilot with explicit test-only dimensions and no product-design claims. W1–W10 remain OPEN until evidence is collected. Keep dimensioned/fabrication release blocked until M1.21 E1–E10, M1.22 D1–D10 and M1.23 C1–C10 are evidenced.

## Continuation protocol

At every meaningful advance: update project document and index; update this AndreOS Memory file with milestone, exact paths, commit SHAs, PR state and open gates; fetch changed files to verify; keep PR Draft/open and never merge without explicit instruction; report created versus unverified work. Never claim physical tests, supplier contact, legal approval or installation without evidence.

## M1.25 preparation checkpoint (2026-11-15)

**Milestone:** CAD model provenance and dimensional evidence control.  
**Product branch:** `feat/charger-hardware-v1-component-selection`.  
**Status:** specification and schema published; not yet validated by a JSON Schema validator and no component records populated.

Product files:
- `docs/03-engineering/CHARGER-HARDWARE-V1-M1-25-CAD-MODEL-PROVENANCE-AND-DIMENSIONAL-EVIDENCE.md` — commit `4be82365866af3b71d794bda4e88195beab46f7b`.
- `schemas/cad/component-envelope-record.schema.json` — commit `a803204e6d1107a2dab389c9f499cda9851f8eac`.
- Index update `docs/00-index/CHARGER-HARDWARE-V1-INDEX.md` — commit `ae90a379bcc9f13daa77cb0e5fb3892f0ef19899`.

The specification classifies evidence A–F (manufacturer controlled drawing, manufacturer CAD, manufacturer datasheet, verified physical measurement, derived engineering, visual/third-party unverified), requires exact SKU/variant/revision, source metadata and hashes, explicit mm dimensions/datums, model format/hash/units/orientation, separate installation/service envelopes, review scope and independent review for design release. It explicitly prohibits unverified third-party models as dimensional authority. JSON Schema checks structure only; it does not authenticate URLs/files or prove dimensional correctness.

P1–P10 remain OPEN. No exact component envelope is populated or approved; no CAD model or product geometry is created; no schema validator run is claimed. M1.21 E1–E10, M1.22 D1–D10, M1.23 C1–C10 and M1.24 W1–W10 remain open unless separately evidenced. PR #2 remains Draft/open/not merged. Next: validate schema syntax, add a real record only after exact manufacturer evidence is available, then implement/test a validator and independent review. Keep workstation execution separate; do not infer PC availability.

## M1.26 implementation checkpoint (2026-11-15)

**Milestone:** CAD evidence validator and CI.  
**Product branch:** `feat/charger-hardware-v1-component-selection`.  
**Status:** validator, unit tests and CI workflow committed; automated execution not yet observed; no test pass is claimed.

Product files:
- `tools/cad/validate_component_envelopes.py` — commit `ad4a37faa23c7610d88feef5b48bc75cfae9965e`; offline JSON Schema + semantic validation, path containment and SHA-256 checks.
- `tests/cad/test_validate_component_envelopes.py` — commit `d8adf911de94578b41d5a79a54b6fc6e18b7c7b0`; seven positive/negative unit tests authored.
- `tools/cad/__init__.py` — commit `793c8fdeba86d73b9953c60043a9d7b289b4f76a`.
- `requirements-cad-validation.txt` — commit `137321912ecf7fb4f1cae39f3b91ec7317869964`.
- `.github/workflows/cad-envelope-validation.yml` — commit `81c20aa0ce0826946763c9ce340994b3dd9c79a1`; Python 3.12, JSON Schema Draft 2020-12 check and unit-test execution.
- `docs/03-engineering/CHARGER-HARDWARE-V1-M1-26-CAD-EVIDENCE-VALIDATOR-AND-CI.md` — commit `26469031166235e1931335d90a7b306767e086ff`.
- Index update — `docs/00-index/CHARGER-HARDWARE-V1-INDEX.md`, commit `42c268ebc071363491750f94f70077a48be2a19d`.

The validator is intentionally offline and does not authenticate manufacturer URLs, open CAD geometry, or establish dimensional correctness. It detects schema errors, duplicate identities/source IDs, missing or mismatched source references, path traversal, missing/mismatched local SHA-256, and inadequate release review. CLI intentionally fails closed if no component records exist. No production component record is fabricated to satisfy CI.

At latest check, PR #2 head `42c268ebc071363491750f94f70077a48be2a19d`, 70 commits, 37 changed files, 6,191 additions; open/Draft/not merged. `fetch_commit_workflow_runs` returned no runs for the latest head, so CI is still PENDING/UNOBSERVED. Unit tests have NOT been executed locally or confirmed in GitHub Actions. Next: inspect workflow run/checks; fix any failures; then run tests. After CI passes, add the first exact component record only when manufacturer evidence and licensing allow. M1.25 P1–P10 and M1.26 V3/V4 remain pending as applicable; no component envelope or CAD geometry approved.

M1.26 documentation reconciliation: M1.25 specification updated in commit `d8ca5ca0379b856fe533ed09cb3dde37b3ea3256` so P8 now explicitly waits for confirmed CI execution; index reconciled in commit `8ad7a91079520696f2871349653db5b11e49739b`. Validator code/tests/workflow remain committed as above. No workflow run is visible at the latest check; execution remains unverified.


## M1.27 component evidence register checkpoint (2026-11-17)

**Milestone:** controlled component candidate and evidence register.  
**Product repository:** `AndreVazao/VAZAO-EVSE-Platform`.  
**Product branch:** `feat/charger-hardware-v1-component-selection`.  
**Status:** register and index published; no component selected or approved for production.

Product file:
- `docs/04-bom/CHARGER-HARDWARE-V1-M1-27-COMPONENT-EVIDENCE-REGISTER.md` — commit `46bb8e941844aaaeffe9b3c18afe4ccdb4e209b0`.
- Index `docs/00-index/CHARGER-HARDWARE-V1-INDEX.md` — commit `c20e5ac0dba9055567aa2e9425e240b5c0aac16c`.

The register classifies CHARX SEC-1000/SEC-3xxx and SEC-3150 1138965 as study candidates; CHARX 2902802 as an alternative; Bender CC613 and ISKRA WM3M4C 1429603 as procurement-blocked lifecycle references; EEM-XM355 1674509 as point-meter/load-management prototype candidate; EEM-XM375 1674510 as a compatibility hold; EMH iML e-moc as OCMF prototype candidate; Carlo Gavazzi EM340DINAV23XS1PFB and EM24DINAV23XE1PFA as study alternatives; and the RCM 1309697, RFID 1391227, STEP3 1170953 and accessory cable 1360462 as candidates requiring renewed exact-variant evidence. Protection, contactor/driver, Type 2, enclosure, HMI and communications remain architecture-only/unselected. These are project-record classifications, not a fresh manufacturer lifecycle or datasheet audit.

M1.27 defines ten selection gates and required dossier fields: exact identity/revision, lifecycle, stored source metadata/hash, application-specific electrical ratings, terminal/pinout, compatibility, failure/safe-state, metrology, mechanical provenance under M1.25, supply chain and independent approval. No component-envelope JSON records or numeric dimensions were fabricated. No manufacturer RFI was sent.

**M1.26 verification reconciliation:** fetched from the product feature branch and confirmed that validator, seven authored tests, dependency, CI workflow and M1.26 specification exist. The workflow is configured for pull requests touching CAD paths and pushes to main; no successful Actions run was observed in this check. Test execution remains PENDING/UNOBSERVED, not passed. PR #2 was open, Draft, not merged, mergeable at the check; head before M1.27 writes was `8ad7a91079520696f2871349653db5b11e49739b`.

Open gates remain: M1.26 Actions execution; exact controller terminal/topology and 6 A bus budget/fault isolation; complete auxiliary 12 V budget; contactor/RCM/RCD coordination; per-output meter/OCMF/MID and Portuguese metrology/fiscal suitability; supplier RFI not sent; exact protection/cable/enclosure/Type 2; mechanical component envelopes; CAD workstation inventory and native CAD pilot; all physical/bench/thermal/environmental/structural tests NOT STARTED. PR #2 remains Draft/open and must not be merged without explicit instruction.


## M1.26 CI execution confirmation (2026-11-17)

Correction to the 2026-11-15 pending/unobserved status: GitHub Actions run `44028175510` for commit `c20e5ac0dba9055567aa2e9425e240b5c0aac16c` completed with conclusion `success`. Job `validate-cad-evidence-tooling` completed successfully. The JSON Schema validation step and unit-test step both completed successfully; the unit suite contains seven tests. Run URL: https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/44028175510.

Product documentation reconciled:
- `docs/03-engineering/CHARGER-HARDWARE-V1-M1-26-CAD-EVIDENCE-VALIDATOR-AND-CI.md` — commit `400a43616152e7fe723e6dcf2ac1d9f96b31aa19`.
- `docs/00-index/CHARGER-HARDWARE-V1-INDEX.md` — commit `03e0b0ef9ce99d76b45c05dbd735d1383ee92989`.

This closes M1.26 V3 (schema check) and V4 (unit tests) for the tooling. It does NOT validate a real component record, manufacturer source authenticity, dimensional accuracy, CAD geometry or product design. V5–V8 remain open. No bench/physical test or production approval is implied.


## M1.28 CHARX controller primary-source audit (2026-11-17)

**Milestone:** exact controller identity, manufacturer interface and cluster-limit audit.  
**Product branch:** `feat/charger-hardware-v1-component-selection`.  
**Status:** primary-source desk review published; candidate architecture not approved.

Product files:
- `docs/03-engineering/CHARGER-HARDWARE-V1-M1-28-CHARX-CONTROLLER-MANUFACTURER-EVIDENCE-AUDIT.md` — commit `42458b6a693f0cf8c6990ea757907dd89666302d`.
- M1.27 register amendment `docs/04-bom/CHARGER-HARDWARE-V1-M1-27-COMPONENT-EVIDENCE-REGISTER.md` — commit `483ba88804413e086929abbf2b878d80b9be61b0`.
- Index `docs/00-index/CHARGER-HARDWARE-V1-INDEX.md` — commit `5fb23898267806a09e771173892f05771cb14f16`.

Official Phoenix Contact references reviewed on 2026-11-17: SEC-1000 1139034 and SEC-3000 1139022 Portugal product pages; family ordering data; interface/terminal overview; SEC-3xxx + SEC-1000 cluster documentation; UM EN CHARX SEC Revision 06 / firmware 1.9.1 manual index; SEC-1000 stand-alone/Event Actions guidance. Exact order numbers now recorded for SEC-1000 1139034, SEC-3000 1139022, SEC-3050 1139018, SEC-3100 1139012 and SEC-3150 1138965.

Manufacturer states up to 11 SEC-1000 per SEC-3xxx via DIN-rail connector, supply via bus, automatic communication and a 6 A nominal backplane current limit. It requires full configuration current consumption calculation. SEC-1000 and SEC-3xxx contactor terminal arrangements differ; both product pages publish a floating contact interface up to 250 VAC/30 VDC, 2 A, max 1500 VA, but coil compatibility is not assumed. SEC-3xxx supports 2× Ethernet and embedded Linux; 4G/2G belongs to SEC-31xx; ISO/IEC 15118 belongs to SEC-3x50. SEC-1000 standalone authorization needs Event Actions; in a cluster client arrangement the SEC-3xxx application processes charging release.

Four-point study topology is now expressed exactly as 1 × SEC-3000 (1139022) + 3 × SEC-1000 (1139034), within module-count allowance but NOT proven within the 6 A bus budget. The 12 V worst-case budget, supply injection, exact wiring, contactor coil/feedback, per-output safety under server/bus loss, offline authorisation and fault-injection tests remain OPEN/NOT STARTED. M1.28 is a manufacturer-source desk review; online source files have not yet been archived with M1.25 SHA-256 records. No supplier confirmation, hardware sample, bench test, production selection or mains energisation is claimed.

M1.26 CI confirmation remains valid: run `44028175510` completed successfully with JSON Schema and seven unit tests passing. It validates the tooling only; no real component records or CAD geometry are approved.


## M1.29 multi-output feeder topologies and cable sizing checkpoint (2026-11-18)

**New user requirement:** dual- and quad-output chargers must support both (a) independent incoming installation feeders, one per output, and (b) one common incoming feeder that is distributed to the output branches. Hybrid feeder groups and common feeder with enforced load management are also considered. The installation topology must drive cable sizing for both incoming feeders and internal/output branches and must be reflected in wiring, BOM, CAD cable-entry/terminal envelopes and installation instructions.

**Product branch:** `feat/charger-hardware-v1-component-selection`.  
**Milestone document:** `docs/03-engineering/CHARGER-HARDWARE-V1-M1-29-MULTI-OUTPUT-FEEDER-TOPOLOGIES-AND-CABLE-SIZING.md` — commit `457d60a160e3d5fb9c00a5ad0c376ada3856a5d4`.

Updated product docs:
- `docs/04-bom/CHARGER-HARDWARE-V1-BOM.md` — commit `f5c9eb8428b2a32e73ad374e4ffea809f483f23e`; split independent/common incoming cables, branch wiring, glands, main distribution, main/output protection, neutral and PE items.
- `docs/03-engineering/CHARGER-HARDWARE-V1-M1-22-DIMENSIONING-CAPACITY-AND-CAD-INPUT-MATRIX.md` — commit `8ee593d719af8a9b5421c32db41e3fc715cf4e1a`; adds feeder-entry, bend-radius, gland, lug, terminal and service envelopes.
- `docs/03-engineering/CHARGER-HARDWARE-V1-ELECTRICAL-SCHEMATIC.md` — commit `f6bef69e6bdf724e1ca6d79d98d9f80e5141c388`; adds independent/common/hybrid/managed multi-output supply arrangements.
- `docs/00-index/CHARGER-HARDWARE-V1-INDEX.md` — commit `294b41a3baad4d0f2ecd707836b992658fd34d24`.

Engineering basis: CTE 64 / IEP Guia Técnico das instalações elétricas para alimentação de VE, Edition 3 (2023-09-14), approved by DGEG as informative/orienting guide, sections 3.1.2, 3.1.3, 3.1.5 and 4.3. It states 1.00 simultaneity for circuits directly feeding individual connection points; a lower simultaneity for circuits feeding multiple points only with load control; dedicated circuits for each EV; max 5% voltage drop origin-to-EV connection; and a 2.5 mm² minimum conductor section for dedicated EV circuits (not a recommendation for 32 A design). RTIEBT and current applicable standards still govern; qualified design required.

Reference planning currents for 22 kW-class / 32 A / 400 V three-phase outputs: single 32 A/phase; dual 64 A/phase; quad 128 A/phase (about 88.68 kVA for quad balanced). These are arithmetic planning values only, not cable sections or protective-device selections. Single-phase configurations require phase-by-phase imbalance analysis. Load-control reductions may be used only when the local secured system enforces the feeder maximum and has a validated safe response to sensor, controller, communications and power failures.

No cable section, cable type, breaker, RCD, busbar, terminal, gland or installation wiring was selected or released. Cable calculations are NOT STARTED; exact lengths, installation methods, conductor material, grouping, ambient/soil conditions, voltage-drop allocation, fault levels, earthing, harmonics and protection coordination are absent. No mains energisation, fabrication or procurement is authorised. PR #2 remains Draft/open/not merged.


### M1.29 clarification — common trunk branches externally

User's “one main cable then derives to four” requirement was expanded to distinguish two physically different cases: (1) common feeder enters the quad charger and splits on its internal distribution block/busbar; (2) common trunk runs from the site main switchboard to an external local distribution/branch enclosure and then four separately protected branch feeders run to the EVSE outputs/units. The latter is particularly relevant to MultiStation/parking-lot installations and is now explicitly documented in M1.29. It has separate trunk and branch cable calculations; voltage drop to each output is the sum of trunk plus its branch; protection/coordination and neutral/PE design are explicit.

Follow-on changes:
- M1.29 document updated with external branching topology — commit `27d1f577c5d9aa4bd6097024b06f33ebd248325b`.
- BOM includes `DB-EXT`, `CABLE-TRUNK`, `CABLE-OUT`, `QF-BRANCH[n]` — commit `5924e364f07217b1257d705eec2366830d5f872e`.
- M1.22 CAD matrix includes external distribution enclosure and separate trunk/branch route inputs — commit `72d59da77e252070f3300f899b43162bba45cecc`.
- Index clarification — commit `8d219b371cca527711b1a6add63654667d65ee2e`.

No cross-section or protective-device rating selected. External trunk sizing must include all downstream branches and any other loads; branch cable sizing remains individual.


## M1.30 cable sizing calculation matrix checkpoint (2026-11-18)

**Branch:** `feat/charger-hardware-v1-component-selection` (VAZÃO EVSE Platform PR #2 remains Draft/open/not merged).

M1.30 adds a per-circuit cable sizing calculation and evidence workflow for all M1.29 topologies: independent feeders; common feeder split internally; external site trunk with separately protected branches; hybrid group feeders; and locally managed common feeder. Every physical segment has its own record, linked to its parent where applicable. Voltage drop to an EV point is the sum of the actual series segments on that route, not the sum of parallel branches.

Files:
- `docs/03-engineering/CHARGER-HARDWARE-V1-M1-30-CABLE-SIZING-CALCULATION-MATRIX.md` — commit `4e100d70f4319bdb015c3d4cca337b92323d333b`.
- `schemas/electrical/cable-sizing-record.schema.json` — commit `8fcf1c24c4ed087c310d2f4365bfa5a124f008f3`.
- Product index and BOM reference the M1.30 calculation framework.

The record contract captures circuit topology and parent, supply and per-phase design current, conductor material/type/core count/section, installation method and correction-factor sources, actual route length, voltage-drop budget/calculation evidence, protective device, manufacturer ampacity evidence, prospective short-circuit and disconnection checks, neutral/PE, terminal/gland/thermal fit, evidence files and independent review. It deliberately does not embed generic cable ampacity tables or claim to calculate/approve engineering results. Schema validity is not proof of source authenticity or electrical correctness.

No installation route, cable type/material/section, ambient/grouping conditions, fault level, loop impedance, protective-device model/settings, or approved maximum demand has been supplied. Therefore all M30 calculation/review gates remain OPEN or NOT STARTED. No cable section, breaker/RCD rating, procurement, installation, fabrication or energisation is released. A qualified competent electrical designer must complete and independently review every real circuit against current Portuguese requirements and applicable standards.


## M1.31 distribution architecture and product capacity matrix checkpoint (2026-11-18)

Existing on branch `feat/charger-hardware-v1-component-selection`: `docs/03-engineering/CHARGER-HARDWARE-V1-M1-31-DISTRIBUTION-ARCHITECTURE-AND-PRODUCT-CAPACITY-MATRIX.md`. It maps Wallbox single/dual, pedestal single/dual/quad, cross-shaped quad and MultiStation to independent/common-internal/hybrid/external-trunk topologies. It separates per-output rating, installed aggregate nameplate, locally enforced aggregate maximum, available site capacity and instantaneous allocation. Defines phase-by-phase constraints and local load-management requirements. Reference 32 A / 400 V three-phase scenario only; no product rating, site capacity, feeder or cable/protection is approved. Index already contains M1.31. This checkpoint is added to persistent memory now; it was not present in the previous memory snapshot.

## M1.32 load-management fail-safe and fault validation checkpoint (2026-11-18)

**Branch:** `feat/charger-hardware-v1-component-selection`.

Created `docs/03-engineering/CHARGER-HARDWARE-V1-M1-32-LOAD-MANAGEMENT-FAILSAFE-AND-FAULT-VALIDATION.md` (commit `ef33799a2be0a55fcb1d236c1a7fe7ee946a554d`). Updated the engineering index and functional electrical schematic to identify the local load-manager enforcement boundary and required failure responses.

M1.32 defines separation between site metering, local load manager, per-output EVSE controllers, protective devices and CPMS/cloud; operating states INIT/NORMAL/LIMITED/SAFE_STOP/MAINTENANCE; phase-aware allocation constraints; fault responses for missing/stale/implausible meter data, phase mapping, watchdog/process/power/bus loss, output non-response, contactor feedback, CPMS/WAN loss, restart and configuration tampering; and 14 bench fault-injection scenarios with required evidence. It does not select hardware, fallback current, response time or safe limit. No physical test is claimed; all test cases are NOT STARTED. Dynamic load management cannot justify reducing feeder capacity until the exact local system is calculated, tested and independently approved.

**PR/repository caveat:** PR #2 was found closed and unmerged on 2026-11-18 at 18:41 UTC. Its branch is 95 commits ahead and 130 behind `main` (compare status diverged). No attempt was made to reopen or merge it, and no new PR was created on this divergent base. The existing work remains on the feature branch pending an explicit recovery/rebase/port strategy. Main does not yet contain M1.29–M1.32. This is a publication/review blocker, not a technical approval.


## Recovery PR #10 — clean baseline, M1.1–M1.2 (2026-11-18)

The historical engineering branch `feat/charger-hardware-v1-component-selection` had diverged from current `main` (at inspection: 98 commits ahead / 130 behind) and PR #2 was closed without merge. No reason for closure was established from the available issue comments/reviews; no reviews or inline review threads were recorded. The old branch and PR #2 were preserved; no force-push, merge, re-open or destructive history operation was performed.

To restore the one-work-PR policy safely, created clean branch `recovery/charger-hardware-m1-1-2` directly from current `main`, then ported only three files in three commits:
- `docs/03-engineering/CHARGER-HARDWARE-V1-COMPONENT-SELECTION-GATE.md` (M1.1)
- `docs/03-engineering/CHARGER-HARDWARE-V1-COMPONENT-CANDIDATES-M1-2.md` (M1.2)
- `docs/00-index/CHARGER-HARDWARE-V1-INDEX.md` (index links and active recovery branch)

Verified branch compare: 3 commits ahead, 0 behind, exactly 3 changed files. Opened Draft PR #10: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/10. PR #10 is the sole open work PR at checkpoint time; it is not merged. This is a documentation-only recovery slice; no CI execution is claimed or required by the current workflow. Technical review remains open.

M1.29–M1.32 and the intervening M1.3–M1.28 work remain preserved on the historical branch and are NOT yet in `main` or the clean recovery branch. They must be recovered sequentially in small, dependency-aware PRs after #10 is reviewed/merged. Do not create another work PR while #10 remains open. Do not merge #10 without explicit user approval. No electrical component, cable, protection, installation or production design is approved by this recovery PR.


## PR #10 audit checkpoint (2026-11-20)

PR #10 remains open, Draft, unmerged, and has no recorded reviews or workflow runs at audit time. Head now has 5 commits and 3 files changed. Manual audit found the index initially omitted M1.1/M1.2 links, and M1.2 referenced M1.5/M1.5A documents not present on main; those were corrected in the same PR branch: the index now links the recovered M1.1/M1.2 documents, and M1.2 explicitly marks later M1.5/M1.5A evidence as unrecovered/pending rather than linking broken paths. CodeRabbit manual review was requested via PR comment; no review result is yet recorded. No merge or new PR created because review/check gates are not yet satisfied.

**Updated standing merge authorization (2026-11-20):** user explicitly authorized autonomous merging whenever the PR is verified ready (review findings resolved, required checks green, no unresolved conflicts/merge blockers), then immediately starting the next clean branch and single work PR. This replaces the earlier requirement to request separate merge authorization. Do not merge if CI/review is absent, red, unresolved, or the readiness evidence is insufficient. Continue one open work PR only.


## PR #10 follow-up review correction (2026-11-20 11:24 UTC)

CodeRabbit manual review completed for head edbb16c; no actionable comments generated in its automated summary, but its manual response identified two items. Both were corrected on the same PR branch: (1) PR validation now reports the accurate branch comparison (6 ahead / 3 behind at the latest recorded comparison; GitHub PR metadata subsequently reported mergeable=true); (2) CC613 lifecycle is now explicitly **unverified**, not asserted discontinued, and procurement remains blocked pending written manufacturer confirmation. The unverified 48-point/cluster headline and firmware claim were removed from M1.2 pending primary-source confirmation. M1.2 now includes the official Phoenix Contact family page as a source. CodeRabbit's checks for that review showed 4/4 pre-merge checks passed and no actionable findings, but that review covered the previous head edbb16c, not the latest correction commit ae52b65. Latest HEAD has no GitHub workflow runs and no combined status checks. PR #10 was changed from Draft to Ready for review. No merge performed: current HEAD lacks fresh review/CI evidence, even though GitHub reports mergeable=true. No second PR opened.


## 2026-11-20 21:41 UTC — PR #10 validation checkpoint

- PR #10 remains the sole open work PR: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/10`; Ready for review, not Draft, open/unmerged.
- HEAD `ae52b65a27ec2c3d5039e06d1626eb8b4de4d83f`; GitHub mergeable=true, but compare `main...recovery/charger-hardware-m1-1-2` still diverged: 6 ahead / 3 behind. Latest main base SHA `0c4450d508dbfd03ca22d16598befe37013a8686`.
- No workflow runs or combined status checks on HEAD; no docs/Markdown validation workflow identified in main. CodeRabbit review available covers older commit `edbb16c`; 4/4 its pre-merge checks passed, but not fresh against latest HEAD. Requested fresh review in PR comment; no response/evidence yet.
- PR description corrected to reflect current Ready-for-review state and validation gaps.
- Merge remains blocked by missing fresh review/CI and branch update. Do not treat mergeable=true or CodeRabbit checks from an older SHA as green validation.
- No additional PR created; one-work-PR rule remains enforced.


## 2026-11-21 10:50 UTC — M1.2 CodeRabbit findings fixed

- PR #10 remains the sole open work PR, Ready for review and unmerged. Current head `b2fc9c8364b8074428f85dd6d192608415bad57d`, 8 commits, 3 files.
- Latest CodeRabbit incremental feedback found: malformed literal `\\n` embedded in Phoenix Contact/Bender source line; stale CC613 discontinued assertion in release status; residual 'do not procure while discontinued' phrase; and 48-point headline not independently verified.
- Fixed all four: separated source entries onto real Markdown lines; CC613 lifecycle now consistently unverified and procurement blocked pending written Bender confirmation; removed 48-point headline and left supported cluster capacity for validation.
- Requested another CodeRabbit review against current HEAD; no response yet. Current HEAD has no GitHub Actions workflow runs or combined status checks.
- Branch remains diverged from main (6 ahead / 3 behind on last comparison); connector has no safe dedicated update/rebase operation identified. No merge, because branch sync and CI/review evidence are still incomplete.


## 2026-11-22 05:34 UTC — PR #10 incremental review and synchronization checkpoint

- PR #10 remains the only open work PR, Ready for review, unmerged. HEAD remains `b2fc9c8364b8074428f85dd6d192608415bad57d`; 8 commits, 3 files, 274 additions / 1 deletion.
- Latest CodeRabbit incremental review (covering HEAD `b2fc9c8`) found no remaining document findings in the reviewed M1.2 content. It confirmed CC613 lifecycle is unverified/procurement blocked, local links resolve, and all six external source URLs returned HTTP 200. It flagged stale PR validation counts and correctly noted there are no repository workflow runs/status contexts; the CodeRabbit check itself is `skipped`, not a CI pass.
- PR description was corrected: current compare is diverged, 8 commits ahead / 4 behind; main HEAD observed `be2c70f8dfa9294f2dba6d0e890b68c3b3bc3b36`, merge base `8a3e64164b0c2beb5b9415f768780754e7a381fa`. Description now explicitly distinguishes CodeRabbit review from repository CI.
- Latest PR metadata after description update reports `mergeable=true`, but the authoritative compare remains `diverged` (8/4). Workflow runs and combined status contexts remain empty. Do not interpret mergeable=true as branch synchronization or CI success.
- Attempt to use the authenticated browser's standard GitHub Update branch control could not start because Browser Use reported insufficient project credits. No branch update, rebase, force-push, merge, or other destructive operation was performed.
- M1.1/M1.2 files were re-read at the PR branch: CC613 lifecycle language is consistent with unverified status and procurement block; no stale discontinued claim or 48-point headline found. No literal escaped newline source issue found.
- Merge remains blocked pending safe branch synchronization and required repository validation/review gates. No second PR created; preserve the single-open-work-PR rule.


## 2026-11-22 — PR #10 provenance and CodeRabbit final content audit

- Re-read the full latest CodeRabbit response on PR #10 for HEAD `b2fc9c8364b8074428f85dd6d192608415bad57d`. It reports no remaining document findings, confirms local targets exist and six external source URLs returned HTTP 200. Its only finding was stale branch counts (already corrected in PR description to 8 ahead / 4 behind). It confirms zero repository workflow runs/status contexts and one skipped CodeRabbit check; not a green CI result.
- Independently fetched the two M1.1/M1.2 source documents from both historical branch `feat/charger-hardware-v1-component-selection` and recovery branch `recovery/charger-hardware-m1-1-2`. Differences are intentional and scoped: M1.1 branch metadata; M1.2 removal of unverified 48-point claim; CC613 status corrected from asserted discontinued to unverified/procurement blocked; M1.5/M1.5A links changed to explicit future recovery; source list normalized; release statement corrected. No unexplained content divergence found in this comparison.
- PR description now reflects current compare 8 ahead / 4 behind, and distinguishes CodeRabbit review from CI. PR remains open and is the only work PR.
- No safe automatic branch update/rebase path is available through the current GitHub connector; Browser Use could not start due insufficient credits. Do not manipulate low-level git refs/trees or force-push. Branch sync remains a blocker.
- Merge remains prohibited until branch synchronization, required CI evidence and any required technical approval/review are resolved. No second PR created.


## 2026-11-22 20:35 UTC — clean recovery PR #18 and documentation CI

- PR #10 was closed without merge after its branch diverged from main. Its historical content was preserved; no force-push or destructive history rewrite was used.
- Created clean branch `recovery/charger-hardware-m1-1-2-mainline` from main SHA `d79a421c9c722c6e4f28cfc27cffd248233b1bfe`; opened sole work PR #18: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/18.
- Recovered M1.1, M1.2 and index in commit `0afb2423900eff954ca83ce4a72f40dd542078fb`. Then added a narrow documentation CI workflow in commit `61001187e32fd1e754b49ddadcdf7ec11d2c3e07`: `.github/workflows/validate-evse-docs.yml`.
- Current compare at checkpoint: 2 commits ahead / 0 behind main; merge-base equals main base SHA above. Four changed files: workflow plus the three recovered documentation files. PR remains open, Ready for review, not merged.
- GitHub Actions run `45067230595`, workflow “Validate EVSE documentation links”, completed SUCCESS. Job `validate-local-markdown-links` passed. Scope is only relative Markdown link existence in changed Markdown files; it is not electrical, ERC, netlist, firmware, CAD or hardware validation. No classic combined status contexts were reported.
- Formal PR reviews and inline review threads remain empty. Do not merge yet: obtain an appropriate technical review and confirm applicable checks remain green at the latest HEAD.
- Repo setting `allow_update_branch=false`; do not rely on GitHub's `mergeable=true` as a substitute for compare/CI/review evidence.
- Engineering safety status unchanged: no component production freeze, no procurement/fabrication/installation/mains energisation authorization; CC613 lifecycle unverified and procurement blocked. M1.3+ recovery remains the next work block after this PR is resolved.


## 2026-11-23 07:06 UTC — PR #18 synchronized with latest main

- Main advanced after PR #18 was opened: commit `66354cd67556d5563779d02ec27f6fe0e60a8835`, adding a read-only KiCad MASTER audit workflow/report for TestStation. This is a separate module from Charger Hardware.
- Independent compare detected PR branch 2 ahead / 1 behind. To preserve both lines, obtained exact Git tree/blob SHAs from GitHub API, built a merged tree based on current main, retained the four PR files and merged the current main index changes with the M1.1/M1.2 index links.
- Created two-parent merge commit `df33ead34140ca0b98832e8ec9f37a1f877d2a7e` with parents current main `66354cd67556d5563779d02ec27f6fe0e60a8835` and prior PR head `61001187e32fd1e754b49ddadcdf7ec11d2c3e07`. Updated branch using non-force fast-forward with expected prior SHA; GitHub accepted.
- Fresh independent compare: `main...recovery/charger-hardware-m1-1-2-mainline` is ahead 3 / behind 0; merge-base is `66354cd67556d5563779d02ec27f6fe0e60a8835`. Diff against current main contains four intended files: documentation workflow, index, M1.1 gate and M1.2 candidates.
- PR #18 remains open and Ready for review, not merged. GitHub metadata says mergeable=true, but current HEAD has no associated PR workflow runs or combined status checks yet. Earlier docs CI run `45067230595` succeeded on previous commit `61001187...`; it does not validate the new HEAD.
- Requested fresh CodeRabbit review against current HEAD via PR comment ID `7093983885`; response/review not yet observed. Formal review list and inline threads were empty at last check.
- PR body corrected with current HEAD, main SHA, merge strategy, compare, and validation limits. Note PR metadata counts/base_sha may lag; rely on independent compare for synchronization.
- No merge. Next: verify a fresh docs CI run for `df33ead...` and inspect CodeRabbit/qualified review. Keep single open PR rule. M1.3 must wait until #18 is eligible and merged.
- Safety status unchanged: M1.1/M1.2 are documentation gates/shortlist only. No production component approval, procurement, fabrication, installation or energisation; CC613 lifecycle unverified/procurement blocked.


## 2026-11-23 13:43 UTC — PR #18 review fixes and second main synchronization

- Revalidated PR #18 and found main had advanced from 66354cd67556d5563779d02ec27f6fe0e60a8835 to 847bf54ef7560dff29573a11323b7a84fca43133 (two commits; latest adds TestStation U19/U2 topology-mismatch evidence). Independent compare showed PR 3 ahead / 2 behind.
- CodeRabbit review on prior HEAD df33ead34140ca0b98832e8ec9f37a1f877d2a7e published four actionable workflow findings: NUL-safe changed-file enumeration, reference-style links, balanced parentheses in destinations, and ignoring fenced/inline code. All four were verified against the old workflow and addressed in .github/workflows/validate-evse-docs.yml.
- Replaced regex extraction with CommonMark token parsing using pinned markdown-it-py==3.0.0 installed inside a temporary venv. The validator now obtains actual link_open tokens (including used reference links), ignores code spans/fences, and retains the existing relative-target filesystem checks. Changed-file enumeration now uses git diff --name-only -z and decodes each NUL-delimited path via os.fsdecode.
- Workflow update commit 8b1375b224c7e449a45233d36cd6a8ce12880feb; a follow-up corrected Python byte/string escape handling, commit 0abe2eb836fa6179aabc3cd175ddce0e3be1c7a1. Verified fetched workflow source contains split(b"\\0"), link_open, and "\\n".join(...) in Python source (actual source escapes represent NUL/newline at runtime).
- Re-synchronized without history rewrite: latest main 847bf54... is parent 1 and branch head 0abe2eb... parent 2. Merge commit 16d02c67b9a39c6c85d2feb2385e91409897cf44; branch ref updated with force=false and expected prior SHA. No force-push.
- Fresh independent compare confirms main...recovery/charger-hardware-m1-1-2-mainline = ahead 7 / behind 0, merge-base exactly 847bf54..., with exactly four intended files in the diff. PR #18 remains the only open work PR.
- PR #18 body refreshed with current main/head, compare, review-fix summary and validation limits. GitHub PR metadata now reports mergeable=true; that is not CI or review approval.
- Previous docs CI run 45128631599 completed SUCCESS on old HEAD df33ead..., before CommonMark fixes. Current HEAD 16d02c... has no workflow run or combined status check reported by the connector at 13:42 UTC. Do not claim current CI passed.
- CodeRabbit's four workflow comments are outdated after the fix. Its two additional findings concern the TestStation KiCad audit report already on main and outside this PR's four-file diff; they were deliberately not mixed into Charger Hardware scope. The CodeRabbit review was COMMENTED, not an approval; no formal qualified approval is recorded.
- PR #18 remains open/unmerged. Do not merge until current-HEAD CI is green and an appropriate technical review is available. Keep one open work PR; M1.3 remains queued behind this PR.
- Safety and procurement status unchanged: M1.1/M1.2 are documentary gates/shortlist only; no production component approval, frozen MPN, purchase, fabrication, installation or energisation. CC613 lifecycle remains unverified and procurement blocked.


## 2026-11-23 13:44 UTC — PR #18 current-HEAD CI confirmation

- To trigger the workflow after the API-created branch synchronization commits, PR #18 was briefly closed and immediately reopened; it remains open and unmerged.
- GitHub Actions run 45186521688, workflow “Validate EVSE documentation links”, ran against exact HEAD 16d02c67b9a39c6c85d2feb2385e91409897cf44 and completed SUCCESS. Job validate-local-markdown-links succeeded, including both “Install CommonMark parser” and “Validate relative links in changed Markdown files”.
- Current compare revalidated: main SHA 847bf54ef7560dff29573a11323b7a84fca43133; branch ahead 7 / behind 0; merge-base equals current main; exactly four intended files in the diff. PR metadata reports open, unmerged, mergeable=true.
- Combined legacy status contexts remain empty; the workflow run itself is the authoritative current-head CI evidence. This workflow only validates relative Markdown links; it does not validate electrical design, ERC, netlist, firmware, CAD or hardware.
- Requested a fresh CodeRabbit review scoped to the exact current four-file diff and HEAD via PR comment ID 7102933412. At the latest review-list query, only the previous COMMENTED review from 07:11 was present; no fresh review/approval yet. The four old workflow threads are outdated after fixes; two old TestStation threads are outside the current diff.
- Merge remains on hold pending fresh technical review. CI is green on current HEAD, but CodeRabbit/qualified review is not yet complete. Do not merge or create another work PR until the review gate is satisfied.


## 2026-11-24 — PR #18 merged; M1.3 recovered and queued

- PR #18 merged successfully, merge commit on main: 5e0e737118bc4cb8ff48ab3de9f4fb6bbcfb15d6. Merge method merge-commit, expected head enforced.
- PR #18 CI documented-link validation run 45186521688 (run #6) succeeded on exact head 16d02c67b9a39c6c85d2feb2385e91409897cf44. Current-head run #7 (45186683650) also reported SUCCESS before merge. This workflow checks changed Markdown local links only, not electrical design, safety, CAD, ERC, netlists, firmware or hardware.
- PR #18 was manually inspected against its four-file diff. CodeRabbit review had six comments: four workflow findings were corrected and verified obsolete on current head; two TestStation findings were on files already in main and out-of-scope. CodeRabbit fresh review allowance was exhausted; no fresh formal approval. Merge proceeded under user standing authorization after CI success, synchronization and manual review of the actual current diff.
- Main now includes M1.1 selection gate and M1.2 evidence-backed shortlist plus CommonMark validator.
- Existing open PR #21 is TestStation: “audit all six TMCS1123 netlist paths”, head c6f19d3b793ba487812627a800e98074bb2f7d6e. It remains the only open PR. Do not open a second PR while #21 remains open, per one-PR-at-a-time rule.
- Created branch recovery/charger-hardware-m1-3-controller-interface from exact merged main SHA 5e0e737118bc4cb8ff48ab3de9f4fb6bbcfb15d6.
- Recovered M1.3 controller interface review from preserved historical branch feat/charger-hardware-v1-component-selection; commit 7f8c5cc2a17305567439778de386e23520491c79. Branch compare is ahead 1 / behind 0, exactly two files: M1.3 controller interface review and index.
- M1.3 recovery was minimally corrected: dated as original 2026-10-30 and recovery 2026-11-24; CC613 explicitly remains historical reference, lifecycle unverified/procurement blocked per M1.2; no controller selection, wiring release, terminal schedule or energisation approval.
- Branch HEAD 7f8c5cc2a17305567439778de386e23520491c79. CI not yet run because no PR opened; PR is queued behind #21. Once #21 merges, open PR for M1.3 and run the document-link workflow, then review findings.
- Current main SHA at this point: 5e0e737118bc4cb8ff48ab3de9f4fb6bbcfb15d6.


## 2026-11-24 18:06 UTC — repository-wide single-PR gate revalidated

- PR #21 remains open and is the sole open PR. It is now reported mergeable=true, but current main is 8 commits ahead of its branch (compare main...work/teststation-u19-u2-followup-interface-reconciliation: ahead 15 / behind 8).
- PR #21 CodeRabbit review remains COMMENTED, with two actionable findings. Both threads are resolved by CodeRabbit, but current HEAD still has no workflow runs or combined status contexts reported. Do not merge until it is synchronized with main, CI evidence is available, and review/manual validation is complete.
- M1.3 recovery branch was created from current main and committed, but no PR opened due the one-open-PR rule. Branch compare remains ahead 1 / behind 0 at the time of initial validation. Revalidate branch/main before opening PR.

## 2026-11-25 14:16 UTC — PR #21 merged; clean M1.3 recovery PR #23 opened

### TestStation PR #21
- PR #21, `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/21`, merged successfully at 2026-11-25 14:14:10 UTC.
- Merge commit on main: `ddd00d18f15a8cb357b5afe35bee6aa0d6aae15a`; previous main parent `5e0e737118bc4cb8ff48ab3de9f4fb6bbcfb15d6`; PR head parent `123608ac647a021cd2a7e68cd68af46a8cc1c427`.
- Exact-head GitHub Actions run #10, ID `45602997699`, workflow “Validate EVSE documentation links”, event `pull_request`, completed SUCCESS on `123608ac647a021cd2a7e68cd68af46a8cc1c427`. Job `validate-local-markdown-links` and all relevant steps completed SUCCESS.
- CI scope is changed Markdown relative-link existence only. It does not validate KiCad ERC/DRC, netlist correctness, electronics, firmware, CAD, hardware, safety or certification.
- CodeRabbit's two inline findings were resolved; one thread was outdated. Manual technical review of the actual three-file PR diff was completed. The report remains strictly documentary/read-only: no schematic, netlist, BOM, PCB, firmware or safety classification changes. No fabrication, purchase, mains energisation or certification approval.
- The merged PR documents six TMCS1123 sensor netlist states, U19 cross-domain joins, physical symbol omissions, ADC pin-polarity naming discrepancy, sensor range/ADC coupling gates and TestStation's three service levels with printable evidence-based reports.

### M1.3 clean recovery and PR #23
- The original queued branch `recovery/charger-hardware-m1-3-controller-interface` became 19 commits behind main after PR #21 and must not be used directly for a new PR.
- Created clean branch `recovery/charger-hardware-m1-3-controller-interface-followup` from exact current main `ddd00d18f15a8cb357b5afe35bee6aa0d6aae15a`.
- Recovered M1.3 controller interface review and reconciled the index on this clean branch. Commit: `2022a7bba93729a5e60ddbfdb2060c618840e1f1`.
- Independent compare `main...recovery/charger-hardware-m1-3-controller-interface-followup`: ahead 1 / behind 0; exactly two files (index and M1.3 controller interface review), 111 additions / 4 deletions.
- Opened PR #23: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/23`; title “docs(evse): recover M1.3 controller interface review”. At opening it was open, non-draft, mergeable=true, one commit and two changed files. It is the sole open work PR.
- At the latest check immediately after opening, no workflow run or combined status context was yet visible for head `2022a7bba93729a5e60ddbfdb2060c618840e1f1`; wait for and verify the actual PR workflow before merge. CodeRabbit/technical review still pending.
- M1.3 remains OPEN evidence gathering. Phoenix Contact CHARX 2902802 is prioritised only for detailed single-output evidence study, not selected. Bender CC613 remains historical multi-point reference; lifecycle unverified and procurement blocked pending written manufacturer confirmation and successor identification. No terminal schedule, wiring release, controller selection, BOM freeze, purchase, energisation or installation approval.
- Next: inspect PR #23 CI and review; resolve findings; merge only when current-head validation and technical review are complete. Maintain one open work PR. Then continue M1.4A Phoenix terminal/interface evidence extraction, followed by M1.4B Bender study only if lifecycle evidence justifies it.

## 2026-11-25 14:16 UTC — PR #23 CI green; M1.3 review correction; M1.4A manufacturer evidence found

### PR #23 latest validation
- PR #23 remains the sole open work PR: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/23`.
- Latest head: `fca8614d4e2bfbe0ecb610bb5943e1739f4bc6cb`; clean compare against main `ddd00d18f15a8cb357b5afe35bee6aa0d6aae15a`: 2 ahead / 0 behind; exactly the index and M1.3 review document.
- Manual review found and corrected a wording contradiction: CC613 was described in one table row as the current multi-point study candidate, while M1.3/M1.2 correctly restrict it to historical reference only. Latest wording consistently says lifecycle unverified and procurement blocked.
- GitHub Actions run #13, ID `45632170192`, completed SUCCESS on exact latest head `fca8614d4e2bfbe0ecb610bb5943e1739f4bc6cb`. Job `validate-local-markdown-links` and all steps passed. Scope remains changed Markdown relative-link existence only.
- CodeRabbit automatic review was paused because the repository has fewer than 10 stars. Explicit `@coderabbitai review` command was accepted and the bot confirmed “Review triggered”; no actual findings/review result had appeared at the latest query. Do not treat the trigger acknowledgement as a completed review.
- PR remains open, mergeable=true, but do not merge until technical review is complete. No controller selection, wiring, schematic, BOM, terminal schedule or energisation release.

### M1.4A Phoenix Contact 2902802 — primary-source research checkpoint (not yet committed to product repo)
- Official Phoenix Contact product page for EM-CP-PP-ETH item 2902802: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802
- Official manufacturer downloads listing was inspected on Phoenix Contact product page. It lists English user manual `um_en_ev_charge_control_104924_en_05.pdf`, revision 05, applicable to EM-CP-PP-ETH device revision 10 or higher; also lists application note revision 03 and 2D/3D product drawing files. The user manual PDF copy inspected was hosted on a third-party mirror, so archive the manufacturer-published official download and verify exact current device revision before treating it as controlled project evidence.
- Manual Rev. 05 identifies terminal functions: LD/EN/24V/ML/XR/GND/ER/LR/VR/GND/CR/24Va/A/B/PE/N/L; PX and CP; locking relays R1–R4; ventilation V1/V2; contactor relay C1/C2. Exact table is manual Section 3.1, printed page 14.
- Manual says 24V output is max 100 mA; 24Va supplies outputs at 7.5–30 V DC; RS-485 A/B is Modbus RTU for an external energy/power meter; C1/C2 relay switches mains to the vehicle through an external contactor. Do not assume C1/C2 can drive any chosen contactor coil: relay max 2 A/250 VAC and switching capacity 1500 VA are hard interface limits to compare against exact coil inrush/holding data and any interposing driver.
- Manual lists 4 digital inputs (24 V nominal, 8 mA; off −3..5 V, on 15..30 V), 4 programmable digital outputs (max 30 V, 0.6 A max/channel), 4 relay outputs (C/V up to 250 VAC, 2 A; R1/R3 and R2/R4 up to 30 VAC/DC, 2 A), 100Base-TX/10Base-T Ethernet with Modbus/TCP, RS-485 Modbus/RTU at 2.4–19.2 kbps (9.6 kbps default), and one supported RS-485 device. Verify exact limits against current official revision before any interface design.
- Contactor feedback: manual Section 7.10, printed page 47, documents monitoring using an NC auxiliary contact and configurable input XR, including Modbus register 390 value 3, 519 delay 500 ms default, and LR output configured for contactor-failure event (register 328 value 35). This is a manufacturer example, not yet an approved VAZÃO safety architecture.
- Residual-current monitoring: manual Sections 7.11–7.12, printed pages 48–49, shows external RCD remote triggering and EV-RCM residual-current monitor integration. This does not replace independent protection coordination or validate a VAZÃO RCD/DC scheme.
- **Catalog/manual discrepancy requiring reconciliation:** current Phoenix Contact product page lists maximum current consumption 40 mA, while the older manual Rev. 05 lists 70 mA at 230 V and 140 mA at 110 V. Do not use either value for PSU sizing until Phoenix confirms current device revision and applicable data.
- Current Phoenix product page lists dimensions 71.6 × 90 × 61 mm, IP20 and operating ambient −25°C to +60°C; manual Rev. 05 gives dimensions in a different order (71.6 × 61 × 90 mm). Treat orientation and enclosure/thermal integration as unapproved until drawing and mounting orientation are reconciled.
- These are research findings only. No M1.4A document or controller terminal schedule has yet been committed. After PR #23 merges, create M1.4A evidence extraction as the next single work PR, cite exact manual pages and retain every unresolved gate. Phoenix 2902802 remains an evaluation candidate, not a selected production controller.

## 2026-11-25 14:23 UTC — M1.3 merged; M1.4A refreshed and PR #24 opened

### M1.3 / PR #23 closure
- PR #23 `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/23` merged successfully.
- Final correction commit before merge: `474b2d9582034233ceb28abc4c9098a1827fdc9e`; merge commit on main: `7d00903c298c765961c43d7437c3efc15dc2b734`.
- CodeRabbit found the remaining contradictory statement that “both remain candidates” in the M1.3 intended-use table row. This was corrected: Phoenix 2902802 is the priority evidence-study candidate for the single-output prototype; Bender CC613 is historical reference only, lifecycle unverified, procurement blocked.
- Latest-head GitHub Actions run #14, ID `45633100244`, completed SUCCESS on exact corrected head `474b2d9582034233ceb28abc4c9098a1827fdc9e`; job `validate-local-markdown-links` passed.
- PR #23 merged after the correction, latest-head CI and manual review. No controller selected and no wiring/energisation released.

### M1.4A — CHARX control advanced 2902802 refreshed; PR #24
- Opened sole work PR #24: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/24`, title “docs(evse): recover M1.4A CHARX advanced interface evidence”.
- Branch: `work/charger-hardware-m1-4a-charx-advanced-manual-audit`, based directly on main `7d00903c298c765961c43d7437c3efc15dc2b734`.
- Head: `e49d190e987c950307174fb683bd8535ca0246f4`; compare is 2 commits ahead / 0 behind; exactly two documentation files changed (M1.4A review and hardware index; 172 additions / 3 deletions).
- M1.4A document distinguishes legacy CHARX control advanced EM-CP-PP-ETH 2902802 from newer CHARX control modular SEC-1000/SEC-3xxx. It does not transfer terminal, supply, backplane, firmware or cluster assumptions between families.
- Official Phoenix product page (https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802) lists English manual `um_en_ev_charge_control_104924_en_05.pdf`, document 104924, revision 05, applicability device revision 10 or higher, manufacturer SHA-256 `6940a22e6bc8cfedacd246a792475bb1ee9d230201b24ac18537964c77a585da`. This checksum is the manufacturer's published value only; PDF not yet archived/downloaded and independently hashed by project.
- M1.4A records terminal/function labels and manual evidence: C1/C2 contactor relay, XR/NC auxiliary feedback example (manual Section 7.10, printed p.47), external RCD remote trigger and EV-RCM integration (Sections 7.11–7.12, printed pp.48–49), RS-485 Modbus RTU one device, Ethernet Modbus/TCP, 4 digital inputs, 4 digital outputs and distinct relay groups. No terminal schedule is released.
- Important unresolved discrepancy: current product page states maximum 40 mA, while manual C05 extraction states 70 mA at 230 V and 140 mA at 110 V. Do not size supply/protection until Phoenix Contact confirms exact revision and applicable value in writing.
- Other gates remain: controlled PDF custody/hash, complete terminal map, contactor coil inrush/holding/suppression, contactor failure response, full RCD/DC protection coordination, meter profile, offline behavior, security/lifecycle and independent engineering review.
- No controller selection, schematic, BOM, procurement, fabrication, mains connection, energisation, installation or certification approval.

### PR #24 current validation state
- PR #24 is the only open work PR. At opening it is mergeable=true; compare 2 ahead / 0 behind.
- At latest query immediately after opening, no workflow run/status was yet visible for head `e49d190e987c950307174fb683bd8535ca0246f4`. Await actual latest-head Markdown-link CI and review before merge.
- Next: verify PR #24 CI, review M1.4A content and any automated findings; do not open another PR until #24 is closed.

## 2026-11-25 14:23 UTC — M1.4A PR #24 merged

- PR #24 `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/24` merged successfully.
- Merge commit on main: `b3d36a9a78272e5e8ef02805c5f654aa9f137777`; previous main `7d00903c298c765961c43d7437c3efc15dc2b734`; PR head `e49d190e987c950307174fb683bd8535ca0246f4`.
- GitHub Actions run #16, ID `45633412654`, completed SUCCESS on exact PR head `e49d190e987c950307174fb683bd8535ca0246f4`. Job `validate-local-markdown-links` passed.
- CodeRabbit automatic review was skipped because repository has fewer than 10 stars; no completed CodeRabbit review claimed. Full two-file diff was manually reviewed. PR was merged under user's standing authorization after latest-head CI and manual review.
- M1.4A is now in main as a refreshed documentary review of Phoenix Contact EM-CP-PP-ETH 2902802 / CHARX control advanced. It remains OPEN and not approved for wiring.
- Main now at `b3d36a9a78272e5e8ef02805c5f654aa9f137777`; no open PRs at verification.
- Remaining hard evidence gate: download official Phoenix C05 PDF into controlled repository archive, independently verify manufacturer-listed SHA-256 `6940a22e6bc8cfedacd246a792475bb1ee9d230201b24ac18537964c77a585da`, and record device revision. Then resolve product-page 40 mA vs manual C05 70 mA at 230 V / 140 mA at 110 V discrepancy in writing.

## 2026-11-25 14:30 UTC — PR #24 merged; M1.23 feeder topology PR #25 opened

### Reconciliation of current repository state
- A fresh GitHub check found PR #23 and PR #24 already merged; the earlier checkpoint saying PR #23 was pending is superseded.
- PR #23 merge commit: `7d00903c298c765961c43d7437c3efc15dc2b734`.
- PR #24 (M1.4A Phoenix CHARX 2902802) merge commit: `b3d36a9a78272e5e8ef02805c5f654aa9f137777`.
- Current `main` at verification: `b3d36a9a78272e5e8ef02805c5f654aa9f137777`.
- PR #24 latest-head Markdown link validation run #16 (`45633412654`) completed SUCCESS on exact head `e49d190e987c950307174fb683bd8535ca0246f4`; job `validate-local-markdown-links` passed.
- M1.4A remains documentary/partial and NOT approved for wiring. Official Phoenix manual C05 PDF is still not archived as a controlled project binary and has not been independently hash-verified. Manufacturer-listed SHA256 is `6940a22e6bc8cfedacd246a792475bb1ee9d230201b24ac18537964c77a585da`; product-page 40 mA vs manual 70 mA at 230 V / 140 mA at 110 V discrepancy remains open.

### M1.23 — dual/quad AC feeder topology and conductor sizing
- User's explicit requirement: dual-output and quad-output products must account for either separate incoming electrical feeders (2 or 4 cables respectively) or one common incoming feeder that locally branches to all outputs. Both arrangements must be engineered and compared.
- Opened PR #25: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/25`, title “docs(evse): define dual and quad AC feeder topology”.
- Branch: `work/charger-hardware-m1-23-ac-feeder-topology`, based directly on current main `b3d36a9a78272e5e8ef02805c5f654aa9f137777`.
- Head: `e077f55cbeee5fd8875ab68ea298978726bc4104`; compare: 1 commit ahead / 0 behind; exactly four documentation files (index, electrical architecture, wiring schedule, new M1.23 design-basis document); 232 additions / 8 deletions.
- New document: `docs/03-engineering/CHARGER-HARDWARE-V1-M1-23-AC-FEEDER-TOPOLOGY-AND-CONDUCTOR-SIZING.md`.
- Updated architecture and wiring schedule to represent:
  - Independent feeders: dual = 2 incoming feeders; quad = 4 incoming feeders.
  - Common feeder: one incoming feeder to a local distribution assembly, then 2 or 4 separately protected branches.
  - Each common trunk and each output branch must have its own conductor calculation.
  - Reference 400 V three-phase, 32 A/output; arithmetic aggregate current envelopes are 64 A dual and 128 A quad if every output simultaneously draws 32 A. These are not breaker ratings or cable selections.
  - Reduced common-feeder capacity can only rely on a validated local load-management limit with sensor/control failure behavior and commissioning evidence; cloud-only limits are insufficient.
  - Cable calculation inputs include conductor material/insulation, installation method, length, ambient/soil temperature, grouping/derating, voltage drop, short-circuit withstand, protective coordination, neutral, PE, terminal limits and Portuguese installation rules.
- No cable cross-section (mm²), breaker, RCD, busbar/distribution block, or preferred topology selected. No procurement or installation approval.
- At PR #25 opening (2026-11-25 14:29:52 UTC), PR is open and mergeable=true; latest head `e077f55cbeee5fd8875ab68ea298978726bc4104`. No Actions workflow run or combined status was visible yet. Must wait for actual CI on this exact latest head and perform manual review before merge.
- PR #25 is the sole open work PR. Do not create another work PR until it is merged/closed.
- Next after PR #25: continue M1.24 on dual/quad feeder distribution and local load-management interface; separately return to M1.4A source custody to obtain/verify the official PDF when a supported binary acquisition path is available.

## 2026-11-25 14:32 UTC — M1.23 PR #25 merged; M1.24 PR #26 opened

### M1.23 / PR #25 closure
- PR #25 `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/25` merged successfully at 2026-11-25 14:30:19 UTC.
- Merge commit on main: `90c38bba92eafdebafa59907958d095729f171a3`; previous main `b3d36a9a78272e5e8ef02805c5f654aa9f137777`; PR head `e077f55cbeee5fd8875ab68ea298978726bc4104`.
- GitHub Actions run #18, ID `45634704957`, completed SUCCESS on exact PR head `e077f55cbeee5fd8875ab68ea298978726bc4104`; job `validate-local-markdown-links` passed.
- PR #25 manually reviewed as a documentation/design-basis change. No cable cross-section, breaker, RCD, busbar, distribution block or preferred feeder topology was selected. No installation or procurement approval.
- M1.23 now merged. Dual/quad topology alternatives are explicit: independent incoming feeders (2 for dual / 4 for quad) versus one common incoming feeder to local distribution with individually protected output branches. Common trunk and every branch require separate installation calculations.
- Reference envelope recorded: 32 A per 400 V three-phase output; aggregate 64 A dual and 128 A quad only if all outputs simultaneously draw 32 A. These are arithmetic design envelopes, not protective-device ratings or conductor selections.
- A reduced common feeder limit can only be relied on after validated local load management with phase measurement, failure behavior and commissioning evidence; cloud-only control is insufficient.

### M1.24 / PR #26 opened
- Opened sole work PR #26: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/26`, title “docs(evse): define local dual and quad load management”.
- Branch: `work/charger-hardware-m1-24-local-load-management`, based on current main `90c38bba92eafdebafa59907958d095729f171a3`.
- Latest head: `0917a3f4f9d0e0f3d3e566524c9d2b1a2176420a`; compare 2 commits ahead / 0 behind; final net diff exactly four files: index, electrical architecture, wiring schedule and new M1.24 document (155 additions / 2 deletions). One corrective preservation commit is present in branch history; final diff is clean and preserves M1.23.
- New document: `docs/03-engineering/CHARGER-HARDWARE-V1-M1-24-LOCAL-LOAD-MANAGEMENT-INTERFACE.md`.
- Defines local energy-manager boundary, phase measurement contract, per-output current allocation, setpoint acknowledgement/timeout, degraded/fail-safe behavior, independent-vs-common feeder implications and commissioning test evidence.
- Explicitly does not claim Phoenix Contact CHARX control advanced 2902802 supports multi-output master/cluster dynamic load management; exact manufacturer evidence required. No energy manager, sensor, protocol, setpoint, fallback current, algorithm, cable or protective device selected.
- At latest check PR #26 open and mergeable=true, no review threads, and no Actions run/status visible yet for exact head `0917a3f4f9d0e0f3d3e566524c9d2b1a2176420a`. Wait for latest-head Markdown-link CI and complete manual review before merge.
- PR #26 is the sole open work PR. Do not create another work PR until it is merged/closed.

### Source custody reminder
- M1.4A Phoenix official manual C05 remains not archived as a controlled binary and not independently hash-verified. Manufacturer-published checksum is recorded, but not project-verified. The 40 mA product-page vs 70 mA at 230 V / 140 mA at 110 V manual discrepancy remains open and must be confirmed in writing by Phoenix before PSU sizing.

## 2026-11-25 14:32 UTC — M1.24 PR #26 merged; next gate M1.25

- PR #26 `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/26` merged at 2026-11-25 14:32:14 UTC.
- Merge commit/current main: `7c47eefd4de2bfb15497b40e39164a81843e187a`.
- Latest-head GitHub Actions run #20, ID `45635071466`, completed SUCCESS on exact PR head `0917a3f4f9d0e0f3d3e566524c9d2b1a2176420a`; job `validate-local-markdown-links` passed.
- PR #26 manually reviewed. Scope is requirements/architecture documentation only. No controller, meter, CT, protocol, setpoint, fallback current, cable, breaker, RCD or algorithm selected. No wiring or energisation approval.
- M1.24 defines local energy-manager boundary, phase measurement requirements, per-output current allocation, local setpoint acknowledgement/timeouts, degraded/fail-safe modes, independent/common feeder behavior and commissioning evidence.
- Current `main` is `7c47eefd4de2bfb15497b40e39164a81843e187a`; zero open PRs verified after merge.
- Next milestone M1.25: compare concrete local energy manager / phase measurement / EVSE-controller setpoint interfaces against M1.24 using current manufacturer manuals and verifiable protocol evidence. Keep Phoenix CHARX control advanced 2902802 unsupported for multi-output load management until explicit evidence is found. No hardware selection by inference.
- Continue the one-open-PR policy: create a clean branch from current main, open one small PR, wait for exact-head CI and review, merge, then create the next branch.
- M1.4A source-custody task remains open separately: obtain official Phoenix C05 PDF, archive original binary and independently verify the manufacturer's listed SHA-256; resolve 40 mA vs 70/140 mA discrepancy with written manufacturer confirmation before PSU sizing.

## 2026-11-25 14:33 UTC — M1.25 candidate matrix PR #27 opened

- PR #27: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/27`, title “docs(evse): compare local load management candidates”.
- Branch `work/charger-hardware-m1-25-load-manager-candidates` based directly on current main `7c47eefd4de2bfb15497b40e39164a81843e187a`.
- Head `a2293db900df49dc522f7c121752296dd4d61050`; compare 1 ahead / 0 behind; exactly two files (index + new M1.25 candidate evidence matrix), 111 additions / 2 deletions.
- M1.25 compares manufacturer-described local load-management candidates: Phoenix Contact CHARX SEC-3xxx; Bender CC613 DLM Master; Versinetic LinkRay; aCharge TELECONTROL; ABB Terra AC local DLM as vendor-specific architecture reference only.
- Critical family distinction: CHARX SEC-3xxx has manufacturer-described embedded higher-level load-management functions; SEC-1000 is a different configuration and must not inherit SEC-3xxx claims; legacy CHARX control advanced 2902802 from M1.4A is a different family and is not proven multi-output capable.
- Bender CC613 DLM docs describe Master + external Modbus/Ethernet meter, but lifecycle/support and exact order code remain unconfirmed; procurement stays blocked pending written manufacturer confirmation.
- No manager, meter, CT, protocol, cable, protection, BOM or wiring selected. Vendor feature claims are research evidence only, not VAZÃO acceptance.
- At latest check PR #27 open and mergeable=true, no review threads and no workflow run visible yet for exact head `a2293db900df49dc522f7c121752296dd4d61050`. Wait for exact-head Markdown-link CI and manual review before merge.
- PR #27 is the sole open work PR. Do not create another work PR until it is merged/closed.
- AndreOS Memory was updated with M1.23/M1.24 merges and M1.25 current state; this checkpoint extends that history.

## 2026-11-25 14:33 UTC — M1.25 PR #27 merged

- PR #27 `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/27` merged successfully at 2026-11-25 14:33:36 UTC.
- Merge commit/current main: `52b8afad47643abf4bdd72f4ecd5effb0b35e766`.
- GitHub Actions run #22, ID `45635329264`, completed SUCCESS on exact PR head `a2293db900df49dc522f7c121752296dd4d61050`; job `validate-local-markdown-links` passed.
- Manual review completed for the two-file documentary diff. No controller/manager/meter/CT/protocol selection, wiring, cable or protective rating released.
- M1.25 now in main: candidate evidence matrix for Phoenix Contact CHARX SEC-3xxx, Bender CC613 DLM, Versinetic LinkRay, aCharge TELECONTROL and ABB Terra AC as vendor-specific reference. All remain unselected pending technical packs and compatibility/fail-safe verification.
- Current main `52b8afad47643abf4bdd72f4ecd5effb0b35e766`; zero open PRs verified after merge.
- Next: M1.26 supplier technical evidence intake/RFI package, without contacting suppliers or claiming responses. Keep one open PR at a time.

## 2026-11-25 14:34 UTC — M1.26 supplier RFI PR #28 opened

- M1.25 PR #27 merged at 14:33:36 UTC; merge/current main at that point `52b8afad47643abf4bdd72f4ecd5effb0b35e766`. Exact-head GitHub Actions run #22 (`45635329264`) succeeded.
- Opened sole work PR #28: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/28`, title “docs(evse): prepare supplier technical evidence request”.
- Branch `work/charger-hardware-m1-26-supplier-evidence-rfi` based on `52b8afad47643abf4bdd72f4ecd5effb0b35e766`; head `d2f0e7ff26a9e59f354328a547e3af903b32b44f`; compare 1 ahead / 0 behind; exactly two files (index and new M1.26 RFI template), 154 additions / 2 deletions.
- New file `docs/03-engineering/CHARGER-HARDWARE-V1-M1-26-SUPPLIER-TECHNICAL-EVIDENCE-REQUEST.md` is an internal, reusable supplier technical evidence request. It asks for exact model/revision, topology/scale, phase measurement, per-output setpoint semantics, Modbus/API maps, timeout/acknowledgement, fail-safe behavior, electrical data, cybersecurity, lifecycle and controlled document custody. Includes specific questions for Phoenix SEC-3xxx, Bender CC613, Versinetic LinkRay and aCharge TELECONTROL.
- RFI explicitly marked NOT SENT. No supplier contact, response, product selection or compatibility claim.
- At opening PR #28 open and mergeable=true; no workflow run visible yet for exact head `d2f0e7ff26a9e59f354328a547e3af903b32b44f`. Await latest-head Markdown-link CI and manual review before merge.
- PR #28 is the only open work PR. Do not create another until it is merged/closed.

## 2026-11-25 14:34 UTC — M1.26 PR #28 merged

- PR #28 `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/28` merged successfully at 2026-11-25 14:34:46 UTC.
- Merge commit/current main: `5236b9258879bc127441495c7ccc39814b69222e`.
- GitHub Actions run #24, ID `45635539075`, completed SUCCESS on exact PR head `d2f0e7ff26a9e59f354328a547e3af903b32b44f`; job `validate-local-markdown-links` passed.
- M1.26 internal supplier technical evidence request template is now merged. It remains explicitly NOT SENT. No supplier contacted and no responses claimed.
- The RFI requests exact product/order code and revision, point count/topology, phase measurement, setpoint/acknowledgement, Modbus/API maps, timeouts, fault behavior, electrical data, cybersecurity, lifecycle and controlled-document custody. Includes candidate-specific questions for Phoenix SEC-3xxx, Bender CC613, Versinetic LinkRay and aCharge TELECONTROL.
- Current main `5236b9258879bc127441495c7ccc39814b69222e`; zero open PRs verified after merge.
- M1.23/M1.24/M1.25/M1.26 are merged. Dual/quad feeder options and load-management requirements are documented; candidate selection and cable sections remain open.
- Next useful engineering step: M1.27 local load-management verification plan / TestStation acceptance matrix, independent of supplier response timing. Supplier RFI must only be sent after user authorizes actual external contact.

## 2026-11-25 14:35 UTC — M1.27 TestStation acceptance plan PR #29 opened

- PR #28 M1.26 was merged at 14:34:46 UTC; merge/current main at that time `5236b9258879bc127441495c7ccc39814b69222e`. Exact-head Actions run #24 (`45635539075`) passed.
- Opened sole work PR #29: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/29`, title “docs(evse): define load management TestStation acceptance plan”.
- Branch `work/charger-hardware-m1-27-load-management-test-plan`, based directly on main `5236b9258879bc127441495c7ccc39814b69222e`; head `570e731c9b98d8153a07c1b16e2228e96747aa3c`; compare 1 ahead / 0 behind; exactly two files (index and new M1.27 test plan), 130 additions / 2 deletions.
- New M1.27 defines three TestStation service levels: technician quick verification, service/fault diagnosis, and factory/development validation. Every level must produce a traceable report; test status distinguishes PASS/FAIL/NOT RUN/INCONCLUSIVE.
- Defines 20 test cases for phase mapping, measurement accuracy, dual/quad demand, allocation/fairness, phase asymmetry, new-session admission, sensor and bus faults, watchdog/reset, stale commands, configuration corruption, cloud loss, restoration, stability, and common/independent feeder modes.
- Requires Level 3 factory validation with calibrated references, raw data, event timeline, firmware/config hashes and reviewer approval before using DLM to justify reduced common-feeder capacity.
- No tests claimed executed, no numeric tolerances invented, no hardware selected, no cable/protection ratings approved.
- At latest check PR #29 open and mergeable=true, no workflow run visible yet for exact head `570e731c9b98d8153a07c1b16e2228e96747aa3`. Await latest-head Markdown-link CI and manual review before merge.
- PR #29 is the sole open work PR. Do not create another work PR until it is merged/closed.


## 2026-11-26 06:18 UTC — M1.27 PR #29 merged; charger-only focus reaffirmed

- User clarified the scope of the active VAZÃO EVSE development conversation: develop the chargers exclusively. Follow the TestStation only insofar as its capabilities need to adapt to charger development/validation; do not make TestStation itself the product-development focus here.
- PR #29 https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/29 was revalidated on its final head 6fd3de232f16165b7230964392a78bcf9782bd47. GitHub Actions run #27, ID 45662493710, completed SUCCESS; job validate-local-markdown-links passed. Manual review covered the full two-file diff and its acceptance-state corrections.
- PR #29 merged successfully at 2026-11-26 06:18:39 UTC. Merge commit/current main: 49d69457d905d507197f2773532310411296fc40. Post-merge compare main versus merge commit was IDENTICAL (0 ahead / 0 behind).
- M1.27 remains a test-plan baseline only. It defines 20 load-management tests and TestStation evidence/report requirements; no physical tests are claimed executed and no hardware/cable/protection is approved.

## 2026-11-26 06:20 UTC — M1.28 Output Cell architecture PR #30 opened

- Created branch work/charger-hardware-m1-28-output-channel-architecture directly from current main 49d69457d905d507197f2773532310411296fc40.
- Opened sole active work PR #30: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/30, title “docs(evse): define repeatable output channel architecture”.
- Head a92a40675520999b4b7a7b60d68347179f055e6e; compare 2 commits ahead / 0 behind; exactly two files changed: index and new docs/03-engineering/CHARGER-HARDWARE-V1-M1-28-REPEATABLE-OUTPUT-CHANNEL-ARCHITECTURE.md (249 additions / 2 deletions).
- M1.28 defines one repeatable Output Cell for Single, Dual, Quad, Wallbox and future MultiStation variants; local safety authority per output; shared assemblies; control hierarchy; logical operating states; preconditions for charging; current-limit contract; switching/feedback and protective boundary; separation of feeder, diagnostic and revenue metering; fault containment/recovery; optional module classes; required interface evidence; variant verification matrix.
- M1.28 is functional architecture only. No EVSE MCU, contactor, meter, RCD/RCM, cable, terminal, protocol, protection rating, fallback current, schematic, BOM or component has been selected. No mains energisation, physical test or compliance approval is claimed.
- No workflow run was visible immediately after PR #30 creation; await exact-head CI and manual review before merge. PR #30 is the only open work PR.
- Next milestone M1.29: requirements-to-interface matrix for the exact single-output V1 prototype, tracing safety, measurement, power switching, communications and service interfaces to manufacturer-evidenced parts or explicit open decisions.


## 2026-11-26 06:20 UTC — M1.28 PR #30 merged

- PR #30 https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/30 merged successfully at 2026-11-26 06:20:58 UTC.
- Exact-head GitHub Actions run #29, ID 45767519066, completed SUCCESS on head a92a40675520999b4b7a7b60d68347179f055e6e; job validate-local-markdown-links passed.
- Manual review completed on the exact two-file diff. Merge commit/current main: bc39cafd70c4efd4e5ce3aebb94b57f5d4eb01ca. Post-merge compare main versus merge commit was IDENTICAL (0 ahead / 0 behind).
- M1.28 is now merged: repeatable Output Cell architecture and operating-state model for Single, Dual, Quad, Wallbox and MultiStation. It establishes local safety ownership per output, shared-vs-channel functions, authority hierarchy, charging preconditions, current-limit contract, feedback/fault containment, measurement separation, optional-module boundary and evidence gates.
- No component, controller, contactor, meter, protection, cable, terminal, protocol, fallback value, schematic or BOM was selected. No physical tests, energisation or compliance approval claimed.
- PR #30 is closed/merged. The next product milestone is M1.29: requirements-to-interface traceability for the exact single-output V1 prototype. Continue one open PR at a time.
- AndreOS Memory commit recording this checkpoint: 1c82931e5edc79ac0e588039b1161619ebc89455.

## 2026-11-26 06:22 UTC — M1.29 single-output interface traceability PR #31 opened

- PR #30 M1.28 merged at 06:20:58 UTC; exact-head Actions run #29 (ID 45767519066) succeeded and manual review passed. Main is bc39cafd70c4efd4e5ce3aebb94b57f5d4eb01ca.
- Created branch work/charger-hardware-m1-29-single-output-interface-traceability from that exact main commit.
- Opened sole work PR #31: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/31, title “docs(evse): trace single-output prototype interfaces”.
- Head fcc0cf07407d51443e4ed8e019dd2036a4f67610; compare 2 commits ahead / 0 behind; exactly two files changed (index and new M1.29 traceability matrix), 142 additions / 2 deletions.
- M1.29 registers 24 interfaces for the first single-output V1 prototype: AC input/isolation, overcurrent, residual-current/DC, surge, PE, CP/PP, safety controller, application processor, contactor/driver, per-output metering, feeder measurement, local energy manager, auxiliary SELV, fieldbus, network, RFID, HMI, thermal, enclosure, service/TestStation interface, event storage/RTC, firmware integrity, internal conductors/terminals and Type 2 connector.
- Each interface is classified as REQ DEFINED, CANDIDATE ONLY, EVIDENCE GAP or OPEN. Existing Phoenix SEC-1000 and 2902802 controller candidates, Carlo Gavazzi EM340/EM24 meter candidates and M1.25 load-manager candidates are recorded without selection.
- Key unresolved gates retained: target installation supply/earthing/fault current; RCD/DC architecture; exact controller evidence; contactor/coil/feedback; complete auxiliary load budget; exact meter certificate and Portuguese billing applicability; feeder measurement boundary; enclosure/thermal design; cable/terminal calculation. Phoenix 2902802 controlled manual custody and 40 mA versus 70/140 mA consumption discrepancy remain open.
- No component, protection rating, cable section, PSU wattage, coil voltage, CP threshold, protocol, schematic, BOM, mains energisation or compliance approval is claimed.
- No workflow run was visible immediately after PR #31 creation; await exact-head CI and manual review. PR #31 is the only open work PR.
- AndreOS Memory update commit: bb5724181709b1cb0ec76d9de11d82591d1698a3 (M1.29 PR checkpoint will be appended in a subsequent memory commit).


## 2026-11-26 21:24 UTC — M1.29 PR #31 merged; M1.30 controller evidence PR #32 opened

- PR #31 https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/31 merged at 21:23 UTC after exact-head GitHub Actions run #31 (ID 45767711854) SUCCESS. Manual diff review completed. Merge commit/current main: 802ec5e13c35c2edf9eb3263aea8692b933bca2f; post-merge compare IDENTICAL (0 ahead/behind).
- M1.29 is merged: 24 single-output prototype interfaces traceable; no components, cable/protection values, PSU rating, schematic/BOM or energisation approved.
- M1.30 controller evidence review created in `docs/03-engineering/CHARGER-HARDWARE-V1-M1-30-EVSE-CONTROLLER-EVIDENCE-REVIEW.md`; index updated.
- Current official Phoenix product pages (reviewed 2026-11-26) list SEC-1000 1139034 supply 12 V DC ±5%, max 2 A stand-alone, <50 mA no-load without external loads; meter/RFID/DC residual-current peripherals listed. This makes supply budget and exact modular peripheral compatibility priority gates.
- Official current catalog for EM-CP-PP-ETH 2902802 lists max 40 mA, <1 W no-load, Ethernet Modbus/TCP, RS-485 and one point. Historical 40 mA vs 70/140 mA discrepancy is narrowed but remains partially unresolved pending exact controlled manual revision, binary custody and hash verification. No supplier contacted.
- M1.30 PR #32: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/32, branch `work/charger-hardware-m1-30-controller-evidence-review`, opened 2026-11-26 21:23 UTC. Initial head 313025f03f0ce73c7c4b53cbf4cd04488e61c95b; corrective index commit 2e22f5f07f4aab1b5e235b959c5008de4ac37497 fixes accidental literal newline. Re-fetch PR exact head and CI before review/merge. Two-file documentary change, no controller selection or design release.
- Source pages: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034 and https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802. Pages reviewed, not archived; no PDF SHA verified.
- Next milestone after PR32: controlled-document custody and protection architecture evidence matrix, focusing RCD/DC detection, contactor feedback, local safe-state behavior, installation assumptions. Do not freeze schematic/BOM until evidence and calculations complete.
- Continue charger-only scope; TestStation is only a verification aid. One open PR at a time.


## 2026-11-27 05:11 UTC — M1.30 merged; M1.31 protection architecture PR #33 opened

- PR #32 M1.30 controller evidence review merged at 2026-11-27 05:11 UTC. Exact head CI run #34 / ID 45897854759 SUCCESS; markdown relative-link validation passed. Merge commit 63d29427e2a0093c2b796663dd02f7927a11bc12f. Post-merge compare main vs merge: IDENTICAL.
- M1.30 captures catalog evidence for Phoenix SEC-1000 1139034 (12 V DC ±5%, max 2 A standalone, modular meter/RFID/DC residual detection peripheral interfaces) and EM-CP-PP-ETH 2902802 (catalog 40 mA, <1 W no-load, Ethernet Modbus/TCP, RS-485, single point). Controller remains unselected; PDFs not archived/hash-verified; no supplier contact.
- PR #33 M1.31 Protection Architecture Evidence Matrix: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/33, branch work/charger-hardware-m1-31-protection-architecture-evidence, current head fbaa94ac35ffeba1e6f108c9a30b0d484f9dcd8c. Open; CI not yet surfaced at checkpoint. Documentary change (index + 113-row-line protection evidence doc), 16 protection-function gates P-01–P-16 all OPEN.
- M1.31 defines protection boundary, local safe-state contract, function/hazard matrix, standards-family review targets (editions/applicability not verified), input dependencies and schematic release gates. No breaker/RCD/RDC-DD/SPD/contactor/cable/controller selected, no thresholds/sections, no schematic/BOM, no energisation or tests claimed.
- Current main is 63d29427e2a0093c2b796663dd02f7927a11bc12f after M1.30. Continue only charger development; TestStation is verification aid. One open PR at a time.
- Next milestone: M1.32 contactor/switching/feedback architecture evidence, requiring design input assumptions and controlled manufacturer docs before candidate ratings or selection.


## 2026-11-27 05:12 UTC — M1.31 protection architecture matrix merged

- PR #33 https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/33 merged at 05:12 UTC. Exact-head Actions run #37 / ID 45944357686 SUCCESS; local Markdown link validation passed. Merge commit/current main: f486712f3592be684d1566e34d108743d2ca22a8; compare main vs merge IDENTICAL.
- M1.31 matrix P-01 through P-16 establishes protection functions and required evidence (isolation, overcurrent, residual AC/DC, PE/bonding, contactor, CP/PP, surge, thermal, connector, auxiliary, metering separation, safe state, output fault containment, service interface, emergency/service stop). All gates remain OPEN.
- Standards families are only review targets; editions, Portuguese/EU scope and applicability remain unverified. No breaker/RCD/RDC-DD/SPD/contactor/cable/controller selected; no trip values or conductor sections; no schematic/BOM or mains tests.
- Current main after PR #33: f486712f3592be684d1566e34d108743d2ca22a8. No open PR at checkpoint.
- Next M1.32: contactor/switching and feedback interface architecture; first document required ratings, fail-state, welded-contact detection, feedback signal, isolation and controller boundary. Candidate rating selection deferred until supply/installation/fault assumptions and exact controlled manufacturer docs.


## 2026-11-27 05:13 UTC — M1.32 contactor feedback architecture PR #34 opened

- PR #33 M1.31 Protection Architecture merged; exact-head run #37 / ID 45944357686 SUCCESS. Main/merge compare identical at f486712f3592be684d1566e34d108743d2ca22a8.
- PR #34 https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/34, branch work/charger-hardware-m1-32-contactor-feedback-architecture. Initial head 362cb87a4eb48a70cbd3683fe6cb569817fddf2c; corrected index commit d5077d68e37906d88eedaa99032348132d7b1b81. Exact current head needs re-fetch before final review. CI run #39 / ID 45944479418 started; parser installation in progress at checkpoint.
- M1.32 defines switching/contactor function requirements SW-01..SW-15, feedback truth-table semantics, selection prerequisites, and 8 verification tests SW-T01..SW-T08 (NOT RUN). No contactor/relay/coil/poles/ratings/feedback method/suppression selected. No schematic/BOM or mains test/energisation claimed.
- After PR34 closes, next M1.33: complete auxiliary power budget evidence matrix across controller, coil, sensors, residual-current interfaces, meters, RFID, comms, HMI and options, including steady, peak and inrush; do not size PSU until exact manufacturer data captured.
- Current project main at M1.31 merge: f486712f3592be684d1566e34d108743d2ca22a8. One open PR only; charger-only focus.


## 2026-11-27 06:53 UTC — M1.32 merged; M1.33 auxiliary power budget PR #35 opened

- PR #34 `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/34` merged successfully at 06:51:11 UTC. Exact final head `d5077d68e37906d88eedaa99032348132d7b1b81`; Actions run #40 / ID `45944493751` completed SUCCESS, including `validate-local-markdown-links`. Manual review covered the exact two-file diff. Merge commit/current main: `2d6ae913a28cf223b8cb98106b8a87246576f718`; post-merge compare main vs merge: IDENTICAL.
- M1.32 is now merged: switching/contactor requirements SW-01..SW-15, feedback truth-table semantics, safe-state contract, selection prerequisites and verification seeds SW-T01..SW-T08 (NOT RUN). No actuator, coil voltage, poles, current/fault ratings, feedback device or suppression selected; no schematic/BOM or energisation.
- Created M1.33 branch `work/charger-hardware-m1-33-auxiliary-power-budget` from exact main `2d6ae913a28cf223b8cb98106b8a87246576f718`.
- Opened sole work PR #35: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/35`, title “docs(evse): add M1.33 auxiliary power budget evidence matrix”. Current exact head `dc0201a1898a3aae58f7a55d6fb97b327792f430`; 2 files (index + new M1.33 document), 113 additions / 2 deletions. The index line-break issue introduced in the first edit was corrected and the final patch re-fetched; it now contains clean separate M1.32/M1.33 list entries.
- M1.33 inventories 16 load groups: controller, peripheral interfaces, actuator coil, feedback, residual-current interface, meter, RFID/NFC, Ethernet, LTE, HMI, payment, sensors, cooling, local load manager, optional printer and service/diagnostic interface. It separates per-cell/shared loads for Single, Dual, Quad and MultiStation and defines steady, peak, startup/inrush, pickup/hold and simultaneity calculations.
- Phoenix CHARX SEC-1000 figures are carried forward only as M1.30 catalog evidence (12 V DC ±5%, max 2 A standalone, <50 mA no-load without external loads); controlled manual revision, external-load profile and startup profile remain OPEN. The 2 A figure is explicitly not used to size a system supply.
- All M1.33 gates AP-01..AP-10 remain OPEN. No auxiliary PSU, rail, fuse, conductor, converter, margin or distribution topology selected. No tests, schematic/BOM freeze or energisation claimed.
- PR #35 was open/mergeable at creation. No workflow run or combined status was visible for final head `dc0201a1898a3aae58f7a55d6fb97b327792f430` at 06:53 UTC; CI is PENDING/UNOBSERVED. Do not merge until exact-head CI success and manual review. PR #35 is the only open work PR.
- Current product main `2d6ae913a28cf223b8cb98106b8a87246576f718`. Next action: re-fetch PR #35 exact head and CI, inspect final patch, then merge only if all checks pass. Next engineering work after M1.33: obtain/retain controlled manufacturer documents and populate actual load values before any auxiliary supply selection. Charger-only focus remains; TestStation is only a verification aid.


## 2026-11-27 06:53 UTC — M1.33 PR #35 merged

- PR #35 `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/35` is confirmed closed/merged at 06:52:54 UTC. Exact final PR head `dc0201a1898a3aae58f7a55d6fb97b327792f430`; GitHub Actions run #44 / ID `45954669420` completed SUCCESS. Job `validate-local-markdown-links` and changed-Markdown relative-link validation passed.
- Merge commit returned by GitHub: `1b40720e26b0d9cdf72cf7d096c99741fc9de532`. A post-merge compare request against `main` returned GitHub API 404 twice, so main-vs-merge identity is NOT YET VERIFIED. Do not claim compare identical until a fresh main ref and compare are obtained.
- M1.33 is integrated according to PR metadata. It documents 16 auxiliary load groups, Single/Dual/Quad/MultiStation quantity model, shared/per-output allocation, steady/peak/startup/inrush/pickup/hold methodology, and evidence gates AP-01..AP-10. All gates remain OPEN. No PSU, voltage rail, fuse, conductor, converter, design margin or auxiliary distribution topology selected; no tests, schematic/BOM freeze or energisation claimed.
- Product main at PR #35 base was `2d6ae913a28cf223b8cb98106b8a87246576f718`; PR merge commit is `1b40720e26b0d9cdf72cf7d096c99741fc9de532`. No new work PR opened yet. Revalidate default branch head/compare before opening the next branch.
- Next milestone candidate M1.34: controlled manufacturer-document custody and auxiliary load evidence intake. Priority: exact SEC-1000 controlled manual/revision and complete peripheral/extension load profile; identify candidate contactor coil data only after system input assumptions; retain original source files and SHA-256, separate catalog-level evidence from controlled technical evidence. Do not invent values or contact suppliers without user authorisation.


## 2026-11-27 14:55 UTC — M1.34 controlled-document intake PR #36

- Revalidated PR #35 merge integration: compare from its parent `2d6ae913a28cf223b8cb98106b8a87246576f718` to merge commit `1b40720e26d0b9cdf72cf7d096c99741fc9de532` returned ahead_by=5, behind_by=0 and exactly the intended 2 changed files (index + M1.33 doc). This validates the merged content against the parent baseline; it is not a fresh compare to current main.
- Official Phoenix Contact Portugal product page was reviewed for CHARX SEC-1000 item 1139034; catalog details remain preliminary. Discovery also surfaced a third-party manual listing claiming CHARX SEC user manual, firmware 1.6.2, revision 05, date 2024-09-09 and SEC-1000 applicability. This third-party listing is E0 discovery only; official source download, file custody and hash remain OPEN. Public sources: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034 and https://www.notice-facile.com/en/manual/1428556/phoenix%2Bcontact%2Bcharx-sec-1000.
- Opened sole work PR #36: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/36`, branch `work/charger-hardware-m1-34-controlled-document-evidence-intake`. It contains M1.34 evidence classifications E0–E5, document custody and SHA-256 workflow, controller source register, claims SEC-C01..C10, intake gates DI-01..DI-09, and index update. No document file was downloaded or archived; no hashes claimed.
- Initial index update contained literal backslash-n formatting; corrected through a subsequent commit. Exact final head at this checkpoint `c6e98409623acee90aa010f25287253148999f27`; the patch was re-fetched after correction. Workflow runs were not yet visible and combined status had no checks at this timestamp; CI is PENDING/UNOBSERVED. Do not merge until exact-head CI success and manual patch review.
- M1.34 does not select controller, PSU, rail, fuse, conductor, converter, margin, distribution topology; no schematic/BOM freeze, tests or energisation. The one-open-PR rule is being followed.


## 2026-11-27 14:56 UTC — M1.34 merged; M1.35 PR #37 opened

- PR #36 M1.34 merged and confirmed: CI run #48 / ID `46020152578` SUCCESS; Markdown link validation passed. Merge commit `937312ac71d7a0726c83d081d89aa76e489f26ad`. Compare from prior merge `1b40720e26d0b9cdf72cf7d096c99741fc9de532` to M1.34 merge: ahead_by 5, behind_by 0, exactly index + M1.34 doc. 
- Official Phoenix Contact PT product page was inspected and catalog claims reviewed, but the official download link was not successfully resolved into a downloadable controlled manual. Third-party manual reference remains discovery only; no PDF archived, no hash and no supplier contact.
- Sole open work PR #37: `https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/37`, branch `work/charger-hardware-m1-35-controller-catalog-claims-review`, current head `66d55fd10169e2b217c3cf63de5b244d11a9ddb7`. M1.35 conservative interpretation review of controller catalog claims CC-01..CC-11 and gates G-CC1..G-CC7; index updated. Review warns not to assume four 600 mA outputs simultaneously, or infer contactor coil compatibility from floating contact rating. No controller selected, no M1.33 numeric budget update, no PSU/rail/fuse/conductor selection, no schematic/BOM/test/energisation.
- PR #37 exact-head workflow run #50 / ID `46020364959` is IN PROGRESS; parser setup underway, link-validation pending. Diff inspected and is limited to 2 intended documents. Merge only after exact-head CI success and manual review.
- M1.34/35 and main integration state; next step controlled manual retrieval through official manufacturer channel, exact original file custody + SHA-256, page-referenced review, then M1.33 update. One open PR rule followed.


## 2026-11-27 14:57 UTC — M1.35 PR #37 merged

- PR #37 merged after exact-head CI success. Run #50 / ID `46020364959` SUCCESS; Markdown relative-link validation passed. Exact PR head `66d55fd10169e2b217c3cf63de5b244d11a9ddb7`; merge commit `b76e735cc1fc6940033b3daca96e05c4a3c9d6ea`.
- Post-merge compare from M1.34 merge `937312ac71d7a0726c83d081d89aa76e489f26ad` to M1.35 merge: ahead_by 3, behind_by 0; exact intended files index + M1.35 document.
- M1.35 catalog interpretation matrix CC-01..CC-11 and gates G-CC1..G-CC7 merged. It explicitly prevents treating 4 x 600 mA outputs as simultaneous system capacity or controller floating contact as coil supply/compatibility. Catalog evidence only; manual still OPEN.
- No current open work PR after merge at this checkpoint. Continue next small PR, starting from exact merge SHA. Next practical task: create a manufacturer document-request / controller evidence questions matrix, without claiming outreach, to identify specific data needed to resolve M1.33 and controller gates.
