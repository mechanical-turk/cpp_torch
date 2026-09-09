import bpy, json, re
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t')
OUT=ROOT/'outputs/short-06-blender-motion'
s=bpy.context.scene; cam=s.camera; hud=bpy.data.collections['03 • Code and timings']
assert (s.render.resolution_x,s.render.resolution_y)==(2360,2352)
W,H=2360,2352
vf=cam.data.view_frame(scene=s)
viewh=max(v.y for v in vf)-min(v.y for v in vf)
unit=viewh/H
s.frame_set(1)
origin=Vector((0,0,0)); old=world_to_camera_view(s,cam,origin)
cam.data.shift_y+=.01
trial=world_to_camera_view(s,cam,origin)
cam.data.shift_y-=.01
cam.data.shift_y+=(-200/H)/(trial.y-old.y)*.01
new=world_to_camera_view(s,cam,origin)
assert abs((old.y-new.y)*H-200)<.01

def keys(o,attr,values):
    for f,v in values:
        setattr(o,attr,v);o.keyframe_insert(data_path=attr,frame=f)
    if o.animation_data and o.animation_data.action:
        for slot in o.animation_data.action.slots:
            for layer in o.animation_data.action.layers:
                for strip in layer.strips:
                    bag=strip.channelbag(slot)
                    if bag:
                        for fc in bag.fcurves:
                            for k in fc.keyframe_points:
                                if fc.data_path not in {'hide_render','hide_viewport'}:
                                    k.interpolation='BEZIER';k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'
def visible(o,start,end):
    for f,v in [(0,True),(start,False),(end+1,True)]:
        o.hide_render=v;o.keyframe_insert(data_path='hide_render',frame=f)
        o.hide_viewport=v;o.keyframe_insert(data_path='hide_viewport',frame=f)
def emit(name,rgb):
    m=bpy.data.materials.new(name);m.use_nodes=True
    n=m.node_tree.nodes;n.clear();o=n.new('ShaderNodeOutputMaterial');e=n.new('ShaderNodeEmission')
    e.inputs['Color'].default_value=(*rgb,1);e.inputs['Strength'].default_value=1
    m.node_tree.links.new(e.outputs[0],o.inputs['Surface']);return m
coral=emit('Motion • warm coral',(.98,.22,.12))
mint=emit('Motion • electric mint',(.12,.98,.68))
ivory=bpy.data.materials['Type • ivory']
keyword=bpy.data.materials['Syntax • keyword'];typ=bpy.data.materials['Syntax • type']
number=bpy.data.materials['Syntax • number']

before=s.objects['Code • before'];after=s.objects['Code • after']
base=before.location.copy();mono=before.data.font;size=before.data.size
old_lines=before.data.body.splitlines();new_lines=after.data.body.splitlines()
dummy=before.copy();dummy.data=before.data.copy();hud.objects.link(dummy)
dummy.animation_data_clear();dummy.data.body=old_lines[-1];bpy.context.view_layer.update()
gap=(min(v[1] for v in dummy.bound_box)-min(v[1] for v in before.bound_box))/6
bpy.data.objects.remove(dummy,do_unlink=True)
assert .6<gap<1.1,gap
for o in list(s.objects):
    if o.name.startswith(('Code •','Timing •')):bpy.data.objects.remove(o,do_unlink=True)

def font_obj(name,body,loc,font,fontsize,material,align='LEFT'):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.font=font;d.size=fontsize;d.align_x=align;d.resolution_u=8
    o=bpy.data.objects.new(name,d);hud.objects.link(o);o.parent=cam;o.location=loc;d.materials.append(material);return o
def row(name,body,i,start,end):
    o=font_obj(name,body,(base.x,base.y-i*gap,base.z),mono,size,ivory)
    for m in (keyword,typ,number):o.data.materials.append(m)
    for match in re.finditer(r'\b(struct|for|int|Player|SplitPlayers|array|vector|\d+)\b',body):
        word=match.group();j=1 if word in {'struct','for'} else 3 if word.isdigit() else 2
        for k in range(match.start(),match.end()):o.data.body_format[k].material_index=j
    visible(o,start,end);return o
def curve(name,pts,material,r=3):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r*unit;d.bevel_resolution=3
    sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts):p.co=(*co,1)
    o=bpy.data.objects.new(name,d);hud.objects.link(o);o.parent=cam;d.materials.append(material);return o
changed={0:0,1:3,2:6,6:11}
for i,(a,b) in enumerate(zip(old_lines,new_lines)):
    if not a:continue
    if i not in changed:
        row(f'Code • unchanged {i}',a,i,1,288)
    else:
        delay=changed[i];f=159+delay
        oldrow=row(f'Code • outgoing {i}',a,i,1,f+8)
        loc=oldrow.location.copy()
        keys(oldrow,'location',[(1,loc),(f,loc),(f+8,loc+Vector((-38*unit,0,0)))])
        keys(oldrow,'scale',[(1,(1,1,1)),(f,(1,1,1)),(f+8,(1,.015,1))])
        newrow=row(f'Code • incoming {i}',b,i,f+9,288);loc=newrow.location.copy()
        keys(newrow,'location',[(f+9,loc+Vector((65*unit,0,0))),(f+21,loc)])
        keys(newrow,'scale',[(f+9,(1,.015,1)),(f+17,(1,1.10,1)),(f+24,(1,1,1))])
        # A brief underline identifies only the changed line, then clears.
        bpy.context.view_layer.update()
        right=max(v[0] for v in newrow.bound_box)
        line=curve(f'Code • change underline {i}',[(base.x,loc.y-15*unit,base.z+.025),(base.x+right,loc.y-15*unit,base.z+.025)],mint,2)
        visible(line,f+10,217)
        keys(line.data,'bevel_factor_end',[(f+10,0),(f+24,1),(211,1),(217,0)])
    endrow=row(f'Code • final {i}',b,i,361,456)
    loc=endrow.location.copy()
    keys(endrow,'location',[(361,loc+Vector((0,-15*unit,0))),(370,loc)])

# Pixel positions refer to the new composition, including the requested shift.
frame=cam.data.view_frame(scene=s);xmin=min(v.x for v in frame);ymax=max(v.y for v in frame)
def px(x,y,z=-8):return Vector((xmin+x*unit,ymax-y*unit,z))
display=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Black.ttf')
regular=bpy.data.fonts.load('/System/Library/Fonts/HelveticaNeue.ttc')
def center_object(o,x,y):
    bpy.context.view_layer.update()
    lo=Vector((min(v[0] for v in o.bound_box),min(v[1] for v in o.bound_box),0))
    hi=Vector((max(v[0] for v in o.bound_box),max(v[1] for v in o.bound_box),0))
    center=(lo+hi)/2;o.location=px(x,y)-Vector((center.x,center.y,0))
    return o
def result_group(name,value,x,mat,start):
    parent=bpy.data.objects.new(name+' • motion',None);hud.objects.link(parent);parent.parent=cam
    digit=font_obj(name+' • value',value,(0,0,0),display,1.50,mat)
    unittext=font_obj(name+' • unit','ms',(0,0,0),regular,.70,mat)
    bpy.context.view_layer.update()
    dw=max(v[0] for v in digit.bound_box)-min(v[0] for v in digit.bound_box)
    uw=max(v[0] for v in unittext.bound_box)-min(v[0] for v in unittext.bound_box)
    digit.parent=parent;unittext.parent=parent
    digit.location=(-.5*(dw+uw+20*unit),0,0)
    unittext.location=(digit.location.x+dw+20*unit,0,0)
    bpy.context.view_layer.update()
    bounds=[Vector(v)+o.location for o in [digit,unittext] for v in o.bound_box]
    midy=(min(v.y for v in bounds)+max(v.y for v in bounds))/2
    parent.location=px(x,510)-Vector((0,midy,0))
    # Parent pivot is the optical center, so entry scaling preserves alignment.
    digit.location.y-=midy;unittext.location.y-=midy;parent.location=px(x,510)
    for o in [digit,unittext]:visible(o,start,360)
    loc=parent.location.copy()
    keys(parent,'scale',[(start,(.86,.86,1)),(start+8,(1.055,1.055,1)),(start+14,(1,1,1))])
    keys(parent,'location',[(start,loc+Vector((0,-18*unit,0))),(start+10,loc)])
    return parent,digit,unittext
left=result_group('Timing • before','4.36',715,coral,289)
right=result_group('Timing • after','0.35',1660,mint,305)
arrow=curve('Timing • drawing arrow',[px(1030,510,-7.95),px(1310,510,-7.95)],ivory,4)
visible(arrow,294,360);keys(arrow.data,'bevel_factor_end',[(294,0),(305,1)])
head=curve('Timing • arrowhead',[px(1279,487,-7.95),px(1310,510,-7.95),px(1279,533,-7.95)],mint,4)
visible(head,303,360);keys(head.data,'bevel_factor_end',[(303,0),(308,1)])
spark=curve('Timing • traveling accent',[(-15*unit,0,0),(15*unit,0,0)],mint,6)
visible(spark,295,307);keys(spark,'location',[(295,px(1030,510,-7.94)),(306,px(1310,510,-7.94))])
keys(spark,'scale',[(295,(.1,.1,1)),(299,(1,1,1)),(307,(.02,.02,1))])
ratio=font_obj('Timing • ratio','12.5× faster',(0,0,-8),display,1.50,mint,'CENTER')
center_object(ratio,1180,820);visible(ratio,314,360);loc=ratio.location.copy()
keys(ratio,'location',[(314,loc+Vector((0,-26*unit,0))),(325,loc)])
keys(ratio,'scale',[(314,(.92,.92,1)),(322,(1.025,1.025,1)),(329,(1,1,1))])

# Verify all visible foreground remains inside the canvas and partition.
all_bounds=[W,H,0,0];hud_bounds=[W,H,0,0];model_bounds=[W,H,0,0]
states={}; offenders=[]
for f in range(1,457):
    s.frame_set(f)
    states[f]=[]
    for o in s.objects:
        if o.hide_render:continue
        states[f].append((o.name,tuple(round(x,6) for row in o.matrix_world for x in row),round(getattr(o.data,'bevel_factor_end',1),6)))
        if o.type not in {'FONT','MESH','CURVE'}:continue
        if o.type=='CURVE' and o.data.bevel_factor_end<.001:continue
        if o not in hud.objects.values() and o not in bpy.data.collections['01 • Player assemblies'].objects.values():continue
        b=hud_bounds if o in hud.objects.values() else model_bounds
        for corner in o.bound_box:
            p=world_to_camera_view(s,cam,o.matrix_world@Vector(corner));x=p.x*W;y=(1-p.y)*H

            if b is hud_bounds and y>1090:offenders.append((f,o.name,x,y))
            b[0]=min(b[0],x);b[1]=min(b[1],y);b[2]=max(b[2],x);b[3]=max(b[3],y)
            all_bounds[0]=min(all_bounds[0],x);all_bounds[1]=min(all_bounds[1],y);all_bounds[2]=max(all_bounds[2],x);all_bounds[3]=max(all_bounds[3],y)
assert all_bounds[0]>100 and all_bounds[2]<W-100 and all_bounds[1]>200 and all_bounds[3]<H-100,all_bounds
assert hud_bounds[3]<1100 and model_bounds[1]>1100,(hud_bounds,model_bounds)
mapping={};seen={}
for f,state in states.items():
    key=repr(state)
    mapping[f]=seen.setdefault(key,f)
s.frame_set(340)
centers=[]
for group in [left,right]:
    ys=[]
    for o in group[1:]:
        ys.extend((1-world_to_camera_view(s,cam,o.matrix_world@Vector(v)).y)*H for v in o.bound_box)
    centers.append((min(ys)+max(ys))/2)
assert max(abs(y-510) for y in centers)<.01,centers
report={'resolution':[W,H],'content_shift_down_px':200,'camera_shift_y':cam.data.shift_y,'foreground_bounds_px':all_bounds,'hud_bounds_px':hud_bounds,'model_bounds_px':model_bounds,'timing_text_optical_centers_y_px':centers,'arrow_center_y_px':510,'history_plates':sum('• plate ' in o.name for o in s.objects),'duration_seconds':19,'fps':24,'frames':456,'distinct_scene_frames':len(set(mapping.values())),'frame_map':mapping,'upper_render_region_height_px':1100,'platform_composer_verified':False}
(OUT/'scene-verification.json').write_text(json.dumps(report,indent=2))
s['README']='2360x2352. All content shifted down 200px. Staggered code-line replacement, brief change underlines, optically aligned kinetic coral/mint timing comparison. Models and benchmark unchanged. 24fps, 19 seconds, silent.'
for name in ['About this scene','Wide camera checks']:
    if bpy.data.texts.get(name):bpy.data.texts.remove(bpy.data.texts[name])
t=bpy.data.texts.new('About this scene');t.write(s['README'])
s.render.use_border=False;s.render.resolution_percentage=100
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'cpp-data-layout-motion.blend'))
for f in [1,178,340]:
    s.frame_set(f);s.render.filepath=str(ROOT/f'work/short-06-blender-motion/check-{f}.png');bpy.ops.render.render(write_still=True)
print('REVISION_OK',json.dumps({k:v for k,v in report.items() if k!='frame_map'}),flush=True)
