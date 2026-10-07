from pathlib import Path
from collections import Counter
import pcbnew as p,json,csv,zipfile,hashlib,re,math,os
root=Path(__file__).resolve().parent.parent;base=root.parent;b=p.LoadBoard(str(root/(root.name+'.kicad_pcb')));layout=json.loads((root/'panel-layout.json').read_text());fs={f.GetReference():f for f in b.GetFootprints()};report=[]
for entry in layout['placements']:
 name=entry['project'];src=p.LoadBoard(str(root/'source-snapshots'/name/(entry['source_stem']+'.kicad_pcb')));dx=round(entry['dx_mm']*1000000);dy=round(entry['dy_mm']*1000000);mapping=entry['references']
 def nn(value):
  if value.startswith('unconnected-('):return re.sub(r'\(([^)]+)-Pad',lambda m:'('+mapping[m[1]]+'-Pad',value)
  return '/'+name+'/'+value.lstrip('/') if value else ''
 for f in src.GetFootprints():
  g=fs[mapping[f.GetReference()]];assert g.GetPosition().x==f.GetPosition().x+dx and g.GetPosition().y==f.GetPosition().y+dy
  assert g.GetOrientationDegrees()==f.GetOrientationDegrees() and g.GetLayer()==f.GetLayer()
  for pad in f.Pads():
   q=g.FindPadByNumber(pad.GetNumber());assert q.GetPosition().x==pad.GetPosition().x+dx and q.GetPosition().y==pad.GetPosition().y+dy
   assert q.GetNetname()==nn(pad.GetNetname()),(name,g.GetReference(),pad.GetNumber(),q.GetNetname(),nn(pad.GetNetname()))
   assert q.GetSize()==pad.GetSize() and q.GetDrillSize()==pad.GetDrillSize()
 def sig(t,dx=0,dy=0,new=False):
  name2=nn(t.GetNetname()) if new else t.GetNetname()
  if isinstance(t,p.PCB_VIA):return ('via',name2,t.GetPosition().x+dx,t.GetPosition().y+dy,t.GetWidth(p.F_Cu),t.GetDrill())
  ends=sorted([(t.GetStart().x+dx,t.GetStart().y+dy),(t.GetEnd().x+dx,t.GetEnd().y+dy)]);return ('track',name2,t.GetLayer(),t.GetWidth(),tuple(ends))
 originals=Counter(sig(t,dx,dy,True) for t in src.GetTracks());copies=Counter(sig(t) for t in b.GetTracks() if t.GetNetname().startswith('/'+name+'/'))
 assert originals==copies,name
 report.append(name+': verified every footprint, pad/net assignment, copper trace and via preserved under translation.')
assert len(list(b.GetTracks()))==sum(len(list(p.LoadBoard(str(root/'source-snapshots'/e['project']/(e['source_stem']+'.kicad_pcb'))).GetTracks())) for e in layout['placements'])
# Conservative copper clearance uses bounding boxes, so round pads/vias
# can only have more clearance than this lower bound.
minimum=1000.;holes=1000.
for item in list(b.GetTracks())+[pad for f in b.GetFootprints() for pad in f.Pads()]:
 bb=item.GetBoundingBox();box=(p.ToMM(bb.GetLeft()),p.ToMM(bb.GetRight()),p.ToMM(bb.GetTop()),p.ToMM(bb.GetBottom()))
 dist=min([max(box[0]-q,q-box[1]) for q in layout['v_score_vertical_mm']]+[max(box[2]-q,q-box[3]) for q in layout['v_score_horizontal_mm']])
 if isinstance(item,p.PAD) and item.GetAttribute()==p.PAD_ATTRIB_NPTH:holes=min(holes,dist)
 else:minimum=min(minimum,dist)
assert minimum>=.399999 and holes>=.399999,(minimum,holes)
prod=root/'manufacturing'
with open(prod/'bom.csv') as f:bom=list(csv.DictReader(f))
refs=[ref for row in bom for ref in row['Designator'].split(',')];assert len(refs)==len(set(refs))==60 and sum(int(r['Quantity']) for r in bom)==60
assert {r['LCSC']:int(r['Quantity']) for r in bom}=={'C19273925':56,'C19273928':2,'C19273929':2}
with open(prod/'cpl.csv') as f:cpl=list(csv.DictReader(f))
assert len(cpl)==60 and {r['Designator'] for r in cpl}==set(refs)
for row in cpl:
 f=fs[row['Designator']];box=list(f.Pads())[0].GetBoundingBox()
 for pad in f.Pads():box.Merge(pad.GetBoundingBox())
 q=box.GetCenter();assert abs(float(row['Mid X'])-p.ToMM(q.x))<.000002 and abs(float(row['Mid Y'])-(layout['height_mm']-p.ToMM(q.y)))<.000002
 assert row['Layer']=='top' and float(row['Rotation'])==f.GetOrientationDegrees()
 assert 0<float(row['Mid X'])<layout['width_mm'] and 0<float(row['Mid Y'])<layout['height_mm']
for name in json.loads((root/'source-manifest.json').read_text()):
 for filename,digest in name['hashes'].items():assert hashlib.sha256((base/name['project']/filename).read_bytes()).hexdigest()==digest,(name['project'],filename)
with zipfile.ZipFile(prod/'gerber.zip') as z:
 assert len([n for n in z.namelist() if n.endswith('.drl')])==2
 assert len([n for n in z.namelist() if n.endswith(('.gtl','.gbl','.gtp','.gbp','.gto','.gbo','.gts','.gbs','.gm1','.gbr'))])==10
score=(prod/'gerbers'/('keyboardBreakoutPanel-V-CUT.gbr')).read_text();assert len(re.findall(r'D01\*',score))==7
edge=(prod/'gerbers'/('keyboardBreakoutPanel-Edge_Cuts.gm1')).read_text();assert 'X152400000Y73300000' in edge and 'X0Y0' in edge
npth=(prod/'gerbers'/('keyboardBreakoutPanel-NPTH.drl')).read_text();assert len(re.findall(r'^X',npth,re.M))==19
report.extend([f'Conservative minimum copper clearance from V-score centerline: {minimum:.4f} mm (required 0.4 mm).',f'Minimum NPTH edge clearance from V-score centerline: {holes:.4f} mm.','BOM and CPL: 60 unique matching designators, all top side; 56 x C19273925, 2 x C19273928, 2 x C19273929.','All CPL positions equal pad-bounding-box centers relative to the same lower-left origin as Gerbers/drills.','Gerber ZIP: 9 fabrication layers plus V-CUT guide and 2 drill files. Seven full-span score lines.','19 NPTH holes: 16 original mounting holes plus 3 tooling holes.','All four source PCB/schematic/project hashes unchanged.'])
(prod/'validation.txt').write_text('\n'.join(report)+'\n');print('\n'.join(report),flush=True);os._exit(0)
