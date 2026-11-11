"""Scoped translation of retained reference identity colors; semantic roles live in CSS."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PALETTE=json.loads((ROOT/'theme/palette.json').read_text())
COLORS=PALETTE['source-map']
def theme_colors(text):
 def color(match):
  token=match.group(0);base=token[:7].lower()
  return COLORS.get(base,token[:7])+token[7:]
 return re.sub(r'#[0-9a-fA-F]{8}(?![0-9a-fA-F])|#[0-9a-fA-F]{6}(?![0-9a-fA-F])',color,text)
def theme_engine(text):
 text=theme_colors(text)
 # The reference uses both string colors and decimal THREE.Color literals.
 for old,new in COLORS.items():
  text=re.sub(r'(?<=\()'+str(int(old[1:],16))+r'(?=[,)])',str(int(new[1:],16)),text)
 return text

def rive_transfer():
    # Embedded artwork uses discrete inks with distinct red-channel values.
    # A bounded lookup avoids the ill-conditioned four-anchor RGB transform
    # (the original olive neutrals are nearly collinear).
    anchors=[(0,'#101b30'),(40,'#101b30'),(180,'#a6b6cb'),(210,'#ef6b19'),(244,'#f4f6fa'),(255,'#f4f6fa')]
    tables=[]
    for channel in range(3):
        values=[]
        for value in range(256):
            lo,hi=next((a,b) for a,b in zip(anchors,anchors[1:]) if a[0]<=value<=b[0])
            t=(value-lo[0])/(hi[0]-lo[0]);offset=1+channel*2
            v=int(lo[1][offset:offset+2],16)*(1-t)+int(hi[1][offset:offset+2],16)*t
            values.append(f'{v/255:.6f}')
        tables.append('<feFunc'+ 'RGB'[channel]+' type="table" tableValues="'+' '.join(values)+'"/>')
    return '<feColorMatrix color-interpolation-filters="sRGB" type="matrix" values="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 1 0"/><feComponentTransfer color-interpolation-filters="sRGB">'+''.join(tables)+'</feComponentTransfer>'
