"""Adapt retained page DOMs; keep source hooks for the original page controllers."""
import copy, hashlib, json, re, urllib.parse, urllib.request
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup, NavigableString, Comment
from theme import theme_colors
ROOT=Path(__file__).resolve().parents[1];PUBLIC=ROOT/'public'
assets=json.loads((ROOT/'max-assets.json').read_text());bio=json.loads((ROOT/'content/max.json').read_text())
home=BeautifulSoup((PUBLIC/'index.html').read_text(),'html.parser')
photos=assets['photos'];sources=json.loads((ROOT/'reference/pages/resources.json').read_text()) if (ROOT/'reference/pages/resources.json').exists() else {}

def clean_markup(markup):return '\n'.join(line.expandtabs(2).rstrip() for line in markup.splitlines())+'\n'
def fragment(markup):return BeautifulSoup(markup,'html.parser')
def sethtml(el,markup):
 if el:el.clear();el.append(fragment(markup))
def text(el,value):
 if el:el.clear();el.append(str(value))
def ordinal(n):return str(n)+('th' if 10<int(n)%100<14 else {1:'st',2:'nd',3:'rd'}.get(int(n)%10,'th'))
def results(year):
 path=ROOT/f'content/results-{year}.json'
 return json.loads(path.read_text())['MRData']['RaceTable']['Races'] if path.exists() else []
def local(url):
 if 'plugins/Basic/assets/placeholder' in url:return '/max/mv-orange.svg'
 if not url.startswith(('https://cdn.prod.website-files.com/','https://d3e54v103j8qbb.cloudfront.net/')):return url
 name=urllib.parse.unquote(urllib.parse.urlparse(url).path.rsplit('/',1)[-1]);p=PUBLIC/'reference'/name
 if not p.exists():
  try:p.write_bytes(urllib.request.urlopen(url,timeout=20).read());sources[str(p.relative_to(ROOT))]=url
  except Exception as e:print('Missing reference resource',url,e);return url
 if name.endswith('.svg'):
  themed=PUBLIC/'theme-vectors'/name;themed.parent.mkdir(exist_ok=True);themed.write_text(theme_colors(p.read_text()));return '/theme-vectors/'+urllib.parse.quote(name)
 return '/reference/'+urllib.parse.quote(name)

def adapt_view(view):
 # Footer, archive and social controls are shared, not independently approximated.
 for selector in ['.is-footer','.home-helmets','.is-callout-socials']:
  old=view.select_one(selector);shared=home.select_one(selector)
  if old and shared:old.replace_with(copy.deepcopy(shared))
 shared={img.get('src') for img in view.select('img[src^="/max/"]')}
 # Each narrative slot gets its own photograph; avoid the known alternate
 # exports of the same shot and images already present in shared sections.
 pool=iter(p for i,p in enumerate(photos) if i not in [3,9,16,25] and p['path'] not in shared)
 for i,img in enumerate(view.select('img')):
  src=img.get('src','');classes=' '.join(img.get('class',[]))
  if '/max/' in src:continue
  if 'w-dyn-bind-empty' in classes:
   img['src']='/max/mv-orange.svg';img['alt']='';img.attrs.pop('srcset',None);continue
  if 'signature' in src.lower():img['src']='/max/signature-orange.svg';img['alt']='Max Verstappen signature'
  elif 'flag-UK' in src and 'hero' in str(img.parent.get('class')):img['src']='/max/netherlands.svg';img['alt']='Netherlands'
  elif any(k in src.lower() for k in ['logo-','ln4-ln4-collab']):img['src']=f'/max/world-{i%4}.svg';img['alt']='Verstappen Racing'
  elif 'blobs_footer' in src:img['src']='/max/mv-watermark.svg'
  elif any(k in classes for k in ['off-t-hero-scroll','is-horizontal-scroll','is-visor-scroll','is-clip-fix','f1-highlight-img','is-otot-home-end','is-highlight-mouse']):
   img['src']=next(pool)['path'];img['alt']='Max Verstappen · Racing archive'
  else:img['src']=local(src)
  img.attrs.pop('srcset',None);img.attrs.pop('sizes',None)
 for el in view.find_all():
  for attr in ['href','src','poster']:
   if el.has_attr(attr):el[attr]=local(el[attr])
  el.attrs.pop('data-stream-url',None)
 for node in list(view.find_all(string=True)):
  if isinstance(node,Comment) or node.parent.name in ['script','style']:continue
  value=str(node)
  for old,new in [('LANDO NORRIS','MAX VERSTAPPEN'),('Lando Norris','Max Verstappen'),('Lando’s','Max’s'),('Lando','Max'),('lando','max'),('last lap max','MAX VERSTAPPEN'),('mclaren','red bull'),('McLaren','Red Bull'),('MCLAREN','RED BULL'),('since 2019','since 2016'),('26 y.o','29 y.o'),('Bristol, UK','Hasselt, Belgium')]:value=value.replace(old,new)
  if value!=str(node):node.replace_with(NavigableString(value))
 for a in list(view.select('a[href]')):
  href=a['href']
  if any(x in href for x in ['landonorris.store','store.landonorris']):
   # Keep the source button geometry and use the existing non-commerce archive.
   a['href']='/helmets/';
   for n in list(a.find_all(string=True)):
    if n.strip():n.replace_with('VIEW HELMETS')
  elif 'instagram.com' in href:a['href']='https://www.instagram.com/maxverstappen1/'
  elif 'youtube.com' in href:a['href']='https://www.youtube.com/@MaxVerstappen1'
  elif 'tiktok.com' in href:a['href']='https://www.facebook.com/MaxVerstappen';text(a,'Facebook')
  elif 'twitch.tv' in href:a['href']='https://twitter.com/Max33Verstappen';text(a,'X / Twitter')
  elif href.startswith('mailto:') or a.has_attr('data-signup-trigger'):a['href']='#about';a['data-mv-panel']='about'
 for el in view.select('.on-t-hero-stats-ui-box2-col-2-svg'):sethtml(el,'<img src="/max/mv-orange.svg" alt="MV" style="width:100%;height:100%;object-fit:contain">')
 for el in view.select('.impact-text-w .text-impact-lg-mona'):sethtml(el,bio['copy']['statement'])
 for el in view.select('.text-eyebrow'):
  if 'red bull f1' in el.get_text().lower():text(el,'RED BULL RACING · SINCE 2016')
 for el in view.select('[data-cal-list="first-competed-date"]'):text(el,'—')
 for el in view.select('.calendar-rich-text'):text(el,'Explore this circuit and its place on the Formula 1 calendar.')
 for el in view.select('.horizontal-item-text'):
  if any(term in el.get_text() for term in ['Lego','Sawaya','replica','photography','green']):text(el,'Precision. Competition. A shared passion for racing, on the track and beyond.')
 for el in view.select('.horizontal-item-layout .text-eyebrow'):
  if re.search(r'20\d\d',el.get_text()):text(el,'MAX VERSTAPPEN · RACE ARCHIVE')
 return view

def render(route,view,source=None):
 page=copy.deepcopy(home);page.select_one('[data-taxi-view]').replace_with(view)
 if source:
  page.html['data-wf-page']=source.html.get('data-wf-page','')
 page.title.string={'on-track':'On Track','off-track':'Off Track','calendar':'Calendar','partnerships':'Racing Worlds','helmets':'Helmet Archive','legal/privacy-policy':'Privacy','legal/terms-conditions':'About & Credits'}.get(route,'Helmet Edition')+' — Max Verstappen · MV33'
 for a in page.select('a[href]'):
  a.attrs.pop('data-mv-panel',None) if a.get('href') in ['/on-track','/off-track','/calendar','/partnerships'] else None
  if a.get('href')=='#about' and a.get_text(strip=True) in ['Privacy Policy','Terms']:a['href']='/legal/privacy-policy' if 'Privacy' in a.get_text() else '/legal/terms-conditions';a.attrs.pop('data-mv-panel',None)
  if a.get('href')=='/off-track' and 'Racing Worlds' in a.get_text():a['href']='/partnerships'
  if 'w--current' in a.get('class',[]):a['class'].remove('w--current')
  if a.get('href')=='/'+route:a['class']=a.get('class',[])+['w--current'];a['aria-current']='page'
  else:a.attrs.pop('aria-current',None)
 css=page.new_tag('link',rel='stylesheet',href='/pages.css?v='+hashlib.sha256((PUBLIC/'pages.css').read_bytes()).hexdigest()[:10]);page.head.append(css)
 page.body['data-mv-subpage']=route
 path=PUBLIC/route/'index.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(clean_markup(theme_colors(str(page))))

for route in ['on-track','off-track','calendar']:
 source=BeautifulSoup((ROOT/'reference/pages'/f'{route}.html').read_text(),'html.parser');view=adapt_view(copy.deepcopy(source.select_one('[data-taxi-view]')))
 if route=='on-track':
  sethtml(view.select_one('.on-t-hero-stats-para-w h2'),'From a Formula 1 debut in 2015 to four consecutive world titles. Max Verstappen keeps <span class="text-body-lg-brier c-lime">chasing the limit</span>.')
  # Historic statistics have an explicit cutoff, independent of the live calendar.
  rs=[r for y in range(2015,2025) for r in results(y)];podiums=sum(int(r['Results'][0]['position'])<=3 for r in rs)
  wrap=view.select_one('[data-podium="wrap"]');first=wrap.select_one('.w-dyn-item') if wrap else None
  if first:
   # Source's gigantic counter is ordinary text inside the CMS item.
   for n in first.find_all(string=re.compile(r'^\d+$')):n.replace_with(str(podiums))
  if len(view.select('.f1-car-stats-item'))>1:text(view.select('.f1-car-stats-item')[1].select_one('h3'),'STARTS FROM P1')
  values=[sum(r['Results'][0]['position']=='1' for r in rs),sum(r['Results'][0].get('grid')=='1' for r in rs),4,0,sum(r['Results'][0].get('FastestLap',{}).get('rank')=='1' for r in rs)]
  # Replace the average slot with championship titles; the numeric layout remains.
  stats=view.select('.f1-car-stats-item')
  if len(stats)>2:text(stats[2].select('h3')[0],'world titles');
  for el,value in zip(view.select('[data-car-counter="digit"]'),values):text(el,value)
  if len(stats)>2:
   for el in stats[2].select('.f1-car-stat-label-w'):el.decompose()
  sethtml(view.select_one('.on-t-career'),'F1 CAREER<br><span class="text-title-lg-brier c-grey-on-track">2015–2024</span>')
  for el in view.select('.on-t-hero-stats-ui-sec1-row.is-2 [data-text-format="position"]'):text(el,ordinal(results(2026)[-1]['Results'][0]['position']))
  years=view.select_one('.f1-car-stat-past-v2-grid-w');template=copy.deepcopy(years.select_one('[data-stat-item]'));years.clear()
  standings={2024:1,2023:1,2022:1,2021:1,2020:3,2019:3,2018:4,2017:6,2016:5,2015:12}
  for year in range(2024,2014,-1):
   row=copy.deepcopy(template);cells=row.select('.f1-car-stat-past-v2-grid-inner');text(cells[0],year);text(cells[1],ordinal(standings[year]));text(cells[2],sum(int(r['Results'][0]['position'])<=3 for r in results(year)));years.append(row)
  for el in view.select('.title-para-w p'):
   if 'seven seasons' in el.get_text():text(el,'A selection of Max’s race victories. Career totals and season results below cover 2015–2024.')
  for row,r in zip(view.select('.f1-highlight-grid.is-highlights'),[r for r in reversed(results(2024)) if r['Results'][0]['position']=='1']):
   cells=row.select('.f1-highlight-grid-item');
   if len(cells)>=5:
    text(cells[1].select_one('.text-on-t-stat-label-major'),r['Circuit']['Location']['country']);text(cells[2],date.fromisoformat(r['date']).strftime('%-d %b %y'));text(cells[3],'1st');text(cells[4],r['Results'][0].get('Time',{}).get('time','—'))
  for el in view.select('.horizontal-item-text'):text(el,'Four consecutive titles. One racing instinct.')
  for el in view.select('.horizontal-item-img-text'):text(el,'MAX VERSTAPPEN · RACE ARCHIVE')
  junior=[('FIA Formula 3 European Championship · 3rd','2014'),('Zandvoort Masters · Winner','2014'),('CIK-FIA World KZ Championship · Winner','2013'),('European KF & KZ Championships · Winner','2013')]
  for i,el in enumerate(view.select('.pre-f1-car-stats-item')):
   if i>=len(junior):el.decompose();continue
   text(el.select_one('.pre-f1-car-stats-text-w'),junior[i][0]);text(el.select_one('.text-eyebrow'),junior[i][1])
  for el in view.select('h2 span'):
   if el.get_text()=='2007-2019':text(el,'2005–2014')
 elif route=='off-track':
  sethtml(view.select_one('.on-t-hero-stats-para-w h2'),'Away from the Formula 1 paddock, the racing never stops. A world of <span class="text-body-lg-brier c-green-off-white-2">GT and sim racing</span>.')
  text(view.select_one('.off-t-hero-sub-para-mw p'),bio['copy']['worlds']['en'])
  titles=['SIM RACING','GT RACING','VERSTAPPEN RACING','THE ORANGE ARMY']
  descriptions=['Precision, teamwork and competition on the virtual circuit.','Taking the racing instinct beyond Formula 1.','One racing world, from the simulator to the circuit.','A shared passion for racing, at home and around the world.']
  for i,h in enumerate(view.select('h3.text-title-reg-brier')):
   text(h,titles[i%4]);container=h.parent
   caption=h.find_parent(class_='off-t-horiz-title-w')
   if caption:text(caption.select_one('.text-eyebrow'),descriptions[i%4])
 elif route=='calendar':
  # Bind the current Max snapshot to the reference's race and track hooks.
  current={r['round']:r for r in results(2026)}
  qualifying={r['round']:r['QualifyingResults'][0] for r in json.loads((ROOT/'content/qualifying-2026.json').read_text())['MRData']['RaceTable']['Races']}
  standing=json.loads((ROOT/'content/standings-2026.json').read_text())['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][0]
  header=view.select_one('.is-on-t-calendar')
  if header:
   nums=header.select('.text-on-t-stat-label-major.flex')
   if nums:
    text(nums[0],standing['position'])
    suffix=nums[0].find_parent(class_='f1-highlight-grid-item-text-layout')
    if suffix:
     for el in suffix.select('.text-on-t-stat-label-sm'):text(el,ordinal(standing['position'])[len(standing['position']):])
  for row in view.select('[data-cal-item]'):
   rnd=row.select_one('[data-text-format="round"]');race=current.get(rnd.get_text(strip=True) if rnd else '')
   res=race['Results'][0] if race else {}
   qual=qualifying.get(rnd.get_text(strip=True) if rnd else '',{})
   pos=row.select_one('[data-text-format="position"]');text(pos,ordinal(res['position']) if res else '—')
   for el in row.select('[data-cal-list]'):
    key=el['data-cal-list']
    if key=='first-competed-date':text(el,'—')
    if key.endswith(('-time-result','-time-pos')):text(el,'—')
    if key=='qual-time-pos' and qual:text(el,ordinal(qual['position']))
    if key=='qual-time-result' and qual:text(el,qual.get('Q3') or qual.get('Q2') or qual.get('Q1') or '—')
    if key=='race-time-pos' and res:text(el,ordinal(res['position']))
    if key=='race-time-result' and res:text(el,res.get('Time',{}).get('time',res.get('status','—')))
   for el in row.select('.f1-highlight-trophy-w'):el['class']=el.get('class',[])+['w-condition-invisible']
   cells=row.select('.f1-highlight-grid-item')
   if cells:text(cells[-1].select_one('.text-on-t-stat-label-reg'),res.get('FastestLap',{}).get('Time',{}).get('time','—'))
  for el in view.select('h2'):
   if 'schedule' in el.get_text():text(el,'Explore the Formula 1 calendar and Max’s archived season results.')
  for el in view.select('[data-cal-target="standing"]'):text(el,'—')
  # Rebuild historical accordions with real Max race records and source row hooks.
  items=view.select('[data-calendar-history="item"]');template=copy.deepcopy(items[0]);host=items[0].parent
  for item in items:item.decompose()
  for year in range(2025,2014,-1):
   item=copy.deepcopy(template);trigger=item.select_one('[data-calendar-history="trigger"]');text(trigger.select_one('h3'),year)
   text(trigger.select_one('[data-text-format="position"]'),ordinal({2025:2,2024:1,2023:1,2022:1,2021:1,2020:3,2019:3,2018:4,2017:6,2016:5,2015:12}[year]))
   nums=trigger.select('.text-on-t-stat-label-major.flex')
   if nums:text(nums[-1],sum(int(r['Results'][0]['position'])<=3 for r in results(year)))
   listing=item.select_one('.f1-highlight-list');rowtemplate=copy.deepcopy(listing.select_one('[data-stat-item-dd]'));listing.clear()
   for r in results(year):
    row=copy.deepcopy(rowtemplate);res=r['Results'][0];cells=row.select('.f1-highlight-grid-item');text(cells[0].select_one('[data-text-format="round"]'),r['round']);text(cells[1].select_one('h4'),r['Circuit']['Location']['country']);
    for flag in cells[1].select('.flag-w'):flag.decompose()
    text(cells[2],date.fromisoformat(r['date']).strftime('%-d %b %y'));text(cells[3].select_one('[data-text-format="position"]'),ordinal(res['position']));text(cells[4],res.get('FastestLap',{}).get('Time',{}).get('time','—'))
    for trophy in row.select('.f1-highlight-trophy-w'):trophy.decompose()
    listing.append(row)
   host.append(item)
 render(route,view,source)

# The source Partnerships URL currently serves its 404 page. Adapt its Off Track
# composition for the documented racing worlds rather than reproduce a dead end.
source=BeautifulSoup((ROOT/'reference/pages/off-track.html').read_text(),'html.parser');view=adapt_view(copy.deepcopy(source.select_one('[data-taxi-view]')))
sethtml(view.select_one('h1'),'<span class="text-on-t-hero-heading-mona margin">RACING</span>WORLDS')
sethtml(view.select_one('.on-t-hero-stats-para-w h2'),bio['copy']['worlds']['en']);text(view.select_one('.off-t-hero-sub-para-mw p'),bio['copy']['worlds']['zh'])
for h,value in zip(view.select('h3.text-title-reg-brier'),['RED BULL RACING','VERSTAPPEN RACING','SIM RACING','ORANGE ARMY']):text(h,value)
for p in view.select('.off-t-horiz-title-w .text-eyebrow'):text(p,'From the paddock to the virtual circuit. Explore Max Verstappen’s racing world.')
text(view.select_one('.off-t-hero-sub-para-mw p'),bio['copy']['worlds']['zh'])
render('partnerships',view,source)

# Archive is the same source helmet display, with real edition destinations.
view=fragment('<div data-taxi-view data-page="partnerships" class="taxi-w mv-archive-page" data-nav-theme-target="light"><section class="s"><div class="c"><a class="mv-archive-return" href="/" aria-label="返回主页 / Back to home">← HOME / 返回主页</a><h1 class="text-impact-lg-mona">Helmet<br><strong>Archive</strong></h1></div></section></div>').div
view.append(copy.deepcopy(home.select_one('.home-helmets')));view.append(copy.deepcopy(home.select_one('.is-footer')));render('helmets',view)

for route,title,body in [('legal/privacy-policy','Privacy','<p>This independent fan study has no account system, checkout or newsletter subscription. It serves local fonts and media. External links open services with their own privacy policies.</p><p>本网站为独立车迷练习，没有账户、结账或邮件订阅系统。外部网站适用其各自的隐私政策。</p>'),('legal/terms-conditions','About & Credits','<p>MV33 is an unofficial, non-commercial Max Verstappen frontend study. It is not affiliated with Max Verstappen, Red Bull Racing or Formula 1.</p><p>Interface structure and animation reference: Lando Norris / OFF+BRAND. Photography: the credited F1, Verstappen and Red Bull sources. Helmet edition model: Maubian, CC BY 4.0, with reconstructed UVs and livery.</p><p><a href="/assets.html">Explore the full asset library and source credits ↗</a></p>')]:
 source=BeautifulSoup((ROOT/'reference/pages/legal-terms-conditions.html').read_text(),'html.parser');view=copy.deepcopy(source.select_one('[data-taxi-view]'));section=view.select_one('section');section.clear();section.append(fragment(f'<div class="c"><div class="legal-rich-text w-richtext"><h1>{title}</h1>{body}</div></div>'));view.select_one('.is-footer').replace_with(copy.deepcopy(home.select_one('.is-footer')));render(route,view,source)
(ROOT/'reference/pages/resources.json').write_text(json.dumps(sources,indent=2))
# Detail pages share the source navigation, full-screen menu and ending scene.
for edition in ['season-2023','zandvoort-2024']:
 detail=BeautifulSoup((PUBLIC/'helmets'/edition/'index.html').read_text(),'html.parser')
 view=fragment('<div data-taxi-view data-page="partnerships" class="taxi-w mv-edition-page" data-nav-theme-target="dark"></div>').div
 for child in list(detail.main.children):view.append(copy.deepcopy(child))
 view.append(copy.deepcopy(home.select_one('.is-footer')))
 render('helmets/'+edition,view)
 dest=PUBLIC/'helmets'/edition/'index.html';page=BeautifulSoup(dest.read_text(),'html.parser')
 for link in detail.select('link[rel=stylesheet]'):page.head.append(copy.deepcopy(link))
 page.head.append(copy.deepcopy(detail.select_one('script[type=importmap]')))
 for script in detail.select('#helmet-edition,script[type=module]'):page.body.append(copy.deepcopy(script))
 page.title.string=detail.title.string
 dest.write_text(clean_markup(str(page)))
# These two source-backed editions have photography rather than invented 3D paint.
for edition,index,name in [('season-2024',0,'SEASON 2024'),('usa-2024',1,'USA 2024')]:
 h=assets['helmets'][index]
 gallery=''.join(f'<figure><img src="{photo}" alt="Max Verstappen {name} · view {i+1}" loading="lazy"></figure>' for i,photo in enumerate(h['images']))
 view=fragment(f'<div data-taxi-view data-page="partnerships" class="taxi-w mv-edition-page mv-photo-edition" data-nav-theme-target="dark"><section class="s"><div class="c"><h1 class="text-impact-lg-mona">{name}</h1><img class="mv-edition-cover" src="{h["images"][0]}" alt="Max Verstappen {name}"><a class="mv-archive-return" href="/helmets/">ALL HELMETS ↗</a></div></section><section class="mv-edition-photos">{gallery}</section></div>').div
 view.append(copy.deepcopy(home.select_one('.is-footer')));render('helmets/'+edition,view)
print('Built eleven internal routes with shared navigation')
