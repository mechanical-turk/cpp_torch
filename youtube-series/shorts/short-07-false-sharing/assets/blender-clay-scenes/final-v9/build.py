"""Apply the approved sculpted-clay study to the complete revision-8 timeline.

Native meshes, shaders and lighting match extreme-clay-study-v2; animation,
inline code, scene timing, semantic palette and framing are preserved.
"""
import os
os.environ['CYCLES_METAL_DISABLE_BINARY_ARCHIVES']='1'
import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;W=O/'_render';W.mkdir(exist_ok=True)
SOURCE=O.parent/'final-v8/false-sharing-final.blend'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));s=bpy.context.scene
MODEL=bpy.data.collections['01 • Clay models'];HUD=bpy.data.collections['02 • Code and results'];ground=s.objects['Continuous clay studio ground']
# Capture every ownership color before replacing procedural material nodes.
visible=list(MODEL.all_objects)
materials={slot.material for o in visible if o.type in ['MESH','META'] for slot in o.material_slots if slot.material}
animated_colors={}
for m in materials:
 if m.node_tree and m.node_tree.animation_data and m.node_tree.animation_data.action:
  bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
  poses={}
  for f in range(1,865,2):
   s.frame_set(f);poses[f]=tuple(bs.inputs['Base Color'].default_value)
  animated_colors[m.name]=poses
s.frame_set(551);bpy.context.view_layer.update()
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
 ramp=n.new('ShaderNodeValToRGB');ramp.name='Clay pigment variation';ramp.color_ramp.elements[0].color=tuple(v*.82 for v in base[:3])+(1,);ramp.color_ramp.elements[1].color=tuple(min(1,v*1.13+.001) for v in base[:3])+(1,);l.new(pigment.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color'])
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

# The pigment ramp must follow ownership too: a static ramp would silently
# freeze the tray's visible color despite the original Base Color animation.
for name,poses in animated_colors.items():
 m=bpy.data.materials[name];ramp=m.node_tree.nodes['Clay pigment variation'].color_ramp
 for f,color in poses.items():
  ramp.elements[0].color=tuple(v*.82 for v in color[:3])+(1,)
  ramp.elements[1].color=tuple(min(1,v*1.13+.001) for v in color[:3])+(1,)
  for element in ramp.elements:element.keyframe_insert(data_path='color',frame=f)
 for layer in m.node_tree.animation_data.action.layers:
  for strip in layer.strips:
   for slot in m.node_tree.animation_data.action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
assert all(n.type!='TEX_WAVE' and not (n.type=='MATH' and n.operation in ['SINE','COSINE']) for m in materials for n in m.node_tree.nodes)
s.render.resolution_x=2160;s.render.resolution_y=2300;s.render.resolution_percentage=100
s.render.use_border=False;s.render.use_crop_to_border=False;s.render.film_transparent=False
s.cycles.samples=96;s.cycles.adaptive_threshold=.007;s.cycles.use_denoising=True;s.cycles.use_animated_seed=False;s.cycles.seed=0
s.render.use_persistent_data=False;s.camera.data.dof.use_dof=False;s.render.use_motion_blur=False
WIDTH,HEIGHT,END=2160,2300,864;cam=s.camera
def visible_bounds(obs):
 vs=[world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for o in obs if not o.hide_render for v in o.bound_box]
 if not vs:return None
 return [min(v.x for v in vs)*WIDTH,min(1-v.y for v in vs)*HEIGHT,max(v.x for v in vs)*WIDTH,max(1-v.y for v in vs)*HEIGHT]
prior=json.loads((O.parent/'final-v8/scene-verification.json').read_text())
manifest=json.loads((O.parent/'final-v8/scene-manifest.json').read_text());manifest.update(revision=9,approved_reference=str(O.parent/'extreme-clay-study-v2/extreme-clay-study.blend'),aesthetic='Approved hand-sculpted plasticine, nonperiodic smears, rolled rims and thumb presses');(O/'scene-manifest.json').write_text(json.dumps(manifest,indent=2))
val=bpy.data.materials['V8 arrow reveal'].node_tree.nodes['Draw progress']
overall={'hud':[WIDTH,HEIGHT,0,0],'labels':[WIDTH,HEIGHT,0,0],'model':[WIDTH,HEIGHT,0,0]};violations=[]
maps={'model':{},'hud':{}};seen={'model':{},'hud':{}}
for f in range(1,END+1):
    s.frame_set(f);bpy.context.view_layer.update()
    groups={'hud':[o for o in HUD.objects if o.type in {'FONT','CURVE'}],
            'labels':[o for o in MODEL.objects if o.type=='FONT'],
            'model':[o for o in MODEL.objects if o.type in {'FONT','MESH','CURVE'}]}
    for name,obs in groups.items():
        b=visible_bounds(obs)
        if not b:continue
        overall[name]=[min(overall[name][0],b[0]),min(overall[name][1],b[1]),max(overall[name][2],b[2]),max(overall[name][3],b[3])]
        safe=(180,480,1812,1180) if name=='hud' else (120,440,1872,2260) if name=='labels' else (0,990,2160,2300)
        if b[0]<safe[0] or b[1]<safe[1] or b[2]>safe[2] or b[3]>safe[3]:violations.append((f,name,b))
    for tag,coll in [('model',MODEL),('hud',HUD)]:
        state=[]
        for o in coll.objects:
            if o.hide_render or o.type not in {'FONT','MESH','CURVE','META'}:continue
            state.append((o.name,tuple(round(v,6) for row in o.matrix_world for v in row)))
            if o.type=='META':state.append(tuple(tuple(round(v,5) for v in e.co)+(round(e.radius,5),) for e in o.data.elements))
        if tag=='model':state.append(tuple(tuple(bpy.data.materials[n].node_tree.nodes['Clay pigment variation'].color_ramp.elements[0].color) for n in sorted(animated_colors)))
        else:state.append(round(val.outputs[0].default_value,6))
        digest=hashlib.sha256(repr(state).encode()).hexdigest();maps[tag][str(f)]=seen[tag].setdefault(digest,f)
report={'bounds':overall,'frame_maps':maps,'unique_states':{k:len(v) for k,v in seen.items()},'split_y':990,
        'violations':violations[:30],'violation_count':len(violations),'events':prior['events'],'writes':prior['writes'],
        'same_canonical_trays':s.objects['Tray • shell'].data==s.objects['Independent line • Tray • shell'].data,
        'native_resolution':[WIDTH,HEIGHT],'no_post_render_scaling':True,'template_scale':2}
(O/'scene-verification.json').write_text(json.dumps(report,indent=2));print('AUDIT',json.dumps({k:v for k,v in report.items() if k!='frame_maps'}),flush=True)
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'false-sharing-final.blend'))
assert not violations, 'Safe-zone/layout audit failed; inspect scene-verification.json before rendering.'
