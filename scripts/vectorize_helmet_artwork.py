"""Source-faithful flat SVG color separations from retained 2023 product views.
The source photos stay unmodified. Vectors remove photographed illumination;
they do not invent a manufacturer UV layout or a new helmet design.
"""
from pathlib import Path
import tempfile,xml.etree.ElementTree as ET,json,base64,io
import numpy as np
from PIL import Image
import vtracer
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/derived/helmet-artwork';OUT.mkdir(parents=True,exist_ok=True)
colors={1:'#a5afbd',2:'#123b92',3:'#ff4d21',4:'#ffe000',5:'#111a2a',6:'#e53b24'}
records=[]
for view in ['front','right','left','back']:
 photo=Image.open(ROOT/'assets/source/max-helmet/photos-2023'/(view+'.jpg')).convert('RGB');a=np.asarray(photo,dtype=np.float32)/255
 hi=a.max(2);lo=a.min(2);sat=(hi-lo)/np.maximum(hi,.001);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
 labels=np.zeros(hi.shape,dtype=np.uint8)
 labels[(sat<.27)&(hi<.60)&(hi>=.28)]=1
 labels[(b>r*1.15)&(b>g*.98)&(sat>.26)]=2
 labels[(r>g*1.2)&(r>b*1.3)&(sat>.3)]=3
 labels[(r>.4)&(g>.32)&(b<np.minimum(r,g)*.65)&(g>r*.68)]=4
 labels[hi<.28]=5
 if view=='front':
  yy,xx=np.indices(hi.shape);region=(xx>750)&(xx<1530)&(yy>730)&(yy<1165)
  labels[(labels==3)&region]=6
 w,h=photo.size;svg=ET.Element('svg',{'xmlns':'http://www.w3.org/2000/svg','width':str(w),'height':str(h),'viewBox':f'0 0 {w} {h}'})
 ET.SubElement(svg,'rect',{'width':str(w),'height':str(h),'fill':'#f3f5f8'})
 with tempfile.TemporaryDirectory(prefix='mv33-vector-art-') as tmp:
  for label,color in colors.items():
   if not np.any(labels==label):continue
   im=Image.fromarray(np.where(labels==label,0,255).astype(np.uint8));mask=Path(tmp)/f'{label}.png';trace=Path(tmp)/f'{label}.svg';im.save(mask)
   vtracer.convert_image_to_svg_py(str(mask),str(trace),colormode='binary',mode='spline',filter_speckle=6,corner_threshold=75,length_threshold=3.5,splice_threshold=45,path_precision=3)
   root=ET.parse(trace).getroot();group=ET.SubElement(svg,'g',{'fill':color})
   for path in root:
    if path.tag.endswith('path'):
     path.tag='path';path.attrib.pop('fill',None);group.append(path)
 # Real clear hardware is a separate material, not an ink color. Preserve its
 # source detail inside tight source-coordinate silhouettes, away from logos.
 if view=='front':
  hardware=[[(900,583),(918,510),(950,486),(976,502),(1005,591)],[(1254,590),(1270,506),(1300,488),(1335,511),(1368,598)],[(841,734),(857,634),(888,590),(918,601),(956,733)],[(1307,735),(1320,624),(1345,599),(1381,616),(1425,745)],[(975,1842),(1267,1842),(1265,1924),(1225,1990),(1123,2084),(1018,1986),(977,1924)]]
  defs=ET.SubElement(svg,'defs')
  for i,points in enumerate(hardware):
   x0=min(p[0] for p in points);y0=min(p[1] for p in points);x1=max(p[0] for p in points);y1=max(p[1] for p in points)
   clip=ET.SubElement(defs,'clipPath',{'id':f'hardware-{i}'})
   ET.SubElement(clip,'polygon',{'points':' '.join(f'{x},{y}' for x,y in points)})
   raw=io.BytesIO();photo.crop((x0,y0,x1,y1)).save(raw,format='PNG')
   ET.SubElement(svg,'image',{'x':str(x0),'y':str(y0),'width':str(x1-x0),'height':str(y1-y0),'clip-path':f'url(#hardware-{i})','href':'data:image/png;base64,'+base64.b64encode(raw.getvalue()).decode()})
 path=OUT/(view+'-flat.svg');ET.ElementTree(svg).write(path,encoding='unicode');records.append({'view':view,'source':f'assets/source/max-helmet/photos-2023/{view}.jpg','output':str(path.relative_to(ROOT)),'size':[w,h],'method':'Flat ink-color separations traced to source-derived spline vectors; highlights removed from color artwork. Front clear vents and latch preserve tightly clipped original hardware photography.'});print('VECTOR',view,path.stat().st_size,flush=True)
(ROOT/'docs/research/helmet-vector-artwork.json').write_text(json.dumps(records,indent=2)+'\n')
