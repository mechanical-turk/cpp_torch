"""Extreme handmade plasticine look study; isolated from approved final-v8."""
import os
os.environ['CYCLES_METAL_DISABLE_BINARY_ARCHIVES']='1'
import bpy,math,json,argparse,sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=argparse.ArgumentParser();P.add_argument('--final',action='store_true');a=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
O=Path(__file__).resolve().parent;W=O/'_render';W.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(O.parent/'final-v8/false-sharing-final.blend'))
s=bpy.context.scene;s.frame_set(551);bpy.context.view_layer.update()
MODEL=bpy.data.collections['01 • Clay models'];HUD=bpy.data.collections['02 • Code and results'];ground=s.objects['Continuous clay studio ground']
# Freeze this single pose before changing shaders or sculpting shared geometry.
for blocks in [bpy.data.objects,bpy.data.materials,bpy.data.curves,bpy.data.metaballs]:
 for b in blocks:
  if hasattr(b,'animation_data_clear'):b.animation_data_clear()
  if hasattr(b,'node_tree') and b.node_tree:b.node_tree.animation_data_clear()
visible=[o for o in MODEL.all_objects if not o.hide_render]
materials={slot.material for o in visible if o.type in ['MESH','META'] for slot in o.material_slots if slot.material}

def clay(m):
 nt=m.node_tree;n=nt.nodes;l=nt.links
 bs=next(x for x in n if x.type=='BSDF_PRINCIPLED');base=tuple(bs.inputs['Base Color'].default_value)
 # Replace the noisy/sandy bump stack with kneading and isolated finger impressions.
 for socket in ['Normal','Roughness','Base Color']:
  for link in list(bs.inputs[socket].links):l.remove(link)
 tex=n.new('ShaderNodeTexCoord');tex.label='Stable local sculpt coordinates'
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=7.5;noise.inputs['Detail'].default_value=2.3;noise.inputs['Roughness'].default_value=.48;l.new(tex.outputs['Generated'],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=tuple(c*.76 for c in base[:3])+(1,);ramp.color_ramp.elements[1].color=tuple(min(1,c*1.18+.002) for c in base[:3])+(1,);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color'])
 rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.72;rough.inputs['To Max'].default_value=.87;l.new(noise.outputs['Fac'],rough.inputs['Value']);l.new(rough.outputs[0],bs.inputs['Roughness'])
 bs.inputs['Coat Weight'].default_value=0;bs.inputs['Sheen Weight'].default_value=.08;bs.inputs['Specular IOR Level'].default_value=.24;bs.inputs['Subsurface Weight'].default_value=.045;bs.inputs['Subsurface Radius'].default_value=(.7,.38,.2);bs.inputs['Subsurface Scale'].default_value=.12
 def mathnode(op,x,y=None):
  node=n.new('ShaderNodeMath');node.operation=op
  if hasattr(x,'is_output'):l.new(x,node.inputs[0])
  else:node.inputs[0].default_value=x
  if y is not None:
   if hasattr(y,'is_output'):l.new(y,node.inputs[1])
   else:node.inputs[1].default_value=y
  return node.outputs[0]
 height=mathnode('MULTIPLY',noise.outputs['Fac'],.7)
 for cx,cy,rotation in [(.83,.76,.38),(.13,.15,-.52)]:
  sub=n.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';l.new(tex.outputs['Generated'],sub.inputs[0]);sub.inputs[1].default_value=(cx,cy,0)
  mapping=n.new('ShaderNodeVectorRotate');mapping.rotation_type='AXIS_ANGLE';mapping.inputs['Axis'].default_value=(0,0,1);mapping.inputs['Angle'].default_value=rotation;l.new(sub.outputs[0],mapping.inputs['Vector'])
  ellipse=n.new('ShaderNodeVectorMath');ellipse.operation='MULTIPLY';ellipse.inputs[1].default_value=(1,1.42,0);l.new(mapping.outputs[0],ellipse.inputs[0])
  length=n.new('ShaderNodeVectorMath');length.operation='LENGTH';l.new(ellipse.outputs[0],length.inputs[0]);r=length.outputs['Value']
  mask=n.new('ShaderNodeMapRange');mask.interpolation_type='SMOOTHERSTEP';mask.clamp=True;mask.inputs['From Min'].default_value=.075;mask.inputs['From Max'].default_value=.245;mask.inputs['To Min'].default_value=1;mask.inputs['To Max'].default_value=0;l.new(r,mask.inputs[0])
  warp=n.new('ShaderNodeTexNoise');warp.inputs['Scale'].default_value=18;warp.inputs['Detail'].default_value=1.5;l.new(tex.outputs['Generated'],warp.inputs[0])
  wave=mathnode('SINE',mathnode('ADD',mathnode('MULTIPLY',r,245),mathnode('MULTIPLY',warp.outputs['Fac'],4.6)))
  wave=mathnode('MULTIPLY',wave,.19);wave=mathnode('SUBTRACT',wave,.22)
  separate=n.new('ShaderNodeSeparateXYZ');l.new(mapping.outputs[0],separate.inputs[0])
  partial=n.new('ShaderNodeMapRange');partial.interpolation_type='SMOOTHERSTEP';partial.inputs['From Min'].default_value=-.045;partial.inputs['From Max'].default_value=.065;l.new(separate.outputs['X'],partial.inputs[0]);partial.clamp=True
  wave=mathnode('MULTIPLY',wave,partial.outputs[0])
  height=mathnode('ADD',height,mathnode('MULTIPLY',wave,mask.outputs[0]))
 bump=n.new('ShaderNodeBump');bump.label='Pressed fingerprints and shallow thumb dents';bump.inputs['Strength'].default_value=.66;bump.inputs['Distance'].default_value=.068;l.new(height,bump.inputs['Height'])
 fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=105;fine.inputs['Detail'].default_value=2;l.new(tex.outputs['Generated'],fine.inputs[0])
 grain=n.new('ShaderNodeBump');grain.inputs['Strength'].default_value=.20;grain.inputs['Distance'].default_value=.011;l.new(fine.outputs['Fac'],grain.inputs['Height']);l.new(bump.outputs[0],grain.inputs['Normal']);l.new(grain.outputs[0],bs.inputs['Normal'])
 m['look_study']='Worked plasticine: pigment marbling, shallow thumb impressions, curved ridges, fine grain'
for m in materials:clay(m)
# Keep family meshes shared: one canonical hand-sculpt per existing mesh.
meshes={}
for o in visible:
 if o.type!='MESH':continue
 if 'shell' in o.name:
  if o.data.name not in meshes:
   old=o.data;mesh=old.copy();mesh.name=old.name+' • thumb-shaped master';meshes[old.name]=mesh
   for v in mesh.vertices:
    x,y,z=v.co;h=max(0,min(1,z/1.0))
    v.co.x=x*(1+.022*math.sin(5.8*y+.4)*h+.011*math.sin(9*z+2*x))
    v.co.y=y*(1+.019*math.sin(6.3*x+.8)*h)
    v.co.z=z+h*(.04*math.sin(6.5*x+1)+.022*math.sin(8*y)+.018*math.sin(15*x+6*y))
  o.data=meshes[o.data.name]
  for mod in o.modifiers:
   if mod.type=='DISPLACE':mod.strength=.052
 # Dashes share one gently kneaded canonical mesh, preserving pulse layout.
 if ' dash ' in o.name:
  if o.data.name not in meshes:
   old=o.data;mesh=old.copy();mesh.name='Pinched clay path master';meshes[old.name]=mesh
   for v in mesh.vertices:
    x,y,z=v.co;v.co.x*=1+.045*math.sin(y*5);v.co.z*=1+.04*math.cos(x*5+y*3)
  o.data=meshes[o.data.name]
# Preserve crisp shadow shapes and add grazing light for shallow fingerprints.
key=s.objects['Studio warm key'];key.data.energy=1650;key.data.size=2.2
s.objects['Cool edge strip'].data.energy=780;s.objects['Cool edge strip'].data.size=1.1
s.objects['Restrained neutral front fill'].data.energy=140
# Ground retains its approved continuous gradient; reduce sandy microtexture.
for node in ground.active_material.node_tree.nodes:
 if node.type=='AMBIENT_OCCLUSION':node.samples=8
s.render.resolution_x=2160;s.render.resolution_y=2300;s.render.resolution_percentage=100 if a.final else 50
s.render.use_border=False;s.render.use_crop_to_border=False;s.render.film_transparent=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.image_settings.compression=25
s.cycles.samples=192 if a.final else 48;s.cycles.adaptive_threshold=.007 if a.final else .018;s.cycles.use_denoising=True;s.cycles.use_animated_seed=False;s.cycles.seed=0;s.render.use_persistent_data=False;s.camera.data.dof.use_dof=False;s.render.use_motion_blur=False
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.kernel_optimization_level='OFF';prefs.metalrt='OFF';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU'
# Audit unchanged essential lettering against the supplied template rectangle.
bpy.context.view_layer.update();bounds=[]
for o in s.objects:
 if o.type=='FONT' and not o.hide_render:
  coords=[world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for v in o.bound_box]
  if coords:bounds.append((o.name,[min(v.x for v in coords)*2160,min(1-v.y for v in coords)*2300,max(v.x for v in coords)*2160,max(1-v.y for v in coords)*2300]))
errors=[(name,b) for name,b in bounds if b[0]<120 or b[1]<440 or b[2]>1872 or b[3]>2300]
assert not errors,errors
(O/'verification.json').write_text(json.dumps({'resolution':[2160,2300],'source_frame':551,'essential_text_safe_zone_errors':errors,'canonical_hand_sculpt_meshes':len(meshes),'study_only':True},indent=2))
if a.final:bpy.ops.wm.save_as_mainfile(filepath=str(O/'extreme-clay-study.blend'))
# Mesh glyphs once to avoid the known animated FONT tessellation bug.
bpy.ops.object.select_all(action='DESELECT')
fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
bpy.context.view_layer.objects.active=fonts[0];bpy.ops.object.convert(target='MESH')
tag='final' if a.final else 'preview'
HUD.hide_render=True;s.render.image_settings.color_mode='RGB';s.render.filepath=str(W/(tag+'-plate.png'));bpy.ops.render.render(write_still=True)
MODEL.hide_render=True;HUD.hide_render=False;ground.hide_render=True;s.cycles.device='CPU';s.cycles.samples=64;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.render.filepath=str(W/(tag+'-code.png'));bpy.ops.render.render(write_still=True)
print('STUDY_RENDER_COMPLETE',tag,flush=True)
