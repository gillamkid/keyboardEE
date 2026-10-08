leftMainboard -- Glove80 LH controller, photograph reconstruction
KiCad 9 project, draft revision 1

OPEN
Open leftMainboard.kicad_pro in KiCad. Both an editable board and a four-sheet
schematic are included. Reconstruction.pretty and Reconstruction.kicad_sym
are project-local libraries. Your existing breakout projects were not edited.

STATUS AND SCOPE
This is a best-effort reconstruction of the photographed Rev J / 2022 board.
Component positions, four mounting holes, USB/GPIO/power/battery connectors,
FPC rows and the long matrix bus bundle follow the photos. Native F.Cu/B.Cu
routing represents the inferred netlist. Ambiguous paths were re-routed;
the native copper is an approximation, not a verified trace-for-trace clone.
Do not fabricate or energize this draft as a verified Glove80 replacement.

The photos do not establish all resistor/capacitor values, concealed connections,
board thickness/layer stack, every semiconductor MPN or connector polarity.
The power stage and LED interface require actual-board continuity checks and
identification of U1/Q1/Q2/Q3 before a working circuit can be claimed.
U1 BOOST_COMP and BOOST_SS are deliberately unresolved named terminals.
The final LED return IN40 is intentionally not connected to the processor.

LAYOUT GEOMETRY
Nominal size: 45 x 75 mm, estimated from known module dimensions and pitches.
Notch: approximately 7.5 x 25 mm. Holes: approximately 3 mm diameter.
Coordinates and dimensions were inferred from photos without a ruler; expect
roughly 0.5--1 mm placement/dimension uncertainty. Confirm the actual dimensions,
hole plating, screw clearance and enclosure fit before using the board mechanically.
Larger substitute footprints occasionally require small placement shifts.
The native routing uses 0.10 mm minimum clearance and some 0.10 mm escape tracks,
with 0.40/0.20 and 0.45/0.20 mm vias. These are reconstruction assumptions.
Some MCU escapes use vias in pads; the actual board's via process is unverified.
The rear ground fill and long front strap are photo-derived; additional top-side
ground areas and stitching connections are inferred to complete draft connectivity.

PHOTOGRAPH REFERENCES
references/Top.png: populated board, rectified to 30 pixels per mm.
references/TopSanded.png and BottomSanded.png: registered surface-copper photos.
The *-grid.png files add a 1 mm coordinate grid. Bottom images are registered
in the same top-view coordinate system as the KiCad PCB.
references/photo-registration.json records the homographies and mounting-hole landmarks.

User.1 (Photo top copper) and User.2 (Photo bottom copper) hold native graphical
copper-edge contours extracted from the photos. They are documentary graphics.
They do not represent electrical nets or contribute to fabrication copper.
Thresholding includes some sanding artifacts and misses obscured/shadowed copper;
the registered photographs retain the original evidence. Toggle these layers
individually to compare them against the editable F.Cu/B.Cu routing.
The battery envelope is on Dwgs.User; it is not an assembled PCB component.
Reference designators are on F.Fab to keep the densely packed silk uncluttered.

CONNECTORS -- REQUESTED USER PINOUTS
J7, 14 contacts, nearest the processor:
1 R0, 2 R1, 3 R2, 4 R3, 5 R4, 6 R5, 7 VDD, 8 GND,
9 IN16, 10 IN0, 11 C2, 12 C1, 13 C0, 14 NC. Anchors 15/16 NC.
J8, nearest 12-contact connector to J7:
1..6 R0..R5, 7 VDD, 8 GND, 9 IN22, 10 IN16, 11 C3, 12 NC.
J9, middle remaining 12-contact connector:
1..6 R0..R5, 7 VDD, 8 GND, 9 IN28, 10 IN22, 11 C4, 12 NC.
J10, farthest connector from J7:
1..6 R0..R5, 7 VDD, 8 GND, 9 IN40, 10 IN28, 11 C6, 12 C5.
All 12-contact mechanical anchors 13/14 are NC.
VDD denotes the external LED supply, estimated at 5 V, not the MCU 2.4 V rail.
FPC MPNs are substitutes from your breakout libraries, not identified factory parts.

FIRMWARE MAPPING -- CONFIRMED BY OFFICIAL DEVICE TREE
R0: P0.26
R1: P0.05
R2: P0.06
R3: P0.08
R4: P0.07
R5: P1.09
C0: P1.01
C1: P1.03
C2: P1.05
C3: P1.07
C4: P1.06
C5: P1.04
C6: P1.08
LED serial data: P0.27
LED power enable: P0.31
Rear status LED PWM: P1.15

The LH firmware array lists columns in the opposite order from your C0-at-thumb
numbering; the table above translates to your physical C0..C6 convention.
Each half has 40 LEDs. The inferred external chain follows 16 + 6 + 6 + 12 keys:
IN0 -> J7 breakout -> IN16 -> J8 -> IN22 -> J9 -> IN28 -> J10 -> IN40.

J3 GPIO/SWD header, 2 x 6, pitch 1.27 mm:
1 GND, 2 VEXT_2V4, 3 VDDH, 4 EXT1, 5 EXT2, 6 EXT3,
7 EXT4, 8 EXT5, 9 EXT6/SWO, 10 RESET, 11 SWDCLK, 12 SWDIO.
EXT1: P0.22
EXT2: P0.21
EXT3: P0.24
EXT4: P0.20
EXT5: P0.25
EXT6: P1.00
MoErgo documents VEXT as typically 2.4 V and VDDH as approximately 3--5 V.
RESET connects to module P0.18; SWDIO/SWDCLK use their dedicated module pads.

PARTS WITH THE STRONGEST EVIDENCE
U4: Raytac MDBT50Q nRF52840 module, PCB antenna variant; suffix P1MV2 inferred.
U2: TP4056 charger marking clearly visible; exact package/ordering suffix inferred.
U3: Nexperia PRTR5V0U2X USB protection, consistent with %R1 marking and SOT143.
L1: 330 marking supports 33 uH; current rating and exact MPN are unknown.
J3: official GPIO header and mapping, with photographed 1.27 mm pitch.

PARTS / DETAILS REQUIRING IDENTIFICATION OR MEASUREMENT
U1: unidentified eight-pin boost controller, marking resembles MXCEA/M1CEA.
The TPS61085-like functional pin map is only a provisional guess; no compatible
replacement or original pinout was established. Feedback/compensation/soft-start
and LED-enable behavior must be checked. Do not order U1 based on this guess.
U5: b25 marking suggests 74CBTLV1G125GV. That device is a 2.3--3.6 V bus switch;
it is not a generic 5 V buffer. The draft uses VEXT_2V4 for its supply, but the
photographed LED voltage-translation topology is unresolved.
Q1/Q2/Q3: three-terminal devices; MOSFET/BJT type, polarity and pin function uncertain.
D3/D4: likely Schottky diodes; BAT54WS and PMEG2010ER are estimates, not verified.
D5: status LED package/colour/current rating inferred.
F1: likely a USB resettable fuse; 500 mA is a placeholder estimate.
Y1: likely a 32.768 kHz crystal; load capacitance and exact package unverified.
L2/L3: ferrite/filter and 10 uH MCU power inductor estimates.
Every resistor/capacitor value, rating and package is inferred. Even apparently
standard 5.1k USB CC resistors should be confirmed on the actual board.
SW1: latching DPDT-style power switch; footprint and terminal assignment estimated.
SW2: tactile reset switch; exact vendor/mechanical dimensions unverified.
J1: generic 16-contact USB-C footprint; compare shell lands with the factory part.
J2: estimated 1.25 mm three-wire LiPo connector; verify family AND BATTERY POLARITY.
TP1..TP14: exposed small lands beside the column-filter components; their probing
function and inferred column/GND assignments are unconfirmed.
H1..H4: inferred plated holes, confirm whether the originals are plated.
See component-confidence.csv for the evidence and candidate for every footprint.

VALIDATION
review/ contains the final KiCad DRC and ERC reports, netlist export, board
previews and a schematic-to-PCB audit. Unresolved DRC findings are preserved.
The schematic symbols are evidence-capture symbols with passive electrical pins;
ERC cannot validate the assumed IC functions or prove that this circuit works.
Passing net/pin checks establishes consistency of the reconstruction only.

Evidence sources and the pinned firmware revision are in references/sources.txt.

FINAL CHECK RESULTS (KiCad 9.0.8, 2026-10-07)
300 physical pad instances checked against the inferred pin maps and schematic.
0 pin-map mismatches; 0 schematic/PCB parity issues; 0 unrouted connections.
8 DRC errors, all courtyard overlaps among estimated footprints.
20 DRC warnings: unused track/via ends remain in the reconstructed buses.
0 ERC errors; 4 singleton global-label warnings (IN40, BOOST_COMP, BOOST_SS, CHARGE_DONE).
The latter reflect an unused final LED return and unresolved/unused power-stage terminals.
Detailed counts and component pairs are in review/drc.rpt and schematic-pcb-audit.json.
These checks establish internal net consistency, not a verified working circuit.

PROJECT-LOCAL 3D MODELS
All 60 fitted component footprints now have local 3D models under 3dmodels/.
Model assignments are updated in the PCB and Reconstruction.pretty library.
SW1, SW2 and L1 use explicitly approximate photo-based visualization models;
J2 and Y1 use representative library models for the estimated package.
See 3dmodels/README.txt and review/3d-model-coverage.csv for provenance and limits.

EMBEDDED SANDED-BOARD PHOTOGRAPHS 20261007-185202
Actual full-color PNG photos are embedded directly in the PCB, at registered 45x75mm size. User.3: Sanded top photo. User.4: Sanded bottom photo (registered to the same top-view coordinates). Select one of these layers in the PCB Editor Appearance panel; show one photo at a time. User.1/User.2 remain the earlier copper contour references. Images are locked against accidental movement. Local view preferences show the top photo at full opacity and hide the other photo and contour layers. Board copper, pads, component placements, models and connections were preserved. See review/embedded-sanded-photos.json.
