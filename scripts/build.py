"""Build a local MV33 adaptation from the retained reference DOM and renderer."""
import json
import hashlib
import re
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT/'public'
assets = json.loads((ROOT/'max-assets.json').read_text())
soup = BeautifulSoup((ROOT/'reference/lando-home.html').read_text(), 'html.parser')

def local(url):
    if url.startswith('https://cdn.prod.website-files.com/') or url.startswith('https://d3e54v103j8qbb.cloudfront.net/'):
        name = urllib.parse.unquote(urllib.parse.urlparse(url).path.rsplit('/', 1)[-1])
        if (PUBLIC/'reference'/name).exists(): return '/reference/'+urllib.parse.quote(name)
    return url

# Keep the renderer/Webflow dependency order. Remove original analytics only.
for script in list(soup.find_all('script')):
    src = script.get('src', '')
    if src.startswith('/avlj') or 'google' in script.text or 'gtag(' in script.text:
        script.decompose()
    elif 'lando-by-OFF' in src:
        script['src'] = '/engine.js?v=20261108-photo4'
    elif src:
        script['src'] = local(src)
        script.attrs.pop('integrity', None)
        script.attrs.pop('crossorigin', None)

for tag in soup.find_all():
    tag.attrs.pop('integrity', None)
    tag.attrs.pop('crossorigin', None)
    for attr in ['src', 'href', 'poster']:
        if tag.has_attr(attr): tag[attr] = local(tag[attr])
    if tag.has_attr('srcset'):
        tag['srcset'] = ', '.join(local(p.strip().split(' ')[0])+' '+p.strip().split(' ')[-1]
                                 for p in tag['srcset'].split(', ') if ' ' in p.strip())
    if tag.has_attr('data-stream-url'): del tag['data-stream-url']

# Preserve selectors and data attributes: the original timelines bind to them.
for node in list(soup.find_all(string=True)):
    if isinstance(node, Comment): continue
    if node.parent.name in ['script', 'style']: continue
    text = str(node)
    for old, new in [('LANDO NORRIS', 'MAX VERSTAPPEN'), ('Lando Norris', 'Max Verstappen'),
                     ('Lando', 'Max'), ('lando', 'max'), ('Norris', 'Verstappen'),
                     ('norris', 'verstappen'), ('MCLAREN', 'RED BULL'), ('Mclaren', 'Red Bull'),
                     ('mclaren', 'red bull'), ('since 2019', 'since 2016'),
                     ('SINCE 2019', 'SINCE 2016'), ('2025 Red Bull Formula 1 Driver', 'Formula 1 Driver')]:
        text = text.replace(old, new)
    if text != str(node): node.replace_with(NavigableString(text))

soup.html['lang'] = 'zh-CN'
soup.title.string = 'MV33 — Max Verstappen · 维斯塔潘'
for meta in soup.select('meta[property],meta[name]'):
    if meta.get('property','').startswith(('og:', 'twitter:')) or meta.get('name') in ['description','twitter:title','twitter:description','twitter:image']:
        if 'image' in meta.get('property','') or 'image' in meta.get('name',''):
            meta['content'] = '/max/portrait.webp'
        elif 'title' in meta.get('property','') or 'title' in meta.get('name',''):
            meta['content'] = 'MV33 — Max Verstappen'
        else: meta['content'] = '维斯塔潘主题 · 个人前端还原练习 / An unofficial fan-made frontend study.'

brand = soup.select_one('.nav-brand')
brand.clear()
brand.append(BeautifulSoup('''<svg viewBox="0 0 138 63" width="138" height="63" role="img" aria-label="Max Verstappen"><text nav-brand-path="1" x="0" y="31" font-family="Brier" font-size="42" font-weight="700" fill="currentColor">MAX</text><text nav-brand-path="2" x="0" y="60" textLength="137" lengthAdjust="spacingAndGlyphs" font-family="Mona Sans Variable" font-weight="900" font-size="23" fill="currentColor">VERSTAPPEN</text></svg>''', 'html.parser'))

for canvas in soup.select('[data-rive-ln4]'):
    canvas['class'] = ['mv-original-logo']
    image = soup.new_tag('img', src='/max/mv-orange.svg', alt='MV')
    image['class'] = ['mv-logo-overlay']
    canvas.parent.append(image)

mobile_name=soup.select_one('.home-hero-tablet-text-w')
if mobile_name:
    mobile_name.clear()
    mobile_name.append(BeautifulSoup('<div class="mv-mobile-wordmark"><span>MAX</span><strong>VERSTAPPEN</strong></div>', 'html.parser'))

photos = assets['photos']
photo_order = [4, 18, 12, 10, 0, 9, 19, 22, 25, 27]
for i, image in enumerate(soup.select('.is-horizontal-scroll')):
    p = photos[photo_order[i % len(photo_order)] % len(photos)]
    image['src'] = p['path']; image['alt'] = 'Max Verstappen · 官方赛事影像'
    image.attrs.pop('srcset', None); image.attrs.pop('sizes', None)
    tile=image.find_parent(class_='horizontal-item') or image.parent.parent
    for caption in tile.find_all(string=re.compile(r', 20\d\d$')):
        source_url=next((r['url'] for r in json.loads((ROOT/'assets-manifest.json').read_text()) if r.get('path')=='public'+p['path']), '')
        caption.replace_with('Mexico City, 2026' if 'Mexico' in source_url else 'São Paulo, 2026')
for i, image in enumerate(soup.select('.menu-img-top,.menu-img-no-blend')):
    p = photos[[2, 4, 12, 1, 10][(i//2)%5] % len(photos)]
    image['src'] = p['path'];image['alt']='Max Verstappen'
    image.attrs.pop('srcset', None)
for i, image in enumerate(soup.select('.is-social-card')):
    p = photos[[6, 10, 12, 19, 21, 25, 27][i % 7] % len(photos)]
    image['src']=p['path'];image['alt']='Max Verstappen · 赛事影像'
    image.attrs.pop('srcset',None)
for i, image in enumerate(soup.select('.otot-home-img')):
    image['src']=photos[[7,4][i%2]]['path'];image['alt']='Max Verstappen'
    image.attrs.pop('srcset',None)
for image in soup.select('.is-otot-home-end'):
    image['src']=photos[6]['path'];image['alt']='Max Verstappen in the paddock';image.attrs.pop('srcset',None)

# A gallery entry is an actual sourced model or view, never an invented helmet.
unique_helmets=[]
for helmet in assets['helmets']:
    if len(helmet['images'])>1 and helmet['title'] not in [h['title'] for h in unique_helmets]: unique_helmets.append(helmet)
unique_helmets.sort(key=lambda h:int(re.search(r'20\d\d',h['title']).group()) if re.search(r'20\d\d',h['title']) else 0,reverse=True)
views = ['View 01', 'View 02', 'View 03', 'View 04', 'View 05', 'View 06']
for i, item in enumerate(soup.select('.helmet-grid-item')):
    helmet = unique_helmets[i % len(unique_helmets)]
    view = i // len(unique_helmets)
    pics = helmet['images']
    for j, image in enumerate(item.select('.helmet-grid-item-img-helmet,.helmet-grid-item-reveal-img')):
        image['src'] = pics[(view+j) % len(pics)]
        image['alt'] = helmet['title']+' · '+views[view % len(views)]
        image.attrs.pop('srcset',None)
    label = item.parent.select_one('h3')
    name=re.sub(r'1:2|Max Verstappen|Mini Helmet|20\d\d','',helmet['title']).strip()
    if label: label.string = name+' / '+views[view % len(views)]
    for text in list(item.parent.find_all(string=re.compile(r'^20\d\d$'))):
        text.replace_with(re.search(r'20\d\d',helmet['title']).group())
    item['data-max-helmet'] = str(assets['helmets'].index(helmet))
    item['role']='button';item['tabindex']='0'

# Use the real MV emblem in signature/image positions, preserving their boxes.
for image in soup.find_all('img'):
    src=image.get('src','')
    if 'signature' in src.lower():
        image['src']='/max/signature.png';image['alt']='Max Verstappen signature';image['class']=image.get('class',[])+['mv-signature-image'];image.attrs.pop('srcset',None)
    elif any(t in src.lower() for t in ['ln-logo','ln4-logo','norris-text','ln1.webp','blobs_footer']):
        image['src']='/max/mv-orange.svg';image['alt']='MV';image.attrs.pop('srcset',None)

for i,image in enumerate(soup.select('.is-exe-scroll')):
    image['src']=photos[[4,12,18,10][i%4]]['path'];image['alt']='Max Verstappen · Racing moments';image.attrs.pop('srcset',None)
for image in soup.select('.footer-bg-img'):
    image['src']=unique_helmets[0]['images'][0];image['alt']='Max Verstappen helmet'

# Avoid showing another driver's partner marks as Max endorsements.
worlds=['RED BULL RACING','VERSTAPPEN RACING','TEAM REDLINE','VERSTAPPEN.COM']
for i,image in enumerate(soup.select('.home-collab-marquee-svg,.footer-marquee-svg')):
    name=f'world-{i%4}.svg'
    image['src']='/max/'+name;image['alt']=worlds[i%4];image.attrs.pop('srcset',None)
    markup=f'<svg xmlns="http://www.w3.org/2000/svg" width="500" height="100" viewBox="0 0 500 100"><text x="250" y="65" fill="#dde1d2" font-family="sans-serif" font-weight="900" text-anchor="middle" font-size="32">{worlds[i%4]}</text></svg>'
    (PUBLIC/'max'/name).write_text(markup)
    if image.name!='img':
        image.clear();image.append(BeautifulSoup(markup,'html.parser'))

for anchor in soup.select('a[href]'):
    href=anchor['href']
    if 'landonorris' in href and ('store' in href or '.store' in href):
        anchor['href']='https://store.verstappen.com/en/';anchor['target']='_blank';anchor['rel']='noopener noreferrer'
    elif 'instagram.com/' in href: anchor['href']='https://www.instagram.com/maxverstappen1/'
    elif 'youtube.com/' in href: anchor['href']='https://www.youtube.com/@MaxVerstappen1'
    elif 'tiktok.com/' in href:
        anchor['href']='https://www.facebook.com/MaxVerstappen'
        for node in anchor.find_all(string=re.compile('tiktok',re.I)):node.replace_with('Facebook')
    elif 'twitch.tv/' in href:
        anchor['href']='https://twitter.com/Max33Verstappen'
        for node in anchor.find_all(string=re.compile('twitch',re.I)):node.replace_with('X / Twitter')
    elif href.startswith('mailto:'):
        anchor['href']='#about';anchor['data-mv-panel']='about'
    elif href.startswith('/legal/'):
        anchor['href']='#about';anchor['data-mv-panel']='about'
    if anchor.has_attr('title'): anchor['title']=anchor['title'].replace('Lando','Max')
    if anchor.has_attr('data-signup-trigger'):
        anchor['href']='#about';anchor['data-mv-panel']='about'

for text in list(soup.find_all(string=True)):
    if isinstance(text, Comment): continue
    if text.parent.name in ['script','style']:continue
    replacements={"World Drivers' Champion":"The Verstappen Collection",
                  '© 2026 Max Verstappen.':'MV33 — Fan-made study.',
                  'business enquiries':'About this site','Sign\u00a0Up':'About','Sign Up':'About',
                  'Message from max':'Discover Max',
                  'Celebrate this incredible moment with a collection designed for the fans who never stopped believing. Wear it, frame it, treasure it forever.':'Explore the world of Max Verstappen. Racing, helmets and collectibles, brought together for the fans.',
                  'Lando is proud':'Max is proud',
                  'Since I was 7 years old and had my first experience with kart racing, I’ve worked tirelessly to make that dream come true.':'From the paddock to the podium. A life shaped by racing, on and off the track.',
                  'From his iconic blobs to innovative one-off designs, Max has always been passionate about designing innovative and memorable helmets.':'Explore the details of Max’s helmets, from season designs to special editions and memorable race weekends.',
                  'Max is proud to collaborate with a range of partners, who share his passion for performance across a range of industries.':'From Formula 1 to GT racing and the virtual circuit. Explore the worlds of Max Verstappen.'}
    value=str(text)
    for a,b in replacements.items():value=value.replace(a,b)
    if value!=str(text):text.replace_with(value)

for quote in soup.select('.horizontal-item-text'):
    if 'It doesn’t matter' in quote.get_text():
        quote.clear()
        quote.append(BeautifulSoup('A life shaped by <span class="span-green-off-white-1">racing</span>, on the track and <span class="span-green-off-white-1">beyond</span> every finish line.', 'html.parser'))
for heading in soup.select('h2'):
    if 'World Drivers' in heading.get_text():
        heading.clear();heading.append(BeautifulSoup('THE VERSTAPPEN<br/>COLLECTION', 'html.parser'))

# Preserve English line geometry; translations sit in existing paragraph flow.
translations={
    'Most recent results, career stats and photos from trackside.':'赛道之上：比赛记录与围场影像。',
    'Campaigns, shoots and other such promotional materials for fans':'赛道之外：生活、活动与赛车热爱。',
    'From his iconic blobs to innovative one-off designs, Max has always been passionate about designing innovative and memorable helmets.':'头盔收藏：不同赛季的设计与细节。',
    'Lando is proud to collaborate with a range of partners, who share his passion for performance across a range of industries.':'从 F1 到模拟赛车，探索维斯塔潘的竞速世界。',
    'Explore the world of Max Verstappen. Racing, helmets and collectibles, brought together for the fans.':'探索维斯塔潘的赛车、头盔与收藏世界。',
    'Explore the details of Max’s helmets, from season designs to special editions and memorable race weekends.':'从赛季设计到特别涂装，近看维斯塔潘的头盔收藏。',
    'From Formula 1 to GT racing and the virtual circuit. Explore the worlds of Max Verstappen.':'从 F1、GT 赛车到虚拟赛道，探索维斯塔潘的竞速世界。',
}
for p in list(soup.select('p')):
    txt=p.get_text(' ',strip=True)
    if txt in translations:
        span=soup.new_tag('span');span['class']=['mv-zh'];span.string=translations[txt];p.append(span)
for h in list(soup.select('h2')):
    txt=h.get_text(' ',strip=True).lower()
    if txt in ['helmets','partners','what’s up on socials']:
        h['data-zh']={'helmets':'头盔收藏','partners':'竞速世界','what’s up on socials':'社交动态'}[txt]

# This is a driver showcase: remove purchase links instead of redirecting to a shop.
for anchor in list(soup.select('a[href]')):
    if any(host in anchor['href'] for host in ['store.verstappen.com', 'landonorris.store', 'store.landonorris']):
        anchor.decompose()
for node in list(soup.find_all(string=True)):
    if node.parent.name in ['script', 'style'] or isinstance(node, Comment): continue
    text = str(node)
    for old, new in [('LANDO STORE', 'RACING MOMENTS'), ('THE VERSTAPPEN', 'A LIFE IN'),
                     ('COLLECTION', 'RACING'), ('The Verstappen Collection', 'A Life in Racing'),
                     ('Explore the world of Max Verstappen. Racing, helmets and collectibles, brought together for the fans.',
                      'From the paddock to the podium. Moments from a life in racing.'),
                     ('探索维斯塔潘的赛车、头盔与收藏世界。', '从围场到领奖台，记录维斯塔潘的竞速时刻。')]:
        text = text.replace(old, new)
    if text != str(node): node.replace_with(text)
# Shopping-bag ornament belonged to the old promotion.
for label in soup.select('.text-eyebrow'):
    if label.get_text(strip=True) == 'RACING MOMENTS':
        icon = label.parent.select_one('.eyebrow-icon-w')
        if icon: icon.decompose()
# LN artwork is embedded in the transition and landscape-warning Rive files.
# Keep their timing hooks but replace the visible art with the official MV mark.
for canvas in soup.select('[data-rive-mob-landscape]'):
    canvas['class'] = canvas.get('class', []) + ['mv-original-logo']
    image = soup.new_tag('img', src='/max/mv-orange.svg', alt='MV')
    image['class'] = ['mv-transition-logo']
    canvas.parent.append(image)

# Two real edition routes, accessible from the archive and the main menu.
edition_links='<div class="mv-editions"><a href="/helmets/season-2023/">SEASON 2023 / 常规款 ↗</a><a href="/helmets/zandvoort-2024/">ZANDVOORT 2024 / 荷兰站 ↗</a></div>'
archive=soup.select_one('.helmet-grid')
if archive: archive.insert_before(BeautifulSoup(edition_links,'html.parser'))
menu=soup.select_one('.nav-menu-links-col')
if menu: menu.append(BeautifulSoup(edition_links,'html.parser'))
footer=soup.select_one('.footer-links-col')
if footer: footer.append(BeautifulSoup(edition_links,'html.parser'))
credit=soup.new_tag('p');credit['class']=['mv-model-credit']
credit.append(BeautifulSoup('3D: <a href="https://skfb.ly/pEDBZ" target="_blank" rel="noopener">“Helmet Redbull - Max Verstappen”</a> by Maubian / <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>. Adapted mesh scale, web textures and livery.','html.parser'))
if footer:footer.append(credit)

# Remove any remaining reference-only photographic fallbacks.
for image in soup.select('.is-collab-placeholder,.is-footer-rive'):
    image['src']='/max/mv-orange.svg';image['alt']='MV'

# A responsive srcset must never override a substituted Max photograph.
for image in soup.select('img[src^="/max/"]'):
    image.attrs.pop('srcset',None)
    image.attrs.pop('sizes',None)

for icon in list(soup.select('link[rel~="icon"],link[rel="apple-touch-icon"]')):
    icon.decompose()
soup.head.append(soup.new_tag('link', rel='icon', type='image/svg+xml', href='/max/favicon-light.svg', id='mv-favicon'))

head_style=soup.new_tag('link',rel='stylesheet',href='/mv33.css');soup.head.append(head_style)
bridge=soup.new_tag('script',src='/texture-bridge.js');
soup.head.insert(0,bridge)
for src in ['/intro.js','/helmet-materials.js']:
    soup.head.append(soup.new_tag('script',src=src))
app=soup.new_tag('script',src='/mv33.js',defer='');soup.body.append(app)
data=soup.new_tag('script',id='mv33-assets',type='application/json');data.string=json.dumps(assets,ensure_ascii=False);soup.body.append(data)

# Content-address adapters so an existing preview cannot reuse yesterday's scripts.
for tag, attr in [(t, 'src') for t in soup.select('script[src]')] + [(t, 'href') for t in soup.select('link[href]')]:
    url = tag[attr]
    if url in ['/texture-bridge.js', '/mv33.js', '/mv33.css', '/intro.js', '/helmet-materials.js']:
        tag[attr] = url + '?v=' + hashlib.sha256((PUBLIC/url.lstrip('/')).read_bytes()).hexdigest()[:12]
for path in (PUBLIC/'reference').glob('*.css'):
    css=path.read_text()
    for url in set(re.findall(r'https://cdn\.prod\.website-files\.com/[^\s"\x27)]+',css)):
        css=css.replace(url,local(url))
    path.write_text(css)

engine=(ROOT/'reference/lando-engine.js').read_text()
engine=engine.replace('https://lando.itsoffbrand.io/gl','/gl')
engine=engine.replace('https://assets.itsoffbrand.io/lando/rive/','/rive/')
engine=engine.replace('https://lando.itsoffbrand.io/rive/','/rive/')
engine=engine.replace('f.wasmURL="https://unpkg.com/".concat(C.name,"@").concat(C.version,"/rive.wasm")','f.wasmURL="/rive/rive.wasm"')
engine=engine.replace('iQ=window.innerWidth>991?"webp":"ktx2"','iQ="webp"')
engine=engine.replace('this.activeTextureLoader=window.innerWidth>991?this.customTextureLoader:this.customKtx2TextureLoader','this.activeTextureLoader=this.customTextureLoader')
engine=engine.replace('customTextureLoader(A,Q){return new Promise((B)=>{this.textureLoader.load(A,',
'''customTextureLoader(A,Q){return new Promise(async(B)=>{try{if(window.mv33TextureURL)A=await window.mv33TextureURL(A);this.textureLoader.load(A,''')
engine=engine.replace('B(),Q(E)},void 0,(E)=>{console.error(E)})})}customKtx2TextureLoader',
'''B(),Q(E)},void 0,(E)=>{console.error(E);B()})}catch(e){console.error(e);B()}})}customKtx2TextureLoader''',1)
engine=engine.replace('WE DID IT AT HOME WE DID IT AT HOME','MAX VERSTAPPEN MAX VERSTAPPEN')
engine=engine.replace('A BRITISH GP WEEKEND I WILL REMEMBER FOREVER','A LIFE IN RACING ON AND OFF THE TRACK')
# Slightly stronger pointer tilt makes the inferred front-surface depth legible.
engine=engine.replace('movement:{intensity:0.075,ease:0.025}', 'movement:{intensity:0.095,ease:0.025}',1)
# Keep the reference displaced-portrait architecture, with enough geometry for inferred facial depth.
engine=engine.replace('new QB(1,1,128,128)','new QB(1,1,256,256)')
engine=engine.replace('normalMap:this.gl.assets.textures.head.normal,roughnessMap:this.gl.assets.textures.head.roughness,metalnessMap:this.gl.assets.textures.head.roughness','normalMap:this.gl.assets.textures.head.normal,normalScale:new kA(0.3,0.3),roughness:0.8,metalness:0')
# Match a Retina display instead of the reference's desktop 1.25 DPR cap.
engine=engine.replace('this.width>768?Math.min(window.devicePixelRatio,1.25):Math.min(window.devicePixelRatio,2)','Math.min(window.devicePixelRatio,2)')
# Retain the source boot sequencing, replace its LN-specific Rive transition art.
start=engine.index('async function BL(){');end=engine.index('var xU,mj=',start)
engine=engine[:start]+"async function BL(){window.mv33Transition.mount();xJ={initialInput:{value:true},transitionInInput:{value:false},transitionOutInput:{value:false}};return xJ;}function EL(){window.mv33Transition.cover();}function H$(){window.mv33Transition.reveal();}"+engine[end:]
# Render the author's actual GLB, preserving its UVs and native PBR materials.
source_model='/models/source-fit-season-2023.glb?v='+hashlib.sha256((PUBLIC/'gl/models/source-fit-season-2023.glb').read_bytes()).hexdigest()[:12]
artist_model='/models/season-2023.glb?v='+hashlib.sha256((PUBLIC/'gl/models/season-2023.glb').read_bytes()).hexdigest()[:12]
engine=engine.replace('vQ+"/models/helmet-21.glb"','(new URLSearchParams(location.search).get("helmet")==="source"?vQ+"'+source_model+'":vQ+"'+artist_model+'")')
engine=engine.replace('this.helmet=new F9({scene:this.defaultScene,camera:this.camera}),document.addEventListener', 'this.helmet=new F9({scene:this.defaultScene,camera:this.camera}),window.mv33HeadScene=this,document.addEventListener')
start=engine.index('class F9{');end=engine.index('var a5=',start)
engine=engine[:start]+(ROOT/'scripts/helmet-scene.js').read_text()+engine[end:]
# Later scroll scenes use the same authored material maps rather than Norris art.
for variant in ['Lime','Dark','Grid','Disco','Google']:
    engine=engine.replace('this.gl.assets.textures.helmet.diffuse'+variant,
                          'this.gl.assets.models.helmet.scene.getObjectByName("helmet").material.map')
engine=engine.replace('normalMap:this.gl.assets.textures.helmet.normal,metalness:1,roughness:0.05,envMap:this.gl.assets.hdri.light,envMapIntensity:3',
                      'map:this.gl.assets.models.helmet.scene.getObjectByName("helmet").material.map,metalness:0.35,roughness:0.3,envMap:this.gl.assets.hdri.light,envMapIntensity:1')
engine=engine.replace('map:this.gl.assets.textures.glass.base,roughnessMap:this.gl.assets.textures.glass.roughness,normalMap:this.gl.assets.textures.glass.normal,metalnessMap:this.gl.assets.textures.helmet.metallic,',
                      'map:this.gl.assets.models.helmet.scene.getObjectByName("glass").material.map,metalness:0.75,roughness:0.16,')
(PUBLIC/'engine.js').write_text(engine)
soup.select_one('script[src^="/engine.js"]')['src'] = '/engine.js?v=' + hashlib.sha256(engine.encode()).hexdigest()[:12]
(PUBLIC/'index.html').write_text(str(soup))
print('Built public/index.html and patched original renderer.')
