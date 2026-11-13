# AndreOS Memory — VAZÃO EVSE TestStation V1 / KiCad engineering state

**Checkpoint:** 2026-11-13 UTC  
**Product repo:** `AndreVazao/VAZAO-EVSE-Platform`  
**Active review branch:** `review/teststation-physical-symbol-migration`  
**Active PR:** [#7 — EVSE: add review-only PBS footprint candidate and geometry guard](https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/7)  
**Boundary:** PR #7 is to remain Draft/open/unmerged. Never merge, change production master, or approve fabrication without André's explicit authorization and closure of engineering gates.

## Project safety rules

- Production master: `hardware/teststation/V1/CAD/schematics/TS-V1-M2.9-K-MASTER.kicad_sch` — do not alter.
- Immutable legacy baseline: `hardware/teststation/V1/CAD/schematics/TS-V1-M2.9-F-MASTER-BASELINE.sch` — preserve byte-for-byte.
- Review-only baseline and migration copies are evidence artifacts, not a golden circuit.
- All future schematic/wiring changes must be in a separate review-only copy/branch. Do not auto-repair based on ERC, visual proximity, or legacy net coincidence.
- Evidence before assumptions. Keep every approved-destination field blank until circuit requirements and qualified review establish it.
- No PCB fabrication, EV connection, mains energisation, or production release is authorized by these checks.

## Latest verified branch and CI state

Latest documentation commits:
- Manufacturer interface evidence review: `d9304b0ec6c79f2381efdec17309873e6cabcd9f`.
- Review workspace README update: `dd269125736bc3d667142c213d6304f9457959b1`.

The evidence review file was fetched back from the review branch and verified:
`hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-K-TMCS1123-A3-ADS131M06-INTERFACE-EVIDENCE-REVIEW-2026-11-13.md`.

Successful CI:
- [Physical migration #38](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/43414417330): geometry, native KiCad 10 footprint load, baseline/migrated schematic exports and evidence upload passed.
- [Verified-symbol/intent #87](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/43414417367): static pin maps; U2/U19 21-pin matrix; all-six TMCS1123 60-pin matrix; KiCad 10 native footprint loads; symbol export; master ERC/netlist export; connectivity audit and ERC triage passed.

Both workflows completed on the pre-documentation code/data head. The two subsequent commits are documentation-only and do not change schematics, symbols, matrices, validators or workflow code. Do not treat these CI runs as validation of any new wiring or as electrical approval.

PR #7 was re-fetched on 2026-11-13 and confirmed open. Its existing description states Draft/unmerged and prohibits production merge. The PR was given a new comment (ID `6852065260`) recording CI #38/#87 and the new manufacturer evidence review. No merge action was performed.

## Root cause and known migration impact

Shared symbol changes affect all six TMCS1123 sensors U15–U20 and both ADS131M06 ADCs U1/U2.

### TMCS1123 anchor displacement

The old schematic geometry is unchanged while physical pin anchors move in the complete symbol. The migrated export consequently captures phase labels on the wrong physical functions for all six sensors:
- Pin 8 VS is attached to the old phase-current label `/<ZONE>_<PHASE>_I`.
- Pin 9 VOC is attached to the old phase-return label `/<ZONE>_<PHASE>_I_RET`.
- Pin 5 VREF loses that old return label.

These are geometric anchor-displacement observations, not intended/approved connectivity. No wires or labels were repaired.

U19 also had suspicious baseline connections:
- U19 pin 3 GND ↔ U2 pin 17 CS.
- U19 pin 2 IN− ↔ U2 pin 20 DOUT.
- U19 pin 8 VS ↔ U2 pin 19 SCLK.

These are incompatible by function and must not be restored. The migration removed these suspicious coincidences; replacement destinations remain TBD.

### ERC interpretation

Earlier baseline/migrated comparison:
- Baseline: 353 messages (300 errors, 53 warnings).
- Migrated: 436 messages (383 errors, 53 warnings), +83 errors.

The +83 is not 83 new electrical faults. The detailed rule delta includes +54 `pin_not_connected` from newly represented physical pins (42 ADS131M06 + 12 TMCS1123), +26 `pin_not_driven`, +10 `power_pin_not_driven`, and reductions in dangling-label/wire endpoint and pin-to-pin findings. Some label endpoints now attach to the wrong VS/VOC pins. The raw ERC total is a mixed symbol-completeness/type-correction/anchor-displacement signal, not a quality score. Neither baseline nor migrated connectivity is approved.

## Machine-readable review guards

- `hardware/teststation/V1/CAD/verification/netlist/M2.9-K-U2-U19-PIN-TO-NET-INTENT-REVIEW.csv`: 21 rows covering selected physical pins on U2/U19; all approved destinations blank.
- `hardware/teststation/V1/CAD/verification/scripts/validate_u2_u19_intent_review.py`: validates exact functions, observed nets and no approved destinations.
- `hardware/teststation/V1/CAD/verification/netlist/M2.9-K-TMCS1123-ALL-CHANNELS-MIGRATION-IMPACT.csv`: 60 rows, all 10 pins on U15–U20; all approved destinations blank.
- `hardware/teststation/V1/CAD/verification/scripts/validate_tmcs1123_migration_impact.py`: validates six references, pin/function/type maps, observed net names, anchor displacement and suspicious U19 baseline pairings.
- `.github/workflows/validate-evse-symbol-library.yml`: runs both matrix guards and symbol/footprint/KiCad validation.
- `.github/workflows/validate-evse-symbol-migration.yml`: review-only schematic/footprint migration checks.

## Manufacturer evidence — 2026-11-13

### TMCS1123A3AQDVGR (U15–U20)

TI datasheet SBOSA24D Rev. D, revised May 2026:
- Exact orderable A3 part is ACTIVE, production, SOIC DVG 10-pin.
- Sensitivity: 75 mV/A.
- Supply range: 3.0–5.5 V.
- Listed linear range at 5 V: −32 A to +32 A.
- Listed linear range at 3.3 V: −32 A to +9.3 A. Do not assume symmetric ±32 A at 3.3 V.
- Device-comparison table lists no zero-current output voltage for A3; do not assume the 1.65 V VREF arrangement of B1/B3.
- Pin 4 ALERT and pin 7 OC are active-low open-drain; if unused TI says connect to GND.
- Pin 5 VREF may be left floating if unused; exact A3 behaviour must be confirmed before using it as a measurement return.
- Pin 9 VOC sets overcurrent threshold; if unused TI says connect to VS.
- Pin 10 NC may be connected to GND or left floating.

Sources:
- https://www.ti.com/lit/ds/symlink/tmcs1123.pdf
- https://www.ti.com/product/TMCS1123/part-details/TMCS1123A3AQDVGR

### TI reference design non-transferability

TI TIDA-010937 / TIDUF65 uses TMCS1123B1/B3 and describes using their 1.65 V VREF output as a pseudo-differential ADC negative input. It uses ADS7043 and AMC1035, not ADS131M06. That topology is not a drop-in solution for this project's A3 sensors and ADS131M06. Do not copy its VREF wiring.

Sources:
- https://www.ti.com/tool/TIDA-010937
- https://www.ti.com/document-viewer/lit/html/TIDUF65/GUID-2BE7F651-9C30-4166-9050-B61D613FE533
- https://www.ti.com/document-viewer/lit/html/TIDUF65/GUID-E3BD6673-6101-4215-A521-9DE8D466D3A2

### ADS131M06IPBSR (U1/U2)

TI PBS 32-pin TQFP channel pins:
- Channel 3: AIN3N pin 3, AIN3P pin 4.
- Channel 4: AIN4N pin 6, AIN4P pin 5.
- Channel 5: AIN5N pin 7, AIN5P pin 8.

Sources:
- https://www.ti.com/document-viewer/ADS131M06/datasheet/GUID-5F789CD3-8B9C-470F-B37E-5D1F326C7DC4
- https://www.ti.com/product/ADS131M06

Existing legacy functional grouping says U15–U17 → U1 channels 3–5 and U18–U20 → U2 channels 3–5. This establishes grouping only, not exact sensor output conditioning, ADC N/P polarity, return/reference topology, or destination nets.

## Footprint review-only candidates

- U2 ADS131M06IPBSR PBS TQFP-32: candidate footprint/CSV at `hardware/teststation/V1/CAD/review/physical-symbol-migration/footprints/VAZAO_EVSE_Review.pretty/ADS131M06IPBSR_PBS_TQFP-32_5x5mm_P0.5mm.kicad_mod`; 32/32 pad coordinates match CSV and native KiCad `pcbnew` load passed. Still no 1:1 graphical signoff, independent CAD/sample comparison or fabrication approval.
- U19 TMCS1123A3AQDVGR DVG0010A: candidate uses TI HV/isolation land-pattern option, 8.1 mm example clearance/creepage versus 7.3 mm IPC nominal. Native KiCad load and CSV check passed. Board-level insulation compliance is not established; no production footprint assignment.

## Next engineering work — no guessing

1. Establish the actual maximum RMS, peak, fault and transient current for every measured phase; decide whether A3 range is suitable. In particular, verify whether the intended sensor supply is 5 V and quantify tolerance/derating.
2. Establish the exact isolated 5 V supply and return domain for each of U15–U20 and U1/U2. Do not common isolated returns by assumption.
3. Design/review the analog VOUT-to-ADS131M06 input network: common-mode and differential range, protection, filter, buffering and ADC PGA settings.
4. Approve each sensor's exact ADC channel and N/P polarity.
5. Decide per sensor whether ALERT and OC are used. If OC is used, establish threshold current, VOC resistor/DAC network, pull-up domain and hardware reaction. If unused, follow TI pin handling.
6. Resolve pin 5 VREF treatment for the exact A3 variant; never assign it to `*_I_RET` by assumption.
7. Only after the above evidence, populate approved destination nets in the matrices.
8. Make wiring changes only in a fresh review-only schematic copy, then regenerate KiCad netlist/ERC and compare every physical pin against the approved matrix.
9. Perform graphical 1:1 footprint inspection and board-level creepage/clearance/insulation review.
10. Keep PR #7 Draft/unmerged. No production master/legacy baseline/PCB changes, fabrication or mains energisation.

## Continuation protocol

At every meaningful advance: update the product repo's engineering evidence and index as appropriate; append a checkpoint here without overwriting earlier history; record exact paths, commit SHAs, CI runs, PR state and unresolved gates; fetch changed files back to verify. Never claim a physical test, approval, supplier confirmation or production readiness without retained evidence.


## 2026-11-13 continuation — critical TMCS1123 current-range discrepancy

A new comparison against the project's historical M2.3 requirement (32 A_RMS continuous per phase, plus overload margin) shows that the BOM-selected TMCS1123A3 is not adequate for linear sinusoidal measurement at 32 A_RMS:
- 32 A_RMS sinusoidal current = 45.25 A peak.
- A3 at 5 V: ±32 A linear range.
- A3 at 3.3 V: −32 A to +9.3 A linear range.
- The 80 A_RMS family rating is a thermal/current-path rating, not the A3 analog linear range.

Correction to the previous checkpoint/evidence note: A3 does have a zero-current reference. TI specifies all A-family variants at VREF = VOUT,0A = 2.5 V. Pin 5 VREF is a precision reference output, not a current return. The prior statement that A3 had no zero-current reference is withdrawn.

Historical M2.5's assertion that 80 A_RMS makes 32 A comfortably measurable was therefore incorrect for A3. M2.9-J's VS → 3V3_MEAS instruction is also incompatible with A3's strongly asymmetric 3.3 V measurement range for a sinusoidal 32 A_RMS requirement. The historical 47 Ω / 4.7 nF interface note is incomplete and not approved as a filter.

A1 at 5 V (±96 A, 25 mV/A) and B1 at 3.3 V (±62 A, 25 mV/A) are comparison candidates only. ADS131M06 PGA=1 differential FSR is ±1.2 V; at 32 A_RMS both candidates produce about 1.131 V peak differential, leaving little headroom, so the analog front end must be scaled and common-mode checked. No variant has been selected.

Product repo review branch additions/updates:
- `hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-K-CURRENT-CHANNEL-RANGE-AUDIT-2026-11-13.md`
- `hardware/teststation/V1/CAD/verification/netlist/M2.9-K-TMCS1123-VARIANT-RANGE-COMPARISON.csv`
- `hardware/teststation/V1/CAD/verification/scripts/validate_tmcs1123_variant_range.py`
- Updated interface evidence review, physical migration README, M2.5 historical note, M2.9-J point-to-point contract and validation workflow to record/screen the discrepancy.
- Commits: range audit `834458e635af47010ee53c92b3cdbf8cb43414ff`; corrections/docs `ab14c103ce2fa58dc43d9a26013dae4fc6acd479`, `87341da91c93c7d6bc598de380f27edaad65aa20`, `abc4f22f54355c46a627aa840ddb869d030f7f0e`, `4f0ece154708667b00ef1fd5fd712f665bcd1c39`; CSV `705aa4b3511d85f92e3ee4467d39d139c66ccb77`; validator `e1c3b0c43c1761644fd4d48b250ddfb22b407b9b`; workflow `26596924773ae6a8f9db0cd0a2cee149d5f2b953`.

The static validator and workflow changes have been fetched back from the review branch. A workflow run for the newest workflow commit has not yet been confirmed. Do not claim CI success until a run and its steps are fetched.

PR #7 remains open, Draft and unmerged. No schematic, BOM, matrix destination, PCB, master or legacy baseline was modified. No fabrication or mains energization is authorized.


### Follow-up correction and CI evidence — 2026-11-13

The product review note was re-fetched and one remaining stale sentence was found in its pin table and TIDA comparison paragraph. Both were corrected in product commit `fe7b19c8c59b06206f3ada18358b77b3fe30e0e6`; the review README was updated in `c4e51c013b451856d63e540651e2894a5ee5005b`. Correct statement: A3 uses 2.5 V zero-current reference, not "no reference".

The range arithmetic validator was executed by GitHub Actions and the new step completed SUCCESS in run [43435822792](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/43435822792):
- static symbol pin maps passed;
- U2/U19 matrix passed;
- all-six TMCS1123 migration matrix passed;
- **TMCS1123 RMS-to-peak and ADC range comparison passed**;
- KiCad 10 installation was still in progress at the last inspection, so the entire workflow was not yet complete.

Other in-progress runs on commit `26596924773ae6a8f9db0cd0a2cee149d5f2b953` at last inspection:
- physical migration PR run `43435832184`;
- verified-symbol PR run `43435832249`;
- verified-symbol push run `43435822792`.

The workflow run list was re-queried after these starts; no overall conclusion was available yet. Do not describe the full workflow as passed until job steps and conclusion are fetched.


### ADS131M06 input-voltage/common-mode screening — 2026-11-13

Further TI ADS131M06 review established for PGA gains 1/2/4: AVDD 2.7–3.6 V; recommended individual AIN pin voltage AGND−1.3 V to AVDD; internal-reference differential FSR ±1.2 V / gain.

This distinguishes differential full-scale from individual pin voltage:
- B1 at 3.3 V: at 32 A_RMS sine, VOUT approx 0.519–2.781 V and differential ±1.131 V; at 40 A_RMS, VOUT approx 0.236–3.064 V but differential ±1.414 V, requiring attenuation no greater than about 0.849 just to meet ADC differential range.
- A1 at 5 V: at 32 A_RMS, VOUT approx 1.369–3.631 V; at 40 A_RMS, 1.086–3.914 V. Direct VOUT/VREF connection to a 3.3 V ADS131M06 exceeds the recommended individual AIN ceiling.

B1 is the closer match to the historic 3V3 measurement domain and ADC common-mode window, but only if required peak current remains within ±62 A and thermal/overload limits are validated. A1 has ±96 A peak range but requires a deliberate analog level/attenuation network. Neither is selected.

Updated product audit commit `9f31b973f94b7ea866392ddd95c5fdb4185d2df9`; README commit `3d2cb8a3db52b0712d6c97f4a4792f485de5df8a`. TI ADS131M06 evidence: https://www.ti.com/lit/ds/symlink/ads131m06.pdf. Latest workflow reruns on later documentation-only commits were still in progress at last check; the dedicated range arithmetic step had passed on commit `26596924773ae6a8f9db0cd0a2cee149d5f2b953`.


### Full CI confirmation on range-guard code head — 2026-11-13

Fetched complete job step summaries and confirmed:
- Verified-symbol workflow [#43435832249](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/43435832249): **SUCCESS**. Static pin-map regression, U2/U19 intent guard, six-sensor impact guard, new TMCS1123 RMS-to-peak/ADC arithmetic guard, KiCad 10 installation, footprint geometry/CSV, native pcbnew load, symbol export, master ERC/netlist export, connectivity audit, ERC triage and artifact upload all passed.
- Physical migration workflow [#43435832184](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/43435832184): **SUCCESS**. Pin-map regression, footprint geometry and U19 coordinate guards, KiCad 10 installation, native footprint load, baseline/migrated schematic exports and artifact upload all passed.

Both runs are on code head `26596924773ae6a8f9db0cd0a2cee149d5f2b953`, which includes the new CSV and Python range validator and the workflow wiring. Subsequent product commits through README commit `57d8e462b93d0e6906b42b3526267e9cabd4f922` are documentation-only; exact-head reruns are underway but not yet completed. Do not imply these older runs tested later docs, although no code/matrix/workflow behavior changed after the validated code head.

PR #7 re-fetched: open, Draft, merged=false, head `3d2cb8a3db52b0712d6c97f4a4792f485de5df8a`, mergeable=true, mergeable_state=unstable. Keep it Draft/unmerged.


### Latest PR head recheck — 2026-11-13

After the README checkpoint commit, PR #7 was re-fetched:
- head `57d8e462b93d0e6906b42b3526267e9cabd4f922`;
- state open, Draft=true, merged=false;
- mergeable=true, mergeable_state=unstable.

Exact-head workflows #43436298436 (physical migration) and #43436298089 (verified symbol library) were in progress at the last check. They are documentation-only relative to the fully validated code head `2659692`; prior successful full runs remain the evidence for code/validator behavior. No further commits should be made merely to chase these redundant reruns; monitor and report their final state if they complete.
