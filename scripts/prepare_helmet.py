"""Run with Blender --background --python scripts/prepare_helmet.py."""
import bpy, json, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'assets/source/max-helmet/original.glb'))
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
world_points=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
lo=Vector(tuple(min(v[i] for v in world_points) for i in range(3)))
hi=Vector(tuple(max(v[i] for v in world_points) for i in range(3)))
center=(lo+hi)*.5
scale=.077/(hi.z-lo.z)
for o in objects:
 world=o.matrix_world.copy()
 for v in o.data.vertices:
  p=(world@v.co-center)*scale
  v.co=(-p.x,-p.y,p.z+.004)
 o.parent=None;o.matrix_world.identity()
 mat=o.data.materials[0]
 o.name={'aiStandardSurface6SG':'helmet','aiStandardSurface7SG':'glass','aiStandardSurface8SG':'plastic'}[mat.name]
 for p in o.data.polygons:p.use_smooth=True
for im in bpy.data.images:
 if im.type=='IMAGE' and im.size[0]>2048:im.scale(2048,2048)
# Keep the model's authored UVs and all three original PBR materials.
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
output=ROOT/'assets/source/max-helmet/base.glb'
bpy.ops.export_scene.gltf(filepath=str(output),export_format='GLB',use_selection=True,export_materials='EXPORT',export_image_format='JPEG',export_jpeg_quality=90,export_extras=True)
print('EXPORTED',output,output.stat().st_size)
