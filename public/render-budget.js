/* Bound WebGL work independently of the display's 60/120Hz refresh rate. */
(() => {
 const budget=window.mv33RenderBudget={activeFPS:60,idleFPS:30,frames:0,deltaMs:16.67,lastFrame:0,lastInput:performance.now()};
 const wake=()=>{budget.lastInput=performance.now();};
 for(const event of ['pointermove','pointerdown','touchmove','wheel','keydown','scroll'])window.addEventListener(event,wake,{passive:true});
 document.addEventListener('visibilitychange',()=>{budget.lastFrame=0;wake();});
 budget.beginFrame=()=>{
  if(document.hidden)return false;
  const now=performance.now(),phase=document.querySelector('.transition-w')?.dataset.phase;
  // The visible wireframe scan is continuous motion even without input.
  const scanVisible=!!(window.mv33HeadScene?.isRendering && window.mv33HeadScene.helmet?.wireframeMesh?.visible);
  const active=scanVisible||now-budget.lastInput<1800||!window.loadingComplete||(phase&&phase!=='complete');
  const interval=1000/(active?budget.activeFPS:budget.idleFPS),elapsed=now-budget.lastFrame;
  if(budget.lastFrame&&elapsed+.5<interval)return false;
  budget.deltaMs=budget.lastFrame?elapsed:interval;
  budget.lastFrame=now;budget.frames++;
  return true;
 };
})();
