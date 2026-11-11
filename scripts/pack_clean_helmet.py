"""Replace only the shell image inside a GLB; geometry, UVs and hardware are byte-preserved."""
from pathlib import Path
import json,struct,hashlib
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'public/gl/models/season-2023.glb';texture=ROOT/'public/max/materials/season-2023-helmet-clean.png';out=ROOT/'public/gl/models/season-2023-clean.glb'
data=source.read_bytes();n=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+n]);binary=data[28+n:]
shell=next(i for i in doc['images'] if i.get('name')=='season-2023-helmet');view_index=shell['bufferView'];replacement=texture.read_bytes();packed=bytearray()
for i,view in enumerate(doc['bufferViews']):
 chunk=replacement if i==view_index else binary[view.get('byteOffset',0):view.get('byteOffset',0)+view['byteLength']]
 packed.extend(b'\0'*((-len(packed))%4));view['byteOffset']=len(packed);view['byteLength']=len(chunk);packed.extend(chunk)
packed.extend(b'\0'*((-len(packed))%4));doc['buffers'][0]['byteLength']=len(packed);shell['mimeType']='image/png';shell['name']='season-2023-clean-vector-artwork'
doc['asset'].setdefault('extras',{})['colorReconstruction']='2023 source-derived vector color separations, lossless atlas; geometry and UVs unchanged.'
js=json.dumps(doc,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
out.write_bytes(struct.pack('<III',0x46546c67,2,28+len(js)+len(packed))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(packed),0x004e4942)+packed)
print('PACKED',out,out.stat().st_size,hashlib.sha256(out.read_bytes()).hexdigest())
