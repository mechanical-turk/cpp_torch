import bpy, math, re, json, hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t');O=R/'outputs/clay-animation-v2';W=R/'work/clay-animation-v2'
bpy.ops.wm.open_mainfile(filepath=str(R/'outputs/clay-studio-lighting/retro-sunset-clay-studio.blend'))
s=bpy.context.scene;cam=s.camera;unit=(7*36/80)/2360
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.kernel_optimization_level='OFF';prefs.metalrt='OFF';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.render.use_persistent_data=True;s.render.fps=24;s.render.fps_base=1;s.frame_start=1;s.frame_end=360
s.cycles.samples=96;s.cycles.adaptive_threshold=.012;s.cycles.filter_width=1;s.cycles.use_denoising=True;s.render.image_settings.compression=15

def collection(name):c=bpy.data.collections.new(name);s.collection.children.link(c);return c
MODEL=collection('01 • Clay models');HUD=collection('02 • Code and results');STAGE=collection('03 • Studio')
def move(o,c):
    for old in list(o.users_collection):old.objects.unlink(o)
    c.objects.link(o)
scores=[s.objects[f'Score {v} assembly'] for v in [7,2,9]];histories=[s.objects[f'History {i} assembly'] for i in range(3)]
for o in list(s.objects):
    if o in scores+histories or o.parent in scores+histories:move(o,MODEL)
    elif o.type=='LIGHT' or o==cam or o.name=='Continuous clay studio ground':move(o,STAGE)
    else:move(o,HUD)
def keys(o,prop,values):
    for f,v in values:setattr(o,prop,v);o.keyframe_insert(data_path=prop,frame=f)
    if getattr(o,'animation_data',None) and o.animation_data.action:
        for slot in o.animation_data.action.slots:
            for layer in o.animation_data.action.layers:
                for strip in layer.strips:
                    bag=strip.channelbag(slot)
                    if bag:
                        for fc in bag.fcurves:
                            for k in fc.keyframe_points:
                                if fc.data_path not in ['hide_render','hide_viewport']:
                                    k.interpolation='BEZIER';k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'
def visible(o,start,end):
    keys(o,'hide_render',[(0,True),(start,False),(end+1,True)])
    keys(o,'hide_viewport',[(0,True),(start,False),(end+1,True)])
def bounds(group):
    vs=[world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for o in group.children for v in o.bound_box if o.type in ['FONT','MESH','CURVE']]
    return [min(v.x for v in vs)*2360,min(1-v.y for v in vs)*2352,max(v.x for v in vs)*2360,max(1-v.y for v in vs)*2352]
def fit(g,cx,bottom,width):
    for _ in range(6):
        bpy.context.view_layer.update();b=bounds(g);g.scale*=width/(b[2]-b[0]);bpy.context.view_layer.update();b=bounds(g)
        dx=cx-(b[0]+b[2])/2;dy=bottom-b[3]
        g.location.x+=.1;bpy.context.view_layer.update();bx=bounds(g);g.location.x-=.1
        g.location.y+=.1;bpy.context.view_layer.update();by=bounds(g);g.location.y-=.1
        g.location.x+=dx/(((bx[0]+bx[2])-(b[0]+b[2]))/.2);g.location.y+=dy/((by[3]-b[3])/.1)
    bpy.context.view_layer.update()
# Duplicate the complete center assemblies, including their local sculpture.
# Every peer shares geometry, local transforms, deformation and scale animation.
def duplicate_family(groups, master, names, is_score):
    for g in groups:
        if g==master:continue
        for child in list(g.children):bpy.data.objects.remove(child,do_unlink=True)
        bpy.data.objects.remove(g,do_unlink=True)
    for child in master.children:
        for mod in child.modifiers:
            if mod.type=='DISPLACE':mod.texture_coords='LOCAL'
    master.location.x=0
    result=[]
    for i,name in enumerate(names):
        if name==master.name:g=master
        else:
            g=master.copy();MODEL.objects.link(g);g.name=name
            for child in master.children:
                o=child.copy();o.data=child.data;MODEL.objects.link(o);o.parent=g
                if is_score:
                    value=[7,2,9][i]
                    if child.type=='FONT' and child.data.body=='2':
                        o.data=child.data.copy();o.data.body=str(value);o.name=f'Score {value} numeral'
                    elif child.type=='FONT':o.name=f'Score {value} label'
                    else:o.name=child.name.rsplit(' ',1)[0]+f' {value}'
                else:
                    if child.type=='FONT':o.name=f'History {i} label'
                    elif 'card' in child.name:o.name=f'History {i} • card '+child.name.rsplit(' ',1)[-1]
                    else:o.name=child.name.rsplit(' ',1)[0]+f' {i}'
        result.append(g)
    return result
scores=duplicate_family(scores,scores[1],[f'Score {v} assembly' for v in [7,2,9]],True)
histories=duplicate_family(histories,histories[1],[f'History {i} assembly' for i in range(3)],False)

def screen_x_at(g,cx):
    # Position roots on a common world-space row; never resize peers to fit independently.
    bpy.context.view_layer.update()
    p=world_to_camera_view(s,cam,g.matrix_world.translation)
    g.location.x+=.1;bpy.context.view_layer.update()
    q=world_to_camera_view(s,cam,g.matrix_world.translation)
    g.location.x-=.1
    return g.location.x+(cx-p.x*2360)/((q.x-p.x)*2360/.1)

final={}
for family,width,offsets in [(scores,405,[-416,0,416]),(histories,525,[-536,0,536])]:
    master=family[1];master.location.x=0;bpy.context.view_layer.update()
    # One scale and y-position from the canonical model for the entire row.
    scale=master.scale.copy();end=master.location.copy()
    for g,dx in zip(family,offsets):
        g.location=end;g.scale=scale;g.location.x=screen_x_at(g,1180+dx)
        final[g.name]=(g.location.copy(),scale.copy())

# Fit only the master at the optical center. Reuse that exact scale and depth.
for family,width in [(scores,270),(histories,345)]:
    master=family[1];fit(master,1180,1710,width)
    small=master.scale.copy();row_loc=master.location.copy()
    for i,g in enumerate(family):
        g.scale=small;g.location=row_loc
        g.location.x=screen_x_at(g,(393+610*i) if family is scores else (711+610*i))
        start=g.location.copy();end,scale=final[g.name]
        if family is scores:
            keys(g,'location',[(1,start),(166,start),(185,start+Vector((0,-.25,1.55))),(213,end+Vector((0,0,1.55))),(230,end),(235,end+Vector((0,0,.07))),(242,end),(360,end)])
            keys(g,'scale',[(1,small),(159,small),(166,Vector((small.x,small.y,small.z*.97))),(185,small),(213,scale),(230,Vector((scale.x,scale.y,scale.z*.97))),(238,scale),(360,scale)])
        else:
            keys(g,'location',[(1,start),(185,start),(242,end),(360,end)])
            keys(g,'scale',[(1,small),(185,small),(242,scale),(360,scale)])
# Keep the approved result exactly at its final position and scale.
for name,start in [('Result 4.36',289),('Result 0.35',305)]:
    g=s.objects[name];loc=g.location.copy();sc=g.scale.copy()
    for o in g.children:visible(o,start,360)
    keys(g,'location',[(start,loc+Vector((0,-18*unit,0))),(start+10,loc)])
    keys(g,'scale',[(start,sc*.86),(start+8,sc*1.035),(start+14,sc)])
arrow=s.objects['Clean sculpted ivory arrow'];visible(arrow,294,360)
# A material reveal draws the clean solid without bending or rebuilding its geometry.
m=arrow.data.materials[0].copy();m.name='Clay arrow • reveal';arrow.data.materials[0]=m;n=m.node_tree.nodes;l=m.node_tree.links
out=next(n for n in n if n.type=='OUTPUT_MATERIAL');shader=out.inputs['Surface'].links[0].from_socket
coord=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(coord.outputs['Object'],sep.inputs[0])
reveal=n.new('ShaderNodeValue');reveal.name='Draw progress';keys(reveal.outputs[0],'default_value',[(294,-.02),(308,1.02)])
mask=n.new('ShaderNodeMath');mask.operation='GREATER_THAN';remap=n.new('ShaderNodeMapRange');remap.inputs['From Min'].default_value=-209*unit;remap.inputs['From Max'].default_value=211*unit;remap.clamp=False;l.new(sep.outputs['X'],remap.inputs['Value']);l.new(remap.outputs['Result'],mask.inputs[0]);l.new(reveal.outputs[0],mask.inputs[1])
trans=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');l.new(mask.outputs[0],mix.inputs[0]);l.new(shader,mix.inputs[1]);l.new(trans.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
ratio=s.objects['Speedup'];loc=ratio.location.copy();sc=ratio.scale.copy();visible(ratio,314,360)
keys(ratio,'location',[(314,loc+Vector((0,-26*unit,0))),(325,loc)]);keys(ratio,'scale',[(314,sc*.92),(322,sc*1.025),(329,sc)])

def lin(h):
    a=[int(h[i:i+2],16)/255 for i in (0,2,4)];return tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in a)
def paint(name,h):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*lin(h),1);o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);return m
white=paint('Code • ivory','FFF0D5');keyword=paint('Code • lilac','DCAEF1');typ=paint('Code • aqua','84E3D4');number=paint('Code • amber','F3C56B');mint=bpy.data.materials['Mint timing'];mono=bpy.data.fonts.load('/System/Library/Fonts/Menlo.ttc')
def px(x,y,z=-7):return Vector(((x-1180)*unit,(1176-y)*unit,z))
def row(name,body,i,start,end):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.font=mono;d.size=105*unit;d.resolution_u=12
    for m in [white,keyword,typ,number]:d.materials.append(m)
    for match in re.finditer(r'\b(struct|for|int|Player|SplitPlayers|array|vector|\d+)\b',body):
        word=match.group();j=1 if word in ['struct','for'] else 3 if word.isdigit() else 2
        for k in range(match.start(),match.end()):d.body_format[k].material_index=j
    o=bpy.data.objects.new(name,d);HUD.objects.link(o);o.parent=cam;o.location=px(285,415+i*107-(37 if i>=5 else 0));visible(o,start,end);return o
old='struct Player {\n  int score;\n  array<int, 15> history;\n};\n\nfor (int id : ids)\n  total += players[id].score;'.splitlines()
new='struct SplitPlayers {\n  vector<int> scores;\n  vector<array<int, 15>> histories;\n};\n\nfor (int id : ids)\n  total += scores[id];'.splitlines()
changed={0:0,1:3,2:6,6:11}
for i,(a,b) in enumerate(zip(old,new)):
    if not a:continue
    if i not in changed:row(f'Code • unchanged {i}',a,i,1,288)
    else:
        f=159+changed[i];o=row(f'Code • outgoing {i}',a,i,1,f+8);loc=o.location.copy()
        keys(o,'location',[(1,loc),(f,loc),(f+8,loc+Vector((-38*unit,0,0)))]);keys(o,'scale',[(1,(1,1,1)),(f,(1,1,1)),(f+8,(1,.015,1))])
        o=row(f'Code • incoming {i}',b,i,f+9,288);loc=o.location.copy()
        keys(o,'location',[(f+9,loc+Vector((65*unit,0,0))),(f+21,loc)]);keys(o,'scale',[(f+9,(1,.015,1)),(f+17,(1,1.10,1)),(f+24,(1,1,1))])
        bpy.context.view_layer.update();right=max(v[0] for v in o.bound_box)
        d=bpy.data.curves.new(f'Code underline {i}','CURVE');d.dimensions='3D';d.bevel_depth=2*unit;d.bevel_resolution=3;sp=d.splines.new('POLY');sp.points.add(1)
        for q,co in zip(sp.points,[(0,-15*unit,0),(right,-15*unit,0)]):q.co=(*co,1)
        u=bpy.data.objects.new(f'Code • underline {i}',d);HUD.objects.link(u);u.parent=cam;u.location=loc+Vector((0,0,.01));d.materials.append(mint);visible(u,f+10,217)
        keys(d,'bevel_factor_end',[(f+10,0),(f+24,1),(211,1),(217,0)])
# Move the orange material highlight exactly 100 image pixels lower.
# Preserve the studio lights and geometry; translate the gradient's center on the ground.
bpy.context.view_layer.update()
rot=cam.matrix_world.to_3x3();floor=s.objects['Continuous clay studio ground']
zlocal=(floor.location.z-cam.location.z-rot[2][0]*(-.3)-rot[2][1]*(-3.4))/rot[2][2]
old_world=cam.matrix_world@Vector((-.3,-3.4,zlocal))
p=world_to_camera_view(s,cam,old_world);old_center=(p.x*2360,(1-p.y)*2352)
target_y=old_center[1]+100
ray=rot@Vector(((old_center[0]-1180)/2360*(36/80),(1176-target_y)/2360*(36/80),-1))
hit=cam.location+ray*((floor.location.z-cam.location.z)/ray.z)
local_center=cam.matrix_world.inverted()@hit
for node in floor.data.materials[0].node_tree.nodes:
    if node.type=='MATH' and node.operation=='ADD':
        if abs(node.inputs[1].default_value-3.4)<1e-5:node.inputs[1].default_value=-local_center.y
        elif abs(node.inputs[1].default_value-.3)<1e-5:node.inputs[1].default_value=-local_center.x
gradient_centers={'before':old_center,'after':(old_center[0],target_y)}

# Audit every frame and cache only truly identical rendered states.
low=[2360,2352,0,0];high=[2360,2352,0,0];maps={'lower':{},'upper':{}};seen={'lower':{},'upper':{}}
for f in range(1,361):
    s.frame_set(f)
    for tag,coll,bb in [('lower',MODEL,low),('upper',HUD,high)]:
        state=[]
        for o in coll.objects:
            if o.type not in ['FONT','CURVE','MESH'] or o.hide_render:continue
            if o.type=='CURVE' and getattr(o.data,'bevel_factor_end',1)<.001:continue
            state.append((o.name,tuple(round(v,7) for row_ in o.matrix_world for v in row_),round(getattr(o.data,'bevel_factor_end',1),7)))
            for corner in o.bound_box:
                p=world_to_camera_view(s,cam,o.matrix_world@Vector(corner));x=p.x*2360;y=(1-p.y)*2352
                bb[0]=min(bb[0],x);bb[1]=min(bb[1],y);bb[2]=max(bb[2],x);bb[3]=max(bb[3],y)
        if tag=='upper' and not arrow.hide_render:state.append(('reveal',round(reveal.outputs[0].default_value,7)))
        key=hashlib.sha256(repr(state).encode()).hexdigest();maps[tag][f]=seen[tag].setdefault(key,f)
assert low[1]>1050 and high[3]<1050,(low,high)
assert min(low[0],high[0])>150 and max(low[2],high[2])<2210 and high[1]>200 and low[3]<2230,(low,high)
s.frame_set(340)
for g in scores+histories:
    a,b=final[g.name];assert (g.location-a).length<1e-6 and (g.scale-b).length<1e-6
report={'resolution':[2360,2352],'fps':24,'frames':360,'duration':15,'partition_y':1050,'model_bounds':low,'hud_bounds':high,'history_cards':45,'model_unique_frames':len(seen['lower']),'hud_unique_frames':len(seen['upper']),'frame_maps':maps,'canonical_duplicates':True,'code_font_multiplier':1.5,'code_origin_px':[285,415],'code_line_step_px':107,'code_blank_gap_reduction_px':37,'tail_removed':True,'gradient_highlight_shift_px':100}

consistency=[]
for f in range(1,361):
    s.frame_set(f)
    for family in [scores,histories]:
        reference=family[1]
        assert all((g.scale-reference.scale).length<1e-7 for g in family),(f,'scale',family)
        assert all(abs(g.location.y-reference.location.y)<1e-7 and abs(g.location.z-reference.location.z)<1e-7 for g in family),(f,'depth',family)
for family in [scores,histories]:
    meshsets=[{o.data.name for o in g.children if o.type=='MESH'} for g in family]
    assert meshsets[0]==meshsets[1]==meshsets[2]
    consistency.append({'family':'scores' if family is scores else 'histories','shared_meshes':sorted(meshsets[0]),'shared_scale_all_frames':True,'shared_depth_all_frames':True})
report['uniformity']=consistency
report['gradient_centers_px']=gradient_centers
assert len([o for o in MODEL.objects if '• card ' in o.name])==45
assert len([o for o in MODEL.objects if o.type=='FONT' and o.data.body=='score'])==3
assert len([o for o in MODEL.objects if o.type=='FONT' and o.data.body=='history'])==3

(O/'scene-verification.json').write_text(json.dumps(report,indent=2));print('ANIMATION_AUDIT',json.dumps({k:v for k,v in report.items() if k!='frame_maps'}),flush=True)
for marker in list(s.timeline_markers):s.timeline_markers.remove(marker)
for f,name in [(1,'Struct layout'),(159,'Code transforms'),(166,'Scores lift'),(213,'Scores gather'),(242,'Separate arrays'),(289,'Benchmark result')]:s.timeline_markers.new(name,frame=f)
s['README']='Approved Retro Sunset studio clay scene animated at 24 fps, 15 seconds. Same studio materials, lights and camera. All score and history assemblies are canonical linked duplicates with common scale animation. Code font is 1.5 times the prior size. Ends on the benchmark; no return to code. Code transforms visibly; all scores gather; 45 history cards remain; clean arrow reveals through its material. No narration or caption overlays.'
s.render.resolution_percentage=100;s.frame_set(1);s.render.filepath=str(W/'frames/frame_');bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'cpp-data-layout-clay-animation.blend'))
s.render.resolution_percentage=50;s.cycles.samples=24
for f in [1,202,340]:
    s.frame_set(f);s.render.filepath=str(W/f'check-{f}.png');bpy.ops.render.render(write_still=True);print('CHECK_DONE',f,flush=True)
