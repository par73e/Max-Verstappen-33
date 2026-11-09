/* Authored hardware UVs stay intact; only the painted shell uses reconstructed livery. */
window.mv33ApplyHelmetMaterial = (mesh, environment, edition='season-2023') => {
 const material=mesh.material.clone();
 material.envMap=environment;material.transparent=false;material.opacity=1;material.depthWrite=true;
 if('transmission' in material)material.transmission=0;
 if(mesh.name==='glass'){
  // The ORACLE strip belongs to the separate plastic mesh. Projecting that strip
  // onto the visor as well produced a second, displaced edge and a flat reflection.
  material.metalnessMap=null;material.roughnessMap=null;
  if(!mesh.userData.sourceFit)material.map=null;
  material.color.setHex(edition==='zandvoort-2024'?0xb26e72:0xeab65d);
  material.metalness=1;material.roughness=.22;material.envMapIntensity=.8;
  material.normalScale?.set(.12,.12);
  material.envMapRotation?.set(0,1.7,0);
  if('iridescence' in material){material.iridescence=edition==='zandvoort-2024'?.65:.3;material.iridescenceIOR=1.35;material.iridescenceThicknessRange=[180,380];}
 }else if(mesh.name==='helmet'){
  material.metalness=.02;material.roughness=.3;material.envMapIntensity=.8;
  if('clearcoat' in material){material.clearcoat=.9;material.clearcoatRoughness=.14;}
 }else{
  // Source normals, roughness and decals use the artist's matching UV layout.
  material.metalness=.12;material.roughness=.3;material.envMapIntensity=.65;
  material.normalScale?.set(.5,.5);
 }
 if(mesh.userData.sourceFit&&mesh.name==='glass'){
  const tint=material.color.clone();material.color.setHex(0xffffff);
  material.onBeforeCompile=shader=>{
   shader.uniforms.mvTint={value:tint};
   shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying float mvY;varying float mvX;').replace('#include <begin_vertex>','#include <begin_vertex>\nmvY=position.y;mvX=position.x;');
   shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nvarying float mvY;varying float mvX;uniform vec3 mvTint;').replace('#include <map_fragment>','#include <map_fragment>\nfloat mvBandBottom=0.007-0.0045*pow(clamp(abs(mvX)/0.036,0.0,1.0),2.0);float mvGlass=smoothstep(-0.0105,-0.008,mvY)*(1.0-smoothstep(mvBandBottom-0.0005,mvBandBottom+0.0005,mvY));diffuseColor.rgb=mix(diffuseColor.rgb,mvTint,mvGlass);').replace('#include <metalnessmap_fragment>','#include <metalnessmap_fragment>\nmetalnessFactor=mix(0.02,1.0,mvGlass);').replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\nroughnessFactor=mix(0.4,0.22,mvGlass);');
  };
  material.customProgramCacheKey=()=> 'mv-source-fit-visor-3';
 }
 material.needsUpdate=true;mesh.material=material;return material;
};
