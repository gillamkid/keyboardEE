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

L1 marking updated 20261009-082051: replaced the EasyEDA top logo with large centered white 1R8 lettering in both local STEP and VRML models. Body, windings, and terminals retained; existing model alignment retained. These are now customized derivatives of the EasyEDA source, superseding the earlier byte-identical STEP note. Board and schematic files were not edited. Original model copies are in leftMainboard-backups/before-L1-1R8-marking-20261009-082051.zip.

L1 marking style updated 20261009-082717: 1R8 rotated 90 degrees counterclockwise relative to the prior marking, changed to regular-weight DejaVu Sans, stretched to 1.85 mm glyph height (previously about 1.58 mm), with dark ink to resemble ../1R8.JPG. Text length remains 4.15 mm. Both STEP and VRML previewed in KiCad. PCB, footprint, schematic, and placement files unchanged. Backup: leftMainboard-backups/before-L1-1R8-style-20261009-082717.zip.

L1 marking updated 20261009-083307: changed the 1R8 font from regular to ExtraLight for thinner strokes. Marking dimensions, position, dark ink, and counterclockwise orientation retained. Both STEP and VRML verified in KiCad renders. Original model body preserved. Backup: leftMainboard-backups/before-L1-1R8-thinner-20261009-083307.zip.

L1 marking updated 20261009-084100: restored the approved regular-weight DejaVu Sans font, undoing ExtraLight. Stretched character height when read upright from 1.85 to 2.20 mm (about 19%) without changing the 4.15 mm text width. Existing 90-degree counterclockwise orientation and dark ink retained. Both STEP and VRML verified in KiCad renders. Backup: leftMainboard-backups/before-L1-1R8-taller-20261009-084100.zip.

L1 marking updated 20261009-084437: reduced the 1R8 lettering by 10% in both planar dimensions: upright text width 3.735 mm and character height 1.98 mm. Font weight, aspect ratio, dark ink, centering and rotation retained. STEP and VRML renders verified. Backup: leftMainboard-backups/before-L1-1R8-smaller-20261009-084437.zip.

Q1/Q3 model update 20261009-121635: selected C7420339 / R+O BSS138. Source: JLCEDA/EasyEDA Official Library, https://lceda.cn/ and https://easyeda.com. UUID d777607a152f4f3aac9bb0d0c14ed6fd. Local STEP SOT-23-3P_L2.9-W1.3-H1.0-LS2.4-P0.95_C7420339_EasyEDA.step and colored VRML SOT-23-3P_L2.9-W1.3-H1.0-LS2.4-P0.95_C7420339_EasyEDA.wrl. VRML shares native STEP coordinate system. Both Q1/Q3 use scale 1, rotation 0, offset (0,0,-0.050795) mm. Q3 previous C15127 package has identical geometry; Q1 previous package model is replaced. Footprint geometry and routing remain unchanged.

Q1/Q3 custom marking 20261009-122546: removed the EasyEDA top logo, SOT-23-3P lettering and the dot so the only top marking is centered S S. Regular DejaVu Sans, light grey ink, upright marking dimensions 1.65x0.60 mm, aligned along the long housing axis. Both local C7420339 STEP/VRML are customized derivatives of JLCEDA/EasyEDA Official Library geometry (https://lceda.cn/ and https://easyeda.com), superseding native-source byte identity. Outer molded housing, chamfers, terminals, seating plane and model transforms retained. STEP/VRML rendered and inspected in KiCad; CAD validity checks passed. Backup leftMainboard-backups/before-Q1-Q3-SS-marking-20261009-122546.zip.

Q1/Q3 S S marking resized 20261009-123006: DejaVu Sans Regular, using the same font file as the L1 1R8 marking (the S S model already used this font). Reduced planar dimensions by 5%, from 1.65x0.60 to 1.5675x0.57 mm. Centering, rotation, font weight, light grey color and package preserved. Both STEP and VRML validated and visually inspected in KiCad. Backup leftMainboard-backups/before-Q1-Q3-SS-smaller-20261009-123006.zip.

U4 Raytac model customized 20261009-132540: project-local COMM-SMD_MDBT50Q-1MV2_C5119772_EasyEDA.step and .wrl. Antenna PCB changed from green to sRGB #006699; metal antenna traces/contacts preserved. Shield changed from near-white to grey #808080. Raised EasyEDA top logo removed; five-line DejaVu Sans Regular dark label added, as requested:
Raytac Corporation
FCC ID: SH6MDBT50Q
IC: 8017A-MDBT50Q
CMIIT ID: 2018DJ5128
Model No.: MDBT50Q
Original package dimensions, chamfers, leads and model placement retained. Native STEP and VRML are customized derivatives of JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com), rather than byte-identical source copies. STEP/VRML renders inspected, CAD bodies valid. PCB/schematic/footprint files unchanged. Backup leftMainboard-backups/before-U4-Raytac-custom-model-20261009-132540.zip.

U4 Raytac model style updated 20261009-133050: antenna PCB darkened from #006699 to #005580. Label rotated 90 degrees clockwise in top view; line pitch reduced from 1.30 to 0.85 mm (about 35%); rotated block is horizontally centered and its start is anchored 0.70 mm below the physical top edge of the shield. Text content, font size/weight and grey shield retained. STEP/VRML render alignment inspected; CAD valid. No PCB/schematic/footprint edits. Backup leftMainboard-backups/before-U4-Raytac-style-20261009-133050.zip.

U4 Raytac model style updated 20261009-133555: Antenna trace darkened to #806600; blue PCB #005580 and grey shield #808080 retained. Raytac label rotated 90 degrees clockwise with 0.85 mm line pitch and anchored 0.70 mm from the physical top and right shield edges. Module contacts and package geometry unchanged. Only the 51 antenna copper faces were recolored; all 305 original yellow contact/underside faces remain unchanged. Both STEP and VRML render checks passed, CAD valid, and all PCB/schematic/footprint files preserved. Backup leftMainboard-backups/before-U4-Raytac-dark-trace-top-right-20261009-133555.zip.

F1 custom appearance 20261009-142945
Custom F1 model for Bourns MF-NSMF150-2 (C89655), based on supplied product photo: gold terminals, charcoal body, squared gold 8 with underline, dot on positive-X terminal toward positive Y. EasyEDA lettering removed. Derived from the existing project-local 1206 model.
Source credit: JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Both STEP and VRML are customized derivatives. Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-F1-custom-model-20261009-142945.zip

F1 custom appearance 20261009-152544
Custom F1 model for Bourns MF-NSMF150-2 (C89655), based on supplied product photo: darker bronze terminals and marking (#A4824D), narrower 1.86 mm charcoal center, squared 8 with underline, dot on positive-X terminal toward positive Y. EasyEDA lettering removed. Derived from the existing project-local 1206 model.
Source credit: JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Both STEP and VRML are customized derivatives. Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-F1-custom-model-20261009-152544.zip

F1 custom appearance 20261009-152905
Custom F1 model for Bourns MF-NSMF150-2 (C89655), based on supplied product photo: darker bronze terminals and marking (#A4824D), narrower 1.66 mm charcoal center, squared 8 with underline, terminal dot removed at user request. EasyEDA lettering removed. Derived from the existing project-local 1206 model.
Source credit: JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Both STEP and VRML are customized derivatives. Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-F1-custom-model-20261009-152905.zip

U2 custom TP4056 marking 20261009-220904
Custom model top marking: original ESOP8 and EasyEDA lettering removed, replaced with centered TP4056 in DejaVu Sans Regular; light-gray dot in the existing pin-1 recess. Package, leads, exposed pad, model transform and PCB footprint unchanged.
Both STEP and VRML are customized derivatives of JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-U2-TP4056-marking-20261009-220904.zip

U2 custom TP4056 marking 20261009-221213
Custom model top marking: original ESOP8 and EasyEDA lettering removed, replaced with TP4056 in DejaVu Sans Regular, rotated 90 degrees clockwise and anchored 0.25 mm from the flat top edges at text-upright top/left; light-gray dot in the existing pin-1 recess. Package, leads, exposed pad, model transform and PCB footprint unchanged.
Both STEP and VRML are customized derivatives of JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-U2-TP4056-marking-20261009-221213.zip

U1 custom VTGEA marking 20261009-222217
Custom U1 top marking: EasyEDA logo and original misplaced dot removed; centered VTGEA in DejaVu Sans Regular, rotated 90 degrees clockwise; light-gray pin-1 dot moved to native (-X,-Y), verified against footprint pad 1. Package outline, leads, exposed pad, model transform and PCB footprint unchanged.
Both STEP and VRML are customized derivatives of JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-U1-VTGEA-marking-20261009-222217.zip

U1 custom VTGEA marking 20261009-222541
Custom U1 top marking: EasyEDA logo and original misplaced dot removed; centered VTGEA in DejaVu Sans Regular, rotated 90 degrees counterclockwise from its previous position (now upright); light-gray pin-1 dot moved to native (-X,-Y), verified against footprint pad 1. Package outline, leads, exposed pad, model transform and PCB footprint unchanged.
Both STEP and VRML are customized derivatives of JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-U1-VTGEA-marking-20261009-222541.zip

U2 custom TP4056 marking 20261009-222541
Custom model top marking: original ESOP8 and EasyEDA lettering removed, replaced with TP4056 in DejaVu Sans Regular, rotated 90 degrees clockwise and anchored 0.40 mm from the flat top edges at text-upright top/left (shifted 0.15 mm down and right from prior position); light-gray dot in the existing pin-1 recess. Package, leads, exposed pad, model transform and PCB footprint unchanged.
Both STEP and VRML are customized derivatives of JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-U2-TP4056-marking-20261009-222541.zip

U1 custom VTGEA marking 20261009-222832
Custom U1 top marking: EasyEDA logo and original misplaced dot removed; centered VTGEA in DejaVu Sans Regular, reduced 10 percent to 1.755 x 0.324 mm, rotated 90 degrees counterclockwise from its previous position (now upright); light-gray pin-1 dot moved to native (-X,-Y), verified against footprint pad 1. Package outline, leads, exposed pad, model transform and PCB footprint unchanged.
Both STEP and VRML are customized derivatives of JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-U1-VTGEA-marking-20261009-222832.zip

U2 custom TP4056 marking 20261009-222832
Custom model top marking: original ESOP8 and EasyEDA lettering removed, replaced with TP4056 in DejaVu Sans Regular, rotated 90 degrees clockwise and anchored 0.60 mm from the flat top edges at text-upright top/left (shifted another 0.20 mm down and right; cumulative shift 0.35 mm on each axis); light-gray dot in the existing pin-1 recess. Package, leads, exposed pad, model transform and PCB footprint unchanged.
Both STEP and VRML are customized derivatives of JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-U2-TP4056-marking-20261009-222832.zip

SW2: C2906282 / SHOU HAN TS3735A 250gf 030. Footprint and STEP/VRML models imported from JLCEDA/EasyEDA Official Library (https://lceda.cn/ and https://easyeda.com). Source: https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/c36bae7e99004b83bd4fdc1d298f3360

SW2 custom amber model 20261010-134504
Custom SW2 appearance based on supplied photograph: circular button reduced 10% from 3.0 to 2.7 mm, recoloured amber (#805900), with matching vertical amber rectangle 1.20 x 3.20 mm stopping 0.25 mm from body edges. Body, terminals, footprint, placement and routing unchanged.
Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-SW2-amber-model-20261010-134504.zip

SW2 custom amber model 20261010-135326
Custom SW2 appearance based on supplied photograph: circular button reduced 10% from 3.0 to 2.7 mm, recoloured amber (#946900), with matching vertical amber rectangle 1.20 x 3.20 mm stopping 0.25 mm from body edges. Body, terminals, footprint, placement and routing unchanged.
Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-SW2-amber-model-20261010-135326.zip

Q2 custom 5PEY marking 20261010-142226
Custom Q2 model top: original EasyEDA logo, package text and pin-1 dot removed; centered 5PEY in DejaVu Sans Regular, 2.0 x 0.48 mm, oriented along the package long axis. Existing SOT-23 package visualization retained for selected TECH PUBLIC DMG2305UX C2940629. Model transform, package outline, terminals, manually sized PCB pads, footprint, placement and routing unchanged.
Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-Q2-5PEY-marking-20261010-142226.zip

Q2 custom 5PEY marking 20261010-142521
Custom Q2 model top: original EasyEDA logo, package text and pin-1 dot removed; 5PEY in DejaVu Sans Regular reduced 10 percent to 1.8 x 0.432 mm, rotated 180 degrees from previous marking (native -90 degrees), and anchored 0.20 mm from the right flat-top edge as read upright, with vertical centering retained. Existing SOT-23 package visualization retained for selected TECH PUBLIC DMG2305UX C2940629. Model transform, package outline, terminals, manually sized PCB pads, footprint, placement and routing unchanged.
Backup: /home/sam.gillam/keyboardEE/0.0.1-custom-pcb/leftMainboard/leftMainboard-backups/before-Q2-5PEY-marking-20261010-142521.zip
