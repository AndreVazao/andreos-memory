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
