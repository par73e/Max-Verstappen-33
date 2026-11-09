"""Offline relative depth for the source-style displaced portrait; no inference in the browser."""
from pathlib import Path
import argparse,json
import numpy as np
from PIL import Image,ImageFilter
import onnxruntime as ort
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--model',required=True);args=p.parse_args()
source=Image.open(ROOT/'public/max/portrait-studio-source.jpg').convert('RGB')
w,h=source.size;rw=518;rh=round(h/w*rw/14)*14
im=np.asarray(source.resize((rw,rh),Image.Resampling.BICUBIC),dtype=np.float32)/255
im=(im-np.array([.485,.456,.406],dtype=np.float32))/np.array([.229,.224,.225],dtype=np.float32)
opts=ort.SessionOptions();opts.intra_op_num_threads=4
session=ort.InferenceSession(args.model,sess_options=opts,providers=['CPUExecutionProvider'])
depth=session.run(None,{'pixel_values':np.transpose(im,(2,0,1))[None].astype(np.float32)})[0][0]
depth=np.asarray(Image.fromarray(depth).resize((w,h),Image.Resampling.BICUBIC))
alpha=np.asarray(Image.open(ROOT/'public/max/portrait-studio-alpha.png').getchannel('A').resize((w,h),Image.Resampling.LANCZOS))
lo,hi=np.percentile(depth[alpha>220],[2,98]);relative=np.clip((depth-lo)/(hi-lo),0,1)
# Extend foreground depth beyond the silhouette before smoothing. The alpha edge
# must not become a discontinuity in the displaced geometry.
encoded=(80+relative*110).astype(np.uint8)
foreground=Image.fromarray(np.where(alpha>128,encoded,0).astype(np.uint8))
extended=np.asarray(foreground.filter(ImageFilter.MaxFilter(49)))
field=np.where(alpha>128,encoded,np.maximum(80,extended)).astype(np.uint8)
out=Image.fromarray(field).filter(ImageFilter.GaussianBlur(1.5));out.save(ROOT/'public/max/portrait-studio-depth.png')
record={'model':'onnx-community/depth-anything-v2-small','license':'Apache-2.0','source':'https://huggingface.co/onnx-community/depth-anything-v2-small','input':str(source.size),'inference':[rw,rh],'relativeRange':[float(lo),float(hi)],'note':'Monocular relative depth, not a scan or full 3D head; foreground edge extended before smoothing.'}
(ROOT/'docs/research/portrait-depth.json').write_text(json.dumps(record,indent=2))
print(record)
