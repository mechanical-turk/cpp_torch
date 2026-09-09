import bpy, math, json, argparse, sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
parser=argparse.ArgumentParser(description='Build and render the native Retro Sunset clay still.')
parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
parser.add_argument('--preview',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True);WORK=OUT
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=64 if args.preview else 192;s.cycles.adaptive_threshold=.008;s.cycles.use_denoising=True
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.kernel_optimization_level='OFF';prefs.metalrt='OFF';prefs.get_devices()
    devices=[]
    for d in prefs.devices:d.use=d.type=='METAL';devices.append((d.name,d.type,d.use))
    if any(d[1]=='METAL' for d in devices):s.cycles.device='GPU'
    print('CYCLES_DEVICES',devices,flush=True)
except Exception as e:print('CYCLES_CPU',str(e),flush=True)
s.render.resolution_x=2360;s.render.resolution_y=2352;s.render.resolution_percentage=50 if args.preview else 100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.film_transparent=False
s.view_settings.view_transform='Khronos PBR Neutral';s.view_settings.look='None';s.view_settings.exposure=0
s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.3,.23,.25,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.20
def lin(h):
    a=[int(h[i:i+2],16)/255 for i in (0,2,4)];return tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in a)
def mat(name,h,rough=.67,grain=.10,emission=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*lin(h),1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*lin(h),1);p.inputs['Roughness'].default_value=rough
    p.inputs['Specular IOR Level'].default_value=.26;p.inputs['Metallic'].default_value=0
    if emission:p.inputs['Emission Color'].default_value=(*lin(h),1);p.inputs['Emission Strength'].default_value=emission
    if grain:
        n=m.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=42;n.inputs['Detail'].default_value=2
        b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=grain;b.inputs['Distance'].default_value=.014
        coord=m.node_tree.nodes.new('ShaderNodeTexCoord');m.node_tree.links.new(coord.outputs['Object'],n.inputs['Vector'])
        m.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs[0],p.inputs['Normal'])
        soft=m.node_tree.nodes.new('ShaderNodeTexNoise');soft.inputs['Scale'].default_value=3.5;soft.inputs['Detail'].default_value=3
        m.node_tree.links.new(coord.outputs['Object'],soft.inputs['Vector'])
        tones=m.node_tree.nodes.new('ShaderNodeValToRGB');tones.color_ramp.elements[0].color=tuple(c*.83 for c in lin(h))+(1,);tones.color_ramp.elements[1].color=tuple(c*1.06 for c in lin(h))+(1,)
        m.node_tree.links.new(soft.outputs['Fac'],tones.inputs[0]);m.node_tree.links.new(tones.outputs[0],p.inputs['Base Color'])
    return m
def paint(name,h):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*lin(h),1)
    o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs['Surface']);return m
gold=mat('Golden sculpted clay','F7A71B',.65,.23);blue=mat('Cobalt clay cards','2558BE',.67,.18)
navy=mat('Plum navy clay cradle','40485E',.67,.22);brown=mat('Amber recessed clay face','532707',.84,.18,.02)
dark=mat('Recessed history plaque','211728',.79,.09,.04);ivory=mat('Ivory raised clay letters','FFF0D5',.64,.05,.22)
coral=paint('Coral timing','FF8D6C');mint=paint('Mint timing','7AF5C4');cream=mat('Ivory clay arrow','F5DCAA',.61,.07)

def points(w,d,r,n=12):
    p=[]
    for x,y,a in [(w/2-r,d/2-r,0),(-w/2+r,d/2-r,90),(-w/2+r,-d/2+r,180),(w/2-r,-d/2+r,270)]:
        for j in range(n):
            t=math.radians(a+j*90/n);p.append((x+r*math.cos(t),y+r*math.sin(t)))
    return p
def loft(name,rings,material,parent=None,sub=2,cap_bottom=True,cap_top=False):
    verts=[]
    for z,w,d,r in rings:verts += [(x,y,z) for x,y in points(w,d,r)]
    N=48;faces=[]
    if cap_bottom:faces.append(tuple(reversed(range(N))))
    for k in range(len(rings)-1):
        for i in range(N):j=(i+1)%N;faces.append((k*N+i,k*N+j,(k+1)*N+j,(k+1)*N+i))
    if cap_top:faces.append(tuple(range((len(rings)-1)*N,len(rings)*N)))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);s.collection.objects.link(o);o.data.materials.append(material)
    if parent:o.parent=parent
    for p in mesh.polygons:p.use_smooth=True
    if sub:m=o.modifiers.new('Sculpted continuous curvature','SUBSURF');m.levels=sub;m.render_levels=sub
    return o
def rounded(name,w,d,h,r,material,parent=None):
    # Closely supported top/bottom rings keep the recessed faces broad and smooth.
    return loft(name,[(-h/2,w-.035,d-.035,max(.03,r-.015)),(-h/2+.009,w,d,r),(h/2-.009,w,d,r),(h/2,w-.035,d-.035,max(.03,r-.015))],material,parent,1,True,True)
def empty(name):o=bpy.data.objects.new(name,None);s.collection.objects.link(o);return o
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf');bold=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf');heavy=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Black.ttf')
def text(name,body,size,material,parent=None,font_=font):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.size=size;d.font=font_;d.align_x='CENTER';d.resolution_u=12
    if material==ivory:d.extrude=.0018;d.bevel_depth=.0006;d.bevel_resolution=3
    o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.data.materials.append(material)
    if parent:o.parent=parent
    return o

score_groups=[];history_groups=[];card_master=None
score_meshes=[];tray_meshes=[]
for i,value in enumerate([7,2,9]):
    parent=empty(f'Score {value} assembly');score_groups.append(parent);parent.location=((i-1)*2.44,-5.3,0)
    if i==0:
        shell=loft('Score • monolithic soft clay shell',[(.025,1.99,2.64,.38),(.10,2.22,2.87,.43),(.28,2.37,3.01,.46),(.71,2.40,3.04,.46),(1.02,2.35,3.01,.42),(1.135,2.23,2.87,.37),(1.16,2.01,2.65,.33),(1.095,1.88,2.52,.29),(.91,1.85,2.49,.28)],gold,parent,2)
        face=rounded('Score • deep amber inset',1.855,2.495,.040,.285,brown,parent);face.location.z=.91
        score_meshes=[shell,face]
    else:
        for master in score_meshes:
            o=master.copy();o.data=master.data;s.collection.objects.link(o);o.parent=parent;o.name=master.name+f' {value}'
    label=text(f'Score {value} label','score',.64,ivory,parent);label.location=(0,.63,.945)
    numeral=text(f'Score {value} numeral',str(value),1.72,ivory,parent,bold);numeral.location=(0,-.80,.945)

    hp=empty(f'History {i} assembly');history_groups.append(hp);hp.location=((i-1)*3.16,-1.5,0)
    if i==0:
        tray=loft('History • continuous rounded cradle',[(.025,2.90,2.30,.35),(.12,3.10,2.54,.36),(.40,3.17,2.62,.36),(1.30,3.16,2.62,.33),(1.50,3.05,2.55,.30),(1.56,2.87,2.40,.25),(1.515,2.69,2.23,.22),(1.36,2.65,2.19,.20),(.32,2.61,2.15,.18)],navy,hp,2)
        plaque=rounded('History • front inset plaque',2.27,.96,.035,.19,dark,hp);plaque.rotation_euler.x=math.radians(90);plaque.location=(0,-1.328,.82)
        tray_meshes=[tray,plaque]
    else:
        for master in tray_meshes:
            o=master.copy();o.data=master.data;s.collection.objects.link(o);o.parent=hp;o.name=master.name+f' {i}'
    for j in range(15):
        if card_master is None:
            # Tall broad cards rise visibly out of the cradle; shoulders are smoothly rounded.
            bpy.ops.mesh.primitive_cube_add(size=1);o=bpy.context.object;o.name='History 0 • card 01';o.dimensions=(.171,1.82,1.63)
            bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
            bevel=o.modifiers.new('Rounded card edges','BEVEL');bevel.width=.071;bevel.segments=8
            normal=o.modifiers.new('Soft card normals','WEIGHTED_NORMAL');normal.keep_sharp=True
            for p in o.data.polygons:p.use_smooth=True
            o.data.materials.append(blue);card_master=o
        else:o=card_master.copy();o.data=card_master.data;s.collection.objects.link(o)
        o.name=f'History {i} • card {j+1:02}';o.parent=hp;o.location=((j-7)*.174,.18,1.22)
    label=text(f'History {i} label','history',.70,ivory,hp);label.rotation_euler.x=math.radians(90);label.location=(0,-1.352,.60)

# Hand-tinted clay: ochre in the thicker body, sunny gold along the rolled lip.
gn=gold.node_tree.nodes;gl=gold.node_tree.links;gp=gn.get('Principled BSDF')
gtc=gn.new('ShaderNodeTexCoord');gsep=gn.new('ShaderNodeSeparateXYZ');gl.new(gtc.outputs['Generated'],gsep.inputs[0])
gr=gn.new('ShaderNodeValToRGB');gr.color_ramp.interpolation='EASE'
gr.color_ramp.elements[0].position=0;gr.color_ramp.elements[0].color=(*lin('883701'),1)
gr.color_ramp.elements[1].position=.90;gr.color_ramp.elements[1].color=(*lin('FFB522'),1)
ge=gr.color_ramp.elements.new(.52);ge.color=(*lin('C77508'),1)
gl.new(gsep.outputs['Z'],gr.inputs[0]);gl.new(gr.outputs[0],gp.inputs['Base Color'])
# A very small sculptural variation breaks mathematically perfect edges.
clayform=bpy.data.textures.new('Subtle hand-shaped clay variation',type='CLOUDS');clayform.noise_scale=.32;clayform.noise_depth=1
for assembly in score_groups+history_groups:
    for obj in assembly.children:
        if obj.type=='MESH' and ('monolithic' in obj.name or 'continuous rounded' in obj.name):
            deform=obj.modifiers.new('Soft handmade contour','DISPLACE');deform.texture=clayform;deform.strength=.021;deform.mid_level=.5;deform.texture_coords='GLOBAL'
# Camera and the physical backdrop are new; no old animation geometry is reused.
cd=bpy.data.cameras.new('Reference camera');cam=bpy.data.objects.new('Reference camera',cd);s.collection.objects.link(cam)
cam.location=(0,-22,22);cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='PERSP';cd.lens=80;cd.sensor_width=36;cd.ortho_scale=14;s.camera=cam
unit=14/2360
def pixel(x,y,z=-7):return Vector(((x/2360-.5)*14,(.5-y/2352)*2352*unit,z))
def group_bounds(group):
    coords=[]
    for o in group.children:
        if o.type not in {'MESH','FONT','CURVE'}:continue
        coords += [world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for v in o.bound_box]
    return [min(p.x for p in coords)*2360,min(1-p.y for p in coords)*2352,max(p.x for p in coords)*2360,max(1-p.y for p in coords)*2352]
bpy.context.view_layer.update()
# Align the two model rows with the reference image's measured vertical centers.
# Match the reference's screen-space sizes while retaining real perspective.
for groups,target,width,centers in [(score_groups,990/1254*2352,405,[416/1254*2360,634/1254*2360,852/1254*2360]),(history_groups,700/1254*2352,525,[350/1254*2360,630/1254*2360,913/1254*2360])]:
    for g,cx in zip(groups,centers):
        for iteration in range(5):
            bpy.context.view_layer.update();b=group_bounds(g);g.scale*=width/(b[2]-b[0]);bpy.context.view_layer.update();b=group_bounds(g)
            dx=cx-(b[0]+b[2])/2;dy=target-(b[1]+b[3])/2
            g.location.x+=.1;bpy.context.view_layer.update();bx=group_bounds(g);g.location.x-=.1
            g.location.y+=.1;bpy.context.view_layer.update();by=group_bounds(g);g.location.y-=.1
            g.location.x+=dx/(((bx[0]+bx[2])-(b[0]+b[2]))/.2)
            g.location.y+=dy/(((by[1]+by[3])-(b[1]+b[3]))/.2)
        bpy.context.view_layer.update()

# Match the deeper pillowy sidewalls of the hero's score tiles.
for g in score_groups:
    g.scale.z*=1.30
    bpy.context.view_layer.update();b=group_bounds(g);target=990/1254*2352
    g.location.y+=.1;bpy.context.view_layer.update();by=group_bounds(g);g.location.y-=.1
    g.location.y+=(target-(b[1]+b[3])/2)/(((by[1]+by[3])-(b[1]+b[3]))/.2)
bpy.context.view_layer.update()
ground=mat('Textured Retro Sunset ground','9E4027',.89,.30,.10)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.025));floor=bpy.context.object;floor.name='Continuous clay studio ground';floor.data.materials.append(ground)
nodes=ground.node_tree.nodes;links=ground.node_tree.links;p=nodes.get('Principled BSDF');p.inputs['Specular IOR Level'].default_value=.12
geo=nodes.new('ShaderNodeNewGeometry');xf=nodes.new('ShaderNodeVectorTransform');xf.vector_type='POINT';xf.convert_from='WORLD';xf.convert_to='CAMERA';links.new(geo.outputs['Position'],xf.inputs[0])
sep=nodes.new('ShaderNodeSeparateXYZ');links.new(xf.outputs[0],sep.inputs[0])
def mathnode(op,a=None,b=None):
    n=nodes.new('ShaderNodeMath');n.operation=op
    if a is not None:
        if isinstance(a,(int,float)):n.inputs[0].default_value=a
        else:links.new(a,n.inputs[0])
    if b is not None:
        if isinstance(b,(int,float)):n.inputs[1].default_value=b
        else:links.new(b,n.inputs[1])
    return n.outputs[0]
x=mathnode('DIVIDE',mathnode('ADD',sep.outputs['X'],.3),8.5)
y=mathnode('DIVIDE',mathnode('ADD',sep.outputs['Y'],3.4),6.4)
dist=mathnode('SQRT',mathnode('ADD',mathnode('MULTIPLY',x,x),mathnode('MULTIPLY',y,y)))
ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='EASE'
stops=[(0,'C67653'),(.45,'B35C45'),(.80,'572536'),(1,'2D1223')]
cr=ramp.color_ramp;cr.elements.remove(cr.elements[1]);cr.elements[0].position=0;cr.elements[0].color=(*lin(stops[0][1]),1)
for pos,h in stops[1:]:e=cr.elements.new(pos);e.color=(*lin(h),1)
links.new(dist,ramp.inputs[0])
# Texture the same continuous ground, including its soft ambient contribution.
tex=nodes.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=48;tex.inputs['Detail'].default_value=2;links.new(geo.outputs['Position'],tex.inputs['Vector'])
variation=nodes.new('ShaderNodeMapRange');variation.inputs['From Min'].default_value=0;variation.inputs['From Max'].default_value=1;variation.inputs['To Min'].default_value=.82;variation.inputs['To Max'].default_value=1.12;links.new(tex.outputs['Fac'],variation.inputs['Value'])
mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;links.new(ramp.outputs[0],mix.inputs[1]);links.new(variation.outputs['Result'],mix.inputs[2])
ao=nodes.new('ShaderNodeAmbientOcclusion');ao.inputs['Distance'].default_value=.72;ao.samples=16
contact=nodes.new('ShaderNodeMixRGB');contact.blend_type='MULTIPLY';contact.inputs[0].default_value=.75;links.new(mix.outputs[0],contact.inputs[1]);links.new(ao.outputs['AO'],contact.inputs[2])
links.new(contact.outputs[0],p.inputs['Base Color']);links.new(contact.outputs[0],p.inputs['Emission Color'])
def area(name,loc,target,power,size,color):
    d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    d.energy=power;d.shape='DISK';d.size=size;d.color=color;return o
area('Large warm key',(-4,-3,8),(0,-3,0),1450,4,(1,.87,.73))
area('Cool soft fill',(2,-10,5),(0,-3,1),600,5,(.68,.81,1))
area('Front warm lift',(0,-10,6),(0,-3,.5),180,7,(1,.88,.76))

unit=(7*36/80)/2360
def pixel(x,y,z=-7):return Vector(((x-1180)*unit,(1176-y)*unit,z))
# The result's type is sized from visible glyph bounds, not font baselines.
def fit_height(o,pixels):
    bpy.context.view_layer.update();h=max(v[1] for v in o.bound_box)-min(v[1] for v in o.bound_box);o.data.size*=pixels*unit/h;bpy.context.view_layer.update()
def value_group(value,center,material):
    parent=empty('Result '+value);parent.parent=cam
    digit=text('Value '+value,value,1,material,parent,heavy);fit_height(digit,145)
    ms=text('Unit '+value,'ms',1,material,parent,font);fit_height(ms,55)
    dw=max(v[0] for v in digit.bound_box)-min(v[0] for v in digit.bound_box);uw=max(v[0] for v in ms.bound_box)-min(v[0] for v in ms.bound_box)
    gap=16*unit;digit.location.x=-(dw+uw+gap)/2+dw/2;ms.location.x=-(dw+uw+gap)/2+dw+gap+uw/2
    bpy.context.view_layer.update();lo=min(v[1] for v in digit.bound_box);hi=max(v[1] for v in digit.bound_box);mid=(lo+hi)/2
    digit.location.y=-mid;ms.location.y=-mid
    parent.location=pixel(center,490);return parent
value_group('4.36',605,coral);value_group('0.35',1740,mint)
ratio=text('Speedup','12.5× faster',1,mint,cam,heavy);fit_height(ratio,136);bpy.context.view_layer.update()
ratio.scale.x=.92
mid=(min(v[1] for v in ratio.bound_box)+max(v[1] for v in ratio.bound_box))/2;ratio.location=pixel(1180,775)-Vector((0,mid,0))
def tube(name,coords,r):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r*unit;d.bevel_resolution=6;d.use_fill_caps=True
    sp=d.splines.new('BEZIER');sp.bezier_points.add(len(coords)-1)
    for p,co in zip(sp.bezier_points,coords):p.co=pixel(*co);p.handle_left_type='VECTOR';p.handle_right_type='VECTOR'
    o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.parent=cam;o.data.materials.append(cream);return o
tube('Sculpted clay arrow shaft',[(979,490,-6.95),(1385,490,-6.95)],14)
tube('Sculpted clay arrow head',[(1320,445,-6.95),(1385,490,-6.95),(1320,535,-6.95)],14)
for x,y in [(979,490),(1320,445),(1385,490),(1320,535)]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=14*unit);o=bpy.context.object;o.name='Rounded arrow end';o.parent=cam;o.location=pixel(x,y,-6.95);o.data.materials.append(cream)
    for poly in o.data.polygons:poly.use_smooth=True
# Fuse the shaft, chevron and end caps into one soft continuous piece of clay.
bpy.ops.object.select_all(action='DESELECT')
arrow_parts=[o for o in s.objects if o.name.startswith(('Sculpted clay arrow','Rounded arrow end'))]
for o in arrow_parts:o.select_set(True)
bpy.context.view_layer.objects.active=arrow_parts[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join()
arrow=bpy.context.object;arrow.name='One sculpted ivory clay arrow'
remesh=arrow.modifiers.new('Fuse clay joints','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.0025;remesh.use_smooth_shade=True
smooth=arrow.modifiers.new('Soft hand-shaped transitions','SMOOTH');smooth.factor=.65;smooth.iterations=3
ar=area('Arrow softbox',(0,0,0),(0,0,-1),120,2,(1,.94,.84));ar.parent=cam;ar.location=(-.3,2.4,-4.7);ar.rotation_euler=(Vector((0,1.24,-7))-ar.location).to_track_quat('-Z','Y').to_euler()
s['README']='Single native Cycles still rebuilt from scratch to match the chosen Retro Sunset clay hero reference. No animation rendering. Monolithic sculpted gold shells, recessed amber faces, open navy cradles and 45 retained cobalt cards, soft physical lights and camera-mapped warm ground.'
s.frame_start=s.frame_end=1
s.render.filepath=str(OUT/('preview.png' if args.preview else 'retro-sunset-clay-still.png'))
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.region_3d.view_perspective='CAMERA'
            a.spaces.active.overlay.show_overlays=False
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'retro-sunset-clay-still.blend'))
bpy.ops.render.render(write_still=True)
report={'resolution':[s.render.resolution_x*s.render.resolution_percentage//100,s.render.resolution_y*s.render.resolution_percentage//100],'samples':s.cycles.samples,'frames':[s.frame_start,s.frame_end],'fonts_packed':all(f.packed_file is not None for f in (font,bold,heavy)),'history_labels':sum(o.type=='FONT' and o.data.body=='history' for o in s.objects),'score_labels':sum(o.type=='FONT' and o.data.body=='score' for o in s.objects),'renderer':'Cycles','devices':devices if 'devices' in globals() else [],'history_cards':sum('• card ' in o.name for o in s.objects),'gold_bounds':[group_bounds(g) for g in score_groups],'history_bounds':[group_bounds(g) for g in history_groups]}
(WORK/'scene-check.json').write_text(json.dumps(report,indent=2));print('STILL_DONE',json.dumps(report),flush=True)
