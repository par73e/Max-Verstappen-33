"""Blender UV baking: official multi-view photographs onto the credited artist mesh.
Approximate reconstruction, not an official helmet scan or supplied 2023/24 model.
"""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'assets/source/max-helmet/base.glb'))
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
for o in objects:
 matrix=o.matrix_world.copy()
 for v in o.data.vertices:v.co=matrix@v.co
 o.parent=None;o.matrix_world.identity()
# The artist atlas reuses islands. Give the photographic bake unique UV space.
for obj in objects:
 if obj.name!='helmet':continue
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=.015);bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.export_scene.gltf(filepath=str(ROOT/'assets/source/max-helmet/bake-base.glb'),export_format='GLB',export_materials='EXPORT',export_image_format='JPEG',export_jpeg_quality=90)
points=[v.co.copy() for o in objects for v in o.data.vertices]
# Angles are camera positions around the helmet: 0 is frontal, positive is right.
views={
 'season-2023':[
  ('hq-front.jpg',0,(102,195,795,1005)),
  ('hq-right.jpg',42,(85,220,820,940)),
  ('hq-left.jpg',-42,(85,220,820,940)),
  ('hq-back.jpg',180,(110,195,790,1005))],
 'zandvoort-2024':[
  ('orange-2024-04.jpg',30,(205,50,710,590)),
  ('orange-2024-03.jpg',-40,(180,55,740,575)),
  ('orange-2024-05.jpg',80,(150,65,765,570)),
  ('orange-2024-06.jpg',180,(240,50,695,590)),
  ('orange-2024-07.jpg',140,(190,50,735,565)),
  ('orange-2024-08.jpg','top',(255,35,680,590))]
}
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=1
scene.render.bake.use_pass_direct=False;scene.render.bake.use_pass_indirect=False;scene.render.bake.margin=12
outdir=ROOT/'public/max/materials';outdir.mkdir(exist_ok=True)
metadata=[]
def mathnode(nodes,links,op,a,b=None):
 n=nodes.new('ShaderNodeMath');n.operation=op
 for idx,v in enumerate([a,b] if b is not None else [a]):
  if hasattr(v,'node'):links.new(v,n.inputs[idx])
  else:n.inputs[idx].default_value=v
 return n.outputs[0]
requested=next((a.split('=',1)[1] for a in sys.argv if a.startswith('--edition=')),None)
for edition,photos in views.items():
 if requested and edition!=requested:continue
 for obj in objects:
  if obj.name!='helmet':continue
  # Visor is given a separate reflective physical material, avoiding baked reflections.
  mat=bpy.data.materials.new(edition+'-'+obj.name);mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear()
  geo=n.new('ShaderNodeNewGeometry');direction_node=n.new('ShaderNodeVectorMath');direction_node.operation='NORMALIZE'
  # Horizontal view confidence must not collapse at the crown: raising a small
  # 3D direction cosine to 64 underflows to zero and creates a black cap.
  if edition=='season-2023':
   horizontal=n.new('ShaderNodeVectorMath');horizontal.operation='MULTIPLY';l.new(geo.outputs['Position'],horizontal.inputs[0]);horizontal.inputs[1].default_value=(1,1,0);l.new(horizontal.outputs['Vector'],direction_node.inputs[0])
  else:l.new(geo.outputs['Position'],direction_node.inputs[0])
  colors=[];weights=[]
  for filename,angle,box in photos:
   direction=Vector((0,0,1)) if angle=='top' else Vector((math.sin(math.radians(angle)),-math.cos(math.radians(angle)),0))
   right=Vector((1,0,0)) if angle=='top' else Vector((-direction.y,direction.x,0))
   up=Vector((0,-1,0)) if angle=='top' else Vector((0,0,1))
   coords=n.new('ShaderNodeCombineXYZ');im=bpy.data.images.load(str(ROOT/'assets/source/max-helmet/photos-2023'/filename.removeprefix('hq-') if filename.startswith('hq-') else ROOT/'public/max'/filename),check_existing=True);w,h=im.size
   if filename.startswith('hq-'):box=tuple(v*(w/900 if k in [0,2] else h/1200) for k,v in enumerate(box))
   for axis,vec,imin,imax in [(0,right,box[0]/w,box[2]/w),(1,up,1-box[3]/h,1-box[1]/h)]:
    low=min(p.dot(vec) for p in points);high=max(p.dot(vec) for p in points)
    dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(geo.outputs['Position'],dot.inputs[0]);dot.inputs[1].default_value=vec
    k=(imax-imin)/(high-low);v=mathnode(n,l,'MULTIPLY_ADD',dot.outputs['Value'],k)
    v.node.inputs[2].default_value=imin-low*k
    if edition=='season-2023' and axis==1:
     # Register the forehead decals above the authored ORACLE strip. The source
     # photograph's band is lower than this mesh's band; using full-body bounds
     # otherwise cuts through the Red Bull wordmark. Blend inside the visor gap.
     z=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],z.inputs[0])
     ramp=n.new('ShaderNodeMapRange');ramp.clamp=True;ramp.interpolation_type='SMOOTHSTEP'
     l.new(z.outputs['Z'],ramp.inputs['Value']);ramp.inputs['From Min'].default_value=.014;ramp.inputs['From Max'].default_value=.021
     lifted=mathnode(n,l,'MULTIPLY_ADD',v,1.26);lifted.node.inputs[2].default_value=(1-1.26)*imax
     delta=mathnode(n,l,'SUBTRACT',lifted,v);offset=mathnode(n,l,'MULTIPLY',delta,ramp.outputs['Result']);v=mathnode(n,l,'ADD',v,offset)
    l.new(v,coords.inputs[axis])
   tex=n.new('ShaderNodeTexImage');tex.image=im;tex.extension='EXTEND';l.new(coords.outputs[0],tex.inputs['Vector']);colors.append(tex.outputs['Color'])
   dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(direction_node.outputs['Vector'],dot.inputs[0]);dot.inputs[1].default_value=direction
   positive=mathnode(n,l,'MAXIMUM',dot.outputs['Value'],0.3);weight=mathnode(n,l,'POWER',positive,64)
   if edition=='season-2023' and angle==0:weight=mathnode(n,l,'MULTIPLY',weight,4)
   weights.append(weight)
  total=weights[0]
  for weight in weights[1:]:total=mathnode(n,l,'ADD',total,weight)
  last=None
  for color,weight in zip(colors,weights):
   normal=mathnode(n,l,'DIVIDE',weight,total)
   mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;l.new(color,mix.inputs[1]);l.new(normal,mix.inputs[2])
   if last is None:last=mix.outputs[0]
   else:
    add=n.new('ShaderNodeMixRGB');add.blend_type='ADD';add.inputs[0].default_value=1;l.new(last,add.inputs[1]);l.new(mix.outputs[0],add.inputs[2]);last=add.outputs[0]
  emission=n.new('ShaderNodeEmission');l.new(last,emission.inputs[0]);output=n.new('ShaderNodeOutputMaterial');l.new(emission.outputs[0],output.inputs[0])
  image=bpy.data.images.new(edition+'-'+obj.name,width=4096,height=4096,alpha=False)
  target=n.new('ShaderNodeTexImage');target.image=image;n.active=target
  obj.data.materials.clear();obj.data.materials.append(mat)
  bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
  bpy.ops.object.bake(type='EMIT')
  path=outdir/(edition+'-'+obj.name+'.jpg');image.filepath_raw=str(path);image.file_format='JPEG';image.save();metadata.append({'edition':edition,'part':obj.name,'path':str(path.relative_to(ROOT))})
  print('BAKED',edition,obj.name,flush=True)
record_path=ROOT/'docs/research/helmet-baking.json'
if requested and record_path.exists():metadata=[r for r in json.loads(record_path.read_text()) if r['edition']!=requested and r['part']=='helmet']+metadata
record_path.write_text(json.dumps(metadata,indent=2))
