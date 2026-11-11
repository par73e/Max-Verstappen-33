"""Trace the retained CC0 signature into smooth, scalable orange artwork.

Optional preparation: uv pip install --python .venv/bin/python vtracer==0.6.15
Ordinary build/preview uses the checked-in SVG and does not need VTracer.
"""
from pathlib import Path
from PIL import Image
import tempfile
import vtracer

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='mv33-signature-') as directory:
    image = Image.open(ROOT/'public/max/signature.png').convert('RGBA')
    background = Image.new('RGB', image.size, 'white')
    background.paste(image, mask=image.getchannel('A'))
    background.resize((1200, 848), Image.Resampling.LANCZOS).save(Path(directory)/'trace.png')
    vtracer.convert_image_to_svg_py(
        str(Path(directory)/'trace.png'), str(Path(directory)/'trace.svg'),
        colormode='binary', mode='spline', filter_speckle=8,
        corner_threshold=90, length_threshold=4, splice_threshold=45, path_precision=3,
    )
    svg = (Path(directory)/'trace.svg').read_text()
    svg = svg.replace('width="1200" height="848"', 'width="1200" height="848" viewBox="0 0 1200 848" role="img" aria-label="Max Verstappen signature"')
    svg = svg.replace('#000000', '#ef6b19')
    (ROOT/'public/max/signature-orange.svg').write_text(svg)
