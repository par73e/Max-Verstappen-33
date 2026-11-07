/* Homepage adaptation only. Reference engine remains responsible for motion. */
(() => {
  const assets=JSON.parse(document.getElementById('mv33-assets').textContent);
  const panel=document.createElement('section');panel.className='mv-panel';panel.hidden=true;
  panel.setAttribute('role','dialog');panel.setAttribute('aria-modal','true');panel.setAttribute('aria-labelledby','mv-panel-title');
  panel.innerHTML='<button class="mv-panel-close" aria-label="关闭 / Close"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2"/></svg></button><div class="mv-panel-content"></div>';
  document.body.append(panel);let lastFocus;
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid=(photos)=>'<div class="mv-panel-grid">'+photos.map(p=>`<figure><img src="${esc(p.path)}" alt="${esc(p.alt||'Max Verstappen')}" loading="lazy"><figcaption><a href="${esc(p.source||'https://www.verstappen.com/')}" target="_blank" rel="noopener noreferrer">来源 / Source</a></figcaption></figure>`).join('')+'</div>';
  function open(kind,index){
    lastFocus=document.activeElement;
    const content=panel.querySelector('.mv-panel-content');let html='';panel.classList.toggle('mv-panel--helmet',kind==='helmet');
    if(kind==='helmet'){
      const h=assets.helmets[index]||assets.helmets[0];html=`<h2 id="mv-panel-title">${esc(h.title.replace('1:2 Max Verstappen ','').replace('Mini Helmet',''))}</h2><p>头盔细节 · 多角度摄影 / Helmet details</p>`+grid(h.images.map(path=>({path,source:h.source,alt:h.title})));
    }else if(kind==='calendar'){
      html='<h2 id="mv-panel-title">RACE<br>CALENDAR</h2><p>赛事日历</p><p>首屏保留参考站的圣保罗赛事卡片构图。本站是前端还原练习，赛程以 F1 官方发布为准。</p><p><a href="https://www.formula1.com/en/racing/2026" target="_blank" rel="noopener noreferrer">查看 F1 官方赛历 / View official calendar ↗</a></p>';
    }else if(kind==='about'){
      html='<h2 id="mv-panel-title">MV33<br>THE STUDY.</h2><p>维斯塔潘主题的个人前端还原练习。<br>An unofficial Max Verstappen fan-made frontend study.</p><p>页面结构、样式和动画实现参考 <a href="https://landonorris.com/" target="_blank" rel="noopener noreferrer">Lando Norris — OFF+BRAND</a>。人物与赛事图片来自 F1、Verstappen 官方新闻和 Red Bull Shop。原始文件和来源记录保存在项目的素材台账中。</p><p>这是第一版：人像使用 F1 官方透明照片，头盔使用参考模型及 Max 商品摄影投影适配；尚不是 Max 专属三维头盔模型。头盔画廊展示三款真实头盔的不同视角。</p><p><a href="/assets.html" target="_blank">查看素材样张 / Asset contact sheet ↗</a></p>';
    }else{
      const on=kind==='on-track';html=`<h2 id="mv-panel-title">${on?'ON':'OFF'}<br>TRACK</h2><p>${on?'赛道之上 · 围场与竞速影像':'赛道之外 · 维斯塔潘的竞速世界'}</p>`+grid(assets.photos.filter((p,i)=>on?i%3!==1:i%3===1));
    }
    content.innerHTML=html;panel.hidden=false;panel.scrollTop=0;
    window.lenisStop?.();document.body.style.overflow='hidden';panel.querySelector('button').focus();
  }
  function close(){panel.hidden=true;document.body.style.overflow='';window.lenisStart?.();lastFocus?.focus();}
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
    const helmet=e.target.closest('[data-max-helmet]');
    if(helmet){e.preventDefault();e.stopImmediatePropagation();open('helmet',Number(helmet.dataset.maxHelmet));return;}
    const link=e.target.closest('a');if(!link)return;
    const href=link.getAttribute('href');
    if(['/on-track','/off-track','/calendar','/partnerships'].includes(href)||link.dataset.mvPanel){
      e.preventDefault();e.stopImmediatePropagation();
      const menuClose=document.querySelector('[data-nav-toggle][aria-expanded="true"],button[aria-label="Close menu"]');
      if(menuClose)menuClose.click();
      open(link.dataset.mvPanel||href.slice(1));
    }else if(href==='/'){
      e.preventDefault();e.stopImmediatePropagation();window.lenis?.scrollTo(0,{duration:1});
      const closeButton=document.querySelector('button[aria-label="Close menu"]');if(closeButton)closeButton.click();
    }
  },true);
  document.querySelectorAll('[data-max-helmet]').forEach(item=>item.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open('helmet',Number(item.dataset.maxHelmet));}}));
  const discover=document.querySelector('[data-hero-anim="msg"]');
  if(discover){discover.setAttribute('role','button');discover.setAttribute('tabindex','0');discover.setAttribute('aria-label','认识维斯塔潘 / Discover Max');discover.style.cursor='pointer';discover.addEventListener('click',()=>open('off-track'));discover.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open('off-track');}});}
  // Retain the original Rive state machines, replacing only Lando-specific art.
  document.querySelectorAll('canvas[data-rive-file="signature"]').forEach(c=>{
    c.style.opacity='0';const img=document.createElement('img');img.src='/max/signature.png';img.alt='Max Verstappen signature';img.className='mv-signature-overlay';c.parentElement.style.position='relative';c.parentElement.append(img);
  });
  const signaturePairs=[...document.querySelectorAll('canvas[data-rive-file="signature"]')].map(c=>[c,c.parentElement.querySelector('.mv-signature-overlay')]);
  function syncArtwork(){
    document.documentElement.dataset.mvNavTheme=document.querySelector('.nav')?.dataset.navTheme||'dark';
    document.documentElement.dataset.mvAtEnd=String(scrollY+innerHeight>=document.documentElement.scrollHeight-3&&document.querySelector('button[data-nav-ham]')?.getAttribute('aria-expanded')!=='true');
    for(const [c,img] of signaturePairs){const input=c.riveInputs?.find(i=>i.name==='scroll');const progress=input?Math.min(1,input.value/700):1;img.style.opacity=String(Math.min(1,progress*4));img.style.clipPath=`inset(0 ${(1-progress)*100}% 0 0)`;}
    requestAnimationFrame(syncArtwork);
  }
  requestAnimationFrame(syncArtwork);
  // Code-native photographic rendering: remove only edge-connected white
  // studio backdrops; retain white helmet shells and unmodified source files.
  const cutoutCache=new Map();
  function studioCutout(src){
    if(cutoutCache.has(src))return cutoutCache.get(src);
    const promise=new Promise(resolve=>{
      const image=new Image();image.onload=()=>{
        const scale=Math.min(1,900/image.width);const w=Math.round(image.width*scale),h=Math.round(image.height*scale);
        const c=document.createElement('canvas');c.width=w;c.height=h;const ctx=c.getContext('2d',{willReadFrequently:true});ctx.drawImage(image,0,0,w,h);
        const frame=ctx.getImageData(0,0,w,h),d=frame.data,seen=new Uint8Array(w*h),queue=new Int32Array(w*h);let head=0,tail=0;
        const add=(p)=>{if(p<0||p>=w*h||seen[p])return;seen[p]=1;const k=p*4;if(Math.min(d[k],d[k+1],d[k+2])<240||Math.max(d[k],d[k+1],d[k+2])-Math.min(d[k],d[k+1],d[k+2])>14)return;queue[tail++]=p;};
        for(let x=0;x<w;x++){add(x);add((h-1)*w+x);}for(let y=0;y<h;y++){add(y*w);add(y*w+w-1);}
        while(head<tail){const p=queue[head++];d[p*4+3]=0;if(p%w)add(p-1);if(p%w<w-1)add(p+1);add(p-w);add(p+w);}
        // Repair narrow light channels connected to the backdrop. Keep the
        // sourced silhouette and recover interior shell pixels row by row.
        const source=ctx.getImageData(0,0,w,h).data;
        for(let y=0;y<h;y++){
          let left=-1,right=-1;
          for(let x=0;x<w;x++){const k=(y*w+x)*4;if(d[k+3]){if(left<0)left=x;right=x;}}
          if(right-left<15)continue;
          for(let x=left+2;x<right-2;x++){const k=(y*w+x)*4;if(!d[k+3]){d[k]=source[k];d[k+1]=source[k+1];d[k+2]=source[k+2];d[k+3]=255;}}
        }
        ctx.putImageData(frame,0,0);resolve(c.toDataURL());
      };image.onerror=()=>resolve(src);image.src=src;
    });cutoutCache.set(src,promise);return promise;
  }
  document.querySelectorAll('.helmet-grid-item-img-helmet,.helmet-grid-item-reveal-img,.footer-bg-img').forEach(async image=>{
    if(image.getAttribute('src').startsWith('/max/helmet-'))image.src=await studioCutout(image.getAttribute('src'));
  });
  const hero=document.querySelector('.c.home-hero');if(hero){const caption=document.createElement('div');caption.className='mv-fan-label';caption.textContent='MAX VERSTAPPEN / 麦克斯·维斯塔潘';hero.append(caption);}
  // Collect observable failures for local QA without third-party telemetry.
  window.mv33Errors ??=[];
})();
