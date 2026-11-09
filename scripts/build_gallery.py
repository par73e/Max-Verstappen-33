"""Build a browsable source-backed contact sheet from the asset inventory."""
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'max-assets.json').read_text())
records=json.loads((ROOT/'assets-manifest.json').read_text())
sources={r.get('path'):r.get('source',r.get('url','https://www.verstappen.com/')) for r in records}
out=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MV33 · 素材库</title><style>body{background:#282c20;color:#f4f4ed;font:15px/1.6 system-ui,sans-serif;margin:0;padding:40px max(20px,5vw)}h1{font-size:48px;line-height:1;margin:20px 0}h2{margin-top:65px;font-size:28px}main{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:30px 20px}figure{margin:0;min-width:0}img{width:100%;height:230px;object-fit:contain;background:#f4f4ed}figcaption{margin-top:8px;font-size:12px;overflow-wrap:anywhere}a{color:#d2ff00;text-underline-offset:4px}.actions{display:flex;gap:18px;margin-top:6px}header p{max-width:65ch;color:#dde1d2}@media(max-width:800px){main{grid-template-columns:repeat(2,minmax(0,1fr))}img{height:170px}h1{font-size:36px}}</style><header><a href="/">← 首页 / Home</a><h1>MV33 ASSET LIBRARY</h1><p>原始图片、候选素材与来源索引。头盔档案图用于寻找款式和角度；首页陈列使用三款商品摄影的不同视角。所有原始文件保持不变。</p></header>''']
def card(path,title,source):
    return f'<figure><a href="{html.escape(path)}" target="_blank"><img src="{html.escape(path)}" alt="{html.escape(title)}" loading="lazy"></a><figcaption>{html.escape(title)}<br>{html.escape(path)}<div class="actions"><a href="{html.escape(source)}" target="_blank" rel="noopener noreferrer">来源 / Source ↗</a><a href="{html.escape(path)}" download>原图 / Download</a></div></figcaption></figure>'
groups=[('人物与标识 / Portrait & identity',[(data['portrait'],'Historical F1 portrait extraction'),('/max/portrait-studio-source.jpg','Current hero · source studio portrait'),('/max/portrait-studio-alpha.png','Current hero · opacity extraction'),('/max/portrait-studio-depth.png','Current hero · inferred relative depth'),('/max/portrait-front-source.png','Original front portrait'),('/max/helmet-2023-front-cutout.png','2023 front helmet cutout'),(data['logo'],'MV 标识'),('/max/signature.png','Max 签名')]),
        ('Orange Tribute 2024 / 荷兰站橙色款',[(f'/max/orange-2024-{i:02d}.jpg','Orange Tribute 2024 · Official photography') for i in range(9)]),
        ('赛事照片 / Editorial photography',[(p['path'],p.get('alt') or 'Max Verstappen') for p in data['photos']]),
        ('官方头盔商品图 / Helmet product photography',[(p,h['title']) for h in data['helmets'] if len(h['images'])>1 for p in h['images']]),
        ('头盔档案候选 / Helmet archive candidates',[(p,h['title']) for h in data['helmets'] if len(h['images'])==1 for p in h['images']]),
        ('横幅与补充素材 / Banners',[(p['path'],p.get('alt') or 'Official banner') for p in data['banners']])]
out.append('<h2>三维头盔 / 3D helmets</h2><p><a href="/helmets/season-2023/">2023 Season ↗</a> · <a href="/helmets/zandvoort-2024/">Zandvoort 2024 ↗</a></p><p>“<a href="https://skfb.ly/pEDBZ">Helmet Redbull - Max Verstappen</a>” by Maubian / <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Geometry normalized; UVs and liveries reconstructed from the credited photographs. Approximation, not an official scan.</p>')
seen=set()
for title,items in groups:
    out.append('<h2>'+html.escape(title)+'</h2><main>')
    for path,label in items:
        if path in seen:continue
        seen.add(path);out.append(card(path,label,sources.get('public'+path,'https://www.verstappen.com/')))
    out.append('</main>')
out.append('</html>');(ROOT/'public/assets.html').write_text(''.join(out))
print('Built asset gallery:',len(seen),'files')
