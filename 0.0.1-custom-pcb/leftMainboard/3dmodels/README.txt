Project-local component models, added 20261007-164829

All 60 assembled component footprints have a resolvable model.
All model references use ${KIPRJMOD}/3dmodels; no global paths or symlinks.

KiCad/ contains unmodified KiCad library STEP models pinned to commit
8d4070daa0fa3f7a7f3c176f4ca7bffc4df392be, with license and attribution.
EasyEDA/ contains copies of the FPC models in your rightPointerThumbBreakout project.
PhotoEstimates/ contains original approximate VRML visualizations for SW1, SW2 and L1.
Their dimensions, height, terminal shapes and actuator travel are unverified.
J2 uses a representative JST GH 3-contact model; Y1 uses a 3215 crystal model.
These models do not identify the original parts or validate the footprint dimensions.

TP1..TP14 and H1..H4 are bare copper pads/holes, not mounted components.
The battery envelope is a user drawing, not a fitted component model.
See ../review/3d-model-coverage.csv for per-component assignments.

J7 14-pin model re-import: uses a fresh local path named rightPointerThumbBreakout_14pin_856d6481.wrl, copied byte-for-byte from rightPointerThumbBreakout J1, with identical model transforms and electrical pad geometry. The donor file is an approximate closed-connector visualization. Its shape was already identical to the previous local copy; the new filename forces a fresh model reference.

J7 updated 20261007-182405: detailed native STEP for the exact HC-FPC-0.5-14P-FH20 (C19273929), from JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). The former approximate-box model and donor-copy notes above describe superseded models. Source model UUID 93a531ee7c4948b48f4bb060f02c7727. Imported native STEP with offset (-0.25, -1.375, 1.02) mm to center its 14 contacts and seat its solder feet on the PCB. Electrical footprint, component selection and routing were preserved. Detailed source: review/14pin-model-source.json.

EASYEDA MODEL DETAIL AUDIT 20261007-183932
Checked all 60 mounted component models. Updated 52 model assignments with detailed native STEP geometry from JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Models include the radio module PCB antenna, connector housing details, IC molded bodies/leads, and passive terminations. Retained eight already detailed or better-fitting estimates: J3, J7-J10, SW1, SW2, L1. Unknown original parts use clearly documented representative package models; source LCSC numbers are model provenance, not BOM selections. Heights and exact component identities remain unverified. Earlier KiCad model notes describe superseded assignments where relevant. PCB and local footprint libraries updated together; geometry, pads, routes, symbols and schematic values unchanged. See ../review/easyeda-model-audit.csv for every component and source.

L1 replacement 20261008-135743: C5339378 / XRCD54-1R8M, 1.8uH. Local EasyEDA STEP and colored OBJ-to-VRML files: EasyEDA/XRCD54_5.8x5.2x4.5mm_C5339378_EasyEDA.step and .wrl. Only STEP is enabled in the footprint; both models use the same raw coordinate system and KiCad offset (0.0005305,-0.0004572,0.01), rotation Z=270 degrees, scale 1. Source: JLCEDA/EasyEDA Official Library, https://lceda.cn/ and https://easyeda.com. Component API https://easyeda.com/api/products/C5339378/components; STEP https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/e715833d7af94da094ca35faf1e2bc74; OBJ https://modules.easyeda.com/3dmodel/e715833d7af94da094ca35faf1e2bc74. STEP copy is byte-identical to the downloaded source. Model does not verify original Glove80 part identity or boost-controller compatibility.

SW1 replacement 20261008-152253: C528770 / Yuandi TK-6580A-1. Local footprint and detailed STEP/VRML from JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Native STEP enabled, VRML available locally. Model UUID b0bada8f8748472091d08ab2de7a970d. The placeholder switch and false neighboring contact row are superseded. Manufacturer pin mapping: commons 1/2; unlatched contacts 3/5; latched contacts 4/6. Model/footprint do not identify the original Glove80 switch.

J2 replacement 20261008-161252: C293633 / Molex 53398-0371, vertical PicoBlade 3-pin 1.25 mm SMT. Exact-part KiCad footprint copied into local Reconstruction.pretty. Detailed STEP and colored VRML imported from JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). STEP enabled and explicitly aligned to footprint; colored VRML normalized to the native STEP coordinate system and uses the same placement transform. Model UUID c08d1616c3c0494abcf70397badd0eef. PCB top-to-bottom: pad 3 GND, pad 2 BAT_NTC, pad 1 VBAT. Two MP pads are mechanical retainers with no assigned net.

U1 replacement 20261008-174243: C178240 / Silergy SY7088DGC, DFN2x3-8 with ground pad 9. User-reported VTGEA marking matches manufacturer VTxyz. Local footprint, native STEP, and colored VRML imported from JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com); STEP enabled. Model UUID 8b668c87635a4eb1a2b9b0749b2a08a1. Actual pin mapping: 1/2 BOOST_SW; 3 LED_ENABLE; 4/9 GND; 5 BOOST_FB; 6 VDDH input; 7/8 VDD output. All PCB tracks/vias/zones untouched at user request.
