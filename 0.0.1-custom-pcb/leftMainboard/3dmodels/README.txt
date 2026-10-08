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
