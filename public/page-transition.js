/* Native document navigation uses the same MV cover as in-page routes. */
(() => {
 document.addEventListener('click', async event => {
  const link=event.target.closest('a[href]');
  if(!link || event.defaultPrevented || event.button!==0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.hasAttribute('download') || (link.target && link.target!=='_self')) return;
  const url=new URL(link.href,location.href);
  if(url.origin!==location.origin || !(/^\/(on-track|off-track|calendar|partnerships|helmets(?:\/[^/]+)?|legal\/(privacy-policy|terms-conditions))\/?$/.test(url.pathname) || url.pathname==='/' || url.pathname==='/assets.html') || (url.pathname===location.pathname && url.search===location.search)) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  if(window.mv33Transition.phase!=='complete')return;
  await window.mv33Transition.cover();
  location.href=url.href;
 },true);
 window.addEventListener('pageshow',event=>{if(event.persisted && window.mv33Transition?.phase!=='complete')window.mv33Transition.reveal()});
})();
