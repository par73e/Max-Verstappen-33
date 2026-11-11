import * as THREE from 'three';
import {GLTFLoader} from '/vendor/three/GLTFLoader.js';
import {RGBELoader} from '/vendor/three/RGBELoader.js';
import {OrbitControls} from '/vendor/three/OrbitControls.js';
const edition=JSON.parse(document.getElementById('helmet-edition').textContent);
await import(edition.materials);
const media=matchMedia('(prefers-color-scheme: dark)');
const icon=()=>document.getElementById('mv-favicon').href=media.matches?'/max/favicon-dark.svg':'/max/favicon-light.svg';icon();media.addEventListener('change',icon);
const stage=document.querySelector('.model-stage'),canvas=document.getElementById('helmet-canvas'),status=document.getElementById('model-status');
window.mvHelmetPage={state:'loading',errors:[]};
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
try {
 const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true,powerPreference:'high-performance'});
 renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.92;
 const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(30,1,.001,5);
 const target=new THREE.Vector3(0,.004,0);camera.position.set(0,.012,.205);
 const controls=new OrbitControls(camera,canvas);controls.target.copy(target);controls.enableDamping=true;controls.enablePan=false;controls.enableZoom=true;controls.minDistance=.13;controls.maxDistance=.35;controls.minPolarAngle=.35;controls.maxPolarAngle=Math.PI-.35;controls.rotateSpeed=.65;controls.zoomSpeed=.6;controls.update();
 scene.add(new THREE.HemisphereLight(0xffffff,0x757866,1.4));
 const light=new THREE.DirectionalLight(0xffffff,1.2);light.position.set(-.1,.15,.2);scene.add(light);
 const fill=new THREE.DirectionalLight(0xffdec6,.6);fill.position.set(.15,0,-.1);scene.add(fill);
 const env=await new RGBELoader().loadAsync('/gl/hdri/studio_small_08_1k--light.hdr');const pmrem=new THREE.PMREMGenerator(renderer);const environment=pmrem.fromEquirectangular(env).texture;scene.environment=environment;env.dispose();pmrem.dispose();
 const gltf=await new GLTFLoader().loadAsync(edition.model);const model=gltf.scene,group=new THREE.Group(),wire=new THREE.Group();group.add(model,wire);scene.add(group);
 const surfaceNormal=await new THREE.TextureLoader().loadAsync('/max/materials/shell-surface-normal.png');surfaceNormal.flipY=false;
 const meshes=[];model.traverse(o=>{if(o.isMesh)meshes.push(o)});
 meshes.forEach(mesh=>{
  window.mv33ApplyHelmetMaterial(mesh,environment,edition.id);
  if(mesh.name==='helmet'){mesh.material.normalMap=surfaceNormal;mesh.material.normalScale.set(.55,.55);}
  for(const key of ['map','normalMap','roughnessMap','metalnessMap'])if(mesh.material[key]){mesh.material[key].anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());mesh.material[key].needsUpdate=true;}
  const geometry=new THREE.WireframeGeometry(mesh.geometry);const lines=new THREE.LineSegments(geometry,new THREE.LineBasicMaterial({color:0x535b4d,transparent:true,opacity:.16}));lines.position.copy(mesh.position);lines.rotation.copy(mesh.rotation);lines.scale.copy(mesh.scale);wire.add(lines);
 });
 model.scale.set(1.0435,.9565,1);wire.scale.copy(model.scale);
 wire.visible=false;
 let needsRender=true;controls.addEventListener('change',()=>{needsRender=true;});
 const resize=()=>{const {width,height}=stage.getBoundingClientRect();if(!width||!height)return;renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();needsRender=true;};new ResizeObserver(resize).observe(stage);resize();
 let stageVisible=true;new IntersectionObserver(entries=>{stageVisible=entries[0].isIntersecting},{rootMargin:'100px'}).observe(stage);
 const start=performance.now();let lastTime=0,targetTheta=null,wireMode=false;
 function frame(now){
  if(document.hidden||!stageVisible){lastTime=now;requestAnimationFrame(frame);return;}
  const dt=Math.min((now-lastTime)/1000,.05);lastTime=now;
  if(targetTheta!==null){const phi=controls.getPolarAngle(),theta=controls.getAzimuthalAngle(),diff=Math.atan2(Math.sin(targetTheta-theta),Math.cos(targetTheta-theta));const next=theta+diff*Math.min(1,dt*8);const radius=camera.position.distanceTo(target);camera.position.setFromSpherical(new THREE.Spherical(radius,phi,next)).add(target);if(Math.abs(diff)<.001)targetTheta=null;}
  const changed=controls.update();const progress=reduced.matches?1:Math.min(1,(now-start)/750);group.scale.setScalar(.94+.06*(1-Math.pow(1-progress,3)));if(needsRender||changed||progress<1||targetTheta!==null){renderer.render(scene,camera);needsRender=false;}requestAnimationFrame(frame);
 }
 controls.addEventListener('start',()=>{targetTheta=null;document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed','false'))});
 const view=angle=>{targetTheta=angle;if(reduced.matches){const radius=camera.position.distanceTo(target);camera.position.setFromSpherical(new THREE.Spherical(radius,Math.PI/2,angle)).add(target);targetTheta=null;controls.update();}};
 document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));view({front:0,left:-Math.PI/3,right:Math.PI/3,back:Math.PI}[button.dataset.view]);}));
 document.getElementById('wireframe').addEventListener('click',e=>{wireMode=!wireMode;model.visible=!wireMode;wire.visible=wireMode;needsRender=true;e.currentTarget.setAttribute('aria-pressed',String(wireMode));});
 canvas.addEventListener('keydown',event=>{if(['ArrowLeft','ArrowRight','Home'].includes(event.key)){event.preventDefault();view(event.key==='Home'?0:controls.getAzimuthalAngle()+(event.key==='ArrowLeft'?-.2:.2));}});
 stage.classList.add('model-ready');window.mvHelmetPage={state:'ready',edition:edition.id,model,wire,renderer,camera,controls,errors:[]};requestAnimationFrame(frame);
} catch(error){stage.classList.add('model-failed');status.textContent='三维预览未加载，显示原始摄影 / Showing the source photograph';window.mvHelmetPage.errors.push(String(error));window.mvHelmetPage.state='fallback';console.error(error);}
