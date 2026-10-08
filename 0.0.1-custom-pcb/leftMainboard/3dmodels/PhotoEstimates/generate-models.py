from pathlib import Path
import math
root=Path('/tmp/mainboard-3d/models/PhotoEstimates');root.mkdir(exist_ok=True)
# VRML units are inches / 10 (2.54 mm), as used by KiCad's model loader.
# Inputs use local footprint millimetres: X right, Y down, Z above PCB top.
black=(.055,.06,.065);metal=(.72,.73,.74);white=(.90,.88,.78);gray=(.20,.21,.22);bronze=(.48,.22,.08);yellow=(.82,.66,.08)
def box(x,y,z,dx,dy,dz,col):return shape(x,y,z,f'Box {{ size {dx/2.54:.7f} {dy/2.54:.7f} {dz/2.54:.7f} }}',col)
def cylinder(x,y,z,r,h,col):
 n=48;points=[]
 for zz in [-h/2,h/2]:
  for i in range(n):points.append((r*math.cos(2*math.pi*i/n)/2.54,r*math.sin(2*math.pi*i/n)/2.54,zz/2.54))
 faces=[]
 for i in range(n):j=(i+1)%n;faces.extend([i,j,j+n,i+n,-1])
 faces.extend(list(range(n-1,-1,-1))+[-1]+list(range(n,2*n))+[-1])
 coords=', '.join(' '.join(f'{v:.7f}' for v in pt) for pt in points)
 geo='IndexedFaceSet { solid TRUE creaseAngle 0.8 coord Coordinate { point [ '+coords+' ] } coordIndex [ '+', '.join(map(str,faces))+' ] }'
 return shape(x,y,z,geo,col)
def shape(x,y,z,geo,col,rot=''):
 return f'Transform {{ translation {x/2.54:.7f} {-y/2.54:.7f} {z/2.54:.7f} {rot} children [ Shape {{ appearance Appearance {{ material Material {{ diffuseColor {col[0]} {col[1]} {col[2]} specularColor 0.15 0.15 0.15 shininess 0.25 }} }} geometry {geo} }} ] }}\n'
def write(n,body):
 (root/(n+'.wrl')).write_text('#VRML V2.0 utf8\n# Photo-estimated visualization, not a manufacturer dimensional model.\n# Generated for mainboard reconstruction, 2026-10-07. Coordinates use KiCad VRML units.\n'+''.join(body))
body=[box(0,0,.25,6,6,.5,(.48,.48,.49)),cylinder(0,0,2.05,2.75,3.5,gray),cylinder(0,0,.68,2.64,.12,bronze)]
for x in [-2.9,2.9]:body.append(box(x,.6,.16,1.6,4,.30,metal))
write('Inductor_6x6mm_PhotoEstimate',body)
body=[box(0,0,.5,3.6,3.6,.8,black),box(0,0,.95,3.35,3.35,.16,metal),cylinder(0,0,1.38,1.36,.78,yellow)]
for x in [-1.55,1.55]:
 for y in [-1.55,1.55]:body.append(box(x,y,.12,.7,1,.24,metal))
write('Reset_Tactile_4mm_PhotoEstimate',body)
for side,mirror in [('RH',1),('LH',-1)]:
 body=[box(0,0,2.2,6.7,6.7,4.1,black),box(mirror*3.5,0,2.1,1.8,2.4,2.5,white),box(mirror*4.55,0,2.1,.7,2.4,2.5,white)]
 for x in [-.7,1.3]:
  for y in [-3.25,3.25]:body.append(box(mirror*x,y,.12,.75,1.15,.24,metal))
 for x in [-3.175,-1.905,-.635,.635,1.905,3.175]:body.append(box(mirror*x,4.6,.16,.5,2.6,.3,metal))
 write('PowerSwitch_DPDT_'+side+'_PhotoEstimate',body)
