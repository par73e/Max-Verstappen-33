/* Source photograph RGB + registered opacity and inferred relative depth. */
(() => {
 window.mv33Errors=[];
 window.addEventListener('error',e=>window.mv33Errors.push(e.message||e.target?.src),true);
 window.addEventListener('unhandledrejection',e=>window.mv33Errors.push(String(e.reason)));
 const image=src=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=src;});
 const canvas=(w=2048,h=w)=>Object.assign(document.createElement('canvas'),{width:w,height:h});
 const portraits=(async()=>{
  const [photo,cutout,depthImage]=await Promise.all([image('/max/portrait-studio-source.jpg'),image('/max/portrait-studio-alpha.png'),image('/max/portrait-studio-depth.png')]);
  // Native photo is a chest-up studio portrait, registered by eye line and face axis.
  const x=-272,y=411,width=2592,height=width*photo.height/photo.width;
  const draw=(context,img,factor=1)=>{context.imageSmoothingEnabled=true;context.imageSmoothingQuality='high';context.drawImage(img,x*factor,y*factor,width*factor,height*factor);};
  const color=canvas(4096),ctx=color.getContext('2d');draw(ctx,photo,2);
  const mask=canvas(),mc=mask.getContext('2d',{willReadFrequently:true});draw(mc,cutout);
  const alpha=canvas(),ac=alpha.getContext('2d'),a=mc.getImageData(0,0,2048,2048);
  for(let i=0;i<a.data.length;i+=4){a.data[i]=a.data[i+1]=a.data[i+2]=a.data[i+3];a.data[i+3]=255;}ac.putImageData(a,0,0);
  const depth=canvas(),dc=depth.getContext('2d',{willReadFrequently:true});dc.fillStyle='rgb(80,80,80)';dc.fillRect(0,0,2048,2048);draw(dc,depthImage);
  const d=dc.getImageData(0,0,2048,2048).data;
  const normal=canvas(),nc=normal.getContext('2d'),n=nc.createImageData(2048,2048);
  // Derive tangent-space normals from the very same displacement field. Surface
  // normals now follow the nose, eye sockets and cheeks, rather than a flat blue map.
  for(let row=0;row<2048;row++)for(let col=0;col<2048;col++){
   const i=(row*2048+col)*4;
   const dx=(d[(row*2048+Math.min(2047,col+12))*4]-d[(row*2048+Math.max(0,col-12))*4])*.95/24;
   const dy=(d[(Math.min(2047,row+12)*2048+col)*4]-d[(Math.max(0,row-12)*2048+col)*4])*.95/24;
   const len=Math.hypot(dx,dy,1);n.data[i]=Math.round(127.5-127.5*dx/len);n.data[i+1]=Math.round(127.5+127.5*dy/len);n.data[i+2]=Math.round(127.5+127.5/len);n.data[i+3]=255;
  }nc.putImageData(n,0,0);
  const rough=canvas();const rc=rough.getContext('2d');rc.fillStyle='#d9d9d9';rc.fillRect(0,0,2048,2048);
  const diffuse=color.toDataURL('image/jpeg',.97);
  window.mv33PortraitInfo={method:'photo + inferred depth + derived normals',source:[photo.width,photo.height],texture:4096,meshSegments:256};
  return {diffuse,alpha:alpha.toDataURL(),depth:depth.toDataURL(),normal:normal.toDataURL(),roughness:rough.toDataURL(),shadow:diffuse,'shadow-softer-edit':diffuse,'shadow-to-zip-edit':diffuse};
 })();
 window.mv33TextureURL=async url=>{if(url.includes('/textures/head/')){const key=url.split('/').pop().split('.')[0];return (await portraits)[key]||url;}return url;};
 window.mv33TexturesReady=portraits;
 const media=matchMedia('(prefers-color-scheme: dark)');const icon=()=>{const i=document.getElementById('mv-favicon');if(i)i.href=media.matches?'/max/favicon-dark.svg':'/max/favicon-light.svg';};document.addEventListener('DOMContentLoaded',icon,{once:true});media.addEventListener('change',icon);
})();
