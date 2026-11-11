"""Bake a small physical edge bevel into the existing shell UVs; no livery rebake.
Run with Blender --background --python scripts/bake_helmet_surface_normals.py.
"""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'assets/source/max-helmet/bake-base.glb'))
obj=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.name=='helmet')
for o in list(bpy.context.scene.objects):
 if o!=obj:bpy.data.objects.remove(o,do_unlink=True)
mat=bpy.data.materials.new('Shell edge finish');mat.use_nodes=True
nodes=mat.node_tree.nodes;links=mat.node_tree.links
bsdf=next(n for n in nodes if n.type=='BSDF_PRINCIPLED')
bevel=nodes.new('ShaderNodeBevel');bevel.inputs['Radius'].default_value=.00012;bevel.samples=4
links.new(bevel.outputs['Normal'],bsdf.inputs['Normal'])
obj.data.materials.clear();obj.data.materials.append(mat)
image=bpy.data.images.new('shell-surface-normal',width=2048,height=2048,alpha=False)
image.colorspace_settings.name='Non-Color'
image.generated_color=(.5,.5,1,1)
target=nodes.new('ShaderNodeTexImage');target.image=image;nodes.active=target
bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16
scene.render.bake.margin=16;scene.render.bake.normal_space='TANGENT';scene.render.bake.use_selected_to_active=False
bpy.ops.object.bake(type='NORMAL')
path=ROOT/'public/max/materials/shell-surface-normal.png';image.filepath_raw=str(path);image.file_format='PNG';image.save()
(ROOT/'docs/research/helmet-surface-normal.json').write_text(json.dumps({'source':'assets/source/max-helmet/bake-base.glb','author':'Maubian','license':'CC-BY-4.0','output':str(path.relative_to(ROOT)),'size':[2048,2048],'method':'Cycles tangent normal bake, Bevel shader radius .00012, 4 samples, existing shell UVs','note':'Surface edge finish from existing mesh, not a transferred Norris normal map or invented sponsor relief.'},indent=2)+'\n')
print('NORMAL_BAKED',path,flush=True)
