/* Inserted into the retained engine: native Max geometry/materials, shared wireframe. */
class F9 {
  constructor(settings) {
    this.gl = new RQ(); this.settings = settings;this.surfaceRevision=0;this.draws=0;
    this.instance = this.gl.assets.models.helmet.scene.clone(true);
    // Match the reference helmet scale while retaining the artist mesh proportions.
    this.sourceFit=this.instance.children.some(o=>o.userData.sourceFit);
    this.setHelmetScale();
    this.bannerTexture=this.sourceFit?this.gl.assets.textureLoader.load('/max/helmet-2023-front-hq.jpg',()=>{this.surfaceRevision++;}):null;
    this.frontArtworkReady={value:0};
    this.frontArtwork=this.sourceFit?this.gl.assets.textureLoader.load('/max/materials/season-2023-front-flat.png',()=>{this.frontArtworkReady.value=1;this.surfaceRevision++;},undefined,()=>{window.mv33Errors?.push('Front artwork failed to load');}):null;
    this.instance.traverse(mesh => {
      if (!mesh.isMesh) return;
      // Refit the lower front and visor band without changing the source GLB.
      // All helmet components share the same vertical mapping to avoid gaps.
      if(!this.sourceFit){
        mesh.geometry=mesh.geometry.clone();
        const position=mesh.geometry.attributes.position;
        const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
        for(let i=0;i<position.count;i++){
          let x=position.getX(i),y=position.getY(i),z=position.getZ(i);
          const front=smooth(.008,.035,z),lower=1-smooth(-.034,-.018,y),center=1-smooth(.006,.031,Math.abs(x));
          x*=1-.055*front*lower;
          y-=.0015*front*lower*center;
          z+=.0010*front*lower*center;
          // Compress the visor-height band and redistribute that height into
          // the chin. Apply the same continuous mapping to every component.
          const top=.0217,bottom=-.00825,chin=-.0345,visorScale=.82;
          const raised=top+(bottom-top)*visorScale;
          let ySlope=1;
          if(y<top&&y>=bottom){y=top+(y-top)*visorScale;ySlope=visorScale;}
          else if(y<bottom&&y>chin){ySlope=(raised-chin)/(bottom-chin);y=chin+(y-chin)*ySlope;}
          position.setXYZ(i,x,y,z);
          const normal=mesh.geometry.attributes.normal;
          if(normal&&ySlope!==1){
            const nx=normal.getX(i),ny=normal.getY(i)/ySlope,nz=normal.getZ(i),length=Math.hypot(nx,ny,nz)||1;
            normal.setXYZ(i,nx/length,ny/length,nz/length);normal.needsUpdate=true;
          }
        }
        position.needsUpdate=true;mesh.geometry.computeBoundingBox();mesh.geometry.computeBoundingSphere();
      }
      window.mv33ApplyHelmetMaterial(mesh,this.gl.assets.hdri.light,'season-2023',{offscreen:true,bannerTexture:this.bannerTexture,frontArtwork:this.frontArtwork,frontArtworkReady:this.frontArtworkReady});
      if(mesh.name==='helmet'&&!this.sourceFit){
        this.gl.assets.textureLoader.load('/max/materials/shell-surface-normal.png',normal=>{
          normal.flipY=false;mesh.material.normalMap=normal;mesh.material.normalScale.set(.55,.55);mesh.material.needsUpdate=true;this.surfaceRevision++;
        },undefined,error=>window.mv33Errors?.push('Shell surface normal failed: '+error));
      }
      for(const key of ['map','normalMap','roughnessMap','metalnessMap'])if(mesh.material[key]){mesh.material[key].anisotropy=Math.min(8,this.gl.renderer.instance.capabilities.getMaxAnisotropy());mesh.material[key].needsUpdate=true;}
      if(this.sourceFit&&mesh.name==='plastic')mesh.material=new rC({transparent:true,opacity:.25,matcap:this.gl.assets.textures.plastic.matcap,side:hB,depthWrite:false});
    });
    this.scene = new rB(); this.scene.add(this.instance);
    this.renderTarget = new XB(...this.targetSize(), {samples: 2});
    this.wireframeMeshMaterial = new fQ({wireframe: true, transparent: true, depthWrite: false,
      uniforms: {uTime: new YA(0), uOpacity: new YA(1)},
      vertexShader: 'varying vec3 vPosition;void main(){vPosition=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
      fragmentShader: 'varying vec3 vPosition;uniform float uTime;uniform float uOpacity;void main(){float phase=-vPosition.y*10.0-uTime;float band=fract(phase);float edge=max(fwidth(phase),0.002);float scan=pow(band,4.0)*smoothstep(0.0,edge,1.0-band)*0.1;gl_FragColor=vec4(vec3(0.0),scan*uOpacity);}'
    });
    const geometries = [];
    this.instance.traverse(mesh => {
      if (!mesh.isMesh) return;
      const geometry = mesh.geometry.clone();
      for (const key of Object.keys(geometry.attributes)) if (key !== 'position') geometry.deleteAttribute(key);
      geometries.push(geometry);
    });
    this.wireframeMesh = new OQ(s5(geometries), this.wireframeMeshMaterial);
    this.wireframeMesh.position.copy(this.instance.position);
    this.wireframeMesh.scale.copy(this.instance.scale);
    this.settings.scene.add(this.wireframeMesh);
    window.mv33Helmet = {instance: this.instance, wireframe: this.wireframeMesh, source: this.sourceFit?'OFF+BRAND reference geometry / Max reconstructed livery':'Maubian / CC BY 4.0'};
  }
  setHelmetScale(){
    const scale=this.sourceFit?[7.038,7.038,7.242]:(window.innerWidth>991?[7.75,7.104,7.644]:[7.3332,6.7221,7.23135]);
    this.instance.scale.set(...scale);
  }
  targetSize(){
    const {width,height,pixelRatio}=this.gl.sizes;
    const ratio=Math.min(window.devicePixelRatio,2,Math.sqrt(5000000/(width*height)));
    return [Math.max(1,Math.round(width*ratio)),Math.max(1,Math.round(height*ratio))];
  }
  resize(){this.setHelmetScale();this.renderTarget.setSize(...this.targetSize());this.lastFrameSignature=null;}
  update(){
    this.wireframeMesh.visible=window.innerWidth>991||document.querySelector('[data-home-swipe-toggle]')?.getAttribute('aria-pressed')==='true'||window.mv33HeadScene?.headDefault.uniforms.uHelmetHover.value>.001;
    this.wireframeMesh.position.copy(this.instance.position);
    this.wireframeMesh.scale.copy(this.instance.scale);
    this.wireframeMesh.rotation.copy(this.instance.rotation);
    this.wireframeMeshMaterial.uniforms.uTime.value=this.gl.time.elapsed;
    // A stationary PBR helmet can be sampled by the fluid compositor without
    // redrawing its full-resolution color target on every animation frame.
    this.instance.updateMatrixWorld(true);this.settings.camera.updateMatrixWorld();
    const signature=[...this.instance.matrixWorld.elements,...this.settings.camera.matrixWorldInverse.elements,...this.settings.camera.projectionMatrix.elements,this.surfaceRevision,this.renderTarget.width,this.renderTarget.height].map(v=>Math.round(v*100000)).join(',');
    if(signature===this.lastFrameSignature)return;
    this.lastFrameSignature=signature;this.draws++;
    this.gl.renderer.instance.setRenderTarget(this.renderTarget);
    this.gl.renderer.instance.render(this.scene,this.settings.camera);
    this.gl.renderer.instance.clear();
  }
}
