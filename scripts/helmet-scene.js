/* Inserted into the retained engine: native Max geometry/materials, shared wireframe. */
class F9 {
  constructor(settings) {
    this.gl = new RQ(); this.settings = settings;
    this.instance = this.gl.assets.models.helmet.scene.clone(true);
    // Fit the narrower artist mesh to the source helmet/head relationship.
    this.sourceFit=this.instance.children.some(o=>o.userData.sourceFit);
    this.instance.scale.set(...(this.sourceFit?[6.9,6.9,7.1]:[7.2,6.6,7.1]));
    this.instance.traverse(mesh => {
      if (!mesh.isMesh) return;
      window.mv33ApplyHelmetMaterial(mesh,this.gl.assets.hdri.light);
      for(const key of ['map','normalMap','roughnessMap','metalnessMap'])if(mesh.material[key]){mesh.material[key].anisotropy=Math.min(8,this.gl.renderer.instance.capabilities.getMaxAnisotropy());mesh.material[key].needsUpdate=true;}
      if(this.sourceFit&&mesh.name==='plastic')mesh.material=new rC({transparent:true,opacity:.25,matcap:this.gl.assets.textures.plastic.matcap,side:hB,depthWrite:false});
    });
    this.scene = new rB(); this.scene.add(this.instance);
    this.renderTarget = new XB(this.gl.sizes.width * this.gl.sizes.pixelRatio, this.gl.sizes.height * this.gl.sizes.pixelRatio, {samples: 4});
    this.wireframeMeshMaterial = new fQ({wireframe: true, transparent: true, depthWrite: false,
      uniforms: {uTime: new YA(0), uOpacity: new YA(1)},
      vertexShader: 'varying vec3 vPosition;void main(){vPosition=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
      fragmentShader: 'varying vec3 vPosition;uniform float uTime;uniform float uOpacity;void main(){float scan=pow(fract(-vPosition.y*10.0-uTime),4.0)*0.1;gl_FragColor=vec4(vec3(0.0),scan*uOpacity);}'
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
  resize(){this.renderTarget.setSize(this.gl.sizes.width*this.gl.sizes.pixelRatio,this.gl.sizes.height*this.gl.sizes.pixelRatio);}
  update(){
    this.wireframeMesh.position.copy(this.instance.position);
    this.wireframeMesh.scale.copy(this.instance.scale);
    this.wireframeMesh.rotation.copy(this.instance.rotation);
    this.wireframeMeshMaterial.uniforms.uTime.value=this.gl.time.elapsed;
    this.gl.renderer.instance.setRenderTarget(this.renderTarget);
    this.gl.renderer.instance.render(this.scene,this.settings.camera);
    this.gl.renderer.instance.clear();
  }
}
