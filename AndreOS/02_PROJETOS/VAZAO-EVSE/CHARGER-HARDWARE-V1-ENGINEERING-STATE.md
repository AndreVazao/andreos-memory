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
