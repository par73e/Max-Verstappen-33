"""Keep reference geometry/UVs intact and adapt its material artwork."""
import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'public/gl/models/helmet-21.glb'))
for obj in bpy.context.scene.objects:
 if obj.type!='MESH':continue
 mat=bpy.data.materials.new('MV33-source-fit-'+obj.name);mat.use_nodes=True
 shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
 shader.inputs['Roughness'].default_value=.3;shader.inputs['Metallic'].default_value=.02
 if obj.name!='plastic':
  tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/'public/max/materials/source-fit'/('season-2023-'+obj.name+'.jpg')))
  mat.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color'])
  normal=mat.node_tree.nodes.new('ShaderNodeTexImage')
  normal.image=bpy.data.images.load(str(ROOT/('public/gl/textures/'+('helmet/webp/Norris_Helmet_mat_Normal.webp' if obj.name=='helmet' else 'glass/webp/Norris_Glass_mat_Normal.webp'))));normal.image.colorspace_settings.name='Non-Color'
  nm=mat.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.5
  mat.node_tree.links.new(normal.outputs['Color'],nm.inputs['Color']);mat.node_tree.links.new(nm.outputs['Normal'],shader.inputs['Normal'])
 obj.data.materials.clear();obj.data.materials.append(mat)
 obj['sourceFit']=True;obj['geometrySource']='Lando Norris / OFF+BRAND reference helmet-21.glb'
 obj['adaptation']='Original geometry and UVs; reconstructed Max 2023 photographic livery. Not a Schuberth scan.'
bpy.ops.export_scene.gltf(filepath=str(ROOT/'public/gl/models/source-fit-season-2023.glb'),export_format='GLB',export_extras=True,export_image_format='JPEG',export_jpeg_quality=95)
