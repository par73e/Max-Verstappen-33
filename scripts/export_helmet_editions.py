"""Export the baked livery reconstructions on the attributed Maubian geometry."""
import bpy,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for edition in ['season-2023','zandvoort-2024']:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.gltf(filepath=str(ROOT/'assets/source/max-helmet/bake-base.glb'))
 for obj in bpy.context.scene.objects:
  if obj.type!='MESH':continue
  mat=obj.data.materials[0];bsdf=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
  if obj.name=='helmet':
   for key,value in [('Roughness',.34),('Metallic',.02),('Alpha',1),('Transmission Weight',0)]:
    for link in list(bsdf.inputs[key].links):mat.node_tree.links.remove(link)
    bsdf.inputs[key].default_value=value
   for link in list(bsdf.inputs['Normal'].links):mat.node_tree.links.remove(link)
   tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/'public/max/materials'/(edition+'-helmet.jpg')))
   mat.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
  elif obj.name=='glass':
   # Export an opaque coated visor. Its source blue color/opacity and packed
   # metalness maps are unused at runtime; omit them instead of shipping 3 MB.
   for key,value in [('Base Color',(.82,.47,.12,1)),('Roughness',.22),('Metallic',1),('Alpha',1),('Transmission Weight',0)]:
    for link in list(bsdf.inputs[key].links):mat.node_tree.links.remove(link)
    bsdf.inputs[key].default_value=value
  obj['attribution']='Helmet Redbull - Max Verstappen by Maubian / CC BY 4.0'
  obj['adaptation']='Photographic livery reconstruction, '+edition
 path=ROOT/'public/gl/models'/(edition+'.glb')
 bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',export_materials='EXPORT',export_image_format='JPEG',export_jpeg_quality=95,export_extras=True)
 data=path.read_bytes();length=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+length]);tail=data[20+length:]
 doc['asset']['extras']={'author':'Maubian','source':'https://skfb.ly/pEDBZ','license':'CC-BY-4.0','licenseUrl':'https://creativecommons.org/licenses/by/4.0/','modifications':'Normalized geometry and reconstructed '+edition+' UV material from attributed photographs. Approximation, not an official scan.'}
 js=json.dumps(doc,separators=(',',':')).encode();js+=b' '*((-len(js))%4);path.write_bytes(struct.pack('<III',0x46546c67,2,20+len(js)+len(tail))+struct.pack('<II',len(js),0x4e4f534a)+js+tail)
 print('EDITION',edition,path.stat().st_size,flush=True)
