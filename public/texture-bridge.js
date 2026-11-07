/* Runtime texture adaptation: original source photographs stay unmodified. */
(() => {
  window.mv33Errors=[];
  window.addEventListener('error',e=>window.mv33Errors.push(e.message||e.target?.src),true);
  window.addEventListener('unhandledrejection',e=>window.mv33Errors.push(String(e.reason)));
  const cache = new Map();
  const image = (src) => new Promise((resolve, reject) => {
    const img = new Image(); img.onload = () => resolve(img); img.onerror = reject; img.src = src;
  });
  const canvas = (w = 2048, h = w) => {
    const c = document.createElement('canvas'); c.width = w; c.height = h; return c;
  };
  const portraits = (async () => {
    const img = await image('/max/portrait.webp');
    const color = canvas(); const ctx = color.getContext('2d', {willReadFrequently:true});
    // Eye line and head width aligned to the original square head plane.
    const scale = 1.72; ctx.drawImage(img, -75, 345, img.width * scale, img.height * scale);
    const pixels = ctx.getImageData(0, 0, 2048, 2048);
    const alpha = canvas();const depth = canvas(); const normal = canvas();const rough = canvas();
    const a = alpha.getContext('2d').createImageData(2048,2048);
    const d = depth.getContext('2d').createImageData(2048,2048);
    for (let i=0;i<pixels.data.length;i+=4) {
      const v=pixels.data[i+3];a.data[i]=a.data[i+1]=a.data[i+2]=v;a.data[i+3]=255;
      const x=(i/4)%2048,y=Math.floor(i/4/2048);
      const bulge=Math.exp(-(((x-1024)/520)**2+((y-1050)/660)**2));
      d.data[i]=d.data[i+1]=d.data[i+2]=Math.round((80+bulge*100)*v/255);d.data[i+3]=255;
    }
    alpha.getContext('2d').putImageData(a,0,0);depth.getContext('2d').putImageData(d,0,0);
    const n=normal.getContext('2d');n.fillStyle='rgb(128,128,255)';n.fillRect(0,0,2048,2048);
    const r=rough.getContext('2d');r.fillStyle='#999';r.fillRect(0,0,2048,2048);
    return {diffuse:color.toDataURL(),alpha:alpha.toDataURL(),depth:depth.toDataURL(),
      normal:normal.toDataURL(),roughness:rough.toDataURL(),shadow:color.toDataURL(),
      'shadow-softer-edit':color.toDataURL(),'shadow-to-zip-edit':color.toDataURL()};
  })();
  const helmet = (async () => {
    const img=await image('/max/helmet-00-04.jpg');const c=canvas(1024);
    const ctx=c.getContext('2d');ctx.fillStyle='#f4f4ed';ctx.fillRect(0,0,1024,1024);
    ctx.drawImage(img,80,205,745,750,0,0,1024,1024);
    return c.toDataURL();
  })();
  window.mv33TextureURL = async (url) => {
    if(cache.has(url))return cache.get(url);
    if(url.includes('/textures/head/')){
      const key=url.split('/').pop().split('.')[0];const textures=await portraits;
      return textures[key] || url;
    }
    if(/Norris_Helmet_mat_BaseColor/.test(url))return await helmet;
    return url;
  };
  window.mv33TexturesReady=portraits;
})();
