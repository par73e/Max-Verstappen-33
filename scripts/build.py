"""Build a local MV33 adaptation from the retained reference DOM and renderer."""
import copy
import json
import hashlib
import re
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment
from PIL import Image
from theme import theme_colors,theme_engine,PALETTE,rive_transfer

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT/'public'
assets = json.loads((ROOT/'max-assets.json').read_text())
content = json.loads((ROOT/'content/max.json').read_text())
soup = BeautifulSoup((ROOT/'reference/lando-home.html').read_text(), 'html.parser')

def local(url):
    if url.startswith('https://cdn.prod.website-files.com/') or url.startswith('https://d3e54v103j8qbb.cloudfront.net/'):
        name = urllib.parse.unquote(urllib.parse.urlparse(url).path.rsplit('/', 1)[-1])
        if (PUBLIC/'reference'/name).exists():
            if name.endswith('.svg'):
                original=(PUBLIC/'reference'/name).read_text()
                themed=theme_colors(original)
                if themed!=original:
                    (PUBLIC/'theme-vectors').mkdir(exist_ok=True)
                    (PUBLIC/'theme-vectors'/name).write_text(themed)
                    return '/theme-vectors/'+urllib.parse.quote(name)
            return '/reference/'+urllib.parse.quote(name)
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
    logo = BeautifulSoup((PUBLIC/'max/mv-orange.svg').read_text(), 'html.parser').svg
    # Hide the tiny registered-trademark glyph in this compact animated mark.
    for path in logo.select('g > path')[3:]: path.decompose()
    logo['viewbox'] = '0 0 674 336'
    logo['class'] = ['mv-logo-overlay']
    logo['aria-label'] = 'Max Verstappen'
    logo['role'] = 'img'
    for i, path in enumerate(logo.select('g > path')[:3]):
        path['class'] = ['mv-logo-piece', 'mv-logo-core' if i == 2 else 'mv-logo-wing']
    canvas.parent.append(logo)

mobile_name=soup.select_one('.home-hero-tablet-text-w')
if mobile_name:
    mobile_name.clear()
    mobile_name.append(BeautifulSoup('<div class="mv-mobile-wordmark"><span>MAX</span><strong>VERSTAPPEN</strong></div>', 'html.parser'))

photos = assets['photos']
photo_order = [0, 1, 10, 11, 12, 13, 14, 17, 18, 20]
for i, image in enumerate(soup.select('.is-horizontal-scroll')):
    p = photos[photo_order[i % len(photo_order)] % len(photos)]
    image['src'] = p['path']; image['alt'] = 'Max Verstappen · 官方赛事影像'
    image.attrs.pop('srcset', None); image.attrs.pop('sizes', None)
    tile=image.find_parent(class_='horizontal-item') or image.parent.parent
    for caption in tile.find_all(string=re.compile(r', 20\d\d$')):
        source_url=next((r['url'] for r in json.loads((ROOT/'assets-manifest.json').read_text()) if r.get('path')=='public'+p['path']), '')
        place='Mexico City' if 'GP_Mexico' in source_url else 'São Paulo' if 'GP_Sao_Paulo' in source_url else 'Race archive'
        year=re.search(r'/img/(20\d{2})/',source_url)
        caption.replace_with(place+(', '+year.group(1) if year else ''))
for i, image in enumerate(soup.select('.menu-img-top,.menu-img-no-blend')):
    p = photos[[2, 4, 12, 1, 10][(i//2)%5] % len(photos)]
    image['src'] = p['path'];image['alt']='Max Verstappen'
    image.attrs.pop('srcset', None)
for i, image in enumerate(soup.select('.is-social-card')):
    p = photos[[4, 5, 8, 15, 21, 27, 28][i % 7] % len(photos)]
    image['src']=p['path'];image['alt']='Max Verstappen · 赛事影像'
    image.attrs.pop('srcset',None)
for i, image in enumerate(soup.select('.otot-home-img')):
    image['src']=photos[[7,24][i%2]]['path'];image['alt']='Max Verstappen'
    image.attrs.pop('srcset',None)
for image in soup.select('.is-otot-home-end'):
    image['src']='/max/max-rb20-seated-3840.webp';image['alt']='Max Verstappen seated beside the RB20 · Will Cornelius / Red Bull Content Pool, 2024';image.attrs.pop('srcset',None)

# One canonical right-facing view per real design. Alternate angles remain
# in each detail page instead of repeating the same design across the archive.
archive_cards=json.loads((ROOT/'content/helmet-archive.json').read_text())
items=soup.select('.helmet-grid-item')
for i,item in enumerate(items):
    if i>=len(archive_cards):
        outer=item.find_parent(class_='w-dyn-item')
        (outer or item.parent).decompose()
        continue
    card=archive_cards[i]
    image=item.select_one('.helmet-grid-item-img-helmet')
    image['src']=card['image'];image['alt']=f"Max Verstappen {card['name']} {card['year']} · right-facing three-quarter view"
    image.attrs.pop('srcset',None);image.attrs.pop('sizes',None)
    # Read alpha bounds; position with CSS instead of mutating the source bitmap.
    with Image.open(PUBLIC/card['image'].lstrip('/')) as bitmap:
        x0,y0,x1,y1=bitmap.getchannel('A').point(lambda a:255 if a>32 else 0).getbbox()
        scale=min(406.89*.64/(x1-x0),411*.54/(y1-y0))
        left=(406.89-(x1-x0)*scale)/2-x0*scale
        top=(411-(y1-y0)*scale)/2-y0*scale-411*.01
        image['style']=f'width:{bitmap.width*scale/406.89*100:.4f}%;height:{bitmap.height*scale/411*100:.4f}%;left:{left/406.89*100:.4f}%;top:{top/411*100:.4f}%'
    reveal=item.select_one('.helmet-grid-item-reveal-img')
    reveal['src']=card['worn'];reveal['alt']=f"Max Verstappen wearing {card['name']} {card['year']}"
    reveal.attrs.pop('srcset',None);reveal.attrs.pop('sizes',None)
    reveal['style']=f'object-position:{card["wornPosition"]};transform:scale({card.get("wornScale",1)});transform-origin:{card["wornPosition"]}'
    reveal['loading']='eager';reveal['decoding']='async';reveal['fetchpriority']='low'
    window=soup.new_tag('div');window['class']=['mv-helmet-reveal-window'];window['aria-hidden']='true'
    photo=soup.new_tag('div');photo['class']=['mv-helmet-reveal-photo']
    reveal.wrap(photo);photo.wrap(window)
    item['data-mv-worn']='';item['data-helmet-edition']=card['id']
    label=item.parent.select_one('h3')
    if label:label.string=card['name']
    for year in item.parent.select('.text-title-small-label.date'):year.string=card['year']
    item['data-max-helmet']=str(card['assetIndex'])
    item.name='a';item['href']='/helmets/'+card['id']+'/';item['role']='link';item['tabindex']='0'

# Use the real MV emblem in signature/image positions, preserving their boxes.
for image in soup.find_all('img'):
    src=image.get('src','')
    if 'signature' in src.lower():
        image['src']='/max/signature-orange.svg';image['alt']='Max Verstappen signature';image['class']=image.get('class',[])+['mv-signature-image'];image.attrs.pop('srcset',None)
    elif any(t in src.lower() for t in ['ln-logo','ln4-logo','norris-text','ln1.webp']):
        image['src']='/max/mv-orange.svg';image['alt']='MV';image.attrs.pop('srcset',None)

for i,image in enumerate(soup.select('.is-exe-scroll')):
    image['src']=photos[[2,6,19,26][i%4]]['path'];image['alt']='Max Verstappen · Racing moments';image.attrs.pop('srcset',None)
for image in soup.select('.footer-bg-img'):
    image['src']='/max/footer-max-worn-2024.png';image['alt']='Max Verstappen wearing his 2024 helmet and Red Bull race suit';image.attrs.pop('srcset',None)

# Avoid showing another driver's partner marks as Max endorsements.
worlds=['RED BULL RACING','VERSTAPPEN RACING','VERSTAPPEN SIM RACING','VERSTAPPEN.COM']
for i,image in enumerate(soup.select('.home-collab-marquee-svg,.footer-marquee-svg')):
    name=f'world-{i%4}.svg'
    image['src']='/max/'+name;image['alt']=worlds[i%4];image.attrs.pop('srcset',None)
    markup=f'<svg xmlns="http://www.w3.org/2000/svg" width="500" height="100" viewBox="0 0 500 100"><text x="250" y="65" fill="#dde1d2" font-family="sans-serif" font-weight="900" text-anchor="middle" font-size="32"'+(' textLength="460" lengthAdjust="spacingAndGlyphs"' if i%4==2 else '')+f'>{worlds[i%4]}</text></svg>'
    (PUBLIC/'max'/name).write_text(theme_colors(markup))
    if image.name!='img':
        image.clear();image.append(BeautifulSoup(markup,'html.parser'))

# Keep the reference logo-strip scale instead of tiny uniform body labels.
for i,mark in enumerate(soup.select('.footer-marquee-svg')):
    if i%4==3:
        # Standalone SVG is XML: retain viewBox/clipPath case from the original.
        artwork=re.sub(r'fill="#[0-9a-fA-F]+"','fill="#d8e1ed"',(PUBLIC/'max/mv.svg').read_text())
        if mark.name=='img':
            (PUBLIC/'max/footer-mv.svg').write_text(artwork);mark['src']='/max/footer-mv.svg';mark['alt']='Max Verstappen'
        else:
            mark.clear();mark.append(BeautifulSoup(artwork,'html.parser').svg)
    else:
        label=worlds[i%4]
        lines=['RED BULL','RACING'] if i%4==0 else ['VERSTAPPEN','RACING' if i%4==1 else 'SIM RACING']
        width=300 if i%4==0 else 430
        artwork=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="140" viewBox="0 0 {width} 140"><g fill="#d8e1ed" text-anchor="middle" font-family="Mona Sans Variable,Arial,sans-serif" font-weight="850" font-size="62" letter-spacing="-2"><text x="{width/2}" y="60">{lines[0]}</text><text x="{width/2}" y="125">{lines[1]}</text></g></svg>'
        if mark.name=='img':
            file=f'footer-world-{i%4}.svg';(PUBLIC/'max'/file).write_text(artwork);mark['src']='/max/'+file;mark['alt']=label
        else:mark.clear();mark.append(BeautifulSoup(artwork,'html.parser'))

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
        pass
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
edition_links='<div class="mv-editions"><a href="/helmets/">HELMET ARCHIVE / 头盔档案 ↗</a><a href="/helmets/zandvoort-2024/">ORANGE TRIBUTE / 橙色致敬 ↗</a></div>'
archive=soup.select_one('.helmet-grid')
if archive: archive.insert_before(BeautifulSoup(edition_links,'html.parser'))
# Restore the reference's primary header control as a local archive action.
reference_dom=BeautifulSoup((ROOT/'reference/lando-home.html').read_text(),'html.parser')
archive_button=copy.deepcopy(reference_dom.select_one('.btn-layout.is-nav a'))
archive_button['href']='/helmets/';archive_button.attrs.pop('target',None)
archive_button.select_one('.btn-text').string='Helmets'
icon=archive_button.select_one('.btn-icon-svg');icon.clear();icon.append(BeautifulSoup('<img src="/max/mv-orange.svg" alt="" style="width:100%;height:100%;object-fit:contain;filter:brightness(0)">','html.parser'))
soup.select_one('.btn-layout.is-nav').insert(0,archive_button)
footer=soup.select_one('.footer-links-col')
footer_archive=copy.deepcopy(reference_dom.select_one('.footer-links-col > a'))
footer_archive['href']='/helmets/';footer_archive.attrs.pop('target',None)
footer_archive.select_one('.btn-text').string='Helmets'
if footer:footer.append(footer_archive)
# Source footer columns keep their original height. Asset/geometry credits live
# in the About dialog, legal page and asset library rather than this link lane.
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

# Render the MV loading frame in HTML, before the engine can mount its animation.
# The reference transition otherwise paints lime while scripts/assets are loading.
transition=soup.select_one('.transition-w')
# Keep the original loader hooks: the engine captures them before mount().
poster=soup.new_tag('div',attrs={'class':'mv-intro-poster','aria-label':'MV'})
breath=soup.new_tag('div',attrs={'class':'mv-loader-breath','aria-hidden':'true'})
for i,path in enumerate(BeautifulSoup((PUBLIC/'max/mv-orange.svg').read_text(),'html.parser').find_all('path')[:3]):
    piece=soup.new_tag('span',attrs={'class':['mv-loader-piece',['mv-loader-right','mv-loader-left','mv-loader-core'][i]]})
    mark=soup.new_tag('svg',attrs={'viewBox':'0 0 674 336','aria-hidden':'true'})
    mark.append(path);piece.append(mark);breath.append(piece)
poster.append(breath)
transition.append(poster)
critical=soup.new_tag('style',id='mv-first-paint')
# Keep the root background transparent: the reference WebGL wrapper uses z-index
# -1 and otherwise gets painted underneath the opaque body background.
critical.string='''.transition-w:not([data-phase]){display:block!important;position:fixed;inset:0;width:100%;height:100%;z-index:9999;background:#101823!important}
.transition-w:not([data-phase])>:not(.mv-intro-poster),.transition-w[data-phase]>:not(.mv-intro):not(.mv-intro-poster):not(.mv-cover){visibility:hidden}
.mv-intro-poster{position:absolute;inset:0;display:grid;place-items:center}
.mv-intro-poster svg{display:block;width:min(30vw,210px);height:auto}'''+(PUBLIC/'loader.css').read_text()

head_style=soup.new_tag('link',rel='stylesheet',href='/mv33.css');soup.head.append(head_style)
soup.head.append(soup.new_tag('link',rel='stylesheet',href='/theme.css'))
bridge=soup.new_tag('script',src='/texture-bridge.js');
soup.head.insert(0,bridge)
soup.head.insert(0,critical)
palette_script=soup.new_tag('script');palette_script.string='window.mv33Palette='+json.dumps(PALETTE)+';'
soup.head.insert(1,palette_script)
# Rive's hardware renderer retains embedded artwork colors. A palette-specific
# sRGB transfer maps only its output canvases, leaving photos and WebGL untouched.
filter_svg='<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="position:absolute;width:0;height:0;pointer-events:none"><defs><filter id="mv-rive-palette" color-interpolation-filters="sRGB">'+rive_transfer()+'</filter></defs></svg>'
soup.body.insert(0,BeautifulSoup(filter_svg,'html.parser'))
for src in ['/render-budget.js','/intro.js','/helmet-materials.js','/page-transition.js']:
    soup.head.append(soup.new_tag('script',src=src))
app=soup.new_tag('script',src='/mv33.js',defer='');soup.body.append(app)
data=soup.new_tag('script',id='mv33-assets',type='application/json');data.string=json.dumps(assets,ensure_ascii=False);soup.body.append(data)
bio=soup.new_tag('script',id='mv33-content',type='application/json');bio.string=json.dumps(content,ensure_ascii=False).replace('<','\\u003c');soup.body.append(bio)

# Factual adaptation is explicit and source-backed, not a surname substitution.
statement=soup.select_one('.impact-content-w .text-impact-lg-mona')
if statement:statement.clear();statement.append(BeautifulSoup(content['copy']['statement'],'html.parser'))
for quote,key in zip(soup.select('.horizontal-item-text'),['galleryTitles','galleryDebut']):
    quote.clear();quote.append(BeautifulSoup(content['copy'][key],'html.parser'))
for block,key in zip(soup.select('.otot-home-text-col'),['onTrack','offTrack']):
    p=block.select_one('p')
    if p:p.clear();p.append(BeautifulSoup(content['copy'][key]['en']+'<span class="mv-zh">'+content['copy'][key]['zh']+'</span>','html.parser'))
for p in soup.select('p'):
    if 'From Formula 1 to GT racing' in p.get_text():
        p.clear();p.append(BeautifulSoup(content['copy']['worlds']['en']+'<span class="mv-zh">'+content['copy']['worlds']['zh']+'</span>','html.parser'))
for node in list(soup.find_all(string=True)):
    if isinstance(node,Comment) or node.parent.name in ['script','style']:continue
    value=str(node)
    for old,new in [('Next Race','Race Archive'),('Calendar','Calendar'),('Sāo Paulo','São Paulo'),('Hall of Fame','Design Archive'),('view partnerships','Explore racing'),('Partnerships','Racing Worlds'),('partners','RACING'),('&campaigns','BEYOND F1'),('All rights reserved','Unofficial fan site')]:value=value.replace(old,new)
    if value!=str(node):node.replace_with(value)
for badge in soup.select('.horizontal-pill-text'):badge.string='MV'
footer_title=soup.select_one('h2.footer')
if footer_title:
    footer_title.clear();footer_title.append(BeautifulSoup('Always <span class="text-impact-sm-brier c-lime-off">bringing</span> the <span class="text-impact-sm-brier c-lime-off">fight</span>.','html.parser'))
for a in soup.select('.home-hero-next-race-row[href]'):a.attrs.pop('data-mv-panel',None)
for label in soup.select('.footer-bg-bottom-btn-w .btn-text'):label.string='About this project'
for meta in soup.select('meta[property],meta[name]'):
    key=meta.get('property',meta.get('name',''))
    if key in ['og:image','twitter:image']:meta['content']='/max/portrait-serious-2k.png'
    elif key=='og:type':meta['content']='website'
    elif key in ['description','og:description','twitter:description']:meta['content']='Max Verstappen · Oracle Red Bull Racing · Four-time F1 world champion, 2021–2024. 维斯塔潘主题非官方车迷网站。'
for title in soup.select('h2.screen-reader'):title.string='Four-time Formula 1 World Champion · 2021–2024'

# Content-address adapters so an existing preview cannot reuse yesterday's scripts.
for tag, attr in [(t, 'src') for t in soup.select('script[src]')] + [(t, 'href') for t in soup.select('link[href]')]:
    url = tag[attr]
    if url in ['/texture-bridge.js', '/mv33.js', '/mv33.css', '/intro.js', '/helmet-materials.js', '/render-budget.js', '/page-transition.js', '/theme.css']:
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
# Keep the reference pointer amplitude so the portrait does not drift away
# from the helmet during local reveals (the helmet uses 1/1.5 of head rotation).
# Keep the reference displaced-portrait architecture, with enough geometry for inferred facial depth.
engine=engine.replace('new QB(1,1,128,128)','new QB(1,1,256,256)')
# Touch screens have no hover pointer trail. Keep the explicit helmet lock/wipe,
# but prevent an old fluid-cursor streak from cutting through the resting face.
engine=engine.replace('uHelmetHover:new YA(0),','uHelmetHover:new YA(0),uPointerTrail:new YA(window.innerWidth>991?1:0),')
engine=engine.replace('Q.uniforms.uHelmetHover=this.uniforms.uHelmetHover,','Q.uniforms.uHelmetHover=this.uniforms.uHelmetHover,Q.uniforms.uPointerTrail=this.uniforms.uPointerTrail,')
engine=engine.replace('uniform float uHelmetHover;','uniform float uHelmetHover;\n uniform float uPointerTrail;')
engine=engine.replace('float cursorEffect = step(0.1, textureCursorEffect.r);','float cursorEdge = max(fwidth(textureCursorEffect.r), 0.01); float cursorEffect = smoothstep(0.1 - cursorEdge, 0.1 + cursorEdge, textureCursorEffect.r) * uPointerTrail;')
engine=engine.replace('if(this.headDefault.update(this.helmetRevealValue,this.scrollProgress),','if(this.renderPlane.mesh.material.uniforms.uPointerTrail.value=this.headDefault.uniforms.uPointerTrail.value=(window.innerWidth>991||document.querySelector("[data-home-swipe-toggle]")?.getAttribute("aria-pressed")==="true")?1:0,this.headDefault.update(this.helmetRevealValue,this.scrollProgress),')
engine=engine.replace('normalMap:this.gl.assets.textures.head.normal,roughnessMap:this.gl.assets.textures.head.roughness,metalnessMap:this.gl.assets.textures.head.roughness','normalMap:this.gl.assets.textures.head.normal,normalScale:new kA(0.3,0.3),roughness:0.8,metalness:0')
# Bound full-screen buffers while keeping texture and DOM/SVG source detail.
engine=engine.replace('this.width>768?Math.min(window.devicePixelRatio,1.25):Math.min(window.devicePixelRatio,2)',
    'Math.min(window.devicePixelRatio,this.width>768?1.5:2,Math.sqrt(3000000/(this.width*this.height)))')
# GSAP can tick at 120Hz. Render at 60Hz during interaction, 30Hz while idle,
# and never submit WebGL work for a hidden document. Use the actual frame delta.
engine=engine.replace('update(){if(this.isLoaded){if(this.renderer.update()',
    'update(){if(document.hidden)return;if(window.mv33RenderBudget){if(!window.mv33RenderBudget.beginFrame())return;this.time.delta=Math.min(window.mv33RenderBudget.deltaMs,33.3333333333)/10;}if(this.isLoaded){if(this.renderer.update()')
# Retain the source boot sequencing, replace its LN-specific Rive transition art.
start=engine.index('async function BL(){');end=engine.index('var xU,mj=',start)
engine=engine[:start]+"async function BL(){window.mv33Transition.mount();xJ={initialInput:{value:true},transitionInInput:{value:false},transitionOutInput:{value:false}};return xJ;}function EL(){window.mv33Transition.cover();}function H$(){window.mv33Transition.reveal();}"+engine[end:]
# Use reference proportions by default; keep the Maubian model as a comparison.
source_model='/models/source-fit-season-2023.glb?v='+hashlib.sha256((PUBLIC/'gl/models/source-fit-season-2023.glb').read_bytes()).hexdigest()[:12]
artist_name='season-2023-clean.glb'
artist_model='/models/'+artist_name+'?v='+hashlib.sha256((PUBLIC/'gl/models'/artist_name).read_bytes()).hexdigest()[:12]
engine=engine.replace('vQ+"/models/helmet-21.glb"','(new URLSearchParams(location.search).get("helmet")==="artist"?vQ+"'+artist_model+'":vQ+"'+source_model+'")')
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
engine=theme_engine(engine)
(PUBLIC/'engine.js').write_text(engine)
soup.select_one('script[src^="/engine.js"]')['src'] = '/engine.js?v=' + hashlib.sha256(engine.encode()).hexdigest()[:12]
(PUBLIC/'index.html').write_text(theme_colors(str(soup)))
print('Built public/index.html and patched original renderer.')
