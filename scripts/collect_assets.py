"""Acquire public reference files and Max assets with a reproducible source ledger."""
import concurrent.futures as futures
import hashlib
import json
import re
import shutil
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
REF = ROOT / 'reference'
MANIFEST = ROOT / 'assets-manifest.json'
PUBLIC.mkdir(exist_ok=True)
REF.mkdir(exist_ok=True)
previous_records = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
previous_assets = json.loads((ROOT/'max-assets.json').read_text()) if (ROOT/'max-assets.json').exists() else {}
records = [r for r in previous_records if r.get('role') in ['max-helmet-archive', 'max-signature']]

def fetch(url, path, source=None, role='reference'):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if not path.exists():
            request = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Referer': source or 'https://landonorris.com/',
            })
            with urllib.request.urlopen(request, timeout=35) as response:
                data = response.read()
            path.write_bytes(data)
        data = path.read_bytes()
        record = dict(path=str(path.relative_to(ROOT)), url=url,
                      source=source or url, role=role, bytes=len(data),
                      sha256=hashlib.sha256(data).hexdigest(), status='downloaded')
    except Exception as error:
        record = dict(path=str(path.relative_to(ROOT)), url=url,
                      source=source or url, role=role, status='failed', error=str(error))
    records.append(record)
    return record

def parallel(jobs):
    with futures.ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda args: fetch(*args), jobs))

def cdn_path(url):
    parsed = urllib.parse.urlparse(url)
    return PUBLIC / 'reference' / urllib.parse.unquote(parsed.path.rsplit('/', 1)[-1])

reference_html = Path('/private/tmp/mv33-reference.html').read_text()
engine = Path('/private/tmp/lando-engine.js').read_text()
css = Path('/private/tmp/lando-reference.css').read_text()
(REF / 'lando-home.html').write_text(reference_html)
(REF / 'lando-engine.js').write_text(engine)
(REF / 'lando.css').write_text(css)
soup = BeautifulSoup(reference_html, 'html.parser')
urls = set(re.findall(r'https://cdn\.prod\.website-files\.com/[^\s"\x27<>),]+', reference_html + css))
urls.update(e['src'] for e in soup.select('script[src]') if e['src'].startswith('https://d3e54'))
urls = {u for u in urls if re.search(r'\.(webp|png|jpe?g|svg|woff2|js|css)(?:\?|$)', u)}
parallel([(url, cdn_path(url), 'https://landonorris.com/', 'reference-design') for url in urls])

# The original renderer's asset paths, resolved without executing the bundle.
config = engine[engine.index('var vQ='):engine.index('async function BL')]
glpaths = set(re.findall(r'vQ\+"([^"]+)"', config))
for template in re.findall(r'vQ\+`([^`]+)`', config):
    for kind in ['webp', 'ktx2']:
        glpaths.add(template.replace('${iQ}', kind))
glpaths = {p for p in glpaths if not p.endswith('/')}
glpaths.update(['/draco/draco_decoder.js', '/draco/draco_decoder.wasm',
                '/draco/draco_wasm_wrapper.js', '/basis/basis_transcoder.js',
                '/basis/basis_transcoder.wasm'])
parallel([('https://lando.itsoffbrand.io/gl'+p, PUBLIC/'gl'/p.lstrip('/'),
           'https://landonorris.com/', 'reference-renderer') for p in sorted(glpaths)])
rive_names = ['btn-ui', 'circuits', 'ln4', 'mob-landscape', 'phrases', 'reef', 'signature']
parallel([('https://assets.itsoffbrand.io/lando/rive/'+n+'.riv', PUBLIC/'rive'/(n+'.riv'),
           'https://landonorris.com/', 'reference-animation') for n in rive_names]
         + [('https://lando.itsoffbrand.io/rive/page-transition.riv', PUBLIC/'rive/page-transition.riv',
             'https://landonorris.com/', 'reference-animation')])

# Official Formula 1 transparent driver cutout, kept unmodified.
portrait_url = 'https://media.formula1.com/image/upload/c_fill,w_1400/q_auto/v1740000001/common/f1/2026/redbullracing/maxver01/2026redbullracingmaxver01right.webp'
fetch(portrait_url, PUBLIC/'max/portrait.webp', 'https://www.formula1.com/en/drivers/max-verstappen', 'max-portrait')
fetch('https://www.verstappen.com/_shoppingcart/img/landingpage/mv.svg', PUBLIC/'max/mv.svg', 'https://www.verstappen.com/', 'max-logo')

official = BeautifulSoup(Path('/private/tmp/mv33-official.html').read_text(), 'html.parser')
articles = list(dict.fromkeys(a['href'] for a in official.select('a[href]') if 'news.verstappen.com/en/article/' in a['href']))
parallel([(url, REF/('news-'+url.rstrip('/').split('/')[-1]+'.html'), url, 'source-page') for url in articles[:10]])
photos = []
for url in articles[:10]:
    page = REF/('news-'+url.rstrip('/').split('/')[-1]+'.html')
    if not page.exists(): continue
    doc = BeautifulSoup(page.read_text(), 'html.parser')
    for img in doc.select('img[src]'):
        src = urllib.parse.urljoin(url, img['src'])
        if '/img/2026/' in src and src not in [r[0] for r in photos]:
            photos.append((src, url, img.get('alt', 'Max Verstappen')))
parallel([(src, PUBLIC/'max'/f'photo-{i:02d}{Path(urllib.parse.urlparse(src).path).suffix}', url, 'max-photo')
          for i, (src, url, alt) in enumerate(photos[:40])])

# Product photography is available publicly without a store account.
category = 'https://www.redbullshop.com/en-int/c/rbr-special-editions/'
fetch(category, REF/'helmet-category.html', category, 'source-page')
cat = BeautifulSoup((REF/'helmet-category.html').read_text(), 'html.parser') if (REF/'helmet-category.html').exists() else None
product_urls = ['https://www.redbullshop.com/en-int/p/RBR24310/',
                'https://www.redbullshop.com/en-int/p/1%3A2-Max-Verstappen-Brazil-GP-2025-Mini-Helmet/M-RBR25256/']
if cat:
    product_urls += [urllib.parse.urljoin(category, a['href']) for a in cat.select('a[href]')
                     if '/p/' in a['href'] and ('helmet' in a['href'].lower())]
product_urls = list(dict.fromkeys(product_urls))[:12]
parallel([(url, REF/f'helmet-product-{i:02d}.html', url, 'source-page') for i, url in enumerate(product_urls)])
helmets = []
for i, url in enumerate(product_urls):
    path = REF/f'helmet-product-{i:02d}.html'
    if not path.exists(): continue
    doc = BeautifulSoup(path.read_text(), 'html.parser')
    title = doc.find('h1').get_text(' ', strip=True) if doc.find('h1') else f'Helmet {i}'
    images = list(dict.fromkeys(img['src'] for img in doc.select('img[src]')
                               if 'assets.redbullshop.com/' in img['src'] and 'Helmet' in img.get('alt', '')))
    if not images: continue
    paths = []
    for j, image in enumerate(images[:6]):
        # Preserve the exact image URL supplied by the product page.
        out = PUBLIC/'max'/f'helmet-{i:02d}-{j:02d}.jpg'
        result = fetch(image, out, url, 'max-helmet')
        if result['status'] == 'downloaded': paths.append('/'+str(out.relative_to(PUBLIC)))
    helmets.append(dict(title=title, source=url, images=paths))

# Keep separately curated archive candidates when the main acquisition reruns.
helmets.extend(h for h in previous_assets.get('helmets', [])
               if len(h['images']) == 1 and 'helmetarchive.com' in h['source'])

# Official landing-page banner images for the store/editorial sections.
banners = []
for image in official.select('img[src]'):
    src = urllib.parse.urljoin('https://www.verstappen.com/', image['src'])
    if '/img/banner/' in src and src not in [x['url'] for x in banners]:
        i = len(banners)
        result = fetch(src, PUBLIC/'max'/f'banner-{i:02d}.jpg', 'https://www.verstappen.com/', 'max-banner')
        if result['status'] == 'downloaded': banners.append(dict(url=src, path=f'/max/banner-{i:02d}.jpg', alt=image.get('alt', '')))

inventory = dict(portrait='/max/portrait.webp', logo='/max/mv.svg',
                 photos=[dict(path='/max/'+f'photo-{i:02d}{Path(urllib.parse.urlparse(src).path).suffix}', source=url, alt=alt)
                         for i, (src, url, alt) in enumerate(photos[:40])
                         if (PUBLIC/'max'/f'photo-{i:02d}{Path(urllib.parse.urlparse(src).path).suffix}').exists()],
                 helmets=helmets, banners=banners)
(ROOT/'max-assets.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2))
MANIFEST.write_text(json.dumps(records, ensure_ascii=False, indent=2))
print(json.dumps(dict(downloaded=sum(r['status']=='downloaded' for r in records),
                     failed=[r for r in records if r['status']=='failed'],
                     photos=len(inventory['photos']), helmets=len(helmets), banners=len(banners)), ensure_ascii=False, indent=2))
