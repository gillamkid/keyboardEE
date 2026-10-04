"""Create JLC BOM/CPL files and validate panel quantities. Run after position export."""
from pathlib import Path
import csv,json,zipfile,hashlib,collections,pcbnew as p
BASE=Path(__file__).resolve().parent.parent;OUT=BASE/'manufacturing';parts=json.loads((OUT/'parts.json').read_text())
comments={'C1':'GRM155R71C104KA88D 100nF 16V X7R 10%','D1':'1N4148WS','LED1':'WS2812B-2020','SW1':'CPG135001S30','J1':'HC-FPC-0.5-6P-FH20'}
packages={'C1':'0402','D1':'SOD-323','LED1':'SMD,2.2x2mm','SW1':'SMD','J1':'SMD,P=0.5mm'}
for kind,infile in [('panel','panel-kicad-positions.csv'),('single-board','single-board-kicad-positions.csv')]:
 rows=list(csv.DictReader((OUT/infile).open()));expected=35 if kind=='panel' else 5
 assert len(rows)==expected,(kind,len(rows))
 assert len({r['Ref'] for r in rows})==expected
 refs=[]
 with (OUT/(kind+'-BOM.csv')).open('w',newline='') as f:
  writer=csv.writer(f);writer.writerow(['Comment','Designator','Footprint','LCSC Part #'])
  for ref in ['C1','D1','J1','LED1','SW1']:
   group=[r['Ref'] for r in rows if r['Ref'].split('_')[0]==ref];assert len(group)==(7 if kind=='panel' else 1)
   refs+=group;writer.writerow([comments[ref],','.join(group),packages[ref],parts[ref]['LCSC Part']])
 with (OUT/(kind+'-CPL.csv')).open('w',newline='') as f:
  writer=csv.writer(f);writer.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
  for r in rows:
   writer.writerow([r['Ref'],f"{float(r['PosX']):.6f}mm",f"{float(r['PosY']):.6f}mm",r['Side'],f"{float(r['Rot'])%360:.6f}"])
 assert set(refs)=={r['Ref'] for r in rows}
 # Polarity comes from actual pad coordinates, independent of placement-tool
 # rotation conventions. Upload preview must match these points.
 b=p.LoadBoard(str(OUT/'chocPcb-7up.kicad_pcb') if kind=='panel' else str(BASE/'AdafruitNeoKeyChocSocketBreakout.kicad_pcb'))
 origin=b.GetDesignSettings().GetAuxOrigin() if kind=='panel' else p.VECTOR2I(0,0)
 with (OUT/(kind+'-polarity-check.csv')).open('w',newline='') as f:
  writer=csv.writer(f);writer.writerow(['Designator','Feature','Pad','X_mm','Y_mm','View'])
  for fp in b.GetFootprints():
   ref=fp.GetReference().split('_')[0]
   important={'D1':('C','Cathode stripe'),'LED1':('1','Pin 1 / DOUT'),'J1':('1','Pin 1 / SWITCHA')}.get(ref)
   if important:
    a=next(a for a in fp.Pads() if a.GetNumber()==important[0]);pos=a.GetPosition();writer.writerow([fp.GetReference(),important[1],important[0],f'{p.ToMM(pos.x-origin.x):.6f}',f'{p.ToMM(origin.y-pos.y):.6f}','Front/top X-Y projection; bottom LED mirrored when viewed underneath'])
# Manufacturing zip contains plot layers and drill data only, not maps/BOM/CPL.
with zipfile.ZipFile(OUT/'chocPcb-7up-Gerbers.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted((OUT/'panel-gerbers').iterdir()):
  if f.suffix in ['.gtl','.gbl','.gtp','.gbp','.gto','.gbo','.gts','.gbs','.gm1','.drl']:z.write(f,f.name)
assert len(zipfile.ZipFile(OUT/'chocPcb-7up-Gerbers.zip').namelist())==11
print('Panel:',expected,'components validated; panel BOM/CPL=35 placements, seven of each part. Two assembled panels=70 components / 14 boards.')
