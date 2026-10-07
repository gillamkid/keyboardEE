keyboardBreakoutPanel Rev 1 — JLCPCB ordering files

Open keyboardBreakoutPanel.kicad_pro in KiCad. The PCB is a 152.4 x 73.3 mm
V-scored panel with one copy of each of the four breakout boards, a combined
four-sheet schematic, 5 mm handling rails, 3 tooling holes and 3 top fiducials.
The four source projects are unchanged. Connector geometry, electrical pin
assignments, traces, vias and drill sizes are preserved under translation.

Files to upload:
  manufacturing/gerber.zip — fabrication layers, drill files, V-CUT guide, notes
  manufacturing/bom.csv    — complete panel bill of materials, 60 connectors
  manufacturing/cpl.csv    — complete panel placements, TOP only

JLCPCB order settings:
  Delivery Format: Panel by Customer
  Panel array: 1 row x 4 columns, four different designs, unequal column widths
  Panel size: 152.4 x 73.3 mm; 2 layers; 1.6 mm FR4
  PCB Assembly: Standard Assembly, top side
  BOM/CPL file type: "Complete File, just proceed with my own files"
  V-score lines and handling rails: already included; use attached V-CUT guide
  Do not add another array or replicate these complete-panel BOM/CPL files.
  PCB quantity is panel quantity: N panels gives N copies of EACH board,
  or 4N individual subboards total. Leave rails attached through assembly.

Paste into fabrication remarks:
  Four different breakout PCBs in a 1 x 4 customer panel, 152.4 x 73.3 mm.
  Double-sided V-score along all seven full-span lines in V-CUT.gbr.
  Do not route the V-CUT lines; retain 5 mm rails during top-side assembly.
  BOM/CPL already contain all 60 panel components; no data replication.

Before confirming the JLCPCB order, check selected C-codes, stock availability,
all 60 placements/rotations, and the factory V-score engineering preview.

Validation:
  PCB DRC: 0 reported violations, 0 unconnected items, 0 schematic parity issues.
  Schematic ERC: 0 violations.
  Conservative minimum copper-to-V-score centerline clearance: 0.65 mm.
  Minimum NPTH edge-to-score centerline clearance: 1.20 mm.
  BOM/CPL references, quantities and shared Gerber/drill/CPL origin verified.
  All source PCB/schematic/project hashes verified unchanged.
  Detailed evidence: manufacturing/validation.txt, drc.rpt and erc.rpt.

Panel-specific courtyard rule:
  Six pairs of original mounting-hole screw-head courtyards overlap across
  subboard boundaries. These holes are not populated by JLCPCB, and screws
  are installed after boards are separated. keyboardBreakoutPanel.kicad_dru
  ignores ONLY the courtyard check for those six specific cross-board pairs.
  Assembly-component courtyard checks and copper/drill clearances remain active.
  Native rule areas prohibit copper within 0.4 mm of every V-score centerline.

Reference names:
  PCB/schematic/BOM/CPL use unique panel refs J1-J60.
  Original local J references remain on each board's silkscreen for familiar
  identification; reference-map.csv gives the exact mapping.
  LPK = leftPinkieBreakout (J1-J13)
  LPT = leftPointerThumbBreakout (J14-J30)
  RPT = rightPointerThumbBreakout (J31-J47)
  RPK = rightPinkieBreakout (J48-J60)
  Serial placeholders remain horizontal on bottom silkscreen and clear of
  traces. The left pointer's inherited placeholder was moved in this panel.

Preview files:
  manufacturing/panel-routing.png / .svg — copper and V-score overview
  manufacturing/panel-top.png — rendered components; V-scores are mechanical
  drawing metadata and do not appear as physical grooves in KiCad 3D rendering.
  manufacturing/panel-drawing.pdf / .svg — fabrication dimensions and score map

Official JLCPCB requirements consulted 2026-10-06:
  https://jlcpcb.com/help/article/pcb-panelization
  https://jlcpcb.com/capabilities/Capabilities?type=1
  https://jlcpcb.com/help/article/how-to-add-edge-rails-fiducials-for-pcb-assembly-order
  https://jlcpcb.com/help/article/common-bom-and-cpl-matching-issues-and-explanations

Source snapshots are frozen build inputs; the original sibling projects remain
available for editing. The panel is a snapshot and does not update automatically
when a source board changes.

Optional rebuild scripts: manufacturing/build-panel.py requires KiCad pcbnew and
sexpdata (available here with PYTHONPATH=/tmp/chocpcb-python). After rebuilding,
run export-jlcpcb.py and validate-panel.py, rerun DRC/ERC, and refresh previews.
