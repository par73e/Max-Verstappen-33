"""Build a local MV33 adaptation from the retained reference DOM and renderer."""
import json
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
        script['src'] = '/engine.js'
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
    image = soup.new_tag('img', src='/max/mv.svg', alt='MV')
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
        image['src']='/max/mv.svg';image['alt']='MV';image.attrs.pop('srcset',None)

for i,image in enumerate(soup.select('.is-exe-scroll')):
    image['src']=assets['banners'][[0,1,2,3][i%4]]['path'];image['alt']='Verstappen collection';image.attrs.pop('srcset',None)
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

# Remove any remaining reference-only photographic fallbacks.
for image in soup.select('.is-collab-placeholder,.is-footer-rive'):
    image['src']='/max/mv.svg';image['alt']='MV'

# A responsive srcset must never override a substituted Max photograph.
for image in soup.select('img[src^="/max/"]'):
    image.attrs.pop('srcset',None)
    image.attrs.pop('sizes',None)

head_style=soup.new_tag('link',rel='stylesheet',href='/mv33.css');soup.head.append(head_style)
bridge=soup.new_tag('script',src='/texture-bridge.js');
soup.head.insert(0,bridge)
app=soup.new_tag('script',src='/mv33.js',defer='');soup.body.append(app)
data=soup.new_tag('script',id='mv33-assets',type='application/json');data.string=json.dumps(assets,ensure_ascii=False);soup.body.append(data)

(PUBLIC/'index.html').write_text(str(soup))
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
# Keep the same 3D geometry, slicing shader and timelines; replace the livery
# sampling with a frontal photographic projection of the sourced Max helmet.
engine=engine.replace('texture2D(tCurrentTexture, vUv)','texture2D(tCurrentTexture, vec2(vLocalPosition.x * 9.0 + 0.5, vLocalPosition.y * 9.0 + 0.52))')
engine=engine.replace('texture2D(tNextTexture, vUv)','texture2D(tNextTexture, vec2(vLocalPosition.x * 9.0 + 0.5, vLocalPosition.y * 9.0 + 0.52))')
(PUBLIC/'engine.js').write_text(engine)
print('Built public/index.html and patched original renderer.')
