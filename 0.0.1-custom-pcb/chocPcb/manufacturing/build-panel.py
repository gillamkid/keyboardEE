"""Build a seven-up native KiCad panel; no external geometry dependencies.
Run: PYTHONPATH=/tmp/chocpcb-python python3 manufacturing/build-panel.py
"""
from pathlib import Path
import copy,uuid,json,shutil,sexpdata as sx,pcbnew as p
BASE=Path(__file__).resolve().parent.parent; OUT=BASE/'manufacturing';OUT.mkdir(exist_ok=True)
S=sx.Symbol;tag=lambda a:str(a[0]) if isinstance(a,list) and a else '';one=lambda a,k:next((v for v in a if tag(v)==k),None);prop=lambda a,k:next((v for v in a if tag(v)=='property' and v[1]==k),None)
uid=lambda:str(uuid.uuid4());mm=p.FromMM
src=BASE/'AdafruitNeoKeyChocSocketBreakout.kicad_pcb';b=p.LoadBoard(str(src));root=sx.loads(src.read_text())
# Source outline must remain the user's 17.3 x 17.5 mm rectangle.
outline=p.SHAPE_POLY_SET();assert b.GetBoardPolygonOutlines(outline) and outline.OutlineCount()==1
ch=outline.Outline(0);coords=[(p.ToMM(ch.CPoint(i).x),p.ToMM(ch.CPoint(i).y)) for i in range(ch.PointCount())]
L=min(x for x,y in coords);R=max(x for x,y in coords);T=min(y for x,y in coords);B=max(y for x,y in coords);w=R-L;h=B-T
assert abs(w-17.3)<.001 and abs(h-17.5)<.001,(w,h)
# 4 mm channels between boards, 2 mm routed channels to support material.
# Wide side frames pad the narrow 2-column array to 70 mm. At least 6 mm
# of top/bottom handling rail remains. Bottom-right position stays solid FR4.
PW,PH=70.,94.;gap=4.;x0=(PW-(2*w+gap))/2;y0=6.
placements=[(x0+c*(w+gap),y0+r*(h+gap)) for r in range(4) for c in range(2)][:7]
def rect(l,t,r,b):
 poly=p.SHAPE_POLY_SET();poly.NewOutline()
 for x,y in [(l,t),(r,t),(r,b),(l,b)]:poly.Append(mm(x),mm(y))
 return poly
panel=rect(0,0,PW,PH)
for x,y in placements:
 cuts=rect(x-2,y-2,x+w+2,y+h+2);cuts.BooleanSubtract(rect(x,y,x+w,y+h))
 for side in [0,1]:
  cuts.BooleanSubtract(rect(x-2 if side==0 else x+w,y+h/2-2.5,x if side==0 else x+w+2,y+h/2+2.5))
 panel.BooleanSubtract(cuts)
assert panel.OutlineCount()==1
keep=[copy.deepcopy(a) for a in root if tag(a) not in ['footprint','segment','via','zone','gr_line','gr_arc','gr_text','gr_poly','gr_circle','dimension','net','uuid']]
keep.append([S('net'),0,''])
for boardnum,(x,y) in enumerate(placements,1):
 dx,dy=x-L,y-T
 netmap={0:0}
 for a in root:
  if tag(a)=='net' and a[1]:
   netmap[a[1]]=boardnum*100+a[1];keep.append([S('net'),netmap[a[1]],f'B{boardnum}/{a[2]}'])
 def renew(a):
  if not isinstance(a,list):return
  if tag(a)=='uuid':a[1]=uid()
  if tag(a)=='net' and a[1]:a[1]=netmap[a[1]];a[2:]=[f'B{boardnum}/{a[2]}'] if len(a)>2 else []
  for v in a:renew(v)
 def offset(a):
  if tag(a) in ['at','start','mid','end','center','xy'] and len(a)>=3 and isinstance(a[1],(float,int)):
   a[1]=round(a[1]+dx,7);a[2]=round(a[2]+dy,7)
  else:
   for v in a:
    if isinstance(v,list):offset(v)
 for old in root:
  k=tag(old)
  if k not in ['footprint','segment','via','zone','gr_line','gr_arc','gr_text','gr_poly','gr_circle','dimension']:continue
  if k.startswith('gr_') and one(old,'layer') and one(old,'layer')[1]=='Edge.Cuts':continue
  a=copy.deepcopy(old);renew(a)
  if k=='footprint':
   at=one(a,'at');at[1]=round(at[1]+dx,7);at[2]=round(at[2]+dy,7)
   ref=prop(a,'Reference');originalref=ref[2];ref[2]=f'{originalref}_{boardnum}';ref[:]=[v for v in ref if tag(v)!='hide'];ref.append([S('hide'),S('yes')])
   if one(a,'path'):a.remove(one(a,'path'))
   # Keep original short silkscreen references as board graphics; use unique
   # assembly reference designators in BOM/CPL without overcrowding the board.
   f=next(f for f in b.GetFootprints() if f.GetReference()==originalref);r=f.Reference()
   if r.IsVisible():
    effects=copy.deepcopy(one(ref,'effects'));pos=r.GetPosition()
    angle=r.GetTextAngle().AsDegrees()
    keep.append([S('gr_text'),originalref,[S('at'),round(p.ToMM(pos.x)+dx,7),round(p.ToMM(pos.y)+dy,7),angle],[S('layer'),'F.SilkS' if r.GetLayer()==p.F_SilkS else 'B.SilkS'],[S('uuid'),uid()],effects])
  else:offset(a)
  keep.append(a)
# Extract manufactured outline including routed cutouts. Native boolean
# operations yield exact line segments rather than rasterized boundaries.
def edge_chain(chain):
 pts=[chain.CPoint(i) for i in range(chain.PointCount())]
 for a,c in zip(pts,pts[1:]+pts[:1]):
  if a==c:continue
  keep.append([S('gr_line'),[S('start'),p.ToMM(a.x),p.ToMM(a.y)],[S('end'),p.ToMM(c.x),p.ToMM(c.y)],[S('stroke'),[S('width'),.05],[S('type'),S('default')]],[S('layer'),'Edge.Cuts'],[S('uuid'),uid()]])
edge_chain(panel.Outline(0))
for i in range(panel.HoleCount(0)):edge_chain(panel.Hole(0,i))
# Keep models and project libraries accessible from this subdirectory.
def fix_model(a):
 if not isinstance(a,list):return
 if tag(a)=='model':a[1]=a[1].replace('${KIPRJMOD}/','${KIPRJMOD}/../').replace('$(KIPRJMOD)/','$(KIPRJMOD)/../')
 for v in a:fix_model(v)
fix_model(keep)
path=OUT/'chocPcb-7up.kicad_pcb';path.write_text(sx.dumps(keep).replace(') (', ')\n('));pb=p.LoadBoard(str(path));pb.GetDesignSettings().SetAuxOrigin(p.VECTOR2I(mm(0),mm(PH)))
# NPTH breakaway perforations, 5 x 0.6 mm holes at 1 mm pitch, two opposing
# 5 mm tabs on each board. Tooling holes are 2 mm diameter.
panellib=OUT/'PanelParts.pretty';panellib.mkdir(exist_ok=True)
shutil.copy2(BASE/'ProjectParts.pretty/TestPoint_Pad_2.0x2.0mm.kicad_mod',panellib/'_seed.kicad_mod')
def npth(ref,x,y,diam):
 f=p.FOOTPRINT(pb);f.SetReference(ref);f.SetValue('NPTH');f.SetFPID(p.LIB_ID('PanelParts','NPTH_'+str(diam)));f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_POS_FILES|p.FP_EXCLUDE_FROM_BOM);f.SetPosition(p.VECTOR2I(mm(x),mm(y)));f.Reference().SetVisible(False);f.Value().SetVisible(False)
 pad=p.PAD(f);pad.SetNumber('');pad.SetAttribute(p.PAD_ATTRIB_NPTH);pad.SetShape(p.PAD_SHAPE_CIRCLE);pad.SetSize(p.VECTOR2I(mm(diam),mm(diam)));pad.SetDrillSize(p.VECTOR2I(mm(diam),mm(diam)));pad.SetPosition(f.GetPosition());pad.SetLayerSet(p.LSET.AllCuMask());f.Add(pad);pb.Add(f);p.FootprintSave(str(panellib),p.FOOTPRINT(f))
for n,(x,y) in enumerate(placements,1):
 for side,xx in [('L',x),('R',x+w)]:
  for k in range(5):npth(f'MB{n}{side}{k+1}',xx,y+h/2-2+k,.6)
for n,(x,y) in enumerate([(3.85,3.85),(PW-3.85,3.85),(3.85,PH-3.85)],1):npth(f'TOOL{n}',x,y,2.)
# Three asymmetric global fiducials per side, 1 mm copper / 2 mm mask window.
for side,layer,mask in [('F',p.F_Cu,p.F_Mask),('B',p.B_Cu,p.B_Mask)]:
 for n,(x,y) in enumerate([(7.85,3.85),(PW-7.85,3.85),(7.85,PH-3.85)],1):
  f=p.FOOTPRINT(pb);f.SetReference(f'FID{side}{n}');f.SetValue('Fiducial');f.SetFPID(p.LIB_ID('PanelParts','Fiducial_1mm_'+side));f.SetLayer(layer);f.SetPosition(p.VECTOR2I(mm(x),mm(y)));f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_POS_FILES|p.FP_EXCLUDE_FROM_BOM);f.Reference().SetVisible(False);f.Value().SetVisible(False)
  a=p.PAD(f);a.SetNumber('');a.SetAttribute(p.PAD_ATTRIB_SMD);a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetSize(p.VECTOR2I(mm(1),mm(1)));a.SetLocalSolderMaskMargin(mm(.5));ls=p.LSET();ls.AddLayer(layer);ls.AddLayer(mask);a.SetLayerSet(ls);a.SetPosition(f.GetPosition());f.Add(a);pb.Add(f);p.FootprintSave(str(panellib),p.FOOTPRINT(f))
# Frame-only instructions, outside all assembly and routing areas.
for txt,x,y in [('chocPcb 7-up / TWO assembled panels = 14 boards',35,1.65),('SUPPORT ONLY',46,78.5)]:
 t=p.PCB_TEXT(pb);t.SetText(txt);t.SetPosition(p.VECTOR2I(mm(x),mm(y)));t.SetTextSize(p.VECTOR2I(mm(1),mm(1)));t.SetTextThickness(mm(.15));t.SetLayer(p.F_SilkS);pb.Add(t)
p.SaveBoard(str(path),pb,True)
# Panel has no schematic; preserve source DRC constraints without parity checks.
shutil.copy2(BASE/'AdafruitNeoKeyChocSocketBreakout.kicad_pro',OUT/'chocPcb-7up.kicad_pro')
for table in ['fp-lib-table','sym-lib-table']:
 text=(BASE/table).read_text().replace('${KIPRJMOD}/','${KIPRJMOD}/../').replace('$(KIPRJMOD)/','$(KIPRJMOD)/../')
 if table=='fp-lib-table':text=text.rstrip()[:-1]+'\n(lib (name "PanelParts") (type "KiCad") (uri "${KIPRJMOD}/PanelParts.pretty") (options "") (descr "Panel tooling and fiducials"))\n)\n'
 (OUT/table).write_text(text)
(OUT/'panel-layout.json').write_text(json.dumps({'width_mm':PW,'height_mm':PH,'boards_per_panel':7,'assembled_panels_for_14_boards':2,'board_width_mm':w,'board_height_mm':h,'gap_mm':gap,'placements':placements,'routed_channel_to_frame_mm':2,'tab_width_mm':5,'mouse_bite_diameter_mm':.6,'mouse_bite_pitch_mm':1,'tabs_per_board':2,'tooling_holes':3,'fiducials_per_side':3},indent=2))
print('Built',path,'outline holes',panel.HoleCount(0),'7 boards, 35 assembly components, 70 mouse bite holes, 3 tooling holes.')
