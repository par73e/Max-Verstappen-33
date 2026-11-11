/* Source lifecycle: initial/loading -> ready -> page-in reveal. Native MV SVG art. */
(() => {
 let root,mask,logo,shade,coverLayer,frame=0,timer=0,phase='idle',startedAt=0,cycles=0;
 const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
 const art='<path d="M561.703 156.65L673.914 268.775H449.493Z"/><path d="M112.21 156.65L224.747 268.775H0Z"/><path d="M336.957 335.725L0 0L213.33 33.475L336.957 156.65L460.584 33.475L673.914 0Z"/>';
 const animatedArt=art.replace('<path ','<path class="mv-loader-piece mv-loader-right" ').replace('<path d="M112','<path class="mv-loader-piece mv-loader-left" d="M112').replace('<path d="M336','<path class="mv-loader-piece mv-loader-core" d="M336');
 const transform=(scale,cx,cy)=>`translate(${cx} ${cy}) scale(${scale}) translate(-337 -${169+(245-169)*Math.min(1,Math.max(0,(scale-.3)/2))})`;
 function render(progress){
  const w=innerWidth,h=innerHeight,initial=Math.min(w*.3,210)/674;
  const eased=progress*progress*progress;
  const scale=initial*Math.exp(Math.log(Math.max(w,h)*.07/initial)*eased);
  root.querySelector('.mv-intro').setAttribute('viewBox',`0 0 ${w} ${h}`);
  mask.setAttribute('transform',transform(scale,w/2,h/2));
  mask.style.opacity=progress>0?'1':'0';
  shade.style.opacity=phase==='revealing'?'1':'0';
  logo.style.opacity=String(1-Math.min(1,progress*5));root.dataset.progress=progress.toFixed(3);
 }
 function mount(){
  if(root&&phase!=='complete')return;
  root=document.querySelector('.transition-w');if(!root)return;
  cancelAnimationFrame(frame);clearTimeout(timer);
  startedAt=performance.now();cycles=0;
  // Preserve the first-paint logo and its already-running animation.
  logo=root.querySelector('.mv-intro-poster');
  if(!logo)return;
  root.insertAdjacentHTML('afterbegin',`<svg class="mv-intro" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs><mask id="mv-intro-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="100%" height="100%"><rect x="0" y="0" width="100%" height="100%" fill="white"/><g class="mv-intro-hole" fill="black">${art}</g></mask></defs><rect class="mv-intro-shade" width="100%" height="100%" fill="#101823" mask="url(#mv-intro-mask)"/></svg>`);
  mask=root.querySelector('.mv-intro-hole');shade=root.querySelector('.mv-intro-shade');
  root.insertAdjacentHTML('beforeend',`<div class="mv-cover" aria-hidden="true" style="position:absolute;inset:0;overflow:hidden;pointer-events:none;display:none"><div class="mv-cover-bg" style="position:absolute;inset:0;background:#101823;opacity:0"></div><svg class="mv-cover-three" viewBox="0 0 100 140" style="position:absolute;left:50%;top:50%;width:min(22vw,160px);height:auto;overflow:visible;transform:translate(-50%,-50%);will-change:transform,opacity"><path d="M12 8H63Q91 8 91 31Q91 55 69 67Q92 73 89 101Q86 132 53 132H8L12 112H53Q67 112 68 99Q69 86 54 86H27L31 66H57Q70 66 72 49Q74 28 57 28H8Z" fill="none" stroke="#101823" stroke-width="14" stroke-linejoin="round"/></svg></div>`);
  coverLayer=root.querySelector('.mv-cover');
  const breath=logo.querySelector('.mv-loader-breath');
  const animation=breath.getAnimations().find(a=>a.animationName==='mv-loader-cycle');
  cycles=Math.min(2,Math.floor((animation?.currentTime||0)/1500));root.dataset.cycles=cycles;
  breath.addEventListener('animationiteration',event=>{if(event.target!==event.currentTarget)return;cycles=Math.max(cycles,1);root.dataset.cycles=cycles;});
  breath.addEventListener('animationend',event=>{if(event.target!==event.currentTarget)return;finishCycles();});
  watchCycles(animation);
  root.style.cssText='visibility:visible;pointer-events:auto;background:#101823';
  root.removeAttribute('aria-hidden');
  root.setAttribute('role','status');root.setAttribute('aria-label','正在加载维斯塔潘 / Loading Max Verstappen');
  phase='loading';root.dataset.phase=phase;render(0);
 }
 function finishCycles(){
  cycles=2;root.dataset.cycles=cycles;if(phase==='ready')runReveal();
 }
 function watchCycles(animation){
  if(!animation)return;
  animation.finished.then(()=>{if(animation.playState==='finished')finishCycles();}).catch(()=>{});
 }
 function runReveal(){
  phase='revealing';root.dataset.phase=phase;render(0);root.style.background='transparent';window.dispatchEvent(new Event('mv33:intro-reveal'));
  const duration=reduced()?180:550,start=performance.now();cancelAnimationFrame(frame);
  const tick=now=>{if(phase!=='revealing')return;const t=Math.min(1,(now-start)/duration);if(reduced())root.style.opacity=String(1-t);else render(t);if(t<1)frame=requestAnimationFrame(tick);else{phase='complete';root.dataset.phase=phase;root.style.visibility='hidden';root.style.pointerEvents='none';root.setAttribute('aria-hidden','true');root.getAnimations({subtree:true}).forEach(a=>a.pause());window.dispatchEvent(new Event('mv33:intro-complete'));}};
  frame=requestAnimationFrame(tick);
 }
 function reveal(){
  if(!root||['ready','revealing','complete'].includes(phase))return;
  phase='ready';root.dataset.phase=phase;
  // Wait for two complete visible cycles and for the page to be ready.
  const animation=logo.querySelector('.mv-loader-breath').getAnimations().find(a=>a.animationName==='mv-loader-cycle');
  if(animation?.playState==='finished')cycles=2;
  if(reduced()||cycles>=2)runReveal();
 }
 async function cover(){
  if(!root)mount();cancelAnimationFrame(frame);clearTimeout(timer);phase='covering';root.dataset.phase=phase;
  root.style.visibility='visible';root.style.opacity='1';root.style.background='transparent';root.style.pointerEvents='auto';root.removeAttribute('aria-hidden');
  cycles=0;root.dataset.cycles='0';render(0);logo.style.opacity='0';
  // Hold the logo at its original shape until the expanding cover has settled.
  const logoAnimations=logo.getAnimations({subtree:true});
  logoAnimations.forEach(a=>{a.cancel();a.pause();});
  coverLayer.style.display='block';
  const number=coverLayer.querySelector('.mv-cover-three'),background=coverLayer.querySelector('.mv-cover-bg');
  const duration=reduced()?1:430;
  const covering=number.animate([
   {transform:'translate(-50%,-50%) scale(.05)',opacity:1,offset:0},
   {transform:'translate(-50%,-50%) scale(.3)',opacity:1,offset:.23},
   {transform:'translate(-50%,-50%) scale(1)',opacity:1,offset:.42},
   {transform:'translate(-50%,-50%) scale(2.8)',opacity:1,offset:.65},
   {transform:'translate(-50%,-50%) scale(18)',opacity:1,offset:1}
  ],{duration,easing:'linear',fill:'both'});
  const fill=background.animate([{opacity:0,offset:0},{opacity:0,offset:.84},{opacity:1,offset:1}],{duration,fill:'both'});
  await Promise.all([covering.finished,fill.finished]);
  root.style.background='#101823';coverLayer.style.display='none';covering.cancel();fill.cancel();
  startedAt=performance.now();phase='loading';root.dataset.phase=phase;render(0);
  logoAnimations.forEach(a=>{a.cancel();a.play();});
  watchCycles(logoAnimations.find(a=>a.animationName==='mv-loader-cycle'));
 }
 window.addEventListener('resize',()=>{if(root&&['loading','ready'].includes(phase))render(0);});
 window.mv33Transition={mount,reveal,cover,get phase(){return phase;},get elapsed(){return performance.now()-startedAt;}};
})();
