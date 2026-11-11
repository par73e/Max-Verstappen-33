/* Authored hardware UVs stay intact; only the painted shell uses reconstructed livery. */
window.mv33ApplyHelmetMaterial = (mesh, environment, edition='season-2023', options={}) => {
 const material=mesh.material.clone();
 material.envMap=environment;material.transparent=false;material.opacity=1;material.depthWrite=true;
 if('transmission' in material)material.transmission=0;
 if(mesh.name==='glass'){
  // The ORACLE strip belongs to the separate plastic mesh. Projecting that strip
  // onto the visor as well produced a second, displaced edge and a flat reflection.
  material.metalnessMap=null;material.roughnessMap=null;
  if(!mesh.userData.sourceFit)material.map=null;
  material.color.setHex(edition==='zandvoort-2024'?0x795d70:0x9f7a46);
  material.metalness=1;material.roughness=.085;material.envMapIntensity=1.15;
  if('clearcoat' in material){material.clearcoat=.65;material.clearcoatRoughness=.055;}
  material.normalScale?.set(.35,.35);
  material.envMapRotation?.set(0,0,0);
  if('iridescence' in material){material.iridescence=edition==='zandvoort-2024'?.5:.12;material.iridescenceIOR=1.35;material.iridescenceThicknessRange=[180,300];}
 }else if(mesh.name==='helmet'){
  material.metalness=.02;material.roughness=edition==='season-2023'?.25:.26;material.envMapIntensity=edition==='season-2023'?.9:1;
  if('specularIntensity' in material)material.specularIntensity=edition==='season-2023'?.68:.65;
  if('clearcoat' in material){material.clearcoat=edition==='season-2023'?.6:.6;material.clearcoatRoughness=edition==='season-2023'?.085:.09;}
 }else{
  // Source normals, roughness and decals use the artist's matching UV layout.
  material.metalness=.16;material.roughness=.24;material.envMapIntensity=1.05;
  material.normalScale?.set(.5,.5);
 }
 if(mesh.userData.sourceFit&&mesh.name==='glass'&&options.bannerTexture){
  const tint=material.color.clone().setHex(0x0b0b0b);material.color.setHex(0xffffff);material.map=null;
  material.envMapIntensity=1.5;material.roughness=.06;material.metalness=.15;
  if('clearcoat' in material){material.clearcoat=.8;material.clearcoatRoughness=.04;}
  if('iridescence' in material)material.iridescence=0;
  const image=options.bannerTexture;
  image.colorSpace='srgb';image.flipY=true;
  material.onBeforeCompile=shader=>{
   shader.uniforms.mvTint={value:tint};shader.uniforms.mvBanner={value:image};
   shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 mvPos;').replace('#include <begin_vertex>','#include <begin_vertex>\nmvPos=position;');
   shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nvarying vec3 mvPos;uniform vec3 mvTint;uniform sampler2D mvBanner;').replace('#include <map_fragment>',`#include <map_fragment>
    float mvBottom=0.0114-0.0015*pow(clamp(abs(mvPos.x)/0.036,0.0,1.0),2.0);
    float mvTop=0.0167-0.002*pow(clamp(abs(mvPos.x)/0.036,0.0,1.0),2.0);
    float mvBand=smoothstep(mvBottom,mvBottom+0.0004,mvPos.y)*(1.0-smoothstep(mvTop-0.0004,mvTop,mvPos.y))*smoothstep(0.005,0.02,mvPos.z);
    vec2 bannerUv=vec2(0.5+mvPos.x*10.2,mix(1.0-550.0/1200.0,1.0-465.0/1200.0,clamp((mvPos.y-mvBottom)/(mvTop-mvBottom),0.0,1.0)));
    vec3 banner=texture2D(mvBanner,bannerUv).rgb;
    diffuseColor.rgb=mix(mvTint,banner,mvBand);
   `).replace('#include <metalnessmap_fragment>','#include <metalnessmap_fragment>\nmetalnessFactor=mix(0.15,0.02,mvBand);').replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\nroughnessFactor=mix(0.06,0.32,mvBand);');
  };
  material.customProgramCacheKey=()=> 'mv-source-fit-visor-black-1';
 }
 // Remove the visor's photographic red reflection incorrectly projected onto
 // the source shell; retain geometry and its separate painted chin artwork.
 if(mesh.userData.sourceFit&&mesh.name==='helmet'){
  const art=options.frontArtwork;if(art){art.colorSpace='srgb';art.flipY=true;}
  const prepare=material.onBeforeCompile;
  material.onBeforeCompile=shader=>{
   prepare.call(material,shader);
   shader.uniforms.mvFrontArt={value:art};shader.uniforms.mvFrontArtReady=options.frontArtworkReady||{value:0};
   shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 mvShellPos;').replace('#include <begin_vertex>','#include <begin_vertex>\nmvShellPos=position;');
   shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nvarying vec3 mvShellPos;uniform sampler2D mvFrontArt;uniform float mvFrontArtReady;').replace('#include <map_fragment>',`#include <map_fragment>
    // Replace only the two damaged front artwork regions with the clean
    // source-derived vector color separation, projected in model coordinates.
    float crownMask=(1.0-smoothstep(0.0154,0.0185,abs(mvShellPos.x)))*smoothstep(0.0162,0.0180,mvShellPos.y)*(1.0-smoothstep(0.0308,0.0325,mvShellPos.y))*smoothstep(0.015,0.022,mvShellPos.z);
    vec2 crownUv=vec2(0.5+mvShellPos.x*10.22,1.0-(1150.0-(mvShellPos.y-0.0175)*(370.0/0.013))/3000.0);
    vec3 crown=texture2D(mvFrontArt,crownUv).rgb;
    diffuseColor.rgb=mix(diffuseColor.rgb,crown,crownMask*mvFrontArtReady);
    float chinMask=(1.0-smoothstep(0.0088,0.0128,abs(mvShellPos.x)))*smoothstep(-0.034,-0.0325,mvShellPos.y)*(1.0-smoothstep(-0.016,-0.014,mvShellPos.y))*smoothstep(0.035,0.042,mvShellPos.z);
    vec2 chinUv=vec2(0.5+mvShellPos.x*10.7,1.0-(2405.0-(mvShellPos.y+0.0283)*(300.0/0.0115))/3000.0);
    vec3 chin=texture2D(mvFrontArt,chinUv).rgb;
    diffuseColor.rgb=mix(diffuseColor.rgb,chin,chinMask*mvFrontArtReady);
    float front=smoothstep(0.025,0.04,mvShellPos.z);
    float centre=1.0-smoothstep(0.026,0.031,abs(mvShellPos.x));
    float band=smoothstep(-0.010,-0.0085,mvShellPos.y)*(1.0-smoothstep(-0.001,-0.0002,mvShellPos.y));
    float unwanted=front*centre*band;
    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.86,0.88,0.90),unwanted);
    vec2 vent=vec2((abs(mvShellPos.x)-0.012)/0.0053,(mvShellPos.y+0.0054)/0.0017);
    float ventShape=(1.0-smoothstep(0.84,1.0,length(vent)))*front*centre*band;
    vec2 grille=fract(vec2(mvShellPos.x*1800.0,mvShellPos.y*2000.0));
    float holes=step(0.48,grille.x)*step(0.48,grille.y);
    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.10+0.18*holes),ventShape*0.9);
   `);
  };
  material.customProgramCacheKey=()=> 'mv-source-fit-shell-clean-6';
 }
 // The home hero renders into an offscreen target before compositing. Compress
 // specular peaks there; edition pages already use renderer ACES tone mapping.
 if(options.offscreen){
  const prepare=material.onBeforeCompile;
  const programKey=material.customProgramCacheKey.bind(material);
  const previousKey=programKey();
  material.onBeforeCompile=shader=>{
   prepare.call(material,shader);
   shader.fragmentShader=shader.fragmentShader.replace('#include <opaque_fragment>',`
    ${mesh.name==='helmet'&&!mesh.userData.sourceFit ? 'float mvFacing=abs(dot(normalize(normal),normalize(vViewPosition))); float mvRim=pow(1.0-clamp(mvFacing,0.0,1.0),3.0); outgoingLight*=1.0-0.12*mvRim;' : ''}
    vec3 mvExposed=max(outgoingLight*0.92,vec3(0.0));
    outgoingLight=clamp((mvExposed*(2.51*mvExposed+0.03))/(mvExposed*(2.43*mvExposed+0.59)+0.14),0.0,1.0);
    #include <opaque_fragment>
   `);
  };
  material.customProgramCacheKey=()=>previousKey+'-mv-offscreen-finish-2';
 }
 // Approximate the two small grey chin vents from the 2023 front photo.
 // Coordinates are in the original helmet local space, not in screen pixels.
 if(edition==='season-2023' && mesh.name==='helmet' && !mesh.userData.sourceFit){
  const prepare=material.onBeforeCompile;
  const previousKey=material.customProgramCacheKey.bind(material)();
  material.onBeforeCompile=shader=>{
   prepare.call(material,shader);
   shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 mvVentPos;').replace('#include <begin_vertex>','#include <begin_vertex>\nmvVentPos = position;');
   shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nvarying vec3 mvVentPos;').replace('#include <map_fragment>',`#include <map_fragment>
    vec2 mvVent=vec2(abs(mvVentPos.x)-0.0105,mvVentPos.y+0.0205);
    float mvVentHeight=0.0017;
    float mvVentWidth=0.0028*clamp((mvVentHeight-mvVent.y)/(2.0*mvVentHeight),0.0,1.0);
    float mvVentDistance=max(abs(mvVent.x)-mvVentWidth,max(mvVent.y-mvVentHeight,-mvVent.y-mvVentHeight));
    float mvVentMask=(1.0-smoothstep(-0.00022,0.00022,mvVentDistance))*smoothstep(0.025,0.038,mvVentPos.z);
    float mvDots=step(0.45,fract((mvVentPos.x+mvVentPos.y)*1500.0))*step(0.45,fract((mvVentPos.x-mvVentPos.y)*1500.0));
    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.30+0.22*mvDots),mvVentMask*0.5);
   `);
  };
  material.customProgramCacheKey=()=>previousKey+'-mv-2023-chin-vents-1';
 }
 material.needsUpdate=true;mesh.material=material;return material;
};
