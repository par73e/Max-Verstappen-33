/* Source-compatible loader lifecycle: mount -> cover/reveal. MV replaces Rive's LN art. */
(() => {
 let root, mask, logo, frame=0, phase='idle', startedAt=0;
 const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
 const art='<path d="M561.703 156.65L673.914 268.775H449.493Z"/><path d="M112.21 156.65L224.747 268.775H0Z"/><path d="M336.957 335.725L0 0L213.33 33.475L336.957 156.65L460.584 33.475L673.914 0Z"/>';
 const transform=(scale,cx,cy)=>`translate(${cx} ${cy}) scale(${scale}) translate(-337 -${169+(245-169)*Math.min(1,Math.max(0,(scale-.3)/2))})`;
 function render(progress){
  const w=innerWidth,h=innerHeight,initial=Math.min(w*.3,210)/674;
  const eased=progress*progress*progress;
  const scale=initial*Math.exp(Math.log(Math.max(w,h)*.07/initial)*eased);
  root.querySelector('svg').setAttribute('viewBox',`0 0 ${w} ${h}`);
  mask.setAttribute('transform',transform(scale,w/2,h/2));logo.setAttribute('transform',transform(scale,w/2,h/2));
  logo.style.opacity=String(1-Math.min(1,progress*5));
  root.dataset.progress=progress.toFixed(3);
 }
 function mount(){
  root=document.querySelector('.transition-w');if(!root)return;
  root.innerHTML=`<svg class="mv-intro" xmlns="http://www.w3.org/2000/svg" aria-label="MV"><defs><mask id="mv-intro-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="100%" height="100%"><rect x="0" y="0" width="100%" height="100%" fill="white"/><g class="mv-intro-hole" fill="black">${art}</g></mask></defs><rect width="100%" height="100%" fill="#101823" mask="url(#mv-intro-mask)"/><g class="mv-intro-mark" fill="#ef6b19">${art}</g></svg>`;
  mask=root.querySelector('.mv-intro-hole');logo=root.querySelector('.mv-intro-mark');
  root.style.cssText='visibility:visible;pointer-events:auto;background:transparent';phase='loading';root.dataset.phase=phase;render(0);startedAt=performance.now();
 }
 function reveal(){
  if(!root||phase==='revealing'||phase==='complete')return;
  phase='revealing';root.dataset.phase=phase;window.dispatchEvent(new Event('mv33:intro-reveal'));
  const duration=reduced()?180:850,start=performance.now();cancelAnimationFrame(frame);
  const tick=now=>{const t=Math.min(1,(now-start)/duration);render(t);if(t<1)frame=requestAnimationFrame(tick);else{phase='complete';root.dataset.phase=phase;root.style.visibility='hidden';root.style.pointerEvents='none';window.dispatchEvent(new Event('mv33:intro-complete'));}};
  frame=requestAnimationFrame(tick);
 }
 function cover(){if(!root)mount();cancelAnimationFrame(frame);phase='loading';root.dataset.phase=phase;root.style.visibility='visible';root.style.pointerEvents='auto';render(0);}
 window.addEventListener('resize',()=>{if(root&&phase==='loading')render(0);});
 window.mv33Transition={mount,reveal,cover,get phase(){return phase;},get elapsed(){return performance.now()-startedAt;}};
})();
