/* Homepage adaptation only. Reference engine remains responsible for motion. */
(() => {
  const assets=JSON.parse(document.getElementById('mv33-assets').textContent);
  const biography=JSON.parse(document.getElementById('mv33-content').textContent);
  const panel=document.createElement('section');panel.className='mv-panel';panel.hidden=true;
  panel.setAttribute('role','dialog');panel.setAttribute('aria-modal','true');panel.setAttribute('aria-labelledby','mv-panel-title');
  panel.innerHTML='<button class="mv-panel-close" aria-label="关闭 / Close"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2"/></svg></button><div class="mv-panel-content"></div>';
  document.body.append(panel);let lastFocus;
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid=(photos)=>'<div class="mv-panel-grid">'+photos.map(p=>`<figure><img src="${esc(p.path)}" alt="${esc(p.alt||'Max Verstappen')}" loading="lazy"><figcaption><a href="${esc(p.source||'https://www.verstappen.com/')}" target="_blank" rel="noopener noreferrer">来源 / Source</a></figcaption></figure>`).join('')+'</div>';
  const sources=keys=>'<p class="mv-fact-sources">资料来源 / Sources: '+keys.map(key=>{const s=biography.sources[key];return `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.label)}</a>`}).join(' · ')+`<br>资料核对日期：${esc(biography.verifiedOn)}</p>`;
  const milestones=()=>'<ul class="mv-career-facts">'+biography.milestones.map(m=>`<li><strong>${esc(m.year)}</strong> — ${esc(m.en)}<span class="mv-zh">${esc(m.zh)}</span></li>`).join('')+'</ul>';
  async function transition(action){
    const loader=window.mv33Transition;
    if(!loader){action();return;}
    if(loader.phase!=='complete')return;
    await loader.cover();action();loader.reveal();
  }
  function open(kind,index){transition(()=>openNow(kind,index));}
  function openNow(kind,index){
    lastFocus=document.activeElement;
    const content=panel.querySelector('.mv-panel-content');let html='';panel.classList.toggle('mv-panel--helmet',kind==='helmet');
    if(kind==='helmet'){
      const h=assets.helmets[index]||assets.helmets[0];html=`<h2 id="mv-panel-title">${esc(h.title.replace('1:2 Max Verstappen ','').replace('Mini Helmet',''))}</h2><p>头盔细节 · 多角度摄影 / Helmet details</p>`+grid(h.images.map(path=>({path,source:h.source,alt:h.title})));
    }else if(kind==='calendar'){
      html='<h2 id="mv-panel-title">RACE<br>ARCHIVE</h2><p>赛事影像档案 · 圣保罗与墨西哥城，2026<br>Race photographs · São Paulo &amp; Mexico City, 2026</p><p>回看维斯塔潘的围场与赛道影像。完整赛程请查看 F1 官方赛历。<br>Explore Max’s race weekends. Visit Formula 1 for the full calendar.</p>'+sources(['calendar'])+grid(assets.photos.slice(0,6));
    }else if(kind==='about'){
      html='<h2 id="mv-panel-title">MV33<br>THE STUDY.</h2><p>维斯塔潘主题的个人前端还原练习。<br>An unofficial Max Verstappen fan-made frontend study.</p><p>页面结构、样式和动画实现参考 <a href="https://landonorris.com/" target="_blank" rel="noopener noreferrer">Lando Norris — OFF+BRAND</a>。人物与赛事图片来自 F1、Verstappen 官方新闻和 Red Bull Shop。原始文件和来源记录保存在项目的素材台账中。</p><p>封面使用工作室人像与参考站 OFF+BRAND 头盔几何，实体和线框共用几何。维斯塔潘涂装依据多角度摄影近似重建，并非官方头盔扫描。</p><p>独立头盔详情页使用 “<a href="https://skfb.ly/pEDBZ" target="_blank" rel="noopener">Helmet Redbull - Max Verstappen</a>” by Maubian / <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>。已调整比例、UV 与涂装。</p><p><a href="/assets.html" target="_blank">查看素材样张 / Asset contact sheet ↗</a></p>';
    }else if(kind==='on-track'||kind==='profile'){
      html=`<h2 id="mv-panel-title">${kind==='profile'?'MAX<br>VERSTAPPEN':'ON<br>TRACK'}</h2><p>Oracle Red Bull Racing · Netherlands<br>红牛车队 · 荷兰车手</p>`+milestones()+sources(['f1','redBull'])+grid(assets.photos.filter((p,i)=>i%3!==1));
    }else{
      html=`<h2 id="mv-panel-title">${kind==='worlds'?'RACING<br>WORLDS':'OFF<br>TRACK'}</h2><p>Beyond Formula 1 · GT &amp; sim racing<br>F1 之外 · GT 赛车与模拟赛车</p><p>${esc(biography.copy.worlds.en)}<span class="mv-zh">${esc(biography.copy.worlds.zh)}</span></p><p>In March 2026, Team Redline became Verstappen Sim Racing.<span class="mv-zh">2026 年 3 月，Team Redline 更名为 Verstappen Sim Racing。</span></p>`+sources(['sim'])+grid(assets.photos.filter((p,i)=>i%3===1));
    }
    content.innerHTML=html;panel.hidden=false;panel.scrollTop=0;
    window.lenisStop?.();document.body.style.overflow='hidden';panel.querySelector('button').focus();
  }
  function close(){transition(()=>{panel.hidden=true;document.body.style.overflow='';window.lenisStart?.();lastFocus?.focus();});}
  panel.querySelector('button').addEventListener('click',close);
  document.addEventListener('keydown',e=>{
    if(panel.hidden)return;if(e.key==='Escape')close();
    if(e.key==='Tab'){
      const els=[...panel.querySelectorAll('button,a[href]')];const first=els[0],last=els.at(-1);
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    }
  });
  document.addEventListener('click',e=>{
    const link=e.target.closest('a');if(!link)return;
    const href=link.getAttribute('href');
    if(link.dataset.mvPanel){
      e.preventDefault();e.stopImmediatePropagation();
      window.closeNavigation?.();open(link.dataset.mvPanel);
    }else if(href==='/' && document.querySelector('[data-page=home]')){
      e.preventDefault();e.stopImmediatePropagation();window.lenis?.scrollTo(0,{duration:1});
      const closeButton=document.querySelector('button[aria-label="Close menu"]');if(closeButton)closeButton.click();
    }
  },true);
  document.querySelectorAll('[data-max-helmet]').forEach(item=>item.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();item.click();}}));
  const discover=document.querySelector('[data-hero-anim="msg"]');
  if(discover){discover.setAttribute('role','button');discover.setAttribute('tabindex','0');discover.setAttribute('aria-label','认识维斯塔潘 / Discover Max');discover.style.cursor='pointer';discover.addEventListener('click',()=>open('profile'));discover.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open('profile');}});}
  // Retain the original Rive state machines, replacing only Lando-specific art.
  document.querySelectorAll('canvas[data-rive-file="signature"]').forEach(c=>{
    c.style.opacity='0';const img=document.createElement('img');img.src='/max/signature-orange.svg';img.alt='Max Verstappen signature';img.className='mv-signature-overlay';c.parentElement.style.position='relative';c.parentElement.append(img);
  });
  const signaturePairs=[...document.querySelectorAll('canvas[data-rive-file="signature"]')].map(c=>[c,c.parentElement.querySelector('.mv-signature-overlay')]);
  const logoPairs=[...document.querySelectorAll('canvas[data-rive-ln4]')].map(c=>[c,c.parentElement.querySelector('.mv-logo-overlay')]);
  function syncArtwork(){
    document.documentElement.dataset.mvNavTheme=document.querySelector('.nav')?.dataset.navTheme||'dark';
    document.documentElement.dataset.mvAtEnd=String(scrollY+innerHeight>=document.documentElement.scrollHeight-3&&document.querySelector('button[data-nav-ham]')?.getAttribute('aria-expanded')!=='true');
    // The source's top-marker / mobile scroll handler owns this input. Use the
    // same state for MV artwork so the CSS transition reverses mid-flight.
    for(const [c,logo] of logoPairs){
      if(!logo)continue;
      const active=c.riveInputs?.find(i=>i.name==='logo-active')?.value??scrollY<=10;
      const value=String(active);
      if(logo.dataset.active!==value)logo.dataset.active=value;
    }
    for(const [c,img] of signaturePairs){const input=c.riveInputs?.find(i=>i.name==='scroll');const scrollSignature=c.getAttribute('data-rive-state-machine')==='signature_scroll';const progress=scrollSignature?(input?Math.min(1,input.value/700):0):1;img.style.opacity=String(Math.min(1,progress*4));img.style.clipPath=`inset(0 ${(1-progress)*100}% 0 0)`;}
    requestAnimationFrame(syncArtwork);
  }
  requestAnimationFrame(syncArtwork);
  // The archive controller owns reveal intent, decoding and reversal. Static
  // alpha assets avoid canvas flood-fill work and data-URL uploads on this page.
  const archiveItems=[...document.querySelectorAll('[data-mv-worn]')];
  const motion=matchMedia('(prefers-reduced-motion: reduce)');
  window.mvHelmetArchive={items:archiveItems};
  archiveItems.forEach(item=>{
    const image=item.querySelector('.helmet-grid-item-reveal-img');
    const windowEl=item.querySelector('.mv-helmet-reveal-window');
    const photo=item.querySelector('.mv-helmet-reveal-photo');
    if(!image||!windowEl||!photo)return;
    let hovered=false,ready=false,preparing,player,photoPlayer;
    const duration=650;
    item.dataset.revealState='closed';item.dataset.revealReady='false';
    const intended=()=>hovered||item.matches(':focus-visible');
    function update(){
      if(!ready)return;
      const open=intended(),time=Math.max(0,Math.min(duration,player.currentTime||0));
      item.dataset.revealActive=String(open);
      if(motion.matches||(open&&time>=duration)||(!open&&time<=0)){
        for(const animation of [player,photoPlayer]){animation.pause();animation.currentTime=open?duration:0;}
        item.dataset.revealState=open?'open':'closed';return;
      }
      photoPlayer.currentTime=time;
      for(const animation of [player,photoPlayer]){animation.updatePlaybackRate(open?1:-1);animation.play();}
      item.dataset.revealState=open?'opening':'closing';
    }
    function prepare(){
      if(preparing)return preparing;
      preparing=(async()=>{
        try{
          await image.decode();
          const options={duration,easing:'cubic-bezier(.65,0,.25,1)',fill:'both'};
          player=windowEl.animate([{transform:'translate3d(0,-100%,0)'},{transform:'translate3d(0,0,0)'}],options);
          photoPlayer=photo.animate([{transform:'translate3d(0,100%,0)'},{transform:'translate3d(0,0,0)'}],options);
          for(const animation of [player,photoPlayer]){animation.pause();animation.currentTime=0;}
          player.onfinish=()=>{item.dataset.revealState=player.currentTime>=duration-1?'open':'closed';};
          ready=true;item.dataset.revealReady='true';update();
        }catch(error){item.dataset.revealState='unavailable';}
      })();return preparing;
    }
    item.addEventListener('pointerenter',event=>{if(event.pointerType==='touch')return;hovered=true;prepare();update();});
    item.addEventListener('pointerleave',()=>{hovered=false;update();});
    item.addEventListener('focus',()=>{prepare();update();});
    item.addEventListener('blur',update);
    motion.addEventListener('change',update);
    prepare();
  });
  const hero=document.querySelector('.c.home-hero');if(hero){const caption=document.createElement('div');caption.className='mv-fan-label';caption.textContent='MAX VERSTAPPEN / 麦克斯·维斯塔潘';hero.append(caption);}
  // Collect observable failures for local QA without third-party telemetry.
  window.mv33Errors ??=[];
})();
