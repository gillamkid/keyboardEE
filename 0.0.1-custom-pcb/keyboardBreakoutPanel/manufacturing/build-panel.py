from pathlib import Path
import copy,uuid,json,re,csv,shutil,sys,os
import sexpdata as sx,pcbnew as p
sys.excepthook=lambda t,e,tb:(__import__('traceback').print_exception(t,e,tb),sys.stderr.flush(),os._exit(1))
ROOT=Path(__file__).resolve().parent.parent;NAME=ROOT.name;S=sx.Symbol;uid=lambda:str(uuid.uuid4());tag=lambda x:str(x[0]) if isinstance(x,list) and x else '';one=lambda x,k:next((v for v in x if tag(v)==k),None);prop=lambda x,k:next((v for v in x if tag(v)=='property' and v[1]==k),None)
manifest=json.loads((ROOT/'source-manifest.json').read_text());panelroot=uid();refs={};refcounts={};placements=[];keep=None;netcount=0;sheets=[];maprows=[];PW,PH=152.4,73.3;x=5.;schemroot=[S('kicad_sch'),[S('version'),20250114],[S('generator'),S('eeschema')],[S('generator_version'),'9.0'],[S('uuid'),panelroot],[S('paper'),'A4'],[S('title_block'),[S('title'),NAME],[S('rev'),'1']],[S('lib_symbols')]]
def dump(path,a):path.write_text(sx.dumps(a).replace(') (',')\n('))
def renew(a,m):
 if not isinstance(a,list):return
 if tag(a)=='uuid':a[1]=m.setdefault(a[1],uid())
 for v in a:renew(v,m)
def offset(a,dx,dy):
 if tag(a) in ['at','start','mid','end','center','xy'] and len(a)>=3 and isinstance(a[1],(int,float)):
  a[1]=round(a[1]+dx,7);a[2]=round(a[2]+dy,7)
 else:
  for v in a:
   if isinstance(v,list):offset(v,dx,dy)
for index,m in enumerate(manifest):
 name=m['project'];stem=m['source_stem'];snap=ROOT/'source-snapshots'/name;source=p.LoadBoard(str(snap/(stem+'.kicad_pcb')));src=sx.loads((snap/(stem+'.kicad_pcb')).read_text());sch=sx.loads((snap/(stem+'.kicad_sch')).read_text());sheetid=uid();uuids={one(sch,'uuid')[1]:sheetid};renew(sch,uuids)
 fs={f.GetReference():f for f in source.GetFootprints()};refmap={}
 for old in sorted(fs,key=lambda v:(re.sub(r'\d+$','',v),int(re.search(r'\d+$',v).group()))):
  pre=re.sub(r'\d+$','',old);refcounts[pre]=refcounts.get(pre,0)+1;refmap[old]=pre+str(refcounts[pre])
 for a in sch:
  if tag(a)!='symbol':continue
  ref=prop(a,'Reference');old=ref[2];assert old in refmap,old;ref[2]=refmap[old]
  ins=one(a,'instances');ins[:]=[S('instances'),[S('project'),NAME,[S('path'),'/'+panelroot+'/'+sheetid,[S('reference'),refmap[old]],[S('unit'),one(a,'unit')[1]]]]]
 one(sch,'title_block')[1:]=[[S('title'),name],[S('rev'),'1']]
 si=one(sch,'sheet_instances')
 if si:sch.remove(si)
 filename=name+'.kicad_sch';dump(ROOT/filename,sch)
 sxpos=35+(index%2)*115;sypos=45+(index//2)*60
 sheet=[S('sheet'),[S('at'),sxpos,sypos],[S('size'),95,30],[S('fields_autoplaced')],[S('stroke'),[S('width'),0],[S('type'),S('default')]],[S('fill'),[S('color'),0,0,0,0]],[S('uuid'),sheetid],[S('property'),'Sheetname',name,[S('at'),sxpos,sypos-.6,0],[S('effects'),[S('font'),[S('size'),1.27,1.27]],[S('justify'),S('left'),S('bottom')]]],[S('property'),'Sheetfile',filename,[S('at'),sxpos,sypos+30+.6,0],[S('effects'),[S('font'),[S('size'),1.27,1.27]],[S('justify'),S('left'),S('top')]]],[S('instances'),[S('project'),NAME,[S('path'),'/'+panelroot,[S('page'),str(index+2)]]]]]
 schemroot.append(sheet)
 edge=[a for a in src if tag(a)=='gr_line' and one(a,'layer')[1]=='Edge.Cuts'];xs=[v[1] for a in edge for v in [one(a,'start'),one(a,'end')]];ys=[v[2] for a in edge for v in [one(a,'start'),one(a,'end')]];L,R,T,B=min(xs),max(xs),min(ys),max(ys);w=round(R-L,6);assert round(B-T,6)==63.3;dx,dy=x-L,5.-T
 placements.append({'project':name,'source_stem':stem,'x_mm':x,'y_mm':5.,'width_mm':w,'height_mm':63.3,'dx_mm':dx,'dy_mm':dy,'references':refmap,'sheet_uuid':sheetid,'uuid_map':uuids})
 if keep is None:
  keep=[S('kicad_pcb')]+[copy.deepcopy(a) for a in src if tag(a) in ['kicad_pcb','version','generator','generator_version','general','paper','layers','setup']];keep.append([S('net'),0,''])
 netmap={0:0};netnames={}
 for a in src:
  if tag(a)=='net' and a[1]:
   netcount+=1;netmap[a[1]]=netcount;old=a[2]
   if old.startswith('unconnected-('):new=re.sub(r'\(([^)]+)-Pad',lambda mat:'('+refmap[mat[1]]+'-Pad',old)
   else:new='/'+name+'/'+old.lstrip('/')
   netnames[a[1]]=new;keep.append([S('net'),netcount,new])
 def resetnet(a):
  if not isinstance(a,list):return
  if tag(a)=='net' and a[1]:old=a[1];a[1]=netmap[old];a[2:]=[netnames[old]] if len(a)>2 else []
  for v in a:resetnet(v)
 for old in src:
  k=tag(old)
  if k not in ['footprint','segment','via','zone','gr_line','gr_arc','gr_text','gr_poly','gr_circle','gr_rect','dimension']:continue
  if k.startswith('gr_') and one(old,'layer') and one(old,'layer')[1]=='Edge.Cuts':continue
  a=copy.deepcopy(old);renew(a,{});resetnet(a)
  if k=='footprint':
   ref=prop(a,'Reference');originalref=ref[2];ref[2]=refmap[originalref];at=one(a,'at');at[1]+=dx;at[2]+=dy
   f=fs[originalref];r=f.Reference()
   # Keep the original local silkscreen names; panel-wide references are unique
   # in schematic/PCB/BOM/CPL and explicitly mapped in reference-map.csv.
   if r.IsVisible():
    eff=copy.deepcopy(one(ref,'effects'));eff[:]=[v for v in eff if tag(v)!='hide'];q=r.GetPosition();keep.append([S('gr_text'),originalref,[S('at'),round(p.ToMM(q.x)+dx,7),round(p.ToMM(q.y)+dy,7),r.GetTextAngle().AsDegrees()],[S('layer'),r.GetLayerName().replace('Silkscreen','SilkS')],[S('uuid'),uid()],eff])
   ref[:]=[v for v in ref if tag(v)!='hide'];ref.append([S('hide'),S('yes')])
   path=one(a,'path')
   if path:
    originalsym=path[1].split('/')[-1]
    if originalsym in uuids:path[1]='/'+sheetid+'/'+uuids[originalsym]
    else:a.remove(path)
   for key,val in [('sheetname','/'+name+'/'),('sheetfile',filename)]:
    q=one(a,key)
    if q:q[1]=val
   maprows.append([name,originalref,refmap[originalref],f.GetValue(),p.ToMM(f.GetPosition().x)+dx,p.ToMM(f.GetPosition().y)+dy])
  else:offset(a,dx,dy)
  keep.append(a)
 x=round(x+w,6)
assert x==147.4
schemroot.append([S('sheet_instances'),[S('path'),'/',[S('page'),'1']]])
dump(ROOT/(NAME+'.kicad_sch'),schemroot)
for a,z in [((0,0),(PW,0)),((PW,0),(PW,PH)),((PW,PH),(0,PH)),((0,PH),(0,0))]:keep.append([S('gr_line'),[S('start'),*a],[S('end'),*z],[S('stroke'),[S('width'),.05],[S('type'),S('default')]],[S('layer'),'Edge.Cuts'],[S('uuid'),uid()]])
dump(ROOT/(NAME+'.kicad_pcb'),keep)
pro=json.loads((ROOT/'source-snapshots/leftPinkieBreakout/leftPinkieBreakout.kicad_pro').read_text());pro['meta']['filename']=NAME+'.kicad_pro';pro['board']['design_settings']['drc_exclusions']=[]
pro.get('pcbnew',{}).get('last_paths',{})['step']=NAME+'.step'
(ROOT/(NAME+'.kicad_pro')).write_text(json.dumps(pro,indent=2))
b=p.LoadBoard(str(ROOT/(NAME+'.kicad_pcb')));b.GetTitleBlock().SetTitle(NAME);b.GetTitleBlock().SetRevision('1');b.GetDesignSettings().SetAuxOrigin(p.VECTOR2I(p.FromMM(0),p.FromMM(PH)));b.GetDesignSettings().SetGridOrigin(p.VECTOR2I(0,0));b.SetLayerName(p.User_1,'V-SCORE');owned=[];mm=p.FromMM;V=lambda x,y:p.VECTOR2I(mm(x),mm(y))
# Three 2 mm tooling holes and three 1 mm top fiducials in the 5 mm rails.
lib=ROOT/'PanelParts.pretty';lib.mkdir(exist_ok=True)
def panelpart(ref,x,y,diam,hole=False):
 f=p.FOOTPRINT(b);f.SetReference(ref);f.SetValue('Tooling hole' if hole else 'Fiducial');f.SetFPID(p.LIB_ID('PanelParts','ToolingHole_2mm' if hole else 'Fiducial_1mm'));f.SetPosition(V(x,y));f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_POS_FILES|p.FP_EXCLUDE_FROM_BOM);f.Reference().SetVisible(False);f.Value().SetVisible(False)
 a=p.PAD(f);a.SetNumber('');a.SetAttribute(p.PAD_ATTRIB_NPTH if hole else p.PAD_ATTRIB_SMD);a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetSize(V(diam,diam));a.SetPosition(V(x,y))
 if hole:a.SetDrillSize(V(diam,diam));a.SetLayerSet(p.LSET.AllCuMask())
 else:
  ls=p.LSET();ls.AddLayer(p.F_Cu);ls.AddLayer(p.F_Mask);a.SetLayerSet(ls);a.SetLocalSolderMaskMargin(mm(.5))
 f.Add(a);b.Add(f);owned.extend([f,a]);p.PCB_IO_MGR.PluginFind(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(lib),p.FOOTPRINT(f))
for n,(a,z) in enumerate([(8,2.5),(PW-8,2.5),(8,PH-2.5)],1):panelpart('TOOL'+str(n),a,z,2,True)
for n,(a,z) in enumerate([(3.85,3.85),(PW-3.85,3.85),(3.85,PH-3.85)],1):panelpart('FID'+str(n),a,z,1)
# V-score guide lines are on User.1, exported as a separate V-CUT Gerber.
vertical=[5,33.7,76.2,118.7,147.4];horizontal=[5,68.3]
for axis,values in [('x',vertical),('y',horizontal)]:
 for q in values:
  a,z=(V(q,0),V(q,PH)) if axis=='x' else (V(0,q),V(PW,q));line=p.PCB_SHAPE(b);line.SetShape(p.SHAPE_T_SEGMENT);line.SetStart(a);line.SetEnd(z);line.SetWidth(mm(.05));line.SetLayer(p.User_1);b.Add(line);owned.append(line)
  zone=p.ZONE(b);zone.SetIsRuleArea(True);ls=p.LSET();ls.AddLayer(p.F_Cu);ls.AddLayer(p.B_Cu);zone.SetLayerSet(ls);zone.SetDoNotAllowTracks(True);zone.SetDoNotAllowVias(True);zone.SetDoNotAllowPads(True);zone.SetDoNotAllowCopperPour(True);zone.SetDoNotAllowFootprints(False);zone.SetZoneName('V-score copper clearance 0.4 mm')
  poly=zone.Outline();poly.NewOutline();coords=[(q-.4,0),(q+.4,0),(q+.4,PH),(q-.4,PH)] if axis=='x' else [(0,q-.4),(PW,q-.4),(PW,q+.4),(0,q+.4)]
  for xx,yy in coords:poly.Append(mm(xx),mm(yy))
  b.Add(zone);owned.append(zone)
for text,xx,yy in [(NAME+' Rev1 / ONE SET',PW/2,2.5),('LPK',19.35,70.8),('LPT',54.95,70.8),('RPT',97.45,70.8),('RPK',133.05,70.8)]:
 t=p.PCB_TEXT(b);t.SetText(text);t.SetPosition(V(xx,yy));t.SetTextSize(V(1,1));t.SetTextThickness(mm(.15));t.SetLayer(p.F_SilkS);b.Add(t);owned.append(t)
b.BuildConnectivity();p.SaveBoard(str(ROOT/(NAME+'.kicad_pcb')),b,True)
table=sx.loads((ROOT/'fp-lib-table').read_text());table=[v for v in table if not(tag(v)=='lib' and one(v,'name')[1]=='PanelParts')];table=sx.dumps(table);table=table[:-1]+'\n(lib (name "PanelParts") (type "KiCad") (uri "${KIPRJMOD}/PanelParts.pretty") (options "") (descr "Panel fiducials and tooling"))\n)\n';(ROOT/'fp-lib-table').write_text(table)
(ROOT/'panel-layout.json').write_text(json.dumps({'width_mm':PW,'height_mm':PH,'rail_width_mm':5,'board_count':4,'placements':placements,'v_score_vertical_mm':vertical,'v_score_horizontal_mm':horizontal,'copper_clearance_mm':.4,'assembly_components':60},indent=2))
with open(ROOT/'reference-map.csv','w',newline='') as f:w=csv.writer(f);w.writerow(['Source board','Original reference','Panel reference','Value','Panel X mm','Panel Y mm']);w.writerows(maprows)
print('Built native KiCad panel, combined four-sheet schematic, 60 assembly connectors, three tooling holes, three fiducials and seven full-span V-scores.',flush=True);os._exit(0)
