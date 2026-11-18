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


## 2026-11-13 continuation — provisional ±70 A current-channel envelope

André delegated the choice of sensible engineering numbers because the exact waveform/overload figures were not known. A provisional design envelope was therefore recorded, explicitly as an engineering proposal rather than a frozen product requirement:
- 32 A RMS continuous per phase (existing M2.3 baseline);
- ±70 A instantaneous measurement target;
- 40 A RMS for 10 s and 48 A RMS for 1 s are analysis/test scenarios only. They do not establish thermal withstand, protection coordination or permission to energize.
- 48 A RMS sine = 67.88 A peak, hence the provisional ±70 A target.

**Preferred next study candidate:** TMCS1123A1AQDVGR at 5 V, because its ±96 A sensor linear range covers ±70 A. It is not selected in the BOM. A3 remains the recorded BOM item and is unsuitable for a 32 A RMS sine measurement in its ±32 A peak linear range. B1 at 3.3 V is limited to ±62 A and cannot meet the ±70 A target.

Important correction to earlier memory text above: TI specifies A-family zero-current reference at 2.5 V, including A3. The earlier statement that A3 had no zero-current reference is withdrawn. Pin 5 VREF is a reference output, not a current return.

A1 cannot connect directly to the 3.3 V ADS131M06: its output common-mode/range and the ±1.75 V differential at ±70 A require an engineered conditioning stage. Preliminary target only: differential attenuation about 0.60 (±1.05 V at ±70 A), with output common-mode near 1.65 V, then ADS131M06 PGA=1. This is a transfer target, not an approved resistor network or circuit.

Product repo PR #7 / branch review/teststation-physical-symbol-migration received:
- New proposal: hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-K-CURRENT-CHANNEL-DESIGN-ENVELOPE-PROPOSAL-2026-11-13.md.
- Updated comparison CSV to include 48 A RMS and ±70 A peak sensor linear checks.
- Updated validate_tmcs1123_variant_range.py to guard all five checks and ensure no BOM selection.
- Appended correction to M2.3 and updated review README.
- Product commits in this continuation: 423658ea473137989edd5976feecf7c8fce2dcb1 (proposal); 122d8e493bb15d649ed1d8adab2ea7aab72d1861 (CSV); 2164e16c8d70a2a9fa4c5afe91e05ac0c13d85b2 (validator); 04c50be9c6f080e60c242637f646268728242ad3 (README); 9b5775d8c83e9852377f92e12b09011a7fec281e (M2.3 correction and final branch head).
- Latest branch head re-fetched from GitHub. PR #7 remains open, Draft, merged=false, mergeable=true. No master, legacy baseline, schematic, BOM, wiring, PCB or calibration constant changed.
- Exact-head CI at last check: verified-symbol run 43440733694 and physical migration run 43440733631 were still in progress. Do not claim success until final conclusions and job steps are checked.

Engineering gates remain: TI transient/thermal SOA for exact A1 orderable; ambient/board temperature; conductor/PCB/terminal heating; overload repetition; protection clearing time; crest factor/fault envelope; complete A1-to-ADS131M06 common-mode, absolute-max, impedance, filtering, phase/noise and fault analysis. No overload test, fabrication or mains energization is authorized.


### Exact-head validation progress — 2026-11-13 14:15 UTC

The two exact-head PR workflows for product commit 9b5775d8c83e9852377f92e12b09011a7fec281e were inspected at job-step level:
- Verified-symbol run 43440733694: static symbol pin maps, U2/U19 intent matrix, six-sensor TMCS migration matrix, and the updated TMCS1123 32/40/48 Arms + ±70 A peak arithmetic guard all completed SUCCESS. The job remained in KiCad 10 installation; later native footprint, symbol, master ERC/netlist and triage steps were pending.
- Physical migration run 43440733631: pin-map, footprint geometry/CSV and U19 coordinate checks completed SUCCESS. The job remained in KiCad 10 installation; native footprint load and baseline/migrated schematic export were pending.

Therefore the new range guard itself is verified passing on the exact PR head, but neither complete workflow is yet declared successful. PR #7 remains open/Draft/unmerged.



## 2026-11-13 evening continuation — A1 to ADS131M06 AFE study

Re-fetched product repository state before continuing:
- PR #7 is open, Draft, unmerged; its actual head at this check is `9b5775d8c83e9852377f92e12b09011a7fec281e`. Do not rely on the earlier stale `57d8e46` snapshot.
- A separate stacked branch `review/teststation-current-afe-design-study` was created from PR #7's head.
- Product PR #8: https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/8
- PR #8 is open, Draft, unmerged, based on PR #7 branch; after retargeting, the PR diff is only 3 files / 3 commits. Keep both PRs Draft and unmerged.
- PR #8 head: `0f01e3c31af1508110c36fc895b7009cf834f923`.

New product files in PR #8:
- `hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-K-A1-ADS131M06-ANALOG-FRONT-END-STUDY-2026-11-13.md`
- `hardware/teststation/V1/CAD/verification/scripts/validate_tmcs1123_a1_afe_study.py`
- `.github/workflows/validate-evse-symbol-library.yml` updated to include and run the arithmetic guard.

Important engineering correction:
- The earlier 0.60 attenuation suggestion is explicitly not frozen and is superseded as a first-pass value.
- The A1 AFE study uses nominal differential attenuation **0.50 or lower** as the next design-study target. At ±70 A and +0.4% sensitivity-only screening, the ADC differential magnitude is 0.8785 V, leaving 0.3215 V to the nominal ±1.2 V PGA=1 FSR. Ideal ADC input pins around 1.65 V common-mode are 1.21075 V and 2.08925 V. This is arithmetic only; ADC reference tolerance, full error budget, FDA input common-mode, output swing, noise, stability, filter response and thermal/SOA are not validated.
- A1 sensor VOUT itself spans nominal 0.75–4.25 V at ±70 A. A 3.3 V-only input stage must not be assumed to tolerate this; selected conditioning must explicitly meet sensor-side input common-mode range and ADC-side 3.3 V constraints.
- The A1 study proposes high-impedance differential sensing of VOUT relative to VREF, followed by conditioning/scaling and an FDA/filter stage with controlled output common-mode near 1.65 V. No amplifier or passive values are selected.
- TI ADS131M06 source confirms PGA=1 differential FSR ±1.2 V, recommended individual AIN range AGND−1.3 V to AVDD for gains 1/2/4, and nominal PGA input impedance relationship 330 kΩ × 4.096 MHz / fMOD. Driver source impedance must be checked at actual clock configuration.
- TI TMCS1123 Rev D confirms A1 25 mV/A, A-family VREF=2.5 V, max VOUT capacitive load 4.7 nF, 250 kHz bandwidth and local 100 nF VS decoupling. Thermal current ratings are temperature dependent and do not approve the proposed overload durations.

Arithmetic check was independently evaluated: at 70 A, 25.1 mV/A sensitivity screening and 0.50 scaling yield ±0.8785 V differential; ideal ADC pins 1.21075–2.08925 V; differential headroom 0.3215 V to nominal ±1.2 V.

CI status at checkpoint: workflow runs were not yet returned by the commit-run listing; do not claim the new validator or full workflow passed until PR #8 check-runs are inspected. PR #8 is Draft and stacked on PR #7; no master/BOM/schematic/net/pin-to-net/PCB/firmware change, fabrication or energization authorization.


## 2026-11-15 — THP210 FDA candidate screening

PR #8 latest head: `36aee363faf83c620917896c405e8fca443e599b`.
PR #8 remains open, Draft, unmerged and stacked on PR #7 branch.
- Updated A1/ADS131M06 AFE study to evaluate TI THP210 as first FDA candidate (not selected BOM).
- Updated arithmetic guard to use 2.25 V output common-mode, grounded in TI's documented 5 V single-supply THP210 application.
- New candidate screening:
  - TMCS1123A1 VOUT nominal 0.75–4.25 V at ±70 A; VREF 2.5 V.
  - VOUT/VREF pair common-mode = 1.625–3.375 V.
  - THP210 at 5 V has specified input common-mode range VS−+1 V to VS+−1 V = 1–4 V; nominal DC pair common-mode margin at least 625 mV.
  - Candidate differential gain = 0.50; ±70 A plus sensitivity-only +0.4% screen produces ±0.8785 V differential.
  - VOCM study target 2.25 V gives ideal outputs 1.81075–2.68925 V, within ADS131M06 3.3 V individual AIN range and below ±1.2 V PGA=1 differential FSR by 321.5 mV.
  - TI TMCS1123 Rev D: VREF max capacitive load 20 nF, VREF load regulation 0.2 mV/mA over specified ±5 mA test range, VOUT max capacitive load 4.7 nF.
  - Example RI=4k/RF=2k ratio only for simulation: estimated source branch current ~0.220 mA and VREF load-regulation contribution ~0.044 mV. Values not approved.
- Critical THP210 absolute max differential voltage between IN+ and IN− is ±0.5 V; do not connect full sensor differential directly across the pins. The intended closed-loop FDA network must be checked for input-pin differential voltage and all startup/fault/power-off cases. THP210 inputs are diode-clamped to rails.
- THP210 datasheet demonstrates 5 V single supply and differential-source-to-differential-output configuration; nevertheless, ADS131M06 is delta-sigma and its input impedance/settling interaction must be checked rather than assuming TI's SAR EVM result transfers.
- Local arithmetic independently checked: 0.75–4.25 V sensor output, pair CM 1.625–3.375 V, differential output ±0.8785 V, output pins 1.81075–2.68925 V, headroom 0.3215 V.
- New CI runs on PR #8 head: #43707308902 symbol library, #43707308845 review schematics; both in progress at checkpoint. Do not claim success until exact-head runs complete.
- No BOM/schematic/net/pin-to-net/PCB/firmware changes. No fabrication, overload testing or mains energization approval.


## 2026-11-15 continuation — ADS131M06 filter and simulation references

Further AFE research added to product PR #8:
- TI ADS131M06 Rev A §9.1.2 / Figure 9-1 recommends a single-order analogue anti-alias filter for each channel; the illustrated differential network is 1 kΩ in each input leg and 10 nF across the ADC input pair. TI states the recommendation for CLKIN 2–8.2 MHz.
- Differential first-order approximation: Rdiff≈2 kΩ, Cdiff=10 nF, pole≈7.96 kHz. This is only a screening calculation; source impedance, ADC input impedance, THP210 stability, common-mode and parasitics need inclusion.
- This is now the preferred manufacturer reference network to evaluate instead of the legacy 47 Ω / 4.7 nF note; it is not frozen or authorized for MASTER.
- TI THP210 product page lists a PSpice model and TINA-TI reference/SPICE models. They can support simulation but do not replace silicon corner/ADC switched-input validation.
- Actual ADS131M06 CLKIN and register/OSR configuration have not yet been found/verified in the current project source snapshot. Must identify before finalizing filter cutoff and source impedance.
- Latest PR #8 head after filter reference note: `fd29ebb82394d72c929210d26c9d697ce3ce2e64`. New CI triggered; check exact-head runs before claiming pass.
- All work remains design study only. No BOM, MASTER schematic, net mapping, PCB, firmware, fabrication or energization change/approval.


## 2026-11-15 continuation — exact-head CI and ADC/sensor-rail source audit

Product PR #8 was re-fetched:
- https://github.com/AndreVazao/VAZAO-EVSE-Platform/pull/8
- Open, Draft, unmerged, base remains PR #7 branch.
- Exact head before this continuation: `fd29ebb82394d72c929210d26c9d697ce3ce2e64`.
- PR #7 remains open, Draft, unmerged; production MASTER/BOM/legacy baseline untouched.

Exact-head workflow evidence for PR #8 head `fd29ebb82394d72c929210d26c9d697ce3ce2e64`:
- Verified symbol library run #43707363902: SUCCESS. Steps included static pin maps, U2/U19 intent guard, all-six TMCS1123 impact guard, RMS-to-peak/ADC range check, A1-to-ADS131M06 AFE arithmetic validator, KiCad 10 CLI, native footprint loads, symbol export, master ERC/netlist export, connectivity audit and triage. Only the optional control-issue reporting step was skipped.
- Physical symbol migration run #43707363906: SUCCESS. Steps included pin-map regression, footprint geometry/CSV, U19 coordinates, KiCad 10, native pcbnew footprint load and baseline/migrated schematic exports.
- This confirms automated/static/native KiCad validation at that exact head only. It does not prove analog stability, SPICE behaviour, bench operation, safety or production readiness.

Source audit inspected the A1 AFE study, M2.9-J point-to-point contract, M2.9-L electrical implementation contract, and M2.2/M2.5/M2.0 architecture docs. PR #8 changes only three files (study, arithmetic validator, workflow); it contains no firmware or ADS131M06 register/clock implementation. Searches for ADS131M06 clock/OSR/register configuration and STM32G474 SPI driver did not locate such a source in the indexed repo snapshot. M2.9-J itself explicitly leaves CLKIN/XTAL implementation on HOLD. Therefore actual fCLKIN, fMOD, OSR, data rate, digital-filter mode, PGA registers, SPI rate and SYNC sequencing remain OPEN; do not infer defaults.

Critical cross-document discrepancy discovered:
- M2.9-J section 6 says TMCS1123 VS → 3V3_MEAS.
- PR #8 A1/THP210 study assumes TMCS1123A1 at regulated 5 V and calculates VOUT 0.75–4.25 V nominal at ±70 A (4.2675 V on the sensitivity-only +0.4% high-side screen).
- The 4.25 V positive output cannot be silently reconciled with a 3.3 V sensor supply. Sensor VS rail is now a blocking HOLD requiring exact variant, output range, supply tolerance/startup/brownout, power tree and domain review. Do not automatically decide 5 V or change M2.9-J/BOM.
- ADC reference discrepancy also requires closure: M2.2 calls internal ADS131M06 reference the initial prototype baseline, while M2.9-J/M2.9-L describe a dedicated ADC reference/REFIN network. Need actual circuit and firmware register evidence.

New product evidence note created on PR #8 branch:
`hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-K-ADC-CONFIGURATION-AND-SENSOR-RAIL-HOLD-2026-11-15.md`
Product commit: `652eda7ca3624f81a225e09f15be32539b3b94ee`.
It records the source audit, missing ADC configuration, sensor VS contradiction, ADC reference discrepancy, hold points and explicit non-change boundary. No schematic/BOM/net/firmware/PCB changes. Need fetch the file back and verify; then inspect exact-head CI for new commit (documentation-only change may trigger reruns). PRs #7/#8 remain Draft/unmerged.


## 2026-11-17 continuation — TMCS1123 Rev D and ADS131M06 rate screening

Product PR #8 new head: `5ed914ccd34c9db08025b6de3583a76e4b7c23dd`. New review-only document: `M2.9-M-TMCS1123-VARIANT-AND-ADC-RATE-SCREENING-2026-11-17.md`.

TI TMCS1123 Rev D Table 4-1 corrects the variant/supply picture:
- A1A at 5 V: ±96 A linear; at 3.3 V: −96 A to +28 A.
- B1A at 3.3 V: ±62 A; at 5 V: −62 A to +130 A.
- A3A at 5 V: ±32 A; at 3.3 V: −32 A to +9.3 A.
Thus A1A at 5 V is the only symmetric ±70 A linear candidate among these A/B variants, but remains a study candidate, not BOM selection. Its ±96 A linear range is not a thermal rating.

TI Rev D thermal SOA depends on PCB, airflow, ambient, current duration and duty. The 32 A_RMS continuous requirement and provisional ±70 A peak must be evaluated separately. A continuous 70 A peak sine equals 49.5 A_RMS and cannot be presumed acceptable at high ambient. The duration/repetition/duty of ±70 A events remain unspecified.

Power tree audit: M2.9-I's six isolated 5 V converters are dedicated to six AMC1311B voltage channels. No approved shared/partitioned 5V_MEAS rail for six TMCS1123 and six THP210 devices was located. The current M2.9-J 3V3_MEAS sensor supply cannot be retained unchanged for symmetric ±70 A with A1A. Any 5 V rail requires full domain, grounding, noise, current budget, sequencing and fault review. No changes made.

TI ADS131M06 Rev A: with 8.192 MHz CLKIN in HR mode, OSR 1024/512/256/128 corresponds to 4/8/16/32 kSPS. These are datasheet comparison options only; actual clock, OSR, filter, PGA and SPI configuration remain OPEN. No firmware/register changes made.

Exact-head CI for preceding code commit `652eda7ca3624f81a225e09f15be32539b3b94ee` completed SUCCESS: #43746490496 and #43746490537. Latest head `5ed914c...` is documentation-only and returned no new workflow runs; CI success must not be attributed to this latest commit. PR #8 remains Draft/open/unmerged, 8 ahead/0 behind its base. GitHub PR detail returned mergeable=false during recalculation; no merge attempted.

No MASTER, BOM, netlist, pin mapping, firmware, PCB, fabrication or energization changes. Detailed source links and calculations are in M2.9-M.


## 2026-11-18 — M2.9-N native power-tree source audit

Product repository PR #8 added documentation-only M2.9-N:
`hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-N-5V-SENSOR-RAIL-AND-POWER-DOMAIN-AUDIT-2026-11-18.md`
Commit: `d7648844012224a68c023712da033a36fedadcf0`.

### Native schematic findings

Read-only inspection of `hardware/teststation/V1/CAD/schematics/TS-V1-M2.9-K-MASTER.kicad_sch` on PR #8 branch (title-block M2.9-L.2):
- U15–U20 are still TMCS1123A3AQDVGR.
- U9–U14 are six MEE1S2405SC isolated converters, with ISO5_A1..B3 labels.
- One 3V3_MEAS label is present; 5V_MEAS label and TLV70033 symbol instance are absent.
- Pin 8 VS and pin 3 GND have no explicit wire endpoint at the pin coordinate for any of U15–U20:
  - U15: VS (88.90,45.72), GND (88.90,38.10)
  - U16: VS (88.90,60.96), GND (88.90,53.34)
  - U17: VS (88.90,76.20), GND (88.90,68.58)
  - U18: VS (190.50,45.72), GND (190.50,38.10)
  - U19: VS (190.50,60.96), GND (190.50,53.34)
  - U20: VS (190.50,76.20), GND (190.50,68.58)
This is a source-coordinate inspection, not a KiCad ERC/netlist run. The native source currently does not explicitly implement the six sensor supply/ground connections. It is more than a missing rail label.

### Power-domain discrepancy

M2.6 §17 describes each AMC1311B isolated channel as MEE1S2405SC 5 V followed by TLV70033 3.3 V; M2.9-I §4 describes the isolated 5 V as the AMC1311B supply. Reconcile against exact AMC1311B supply pins and source schematic/BOM. Do not assume either prose statement is authoritative.

M2.9-J says TMCS VS -> 3V3_MEAS, but that cannot be retained unchanged if the M2.9-M A1A 5 V candidate and symmetric ±70 A linear range are kept. TI product data lists TMCS1123 max quiescent current 14 mA; six sensors = 84 mA / 0.42 W at 5 V before FDA, ADC, reference, MCU, regulator loss and margins. TI THP210 lists 0.95 mA typical; six = 5.7 mA typical only, not a guaranteed maximum budget.

### Current status / boundaries

- A1A at 5 V remains a study candidate, not BOM selection.
- Dedicated 5V_MEAS remains an architecture option only; regulator, ground topology, ripple/noise, sequencing, fault behaviour and load budget OPEN.
- Six MEE1S2405SC outputs remain dedicated independent floating voltage-measurement domains; do not repurpose or parallel.
- Next: pin-level power-net extraction from native KiCad, reconciliation with BOM and M2.6/M2.9-I/J, then full six-sensor/FDA load and ground-domain matrix.
- PR #7/#8 remain Draft/open/unmerged; PR #8 compare 9 ahead / 0 behind, mergeable=true at latest check.
- No KiCad ERC result claimed on latest head. No MASTER/BOM/net/pin/firmware/PCB edits, fabrication or energization.


### Additional native source pin check — U9–U14

Coordinate-level inspection of the four MEE1S2405SC pins in M2.9-K MASTER (M2.9-L.2 title block) found:
- U9: no pin wire endpoints.
- U10/U11/U13/U14: VIN+ has a wire endpoint; VIN− and both output pins do not.
- U12: no pin wire endpoints.
No converter output pin has an explicit wire endpoint, so the six ISO5 outputs are not shown as connected/generated in this source snapshot. This qualifies the architecture prose: six isolated domains are the intended design, but not verified implementation in this native schematic. No KiCad netlist/ERC run is claimed. Full audit in product repo M2.9-N, updated through commit `3caf81c1a910b521c185797ef8717a1ffbe4ecb0`.


A 36-row CSV observation register now accompanies M2.9-N:
`hardware/teststation/V1/CAD/verification/netlist/M2.9-N-POWER-PIN-CONNECTIVITY-AUDIT.csv`.
It records U15–U20 pins 3/8 and U9–U14 pins 1–4 with source coordinates and whether a wire endpoint exists. All resolved-net fields remain blank; no electrical destination is inferred. It is not an approved netlist or pin-to-net contract. Product documentation commit `d5157af05e2aa118821ced2c8366ce9e6584dadc`.


## Checkpoint 2026-11-18

Latest product PR #8 head: `d5157af05e2aa118821ced2c8366ce9e6584dadc`, 14 commits ahead and 0 behind PR #7 base. PR #7 and PR #8 remain open Draft, unmerged. Exact-head GitHub Actions runs #44269948933 and #44269949087 are still running. Static pin-map, sensor-range/AFE arithmetic and footprint checks completed successfully; KiCad 10 installation and native schematic/ERC/netlist checks are still pending. No exact-head KiCad/ERC pass is claimed.


## 2026-11-18 correction — KiCad 10 review netlist

The coordinate-only observations added earlier on 2026-11-18 are superseded for the review-migration artifact: the manual method did not account for the complete symbol transforms. KiCad 10.0.8 netlist from workflow #44269949087 resolves:
- U15–U20 pin 8 VS -> respective `*_I` label; pin 9 VOC -> respective `*_I_RET` label.
- Sensor pins 1 IN+, 2 IN−, 3 GND, 5 VREF and 6 VOUT are unconnected.
- U10/U11/U13/U14 pin 1 VIN+ carry ISO5 labels; all converter VIN− and VOUT−/VOUT+ pins unconnected; U9/U12 all four pins unconnected.
- ADS131M06 U1/U2 power/reference pins checked are unconnected.
This export is the review-only `TS-V1-M2.9-K-MASTER-SYMBOL-MIGRATION.kicad_sch`, not the production MASTER. ERC: baseline 300 errors/53 warnings; migrated review 383 errors/53 warnings. This is a serious review migration mapping defect, not a passing validation.

Full evidence in product repo:
`hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-O-KICAD10-REVIEW-NETLIST-AND-POWER-CONNECTIVITY-AUDIT-2026-11-18.md`
Corrected 98-row KiCad netlist CSV:
`hardware/teststation/V1/CAD/verification/netlist/M2.9-N-POWER-PIN-CONNECTIVITY-AUDIT.csv`.
Separate MASTER workflow #44269948933 remains pending; only its generated netlist can establish the MASTER connectivity. No production changes approved.


**Interpretation qualification:** the VS/VOC label placement is recorded as an observed unresolved mapping mismatch / `BLOCKED_ANCHOR_DISPLACEMENT`, not a proven production wiring defect or a prescribed correction. The KiCad artifact is the review-only migration schematic. The actual MASTER netlist is still required before asserting the production power tree.
