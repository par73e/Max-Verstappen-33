"""Check the complete static route graph, not just the homepage build."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]/'public'
errors=[];pages=list(ROOT.rglob('*.html'))
for path in pages:
 soup=BeautifulSoup(path.read_text(),'html.parser')
 for el,attr in [(a,'href') for a in soup.select('a[href]')]+[(a,'src') for a in soup.select('img[src],script[src]')]+[(a,'href') for a in soup.select('link[rel=stylesheet]')]:
  url=urlsplit(el[attr])
  if url.scheme or url.netloc or not url.path.startswith('/'):continue
  target=ROOT/unquote(url.path.lstrip('/'))
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{path.relative_to(ROOT)}: missing {el[attr]}')
for route in ['on-track','off-track','calendar','partnerships','helmets','helmets/season-2023','helmets/zandvoort-2024','helmets/season-2024','helmets/usa-2024','legal/privacy-policy','legal/terms-conditions']:
 path=ROOT/route/'index.html'
 if not path.exists():errors.append(f'Missing route {route}');continue
 s=BeautifulSoup(path.read_text(),'html.parser')
 if not s.select_one('[data-taxi-view][data-page]'):errors.append(f'{route}: missing source controller hook')
 if not s.select_one('[data-nav-ham]'):errors.append(f'{route}: missing shared menu')
 if s.select_one('a[data-mv-panel][href="/on-track"],a[data-mv-panel][href="/calendar"]'):errors.append(f'{route}: navigation still intercepted by a content panel')
if errors:raise SystemExit('\n'.join(errors))
print(f'Validated {len(pages)} HTML pages: internal destinations, scripts, images and shared route hooks.')
