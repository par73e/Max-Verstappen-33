/* Run in a same-origin browser page after image_gen extraction.
 * Returns the base64 2048px PNG. Original photographic interiors are retained;
 * AI cutout color is used only in a 24px silhouette band to avoid blue halos.
 */
(async () => {
  const load=src=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=src;});
  const [photo,cutout]=await Promise.all([load('/max/portrait-serious-source.png'),load('/max/portrait-serious-ai-cutout.png')]);
  const size=2048,canvas=document.createElement('canvas');canvas.width=canvas.height=size;
  const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';
  ctx.drawImage(photo,0,0,size,size);const original=ctx.getImageData(0,0,size,size);
  ctx.clearRect(0,0,size,size);ctx.drawImage(cutout,0,0,size,size);const extracted=ctx.getImageData(0,0,size,size);
  const count=size*size,distance=new Uint8Array(count).fill(255),queue=new Int32Array(count);let tail=0;
  for(let i=0;i<count;i++)if(extracted.data[i*4+3]<250){distance[i]=0;queue[tail++]=i;}
  for(let head=0;head<tail;head++){
    const i=queue[head],d=distance[i]+1;if(d>24)continue;
    const add=j=>{if(distance[j]>d){distance[j]=d;queue[tail++]=j;}};
    if(i%size)add(i-1);if(i%size<size-1)add(i+1);if(i>=size)add(i-size);if(i<count-size)add(i+size);
  }
  for(let i=0;i<count;i++){
    const k=i*4,weight=Math.min(1,distance[i]/24);
    for(let ch=0;ch<3;ch++)extracted.data[k+ch]=Math.round(extracted.data[k+ch]*(1-weight)+original.data[k+ch]*weight);
  }
  ctx.putImageData(extracted,0,0);return canvas.toDataURL('image/png').split(',')[1];
})();
