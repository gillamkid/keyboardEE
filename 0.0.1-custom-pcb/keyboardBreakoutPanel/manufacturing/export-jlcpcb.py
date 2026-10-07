from pathlib import Path
import pcbnew as p,json,csv,sqlite3,subprocess,zipfile,os,sys,re,math
ROOT=Path(__file__).resolve().parent.parent;name=ROOT.name;cli='/home/sam.gillam/.local/opt/kicad-9.0.8/bin/kicad-cli';b=p.LoadBoard(str(ROOT/(name+'.kicad_pcb')));owned=[]
# Preserve each original board's short on-board references, with unique
# manufacturing references already in schematic, PCB, BOM and CPL.
placements=json.loads((ROOT/'panel-layout.json').read_text())['placements'];fps={f.GetReference():f for f in b.GetFootprints()};codes={'HC-FPC-0.5-6P-FH20':'C19273925','HC-FPC-0.5-12P-FH20':'C19273928','HC-FPC-0.5-14P-FH20':'C19273929'}
for entry in placements:
 for old,new in entry['references'].items():
  f=fps[new];f.SetField('SourceBoard',entry['project']);f.GetFieldByName('SourceBoard').SetVisible(False);f.SetField('OriginalReference',old);f.GetFieldByName('OriginalReference').SetVisible(False)
  if f.GetValue() in codes:f.SetField('LCSC',codes[f.GetValue()]);f.GetFieldByName('LCSC').SetVisible(False)
# The left pointer's inherited serial placeholder is moved within this panel
# into the unused bottom-left corner; source board remains unchanged.
entry=next(e for e in placements if e['project']=='leftPointerThumbBreakout');rects=[d for d in b.GetDrawings() if isinstance(d,p.PCB_SHAPE) and d.GetShape()==p.SHAPE_T_RECT and d.GetLayer()==p.B_SilkS and entry['x_mm']<=p.ToMM(d.GetStart().x)<entry['x_mm']+entry['width_mm']];assert len(rects)==1
rect=rects[0];x=entry['x_mm']+.7;rect.SetStart(p.VECTOR2I(p.FromMM(x),p.FromMM(65.7)));rect.SetEnd(p.VECTOR2I(p.FromMM(x+10),p.FromMM(67.7)))
for d in b.GetDrawings():
 if isinstance(d,p.PCB_SHAPE) and d.GetLayer()==p.B_SilkS and d.GetShape()==p.SHAPE_T_RECT:
  bb=d.GetBoundingBox();bb.Inflate(p.FromMM(.5));assert all(not bb.Intersects(t.GetBoundingBox()) for t in b.GetTracks())
p.SaveBoard(str(ROOT/(name+'.kicad_pcb')),b,True)
prod=ROOT/'manufacturing';prod.mkdir(exist_ok=True);gerbers=prod/'gerbers';gerbers.mkdir(exist_ok=True)
assembly=sorted([f for f in fps.values() if f.GetReference().startswith('J')],key=lambda f:int(f.GetReference()[1:]));assert len(assembly)==60
groups={}
for f in assembly:groups.setdefault((f.GetValue(),str(f.GetFPID().GetLibItemName()),codes[f.GetValue()]),[]).append(f.GetReference())
with open(prod/'bom.csv','w',newline='') as out:
 w=csv.writer(out);w.writerow(['Comment','Designator','Footprint','LCSC','Quantity'])
 for (value,package,code),refs in groups.items():w.writerow([value,','.join(refs),package,code,len(refs)])
cor=sqlite3.connect('/home/sam.gillam/.local/share/kicad/9.0/3rdparty/plugins/com_github_bouni_kicad-jlcpcb-tools/jlcpcb/corrections.db');corr=cor.execute('select regex,rotation,offset_x,offset_y from correction').fetchall();cor.close()
def correction(f):
 for value in (f.GetReference(),f.GetValue(),str(f.GetFPID().GetLibItemName())):
  for anchored in (True,False):
   for regex,rot,ox,oy in corr:
    if re.match('(?:'+regex+')$' if anchored else regex,value):return rot,ox,oy
 return 0,0,0
origin=b.GetDesignSettings().GetAuxOrigin()
with open(prod/'cpl.csv','w',newline='') as out:
 w=csv.writer(out);w.writerow(['Designator','Val','Package','Mid X','Mid Y','Rotation','Layer'])
 for f in assembly:
  pads=list(f.Pads());box=pads[0].GetBoundingBox()
  for pad in pads:box.Merge(pad.GetBoundingBox())
  q=box.GetCenter();rot,ox,oy=correction(f);a=math.radians(f.GetOrientationDegrees());x=p.ToMM(q.x-origin.x)+ox*math.cos(a)+oy*math.sin(a);y=-p.ToMM(q.y-origin.y)+ox*math.sin(a)-oy*math.cos(a)
  w.writerow([f.GetReference(),f.GetValue(),str(f.GetFPID().GetLibItemName()),round(x,6),round(y,6),(f.GetOrientationDegrees()+rot)%360,'top'])
# Plugin metadata allows later KiCad JLCPCB Tools exports to retain LCSC choices.
jlc=ROOT/'jlcpcb';jlc.mkdir(exist_ok=True);db=sqlite3.connect(jlc/'project.db');db.execute('CREATE TABLE IF NOT EXISTS part_info (reference NOT NULL PRIMARY KEY,value TEXT NOT NULL,footprint TEXT NOT NULL,lcsc TEXT,stock NUMERIC,exclude_from_bom NUMERIC DEFAULT 0,exclude_from_pos NUMERIC DEFAULT 0)')
for f in fps.values():
 active=f.GetReference().startswith('J');db.execute('INSERT OR REPLACE INTO part_info VALUES (?,?,?,?,?,?,?)',(f.GetReference(),f.GetValue(),str(f.GetFPID().GetLibItemName()),codes.get(f.GetValue(),''),None,int(not active),int(not active)))
db.commit();db.close()
subprocess.run([cli,'pcb','export','gerbers','-l','F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts,User.1','--use-drill-file-origin','-o',str(gerbers)+'/',str(ROOT/(name+'.kicad_pcb'))],check=True)
subprocess.run([cli,'pcb','export','drill','--excellon-separate-th','--drill-origin','plot','-o',str(gerbers)+'/',str(ROOT/(name+'.kicad_pcb'))],check=True)
score=next(f for f in gerbers.iterdir() if f.name==name+'-V-SCORE.gbr');score.rename(gerbers/(name+'-V-CUT.gbr')) if score.name!=name+'-V-CUT.gbr' else None
with zipfile.ZipFile(prod/'gerber.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(gerbers.iterdir()):
  if f.suffix in ('.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1','.drl','.gbr'):z.write(f,f.name)
if (prod/'FABRICATION_NOTES.txt').exists():
 with zipfile.ZipFile(prod/'gerber.zip','a',zipfile.ZIP_DEFLATED) as z:z.write(prod/'FABRICATION_NOTES.txt','FABRICATION_NOTES.txt')
print('Generated manufacturing/gerber.zip, bom.csv and cpl.csv: 60 top-side connectors; separate V-CUT Gerber included.',flush=True);os._exit(0)
