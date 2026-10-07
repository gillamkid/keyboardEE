rightPinkieBreakout routing update, 2026-10-06.
Rebuilt routing to use the same pattern as rightPointerThumbBreakout and leftPointerThumbBreakout: vertical F.Cu trunks between the connector columns, horizontal B.Cu buses at each connector row, short vertical connector drops, and short 45-degree LED interconnect fanouts.
Main J1 is the existing 12-pin FPC connector. All connector positions, orientations, pad coordinates, pad numbering and net assignments preserved. Board outline, mounting holes and silkscreen preserved. Schematic and project settings unchanged.
VDD/GND trunks and row buses: 0.5 mm. J1 power fanout on B.Cu: 0.3 mm; short top pad feeds: 0.25 mm. Signal tracks: 0.15 mm. Vias: 0.45 mm diameter / 0.2 mm drill.
LED chain remains IN28 through IN40, C5/C6 and R0-R5 unchanged. FPC mounting pads remain isolated.
PCB DRC: 0 violations, 0 unconnected items, 0 schematic parity issues. Schematic ERC: 0 violations.
JLCPCB production files refreshed in jlcpcb/production_files: BOM-columnBreakout.csv, CPL-columnBreakout.csv, GERBER-columnBreakout.zip. All 13 assembly connectors included; ZIP contains 9 Gerber layers and 2 drill files.
Previous board saved in routing-backups; previous manufacturing files saved in manufacturing-before-refresh ZIP.
Preview: 2026-10-06-routing.png / .svg; red = top copper, blue = bottom copper.
Routing: 129 track segments, 82 vias. Top-layer vertical trace length: 98.6%; bottom-layer horizontal trace length: 100.0%.
