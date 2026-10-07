from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
from pathlib import Path
BASE=Path('/home/sam.gillam/keyboardEE/0.0.1-custom-pcb'); OUT=Path('/tmp/glove-mainboard'); SCALE=30
# Four screw centers; dimensions inferred jointly from Raytac land pattern and 1.27mm GPIO pitch.
pts={'RH':[(2.5,2.5),(30.5,2.5),(10.5,72.5),(24.5,72.5)],'LH':[(14.5,2.5),(42.5,2.5),(20.5,72.5),(34.5,72.5)]}
source={
 'TopSanded':{'RH':[(519.5,143.5),(810.5,144.5),(606.5,869),(751.5,870)],'LH':[(1201.5,146),(1494.5,149),(1249,874),(1395,875)]},
 'Top':{'RH':[(425,112),(739,106),(523,899),(680,900)],'LH':[(1252,114),(1589,111),(1311,928),(1475,934)]},
 'BottomSanded':{'RH':[(553.5,985.5),(834,986),(618,267.5),(768,270)],'LH':[(1208.5,966.5),(1488.5,964),(1266,252),(1414.5,250)]}}
matrices={}
for typ,pairs in source.items():
 im=Image.open(BASE/('mainBoards'+typ+'.JPG'))
 for side,src in pairs.items():
  dst=np.array(pts[side],dtype=float)*SCALE; src=np.array(src,dtype=float)*5
  a=[];rhs=[]
  for (x,y),(u,v) in zip(dst,src):
   a.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]); rhs.extend([u,v])
  h=np.linalg.solve(a,rhs); matrices[side+'-'+typ]=list(h)
  out=im.transform((45*SCALE,75*SCALE),Image.Transform.PERSPECTIVE,list(h),resample=Image.Resampling.BICUBIC)
  out.save(OUT/(side+'-'+typ+'-rectified.png'))
  grid=out.copy();draw=ImageDraw.Draw(grid)
  for x in range(0,46):
   if x%5==0:draw.line((x*SCALE,0,x*SCALE,75*SCALE),fill=(40,120,240),width=1);draw.text((x*SCALE+3,3),str(x),fill='blue')
  for y in range(0,76):
   if y%5==0:draw.line((0,y*SCALE,45*SCALE,y*SCALE),fill=(40,120,240),width=1);draw.text((3,y*SCALE+3),str(y),fill='blue')
  grid.save(OUT/(side+'-'+typ+'-grid.png'))
(OUT/'photo-registration.json').write_text(json.dumps({'width_mm':45,'height_mm':75,'px_per_mm':SCALE,'hole_centers_mm':pts,'source_hole_centers_preview_px':source,'output_pixel_to_input_pixel':matrices},indent=2))
