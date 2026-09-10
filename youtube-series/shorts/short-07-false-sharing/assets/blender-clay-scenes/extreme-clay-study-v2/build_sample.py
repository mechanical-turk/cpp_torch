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
 output=next(x for x in n if x.type=='OUTPUT_MATERIAL')
 for x in list(n):
  if x not in [bs,output]:n.remove(x)
 for link in list(l):l.remove(link)
 l.new(bs.outputs[0],output.inputs['Surface'])
 coord=n.new('ShaderNodeTexCoord')
 pigment=n.new('ShaderNodeTexNoise');pigment.inputs['Scale'].default_value=3.8; pigment.inputs['Detail'].default_value=2; l.new(coord.outputs['Generated'],pigment.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=tuple(v*.82 for v in base[:3])+(1,);ramp.color_ramp.elements[1].color=tuple(min(1,v*1.13+.001) for v in base[:3])+(1,);l.new(pigment.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color'])
 rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.68;rough.inputs['To Max'].default_value=.84;l.new(pigment.outputs['Fac'],rough.inputs[0]);l.new(rough.outputs[0],bs.inputs['Roughness'])
 bs.inputs['Coat Weight'].default_value=0;bs.inputs['Sheen Weight'].default_value=.08;bs.inputs['Specular IOR Level'].default_value=.27;bs.inputs['Subsurface Weight'].default_value=.035;bs.inputs['Subsurface Radius'].default_value=(.7,.38,.2);bs.inputs['Subsurface Scale'].default_value=.08
 # Irregular clay smears: nonperiodic stretched noise, with no rings or waves.
 stretch=n.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(1.2,4.5,1.5);l.new(coord.outputs['Object'],stretch.inputs[0])
 smear=n.new('ShaderNodeTexNoise');smear.inputs['Scale'].default_value=4;smear.inputs['Detail'].default_value=2.4;smear.inputs['Roughness'].default_value=.45;l.new(stretch.outputs[0],smear.inputs[0])
 bump=n.new('ShaderNodeBump');bump.label='Nonperiodic worked-clay smears';bump.inputs['Strength'].default_value=.28;bump.inputs['Distance'].default_value=.019;l.new(smear.outputs['Fac'],bump.inputs['Height'])
 fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=95;fine.inputs['Detail'].default_value=2;l.new(coord.outputs['Object'],fine.inputs[0])
 grain=n.new('ShaderNodeBump');grain.inputs['Strength'].default_value=.17;grain.inputs['Distance'].default_value=.008;l.new(fine.outputs['Fac'],grain.inputs['Height']);l.new(bump.outputs[0],grain.inputs['Normal']);l.new(grain.outputs[0],bs.inputs['Normal'])
 m['look_study']='No radial patterns: pigment variation, nonperiodic smears and fine grain'
for m in materials:clay(m)

# Dense, evenly spaced rounded-rectangle rings make actual thumb dents possible
# along the straight runs as well as the corners. One shared master per family.
def contour(w,d,r,N=128):
 points=[]
 for x,y,a in [(w/2-r,d/2-r,0),(-w/2+r,d/2-r,90),(-w/2+r,-d/2+r,180),(w/2-r,-d/2+r,270)]:
  for j in range(24):
   angle=math.radians(a+j*90/24);points.append(Vector((x+r*math.cos(angle),y+r*math.sin(angle))))
 lengths=[0.0]
 for i in range(len(points)):lengths.append(lengths[-1]+(points[(i+1)%len(points)]-points[i]).length)
 out=[];seg=0
 for i in range(N):
  dist=lengths[-1]*i/N
  while lengths[seg+1]<dist:seg+=1
  u=(dist-lengths[seg])/(lengths[seg+1]-lengths[seg]);out.append(points[seg].lerp(points[(seg+1)%len(points)],u))
 return out

def sculpted_shell(name,rings,is_tray=False):
 vertices=[];N=128
 # Uneven, widely spaced presses, not a repeating scallop pattern.
 presses=[(.065,.028,.10),(.235,.036,.055),(.42,.03,.13),(.705,.025,.085),(.865,.037,.07)]
 maxz=max(v[0] for v in rings)
 for z,w,d,r in rings:
  for i,p in enumerate(contour(w,d,r,N)):
   x,y=p;t=i/N;top=math.exp(-((z-maxz)/.28)**2);press=0
   for center,radius,depth in presses:
    dt=min(abs(t-center),1-abs(t-center));press+=depth*math.exp(-(dt/radius)**2)
   # Thumb compression lowers the crown and displaces a little clay outward.
   z1=z-press*top
   radial=Vector((x,y));radial.normalize()
   spread=press*top*.25
   x+=radial.x*spread;y+=radial.y*spread
   # Broad asymmetry and a few real soft folds on the exposed outer wall.
   x+=.021*math.sin(y*2.3+.4)*min(1,z/.5)
   y+=.020*math.sin(x*2.8+1.0)*min(1,z/.5)
   if y < -d*.39:
    for center in ([-1.99,1.87] if is_tray else [-1.03,.98]):
     groove=x-center+.2*(z-.65)
     gate=math.exp(-((z-.64)/.28)**2)
     y+=gate*(.030*math.exp(-(groove/.11)**2)-.012*math.exp(-((groove+.11)/.10)**2))
   vertices.append((x,y,z1))
 faces=[tuple(reversed(range(N)))]
 for j in range(len(rings)-1):
  for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
 for face in mesh.polygons:face.use_smooth=True
 return mesh
counter_rings=[(.025,2.12,2.72,.42),(.08,2.37,2.98,.48),(.24,2.49,3.11,.51),(.57,2.43,3.07,.49),(.88,2.47,3.13,.49),(1.07,2.54,3.17,.50),(1.23,2.43,3.08,.46),(1.30,2.20,2.86,.41),(1.25,2.01,2.68,.36),(1.12,1.89,2.52,.30),(.91,1.855,2.495,.285)]
tray_rings=[(.025,4.45,2.97,.43),(.09,4.66,3.16,.48),(.22,4.73,3.23,.49),(.48,4.63,3.14,.48),(.75,4.66,3.17,.46),(.92,4.73,3.24,.46),(1.055,4.59,3.09,.42),(1.10,4.41,2.94,.37),(1.035,4.23,2.77,.32),(.91,4.13,2.68,.29),(.72,4.12,2.67,.28),(.23,4.13,2.67,.27)]
meshes={}
for o in visible:
 if o.type!='MESH':continue
 if 'shell' in o.name:
  key=o.data.name
  if key not in meshes:
   tray='Tray' in o.name
   master=sculpted_shell(('Hand-rolled tray' if tray else 'Hand-rolled counter')+' master',tray_rings if tray else counter_rings,tray)
   for material in o.data.materials:master.materials.append(material)
   meshes[key]=master
  # Preserve the actual object-linked worker color during data replacement.
  slots=[(slot.link,slot.material) for slot in o.material_slots]
  o.data=meshes[key]
  for slot,(kind,material) in zip(o.material_slots,slots):slot.link=kind;slot.material=material
  for modifier in list(o.modifiers):o.modifiers.remove(modifier)
  sub=o.modifiers.new('Soft sculpted roll','SUBSURF');sub.levels=2;sub.render_levels=2
 if ' dash ' in o.name:
  key=o.data.name
  if key not in meshes:
   mesh=o.data.copy();mesh.name='Pinched path master'
   for v in mesh.vertices:
    x,y,z=v.co;pinch=math.exp(-((y-.15)/.3)**2);v.co.x*=1-.095*pinch;v.co.z*=1+.08*pinch
   meshes[key]=mesh
  o.data=meshes[key]
# Raised, softly rounded clay lettering on physical faces only. Code is untouched.
for o in visible:
 if o.type=='FONT':
  o.data=o.data.copy();o.data.extrude=.009;o.data.bevel_depth=.005;o.data.bevel_resolution=4
assert s.objects['Counter a • shell'].data==s.objects['Counter b • shell'].data
assert s.objects['Tray • shell'].data==s.objects['Independent line • Tray • shell'].data
# Preserve crisp shadow shapes and add grazing light for real sculpted rolls.
key=s.objects['Studio warm key'];key.data.energy=1650;key.data.size=2.2
s.objects['Cool edge strip'].data.energy=780;s.objects['Cool edge strip'].data.size=1.1
s.objects['Restrained neutral front fill'].data.energy=140
# Ground retains its approved continuous gradient; reduce sandy microtexture.
for node in ground.active_material.node_tree.nodes:
 if node.type=='AMBIENT_OCCLUSION':node.samples=8
s.render.resolution_x=2160;s.render.resolution_y=2300;s.render.resolution_percentage=100 if a.final else 50
s.render.use_border=False;s.render.use_crop_to_border=False;s.render.film_transparent=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.image_settings.compression=25
s.cycles.samples=96 if a.final else 48;s.cycles.adaptive_threshold=.007 if a.final else .018;s.cycles.use_denoising=True;s.cycles.use_animated_seed=False;s.cycles.seed=0;s.render.use_persistent_data=False;s.camera.data.dof.use_dof=False;s.render.use_motion_blur=False
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
(O/'verification.json').write_text(json.dumps({'resolution':[2160,2300],'source_frame':551,'essential_text_safe_zone_errors':errors,'canonical_hand_sculpt_meshes':len(meshes),'study_only':True,'radial_pattern_nodes':False,'linked_family_geometry':True},indent=2))
print('BUILD_READY',len(meshes),flush=True)
assert all(n.type!='TEX_WAVE' and not (n.type=='MATH' and n.operation in ['SINE','COSINE']) for m in materials for n in m.node_tree.nodes)
if a.final:bpy.ops.wm.save_as_mainfile(filepath=str(O/'extreme-clay-study.blend'))
# Mesh glyphs once to avoid the known animated FONT tessellation bug.
bpy.ops.object.select_all(action='DESELECT')
fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
bpy.context.view_layer.objects.active=fonts[0];bpy.ops.object.convert(target='MESH')
tag='final' if a.final else 'preview'
print('RENDER_CLAY',tag,flush=True)
HUD.hide_render=True;s.render.image_settings.color_mode='RGB';s.render.filepath=str(W/(tag+'-plate.png'));bpy.ops.render.render(write_still=True)
MODEL.hide_render=True;HUD.hide_render=False;ground.hide_render=True;s.cycles.device='CPU';s.cycles.samples=64;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.render.filepath=str(W/(tag+'-code.png'));bpy.ops.render.render(write_still=True)
print('STUDY_RENDER_COMPLETE',tag,flush=True)
